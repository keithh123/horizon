# Project Horizon polish pass: handoff report (2026-11-22)

Written so another assistant can pick the work up cold. Everything below is what was actually done or measured in this session.
Nothing is committed (but `git add -A` was run by mistake, so ~241 files are STAGED, including `.claude/` and regenerated outputs).
No .mrpack was built, no fresh Prism import was done, nothing was released.

## Context

- Repo: Project Horizon modpack, Minecraft 1.21.1 / NeoForge 21.1.267, Prism Launcher, branch `expansion-0.3.0`, version 0.3.1.
- Task given: a 7-part polish pass (baseline, 36 boss trophies, quest book, exploration/loot, shaders/effects, stutter, release).
- Tooling in repo: `scripts/horizon.py` (QA CLI, untracked at session start), 5 skills in `.claude/skills/horizon-*`, generators in `scripts/`.
- Machine: Windows 11, Ryzen 5 9600X, 32 GB, RTX 5070. Game files: `%APPDATA%\PrismLauncher\instances\`. QA work dir: `C:\ph-work` (short path, see "Environment gotchas").
- The user's own Prism instances (0.3.1 etc.) were not modified. A new disposable instance `ProjectHorizon-QA` (177 mods) was built for all client tests.

## 1. Baseline

- `python scripts/horizon.py qa loot` (real headless dedicated server, `tests/server_smoke.txt`): finished, 4 loot audits ran. Only load errors are the known harmless `wares:` loot tables (KNOWN_ISSUES #4), a Sculk Sensor message, and an incendium smithing recipe that falls back to vanilla.
- First attempt failed because the repo path is >260 chars, Java couldn't open the relative `@win_args.txt`. Fix: `PH_WORK` env override so QA files live at `C:\ph-work` (added to horizon.py).
- NOT done: the full "record exact active mods/settings/world overrides" baseline document; Immersive Portals and its two companions were not touched (they are not in the pack).

## 2. Trophies (36 boss trophy blocks)

- Symptom (user screenshots): held item, inventory/EMI and Heracles quest nodes showed the magenta/black missing-texture cube.
- Root cause (confirmed by decompiling KubeJS 2101.7.2-build.381 `BlockBuilder.generateBlockModels`): when a block has BOTH `.parentModel(...)` and a custom shape (`.box(...)`), KubeJS also appends an element for the box whose faces use texture variables that don't exist, so an untextured cuboid is drawn.
- Fix: `scripts/gen_assets.py` now emits `.modelGenerator(mg => { mg.parent('horizon:block/trophy_base'); mg.textures({base:..., emblem:...}) })` instead of `.parentModel().textures()`. The model generator hook returns before the box element is added; `.box(2,0,2,14,15,14)` is kept so collision/selection shape is unchanged. Regenerated `kubejs/startup_scripts/horizon_items.js` (all 36 trophies). Registry IDs unchanged.
- VERIFIED by the user's screenshots in the QA instance: placed Sun Spirit trophy (pedestal + sunburst plaque, correct selection box), EMI/creative list showing all trophies, Heracles Hall of Legends nodes showing trophy icons.
- NOT done: art pass (Yeti/Sun Spirit/Ignis pilot then all 36; user said the models are "sub par" and told me to defer it), real boss-kill first-win reward test, second-kill duplicate check, Yeti/Underworld Knight intro invulnerability check. The `qa trophies` fixture itself never produced logic results (see Environment gotchas, `global` was read-only).

## 3. Quest book

Edits in `scripts/gen_quests.py` and `scripts/audit_quests.py`:
- Copy: the repeated "Why it matters" line replaced by `&aDo:&r` (action) and `&6You get:&r` (payoff). Atlas payoffs come from each family's signature reward; legend payoffs name the reward ("Starforged Heart + trophy, first kill only" / "Ancient Core + trophy"); trial payoff states gear/gems/XP, no relics. Welcome quest: removed the leftover 0.3.0 changelog paragraph; Check task, Timber unlock, IDs, prerequisites, retroactive credit unchanged. Auditor now requires "Do:" and "You get:".
- Layout: new `layout(chapter, quests)`. Hall of Legends: 8 realm rows (`REALMS` table: Overworld/Vanilla, Cataclysm Nether+End, Cataclysm Sea/Sand/Ruins, Aether, Mowzie, BOMD, Block Factory, other), Curator quest at the bottom; the generator asserts every boss is in exactly one realm. Atlas: clusters by destination (`ATLAS_GROUPS`), exchange/gem/salvage quests to the side. Mastery: build row, then trials in a grid, gem bench to the side. All other chapters: longest prerequisite chain stays on row 0 (main path), side quests below.
- Result: 143 quests in 13 chapters regenerate, auditor "143 audited, 0 problems", same file names/IDs as before (git shows only modifications), no overlapping node positions (checked per chapter).
- Installed into `ProjectHorizon-QA`. NOT checked in the client: centring, zoom, clicking, locked nodes, popups, reward claims, small/large GUI scales. Hall of Legends is ~514 units tall.

## 4. Loot and exploration

- Audit finding: `manifests/loot_report.json` lists 106 placed-but-unassigned loot tables; 80 of them are referenced by structure templates (mostly village houses/shops from other mods) but defined in NO installed jar, so those chests roll nothing. (5 `wares:` tables exist but fail to parse; skipped.)
- Fix: `scripts/gen_datapack.py::emit_fallbacks()` writes 75 fallback tables in the missing ids' namespaces, each pointing at `horizon:fallback/{house,pantry,scholar,arms}` (vanilla items + 12% Wayfarer Shard chance). Counts: house 43, pantry 13, scholar 10, arms 9. Generators and auditors pass; a headless loot run on seed `horizon-qa-2` loaded them with no parse errors. NOT verified by opening a real village chest.
- Structure placement: `/locate structure #horizon:family/<family>` on seed `horizon-qa-3` gave nearest distances: settlement 192, roadside 48, underground 260, temple 0, arcane 215, ocean 742, boss_lair 136, landmark 4031 blocks (hive isn't an Overworld family). Landmark on seeds 4 and 5: 3273 and 1924. Fix: `dungeons_arise:major_structures` spacing 60/44 -> 44/30 in `STRUCTURE_SETS` of gen_datapack.py. After: 734 / 3757 / 1627 (mean -34%, seed 4 got worse). Three seeds is thin evidence.
- Route probe (`tests/route_progression.txt`, `LOCATEAUDIT`): only 6 of 8 audits printed, last one mixed; distances for individual structures: bathhouse 1553, ruin_town 1794, creeping_crypt 2451, catacombs 3497, sunken_city 6736, keep_kayra 9587 blocks. Payoff conclusions were NOT drawn from it. `minecraft:village_plains` at 3660 was a bad probe (CTOV replaces those villages).
- `docs/MIGRATION.md` got a section describing the existing-save impact (new chunks only follow the denser grid; opened containers unchanged).
- NOT done: relic/token/salvage stage review, recipe-gate audit, Apotheosis/Simply Swords chase-loot tie-in, content additions, client playthroughs of early/mid/late routes (what the player buys/unlocks), migration test on copied saves, full loot audit re-run after the landmark change.
- New test files: `tests/route_progression.txt`, `tests/route_families.txt`, `tests/route_landmark.txt`.

