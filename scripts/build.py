"""Build Project Horizon from manifests/lock.json.

  python scripts/build.py mrpack                 -> dist/ProjectHorizon-<ver>.mrpack
  python scripts/build.py instance [--groups a,b] [--name N]
        -> a Prism instance in %APPDATA%/PrismLauncher/instances/<N> (dev/testing).
           --groups limits mods to roster groups (+ their deps) for staged testing.

Overrides (config, defaultconfigs, kubejs, datapacks, shaderpacks options, profiles)
are copied from the repo into the pack/instance. Third-party jars are never
redistributed: the .mrpack only references Modrinth CDN URLs with hashes.
"""
import hashlib, json, os, shutil, sys, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix \?\ - the repo may live deep on disk
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
VERSION = (ROOT / "VERSION").read_text().strip()
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
UA = {"User-Agent": "project-horizon-builder/0.1"}
# repo dir -> path inside .minecraft
OVERRIDES = {"config": "config", "defaultconfigs": "defaultconfigs", "kubejs": "kubejs",
             "datapacks": "kubejs/data", "resourcepacks": "resourcepacks",
             "shaderpacks": "shaderpacks", "profiles": "horizon-profiles", "options": ".",
             "schematics": "schematics"}   # schematics: optional headquarters plans (Create reads .minecraft/schematics)


def lock():
    return json.loads((ROOT / "manifests/lock.json").read_text())


VARIANTS = {None: {"suffix": "", "name": "Project Horizon", "note": ""},
            "lab": {"suffix": "-lab", "name": "Project Horizon (lab)", "note": " Untested ports."},
            "depths": {"suffix": "-depths", "name": "Project Horizon: Depths",
                       "note": " NEW WORLDS ONLY: Infinity Cave merged into Horizon terrain, overworld floor at Y -128."}}


def ports(variant=None):
    """Locally built jars (ports/, scripts/build_ports.py). Shipped inside the pack because their
    licenses permit redistribution; see docs/PORTS.md. A port with a 'variant' ships only in that variant."""
    f = ROOT / "manifests/ports_lock.json"
    out = []
    for p in (json.loads(f.read_text())["ports"] if f.exists() else []):
        jar = ROOT / "ports/dist" / p["file"]
        if hashlib.sha512(jar.read_bytes()).hexdigest() != p["hashes"]["sha512"]:
            raise SystemExit(f"port {p['name']}: ports/dist/{p['file']} does not match ports_lock.json - run scripts/build_ports.py")
        if p.get("variant") in (None, variant):
            out.append(dict(p, path=jar))
    return out


def select(mods, groups):
    if not groups:
        return mods
    by_id = {m["project_id"]: m for m in mods}
    keep = {m["project_id"] for m in mods if m["group"] in groups}
    changed = True
    while changed:
        changed = False
        for pid in list(keep):
            for d in by_id[pid]["deps"]:
                if d["type"] == "required" and d["project_id"] in by_id and d["project_id"] not in keep:
                    keep.add(d["project_id"]); changed = True
    return [m for m in mods if m["project_id"] in keep]


def fetch(item):
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / item["file"]
    if dest.exists() and hashlib.sha512(dest.read_bytes()).hexdigest() == item["hashes"]["sha512"]:
        return dest
    with urllib.request.urlopen(urllib.request.Request(item["url"], headers=UA), timeout=120) as r:
        data = r.read()
    if hashlib.sha512(data).hexdigest() != item["hashes"]["sha512"]:
        raise SystemExit(f"hash mismatch {item['file']}")
    dest.write_bytes(data)
    return dest


MIRRORED = ["kubejs/data", "kubejs/server_scripts", "kubejs/startup_scripts", "kubejs/client_scripts", "kubejs/assets",
            "config/heracles/quests"]   # fully owned by the pack: stale files from older versions are removed


def prune_mirrored(target: Path, staged: Path):
    """Delete files under the pack-owned dirs of an existing install that the new build no longer ships
    (e.g. 0.1.0 loot modifiers). Player data (saves, options, other configs) is never touched."""
    removed = 0
    for rel in MIRRORED:
        d = target / rel
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if f.is_file() and not (staged / rel / f.relative_to(d)).exists():
                f.unlink()
                removed += 1
    return removed


