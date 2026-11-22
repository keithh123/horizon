# Building Project Horizon from source

Requires Python 3.11+, Java 21 (for the test server) and network access for `resolve.py` / jar downloads.
Jar downloads are cached in `~/.cache/project-horizon/jars` (override with `PH_CACHE`).

## One command

```
python scripts/build_all.py            # full pipeline, twice, and fails unless the second run changes nothing
python scripts/build_all.py --mrpack   # ...then dist/ProjectHorizon-<version>.mrpack
```

`--offline` skips `resolve.py`; `--no-configs` skips `patch_configs.py` (which needs a dev instance that has launched once).

## Pipeline and file ownership

Every generator owns a disjoint set of outputs and deletes **only** what it owns. In 0.1.0, `patch_configs.py`
deleted the whole `config/` directory (taking the quest book in `config/heracles` with it) and `gen_datapack.py`
deleted the whole `datapacks/` directory (taking the structure tag written by `gen_quests.py` with it). Both are fixed.

| Step | Reads | Owns (writes / may delete) |
|---|---|---|
| `resolve.py --frozen` | `manifests/roster.json` | `manifests/lock.json` |
| `check_deps.py` | lock + every jar's `neoforge.mods.toml` (incl. jar-in-jar) | `manifests/deps_report.json` |
| `index_ids.py` | jars | `manifests/ids.json` (lang/model/data inferred - a validation aid, not runtime proof) |
| `audit_loot.py` | jars (structure `.nbt`, loot tables, processors, GLMs) | `manifests/loot_audit.json` |
| `gen_assets.py` | `manifests/legends.json` + item table in the script | files listed in `kubejs/.generated-assets.json` (textures, trophy model, lang, `startup_scripts/horizon_items.js`, `startup_scripts/horizon_data.js`, `client_scripts/horizon_tooltips.js`) |
| `gen_datapack.py` | `loot_families.json`, `legends.json`, `expeditions.json`, `loot_audit.json`, `loot_calibration.json`, ids | files listed in `datapacks/.generated.json`; `manifests/loot_report.json`, `manifests/salvage_report.json`, `docs/LOOT_BUDGET.md` |
| `gen_quests.py` | families, legends, expeditions, generated datapack/asset manifests, ids | `config/heracles/quests/`, `config/heracles/groups.txt` |
| `patch_configs.py` | dev instance configs (`PH_INSTANCE`, default `ProjectHorizon-dev`) | exactly the files in its `EDITS` table; `manifests/config_changes.md` |
| `gen_profiles.py` | `profiles/*.json`, shader zips | `profiles/shader_options.json` |
| `gen_docs.py` | lock, roster | `docs/MODLIST.md` |

Hand-written sources that no generator touches: `kubejs/server_scripts/horizon_events.js`,
`kubejs/server_scripts/horizon_recipes.js`, everything in `manifests/*.json` that is listed as an input above,
`profiles/*.json`, `profiles/apply-profile.ps1`, `profiles/effects.json`, `options/options.txt`, `tests/*.txt`.

## Validation layers

1. **Static:** `check_deps.py` evaluates every Maven version range FML would see (not just "project present").
   `gen_datapack.py`/`gen_quests.py` abort on unknown ids, missing Apotheosis gems, a quest reward that would
   complete another quest's item task, or any structure whose expected relic yield exceeds the hard ceilings.
2. **Runtime (headless):** `scripts/server_test.py <server_dir> <world> <seed> tests/server_smoke.txt` boots the
   dedicated server, reports every loot-table/recipe/KubeJS parse error, rolls tables, places real structures and
   audits their containers with `/horizon audit`.
3. **Calibration:** `tests/calibration.txt` + `scripts/calibrate.py` measure real container counts of placed
   structures (jigsaw repeats included) into `manifests/loot_calibration.json`, which the budget solver then uses.
4. **Client / gameplay:** see `docs/VALIDATION_REPORT.md` for what was played by hand and what was not.

## Test instances

- `python scripts/build.py instance --name ProjectHorizon-expansion` builds/updates a Prism instance. Updating an
  existing instance removes stale pack-owned files (old loot modifiers, scripts, quests) but never touches saves,
  `options.txt` or configs the pack does not ship.
- `scripts/smoke.sh` launches only `$PH_INSTANCE` and no longer kills other Java processes (see the script).
- `python scripts/gen_portal_guards.py [--jar immersive_infinity.jar]` regenerates `datapacks/immersive_infinity/` (owned, listed in
  `datapacks/.generated-portal-guards.json`); not part of `build_all.py` because Immersive Infinity is not in the roster.
- `python scripts/patch_micimmptl.py <orig.jar> <patched.jar>` disables the Voxy mixins of Make it Compatible: Immersive Portals
  (incompatible with Voxy 0.2.16-beta). Instance-only: the add-on is not shipped.
