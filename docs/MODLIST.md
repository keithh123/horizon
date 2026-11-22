# Mod list - Project Horizon 0.3.0

Minecraft 1.21.1 - NeoForge 21.1.267 - 176 mods - generated 2026-11-21 from `manifests/lock.json`.

Channel `beta`/`alpha` is the upstream author's label. Side = Modrinth client/server metadata (the pack installs everything on the client because singleplayer runs an integrated server).

## Renderer (8)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Forgified Fabric API](https://modrinth.com/project/Aqlf1Shp) | `0.116.15+2.3.6+1.21.1` | release | req/req | Apache-2.0 | Fabric API surface required by Roxy/Voxy. |
| [Iris Shaders](https://modrinth.com/project/YL57xq9U) | `1.8.14-beta.1+1.21.1-neoforge` | release | req/uns | LGPL-3.0-only | Shader loader; Voxy-aware shader integration. |
| [Reese's Sodium Options](https://modrinth.com/project/Bh37bMuy) | `mc1.21.1-2.2.6+neoforge` | release | req/uns | MIT | Usable video settings UI for Sodium's expanded option set. |
| [Roxy](https://modrinth.com/project/Ap78bKTp) | `0.4.2.1-neoforge+mc1.21.1` | beta | req/uns | MIT | Translation layer that runs the original Voxy jar on NeoForge 1.21.1. |
| [Sodium](https://modrinth.com/project/AANobbMI) | `mc1.21.1-0.8.13-neoforge` | release | req/uns | LicenseRef-Polyform-Shield-1.0.0 | Renderer foundation required by Roxy/Voxy and Iris. |
| [Sodium Extra](https://modrinth.com/project/PtjYWJkn) | `mc1.21.1-0.9.5+neoforge` | release | req/uns | LGPL-3.0-only | Extra Sodium toggles used by the Performance profile (particles, animations, fog). |
| [voxy](https://modrinth.com/project/fxxUqruK) | `0.2.16-beta` | beta | req/uns | LicenseRef-All-Rights-Reserved | Long-distance LOD renderer. Roxy's only verified jar: voxy-0.2.16-beta for MC 1.21.11 (loaded through Roxy, not natively). |
| [Voxygen](https://modrinth.com/project/xT0lnNE9) | `2.4.2` | beta | req/req | LicenseRef-iSeeEthan-Custom-License | Generates real chunks in the background and feeds them to Voxy, so distant LODs match the modded terrain exactly (no seed approximation). Roxy ships compat for this v2 line. |

## Performance (6)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Entity Culling](https://modrinth.com/project/NNAgCjsB) | `1.12.1` | release | req/uns | LicenseRef-tr7zw-Protective-License | Skips rendering hidden entities/block entities - important with large factories. |
| [FerriteCore](https://modrinth.com/project/uXXizFIs) | `7.0.3-neoforge` | release | opt/opt | MIT | Blockstate/model memory deduplication. |
| [ImmediatelyFast](https://modrinth.com/project/5ZwdcRci) | `1.6.15+1.21.1-neoforge` | release | req/uns | LGPL-3.0-or-later | Batches immediate-mode rendering (HUD, text, maps). |
| [Lithium](https://modrinth.com/project/gvQqBUqZ) | `mc1.21.1-0.15.4-neoforge` | release | opt/opt | LGPL-3.0-only | Server-tick optimisations (AI, collisions, chunk ticking). NeoForge build. |
| [ModernFix](https://modrinth.com/project/nmDcB62a) | `5.27.27+mc1.21.1` | release | opt/opt | LGPL-3.0-only | Load time and memory reduction; biggest single win for large packs. |
| [spark](https://modrinth.com/project/l6YH9Als) | `1.10.124-neoforge` | release | opt/opt | GPL-3.0-only | Profiler for tick/frame/memory analysis. |

## Worldgen (4)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Incendium Legacy](https://modrinth.com/project/ZVzW5oNS) | `5.4.4` | alpha | opt/req | LicenseRef-Stardust-Labs-License | Nether biome + structure overhaul (Stardust Labs). Only 1.21.1 build is tagged alpha upstream; smoke-tested. |
| [Nullscape](https://modrinth.com/project/LPjGiSO4) | `1.2.14` | release | opt/req | LicenseRef-Stardust-Labs-License | End terrain overhaul (Stardust Labs) - gives the End exploration value. |
| [Tectonic](https://modrinth.com/project/lWDHr9jE) | `3.0.28-neoforge-21.1` | release | opt/req | MIT | Terrain shaping: huge mountain ranges, deep valleys, rivers; officially Terralith-compatible. |
| [Terralith](https://modrinth.com/project/8oi3bsk5) | `2.6.2` | release | opt/req | LicenseRef-Stardust-Labs-License | Biome foundation: ~95 vanilla-block biomes, cave biomes, works with vanilla tooling and Voxy's server-side LOD build. |

## Structures (18)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [ChoiceTheorem's Overhauled Village](https://modrinth.com/project/fgmhI8kH) | `3.6.4` | release | uns/req | CC-BY-NC-ND-4.0 | Biome-specific village overhaul. |
| [Dungeons and Taverns](https://modrinth.com/project/tpehi7ww) | `v4.4.4+mod` | release | opt/req | LicenseRef-All-Rights-Reserved | Uncommon tier: taverns, illager hideouts, ancient ruins. |
| [Explorify](https://modrinth.com/project/HSfsxuTo) | `v1.6.6` | release | opt/req | LicenseRef-All-Rights-Reserved | Common/uncommon tier: small vanilla-styled ruins, camps and shrines. |
| [Repurposed Structures - Neoforge/Forge](https://modrinth.com/project/QDNS5oAT) | `7.5.22+1.21.1-neoforge` | release | uns/req | LGPL-3.0-only | Biome-matched variants of vanilla structures; very configurable rarity. |
| [Structory](https://modrinth.com/project/aKCwCJlY) | `1.3.17` | release | opt/req | LicenseRef-Stardust-Labs-License | Common tier: atmospheric ruins and minor discoveries. |
| [Towns and Towers](https://modrinth.com/project/DjLobEOy) | `1.13.11` | release | opt/req | CC-BY-NC-SA-4.0 | Settlements and pillager outposts with regional variety. |
| [When Dungeons Arise](https://modrinth.com/project/8DfbfASn) | `2.1.68` | release | uns/req | LicenseRef-All-Rights-Reserved | Rare/legendary tier: huge hand-built dungeons and landmarks. |
| [YUNG's Better Desert Temples](https://modrinth.com/project/XNlO7sBv) | `1.21.1-NeoForge-4.1.5` | release | uns/req | LGPL-3.0-only | Vanilla structure overhaul. |
| [YUNG's Better Dungeons](https://modrinth.com/project/o1C1Dkj5) | `1.21.1-NeoForge-5.1.4` | release | uns/req | LGPL-3.0-only | Tier: common/uncommon underground discoveries. |
| [YUNG's Better End Island](https://modrinth.com/project/2BwBOmBQ) | `1.21.1-NeoForge-3.1.2` | release | uns/req | LGPL-3.0-only | Better dragon fight arena. |
| [YUNG's Better Jungle Temples](https://modrinth.com/project/z9Ve58Ih) | `1.21.1-NeoForge-3.1.2` | release | uns/req | LGPL-3.0-only | Vanilla structure overhaul. |
| [YUNG's Better Mineshafts](https://modrinth.com/project/HjmxVlSr) | `1.21.1-NeoForge-5.1.1` | release | uns/req | LGPL-3.0-only | Vanilla structure overhaul. |
| [YUNG's Better Nether Fortresses](https://modrinth.com/project/Z2mXHnxP) | `1.21.1-NeoForge-3.1.5` | release | uns/req | LGPL-3.0-only | Vanilla structure overhaul. |
| [YUNG's Better Ocean Monuments](https://modrinth.com/project/3dT9sgt4) | `1.21.1-NeoForge-4.1.2` | release | uns/req | LGPL-3.0-only | Vanilla structure overhaul. |
| [YUNG's Better Strongholds](https://modrinth.com/project/kidLKymU) | `1.21.1-NeoForge-5.1.3` | release | uns/req | LGPL-3.0-only | Vanilla structure overhaul. |
| [YUNG's Better Witch Huts](https://modrinth.com/project/t5FRdP87) | `1.21.1-NeoForge-4.1.1` | release | uns/req | LGPL-3.0-only | Vanilla structure overhaul. |
| [YUNG's Bridges](https://modrinth.com/project/Ht4BfYp6) | `1.21.1-NeoForge-5.1.1` | release | uns/req | LGPL-3.0-only | Natural river crossings - travel flavour. |
| [YUNG's Extras](https://modrinth.com/project/ZYgyPyfq) | `1.21.1-NeoForge-5.1.1` | release | uns/req | LGPL-3.0-only | Small common discoveries. |

## Dimensions (4)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Deeper and Darker](https://modrinth.com/project/fnAffV0n) | `1.4.1-neoforge-1.21.1` | release | req/req | AGPL-3.0-only | Otherside dimension beyond Ancient Cities; Warden-tier progression. |
| [The Aether](https://modrinth.com/project/YhmgMVyu) | `1.21.1-1.5.10-neoforge` | release | req/req | LicenseRef-Custom | Sky dimension with three dungeon bosses and its own gear line. |
| [The Bumblezone - NeoForge/Forge](https://modrinth.com/project/38tpSycf) | `7.19.3+1.21.1-neoforge` | release | req/req | LicenseRef-All-Rights-Reserved | Unique bee dimension with its own challenge/quest-like progression. |
| [The Undergarden](https://modrinth.com/project/Ejfl5qDL) | `0.9.6` | beta | req/req | LicenseRef-All-Rights-Reserved | Underground dimension with a boss and its own material tier. |

## Rpg (13)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Apotheosis](https://modrinth.com/project/rqFWfVlz) | `1.21.1-8.9.0` | release | req/req | MIT | Core loot system: affixes, rarities, gems, sockets, world tiers, bosses. |
| [Apothic Attributes](https://modrinth.com/project/DGaH8Rh0) | `1.21.1-2.11.0` | release | req/req | MIT | Attribute framework used by Apotheosis (crit, armor pierce, etc.). |
| [Apothic-Enchanting](https://modrinth.com/project/pL8MtgqY) | `1.21.1-1.6.4` | release | req/req | MIT | Enchanting overhaul; gives enchanting long-term depth. |
| [Apothic-Spawners](https://modrinth.com/project/DfxVkOAO) | `1.21.1-1.4.0` | release | req/req | MIT | Spawner modification - controlled mob-farm progression. |
| [Artifacts](https://modrinth.com/project/P0Mu4wcQ) | `13.2.5` | release | req/req | MIT | Exploration-found accessories (common/uncommon loot). |
| [Better Combat](https://modrinth.com/project/5sy6g3kz) | `2.4.0+1.21.1-neoforge` | release | req/req | LicenseRef-All-Rights-Reserved | Directional, combo-based melee. |
| [Curios API](https://modrinth.com/project/vvuO3ImH) | `9.6.0+1.21.1` | release | req/req | LGPL-3.0-or-later | Accessory slot framework. |
| [Gateways to Eternity](https://modrinth.com/project/8OIeAukW) | `1.21.1-5.1.0` | release | req/req | MIT | Bounded, readable wave challenges (fixed waves, fixed entity counts, visible timer). Activates the gateway data Apotheosis already ships and hosts Horizon's late-game Trials, which consume exploration relics instead of producing them. |
| [L_Ender's Cataclysm](https://modrinth.com/project/46KJle7n) | `3.33` | release | req/req | CC-BY-NC-ND-4.0 | Late-game structure bosses with progression-defining drops. |
| [Mowzie's Mobs](https://modrinth.com/project/BFbX9xcm) | `1.8.2` | release | req/req | LicenseRef-Mowzies-Mobs-License | Mid-game overworld mini-bosses that make exploring dangerous. |
| [Relics](https://modrinth.com/project/OCJRPujW) | `0.10.7.8` | release | req/req | LicenseRef-All-Rights-Reserved | Levelling relics found in structures (rare/legendary loot). |
| [ShatterLib | OctoLib](https://modrinth.com/project/RH2KUdKJ) | `0.6.3.2+1.21` | release | req/req | LicenseRef-All-Rights-Reserved | Provides mod id 'octolib' required by Relics 0.10.x (undeclared in Modrinth metadata; found by launch test). |
| [Simply Swords](https://modrinth.com/project/bK3Ubu9p) | `1.70.2-1.21.1` | release | req/req | LicenseRef-Custom | Weapon variety with unique uniques; Better Combat movesets built in. |

## Magic (4)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Ars Nouveau](https://modrinth.com/project/TKB6INcv) | `5.13.5` | release | req/req | LicenseRef-All-Rights-Reserved | Utility/automation magic: glyph spells, mana, rituals, item transport. |
| [Iron's Lib](https://modrinth.com/project/9nfaJPtX) | `1.21.1-2.4.0` | release | req/req | LicenseRef-All-Rights-Reserved | Iron's Spells requires irons_lib >=1.21.1-2 <1.21.1-3 (undeclared in Modrinth metadata; found by launch test). |
| [Iron's Spells 'n Spellbooks](https://modrinth.com/project/s4OWxYQQ) | `1.21.1-3.16.4` | release | req/req | LicenseRef-All-Rights-Reserved | Combat magic: schools, spellbooks, scroll loot, boss encounters. |
| [Occultism](https://modrinth.com/project/sbJh4AZw) | `1.21.1-neoforge-1.227.0` | release | req/req | MIT | Spirit-based automation and storage; ritual crafting. |

## Technology (12)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Applied Energistics 2](https://modrinth.com/project/XxWD5pD3) | `19.2.20` | release | req/req | LicenseRef-Multiple | Digital storage and autocrafting across all tech mods. |
| [Applied Energistics 2 Wireless Terminals](https://modrinth.com/project/pNabrMMw) | `19.5.1` | release | req/req | MIT | Wireless crafting/pattern terminals (ae2wtlib). |
| [Applied Mekanistics](https://modrinth.com/project/IiATswDj) | `1.6.3` | release | req/req | LGPL-3.0-only | Official AE2 storage/autocrafting of Mekanism chemicals. |
| [CC: Tweaked](https://modrinth.com/project/gu7yAYhd) | `1.122.0` | beta | req/req | LicenseRef-CCPL | Programmable computers/turtles; CC tags its stable line as beta. |
| [Create](https://modrinth.com/project/LNytGWDc) | `6.0.10+mc1.21.1` | release | opt/req | LicenseRef-Create-Mod-License | Mechanical engineering - early/mid technology backbone. |
| [Create Crafts & Additions](https://modrinth.com/project/kU1G12Nn) | `neoforge-1.21.1-1.7.2` | release | req/req | MIT | Bridges Create rotational power and FE electricity. |
| [Create: Enchantment Industry](https://modrinth.com/project/JWGBpFUP) | `2.4.2` | release | req/req | LGPL-3.0-or-later | Liquid XP + automated enchanting; ties Create to Apotheosis enchanting. |
| [MEGA Cells](https://modrinth.com/project/jjuIRIVr) | `4.11.0` | release | req/req | LGPL-3.0-only | MEGA Cells: late-game AE2 storage tiers. |
| [Mekanism](https://modrinth.com/project/Ce6I4WUE) | `10.7.19.85` | release | req/req | MIT | Ore multiplication, chemistry, jetpacks/MekaSuit - the mid-game processing pillar. |
| [Mekanism Generators](https://modrinth.com/project/OFVYKsAk) | `10.7.19.85` | release | req/req | MIT | Mekanism power line up to fission/fusion. |
| [Modern Industrialization](https://modrinth.com/project/Gov5Dboq) | `2.5.13` | release | req/req | MIT | Deep multiblock industrial progression (steam -> electric -> fusion). |
| [Powah!](https://modrinth.com/project/KZO4S4DO) | `6.2.10-neoforge` | release | req/req | LGPL-3.0-only | Mid-game FE generation tiers, simple to learn. |

## Qol (17)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [AppleSkin](https://modrinth.com/project/EsAfCjCV) | `3.0.9+mc1.21` | release | opt/opt | Unlicense | Food/saturation readout. |
| [Controlling](https://modrinth.com/project/xv94TkTM) | `19.0.5` | release | req/uns | MIT | Searchable keybinds and conflict view. |
| [Corpse](https://modrinth.com/project/WrpuIfhw) | `neoforge-1.21.1-1.1.22` | release | req/req | LicenseRef-All-Rights-Reserved | Death recovery: items stay in a corpse at the death spot (also for void deaths) instead of despawning, so dying costs a trip back, not the whole kit. |
| [EMI](https://modrinth.com/project/fRiHVvU7) | `1.1.24+1.21.1+neoforge` | release | req/opt | MIT | Primary recipe viewer with recipe trees. |
| [Farmer's Delight](https://modrinth.com/project/R2OftAxM) | `1.21.1-1.3.4` | release | req/req | MIT | Food variety that makes survival more than bread. |
| [Jade 🔍](https://modrinth.com/project/nvQzSEkH) | `15.10.6+neoforge` | release | opt/opt | CC-BY-NC-SA-4.0 | Block/entity tooltips. |
| [Just Enough Items (JEI)](https://modrinth.com/project/u6dRKJwZ) | `19.64.0.455` | release | opt/opt | MIT | Loads JEI-only plugins (Create, etc.); EMI hides JEI's UI. |
| [KubeJS](https://modrinth.com/project/umyGl7zF) | `2101.7.2-build.381` | release | opt/opt | LGPL-3.0-only | Recipe/loot/progression scripting. |
| [Lootr](https://modrinth.com/project/EltpO5cN) | `1.21.1-1.11.38.127` | release | req/req | MIT | Per-player structure loot: each player opens their own copy of every structure container, so the expedition reward budget (docs/LOOT.md) holds per player in multiplayer instead of first-come-first-served. |
| [Mouse Tweaks](https://modrinth.com/project/aC3cM3Vq) | `1.21-2.26.1-neoforge` | release | req/uns | BSD-3-Clause | Inventory drag/scroll handling. |
| [Odyssey Quests](https://modrinth.com/project/lo90fZoB) | `2.0.3` | beta | req/req | MIT | Quest book (Heracles). FTB Quests is CurseForge-only and cannot be in an .mrpack. |
| [Polymorph](https://modrinth.com/project/tagwiZkJ) | `1.1.0+1.21.1` | release | req/req | LGPL-3.0-or-later | Resolves recipe output conflicts between mods. |
| [Sophisticated Backpacks](https://modrinth.com/project/TyCTlI4b) | `1.21.1-3.26.22.2257` | release | req/req | LicenseRef-All-Rights-Reserved | Upgradeable backpacks. |
| [Sophisticated Storage](https://modrinth.com/project/hMlaZH8f) | `1.21.1-1.6.20.2239` | release | req/req | LicenseRef-All-Rights-Reserved | Upgradeable chests/barrels with sorting. |
| [Waystones](https://modrinth.com/project/LOpKHB2A) | `21.1.47+neoforge-1.21.1` | release | req/req | LicenseRef-All-Rights-Reserved | Discoverable fast travel - must be found in villages/structures. |
| [Xaero's Minimap](https://modrinth.com/project/1bokaNcj) | `neoforge-1.21.1-26.6.0` | release | req/opt | LicenseRef-All-Rights-Reserved | Minimap. |
| [Xaero's World Map](https://modrinth.com/project/NcUtCpym) | `neoforge-1.21.1-1.47.0` | release | req/opt | LicenseRef-All-Rights-Reserved | World map. |

## Atmosphere (3)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [AmbientSounds](https://modrinth.com/project/fM515JnW) | `6.3.11` | release | req/uns | LGPL-3.0-only | Biome/time-aware ambient soundscapes. |
| [Particle Rain](https://modrinth.com/project/nrikgvxm) | `v4.0.4+1.21.1-neoforge` | release | req/uns | MIT | Better weather particles. |
| [Subtle Effects](https://modrinth.com/project/4q8UOK1d) | `1.15.3` | release | req/opt | LicenseRef-All-Rights-Reserved | Configurable ambient polish (fireflies, sparks, steam, dust, biome particles). Weather particles stay with Particle Rain; overlapping options are disabled in config. |

## Dependency (38)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Architectury API](https://modrinth.com/project/lhGA9TYQ) | `13.0.12+neoforge` | release | req/req | LGPL-3.0-only | Required by effectual, shatterbyte-lib, simply-swords, simply-tooltips, tlib |
| [Balm](https://modrinth.com/project/MBAkmtvl) | `21.0.67+neoforge-1.21.1` | release | opt/opt | LicenseRef-All-Rights-Reserved | Required by waystones |
| [Better Advanced Tooltips](https://modrinth.com/project/iHLDc0eo) | `2101.1.0-build.5` | release | req/req | MIT | Required by kubejs |
| [Better ModList](https://modrinth.com/project/sbpqhzIG) | `21.1.5` | release | req/uns | MIT | Required by voxy-worldgen |
| [CERBON's API](https://modrinth.com/project/GkIc6rRo) | `1.3.0` | release | req/req | LGPL-3.0-only | Required by bosses-of-mass-destruction-forge, cerbons-api |
| [Cloth Config API](https://modrinth.com/project/9s6osm5g) | `15.0.140+neoforge` | release | opt/opt | LGPL-3.0-only | Required by better-combat, bosses-of-mass-destruction-forge, cristel-lib, effectual, powah, spider-overhaul, voxy-worldgen |
| [Create: Dragons Plus](https://modrinth.com/project/dzb1a5WV) | `1.11.9` | release | req/req | LGPL-3.0-or-later | Required by create-enchantment-industry |
| [CreativeCore](https://modrinth.com/project/OsZiaDHq) | `2.13.55` | release | req/opt | LGPL-3.0-only | Required by ambientsounds |
| [Cristel Lib](https://modrinth.com/project/cl223EMc) | `neoforge-1.21.1-3.1.7` | release | opt/req | CC-BY-NC-ND-4.0 | Required by towns-and-towers |
| [Fzzy Config](https://modrinth.com/project/hYykXjDp) | `0.7.7+fix1+1.21+neoforge` | release | req/req | LicenseRef-TDL-M | Required by simply-swords, simply-tooltips, subtle-effects |
| [Geckolib](https://modrinth.com/project/8BmcQJ2H) | `4.9.3` | release | req/opt | MIT | Required by bosses-of-mass-destruction-forge, bossesrise, companions-mod, fantasy_armor, mowzies-mobs, occultism |
| [GuideME](https://modrinth.com/project/Ck4E7v7R) | `21.1.22` | release | req/req | LicenseRef-Multiple-OSS-Licenses | Required by ae2, modern-industrialization, powah |
| [Iceberg](https://modrinth.com/project/5faXoLqX) | `1.3.2` | release | req/req | CC-BY-NC-ND-4.0 | Required by advancement-plaques, legendary-tooltips |
| [Knight Lib](https://modrinth.com/project/hAnl9nbm) | `2.0.5` | release | req/req | GPL-3.0-only | Required by companions-mod |
| [Kotlin for Forge](https://modrinth.com/project/ordsPcFz) | `5.13.0` | release | opt/opt | LGPL-2.1-only | Required by fzzy-config, respawn-recap |
| [Lionfish-API](https://modrinth.com/project/FoVacERa) | `3.1` | release | req/req | LGPL-3.0-only | Required by l_enders-cataclysm |
| [Lithostitched](https://modrinth.com/project/XaDC71GB) | `1.8.1-neoforge-21.1` | release | uns/req | MIT | Required by ct-overhaul-village, tectonic, terralith |
| [MezzConfig](https://modrinth.com/project/7tEfOcA7) | `0.7.1` | beta | opt/opt | MIT | Required by jei |
| [MidnightLib](https://modrinth.com/project/codAaoxh) | `1.10.0+1.21.1-neoforge` | release | opt/opt | MIT | Required by visual-overhaul |
| [Modonomicon](https://modrinth.com/project/692GClaE) | `1.21.1-1.123.1` | release | req/req | MIT AND CC-BY-4.0 | Required by occultism |
| [Moog's Structure Lib (moogs_structures)](https://modrinth.com/project/1oUDhxuy) | `3.4.2-neoforge-1.21.1` | release | uns/req | LGPL-3.0-only | Required by mmr-moogs-mineshafts-reimagined |
| [MossyLib](https://modrinth.com/project/ffLDUGbm) | `2.0.0+1.21.1+neoforge` | release | req/uns | CC-BY-ND-4.0 | Required by inventory-particles |
| [MRU](https://modrinth.com/project/SNVQ2c0g) | `1.0.41+1.21.1-neoforge` | release | opt/opt | LicenseRef-All-Rights-Reserved | Required by sound |
| [oωo (owo-lib)](https://modrinth.com/project/ccKDOlHs) | `0.12.15.6-beta.1+1.21` | beta | req/req | MIT | Required by aether |
| [Patchouli](https://modrinth.com/project/nU0bVIaL) | `1.21.1-93-neoforge` | release | req/req | CC-BY-NC-SA-3.0 | Required by apotheosis |
| [Placebo](https://modrinth.com/project/tCkE8p2N) | `1.21.1-9.9.4` | release | opt/opt | MIT | Required by apotheosis, apothic-attributes, apothic-enchanting, apothic-spawners, gateways-to-eternity |
| [playerAnimator](https://modrinth.com/project/gedNE4y2) | `2.0.4+1.21.1-forge` | beta | req/req | MIT | Required by better-combat |
| [Prism](https://modrinth.com/project/1OE8wbN0) | `1.0.11` | release | req/uns | CC-BY-NC-ND-4.0 | Required by legendary-tooltips |
| [Resourceful Lib](https://modrinth.com/project/G1hIVOrD) | `3.0.12` | release | req/req | MIT | Required by odyssey-quests, the-bumblezone |
| [Rhino](https://modrinth.com/project/sk9knFPE) | `2101.2.7-build.85+Rhino-1.21` | release | opt/opt | MPL-2.0 | Required by kubejs |
| [Searchables](https://modrinth.com/project/fuuu3xnx) | `1.0.2` | release | req/uns | MIT | Required by controlling |
| [Simply Tooltips](https://modrinth.com/project/6avVoBVB) | `0.1.5` | release | req/uns | LicenseRef-Timefall-Development-License-1.2 | Required by simply-swords |
| [SmartBrainLib](https://modrinth.com/project/PuyPazRT) | `1.16.11` | release | uns/req | MPL-2.0 | Required by occultism |
| [Sophisticated Core](https://modrinth.com/project/nmoqTijg) | `1.21.1-1.5.39.2489` | release | req/req | LicenseRef-All-Rights-Reserved | Required by sophisticated-backpacks, sophisticated-storage |
| [SWAY API](https://modrinth.com/project/Gj6Yce3v) | `2.4.5-neoforge+1.21.1` | release | req/uns | CC-BY-NC-SA-4.0 | Required by mc2-interactive-foliage |
| [TLib](https://modrinth.com/project/sBn7rVvc) | `1.5.0-1.21.1` | release | opt/opt | MIT | Required by effectual |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/project/1eAoo2KR) | `3.8.2+1.21.1-neoforge` | release | opt/opt | LGPL-3.0-or-later | Required by better-clouds, particle-interactions, seamless-sleep, sound, spatial-gui, windy |
| [YUNG's API](https://modrinth.com/project/Ua7DFN59) | `1.21.1-NeoForge-5.1.9` | release | req/req | LGPL-3.0-only | Required by yungs-better-desert-temples, yungs-better-dungeons, yungs-better-end-island, yungs-better-jungle-temples, yungs-better-mineshafts, yungs-better-nether-fortresses, yungs-better-ocean-monuments, yungs-better-strongholds, yungs-better-witch-huts, yungs-bridges, yungs-extras |

## Shaders

| Shader | Version | Why |
|---|---|---|
| complementary-reimagined | `r5.9.3` | Default shader. Voxy support since r5.8.1. r5.9.3 chosen over r5.10 (3 days old). |
| complementary-unbound | `r5.9.3` | Cinematic profile alternative. |

## Considered and rejected

| Candidate | Reason |
|---|---|
| the-twilight-forest | CurseForge-only; not distributable through Modrinth .mrpack. Documented as optional manual add-on. |
| ftb-quests | CurseForge-only. Replaced by Odyssey Quests. |
| alexs-caves | No 1.21.1 build (1.20.1 only). |
| biomes-o-plenty / regions-unexplored / oh-the-biomes-weve-gone | Would stack a second biome-placement system on top of Terralith; one foundation chosen. |
| distanthorizons | Mutually exclusive with Voxy. |
| c2me-neoforge | Alpha; worldgen threading risk with heavy worldgen datapacks. |
| noisium | Last 1.21.1 build Aug 2024; overlaps with Lithostitched/Tectonic noise handling. |
| enderio | 1.21.1 line is beta-only; MI + Powah + Create Additions cover its role. |
| industrial-foregoing | Requires Titanium beta; overlaps MI. Excluded for stability. |
| advancedperipherals | Alpha on 1.21.1. |
| idas | Modrinth metadata for 1.13.7+1.21.1-neoforge requires Quark, Supplementaries, Create and Integrated API: two large content mods to get one structure pack, on top of 18 structure mods. |
| simplymore | Only an alpha build (1.3.0_alpha5) for NeoForge 1.21.1; would dilute the Simply Swords/Apotheosis weapon pool. |
| particular-reforged | Overlaps Subtle Effects (ambient particles). One ambient-particle mod is enough; Subtle Effects has finer per-effect config. |
| loot-beams-refork | Apotheosis already draws rarity beams/particles for affix items; a second beam renderer duplicates them. Horizon finds use server-side pickup feedback instead. |
| explorers-compass / natures-compass | Point-to-anything compasses remove discovery. Clues come from exploration maps in loot and quest guidance instead. |
| yungs-cave-biomes | Adds cave biomes = a second biome source under Terralith's cave biomes. |
