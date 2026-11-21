"""Generate the pack's data overrides into datapacks/ (shipped as kubejs/data).

1. Ore unification  - disable duplicate ore generators (biome modifiers -> neoforge:none)
2. Structure tiers  - re-space selected structure sets (copied from the jar, spacing scaled)
3. Exploration loot - NeoForge global loot modifiers inject tiered Horizon relics into
                      chest / boss loot tables, chosen from the real loot-table index.
Every id is checked against manifests/ids.json; unknown ids abort the build.
"""
import json, os, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix \?\ - the repo may live deep on disk
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
OUT = ROOT / "datapacks"
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
IDS = json.loads((ROOT / "manifests/ids.json").read_text())
LOCK = json.loads((ROOT / "manifests/lock.json").read_text())


VANILLA_CHESTS = ["village/village_" + v for v in ("armorer", "butcher", "cartographer", "desert_house", "fisher", "fletcher", "mason",
                  "plains_house", "savanna_house", "shepherd", "snowy_house", "taiga_house", "tannery", "temple", "toolsmith", "weaponsmith")] + [
    "ruined_portal", "shipwreck_map", "shipwreck_supply", "shipwreck_treasure", "abandoned_mineshaft", "simple_dungeon", "pillager_outpost",
    "igloo_chest", "underwater_ruin_small", "underwater_ruin_big", "stronghold_corridor", "stronghold_crossing", "stronghold_library",
    "bastion_bridge", "bastion_hoglin_stable", "bastion_other", "bastion_treasure", "ancient_city", "ancient_city_ice_box", "woodland_mansion",
    "nether_bridge", "buried_treasure", "jungle_temple", "desert_pyramid", "end_city_treasure"]
IDS["loot_table"] = sorted(set(IDS["loot_table"]) | {f"minecraft:chests/{c}" for c in VANILLA_CHESTS}
                           | {f"minecraft:entities/{e}" for e in ("ender_dragon", "wither", "warden", "elder_guardian")})


def need(kind, i):
    if i.startswith("minecraft:") and kind in ("entity", "item"):
        return i
    if i not in IDS[kind]:
        raise SystemExit(f"unknown {kind} id: {i}")
    return i


def write(rel, obj):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")


def jar_json(ns_path):  # "ns:worldgen/structure_set/x" -> parsed json from whichever jar has it
    ns, path = ns_path.split(":")
    name = f"data/{ns}/{path}.json"
    for m in LOCK["mods"]:
        with zipfile.ZipFile(CACHE / m["file"]) as z:
            if name in z.namelist():
                return json.loads(z.read(name))
    raise SystemExit(f"not found in jars: {name}")


# ---------------------------------------------------------------- 1. ores
# Mekanism owns tin/lead/uranium/osmium; MI keeps its unique ores
# (antimony, bauxite, monazite, nickel, salt, tungsten, lignite); Powah's
# uraninite is obtained from Mekanism uranium (recipe in kubejs).
DISABLE_ORES = [
    *(f"modern_industrialization:{p}ore_generator_{o}" for o in ("tin", "lead", "uranium") for p in ("", "deepslate_")),
    "powah:uraninite_ore", "powah:uraninite_ore_dense", "powah:uraninite_ore_poor",
]

# ------------------------------------------------------- 2. structure tiers
# (set id, spacing, separation, tier) - only sets whose defaults clash with the
# tier design are touched; everything else keeps the author's tuning.
STRUCTURE_SETS = [
    ("dungeons_arise:major_structures", 60, 44, "rare/legendary landmarks"),
    ("mowziesmobs:frostmaw_spawns", 40, 16, "rare mini-boss"),
    ("mowziesmobs:monasteries", 36, 14, "rare mini-boss"),
    ("mowziesmobs:umvuthana_groves", 36, 14, "rare mini-boss"),
    ("mowziesmobs:wrought_chambers", 24, 10, "uncommon mini-boss"),
    ("apotheosis:towers", 32, 20, "uncommon boss tower"),
]

# ------------------------------------------------------ 3. exploration loot
COMMON_NS = {"explorify", "structory", "yungs_extras", "towns_and_towers", "ctov", "nova_structures", "repurposed_structures", "betterwitchhuts"}
RARE_NS = {"dungeons_arise", "betterdungeons", "betterstrongholds", "betterfortresses", "betterdeserttemples", "betterjungletemples",
           "betteroceanmonuments", "incendium", "deeperdarker", "aether", "undergarden", "irons_spellbooks", "mowziesmobs", "the_bumblezone", "apotheosis"}
LEGENDARY_PATTERNS = [r"^cataclysm:chests/", r"^dungeons_arise:chests/(keep_kayra|shiraz_palace|plague_asylum|heavenly_|typhon|mechanical_nest|thornborn|kisegi)",
                      r"^minecraft:chests/(end_city_treasure|ancient_city$|bastion_treasure)"]
