// Project Horizon - headquarters campaign (hand-written).
// Rhino note: KubeJS 2101's Rhino rejects block-scoped const/let inside function bodies at run time ("redeclaration of
// var"), so every declaration inside a function is a function-scoped var. Top-level declarations stay const. Stage data: global.HORIZON_HQ, generated from
// manifests/headquarters.json by scripts/gen_headquarters.py. Design: docs/PROGRESSION.md, reference: docs/HEADQUARTERS.md.
//
// Authority: the server ledger in server.persistentData.horizon_hq is the ONLY source of truth. Quest completions and
// horizon:hq/* advancements are mirrors granted from it (their criterion is minecraft:impossible), never inputs.
// Every action (button click = chat command) is re-validated here: membership, distance to the bound charter,
// prerequisites, requirements and contributions. Contributions are counted first and consumed all-or-nothing, the stage
// is written before rewards are handed out, and a repeated/concurrent click finds the stage already recorded (no-op).
// Scans are bounded (charter scan volume, on click only, rate-limited); nothing runs per tick; no chunk is force-loaded.
//
// The section between @core-begin and @core-end is plain JavaScript with no Minecraft calls. tests/hq_sim.js runs it
// under Node against a fake world to exercise the state paths (double clicks, replays, parties, migration).

const HQD = global.HORIZON_HQ

