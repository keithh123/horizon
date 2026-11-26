# Graph Report - horizon  (2026-11-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1738 nodes · 4318 edges · 121 communities (74 shown, 47 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 48 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `56efa145`
- Check the source-content fingerprint with `python scripts/horizon_graph.py status`; the commit above is provenance, not the freshness check.
- Run `python scripts/horizon_graph.py build` after code changes (no API cost).

## Community Hubs (Navigation)
- manifests/lock.json
- heracles:item
- manifests/legends.json
- net.neoforged.fml.common.Mod
- horizon.py
- org.spongepowered.asm.mixin.injection.Inject
- heracles:xp
- heracles:advancement
- horizon_headquarters.js
- org.spongepowered.asm.mixin.gen.Accessor
- json
- re
- zipfile
- net.minecraft.world.level.block.state.BlockState
- CampfireSmokeParticleMixin.java
- build.py
- org.spongepowered.asm.mixin.Mixin
- audit_loot.py
- SnowyLeavesPlus.java
- horizon_graph.py
- QuestPopupScreen.java
- The High Landmarks (Expedition Hall option)
- ClientBridge.java
- First Blood [14bountiesandhunts_b_hunter]
- ArmourSoundTweak.java
- Iron Age [0thehorizoncampaign_c_iron]
- Geckolib [geckolib]
- gen_headquarters.py
- hq_sim.js
- BettersmokeConfig
- V. Foundry and Logistics (headquarters stage)
- EatingAnimation.java
- gen_datapack.py
- Bounty: Sky Wardens [14bountiesandhunts_b_aether_trio]
- sys
- gen_quests.py
- III. Expedition Hall (headquarters stage)
- Accessories [accessories]
- GuiGraphicsMixin.java
- Cloth Config API [cloth-config]
- at
- II. Workshop (headquarters stage)
- A Gem of Your Choosing [11expeditionatlas_exchange_gem]
- The Hall of Legends [12halloflegends_hall]
- I. Outpost (headquarters stage)
- Bounty: Fire and Blood [14bountiesandhunts_b_nether_cabal]
- Trial of Cinders
- VI. Observatory and Horizon Beacon (headquarters stage)
- The Controller [8thedigitalage_ae_controller]
- apotheosis:epic
- Trial of the Void
- Trial of the Tides
- manifests/headquarters.json
- YUNG's API [yungs-api]
- horizon_events.js
- plans
- Lithostitched [lithostitched]
- HorizonGraphTests
- manifests/loot_families.json
- Keeper of the Hall [0thehorizoncampaign_c_curator]
- Bounty: Sea Raiders [14bountiesandhunts_b_sea_raiders]
- Resourceful Lib [resourceful-lib]
- Create [create]
- main
- The Hollow Roads (Expedition Hall option)
- The Horizon Gauntlet
- Bounty: Mass Destruction [14bountiesandhunts_b_mass_destruction]
- Applied Energistics 2 [ae2]
- YetAnotherConfigLib (YACL) [yacl]
- Sodium [sodium]
- Enchanting Apparatus [5arcanestudies_ars_apparatus]
- Spirit Circle (Occultism) (Arcane Conservatory option)
- Mechanical Press [6mechanicalrevolution_press]
- remap_intermediary.py
- World Tier: Haven [3forgedinadventure_apoth_haven]
- Conqueror of Calamity [0thehorizoncampaign_c_conqueror]
- Brass Age [6mechanicalrevolution_brass]
- Apotheosis [apotheosis]
- WindDirectionSlider
- Bounty: End Cabal [14bountiesandhunts_b_end_cabal]
- Electric Blast Furnace [7industrialexpansion_mi_ebf]
- net.minecraft.world.level.block.Block
- Hunt: The Withering [0thehorizoncampaign_c_wither]
- Antimatter [10beyondthehorizon_antimatter]
- Metallurgy [7industrialexpansion_mek_metallurgic]
- Legendary Tooltips [legendary-tooltips]
- apply-profile.ps1
- KubeJS [kubejs]
- nbt
- smoke.sh
- Nothing Wasted [11expeditionatlas_salvage]
- Archmage [10beyondthehorizon_archmage]
- Programmable World [7industrialexpansion_cc]
- Unlimited Storage [10beyondthehorizon_mega]
- Bee Whisperer [10beyondthehorizon_bumble_all]

