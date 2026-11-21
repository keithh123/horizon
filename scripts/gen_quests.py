"""Generate the Odyssey Quests (Heracles) quest book into config/heracles/.

Quests are declared compactly below and expanded to Heracles' JSON schema
(earth.terrarium.heracles.api.quests.Quest codec, Heracles 2.0.x for 1.21.1).
Every item / advancement / entity / structure / dimension id is validated
against manifests/ids.json, so a quest can never reference a missing object.

Task shorthand:  ("adv", "ns:path")  ("item", "ns:id", count)  ("dim", "ns:dim")
                 ("kill", "ns:entity", count)  ("struct", "ns:structure" | "#tag")
Reward shorthand: ("item", "ns:id", count)  ("xp", levels)  ("loot", "ns:table")
"""
import json, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
IDS = {k: set(v) for k, v in json.loads((ROOT / "manifests/ids.json").read_text()).items()}
OUT = ROOT / "config" / "heracles"
HORIZON_ITEMS = {"horizon:wayfarer_shard", "horizon:ancient_core", "horizon:starforged_heart"}
VANILLA_DIMS = {"minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"}
SHARD, CORE, HEART = sorted(HORIZON_ITEMS)[2], sorted(HORIZON_ITEMS)[0], sorted(HORIZON_ITEMS)[1]