// @core-begin
const HQCore = (function () {
  var D = HQD
  var STAGES = D.stages
  var BYID = {}
  STAGES.forEach((s, i) => { s.index = i; BYID[s.id] = s })
  var LEDGER_VERSION = D.ledger_version

  function emptyLedger() { return { v: LEDGER_VERSION, seq: 0, players: {}, hqs: {} } }

  function migrateHq(hq) {
    // v1 is the first ledger. Future versions add fields here; never drop recorded stages, options or facts.
    if (!hq.v) hq.v = 1
    ;['stages', 'options', 'facts', 'services', 'rewarded', 'names'].forEach(k => { if (!hq[k]) hq[k] = {} })
    ;['members', 'invites', 'log'].forEach(k => { if (!hq[k]) hq[k] = [] })
    hq.v = LEDGER_VERSION
    return hq
  }

  function log(hq, now, text) {
    hq.log.push({ t: now, text: text })
    if (hq.log.length > 24) hq.log.splice(0, hq.log.length - 24)
  }

  function hqOf(L, uuid) {
    var id = L.players[uuid]
    return id ? L.hqs[id] || null : null
  }

  function hqAt(L, anchor) {
    var ids = Object.keys(L.hqs)
    for (var i = 0; i < ids.length; i++) {
      var a = L.hqs[ids[i]].anchor
      if (a && a.dim === anchor.dim && a.x === anchor.x && a.y === anchor.y && a.z === anchor.z) return L.hqs[ids[i]]
    }
    return null
  }

  function done(hq, stageId) { return !!hq.stages[stageId] }
  function optionDone(hq, stageId, optId) { return !!(hq.options[stageId] && hq.options[stageId][optId]) }

  function currentIndex(hq) {   // number of commissioned stages in order
    var i = 0
    while (i < STAGES.length && done(hq, STAGES[i].id)) i++
    return i
  }

  // ---- facts: advancement-based evidence, recorded the first time any member is seen holding it
  function recordFacts(hq, env, uuid) {
    var n = 0
    D.facts.forEach(a => {
      if (!hq.facts[a] && env.hasAdv(uuid, a)) { hq.facts[a] = uuid; n++ }
    })
    return n
  }

  function factOk(hq, env, adv) {
    if (hq.facts[adv]) return true
    for (var i = 0; i < hq.members.length; i++) {
      var m = hq.members[i]
      if (env.isOnline(m) && env.hasAdv(m, adv)) { hq.facts[adv] = m; return true }
    }
    return false
  }

  function blockMatches(id, pattern, scan) {
    if (pattern.charAt(0) === '#') return 0          // tags are counted separately by the adapter
    if (pattern.charAt(pattern.length - 1) === '*') return id.indexOf(pattern.substring(0, pattern.length - 1)) === 0
    return id === pattern
  }

  function countBlocks(scan, blocks) {
    var n = 0
    blocks.forEach(b => {
      if (b.charAt(0) === '#') n += scan.tags[b] || 0
      else Object.keys(scan.ids).forEach(id => { if (blockMatches(id, b, scan)) n += scan.ids[id] })
    })
    return n
  }

  function checkReq(hq, env, r, ctx) {
    if (r.kind === 'adv') {
      var ok = factOk(hq, env, r.adv)
      return { ok: ok, detail: ok ? 'done' : 'not yet' }
    }
    if (r.kind === 'adv_any') {
      var n = 0
      r.advs.forEach(a => { if (factOk(hq, env, a)) n++ })
      return { ok: n >= r.count, detail: Math.min(n, r.count) + '/' + r.count }
    }
    if (r.kind === 'block_any') {
      if (!ctx.scan) return { ok: false, detail: 'no bound charter' }
      var n = countBlocks(ctx.scan, r.blocks)
      return { ok: n >= r.count, detail: Math.min(n, r.count) + '/' + r.count + ' at the station' }
    }
    if (r.kind === 'respawn_near') {
      if (!hq.anchor) return { ok: false, detail: 'no bound charter' }
      for (var i = 0; i < hq.members.length; i++) {
        var m = hq.members[i]
        if (env.isOnline(m) && env.respawnNear(m, hq.anchor, r.radius)) return { ok: true, detail: 'home spawn set' }
      }
      return { ok: false, detail: 'no online member respawns here' }
    }
    return { ok: false, detail: 'unknown requirement ' + r.kind }
  }

  function costStatus(env, uuid, cost) {
    return cost.map(c => { var have = env.count(uuid, c[0]); return { item: c[0], need: c[1], have: have, ok: have >= c[1] } })
  }

  function prereqsMet(hq, s) {
    for (var i = 0; i < s.requires.length; i++) if (!done(hq, s.requires[i])) return false
    return true
  }

  // Full status of one stage for one acting player. Pure read; may record newly witnessed facts.
  function evaluate(hq, env, stageId, uuid, ctx) {
    var s = BYID[stageId]
    var out = { stage: s, done: done(hq, stageId), prereqs: prereqsMet(hq, s), reqs: [], options: [], cost: costStatus(env, uuid, s.cost) }
    s.requirements.forEach(r => { var c = checkReq(hq, env, r, ctx); out.reqs.push({ r: r, ok: c.ok, detail: c.detail }) })
    var optDone = 0
    if (s.choices) {
      s.choices.options.forEach(o => {
        var od = optionDone(hq, stageId, o.id)
        if (od) optDone++
        var reqs = o.requirements.map(r => { var c = checkReq(hq, env, r, ctx); return { r: r, ok: c.ok, detail: c.detail } })
        out.options.push({ o: o, done: od, reqs: reqs, cost: costStatus(env, uuid, o.cost), ready: !od && out.prereqs && reqs.every(x => x.ok) })
      })
    }
    out.optDone = optDone
    out.choicesOk = !s.choices || optDone >= s.choices.min
    out.reqsOk = out.reqs.every(x => x.ok)
    out.costOk = out.cost.every(x => x.ok)
    out.ready = !out.done && out.prereqs && out.reqsOk && out.choicesOk && out.costOk
    out.reason = out.done ? 'already commissioned' : !out.prereqs ? 'commission ' + s.requires.map(r => BYID[r].title).join(', ') + ' first'
      : !out.reqsOk ? 'requirements missing' : !out.choicesOk ? (s.choices.min - optDone) + ' more ' + s.choices.title.toLowerCase() + ' needed'
      : !out.costOk ? 'contribution missing from your inventory' : 'ready'
    return out
  }

  function consumeAll(env, uuid, cost) {
    // all-or-nothing: verify every line first (already done by the caller), then remove
    for (var i = 0; i < cost.length; i++) if (env.count(uuid, cost[i][0]) < cost[i][1]) return false
    cost.forEach(c => env.consume(uuid, c[0], c[1]))
    return true
  }

  function memberCheck(L, env, uuid, needNear) {
    var hq = hqOf(L, uuid)
    if (!hq) return { err: 'You are not part of a headquarters. Right-click a Survey Charter to found one.' }
    if (needNear) {
      if (!hq.anchor) return { err: 'Your headquarters has no bound charter. Place a Survey Charter and bind it.' }
      if (!env.near(uuid, hq.anchor, D.charter.interaction_radius)) return { err: 'Stand within ' + D.charter.interaction_radius + ' blocks of your bound charter.' }
      if (!env.anchorIntact(hq.anchor)) return { err: 'Your charter is gone. Progress is kept; place a new charter and bind it.' , dormant: true }
    }
    return { hq: hq }
  }

  function mirrorsFor(hq) {
    var a = ['horizon:hq/root']
    STAGES.forEach(s => {
      if (done(hq, s.id)) a.push('horizon:hq/' + s.id)
      if (s.choices) s.choices.options.forEach(o => { if (optionDone(hq, s.id, o.id)) a.push('horizon:hq/' + s.id + '/' + o.id) })
    })
    return a
  }

  function syncMirrors(hq, env, uuid) {
    var n = 0
    mirrorsFor(hq).forEach(a => { if (!env.hasAdv(uuid, a)) { env.grantAdv(uuid, a); n++ } })
    return n
  }

  function syncOnline(hq, env) { hq.members.forEach(m => { if (env.isOnline(m)) syncMirrors(hq, env, m) }) }

  // ---------------------------------------------------------------- actions (each returns {ok, msg})
  function found(L, env, uuid, name, anchor) {
    if (hqOf(L, uuid)) return { ok: false, msg: 'You already belong to a headquarters. Leave it first, or bind this charter to it.' }
    if (hqAt(L, anchor)) return { ok: false, msg: 'This charter is already bound to a headquarters.' }
    L.seq++
    var id = 'hq' + L.seq
    var hq = migrateHq({ id: id, name: name + "'s Station", owner: uuid, members: [uuid], created: env.now() })
    hq.names[uuid] = name
    hq.anchor = anchor
    log(hq, env.now(), 'founded by ' + name)
    L.hqs[id] = hq
    L.players[uuid] = id
    recordFacts(hq, env, uuid)
    syncMirrors(hq, env, uuid)
    env.fx('found', hq, uuid, null)
    return { ok: true, msg: 'Headquarters founded: ' + hq.name + '. The charter is your station anchor.' }
  }

  function bind(L, env, uuid, anchor) {
    var hq = hqOf(L, uuid)
    if (!hq) return { ok: false, msg: 'Found a headquarters first.' }
    var other = hqAt(L, anchor)
    if (other && other.id !== hq.id) return { ok: false, msg: 'This charter belongs to another headquarters.' }
    if (other && other.id === hq.id) return { ok: true, msg: 'Already bound here.' }
    var old = hq.anchor
    hq.anchor = anchor
    log(hq, env.now(), 'charter bound at ' + anchor.x + ' ' + anchor.y + ' ' + anchor.z + ' (' + anchor.dim + ')' + (old ? ', moved from ' + old.x + ' ' + old.y + ' ' + old.z : ''))
    return { ok: true, msg: 'Headquarters ' + (old ? 'relocated' : 'bound') + ' here. Commissioned stages are kept; room checks use the new location from now on.' }
  }

  function charterRemoved(L, env, anchor, uuid, isAdmin) {
    var hq = hqAt(L, anchor)
    if (!hq) return { ok: true, allow: true }
    if (!isAdmin && hq.members.indexOf(uuid) < 0) return { ok: false, allow: false, msg: 'This charter anchors ' + hq.name + '. Only its members can move it.' }
    hq.anchor = null
    log(hq, env.now(), 'charter removed' + (uuid ? ' by ' + (hq.names[uuid] || uuid) : ''))
    return { ok: true, allow: true, hq: hq, msg: 'Headquarters dormant: progress is kept, services pause until a charter is placed and bound.' }
  }

  function anchorLost(L, env, hq) {   // the anchor chunk is loaded and the block is no longer a charter
    if (!hq.anchor) return
    hq.anchor = null
    log(hq, env.now(), 'charter missing (destroyed without a member breaking it); headquarters dormant')
  }

  function invite(L, env, uuid, targetUuid, targetName) {
    var hq = hqOf(L, uuid)
    if (!hq) return { ok: false, msg: 'Found a headquarters first.' }
    if (hq.members.indexOf(targetUuid) >= 0) return { ok: false, msg: targetName + ' is already a member.' }
    if (hq.invites.indexOf(targetUuid) < 0) hq.invites.push(targetUuid)
    hq.names[targetUuid] = targetName
    log(hq, env.now(), (hq.names[uuid] || uuid) + ' invited ' + targetName)
    return { ok: true, msg: targetName + ' is invited to ' + hq.name + '.', hq: hq }
  }

  function join(L, env, uuid, name, hqId) {
    var hq = L.hqs[hqId]
    if (!hq) return { ok: false, msg: 'No such headquarters.' }
    if (hqOf(L, uuid)) return { ok: false, msg: 'Leave your current headquarters first.' }
    var i = hq.invites.indexOf(uuid)
    if (i < 0) return { ok: false, msg: 'You have not been invited to ' + hq.name + '.' }
    hq.invites.splice(i, 1)
    hq.members.push(uuid)
    hq.names[uuid] = name
    L.players[uuid] = hq.id
    log(hq, env.now(), name + ' joined')
    recordFacts(hq, env, uuid)
    syncMirrors(hq, env, uuid)       // late joiner: quest mirrors catch up; stage rewards were already paid to the station
    return { ok: true, msg: 'You joined ' + hq.name + '. Its commissioned stages now show in your quest book; its rewards were already handed out.', hq: hq }
  }

  function leave(L, env, uuid) {
    var hq = hqOf(L, uuid)
    if (!hq) return { ok: false, msg: 'You are not part of a headquarters.' }
    hq.members.splice(hq.members.indexOf(uuid), 1)
    delete L.players[uuid]
    log(hq, env.now(), (hq.names[uuid] || uuid) + ' left')
    if (hq.owner === uuid) hq.owner = hq.members.length ? hq.members[0] : null
    if (!hq.members.length) {
      hq.anchor = null      // an empty station releases its charter; the record stays for /horizon hqadmin recovery
      log(hq, env.now(), 'no members left; record kept, charter released')
    }
    // Mirrors already granted to the leaver stay (advancements are never revoked); the ledger alone decides stages.
    return { ok: true, msg: 'You left ' + hq.name + '. Your own quests and relics are untouched; the station keeps its progress.' }
  }

  function unlockedServices(hq) {
    var out = {}
    STAGES.forEach(s => {
      if (done(hq, s.id)) s.services.forEach(k => out[k] = true)
      if (s.choices) s.choices.options.forEach(o => { if (optionDone(hq, s.id, o.id)) o.services.forEach(k => out[k] = true) })
    })
    Object.keys(out).forEach(k => { var r = D.services[k].replaced_by; if (r && out[r]) delete out[k] })
    return out
  }

  function contribute(L, env, uuid, stageId, optId, ctx) {
    var m = memberCheck(L, env, uuid, true)
    if (m.err) return { ok: false, msg: m.err, dormant: m.dormant }
    var hq = m.hq, s = BYID[stageId]
    if (!s || !s.choices) return { ok: false, msg: 'That stage has no choices.' }
    var o = s.choices.options.filter(x => x.id === optId)[0]
    if (!o) return { ok: false, msg: 'Unknown option.' }
    if (optionDone(hq, stageId, optId)) return { ok: false, msg: o.title + ' is already recorded for this station.', noop: true }
    var ev = evaluate(hq, env, stageId, uuid, ctx)
    var st = ev.options.filter(x => x.o.id === optId)[0]
    if (!ev.prereqs) return { ok: false, msg: 'Commission ' + s.requires.map(r => BYID[r].title).join(', ') + ' first.' }
    if (!st.reqs.every(x => x.ok)) return { ok: false, msg: o.title + ': ' + st.reqs.filter(x => !x.ok).map(x => x.r.text).join('; ') }
    if (!st.cost.every(x => x.ok)) return { ok: false, msg: 'Bring: ' + st.cost.filter(x => !x.ok).map(x => (x.need - x.have) + 'x ' + x.item).join(', ') }
    if (!consumeAll(env, uuid, o.cost)) return { ok: false, msg: 'Contribution changed; try again.' }
    if (!hq.options[stageId]) hq.options[stageId] = {}
    hq.options[stageId][optId] = { t: env.now(), by: uuid }
    log(hq, env.now(), (hq.names[uuid] || uuid) + ' contributed ' + o.title)
    syncOnline(hq, env)
    env.fx('contribute', hq, uuid, { stage: s, option: o })
    return { ok: true, msg: o.title + ' recorded. ' + o.contribution, hq: hq }
  }

  function commission(L, env, uuid, stageId, ctx) {
    var m = memberCheck(L, env, uuid, true)
    if (m.err) return { ok: false, msg: m.err, dormant: m.dormant }
    var hq = m.hq, s = BYID[stageId]
    if (!s) return { ok: false, msg: 'Unknown stage.' }
    if (done(hq, stageId)) return { ok: false, msg: s.title + ' is already commissioned.', noop: true }
    var ev = evaluate(hq, env, stageId, uuid, ctx)
    if (!ev.ready) return { ok: false, msg: s.title + ': ' + ev.reason + '.', ev: ev }
    if (!consumeAll(env, uuid, s.cost)) return { ok: false, msg: 'Contribution changed; try again.' }
    hq.stages[stageId] = { t: env.now(), by: uuid }        // recorded before any reward: a crash never pays twice
    log(hq, env.now(), (hq.names[uuid] || uuid) + ' commissioned ' + s.numeral + '. ' + s.title)
    var pay = !hq.rewarded[stageId]
    hq.rewarded[stageId] = true
    env.save()
    if (pay) {
      s.rewards.forEach(r => env.give(uuid, r[0], r[1]))
      s.reward_loot.forEach(t => env.giveLoot(uuid, t))
    }
    syncOnline(hq, env)
    env.fx(stageId === STAGES[STAGES.length - 1].id ? 'finale' : 'commission', hq, uuid, { stage: s })
    return { ok: true, msg: s.numeral + '. ' + s.title + ' commissioned. ' + s.unlocks, hq: hq }
  }

  function service(L, env, uuid, svcId) {
    var m = memberCheck(L, env, uuid, true)
    if (m.err) return { ok: false, msg: m.err, dormant: m.dormant }
    var hq = m.hq, sv = D.services[svcId]
    if (!sv) return { ok: false, msg: 'Unknown service.' }
    if (!unlockedServices(hq)[svcId]) return { ok: false, msg: sv.title + ' is not available at this station yet.' }
    var now = env.now()
    if (!hq.services[svcId]) hq.services[svcId] = { hq: -1e12, players: {} }
    var rec = hq.services[svcId]
    var last = sv.scope === 'hq' ? rec.hq : (rec.players[uuid] === undefined ? -1e12 : rec.players[uuid])
    var wait = last + sv.cooldown_ticks - now
    if (wait > 0) return { ok: false, msg: sv.title + ' is ready again in ' + Math.ceil(wait / 1200) + ' min.' }
    var cost = costStatus(env, uuid, sv.cost)
    if (!cost.every(x => x.ok)) return { ok: false, msg: 'Bring: ' + cost.filter(x => !x.ok).map(x => (x.need - x.have) + 'x ' + x.item).join(', ') }
    if (!consumeAll(env, uuid, sv.cost)) return { ok: false, msg: 'Cost changed; try again.' }
    if (sv.scope === 'hq') rec.hq = now; else rec.players[uuid] = now
    env.save()
    if (sv.kind === 'loot') env.giveLoot(uuid, sv.loot)
    else sv.effects.forEach(e => env.effect(uuid, e[0], e[1], e[2]))
    env.fx('service', hq, uuid, { service: sv })
    return { ok: true, msg: sv.title + ': ' + sv.text }
  }

  // Admin fixture: marks a stage commissioned for testing later stages. Flagged, unrewarded, logged.
  function adminFixture(L, env, hqId, stageId) {
    var hq = L.hqs[hqId], s = BYID[stageId]
    if (!hq || !s) return { ok: false, msg: 'unknown hq or stage' }
    if (done(hq, stageId)) return { ok: false, msg: 'already commissioned' }
    hq.stages[stageId] = { t: env.now(), by: 'admin', fixture: true }
    hq.rewarded[stageId] = true      // fixtures never pay rewards
    if (s.choices) {
      if (!hq.options[stageId]) hq.options[stageId] = {}
      s.choices.options.slice(0, s.choices.min).forEach(o => { if (!hq.options[stageId][o.id]) hq.options[stageId][o.id] = { t: env.now(), by: 'admin', fixture: true } })
    }
    log(hq, env.now(), 'ADMIN FIXTURE: ' + s.title + ' marked commissioned (no rewards)')
    syncOnline(hq, env)
    return { ok: true, msg: 'fixture: ' + hq.id + ' ' + s.title }
  }

  return { emptyLedger: emptyLedger, migrateHq: migrateHq, hqOf: hqOf, hqAt: hqAt, evaluate: evaluate, recordFacts: recordFacts,
           found: found, bind: bind, charterRemoved: charterRemoved, anchorLost: anchorLost, invite: invite, join: join, leave: leave,
           contribute: contribute, commission: commission, service: service, unlockedServices: unlockedServices,
           syncMirrors: syncMirrors, mirrorsFor: mirrorsFor, adminFixture: adminFixture, currentIndex: currentIndex,
           STAGES: STAGES, BYID: BYID, LEDGER_VERSION: LEDGER_VERSION }
})()
// @core-end

