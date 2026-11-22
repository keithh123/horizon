# Changelog

## 0.3.0 (2026-11-21): expansion candidate

- 176 locked mods (+60: 51 requested native NeoForge 1.21.1 builds pinned by version id, 9 dependencies), 6 resource packs
  (Fresh Animations + official Extensions bundle, Fluid & Foolish, Vocal Villagers, Fire Rekindled, Animated Hearts) and
  7 local jars (docs/PORTS.md): Grand Teleport metadata repack, 5 source ports, Weather Glass (verbatim).
- Every audit entry has a status in docs/EXPANSION_CHECKLIST.md (62 implemented, 3 already present, 8 blocked,
  3 not ported yet, 12 FA add-ons not installed with reasons, 1 excluded by user).
- Blocked with concrete reasons: Infinity Cave and Blooming Biosphere (both replace the overworld dimension/noise
  settings owned by Terralith/Tectonic), Actually 3D Stuff (1.21.9+ model features), Cinematic Interactions and Cube
  Animals (CurseForge-only, All Rights Reserved), Soft Leaves, Tight Fire, Feur (All Rights Reserved).
- Fresh Animations: base + Extensions only. FA Player Extension/Player Compats removed after Punchy Moves reported them
  incompatible in game; F.M.R.P, Fresh Compats, Fresh Illager Mod Compats target mods Horizon does not have.
- Loot: new boss arenas join boss_lair (no Starforged Heart), homesteads/settlement, Moog's mineshafts/underground.
  Expansion structures only constrain their own loot tables, so all 0.2.0 calibrated budgets are byte-identical.
  10 new mini-tier Legends (Ancient Core + trophy); dense sets re-spaced (spider nests 8/6 -> 28/12, 3 MMR sets -> 40/20).
- Ownership configs: Cave Dust (cave dust), Footprint Particle (footprints), Swinging Lanterns (lanterns), Auto Third
  Person (elytra camera). Profiles control Better Clouds, Cozy Critters, Windy, Cave Dust, Interactive Foliage waving,
  Effectual trails and Streams Reflowing particles.
- Fixes found by testing: Visual Overhaul first-launch NPE (seed config), Grand Teleport invalid version string and
  server crash, checker quirks (Clavis/Lootr Maven ordering, More Sounds optional `forge`), patch_configs syntax/idempotency.
- Tooling: probe_expansion.py, build_ports.py, remap_intermediary.py, gen_checklist.py; server_test.py LOCATEAUDIT.
- Not changed: 0.2.0 mods' versions, calibrated loot, existing quests (10 legend quests appended by the generator), saves.


## 0.2.0 (2026-11-21)

- 116 mods (added Lootr, Corpse, Subtle Effects, Gateways to Adventure and dependencies).
- Curated reward families with per-structure relic budgets; loot budgets now use **measured** container counts from real placed structures (25 of 26 calibration structures; `minecraft:end_city` could not be measured and uses template counts).
- 133 quests in 13 chapters; 26 boss trophies and relic/token textures generated.
- Dependency checker evaluates Maven version ranges (`check_deps.py`). Subtle Effects vs Fzzy Config `0.7.7+fix1` was a false alarm in the checker's version ordering; FML accepts it (client launched). Recorded as a launch-verified exemption.
- New `profiles/effects.json` (Subtle Effects density/distance per profile); profile switching re-verified on a 0.2.0 instance (BOM-free).
- `gen_profiles.py` ignores `effects.json`; calibration is run in chunks (a single 26-structure run stalled after 10).
- Not changed: saves, mods' versions.

## 0.1.0 (2026-11-21): first playable build

- 112 mods on NeoForge 21.1.267, all resolved from Modrinth with pinned sha512.
- Voxy via Roxy + Voxy World Gen V2 + Iris + Complementary Reimagined r5.9.3.
- Terralith + Tectonic terrain; Incendium and Nullscape for the Nether and End; 18 structure mods with tier-based spacing changes.
- Exploration relics (Wayfarer Shard / Ancient Core / Starforged Heart) injected into 627 loot tables and 22 boss tables; they gate the ME controller, both fusion reactors and MEGA 256M, and feed back into Apotheosis and Iron's.
- Ore unification across Mekanism, Modern Industrialization and Powah.
- Balance changes: Simply Swords damage and loot, Apotheosis charms and boss cooldown.
- 76-quest Odyssey Quests book in 10 chapters.
- Conflict-free default keybinds; Performance/Balanced/Cinematic profiles with a switcher script.
- Dedicated server target (`build.py server`), validated headless at 20 TPS across all 9 dimensions.
- Fixes found by testing: undeclared deps (OctoLib, Iron's Lib), `.mrpack` env flags dropping 16 mods, options.txt data version.
