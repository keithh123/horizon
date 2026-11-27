"""Build manifests/ids.json: registry ids found in the locked jars.

Items/blocks/entities come from lang keys (item.<ns>.<path>, block.<ns>.<path>,
entity.<ns>.<path>) plus item model files; structures, structure sets,
dimensions, loot tables, biome modifiers and advancements come from data/.
Used by gen_content.py to validate every id it references.
"""
import io, json, re, zipfile
from pathlib import Path
import sys as _sys; _sys.path.insert(0, str(Path(__file__).resolve().parent))
import os

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix \?\ - the repo may live deep on disk
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
DATA_KINDS = {
    "worldgen/structure": "structure", "worldgen/structure_set": "structure_set",
    "dimension": "dimension", "loot_table": "loot_table", "advancement": "advancement",
    "neoforge/biome_modifier": "biome_modifier", "worldgen/placed_feature": "placed_feature",
}


def scan(z, out):
    for n in z.namelist():
        if n.endswith(".jar") and n.startswith("META-INF/jar"):
            try:
                scan(zipfile.ZipFile(io.BytesIO(z.read(n))), out)
            except zipfile.BadZipFile:
                pass
            continue
        m = re.match(r"assets/([^/]+)/lang/en_us\.json$", n)
        if m:
            try:
                lang = json.loads(z.read(n).decode("utf-8", "ignore"))
            except Exception:
                continue
            for k in lang:
                km = re.match(r"(item|block|entity)\.([a-z0-9_.-]+?)\.([a-z0-9_/.-]+)$", k)
                if km and km.group(2) == m.group(1):
                    out[km.group(1)].add(f"{km.group(2)}:{km.group(3)}")
            continue
        m = re.match(r"assets/([^/]+)/models/item/([a-z0-9_/.-]+)\.json$", n)
        if m:
            out["item"].add(f"{m.group(1)}:{m.group(2)}")
            continue
        m = re.match(r"assets/([^/]+)/items/([a-z0-9_/.-]+)\.json$", n)
        if m:
            out["item"].add(f"{m.group(1)}:{m.group(2)}")
            continue
        m = re.match(r"data/([^/]+)/(.+)\.json$", n)
        if m:
            rest = m.group(2)
            for prefix, kind in DATA_KINDS.items():
                if rest.startswith(prefix + "/"):
                    out[kind].add(f"{m.group(1)}:{rest[len(prefix) + 1:]}")
                    break


def main():
    lock = json.loads((ROOT / "manifests/lock.json").read_text())
    lock = __import__('shipped', fromlist=['with_ports']).with_ports(lock)   # + shipped port jars (scripts/shipped.py)
    out = {k: set() for k in ["item", "block", "entity", *DATA_KINDS.values()]}
    per_mod = {}
    for m in lock["mods"]:
        before = {k: len(v) for k, v in out.items()}
        with zipfile.ZipFile(CACHE / m["file"]) as z:
            scan(z, out)
        per_mod[m["slug"]] = {k: len(out[k]) - before[k] for k in out}
    # blocks are also items in nearly all cases
    out["item"] |= out["block"]
    res = {k: sorted(v) for k, v in out.items()}
    (ROOT / "manifests/ids.json").write_text(json.dumps(res, indent=0))
    print({k: len(v) for k, v in res.items()})


if __name__ == "__main__":
    main()
