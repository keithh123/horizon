// Project Horizon - exploration relics.
// These three items cannot be crafted or mass-produced. They come only from
// structure chests and bosses (see datapacks/horizon/loot_modifiers), so the
// tech tree keeps a dependency on exploring the world.
//   Wayfarer Shard   - common structures (ruins, camps, villages, small dungeons)
//   Ancient Core     - rare dungeons, dimension dungeons, mini-bosses
//   Starforged Heart - legendary structures and major bosses

StartupEvents.registry('item', event => {
  event.create('horizon:wayfarer_shard')
    .texture('minecraft:item/amethyst_shard')
    .rarity('uncommon')
    .maxStackSize(64)

  event.create('horizon:ancient_core')
    .texture('minecraft:item/heart_of_the_sea')
    .rarity('rare')
    .maxStackSize(16)

  event.create('horizon:starforged_heart')
    .texture('minecraft:item/nether_star')
    .rarity('epic')
    .glow(true)
    .maxStackSize(16)
})
