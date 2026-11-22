// Project Horizon - server events (hand-written; boss/item data comes from the generated horizon_data.js).
//
//  1. Party credit: when a legend dies, every player within partyRadius blocks in the same dimension gets the
//     "party" criterion of horizon:legend/<boss>. The advancement (generated datapack) awards the relic + trophy
//     once per player and runs the feedback function. Kill credit alone would reward only the last hit.
//  2. Discovery feedback: the first time a player holds each Horizon item, and on later finds of rare tiers,
//     a short sound (+ particles for hearts) and an action-bar line. Tiered and throttled; ordinary finds are quiet.
//  3. /horizon fx quiet|normal  - per-player: suppress Horizon sounds/particles/titles (also hides others' boss fx).
//     /horizon audit <radius> [rolls]  (op) - roll the real loot tables of every container block entity in loaded
//     chunks around you and tally Horizon/Apotheosis rewards. Used by the validation report; never modifies blocks.

const H = global.HORIZON

function quiet(p) { return p.tags.contains('horizon_fx_quiet') }

// ---------------------------------------------------------------------------- 1. party credit
Object.keys(H.legends).forEach(id => {
  const leg = H.legends[id]
  EntityEvents.death(id, event => {
    const boss = event.entity
    const server = event.server
    if (!server) return
    let credited = 0
    server.players.forEach(p => {
      if (p.level.dimension.toString() !== boss.level.dimension.toString()) return
      if (p.distanceToSqr(boss) > H.partyRadius * H.partyRadius) return
      server.runCommandSilent(`advancement grant ${p.username} only horizon:legend/${leg.path} party`)
      credited++
    })
    console.info(`[horizon] ${id} died; ${credited} player(s) credited for horizon:legend/${leg.path}`)
  })
})

// ---------------------------------------------------------------------------- 2. discovery feedback
const SOUNDS = {
  // cues are Horizon sound events (kubejs/assets/horizon/sounds.json, re-skinnable by the Horizon-16x pack);
  // each maps to vanilla sounds, so every tier is distinct: chime / resonating crystal / beacon
  1: ['horizon:cue.item_found', 1, 1],
  2: ['horizon:cue.rare_loot', 1, 1],
  3: ['horizon:cue.mythic', 1, 1]
}

Object.keys(H.tiers).forEach(itemId => {
  PlayerEvents.inventoryChanged(itemId, event => {
    const p = event.player
    if (!p || p.level.isClientSide()) return
    const data = p.persistentData
    const key = 'horizon_seen_' + itemId.replace(':', '_')
    const count = p.inventory.countItem(event.item.item)
    const last = data.getInt(key + '_n')
    data.putInt(key + '_n', count)
    if (count <= last) return                       // moved/spent, not found
    const now = p.level.gameTime
    if (now - data.getLong('horizon_fx_t') < 40) return   // at most one cue per 2 s
    data.putLong('horizon_fx_t', now)
    const tier = H.tiers[itemId]
    const first = !data.getBoolean(key)
    data.putBoolean(key, true)
    if (quiet(p) || (!first && tier < 2)) return
    const s = SOUNDS[tier]
    p.server.runCommandSilent(`execute as ${p.username} at @s run playsound ${s[0]} player @s ~ ~ ~ ${s[1]} ${s[2]}`)
    if (tier === 3) {
      p.server.runCommandSilent(`execute as ${p.username} at @s run particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.03 14 normal @a[distance=..24,tag=!horizon_fx_quiet]`)
    }
    const name = H.names[itemId] || itemId
    const msg = first ? `New discovery: ${name}` : `${name} recovered`
    const colour = tier === 3 ? 'light_purple' : tier === 2 ? 'aqua' : 'green'
    p.server.runCommandSilent(`title ${p.username} actionbar {"text":"${msg}","color":"${colour}"}`)
  })
})

// ---------------------------------------------------------------------------- 3. commands
ServerEvents.commandRegistry(event => {
  const { commands: Commands, arguments: Arguments } = event
  const setFx = (ctx, q) => {
    const p = ctx.source.player
    if (q) p.addTag('horizon_fx_quiet'); else p.removeTag('horizon_fx_quiet')
    p.tell(q ? 'Horizon effects: quiet (no Horizon sounds, particles or titles)' : 'Horizon effects: normal')
    return 1
  }
  event.register(Commands.literal('horizon')
    .then(Commands.literal('fx')
      .then(Commands.literal('quiet').executes(ctx => setFx(ctx, true)))
      .then(Commands.literal('normal').executes(ctx => setFx(ctx, false))))
    .then(Commands.literal('audit').requires(src => src.hasPermission(2))
      .then(Commands.argument('radius', Arguments.INTEGER.create(event))
        .executes(ctx => audit(ctx, Arguments.INTEGER.getResult(ctx, 'radius'), 1))
        .then(Commands.argument('rolls', Arguments.INTEGER.create(event))
          .executes(ctx => audit(ctx, Arguments.INTEGER.getResult(ctx, 'radius'), Arguments.INTEGER.getResult(ctx, 'rolls')))))))
})

