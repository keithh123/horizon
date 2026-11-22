"""Generate the merged worldgen for the Horizon Depths variant (Infinity Cave on top of Tectonic + Terralith).

Infinity Cave 0.7 ships an always-on built-in datapack (`infinity_cave_terralith` when Terralith is loaded,
Pack.Position.TOP, required) that carries full copies of Terralith-era `minecraft:` worldgen files. Loaded as-is it
replaces Tectonic's noise router and Terralith 2.6.2's biome source with older copies. Its own changes on top of
Terralith are small, so this script re-applies only those changes on top of the files Horizon actually runs with:

  noise_settings/overworld   Tectonic 'terratonic' overlay (the one active with Terralith on 1.21.1)
                             + noise min_y -128 / height 448 (top stays at 320)
                             + Infinity Cave's 4 biome-gated deep surface rules, inserted after the bedrock floor
  final_density              min(Tectonic final_density, Infinity Cave deep cave term for -124 <= y < -14)
  dimension/overworld        Terralith 2.6.2 biome source + Infinity Cave's 6 deep biomes (parameters verbatim)
  biomes (minecraft:, terralith:) that Infinity Cave edits: Terralith 2.6.2 biome + the infinity_cave:* features
                             Infinity Cave adds (same step, same relative position); everything else Terralith's
  dimension_type/overworld   Infinity Cave's (min_y -128, height 448), unchanged

Every other `minecraft:` worldgen file in the IC pack that only duplicates Terralith is dropped, so Tectonic's and
Terralith's own versions stay in effect. Outputs (owned by this script): ports/infinitycave/gen/** and
ports/infinitycave/merge.json (consumed by build_ports.py: 'add' + 'drop').

  python scripts/gen_deepcaves.py
"""
import json, shutil, sys, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ports  # noqa: E402  (fetch + pinned cache)

ROOT = build_ports.ROOT
PORT = ROOT / "ports" / "infinitycave"
GEN = PORT / "gen"
PACK = "resourcepacks/infinity_cave_terralith/data/"
TEC_OVERLAY = "resourcepacks/tectonic/overlay.terratonic/data/"
TEC_BASE = "resourcepacks/tectonic/data/"
FD = "minecraft/worldgen/density_function/overworld/noise_router/final_density.json"
NS = "minecraft/worldgen/noise_settings/overworld.json"
DIM = "minecraft/dimension/overworld.json"
WORLDGEN_PREFIXES = ("minecraft/worldgen/", "minecraft/dimension/")


def j(b):
    return json.loads(b.decode("utf-8-sig"))


def canon(x):
    return json.dumps(x, sort_keys=True)


def lock_jar(slug):
    lock = json.loads((ROOT / "manifests/lock.json").read_text())
    m = next(m for m in lock["mods"] if m["slug"] == slug)
    return build_ports.fetch(m["url"], m["hashes"]["sha512"])


def merge_biome(ter, ic):
    """Terralith biome + the infinity_cave:* placed features IC inserted, per generation step."""
    out = json.loads(json.dumps(ter))
    feats = out.setdefault("features", [])
    for step, ic_list in enumerate(ic.get("features", [])):
        added = [f for f in ic_list if isinstance(f, str) and f.startswith("infinity_cave:")]
        if not added:
            continue
        while len(feats) <= step:
            feats.append([])
        cur = feats[step]
        new = [f for f in added if f not in cur]
        # IC prepends its depth features (stone layers run before ores); otherwise it appends
        feats[step] = new + cur if ic_list[0] in added else cur + new
    return out