// ================================================================ Minecraft adapter (KubeJS 2101 / NeoForge 21.1)
const HQ_ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
const HQ_ResourceKey = Java.loadClass('net.minecraft.resources.ResourceKey')
const HQ_Registries = Java.loadClass('net.minecraft.core.registries.Registries')
const HQ_BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
const HQ_TagKey = Java.loadClass('net.minecraft.tags.TagKey')
const HQ_BlockPos = Java.loadClass('net.minecraft.core.BlockPos')
const HQ_CompoundTag = Java.loadClass('net.minecraft.nbt.CompoundTag')
const HQ_LootParamsBuilder = Java.loadClass('net.minecraft.world.level.storage.loot.LootParams$Builder')
const HQ_LootContextParams = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParams')
const HQ_LootContextParamSets = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParamSets')
const HQ_MobEffectInstance = Java.loadClass('net.minecraft.world.effect.MobEffectInstance')
const HQ_UUID = Java.loadClass('java.util.UUID')
const HQ_CHARTER = HQD.charter.block
// colour helpers: Text.<colour>() takes a component, so wrap strings first
const HQT = {}
;['gray', 'darkGray', 'gold', 'yellow', 'aqua', 'green', 'red', 'white'].forEach(c => { HQT[c] = s => Text.of(String(s))[c]() })
const HQ_KEY = 'horizon_hq'

// ---- persistence: one compound; every headquarters is its own JSON string (stays far below the NBT string limit)
function hqLoad(server) {
  var pd = server.persistentData
  var L = HQCore.emptyLedger()
  if (!pd.contains(HQ_KEY)) return L
  var root = pd.getCompound(HQ_KEY)
  L.v = root.getInt('v') || HQCore.LEDGER_VERSION
  L.seq = root.getInt('seq')
  var pl = root.getCompound('players')
  pl.getAllKeys().forEach(k => { L.players[String(k)] = String(pl.getString(k)) })
  var hs = root.getCompound('hqs')
  hs.getAllKeys().forEach(k => {
    try { L.hqs[String(k)] = HQCore.migrateHq(JSON.parse(String(hs.getString(k)))) }
    catch (e) { console.error(`[horizon-hq] unreadable record ${k}: ${e}; left untouched in NBT`) }
  })
  return L
}