## God Nodes (most connected - your core abstractions)
1. `heracles:xp` - 189 edges
2. `heracles:advancement` - 183 edges
3. `heracles:item` - 124 edges
4. `VI. Observatory and Horizon Beacon (headquarters stage)` - 36 edges
5. `AbstractParticleAccessor` - 27 edges
6. `Master Cartographer [15discoveriesandrelics_d_cartographer]` - 26 edges
7. `apotheosis:gem_dust` - 25 edges
8. `II. Workshop (headquarters stage)` - 24 edges
9. `First Blood [14bountiesandhunts_b_hunter]` - 24 edges
10. `QuestPopupScreen` - 22 edges

## Surprising Connections (you probably didn't know these)
- `The Great Lens [0headquarterscampaign_hq_lens]` --task_reference--> `horizon:observatory_lens`  [EXTRACTED]
  config/heracles/quests/0headquarterscampaign/0headquarterscampaign_hq_lens.json → manifests/headquarters.json
- `Pressed True [0headquarterscampaign_hq_plates]` --task_reference--> `horizon:survey_plate`  [EXTRACTED]
  config/heracles/quests/0headquarterscampaign/0headquarterscampaign_hq_plates.json → manifests/headquarters.json
- `Trial of Cinders [13masteryandtrials_trial_cinders]` --task_reference--> `horizon:trial/cinders`  [EXTRACTED]
  config/heracles/quests/13masteryandtrials/13masteryandtrials_trial_cinders.json → manifests/headquarters.json
- `Trial of the Tides [13masteryandtrials_trial_tides]` --task_reference--> `horizon:trial/tides`  [EXTRACTED]
  config/heracles/quests/13masteryandtrials/13masteryandtrials_trial_tides.json → manifests/headquarters.json
- `Trial of the Void [13masteryandtrials_trial_void]` --task_reference--> `horizon:trial/void`  [EXTRACTED]
  config/heracles/quests/13masteryandtrials/13masteryandtrials_trial_void.json → manifests/headquarters.json

## Import Cycles
- None detected.

## Communities (121 total, 47 thin omitted)

### Community 0 - "manifests/lock.json"
Cohesion: 0.03
Nodes (113): AdoraBuild: Structures [adorabuild-structures], AmbientSounds [ambientsounds], AppleSkin [appleskin], Ars Nouveau [ars-nouveau], Artifacts [artifacts], Ascended Quark [ascended-quark], ATMOSPHERICS [atmospherics], Auto Third Person [auto-third-person] (+105 more)

### Community 1 - "heracles:item"
Cohesion: 0.06
Nodes (79): apotheosis:gem_dust, apotheosis:progression/ascent, apotheosis:progression/frontier, apotheosis:sigil_of_socketing, deeperdarker:main/enter_otherside, heracles:block_interaction, heracles:changed_dimension, heracles:item (+71 more)

### Community 2 - "manifests/legends.json"
Cohesion: 0.05
Nodes (47): The Slider (aether:slider), Sun Spirit (aether:sun_spirit), Valkyrie Queen (aether:valkyrie_queen), Infernal Dragon (block_factorys_bosses:infernal_dragon), Kraken (block_factorys_bosses:kraken), Sandworm (block_factorys_bosses:sandworm), Underworld Knight (block_factorys_bosses:underworld_knight), Yeti (block_factorys_bosses:yeti) (+39 more)

### Community 3 - "net.neoforged.fml.common.Mod"
Cohesion: 0.09
Nodes (4): BettersmokeClient, HorizonQuestBook, ItemLandingSound, ModelAngles

### Community 4 - "horizon.py"
Cohesion: 0.10
Nodes (42): bare(), cmd_add(), cmd_check(), cmd_crash(), cmd_find(), cmd_perf(), cmd_qa(), confirm_experimental() (+34 more)

### Community 5 - "org.spongepowered.asm.mixin.injection.Inject"
Cohesion: 0.10
Nodes (7): LeavesBlockMixin, Snowiness, full, high, low, medium, none

### Community 6 - "heracles:xp"
Cohesion: 0.07
Nodes (50): apotheosis:gem_cutting_table, heracles:check, heracles:xp, horizon:hq/conservatory, horizon:hq/conservatory/ars, horizon:hq/conservatory/irons, horizon:hq/conservatory/occultism, horizon:hq/foundry (+42 more)

