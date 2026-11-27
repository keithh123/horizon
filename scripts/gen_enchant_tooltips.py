"""Enchantment tooltip descriptions -> lang files (0.6.1).

Reads manifests/enchantment_tooltips.json (hand-written, one description per enchantment id) and writes
kubejs/assets/<namespace>/lang/en_us.json with `enchantment.<namespace>.<path>.desc` keys. Apothic Enchanting prints these
under each enchantment line when "Enable Inlined Enchantment Descriptions" is true (scripts/patch_configs.py). Minecraft merges
lang files key by key across packs, so these files add descriptions without replacing any mod's names.

Ownership: exactly the files listed in kubejs/.generated-enchant.json (deleted and rewritten each run). The horizon namespace
lang file belongs to gen_assets.py; this script refuses to write into a file it does not own.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "manifests/enchantment_tooltips.json"
OWN = ROOT / "kubejs/.generated-enchant.json"
MAX_LEN = 140   # one or two tooltip lines; keep them concise


def main():
    desc = json.loads(SRC.read_text(encoding="utf-8"))["descriptions"]
    by_ns = {}
    for eid, text in sorted(desc.items()):
        ns, _, path = eid.partition(":")
        if not ns or not path or not text.strip():
            raise SystemExit(f"bad entry {eid!r}")
        if len(text) > MAX_LEN:
            raise SystemExit(f"{eid}: description is {len(text)} chars (max {MAX_LEN})")
        by_ns.setdefault(ns, {})[f"enchantment.{ns}.{path}.desc"] = text
    old = json.loads(OWN.read_text()) if OWN.exists() else []
    for rel in old:
        (ROOT / rel).unlink(missing_ok=True)
    owned = []
    for ns, keys in sorted(by_ns.items()):
        rel = f"kubejs/assets/{ns}/lang/en_us.json"
        out = ROOT / rel
        if out.exists() and rel not in old:
            raise SystemExit(f"{rel} exists and is not owned by this script")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(keys, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        owned.append(rel)
    OWN.write_text(json.dumps(owned, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"enchantment tooltips: {len(desc)} descriptions in {len(owned)} namespaces")


if __name__ == "__main__":
    main()