# Player preference files: shipped for NEW installs, never overwritten on an existing one (0.6.0 copied options/options.txt
# over the player's file on every update). Targeted, documented changes go through migrate_options() instead.
PRESERVE_IF_PRESENT = {"options.txt", "config/iris.properties"}


def copy_overrides(target: Path, existing: bool = False):
    for src, dst in OVERRIDES.items():
        s = ROOT / src
        if not s.exists():
            continue
        for f in s.rglob("*"):
            if f.is_file() and f.name != ".gitkeep" and not f.name.startswith(".generated"):
                out = target / dst / f.relative_to(s)
                if existing and out.exists() and out.relative_to(target).as_posix() in PRESERVE_IF_PRESENT:
                    continue
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out)


def set_resourcepacks(options: Path, packs):
    """Enable the pack's resource packs in lock order (first = lowest priority) above vanilla/mod resources,
    keeping any extra packs the player enabled (they stay on top)."""
    # UTF-8 explicitly: pack names contain section signs (0.6.0 read cp1252 on Windows and duplicated them as mojibake)
    lines = options.read_text(encoding="utf-8").splitlines() if options.exists() else []
    # packs with enabled_by_default=false ship in resourcepacks/ but are left for the player to enable (unverified visuals)
    ours = ["vanilla", "mod_resources"] + [f"file/{p['file']}" for p in packs if p.get("enabled_by_default", True)] + [f"file/{n}" for n in LOCAL_PACKS]
    old = next((l for l in lines if l.startswith("resourcePacks:")), None)
    extra = []
    if old:
        try:
            extra = [x for x in json.loads(old.split(":", 1)[1]) if x not in ours and x not in KNOWN_OLD]   # incl. optional packs the player enabled
        except ValueError:
            pass
    rp = options.parent / "resourcepacks"
    if rp.is_dir():   # drop enabled file/ entries whose zip/folder no longer exists (incl. 0.6.0's mojibake duplicates)
        extra = [x for x in extra if not x.startswith("file/") or (rp / x[5:]).exists()]
    line = "resourcePacks:" + json.dumps(ours + extra, separators=(",", ":"))
    # incompatibleResourcePacks = packs the player accepted although their pack_format is newer; Minecraft silently drops
    # an enabled pack that is incompatible and not listed here. Ours: roster accept_newer_format; the player's: kept if still on.
    accepted = [f"file/{p['file']}" for p in packs if p.get("accept_newer_format") and p.get("enabled_by_default", True)]
    old_inc = next((l for l in lines if l.startswith("incompatibleResourcePacks:")), None)
    if old_inc:
        try:
            accepted += [x for x in json.loads(old_inc.split(":", 1)[1]) if x in extra and x not in accepted]
        except ValueError:
            pass
    inc = "incompatibleResourcePacks:" + json.dumps(accepted, separators=(",", ":"))
    lines = [l for l in lines if not l.startswith(("resourcePacks:", "incompatibleResourcePacks:"))] + [line, inc]
    options.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")


# file/<name> entries Horizon itself enabled or shipped at some point (pruned from the enabled list when no longer shipped;
# anything else the player added is kept). 0.6.1: FA Player Extension is shipped again (Punchy Moves removed), so it is no
# longer here; the 0.3.0 All-Extensions bundle duplicates Details/Emissive/Quivers/Objects; Fluid & Foolish was Punchy Moves'
# animation pack.
KNOWN_OLD = {"file/FA-Player-Compats-1.3.1-mc1.21.1.zip", "file/Freshly Modded 3.0.5.zip",
             "file/FA+All_Extensions-v1.10.1.zip", "file/Fluid & Foolish 1.0.1.zip"}
# files removed from resourcepacks/ on update (still on disk would let Punchy-era detection or duplicates come back)
STALE_FILES = {"Fluid & Foolish 1.0.1.zip"}


LOCAL_PACKS = ["Horizon-16x.zip"]   # built by scripts/gen_resourcepack.py into resourcepacks/; highest priority of ours


def deployed(m):
    """File name a mod is installed under. Mods flagged disabled_by_default ship as <jar>.disabled (Prism lists them
    as disabled; the player ticks them on). A copy the player already enabled is left alone."""
    return m["file"] + (".disabled" if m.get("disabled_by_default") else "")


