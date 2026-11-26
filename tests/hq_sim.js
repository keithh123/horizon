// Headquarters ledger state tests: runs the real core of kubejs/server_scripts/horizon_headquarters.js (the section
// between @core-begin and @core-end) under Node against a fake world. No Minecraft involved: this proves ledger logic
// (idempotence, parties, migration, costs, services), not KubeJS/Minecraft API behaviour - that is server_test.py's job.
//
//   node tests/hq_sim.js            (exit 1 on any failure; run by scripts/horizon.py check and build_all.py)
'use strict'
const fs = require('fs'), path = require('path'), vm = require('vm')
const ROOT = path.resolve(__dirname, '..')
const ctx = { global: {}, console: console }
vm.createContext(ctx)
vm.runInContext(fs.readFileSync(path.join(ROOT, 'kubejs/startup_scripts/horizon_hq_data.js'), 'utf8'), ctx)
const src = fs.readFileSync(path.join(ROOT, 'kubejs/server_scripts/horizon_headquarters.js'), 'utf8')
const core = src.substring(src.indexOf('// @core-begin'), src.indexOf('// @core-end'))
vm.runInContext('const HQD = global.HORIZON_HQ\n' + core + '\nthis.HQCore = HQCore', ctx)
const C = ctx.HQCore, D = ctx.global.HORIZON_HQ

let fails = 0, passes = 0
function ok(cond, name) { if (cond) passes++; else { fails++; console.log('FAIL ' + name) } }

// ---------------------------------------------------------------- fake world
function World() {
  const w = { t: 1000, players: {}, saves: 0, fx: [], scans: {} }
  w.add = (u, opts) => { w.players[u] = Object.assign({ online: true, adv: {}, inv: {}, pos: null, respawn: null, given: [], loot: [], effects: [] }, opts || {}); return w.players[u] }
  w.env = {
    now: () => w.t,
    save: () => { w.saves++ },
    isOnline: u => !!(w.players[u] && w.players[u].online),
    hasAdv: (u, a) => !!(w.players[u] && w.players[u].online && w.players[u].adv[a]),
    grantAdv: (u, a) => { if (w.players[u].online) w.players[u].adv[a] = true },   // like the adapter: offline players wait for login
    near: (u, an, r) => { const p = w.players[u]; return !!(p && p.online && p.pos && p.pos.dim === an.dim && Math.hypot(p.pos.x - an.x, p.pos.y - an.y, p.pos.z - an.z) <= r) },
    respawnNear: (u, an, r) => { const p = w.players[u]; return !!(p && p.respawn && p.respawn.dim === an.dim && Math.hypot(p.respawn.x - an.x, p.respawn.y - an.y, p.respawn.z - an.z) <= r) },
    anchorIntact: an => !(w.broken && w.broken[an.x + ',' + an.y + ',' + an.z]),
    count: (u, it) => (w.players[u] && w.players[u].inv[it]) || 0,
    consume: (u, it, n) => { const inv = w.players[u].inv; if ((inv[it] || 0) < n) throw new Error('overdraw ' + it); inv[it] -= n },
    give: (u, it, n) => { const p = w.players[u]; p.given.push([it, n]); p.inv[it] = (p.inv[it] || 0) + n },
    giveLoot: (u, t) => w.players[u].loot.push(t),
    effect: (u, e, d, a) => w.players[u].effects.push(e),
    fx: (k, hq, u, d) => w.fx.push(k)
  }
  return w
}
const A0 = { dim: 'minecraft:overworld', x: 0, y: 64, z: 0 }
const near = { dim: 'minecraft:overworld', x: 2, y: 64, z: 1 }
function fullScan(extra) {
  const ids = { 'minecraft:chest': 2, 'minecraft:cartography_table': 1, 'create:mechanical_press': 1, 'create:depot': 1, 'minecraft:crafting_table': 1,
    'minecraft:smithing_table': 1, 'minecraft:lectern': 1, 'horizon:discovery_case': 1, 'ars_nouveau:enchanting_apparatus': 1, 'ae2:controller': 1,
    'mekanism:enrichment_chamber': 1, 'horizon:observatory_lens': 1 }
  Object.assign(ids, extra || {})
  return { scan: { ids: ids, tags: { '#c:chests': ids['minecraft:chest'] || 0 } } }
}
const emptyScan = { scan: { ids: {}, tags: {} } }
function give(p, cost, mult) { cost.forEach(c => { p.inv[c[0]] = (p.inv[c[0]] || 0) + c[1] * (mult || 1) }) }
const stage = id => C.BYID[id]
const allAdvs = () => { const a = {}; D.facts.forEach(f => a[f] = true); return a }

