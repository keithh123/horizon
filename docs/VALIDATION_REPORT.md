# Validation report: Project Horizon 0.1.0

Date: 2026-11-21. Machine: Ryzen 5 9600X, 32 GB, RTX 5070, Windows 11, Prism Launcher 11.1.1.
Evidence comes from the game logs (`latest.log`, `logs/kubejs/*`) and in-game F2 screenshots.

## Passed

| Test | Evidence |
|---|---|
| Dependency resolution | `scripts/resolve.py`: 112 mods, 0 missing deps, 0 declared incompatibilities, no duplicate projects |
| Foundation (renderer + perf, 13 mods) launches | Title screen; world created; `Voxy render system created … MDICSectionRenderer` |
| Staged installs | Stage 1 (worldgen/structures/dimensions, 45 mods) OK. Stage 2 (+RPG/magic) **crashed** on 2 undeclared deps, which were fixed and retested OK. Stage 3 (all, 110 → 112 mods) OK. |
| `.mrpack` structure | 114 files, all URLs on Modrinth's CDN whitelist, no duplicate paths, sampled URLs return 200 with matching sizes |
| **Fresh Prism import** | `prismlauncher --import` created `ProjectHorizon-0.1.0`: MC 1.21.1, NeoForge 21.1.267, 112 jars, **all sha512 match the lock**, both shaders, all overrides |
| Imported instance launches | Title screen in ~30 s |
| World create / save / reopen | `ImportTest` created, saved on quit, reopened via quick play. Voxy World Gen data persisted for 6 dimensions. |
| KubeJS | Startup 2/2, client 2/2, server 1/1 scripts, 0 errors. Recipes: **13 added, 6 removed, 0 failed** |
| Relic items | `/give horizon:ancient_core` works; textures and rarity render |
| Global loot modifiers | `/loot give … cataclysm:entities/ignis` ×2 gave 3 Starforged Hearts |
| Structure tag + spacing | `/locate structure #horizon:arise_any`: WDA abandoned temple 610 blocks away |
| Quests | Heracles `Loading quests` with no `Failed to load quest`. `J` opens the book. "Discover Quests" toast shows. |
| Dimensions entered | Aether, Otherside, Bumblezone, Undergarden, Nether (Incendium), End (Nullscape). Pack advancements fired. |
| Shaders + Voxy | Complementary renders. `IrisVoxyRenderPipeline` active in the Overworld. |
| Voxy World Gen | `voxy integration initialized (enabled: true)`, ~15 chunks/s, server tick 14.6 ms |
| Config patches | 12 settings in 5 files, each asserted to match exactly once against the generated defaults |
| Keybinds | 248 audited, 0 in-world conflicts left (modifier keys and GUI-only recipe-viewer keys excluded) |
| Performance profiles | `apply-profile.ps1` switches Performance ⇄ Balanced correctly (options, Voxy, Iris, instance memory), BOM-free |
| **Dedicated server** (EULA accepted by the operator) | `build.py server`: 97 server-side mods (15 client-only mods correctly excluded). `Done (11.544s)`. **20.0 TPS in all 9 dimensions**, overall 1.1–1.2 ms/tick idle. KubeJS 13 added / 6 removed / 0 failed. Quests loaded. `/locate` of the WDA tag (71 blocks) and Burning Arena in the Nether (5,649 blocks, i.e. legendary rarity) both work. Aether/Otherside/Bumblezone/Undergarden chunks force-loaded. Ignis loot dropped. `save-all` and `stop` completed cleanly. |

## Failed / known defects

| Issue | Impact | Status |
|---|---|---|
| Complementary r5.9.3 Voxy shader patch fails in **the End** (`undefined variable "texCoord"`) | Voxy falls back to its normal pipeline: distant End terrain renders without shader styling | Known issue. Watch for a Complementary fix. |
| GeckoLib "Unable to parse animation" ×3 at startup | 3 animations of one mob may not play | Cosmetic, upstream |
| `POI data mismatch` server errors while teleporting between dimensions | None observed | Vanilla/upstream log noise |
| An MI energy tooltip ("Total Energy Stored: 6000 EU") appeared on a hovered vanilla block in the creative inventory | Cosmetic tooltip | Not investigated |

## Untested (be aware)

- **Dedicated server with a player connected**: the server was tested headless only. A client joining over the network, and server/client config sync, have not been tried.
- Distant-horizon **screenshot proof** of Voxy LODs: the renderer and worldgen were confirmed by logs, but the planned high-altitude screenshot was interrupted (player fell, then a Windows Family Safety window took focus).
- Hands-on **combat** (Better Combat movesets, Simply Swords uniques, Apotheosis affix rolls in a fight, boss fights), **spellcasting**, and **building machines** (Create contraption, Mekanism, MI multiblocks, AE2 autocrafting). These were verified only at the recipe/registry/log level, not by playing.
- Completing quests and claiming rewards (loading and opening the book only).
- Performance and Cinematic frame rates, multi-hour sessions, Spark profiles, large factories.
- Survival balance over a real playthrough. The balance changes are reasoned and documented, not playtested.
- Twilight Forest add-on (CurseForge-only, not part of the pack).

## Verdict

The pack imports and launches cleanly in Prism. Its content, integration scripts, loot, quests and all
dimensions load, and Voxy runs with shaders. It is **playable, not finished**: the untested list above is
real work, especially gameplay balance and a multiplayer session with players connected.

Server-only log notes (harmless): Relics' client-only `ScreenMixin` is skipped on the dedicated server
("invalid dist"), and a Tectonic `fabric:overlays` metadata condition is reported. Both appear without
any functional effect.
