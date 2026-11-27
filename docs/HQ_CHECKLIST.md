# 0.6 completion checklist (headquarters campaign)

Status words: **done** (implemented and verified as stated), **done - unverified in client** (implemented; only static,
Node or dedicated-server evidence), **deferred** (deliberately not done, reason given), **not done**.

| # | Requirement (prompt section) | Status | Evidence / where |
|---|---|---|---|
| 1 | Baseline, snapshot recheck, discrepancies, mod decision ledger (§1) | done | docs/HQ_BASELINE.md |
| 2 | Six stages end to end, player-chosen location, founding kit, charter, plans incl. ruined-outpost restoration (§2) | done - unverified in client | manifests/headquarters.json, docs/HEADQUARTERS.md, docs/HQ_PLANS.md, schematics/ |
| 3 | Per stage: prerequisites, sources, commissioning action, contributions, expedition requirement, unlocks, physical expression, explanation, sound, solo/co-op, recovery, tests (§2) | done - unverified in client | docs/HEADQUARTERS.md (generated per stage), docs/PROGRESSION.md (state rules), tests/hq_sim.js |
| 4 | Vertical slice Outpost -> Workshop verified first | done (server fixture) | tests/evidence/server_hq_2026-11-26.txt (23/23) |
| 5 | Data-driven source + generated quests/recipes/translations/advancements; generator ownership and audits (§3) | done | scripts/gen_headquarters.py, gen_assets.py, gen_quests.py, audit_quests.py, build_all.py, horizon.py routing |
| 6 | Controller interaction showing stage, satisfied/missing, alternatives, costs, next unlock, commission action (§3) | done - unverified in client | `hqPanel` in kubejs/server_scripts/horizon_headquarters.js |
| 7 | Server authority, re-check, consume once, idempotent clicks/callbacks/reloads (§3) | done | hq_sim (double click, replay), server selftest before/after /reload |
| 8 | Processing/research/expedition proofs, documented predicates (§3) | done | `proves` text per requirement in docs/HEADQUARTERS.md; receipts list in headquarters.json |
| 9 | One canonical ledger; quests/advancements mirror it (§3) | done | impossible-criterion mirrors; audit rule "stage quests complete only on mirrors" |
| 10 | Parties: solo, distinct, membership changes, offline, late joiners, reconnect, deaths (§3) | done - two-player UX unverified | docs/PROGRESSION.md §Parties; hq_sim party tests |
| 11 | First-kill relic semantics preserved; shared milestones never pay personal relics (§3) | done | legends untouched; no relic in any HQ reward (validated) |
| 12 | Versioned persistence, admin diagnostics/recovery, relocation, broken controller, unlock vs service (§3) | done | `/horizon hqadmin`, migrateHq, restart test, selftest dormant/rebind |
| 13 | No per-tick scans, no forced chunk loads (§3) | done | docs/PERFORMANCE.md 0.6 section; code review: scans only on click |
| 14 | Stable ids, explicit migration, legacy commissioning path (§3) | done | docs/MIGRATION.md 0.6; 214/214 quest ids |
| 15 | AStages | deferred | docs/HQ_BASELINE.md §3 |
| 16 | Open Parties and Claims | deferred | docs/HQ_BASELINE.md §3 |
| 17 | Construction Sticks, FramedBlocks, Handcrafted, Create Deco, Comforts (§4) | done - unverified in client | lock.json; jar metadata in docs/HQ_BASELINE.md; config/constructionstick-startup.toml |
| 18 | Fresh Compats pilot + load order (§4) | shipped, not enabled (visual check impossible) | docs/RESOURCE_PACKS.md |
| 19 | First-person Model + NEA + FPM Compat pilot (§4) | optional preset, ships disabled | docs/ART_DIRECTION.md, lock.json `disabled_by_default` |
| 20 | Conditional/experimental candidates (§4) | deferred with reasons | manifests/roster.json `rejected`, docs/HQ_BASELINE.md |
| 21 | Structure family identities agree with quest text; home use per family (§5) | done | loot_families.json `home`, atlas quests "Brings home" |
| 22 | Progression graph, alternatives, luck bottlenecks (§5) | done | docs/HQ_GRAPH.md (build-enforced) |
| 23 | Relics never from repeatable sources; services/supply never mint relics (§5) | done | gen_headquarters validation; hq_sim static checks |
| 24 | Authored commissions instead of Bountiful (§5) | done (charter services) | services in headquarters.json |
| 25 | Loot/affix/armour balance review against encounters (§5) | not done | requires play sessions; 0.5 budgets unchanged |
| 26 | Headquarters spine as main quest chapter, branches labelled (§6) | done | config/heracles/groups.txt |
| 27 | Readable maps, no overlapping icons (§6) | done (static) | audit_quests overlap rule; rendering in client unverified |
| 28 | Original fiction told through entries/notes (§6) | done | headquarters.json `fiction`, stage `log` lines, charter chapter |
| 29 | Art direction document and original assets with editable masters (§7) | done - in-game look unverified | docs/ART_DIRECTION.md, art/horizon/*.txt |
| 30 | Shader/no-shader tuning, Voxy chain re-test, End issue (§7) | not done (no GPU); End limitation retained | KNOWN_ISSUES #1 |
| 31 | First-person/animation/camera matrix (§7) | not done (no client) | docs/ART_DIRECTION.md ownership table |
| 32 | HUD/sound family, subtitles (§7) | done - volumes unverified | gen_resourcepack.py CUES, KubeJS lang subtitles |
| 33 | Portable pack, Terrain Diffusion kept out, instance-only reconciled (§8) | done | roster `instance_only`, docs/INSTALLATION.md |
| 34 | New assets/schematics in build copy rules and ownership (§8) | done | build.py OVERRIDES `schematics`; build_all OWNED_DIRS |
| 35 | Performance profiling (§8) | not done (no client) | docs/PERFORMANCE.md 0.6 section |
| 36 | Static evidence + second full generator run byte-identical (§9) | done | 1386 owned files identical (VALIDATION_REPORT) |
| 37 | Dedicated-server boot + new world (§9) | done | tests/evidence/server_hq_2026-11-26.txt |
| 38 | Fresh Prism import (§9) | Prism import **not done**; headless install of the .mrpack verified byte-exact (client 0 problems, server set = tested set) | scripts/mrpack_install.py, VALIDATION_REPORT |
| 39 | Two-player multiplayer (§9) | not done (no second client) | - |
| 40 | Graphify refresh incl. headquarters relations + regression checks (§9) | done (9/9 tests) | scripts/horizon_graph.py `headquarters()`, tests/test_horizon_graph.py |