// ---------------------------------------------------------------- 1. founding, unmet requirements, prerequisite order
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near })
  ok(C.found(L, w.env, 'A', 'Alice', A0).ok, 'found ok')
  ok(!C.found(L, w.env, 'A', 'Alice', { dim: 'minecraft:overworld', x: 50, y: 64, z: 0 }).ok, 'cannot found twice')
  ok(a.adv['horizon:hq/root'], 'root mirror granted on founding')
  const r = C.commission(L, w.env, 'A', 'outpost', emptyScan)
  ok(!r.ok && /requirements/.test(r.msg), 'outpost unmet -> refused: ' + r.msg)
  ok(!C.commission(L, w.env, 'A', 'workshop', fullScan()).ok, 'workshop before outpost refused')
  ok(Object.keys(C.hqOf(L, 'A').stages).length === 0, 'no stage recorded on refusal')
}

// ---------------------------------------------------------------- 2. normal commissioning, exact consumption, double click, no partial consumption
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near, respawn: A0, adv: allAdvs() })
  C.found(L, w.env, 'A', 'Alice', A0)
  give(a, stage('outpost').cost)
  a.inv['minecraft:torch'] += 5                       // surplus must survive
  const r = C.commission(L, w.env, 'A', 'outpost', fullScan())
  ok(r.ok, 'outpost commissioned: ' + r.msg)
  ok(a.inv['minecraft:paper'] === 0 && a.inv['minecraft:torch'] === 5, 'cost consumed exactly once')
  const rewardsN = a.given.length
  ok(rewardsN === stage('outpost').rewards.length && a.loot.length === 1, 'rewards paid once')
  give(a, stage('outpost').cost)
  const r2 = C.commission(L, w.env, 'A', 'outpost', fullScan())
  ok(!r2.ok && r2.noop, 'double click is a no-op')
  ok(a.given.length === rewardsN && a.inv['minecraft:paper'] === 3, 'double click: no extra reward, no consumption')
  ok(a.adv['horizon:hq/outpost'], 'outpost mirror granted')
  // workshop: andesite present, plates missing -> nothing consumed
  a.inv['create:andesite_alloy'] = 8
  const r3 = C.commission(L, w.env, 'A', 'workshop', fullScan())
  ok(!r3.ok && a.inv['create:andesite_alloy'] === 8, 'partial contribution not consumed')
  // not near the charter
  a.pos = { dim: 'minecraft:overworld', x: 200, y: 64, z: 0 }
  a.inv['horizon:survey_plate'] = 4
  ok(!C.commission(L, w.env, 'A', 'workshop', fullScan()).ok, 'remote commissioning refused')
  a.pos = near
  ok(C.commission(L, w.env, 'A', 'workshop', fullScan()).ok, 'workshop commissioned near charter')
  // block evidence matters: without a press at the station the workshop requirement fails for a fresh station
}