# ---------------------------------------------------------------- the book
# chapter -> list of (id, title, icon, description, deps, tasks, rewards)
C = {}
C["1 - The First Steps"] = [
    ("welcome", "Welcome to the Horizon", "minecraft:compass",
     ["The world is enormous. Mountains here are real mountains, and with Voxy you can see them from very far away.",
      "This book is a guide, not a checklist: every chapter is optional. Follow what interests you.",
      "Press &eJ&r any time to reopen it (keybinds are searchable in Options > Controls)."], [], [("adv", "minecraft:story/root")], [("item", "minecraft:bread", 8)]),
    ("wood", "Timber!", "minecraft:oak_log", ["Gather wood for tools and a first shelter."], ["welcome"],
     [("item", "#minecraft:logs", 16)], [("item", "minecraft:torch", 16)]),
    ("stone_age", "Stone Age", "minecraft:stone_pickaxe", ["Mine stone and craft better tools."], ["wood"],
     [("adv", "minecraft:story/mine_stone")], [("xp", 2)]),
    ("iron", "Iron Will", "minecraft:iron_ingot", ["Smelt iron. Most of the pack's machines start here."], ["stone_age"],
     [("adv", "minecraft:story/smelt_iron")], [("item", "minecraft:iron_ingot", 6)]),
    ("bed", "A Place to Rest", "minecraft:red_bed", ["Sleep through your first night. Bosses and dungeons do not rest - you should."], ["wood"],
     [("adv", "minecraft:adventure/sleep_in_bed")], [("item", "farmersdelight:cooking_pot", 1)]),
    ("kitchen", "Hearty Meals", "farmersdelight:cooking_pot", ["Farmer's Delight meals give long buffs. AppleSkin shows saturation on hover."], ["bed"],
     [("item", "farmersdelight:cooking_pot", 1)], [("item", "minecraft:golden_carrot", 8)]),
    ("backpack", "Pack Mule", "sophisticatedbackpacks:backpack", ["A backpack makes long expeditions possible."], ["iron"],
     [("item", "sophisticatedbackpacks:backpack", 1)], [("xp", 3)]),
    ("diamonds", "Diamonds!", "minecraft:diamond", ["Deep caves under Terralith's mountains hide diamonds - and danger."], ["iron"],
     [("adv", "minecraft:story/mine_diamond")], [("item", SHARD, 1)]),
]
C["2 - The Wild Frontier"] = [
    ("first_ruin", "Something Old", "minecraft:mossy_cobblestone",
     ["Explore any ruin, camp or shrine. Small sites hold &bWayfarer Shards&r - the first exploration relic."], [],
     [("item", SHARD, 1)], [("item", "minecraft:map", 3)]),
    ("waystone", "Ley Lines", "waystones:waystone",
     ["Waystones cannot be crafted cheaply: find one in a village and activate it. A warp stone needs a Wayfarer Shard."], ["first_ruin"],
     [("item", "waystones:warp_stone", 1)], [("item", "minecraft:ender_pearl", 4)]),
    ("village", "Civilisation", "minecraft:bell", ["Find a village. ChoiceTheorem's overhaul gives every biome its own style."], [],
     [("adv", "minecraft:adventure/trade")], [("item", "minecraft:emerald", 6)]),
    ("dungeon_arise", "When Dungeons Arise", "minecraft:spyglass",
     ["Massive hand-built dungeons are spread far apart. Use the spyglass and Voxy's view distance to spot them on the horizon."],
     ["first_ruin"], [("struct", "#horizon:arise_any")], [("item", SHARD, 2), ("xp", 5)]),
    ("frostmaw", "The Frozen Tyrant", "minecraft:blue_ice", ["A Frostmaw sleeps in cold biomes. Optional, very dangerous, very rewarding."],
     ["dungeon_arise"], [("kill", "mowziesmobs:frostmaw", 1)], [("item", CORE, 1)]),
    ("wroughtnaut", "Iron in the Dark", "minecraft:iron_block", ["Wrought chambers underground hold the Ferrous Wroughtnaut. Hit it from behind."],
     ["dungeon_arise"], [("kill", "mowziesmobs:ferrous_wroughtnaut", 1)], [("item", CORE, 1)]),
    ("core", "Ancient Power", CORE, ["Ancient Cores come from rare dungeons and mini-bosses. They gate the ME controller and give sockets."],
     ["dungeon_arise"], [("item", CORE, 1)], [("xp", 8)]),
]
C["3 - Forged in Adventure"] = [
    ("apoth_haven", "World Tier: Haven", "minecraft:iron_sword",
     ["Apotheosis loot is tiered. Your world tier rises as you progress, unlocking rarer affixes."], [],
     [("adv", "apotheosis:progression/haven")], [("xp", 2)]),
    ("apoth_frontier", "World Tier: Frontier", "minecraft:diamond_sword", ["Reach the Frontier tier. Purple and gold affixes begin to drop."],
     ["apoth_haven"], [("adv", "apotheosis:progression/frontier")], [("item", "apotheosis:gem_dust", 8)]),
    ("socket", "Socket and Gem", "apotheosis:sigil_of_socketing", ["Sigils of Socketing add gem slots. An Ancient Core + gem dust makes two."],
     ["apoth_frontier"], [("item", "apotheosis:sigil_of_socketing", 1)], [("item", "apotheosis:gem_dust", 8)]),
    ("enchant", "Deep Enchanting", "minecraft:enchanting_table",
     ["Apothic Enchanting adds Eterna, Quanta and Arcana. Bookshelves matter - experiment."], ["apoth_haven"],
     [("adv", "minecraft:story/enchant_item")], [("item", "minecraft:lapis_lazuli", 16)]),
    ("simply", "A Blade of Choice", "simplyswords:iron_longsword",
     ["Simply Swords weapons are sidegrades with movesets from Better Combat. Try a few - none is strictly best."], ["apoth_haven"],
     [("item", "#simplyswords:swords", 1)], [("xp", 3)]),
    ("artifact", "Curious Trinket", "artifacts:flippers", ["Artifacts and Relics appear in chests. Equip them in Curios slots (inventory button)."],
     ["apoth_haven"], [("item", "#artifacts:artifacts", 1)], [("xp", 4)]),
    ("apoth_ascent", "World Tier: Ascent", "minecraft:netherite_sword", ["Ascent loot is strong - so are the monsters."],
     ["apoth_frontier"], [("adv", "apotheosis:progression/ascent")], [("item", CORE, 1)]),
]
C["4 - Forgotten Realms"] = [
    ("nether", "We Need to Go Deeper", "minecraft:obsidian", ["Incendium reshapes the Nether into huge, hostile biomes."], [],
     [("dim", "minecraft:the_nether")], [("item", "minecraft:fire_resistance_potion" if False else "minecraft:golden_apple", 2)]),
    ("aether", "Above the Clouds", "minecraft:glowstone", ["Build a glowstone portal to the Aether. Three dungeons, three bosses."], [],
     [("adv", "aether:enter_aether")], [("item", "minecraft:feather", 8)]),
    ("aether_bronze", "The Slider", "aether:bronze_dungeon_key", ["Defeat the Slider in the bronze dungeon."], ["aether"],
     [("adv", "aether:bronze_dungeon")], [("item", CORE, 1)]),
    ("aether_gold", "The Sun Spirit", "aether:gold_dungeon_key", ["Defeat the Sun Spirit atop the gold dungeon."], ["aether_bronze"],
     [("adv", "aether:gold_dungeon")], [("item", HEART, 1)]),
    ("bumblezone", "Buzzing Mysteries", "minecraft:honeycomb", ["Throw an ender pearl into a bee nest to enter the Bumblezone."], [],
     [("dim", "the_bumblezone:the_bumblezone")], [("item", "minecraft:honey_bottle", 6)]),
    ("undergarden", "The Undergarden", "undergarden:catalyst", ["A catalyst lights a portal to the dim world below."], ["nether"],
     [("adv", "undergarden:undergarden/enter_undergarden")], [("xp", 5)]),
    ("forgotten_guardian", "The Forgotten Guardian", "undergarden:forgotten_ingot", ["Defeat the guardian in the catacombs."], ["undergarden"],
     [("adv", "undergarden:undergarden/kill_forgotten_guardian")], [("item", CORE, 1)]),
    ("otherside", "The Otherside", "minecraft:echo_shard", ["Beyond the Ancient Cities lies the Otherside (Deeper and Darker)."], ["nether"],
     [("adv", "deeperdarker:main/enter_otherside")], [("item", CORE, 1)]),
    ("end", "The End?", "minecraft:ender_eye", ["Nullscape turns the End into a vast, strange landscape - not a finish line."], ["nether"],
     [("dim", "minecraft:the_end")], [("xp", 10)]),
    ("dragon", "Free the End", "minecraft:dragon_head", ["The dragon is a beginning. The horizon goes much further."], ["end"],
     [("adv", "minecraft:end/kill_dragon")], [("item", HEART, 1)]),
]
C["5 - Arcane Studies"] = [
    ("ars_start", "Worn Notebook", "ars_nouveau:worn_notebook", ["Ars Nouveau: utility magic, mana and automation. Read the notebook."], [],
     [("item", "ars_nouveau:worn_notebook", 1)], [("item", "ars_nouveau:source_gem", 8)]),
    ("ars_book", "Novice Spellcaster", "ars_nouveau:novice_spell_book", ["Craft a spell book and design your first glyph combination."], ["ars_start"],
     [("adv", "ars_nouveau:novice_spell_book")], [("xp", 4)]),
    ("ars_apparatus", "Enchanting Apparatus", "ars_nouveau:enchanting_apparatus", ["The apparatus crafts most Ars items and enchants gear."],
     ["ars_book"], [("adv", "ars_nouveau:enchanting_apparatus")], [("item", "ars_nouveau:source_gem", 16)]),
    ("irons_start", "Inscription", "irons_spellbooks:inscription_table",
     ["Iron's Spells is combat magic: scrolls found in loot go into a spellbook at the inscription table."], [],
     [("adv", "irons_spellbooks:irons_spellbooks/make_inscription_table")], [("xp", 4)]),
    ("irons_anvil", "Arcane Anvil", "irons_spellbooks:arcane_anvil", ["Upgrade scrolls and imbue weapons."], ["irons_start"],
     [("adv", "irons_spellbooks:irons_spellbooks/make_arcane_anvil")], [("item", "irons_spellbooks:arcane_essence", 8)]),
    ("irons_catacombs", "The Catacombs", "irons_spellbooks:wayward_compass", ["The Dead King waits in the catacombs. Prepare."], ["irons_anvil"],
     [("adv", "irons_spellbooks:irons_spellbooks/enter_catacombs")], [("item", CORE, 1)]),
    ("occultism", "Spirits and Chalk", "occultism:chalk_white", ["Occultism summons spirits that mine, craft and store for you."], [],
     [("adv", "occultism:chalks/root")], [("xp", 4)]),
    ("legendary_ink", "Legendary Ink", "irons_spellbooks:legendary_ink", ["Legendary ink - or a Starforged Heart - writes the strongest scrolls."],
     ["irons_catacombs"], [("adv", "irons_spellbooks:irons_spellbooks/ink_legendary")], [("xp", 15)]),
]
C["6 - Mechanical Revolution"] = [
    ("andesite", "Andesite Alloy", "create:andesite_alloy", ["Create runs on rotation. Everything starts with andesite alloy."], [],
     [("adv", "create:andesite_alloy")], [("item", "create:cogwheel", 8)]),
    ("waterwheel", "Water Power", "create:water_wheel", ["Place a water wheel to generate stress units."], ["andesite"],
     [("item", "create:water_wheel", 1)], [("item", "create:shaft", 16)]),
    ("press", "Mechanical Press", "create:mechanical_press", ["Press plates automatically. Read Ponder scenes with &eW&r on any Create block."],
     ["waterwheel"], [("item", "create:mechanical_press", 1)], [("item", "create:andesite_casing", 8)]),
    ("belt", "Conveyor", "create:belt_connector", ["Belts move items and power. Your first production line."], ["press"],
     [("adv", "create:belt")], [("xp", 4)]),
    ("brass", "Brass Age", "create:brass_ingot", ["Brass unlocks logistics, mechanical crafters and arms."], ["belt"],
     [("adv", "create:brass")], [("item", "create:brass_casing", 8)]),
    ("electric", "Rotation to Power", "createaddition:electric_motor",
     ["Create Crafts & Additions converts rotation to FE and back - the bridge to every other tech mod."], ["brass"],
     [("item", "createaddition:alternator", 1)], [("xp", 6)]),
    ("liquid_xp", "Liquid Experience", "create_enchantment_industry:printer",
     ["Create Enchantment Industry automates enchanting with liquid XP - pair it with Apothic Enchanting."], ["brass"],
     [("item", "create_enchantment_industry:printer", 1)], [("xp", 6)]),
]
C["7 - Industrial Expansion"] = [
    ("mek_metallurgic", "Metallurgy", "mekanism:metallurgic_infuser", ["Mekanism's infuser makes steel and alloys."], [],
     [("item", "mekanism:metallurgic_infuser", 1)], [("item", "mekanism:ingot_osmium", 8)]),
    ("mek_ore", "Ore Multiplication", "mekanism:enrichment_chamber", ["Double, then triple, then quintuple your ores."], ["mek_metallurgic"],
     [("item", "mekanism:enrichment_chamber", 1)], [("xp", 5)]),
    ("mi_steam", "Steam Age", "modern_industrialization:bronze_boiler",
     ["Modern Industrialization starts with steam. Its multiblocks grow into a real industrial base."], [],
     [("item", "modern_industrialization:bronze_boiler", 1)], [("item", "modern_industrialization:bronze_ingot", 16)]),
    ("mi_ebf", "Electric Blast Furnace", "modern_industrialization:electric_blast_furnace", ["Your first big electric multiblock."],
     ["mi_steam"], [("adv", "modern_industrialization:electric_blast_furnace")], [("xp", 10)]),
    ("mi_distill", "Oil and Chemistry", "modern_industrialization:distillation_tower", ["Refine oil into fuels and plastics."], ["mi_ebf"],
     [("adv", "modern_industrialization:distillation_tower")], [("xp", 10)]),
    ("powah", "Simple Power", "powah:energizing_orb", ["Powah: generators and the energizing orb, easy to scale."], [],
     [("item", "powah:energizing_orb", 1)], [("xp", 4)]),
    ("cc", "Programmable World", "computercraft:computer_normal", ["CC: Tweaked computers and turtles can script anything."], [],
     [("item", "computercraft:computer_normal", 1)], [("xp", 4)]),
]
C["8 - The Digital Age"] = [
    ("ae_quartz", "Charged Quartz", "ae2:charged_certus_quartz_crystal", ["AE2 begins with certus quartz and a charger."], [],
     [("adv", "ae2:main/charged_quartz")], [("xp", 3)]),
    ("ae_presses", "Inscriber Presses", "ae2:inscriber", ["Presses come from meteorites. Find one with the meteorite compass."], ["ae_quartz"],
     [("adv", "ae2:main/presses")], [("item", SHARD, 2)]),
    ("ae_controller", "The Controller", "ae2:controller",
     ["An ME controller needs an &dAncient Core&r - the digital age starts with an expedition."], ["ae_presses"],
     [("adv", "ae2:main/controller")], [("item", "ae2:fluix_crystal", 16)]),
    ("ae_crafting", "Autocrafting", "ae2:crafting_unit", ["Build a crafting CPU and encode patterns."], ["ae_controller"],
     [("adv", "ae2:main/crafting_cpu")], [("xp", 10)]),
    ("ae_mek", "Chemical Network", "appmek:chemical_storage_cell_1k" if False else "ae2:pattern_provider",
     ["Applied Mekanistics lets AE2 store and autocraft Mekanism chemicals. Pattern providers drive Create and MI too."],
     ["ae_crafting"], [("item", "ae2:pattern_provider", 1)], [("xp", 8)]),
    ("ae_wireless", "Cut the Cord", "ae2wtlib:wireless_universal_terminal" if False else "ae2:wireless_terminal",
     ["Wireless terminals put the network in your pocket - on expeditions too."], ["ae_controller"],
     [("item", "ae2:wireless_terminal", 1)], [("xp", 5)]),
]
C["9 - Legends and Conquests"] = [
    ("cataclysm_find", "Ruins of Calamity", "minecraft:netherite_scrap", ["L_Ender's Cataclysm structures are legendary and rare. Find one."], [],
     [("adv", "cataclysm:root")], [("xp", 5)]),
    ("ignis", "Ignis", "minecraft:blaze_rod", ["The flame knight in the Burning Arena."], ["cataclysm_find"],
     [("adv", "cataclysm:kill_ignis")], [("item", HEART, 1)]),
    ("monstrosity", "Netherite Monstrosity", "minecraft:netherite_ingot", ["Found in the Soul Blacksmith."], ["cataclysm_find"],
     [("adv", "cataclysm:kill_monstrosity")], [("item", HEART, 1)]),
    ("leviathan", "The Leviathan", "minecraft:heart_of_the_sea", ["Beneath the Sunken City."], ["cataclysm_find"],
     [("adv", "cataclysm:kill_leviathan")], [("item", HEART, 1)]),
    ("harbinger", "The Harbinger", "minecraft:redstone_block", ["Deep in the Ancient Factory."], ["cataclysm_find"],
     [("adv", "cataclysm:kill_harbinger")], [("item", HEART, 1)]),
    ("wither", "Wither Storm Lite", "minecraft:wither_skeleton_skull", ["Summon and defeat the Wither."], [],
     [("adv", "minecraft:nether/summon_wither")], [("item", CORE, 2)]),
    ("warden", "Silence", "minecraft:sculk_catalyst", ["Defeat a Warden. Deeper and Darker gives a reason to."], [],
     [("adv", "deeperdarker:main/kill_warden")], [("item", HEART, 1)]),
    ("apoth_summit", "World Tier: Summit", "minecraft:nether_star", ["Summit: mythic affixes and the deadliest bosses."], [],
     [("adv", "apotheosis:progression/summit")], [("item", "apotheosis:sigil_of_enhancement", 1)]),
]
C["10 - Beyond the Horizon"] = [
    ("all_cataclysm", "Cataclysm Conqueror", "minecraft:dragon_egg", ["Defeat every Cataclysm boss."], [],
     [("adv", "cataclysm:kill_all_bosses")], [("item", HEART, 2)]),
    ("pinnacle", "World Tier: Pinnacle", "minecraft:beacon", ["The highest world tier. Everything is lethal; everything is worth it."], [],
     [("adv", "apotheosis:progression/pinnacle")], [("xp", 30)]),
    ("fusion_mek", "Star in a Jar", "mekanismgenerators:fusion_reactor_controller", ["Build a Mekanism fusion reactor (needs a Starforged Heart)."],
     [], [("item", "mekanismgenerators:fusion_reactor_controller", 1)], [("xp", 20)]),
    ("fusion_mi", "Plasma Engineering", "modern_industrialization:fusion_reactor", ["Build MI's fusion reactor."], [],
     [("item", "modern_industrialization:fusion_reactor", 1)], [("xp", 20)]),
    ("antimatter", "Antimatter", "mekanism:pellet_antimatter", ["The SPS turns polonium into antimatter."], ["fusion_mek"],
     [("adv", "mekanism:antimatter")], [("xp", 30)]),
    ("mega", "Unlimited Storage", "megacells:cell_component_256m", ["A 256M MEGA component - built from a Starforged Heart."], [],
     [("item", "megacells:cell_component_256m", 1)], [("xp", 20)]),
    ("archmage", "Archmage", "ars_nouveau:archmage_spell_book", ["Master Ars Nouveau."], [],
     [("adv", "ars_nouveau:archmage_spell_book")], [("xp", 20)]),
    ("bumble_all", "Bee Whisperer", "the_bumblezone:honey_crystal", ["Discover every Bumblezone biome."], [],
     [("adv", "the_bumblezone:biomes/discover_all_biomes")], [("item", HEART, 1)]),
]

