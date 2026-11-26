# Graph Report - project-horizon  (2026-11-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1491 nodes · 3774 edges · 101 communities (59 shown, 42 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f6bf1729`
- Check the source-content fingerprint with `python scripts/horizon_graph.py status`; the commit above is provenance, not the freshness check.
- Run `python scripts/horizon_graph.py build` after code changes (no API cost).

## Community Hubs (Navigation)
- manifests/lock.json
- heracles:xp
- heracles:item
- net.neoforged.fml.common.Mod
- horizon.py
- LeavesBlockMixin.java
- Master Cartographer [15discoveriesandrelics_d_cartographer]
- heracles:advancement
- manifests/legends.json
- org.spongepowered.asm.mixin.gen.Accessor
- json
- pathlib
- zipfile
- net.minecraft.core.BlockPos
- CampfireSmokeParticleMixin.java
- build.py
- org.spongepowered.asm.mixin.Mixin
- gen_assets.py
- Snowiness
- horizon_graph.py
- Iron Age [0thehorizoncampaign_c_iron]
- ClientBridge.java
- QuestPopupScreen
- ArmourSoundTweak.java
- Walker Between Worlds [15discoveriesandrelics_d_realms]
- Bounty: Sky Wardens [14bountiesandhunts_b_aether_trio]
- Bounty: Mass Destruction [14bountiesandhunts_b_mass_destruction]
- Brass Age [6mechanicalrevolution_brass]
- BettersmokeConfig
- Accessories [accessories]
- EatingAnimation.java
- gen_datapack.py
- Architectury API [architectury-api]
- sys
- gen_quests.py
- A Gem of Your Choosing [11expeditionatlas_exchange_gem]
- build_ports.py
- GuiGraphicsMixin.java
- Trial of Cinders
- Trial of the Tides
- main
- HorizonLinks
- manifests/loot_families.json
- Trial of the Void
- YUNG's API [yungs-api]
- horizon_events.js
- apotheosis:epic
- Bounty: The Block Factory Five [14bountiesandhunts_b_factory]
- Cloth Config API [cloth-config]
- Lithostitched [lithostitched]
- The Horizon Gauntlet
- Create [create]
- main
- The Controller [8thedigitalage_ae_controller]
- Ad Astra [ad-astra]
- Applied Energistics 2 [ae2]
- YetAnotherConfigLib (YACL) [yacl]
- Geckolib [geckolib]
- Sodium [sodium]
- HorizonGraphTests
- net.neoforged.bus.api.IEventBus
- remap_intermediary.py
- World Tier: Haven [3forgedinadventure_apoth_haven]
- Enchanting Apparatus [5arcanestudies_ars_apparatus]
- Electric Blast Furnace [7industrialexpansion_mi_ebf]
- Apotheosis [apotheosis]
- WindDirectionSlider
- emit_fallbacks
- solve
- Inscriber Presses [8thedigitalage_ae_presses]
- Antimatter [10beyondthehorizon_antimatter]
- Legendary Tooltips [legendary-tooltips]
- apply-profile.ps1
- KubeJS [kubejs]
- smoke.sh
- Spirits and Chalk [5arcanestudies_occultism]
- clean_previous

