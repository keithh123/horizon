# Validation report: Project Horizon 0.6.0 (headquarters campaign)

Date: 2026-11-26. Machine: Linux container, 4 vCPU, 15 GB RAM, OpenJDK 21.0.13, no GPU, **no graphical client and no second
player**. Evidence files: `tests/evidence/server_hq_2026-11-26.txt`, `tests/hq_sim.js`, `.horizon/logs/` (local), build log
lines quoted below. Earlier sections of this report (0.1-0.5) describe the Windows reference machine and stay valid for what
0.6 did not change.

## Passed (0.6)

| Test | Evidence |
|---|---|
| Static: stage graph acyclic and ordered, choice minimums satisfiable, every id valid, no relic in any reward/service/supply/kit, no stage refunds its own cost, every requirement kind implemented | `gen_headquarters.py` validation (aborts the build otherwise) |
| Static: no luck-only bottleneck (each required discovery has >= 3 eligible destinations or sits in a choice) | `docs/HQ_GRAPH.md`, enforced by `gen_headquarters.py` |
| Static: 233 quests, 0 audit problems (incl. new rules: no overlapping icons, stage quests complete only on ledger mirrors, XP-only spine rewards); all 214 0.5 quest ids present | `audit_quests.py`; id comparison against `HEAD` |
| Static: dependency ranges for 296 mod ids (lock + shipped ports), 0 failures | `manifests/deps_report.json` |
| Ledger state paths: 71 checks - unmet requirements, prerequisite order, exact consumption, double click, partial contribution not consumed, remote click refused, borrowed machine refused, press-never-ran refused, invites, late joiner (mirrors, no rewards), offline member's facts, login catch-up, replayed sync, independent stations, cannot join twice, owner leaving, last member leaving, mirrors never revoked, 2-of-3 regions, repeated contribution no-op, optional third region, non-member cannot break anchor, dormant station, relocation keeps stages, destroyed anchor, hq/player service scopes and cooldowns, Foundry crate replacement, fixtures unrewarded, migration, full campaign with each reward exactly once and one finale | `node tests/hq_sim.js` -> 71 passed, 0 failed |
| Dedicated server boots (fresh world) with all 0.6 content | "Done" in 108-115 s; KubeJS: startup 3/3 and server 4/4 scripts, 0 errors, 0 warnings; 16 recipes added, 0 failed |
| Real adapter on the dedicated server, before and after `/reload`: found, persistence, unmet refusal, room scan incl. `#c:chests` tag, Outpost commission with exact consumption and rewards (copper stick, emblem, chart), double-commission no-op, Create pressing recipe loaded, Workshop refused until "press ran", Workshop commissioned, plates consumed, iron stick, Supply Crate loot + cooldown, destroyed charter -> dormant with stages kept, dormant refusal, rebind | `/horizon hqadmin selftest`: 23 passed, 0 failed (twice). FakePlayer fixture - see limits |
| Ledger survives a full server restart | second boot lists `hq1 ... stages=3/6`, `hq2 ... 2/6` |
| Service/chart loot tables roll real items from the console | `Dropped 1 [Tide Chart]`, `[Surveyor's Chart]`, `[Lair Chart]`, Foundry crate `Dropped 7 items` |
| All 7 optional plans are valid structure NBT with valid block states | `/place template` of each: "Loaded template ..." x7 |
| Generator ownership / idempotence | see "Release build" below |

## Failed, then fixed (0.6)