function hqSave(server, L) {
  var root = new HQ_CompoundTag()
  root.putInt('v', HQCore.LEDGER_VERSION)
  root.putInt('seq', L.seq)
  var pl = new HQ_CompoundTag()
  Object.keys(L.players).forEach(k => pl.putString(k, L.players[k]))
  root.put('players', pl)
  var old = server.persistentData.contains(HQ_KEY) ? server.persistentData.getCompound(HQ_KEY).getCompound('hqs') : new HQ_CompoundTag()
  var hs = new HQ_CompoundTag()
  old.getAllKeys().forEach(k => { if (!L.hqs[String(k)]) hs.putString(k, old.getString(k)) })   // keep unreadable records
  Object.keys(L.hqs).forEach(k => hs.putString(k, JSON.stringify(L.hqs[k])))
  root.put('hqs', hs)
  server.persistentData.put(HQ_KEY, root)
}

const HQ_TEST = {}   // uuid -> FakePlayer, only while /horizon hqadmin selftest runs
function hqPlayer(server, uuid) { return HQ_TEST[uuid] || server.playerList.getPlayer(HQ_UUID.fromString(uuid)) }
function hqQuiet(p) { return p.tags.contains('horizon_fx_quiet') }
function hqAnchorOf(block) { return { dim: String(block.dimension), x: block.x, y: block.y, z: block.z } }
function hqLevel(server, dim) {   // server.getLevel(ResourceKey) is ambiguous for Rhino (KubeJS adds an overload)
  var found = null
  server.getAllLevels().forEach(l => { if (String(l.dimension) === dim) found = l })
  return found
}

function hqEnv(server, L) {
  var now = () => Number(server.overworld().levelData.getGameTime())   // Level.getGameTime() is not visible to Rhino here
  return {
    now: now,
    save: () => hqSave(server, L),
    isOnline: u => !!hqPlayer(server, u),
    hasAdv: (u, a) => { var p = hqPlayer(server, u); return !!p && !!p.isAdvancementDone(a) },
    grantAdv: (u, a) => {   // same command path the 0.5 legend party credit uses in game
      var p = hqPlayer(server, u)
      if (!p) return
      if (HQ_TEST[u]) p.unlockAdvancement(a)
      else server.runCommandSilent(`advancement grant ${p.username} only ${a}`)
    },
    near: (u, an, r) => {
      var p = hqPlayer(server, u)
      return !!p && String(p.level.dimension) === an.dim && p.distanceToSqr(an.x + 0.5, an.y + 0.5, an.z + 0.5) <= r * r
    },
    respawnNear: (u, an, r) => {
      var p = hqPlayer(server, u)
      if (!p) return false
      var rp = p.getRespawnPosition()
      if (!rp) return false
      if (String(p.getRespawnDimension().location()) !== an.dim) return false
      var dx = rp.x - an.x, dy = rp.y - an.y, dz = rp.z - an.z
      return dx * dx + dy * dy + dz * dz <= r * r
    },
    anchorIntact: an => {
      var lvl = hqLevel(server, an.dim)
      if (!lvl) return false
      var pos = new HQ_BlockPos(an.x, an.y, an.z)
      if (!lvl.isLoaded(pos)) return true             // never force-load; judge it when someone is near
      return String(HQ_BuiltInRegistries.BLOCK.getKey(lvl.getBlockState(pos).getBlock())) === HQ_CHARTER
    },
    count: (u, item) => {
      var p = hqPlayer(server, u)
      if (!p) return 0
      var inv = p.getInventory()
      var n = 0
      for (var i = 0; i < inv.getContainerSize(); i++) { var st = inv.getItem(i); if (!st.isEmpty() && String(st.id) === item) n += st.getCount() }
      return n
    },
    consume: (u, item, n) => {
      var p = hqPlayer(server, u)
      var inv = p.getInventory()
      for (var i = 0; i < inv.getContainerSize() && n > 0; i++) {
        var st = inv.getItem(i)
        if (!st.isEmpty() && String(st.id) === item) { var k = Math.min(n, st.getCount()); st.shrink(k); n -= k }
      }
      inv.setChanged()
      if (n > 0) console.error(`[horizon-hq] consume shortfall ${item} ${n}`)
    },
    give: (u, item, n) => { var p = hqPlayer(server, u); if (p) p.give(Item.of(item, n)) },   // overflow drops at the player
    giveLoot: (u, table) => {
      var p = hqPlayer(server, u)
      if (!p) return
      var lt = server.reloadableRegistries().getLootTable(HQ_ResourceKey.create(HQ_Registries.LOOT_TABLE, HQ_ResourceLocation.parse(table)))
      var params = new HQ_LootParamsBuilder(p.serverLevel()).withParameter(HQ_LootContextParams.ORIGIN, p.position()).withParameter(HQ_LootContextParams.THIS_ENTITY, p).create(HQ_LootContextParamSets.CHEST)
      lt.getRandomItems(params).forEach(st => p.give(st))
    },
    effect: (u, eff, dur, amp) => {
      var p = hqPlayer(server, u)
      if (p) p.addEffect(new HQ_MobEffectInstance(HQ_BuiltInRegistries.MOB_EFFECT.getHolder(HQ_ResourceLocation.parse(eff)).get(), dur, amp, false, true))
    },
    fx: (kind, hq, u, data) => hqFx(server, kind, hq, u, data)
  }
}

// ---- presentation: one owner for commissioning feedback (title + one cue + a short particle burst at the charter)
function hqFx(server, kind, hq, u, data) {
  var actor = hqPlayer(server, u)
  hq.members.forEach(m => {
    var p = hqPlayer(server, m)
    if (!p || hqQuiet(p)) return
    if (kind === 'commission' || kind === 'finale') {
      var s = data.stage
      var nxt = HQCore.STAGES[s.index + 1]
      server.runCommandSilent(`title ${p.username} times 10 70 20`)
      server.runCommandSilent(`title ${p.username} subtitle ${JSON.stringify({ text: nxt ? 'Next: ' + nxt.numeral + '. ' + nxt.title : 'The Lantern Line is open', color: 'gray' })}`)
      server.runCommandSilent(`title ${p.username} title ${JSON.stringify({ text: s.numeral + '. ' + s.title, color: kind === 'finale' ? 'aqua' : 'gold' })}`)
      server.runCommandSilent(`execute as ${p.username} at @s run playsound horizon:cue.${kind === 'finale' ? 'finale' : 'commission'} player @s ~ ~ ~ 1 1`)
      p.tell(HQT.gray('Survey log: ').append(Text.of(s.log).italic()))
    } else if (kind === 'contribute') {
      server.runCommandSilent(`execute as ${p.username} at @s run playsound horizon:cue.contribution player @s ~ ~ ~ 1 1`)
      server.runCommandSilent(`title ${p.username} actionbar ${JSON.stringify({ text: data.option.title + ' recorded for ' + hq.name, color: 'aqua' })}`)
    } else if (kind === 'found' && actor && p === actor) {
      server.runCommandSilent(`execute as ${p.username} at @s run playsound horizon:cue.commission player @s ~ ~ ~ 0.8 1.2`)
    } else if (kind === 'service' && actor && p === actor) {
      server.runCommandSilent(`execute as ${p.username} at @s run playsound horizon:cue.item_found player @s ~ ~ ~ 1 1`)
    }
  })
  if (hq.anchor && (kind === 'commission' || kind === 'finale' || kind === 'found')) {
    var a = hq.anchor
    var n = kind === 'finale' ? 120 : 30
    server.runCommandSilent(`execute in ${a.dim} run particle minecraft:end_rod ${a.x + 0.5} ${a.y + 1.2} ${a.z + 0.5} 0.4 ${kind === 'finale' ? 3 : 0.8} 0.4 0.04 ${n} normal @a[distance=..48,tag=!horizon_fx_quiet]`)
    if (kind === 'finale') server.runCommandSilent(`execute in ${a.dim} run particle minecraft:totem_of_undying ${a.x + 0.5} ${a.y + 1.5} ${a.z + 0.5} 1 1.5 1 0.4 90 normal @a[distance=..48,tag=!horizon_fx_quiet]`)
  }
}