RARE_VANILLA = r"^minecraft:chests/(stronghold_|bastion_|ancient_city|woodland_mansion|nether_bridge|buried_treasure|jungle_temple$|desert_pyramid)"
COMMON_VANILLA = r"^minecraft:chests/(village/|ruined_portal|shipwreck_|abandoned_mineshaft|simple_dungeon|pillager_outpost|igloo|underwater_ruin)"
BOSSES_LEGENDARY = ["minecraft:ender_dragon", "minecraft:wither", "cataclysm:ignis", "cataclysm:netherite_monstrosity", "cataclysm:the_harbinger",
                    "cataclysm:the_leviathan", "cataclysm:ender_guardian", "cataclysm:maledictus", "cataclysm:ancient_remnant", "cataclysm:scylla",
                    "aether:sun_spirit", "deeperdarker:stalker", "minecraft:warden"]
BOSSES_RARE = ["mowziesmobs:ferrous_wroughtnaut", "mowziesmobs:frostmaw", "mowziesmobs:umvuthi", "mowziesmobs:sculptor", "aether:slider",
               "aether:valkyrie_queen", "undergarden:forgotten_guardian", "minecraft:elder_guardian", "irons_spellbooks:dead_king",
               "the_bumblezone:cosmic_crystal_entity"]


def classify(table):
    ns, path = table.split(":")
    if not (path.startswith("chests/") or "/chests/" in path or path.startswith("chest/")):
        return None
    if any(re.search(p, table) for p in LEGENDARY_PATTERNS):
        return "legendary"
    if ns == "minecraft":
        return "rare" if re.search(RARE_VANILLA, table) else "common" if re.search(COMMON_VANILLA, table) else None
    if ns in RARE_NS:
        return "rare"
    if ns in COMMON_NS or ns == "terralith":
        return "common"
    return None


RELIC = {"common": ("horizon:wayfarer_shard", 0.35, [1, 2]),
         "rare": ("horizon:ancient_core", 0.30, [1, 1]),
         "legendary": ("horizon:starforged_heart", 0.45, [1, 1])}


def relic_table(item, chance, count):
    return {"type": "minecraft:chest", "pools": [{"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": chance}],
            "entries": [{"type": "minecraft:item", "name": item,
                         "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": count[0], "max": count[1]}}]}]}]}


def main():
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)
    for bm in DISABLE_ORES:
        need("biome_modifier", bm)
        ns, p = bm.split(":")
        write(f"{ns}/neoforge/biome_modifier/{p}.json", {"type": "neoforge:none"})

    for sid, spacing, sep, why in STRUCTURE_SETS:
        need("structure_set", sid)
        d = jar_json(sid.replace(":", ":worldgen/structure_set/"))
        d["placement"]["spacing"], d["placement"]["separation"] = spacing, sep
        ns, p = sid.split(":")
        write(f"{ns}/worldgen/structure_set/{p}.json", d)

    tiers = {"common": [], "rare": [], "legendary": []}
    for t in IDS["loot_table"]:
        c = classify(t)
        if c:
            tiers[c].append(t)
    for ent in BOSSES_LEGENDARY + BOSSES_RARE:
        need("entity", ent)
        ns, p = ent.split(":")
        t = f"{ns}:entities/{p}"
        if t in IDS["loot_table"]:
            tiers["legendary" if ent in BOSSES_LEGENDARY else "rare"].append(t)
    modifiers = []
    for tier, tables in tiers.items():
        item, chance, count = RELIC[tier]
        write(f"horizon/loot_table/inject/{tier}.json", relic_table(item, chance, count))
        # boss tables always drop (chance 1) via a separate table
        write(f"horizon/loot_table/inject/{tier}_boss.json", relic_table(item, 1.0, [1, 2] if tier == "legendary" else [1, 1]))
        chests = sorted(t for t in tables if "/entities/" not in t and ":entities/" not in t)
        bosses = sorted(t for t in tables if ":entities/" in t)
        for name, group, table in ((f"{tier}_chests", chests, f"horizon:inject/{tier}"), (f"{tier}_bosses", bosses, f"horizon:inject/{tier}_boss")):
            if not group:
                continue
            write(f"horizon/loot_modifiers/{name}.json", {
                "type": "neoforge:add_table",
                "conditions": [{"condition": "minecraft:any_of", "terms": [{"condition": "neoforge:loot_table_id", "loot_table_id": t} for t in group]}],
                "table": table})
            modifiers.append(f"horizon:{name}")
    write("neoforge/loot_modifiers/global_loot_modifiers.json", {"replace": False, "entries": modifiers})
    (ROOT / "manifests/loot_tiers.json").write_text(json.dumps(tiers, indent=1))
    print("ores disabled:", len(DISABLE_ORES), "| structure sets:", len(STRUCTURE_SETS),
          "| loot tables per tier:", {k: len(v) for k, v in tiers.items()})


if __name__ == "__main__":
    main()
