# Changelog

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