// ---- bounded room scan around the anchor (on click only)
function hqScan(server, hq) {
  if (!hq || !hq.anchor) return null
  var a = hq.anchor, sc = HQD.charter.scan
  var lvl = hqLevel(server, a.dim)
  if (!lvl) return null
  var ids = {}, rep = {}
  for (var x = a.x - sc.horizontal; x <= a.x + sc.horizontal; x++) {
    for (var z = a.z - sc.horizontal; z <= a.z + sc.horizontal; z++) {
      if (!lvl.isLoaded(new HQ_BlockPos(x, a.y, z))) continue
      for (var y = a.y - sc.down; y <= a.y + sc.up; y++) {
        var st = lvl.getBlockState(new HQ_BlockPos(x, y, z))
        if (st.isAir()) continue
        var id = String(HQ_BuiltInRegistries.BLOCK.getKey(st.getBlock()))
        ids[id] = (ids[id] || 0) + 1
        if (!rep[id]) rep[id] = st
      }
    }
  }
  var tags = {}
  hqTagPatterns().forEach(t => {
    var key = HQ_TagKey.create(HQ_Registries.BLOCK, HQ_ResourceLocation.parse(t.substring(1)))
    var n = 0
    Object.keys(rep).forEach(id => { if (rep[id]['is(net.minecraft.tags.TagKey)'](key)) n += ids[id] })   // explicit overload
    tags[t] = n
  })
  return { ids: ids, tags: tags }
}

let HQ_TAGS = null
function hqTagPatterns() {
  if (HQ_TAGS) return HQ_TAGS
  var out = {}
  var visit = rs => rs.forEach(r => { if (r.kind === 'block_any') r.blocks.forEach(b => { if (b.charAt(0) === '#') out[b] = true }) })
  HQD.stages.forEach(s => { visit(s.requirements); if (s.choices) s.choices.options.forEach(o => visit(o.requirements)) })
  HQ_TAGS = Object.keys(out)
  return HQ_TAGS
}

// ---- rate limit: one action per player per charter.action_cooldown_ticks
function hqThrottle(p) {
  var now = Number(p.server.overworld().levelData.getGameTime())
  var last = p.persistentData.getLong('horizon_hq_t')
  if (now - last < HQD.charter.action_cooldown_ticks && now >= last) return true
  p.persistentData.putLong('horizon_hq_t', now)
  return false
}

// ---- the panel (chat-based screen: every button is a command the server re-validates)
const HQ_CMD = '/horizon hq '
function btn(label, cmd, hover, colour) {
  return Text.of('[' + label + ']')[colour || 'aqua']().clickRunCommand(cmd).hover(Text.of(hover))
}
function itemName(id) { const s = Item.of(id); return s.isEmpty() ? id : String(s.hoverName.string) }

function hqPanel(server, p, L, env, hq, focus) {
  var scan = hqScan(server, hq)
  var ctx = { scan: scan }
  var cur = HQCore.currentIndex(hq)
  var stageId = focus || (HQCore.STAGES[cur] ? HQCore.STAGES[cur].id : null)
  var line = () => p.tell(HQT.darkGray('---------------------------------------------'))
  line()
  p.tell(HQT.gold(hq.name).bold().append(HQT.gray('  ' + cur + '/' + HQCore.STAGES.length + ' stations commissioned' + (hq.anchor ? '' : '  (DORMANT: no bound charter)'))))
  p.tell(Text.empty().append(HQT.gray('Stages: ')).append(Text.joinSep(Text.of(' '), HQCore.STAGES.map(s =>
    Text.of(s.numeral)[hq.stages[s.id] ? 'green' : (s.index === cur ? 'yellow' : 'darkGray')]().clickRunCommand(HQ_CMD + 'panel ' + s.id)
      .hover(Text.of(s.numeral + '. ' + s.title + (hq.stages[s.id] ? ' - commissioned' : s.index === cur ? ' - next' : s.index > cur + 1 ? ' - later' : '')))))))
  if (!stageId) {
    p.tell(HQT.aqua('The Lantern Line is open. ').append(HQT.gray('Post-campaign: every legend, every realm and the Horizon Gauntlet (quest book: Hall of Legends).')))
  } else {
    var ev = HQCore.evaluate(hq, env, stageId, String(p.uuid), ctx)
    var s = ev.stage
    var spoiler = s.index > cur + 1 && !ev.done
    p.tell(HQT.yellow(s.numeral + '. ' + s.title).bold().append(HQT.gray(ev.done ? '  commissioned' : '')))
    p.tell(HQT.gray(s.summary))
    if (!spoiler && !ev.done) {
      ev.reqs.forEach(x => p.tell(Text.of(x.ok ? ' ✔ ' : ' ✘ ')[x.ok ? 'green' : 'red']().append(HQT.white(x.r.text)).append(HQT.darkGray('  ' + x.detail)).hover(Text.of('Counts: ' + x.r.proves))))
      if (s.choices) {
        p.tell(HQT.gold(' ' + s.choices.title + ': ' + ev.optDone + '/' + s.choices.min).hover(Text.of(s.choices.text)))
        ev.options.forEach(o => {
          var head = Text.of('   ' + (o.done ? '✔ ' : '• ') + o.o.title)[o.done ? 'green' : 'white']().hover(Text.of(o.o.summary + '\n' + o.o.contribution))
          if (!o.done) {
            var need = o.reqs.filter(x => !x.ok).map(x => x.r.text)
            head.append(Text.of('  '))
            head.append(btn(o.ready && o.cost.every(c => c.ok) ? 'Contribute' : 'Details', HQ_CMD + (o.ready ? 'contribute ' + s.id + ' ' + o.o.id : 'panel ' + s.id),
              (need.length ? 'Missing: ' + need.join('; ') + '\n' : '') + 'Contribution: ' + o.cost.map(c => c.have + '/' + c.need + ' ' + itemName(c.item)).join(', '),
              o.ready && o.cost.every(c => c.ok) ? 'green' : 'gray'))
          }
          p.tell(head)
        })
      }
      p.tell(HQT.gray(' Contribution: ').append(Text.joinSep(HQT.gray(', '), ev.cost.map(c => Text.of(c.have + '/' + c.need + ' ' + itemName(c.item))[c.ok ? 'green' : 'red']()))))
      p.tell(HQT.gray(' Unlocks: ').append(HQT.white(s.unlocks)))
      p.tell(Text.empty().append(btn('Commission ' + s.title, HQ_CMD + 'commission ' + s.id, ev.ready ? 'Consumes the contribution once and records the stage for the whole station.' : 'Not yet: ' + ev.reason, ev.ready ? 'green' : 'gray')))
    } else if (ev.done) {
      p.tell(HQT.gray(' Unlocked: ').append(HQT.white(s.unlocks)))
    } else {
      p.tell(HQT.darkGray(' Details open once the stage before it is commissioned.'))
    }
  }
  var sv = HQCore.unlockedServices(hq)
  var ks = Object.keys(sv)
  if (ks.length) p.tell(HQT.gray('Services: ').append(Text.joinSep(Text.of(' '), ks.map(k => btn(HQD.services[k].title, HQ_CMD + 'service ' + k,
    HQD.services[k].text + (HQD.services[k].cost.length ? '\nCost: ' + HQD.services[k].cost.map(c => c[1] + 'x ' + itemName(c[0])).join(', ') : ''), 'aqua')))))
  p.tell(Text.empty().append(btn('Members', HQ_CMD + 'members', 'Who belongs to this station', 'gray')).append(Text.of(' '))
    .append(Text.of('[Invite]').gray().clickSuggestCommand(HQ_CMD + 'invite ').hover(Text.of('Type a player name after the command'))).append(Text.of(' '))
    .append(btn('Refresh', HQ_CMD + 'panel', 'Re-check the station', 'gray')))
  line()
}

// ---- runner: load, act, save, report
function hqRun(p, fn) {
  var server = p.server
  var L = hqLoad(server)
  var env = hqEnv(server, L)
  var res
  try { res = fn(L, env) } catch (e) { console.error(`[horizon-hq] ${e} ${e.stack || ''}`); p.tell(HQT.red('Headquarters error; nothing was changed. See the server log.')); return 0 }
  hqSave(server, L)
  if (res && res.msg) p.tell(Text.of(res.msg)[res.ok ? 'green' : 'yellow']())
  return res && res.ok ? 1 : 0
}

function hqWithAnchorCheck(server, L, env, hq) {
  if (hq && hq.anchor && !env.anchorIntact(hq.anchor)) HQCore.anchorLost(L, env, hq)
}