### Community 7 - "heracles:advancement"
Cohesion: 0.10
Nodes (36): heracles:advancement, heracles:loottable, horizon:atlas/roadside, horizon:rewards/quest/chart_temple, irons_spellbooks:irons_spellbooks/enter_catacombs, irons_spellbooks:irons_spellbooks/ink_legendary, irons_spellbooks:irons_spellbooks/make_inscription_table, minecraft:adventure/trade (+28 more)

### Community 8 - "horizon_headquarters.js"
Cohesion: 0.10
Nodes (32): btn(), HQ_BlockPos, HQ_BuiltInRegistries, HQ_CompoundTag, HQ_FakePlayerFactory, HQ_LootContextParams, HQ_LootContextParamSets, HQ_LootParamsBuilder (+24 more)

### Community 10 - "json"
Cohesion: 0.15
Nodes (14): canon(), j(), lock_jar(), main(), tec(), merge_biome(), patch(), get() (+6 more)

### Community 11 - "re"
Cohesion: 0.07
Nodes (17): visit(), main(), in_range(), main(), manifest_version(), scan(), vkey(), main() (+9 more)

### Community 12 - "zipfile"
Cohesion: 0.16
Nodes (14): build(), fetch(), main(), read_zip(), write_deterministic(), fix_model(), main(), add_model() (+6 more)

### Community 15 - "build.py"
Cohesion: 0.20
Nodes (13): copy_overrides(), deployed(), env(), fetch(), instance(), lock(), managed_names(), mrpack() (+5 more)

### Community 16 - "org.spongepowered.asm.mixin.Mixin"
Cohesion: 0.17
Nodes (4): BillboardParticleAccessor, ModScreensMixin, OffsetBoundsMixin, QuestsScreenInitMixin

### Community 17 - "audit_loot.py"
Cohesion: 0.18
Nodes (7): main(), _nbt(), read_nbt(), icon(), main(), png(), sounds_json()

### Community 19 - "horizon_graph.py"
Cohesion: 0.21
Nodes (11): build(), fingerprint(), graphify(), HorizonLinks, inputs(), is_current(), main(), read() (+3 more)

### Community 21 - "The High Landmarks (Expedition Hall option)"
Cohesion: 0.09
Nodes (31): The High Landmarks (Expedition Hall option), Landmark Chart (charter service), horizon:legend/ferrous_wroughtnaut, horizon:legend/frostmaw, horizon:legend/infernal_dragon, horizon:legend/kraken, horizon:legend/sandworm, horizon:legend/sculptor (+23 more)

### Community 23 - "First Blood [14bountiesandhunts_b_hunter]"
Cohesion: 0.09
Nodes (29): minecraft:adventure/arbalistic, minecraft:adventure/bullseye, minecraft:adventure/hero_of_the_village, minecraft:adventure/kill_a_mob, minecraft:adventure/kill_all_mobs, minecraft:adventure/sniper_duel, minecraft:adventure/totem_of_undying, minecraft:arrow (+21 more)

### Community 25 - "Iron Age [0thehorizoncampaign_c_iron]"
Cohesion: 0.09
Nodes (24): farmersdelight:cooking_pot, heracles:quest_book, minecraft:adventure/sleep_in_bed, minecraft:bread, minecraft:campfire, minecraft:coal, minecraft:cooked_beef, minecraft:golden_carrot (+16 more)

### Community 26 - "Geckolib [geckolib]"
Cohesion: 0.11
Nodes (23): Aether Villages [aether-villages], Architectury API [architectury-api], Born in Chaos [borninchaos], Bosses'Rise [bossesrise], Clavis [clavis], Companions! [companions-mod], Effectual [effectual], Fantasy Armor (Medieval Series) [fantasy_armor] (+15 more)

### Community 27 - "gen_headquarters.py"
Cohesion: 0.18
Nodes (16): adv_display(), alternatives(), clean(), emit_datapack(), emit_doc(), emit_graph(), emit_plans(), emit_server_data() (+8 more)

### Community 28 - "hq_sim.js"
Cohesion: 0.09
Nodes (12): A0, core, ctx, emptyScan, fs, near, path, ROOT (+4 more)

### Community 29 - "BettersmokeConfig"
Cohesion: 0.13
Nodes (3): BettersmokeConfig, BettersmokeConfigScreen, ConfigSlider

### Community 30 - "V. Foundry and Logistics (headquarters stage)"
Cohesion: 0.11
Nodes (19): Mekanism processing (Foundry and Logistics option), Modern Industrialization (Foundry and Logistics option), Powah energizing (Foundry and Logistics option), V. Foundry and Logistics (headquarters stage), ae2:controller, constructionstick:diamond_stick, constructionstick:template_replacement, create:brass_ingot (+11 more)

