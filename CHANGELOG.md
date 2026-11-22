# Changelog

## 0.3.1 (2026-11-22): quest book, hats, resource pack

Honest status first: this pass was built and statically checked, and the headless server was booted and measured, but
**no client could be launched** (the desktop session had no display: GLFW "Failed to find a primary monitor"). Everything
that needs eyes or a mouse is listed as untested in docs/VALIDATION_REPORT.md.

- Quests: 143 quests kept (ids unchanged). "Timber!" was unreachable on a fresh world: the first quest waited on
  `minecraft:story/root` ("craft a crafting table"), which needs the wood Timber! asks for. It now completes on a
  Horizon `minecraft:tick` advancement (same task type, so progress saved by 0.3.0 should stay valid). Fixed: Hearty Meals
  (cooking pot) now follows Iron Will, not Sleep; Flawless Ambition pointed at the Pinnacle advancement (a duplicate of
  another quest) and is now Gem Cutter's Bench (craft the table); five titles that duplicated Hall of Legends entries
  renamed. Every quest now ends with an "Objective" and a "Why it matters" line. `scripts/audit_quests.py` checks
  placeholders, duplicate titles, prerequisites, cycles and the early-chain deadlock (part of build_all).
- Quest book UI (new local mod `horizon_questbook`, original code): inventory button below the player inventory;
  Heracles' own `heracles:quest_book` is now craftable (book + compass), rewarded by the first quest and given once to
  every player on login; one click opens quest details in a popup (description, requirements with state, unmet
  prerequisites, rewards, claim, X and Esc); every open centres the chapter on its tree; the minimap is forced off.
- Cosmetics: Simple Hats 0.4.1. Eight curated hats are quest rewards (Frostmaw, Wrought, Sun Spirit, Dragon, Dead King,
  Cataclysm Conqueror, Curator of Legends, first roadside ruin).
- Effects: rain ripples (Particle Rain owns them; Subtle Effects off), rain/snow audio (Cool Rain owns it; Particle Rain
  volume 0), footsteps/impacts (Effectual run dust and block-place effect off; Footprint Particle splash off); Better
  Combat debug hit boxes off. Reward cues are now Horizon sound events (docs/RESOURCE_PACKS.md).
- Resource packs: new original `Horizon-16x.zip`; the Fresh Animations All-Extensions bundle is replaced by Details,
  Emissive and Quivers (Objects, Spiders, Creepers, Classic Horses held back, reasons in docs/RESOURCE_PACKS.md).
- Shaders: Photon v1.4, Solas 3.9, Noble 1.9.9 and Bliss 2.1.2 added with presets (`apply-profile.ps1 -Profile balanced
  -Shader photon`). Performance stays shader-free. Bliss has no Voxy programs; the switcher warns.
- Clavis ships **disabled by default** (`Clavis-*.jar.disabled`): the lockpicking cursor bug could not be tested.
- Immersive Portals (NeoForge 6.0.7) not enabled: server side loads and ticks like the baseline, client rendering is untested.
- Build: `build.py instance` now removes only jars Horizon itself shipped, so manually added mods survive an update.

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
- Bug fix (0.2.0): Incendium function/component tables (armour-stand heads, artifacts, castle/base) were in the nether
  family; Incendium rolls them via /loot every second and Apotheosis' gem modifier threw. Excluded; only the Incendium
  castle group moves (core 0.68 -> 0.64, still under budget). Verified in game after /reload.
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