## God Nodes (most connected - your core abstractions)
1. `heracles:xp` - 170 edges
2. `heracles:advancement` - 167 edges
3. `heracles:item` - 122 edges
4. `AbstractParticleAccessor` - 27 edges
5. `Master Cartographer [15discoveriesandrelics_d_cartographer]` - 26 edges
6. `apotheosis:gem_dust` - 25 edges
7. `First Blood [14bountiesandhunts_b_hunter]` - 24 edges
8. `QuestPopupScreen` - 22 edges
9. `cmd_qa()` - 20 edges
10. `Keeper of the Hall [0thehorizoncampaign_c_curator]` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Contract: Fortress Raider [14bountiesandhunts_k_blaze]` --task_reference--> `minecraft:blaze_rod`  [EXTRACTED]
  config/heracles/quests/14bountiesandhunts/14bountiesandhunts_k_blaze.json → manifests/expeditions.json
- `Contract: Bone Orchard [14bountiesandhunts_k_skulls]` --task_reference--> `minecraft:wither_skeleton_skull`  [EXTRACTED]
  config/heracles/quests/14bountiesandhunts/14bountiesandhunts_k_skulls.json → manifests/loot_families.json
- `Echoes [15discoveriesandrelics_d_deep]` --reward_reference--> `minecraft:echo_shard`  [EXTRACTED]
  config/heracles/quests/15discoveriesandrelics/15discoveriesandrelics_d_deep.json → manifests/loot_families.json
- `Heart of the Stars [15discoveriesandrelics_d_relic_heart]` --task_reference--> `horizon:starforged_heart`  [EXTRACTED]
  config/heracles/quests/15discoveriesandrelics/15discoveriesandrelics_d_relic_heart.json → manifests/expeditions.json
- `Bee Whisperer [10beyondthehorizon_bumble_all]` --reward_reference--> `horizon:honeyed_seal`  [EXTRACTED]
  config/heracles/quests/10beyondthehorizon/10beyondthehorizon_bumble_all.json → manifests/loot_families.json

## Import Cycles
- None detected.

## Communities (101 total, 42 thin omitted)

### Community 0 - "manifests/lock.json"
Cohesion: 0.04
Nodes (109): AdoraBuild: Structures [adorabuild-structures], AmbientSounds [ambientsounds], AppleSkin [appleskin], Ars Nouveau [ars-nouveau], Artifacts [artifacts], Ascended Quark [ascended-quark], ATMOSPHERICS [atmospherics], Auto Third Person [auto-third-person] (+101 more)

### Community 1 - "heracles:xp"
Cohesion: 0.05
Nodes (77): apotheosis:gem_cutting_table, apotheosis:progression/pinnacle, cataclysm:root, gateways:gate_pearl, heracles:check, heracles:xp, horizon:legend/ancient_remnant, horizon:legend/clawdian (+69 more)

### Community 2 - "heracles:item"
Cohesion: 0.06
Nodes (62): apotheosis:gem_dust, apotheosis:progression/ascent, apotheosis:progression/frontier, apotheosis:sigil_of_socketing, heracles:item, horizon:atlas/underground, horizon:wayfarer_shard, minecraft:adventure/arbalistic (+54 more)

### Community 3 - "net.neoforged.fml.common.Mod"
Cohesion: 0.10
Nodes (4): BettersmokeClient, HorizonQuestBook, ItemLandingSound, ModelAngles

### Community 4 - "horizon.py"
Cohesion: 0.11
Nodes (38): bare(), cmd_add(), cmd_check(), cmd_crash(), cmd_find(), cmd_perf(), cmd_qa(), die() (+30 more)

### Community 6 - "Master Cartographer [15discoveriesandrelics_d_cartographer]"
Cohesion: 0.06
Nodes (57): apotheosis:salvaging_table, heracles:block_interaction, heracles:changed_dimension, heracles:loottable, horizon:atlas/aether, horizon:atlas/arcane, horizon:atlas/boss_lair, horizon:atlas/deep (+49 more)

### Community 7 - "heracles:advancement"
Cohesion: 0.07
Nodes (42): ars_nouveau:archmage_spell_book, heracles:advancement, horizon:legend/ferrous_wroughtnaut, horizon:legend/frostmaw, horizon:legend/sculptor, horizon:legend/umvuthi, horizon:legend/wither, irons_spellbooks:arcane_essence (+34 more)

### Community 8 - "manifests/legends.json"
Cohesion: 0.05
Nodes (35): The Slider (aether:slider), Sun Spirit (aether:sun_spirit), Valkyrie Queen (aether:valkyrie_queen), Infernal Dragon (block_factorys_bosses:infernal_dragon), Kraken (block_factorys_bosses:kraken), Sandworm (block_factorys_bosses:sandworm), Underworld Knight (block_factorys_bosses:underworld_knight), Yeti (block_factorys_bosses:yeti) (+27 more)

### Community 10 - "json"
Cohesion: 0.16
Nodes (13): canon(), j(), lock_jar(), main(), tec(), merge_biome(), get(), main() (+5 more)

### Community 11 - "pathlib"
Cohesion: 0.09
Nodes (8): visit(), main(), main(), find_jar(), main(), refs(), main(), main()

### Community 12 - "zipfile"
Cohesion: 0.15
Nodes (11): main(), _nbt(), read_nbt(), in_range(), main(), manifest_version(), scan(), vkey() (+3 more)

### Community 15 - "build.py"
Cohesion: 0.14
Nodes (18): copy_overrides(), deployed(), env(), fetch(), instance(), lock(), managed_names(), mrpack() (+10 more)

### Community 16 - "org.spongepowered.asm.mixin.Mixin"
Cohesion: 0.13
Nodes (6): BillboardParticleAccessor, ModScreensMixin, OffsetBoundsMixin, QuestClickMixin, QuestsScreenInitMixin, BlockElementDeserializerMixin

### Community 17 - "gen_assets.py"
Cohesion: 0.13
Nodes (15): canvas(), m(), main(), mix(), paint(), pedestal(), png(), put() (+7 more)

### Community 18 - "Snowiness"
Cohesion: 0.13
Nodes (6): Snowiness, full, high, low, medium, none

### Community 19 - "horizon_graph.py"
Cohesion: 0.23
Nodes (13): main(), pipeline(), snapshot(), step(), build(), fingerprint(), graphify(), inputs() (+5 more)

### Community 21 - "Iron Age [0thehorizoncampaign_c_iron]"
Cohesion: 0.09
Nodes (27): farmersdelight:cooking_pot, heracles:quest_book, minecraft:adventure/sleep_in_bed, minecraft:bread, minecraft:campfire, minecraft:coal, minecraft:cooked_beef, minecraft:golden_carrot (+19 more)

### Community 25 - "Walker Between Worlds [15discoveriesandrelics_d_realms]"
Cohesion: 0.13
Nodes (19): deeperdarker:main/enter_otherside, minecraft:cooked_porkchop, minecraft:end/kill_dragon, minecraft:golden_apple, minecraft:story/enter_the_end, minecraft:story/enter_the_nether, simplehats:dragonskullender, undergarden:undergarden/enter_undergarden (+11 more)

### Community 26 - "Bounty: Sky Wardens [14bountiesandhunts_b_aether_trio]"
Cohesion: 0.14
Nodes (18): aether:bronze_dungeon, aether:enter_aether, aether:gold_dungeon, horizon:legend/slider, horizon:legend/sun_spirit, horizon:legend/valkyrie_queen, minecraft:feather, simplehats:halo (+10 more)

### Community 27 - "Bounty: Mass Destruction [14bountiesandhunts_b_mass_destruction]"
Cohesion: 0.15
Nodes (18): apotheosis:progression/summit, apotheosis:sigil_of_enhancement, cataclysm:kill_all_bosses, horizon:legend/gauntlet, horizon:legend/lich, horizon:legend/obsidilith, horizon:legend/void_blossom, minecraft:netherite_scrap (+10 more)

### Community 28 - "Brass Age [6mechanicalrevolution_brass]"
Cohesion: 0.11
Nodes (18): create:andesite_alloy, create:andesite_casing, create:belt, create:brass, create:brass_casing, create:cogwheel, create:mechanical_press, create:shaft (+10 more)

### Community 29 - "BettersmokeConfig"
Cohesion: 0.13
Nodes (3): BettersmokeConfig, BettersmokeConfigScreen, ConfigSlider

### Community 30 - "Accessories [accessories]"
Cohesion: 0.12
Nodes (17): Accessories [accessories], Accessories Compatibility Layer [accessories-compat-layer], Accessories Compat: Elytra & Totem [accessories-compat-vanilla], Accessorify [accessorify], The Aether [aether], Curios API [curios], L_Ender's Cataclysm [l_enders-cataclysm], Lionfish-API [lionfish-api] (+9 more)

### Community 32 - "gen_datapack.py"
Cohesion: 0.23
Nodes (8): chance_entry(), craftable_outputs(), emit_expeditions(), expand_tag(), gem_min_purity(), gem_stack(), jar_files(), jar_index()

### Community 33 - "Architectury API [architectury-api]"
Cohesion: 0.17
Nodes (16): Aether Villages [aether-villages], Architectury API [architectury-api], Clavis [clavis], Effectual [effectual], Fzzy Config [fzzy-config], Hybrid API [HAPI] [hybrid-api], Hybrid Aquatic [hybrid-aquatic], Kotlin for Forge [kotlin-for-forge] (+8 more)

### Community 35 - "gen_quests.py"
Cohesion: 0.13
Nodes (8): computercraft:computer_normal, megacells:cell_component_256m, modern_industrialization:fusion_reactor, powah:energizing_orb, Plasma Engineering [10beyondthehorizon_fusion_mi], Unlimited Storage [10beyondthehorizon_mega], Programmable World [7industrialexpansion_cc], Simple Power [7industrialexpansion_powah]

### Community 36 - "A Gem of Your Choosing [11expeditionatlas_exchange_gem]"
Cohesion: 0.13
Nodes (15): heracles:recipe, horizon:exchange/cinder_idol_blood_lord, horizon:exchange/cinder_idol_inferno, horizon:exchange/cinder_idol_molten_breach, horizon:exchange/echoing_fossil_breach, horizon:exchange/echoing_fossil_guardian, horizon:exchange/honeyed_seal_splendor, horizon:exchange/honeyed_seal_verdant_ruin (+7 more)

### Community 37 - "build_ports.py"
Cohesion: 0.22
Nodes (10): build(), fetch(), main(), read_zip(), write_deterministic(), fix_model(), main(), add_model() (+2 more)

### Community 39 - "Trial of Cinders"
Cohesion: 0.19
Nodes (13): Nether Expeditions loot family [nether], apotheosis:the_nether/blood_lord, apotheosis:the_nether/inferno, apotheosis:the_nether/molten_breach, cataclysm:ignited_berserker, cataclysm:ignited_revenant, horizon:cinder_idol, minecraft:blaze (+5 more)

### Community 40 - "Trial of the Tides"
Cohesion: 0.15
Nodes (13): Ocean Expeditions loot family [ocean], apotheosis:core/lunar, apotheosis:core/slipstream, cataclysm:deepling, cataclysm:deepling_angler, cataclysm:deepling_brute, cataclysm:deepling_priest, horizon:tidebound_doubloon (+5 more)

### Community 41 - "main"
Cohesion: 0.26
Nodes (10): assert_budgets(), emit_apotheosis(), emit_atlas(), emit_families(), emit_legends(), jar_json(), main(), map_entry() (+2 more)

### Community 43 - "manifests/loot_families.json"
Cohesion: 0.17
Nodes (11): The Aether loot family [aether], Arcane Sites loot family [arcane], Roadside Ruins & Camps loot family [roadside], Settlements loot family [settlement], Underground Dungeons loot family [underground], horizon:skyward_plume, irons_spellbooks:inscription_table, minecraft:bell (+3 more)

### Community 44 - "Trial of the Void"
Cohesion: 0.20
Nodes (11): End Expeditions loot family [end], apotheosis:the_end/endersurge, apotheosis:the_end/mageslayer, cataclysm:endermaptera, horizon:ancient_core, horizon:starlit_voidglass, minecraft:end_crystal, minecraft:enderman (+3 more)

### Community 46 - "YUNG's API [yungs-api]"
Cohesion: 0.17
Nodes (12): YUNG's API [yungs-api], YUNG's Better Desert Temples [yungs-better-desert-temples], YUNG's Better Dungeons [yungs-better-dungeons], YUNG's Better End Island [yungs-better-end-island], YUNG's Better Jungle Temples [yungs-better-jungle-temples], YUNG's Better Mineshafts [yungs-better-mineshafts], YUNG's Better Nether Fortresses [yungs-better-nether-fortresses], YUNG's Better Ocean Monuments [yungs-better-ocean-monuments] (+4 more)

### Community 47 - "horizon_events.js"
Cohesion: 0.20
Nodes (10): audit(), auditInner(), LootContextParams, LootContextParamSets, LootParamsBuilder, Registries, ResourceKey, ResourceLocation (+2 more)

### Community 48 - "apotheosis:epic"
Cohesion: 0.25
Nodes (11): Boss Lairs loot family [boss_lair], The Deep (Otherside & Undergarden) loot family [deep], Great Landmarks loot family [landmark], Temples, Mansions & Outposts loot family [temple], apotheosis:epic, apotheosis:mythic, apotheosis:rare, horizon:echoing_fossil (+3 more)

### Community 49 - "Bounty: The Block Factory Five [14bountiesandhunts_b_factory]"
Cohesion: 0.25
Nodes (11): horizon:legend/infernal_dragon, horizon:legend/kraken, horizon:legend/sandworm, horizon:legend/underworld_knight, horizon:legend/yeti, Infernal Dragon [12halloflegends_legend_infernal_dragon], Kraken [12halloflegends_legend_kraken], Sandworm [12halloflegends_legend_sandworm] (+3 more)

### Community 50 - "Cloth Config API [cloth-config]"
Cohesion: 0.18
Nodes (11): Better Combat [better-combat], Better ModList [better-modlist], BetterF3 [betterf3], Cloth Config API [cloth-config], Cristel Lib [cristel-lib], More Culling [moreculling], Mythic Upgrades [mythic-upgrades], playerAnimator [playeranimator] (+3 more)

### Community 51 - "Lithostitched [lithostitched]"
Cohesion: 0.20
Nodes (11): ChoiceTheorem's Overhauled Village [ct-overhaul-village], Dynamic Trees - Quark [dynamic-trees-quark], Dynamic Trees - Regions Unexplored [dynamic-trees-ru], Dynamic Trees - Terralith [dynamic-trees-terralith], Dynamic Trees [dynamictrees], Dynamic Trees Plus [dynamictreesplus], Improved Village Placement [improved-village-placement], Lithostitched [lithostitched] (+3 more)

### Community 52 - "The Horizon Gauntlet"
Cohesion: 0.20
Nodes (10): The Bumblezone loot family [hive], Ender Golem (cataclysm:ender_golem), horizon:honeyed_seal, horizon:starforged_heart, minecraft:evoker, minecraft:honeycomb, minecraft:pillager, minecraft:ravager (+2 more)

### Community 53 - "Create [create]"
Cohesion: 0.29
Nodes (10): Create [create], Create: Dragons Plus [create-dragons-plus], Create: Enchantment Industry [create-enchantment-industry],  Integrated Dungeons and Structures [idas], Integrated API [integrated-api], Integrated Stronghold [integrated-stronghold], Moonlight Lib [moonlight], Quark [quark] (+2 more)

### Community 54 - "main"
Cohesion: 0.24
Nodes (9): check(), grid(), layout(), d(), main(), no_reward_shortcuts(), objective_why(), reward() (+1 more)

### Community 55 - "The Controller [8thedigitalage_ae_controller]"
Cohesion: 0.22
Nodes (9): ae2:fluix_crystal, ae2:main/controller, ae2:main/crafting_cpu, ae2:wireless_terminal, appmek:chemical_storage_cell_1k, The Controller [8thedigitalage_ae_controller], Autocrafting [8thedigitalage_ae_crafting], Chemical Storage [8thedigitalage_ae_mek] (+1 more)

### Community 56 - "Ad Astra [ad-astra]"
Cohesion: 0.25
Nodes (9): Ad Astra [ad-astra], Ad Astra: More Structures [ad-astra-more-structures], Common Storage Lib [common-storage-lib], Creeper Overhaul [creeper-overhaul], Odyssey Quests [odyssey-quests], Resourceful Config [resourceful-config], Resourceful Lib [resourceful-lib], The Bumblezone - NeoForge/Forge [the-bumblezone] (+1 more)

### Community 57 - "Applied Energistics 2 [ae2]"
Cohesion: 0.22
Nodes (9): Applied Energistics 2 [ae2], Applied Energistics 2 Wireless Terminals [applied-energistics-2-wireless-terminals], Applied Mekanistics [applied-mekanistics], GuideME [guideme], MEGA Cells [mega], Mekanism [mekanism], Mekanism Generators [mekanism-generators], Modern Industrialization [modern-industrialization] (+1 more)

### Community 58 - "YetAnotherConfigLib (YACL) [yacl]"
Cohesion: 0.22
Nodes (9): Better Clouds [better-clouds], Controlify (Controller support) [controlify], MRU [mru], Particle Interactions [particle-interactions], Seamless Sleep [seamless-sleep], Sounds [sound], Spatial GUI [spatial-gui], Windy [windy] (+1 more)

### Community 59 - "Geckolib [geckolib]"
Cohesion: 0.22
Nodes (9): Born in Chaos [borninchaos], Bosses of Mass Destruction Forge [bosses-of-mass-destruction-forge], Bosses'Rise [bossesrise], CERBON's API [cerbons-api], Companions! [companions-mod], Fantasy Armor (Medieval Series) [fantasy_armor], Geckolib [geckolib], Knight Lib [knight-lib] (+1 more)

### Community 60 - "Sodium [sodium]"
Cohesion: 0.28
Nodes (9): Sinytra Connector [connector], Continuity [continuity], Forgified Fabric API [forgified-fabric-api], Iris Shaders [iris], Reese's Sodium Options [reeses-sodium-options], Roxy [roxy], Sodium [sodium], Sodium Extra [sodium-extra] (+1 more)

### Community 64 - "World Tier: Haven [3forgedinadventure_apoth_haven]"
Cohesion: 0.29
Nodes (7): apotheosis:progression/haven, minecraft:lapis_lazuli, minecraft:story/enchant_item, World Tier: Haven [3forgedinadventure_apoth_haven], Curious Trinket [3forgedinadventure_artifact], Deep Enchanting [3forgedinadventure_enchant], A Blade of Choice [3forgedinadventure_simply]

### Community 65 - "Enchanting Apparatus [5arcanestudies_ars_apparatus]"
Cohesion: 0.33
Nodes (7): ars_nouveau:enchanting_apparatus, ars_nouveau:novice_spell_book, ars_nouveau:source_gem, ars_nouveau:worn_notebook, Enchanting Apparatus [5arcanestudies_ars_apparatus], Novice Spellcaster [5arcanestudies_ars_book], Worn Notebook [5arcanestudies_ars_start]

### Community 66 - "Electric Blast Furnace [7industrialexpansion_mi_ebf]"
Cohesion: 0.29
Nodes (7): modern_industrialization:bronze_furnace, modern_industrialization:bronze_ingot, modern_industrialization:distillation_tower, modern_industrialization:electric_blast_furnace, Oil and Chemistry [7industrialexpansion_mi_distill], Electric Blast Furnace [7industrialexpansion_mi_ebf], Steam Age [7industrialexpansion_mi_steam]

### Community 67 - "Apotheosis [apotheosis]"
Cohesion: 0.52
Nodes (7): Apotheosis [apotheosis], Apothic Attributes [apothic-attributes], Apothic-Enchanting [apothic-enchanting], Apothic-Spawners [apothic-spawners], Gateways to Eternity [gateways-to-eternity], Patchouli [patchouli], Placebo [placebo]

### Community 69 - "emit_fallbacks"
Cohesion: 0.38
Nodes (6): classify_all(), emit_fallbacks(), first(), is_container_table(), report(), role_of()

### Community 70 - "solve"
Cohesion: 0.29
Nodes (3): group_key(), groups_from_audit(), solve()

### Community 71 - "Inscriber Presses [8thedigitalage_ae_presses]"
Cohesion: 0.50
Nodes (4): ae2:main/charged_quartz, ae2:main/presses, Inscriber Presses [8thedigitalage_ae_presses], Charged Quartz [8thedigitalage_ae_quartz]

### Community 72 - "Antimatter [10beyondthehorizon_antimatter]"
Cohesion: 0.50
Nodes (4): mekanism:antimatter, mekanismgenerators:fusion_reactor_controller, Antimatter [10beyondthehorizon_antimatter], Star in a Jar [10beyondthehorizon_fusion_mek]

### Community 73 - "Legendary Tooltips [legendary-tooltips]"
Cohesion: 0.50
Nodes (4): Advancement Plaques [advancement-plaques], Iceberg [iceberg], Legendary Tooltips [legendary-tooltips], Prism [prism-lib]

### Community 74 - "apply-profile.ps1"
Cohesion: 0.83
Nodes (3): Set-JsonKeys(), Set-LineKeys(), Write-NoBom()

### Community 75 - "KubeJS [kubejs]"
Cohesion: 0.67
Nodes (3): Better Advanced Tooltips [better-advanced-tooltips], KubeJS [kubejs], Rhino [rhino]

## Knowledge Gaps
- **176 isolated node(s):** `SOUNDS`, `ResourceKey`, `ResourceLocation`, `Registries`, `LootContextParams` (+171 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 373 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Iron Age [0thehorizoncampaign_c_iron]` connect `Iron Age [0thehorizoncampaign_c_iron]` to `heracles:item`, `gen_quests.py`, `heracles:advancement`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **What connects `SOUNDS`, `ResourceKey`, `ResourceLocation` to the rest of the system?**
  _176 weakly-connected nodes found - possible missing edges._
- **Should `manifests/lock.json` be split into smaller, more focused modules?**
  _Cohesion score 0.036196911196911194 - nodes in this community are weakly interconnected._
- **Why does `First Blood [14bountiesandhunts_b_hunter]` connect `heracles:item` to `gen_quests.py`, `Iron Age [0thehorizoncampaign_c_iron]`, `heracles:advancement`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **Should `heracles:xp` be split into smaller, more focused modules?**
  _Cohesion score 0.053998632946001365 - nodes in this community are weakly interconnected._
- **Should `heracles:item` be split into smaller, more focused modules?**
  _Cohesion score 0.06187202538339503 - nodes in this community are weakly interconnected._
- **Should `net.neoforged.fml.common.Mod` be split into smaller, more focused modules?**
  _Cohesion score 0.09788359788359788 - nodes in this community are weakly interconnected._
## Horizon coverage

Local code AST plus explicit mod requirements, quest prerequisites, resource IDs, boss/trial declarations and generator ownership. No LLM semantic pass. JSON provenance uses file + source_pointer; L1 is the file anchor. Dynamic KubeJS registrations and prose reasoning can be incomplete: inspect the actual source before edits.
