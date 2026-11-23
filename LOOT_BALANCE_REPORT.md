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

## Update (second pass): dungeon identities
`manifests/loot_families.json` family `extras` (small per-chest chances, applied by `gen_datapack.py`, ids verified at generation):
arcane: arcane essence 22% (1-3), XP bottle 10%; underground: iron 25% (2-5), diamond 3%; boss lairs: golden apple 22%, XP bottles 30% (2-5);
landmarks: diamond 10% (1-2), ender pearl 18%; ocean: nautilus shell 6%, prismarine crystals 20%; Nether: gold 28%, blaze rod 8%;
End: ender pearl 28%, chorus fruit 30%; temples: gold 20%; deep: echo shard 10%; hive: honey 30%.
Relic budgets are unchanged (extras carry no relics). Headless audits of Keep Kayra, Kisegi Sanctuary, a village and a shipwreck ran with the new tables;
rates are a first pass and untested in play. Magic bridge recipes (arcane essence <-> source gems, lapis/amethyst fee) added to `horizon_recipes.js`.
