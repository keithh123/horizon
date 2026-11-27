"""Audit loot sources in the locked jars (read-only; writes manifests/loot_audit.json).

For every structure template (.nbt) it counts containers that carry a LootTable,
plus loot tables assigned by processor lists (rule processors with append_loot).
For every loot table it records nested `minecraft:loot_table` references.
It also lists every global loot modifier shipped by a mod, so import/duplication
systems (e.g. Repurposed Structures' modded-loot importer) are visible.

This is static evidence: jigsaw pools decide how many pieces actually appear,
so per-structure totals are bounds (see docs/LOOT.md for in-game samples).
"""
import gzip, io, json, os, re, struct, zipfile
from collections import defaultdict
from pathlib import Path
import sys as _sys; _sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))


# ---------------------------------------------------------------- minimal NBT
def _nbt(buf, t):
    r = buf.read
    if t == 1: return struct.unpack(">b", r(1))[0]
    if t == 2: return struct.unpack(">h", r(2))[0]
    if t == 3: return struct.unpack(">i", r(4))[0]
    if t == 4: return struct.unpack(">q", r(8))[0]
    if t == 5: return struct.unpack(">f", r(4))[0]
    if t == 6: return struct.unpack(">d", r(8))[0]
    if t == 7: n = struct.unpack(">i", r(4))[0]; r(n); return None
    if t == 8: n = struct.unpack(">H", r(2))[0]; return r(n).decode("utf-8", "replace")
    if t == 9:
        et = r(1)[0]; n = struct.unpack(">i", r(4))[0]
        return [_nbt(buf, et) for _ in range(n)]
    if t == 10:
        d = {}
        while True:
            tt = r(1)[0]
            if tt == 0: return d
            k = r(struct.unpack(">H", r(2))[0]).decode("utf-8", "replace")
            d[k] = _nbt(buf, tt)
    if t == 11: n = struct.unpack(">i", r(4))[0]; r(4 * n); return None
    if t == 12: n = struct.unpack(">i", r(4))[0]; r(8 * n); return None
    raise ValueError(t)


def read_nbt(data):
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    b = io.BytesIO(data)
    t = b.read(1)[0]
    b.read(struct.unpack(">H", b.read(2))[0])
    return _nbt(b, t)


def main():
    lock = json.loads((ROOT / "manifests/lock.json").read_text())
    lock = __import__('shipped', fromlist=['with_ports']).with_ports(lock)   # + shipped port jars (scripts/shipped.py)
    templates = {}          # "ns:path" -> {table: count}
    nested = {}             # table -> [nested tables]
    processors = defaultdict(list)   # processor list -> tables
    glms = {}               # mod -> [modifier ids]
    for m in lock["mods"]:
        try:
            z = zipfile.ZipFile(CACHE / m["file"])
        except (FileNotFoundError, zipfile.BadZipFile):
            continue
        for n in z.namelist():
            mt = re.match(r"data/([^/]+)/structures?/(.+)\.nbt$", n)
            if mt:
                try:
                    root = read_nbt(z.read(n))
                except Exception:
                    continue
                counts = defaultdict(int)
                for blk in root.get("blocks") or []:
                    tag = blk.get("nbt") or {}
                    lt = tag.get("LootTable")
                    if isinstance(lt, str):
                        counts[lt] += 1
                if counts:
                    templates[f"{mt.group(1)}:{mt.group(2)}"] = dict(counts)
                continue
            ml = re.match(r"data/([^/]+)/loot_tables?/(.+)\.json$", n)
            if ml:
                try:
                    txt = z.read(n).decode("utf-8", "ignore")
                except Exception:
                    continue
                refs = re.findall(r'"type"\s*:\s*"minecraft:loot_table"[^}]*?"(?:value|name)"\s*:\s*"([^"]+)"', txt)
                if refs:
                    nested[f"{ml.group(1)}:{ml.group(2)}"] = sorted(set(refs))
                continue
            mp = re.match(r"data/([^/]+)/worldgen/processor_list/(.+)\.json$", n)
            if mp:
                txt = z.read(n).decode("utf-8", "ignore")
                for t in re.findall(r'"loot_table"\s*:\s*"([^"]+)"', txt):
                    processors[f"{mp.group(1)}:{mp.group(2)}"].append(t)
                continue
            if n.endswith("loot_modifiers/global_loot_modifiers.json"):
                try:
                    glms[m["slug"]] = json.loads(z.read(n)).get("entries", [])
                except Exception:
                    pass
    per_table = defaultdict(lambda: {"templates": 0, "containers": 0})
    for tpl, counts in templates.items():
        for t, c in counts.items():
            per_table[t]["templates"] += 1
            per_table[t]["containers"] += c
    out = {"templates": templates, "per_table": dict(per_table), "nested": nested,
           "processor_loot": {k: sorted(set(v)) for k, v in processors.items()}, "global_loot_modifiers": glms}
    (ROOT / "manifests/loot_audit.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print(f"templates with loot: {len(templates)} | distinct tables placed: {len(per_table)} | "
          f"nested tables: {len(nested)} | processor lists with loot: {len(processors)} | mods with GLMs: {len(glms)}")


if __name__ == "__main__":
    main()
