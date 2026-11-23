# Loot balance report (0.5)

Changes:
1. **Repeat drops for 19 mini-bosses** (`manifests/legends.json`: `repeat` = shard where it was empty: Slider, Valkyrie Queen, Frostmaw, Wroughtnaut,
   Umvuthi, Sculptor, Forgotten Guardian, Dead King, Cosmic Crystal, Lich, Obsidilith, Gauntlet, Void Blossom, Yeti, Sandworm, Kraken, Infernal Dragon,
   Underworld Knight, Sacred Pontiff). Intent: a reason to revisit a boss (a Wayfarer Shard, the cheapest relic) without relic inflation.
   Only emitted where the boss's own loot table exists in the jar index (some bosses had none and got no file).
   Generated via `scripts/gen_datapack.py`; first-kill Core/Heart rewards are unchanged.
2. **Quest rewards**: supplies and gem dust scaled by act (food/torches early; gem dust 8-64, diamonds, scrap late). No relics, no item that completes another quest.
3. Existing structure/boss budgets (docs/LOOT_BUDGET.md) were not changed: they are calibrated from real placed structures and capped by build-time assertions.

Not done: per-dungeon identity rewrite, Simply Swords/Apotheosis rebalance, runtime check by opening real chests. Mark all drop rates as untested in play.
