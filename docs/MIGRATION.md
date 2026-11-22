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