### Community 32 - "gen_datapack.py"
Cohesion: 0.10
Nodes (28): assert_budgets(), chance_entry(), classify_all(), clean_previous(), craftable_outputs(), emit_apotheosis(), emit_atlas(), emit_expeditions() (+20 more)

### Community 33 - "Bounty: Sky Wardens [14bountiesandhunts_b_aether_trio]"
Cohesion: 0.14
Nodes (18): aether:bronze_dungeon, aether:enter_aether, aether:gold_dungeon, horizon:legend/slider, horizon:legend/sun_spirit, horizon:legend/valkyrie_queen, minecraft:feather, simplehats:halo (+10 more)

### Community 34 - "sys"
Cohesion: 0.13
Nodes (6): main(), node(), pipeline(), snapshot(), step(), main()

### Community 35 - "gen_quests.py"
Cohesion: 0.13
Nodes (10): apotheosis:progression/pinnacle, modern_industrialization:fusion_reactor, occultism:chalks/root, undergarden:undergarden/kill_forgotten_guardian, Plasma Engineering [10beyondthehorizon_fusion_mi], World Tier: Pinnacle [10beyondthehorizon_pinnacle], The Forgotten Guardian [4forgottenrealms_forgotten_guardian], The Undergarden [4forgottenrealms_undergarden] (+2 more)

### Community 36 - "III. Expedition Hall (headquarters stage)"
Cohesion: 0.12
Nodes (16): The Drowned Coast (Expedition Hall option), Tide Chart (charter service), III. Expedition Hall (headquarters stage), horizon:discovery_case, horizon:emblem_hall, minecraft:anvil, minecraft:book, minecraft:chipped_anvil (+8 more)

### Community 37 - "Accessories [accessories]"
Cohesion: 0.13
Nodes (16): Accessories [accessories], Accessories Compatibility Layer [accessories-compat-layer], Accessories Compat: Elytra & Totem [accessories-compat-vanilla], Accessorify [accessorify], The Aether [aether], Curios API [curios], L_Ender's Cataclysm [l_enders-cataclysm], Lionfish-API [lionfish-api] (+8 more)

### Community 39 - "Cloth Config API [cloth-config]"
Cohesion: 0.12
Nodes (16): Better Combat [better-combat], Better ModList [better-modlist], BetterF3 [betterf3], Bosses of Mass Destruction Forge [bosses-of-mass-destruction-forge], CERBON's API [cerbons-api], Cloth Config API [cloth-config], Cristel Lib [cristel-lib], First-person Model [first-person-model] (+8 more)

### Community 41 - "II. Workshop (headquarters stage)"
Cohesion: 0.13
Nodes (15): II. Workshop (headquarters stage), constructionstick:iron_stick, create:andesite_alloy, create:basin, create:belt, create:depot, create:encased_fan, create:mechanical_press (+7 more)

### Community 42 - "A Gem of Your Choosing [11expeditionatlas_exchange_gem]"
Cohesion: 0.13
Nodes (15): heracles:recipe, horizon:exchange/cinder_idol_blood_lord, horizon:exchange/cinder_idol_inferno, horizon:exchange/cinder_idol_molten_breach, horizon:exchange/echoing_fossil_breach, horizon:exchange/echoing_fossil_guardian, horizon:exchange/honeyed_seal_splendor, horizon:exchange/honeyed_seal_verdant_ruin (+7 more)

### Community 43 - "The Hall of Legends [12halloflegends_hall]"
Cohesion: 0.15
Nodes (15): horizon:legend/cosmic_crystal_entity, horizon:legend/dead_king, horizon:legend/forgotten_guardian, horizon:legend/sacred_pontiff, horizon:legend/stalker, horizon:legend/warden, The Hall of Legends [12halloflegends_hall], Cosmic Crystal [12halloflegends_legend_cosmic_crystal_entity] (+7 more)

### Community 44 - "I. Outpost (headquarters stage)"
Cohesion: 0.14
Nodes (14): I. Outpost (headquarters stage), constructionstick:copper_stick, create:empty_schematic, horizon:emblem_outpost, minecraft:barrel, minecraft:cartography_table, minecraft:glass_pane, minecraft:husbandry/breed_an_animal (+6 more)

