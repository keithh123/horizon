# 0.6 baseline and mod decision ledger

Recorded 2026-11-26 on branch `claude/new-session-5zbr2u`, starting from `56efa14` (0.5.0). Environment: Linux container,
4 vCPU, 15 GB RAM, OpenJDK 21.0.13, Python 3.13, Node 22. **No graphical client and no second player were available**:
every client/visual/multiplayer item below that needs one is marked *unverified*, never *passed*.

## 1. Snapshot claims rechecked

| Claim (prompt snapshot) | Checked | Result |
|---|---|---|
| MC 1.21.1, NeoForge 21.1.267, Java 21, source 0.5.0 | `manifests/lock.json`, `VERSION` | confirmed |
| 245 lock entries incl. disabled Clavis | lock | confirmed (Clavis `disabled_by_default`); 0.6 lock: **253** (+8, see §3) |
| 11 port-lock entries, some variant-only | `manifests/ports_lock.json` | confirmed: 11; `infinitycave` (depths), `modelangles`, `snugfire` (lab) are variant-only; 6 client-only |
| 214 generated quests | `gen_quests.py` run | confirmed 214 in 16 chapters; 0.6: **233 in 17** (all 214 ids kept, byte-identical except chapter label) |
| Reference instance: 259 active jars, 3 renamed-but-identical | not available here (Windows Prism instance) | **not rechecked** - no access to the instance |
| 7 instance-only jars | Modrinth search (jars themselves not available) | Terrain Diffusion is on Modrinth as `neoterrain-diffusion` (server-side worldgen, MIT); byepregen, dtarsnouveau, lootrcorrectif, mobdismembermentneoforge, unium, RU Expansion have **no Modrinth NeoForge 1.21.1 listing** - they stay `instance_only` (manual). Jar metadata inspection *not performed* (jars absent). |
| Balanced profile = Complementary Reimagined r5.9.3 | `profiles/balanced.json` | confirmed (MEDIUM). Performance = none, Cinematic = Complementary Unbound HIGH |
| Fresh Compats excluded because Quark/Supplementaries absent | roster | **stale**: Quark 4.1-488 and Supplementaries 4.1.4 are in the lock. Re-decided in §3. |

## 2. Source-versus-build discrepancies found (and what was done)

1. **Committed generated data was built from a partial jar index.** The committed `ids.json` lacked ids from Ad Astra, Aether
   Villages, Adorabuild and others (11 528 items vs 17 262 from the actual lock). Regenerating from the real lock changes a
   handful of loot-injection rows, drops 5 MVS fallback tables the jars now define, and grows `placed_but_unassigned`. All
   budget ceilings still pass. Outputs were regenerated from the locked jars; this is the correct state.
2. **CRLF vs LF.** Generated files were committed from Windows with CRLF; Linux regeneration writes LF, so every generated file
   "changed". Added `.gitattributes` (`* text=auto eol=lf`, binaries marked) so the repository is EOL-stable across platforms.
3. **The dedicated server could not boot.** Client-only mods whose Modrinth side metadata is not `unsupported` were shipped to
   servers. Controlify crashed mod construction; further client-only mods were found by booting repeatedly. Each now carries a
   roster `side` override (`server: unsupported`) with the reason; see the `0.6: client-only` notes in `manifests/roster.json`
   and VALIDATION_REPORT §Server.
4. **Cue subtitles existed only in the optional Horizon-16x pack.** With the pack off, players saw raw keys. They are now also in
   the KubeJS lang (gen_assets.py).
5. **Server tooling was Windows-only** (`run.bat`, `win_args.txt`). `build.py server` and `server_test.py` now work on Linux too.
6. README claimed "248 mods" and a stale pack filename; updated.

## 3. Mod decision ledger (0.6)

Side: C = client, S = server. Evidence column names what was actually checked.

