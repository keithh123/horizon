// Project Horizon - the physical quest book (heracles:quest_book, right-click opens the same screen as J).
// Craftable (book + compass) and given once per player on their first login after 0.3.1 (existing saves included).
// Hand-written; no generator touches this file.
ServerEvents.recipes(event => {
  event.shapeless('heracles:quest_book', ['minecraft:book', 'minecraft:compass']).id('horizon:quest_book')
})

PlayerEvents.loggedIn(event => {
  const p = event.player
  if (p.persistentData.getBoolean('horizon_book_given')) return
  p.persistentData.putBoolean('horizon_book_given', true)
  if (p.inventory.countItem('heracles:quest_book') === 0) p.give('heracles:quest_book')
})