const ResourceKey = Java.loadClass('net.minecraft.resources.ResourceKey')
const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
const Registries = Java.loadClass('net.minecraft.core.registries.Registries')
const LootParamsBuilder = Java.loadClass('net.minecraft.world.level.storage.loot.LootParams$Builder')
const LootContextParams = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParams')
const LootContextParamSets = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParamSets')
const Vec3 = Java.loadClass('net.minecraft.world.phys.Vec3')

function audit(ctx, radius, rolls) {
  try { return auditInner(ctx, radius, rolls) } catch (e) { console.error(`[horizon-audit] failed: ${e} ${e.stack || ''}`); return 0 }
}

function auditInner(ctx, radius, rolls) {
  const src = ctx.source
  const level = src.level
  const server = src.server
  const cx = Math.floor(src.position.x / 16), cz = Math.floor(src.position.z / 16)
  const r = Math.ceil(radius / 16)
  const tally = {}, tables = {}
  let containers = 0
  const add = (k, n) => { tally[k] = (tally[k] || 0) + n }
  const rollBe = be => {
    const tag = be.saveWithoutMetadata(level.registryAccess())
    let lt = null
    tag.getAllKeys().forEach(k => { if (!lt && String(k).toLowerCase().indexOf('loottable') >= 0 && tag.getTagType(k) === 8) lt = tag.getString(k) })
    if (!lt) return
    containers++
    tables[lt] = (tables[lt] || 0) + 1
    const table = server.reloadableRegistries().getLootTable(ResourceKey.create(Registries.LOOT_TABLE, ResourceLocation.parse(lt)))
    for (let i = 0; i < rolls; i++) rollOnce(table, be)
  }
  const rollOnce = (table, be) => {
    const params = new LootParamsBuilder(level).withParameter(LootContextParams.ORIGIN, Vec3.atCenterOf(be.blockPos)).create(LootContextParamSets.CHEST)
    table.getRandomItems(params).forEach(st => {
      const id = String(st.item.id)
      if (id.startsWith('horizon:')) add(id, st.count)
      else if (id === 'apotheosis:gem') add('apotheosis:gem', st.count)
      else if (String(st.components).indexOf('apotheosis:rarity') >= 0) add('apotheosis:affix_item', st.count)
      else if (id === 'minecraft:filled_map') add('exploration_map', st.count)
      add('_stacks', 1)
    })
  }
  const scanChunk = (x, z) => {
    if (!level.hasChunk(x, z)) return
    level.getChunk(x, z).getBlockEntities().values().forEach(rollBe)
  }
  for (let x = cx - r; x <= cx + r; x++) for (let z = cz - r; z <= cz + r; z++) scanChunk(x, z)
  const per = {}
  Object.keys(tally).forEach(k => per[k] = Math.round(tally[k] / rolls * 100) / 100)
  const line = `[horizon-audit] radius=${radius} rolls=${rolls} containers=${containers} perClear=${JSON.stringify(per)}`
  console.info(line)
  console.info(`[horizon-audit] tables=${JSON.stringify(tables)}`)
  src.sendSystemMessage(Text.of(line))
  return containers
}

// ---------------------------------------------------------------------------- 4. Trials (Gateways to Eternity)
// A completed Horizon Trial credits every player within 48 blocks of the gate with horizon:trial/<id>.
NativeEvents.onEvent('dev.shadowsoffire.gateways.event.GateEvent$Completed', event => {
  const gate = event.getEntity()
  const id = String(gate.nbt.getString('gate'))
  if (!id.startsWith('horizon:trial/')) return
  const server = gate.level.server
  server.players.forEach(p => {
    if (p.level.dimension.toString() === gate.level.dimension.toString() && p.distanceToSqr(gate) <= 48 * 48) {
      server.runCommandSilent(`advancement grant ${p.username} only horizon:${id.replace('horizon:', '')} done`)
    }
  })
  console.info(`[horizon] trial completed: ${id}`)
})