### Community 45 - "Bounty: Fire and Blood [14bountiesandhunts_b_nether_cabal]"
Cohesion: 0.18
Nodes (14): cataclysm:root, horizon:legend/ignis, horizon:legend/maledictus, horizon:legend/netherite_monstrosity, minecraft:netherite_scrap, Hunt: The Flame Knight [0thehorizoncampaign_c_ignis], Ignis [12halloflegends_legend_ignis], Maledictus [12halloflegends_legend_maledictus] (+6 more)

### Community 46 - "Trial of Cinders"
Cohesion: 0.19
Nodes (13): Nether Expeditions loot family [nether], apotheosis:the_nether/blood_lord, apotheosis:the_nether/inferno, apotheosis:the_nether/molten_breach, cataclysm:ignited_berserker, cataclysm:ignited_revenant, horizon:cinder_idol, minecraft:blaze (+5 more)

### Community 48 - "VI. Observatory and Horizon Beacon (headquarters stage)"
Cohesion: 0.15
Nodes (13): VI. Observatory and Horizon Beacon (headquarters stage), horizon:emblem_observatory, horizon:horizon_beacon, horizon:observatory_lens, horizon:realm/bumblezone, horizon:realm/moon, horizon:trial/cinders, horizon:trial/tides (+5 more)

### Community 49 - "The Controller [8thedigitalage_ae_controller]"
Cohesion: 0.15
Nodes (13): ae2:fluix_crystal, ae2:main/charged_quartz, ae2:main/controller, ae2:main/crafting_cpu, ae2:main/presses, ae2:wireless_terminal, appmek:chemical_storage_cell_1k, The Controller [8thedigitalage_ae_controller] (+5 more)

### Community 50 - "apotheosis:epic"
Cohesion: 0.23
Nodes (12): Boss Lairs loot family [boss_lair], The Deep (Otherside & Undergarden) loot family [deep], Great Landmarks loot family [landmark], Temples, Mansions & Outposts loot family [temple], apotheosis:epic, apotheosis:mythic, apotheosis:rare, horizon:echoing_fossil (+4 more)

### Community 51 - "Trial of the Void"
Cohesion: 0.20
Nodes (11): End Expeditions loot family [end], apotheosis:the_end/endersurge, apotheosis:the_end/mageslayer, Ender Golem (cataclysm:ender_golem), cataclysm:endermaptera, horizon:starlit_voidglass, minecraft:end_crystal, minecraft:enderman (+3 more)

### Community 52 - "Trial of the Tides"
Cohesion: 0.17
Nodes (12): Ocean Expeditions loot family [ocean], apotheosis:core/lunar, apotheosis:core/slipstream, cataclysm:deepling, cataclysm:deepling_angler, cataclysm:deepling_brute, cataclysm:deepling_priest, horizon:tidebound_doubloon (+4 more)

### Community 53 - "manifests/headquarters.json"
Cohesion: 0.20
Nodes (9): Supply Crate (charter service), Foundry Supply Crate (charter service), Horizon Chart (charter service), Lair Chart (charter service), Ward of Passage (charter service), IV. Arcane Conservatory (headquarters stage), horizon:ancient_core, horizon:emblem_conservatory (+1 more)

### Community 54 - "YUNG's API [yungs-api]"
Cohesion: 0.17
Nodes (12): YUNG's API [yungs-api], YUNG's Better Desert Temples [yungs-better-desert-temples], YUNG's Better Dungeons [yungs-better-dungeons], YUNG's Better End Island [yungs-better-end-island], YUNG's Better Jungle Temples [yungs-better-jungle-temples], YUNG's Better Mineshafts [yungs-better-mineshafts], YUNG's Better Nether Fortresses [yungs-better-nether-fortresses], YUNG's Better Ocean Monuments [yungs-better-ocean-monuments] (+4 more)

### Community 55 - "horizon_events.js"
Cohesion: 0.20
Nodes (10): audit(), auditInner(), LootContextParams, LootContextParamSets, LootParamsBuilder, Registries, ResourceKey, ResourceLocation (+2 more)

### Community 56 - "plans"
Cohesion: 0.26
Nodes (5): bed(), door(), Plan, plans(), roof()

### Community 57 - "Lithostitched [lithostitched]"
Cohesion: 0.20
Nodes (11): ChoiceTheorem's Overhauled Village [ct-overhaul-village], Dynamic Trees - Quark [dynamic-trees-quark], Dynamic Trees - Regions Unexplored [dynamic-trees-ru], Dynamic Trees - Terralith [dynamic-trees-terralith], Dynamic Trees [dynamictrees], Dynamic Trees Plus [dynamictreesplus], Improved Village Placement [improved-village-placement], Lithostitched [lithostitched] (+3 more)

