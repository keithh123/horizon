"""Generate the Odyssey Quests (Heracles 2.0.x) quest book into config/heracles/.

Owns ONLY config/heracles/quests/ and config/heracles/groups.txt (patch_configs.py never touches them).
Quest ids are <chapterfolder>_<id>; ids from 0.1.0 are preserved.

Task shorthand:  ("adv", "ns:path")  ("item", "ns:id" | "#tag", count)  ("dim", "ns:dim")  ("check",)
                 ("recipe", ["ns:recipe", ...])  ("block", "ns:block" | "#tag")
Reward shorthand: ("item", "ns:id", count[, components])  ("xp", levels)  ("loot", "ns:table")

Design rules (checked at build time):
  * Exploration, kills and dimensions use advancements (retroactive: Heracles' AdvancementTask checks existing
    advancements when the quest unlocks; dimension/structure/kill tasks are NOT retroactive).
  * Boss relics come from horizon:legend/* first-kill advancements, never from quest rewards.
  * No quest reward may complete another quest's item task (no reward chains / shortcuts).
"""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
IDS = {k: set(v) for k, v in json.loads((ROOT / "manifests/ids.json").read_text()).items()}
FAM = json.loads((ROOT / "manifests/loot_families.json").read_text(encoding="utf-8"))
LEG = json.loads((ROOT / "manifests/legends.json").read_text(encoding="utf-8"))
EXP = json.loads((ROOT / "manifests/expeditions.json").read_text(encoding="utf-8"))
GEN = json.loads((ROOT / "datapacks/.generated.json").read_text())["files"] + \
    json.loads((ROOT / "datapacks/.generated-hq.json").read_text())["files"]   # headquarters mirrors/recipes (gen_headquarters.py)
HQ = json.loads((ROOT / "manifests/headquarters.json").read_text(encoding="utf-8"))
HORIZON_ADV = {"horizon:" + f.split("horizon/advancement/")[1][:-5] for f in GEN if f.startswith("horizon/advancement/")}
HORIZON_LOOT = {"horizon:" + f.split("horizon/loot_table/")[1][:-5] for f in GEN if f.startswith("horizon/loot_table/")}
HORIZON_RECIPES = {"horizon:" + f.split("horizon/recipe/")[1][:-5] for f in GEN if f.startswith("horizon/recipe/")}
ASSETS = json.loads((ROOT / "kubejs/.generated-assets.json").read_text())["files"]
HORIZON_ITEMS = set(HQ["items"]) | set(HQ["blocks"]) | {f"horizon:emblem_{s['id']}" for s in HQ["stages"]} | \
                {"horizon:" + f.rsplit("/", 1)[1][:-4] for f in ASSETS if "/textures/item/" in f} | \
                {"horizon:" + f.rsplit("/", 1)[1][:-4] for f in ASSETS if "/textures/block/trophy_" in f}
OUT = ROOT / "config" / "heracles"
VANILLA_DIMS = {"minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"}
SHARD, CORE, HEART = "horizon:wayfarer_shard", "horizon:ancient_core", "horizon:starforged_heart"
F = FAM["families"]


def fam_desc(f):
    d = F[f]
    return [d["identity"], "", "&ePrepare:&r " + d["prep"], "&eSignature rewards:&r " + d["signature"],
            "&eComing back:&r " + d["repeat"], "&eFeeds into:&r " + d["connects"], "&eBrings home:&r " + d["home"]]