// ---------------------------------------------------------------- events
BlockEvents.rightClicked(HQ_CHARTER, event => {
  var p = event.player
  if (!p || p.level.isClientSide() || String(event.hand) !== 'MAIN_HAND') return
  event.cancel()
  if (hqThrottle(p)) return
  var server = p.server
  var anchor = hqAnchorOf(event.block)
  p.persistentData.putString('horizon_hq_pending', JSON.stringify(anchor))
  var L = hqLoad(server)
  var env = hqEnv(server, L)
  var here = HQCore.hqAt(L, anchor)
  var mine = HQCore.hqOf(L, String(p.uuid))
  if (mine) { HQCore.recordFacts(mine, env, String(p.uuid)); HQCore.syncMirrors(mine, env, String(p.uuid)) }
  if (here && mine && here.id === mine.id) { hqPanel(server, p, L, env, mine, null); hqSave(server, L); return }
  if (here) { p.tell(HQT.gray('This charter anchors ' + here.name + '.')); hqSave(server, L); return }
  if (mine) {
    hqWithAnchorCheck(server, L, env, mine)
    p.tell(HQT.yellow('This charter is not bound. ').append(btn(mine.anchor ? 'Move headquarters here' : 'Bind headquarters here', HQ_CMD + 'bind',
      mine.anchor ? 'Relocates the anchor. Stages stay commissioned; room checks happen around the new charter.' : 'Ends the dormant state and resumes services.', 'green')))
    hqSave(server, L)
    return
  }
  p.tell(HQT.gold('Meridian Survey Charter').bold())
  HQD.stages.length && p.tell(HQT.gray('Plant it where your base will grow. Six stations - Outpost, Workshop, Expedition Hall, Arcane Conservatory, Foundry and Observatory - are commissioned here, one after another.'))
  p.tell(Text.empty().append(btn('Found a headquarters here', HQ_CMD + 'found', 'Creates your station with this charter as its anchor. Friends join by invitation.', 'green')))
  hqSave(server, L)
})

BlockEvents.placed(HQ_CHARTER, event => {
  var p = event.entity
  if (!p || !p.isPlayer()) return
  p.setStatusMessage(HQT.aqua('Right-click the charter to found or bind your headquarters.'))
})

BlockEvents.broken(HQ_CHARTER, event => {
  var p = event.player
  if (!p) return
  var server = p.server
  var L = hqLoad(server)
  var env = hqEnv(server, L)
  var r = HQCore.charterRemoved(L, env, hqAnchorOf(event.block), String(p.uuid), p.hasPermissions(2) && p.isCreative())
  if (!r.allow) { event.cancel(); p.tell(HQT.yellow(r.msg)); return }
  hqSave(server, L)
  if (r.msg && r.hq) p.tell(HQT.yellow(r.msg))
})

ItemEvents.rightClicked('horizon:founding_kit', event => {
  var p = event.player
  if (!p || p.level.isClientSide()) return
  event.item.shrink(1)
  HQD.kit.forEach(k => p.give(Item.of(k[0], k[1])))
  p.tell(HQT.gold('Founding Kit unpacked. ').append(HQT.gray('Place the Survey Charter where your base will grow and right-click it.')))
  event.cancel()
})

PlayerEvents.loggedIn(event => {
  var p = event.player
  var server = p.server
  if (!p.persistentData.getBoolean('horizon_kit_given')) {   // new players and established worlds alike, once per player
    p.persistentData.putBoolean('horizon_kit_given', true)
    p.give(Item.of('horizon:founding_kit', 1))
    p.tell(HQT.gold('Project Horizon 0.6: ').append(HQT.gray('a Founding Kit is in your inventory. Unpack it, plant the Survey Charter where your base will grow, and commission your headquarters. Earlier progress counts automatically.')))
  }
  var L = hqLoad(server)
  var env = hqEnv(server, L)
  var hq = HQCore.hqOf(L, String(p.uuid))
  if (!hq) return
  hq.names[String(p.uuid)] = String(p.username)
  HQCore.recordFacts(hq, env, String(p.uuid))
  var n = HQCore.syncMirrors(hq, env, String(p.uuid))
  hqSave(server, L)
  if (n) console.info(`[horizon-hq] ${p.username}: ${n} mirror advancement(s) synced from ${hq.id}`)
})