### Community 59 - "manifests/loot_families.json"
Cohesion: 0.20
Nodes (9): The Aether loot family [aether], Roadside Ruins & Camps loot family [roadside], Settlements loot family [settlement], Underground Dungeons loot family [underground], horizon:skyward_plume, minecraft:bell, minecraft:glowstone, minecraft:mossy_cobblestone (+1 more)

### Community 60 - "Keeper of the Hall [0thehorizoncampaign_c_curator]"
Cohesion: 0.27
Nodes (10): gateways:gate_pearl, horizon:legend/ancient_remnant, horizon:legend/the_harbinger, horizon:trial/horizon, simplehats:crown, Keeper of the Hall [0thehorizoncampaign_c_curator], The Final Trial [0thehorizoncampaign_c_gauntlet], Curator of Legends [12halloflegends_hall_complete] (+2 more)

### Community 61 - "Bounty: Sea Raiders [14bountiesandhunts_b_sea_raiders]"
Cohesion: 0.22
Nodes (10): horizon:legend/clawdian, horizon:legend/elder_guardian, horizon:legend/scylla, horizon:legend/the_leviathan, Clawdian [12halloflegends_legend_clawdian], Elder Guardian [12halloflegends_legend_elder_guardian], Scylla [12halloflegends_legend_scylla], The Leviathan [12halloflegends_legend_the_leviathan] (+2 more)

### Community 62 - "Resourceful Lib [resourceful-lib]"
Cohesion: 0.22
Nodes (10): Ad Astra [ad-astra], Ad Astra: More Structures [ad-astra-more-structures], Common Storage Lib [common-storage-lib], Creeper Overhaul [creeper-overhaul], Handcrafted [handcrafted], Odyssey Quests [odyssey-quests], Resourceful Config [resourceful-config], Resourceful Lib [resourceful-lib] (+2 more)

### Community 63 - "Create [create]"
Cohesion: 0.29
Nodes (10): Create [create], Create: Dragons Plus [create-dragons-plus], Create: Enchantment Industry [create-enchantment-industry],  Integrated Dungeons and Structures [idas], Integrated API [integrated-api], Integrated Stronghold [integrated-stronghold], Moonlight Lib [moonlight], Quark [quark] (+2 more)

### Community 64 - "main"
Cohesion: 0.24
Nodes (9): check(), grid(), layout(), d(), main(), no_reward_shortcuts(), objective_why(), reward() (+1 more)

