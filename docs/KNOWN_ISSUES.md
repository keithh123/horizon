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
| 9 | Ports were tested in game for loading and their main effect; sounds (Armour Sound Tweak, Item Landing Sound) and Eating Animation frames could not be observed by the automated test. | Remove the jar from `mods/` if one misbehaves; see docs/PORTS.md. |
| 10 | Yeti and Underworld Knight (Bosses' Rise) ignore `/kill`/`/damage` during their intro; their first-kill Legend was not observed in testing. | Kill them in a normal fight. |
| 11 | Streams Reflowing pre-computes river plates on new chunks: first minutes in fresh regions load more slowly (the mod says so in chat). | Expected; Performance profile lowers its particle scan. |
| 12 | Spatial GUI moves JEI's recipe/bookmark lists on first launch. | Change back in JEI settings if preferred. |
| 13 | Punchy Moves shows a first-join tutorial and owns an over-the-shoulder camera; Auto Third Person owns vehicle/elytra switching. | Skip the guide; camera options in Punchy Moves' Camera tab. |
| 14 | Prism shows an "Easy There!" prompt on import listing the 7 jars that ship inside the pack (docs/PORTS.md). | Expected for this pack; tick "I trust this modpack". |

## 0.3.1

| # | Issue | Workaround |
|---|---|---|
| 15 | The quest popup, inventory button, one-click open, per-open centring and minimap-off are compiled and their mixin targets were checked against Heracles 2.0.3 bytecode, but have **not been run in a client**. | If the quest screen misbehaves, remove `horizon_questbook-*.jar`; Heracles' own screens return. |
| 16 | Clavis is disabled by default: its lockpicking screen moves the OS cursor with GLFW and the stuck-cursor bug after lockpicking could not be reproduced or fixed here. Moonlight was not available. | Rename `Clavis-*.jar.disabled` to `.jar` to try it (success, cancel and Lootr reopen untested). |
| 17 | Immersive Portals 6.0.7 (native NeoForge) is not shipped. Server: loads, 20 TPS, 5.5 ms/tick vs 5.7 baseline with the three dimensions force-loaded. Client (Voxy/Iris/Sodium, fresh chunks, Nether round trip, End, frame times): untested. | Do not add it to a pack with Voxy until a client run says otherwise. |
| 18 | Bliss Shaders has no Voxy programs: with it, distant terrain is unshaded or missing. Photon, Solas and Noble have them. All presets are generated but not looked at in game. | Use Complementary or Photon (Balanced), Unbound or Solas (Cinematic). |
| 19 | FA Objects, Spiders, Creepers and Classic Horses are held back (not checked against Spider Overhaul, Lootr, Create). | docs/RESOURCE_PACKS.md. |
| 20 | Boss wind-ups: no change beyond Better Combat debug boxes off. Each boss mod owns its animation; Horizon cannot add a telegraph without per-boss work. | - |
| 21 | Existing worlds: the first quest keeps its task type, so saved progress should carry over, but a world where it was already complete was not loaded to confirm. | Back up `saves/` before updating. |