## 5. Shaders / effects

NOT STARTED. No Solas-vs-off screenshots, no river view at 220,69,-832, no fog isolation, no particle sprite work, no shader preset changes. (A Solas perf run exists, see below, but it measured frame times only.) The user's own screenshot at 220,69,-832 showed the night river view with shaders on and the Atmospherics-era look; no analysis was done.

## 6. Performance / stutter

Built a recorder (`python scripts/horizon.py qa perf`): launches the QA game, uses a fixed seed (`horizon-qa-shaders-1`) and `tests/qa_route.json` (4 waypoints, 30 s dwell, creative, day, clear), records client frame gaps (RenderFrameEvent via KubeJS NativeEvents) and integrated-server tick gaps between `HQA-START`/`HQA-END` chat markers. Options: `--shader off|name --voxy-radius N --voxy-tasks N --dwell T --fresh --pregen --label`. Results append to `C:\ph-work\perf_results.jsonl`. Clock is KubeJS `Utils.getSystemTime()` (1 ms resolution; `java.lang.System` is blocked by the KubeJS class filter).

Results (one run per row, fresh world copy, cold Voxy data in the world folder, shaders off unless stated):

| Config | Frame p50/p95/p99 ms | Frames >50 ms (max) | Tick-gap p95/p99/max ms |
|---|---|---|---|
| Voxy WG r128 / 6 tasks (current default) | 7 / 22 / 34 | 59 (163) | 75 / 203 / 9499 |
| r128 / 2 tasks | 7 / 21 / 33 | 36 | 75 / 153 / 6205 |
| r64 / 2 tasks | 7 / 20 / 32 | 38 | 68 / 222 / 6016 |
| Solas, r128 / 6 | 10 / 28 / 37 | 26 (10,625 frames vs 13,466) | 73 / 243 / 10911 |
| Chunky pre-generated area, r128 / 6 | 8 / 27 / 43 | 66 (2798) | 75 / 210 / 1744 |