# structure tag used by the WDA quest (any When Dungeons Arise structure)
ARISE_TAG = sorted(s for s in IDS["structure"] if s.startswith("dungeons_arise:"))


def check(kind, i):
    if i.startswith("#"):
        return i
    if i in HORIZON_ITEMS and kind == "item":
        return i
    if i.startswith("minecraft:") and kind in ("item", "entity", "advancement"):
        return i
    if kind == "dimension" and i in VANILLA_DIMS:
        return i
    if i not in IDS[kind]:
        raise SystemExit(f"unknown {kind}: {i}")
    return i


def task(t, n):
    k = t[0]
    if k == "adv":
        return {"type": "heracles:advancement", "advancements": [check("advancement", t[1])]}
    if k == "item":
        return {"type": "heracles:item", "item": check("item", t[1]), "amount": t[2], "collection": "AUTOMATIC"}
    if k == "dim":
        return {"type": "heracles:changed_dimension", "to": check("dimension", t[1])}
    if k == "kill":
        return {"type": "heracles:kill_entity", "entity": {"type": check("entity", t[1])}, "amount": t[2]}
    if k == "struct":
        return {"type": "heracles:structure", "structures": t[1] if t[1].startswith("#") else check("structure", t[1])}
    raise SystemExit(f"bad task {t}")