C = {}
C["1 - The First Steps"] = [
    ("welcome", "Welcome to the Horizon", "minecraft:compass",
     ["The world is enormous. Mountains here are real mountains, and with Voxy you can see them from very far away.",
      "This book is a guide, not a checklist: every chapter is optional. Follow what interests you.",
      "Press &eJ&r any time to reopen it (keybinds are searchable in Options > Controls).",
      "Dying drops your items into a &ecorpse&r at the spot (also in the void): go back for it."],
     [], [("check",)], [("item", "minecraft:bread", 8), ("item", "heracles:quest_book", 1)]),
    ("wood", "Timber!", "minecraft:oak_log", ["Gather wood for tools and a first shelter."], ["welcome"],
     [("item", "#minecraft:logs", 16)], [("item", "minecraft:torch", 16)]),
    ("stone_age", "Stone Age", "minecraft:stone_pickaxe", ["Mine stone and craft better tools."], ["wood"],
     [("adv", "minecraft:story/mine_stone")], [("xp", 2)]),
    ("iron", "Iron Will", "minecraft:iron_ingot", ["Smelt iron. Most of the pack's machines start here."], ["stone_age"],
     [("adv", "minecraft:story/smelt_iron")], [("item", "minecraft:iron_ingot", 6)]),
    ("bed", "A Place to Rest", "minecraft:red_bed", ["Sleep through your first night. Bosses and dungeons do not rest - you should."], ["wood"],
     [("adv", "minecraft:adventure/sleep_in_bed")], [("item", "minecraft:campfire", 1), ("xp", 2)]),
    ("kitchen", "Hearty Meals", "farmersdelight:cooking_pot",
     ["Farmer's Delight meals give long buffs - the cheapest expedition preparation there is. AppleSkin shows saturation on hover.",
      "&7(Introductory item task: craft or hold a cooking pot.)"], ["iron"],
     [("item", "farmersdelight:cooking_pot", 1)], [("item", "minecraft:golden_carrot", 8)]),
    ("backpack", "Pack Mule", "sophisticatedbackpacks:backpack", ["A backpack makes long expeditions possible.",
     "&7(Introductory item task.)"], ["iron"], [("item", "sophisticatedbackpacks:backpack", 1)], [("xp", 3)]),
    ("diamonds", "Diamonds!", "minecraft:diamond", ["Deep caves under Terralith's mountains hide diamonds - and danger."], ["iron"],
     [("adv", "minecraft:story/mine_diamond")], [("item", "minecraft:spyglass", 1)]),
]
C["2 - The Wild Frontier"] = [
    ("first_ruin", "Something Old", "minecraft:mossy_cobblestone",
     ["Find any roadside ruin, camp, shrine or watchtower. Small sites are where &aWayfarer Shards&r come from.",
      "Completes when you step inside one (also if you already have)."], [],
     [("adv", "horizon:atlas/roadside")], [("item", "minecraft:map", 3), ("item", "simplehats:explorerhat", 1)]),
    ("waystone", "Ley Lines", "waystones:waystone",
     ["Waystones stand in villages and some ruins. Right-click one to activate it - it becomes a fast-travel destination.",
      "A personal &eWarp Stone&r costs a Wayfarer Shard; &eWarp Scrolls&r turn up in village chests."], ["first_ruin"],
     [("block", "#waystones:waystones")], [("item", "minecraft:ender_pearl", 4)]),
    ("village", "Civilisation", "minecraft:bell", ["Find a village and trade. ChoiceTheorem's overhaul gives every biome its own style.",
     "Cartographer chests often hold a &6Surveyor's Chart&r pointing at a great landmark."], [],
     [("adv", "minecraft:adventure/trade")], [("item", "minecraft:emerald", 6)]),
    ("dungeon_arise", "When Dungeons Arise", "minecraft:spyglass",
     ["Massive hand-built landmarks are spread far apart. Spot them on the horizon (Voxy), or follow a Surveyor's Chart.",
      "Completes when you enter a great landmark. Here is a chart to get you started."], ["first_ruin"],
     [("adv", "horizon:atlas/landmark")], [("loot", "horizon:rewards/quest/chart_landmark"), ("xp", 5)]),
    ("frostmaw", "The Frozen Tyrant", "minecraft:blue_ice",
     ["A Frostmaw sleeps in cold biomes. Optional, dangerous - and its first defeat gives you an Ancient Core and a trophy."],
     ["dungeon_arise"], [("adv", "horizon:legend/frostmaw")], [("xp", 8), ("item", "simplehats:icedragonskull", 1)]),
    ("wroughtnaut", "Iron in the Dark", "minecraft:iron_block",
     ["Wrought chambers underground hold the Ferrous Wroughtnaut. Hit it from behind. First defeat: Ancient Core + trophy."],
     ["dungeon_arise"], [("adv", "horizon:legend/ferrous_wroughtnaut")], [("xp", 8), ("item", "simplehats:fullironhelm", 1)]),
    ("core", "Ancient Power", CORE,
     ["Ancient Cores come from temple and landmark treasure rooms and from a mini-boss's first defeat.",
      "They build the ME controller and socketing sigils. &7(Item task.)"], ["dungeon_arise"],
     [("item", CORE, 1)], [("xp", 8)]),
]
C["3 - Forged in Adventure"] = [
    ("apoth_haven", "World Tier: Haven", "minecraft:iron_sword",
     ["Apotheosis loot is tiered. Your world tier rises as you progress, unlocking rarer affixes."], [],
     [("adv", "apotheosis:progression/haven")], [("xp", 2)]),
    ("apoth_frontier", "World Tier: Frontier", "minecraft:diamond_sword", ["Reach the Frontier tier. Purple and gold affixes begin to drop."],
     ["apoth_haven"], [("adv", "apotheosis:progression/frontier")], [("item", "apotheosis:gem_dust", 8)]),
    ("socket", "Socket and Gem", "apotheosis:sigil_of_socketing",
     ["Sigils of Socketing add gem slots. An Ancient Core + 2 gem dust makes two. &7(Item task.)"],
     ["apoth_frontier"], [("item", "apotheosis:sigil_of_socketing", 1)], [("item", "apotheosis:gem_dust", 8)]),
    ("enchant", "Deep Enchanting", "minecraft:enchanting_table",
     ["Apothic Enchanting adds Eterna, Quanta and Arcana. Bookshelves matter - experiment."], ["apoth_haven"],
     [("adv", "minecraft:story/enchant_item")], [("item", "minecraft:lapis_lazuli", 16)]),
    ("simply", "A Blade of Choice", "simplyswords:iron_longsword",
     ["Simply Swords weapons are sidegrades with movesets from Better Combat. Try a few - none is strictly best.",
      "Uniques have their own abilities; duplicates salvage into shards at Apotheosis' salvaging table."], ["apoth_haven"],
     [("item", "#simplyswords:swords", 1)], [("xp", 3)]),
    ("artifact", "Curious Trinket", "artifacts:flippers", ["Artifacts and Relics appear in chests. Equip them in Curios slots (inventory button).",
     "Duplicates salvage into shards and gem dust."], ["apoth_haven"], [("item", "#artifacts:artifacts", 1)], [("xp", 4)]),
    ("apoth_ascent", "World Tier: Ascent", "minecraft:netherite_sword", ["Ascent loot is strong - so are the monsters."],
     ["apoth_frontier"], [("adv", "apotheosis:progression/ascent")], [("item", "apotheosis:gem_dust", 16), ("xp", 10)]),
]
C["4 - Forgotten Realms"] = [
    ("nether", "We Need to Go Deeper", "minecraft:obsidian", ["Incendium reshapes the Nether into huge, hostile biomes."], [],
     [("adv", "minecraft:story/enter_the_nether")], [("item", "minecraft:golden_apple", 2)]),
    ("aether", "Above the Clouds", "minecraft:glowstone", ["Build a glowstone portal to the Aether. Three dungeons, three bosses."], [],
     [("adv", "aether:enter_aether")], [("item", "minecraft:feather", 8)]),
    ("aether_bronze", "Stop the Slider", "aether:bronze_dungeon_key", ["Defeat the Slider in the bronze dungeon (first defeat: Ancient Core + trophy)."],
     ["aether"], [("adv", "aether:bronze_dungeon")], [("xp", 8)]),
    ("aether_gold", "The Sun Spirit", "aether:gold_dungeon_key", ["Defeat the Sun Spirit atop the gold dungeon (first defeat: Starforged Heart + trophy)."],
     ["aether_bronze"], [("adv", "aether:gold_dungeon")], [("xp", 15), ("item", "simplehats:halo", 1)]),
    ("bumblezone", "Buzzing Mysteries", "minecraft:honeycomb", ["Throw an ender pearl into a bee nest to enter the Bumblezone."], [],
     [("dim", "the_bumblezone:the_bumblezone")], [("item", "minecraft:honey_bottle", 6)]),
    ("undergarden", "The Undergarden", "undergarden:catalyst", ["A catalyst lights a portal to the dim world below."], ["nether"],
     [("adv", "undergarden:undergarden/enter_undergarden")], [("xp", 5)]),
    ("forgotten_guardian", "The Forgotten Guardian", "undergarden:forgotten_ingot", ["Defeat the guardian in the catacombs."], ["undergarden"],
     [("adv", "undergarden:undergarden/kill_forgotten_guardian")], [("xp", 10)]),
    ("otherside", "The Otherside", "minecraft:echo_shard", ["Beyond the Ancient Cities lies the Otherside (Deeper and Darker)."], ["nether"],
     [("adv", "deeperdarker:main/enter_otherside")], [("xp", 10)]),
    ("end", "The End?", "minecraft:ender_eye", ["Nullscape turns the End into a vast, strange landscape - not a finish line."], ["nether"],
     [("adv", "minecraft:story/enter_the_end")], [("xp", 10)]),
    ("dragon", "Free the End", "minecraft:dragon_head", ["The dragon is a beginning. Its first defeat gives a Starforged Heart and a trophy;",
     "re-summoned dragons give their usual drops only."], ["end"],
     [("adv", "minecraft:end/kill_dragon")], [("xp", 20), ("item", "simplehats:dragonskullender", 1)]),
]
C["5 - Arcane Studies"] = [
    ("ars_start", "Worn Notebook", "ars_nouveau:worn_notebook", ["Ars Nouveau: utility magic, mana and automation. Read the notebook.",
     "&7Optional route: none of the magic mods is required for tech progression."], [],
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
    ("irons_catacombs", "The Catacombs", "irons_spellbooks:wayward_compass", ["The Dead King waits in the catacombs. Prepare.",
     "His first defeat gives an Ancient Core and a trophy."], ["irons_anvil"],
     [("adv", "irons_spellbooks:irons_spellbooks/enter_catacombs")], [("xp", 8), ("item", "simplehats:amalgalichhat", 1)]),
    ("occultism", "Spirits and Chalk", "occultism:chalk_white", ["Occultism summons spirits that mine, craft and store for you."], [],
     [("adv", "occultism:chalks/root")], [("xp", 4)]),
    ("legendary_ink", "Legendary Ink", "irons_spellbooks:legendary_ink", ["Legendary ink - or a Starforged Heart - writes the strongest scrolls."],
     ["irons_catacombs"], [("adv", "irons_spellbooks:irons_spellbooks/ink_legendary")], [("xp", 15)]),
]
C["6 - Mechanical Revolution"] = [
    ("andesite", "Andesite Alloy", "create:andesite_alloy", ["Create runs on rotation. Everything starts with andesite alloy."], [],
     [("adv", "create:andesite_alloy")], [("item", "create:cogwheel", 8)]),
    ("waterwheel", "Water Power", "create:water_wheel", ["Place a water wheel in flowing water to generate stress units."], ["andesite"],
     [("adv", "create:water_wheel")], [("item", "create:shaft", 16)]),
    ("press", "Mechanical Press", "create:mechanical_press", ["Press plates automatically. Read Ponder scenes with &eW&r on any Create block."],
     ["waterwheel"], [("adv", "create:mechanical_press")], [("item", "create:andesite_casing", 8)]),
    ("belt", "Conveyor", "create:belt_connector", ["Belts move items and power. Your first production line."], ["press"],
     [("adv", "create:belt")], [("xp", 4)]),
    ("brass", "Brass Age", "create:brass_ingot", ["Brass unlocks logistics, mechanical crafters and arms."], ["belt"],
     [("adv", "create:brass")], [("item", "create:brass_casing", 8)]),
    ("electric", "Rotation to Power", "createaddition:electric_motor",
     ["Create Crafts & Additions converts rotation to FE and back - the bridge to every other tech mod.",
      "&7(Item task: craft an alternator. Crafts & Additions has no advancements to prove it is running.)"], ["brass"],
     [("item", "createaddition:alternator", 1)], [("xp", 6)]),
    ("liquid_xp", "Liquid Experience", "create_enchantment_industry:printer",
     ["Create Enchantment Industry automates enchanting with liquid XP - pair it with Apothic Enchanting."], ["brass"],
     [("adv", "create_enchantment_industry:experienced_engineer")], [("xp", 6)]),
]
C["7 - Industrial Expansion"] = [
    ("mek_metallurgic", "Metallurgy", "mekanism:metallurgic_infuser", ["Mekanism's infuser makes steel and alloys."], [],
     [("adv", "mekanism:metallurgic_infuser")], [("item", "mekanism:ingot_osmium", 8)]),
    ("mek_ore", "Ore Multiplication", "mekanism:enrichment_chamber", ["Double, then triple, then quintuple your ores.",
     "Completes on Mekanism's own advancement for the enrichment chamber."], ["mek_metallurgic"],
     [("adv", "mekanism:enricher")], [("xp", 5)]),
    ("mi_steam", "Steam Age", "modern_industrialization:bronze_boiler",
     ["Modern Industrialization starts with steam. Its multiblocks grow into a real industrial base.",
      "Completes on MI's bronze furnace advancement."], [],
     [("adv", "modern_industrialization:bronze_furnace")], [("item", "modern_industrialization:bronze_ingot", 16)]),
    ("mi_ebf", "Electric Blast Furnace", "modern_industrialization:electric_blast_furnace", ["Your first big electric multiblock."],
     ["mi_steam"], [("adv", "modern_industrialization:electric_blast_furnace")], [("xp", 10)]),
    ("mi_distill", "Oil and Chemistry", "modern_industrialization:distillation_tower", ["Refine oil into fuels and plastics."], ["mi_ebf"],
     [("adv", "modern_industrialization:distillation_tower")], [("xp", 10)]),
    ("powah", "Simple Power", "powah:energizing_orb", ["Powah: generators and the energizing orb, easy to scale.",
     "&7(Item task - Powah has no advancements.)"], [], [("item", "powah:energizing_orb", 1)], [("xp", 4)]),
    ("cc", "Programmable World", "computercraft:computer_normal", ["CC: Tweaked computers and turtles can script anything.",
     "&7(Item task.)"], [], [("item", "computercraft:computer_normal", 1)], [("xp", 4)]),
]
C["8 - The Digital Age"] = [
    ("ae_quartz", "Charged Quartz", "ae2:charged_certus_quartz_crystal", ["AE2 begins with certus quartz and a charger."], [],
     [("adv", "ae2:main/charged_quartz")], [("xp", 3)]),
    ("ae_presses", "Inscriber Presses", "ae2:inscriber", ["Presses come from meteorites. Find one with the meteorite compass."], ["ae_quartz"],
     [("adv", "ae2:main/presses")], [("xp", 5)]),
    ("ae_controller", "The Controller", "ae2:controller",
     ["An ME controller needs an &bAncient Core&r - the digital age starts with an expedition."], ["ae_presses"],
     [("adv", "ae2:main/controller")], [("item", "ae2:fluix_crystal", 16)]),
    ("ae_crafting", "Autocrafting", "ae2:crafting_unit", ["Build a crafting CPU and encode patterns."], ["ae_controller"],
     [("adv", "ae2:main/crafting_cpu")], [("xp", 10)]),
    ("ae_mek", "Chemical Storage", "appmek:chemical_storage_cell_1k",
     ["Applied Mekanistics lets AE2 store Mekanism chemicals and autocraft with them.",
      "&7(Item task: craft a 1k chemical storage cell. Applied Mekanistics has no advancements, so the quest cannot",
      "see the cell actually holding gas - fill it yourself.)"],
     ["ae_crafting"], [("item", "appmek:chemical_storage_cell_1k", 1)], [("xp", 8)]),
    ("ae_wireless", "Cut the Cord", "ae2:wireless_terminal",
     ["Wireless terminals put the network in your pocket - on expeditions too. &7(Item task.)"], ["ae_controller"],
     [("item", "ae2:wireless_terminal", 1)], [("xp", 5)]),
]
C["9 - Legends and Conquests"] = [
    ("cataclysm_find", "Ruins of Calamity", "minecraft:netherite_scrap", ["L_Ender's Cataclysm structures are legendary and rare. Find one."], [],
     [("adv", "cataclysm:root")], [("xp", 5)]),
    ("ignis", "Quench the Flame Knight", "minecraft:blaze_rod", ["The flame knight in the Burning Arena. First defeat: Starforged Heart + trophy."], ["cataclysm_find"],
     [("adv", "horizon:legend/ignis")], [("xp", 15)]),
    ("monstrosity", "Break the Monstrosity", "minecraft:netherite_ingot", ["Found in the Soul Blacksmith."], ["cataclysm_find"],
     [("adv", "horizon:legend/netherite_monstrosity")], [("xp", 15)]),
    ("leviathan", "Surface the Leviathan", "minecraft:heart_of_the_sea", ["Beneath the Sunken City."], ["cataclysm_find"],
     [("adv", "horizon:legend/the_leviathan")], [("xp", 15)]),
    ("harbinger", "Shut Down the Harbinger", "minecraft:redstone_block", ["Deep in the Ancient Factory."], ["cataclysm_find"],
     [("adv", "horizon:legend/the_harbinger")], [("xp", 15)]),
    ("wither", "Wither Storm Lite", "minecraft:wither_skeleton_skull",
     ["Summon and defeat the Wither. The first defeat (per player) gives a Starforged Heart and a trophy;",
      "later Withers drop their nether star only, so a Wither farm cannot mint relics."], [],
     [("adv", "horizon:legend/wither")], [("xp", 15)]),
    ("warden", "Silence", "minecraft:sculk_catalyst", ["Defeat a Warden. The first defeat counts for a heart; summoned Wardens after that do not."], [],
     [("adv", "horizon:legend/warden")], [("xp", 15)]),
    ("apoth_summit", "World Tier: Summit", "minecraft:nether_star", ["Summit: mythic affixes and the deadliest bosses."], [],
     [("adv", "apotheosis:progression/summit")], [("item", "apotheosis:sigil_of_enhancement", 1)]),
]
C["10 - Beyond the Horizon"] = [
    ("all_cataclysm", "Cataclysm Conqueror", "minecraft:dragon_egg", ["Defeat every Cataclysm boss."], [],
     [("adv", "cataclysm:kill_all_bosses")], [("item", "apotheosis:sigil_of_enhancement", 1), ("xp", 30), ("item", "simplehats:bigcrown", 1)]),
    ("pinnacle", "World Tier: Pinnacle", "minecraft:beacon", ["The highest world tier. Everything is lethal; everything is worth it."], [],
     [("adv", "apotheosis:progression/pinnacle")], [("xp", 30)]),
    ("fusion_mek", "Star in a Jar", "mekanismgenerators:fusion_reactor_controller", ["Build a Mekanism fusion reactor (needs a Starforged Heart).",
     "&7(Item task: the controller. Form the reactor and ignite it to make it useful.)"],
     [], [("item", "mekanismgenerators:fusion_reactor_controller", 1)], [("xp", 20)]),
    ("fusion_mi", "Plasma Engineering", "modern_industrialization:fusion_reactor", ["Build MI's fusion reactor (needs a Starforged Heart).",
     "&7(Item task: the controller block.)"], [], [("item", "modern_industrialization:fusion_reactor", 1)], [("xp", 20)]),
    ("antimatter", "Antimatter", "mekanism:pellet_antimatter", ["The SPS turns polonium into antimatter."], ["fusion_mek"],
     [("adv", "mekanism:antimatter")], [("xp", 30)]),
    ("mega", "Unlimited Storage", "megacells:cell_component_256m", ["A 256M MEGA component - built from a Starforged Heart. &7(Item task.)"], [],
     [("item", "megacells:cell_component_256m", 1)], [("xp", 20)]),
    ("archmage", "Archmage", "ars_nouveau:archmage_spell_book", ["Master Ars Nouveau."], [],
     [("adv", "ars_nouveau:archmage_spell_book")], [("xp", 20)]),
    ("bumble_all", "Bee Whisperer", "the_bumblezone:honey_crystal", ["Discover every Bumblezone biome."], [],
     [("adv", "the_bumblezone:biomes/discover_all_biomes")], [("item", "horizon:honeyed_seal", 4), ("xp", 15)]),
]

# ---------------------------------------------------------------- new chapters

# Hall of Legends: one small tree per realm, left to right (great-legend realms in the middle, under the Curator).
# boss -> (prerequisite boss or None = the Hall, column inside the realm, row). Prerequisites follow each mod's own
# progression (Aether keys, Deeper Darker's Otherside behind the Warden, Ender Golems guarding the Ender Guardian ...).
# Great legends never wait on a lesser one (except the Aether, where the game itself requires it), so the Curator only
# needs each realm's last great legend: every great legend is still required, through the chain.
# Kill credit is retroactive, so a boss beaten out of order completes as soon as its node unlocks.
REALMS = [
    ("Mowzie's Mobs", {"ferrous_wroughtnaut": (None, 0.5, 1), "frostmaw": ("ferrous_wroughtnaut", 0, 2),
                       "umvuthi": ("ferrous_wroughtnaut", 1, 2), "sculptor": ("umvuthi", 1, 3)}),
    ("Bosses of Mass Destruction", {"lich": (None, 0.5, 1), "obsidilith": ("lich", 0, 2), "gauntlet": ("lich", 1, 2),
                                    "void_blossom": ("gauntlet", 1, 3)}),
    ("Overworld and Vanilla", {"elder_guardian": (None, 0, 1), "wither": (None, 1, 1), "ender_dragon": ("wither", 1, 2),
                               "warden": (None, 2, 1), "stalker": ("warden", 2, 2), "dead_king": ("warden", 3, 2)}),
    ("Cataclysm: Nether and End", {"netherite_monstrosity": (None, 0, 1), "ignis": ("netherite_monstrosity", 0, 2),
                                   "maledictus": ("ignis", 0, 3), "ender_guardian": (None, 1.5, 1),
                                   "the_harbinger": ("ender_guardian", 1, 2), "ender_golem": ("ender_guardian", 2, 2)}),
    ("Cataclysm: Sea, Sand and Ruins", {"the_leviathan": (None, 0.5, 1), "scylla": ("the_leviathan", 0, 2),
                                        "clawdian": ("the_leviathan", 1, 2), "ancient_remnant": (None, 2, 1),
                                        "the_prowler": ("ancient_remnant", 2, 2)}),
    ("The Aether", {"slider": (None, 0, 1), "valkyrie_queen": ("slider", 0, 2), "sun_spirit": ("valkyrie_queen", 0, 3)}),
    ("Block Factory's Bosses", {"yeti": (None, 0.5, 1), "kraken": ("yeti", 0, 2), "infernal_dragon": ("kraken", 0, 3),
                                "sandworm": ("yeti", 1, 2), "underworld_knight": ("sandworm", 1, 3)}),
    ("Other realms", {"forgotten_guardian": (None, 0, 1), "cosmic_crystal_entity": (None, 1, 1.4), "sacred_pontiff": (None, 2, 1)}),
]
LEGEND_TREE = {b: v for _, t in REALMS for b, v in t.items()}
REALM_OF = {f"legend_{b}": r for r, t in REALMS for b in t}
MAJOR_IDS = {f"legend_{b['id'].split(':')[1]}" for b in LEG["bosses"] if b["tier"] == "major"}
_all = [b["id"].split(":")[1] for b in LEG["bosses"]]
assert sorted(_all) == sorted(LEGEND_TREE), "REALMS must list every boss exactly once"
assert all(p is None or p in LEGEND_TREE for p, _, _ in LEGEND_TREE.values()), "REALMS prerequisite is not a boss"
# Curator prerequisites: great legends that no other great legend builds on
_major_parents = {LEGEND_TREE[m[7:]][0] for m in MAJOR_IDS}
CURATOR_DEPS = sorted(m for m in MAJOR_IDS if m[7:] not in _major_parents)
def _ancestors(b):
    out = set()
    while b:
        out.add(b)
        b = LEGEND_TREE[b][0]
    return out
assert {m[7:] for m in MAJOR_IDS} <= set().union(*(_ancestors(m[7:]) for m in CURATOR_DEPS)), "Curator must cover every great legend"

ATLAS_GROUPS = [("Roads and settlements", ["settlement", "roadside", "landmark"]), ("Underground and sea", ["underground", "ocean", "deep"]),
                ("Magic and nature", ["temple", "arcane", "hive"]), ("Other dimensions", ["nether", "aether", "end"]), ("Boss lairs", ["boss_lair"])]
ATLAS_ORDER = ["settlement", "roadside", "underground", "ocean", "hive", "temple", "arcane", "nether", "aether", "deep", "landmark", "end", "boss_lair"]
atlas = [("atlas", "Reading the Atlas", "minecraft:filled_map",
          ["Every structure in this world belongs to an expedition family with its own rewards. Each quest in this chapter",
           "explains one family: what it is, how to prepare, what it gives, and why it is worth coming back.",
           "Rewards are budgeted per structure: a palace is worth more than a shrine, but no single place floods you.",
           "&7Each quest completes the first time you step inside a structure of that family (also retroactively)."],
          [], [("check",)], [("item", "minecraft:map", 2)])]
for f in ATLAS_ORDER:
    d = F[f]
    rew = [("xp", {"early": 3, "early-mid": 5, "mid": 8, "mid-late": 12, "late": 15, "early-late": 6}[d["stage"]])]
    if f in ("settlement", "roadside"):
        rew.append(("loot", "horizon:rewards/quest/chart_temple"))
    atlas.append((f"atlas_{f}", d["title"], d["icon"], [f"&7Stage: {d['stage']}&r"] + fam_desc(f), ["atlas"],
                  [("adv", f"horizon:atlas/{f}")], rew))
atlas += [
    ("exchange", "Expedition Exchange", "horizon:cinder_idol",
     ["Each realm has its own token: Tidebound Doubloons (ocean), Cinder Idols (Nether), Starlit Voidglass (End),",
      "Skyward Plumes (Aether), Echoing Fossils (the Deep) and Honeyed Seals (Bumblezone).",
      "6 tokens + 2 gem dust buy a &echosen&r Apotheosis gem at its lowest purity - then cut it up yourself.",
      "This is targeted progress, not a shop: no affix gear, no top purities, and tokens cannot be crafted."], ["atlas"],
     [("item", "#horizon:tokens", 1)], [("item", "apotheosis:gem_dust", 4)]),
    ("exchange_gem", "A Gem of Your Choosing", "apotheosis:gem_cutting_table",
     ["Craft any Expedition Exchange gem (EMI: search the horizon_exchange recipes)."], ["exchange"],
     [("recipe", sorted(r for r in HORIZON_RECIPES if r.startswith("horizon:exchange/")))], [("xp", 8)]),
    ("salvage", "Nothing Wasted", "apotheosis:salvaging_table",
     ["Duplicate Artifacts, Relics and Simply Swords uniques salvage into Wayfarer Shards and gem dust (uniques can",
      "also give an Ancient Core) at Apotheosis' salvaging table. Only loot-only items salvage - nothing farmable.",
      "&7(Item task: build a salvaging table.)"], ["atlas"],
     [("item", "apotheosis:salvaging_table", 1)], [("xp", 5)]),
]
C["11 - Expedition Atlas"] = atlas

legends = [("hall", "The Hall of Legends", "horizon:trophy_ignis",
            ["Every great foe gives its first slayer (and everyone fighting within 96 blocks) a relic and a &etrophy&r -",
             "a display block for your base. Great bosses give a Starforged Heart, lesser ones an Ancient Core.",
             "The reward is once per player, so summonable bosses (Wither, Warden, re-summoned Dragon) cannot be farmed for relics.",
             "&7Each quest completes when you are credited with the kill (also retroactively)."], [], [("check",)], [("xp", 2)])]
for b in LEG["bosses"]:
    p = b["id"].split(":")[1]
    tier = "great" if b["tier"] == "major" else "lesser"
    legends.append((f"legend_{p}", b["name"], f"horizon:trophy_{p}",
                    [f"A {tier} legend. First defeat: {'Starforged Heart' if b['tier'] == 'major' else 'Ancient Core'} + trophy."],
                    [f"legend_{LEGEND_TREE[p][0]}" if LEGEND_TREE[p][0] else "hall"],
                    [("adv", f"horizon:legend/{p}")], [("xp", 10 if b["tier"] == "major" else 5)]))
legends.append(("hall_complete", "Curator of Legends", "minecraft:lodestone",
                ["Defeat every great legend. The reward is a pearl for the Horizon Gauntlet.",
                 "&7Each realm's path ends in its greatest foe; the Curator waits at the end of all of them."], CURATOR_DEPS, [("check",)],
                [("item", "gateways:gate_pearl", 1, {"gateways:gateway": "horizon:trial/horizon"}), ("xp", 50), ("item", "simplehats:crown", 1)]))
C["12 - Hall of Legends"] = legends

mastery = [("builds", "Choosing a Build", "minecraft:armor_stand",
            ["Apotheosis is the backbone: affixes, gems and world tiers apply to every weapon and armour piece,",
             "including Simply Swords, Cataclysm and Aether gear. Accessories (Artifacts, Relics) add a second layer in Curios slots.",
             "Pick a direction - the quests below are guides, not requirements. Mixing is fine."], [], [("check",)], [("xp", 2)]),
           ("build_crit", "Fast Blades", "simplyswords:iron_rapier",
            ["&eFast melee and crit:&r rapiers, katanas, sais and twinblades (Better Combat combos).",
             "Look for crit chance/damage affixes, &eSamurai&r and &eSlipstream&r gems (Slipstream: Tidebound Doubloons).",
             "Accessories: speed and attack-speed artifacts."], ["builds"], [("check",)], [("xp", 3)]),
           ("build_heavy", "Breaker", "simplyswords:iron_greathammer",
            ["&eHeavy melee and stagger:&r greathammers, greataxes, claymores. Slow swings, big hits, knockback and armour shred.",
             "Look for &eBreach&r (armour pierce, Echoing Fossils), &eBallast&r and &eWarlord&r gems; Cataclysm gear for late game."],
            ["builds"], [("check",)], [("xp", 3)]),
           ("build_tank", "Bulwark", "minecraft:iron_chestplate",  # shield renders blank in Heracles (special item renderer)
            ["&eDefensive sustain:&r shields, armour/protection affixes, life steal and regeneration.",
             "Look for &eGuardian&r (Echoing Fossils) and &eLunar&r gems, Relics with healing, Farmer's Delight buffs."],
            ["builds"], [("check",)], [("xp", 3)]),
           ("build_ranged", "Deadeye", "minecraft:bow",
            ["&eRanged:&r bows and crossbows take Apotheosis ranged affixes (arrow damage/velocity, snipe, volley).",
             "Solar and Lightning gems (Skyward Plumes) suit fast bows; arrow quivers from Relics help."], ["builds"], [("check",)], [("xp", 3)]),
           ("build_spell", "Spellblade and Scholar", "irons_spellbooks:inscription_table",
            ["&eElemental casting:&r Iron's Spells schools (fire, ice, lightning, holy, ender, blood, evocation, nature).",
             "Spell power and school attributes come from Iron's gear and spellbooks; Apotheosis gems still boost the wearer.",
             "Mageslayer (Starlit Voidglass) is the anti-caster gem. Inks: Ancient Core = epic, Starforged Heart = legendary."],
            ["builds"], [("check",)], [("xp", 3)]),
           ("build_summon", "Summoner and Artificer", "ars_nouveau:summon_focus",
            ["&eSummoning and utility:&r Iron's summoning spells, Ars Nouveau familiars and turrets, Occultism spirits.",
             "Less burst, more control and automation - strong for exploring and base-building."], ["builds"], [("check",)], [("xp", 3)])]
for t in EXP["trials"]:
    mastery.append((f"trial_{t['id']}", t["name"], "gateways:gate_pearl",
                    [f"A Gateways to Eternity trial: {len(t['waves'])} fixed waves, fixed enemy counts, a visible timer.",
                     "Cost: " + ", ".join(f"{n}x {i.split(':')[1].replace('_', ' ')}" for i, n in t["cost"].items()) + " (+ ender pearl).",
                     "Rewards: affix gear, gems and XP - never relics. Fight it in the open, away from your base.",
                     "&7Completes when you are within 48 blocks of the gate as its last wave falls."],
                    ["builds"], [("adv", f"horizon:trial/{t['id']}")], [("xp", 10)]))
mastery.append(("perfect_gem", "Gem Cutter's Bench", "apotheosis:gem_cutting_table",
                ["Craft a gem cutting table, then cut gems up toward Perfect purity. Gem dust comes from salvaging and shards.",
                 "&7(Item task: the table itself. Apotheosis has no advancement for gem purity.)"],
                ["builds"], [("item", "apotheosis:gem_cutting_table", 1)], [("xp", 20)]))
C["13 - Mastery and Trials"] = mastery

# ---------------------------------------------------------------- 0.6 headquarters campaign (main spine)
# Every quest here completes on a horizon:hq/* advancement that the server grants only after recording the stage in its
# ledger (kubejs/server_scripts/horizon_headquarters.js). The quests explain; the charter commissions. Rewards are XP only:
# each station's real rewards are paid once per headquarters by the charter, so a party never multiplies them.
HQ_CHAPTER = "0 - Headquarters Campaign"
HQ_POS = {}
HQ_GUIDE = {}


def hq_chapter():
    out, prev = [], "hq_charter"
    prem = HQ["fiction"]["premise"]
    out.append(("hq_charter", "The Last Charter", "horizon:survey_charter",
                ["&6THE LANTERN LINE&r", *prem, "",
                 "Unpack the &eFounding Kit&r, place the &eSurvey Charter&r where your base will grow and right-click it.",
                 "The charter's panel shows what each station needs; its &a[Commission]&r button does the work. Friends join by invitation."],
                [], [("adv", "horizon:hq/root")], [("xp", 2)]))
    HQ_POS["hq_charter"] = (0, 2)
    HQ_GUIDE["hq_charter"] = ("Place a Survey Charter and click Found a headquarters on its panel.",
                           "Your station exists: the charter is its anchor, and every stage below is commissioned there.")
    for i, s in enumerate(HQ["stages"]):
        qid = f"hq_{s['id']}"
        reqs = [f"&7- {r['text']}&r" for r in s["requirements"]]
        if s.get("choices"):
            reqs.append(f"&7- {s['choices']['title']}: {s['choices']['min']} of {len(s['choices']['options'])} (see the branches)&r")
        cost = ", ".join(f"{n}x {c.split(':')[1].replace('_', ' ')}" for c, n in s["cost"])
        out.append((qid, f"{s['numeral']}. {s['title']}", f"horizon:emblem_{s['id']}",
                    [f"&6STATION {s['numeral']}&r  {s['summary']}", "", f"&eWhy:&r {s['why']}", "", "&eNeeds at the station:&r", *reqs,
                     f"&eContribution (consumed once):&r {cost}", f"&eUnlocks:&r {s['unlocks']}",
                     "&7Commission it from the charter panel. This quest completes by itself when the station records it.&r"],
                    [prev], [("adv", f"horizon:hq/{s['id']}")], [("xp", 3 + 2 * i)]))
        HQ_GUIDE[qid] = (f"Commission {s['title']} at your charter.", s["next"])
        HQ_POS[qid] = (2 + 2 * i, 2)
        for j, o in enumerate((s.get("choices") or {}).get("options", [])):
            oid = f"hq_{s['id']}_{o['id']}"
            out.append((oid, o["title"], o["icon"], [o["summary"], "", "&eCounts:&r " + "; ".join(r["text"] for r in o["requirements"]),
                        "&eContribution:&r " + ", ".join(f"{n}x {c.split(':')[1].replace('_', ' ')}" for c, n in o["cost"]),
                        "&eAdds to the station:&r " + o["contribution"]],
                        [prev], [("adv", f"horizon:hq/{s['id']}/{o['id']}")], [("xp", 2)]))
            HQ_GUIDE[oid] = (f"Contribute {o['title']} at the charter panel.", o["contribution"])
            HQ_POS[oid] = (1 + 2 * i + j, 4 + (i % 2))   # branches under their stage; alternate rows so neighbours never overlap
        prev = qid
    # guidance for the two crafted proofs (item tasks only explain; the charter consumes the real thing)
    out.append(("hq_plates", "Pressed True", "horizon:survey_plate",
                ["Craft Survey Blanks (andesite alloy, copper ingot, iron nugget) and put them under a Create &eMechanical Press&r",
                 "on a depot or belt. Only a press makes Survey Plates. The Workshop consumes four."],
                ["hq_outpost"], [("item", "horizon:survey_plate", 4)], [("xp", 2)]))
    HQ_GUIDE["hq_plates"] = ("Hold 4 Survey Plates pressed by a Mechanical Press.", "Proof that your press line runs; the Workshop needs them.")
    HQ_POS["hq_plates"] = (3, 0)
    out.append(("hq_lens", "The Great Lens", "horizon:observatory_lens",
                ["Brass, tinted glass, a spyglass and one &dStarforged Heart&r make the Observatory Lens.",
                 "Place it at the station: the Observatory needs to see it there."],
                ["hq_foundry"], [("item", "horizon:observatory_lens", 1)], [("xp", 5)]))
    HQ_GUIDE["hq_lens"] = ("Craft the Observatory Lens.", "The capstone's centrepiece: the only late relic gate of the campaign.")
    HQ_POS["hq_lens"] = (11, 0)
    out.append(("hq_beyond", "Beyond the Line", "gateways:gate_pearl",
                ["The Lantern Line is open. What remains is optional mastery: every legend in the Hall of Legends, every realm,",
                 "the third region and the other research routes, and the Horizon Gauntlet."],
                ["hq_observatory"], [("check",)], [("xp", 10)]))
    HQ_GUIDE["hq_beyond"] = ("Click Check.", "Opens the post-campaign goals; nothing here gates anything.")
    HQ_POS["hq_beyond"] = (14, 2)
    return out


C[HQ_CHAPTER] = hq_chapter()

# ---------------------------------------------------------------- 0.5 campaign / bounty / discovery chapters
import quest_campaign as _qc
_rest = dict(C)
C.clear()
C[HQ_CHAPTER] = _rest.pop(HQ_CHAPTER)
C[_qc.CAMPAIGN] = _qc.C[_qc.CAMPAIGN]
C.update(_rest)
FOLDERS = {_qc.CAMPAIGN: _qc.CAMPAIGN_FOLDER}   # renamed chapters keep their 0.5 folder so quest ids and progress survive
C[_qc.BOUNTY] = _qc.C[_qc.BOUNTY]
C[_qc.DISCOVER] = _qc.C[_qc.DISCOVER]

# ---------------------------------------------------------------- objective + why-it-matters lines
# (objective, why). Every quest gets both; the generated chapters (atlas, legends, trials) use templates below.
GUIDE = {
 "welcome": ("Click Check, then claim the reward.", "The reward is the Quest Book item: right-click it, or use the button under your inventory."),
 "wood": ("Collect 16 logs of any kind.", "Planks, sticks and a crafting table are the base of every tool you will make."),
 "stone_age": ("Mine stone with a wooden pickaxe.", "Stone tools and a furnace are the gate to iron."),
 "iron": ("Smelt an iron ingot in a furnace.", "Iron makes buckets, shears, armour and most machine parts."),
 "bed": ("Sleep in a bed through the night.", "Sets your spawn and skips night mobs while you build."),
 "kitchen": ("Craft or hold a Farmer's Delight cooking pot.", "Cooked meals give long buffs: the cheapest preparation for any expedition."),
 "backpack": ("Craft a Sophisticated Backpack.", "Extra storage you carry makes long trips to far structures practical."),
 "diamonds": ("Mine a diamond.", "Diamonds unlock enchanting tables, better tools and the later gem tiers."),
 "first_ruin": ("Step inside any roadside ruin, camp, shrine or watchtower.", "Small sites are the main source of Wayfarer Shards and teach you how structure loot works."),
 "waystone": ("Right-click a waystone to activate it.", "Activated waystones become free fast-travel points, so long trips stop costing a day."),
 "village": ("Trade once with a villager.", "Villagers supply emeralds, maps and Surveyor's Charts that point to great landmarks."),
 "dungeon_arise": ("Enter one great landmark (follow the chart you receive).", "Landmarks hold the first boss fights and the Ancient Cores that gate tech."),
 "frostmaw": ("Defeat a Frostmaw in a cold biome.", "First defeat grants an Ancient Core and a trophy for your base."),
 "wroughtnaut": ("Defeat the Ferrous Wroughtnaut in a Wrought chamber.", "First defeat grants an Ancient Core and a trophy for your base."),
 "core": ("Hold one Ancient Core.", "Cores gate the ME controller and gem socketing, so tech and gear progress both depend on expeditions."),
 "apoth_haven": ("Reach the Haven world tier (earned automatically).", "World tier controls which affixes and gems can drop."),
 "apoth_frontier": ("Reach the Frontier world tier.", "Rarer affixes begin to appear and harder monsters spawn."),
 "socket": ("Obtain a Sigil of Socketing.", "Sockets let your best weapon carry gems, which is the core Apotheosis upgrade."),
 "enchant": ("Enchant any item at an enchanting table.", "Apothic Enchanting scales far past vanilla, so a tuned library pays off early."),
 "simply": ("Obtain any Simply Swords weapon.", "Weapon type decides your combos and playstyle: sample a few before committing."),
 "artifact": ("Obtain one Artifact from a chest.", "Curios slots add a second equipment layer; duplicates salvage into shards."),
 "apoth_ascent": ("Reach the Ascent world tier.", "Ascent loot is strong, and so are the monsters; prepare before you push."),
 "nether": ("Enter the Nether.", "Opens Incendium's biomes, fortresses and the materials for Nether-era gear."),
 "aether": ("Light an Aether portal and enter.", "A sky realm with three dungeons and the Skyward Plume token."),
 "aether_bronze": ("Defeat the Slider in the bronze dungeon.", "First defeat grants an Ancient Core and a trophy; its key opens the next dungeon."),
 "aether_gold": ("Defeat the Sun Spirit atop the gold dungeon.", "First defeat grants a Starforged Heart, needed for the highest tech tiers."),
 "bumblezone": ("Throw an ender pearl into a bee nest to enter the Bumblezone.", "Honeyed Seals from this realm buy targeted gems at the Expedition Exchange."),
 "undergarden": ("Light the catalyst portal and enter the Undergarden.", "A dim realm with its own materials, bosses and Echoing Fossil token."),
 "forgotten_guardian": ("Defeat the Forgotten Guardian in the catacombs.", "Its drops forge Undergarden's best gear."),
 "otherside": ("Enter the Otherside via the Ancient City portal.", "Deeper and Darker's dimension holds its strongest gear and bosses."),
 "end": ("Enter the End.", "Nullscape's End is a full expedition area with Starlit Voidglass."),
 "dragon": ("Defeat the Ender Dragon.", "First defeat grants a Starforged Heart and a trophy; the End then opens fully."),
 "ars_start": ("Obtain the Worn Notebook.", "It explains every Ars Nouveau mechanic in-game, so you never need a wiki."),
 "ars_book": ("Craft a Novice Spell Book.", "A spell book is how you cast; glyphs are unlocked by crafting them."),
 "ars_apparatus": ("Craft an Enchanting Apparatus.", "It crafts most Ars items and unlocks the upgrade path."),
 "irons_start": ("Craft an Inscription Table.", "Scrolls found in loot must be inscribed into a spellbook to be cast."),
 "irons_anvil": ("Craft an Arcane Anvil.", "Upgrades scrolls and imbues weapons with spells."),
 "irons_catacombs": ("Enter the Catacombs.", "The Dead King's first defeat grants an Ancient Core and a trophy."),
 "occultism": ("Craft chalk and open the Occultism guide.", "Spirits automate mining, crafting and storage without power."),
 "legendary_ink": ("Obtain Legendary Ink.", "It is the only way to write the strongest spell scrolls."),
 "andesite": ("Craft andesite alloy.", "Every Create machine starts with it."),
 "waterwheel": ("Place a water wheel in flowing water.", "First free source of rotation."),
 "press": ("Build a mechanical press and press a plate.", "Automated plates are the base of most late recipes."),
 "belt": ("Craft a mechanical belt and move an item.", "Belts move items and power: your first production line."),
 "brass": ("Make a brass ingot.", "Brass unlocks logistics, mechanical crafters and arms."),
 "electric": ("Craft a Crafts & Additions alternator.", "It converts rotation into FE and bridges Create to every other tech mod."),
 "liquid_xp": ("Complete Enchantment Industry's engineer advancement.", "Liquid XP automates enchanting; pair it with Apothic Enchanting."),
 "mek_metallurgic": ("Craft a metallurgic infuser.", "Steel and alloys are required for most Mekanism machines."),
 "mek_ore": ("Build an enrichment chamber.", "First ore multiplier, and the entry to further processing chains."),
 "mi_steam": ("Craft a bronze furnace (Modern Industrialization).", "Steam age is MI's start; multiblocks grow from here."),
 "mi_ebf": ("Build the Electric Blast Furnace.", "First big electric multiblock and the gateway to advanced metals."),
 "mi_distill": ("Build a distillation tower.", "Refines oil into fuels and plastics for late recipes."),
 "powah": ("Craft an Energizing Orb.", "Simple scalable power generation."),
 "cc": ("Craft a computer.", "Programmable automation for any machine in the pack."),
 "ae_quartz": ("Charge a certus quartz crystal.", "First step of AE2 and the base of presses and inscribers."),
 "ae_presses": ("Obtain an inscriber press from a meteorite.", "Presses make processors; finding one needs a meteorite compass."),
 "ae_controller": ("Craft an ME controller.", "The controller requires an Ancient Core, which ties AE2 to expeditions."),
 "ae_crafting": ("Build a crafting CPU.", "Autocrafting turns storage into production."),
 "ae_mek": ("Craft a 1k chemical storage cell.", "Lets AE2 hold Mekanism chemicals and craft with them."),
 "ae_wireless": ("Craft a wireless terminal.", "Reach your network away from base, including on expeditions."),
 "cataclysm_find": ("Find any Cataclysm structure.", "Unlocks Cataclysm's bosses, the pack's toughest legends."),
 "ignis": ("Defeat Ignis in the Burning Arena.", "First defeat grants a Starforged Heart and a trophy."),
 "monstrosity": ("Defeat the Netherite Monstrosity.", "First defeat grants a Starforged Heart and a trophy."),
 "leviathan": ("Defeat the Leviathan under the Sunken City.", "First defeat grants a Starforged Heart and a trophy."),
 "harbinger": ("Defeat the Harbinger in the Ancient Factory.", "First defeat grants a Starforged Heart and a trophy."),
 "wither": ("Summon and defeat the Wither.", "First defeat per player grants a Starforged Heart; later ones cannot be farmed for hearts."),
 "warden": ("Defeat a Warden.", "First defeat counts toward a heart; summoned Wardens afterwards do not."),
 "apoth_summit": ("Reach the Summit world tier.", "Mythic affixes drop, and the deadliest bosses spawn."),
 "all_cataclysm": ("Defeat every Cataclysm boss.", "The pack's hardest combat milestone."),
 "pinnacle": ("Reach the Pinnacle world tier.", "The highest tier; every gem can reach Perfect purity."),
 "fusion_mek": ("Craft a fusion reactor controller (needs a Starforged Heart).", "Mekanism's endgame power."),
 "fusion_mi": ("Craft MI's fusion reactor controller (needs a Starforged Heart).", "Modern Industrialization's endgame power."),
 "antimatter": ("Make antimatter in an SPS.", "Antimatter is Mekanism's final resource."),
 "mega": ("Craft a 256M MEGA cell component (needs a Starforged Heart).", "Effectively unlimited storage for a late AE2 base."),
 "archmage": ("Craft an Archmage Spell Book.", "Ars Nouveau's final book; every glyph tier is available."),
 "bumble_all": ("Discover every Bumblezone biome.", "Completing the realm rewards Honeyed Seals for the Exchange."),
 "exchange": ("Obtain any realm token (see the list above).", "Tokens are the only way to buy a specific gem, so they make dungeon runs targeted."),
 "exchange_gem": ("Craft any Exchange gem (EMI: search horizon_exchange).", "Shows the token to gem loop works on your save."),
 "salvage": ("Craft a salvaging table.", "Turns unwanted duplicates into shards, gem dust and sometimes cores."),
 "atlas": ("Click Check.", "Each following quest explains one structure family before you travel."),
 "hall": ("Click Check.", "Explains how first-defeat relics, trophies and hearts work."),
 "builds": ("Click Check.", "Explains the build guides below; none are required."),
 "build_crit": ("Click Check once you have read the guide.", "Helps pick gems and gear for fast melee."),
 "build_heavy": ("Click Check once you have read the guide.", "Helps pick gems and gear for heavy melee."),
 "build_tank": ("Click Check once you have read the guide.", "Helps pick gems and gear for defence."),
 "build_ranged": ("Click Check once you have read the guide.", "Helps pick gems and gear for bows."),
 "build_spell": ("Click Check once you have read the guide.", "Helps pick spell schools and gems."),
 "build_summon": ("Click Check once you have read the guide.", "Helps pick summons and utility tools."),
 "perfect_gem": ("Craft a gem cutting table.", "Gem cutting is the long game of every build: Perfect gems are the strongest bonuses."),
 "hall_complete": ("Defeat every great legend, then click Check.", "Its reward opens the Horizon Gauntlet, the hardest fight in the pack."),
}


GUIDE.update(_qc.GUIDE)
GUIDE.update(HQ_GUIDE)


def objective_why(qid, title):
    if qid in GUIDE:
        return GUIDE[qid]
    if qid.startswith("atlas_"):
        d = F[qid[6:]]
        sig = d["signature"].split(";")[0].rstrip(".")
        return (f"Walk into any {d['title'].lower()} structure ({d['stage']} game).", sig + ".")
    if qid.startswith("legend_"):
        major = qid in MAJOR_IDS
        return (f"Defeat {title} ({REALM_OF.get(qid, 'anywhere')}).",
                ("Starforged Heart" if major else "Ancient Core") + " + trophy, first kill only.")
    if qid.startswith("trial_"):
        return ("Pay the cost at the gate and survive every wave.", "Affix gear, gems and XP. No relics.")
    raise SystemExit(f"quest {qid} has no objective/why line")


# ---------------------------------------------------------------- validation + emit
def check(kind, i):
    if i.startswith("#"):
        return i
    if i.startswith("horizon:"):
        ok = {"item": HORIZON_ITEMS, "advancement": HORIZON_ADV, "loot": HORIZON_LOOT}.get(kind)
        if ok is not None and i not in ok:
            raise SystemExit(f"unknown horizon {kind}: {i}")
        return i
    if i.startswith("minecraft:") and kind in ("item", "entity", "advancement", "block"):
        return i
    if kind == "dimension" and i in VANILLA_DIMS:
        return i
    if i not in IDS[kind if kind != "block" else "item"]:
        raise SystemExit(f"unknown {kind}: {i}")
    return i


def task(t):
    k = t[0]
    if k == "adv":
        return {"type": "heracles:advancement", "advancements": [check("advancement", t[1])]}
    if k == "item":
        return {"type": "heracles:item", "item": check("item", t[1]), "amount": t[2], "collection": "AUTOMATIC"}
    if k == "dim":
        return {"type": "heracles:changed_dimension", "to": check("dimension", t[1])}
    if k == "check":
        return {"type": "heracles:check"}
    if k == "recipe":
        for r in t[1]:
            if r not in HORIZON_RECIPES:
                raise SystemExit(f"unknown recipe {r}")
        return {"type": "heracles:recipe", "recipes": t[1]}
    if k == "block":
        return {"type": "heracles:block_interaction", "block": check("block", t[1])}
    raise SystemExit(f"bad task {t}")


def reward(r):
    if r[0] == "item":
        it = {"id": check("item", r[1]), "count": r[2]}
        if len(r) > 3:
            it["components"] = r[3]
        return {"type": "heracles:item", "item": it}
    if r[0] == "xp":
        return {"type": "heracles:xp", "xptype": "LEVEL", "amount": r[1]}
    if r[0] == "loot":
        return {"type": "heracles:loottable", "loot_table": check("loot", r[1])}
    raise SystemExit(f"bad reward {r}")


def no_reward_shortcuts():
    tasks = {}
    for ch, qs in C.items():
        for q in qs:
            for t in q[5]:
                if t[0] == "item" and not t[1].startswith("#"):
                    tasks.setdefault(t[1], []).append(q[0])
    bad = []
    for ch, qs in C.items():
        for q in qs:
            for r in q[6]:
                if r[0] == "item" and r[1] in tasks and q[0] not in tasks[r[1]]:
                    bad.append(f"{q[0]} rewards {r[1]} which completes {tasks[r[1]]}")
                if r[0] == "item" and r[1] in (SHARD, CORE, HEART):
                    bad.append(f"{q[0]} rewards relic {r[1]}")
    if bad:
        raise SystemExit("reward shortcuts: " + "; ".join(bad))


def grid(rows, pos, x0=0, y0=0, dx=40, dy=44, wrap=7):
    """rows: list of lists of quest ids; each row wraps at `wrap` nodes. Returns next free y."""
    y = y0
    for row in rows:
        for i, qid in enumerate(row):
            pos[qid] = [x0 + (i % wrap) * dx, y + (i // wrap) * dy]
        y += ((len(row) - 1) // wrap + 1) * dy + 14
    return y


def layout(chapter, quests):
    ids = [q[0] for q in quests]
    pos = {}
    if chapter.endswith("Hall of Legends"):
        # realm trees side by side under the Hall, lifted into a shallow arch (outer realms sit higher),
        # Curator under the middle where the great-legend paths end
        dx, dy, gap = 36, 46, 0.9
        widths = [max(c for _, c, _ in t.values()) + 1 for _, t in REALMS]
        total = sum(widths) + gap * (len(REALMS) - 1)
        x, cols = 0.0, []
        for w in widths:
            cols.append(x)
            x += w + gap
        mid = (total - 1) / 2
        for (_, t), x0, w in zip(REALMS, cols, widths):
            lift = ((x0 + (w - 1) / 2 - mid) / mid) ** 2 * 34
            for b, (_, c, r) in t.items():
                pos[f"legend_{b}"] = [round((x0 + c) * dx), round(r * dy + 30 - lift)]
        pos["hall"] = [round(mid * dx), -20]
        pos["hall_complete"] = [round(mid * dx), max(y for _, y in pos.values()) + 70]
        return pos
    if chapter.endswith("Expedition Atlas"):
        pos["atlas"] = [2 * 40, 0]
        y = grid([[f"atlas_{f}" for f in fs] for _, fs in ATLAS_GROUPS], pos, y0=50, wrap=3, dx=40)
        # exchange / salvage / gem to the right of the clusters
        for i, q in enumerate(["exchange", "exchange_gem", "salvage"]):
            pos[q] = [6 * 40, 50 + i * 44]
        return pos
    if chapter.endswith("Mastery and Trials"):
        pos["builds"] = [3 * 40, 0]
        builds = [i for i in ids if i.startswith("build_")]
        trials = [i for i in ids if i.startswith("trial_")]
        y = grid([builds], pos, y0=50, wrap=6)
        pos["perfect_gem"] = [6 * 40, 0]
        grid([trials], pos, y0=y + 10, wrap=6)
        return pos
    if chapter == HQ_CHAPTER:
        return {k: [v[0] * 40, v[1] * 38] for k, v in HQ_POS.items()}
    if chapter in _qc.POS:
        return {k: [v[0] * 44, v[1] * 40] for k, v in _qc.POS[chapter].items()} |                {i: [0, 0] for i in ids if i not in _qc.POS[chapter]}
    # default: columns by depth; the longest prerequisite chain stays on row 0 as the main path, side branches fall below it
    byid = {q[0]: q for q in quests}
    depth = {}
    def d(i):
        if i not in depth:
            deps = byid[i][4]
            depth[i] = 0 if not deps else 1 + max(d(x) for x in deps)
        return depth[i]
    for i in ids:
        d(i)
    main, cur = set(), max(ids, key=lambda i: (depth[i], -ids.index(i)))
    while cur:
        main.add(cur)
        deps = byid[cur][4]
        cur = max(deps, key=lambda x: depth[x]) if deps else None
    rows = {}
    for i in ids:
        col = depth[i]
        if i in main:
            row = 0
        else:
            rows[col] = rows.get(col, 0) + 1
            row = rows[col]
        pos[i] = [col * 44, row * 40]
    return pos


def main():
    no_reward_shortcuts()
    shutil.rmtree(OUT / "quests", ignore_errors=True)   # owned subtree only
    total = 0
    for chapter, quests in C.items():
        ids = {q[0] for q in quests}
        pos = layout(chapter, quests)
        folder = FOLDERS.get(chapter) or "".join(ch for ch in chapter.lower() if ch.isalnum())
        for qid, title, icon, desc, deps, tasks, rewards in quests:
            for dep in deps:
                assert dep in ids, f"{qid}: dependency {dep} not in chapter"
            obj, why = objective_why(qid, title)
            assert title.strip() and not title.lower().startswith("new quest"), qid
            quest = {
                "display": {"icon": {"type": "heracles:item", "item": {"id": check("item", icon)}},
                            "title": json.dumps({"text": title}), "description": desc + ["", "&aDo:&r " + obj, "&6You get:&r " + why], "groups": {chapter: {"position": pos[qid]}}},
                "settings": {"hidden": "LOCKED", "unlockNotification": True},
                "dependencies": [f"{folder}_{d}" for d in deps],
                "tasks": {f"t{i}": task(t) for i, t in enumerate(tasks)},
                "rewards": {f"r{i}": reward(r) for i, r in enumerate(rewards)},
            }
            p = OUT / "quests" / folder / f"{folder}_{qid}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(quest, indent=2), encoding="utf-8")
            total += 1
    (OUT / "groups.txt").write_text("\n".join(C.keys()) + "\n", encoding="utf-8")
    print(f"{total} quests in {len(C)} chapters")


if __name__ == "__main__":
    main()