- No config met the target (25% lower p99 or half the frames >50 ms); no defaults were changed. Differences of ~10% are inside unmeasured run-to-run noise.
- IMPORTANT correction: the "ticks over 50 ms" count in the results file is NOT meaningful. The tick metric is the gap between tick events, so a healthy 20 TPS server reads ~50 ms and ~800 of 2400 "ticks" count as >50. Earlier I wrongly said ~31% of ticks were slow. Only p95/p99/max are interpretable. A better metric would count gaps above ~60-75 ms and store a histogram.
- Chunky experiment: user approved downloading `Chunky-NeoForge-1.4.23.jar` (340,572 bytes, sha512 verified against Modrinth). It was installed ONLY in a throwaway QA server folder `C:\ph-work\qa-server-chunky` (real copy of mods + Chunky), pre-generating x -700..900, z -500..900 (8,989 chunks, 4:24, ~34 c/s) from `tests/pregen.txt`. Chunky is not in the pack, instance, or lock. Effect: worst tick gap 9.5 s -> 1.7 s (the big stalls are on-arrival chunk generation), but p95/p99 tick gaps unchanged and frames slightly worse (one 2.8 s hitch, possibly Voxy ingesting existing chunks; unconfirmed). Not shippable as a per-world step.
- Documented in `docs/PERFORMANCE.md` (two new sections).
- NOT done: repeat runs for noise, warm-Voxy run, river/village/factory scenes, boss/factory scene, time until horizon fills, Streams Reflowing toggle (KNOWN_ISSUES #11 flags its per-chunk precompute), simulation/render distance tests, Voxy WG disabled entirely, particles/Flywheel profiling, spark profiles. The routine tick jitter (p95 ~70-75 ms) is unexplained.

## 7. Release

NOT STARTED: no generator full-run via `build_all.py`, no `.mrpack`, no fresh Prism QA import, no new-world/migrated-save/boss-reward/quest-claim/expedition/dimension-travel/save-reopen checks, no before/after screenshots, no changelog.

## Files changed in the repo (all uncommitted; many staged)

- `scripts/gen_assets.py` (trophy model hook), `kubejs/startup_scripts/horizon_items.js` (regenerated)
- `scripts/gen_quests.py`, `scripts/audit_quests.py`, `config/heracles/quests/**` (143 regenerated files)
- `scripts/gen_datapack.py` (fallback loot tables, landmark spacing), `datapacks/**` (regenerated, includes `dungeons_arise/worldgen/structure_set/major_structures.json` and 75 new fallback tables)
- `scripts/horizon.py` (heavily edited QA tooling: PH_WORK, relative-path fix, loot harness reads the server's own log and ignores known noise, `qa perf`, `--pregen`, game detection = any javaw process, experimental-settings pre-accept, world template cache), `tests/*.txt` new route/pregen files
- `docs/MIGRATION.md`, `docs/PERFORMANCE.md`

## Environment gotchas learned (useful for whoever continues)

- Repo path > 260 chars: use `PH_WORK='C:\ph-work'` and `PH_SERVER=~/.cache/project-horizon/server-expansion` (env vars do NOT persist between tool calls; set them on every call).
- Prism only reads its instance list at startup. A new instance requires restarting Prism (the user approved closing it once).
- Prism launches Java with an argument file, so the process command line does not contain the instance name; the old "is it running" check false-positived a crash after 90 s.
- KubeJS 7: `global.x = ...` is read-only in scripts, `java.lang.System` is class-filtered, `ClientEvents.chatReceived` doesn't exist (use `NativeEvents.onEvent(Java.loadClass('net.neoforged.neoforge.client.event.ClientChatReceivedEvent'), ...)`). The trophy and route fixtures in horizon.py used `global.hqaRan` and never ran; this was fixed for the perf path (script-local variables).
- An unfocused window pauses the integrated server ("Saving and pausing game"): QA options.txt now sets `pauseOnLostFocus:false`.
- Fresh modded worlds trigger the "Worlds using Experimental Settings" dialog; the harness now flips the NBT byte `confirmedExperimentalSettings` to 1 in the QA world copy.
- `server_test.py` WAITLOG patterns cannot contain spaces (it splits on whitespace).
- Voxy stores LOD data in `saves/<world>/voxy`, so deleting the world copy gives cold Voxy.
- Stopping a background task does not stop its child processes: two test matrices once ran at once.

## Process mistakes to know about

- A cleanup command with too broad a process filter killed several `bash.exe` shells (my own tool shells and stuck test copies). No user app was knowingly affected.
- Early perf runs were invalid (paused server, wrong clock, markers not synced, client event missing) and were discarded; only the table above is valid.
- Prism Launcher (user's app) was closed and reopened once with the user's approval; QA games were launched/killed repeatedly with `taskkill javaw.exe`.
