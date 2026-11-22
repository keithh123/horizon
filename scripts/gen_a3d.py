"""Convert Actually 3D Stuff (MIT, by Arch1vways; 1.21.9+ resource pack) into a 1.21.1 NeoForge resource pack.

1.21.9+ selects the held 3D model with an item definition (assets/<ns>/items/<id>.json, `minecraft:select` on
`minecraft:display_context`). 1.21.1 has no item definitions, so each such item becomes a NeoForge
`neoforge:separate_transforms` item model: base = the 3D model, perspectives gui/ground/fixed = the flat model.

Model fixes for the 1.21.1 model loader:
  * element rotation angles outside -45/-22.5/0/22.5/45 (12.5, 15, 25 ... deg) -> 'exact' keeps them and needs the
    angle unlock in the horizon-modelangles client mod (ports/modelangles); 'snap' rounds to the nearest legal angle
  * multi-axis rotations ({"x","y","z"}, 1.21.11 format) -> single dominant axis (approximation, always recorded)
  * display 'on_shelf' and Blockbench metadata are ignored by 1.21.1 and left in place
Items that do not exist in 1.21.1, and item definitions other than a display_context select (compass, potion,
bundle, banner/special renderers, use_duration, fishing cast...) are skipped and listed in the report.

  python scripts/gen_a3d.py [--items a,b,c] [--angles exact|snap] [--out resourcepacks/HorizonA3D.zip]
Report: manifests/a3d_report.json (owned by this script, like the output zip).
"""
import hashlib, json, re, sys, urllib.request, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ports  # noqa: E402

ROOT = build_ports.ROOT
SRC = json.loads((ROOT / "ports/actually3d/source.json").read_text(encoding="utf-8"))
LEGAL = (-45.0, -22.5, 0.0, 22.5, 45.0)
FLAT_CONTEXTS = {"gui", "ground", "fixed"}           # 1.21.1 contexts the pack shows flat ('on_shelf' does not exist)
EPOCH = (1980, 2, 1, 0, 0, 0)


def vanilla_jar():
    import os
    p = Path(os.environ["APPDATA"]) / "PrismLauncher/libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar"
    if not p.exists():
        raise SystemExit(f"need the 1.21.1 client jar (launch any 1.21.1 Prism instance once): {p}")
    return zipfile.ZipFile(p)


def rl(ref, kind):
    ns, _, path = ref.partition(":") if ":" in ref else ("minecraft", "", ref)
    return f"assets/{ns}/{kind}/{path}.json" if kind == "models" else f"assets/{ns}/textures/{path}.png"


def fix_model(m, mode, notes):
    for i, e in enumerate(m.get("elements", [])):
        r = e.get("rotation")
        if not r:
            continue
        if "angle" not in r:                      # 1.21.11 multi-axis form
            comps = {a: float(r.get(a, 0)) for a in "xyz"}
            ax = max(comps, key=lambda a: abs(comps[a]))
            dropped = {a: v for a, v in comps.items() if a != ax and v}
            e["rotation"] = {"origin": r.get("origin", [8, 8, 8]), "axis": ax, "angle": comps[ax]}
            if r.get("rescale"):
                e["rotation"]["rescale"] = True
            notes.append(f"element {i}: multi-axis {comps} -> {ax} {comps[ax]} (dropped {dropped})")
            r = e["rotation"]
        a = float(r["angle"])
        if a not in LEGAL:
            if mode == "snap":
                s = min(LEGAL, key=lambda x: abs(x - a))
                notes.append(f"element {i}: angle {a} -> {s} (snapped)")
                r["angle"] = s
            else:
                notes.append(f"element {i}: angle {a} kept (needs horizon-modelangles)")
    return m


