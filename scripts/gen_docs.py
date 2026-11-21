"""Generate docs/MODLIST.md from manifests/lock.json + roster rejections."""
import json, os
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
L = json.loads((ROOT / "manifests/lock.json").read_text())
R = json.loads((ROOT / "manifests/roster.json").read_text())
ORDER = ["renderer", "performance", "worldgen", "structures", "dimensions", "rpg", "magic", "technology", "qol", "atmosphere", "dependency"]
out = [f"# Mod list - Project Horizon {(ROOT / 'VERSION').read_text().strip()}", "",
       f"Minecraft {L['minecraft']} - NeoForge {L['loader_version']} - {len(L['mods'])} mods - generated {L['generated']} from `manifests/lock.json`.", "",
       "Channel `beta`/`alpha` is the upstream author's label. Side = Modrinth client/server metadata (the pack installs everything on the client because singleplayer runs an integrated server).", ""]
for g in ORDER:
    mods = [m for m in L["mods"] if m["group"] == g]
    if not mods:
        continue
    out += [f"## {g.title()} ({len(mods)})", "", "| Mod | Version | Channel | Side (c/s) | License | Why |", "|---|---|---|---|---|---|"]
    for m in sorted(mods, key=lambda m: m["title"].lower()):
        why = m["why"] if g != "dependency" else "Required by " + ", ".join(sorted(set(m["required_by"])))
        out.append(f"| [{m['title']}](https://modrinth.com/project/{m['project_id']}) | `{m['version']}` | {m['channel']} | {m['client_side'][:3]}/{m['server_side'][:3]} | {m['license']} | {why} |")
    out.append("")
out += ["## Shaders", "", "| Shader | Version | Why |", "|---|---|---|"]
out += [f"| {s['slug']} | `{s['version']}` | {s['why']} |" for s in L["shaders"]]
out += ["", "## Considered and rejected", "", "| Candidate | Reason |", "|---|---|"]
out += [f"| {k} | {v} |" for k, v in R["rejected"].items()]
(ROOT / "docs/MODLIST.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("docs/MODLIST.md:", len(L["mods"]), "mods")
