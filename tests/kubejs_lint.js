// KubeJS 2101 lint (Node, no dependencies). Run: node tests/kubejs_lint.js
//
// Rule: event.cancel()/exit()/success() throw dev.latvian.mods.kubejs.event.EventExit (verified in
// kubejs-neoforge-2101.7.2 bytecode), so any statement after them in the same block never runs. 0.6.0 shipped
// `event.cancel()` as the first statement of the Survey Charter click handler and every real-player click did nothing
// (the FakePlayer selftest bypassed the event). Every such call must be followed directly by `}` (end of its block).
'use strict'
const fs = require('fs')
const path = require('path')

const root = path.join(__dirname, '..', 'kubejs')
const files = []
const walk = d => fs.readdirSync(d, { withFileTypes: true }).forEach(e => {
  const p = path.join(d, e.name)
  if (e.isDirectory()) walk(p)
  else if (/\.js$/.test(e.name)) files.push(p)
})
;['server_scripts', 'client_scripts', 'startup_scripts'].forEach(s => { const p = path.join(root, s); if (fs.existsSync(p)) walk(p) })

const stripComments = src => src.replace(/\/\*[\s\S]*?\*\//g, m => m.replace(/[^\n]/g, ' ')).replace(/\/\/[^\n]*/g, m => ' '.repeat(m.length))
let problems = 0, calls = 0
files.forEach(f => {
  const src = stripComments(fs.readFileSync(f, 'utf8'))
  const re = /\bevent\.(cancel|exit|success)\s*\(/g
  let m
  while ((m = re.exec(src))) {
    calls++
    let i = m.index + m[0].length, depth = 1
    while (i < src.length && depth) { if (src[i] === '(') depth++; else if (src[i] === ')') depth--; i++ }
    const rest = src.slice(i).replace(/^[\s;]*/, '')
    if (rest[0] !== '}') {
      problems++
      const line = src.slice(0, m.index).split('\n').length
      console.log(`FAIL ${path.relative(path.join(root, '..'), f)}:${line}: event.${m[1]}() is not the last statement (it throws EventExit; later code never runs)`)
    }
  }
})
console.log(`kubejs_lint: ${files.length} scripts, ${calls} exit calls, ${problems} problem(s)`)
process.exit(problems ? 1 : 0)
