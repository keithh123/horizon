// Horizon client QA harness (TEST INSTANCES ONLY - never shipped; scripts/build.py does not copy tests/).
// Copy to <instance>/minecraft/kubejs/client_scripts/ on a disposable clone. It polls horizon_qa/cmd.json once a
// second and runs the queued actions through the real client: chat commands, the use key (KeyMapping.click -> the
// same startUseItem path a mouse right-click takes), screen widget dumps/clicks, GUI scale, render distance, Iris
// shader toggle, screenshots and frame-time samples. Results go to horizon_qa/out.json and the game log ([HQA]).
var HQA = { last: -1, queue: [], wait: 0, out: [], frames: null, t: 0 }
var HQA_Screenshot = Java.loadClass('net.minecraft.client.Screenshot')
var HQA_KeyMapping = Java.loadClass('net.minecraft.client.KeyMapping')
var HQA_Inventory = Java.loadClass('net.minecraft.client.gui.screens.inventory.InventoryScreen')
var HQA_Creative = Java.loadClass('net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen')

function hqaLog(s) { console.info('[HQA] ' + s); HQA.out.push(String(s)) }
function hqaFlush() { JsonIO.write('horizon_qa/out.json', { last: HQA.last, lines: HQA.out }) }

function hqaWidgets(screen) {
  var res = []
  screen.children().forEach(w => {
    var r = { cls: String(w).replace(/@[0-9a-f]+$/, '') }
    try { r.x = w.getX(); r.y = w.getY(); r.w = w.getWidth(); r.h = w.getHeight() } catch (e) { }
    try { r.msg = String(w.getMessage().getString()) } catch (e) { }
    try { r.visible = w.visible; r.active = w.active } catch (e) { }
    res.push(r)
  })
  var g = ''
  try { g = ' guiLeft=' + screen.getGuiLeft() + ' guiTop=' + screen.getGuiTop() } catch (e) { }
  hqaLog('screen ' + String(screen).replace(/@[0-9a-f]+$/, '') + ' size=' + screen.width + 'x' + screen.height + g + ' guiScale=' + Client.getWindow().getGuiScale())
  res.forEach(r => hqaLog('  widget ' + JSON.stringify(r)))
}