def managed_names(mc: Path):
    """Jars Horizon itself has shipped (earlier .mrpack indexes, local ports, our own install manifest). Only these
    may be removed on update; anything else in mods/ was added by the player and is never touched."""
    names = set()
    mf = mc / "mods" / ".horizon-managed.json"
    if mf.exists():
        names |= set(json.loads(mf.read_text()))
    for pk in (ROOT / "dist").glob("ProjectHorizon-*.mrpack"):
        with zipfile.ZipFile(pk) as z:
            for f in json.loads(z.read("modrinth.index.json"))["files"]:
                if f["path"].startswith("mods/"):
                    names.add(Path(f["path"]).name.removesuffix(".disabled"))
            names |= {Path(n).name for n in z.namelist() if "/mods/" in n and n.endswith(".jar")}
    lp = ROOT / "manifests/ports_lock.json"
    if lp.exists():
        names |= {p["file"] for p in json.loads(lp.read_text())["ports"]}
    return names


def env(m):
    # Everything in the roster is part of the experience, so it is "required" on
    # every side the mod supports. Modrinth's per-project "optional" flag describes
    # client/server pairing, not pack optionality, and must not leak into the pack.
    # The client always runs an integrated server in singleplayer, so server-only
    # mods (worldgen, structures, AI libs) are REQUIRED on the client too.
    return {"client": "required",
            "server": "unsupported" if m["server_side"] == "unsupported" else "required"}


def mrpack(variant=None):
    L = lock()
    files = [{"path": f"mods/{deployed(m)}", "hashes": {"sha1": m["hashes"]["sha1"], "sha512": m["hashes"]["sha512"]},
              "env": env(m), "downloads": [m["url"]], "fileSize": m["size"]} for m in L["mods"]]
    files += [{"path": f"shaderpacks/{s['file']}", "hashes": {"sha1": s["hashes"]["sha1"], "sha512": s["hashes"]["sha512"]},
               "env": {"client": "optional" if s["slug"] != "complementary-reimagined" else "required", "server": "unsupported"},
               "downloads": [s["url"]], "fileSize": s["size"]} for s in L["shaders"]]
    files += [{"path": f"resourcepacks/{s['file']}", "hashes": {"sha1": s["hashes"]["sha1"], "sha512": s["hashes"]["sha512"]},
               "env": {"client": "required", "server": "unsupported"},
               "downloads": [s["url"]], "fileSize": s["size"]} for s in L.get("resourcepacks", [])]
    index = {"formatVersion": 1, "game": "minecraft", "versionId": VERSION + (f"+{variant}" if variant else ""),
             "name": VARIANTS[variant]["name"],
             "summary": "Exploration-first RPG + technology pack with Voxy long-distance rendering." + VARIANTS[variant]["note"],
             "files": files, "dependencies": {"minecraft": L["minecraft"], "neoforge": L["loader_version"]}}
    out = ROOT / "dist" / f"ProjectHorizon-{VERSION}{VARIANTS[variant]['suffix']}.mrpack"
    out.parent.mkdir(exist_ok=True)
    stage = CACHE.parent / "overrides"
    shutil.rmtree(stage, ignore_errors=True)
    copy_overrides(stage)
    set_resourcepacks(stage / "options.txt", L.get("resourcepacks", []))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("modrinth.index.json", json.dumps(index, indent=2))
        for f in stage.rglob("*"):
            if f.is_file():
                z.write(f, "overrides/" + f.relative_to(stage).as_posix())
        for p in ports(variant):
            root = "client-overrides" if p["side"]["server"] == "unsupported" else "overrides"
            z.write(p["path"], f"{root}/mods/{p['file']}")
    print(f"wrote {out} ({len(files)} files, {out.stat().st_size/1024:.0f} KiB)")


