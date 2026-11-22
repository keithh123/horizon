"""Turn an in-game calibration run into manifests/loot_calibration.json.

  python scripts/calibrate.py <server_log> tests/calibration.txt

tests/calibration.txt places real structures with /place structure and runs `/horizon audit`
(kubejs/server_scripts/horizon_events.js) over each one. The audit logs every container block entity's
loot table and the per-clear Horizon yield over N rolls. This script pairs audits with the structures in
command order and stores {structure: {"tables": {table: containers}, "measured": {...}}}.
gen_datapack.py then budgets those structures from REAL container counts (jigsaw repeats included)
instead of unique-template counts.
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))


def main():
    log = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").splitlines()
    cmds = Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
    structs = [m.group(1) for c in cmds for m in [re.match(r"# \d+ (\S+)", c)] if m]
    heads = [l for l in log if "[horizon-audit] radius=" in l and "KubeJS" in l]
    tabs = [l for l in log if "[horizon-audit] tables=" in l]
    if len(heads) != len(structs) or len(tabs) != len(structs):
        print(f"WARNING: {len(structs)} structures, {len(heads)} audits, {len(tabs)} table lines - pairing by order")
    out = {}
    for s, h, t in zip(structs, heads, tabs):
        m = re.search(r"containers=(\d+) perClear=(\{.*\})", h)
        tables = json.loads(t.split("tables=", 1)[1])
        out[s] = {"containers": int(m.group(1)), "measured": json.loads(m.group(2)), "tables": tables}
        print(f"{s:42} containers={out[s]['containers']:4} {out[s]['measured']}")
    p = ROOT / "manifests/loot_calibration.json"
    old = json.loads(p.read_text()) if p.exists() else {}
    old.update(out)
    p.write_text(json.dumps(old, indent=1, sort_keys=True) + "\n")
    print(f"{len(out)} structures calibrated -> {p.name}")


if __name__ == "__main__":
    main()