### Community 65 - "The Hollow Roads (Expedition Hall option)"
Cohesion: 0.22
Nodes (9): Arcane Sites loot family [arcane], Spell Forge (Iron's Spells) (Arcane Conservatory option), The Hollow Roads (Expedition Hall option), Archive Chart (charter service), horizon:wayfarer_shard, irons_spellbooks:arcane_anvil, irons_spellbooks:arcane_essence, irons_spellbooks:inscription_table (+1 more)

### Community 66 - "The Horizon Gauntlet"
Cohesion: 0.22
Nodes (9): The Bumblezone loot family [hive], horizon:honeyed_seal, horizon:starforged_heart, minecraft:evoker, minecraft:honeycomb, minecraft:pillager, minecraft:ravager, minecraft:vindicator (+1 more)

### Community 67 - "Bounty: Mass Destruction [14bountiesandhunts_b_mass_destruction]"
Cohesion: 0.31
Nodes (9): horizon:legend/gauntlet, horizon:legend/lich, horizon:legend/obsidilith, horizon:legend/void_blossom, Nether Gauntlet [12halloflegends_legend_gauntlet], Night Lich [12halloflegends_legend_lich], Obsidilith [12halloflegends_legend_obsidilith], Void Blossom [12halloflegends_legend_void_blossom] (+1 more)

### Community 68 - "Applied Energistics 2 [ae2]"
Cohesion: 0.22
Nodes (9): Applied Energistics 2 [ae2], Applied Energistics 2 Wireless Terminals [applied-energistics-2-wireless-terminals], Applied Mekanistics [applied-mekanistics], GuideME [guideme], MEGA Cells [mega], Mekanism [mekanism], Mekanism Generators [mekanism-generators], Modern Industrialization [modern-industrialization] (+1 more)

### Community 69 - "YetAnotherConfigLib (YACL) [yacl]"
Cohesion: 0.22
Nodes (9): Better Clouds [better-clouds], Controlify (Controller support) [controlify], MRU [mru], Particle Interactions [particle-interactions], Seamless Sleep [seamless-sleep], Sounds [sound], Spatial GUI [spatial-gui], Windy [windy] (+1 more)

### Community 70 - "Sodium [sodium]"
Cohesion: 0.28
Nodes (9): Sinytra Connector [connector], Continuity [continuity], Forgified Fabric API [forgified-fabric-api], Iris Shaders [iris], Reese's Sodium Options [reeses-sodium-options], Roxy [roxy], Sodium [sodium], Sodium Extra [sodium-extra] (+1 more)

### Community 71 - "Enchanting Apparatus [5arcanestudies_ars_apparatus]"
Cohesion: 0.32
Nodes (8): Source Study (Ars Nouveau) (Arcane Conservatory option), ars_nouveau:enchanting_apparatus, ars_nouveau:novice_spell_book, ars_nouveau:source_gem, ars_nouveau:worn_notebook, Enchanting Apparatus [5arcanestudies_ars_apparatus], Novice Spellcaster [5arcanestudies_ars_book], Worn Notebook [5arcanestudies_ars_start]

### Community 72 - "Spirit Circle (Occultism) (Arcane Conservatory option)"
Cohesion: 0.25
Nodes (8): Spirit Circle (Occultism) (Arcane Conservatory option), occultism:chalk_white, occultism:golden_sacrificial_bowl, occultism:occultism/summon_afrit_smelter, occultism:occultism/summon_djinni_crusher, occultism:occultism/summon_djinni_smelter, occultism:occultism/summon_foliot_lumberjack, occultism:occultism/summon_foliot_otherstone_trader

### Community 73 - "Mechanical Press [6mechanicalrevolution_press]"
Cohesion: 0.25
Nodes (8): create:andesite_casing, create:cogwheel, create:shaft, create:water_wheel, Andesite Alloy [6mechanicalrevolution_andesite], Conveyor [6mechanicalrevolution_belt], Mechanical Press [6mechanicalrevolution_press], Water Power [6mechanicalrevolution_waterwheel]

### Community 75 - "World Tier: Haven [3forgedinadventure_apoth_haven]"
Cohesion: 0.29
Nodes (7): apotheosis:progression/haven, minecraft:lapis_lazuli, minecraft:story/enchant_item, World Tier: Haven [3forgedinadventure_apoth_haven], Curious Trinket [3forgedinadventure_artifact], Deep Enchanting [3forgedinadventure_enchant], A Blade of Choice [3forgedinadventure_simply]

### Community 76 - "Conqueror of Calamity [0thehorizoncampaign_c_conqueror]"
Cohesion: 0.33
Nodes (7): apotheosis:progression/summit, apotheosis:sigil_of_enhancement, cataclysm:kill_all_bosses, simplehats:bigcrown, Conqueror of Calamity [0thehorizoncampaign_c_conqueror], Cataclysm Conqueror [10beyondthehorizon_all_cataclysm], World Tier: Summit [9legendsandconquests_apoth_summit]

### Community 77 - "Brass Age [6mechanicalrevolution_brass]"
Cohesion: 0.29
Nodes (7): create:brass, create:brass_casing, create_enchantment_industry:experienced_engineer, createaddition:alternator, Brass Age [6mechanicalrevolution_brass], Rotation to Power [6mechanicalrevolution_electric], Liquid Experience [6mechanicalrevolution_liquid_xp]

### Community 78 - "Apotheosis [apotheosis]"
Cohesion: 0.52
Nodes (7): Apotheosis [apotheosis], Apothic Attributes [apothic-attributes], Apothic-Enchanting [apothic-enchanting], Apothic-Spawners [apothic-spawners], Gateways to Eternity [gateways-to-eternity], Patchouli [patchouli], Placebo [placebo]

### Community 80 - "Bounty: End Cabal [14bountiesandhunts_b_end_cabal]"
Cohesion: 0.40
Nodes (6): horizon:legend/ender_dragon, horizon:legend/ender_golem, horizon:legend/ender_guardian, Ender Golem [12halloflegends_legend_ender_golem], Ender Guardian [12halloflegends_legend_ender_guardian], Bounty: End Cabal [14bountiesandhunts_b_end_cabal]

### Community 81 - "Electric Blast Furnace [7industrialexpansion_mi_ebf]"
Cohesion: 0.33
Nodes (6): modern_industrialization:bronze_furnace, modern_industrialization:bronze_ingot, modern_industrialization:distillation_tower, Oil and Chemistry [7industrialexpansion_mi_distill], Electric Blast Furnace [7industrialexpansion_mi_ebf], Steam Age [7industrialexpansion_mi_steam]

### Community 83 - "Hunt: The Withering [0thehorizoncampaign_c_wither]"
Cohesion: 0.40
Nodes (5): horizon:legend/wither, Hunt: The Withering [0thehorizoncampaign_c_wither], Ender Dragon [12halloflegends_legend_ender_dragon], Wither [12halloflegends_legend_wither], Wither Storm Lite [9legendsandconquests_wither]

### Community 84 - "Antimatter [10beyondthehorizon_antimatter]"
Cohesion: 0.50
Nodes (4): mekanism:antimatter, mekanismgenerators:fusion_reactor_controller, Antimatter [10beyondthehorizon_antimatter], Star in a Jar [10beyondthehorizon_fusion_mek]

### Community 85 - "Metallurgy [7industrialexpansion_mek_metallurgic]"
Cohesion: 0.50
Nodes (4): mekanism:ingot_osmium, mekanism:metallurgic_infuser, Metallurgy [7industrialexpansion_mek_metallurgic], Ore Multiplication [7industrialexpansion_mek_ore]

### Community 86 - "Legendary Tooltips [legendary-tooltips]"
Cohesion: 0.50
Nodes (4): Advancement Plaques [advancement-plaques], Iceberg [iceberg], Legendary Tooltips [legendary-tooltips], Prism [prism-lib]

### Community 87 - "apply-profile.ps1"
Cohesion: 0.83
Nodes (3): Set-JsonKeys(), Set-LineKeys(), Write-NoBom()

### Community 88 - "KubeJS [kubejs]"
Cohesion: 0.67
Nodes (3): Better Advanced Tooltips [better-advanced-tooltips], KubeJS [kubejs], Rhino [rhino]

## Knowledge Gaps
- **257 isolated node(s):** `SOUNDS`, `ResourceKey`, `ResourceLocation`, `Registries`, `LootContextParams` (+252 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 479 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Frontier Tier [0thehorizoncampaign_c_frontier]` connect `heracles:item` to `gen_quests.py`, `heracles:advancement`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **What connects `SOUNDS`, `ResourceKey`, `ResourceLocation` to the rest of the system?**
  _257 weakly-connected nodes found - possible missing edges._
- **Should `manifests/lock.json` be split into smaller, more focused modules?**
  _Cohesion score 0.03493253373313343 - nodes in this community are weakly interconnected._
- **Why does `Act II: The Wider World [0thehorizoncampaign_c_landmark]` connect `heracles:item` to `gen_quests.py`, `heracles:xp`, `heracles:advancement`, `The High Landmarks (Expedition Hall option)`, `Iron Age [0thehorizoncampaign_c_iron]`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **Should `heracles:item` be split into smaller, more focused modules?**
  _Cohesion score 0.05679974034404414 - nodes in this community are weakly interconnected._
- **Why does `Keeper of the Hall [0thehorizoncampaign_c_curator]` connect `Keeper of the Hall [0thehorizoncampaign_c_curator]` to `heracles:item`, `Bounty: Sky Wardens [14bountiesandhunts_b_aether_trio]`, `gen_quests.py`, `heracles:xp`, `heracles:advancement`, `The Hall of Legends [12halloflegends_hall]`, `Bounty: Fire and Blood [14bountiesandhunts_b_nether_cabal]`, `Bounty: End Cabal [14bountiesandhunts_b_end_cabal]`, `Hunt: The Withering [0thehorizoncampaign_c_wither]`, `Bounty: Sea Raiders [14bountiesandhunts_b_sea_raiders]`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **Should `manifests/legends.json` be split into smaller, more focused modules?**
  _Cohesion score 0.050505050505050504 - nodes in this community are weakly interconnected._
## Horizon coverage

Local code AST plus explicit mod requirements, quest prerequisites, resource IDs, boss/trial declarations and generator ownership. No LLM semantic pass. JSON provenance uses file + source_pointer; L1 is the file anchor. Dynamic KubeJS registrations and prose reasoning can be incomplete: inspect the actual source before edits.
