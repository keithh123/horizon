# Mod list - Project Horizon 0.6.1

Minecraft 1.21.1 - NeoForge 21.1.267 - 253 mods - generated 2026-11-26 from `manifests/lock.json`.

Channel `beta`/`alpha` is the upstream author's label. Side = Modrinth client/server metadata (the pack installs everything on the client because singleplayer runs an integrated server).

## Renderer (9)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Continuity](https://modrinth.com/project/1IjD5062) | `3.0.0+1.21.neoforge` | release | req/uns | LGPL-3.0-only | Connected textures for resource packs. |
| [Forgified Fabric API](https://modrinth.com/project/Aqlf1Shp) | `0.116.15+2.3.6+1.21.1` | release | req/req | Apache-2.0 | Fabric API surface required by Roxy/Voxy. |
| [Iris Shaders](https://modrinth.com/project/YL57xq9U) | `1.8.14-beta.1+1.21.1-neoforge` | release | req/uns | LGPL-3.0-only | Shader loader; Voxy-aware shader integration. |
| [Reese's Sodium Options](https://modrinth.com/project/Bh37bMuy) | `mc1.21.1-2.2.6+neoforge` | release | req/uns | MIT | Usable video settings UI for Sodium's expanded option set. |
| [Roxy](https://modrinth.com/project/Ap78bKTp) | `0.4.2.1-neoforge+mc1.21.1` | beta | req/uns | MIT | Translation layer that runs the original Voxy jar on NeoForge 1.21.1. |
| [Sodium](https://modrinth.com/project/AANobbMI) | `mc1.21.1-0.8.13-neoforge` | release | req/uns | LicenseRef-Polyform-Shield-1.0.0 | Renderer foundation required by Roxy/Voxy and Iris. |
| [Sodium Extra](https://modrinth.com/project/PtjYWJkn) | `mc1.21.1-0.9.5+neoforge` | release | req/uns | LGPL-3.0-only | Extra Sodium toggles used by the Performance profile (particles, animations, fog). |
| [voxy](https://modrinth.com/project/fxxUqruK) | `0.2.16-beta` | beta | req/uns | LicenseRef-All-Rights-Reserved | Long-distance LOD renderer. Roxy's only verified jar: voxy-0.2.16-beta for MC 1.21.11 (loaded through Roxy, not natively). |
| [Voxygen](https://modrinth.com/project/xT0lnNE9) | `2.4.2` | beta | req/req | LicenseRef-iSeeEthan-Custom-License | Generates real chunks in the background and feeds them to Voxy, so distant LODs match the modded terrain exactly (no seed approximation). Roxy ships compat for this v2 line. |

## Performance (16)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [BadOptimizations](https://modrinth.com/project/g96Z4WVZ) | `2.4.1` | release | req/uns | ISC | Small client render optimisations. |
| [Clumps](https://modrinth.com/project/Wnxd13zP) | `19.0.0.1` | release | opt/opt | MIT | Groups XP orbs. |
| [Cull Leaves](https://modrinth.com/project/GNxdLCoP) | `4.1.1+1.21.1-neoforge` | release | req/uns | MIT | Culls hidden leaf faces. |
| [Dynamic FPS](https://modrinth.com/project/LQ3K71Q1) | `3.11.4` | release | req/uns | MIT | Lower FPS when the window is unfocused. |
| [Entity Culling](https://modrinth.com/project/NNAgCjsB) | `1.12.1` | release | req/uns | LicenseRef-tr7zw-Protective-License | Skips rendering hidden entities/block entities - important with large factories. |
| [FerriteCore](https://modrinth.com/project/uXXizFIs) | `7.0.3-neoforge` | release | opt/opt | MIT | Blockstate/model memory deduplication. |
| [ImmediatelyFast](https://modrinth.com/project/5ZwdcRci) | `1.6.15+1.21.1-neoforge` | release | req/uns | LGPL-3.0-or-later | Batches immediate-mode rendering (HUD, text, maps). |
| [Leaves Be Gone](https://modrinth.com/project/AVq17PqV) | `v21.1.1-1.21.1-NeoForge` | release | uns/req | MPL-2.0 | Leaves decay quickly after trees are cut. |
| [Lithium](https://modrinth.com/project/gvQqBUqZ) | `mc1.21.1-0.15.4-neoforge` | release | opt/opt | LGPL-3.0-only | Server-tick optimisations (AI, collisions, chunk ticking). NeoForge build. |
| [Model Gap Fix](https://modrinth.com/project/QdG47OkI) | `1.21-1.10` | release | req/uns | GPL-3.0-only | Fixes item model gaps. |
| [ModernFix](https://modrinth.com/project/nmDcB62a) | `5.27.27+mc1.21.1` | release | opt/opt | LGPL-3.0-only | Load time and memory reduction; biggest single win for large packs. |
| [More Culling](https://modrinth.com/project/51shyZVL) | `1.0.11` | release | req/uns | GPL-3.0-only | More block-face culling. |
| [Packet Fixer](https://modrinth.com/project/c7m1mi73) | `3.3.1` | release | opt/opt | MIT | Raises packet size limits for large modpacks. |
| [Particle Core](https://modrinth.com/project/RSeLon5O) | `0.3.3+1.21+neoforge` | release | req/uns | MIT | Particle rendering optimisations. |
| [ServerCore](https://modrinth.com/project/4WWQxlQP) | `1.5.19+1.21.1` | release | uns/req | MIT | Server tick/chunk optimisations. |
| [spark](https://modrinth.com/project/l6YH9Als) | `1.10.124-neoforge` | release | opt/opt | GPL-3.0-only | Profiler for tick/frame/memory analysis. |

## Worldgen (7)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Incendium Legacy](https://modrinth.com/project/ZVzW5oNS) | `5.4.4` | alpha | opt/req | LicenseRef-Stardust-Labs-License | Nether biome + structure overhaul (Stardust Labs). Only 1.21.1 build is tagged alpha upstream; smoke-tested. |
| [Nullscape](https://modrinth.com/project/LPjGiSO4) | `1.2.14` | release | opt/req | LicenseRef-Stardust-Labs-License | End terrain overhaul (Stardust Labs) - gives the End exploration value. |
| [Regions Unexplored](https://modrinth.com/project/Tkikq67H) | `0.6.3-neoforge-21.1` | release | req/req | MIT | Extra biomes (re-added by the owner in 0.5; stacks with Terralith - check biome placement on a new world). |
| [Tectonic](https://modrinth.com/project/lWDHr9jE) | `3.0.28-neoforge-21.1` | release | opt/req | MIT | Terrain shaping: huge mountain ranges, deep valleys, rivers; officially Terralith-compatible. |
| [TerraBlender](https://modrinth.com/project/kkmrDlKT) | `4.1.0.8` | beta | req/req | LGPL-3.0-only | Biome API required by YUNG's Cave Biomes and Regions Unexplored (their mods.toml requires it; Modrinth metadata does not list it, so the resolver never pulled it in). Pinned to the 0.5 instance jar. |
| [Terralith](https://modrinth.com/project/8oi3bsk5) | `2.6.2` | release | opt/req | LicenseRef-Stardust-Labs-License | Biome foundation: ~95 vanilla-block biomes, cave biomes, works with vanilla tooling and Voxy's server-side LOD build. |
| [YUNG's Cave Biomes](https://modrinth.com/project/cs7iGVq1) | `1.21.1-NeoForge-3.1.1` | release | req/req | LicenseRef-All-Rights-Reserved | Cave biomes (re-added by the owner in 0.5; overlaps Terralith's cave biomes). |

## Structures (34)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [ Integrated Dungeons and Structures](https://modrinth.com/project/Z8OZShAU) | `1.13.7+1.21.1-neoforge` | release | req/req | LicenseRef-All-Rights-Reserved | Integrated Dungeons and Structures: hand-built dungeons and towers. |
| [Ad Astra: More Structures](https://modrinth.com/project/1Z4JHpyZ) | `1.0.2` | release | req/req | LicenseRef-All-Rights-Reserved | Structures on Ad Astra planets. |
| [AdoraBuild: Structures](https://modrinth.com/project/rYlnn25U) | `2.11.0` | release | req/req | LicenseRef-All-Rights-Reserved | Decorative builds and small structures. |
| [Aether Villages](https://modrinth.com/project/3P2XnNW6) | `1.0.8` | release | req/req | LicenseRef-All-Rights-Reserved | Villages in the Aether. |
| [ChoiceTheorem's Overhauled Village](https://modrinth.com/project/fgmhI8kH) | `3.6.4` | release | uns/req | CC-BY-NC-ND-4.0 | Biome-specific village overhaul. |
| [Dungeon Crawl](https://modrinth.com/project/q0rRg4lH) | `2.3.17` | release | uns/req | GPL-3.0-only | Large multi-level underground dungeons. |
| [Dungeons and Taverns](https://modrinth.com/project/tpehi7ww) | `v4.4.4+mod` | release | opt/req | LicenseRef-All-Rights-Reserved | Uncommon tier: taverns, illager hideouts, ancient ruins. |
| [Explorify](https://modrinth.com/project/HSfsxuTo) | `v1.6.6` | release | opt/req | LicenseRef-All-Rights-Reserved | Common/uncommon tier: small vanilla-styled ruins, camps and shrines. |
| [Hopo Better Ruined Portals](https://modrinth.com/project/hIpLSyga) | `1.4.4b` | release | opt/req | LGPL-3.0-only | Varied ruined portals. |
| [Hopo Better Underwater Ruins](https://modrinth.com/project/BuWCQzqf) | `1.2.1b` | release | opt/req | LGPL-3.0-or-later | Varied underwater ruins. |
| [Improved Village Placement](https://modrinth.com/project/KA0MllEw) | `1.2.0-neoforge-21.1` | release | uns/req | MIT | Villages placed on flatter, sensible ground. |
| [Integrated Stronghold](https://modrinth.com/project/KUJdfPQz) | `1.1.4+1.21.1-neoforge` | release | req/req | LicenseRef-All-Rights-Reserved | Rebuilt stronghold (Integrated API). |
| [Integrated Villages](https://modrinth.com/project/o1qh5qIF) | `1.3.3+1.21.1-neoforge` | release | uns/req | LicenseRef-All-Rights-Reserved | Larger, detailed villages (Integrated API). |
| [MSS - Moog's Soaring Structures](https://modrinth.com/project/RJCLIx7k) | `2.2.0` | release | uns/req | GPL-3.0-only | Sky structures. |
| [MVS - Moog's Voyager Structures](https://modrinth.com/project/OQAgZMH1) | `5.1.3` | release | uns/req | MIT | Travel-scale overworld structures. |
| [Philips Ruins](https://modrinth.com/project/KdJhOYVV) | `1.21.1-2.0` | release | req/req | LicenseRef-All-Rights-Reserved | Small ruins with loot across biomes. |
| [Repurposed Structures - Neoforge/Forge](https://modrinth.com/project/QDNS5oAT) | `7.5.22+1.21.1-neoforge` | release | uns/req | LGPL-3.0-only | Biome-matched variants of vanilla structures; very configurable rarity. |
| [Sparse Structures](https://modrinth.com/project/qwvI41y9) | `3.0` | release | uns/req | MIT | Spreads structure spacing so the larger structure set does not crowd. |
| [Structory](https://modrinth.com/project/aKCwCJlY) | `1.3.17` | release | opt/req | LicenseRef-Stardust-Labs-License | Common tier: atmospheric ruins and minor discoveries. |
| [Structures](https://modrinth.com/project/6lxFhM2b) | `4.6` | release | opt/req | LicenseRef-GaraKrrals-Project-License-2.0 | Extra overworld structures. |
| [Structures+](https://modrinth.com/project/6WwYmxGF) | `3.1` | release | opt/req | LicenseRef-GaraKrrals-Project-License-2.0 | Extra overworld structures. |
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

## Dimensions (5)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Ad Astra](https://modrinth.com/project/3ufwT9JF) | `1.16.26` | release | req/req | LicenseRef-Terrarium-Licence | Rockets and planets: late-game space exploration. |
| [Deeper and Darker](https://modrinth.com/project/fnAffV0n) | `1.4.1-neoforge-1.21.1` | release | req/req | AGPL-3.0-only | Otherside dimension beyond Ancient Cities; Warden-tier progression. |
| [The Aether](https://modrinth.com/project/YhmgMVyu) | `1.21.1-1.5.10-neoforge` | release | req/req | LicenseRef-Custom | Sky dimension with three dungeon bosses and its own gear line. |
| [The Bumblezone - NeoForge/Forge](https://modrinth.com/project/38tpSycf) | `7.19.3+1.21.1-neoforge` | release | req/req | LicenseRef-All-Rights-Reserved | Unique bee dimension with its own challenge/quest-like progression. |
| [The Undergarden](https://modrinth.com/project/Ejfl5qDL) | `0.9.6` | beta | req/req | LicenseRef-All-Rights-Reserved | Underground dimension with a boss and its own material tier. |

## Rpg (18)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Accessories](https://modrinth.com/project/jtmvUHXj) | `1.1.0-beta.54+1.21.1` | beta | req/req | MIT | Accessory slot framework (Wisp Forest); Curios mods are routed into it by the compat layer, one accessory UI for the whole pack. |
| [Accessories Compat: Elytra & Totem](https://modrinth.com/project/qWoiYCbs) | `1.0.4+1.21.1-neoforge` | release | req/req | LGPL-3.0-only | Elytra and Totem of Undying can be worn in Accessories slots. |
| [Accessories Compatibility Layer](https://modrinth.com/project/ySnjMzLg) | `0.1.13` | release | req/req | MIT | Routes the Curios API (Artifacts, Relics, Dream Relics) into Accessories so every accessory shares one set of slots. |
| [Accessorify](https://modrinth.com/project/CVRzrXGP) | `2.4.0-beta.5+1.21.1-neoforge` | beta | req/req | MIT | Spyglass, lantern, clock, compass and other vanilla tools work from an accessory slot. |
| [Apotheosis](https://modrinth.com/project/rqFWfVlz) | `1.21.1-8.9.0` | release | req/req | LicenseRef-All-Rights-Reserved | Core loot system: affixes, rarities, gems, sockets, world tiers, bosses. |
| [Apothic Attributes](https://modrinth.com/project/DGaH8Rh0) | `1.21.1-2.11.0` | release | req/req | LicenseRef-All-Rights-Reserved | Attribute framework used by Apotheosis (crit, armor pierce, etc.). |
| [Apothic-Enchanting](https://modrinth.com/project/pL8MtgqY) | `1.21.1-1.6.4` | release | req/req | LicenseRef-All-Rights-Reserved | Enchanting overhaul; gives enchanting long-term depth. |
| [Apothic-Spawners](https://modrinth.com/project/DfxVkOAO) | `1.21.1-1.4.0` | release | req/req | LicenseRef-All-Rights-Reserved | Spawner modification - controlled mob-farm progression. |
| [Artifacts](https://modrinth.com/project/P0Mu4wcQ) | `13.2.5` | release | req/req | MIT | Exploration-found accessories (common/uncommon loot). |
| [Better Combat](https://modrinth.com/project/5sy6g3kz) | `2.4.0+1.21.1-neoforge` | release | req/req | LicenseRef-All-Rights-Reserved | Directional, combo-based melee. |
| [Curios API](https://modrinth.com/project/vvuO3ImH) | `9.5.1+1.21.1` | release | req/req | LGPL-3.0-or-later | Accessory slot framework. Pinned to 9.5.1: Curios 9.6.0 reworked CuriosEntityManager and the Accessories compat layer 0.1.13 mixin into it fails (crash on world load). Unpin once a newer compat layer supports 9.6. |
| [Dream Relics](https://modrinth.com/project/zU7VvEmB) | `1.0.5-neoforge+mc1.21.1` | beta | req/req | MIT | Extra unique accessories. Not yet in the loot budget (docs/LOOT_BUDGET.md). |
| [Gateways to Eternity](https://modrinth.com/project/8OIeAukW) | `1.21.1-5.1.0` | release | req/req | LicenseRef-All-Rights-Reserved | Bounded, readable wave challenges (fixed waves, fixed entity counts, visible timer). Activates the gateway data Apotheosis already ships and hosts Horizon's late-game Trials, which consume exploration relics instead of producing them. |
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

## Qol (31)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [AppleSkin](https://modrinth.com/project/EsAfCjCV) | `3.0.9+mc1.21` | release | opt/opt | Unlicense | Food/saturation readout. |
| [BetterF3](https://modrinth.com/project/8shC1gFX) | `11.0.3` | release | req/uns | MIT | Readable F3 screen. |
| [Cherished Worlds](https://modrinth.com/project/3azQ6p0W) | `10.1.1+1.21.1` | release | req/uns | LGPL-3.0-or-later | Pin favourite worlds. |
| [Chunky](https://modrinth.com/project/fALzjamp) | `1.4.23` | release | opt/opt | GPL-3.0-only | World pre-generation. |
| [Cinematic Zoom](https://modrinth.com/project/QQssavr9) | `1.0.0` | release | req/uns | MIT | Smooth client-side zoom for scouting distant terrain and structures. |
| [Common Storage Lib](https://modrinth.com/project/RgLrNK7l) | `0.0.10` | alpha | req/req | MIT | Storage library. |
| [Controlify (Controller support)](https://modrinth.com/project/DOUdJVEm) | `3.0.1+lts` | release | req/uns | LGPL-3.0-or-later | Controller support. 0.6: client-only (its bootstrap loads client Screen classes); marked server-unsupported after it crashed a dedicated server at mod construction. |
| [Controlling](https://modrinth.com/project/xv94TkTM) | `19.0.5` | release | req/uns | MIT | Searchable keybinds and conflict view. |
| [Corpse](https://modrinth.com/project/WrpuIfhw) | `neoforge-1.21.1-1.1.22` | release | req/req | LicenseRef-All-Rights-Reserved | Death recovery: items stay in a corpse at the death spot (also for void deaths) instead of despawning, so dying costs a trip back, not the whole kit. |
| [Cubes Without Borders](https://modrinth.com/project/ETlrkaYF) | `5.0.0+1.21.0.neoforge` | release | req/uns | MIT | Borderless fullscreen. |
| [EMI](https://modrinth.com/project/fRiHVvU7) | `1.1.24+1.21.1+neoforge` | release | req/opt | MIT | Primary recipe viewer with recipe trees. |
| [Farmer's Delight](https://modrinth.com/project/R2OftAxM) | `1.21.1-1.3.4` | release | req/req | MIT | Food variety that makes survival more than bread. |
| [Jade 🔍](https://modrinth.com/project/nvQzSEkH) | `15.10.6+neoforge` | release | opt/opt | CC-BY-NC-SA-4.0 | Block/entity tooltips. |
| [Just Enough Items (JEI)](https://modrinth.com/project/u6dRKJwZ) | `19.64.0.455` | release | opt/opt | MIT | Loads JEI-only plugins (Create, etc.); EMI hides JEI's UI. |
| [KubeJS](https://modrinth.com/project/umyGl7zF) | `2101.7.2-build.381` | release | opt/opt | LGPL-3.0-only | Recipe/loot/progression scripting. |
| [Lootr](https://modrinth.com/project/EltpO5cN) | `1.21.1-1.11.38.127` | release | req/req | LicenseRef-All-Rights-Reserved | Per-player structure loot: each player opens their own copy of every structure container, so the expedition reward budget (docs/LOOT.md) holds per player in multiplayer instead of first-come-first-served. |
| [More Mouse Tweaks](https://modrinth.com/project/S8drsznD) | `1.1.1+1.21.1` | release | req/uns | Apache-2.0 | Extra inventory mouse shortcuts on top of Mouse Tweaks. |
| [Mouse Tweaks](https://modrinth.com/project/aC3cM3Vq) | `1.21-2.26.1-neoforge` | release | req/uns | BSD-3-Clause | Inventory drag/scroll handling. |
| [MouseTweaks x Accessories Fix](https://modrinth.com/project/bFBJU91s) | `1.4.0` | release | req/uns | MIT | Stops Mouse Tweaks' wheel tweak misbehaving in the Accessories screen. |
| [Odyssey Quests](https://modrinth.com/project/lo90fZoB) | `2.0.3` | beta | req/req | MIT | Quest book (Heracles). FTB Quests is CurseForge-only and cannot be in an .mrpack. |
| [Polymorph](https://modrinth.com/project/tagwiZkJ) | `1.1.0+1.21.1` | release | req/req | LGPL-3.0-or-later | Resolves recipe output conflicts between mods. |
| [Puzzles Lib](https://modrinth.com/project/QAGBst4M) | `21.1.66` | release | opt/opt | MPL-2.0 | Library for Puzzles mods. |
| [Resourceful Config](https://modrinth.com/project/M1953qlQ) | `3.0.11` | release | opt/opt | MIT | Config library. |
| [Resourcify](https://modrinth.com/project/RLzHAoZe) | `1.8.7` | release | req/uns | LGPL-3.0-only | In-game browser/updater for resource packs, data packs and shaders. |
| [Sinytra Connector](https://modrinth.com/project/u58R1TMW) | `2.0.0-beta.17+1.21.1` | beta | opt/opt | MIT | Sinytra Connector: loads Fabric mods on NeoForge. |
| [Smooth Swapping](https://modrinth.com/project/ydZic5r4) | `0.9.3.2-1.21.1` | beta | req/uns | LGPL-3.0-only | Animated inventory swaps. |
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

## Dependency (39)

| Mod | Version | Channel | Side (c/s) | License | Why |
|---|---|---|---|---|---|
| [Architectury API](https://modrinth.com/project/lhGA9TYQ) | `13.0.12+neoforge` | release | req/req | LGPL-3.0-only | Required by aether-villages, effectual, shatterbyte-lib, simply-swords, simply-tooltips, tlib |
| [Balm](https://modrinth.com/project/MBAkmtvl) | `21.0.67+neoforge-1.21.1` | release | opt/opt | LicenseRef-All-Rights-Reserved | Required by waystones |
| [Better Advanced Tooltips](https://modrinth.com/project/iHLDc0eo) | `2101.1.0-build.5` | release | req/req | MIT | Required by kubejs |
| [Better ModList](https://modrinth.com/project/sbpqhzIG) | `21.1.5` | release | req/uns | MIT | Required by voxy-worldgen |
| [CERBON's API](https://modrinth.com/project/GkIc6rRo) | `1.3.0` | release | req/req | LGPL-3.0-only | Required by bosses-of-mass-destruction-forge, cerbons-api |
| [Cloth Config API](https://modrinth.com/project/9s6osm5g) | `15.0.140+neoforge` | release | opt/opt | LGPL-3.0-only | Required by better-combat, betterf3, bosses-of-mass-destruction-forge, cristel-lib, effectual, fpm-x-compat, moreculling, moremousetweaks, mythic-upgrades, powah, spider-overhaul, voxy-worldgen |
| [Create: Dragons Plus](https://modrinth.com/project/dzb1a5WV) | `1.11.9` | release | req/req | LGPL-3.0-or-later | Required by create-enchantment-industry |
| [CreativeCore](https://modrinth.com/project/OsZiaDHq) | `2.13.55` | release | req/opt | LGPL-3.0-only | Required by ambientsounds |
| [Cristel Lib](https://modrinth.com/project/cl223EMc) | `neoforge-1.21.1-3.1.7` | release | opt/req | CC-BY-NC-ND-4.0 | Required by towns-and-towers |
| [Fzzy Config](https://modrinth.com/project/hYykXjDp) | `0.7.7+fix1+1.21+neoforge` | release | req/req | LicenseRef-TDL-M | Required by accessorify, particle-core, simply-swords, simply-tooltips, subtle-effects |
| [Geckolib](https://modrinth.com/project/8BmcQJ2H) | `4.9.3` | release | req/opt | MIT | Required by borninchaos, bosses-of-mass-destruction-forge, bossesrise, companions-mod, creeper-overhaul, fantasy_armor, hybrid-api, hybrid-aquatic, mowzies-mobs, occultism |
| [GuideME](https://modrinth.com/project/Ck4E7v7R) | `21.1.22` | release | req/req | LicenseRef-Multiple-OSS-Licenses | Required by ae2, modern-industrialization, powah |
| [Hybrid API [HAPI]](https://modrinth.com/project/yv9f5EAG) | `mc1.21.1-1.1.3-neoforge` | release | req/req | MIT | Required by hybrid-aquatic |
| [Iceberg](https://modrinth.com/project/5faXoLqX) | `1.3.2` | release | req/req | CC-BY-NC-ND-4.0 | Required by advancement-plaques, legendary-tooltips |
| [Knight Lib](https://modrinth.com/project/hAnl9nbm) | `2.0.5` | release | req/req | GPL-3.0-only | Required by companions-mod |
| [Kotlin for Forge](https://modrinth.com/project/ordsPcFz) | `5.13.0` | release | opt/opt | LGPL-2.1-only | Required by fzzy-config, hybrid-api, hybrid-aquatic, particle-core, resourcify, respawn-recap |
| [Lionfish-API](https://modrinth.com/project/FoVacERa) | `3.1` | release | req/req | LGPL-3.0-only | Required by l_enders-cataclysm |
| [Lithostitched](https://modrinth.com/project/XaDC71GB) | `1.8.1-neoforge-21.1` | release | uns/req | MIT | Required by ct-overhaul-village, hybrid-aquatic, improved-village-placement, regions-unexplored, tectonic, terralith |
| [MezzConfig](https://modrinth.com/project/7tEfOcA7) | `0.7.1` | beta | opt/opt | MIT | Required by jei |
| [MidnightLib](https://modrinth.com/project/codAaoxh) | `1.10.0+1.21.1-neoforge` | release | opt/opt | MIT | Required by cull-leaves, visual-overhaul |
| [Modonomicon](https://modrinth.com/project/692GClaE) | `1.21.1-1.123.1` | release | req/req | MIT AND CC-BY-4.0 | Required by occultism |
| [Moog's Structure Lib (moogs_structures)](https://modrinth.com/project/1oUDhxuy) | `3.4.2-neoforge-1.21.1` | release | uns/req | LGPL-3.0-only | Required by mmr-moogs-mineshafts-reimagined, moogs-voyager-structures, mss-moogs-soaring-structures |
| [MossyLib](https://modrinth.com/project/ffLDUGbm) | `2.0.0+1.21.1+neoforge` | release | req/uns | CC-BY-ND-4.0 | Required by inventory-particles |
| [MRU](https://modrinth.com/project/SNVQ2c0g) | `1.0.41+1.21.1-neoforge` | release | opt/opt | LicenseRef-All-Rights-Reserved | Required by sound |
| [oωo (owo-lib)](https://modrinth.com/project/ccKDOlHs) | `0.12.15.6-beta.1+1.21` | beta | req/req | MIT | Required by accessories, accessories-compat-layer, aether, simple-hats |
| [Patchouli](https://modrinth.com/project/nU0bVIaL) | `1.21.1-93-neoforge` | release | req/req | CC-BY-NC-SA-3.0 | Required by apotheosis |
| [Placebo](https://modrinth.com/project/tCkE8p2N) | `1.21.1-9.9.4` | release | opt/opt | MIT | Required by apotheosis, apothic-attributes, apothic-enchanting, apothic-spawners, gateways-to-eternity |
| [playerAnimator](https://modrinth.com/project/gedNE4y2) | `2.0.4+1.21.1-forge` | beta | req/req | MIT | Required by better-combat |
| [Prism](https://modrinth.com/project/1OE8wbN0) | `1.0.11` | release | req/uns | CC-BY-NC-ND-4.0 | Required by legendary-tooltips |
| [Resourceful Lib](https://modrinth.com/project/G1hIVOrD) | `3.0.12` | release | req/req | MIT | Required by ad-astra, creeper-overhaul, handcrafted, odyssey-quests, the-bumblezone, variants-and-ventures |
| [Rhino](https://modrinth.com/project/sk9knFPE) | `2101.2.7-build.85+Rhino-1.21` | release | opt/opt | MPL-2.0 | Required by kubejs |
| [Searchables](https://modrinth.com/project/fuuu3xnx) | `1.0.2` | release | req/uns | MIT | Required by controlling |
| [Simply Tooltips](https://modrinth.com/project/6avVoBVB) | `0.1.5` | release | req/uns | LicenseRef-Timefall-Development-License-1.2 | Required by simply-swords |
| [SmartBrainLib](https://modrinth.com/project/PuyPazRT) | `1.16.11` | release | uns/req | MPL-2.0 | Required by occultism |
| [Sophisticated Core](https://modrinth.com/project/nmoqTijg) | `1.21.1-1.5.39.2489` | release | req/req | LicenseRef-All-Rights-Reserved | Required by sophisticated-backpacks, sophisticated-storage |
| [SWAY API](https://modrinth.com/project/Gj6Yce3v) | `2.4.5-neoforge+1.21.1` | release | req/uns | CC-BY-NC-SA-4.0 | Required by mc2-interactive-foliage |
| [TLib](https://modrinth.com/project/sBn7rVvc) | `1.5.0-1.21.1` | release | opt/opt | MIT | Required by effectual |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/project/1eAoo2KR) | `3.8.2+1.21.1-neoforge` | release | opt/opt | LGPL-3.0-or-later | Required by better-clouds, controlify, particle-interactions, seamless-sleep, sound, spatial-gui, windy |
| [YUNG's API](https://modrinth.com/project/Ua7DFN59) | `1.21.1-NeoForge-5.1.9` | release | req/req | LGPL-3.0-only | Required by yungs-better-desert-temples, yungs-better-dungeons, yungs-better-end-island, yungs-better-jungle-temples, yungs-better-mineshafts, yungs-better-nether-fortresses, yungs-better-ocean-monuments, yungs-better-strongholds, yungs-better-witch-huts, yungs-bridges, yungs-extras |

## Shaders

| Shader | Version | Why |
|---|---|---|
| complementary-reimagined | `r5.9.3` | Default shader. Voxy support since r5.8.1. r5.9.3 chosen over r5.10 (3 days old). |
| complementary-unbound | `r5.9.3` | Cinematic profile alternative. |
| photon-shader | `v1.4` | Balanced-profile candidate (0.3.1). |
| solas-shader | `3.9` | Cinematic-profile candidate (0.3.1). |
| noble | `1.9.9` | Optional (0.3.1). |
| bliss-shader | `2.1.2` | Optional (0.3.1). |

## Considered and rejected

| Candidate | Reason |
|---|---|
| the-twilight-forest | CurseForge-only; not distributable through Modrinth .mrpack. Documented as optional manual add-on. |
| ftb-quests | CurseForge-only. Replaced by Odyssey Quests. |
| alexs-caves | No 1.21.1 build (1.20.1 only). |
| distanthorizons | Mutually exclusive with Voxy. |
| c2me-neoforge | Alpha; worldgen threading risk with heavy worldgen datapacks. |
| noisium | Last 1.21.1 build Aug 2024; overlaps with Lithostitched/Tectonic noise handling. |
| enderio | 1.21.1 line is beta-only; MI + Powah + Create Additions cover its role. |
| industrial-foregoing | Requires Titanium beta; overlaps MI. Excluded for stability. |
| advancedperipherals | Alpha on 1.21.1. |
| simplymore | Only an alpha build (1.3.0_alpha5) for NeoForge 1.21.1; would dilute the Simply Swords/Apotheosis weapon pool. |
| particular-reforged | Overlaps Subtle Effects (ambient particles). One ambient-particle mod is enough; Subtle Effects has finer per-effect config. |
| loot-beams-refork | Apotheosis already draws rarity beams/particles for affix items; a second beam renderer duplicates them. Horizon finds use server-side pickup feedback instead. |
| explorers-compass / natures-compass | Point-to-anything compasses remove discovery. Clues come from exploration maps in loot and quest guidance instead. |
| biomes-o-plenty / oh-the-biomes-weve-gone | Would stack another biome-placement system on top of Terralith + Regions Unexplored. |
| sodium-dynamic-lights / sodium-options-api / immersive-lanterns | 0.5: Sodium Options API (last build 2025-01) requires Reese's Sodium Options, and every Reese's for Sodium 0.8 declares Options API incompatible, so neither loads. Sodium Dynamic Lights needs Options API; Immersive Lanterns 1.0.6 hard-requires Sodium Dynamic Lights. |
| astages | 0.6: researched, deferred. ARR; the headquarters ledger needs no recipe locks (stage unlocks are rewards and services), so no AStages API is required. Revisit if infrastructure recipe gating becomes a goal. |
| open-parties-and-claims | 0.6: researched, deferred. Beta; its claims would need a fake-player/spell/Gateways test matrix not available here. Headquarters membership (charter invite/join) is built into horizon_headquarters.js; Xaero maps are unaffected. |
| exposure / exposure-catalog | 0.6: conditional, not added. The Visual Overhaul camera-controls conflict was reported on Fabric 1.20.1; no NeoForge 1.21.1 client test was possible here. Photo objectives are not part of the campaign. |
| sound-physics-remastered / autohud / fancymenu / chipped / rechiseled / copycats / create-connected / interiors / amendments / bountiful / patchouli | 0.6: not added; each needs client audio/visual/UI comparison that this release could not perform. Charter panel + quest book cover onboarding (no Patchouli); authored charter services replace Bountiful errands. |
| combat-roll / cameraoverhaul / dynamic-crosshair / lambdynamiclights / ryoamiclights | 0.6: experiments only, not added (first-person and lighting ownership unchanged; see docs/ART_DIRECTION.md). |
| punchymoves / fluid-foolish | 0.6.1: superseded by FA Player Extension + Entity Player Compat as the player-movement owner. Punchy Moves animates the whole player body and its own ConflictingAnimationsState flags any FA Player pack (faplayer, freshanimationsplayer, playerextension); the two cannot both own the body. Punchy! (first-person hands) stays. |
| cataclysm-reimagined | 0.6.1: v1.3.5's inventory models reference cataclysm:item/*_gui textures that exist in neither the pack nor Cataclysm 3.33 (22 'Missing textures in model' warnings in a client log, 0 without it): magenta icons. Native Cataclysm icons kept. |
