"""Regenerate everything in the safe order and prove it is idempotent.

  python scripts/build_all.py [--offline] [--no-configs] [--mrpack]

Order (each step owns disjoint outputs, see docs/BUILDING.md):
  resolve --frozen   manifests/lock.json            (skipped with --offline)
  check_deps         manifests/deps_report.json     (fails on any non-system version-range violation)
  index_ids          manifests/ids.json
  audit_loot         manifests/loot_audit.json
  gen_assets         kubejs/assets, kubejs/startup_scripts, kubejs/client_scripts (listed in kubejs/.generated-assets.json)
  gen_datapack       datapacks/** listed in datapacks/.generated.json, docs/LOOT_BUDGET.md, loot/salvage reports
  gen_headquarters   datapacks/** in datapacks/.generated-hq.json, kubejs/startup_scripts/horizon_hq_data.js, schematics/,
                     docs/HEADQUARTERS.md, docs/HQ_PLANS.md (manifests/headquarters.json)
  hq_sim (node)      tests/hq_sim.js: headquarters ledger state paths against the generated data
  gen_quests         config/heracles/quests, config/heracles/groups.txt
  patch_configs      the config files listed in its EDITS (needs a launched dev instance; --no-configs skips)
  gen_profiles       profiles/shader_options.json
  gen_docs           docs/MODLIST.md
  gen_checklist      docs/EXPANSION_CHECKLIST.md (audit + roster + lock + ports + manifests/validation.json)
Then the whole pipeline runs a second time and every owned output is hashed before/after: any difference
means a generator is not deterministic and the build fails.
"""
import hashlib, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
OWNED_DIRS = ["datapacks", "kubejs", "config", "manifests", "profiles", "resourcepacks", "schematics", "docs/LOOT_BUDGET.md", "docs/MODLIST.md",
              "docs/EXPANSION_CHECKLIST.md", "docs/HEADQUARTERS.md", "docs/HQ_PLANS.md", "docs/HQ_GRAPH.md"]
SKIP = {"lock.json", "deps_report.json", "ports_lock.json"}   # lock carries a date; resolve is network-dependent


def step(*args):
    r = subprocess.run([sys.executable, *args], cwd=ROOT)
    if r.returncode:
        raise SystemExit(f"step failed: {' '.join(args)}")


def node(script):
    exe = shutil.which("node")
    if not exe:
        print(f"SKIPPED {script}: node not found (headquarters ledger tests not run; install Node 18+)")
        return
    if subprocess.run([exe, script], cwd=ROOT).returncode:
        raise SystemExit(f"step failed: {script}")


def snapshot():
    h = {}
    for d in OWNED_DIRS:
        p = ROOT / d
        files = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file()] if p.exists() else []
        for f in files:
            if f.name in SKIP:
                continue
            h[f.relative_to(ROOT).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return h


def pipeline(offline, configs):
    if not offline:
        step("scripts/resolve.py", "--frozen")
    step("scripts/check_deps.py")
    step("scripts/index_ids.py")
    step("scripts/audit_loot.py")
    step("scripts/gen_assets.py")
    step("scripts/gen_datapack.py")
    step("scripts/gen_headquarters.py")
    node("tests/hq_sim.js")
    node("tests/kubejs_lint.js")
    step("scripts/gen_quests.py")
    step("scripts/audit_quests.py")
    step("scripts/gen_resourcepack.py")
    if configs:
        step("scripts/patch_configs.py")
    step("scripts/gen_profiles.py")
    step("scripts/gen_docs.py")
    step("scripts/gen_checklist.py")


def main():
    offline, configs = "--offline" in sys.argv, "--no-configs" not in sys.argv
    pipeline(offline, configs)
    a = snapshot()
    pipeline(True, configs)
    b = snapshot()
    diff = sorted(k for k in a.keys() | b.keys() if a.get(k) != b.get(k))
    if diff:
        raise SystemExit("NOT idempotent, changed on second run:\n  " + "\n  ".join(diff[:40]))
    print(f"idempotent: {len(b)} owned files identical across two full runs")
    if "--mrpack" in sys.argv:
        step("scripts/build.py", "mrpack")


if __name__ == "__main__":
    main()
