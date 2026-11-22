"""Static audit of config/heracles/quests: placeholders, titles, prerequisites, cycles, early-chain deadlocks.
Usage: python scripts/audit_quests.py   (exit 1 on any problem)"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + "?" + chr(92)  # Windows long-path prefix
if __import__("os").name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
Q = ROOT / "config" / "heracles" / "quests"
quests = {}
for f in sorted(Q.rglob("*.json")):
    quests[f.stem] = json.loads(f.read_text(encoding="utf-8"))

problems = []
titles = {}
for qid, q in quests.items():
    d = q["display"]
    raw_t = d["title"]
    try:
        raw_t = json.loads(raw_t) if isinstance(raw_t, str) else raw_t
    except ValueError:
        pass
    if not isinstance(raw_t, dict) or "text" not in raw_t or not isinstance(d["title"], str):
        problems.append(f"{qid}: title must be a string holding component JSON (Heracles 2.0.3 FLAT_CODEC); anything else shows as New Quest")
        raw_t = {"text": str(raw_t)}
    t = raw_t["text"].strip()
    desc = " ".join(d["description"])
    if re.match(r"(?i)new quest|untitled|todo|placeholder", t) or len(t) < 4:
        problems.append(f"{qid}: placeholder title {t!r}")
    titles.setdefault(t.lower(), []).append(qid)
    if "Objective:" not in desc or "Why it matters:" not in desc:
        problems.append(f"{qid}: missing objective/why lines")
    if not q["tasks"]:
        problems.append(f"{qid}: no tasks")
    if not q["rewards"]:
        problems.append(f"{qid}: no rewards")
    for dep in q["dependencies"]:
        if dep not in quests:
            problems.append(f"{qid}: unknown prerequisite {dep}")
for t, ids in titles.items():
    if len(ids) > 1:
        problems.append(f"duplicate title {t!r}: {ids}")

# cycles
state = {}
def visit(n, path):
    if state.get(n) == 2:
        return
    if state.get(n) == 1:
        problems.append("prerequisite cycle: " + " -> ".join(path + [n]))
        return
    state[n] = 1
    for dep in quests[n]["dependencies"]:
        if dep in quests:
            visit(dep, path + [n])
    state[n] = 2
for n in quests:
    visit(n, [])

# early-chain deadlock: a root-reachable quest must not require an advancement that itself needs an item
# the book only unlocks later. The known case: story/root (craft a crafting table) gating the wood quest.
DEADLOCK_ADV = {"minecraft:story/root"}
first = quests.get("1thefirststeps_welcome")
if first:
    # the root quest must complete by something the player can do at once: a Check click. (Advancement tasks only
    # complete from advancement events / quest init, a tick advancement did not complete it in game; story/root needs wood.)
    if [t.get("type") for t in first["tasks"].values()] != ["heracles:check"]:
        problems.append("1thefirststeps_welcome must be a single heracles:check task (verified in game 2026-11-22)")
    if first["dependencies"]:
        problems.append("welcome must have no prerequisites")
    if "1thefirststeps_wood" in quests and quests["1thefirststeps_wood"]["dependencies"] != ["1thefirststeps_welcome"]:
        problems.append("wood quest prerequisite changed")

print(f"{len(quests)} quests audited, {len(problems)} problems")
for p in problems:
    print(" -", p)
sys.exit(1 if problems else 0)
