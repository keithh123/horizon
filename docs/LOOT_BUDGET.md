# Loot budget report (generated)

Expected Horizon rewards for one full clear of each structure group, computed by `scripts/gen_datapack.py` from the
real container counts in the structure templates (`scripts/audit_loot.py`). Each template is counted once; jigsaw
structures that repeat a piece have more containers, so treat these as per-unique-layout figures. Apotheosis' affix
and gem numbers are the expected count of injected affix items / gems on top of each structure's own loot.
Rows marked **(measured)** use container counts from real placed structures (`scripts/calibrate.py`), which include
repeated jigsaw pieces; the solver budgets those structures from the measured counts.

Tables classified: 982 - inject tables: 319 - placed but unassigned (no Horizon injection): 502

## The Aether (`aether`) - 1 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `aether:ruined_portal` | 13 | 0 | 0.49 | 0 | 0.0 | 2.01 | 1.0 | 0.81 |

## Arcane Sites (`arcane`) - 12 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `irons_spellbooks:catacombs` | 88 | 0.83 | 0.7 | 0 | 0.0 | 0 | 1.03 | 1.03 |
| `irons_spellbooks:pyromancer_tower` | 50 | 0.79 | 0.35 | 0 | 0.0 | 0 | 0.8 | 0.8 |
| `irons_spellbooks:villages` | 33 | 0.55 | 0.7 | 0 | 0.0 | 0 | 0.88 | 0.88 |
| `irons_spellbooks:evoker_fort` | 30 | 0.56 | 0.26 | 0 | 0.0 | 0 | 0.51 | 0.51 |
| `terralith:mage` | 29 | 0.8 | 0.69 | 0 | 0.0 | 0 | 1.19 | 1.19 |
| `irons_spellbooks:ice_spider_den` | 18 | 0.57 | 0.25 | 0 | 0.0 | 0 | 0.53 | 0.53 |
| `irons_spellbooks:mountain_tower` | 10 | 0.56 | 0.28 | 0 | 0.0 | 0 | 0.58 | 0.55 |
| `irons_spellbooks:mangrove_hut` | 8 | 0.8 | 0.32 | 0 | 0.0 | 0 | 0.78 | 0.78 |
| `irons_spellbooks:battleground` | 5 | 0.8 | 0.7 | 0 | 0.0 | 0 | 1.2 | 1.2 |
| `irons_spellbooks:impaled_icebreaker` | 4 | 0.65 | 0 | 0 | 0.0 | 0 | 0.93 | 0.93 |
| `irons_spellbooks:priest_house` | 3 | 0.05 | 0.06 | 0 | 0.0 | 0 | 0.08 | 0.08 |
| `irons_spellbooks:priest_house_taiga` | 3 | 0.05 | 0.06 | 0 | 0.0 | 0 | 0.08 | 0.08 |

## Boss Lairs (`boss_lair`) - 7 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `block_factorys_bosses:underworld_arena` | 72 | 0 | 0.99 | 0 | 0.0 | 0 | 2.99 | 2.0 |
| `block_factorys_bosses:dragon_tower` | 25 | 0 | 0 | 0 | 0.0 | 0 | 3.0 | 2.0 |
| `cataclysm:acropolis` | 24 | 0 | 1.01 | 0 | 0.0 | 0 | 3.0 | 1.99 |
| `cataclysm:frosted_prison` | 14 | 0.01 | 1.18 | 0.06 | 0.06 | 0.26 | 3.35 | 2.23 |
| `mowziesmobs:monastery` | 11 | 0 | 1.0 | 0 | 0.0 | 0 | 3.0 | 2.0 |
| `bosses_of_mass_destruction:lich_tower` | 5 | 0 | 1.0 | 0 | 0.0 | 0 | 3.0 | 2.0 |
| `cataclysm:amethyst_nest` | 2 | 0 | 1.0 | 0 | 0.0 | 0 | 1.2 | 0.9 |

