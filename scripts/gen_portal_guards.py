"""Guard Immersive Infinity's portal definitions so a missing mod cannot crash Create New World.

Immersive Infinity 0.6 ships ~70 `data/immersive_infinity/custom_portal_generation/*.json` entries that reference
blocks/items of dozens of third-party mods (DivineRPG, Blue Skies, OrePortal, ...). `custom_portal_generation` is a
datapack *registry*: one unresolved id fails the whole registry load and CreateWorldScreen throws
("Unknown registry key in ResourceKey[minecraft:root / minecraft:item]: ...").

For every definition this script finds the non-vanilla ids it references and checks them against
manifests/ids.json (items + blocks of the locked jars). Definitions that only reference ids we ship are left alone
(the jar's own copy is used, so working portals - Aether, Deeper and Darker, Undergarden x4, Twilight Forest, and the
ones with no registry references - are untouched). Every other definition is re-emitted under kubejs/data
(`datapacks/immersive_infinity/...`) with a `neoforge:conditions` entry: `neoforge:mod_loaded` for each referenced
namespace, so the portal comes back by itself if that mod is ever added, or `neoforge:false` when the mod is present but
an id is missing (a renamed block would otherwise crash the registry again).

Immersive Infinity is NOT in manifests/roster.json (see docs/KNOWN_ISSUES.md #17); the override is inert without it.

  python scripts/gen_portal_guards.py [--jar PATH]     (default: $PH_PORTAL_JAR or the newest immersive_infinity*.jar in
                                                         the dev/test Prism instances)
Owns: datapacks/immersive_infinity/** (listed in datapacks/.generated-portal-guards.json).
"""
import json, os, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix; the repo may live deep on disk
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
PREFIX = "data/immersive_infinity/custom_portal_generation/"
OUT = ROOT / "datapacks/immersive_infinity/custom_portal_generation"
MANIFEST = ROOT / "datapacks/.generated-portal-guards.json"
REF_KEYS = {"from_frame_block", "area_block", "to_frame_block", "item", "block"}


def find_jar(argv):
    if "--jar" in argv:
        return Path(argv[argv.index("--jar") + 1])
    if os.environ.get("PH_PORTAL_JAR"):
        return Path(os.environ["PH_PORTAL_JAR"])
    inst = Path(os.environ.get("APPDATA", "")) / "PrismLauncher/instances"
    jars = sorted(inst.glob("*/minecraft/mods/immersive_infinity*.jar"), key=lambda p: p.stat().st_mtime)
    if not jars:
        raise SystemExit("immersive_infinity jar not found: pass --jar or set PH_PORTAL_JAR")
    return jars[-1]


def refs(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in REF_KEYS and isinstance(v, str):
                out.add(v)
            refs(v, out)
    elif isinstance(o, list):
        for v in o:
            refs(v, out)
    return out


def main():
    ids = json.loads((ROOT / "manifests/ids.json").read_text())
    known = set(ids["item"]) | set(ids["block"])
    jar = find_jar(sys.argv[1:])
    OUT.mkdir(parents=True, exist_ok=True)
    for f in json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []:
        (ROOT / f).unlink(missing_ok=True)
    written, kept = [], []
    with zipfile.ZipFile(jar) as z:
        for n in sorted(z.namelist()):
            m = re.fullmatch(re.escape(PREFIX) + r"(.+)\.json", n)
            if not m:
                continue
            doc = json.loads(z.read(n).decode("utf-8"))
            r = {x for x in refs(doc, set()) if not x.startswith("minecraft:")}
            bad = sorted(x for x in r if x not in known)
            if not bad:
                kept.append(m.group(1))
                continue
            nss = sorted({x.split(":")[0] for x in r})
            present = {x.split(":")[0] for x in known}
            conds = [{"type": "neoforge:mod_loaded", "modid": ns} for ns in nss]
            if any(ns in present for ns in {b.split(":")[0] for b in bad}):
                conds = [{"type": "neoforge:false"}]   # mod shipped but an id is gone: never load
            cond = conds[0] if len(conds) == 1 else {"type": "neoforge:and", "values": conds}
            out = {"neoforge:conditions": [cond], **doc}
            dest = OUT / f"{m.group(1)}.json"
            dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8", newline="\n")
            written.append(dest.relative_to(ROOT).as_posix())
    MANIFEST.write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{jar.name}: {len(written)} guarded, {len(kept)} untouched ({', '.join(kept)})")


if __name__ == "__main__":
    main()