def reward(r):
    if r[0] == "item":
        return {"type": "heracles:item", "item": {"id": check("item", r[1]), "count": r[2]}}
    if r[0] == "xp":
        return {"type": "heracles:xp", "xptype": "LEVEL", "amount": r[1]}
    if r[0] == "loot":
        return {"type": "heracles:loottable", "loot_table": r[1]}
    raise SystemExit(f"bad reward {r}")


def layout(quests):
    depth = {}
    def d(q):
        if q[0] not in depth:
            depth[q[0]] = 0 if not q[4] else 1 + max(d(next(x for x in quests if x[0] == dep)) for dep in q[4])
        return depth[q[0]]
    rows = {}
    pos = {}
    for q in quests:
        col = d(q)
        row = rows.get(col, 0)
        rows[col] = row + 1
        pos[q[0]] = [col * 48, row * 40]
    return pos


def main():
    shutil.rmtree(OUT / "quests", ignore_errors=True)
    total = 0
    for chapter, quests in C.items():
        ids = {q[0] for q in quests}
        pos = layout(quests)
        folder = "".join(ch for ch in chapter.lower() if ch.isalnum())
        for qid, title, icon, desc, deps, tasks, rewards in quests:
            for dep in deps:
                assert dep in ids, f"{qid}: dependency {dep} not in chapter"
            quest = {
                "display": {"icon": {"type": "heracles:item", "item": {"id": check("item", icon)}},
                            "title": title, "description": desc, "groups": {chapter: {"position": pos[qid]}}},
                "settings": {"hidden": "LOCKED", "unlockNotification": True},
                "dependencies": [f"{folder}_{d}" for d in deps],
                "tasks": {f"t{i}": task(t, i) for i, t in enumerate(tasks)},
                "rewards": {f"r{i}": reward(r) for i, r in enumerate(rewards)},
            }
            p = OUT / "quests" / folder / f"{folder}_{qid}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(quest, indent=2), encoding="utf-8")
            total += 1
    (OUT / "groups.txt").write_text("\n".join(C.keys()) + "\n", encoding="utf-8")
    # structure tag for "any When Dungeons Arise structure"
    tag = ROOT / "datapacks/horizon/tags/worldgen/structure/arise_any.json"
    tag.parent.mkdir(parents=True, exist_ok=True)
    tag.write_text(json.dumps({"values": ARISE_TAG}, indent=1))
    print(f"{total} quests in {len(C)} chapters")


if __name__ == "__main__":
    main()