## The Deep (Otherside & Undergarden) (`deep`) - 5 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `deeperdarker:ancient_temple` | 36 | 0 | 1.0 | 0.2 | 0.18 | 2.52 | 2.0 | 1.4 |
| `repurposed_structures:ancient_cities/ocean` | 14 | 0 | 0.99 | 0 | 0.0 | 2.5 | 2.0 | 1.4 |
| `undergarden:denizen_camp` | 13 | 0 | 1.0 | 0 | 0.0 | 2.5 | 2.0 | 1.4 |
| `undergarden:catacombs` | 11 | 0 | 1.0 | 0 | 0.0 | 2.51 | 2.0 | 1.4 |
| `undergarden:depleted_mine` | 3 | 0 | 1.0 | 0 | 0.0 | 2.5 | 1.75 | 1.28 |

## End Expeditions (`end`) - 19 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `nova_structures:end_castle` **(measured)** | 187.0 | 0 | 1.01 | 0.26 | 0.23 | 2.54 | 2.53 | 1.71 |
| `repurposed_structures:shipwrecks/end` | 38 | 0 | 1.0 | 0.25 | 0.23 | 2.55 | 2.56 | 1.7 |
| `repurposed_structures:ancient_cities/end` | 14 | 0 | 0.99 | 0 | 0.0 | 3.0 | 3.0 | 2.0 |
| `cataclysm:ruined_citadel` | 13 | 0.05 | 0.35 | 0.13 | 0.12 | 0.53 | 0.74 | 0.49 |
| `nova_structures:end_lighthouse` | 8 | 0 | 0 | 0 | 0.0 | 3.0 | 3.0 | 2.0 |
| `adorabuild_structures:ancient_palace_1` | 4 | 0 | 0.18 | 0.06 | 0.06 | 0.26 | 0.34 | 0.22 |
| `adorabuild_structures:ancient_palace_2` | 4 | 0 | 0.18 | 0.06 | 0.06 | 0.26 | 0.34 | 0.22 |
| `adorabuild_structures:ancient_palace_3` | 4 | 0 | 0.18 | 0.06 | 0.06 | 0.26 | 0.34 | 0.22 |
| `adorabuild_structures:end_temple_large_1` | 4 | 0 | 0.18 | 0.06 | 0.06 | 0.26 | 0.34 | 0.22 |
| `explorify:end_shipwreck` | 4 | 0 | 0.18 | 0.06 | 0.06 | 0.26 | 0.34 | 0.22 |
| `adorabuild_structures:end_temple_small_1` | 2 | 0 | 0.09 | 0.03 | 0.03 | 0.13 | 0.17 | 0.11 |
| `repurposed_structures:ruined_portals` | 2 | 0 | 1.0 | 0 | 0.0 | 2.1 | 1.2 | 0.9 |
| `adorabuild_structures:end_bubble_medium_1` | 1 | 0 | 0.04 | 0.02 | 0.02 | 0.07 | 0.08 | 0.06 |
| `adorabuild_structures:end_house_medium_1` | 1 | 0 | 0.04 | 0.02 | 0.02 | 0.07 | 0.08 | 0.06 |
| `adorabuild_structures:end_house_medium_2` | 1 | 0 | 0.04 | 0.02 | 0.02 | 0.07 | 0.08 | 0.06 |
| `adorabuild_structures:end_house_medium_3` | 1 | 0 | 0.04 | 0.02 | 0.02 | 0.07 | 0.08 | 0.06 |
| `adorabuild_structures:end_house_small_1` | 1 | 0 | 0.04 | 0.02 | 0.02 | 0.07 | 0.08 | 0.06 |
| `adorabuild_structures:end_house_small_2` | 1 | 0 | 0.04 | 0.02 | 0.02 | 0.07 | 0.08 | 0.06 |
| `adorabuild_structures:end_ship_small_1` | 1 | 0 | 0.04 | 0.02 | 0.02 | 0.07 | 0.08 | 0.06 |

