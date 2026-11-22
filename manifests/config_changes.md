| File | Setting | Reason |
|---|---|---|
| `effectual.json` | `"caveDust": false` | Cave Dust owns underground dust (no double dust layers). |
| `effectual.json` | `"snowFootprints": false` | Footprint Particle owns footprints. |
| `effectual.json` | `"lanternImprovements": false` | Swinging Lanterns owns lantern behaviour. |
| `effectual.json` | `"blockPlaceEffect": false` | Particle Interactions owns block place/break particles. |
| `effectual.json` | `"runDust": false` | Footprint Particle owns running/snow dust; no doubled footstep puffs. |
| `simplehats.json5` | `"enableMobLoot": false` | Hats are curated quest rewards (rare ones) and craftable from scraps; random mob drops would bypass the loot budget. |
| `simplehats.json5` | `"enableChestLoot": false` | Same: no hat bags in structure chests, Horizon's calibrated chest budgets stay exact. |
| `bettercombat/client.json5` | `"isDebugOBBEnabled": false` | Crisp hits: no debug hit-box outlines drawn around targets. |
| `footprintparticle.json` | `"waterSplashLevel": "DISABLED"` | Subtle Effects owns water splashes; no second splash on entering water. |
| `particlerain/config.json` | `"rainVolume": 0.0` | Cool Rain owns rain audio (Particle Rain stays visual); avoids three layered rain loops. |
| `particlerain/config.json` | `"snowVolume": 0.0` | Same: one owner for precipitation audio. |
| `punchy_moves/camera.json` | `"elytraCamera": false` | Auto Third Person owns the elytra/vehicle camera switch; one camera owner per state. |
| `visualoverhaul.json` | (seed file) | Visual Overhaul's first-launch hook writes its config from a PackRepository mixin before MidnightLib registers it (NPE at Options.loadSelectedResourcePacks; client crash, tested). Its built-in packs still load (visualoverhaul:rounddiscs seen in the pack list). |
| `apotheosis/apotheosis.cfg` | `B:"Restrict Charms to Curios"=true` | Potion charms only work from curio slots - stops 20 charms in an inventory stacking buffs. |
| `apotheosis/apotheosis.cfg` | `I:"Boss Spawn Cooldown"=6000` | Apotheosis bosses stay special next to Mowzie's/Cataclysm encounters. |
| `simplyswords/weapon_attributes.toml` | `iron_damageModifier = 1.0` | iron Simply Swords weapons: +3 -> +1 so they sidegrade vanilla/Apotheosis weapons instead of replacing them. |
| `simplyswords/weapon_attributes.toml` | `gold_damageModifier = 1.0` | gold Simply Swords weapons: +3 -> +1 so they sidegrade vanilla/Apotheosis weapons instead of replacing them. |
| `simplyswords/weapon_attributes.toml` | `diamond_damageModifier = 1.0` | diamond Simply Swords weapons: +3 -> +1 so they sidegrade vanilla/Apotheosis weapons instead of replacing them. |
| `simplyswords/weapon_attributes.toml` | `netherite_damageModifier = 1.0` | netherite Simply Swords weapons: +3 -> +1 so they sidegrade vanilla/Apotheosis weapons instead of replacing them. |
| `simplyswords/loot.toml` | `standardLootTableWeight = 0.08` | fewer filler weapons in chests |
| `simplyswords/loot.toml` | `rareLootTableWeight = 0.25` | rare weapons stay rare |
| `simplyswords/loot.toml` | `runicLootTableWeight = 0.35` | runic weapons compete with Apotheosis affix loot |
| `simplyswords/loot.toml` | `uniqueHardPity = 100` | uniques are milestone finds |
| `voxy-config.json` | `"service_threads": 3` | Balanced: leave CPU for worldgen + factories (6-core target). |
| `iris.properties` | `shaderPack=ComplementaryReimagined_r5.9.3.zip` | Complementary Reimagined (Voxy-aware since r5.8.1) is the default look. |