def main():
    spec = json.loads((PORT / "port.json").read_text(encoding="utf-8"))
    ic_z = zipfile.ZipFile(build_ports.fetch(spec["upstream"]["url"], spec["upstream"]["sha512"]))
    tec_z = zipfile.ZipFile(lock_jar("tectonic"))
    ter_z = zipfile.ZipFile(lock_jar("terralith"))
    ic = {n[len(PACK):]: n for n in ic_z.namelist() if n.startswith(PACK) and n.endswith(".json")}
    ter = {n[len("data/"):]: n for n in ter_z.namelist() if n.startswith("data/") and n.endswith(".json")}
    tec_names = set(tec_z.namelist())

    def tec(rel):
        for base in (TEC_OVERLAY, TEC_BASE):
            if base + rel in tec_names:
                return j(tec_z.read(base + rel))
        return None

    shutil.rmtree(GEN, ignore_errors=True)
    add, drop, report = {}, [], {"dropped_duplicates_of_terralith": 0, "merged": [], "kept_ic": []}

    def emit(rel, obj):
        p = GEN / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8")
        add[PACK + rel] = "gen/" + rel

    # 1. final_density: Tectonic's router, plus IC's deep cave term (IC applies it as an outer min with noodle caves)
    ic_fd, ter_fd, tec_fd = j(ic_z.read(ic[FD])), j(ter_z.read(ter[FD])), tec(FD)
    if canon(ic_fd["argument1"]) != canon(ter_fd["argument1"]) or ter_fd["argument2"] != "minecraft:overworld/caves/noodle":
        raise SystemExit("final_density: Infinity Cave/Terralith layout changed; re-check the merge by hand")
    deep = ic_fd["argument2"]["argument2"]
    assert deep["type"] == "minecraft:range_choice" and deep["when_in_range"] == "infinity_cave:custom", deep
    emit(FD, {"type": "minecraft:min", "argument1": tec_fd, "argument2": deep})
    report["merged"].append(FD)

    # 2. noise_settings: Tectonic terratonic + IC vertical range + IC deep surface rules
    ic_ns, ter_ns, tec_ns = j(ic_z.read(ic[NS])), j(ter_z.read(ter[NS])), tec(NS)
    ter_seq = {canon(r) for r in ter_ns["surface_rule"]["sequence"]}
    ic_new = [r for r in ic_ns["surface_rule"]["sequence"]
              if canon(r) not in ter_seq and r.get("if_true", {}).get("type") == "minecraft:biome"
              and all(b.startswith("infinity_cave:") for b in r["if_true"]["biome_is"])]
    if len(ic_new) != 4:
        raise SystemExit(f"expected 4 Infinity Cave deep surface rules, found {len(ic_new)}")
    ns = json.loads(json.dumps(tec_ns))
    ns["noise"]["min_y"] = -128
    ns["noise"]["height"] = (tec_ns["noise"]["min_y"] + tec_ns["noise"]["height"]) + 128   # keep Tectonic's top (320)
    seq = ns["surface_rule"]["sequence"]
    assert seq[0]["if_true"].get("random_name") == "minecraft:bedrock_floor", "surface rule 0 is not the bedrock floor"
    ns["surface_rule"]["sequence"] = seq[:1] + ic_new + seq[1:]
    emit(NS, ns)
    report["merged"].append(NS)

    # 3. biome source: Terralith 2.6.2 + IC deep biomes
    ic_dim, ter_dim = j(ic_z.read(ic[DIM])), j(ter_z.read(ter[DIM]))
    known = {b["biome"] for b in ter_dim["generator"]["biome_source"]["biomes"]}
    extra = [b for b in ic_dim["generator"]["biome_source"]["biomes"] if b["biome"].startswith("infinity_cave:") and b["biome"] not in known]
    dim = json.loads(json.dumps(ter_dim))
    dim["type"] = ic_dim["type"]
    dim["generator"]["biome_source"]["biomes"] += extra
    emit(DIM, dim)
    report["merged"].append(f"{DIM} (+{len(extra)} biomes)")

    # 4. biomes Infinity Cave edits; 5. drop everything else that only shadows Terralith/Tectonic
    for rel, name in sorted(ic.items()):
        if rel in (FD, NS, DIM) or not rel.startswith(WORLDGEN_PREFIXES) and not rel.startswith("terralith/worldgen/biome/"):
            continue
        icd = j(ic_z.read(name))
        if "/worldgen/biome/" in rel and rel in ter:
            terd = j(ter_z.read(ter[rel]))
            if canon(icd) == canon(terd):
                drop.append(name); report["dropped_duplicates_of_terralith"] += 1
            elif any(isinstance(f, str) and f.startswith("infinity_cave:") for st in icd.get("features", []) for f in st):
                emit(rel, merge_biome(terd, icd)); report["merged"].append(rel)
            else:
                drop.append(name); report["dropped_duplicates_of_terralith"] += 1   # only older-Terralith drift
            continue
        if rel in ter or tec(rel) is not None:
            other = j(ter_z.read(ter[rel])) if rel in ter else tec(rel)
            if canon(icd) == canon(other) or tec(rel) is not None:
                drop.append(name); report["dropped_duplicates_of_terralith"] += 1
                continue
        report["kept_ic"].append(rel)   # IC-only files (dimension_type, cave carvers, deep_dark biome, ...)

    merge = {"generated_by": "scripts/gen_deepcaves.py", "add": dict(sorted(add.items())), "drop": sorted(drop), "report": report}
    (PORT / "merge.json").write_text(json.dumps(merge, indent=1) + "\n", encoding="utf-8")
    print(f"merged {len(report['merged'])} files, dropped {len(drop)} shadowing copies, kept IC-only: {report['kept_ic']}")


if __name__ == "__main__":
    main()