| Mod | Version (Modrinth id) | Side | Decision | Campaign role | Evidence |
|---|---|---|---|---|---|
| Construction Sticks | 1.5.0 (`5dwDOCYP`) | C+S | **add** | Copper stick (Outpost), iron (Workshop), diamond + replacement template (Foundry) | jar toml: neoforge [21.1.1,), mc [1.21,1.22); MIT. Config: STARTUP type; shipped `config/constructionstick-startup.toml` forbids placing block-entity blocks (no container content edge cases). Charging/undo behaviour: mod default; *client use unverified*. |
| FramedBlocks | 10.6.3 (`5g0Yxvfb`) | C+S | **add** (the one shape system) | Roofs, beams, observatory frames | jar toml: neoforge [21.1.205,), optional Create [6.0.2,). LGPL-3.0. `allowBlockEntities` defaults **false** (bytecode), kept. Copycats+ not added (one shape system). *Shader/culling unverified.* |
| Handcrafted | 4.0.3 (`JfqnpP2Z`) | C+S | **add** | Inhabited interiors | requires resourcefullib [3.0.0,) - lock has 3.0.12. Terrarium licence; referenced from Modrinth, never bundled. |
| Create Deco | 2.1.3 (`qrcMVoBD`) | C+S | **add** | Workshop/Foundry industrial language | **jar** declares `create [6.0.7,6.1.0)` (Modrinth lists no dependency) - Create 6.0.10 satisfies it. MIT. |
| Comforts | 9.0.5+1.21.1 (`3kpPjcTc`) | C+S | **add** | Expedition sleeping that keeps the HQ respawn | bytecode: `ComfortsEvents.canSetSpawn` cancels `PlayerSetSpawnEvent` for its beds, so the headquarters spawn survives. Jar-in-jar spectrelib. *Seamless Sleep interplay in game unverified.* |
| Fresh Compats (resource pack) | v1.6 (`EHQK5l1g`) | C | **add, not enabled** | FA support for Quark/Supplementaries | needs EMF+ETF (in pack). Ships in `resourcepacks/` but is not switched on (`enabled_by_default: false`): no visual check of its Quark bee variants against Dynamic Trees/EMF was possible. FA Player Extension stays excluded (Punchy Moves conflict). |
| First-person Model + Not Enough Animations + FPM Compat | 2.7.3 / 1.12.7 / 1.2.1 | C | **optional preset, ships disabled** | First-person body | jar tomls: client; FPM Compat requires cloth_config (in pack) and firstperson. The Punchy!/Better Combat/spellcasting matrix could not be run, so the three jars ship as `.disabled`. |
| AStages | 2.5.3 (`ZkTlq92y`) | C+S | **defer** | - | ARR. The headquarters ledger needs no recipe locks; stage unlocks are rewards/services. |
| Open Parties and Claims | 0.33.0 beta (`yWmXD7GW`) | S(+C) | **defer** | - | Beta; claims would need fake-player/spell/Gateways tests. HQ membership is built into the charter (invite/join/leave). |
| Exposure (+Catalog) | 1.9.21 | C+S | defer | archive photos | No NeoForge 1.21.1 client test possible; photo objectives are not in the campaign. |
| Sound Physics Remastered, Auto HUD, FancyMenu, Chipped, Rechiseled, Copycats+, Create: Connected, Interiors, Amendments, Bountiful, Patchouli | appendix pins | - | not added | - | Each needs audio/visual/UI comparison not possible here; charter panel + quest book cover onboarding; authored charter services replace Bountiful. |
| Combat Roll, Camera Overhaul, Dynamic Crosshair, LambDynamicLights, RyoamicLights | appendix pins | C | not added (experiments) | - | Ownership of camera/lighting unchanged (docs/ART_DIRECTION.md). |
| Controlify and other client-only mods (see roster notes) | unchanged versions | C | **tune**: server-unsupported | - | crashed the dedicated server at mod construction / mixin apply (logs in `tests/` evidence). |
| Clavis | 0.2.13 | - | keep disabled | - | chunk/loot-preview freeze not independently repaired. |
| Terrain Diffusion (Windows build) + RU bridge | instance only | - | keep out of the portable pack | - | Windows-only jar would break Linux/macOS and servers. |

No existing mod was upgraded or removed in 0.6. Curios 9.5.1 / Accessories Compat Layer untouched.

## 4. Implementation sequence (as executed)

1. Baseline (this file), regenerate from the real lock, EOL fix.
2. `manifests/headquarters.json` + `scripts/gen_headquarters.py` + `kubejs/server_scripts/horizon_headquarters.js`; Outpost
   and Workshop proven first (tests/hq_sim.js, then the dedicated-server FakePlayer selftest), then Hall, Conservatory,
   Foundry, Observatory through the same core.
3. Quests (`0 - Headquarters Campaign`), art masters, cues, plans (schematics), progression graph.
4. Mod batch (§3), server side fixes, packaging, docs, Graphify refresh.