def main():
    args = sys.argv[1:]
    only = set(args[args.index("--items") + 1].split(",")) if "--items" in args else None
    mode = args[args.index("--angles") + 1] if "--angles" in args else "exact"
    out = ROOT / (args[args.index("--out") + 1] if "--out" in args else "resourcepacks/HorizonA3D.zip")
    src = zipfile.ZipFile(build_ports.fetch(SRC["url"], SRC["sha512"]))
    names = set(src.namelist())
    van = vanilla_jar()
    vnames = set(van.namelist())
    entries, report = {}, {"source": SRC, "angles": mode, "converted": [], "skipped": {}, "approximated": {}, "exact_angles": {}}

    def add_model(ref, seen):
        path = rl(ref, "models")
        if path in seen or path in entries:
            return
        seen.add(path)
        if path not in names:
            if path in vnames:
                return                                 # vanilla parent (item/generated, handheld ...)
            raise KeyError(f"missing model {ref}")
        m = json.loads(src.read(path).decode("utf-8-sig"))
        notes = []
        fix_model(m, mode, notes)
        if notes:
            tgt = report["approximated"] if any("multi-axis" in n or "snapped" in n for n in notes) else report["exact_angles"]
            tgt[ref] = notes
        entries[path] = json.dumps(m, separators=(",", ":")).encode()
        for t in (m.get("textures") or {}).values():
            if isinstance(t, str) and not t.startswith("#"):
                tp = rl(t, "textures")
                if tp in names:
                    entries[tp] = src.read(tp)
                    if tp + ".mcmeta" in names:
                        entries[tp + ".mcmeta"] = src.read(tp + ".mcmeta")
        if m.get("parent"):
            add_model(m["parent"], seen)

    for path in sorted(n for n in names if re.match(r"assets/[^/]+/items/[^/]+\.json$", n)):
        ns, item = path.split("/")[1], path.split("/")[-1][:-5]
        iid = f"{ns}:{item}"
        if only and item not in only and iid not in only:
            continue
        if ns == "minecraft" and f"assets/minecraft/models/item/{item}.json" not in vnames:
            report["skipped"][iid] = "item does not exist in 1.21.1"; continue
        d = json.loads(src.read(path).decode("utf-8-sig"))["model"]
        if not (d.get("type") == "minecraft:select" and d.get("property") == "minecraft:display_context"
                and d.get("fallback", {}).get("type") == "minecraft:model"
                and all(c["model"].get("type") == "minecraft:model" for c in d["cases"])):
            report["skipped"][iid] = f"item definition '{d.get('type')}' {d.get('property', '')} has no 1.21.1 model equivalent (needs item overrides)"
            continue
        flat_ctx = {}
        for c in d["cases"]:
            for w in ([c["when"]] if isinstance(c["when"], str) else c["when"]):
                flat_ctx[w] = c["model"]["model"]
        threed = d["fallback"]["model"]
        own = f"{ns}:item/{item}"
        try:
            add_model(threed, set())
            perspectives = {}
            for ctx, ref in flat_ctx.items():
                if ctx not in FLAT_CONTEXTS:
                    continue
                if ref == own:   # the flat model is the vanilla/mod item model we are about to replace: copy it
                    flat = f"{ns}:item/{item}_a3d_flat"
                    vp = rl(own, "models")
                    base = van.read(vp) if vp in vnames else src.read(vp) if vp in names else None
                    if base is None:
                        raise KeyError(f"no flat model for {own} (mod item model not in the pack)")
                    entries[rl(flat, "models")] = base
                    ref = flat
                else:
                    add_model(ref, set())
                perspectives[ctx] = {"parent": ref}
        except KeyError as e:
            report["skipped"][iid] = str(e); continue
        model = {"loader": "neoforge:separate_transforms", "base": {"parent": threed}, "perspectives": perspectives}
        entries[rl(own, "models")] = json.dumps(model, indent=1).encode()
        report["converted"].append(iid)

    meta = {"pack": {"pack_format": 34, "description": "Actually 3D Stuff by Arch1vways (MIT) - 1.21.1 conversion by Project Horizon"}}
    entries["pack.mcmeta"] = json.dumps(meta, indent=1).encode()
    entries["pack.png"] = src.read("pack.png")
    entries["LICENSE-ActuallY3DStuff.txt".replace("Y", "y")] = (ROOT / "ports/actually3d/LICENSE.txt").read_bytes()
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(entries):
            info = zipfile.ZipInfo(n, EPOCH); info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, entries[n])
    report["output"] = {"file": out.name, "sha512": hashlib.sha512(out.read_bytes()).hexdigest(), "entries": len(entries)}
    (ROOT / "manifests/a3d_report.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(f"{out.name}: {len(report['converted'])} items converted, {len(report['skipped'])} skipped, "
          f"{len(report['approximated'])} models approximated, {len(report['exact_angles'])} need exact angles")


if __name__ == "__main__":
    main()