| Problem | Fix |
|---|---|
| **0.5's dedicated server could not boot**: Controlify (client-only) crashed mod construction | roster side override `server: unsupported` |
| Terra Curio's embedded ParticleStorm declared client-touching GeckoLib mixins as common -> MixinTransformerError on every server | `ports/terracurio` (LGPL repack, mixins moved to the client list) |
| KubeJS 2101 Rhino: block-scoped `const`/`let` in functions -> "redeclaration of var" at run time; `Level.getGameTime()` invisible; `server.getLevel(key)` and `BlockState.is(TagKey)` ambiguous; `level.dimension` is KubeJS's property | function-scoped `var`; `levelData.getGameTime()`; level lookup by iteration; explicit overload `['is(net.minecraft.tags.TagKey)']`; `dimensionKey` (found with an on-server interop probe) |
| Loot with a player context turns exploration maps into Supplementaries' Cartographer's Quill | documented (KNOWN_ISSUES #23); the selftest accepts the quill |
| A bulk "client-only" detection loop misattributed six server mods from mixin warnings | reverted before any build; only Controlify kept (verified by boot) |
| Scanners ignored shipped port jars (Terra Curio vanished from ids/loot audit after becoming a port) | `scripts/shipped.py` adds default-variant ports to index_ids/audit_loot/check_deps/gen_datapack |

## Not verified (0.6) - needs a client and/or a second player

- Charter panel in a real client: layout, hovers, click handling at small/large GUI scales, controller (Controlify) use.
- Real-player advancement reading/granting by the ledger (FakePlayer advancements are no-ops, so the selftest injects facts).
- Two-player invite/join/leave, concurrent clicks from two clients, offline credit with real players.
- Stages III-VI in survival (exercised only in `hq_sim.js` and by fixtures); Gateways trial completion credit; the finale sequence on screen.
- New mods in a client: Construction Sticks charging/undo, FramedBlocks camo/culling/shaders, Handcrafted, Create Deco,
  Comforts with Seamless Sleep; Fresh Compats visuals; First-person Model matrix; Terra Curio/ParticleStorm client effects.
- Art in game (only an 8x contact sheet was inspected), sounds against rain/machinery/combat, subtitles.
- Client performance (frame-time percentiles, memory, GC), shader/no-shader comparisons, Voxy chain in all dimensions.
- A Prism import of the new .mrpack (Prism not available): replaced by a headless install + byte verification (below).

## Release build and packaging (0.6)

| Check | Result |
|---|---|
| `python scripts/build_all.py --no-configs --mrpack` (frozen resolve online; every generator twice) | **idempotent: 1386 owned files identical across two full runs**; `hq_sim` 71/71 in both runs; 233 quests |
| `patch_configs.py` | **skipped deliberately** (`--no-configs`): it reads a launched Windows dev instance, absent here. Its owned files are the 0.5 versions, unchanged |
| `dist/ProjectHorizon-0.6.0.mrpack` | 267 index files, 4.7 MB |
| Headless client install (`scripts/mrpack_install.py ... --side client`) | 267 index files hash-checked, 1370 override files byte-identical, 261 entries in `mods/` (Clavis + the 3 first-person jars `.disabled`), **0 problems**; Fresh Compats present, not enabled in `options.txt` |
| Headless server install (`--side server`) | 186 index files + server overrides, 188 mod entries; identical to the mod set booted in the server tests except Clavis `.disabled` |
| Graphify refresh + `tests/test_horizon_graph.py` | 9/9 tests (incl. new headquarters stage/option/mirror and ownership checks); graph: 6 hq stages, 8 services, 233 quests |

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


---

# Addendum: 0.2.0 (2026-11-21)

| Check | Result |
|---|---|
| Dependency check | 0 failures. Subtle Effects/Fzzy range was a checker false positive; real client loaded both. |
| Client launch (fresh instance, 116 mods) | Reached the title screen in ~42 s. Errors in log: only known noise (GeckoLib x3, Xaero version check, `fabric:overlays`, 4 upstream advancements). |
| Loot calibration | 25 structures measured on a headless server; budgets regenerated; generators idempotent across two runs. |
| Headless server smoke | Boots, 0 Horizon loot/recipe/quest errors, audits run. Not a gameplay test. |
| Profiles | performance / cinematic / balanced switch correctly on the test instance (options, effects, memory). |

**Not tested (no hands-on session was possible):** textures and tooltips in-game, quest completion and reward claiming, Lootr, trophies, Trials, combat, spellcasting, machines, AE2, frame rates/Spark profiles, `minecraft:end_city` calibration, multiplayer. A fresh Prism import of the 0.2.0 `.mrpack` is recorded below once run.

**0.2.0 release package (verified 2026-11-21):** `dist/ProjectHorizon-0.2.0.mrpack` (sha256 `4803c7447f316776dbecd018280e839f863e99aa6fd6060a1311fcbebacd9fdb`, 118 files, 116 mods). Fresh Prism import: all 118 files match their sha512, 943/943 override files present, launches to the title screen in ~39 s with 5 logged errors (the known GeckoLib/Xaero/advancement/`fabric:overlays` noise).

## 0.3.0 expansion

Done: dependency ranges for 205 mod ids (2 launch-verified checker quirks); client launch to title with all jars
(44-50 s); dedicated server start + 3 test runs (`tests/expansion_smoke.txt`): new loot tables through the Horizon GLMs,
structures located in natural Terralith/Tectonic terrain and audited (lich tower 0.9 Ancient Core per clear vs budget
1.0), 12 new bosses/mobs summoned, Legend hook fired for 7 bosses, 20 TPS, Nether/End load; in world with shaders and
Voxy on: Spatial GUI inventory + EMI, F3 metrics; profile switcher for all three profiles on a copy of real configs;
generator pipeline twice (idempotent); 0.2.0 loot groups unchanged (0 of the existing groups differ).

Ports in game: Snowy Leaves (state + tint), Better Smoke (plumes), Grand Teleport (transition), Weather Glass (frost) observed; all 7 load without errors. Fresh Prism import of the 0.3.0 .mrpack: 191/191 files match the lock hashes, title screen in 39 s.
Not done yet: eating frames and port sounds (not observable by automation); Better Combat/spell/Punchy animation interplay;
AE2 terminal screens under Spatial GUI; shader visual check of Better Clouds/Interactive Foliage; matched performance
comparison; multiplayer with real players.


---

# Addendum: 0.3.1 (2026-11-22)

What actually ran:

| Check | Result |
|---|---|
| Full generator pipeline twice (`build_all.py --offline`) | Idempotent: 1051 owned files identical. `check_deps` 0 failures. |
| `audit_quests.py` | 143 quests, 0 problems (placeholders, duplicate titles, prerequisites, cycles, early-chain deadlock). |
| Source port `horizon_questbook` | Compiles with Gradle against Heracles 2.0.3, Resourcefullib, Olympus. |
| Dedicated server (`tests/quest_hats_smoke.txt`) | Boots in ~50 s with 129 server mods, KubeJS 3/3 scripts 0 errors (new `horizon_book.js`), the 8 reward hats and `heracles:quest_book` resolve as items, `horizon:welcome` advancement loads (only the 4 known upstream advancement errors remain), 20 TPS in every dimension. |
| Server with Immersive Portals 6.0.7 (`tests/ip_server_smoke.txt`) | Loads (Immersive Portals Core 1.0.0), 20 TPS; overall 5.46 ms/tick with the three dimensions force-loaded vs 5.66 ms/tick without it (same commands, same seed; world generation noise dominates). |
| `build.py instance` update | On a copy of the 0.3.1 instance: a manually added jar survived, a stale Horizon-shipped jar was removed, `saves/` untouched, Clavis stayed `.jar.disabled`. |

**Could not run: any client.** The session had no display (`glfwGetPrimaryMonitor failed`), so nothing below was seen:
quest popup/inventory button/centring/minimap, claim flow and the early chain through reward claiming, hat rendering,
Fresh Animations add-ons, the Horizon cues, the Photon/Solas/Noble/Bliss presets (only generated and checked for Voxy
programs), Immersive Portals rendering (fresh chunks, Nether round trip, End, frame times), and Clavis (success/cancel/Lootr
reopen, cursor, Moonlight). Treat those as untested until someone plays the build.


## 0.3.1 client pass (2026-11-22)

Fresh Prism import of `ProjectHorizon-0.3.1.mrpack` (185 mod files, Clavis `.jar.disabled`) and a new world.

Passed: J, right-clicking the Heracles quest book, and the inventory button all open the same screen; chapters open centred;
no minimap; one click opens the popup (description, requirements, prerequisites, rewards, Claim); X and Esc close it;
first quest (Check) -> claim -> Timber! unlocks -> 16 logs complete it -> claim; progress and claims survive save/quit;
relog does not repeat the starter-book gift (2 books after relog = 1 gift + 1 quest reward); a copied 0.3.0 world shows its
completed quest ("Spirits and Chalk") as complete and claimable; Photon v1.4 loads with Voxy patches applied and Voxy
terrain visible at the horizon; the Big Crown hat renders on the player.

Not tested: Solas, Noble, Bliss, Complementary Unbound and any shader in the End; Fresh Animations Details/Emissive/Quivers
visuals; the Horizon cue sounds (no audio observation); Immersive Portals client (not enabled); Clavis (not enabled);
Moonlight; hat rarity/Curios slot behaviour; multiplayer.
