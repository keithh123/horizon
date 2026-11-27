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
| 15 | Quest popup, inventory button, book right-click, J, centring, one-click details, X and Esc were played in game on 2026-11-22. Not exercised: popups for selectable/loot-table rewards, editor mode (it keeps Heracles screens), multiplayer. | If the quest screen misbehaves, remove `horizon_questbook-*.jar`; Heracles' own screens return. |
| 16 | Clavis is disabled by default: its lockpicking screen moves the OS cursor with GLFW and the stuck-cursor bug after lockpicking could not be reproduced or fixed here. Moonlight was not available. | Rename `Clavis-*.jar.disabled` to `.jar` to try it (success, cancel and Lootr reopen untested). |
| 17 | Immersive Portals 6.0.7 (native NeoForge) is not shipped. Server: loads, 20 TPS, 5.5 ms/tick vs 5.7 baseline with the three dimensions force-loaded. Client (Voxy/Iris/Sodium, fresh chunks, Nether round trip, End, frame times): untested. | Do not add it to a pack with Voxy until a client run says otherwise. A hand-added test instance (Immersive Portals + Immersive Infinity + Make it Compatible) loads and renders Voxy terrain in the main view only after `gen_portal_guards.py` and `patch_micimmptl.py`; Voxy LODs inside portal views are disabled, and Immersive Portals itself prints an in-game "incompatible with Voxy" warning. |
| 18 | Bliss Shaders has no Voxy programs: with it, distant terrain is unshaded or missing. Photon, Solas and Noble have them. All presets are generated but not looked at in game. | Use Complementary or Photon (Balanced), Unbound or Solas (Cinematic). |
| 19 | FA Objects, Spiders, Creepers and Classic Horses are held back (not checked against Spider Overhaul, Lootr, Create). | docs/RESOURCE_PACKS.md. |
| 20 | Boss wind-ups: no change beyond Better Combat debug boxes off. Each boss mod owns its animation; Horizon cannot add a telegraph without per-boss work. | - |
| 21 | Existing worlds: the first quest changed from an advancement task to a Check task (same boolean storage). A copied 0.3.0 world kept its completed quest, but one with the old first quest already completed was not available to check. | Back up `saves/` before updating. |
| 22 | 0.6: the headquarters campaign has been verified by Node ledger tests (71 checks) and a dedicated-server FakePlayer selftest (23 checks, Outpost and Workshop through the real adapter), **not by a player in a client**. The charter's chat panel layout, button hovers, real-player advancement reading/granting, two-player invite/join and stages III-VI in survival are unverified. | Report anything odd with `/horizon hqadmin info <hq>` output; nothing in the ledger is ever deleted. |
| 23 | 0.6: survey charts and the Outpost chart arrive as a Supplementaries **Cartographer's Quill** when a player receives them (Supplementaries' lazy explorer map: it searches when used). From a console/chest without a player they are filled maps. | Use the quill to draw the map; if it reports no target nearby, try again from elsewhere. |
| 24 | 0.6: Terra Curio is shipped as a local repack (`ports/terracurio`) because its embedded ParticleStorm crashed every dedicated server. The mixin move is server-tested only; ParticleStorm's GeckoLib effects in a client are untested. | If accessory particle effects look wrong, compare with the Modrinth jar on a singleplayer copy. |
| 25 | 0.6: Controlify is now client-only in the pack (it crashed dedicated servers). Controller support on clients is unchanged. | - |
| 26 | 0.6: Fresh Compats ships but is not enabled, and the First-person Model preset (FPM + Not Enough Animations + FPM Compat) ships disabled: neither was visually checked. | Enable Fresh Compats above Fresh Animations in Resource Packs; enable the three `.disabled` jars together in Prism to try first-person bodies. |
| 27 | 0.6: KubeJS logs parse fallbacks for some third-party recipes (e.g. `createdeco:placard`, `incendium:upgrade_elytra`); vanilla parsing takes over and the recipes load. | None needed. |
| 28 | 0.6: a headquarters records "facts" (advancements) when a member is online at login or uses the charter. An advancement earned by a member who never logs in again after earning it while the station was not used is not seen. | Members log in or open the charter once; `/horizon hqadmin resync` records online members. |

## 0.6.1 visual/interaction repair

| # | Issue | Status |
|---|---|---|
| 29 | 0.6.0: right-clicking a placed Survey Charter did nothing (no panel, no message). Cause: KubeJS 2101's `event.cancel()` throws `EventExit` (verified in the 2101.7.2 bytecode), and the charter handler called it as its first statement, so every real click left the handler before any code ran; the FakePlayer selftest never went through the event. The protected-charter break refusal had the same ordering (message never sent). | Fixed: `cancel()` is the last statement in both handlers, the click logic is wrapped with an error message, and `tests/kubejs_lint.js` (run by `build_all.py` and `/horizon-check`) fails on any exit call that is not the last statement. Reproduced and re-checked with real use-key clicks in a client (docs/VALIDATION_REPORT.md 0.6.1). |
| 30 | 0.6.0: the Apothic Attributes and Accessories inventory buttons were drawn on top of each other. Both default to the top-right corner of the player preview: Apothic at guiLeft+25+(51-10)-3, guiTop+7+3 = (63,10), 10x10; Accessories (owo layer) at (66,8), 8x8 (read from both jars). | Fixed: Apothic's button moves to the preview's top-left corner (anchor `top_left`, +3/+3 = (28,10)), shipped through `patch_configs.py` (`config/apotheosis/apothic_attributes.cfg`). Accessories keeps (66,8); Aether's accessory button stays at (27,68). |
| 31 | 0.6.0, shaders OFF: in rain and thunder the whole landscape vanished (sky/fog colour everywhere; nearby chunk fragments, particles and entities still drawn). Clear weather was fine; shaders on hid it. Client bisection on a copy of the affected world (shots in docs/VALIDATION_REPORT.md 0.6.1): not Roxy's weather fog, not Atmospherics, not Sodium fog occlusion, not particles, not render distance; disabling Particle Rain + Cool Rain + Windy + Better Clouds + Weather Glass fixed it, re-enabling all but Weather Glass kept it fixed. | Fixed by removing **Weather Glass 0.6.2** from the default install (moved to the `lab` variant; `ports/weatherglass/port.json`). Tradeoff: no raindrop/frost film on glass panes; Particle Rain still draws rain, splashes and ripples. Not a config tweak: its film/fog layer is drawn whenever it rains. |
| 32 | 0.6.0 instance had `renderDistance:2`; Voxy itself warns in chat that a vanilla render distance below 3 "can cause rare culling near the edge of your screen", and the reported x-ray holes appeared while moving at that setting. The automated route at 2 did not reproduce a hole on demand. | Render distance is the player's choice: `build.py instance` keeps it and only prints a warning below 3 (Voxy's minimum). The profiles never go below 8; use at least 3, ideally 8, with Voxy on. |
| 33 | Mandala's GUI Dark Mode 1.21.5 build declares pack_format 55; Minecraft drops such a pack from `options.txt` unless the player accepted it. | The updater lists it in `incompatibleResourcePacks`; the pack screen shows it as "made for a newer version". |
| 34 | Clicking the charter with an item in the off hand also used that item (a torch was placed against the charter). | Off-hand pass consumed server-side and a client script (`kubejs/client_scripts/horizon_charter_client.js`) consumes the click before vanilla falls through to the off hand. |