def instance(name, groups, variant=None):
    L = lock()
    mods = select(L["mods"], groups)
    inst = Path(os.environ["APPDATA"]) / "PrismLauncher" / "instances" / name
    mc = inst / "minecraft"
    (mc / "mods").mkdir(parents=True, exist_ok=True)
    wanted = {m["file"] for m in mods} | {p["file"] for p in ports(variant)}
    managed = managed_names(mc)
    kept = [f.name for f in (mc / "mods").glob("*.jar") if f.name not in managed]
    for f in (mc / "mods").glob("*.jar*"):
        base = f.name.removesuffix(".disabled")
        if base in managed and base not in wanted:
            f.unlink()
    for p in ports(variant):
        shutil.copy2(p["path"], mc / "mods" / p["file"])
    for i, m in enumerate(mods, 1):
        dest = mc / "mods" / m["file"]
        twin = mc / "mods" / (m["file"] + ".disabled")
        if m.get("disabled_by_default") and not dest.exists():
            dest = twin
        elif m.get("disabled_by_default"):
            pass                      # the player enabled it: keep their choice
        elif twin.exists():
            twin.unlink()             # now enabled by default (0.6.1 first-person preset): no stale .jar/.jar.disabled pair
        shutil.copy2(fetch(m), dest)
        print(f"[{i}/{len(mods)}] {dest.name}", flush=True)
    (mc / "mods" / ".horizon-managed.json").write_text(json.dumps(sorted(managed | wanted), indent=1))
    if kept:
        print(f"kept {len(kept)} jar(s) the player added: {kept}")
    for s in L["shaders"]:
        (mc / "shaderpacks").mkdir(exist_ok=True)
        shutil.copy2(fetch(s), mc / "shaderpacks" / s["file"])
    stage = CACHE.parent / "overrides-instance"
    shutil.rmtree(stage, ignore_errors=True)
    copy_overrides(stage)
    print("pruned stale pack files:", prune_mirrored(mc, stage))
    existing = (mc / "options.txt").exists()
    copy_overrides(mc, existing=existing)
    (mc / "resourcepacks").mkdir(exist_ok=True)
    for old in STALE_FILES:
        stale = mc / "resourcepacks" / old
        if stale.exists():
            stale.unlink()
    for s in L.get("resourcepacks", []):
        shutil.copy2(fetch(s), mc / "resourcepacks" / s["file"])
    set_resourcepacks(mc / "options.txt", L.get("resourcepacks", []))
    if existing:
        for line in migrate_options(mc / "options.txt"):
            print("options.txt:", line)
    write_pack_json(inst, L)
    write_instance_cfg(inst, name)
    print(f"instance {name}: {len(mods)} mods -> {inst}")


MIN_RENDER_DISTANCE = 8   # see docs/KNOWN_ISSUES.md #29 (0.6.1): Voxy needs vanilla chunks around the camera


def migrate_options(options: Path):
    """Targeted, documented options.txt changes for an existing instance; every other key is the player's."""
    lines = options.read_text(encoding="utf-8").splitlines()
    out, changed = [], []
    for l in lines:
        k, _, v = l.partition(":")
        if k == "renderDistance" and v.isdigit() and int(v) < MIN_RENDER_DISTANCE:
            changed.append(f"renderDistance {v} -> {MIN_RENDER_DISTANCE} (Voxy LOD culling holes below this)")
            l = f"renderDistance:{MIN_RENDER_DISTANCE}"
        out.append(l)
    if changed:
        options.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def write_pack_json(inst: Path, L):
    """mmc-pack.json: rewritten only when Minecraft/NeoForge differ (Prism keeps cached component metadata there)."""
    f = inst / "mmc-pack.json"
    want = {"net.minecraft": L["minecraft"], "net.neoforged": L["loader_version"]}
    if f.exists():
        try:
            have = {c["uid"]: c.get("version") for c in json.loads(f.read_text())["components"]}
            if all(have.get(k) == v for k, v in want.items()):
                return
        except (ValueError, KeyError):
            pass
    f.write_text(json.dumps({"formatVersion": 1, "components": [
        {"uid": "net.minecraft", "version": L["minecraft"], "important": True},
        {"uid": "net.neoforged", "version": L["loader_version"]}]}, indent=2))


