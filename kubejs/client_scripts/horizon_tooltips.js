// Explain where exploration relics come from, right on the item.
ItemEvents.modifyTooltips(event => {
  for (const id of ['wayfarer_shard', 'ancient_core', 'starforged_heart']) {
    event.add(`horizon:${id}`, Text.translate(`tooltip.horizon.${id}`).gray())
  }
})
