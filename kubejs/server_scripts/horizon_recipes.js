// Project Horizon - recipe integration.
// Design rules (docs/PROGRESSION.md):
//  * Exploration relics gate a handful of *milestone* machines, never basic tools.
//  * Each gate costs 1 relic per milestone block, not per component, to avoid grind.
//  * Relics have sinks back into RPG itemization so exploration stays rewarding late.

ServerEvents.recipes(event => {
  const SHARD = 'horizon:wayfarer_shard'
  const CORE = 'horizon:ancient_core'
  const HEART = 'horizon:starforged_heart'

  // --- Travel: waystones must be *found*; personal warp stones need a shard.
  event.remove({ output: 'waystones:warp_stone' })
  event.shaped('waystones:warp_stone', ['DSD', 'EGE', 'DED'], {
    D: 'minecraft:amethyst_shard', S: SHARD, E: 'minecraft:ender_pearl', G: '#c:gems/emerald'
  }).id('horizon:waystones/warp_stone')

  // --- The Digital Age: an ME controller needs one Ancient Core.
  event.remove({ output: 'ae2:controller' })
  event.shaped('ae2:controller', ['aba', 'bcb', 'aqa'], {
    a: 'ae2:smooth_sky_stone_block', b: 'ae2:fluix_crystal', c: 'ae2:engineering_processor', q: CORE
  }).id('horizon:ae2/controller')

  // --- Late game storage: 256M MEGA component needs a Starforged Heart.
  event.remove({ output: 'megacells:cell_component_256m' })
  event.shaped('megacells:cell_component_256m', ['aba', 'cdc', 'aha'], {
    a: 'ae2:matter_ball', b: 'megacells:accumulation_processor', c: 'megacells:cell_component_64m',
    d: 'ae2:quartz_vibrant_glass', h: HEART
  }).id('horizon:megacells/cell_component_256m')

  // --- Fusion: both fusion lines need a Starforged Heart (one per reactor).
  event.remove({ output: 'mekanismgenerators:fusion_reactor_controller' })
  event.shaped('mekanismgenerators:fusion_reactor_controller', ['CGC', 'FTF', 'FHF'], {
    C: '#c:circuits/ultimate', G: '#c:glass_panes', F: 'mekanismgenerators:fusion_reactor_frame',
    T: 'mekanism:basic_chemical_tank', H: HEART
  }).id('horizon:mekanism/fusion_reactor_controller')

  event.remove({ output: 'modern_industrialization:fusion_reactor' })
  event.custom({
    type: 'modern_industrialization:assembler', duration: 200, eu: 8,
    item_inputs: [
      { amount: 6, item: 'modern_industrialization:fusion_chamber' },
      { amount: 1, item: 'modern_industrialization:quantum_machine_hull' },
      { amount: 2, item: 'modern_industrialization:quantum_circuit' },
      { amount: 1, item: HEART }
    ],
    item_outputs: [{ amount: 1, item: 'modern_industrialization:fusion_reactor' }]
  }).id('horizon:mi/fusion_reactor')

  // --- Ore unification: Powah uraninite comes from Mekanism uranium
  //     (Powah's own ore generation is disabled in the datapack).
  event.smelting('powah:uraninite', 'mekanism:raw_uranium').xp(0.7).id('horizon:powah/uraninite_smelting')
  event.blasting('powah:uraninite', 'mekanism:raw_uranium').xp(0.7).id('horizon:powah/uraninite_blasting')

  // --- Relic sinks into Apotheosis itemization (exploration -> better gear).
  event.shapeless('2x apotheosis:sigil_of_socketing', [CORE, 'apotheosis:gem_dust', 'apotheosis:gem_dust'])
    .id('horizon:apotheosis/socketing_from_core')
  event.shapeless('apotheosis:sigil_of_enhancement', [HEART, 'apotheosis:gem_dust'])
    .id('horizon:apotheosis/enhancement_from_heart')
  event.shapeless('4x apotheosis:gem_dust', [SHARD, SHARD, SHARD, SHARD])
    .id('horizon:apotheosis/gem_dust_from_shards')

  // --- Relic sinks into magic.
  event.shapeless('irons_spellbooks:epic_ink', [CORE, 'minecraft:glass_bottle', 'minecraft:ink_sac'])
    .id('horizon:irons/epic_ink_from_core')
  event.shapeless('irons_spellbooks:legendary_ink', [HEART, 'minecraft:glass_bottle', 'minecraft:ink_sac'])
    .id('horizon:irons/legendary_ink_from_heart')

  // --- Storage QoL reward for deep exploration.
  event.shaped('sophisticatedbackpacks:stack_upgrade_omega_tier', ['S4S', '4C4', 'S4S'], {
    S: SHARD, '4': 'sophisticatedbackpacks:stack_upgrade_tier_4', C: CORE
  }).id('horizon:backpacks/omega_stack_upgrade')

  // --- 0.5 magic bridge: Iron's arcane essence and Ars source gems convert 1:1 (no net gain: the lapis/amethyst is the fee),
  //     so a caster who explores for one mod's drops can use them in the other.
  event.shapeless('2x ars_nouveau:source_gem', ['irons_spellbooks:arcane_essence', 'irons_spellbooks:arcane_essence', 'minecraft:lapis_lazuli'])
    .id('horizon:magic/essence_to_source')
  event.shapeless('2x irons_spellbooks:arcane_essence', ['ars_nouveau:source_gem', 'ars_nouveau:source_gem', 'minecraft:amethyst_shard'])
    .id('horizon:magic/source_to_essence')
})
