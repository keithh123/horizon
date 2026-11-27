# Updating a 0.6.0 instance to 0.6.1 (visual repair)

**Back up first** (the reference PC's update made `C:/Users/Starl/HorizonBackups/ProjectHorizon-0.6.0_2026-11-26_pre-visual-repair`).
No world data, quest id, ledger field or registry id changes. Run `python scripts/build.py instance --name ProjectHorizon-0.6.0`
with the game closed:

- Kept: instance name/UUID/Java/memory (`instance.cfg`), every `options.txt` key except the ones below, your shader choice
  (`config/iris.properties`), jars you added yourself, resource packs you enabled yourself (they stay on top).
- Changed in `options.txt`: `renderDistance` raised to 8 if it was lower; the Horizon pack list and order; Mandala's GUI added
  to `incompatibleResourcePacks` (packs you had accepted there stay).
- Mods: First-person Model, Not Enough Animations and FPM x Compat are enabled (their `.disabled` copies are removed); Entity
  Player Compat and Modefite are added; Punchy! Moves and Weather Glass are removed.
- Existing headquarters: unchanged. A charter that never answered in 0.6.0 now opens its panel on right-click.

# Migrating a 0.5 world to 0.6 (headquarters campaign)

**Back up the world first.** 0.6 adds 8 mods (5 content, 3 disabled first-person jars) and one resource pack (not enabled);
no mod was removed or upgraded, no terrain provider changed, no registry id was renamed.

1. Import `ProjectHorizon-0.6.0.mrpack` as a new Prism instance (recommended) and copy `saves/<world>` across, or update in
   place (Prism: Import/Update from the mrpack). Do not copy `kubejs/` or `config/heracles/` from the old instance.
2. On first login each player receives one **Founding Kit** (existing players too). Unpack it, place the Survey Charter where
   your base already is, and click **Found a headquarters here**.
3. **Legacy commissioning path:** everything already achieved counts. Location, boss, realm, trial and machine advancements
   are read retroactively, so a 0.5 base usually satisfies most requirements at once. What still has to be done by hand:
   the room checks (blocks at the station), the receipts (press four Survey Plates; enriched iron / energized steel / MI
   steel for the Foundry route) and the stage contributions. There is no automatic grant of stages for old saves: that would
   be an unverified claim of a working workshop.
4. Quest ids from 0.5 are unchanged (214 of 214); the old `0 - The Horizon Campaign` chapter is now labelled
   `0b - The Expedition Road (branch)` with the same folder and ids, so progress is kept. 19 new quests form the
   `0 - Headquarters Campaign` spine.
5. Existing machines keep working: 0.6 adds no recipe locks or item-use restrictions.
6. The Terrain Diffusion (Windows) local variant and its worlds are not touched by the portable pack; keep using that
   instance for those worlds.

Ledger versioning: `horizon_hq` carries `v` (ledger version) and each headquarters its own `v`; `migrateHq` only ever adds
missing fields and never drops stages, options or facts. Unreadable records are left untouched in NBT and logged.

# Migrating a 0.1.0 world to 0.2.0

**Back up the world first** (copy `saves/<world>` somewhere safe). Nothing in 0.2.0 deletes or regenerates
terrain, but you are adding four mods to an existing save.

## Recommended: a new Prism instance

1. Import `ProjectHorizon-0.2.0.mrpack` as a **new** instance (keep the 0.1.0 instance as it is).
2. Copy `saves/<world>` from the 0.1.0 instance into the new instance's `minecraft/saves/`.
3. Optional: copy `options.txt`, `config/xaero*`, `XaeroWaypoints`, `xaero/` if you want your keybinds/waypoints.
   Do **not** copy `kubejs/` or `config/heracles/` - those are pack-owned and changed.
4. Open the world once, let it save, quit, and keep the backup until you have played a session.

Updating the 0.1.0 instance in place also works (Prism: Edit instance -> Version -> Import/Update from the mrpack),
but then delete `minecraft/kubejs/data/horizon/loot_modifiers/` first: 0.1.0's loot modifier files are no longer
referenced, but removing them keeps the folder honest.

## What applies to an existing world

| Change | Existing world | Needs new chunks? |
|---|---|---|
| Relic budgets, regional tokens, charts, Apotheosis family entries | **Unopened** containers roll the new tables when first opened | No |
| Containers already opened in 0.1.0 | Keep what they had - loot is rolled once | - |
| Lootr per-player containers | Lootr converts vanilla-style loot containers **with a loot table still attached** (i.e. unopened) when their chunk loads; opened ones stay normal chests | No |
| Boss first-kill relic + trophy (`horizon:legend/*`) | Works for kills from now on. Kills you made in 0.1.0 are not remembered by the new advancements, so you can earn each once more | No |
| Quest book corrections and new chapters | Applied on load. Quests whose task is now an advancement check your existing advancements when they unlock | No |
| Expedition Atlas quests (`horizon:atlas/*`) | Complete the next time you step into a structure of that family | No |
| Exchange, salvage and Trial recipes | Immediately | No |
| Gateways to Eternity Trials, Corpse | Immediately | No |
| Subtle Effects, profile changes | Client-side, immediately | No |
| Structure spacing (unchanged from 0.1.0) | - | - |

0.2.0 adds no new structure mods and does not change biome or structure placement, so already generated terrain
and newly generated terrain match: there are no seams.

## If you held relics from 0.1.0

They stay valid. 0.1.0 gave far more Starforged Hearts from large structures (see `docs/LOOT.md`); nothing takes
them away. If your world already has a large surplus, the Trials and the enhancement sigil recipe are the intended
sinks.

## Rolling back

Restore the world backup into the 0.1.0 instance. Do not open a world that has been played in 0.2.0 with 0.1.0:
Lootr chests, trophies, tokens and Corpse entities would be lost (unknown blocks/items are removed on load).

## 0.2.0 -> 0.3.0

- Existing 0.2.0 worlds load (the test world was generated without the expansion and opened with it).
- **New chunks only:** Streams Reflowing rivers, Grim Kingdoms, Homesteads, Moog's Mineshafts, Bosses of Mass
  Destruction, Bosses' Rise, Companions and Spider Overhaul structures, Primal animals' biome spawns. Already generated
  terrain keeps its old structures; explore new regions (or a new world) to find them.
- SnowyLeavesPlus adds a `snowiness` property to vanilla leaves (default none): old saves load unchanged; removing the
  mod later returns leaves to their normal state.
- Not included on purpose: Infinity Cave and Blooming Biosphere would rewrite the overworld height/terrain of existing
  saves (see docs/EXPANSION_CHECKLIST.md).
- Back up worlds first; the update replaces pack-owned folders (kubejs data, quests) as before.

## 0.3.2 candidate: worldgen and loot changes (existing saves)

- `dungeons_arise:major_structures` spacing 60/44 -> 44/30. Chunks already generated keep their structures; only newly generated
  chunks use the denser grid, so a migrated world can show two landmark densities (and rarely two landmarks closer than before).
  Measured nearest landmark from spawn on 3 fresh seeds: 4031/3273/1924 blocks before, 734/3757/1627 after (mean -34%, one seed worse).
- 75 village-house and shop loot tables that no installed jar defined (their chests were empty) now exist as small themed
  tables (`horizon:fallback/*`, with a 12% Wayfarer Shard chance). Containers already opened stay as they are.