// ---------------------------------------------------------------- commands
ServerEvents.commandRegistry(event => {
  var { commands: Commands, arguments: Arguments } = event
  var P = ctx => ctx.source.player
  var run = (ctx, fn) => { var p = P(ctx); if (!p) return 0; if (hqThrottle(p)) return 0; return hqRun(p, fn) }
  var pending = p => { try { return JSON.parse(String(p.persistentData.getString('horizon_hq_pending'))) } catch (e) { return null } }
  var nearPending = (p, env, a) => a && env.near(String(p.uuid), a, HQD.charter.interaction_radius) && env.anchorIntact(a)
  var panel = (ctx, focus) => {
    var p = P(ctx); if (!p) return 0
    var server = p.server, L = hqLoad(server), env = hqEnv(server, L), hq = HQCore.hqOf(L, String(p.uuid))
    if (!hq) { p.tell(HQT.yellow('You are not part of a headquarters. Unpack your Founding Kit and right-click the Survey Charter.')); return 0 }
    hqWithAnchorCheck(server, L, env, hq)
    HQCore.recordFacts(hq, env, String(p.uuid))
    hqPanel(server, p, L, env, hq, focus && HQCore.BYID[focus] ? focus : null)
    hqSave(server, L)
    return 1
  }
  event.register(Commands.literal('horizon').then(Commands.literal('hq')
    .executes(ctx => panel(ctx, null))
    .then(Commands.literal('panel').executes(ctx => panel(ctx, null))
      .then(Commands.argument('stage', Arguments.WORD.create(event)).executes(ctx => panel(ctx, String(Arguments.WORD.getResult(ctx, 'stage'))))))
    .then(Commands.literal('found').executes(ctx => run(ctx, (L, env) => {
      var p = P(ctx), a = pending(p)
      if (!nearPending(p, env, a)) return { ok: false, msg: 'Right-click a Survey Charter first and stay near it.' }
      return HQCore.found(L, env, String(p.uuid), String(p.username), a)
    })))
    .then(Commands.literal('bind').executes(ctx => run(ctx, (L, env) => {
      var p = P(ctx), a = pending(p)
      if (!nearPending(p, env, a)) return { ok: false, msg: 'Right-click the new Survey Charter first and stay near it.' }
      var hq = HQCore.hqOf(L, String(p.uuid))
      if (hq) hqWithAnchorCheck(p.server, L, env, hq)
      return HQCore.bind(L, env, String(p.uuid), a)
    })))
    .then(Commands.literal('commission').then(Commands.argument('stage', Arguments.WORD.create(event)).executes(ctx => run(ctx, (L, env) => {
      var p = P(ctx), hq = HQCore.hqOf(L, String(p.uuid))
      if (hq) hqWithAnchorCheck(p.server, L, env, hq)
      return HQCore.commission(L, env, String(p.uuid), String(Arguments.WORD.getResult(ctx, 'stage')), { scan: hqScan(p.server, hq) })
    }))))
    .then(Commands.literal('contribute').then(Commands.argument('stage', Arguments.WORD.create(event)).then(Commands.argument('option', Arguments.WORD.create(event)).executes(ctx => run(ctx, (L, env) => {
      var p = P(ctx), hq = HQCore.hqOf(L, String(p.uuid))
      if (hq) hqWithAnchorCheck(p.server, L, env, hq)
      return HQCore.contribute(L, env, String(p.uuid), String(Arguments.WORD.getResult(ctx, 'stage')), String(Arguments.WORD.getResult(ctx, 'option')), { scan: hqScan(p.server, hq) })
    })))))
    .then(Commands.literal('service').then(Commands.argument('service', Arguments.WORD.create(event)).executes(ctx => run(ctx, (L, env) => {
      var p = P(ctx), hq = HQCore.hqOf(L, String(p.uuid))
      if (hq) hqWithAnchorCheck(p.server, L, env, hq)
      return HQCore.service(L, env, String(p.uuid), String(Arguments.WORD.getResult(ctx, 'service')))
    }))))
    .then(Commands.literal('invite').then(Commands.argument('player', Arguments.PLAYER.create(event)).executes(ctx => run(ctx, (L, env) => {
      var p = P(ctx), t = Arguments.PLAYER.getResult(ctx, 'player')
      var r = HQCore.invite(L, env, String(p.uuid), String(t.uuid), String(t.username))
      if (r.ok) t.tell(HQT.gold(p.username + ' invites you to ' + r.hq.name + '. ').append(btn('Join', HQ_CMD + 'join ' + r.hq.id, 'Leave your own headquarters first if you have one.', 'green')))
      return r
    }))))
    .then(Commands.literal('join').then(Commands.argument('id', Arguments.WORD.create(event)).executes(ctx => run(ctx, (L, env) =>
      HQCore.join(L, env, String(P(ctx).uuid), String(P(ctx).username), String(Arguments.WORD.getResult(ctx, 'id')))))))
    .then(Commands.literal('leave').executes(ctx => {
      var p = P(ctx); if (!p) return 0
      p.tell(HQT.yellow('Leave your headquarters? The station keeps its progress. ').append(btn('Confirm leave', HQ_CMD + 'leave confirm', 'You can be invited back later.', 'red')))
      return 1
    }).then(Commands.literal('confirm').executes(ctx => run(ctx, (L, env) => HQCore.leave(L, env, String(P(ctx).uuid))))))
    .then(Commands.literal('members').executes(ctx => {
      var p = P(ctx); if (!p) return 0
      var L = hqLoad(p.server), hq = HQCore.hqOf(L, String(p.uuid))
      if (!hq) return 0
      p.tell(HQT.gold(hq.name + ': ').append(HQT.white(hq.members.map(m => (hq.names[m] || m) + (m === hq.owner ? ' (founder)' : '')).join(', '))))
      p.tell(Text.empty().append(Text.of('[Leave]').gray().clickRunCommand(HQ_CMD + 'leave').hover(Text.of('Asks for confirmation'))))
      return 1
    }))))
  // ---- bounded admin diagnostics / recovery (op level 2). Never edits a world block.
  event.register(Commands.literal('horizon').then(Commands.literal('hqadmin').requires(src => src.hasPermission(2))
    .then(Commands.literal('list').executes(ctx => {
      var L = hqLoad(ctx.source.server)
      Object.keys(L.hqs).slice(0, 40).forEach(k => { var h = L.hqs[k]; ctx.source.sendSystemMessage(Text.of(`${k} "${h.name}" members=${h.members.length} stages=${HQCore.currentIndex(h)}/6 anchor=${h.anchor ? h.anchor.dim + ' ' + h.anchor.x + ' ' + h.anchor.y + ' ' + h.anchor.z : 'none'}`)) })
      return 1
    }))
    .then(Commands.literal('info').then(Commands.argument('id', Arguments.WORD.create(event)).executes(ctx => {
      var L = hqLoad(ctx.source.server), h = L.hqs[String(Arguments.WORD.getResult(ctx, 'id'))]
      if (!h) return 0
      var txt = JSON.stringify({ id: h.id, v: h.v, owner: h.owner, members: h.members, stages: h.stages, options: h.options, anchor: h.anchor, facts: Object.keys(h.facts).length, log: h.log.slice(-8) })
      ctx.source.sendSystemMessage(Text.of(txt.length > 4000 ? txt.substring(0, 4000) + '...' : txt))
      console.info(`[horizon-hq] info ${txt}`)
      return 1
    })))
    .then(Commands.literal('fixture').then(Commands.argument('id', Arguments.WORD.create(event)).then(Commands.argument('stage', Arguments.WORD.create(event)).executes(ctx => {
      var server = ctx.source.server, L = hqLoad(server), env = hqEnv(server, L)
      var r = HQCore.adminFixture(L, env, String(Arguments.WORD.getResult(ctx, 'id')), String(Arguments.WORD.getResult(ctx, 'stage')))
      hqSave(server, L)
      ctx.source.sendSystemMessage(Text.of('[horizon-hq] ' + r.msg)); console.info(`[horizon-hq] ${r.msg}`)
      return r.ok ? 1 : 0
    }))))
    .then(Commands.literal('unbind').then(Commands.argument('id', Arguments.WORD.create(event)).executes(ctx => {
      var server = ctx.source.server, L = hqLoad(server), h = L.hqs[String(Arguments.WORD.getResult(ctx, 'id'))]
      if (!h) return 0
      h.anchor = null; h.log.push({ t: 0, text: 'ADMIN unbind' }); hqSave(server, L)
      ctx.source.sendSystemMessage(Text.of('[horizon-hq] ' + h.id + ' unbound (progress kept)'))
      return 1
    })))
    .then(Commands.literal('addmember').then(Commands.argument('id', Arguments.WORD.create(event)).then(Commands.argument('player', Arguments.PLAYER.create(event)).executes(ctx => {
      var server = ctx.source.server, L = hqLoad(server), env = hqEnv(server, L), t = Arguments.PLAYER.getResult(ctx, 'player')
      var h = L.hqs[String(Arguments.WORD.getResult(ctx, 'id'))]
      if (!h) return 0
      var old = HQCore.hqOf(L, String(t.uuid))
      if (old) HQCore.leave(L, env, String(t.uuid))
      HQCore.invite(L, env, h.owner || String(t.uuid), String(t.uuid), String(t.username))
      var r = HQCore.join(L, env, String(t.uuid), String(t.username), h.id)
      hqSave(server, L)
      ctx.source.sendSystemMessage(Text.of('[horizon-hq] ' + r.msg))
      return r.ok ? 1 : 0
    }))))
    .then(Commands.literal('selftest').executes(ctx => hqSelftest(ctx.source.server, ctx.source)))
    .then(Commands.literal('resync').executes(ctx => {
      var server = ctx.source.server, L = hqLoad(server), env = hqEnv(server, L)
      var n = 0
      server.players.forEach(p => { var h = HQCore.hqOf(L, String(p.uuid)); if (h) { HQCore.recordFacts(h, env, String(p.uuid)); n += HQCore.syncMirrors(h, env, String(p.uuid)) } })
      hqSave(server, L)
      ctx.source.sendSystemMessage(Text.of(`[horizon-hq] resync: ${n} mirror advancement(s) granted`)); console.info(`[horizon-hq] resync ${n}`)
      return 1
    }))))
})