def write_instance_cfg(inst: Path, name: str):
    """instance.cfg: an EXISTING instance keeps every key (uuid, name, Java path/memory, managed-pack identity, window and
    UI state); only missing keys get Horizon's Balanced defaults. 0.6.0 rewrote the whole file, which would have dropped
    the Prism UUID, the player's Java/memory choice and the managed-pack binding (fixed in 0.6.1)."""
    f = inst / "instance.cfg"
    prof = json.loads((ROOT / "profiles/balanced.json").read_text())
    defaults = {"ConfigVersion": "1.2", "InstanceType": "OneSix", "name": name, "iconKey": "default",
                "OverrideMemory": "true", "MinMemAlloc": str(prof["jvm"]["min_mb"]), "MaxMemAlloc": str(prof["jvm"]["max_mb"]),
                "OverrideJavaArgs": "true", "JvmArgs": prof["jvm"]["args"]}
    if not f.exists():
        f.write_text("[General]\n" + "".join(f"{k}={v}\n" for k, v in defaults.items()))
        return
    # existing instance: only identity keys may be added; memory/JVM/icon stay the player's (Prism defaults if absent)
    defaults = {k: v for k, v in defaults.items() if k in ("ConfigVersion", "InstanceType", "name")}
    lines = f.read_text(encoding="utf-8").splitlines()
    have, section = set(), None
    for l in lines:
        if l.startswith("["):
            section = l
        elif section == "[General]" and "=" in l:
            have.add(l.split("=", 1)[0])
    missing = [f"{k}={v}" for k, v in defaults.items() if k not in have]
    if missing:
        i = lines.index("[General]") + 1 if "[General]" in lines else 0
        if "[General]" not in lines:
            lines.insert(0, "[General]"); i = 1
        lines[i:i] = missing
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")


def server(target: Path, accept_eula: bool, variant=None):
    """Populate an installed NeoForge server dir (java -jar neoforge-installer.jar --installServer)
    with server-side mods and the server-relevant overrides. eula.txt is written only when the
    operator explicitly passes --accept-eula."""
    L = lock()
    if not (target / "run.bat").exists() and not (target / "run.sh").exists():
        raise SystemExit(f"{target} is not an installed NeoForge server (no run.bat / run.sh)")
    mods = [m for m in L["mods"] if m["server_side"] != "unsupported" and not m.get("disabled_by_default")]
    (target / "mods").mkdir(exist_ok=True)
    sports = [p for p in ports(variant) if p["side"]["server"] != "unsupported"]
    wanted = {m["file"] for m in mods} | {p["file"] for p in sports}
    for f in (target / "mods").glob("*.jar"):
        if f.name not in wanted:
            f.unlink()
    for p in sports:
        shutil.copy2(p["path"], target / "mods" / p["file"])
    for m in mods:
        shutil.copy2(fetch(m), target / "mods" / m["file"])
    stage = CACHE.parent / "overrides-server"
    shutil.rmtree(stage, ignore_errors=True)
    copy_overrides(stage)
    print("pruned stale pack files:", prune_mirrored(target, stage))
    for src in ("config", "kubejs", "datapacks"):
        s = ROOT / src
        dst = target / ("kubejs/data" if src == "datapacks" else src)
        for f in s.rglob("*"):
            if f.is_file():
                out = dst / f.relative_to(s)
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out)
    prof = json.loads((ROOT / "profiles/balanced.json").read_text())
    (target / "user_jvm_args.txt").write_text(f"-Xms{prof['jvm']['min_mb']}M -Xmx{prof['jvm']['max_mb']}M {prof['jvm']['args']}\n")
    props = target / "server.properties"
    if not props.exists():
        props.write_text("motd=Project Horizon\nview-distance=10\nsimulation-distance=8\nallow-flight=true\n"
                         "spawn-protection=0\nonline-mode=true\n")
    if accept_eula:
        (target / "eula.txt").write_text("# Accepted by the server operator (https://aka.ms/MinecraftEULA)\neula=true\n")
    print(f"server: {len(mods)} server-side mods -> {target}" + (" (EULA accepted)" if accept_eula else " (eula.txt NOT written)"))


if __name__ == "__main__":
    cmd = sys.argv[1]
    args = sys.argv[2:]
    groups = args[args.index("--groups") + 1].split(",") if "--groups" in args else None
    name = args[args.index("--name") + 1] if "--name" in args else "ProjectHorizon-dev"
    variant = args[args.index("--variant") + 1] if "--variant" in args else None
    if variant not in VARIANTS:
        raise SystemExit(f"unknown variant {variant}; known: {[v for v in VARIANTS if v]}")
    if cmd == "mrpack":
        mrpack(variant)
    elif cmd == "server":
        server(Path(args[0]), "--accept-eula" in args, variant)
    else:
        instance(name, groups, variant)