## The Bumblezone (`hive`) - 19 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `the_bumblezone:sempiternal_sanctum` | 504 | 0 | 0 | 0 | 0.0 | 1.46 | 0 | 0 |
| `the_bumblezone:cell_maze` | 176 | 0.98 | 0.36 | 0 | 0.0 | 1.4 | 0.61 | 0.43 |
| `the_bumblezone:subway` | 31 | 0.99 | 0.34 | 0 | 0.0 | 2.0 | 0.81 | 0.59 |
| `the_bumblezone:bumbling_beepartments` | 28 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.59 |
| `the_bumblezone:battle_cubes` | 22 | 0.99 | 0.35 | 0 | 0.0 | 2.01 | 0.79 | 0.59 |
| `the_bumblezone:honitel` | 20 | 1.0 | 0.34 | 0 | 0.0 | 2.01 | 0.8 | 0.6 |
| `the_bumblezone:honey_cave_room` | 14 | 0.99 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:phantasm_aviary` | 8 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:gazebuzz_cluster` | 7 | 0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:pirate_ship` | 6 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:hive_temple` | 5 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:ancient_hoops` | 4 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:bee_house` | 4 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:candle_parkour` | 4 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:cannon_range` | 4 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:mite_fortress` | 4 | 1.0 | 0 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:throne_pillar` | 4 | 0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:floaters` | 3 | 1.0 | 0.35 | 0 | 0.0 | 2.0 | 0.8 | 0.6 |
| `the_bumblezone:hive_voyager` | 1 | 0.6 | 0.35 | 0 | 0.0 | 1.05 | 0.6 | 0.45 |

## Great Landmarks (`landmark`) - 11 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `dungeons_arise:bandit_towers` **(measured)** | 450.0 | 3.7 | 2.49 | 1.22 | 0.71 | 0 | 4.68 | 2.82 |
| `dungeons_arise:mechanical_nest` **(measured)** | 374.0 | 5.6 | 2.49 | 1.2 | 0.71 | 0 | 6.85 | 4.22 |
| `dungeons_arise:plague_asylum` **(measured)** | 159.0 | 4.55 | 2.92 | 1.2 | 0.73 | 1.99 | 7.24 | 4.51 |
| `dungeons_arise:keep_kayra` **(measured)** | 142.0 | 2.63 | 2.14 | 1.22 | 0.71 | 0 | 4.39 | 2.8 |
| `dungeons_arise:shiraz_palace` **(measured)** | 137.0 | 3.44 | 2.52 | 1.2 | 0.72 | 0 | 5.38 | 3.23 |
| `dungeons_arise:kisegi_sanctuary` **(measured)** | 130.0 | 3.63 | 2.61 | 1.2 | 0.72 | 0.41 | 5.65 | 3.44 |
| `dungeons_arise:thornborn_towers` **(measured)** | 124.0 | 3.4 | 2.55 | 1.2 | 0.74 | 0.21 | 5.28 | 3.3 |
| `dungeons_arise:mining_complex` **(measured)** | 116.0 | 3.89 | 0.27 | 0 | 0.0 | 1.25 | 6.11 | 3.76 |
| `dungeons_arise:heavenly_conqueror` **(measured)** | 22.0 | 3.08 | 1.1 | 1.0 | 0.75 | 0.33 | 2.76 | 1.87 |
| `dungeons_arise:heavenly_challenger` | 12 | 1.31 | 0.98 | 0.16 | 0.15 | 0 | 1.56 | 1.12 |
| `dungeons_arise:heavenly_rider` | 9 | 3.0 | 1.0 | 1.0 | 0.75 | 0 | 2.45 | 1.65 |

## Nether Expeditions (`nether`) - 50 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `incendium:sanctum` **(measured)** | 136.0 | 0.32 | 0.97 | 0.05 | 0.05 | 2.08 | 2.16 | 1.65 |
| `incendium:forbidden_castle` **(measured)** | 115.0 | 0.35 | 0.32 | 0.03 | 0.03 | 0.82 | 0.89 | 0.61 |
| `betterfortresses:fortress` **(measured)** | 99.0 | 0 | 0.69 | 0 | 0.0 | 2.5 | 2.01 | 1.39 |
| `minecraft:bastion_remnant` **(measured)** | 31.0 | 0.35 | 0.28 | 0 | 0.0 | 1.33 | 1.12 | 0.77 |
| `mmr:1_21_0/nether_mineshaft` | 132 | 0 | 0.49 | 0.05 | 0.05 | 2.11 | 1.71 | 0.98 |
| `nova_structures:nether_port` | 93 | 0 | 0.7 | 0 | 0.0 | 2.46 | 1.98 | 1.4 |
| `incendium:castle` | 74 | 0 | 0.64 | 0.05 | 0.05 | 1.67 | 1.45 | 1.0 |
| `incendium:quartz_flats` | 44 | 0 | 0.7 | 0 | 0.0 | 2.5 | 1.99 | 1.39 |
| `betterfortresses:halls` | 43 | 0 | 0.23 | 0 | 0.0 | 1.24 | 0.87 | 0.6 |
| `betterfortresses:keep` | 42 | 0 | 0.43 | 0 | 0.0 | 0.9 | 0.9 | 0.61 |
| `incendium:cvill` | 42 | 0 | 0.7 | 0 | 0.0 | 2.49 | 2.01 | 1.41 |
| `repurposed_structures:bastions/underground` | 37 | 0 | 0.71 | 0.05 | 0.05 | 2.52 | 1.99 | 1.41 |
| `nova_structures:nether_skeleton_tower` | 36 | 0 | 0.7 | 0 | 0.0 | 2.51 | 2.0 | 1.39 |
| `dungeons_arise:scorched_mines` | 23 | 0 | 0.7 | 0.05 | 0.05 | 2.51 | 2.01 | 1.4 |
| `repurposed_structures:temples` | 22 | 2.0 | 1.86 | 0 | 0.0 | 4.19 | 4.95 | 3.57 |
| `incendium:reactor` | 18 | 0 | 0.7 | 0.05 | 0.05 | 2.13 | 1.7 | 1.19 |
| `incendium:pipeline` | 17 | 0 | 0.19 | 0.01 | 0.01 | 0.77 | 0.64 | 0.45 |
| `incendium:the_lab` | 16 | 0 | 0.7 | 0.05 | 0.05 | 2.5 | 2.0 | 1.4 |
| `repurposed_structures:ancient_cities/nether` | 14 | 0 | 0.7 | 0 | 0.0 | 2.5 | 2.0 | 1.4 |
| `betterdungeons:small_nether_dungeon` | 13 | 0 | 0 | 0 | 0.0 | 2.5 | 2.0 | 1.4 |
| `repurposed_structures:shipwrecks/nether` | 10 | 0 | 0.7 | 0.05 | 0.05 | 2.5 | 2.0 | 1.4 |
| `repurposed_structures:cities/nether` | 8 | 0 | 0.7 | 0 | 0.0 | 2.5 | 2.0 | 1.4 |
| `repurposed_structures:strongholds/nether` | 8 | 0 | 0 | 0 | 0.0 | 2.5 | 2.0 | 1.4 |
| `structures:pillager_castle` | 8 | 0.06 | 0.1 | 0 | 0.0 | 0.16 | 0.23 | 0.16 |
| `adorabuild_structures:blackstone_bastion_medium_3` | 6 | 0 | 0.17 | 0.01 | 0.01 | 0.42 | 0.37 | 0.26 |
| ... 25 smaller groups | | | | | | | | |

## Ocean Expeditions (`ocean`) - 22 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `dungeons_arise:undead_pirate_ship` **(measured)** | 44.0 | 0.96 | 0.34 | 0 | 0.0 | 1.85 | 1.45 | 1.01 |
| `minecraft:mineshaft` **(measured)** | 5.0 | 0.46 | 0.03 | 0 | 0.0 | 0.14 | 0.31 | 0.2 |
| `nova_structures:conduit_ruin` | 51 | 0.82 | 0.41 | 0 | 0.0 | 1.99 | 1.38 | 1.02 |
| `cataclysm:sunken_city` | 18 | 0.57 | 0.31 | 0 | 0.0 | 1.52 | 1.06 | 0.75 |
| `dungeons_arise:illager_corsair` | 15 | 0.32 | 0.17 | 0 | 0.0 | 0.72 | 0.58 | 0.41 |
| `dungeons_arise:illager_galley` | 11 | 0.8 | 0.4 | 0 | 0.0 | 2.0 | 1.4 | 1.0 |
| `repurposed_structures:monuments/desert` | 8 | 0.8 | 0.4 | 0 | 0.0 | 2.0 | 1.4 | 1.0 |
| `repurposed_structures:monuments/icy` | 8 | 0.8 | 0.4 | 0 | 0.0 | 2.0 | 1.4 | 1.0 |
| `repurposed_structures:monuments/jungle` | 8 | 0.8 | 0.4 | 0 | 0.0 | 2.0 | 1.4 | 1.0 |
| `repurposed_structures:monuments/nether` | 8 | 0.8 | 0.4 | 0 | 0.0 | 2.0 | 1.4 | 1.0 |
| `adorabuild_structures:bamboo_raft_1` | 3 | 0.05 | 0.09 | 0 | 0.0 | 0.28 | 0.25 | 0.17 |
| `dungeons_arise:fishing_hut` | 3 | 0.8 | 0 | 0 | 0.0 | 2.0 | 1.4 | 1.0 |
| `adorabuild_structures:oak_ship_1` | 2 | 0.0 | 0.09 | 0 | 0.0 | 0.23 | 0.22 | 0.15 |
| `adorabuild_structures:ocean_temple_medium_1` | 2 | 0.07 | 0.03 | 0 | 0.0 | 0.17 | 0.12 | 0.08 |
| `dungeons_arise:typhon` | 2 | 0 | 0.4 | 0 | 0.0 | 2.0 | 1.2 | 0.9 |
| `hopo:underwater_city` | 2 | 0 | 0.11 | 0 | 0.0 | 0.28 | 0.25 | 0.18 |
| `adorabuild_structures:cherry_raft_1` | 1 | 0 | 0.09 | 0 | 0.0 | 0.23 | 0.21 | 0.15 |
| `adorabuild_structures:ocean_temple_medium_2` | 1 | 0.03 | 0.02 | 0 | 0.0 | 0.08 | 0.06 | 0.04 |
| `adorabuild_structures:sand_castle_tiny_1` | 1 | 0 | 0.06 | 0 | 0.0 | 0.14 | 0.13 | 0.09 |
| `adorabuild_structures:spruce_ship_1` | 1 | 0 | 0.09 | 0 | 0.0 | 0.23 | 0.21 | 0.15 |
| `betteroceanmonuments:start` | 1 | 0.03 | 0.02 | 0 | 0.0 | 0.08 | 0.06 | 0.04 |
| `dungeons_arise:lighthouse` | 1 | 0.6 | 0.4 | 0 | 0.0 | 1.05 | 0.6 | 0.45 |

## Roadside Ruins & Camps (`roadside`) - 37 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `nova_structures:badlands_miner_outpost` | 120 | 1.17 | 0.6 | 0 | 0.0 | 0 | 1.37 | 0.95 |
| `nova_structures:desert_ruin` | 111 | 0.48 | 0 | 0 | 0.0 | 0 | 0.01 | 0.01 |
| `dungeons_arise:bathhouse` | 91 | 0.73 | 0 | 0 | 0.0 | 0 | 0.36 | 0 |
| `nova_structures:ruin_town` | 80 | 0.72 | 0 | 0 | 0.0 | 0 | 0 | 0 |
| `nova_structures:underground_house` | 70 | 0.7 | 0 | 0 | 0.0 | 0 | 0 | 0 |
| `nova_structures:toxic_lair` | 59 | 0.7 | 0 | 0 | 0.0 | 0 | 0.29 | 0.18 |
| `nova_structures:jungle_ruin` | 44 | 1.09 | 0.39 | 0 | 0.0 | 0 | 1.11 | 0.76 |
| `terralith:regular` | 35 | 0.74 | 0 | 0 | 0.0 | 0 | 0.45 | 0.26 |
| `dungeons_arise:bandit_village` | 28 | 0.71 | 0.03 | 0 | 0.0 | 0 | 0.41 | 0.18 |
| `terralith:spire` | 26 | 0.7 | 0 | 0 | 0.0 | 0 | 0.4 | 0.19 |
| `dungeons_arise:mushroom_village` | 25 | 0.69 | 0.03 | 0 | 0.0 | 0 | 0.4 | 0.19 |
| `nova_structures:tavern` | 24 | 0.11 | 0 | 0 | 0.0 | 0 | 0 | 0 |
| `nova_structures:shrine` | 20 | 0.7 | 0 | 0 | 0.0 | 0 | 0.4 | 0.26 |
| `dungeons_arise:mushroom_house` | 18 | 0.7 | 0.03 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `explorify:supply_cache` | 14 | 0.7 | 0 | 0 | 0.0 | 0 | 0.41 | 0.25 |
| `nova_structures:wild_ruin` | 14 | 0.12 | 0 | 0 | 0.0 | 0 | 0.01 | 0 |
| `repurposed_structures:ruins/land_cold` | 12 | 0.7 | 0 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `repurposed_structures:ruins/land_hot` | 12 | 0.7 | 0 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `repurposed_structures:ruins/land_icy` | 12 | 0.7 | 0 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `repurposed_structures:ruins/land_warm` | 12 | 0.7 | 0 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `dungeons_arise:illager_campsite` | 9 | 0.3 | 0 | 0 | 0.0 | 0 | 0.18 | 0.11 |
| `dungeons_arise:jungle_tree_house` | 9 | 0.7 | 0.03 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `dungeons_arise:merchant_campsite` | 9 | 0.7 | 0.03 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `betterwitchhuts:witch_hut` | 5 | 0.7 | 0.03 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| `dungeons_arise:small_blimp` | 5 | 0.7 | 0.03 | 0 | 0.0 | 0 | 0.4 | 0.25 |
| ... 12 smaller groups | | | | | | | | |

## Settlements (`settlement`) - 156 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `ctov:large/village_plains` **(measured)** | 171.0 | 1.55 | 0.08 | 0 | 0.0 | 0 | 1.9 | 0.71 |
| `structory:harvest` | 190 | 1.92 | 0 | 0 | 0.0 | 0 | 1.88 | 1.12 |
| `kaisyn:village/exclusives` | 131 | 0.8 | 0.09 | 0 | 0.0 | 0.23 | 1.29 | 0.32 |
| `structory:outcast_villager` | 130 | 2.56 | 0 | 0 | 0.0 | 0 | 3.22 | 1.99 |
| `terralith:village` | 87 | 0.83 | 0 | 0 | 0.0 | 0 | 0.89 | 0.43 |
| `dungeons_arise:greenwood_pub` | 60 | 0.78 | 0 | 0 | 0.0 | 0 | 1.02 | 0.48 |
| `ctov:village/mesa_fortified` | 54 | 0.71 | 0.06 | 0 | 0.0 | 0 | 0.89 | 0.42 |
| `ctov:village/taiga_fortified` | 48 | 0.2 | 0 | 0 | 0.0 | 0 | 0.34 | 0.01 |
| `kaisyn:ships/village_ocean` | 44 | 0.57 | 0.3 | 0 | 0.0 | 1.1 | 1.18 | 0.71 |
| `ctov:village/desert_oasis` | 43 | 0.56 | 0.03 | 0 | 0.0 | 0 | 0.78 | 0.36 |
| `ctov:village/swamp_fortified` | 43 | 0.41 | 0 | 0 | 0.0 | 0 | 0.61 | 0.24 |
| `kaisyn:village/beach_lighthouse` | 40 | 0.49 | 0.1 | 0 | 0.0 | 0.41 | 0.76 | 0.44 |
| `ctov:village/plains` | 39 | 0.26 | 0.06 | 0 | 0.0 | 0 | 0.4 | 0.12 |
| `ctov:village/beach` | 38 | 0.49 | 0.03 | 0 | 0.0 | 0 | 0.67 | 0.29 |
| `ctov:village/halloween` | 38 | 0.56 | 0.03 | 0 | 0.0 | 0 | 0.7 | 0.3 |
| `ctov:village/mesa` | 37 | 0.38 | 0.03 | 0 | 0.0 | 0 | 0.51 | 0.21 |
| `ctov:village/taiga` | 36 | 0.28 | 0.03 | 0 | 0.0 | 0 | 0.38 | 0.09 |
| `ctov:village/plains_fortified` | 35 | 0.27 | 0 | 0 | 0.0 | 0 | 0.35 | 0.06 |
| `ctov:village/jungle_tree` | 34 | 0.24 | 0.06 | 0 | 0.0 | 0 | 0.4 | 0.15 |
| `ctov:village/savanna` | 34 | 0.24 | 0.06 | 0 | 0.0 | 0 | 0.36 | 0.12 |
| `ctov:village/jungle` | 33 | 0.43 | 0.06 | 0 | 0.0 | 0 | 0.63 | 0.31 |
| `ctov:village/mountain` | 33 | 0.36 | 0.03 | 0 | 0.0 | 0 | 0.53 | 0.23 |
| `ctov:village/mountain_alpine` | 33 | 0.43 | 0 | 0 | 0.0 | 0 | 0.59 | 0.25 |
| `ctov:village/swamp` | 33 | 0.44 | 0.03 | 0 | 0.0 | 0 | 0.59 | 0.27 |
| `ctov:village/snowy_igloo` | 31 | 0.37 | 0.03 | 0 | 0.0 | 0 | 0.51 | 0.21 |
| ... 131 smaller groups | | | | | | | | |

## Temples, Mansions & Outposts (`temple`) - 94 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `betterdeserttemples:desert_temple` **(measured)** | 69.0 | 1.52 | 0.9 | 0.03 | 0.03 | 0 | 2.43 | 1.67 |
| `dungeons_arise:illager_fort` **(measured)** | 61.0 | 1.39 | 1.02 | 0 | 0.0 | 0.45 | 2.43 | 1.69 |
| `cataclysm:abandoned_village` **(measured)** | 43.0 | 1.45 | 0.98 | 0.03 | 0.03 | 0.39 | 2.4 | 1.68 |
| `minecraft:illager_mansion` | 358 | 1.52 | 0.93 | 0 | 0.0 | 0 | 3.08 | 1.91 |
| `nova_structures:witch_villa` | 155 | 1.55 | 0.9 | 0 | 0.0 | 0 | 2.28 | 1.61 |
| `nova_structures:lone_citadel` | 117 | 1.18 | 0.9 | 0 | 0.0 | 0 | 2.01 | 1.39 |
| `nova_structures:stray_fort` | 101 | 1.19 | 0.9 | 0 | 0.0 | 0 | 1.99 | 1.44 |
| `kaisyn:outpost/forts` | 87 | 0.89 | 0.51 | 0 | 0.0 | 0 | 1.38 | 0.96 |
| `nova_structures:illager_hideout` | 81 | 1.22 | 0.89 | 0 | 0.0 | 0 | 2.03 | 1.42 |
| `kaisyn:outpost/towers` | 80 | 0.97 | 0.89 | 0 | 0.0 | 0 | 1.75 | 1.23 |
| `repurposed_structures:mansions/birch` | 79 | 1.19 | 0.9 | 0 | 0.0 | 0 | 2.0 | 1.43 |
| `repurposed_structures:mansions/desert` | 79 | 1.19 | 0.9 | 0 | 0.0 | 0 | 2.0 | 1.43 |
| `repurposed_structures:mansions/jungle` | 79 | 1.19 | 0.9 | 0 | 0.0 | 0 | 2.0 | 1.43 |
| `repurposed_structures:mansions/mangrove` | 79 | 1.19 | 0.9 | 0 | 0.0 | 0 | 2.0 | 1.43 |
| `repurposed_structures:mansions/oak` | 79 | 1.19 | 0.9 | 0 | 0.0 | 0 | 2.0 | 1.43 |
| `repurposed_structures:mansions/savanna` | 79 | 1.19 | 0.9 | 0 | 0.0 | 0 | 2.0 | 1.43 |
| `repurposed_structures:mansions/taiga` | 79 | 1.19 | 0.9 | 0 | 0.0 | 0 | 2.0 | 1.43 |
| `repurposed_structures:mansions/snowy` | 78 | 1.2 | 0.9 | 0 | 0.0 | 0 | 1.99 | 1.43 |
| `structory:ruin` | 60 | 1.89 | 0.9 | 0 | 0.0 | 0 | 2.4 | 1.65 |
| `dungeons_arise:mushroom_mines` | 44 | 0 | 0.88 | 0 | 0.0 | 0 | 1.98 | 1.41 |
| `kaisyn:outpost/camps` | 44 | 0.61 | 0.25 | 0 | 0.0 | 0 | 0.87 | 0.61 |
| `kaisyn:ships/pillager_outpost_ocean` | 42 | 0.43 | 0.34 | 0 | 0.0 | 0.47 | 1.06 | 0.67 |
| `dungeons_arise:aviary` | 37 | 1.18 | 0.9 | 0.03 | 0.03 | 0 | 2.01 | 1.4 |
| `repurposed_structures:pyramids` | 32 | 1.2 | 1.9 | 0 | 0.0 | 3.0 | 4.39 | 3.2 |
| `betterdeserttemples:hall_room` | 30 | 0.95 | 0.83 | 0.03 | 0.03 | 0 | 1.75 | 1.23 |
| ... 69 smaller groups | | | | | | | | |

## Underground Dungeons (`underground`) - 54 structure groups

| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |
|---|---|---|---|---|---|---|---|---|
| `irons_spellbooks:citadel` **(measured)** | 136.0 | 2.06 | 0.7 | 0 | 0.0 | 1.17 | 2.89 | 2.2 |
| `minecraft:ancient_city` **(measured)** | 103.0 | 0.8 | 1.29 | 0.01 | 0.01 | 3.22 | 3.67 | 2.5 |
| `minecraft:mansion` **(measured)** | 28.0 | 1.43 | 0.9 | 0 | 0.0 | 0.04 | 2.26 | 1.56 |
| `minecraft:stronghold` **(measured)** | 20.0 | 0.32 | 0.04 | 0 | 0.0 | 0.08 | 0.34 | 0.22 |
| `minecraft:village_plains` **(measured)** | 17.0 | 0.2 | 0.08 | 0 | 0.0 | 0.08 | 0.25 | 0.17 |
| `mmr:1_21_0/desert_mineshaft` | 275 | 0.83 | 0.17 | 0 | 0.0 | 0 | 1.2 | 0.74 |
| `mmr:1_21_0/mineshaft` | 210 | 1.48 | 0.25 | 0 | 0.0 | 0 | 1.05 | 0.68 |
| `mmr:1_21_0/jungle_mineshaft` | 171 | 1.36 | 0.17 | 0 | 0.0 | 0 | 1.17 | 0.76 |
| `mmr:1_21_0/dark_oak_mineshaft` | 167 | 1.35 | 0.18 | 0 | 0.0 | 0 | 1.19 | 0.74 |
| `nova_structures:creeping_crypt` | 153 | 1.38 | 0 | 0 | 0.0 | 0 | 1.38 | 0.92 |
| `nova_structures:undead_crypt` | 145 | 1.45 | 0 | 0 | 0.0 | 0 | 1.16 | 0.72 |
| `nova_structures:remnant` | 130 | 1.3 | 0 | 0 | 0.0 | 0 | 0.59 | 0.35 |
| `mmr:1_21_0/mushroom_mineshaft` | 116 | 1.4 | 0.17 | 0 | 0.0 | 0 | 1.18 | 0.78 |
| `minecraft:illager_mansion/manor_fixed` | 112 | 1.17 | 0.14 | 0 | 0.0 | 0 | 1.04 | 0.66 |
| `mmr:1_21_0/mesa_mineshaft` | 112 | 1.36 | 0.17 | 0 | 0.0 | 0 | 1.21 | 0.77 |
| `mmr:1_21_0/snowy_mineshaft` | 102 | 1.41 | 0.18 | 0 | 0.0 | 0 | 1.39 | 0.74 |
| `nova_structures:bunker` | 87 | 1.53 | 0.25 | 0 | 0.0 | 0 | 1.07 | 0.74 |
| `mmr:1_21_0/deep_dark_mineshaft` | 71 | 1.39 | 0.18 | 0 | 0.0 | 0 | 1.43 | 0.88 |
| `betterstrongholds:rooms` | 66 | 1.39 | 0.24 | 0 | 0.0 | 0 | 1.4 | 0.9 |
| `betterdungeons:small_dungeon` | 53 | 0.56 | 0 | 0 | 0.0 | 0 | 0.71 | 0.44 |
| `betterstrongholds:treasure` | 33 | 0.09 | 0.25 | 0 | 0.0 | 0 | 1.1 | 0.71 |
| `terralith:underground` | 26 | 0.35 | 0.02 | 0 | 0.0 | 0 | 0.42 | 0.26 |
| `betterdungeons:skeleton_dungeon` | 17 | 1.4 | 0.25 | 0 | 0.0 | 0 | 1.4 | 0.9 |
| `structures:dungeon` | 12 | 0.12 | 0 | 0 | 0.0 | 0 | 0.16 | 0.1 |
| `mvs:1_21_0` | 8 | 0.67 | 0.22 | 0 | 0.0 | 0.47 | 0.89 | 0.58 |
| ... 29 smaller groups | | | | | | | | |