function hqaRun(a) {
  var mc = Client, p = mc.player
  var k = a.split(':')[0], v = a.substring(k.length + 1)
  if (k === 'wait') { HQA.wait = Number(v); return }
  if (k === 'cmd') { p.connection.sendCommand(v.charAt(0) === '/' ? v.substring(1) : v); hqaLog('cmd ' + v); return }
  if (k === 'say') { p.connection.sendChat(v); return }
  if (k === 'use') { HQA_KeyMapping.click(mc.options.keyUse.getKey()); hqaLog('use-key click; target=' + (mc.hitResult ? mc.hitResult.getType() : 'none') + (mc.hitResult && mc.hitResult.getBlockPos ? ' ' + mc.hitResult.getBlockPos() : '')); return }
  if (k === 'attack') { HQA_KeyMapping.click(mc.options.keyAttack.getKey()); return }
  if (k === 'hold') { var kv = v.split('='); mc.options['key' + kv[0]].setDown(kv[1] === 'on'); hqaLog('hold ' + v); return }
  if (k === 'look') { var yp = v.split(','); p.connection.sendCommand('tp @s ~ ~ ~ ' + yp[0] + ' ' + yp[1]); return }
  if (k === 'slot') { p.getInventory().selected = Number(v); return }
  if (k === 'rd') { mc.options.renderDistance().set(Number(v)); mc.options.save(); hqaLog('renderDistance=' + mc.options.renderDistance().get()); return }
  if (k === 'gui') { mc.options.guiScale().set(Number(v)); mc.resizeDisplay(); hqaLog('guiScale option=' + v + ' effective=' + mc.getWindow().getGuiScale()); return }
  if (k === 'persp') { var P = Java.loadClass('net.minecraft.client.CameraType'); mc.options.setCameraType(P.values()[Number(v)]); return }
  if (k === 'inv') { mc.setScreen(p.isCreative() ? new HQA_Creative(p, p.connection.enabledFeatures(), true) : new HQA_Inventory(p)); return }
  if (k === 'close') { if (mc.screen) mc.screen.onClose(); return }   // onClose, not setScreen(null): Spatial GUI restores its camera there
  if (k === 'esc') { if (mc.screen) mc.screen.keyPressed(256, 0, 0); return }
  if (k === 'widgets') { if (mc.screen) hqaWidgets(mc.screen); else hqaLog('no screen'); return }
  if (k === 'click') { var c = v.split(','); var s = mc.screen; if (!s) { hqaLog('click: no screen'); return }
    var r1 = s.mouseClicked(Number(c[0]), Number(c[1]), 0); s.mouseReleased(Number(c[0]), Number(c[1]), 0)
    hqaLog('click ' + v + ' handled=' + r1 + ' now=' + (mc.screen ? String(mc.screen).replace(/@[0-9a-f]+$/, '') : 'none')); return }
  if (k === 'shot') { HQA_Screenshot.grab(mc.gameDirectory, 'qa_' + v + '.png', mc.getMainRenderTarget(), m => { }); hqaLog('shot ' + v); return }
  if (k === 'shaders') {
    var I = Java.loadClass('net.irisshaders.iris.Iris')
    if (v.indexOf('pack=') === 0) { I.getIrisConfig().setShaderPackName(v.substring(5)); I.getIrisConfig().setShadersEnabled(true) }
    else I.getIrisConfig().setShadersEnabled(v === 'on')
    I.getIrisConfig().save(); I.reload()
    hqaLog('shaders ' + v + ' -> enabled=' + I.getIrisConfig().areShadersEnabled() + ' pack=' + I.getIrisConfig().getShaderPackName().orElse('none')); return
  }
  if (k === 'reloadpacks') { mc.reloadResourcePacks(); hqaLog('resource reload'); return }
  if (k === 'pos') { hqaLog('pos ' + p.blockPosition() + ' dim=' + mc.level.dimension.location() + ' rd=' + mc.options.renderDistance().get() + ' fps=' + mc.getFps() + ' rain=' + mc.level.rainLevel + ' sections=' + mc.levelRenderer.getSectionStatistics()); return }
  if (k === 'state') { hqaLog('hand=' + p.getMainHandItem() + ' off=' + p.getOffhandItem() + ' screen=' + (mc.screen ? String(mc.screen).replace(/@[0-9a-f]+$/, '') : 'none') + ' camera=' + mc.options.getCameraType()); return }
  if (k === 'perf') {   // perf:<label>:<seconds>: one FPS reading per second (Minecraft's own counter), summarised
    var pv = v.split(':'); HQA.perf = { label: pv[0], left: Number(pv[1] || 30), fps: [] }; return
  }
  if (k === 'respawn') { p.respawn(); mc.setScreen(null); hqaLog('respawn requested'); return }
  if (k === 'particles') { var PS = Java.loadClass('net.minecraft.client.ParticleStatus'); mc.options.particles().set(PS.values()[Number(v)]); hqaLog('particles=' + mc.options.particles().get()); return }
  if (k === 'fog') { var RS = Java.loadClass('com.mojang.blaze3d.systems.RenderSystem'); hqaLog('fog ' + v + ' start=' + RS.getShaderFogStart() + ' end=' + RS.getShaderFogEnd() + ' shape=' + RS.getShaderFogShape() + ' rain=' + mc.level.rainLevel + ' rd=' + mc.options.renderDistance().get()); return }
  if (k === 'rebuild') { mc.levelRenderer.allChanged(); hqaLog('allChanged'); return }
  if (k === 'tip') {   // tooltip lines of the main-hand item, built through the normal ItemTooltipEvent path
    var TC = Java.loadClass('net.minecraft.world.item.Item$TooltipContext'), TF = Java.loadClass('net.minecraft.world.item.TooltipFlag')
    p.getMainHandItem().getTooltipLines(TC.of(mc.level), p, TF.NORMAL).forEach(c => hqaLog('  tip| ' + c.getString()))
    return
  }
  if (k === 'hud') { mc.options.hideGui = (v === 'off'); return }
  if (k === 'f3') { mc.getDebugOverlay().toggleOverlay(); return }
  if (k === 'quit') { mc.level.disconnect(); mc.disconnect(); hqaLog('disconnected'); return }
  hqaLog('unknown action ' + a)
}

function hqaPerfTick() {
  var P = HQA.perf; if (!P) return false
  if (HQA.t % 20 === 0) { P.fps.push(Client.getFps()); P.left-- }
  if (P.left > 0) return true
  var a = P.fps.slice().sort((x, y) => x - y), n = a.length
  HQA.perf = null   // cleared first: a failure below must never jam the queue (0.6.1 QA: Runtime is class-filtered)
  hqaLog('perf ' + P.label + ' seconds=' + n + ' fps min=' + a[0] + ' p5=' + a[Math.floor(n * 0.05)] + ' median=' + a[Math.floor(n / 2)] + ' max=' + a[n - 1] +
    ' (frame ms at median ' + (1000 / a[Math.floor(n / 2)]).toFixed(1) + ', at p5 ' + (1000 / a[Math.floor(n * 0.05)]).toFixed(1) + ')')
  return false
}

ClientEvents.tick(event => {
  if (!Client.player) return
  HQA.t++
  try { if (hqaPerfTick()) return } catch (e) { HQA.perf = null; hqaLog('ERROR perf: ' + e) }
  if (HQA.wait > 0) { HQA.wait--; return }
  if (HQA.queue.length) {
    var a = HQA.queue.shift()
    try { hqaRun(a) } catch (e) { hqaLog('ERROR ' + a + ': ' + e) }
    if (!HQA.queue.length) { hqaLog('done ' + HQA.last); hqaFlush() }
    return
  }
  if (HQA.t % 20 !== 0) return   // Level.getGameTime() is invisible to Rhino here (as on the server)
  var c = null
  try { c = JsonIO.read('horizon_qa/cmd.json') } catch (e) { return }
  if (!c || c.id === undefined || Number(c.id) === HQA.last) return
  HQA.last = Number(c.id); HQA.out = []
  c.actions.forEach(x => HQA.queue.push(String(x)))
  hqaLog('batch ' + HQA.last + ' (' + HQA.queue.length + ' actions)')
})