// ---------------------------------------------------------------- 3. receipts and block evidence: a borrowed press item is not proof
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near, respawn: A0, adv: allAdvs() })
  C.found(L, w.env, 'A', 'Alice', A0)
  C.adminFixture(L, w.env, 'hq1', 'outpost')
  give(a, stage('workshop').cost)
  a.inv['create:mechanical_press'] = 1               // holding the machine is not enough
  const scan = fullScan({ 'create:mechanical_press': 0 })
  const r = C.commission(L, w.env, 'A', 'workshop', scan)
  ok(!r.ok, 'press item in inventory without a press at the station is refused')
  a.adv['create:mechanical_press'] = false
  const L2 = C.emptyLedger(); const w2 = World(); const b = w2.add('B', { pos: near, respawn: A0, adv: allAdvs() })
  b.adv['create:mechanical_press'] = false
  C.found(L2, w2.env, 'B', 'Bob', A0); C.adminFixture(L2, w2.env, 'hq1', 'outpost'); give(b, stage('workshop').cost)
  ok(!C.commission(L2, w2.env, 'B', 'workshop', fullScan()).ok, 'press placed but never ran (no builtin advancement) is refused')
}

// ---------------------------------------------------------------- 4. parties: invites, late joiners, offline credit, independent stations
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near, respawn: A0, adv: allAdvs() })
  const b = w.add('B', { pos: near, adv: {} })
  const c = w.add('C', { pos: { dim: 'minecraft:overworld', x: 500, y: 64, z: 500 }, adv: {} })
  C.found(L, w.env, 'A', 'Alice', A0)
  give(a, stage('outpost').cost); C.commission(L, w.env, 'A', 'outpost', fullScan())
  ok(!C.join(L, w.env, 'B', 'Bob', 'hq1').ok, 'join without invite refused')
  C.invite(L, w.env, 'A', 'B', 'Bob')
  const j = C.join(L, w.env, 'B', 'Bob', 'hq1')
  ok(j.ok && b.adv['horizon:hq/outpost'], 'late joiner gets mirrors')
  ok(b.given.length === 0, 'late joiner gets no stage rewards')
  // A goes offline; A's facts were recorded at founding, so B can commission the workshop on A's processing evidence
  a.online = false
  give(b, stage('workshop').cost)
  const r = C.commission(L, w.env, 'B', 'workshop', fullScan())
  ok(r.ok, 'member commissions with an offline member\'s recorded facts: ' + r.msg)
  ok(!a.adv['horizon:hq/workshop'], 'offline member not granted yet')
  C.syncMirrors(C.hqOf(L, 'A'), w.env, 'A')            // simulates PlayerEvents.loggedIn
  ok(!a.adv['horizon:hq/workshop'], 'offline grant waits for login')
  a.online = true
  ok(C.syncMirrors(C.hqOf(L, 'A'), w.env, 'A') === 1 && a.adv['horizon:hq/workshop'], 'login sync grants the missed mirror')
  ok(C.syncMirrors(C.hqOf(L, 'A'), w.env, 'A') === 0, 'replayed sync grants nothing')
  // independent station
  C.found(L, w.env, 'C', 'Cara', { dim: 'minecraft:overworld', x: 500, y: 64, z: 500 })
  ok(Object.keys(C.hqOf(L, 'C').stages).length === 0 && !c.adv['horizon:hq/outpost'], 'independent station starts empty')
  ok(!C.join(L, w.env, 'C', 'Cara', 'hq1').ok, 'cannot be in two stations')
  // leave / ownership
  ok(C.leave(L, w.env, 'A').ok && C.hqOf(L, 'B').owner === 'B', 'founder leaving transfers ownership')
  ok(C.hqOf(L, 'B').stages.workshop, 'station keeps progress after a member leaves')
  C.leave(L, w.env, 'B')
  ok(L.hqs.hq1 && !L.hqs.hq1.anchor && L.hqs.hq1.members.length === 0, 'last member leaving keeps the record and releases the charter')
  ok(a.adv['horizon:hq/outpost'], 'mirrors are never revoked')
}

