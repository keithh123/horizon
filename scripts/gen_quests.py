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
import json, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
IDS = {k: set(v) for k, v in json.loads((ROOT / "manifests/ids.json").read_text()).items()}
FAM = json.loads((ROOT / "manifests/loot_families.json").read_text(encoding="utf-8"))
LEG = json.loads((ROOT / "manifests/legends.json").read_text(encoding="utf-8"))
EXP = json.loads((ROOT / "manifests/expeditions.json").read_text(encoding="utf-8"))
GEN = json.loads((ROOT / "datapacks/.generated.json").read_text())["files"]
HORIZON_ADV = {"horizon:" + f.split("horizon/advancement/")[1][:-5] for f in GEN if f.startswith("horizon/advancement/")}
HORIZON_LOOT = {"horizon:" + f.split("horizon/loot_table/")[1][:-5] for f in GEN if f.startswith("horizon/loot_table/")}
HORIZON_RECIPES = {"horizon:" + f.split("horizon/recipe/")[1][:-5] for f in GEN if f.startswith("horizon/recipe/")}
ASSETS = json.loads((ROOT / "kubejs/.generated-assets.json").read_text())["files"]
HORIZON_ITEMS = {"horizon:" + f.rsplit("/", 1)[1][:-4] for f in ASSETS if "/textures/item/" in f} | \
                {"horizon:" + f.rsplit("/", 1)[1][:-4] for f in ASSETS if "/textures/block/trophy_" in f}
OUT = ROOT / "config" / "heracles"
VANILLA_DIMS = {"minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"}
SHARD, CORE, HEART = "horizon:wayfarer_shard", "horizon:ancient_core", "horizon:starforged_heart"
F = FAM["families"]


def fam_desc(f):
    d = F[f]
    return [d["identity"], "", "&ePrepare:&r " + d["prep"], "&eSignature rewards:&r " + d["signature"],
            "&eComing back:&r " + d["repeat"], "&eFeeds into:&r " + d["connects"]]


C = {}
C["1 - The First Steps"] = [
    ("welcome", "Welcome to the Horizon", "minecraft:compass",
     ["The world is enormous. Mountains here are real mountains, and with Voxy you can see them from very far away.",
      "This book is a guide, not a checklist: every chapter is optional. Follow what interests you.",
      "Press &eJ&r any time to reopen it (keybinds are searchable in Options > Controls).",
      "Dying drops your items into a &ecorpse&r at the spot (also in the void): go back for it."],
     [], [("adv", "minecraft:story/root")], [("item", "minecraft:bread", 8)]),
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
      "&7(Introductory item task: craft or hold a cooking pot.)"], ["bed"],
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
     [("adv", "horizon:atlas/roadside")], [("item", "minecraft:map", 3)]),
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
     ["dungeon_arise"], [("adv", "horizon:legend/frostmaw")], [("xp", 8)]),
    ("wroughtnaut", "Iron in the Dark", "minecraft:iron_block",
     ["Wrought chambers underground hold the Ferrous Wroughtnaut. Hit it from behind. First defeat: Ancient Core + trophy."],
     ["dungeon_arise"], [("adv", "horizon:legend/ferrous_wroughtnaut")], [("xp", 8)]),
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
    ("aether_bronze", "The Slider", "aether:bronze_dungeon_key", ["Defeat the Slider in the bronze dungeon (first defeat: Ancient Core + trophy)."],
     ["aether"], [("adv", "aether:bronze_dungeon")], [("xp", 8)]),
    ("aether_gold", "The Sun Spirit", "aether:gold_dungeon_key", ["Defeat the Sun Spirit atop the gold dungeon (first defeat: Starforged Heart + trophy)."],
     ["aether_bronze"], [("adv", "aether:gold_dungeon")], [("xp", 15)]),
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
     [("adv", "minecraft:end/kill_dragon")], [("xp", 20)]),
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
     [("adv", "irons_spellbooks:irons_spellbooks/enter_catacombs")], [("xp", 8)]),
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
    ("ignis", "Ignis", "minecraft:blaze_rod", ["The flame knight in the Burning Arena. First defeat: Starforged Heart + trophy."], ["cataclysm_find"],
     [("adv", "horizon:legend/ignis")], [("xp", 15)]),
    ("monstrosity", "Netherite Monstrosity", "minecraft:netherite_ingot", ["Found in the Soul Blacksmith."], ["cataclysm_find"],
     [("adv", "horizon:legend/netherite_monstrosity")], [("xp", 15)]),
    ("leviathan", "The Leviathan", "minecraft:heart_of_the_sea", ["Beneath the Sunken City."], ["cataclysm_find"],
     [("adv", "horizon:legend/the_leviathan")], [("xp", 15)]),
    ("harbinger", "The Harbinger", "minecraft:redstone_block", ["Deep in the Ancient Factory."], ["cataclysm_find"],
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
     [("adv", "cataclysm:kill_all_bosses")], [("item", "apotheosis:sigil_of_enhancement", 1), ("xp", 30)]),
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
                    ["hall"], [("adv", f"horizon:legend/{p}")], [("xp", 10 if b["tier"] == "major" else 5)]))
majors = [f"legend_{b['id'].split(':')[1]}" for b in LEG["bosses"] if b["tier"] == "major"]
legends.append(("hall_complete", "Curator of Legends", "minecraft:lodestone",
                ["Defeat every great legend. The reward is a pearl for the Horizon Gauntlet."], majors, [("check",)],
                [("item", "gateways:gate_pearl", 1, {"gateways:gateway": "horizon:trial/horizon"}), ("xp", 50)]))
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
           ("build_tank", "Bulwark", "minecraft:shield",
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
mastery.append(("perfect_gem", "Flawless Ambition", "apotheosis:gem_cutting_table",
                ["Cut any gem up to Perfect purity at the gem cutting table. Gem dust comes from salvaging and shards."],
                ["builds"], [("adv", "apotheosis:progression/pinnacle")], [("xp", 20)]))
C["13 - Mastery and Trials"] = mastery


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


def layout(quests):
    depth = {}
    def d(q):
        if q[0] not in depth:
            depth[q[0]] = 0 if not q[4] else 1 + max(d(next(x for x in quests if x[0] == dep)) for dep in q[4])
        return depth[q[0]]
    rows, pos = {}, {}
    for q in quests:
        col = d(q)
        row = rows.get(col, 0)
        rows[col] = row + 1
        pos[q[0]] = [col * 48, row * 36]
    return pos


def main():
    no_reward_shortcuts()
    shutil.rmtree(OUT / "quests", ignore_errors=True)   # owned subtree only
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
