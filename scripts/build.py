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
             "shaderpacks": "shaderpacks", "profiles": "horizon-profiles", "options": "."}


def lock():
    return json.loads((ROOT / "manifests/lock.json").read_text())


def ports():
    """Locally built jars (ports/, scripts/build_ports.py). Shipped inside the pack because their
    licenses permit redistribution; see docs/PORTS.md."""
    f = ROOT / "manifests/ports_lock.json"
    out = []
    for p in (json.loads(f.read_text())["ports"] if f.exists() else []):
        jar = ROOT / "ports/dist" / p["file"]
        if hashlib.sha512(jar.read_bytes()).hexdigest() != p["hashes"]["sha512"]:
            raise SystemExit(f"port {p['name']}: ports/dist/{p['file']} does not match ports_lock.json - run scripts/build_ports.py")
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


def copy_overrides(target: Path):
    for src, dst in OVERRIDES.items():
        s = ROOT / src
        if not s.exists():
            continue
        for f in s.rglob("*"):
            if f.is_file() and f.name != ".gitkeep" and not f.name.startswith(".generated"):
                out = target / dst / f.relative_to(s)
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out)


def set_resourcepacks(options: Path, packs):
    """Enable the pack's resource packs in lock order (first = lowest priority) above vanilla/mod resources,
    keeping any extra packs the player enabled (they stay on top)."""
    lines = options.read_text().splitlines() if options.exists() else []
    ours = ["vanilla", "mod_resources"] + [f"file/{p['file']}" for p in packs]
    old = next((l for l in lines if l.startswith("resourcePacks:")), None)
    extra = []
    if old:
        try:
            extra = [x for x in json.loads(old.split(":", 1)[1]) if x not in ours and x not in KNOWN_OLD]
        except ValueError:
            pass
    line = "resourcePacks:" + json.dumps(ours + extra, separators=(",", ":"))
    lines = [l for l in lines if not l.startswith(("resourcePacks:", "incompatibleResourcePacks:"))] + [line, "incompatibleResourcePacks:[]"]
    options.write_text(chr(10).join(lines) + chr(10))


KNOWN_OLD = set()  # file names of resource packs shipped by earlier versions (none before 0.3.0)


def env(m):
    # Everything in the roster is part of the experience, so it is "required" on
    # every side the mod supports. Modrinth's per-project "optional" flag describes
    # client/server pairing, not pack optionality, and must not leak into the pack.
    # The client always runs an integrated server in singleplayer, so server-only
    # mods (worldgen, structures, AI libs) are REQUIRED on the client too.
    return {"client": "required",
            "server": "unsupported" if m["server_side"] == "unsupported" else "required"}


def mrpack():
    L = lock()
    files = [{"path": f"mods/{m['file']}", "hashes": {"sha1": m["hashes"]["sha1"], "sha512": m["hashes"]["sha512"]},
              "env": env(m), "downloads": [m["url"]], "fileSize": m["size"]} for m in L["mods"]]
    files += [{"path": f"shaderpacks/{s['file']}", "hashes": {"sha1": s["hashes"]["sha1"], "sha512": s["hashes"]["sha512"]},
               "env": {"client": "optional" if s["slug"] != "complementary-reimagined" else "required", "server": "unsupported"},
               "downloads": [s["url"]], "fileSize": s["size"]} for s in L["shaders"]]
    files += [{"path": f"resourcepacks/{s['file']}", "hashes": {"sha1": s["hashes"]["sha1"], "sha512": s["hashes"]["sha512"]},
               "env": {"client": "required", "server": "unsupported"},
               "downloads": [s["url"]], "fileSize": s["size"]} for s in L.get("resourcepacks", [])]
    index = {"formatVersion": 1, "game": "minecraft", "versionId": VERSION, "name": "Project Horizon",
             "summary": "Exploration-first RPG + technology pack with Voxy long-distance rendering.",
             "files": files, "dependencies": {"minecraft": L["minecraft"], "neoforge": L["loader_version"]}}
    out = ROOT / "dist" / f"ProjectHorizon-{VERSION}.mrpack"
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
        for p in ports():
            root = "client-overrides" if p["side"]["server"] == "unsupported" else "overrides"
            z.write(p["path"], f"{root}/mods/{p['file']}")
    print(f"wrote {out} ({len(files)} files, {out.stat().st_size/1024:.0f} KiB)")


def instance(name, groups):
    L = lock()
    mods = select(L["mods"], groups)
    inst = Path(os.environ["APPDATA"]) / "PrismLauncher" / "instances" / name
    mc = inst / "minecraft"
    (mc / "mods").mkdir(parents=True, exist_ok=True)
    wanted = {m["file"] for m in mods} | {p["file"] for p in ports()}
    for f in (mc / "mods").glob("*.jar"):
        if f.name not in wanted:
            f.unlink()
    for p in ports():
        shutil.copy2(p["path"], mc / "mods" / p["file"])
    for i, m in enumerate(mods, 1):
        shutil.copy2(fetch(m), mc / "mods" / m["file"])
        print(f"[{i}/{len(mods)}] {m['file']}", flush=True)
    for s in L["shaders"]:
        (mc / "shaderpacks").mkdir(exist_ok=True)
        shutil.copy2(fetch(s), mc / "shaderpacks" / s["file"])
    stage = CACHE.parent / "overrides-instance"
    shutil.rmtree(stage, ignore_errors=True)
    copy_overrides(stage)
    print("pruned stale pack files:", prune_mirrored(mc, stage))
    copy_overrides(mc)
    (mc / "resourcepacks").mkdir(exist_ok=True)
    for s in L.get("resourcepacks", []):
        shutil.copy2(fetch(s), mc / "resourcepacks" / s["file"])
    set_resourcepacks(mc / "options.txt", L.get("resourcepacks", []))
    (inst / "mmc-pack.json").write_text(json.dumps({"formatVersion": 1, "components": [
        {"uid": "net.minecraft", "version": L["minecraft"], "important": True},
        {"uid": "net.neoforged", "version": L["loader_version"]}]}, indent=2))
    prof = json.loads((ROOT / "profiles/balanced.json").read_text())
    cfg = {"ConfigVersion": "1.2", "InstanceType": "OneSix", "name": name, "iconKey": "default",
           "OverrideMemory": "true", "MinMemAlloc": str(prof["jvm"]["min_mb"]), "MaxMemAlloc": str(prof["jvm"]["max_mb"]),
           "OverrideJavaArgs": "true", "JvmArgs": prof["jvm"]["args"]}
    (inst / "instance.cfg").write_text("[General]\n" + "".join(f"{k}={v}\n" for k, v in cfg.items()))
    print(f"instance {name}: {len(mods)} mods -> {inst}")


def server(target: Path, accept_eula: bool):
    """Populate an installed NeoForge server dir (java -jar neoforge-installer.jar --installServer)
    with server-side mods and the server-relevant overrides. eula.txt is written only when the
    operator explicitly passes --accept-eula."""
    L = lock()
    if not (target / "run.bat").exists():
        raise SystemExit(f"{target} is not an installed NeoForge server (no run.bat)")
    mods = [m for m in L["mods"] if m["server_side"] != "unsupported"]
    (target / "mods").mkdir(exist_ok=True)
    sports = [p for p in ports() if p["side"]["server"] != "unsupported"]
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
    if cmd == "mrpack":
        mrpack()
    elif cmd == "server":
        server(Path(args[0]), "--accept-eula" in args)
    else:
        instance(name, groups)