// ---------------------------------------------------------------- 5. choices: two of three regions, idempotent contribution, third stays optional
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near, respawn: A0, adv: allAdvs() })
  C.found(L, w.env, 'A', 'Alice', A0)
  C.adminFixture(L, w.env, 'hq1', 'outpost'); C.adminFixture(L, w.env, 'hq1', 'workshop')
  const hall = stage('hall')
  const [coast, hollows, high] = hall.choices.options
  give(a, coast.cost)
  ok(C.contribute(L, w.env, 'A', 'hall', 'coast', fullScan()).ok, 'coast contributed')
  give(a, coast.cost)
  const again = C.contribute(L, w.env, 'A', 'hall', 'coast', fullScan())
  ok(!again.ok && again.noop && a.inv['horizon:tidebound_doubloon'] === coast.cost[0][1], 'repeated contribution is a no-op and consumes nothing')
  give(a, hall.cost)
  ok(!C.commission(L, w.env, 'A', 'hall', fullScan()).ok, 'hall needs two regions')
  give(a, hollows.cost)
  ok(C.contribute(L, w.env, 'A', 'hall', 'hollows', fullScan()).ok, 'hollows contributed')
  ok(C.unlockedServices(C.hqOf(L, 'A')).survey_ocean && C.unlockedServices(C.hqOf(L, 'A')).survey_archive, 'route services unlocked permanently')
  ok(C.commission(L, w.env, 'A', 'hall', fullScan()).ok, 'hall commissioned with two of three')
  give(a, high.cost)
  ok(C.contribute(L, w.env, 'A', 'hall', 'highlands', fullScan()).ok, 'third region still contributable after the stage')
  ok(a.adv['horizon:hq/hall/highlands'], 'optional route mirrored')
}

// ---------------------------------------------------------------- 6. broken / moved charter, non-member protection
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near, respawn: A0, adv: allAdvs() })
  w.add('X', { pos: near })
  C.found(L, w.env, 'A', 'Alice', A0)
  C.adminFixture(L, w.env, 'hq1', 'outpost')
  ok(!C.charterRemoved(L, w.env, A0, 'X', false).allow, 'non-member cannot break the anchor')
  ok(C.charterRemoved(L, w.env, A0, 'A', false).allow && !C.hqOf(L, 'A').anchor, 'member breaking it makes the station dormant')
  give(a, stage('workshop').cost)
  ok(!C.commission(L, w.env, 'A', 'workshop', fullScan()).ok, 'dormant station cannot commission')
  const A1 = { dim: 'minecraft:overworld', x: 40, y: 70, z: 40 }
  a.pos = { dim: 'minecraft:overworld', x: 41, y: 70, z: 40 }
  ok(C.bind(L, w.env, 'A', A1).ok && C.hqOf(L, 'A').stages.outpost, 'rebinding keeps commissioned stages')
  ok(C.commission(L, w.env, 'A', 'workshop', fullScan()).ok, 'relocated station commissions')
  // exploded charter (no player): adapter reports anchorIntact=false
  w.broken = { '40,70,40': true }
  give(a, stage('hall').cost)
  const r = C.commission(L, w.env, 'A', 'hall', fullScan())
  ok(!r.ok && r.dormant, 'missing anchor block refuses with a dormant message')
}