// ================================================================ automated adapter self-test (op only, DISPOSABLE WORLDS ONLY)
// Drives Outpost -> Workshop with a NeoForge FakePlayer through the real adapter (inventory, advancements, block scan,
// loot, persistence). It places blocks at y=200 above world spawn and creates a test headquarters: never run it on a
// world you care about. Output lines are tagged [horizon-hq-selftest]; scripts/server_test.py collects them.
const HQ_FakePlayerFactory = Java.loadClass('net.neoforged.neoforge.common.util.FakePlayerFactory')
function hqSelftestBody(server, t) {   // separate function: Rhino rejects block-scoped const inside try here
  var lvl = server.overworld()
  var sp = lvl.getSharedSpawnPos()
  var x = sp.x, y = 200, z = sp.z
  var fp = HQ_FakePlayerFactory.getMinecraft(lvl)
  var u = String(fp.uuid)
  HQ_TEST[u] = fp
  fp.getInventory().clearContent()     // FakePlayer instances persist between runs; start from an empty inventory
  fp.setPos(x + 1.5, y, z + 1.5)
  // blocks are placed with the Java API (runCommandSilent setblock did not always apply during testing)
  var place = (bx, by, bz, id) => lvl.setBlock(new HQ_BlockPos(bx, by, bz), HQ_BuiltInRegistries.BLOCK['get(net.minecraft.resources.ResourceLocation)'](HQ_ResourceLocation.parse(id)).defaultBlockState(), 3)
  var cmd = c => {
    var m = c.match(/^setblock (-?\d+) (-?\d+) (-?\d+) ([a-z0-9_:]+)/)
    if (m) return place(Number(m[1]), Number(m[2]), Number(m[3]), m[4])
    m = c.match(/^fill (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) ([a-z0-9_:]+)/)
    if (m) { for (var fx = Number(m[1]); fx <= Number(m[4]); fx++) for (var fy = Number(m[2]); fy <= Number(m[5]); fy++) for (var fz = Number(m[3]); fz <= Number(m[6]); fz++) place(fx, fy, fz, m[7]); return true }
    throw new Error('selftest cmd not supported: ' + c)
  }
  cmd(`fill ${x - 6} ${y - 1} ${z - 6} ${x + 6} ${y + 4} ${z + 6} minecraft:air`)
  cmd(`fill ${x - 6} ${y - 1} ${z - 6} ${x + 6} ${y - 1} ${z + 6} minecraft:stone`)
  cmd(`setblock ${x} ${y} ${z} ${HQ_CHARTER}`)
  var anchor = { dim: 'minecraft:overworld', x: x, y: y, z: z }
  var L = hqLoad(server), env = hqEnv(server, L)
  var prior = HQCore.hqOf(L, u)
  if (prior) HQCore.leave(L, env, u)
  var r = HQCore.found(L, env, u, 'HorizonQA', anchor)
  t('found', r.ok, r.msg)
  t('mirror advancements registered (hq/root, hq/outpost, hq/workshop)', ['horizon:hq/root', 'horizon:hq/outpost', 'horizon:hq/workshop'].every(a => server.advancements.get(HQ_ResourceLocation.parse(a)) !== null))
  // NeoForge FakePlayer advancements are no-ops (probe: unlockAdvancement then isAdvancementDone == false), so this test
  // injects the facts a real member would contribute. Real-player advancement reading/granting needs a client test.
  var witness = advs => { var L0 = hqLoad(server); var h0 = HQCore.hqOf(L0, u); advs.forEach(a => { h0.facts[a] = u }); hqSave(server, L0) }
  hqSave(server, L)
  var hq0 = HQCore.hqOf(hqLoad(server), u)
  t('ledger persisted in server.persistentData', !!hq0 && hq0.anchor.x === x)
  L = hqLoad(server); env = hqEnv(server, L)
  var hq = HQCore.hqOf(L, u)
  r = HQCore.commission(L, env, u, 'outpost', { scan: hqScan(server, hq) })
  t('outpost refused while unmet', !r.ok, r.msg)
  cmd(`setblock ${x + 2} ${y} ${z} minecraft:chest`); cmd(`setblock ${x + 3} ${y} ${z} minecraft:barrel`)
  cmd(`setblock ${x - 2} ${y} ${z} minecraft:cartography_table`)
  cmd(`setblock ${x} ${y} ${z + 3} minecraft:red_bed`)
  fp.setRespawnPosition(lvl.dimensionKey, new HQ_BlockPos(x, y, z + 3), 0, true, false)
  witness(['minecraft:husbandry/plant_seed', 'horizon:atlas/roadside'])
  L = hqLoad(server); env = hqEnv(server, L); hq = HQCore.hqOf(L, u)
  var sc = hqScan(server, hq)
  t('scan counts chests via #c:chests tag', (sc.tags['#c:chests'] || 0) >= 1, JSON.stringify(sc.tags))
  t('scan sees cartography table', (sc.ids['minecraft:cartography_table'] || 0) === 1)
  fp.give(Item.of('minecraft:paper', 3)); fp.give(Item.of('minecraft:torch', 10))
  r = HQCore.commission(L, env, u, 'outpost', { scan: sc })
  t('outpost commissioned', r.ok, r.msg)
  t('cost consumed exactly (torch 10-8=2)', env.count(u, 'minecraft:torch') === 2 && env.count(u, 'minecraft:paper') === 0)
  t('reward: copper construction stick', env.count(u, 'constructionstick:copper_stick') === 1)
  t('reward: emblem', env.count(u, 'horizon:emblem_outpost') === 1)
  // With a player in the loot context Supplementaries turns exploration maps into a Cartographer's Quill (lazy map: the
  // structure search runs when the player uses it). From the console the same table yields a filled map.
  t('reward loot: Surveyor chart (map or Supplementaries Cartographer\'s Quill)', env.count(u, 'minecraft:filled_map') + env.count(u, 'minecraft:map') + env.count(u, 'supplementaries:cartographers_quill') >= 1,
    'filled=' + env.count(u, 'minecraft:filled_map') + ' quill=' + env.count(u, 'supplementaries:cartographers_quill'))
  t('outpost recorded in ledger and marked rewarded', !!hq.stages.outpost && hq.rewarded.outpost === true)
  hqSave(server, L)
  fp.give(Item.of('minecraft:paper', 3)); fp.give(Item.of('minecraft:torch', 8))
  L = hqLoad(server); env = hqEnv(server, L); hq = HQCore.hqOf(L, u)
  r = HQCore.commission(L, env, u, 'outpost', { scan: hqScan(server, hq) })
  t('double commission is a no-op', !r.ok && r.noop && env.count(u, 'constructionstick:copper_stick') === 1 && env.count(u, 'minecraft:paper') === 3)
  // workshop: the press must exist, have run (builtin advancement) and plates must come from pressing
  var recipe = server.recipeManager.byKey(HQ_ResourceLocation.parse('horizon:hq/survey_plate_pressing'))
  t('create:pressing recipe for Survey Plate loaded', recipe.isPresent())
  cmd(`setblock ${x + 4} ${y + 1} ${z + 2} create:mechanical_press`); cmd(`setblock ${x + 4} ${y} ${z + 2} create:depot`)
  cmd(`setblock ${x - 3} ${y} ${z + 2} minecraft:crafting_table`)
  fp.give(Item.of('create:andesite_alloy', 8)); fp.give(Item.of('horizon:survey_plate', 4))
  hqSave(server, L); witness(['horizon:atlas/underground'])
  L = hqLoad(server); env = hqEnv(server, L); hq = HQCore.hqOf(L, u)
  r = HQCore.commission(L, env, u, 'workshop', { scan: hqScan(server, hq) })
  t('workshop refused until a press has actually run', !r.ok && env.count(u, 'horizon:survey_plate') === 4, r.msg)
  hqSave(server, L); witness(['create:mechanical_press'])
  L = hqLoad(server); env = hqEnv(server, L); hq = HQCore.hqOf(L, u)
  r = HQCore.commission(L, env, u, 'workshop', { scan: hqScan(server, hq) })
  t('workshop commissioned', r.ok, r.msg)
  t('plates consumed', env.count(u, 'horizon:survey_plate') === 0)
  t('reward: iron construction stick', env.count(u, 'constructionstick:iron_stick') === 1)
  r = HQCore.service(L, env, u, 'supply_crate')
  t('supply crate service (loot table)', r.ok && env.count(u, 'minecraft:bread') >= 8, r.msg)
  r = HQCore.service(L, env, u, 'supply_crate')
  t('supply crate cooldown', !r.ok)
  hqSave(server, L)
  cmd(`setblock ${x} ${y} ${z} minecraft:air`)
  L = hqLoad(server); env = hqEnv(server, L); hq = HQCore.hqOf(L, u)
  hqWithAnchorCheck(server, L, env, hq)
  t('destroyed charter -> dormant, stages kept', !hq.anchor && !!hq.stages.workshop)
  r = HQCore.commission(L, env, u, 'hall', { scan: hqScan(server, hq) })
  t('dormant station refuses', !r.ok)
  cmd(`setblock ${x} ${y} ${z} ${HQ_CHARTER}`)
  r = HQCore.bind(L, env, u, anchor)
  t('rebind restores anchor', r.ok && !!hq.anchor)
  hqSave(server, L)
  HQCore.leave(L, env, u)          // leave the QA station so the fake player is free for the next run
  hqSave(server, L)
}

function hqSelftest(server, src) {
  var out = []
  var t = (name, cond, extra) => { out.push((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : '')) }
  try {
    hqSelftestBody(server, t)
  } catch (e) {
    out.push('FAIL exception :: ' + e + ' ' + (e.stack || ''))
  } finally {
    Object.keys(HQ_TEST).forEach(k => delete HQ_TEST[k])
  }
  out.forEach(l => { console.info('[horizon-hq-selftest] ' + l); src.sendSystemMessage(Text.of('[horizon-hq-selftest] ' + l)) })
  var fails = out.filter(l => l.indexOf('FAIL') === 0).length
  console.info(`[horizon-hq-selftest] summary ${out.length - fails} passed, ${fails} failed`)
  return fails ? 0 : 1
}
