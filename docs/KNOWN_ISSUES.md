# Known issues

| # | Issue | Workaround |
|---|---|---|
| 1 | Complementary r5.9.3: Voxy shader patch fails in the End. Distant End terrain renders unshaded. | None needed. Overworld, Nether and modded dimensions are unaffected. |
| 2 | With shaders on, Create (Flywheel) falls back to non-instanced rendering. | Expected with Iris. Use the Performance profile (shaders off) for huge contraption bases. |
| 3 | First hour of a new world: Voxy World Gen fills the horizon gradually (~15 chunks/s). | Normal. Lower its radius in `config/voxyworldgenv2*` on weak CPUs. |
| 4 | Startup log shows GeckoLib animation parse errors, an expired Xaero's World Map online version check, a Terralith fzzy-config metadata warning, Roxy optional-compat `ClassNotFoundException`s, and CTOV `wares:` loot-table errors (Wares is not installed). | Harmless. |
| 5 | Some armour/gear ability keys are unbound by default to avoid conflicts (Cataclysm armour, Mekanism legs mode, Occultism satchels, Aether invisibility). | Bind them in Options → Controls (searchable). |
| 6 | The Twilight Forest and FTB Quests are not included (CurseForge-only). | See INSTALLATION.md for the optional Twilight Forest add-on. |
| 7 | Dedicated server tested headless only (20 TPS, all dimensions). A multiplayer session with real players hasn't been tried. | See VALIDATION_REPORT.md. |
| 8 | Beta/alpha upstream builds: Roxy, Voxy, Voxy World Gen, Iris beta, Undergarden, Odyssey Quests, CC: Tweaked, Incendium (alpha). | Pinned and smoke-tested. Back up worlds before updating any of them. |

## 0.3.0 expansion

| # | Issue | Workaround |
|---|---|---|
| 9 | Five source ports and Weather Glass are compiled/hash-pinned but not yet tested in game. | Remove the jar from `mods/` if one misbehaves; see docs/PORTS.md. |
| 10 | Yeti and Underworld Knight (Bosses' Rise) ignore `/kill`/`/damage` during their intro; their first-kill Legend was not observed in testing. | Kill them in a normal fight. |
| 11 | Streams Reflowing pre-computes river plates on new chunks: first minutes in fresh regions load more slowly (the mod says so in chat). | Expected; Performance profile lowers its particle scan. |
| 12 | Spatial GUI moves JEI's recipe/bookmark lists on first launch. | Change back in JEI settings if preferred. |
| 13 | Punchy Moves shows a first-join tutorial and owns an over-the-shoulder camera; Auto Third Person owns vehicle/elytra switching. | Skip the guide; camera options in Punchy Moves' Camera tab. |
| 14 | Seen once: a tooltip reading "Dark Oak Trapdoor - Total Energy Stored: 6000 EU" while hovering the EMI panel in the Spatial GUI inventory. Not reproduced. | Unknown; report if seen again. |