// ---------------------------------------------------------------- 7. services: scopes and cooldowns, replaced service
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near, respawn: A0, adv: allAdvs() })
  const b = w.add('B', { pos: near })
  C.found(L, w.env, 'A', 'Alice', A0); C.invite(L, w.env, 'A', 'B', 'Bob'); C.join(L, w.env, 'B', 'Bob', 'hq1')
  ok(!C.service(L, w.env, 'A', 'supply_crate').ok, 'service locked before workshop')
  C.adminFixture(L, w.env, 'hq1', 'outpost'); C.adminFixture(L, w.env, 'hq1', 'workshop')
  ok(C.service(L, w.env, 'A', 'supply_crate').ok, 'supply crate once')
  ok(!C.service(L, w.env, 'B', 'supply_crate').ok, 'hq-scoped cooldown shared by members (no party multiplication)')
  w.t += 24000
  ok(C.service(L, w.env, 'B', 'supply_crate').ok, 'available again after a day')
  C.adminFixture(L, w.env, 'hq1', 'hall'); C.adminFixture(L, w.env, 'hq1', 'conservatory'); C.adminFixture(L, w.env, 'hq1', 'foundry')
  ok(!C.unlockedServices(C.hqOf(L, 'A')).supply_crate && C.unlockedServices(C.hqOf(L, 'A')).supply_crate_plus, 'foundry replaces the crate')
  a.inv['minecraft:amethyst_shard'] = 4; b.inv['minecraft:amethyst_shard'] = 2
  ok(C.service(L, w.env, 'A', 'ward').ok && C.service(L, w.env, 'B', 'ward').ok, 'ward is per player')
  ok(!C.service(L, w.env, 'A', 'ward').ok && a.inv['minecraft:amethyst_shard'] === 2, 'ward cooldown; cost not taken on refusal')
}

// ---------------------------------------------------------------- 8. fixtures, migration
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near })
  C.found(L, w.env, 'A', 'Alice', A0)
  C.adminFixture(L, w.env, 'hq1', 'outpost')
  const hq = C.hqOf(L, 'A')
  ok(hq.stages.outpost.fixture && a.given.length === 0, 'fixture flagged and unrewarded')
  const old = { id: 'hq9', name: 'Old', owner: 'Z', members: ['Z'], anchor: A0, stages: { outpost: { t: 1, by: 'Z' } } }
  const m = C.migrateHq(JSON.parse(JSON.stringify(old)))
  ok(m.v === C.LEDGER_VERSION && m.stages.outpost && m.facts && m.options && Array.isArray(m.log), 'migration fills new fields, keeps stages')
}

// ---------------------------------------------------------------- 9. full campaign to the finale, rewards exactly once each
{
  const w = World(), L = C.emptyLedger()
  const a = w.add('A', { pos: near, respawn: A0, adv: allAdvs() })
  C.found(L, w.env, 'A', 'Alice', A0)
  let paid = 0
  C.STAGES.forEach(s => {
    if (s.choices) s.choices.options.slice(0, s.choices.min).forEach(o => { give(a, o.cost); ok(C.contribute(L, w.env, 'A', s.id, o.id, fullScan()).ok, 'contribute ' + o.id) })
    give(a, s.cost)
    const r = C.commission(L, w.env, 'A', s.id, fullScan())
    ok(r.ok, 'commission ' + s.id + ': ' + r.msg)
    paid += s.rewards.length
  })
  ok(a.given.length === paid, 'each stage paid exactly once (' + paid + ')')
  ok(w.fx.filter(k => k === 'finale').length === 1, 'finale sequence fired once')
  ok(C.currentIndex(C.hqOf(L, 'A')) === 6, 'all six stages recorded')
  ok(C.mirrorsFor(C.hqOf(L, 'A')).every(x => a.adv[x]), 'every mirror granted')
}

// ---------------------------------------------------------------- 10. static guarantees on the data
{
  const RELICS = ['horizon:wayfarer_shard', 'horizon:ancient_core', 'horizon:starforged_heart']
  ok(D.stages.every(s => s.rewards.every(r => RELICS.indexOf(r[0]) < 0)), 'no stage reward is a relic')
  ok(Object.keys(D.services).every(k => !D.services[k].loot || D.services[k].loot.indexOf('relic') < 0), 'no relic service')
  ok(D.stages.every((s, i) => s.requires.every(r => D.stages.findIndex(x => x.id === r) < i)), 'stage graph acyclic and ordered')
}

console.log(`hq_sim: ${passes} passed, ${fails} failed`)
process.exit(fails ? 1 : 0)
