"""Horizon dev tools: one CLI behind five on-demand skills (.claude/skills/horizon-*/SKILL.md).

  python scripts/horizon.py check quick|release       diff-driven generators + audits / full .mrpack + fresh Prism QA import
  python scripts/horizon.py qa loot|trophies|shaders  headless loot rolls / disposable-world trophy + route checks
  python scripts/horizon.py qa observe <key> [note]   record that a pending visual check was actually seen
  python scripts/horizon.py crash [path]              root error + implicated mods for the newest QA log / crash report
  python scripts/horizon.py find <id-or-name>         drops, recipes, quests, editable sources
  python scripts/horizon.py add boss|expedition|loot-family [--apply]   preview, or validate + write + regenerate

Raw output always goes to .horizon/logs/; stdout is capped at 15 lines (HORIZON_LINES overrides).
Exit codes: 0 ok, 1 check failed, 2 usage/prerequisite, 3 crash, 4 timeout.
Runtime writes (servers, worlds, scripts, configs) only ever land in .horizon/ or in a Prism instance whose name
contains "QA" (PH_QA_INSTANCE, default ProjectHorizon-QA). Env: PH_PRISM_DIR, PH_PRISM_EXE, PH_SERVER.
"""
import argparse, difflib, hashlib, json, os, re, shutil, subprocess, sys, time, zipfile
from pathlib import Path

PLAIN = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + "?" + chr(92)
ROOT = Path(LONG + str(PLAIN)) if os.name == "nt" and not str(PLAIN).startswith(LONG) else PLAIN
WORK = Path(os.environ["PH_WORK"]) if os.environ.get("PH_WORK") else ROOT / ".horizon"
CAP = int(os.environ.get("HORIZON_LINES", 15))
EX_OK, EX_FAIL, EX_USAGE, EX_CRASH, EX_TIMEOUT = 0, 1, 2, 3, 4

# generators in build_all.py order (resolve needs the network and is opt-in)
ORDER = ["check_deps", "index_ids", "audit_loot", "gen_assets", "gen_datapack", "gen_headquarters", "hq_sim", "gen_quests", "audit_quests",
         "gen_resourcepack", "patch_configs", "gen_profiles", "gen_docs", "gen_checklist"]
DOWN = {"index_ids": ["gen_datapack", "gen_headquarters", "gen_quests"], "audit_loot": ["gen_datapack"], "gen_assets": ["gen_quests"],
        "gen_datapack": ["gen_headquarters", "gen_quests"], "gen_headquarters": ["hq_sim", "gen_quests"], "gen_quests": ["audit_quests"]}
RULES = [  # changed source path -> generators that read it (docs/BUILDING.md table)
    (r"^manifests/roster\.json$", ["gen_docs", "gen_checklist"]),
    (r"^manifests/lock\.json$", ["check_deps", "index_ids", "audit_loot", "gen_datapack", "gen_docs", "gen_checklist"]),
    (r"^manifests/(loot_families|expeditions|loot_calibration)\.json$", ["gen_datapack"]),
    (r"^manifests/legends\.json$", ["gen_assets", "gen_datapack", "gen_headquarters"]),
    (r"^manifests/headquarters\.json$", ["gen_assets", "gen_headquarters"]),
    (r"^art/horizon/", ["gen_assets"]),
    (r"^kubejs/server_scripts/horizon_headquarters\.js$", ["hq_sim"]),
    (r"^tests/hq_sim\.js$", ["hq_sim"]),
    (r"^scripts/quest_campaign\.py$", ["gen_quests"]),
    (r"^manifests/(ports_lock|expansion_audit|validation|baseline_slugs)\.json$", ["gen_checklist"]),
    (r"^profiles/(?!shader_options)[^/]+\.json$", ["gen_profiles"]),
]
OUTPUT_RX = re.compile(r"^(config/heracles/|kubejs/(assets|startup_scripts|client_scripts)/|kubejs/\.generated|resourcepacks/|schematics/|"
                       r"datapacks/\.generated|docs/(LOOT_BUDGET|MODLIST|EXPANSION_CHECKLIST|HEADQUARTERS|HQ_PLANS|HQ_GRAPH)\.md$|"
                       r"manifests/(ids|loot_audit|loot_report|salvage_report|deps_report|config_changes|a3d_report|expansion_probe)\.|"
                       r"profiles/shader_options\.json$|\.horizon/)")


# ---------- plumbing ----------
def _rel(p):
    try:
        return Path(p).relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def out(lines, log=None):
    lines = [str(l) for l in lines]
    room = CAP - (1 if log else 0)
    if len(lines) > room:
        lines = lines[:room - 1] + [f"... +{len(lines) - room + 1} more"]
    if log:
        lines.append(f"log: {_rel(log)}")
    print("\n".join(lines))


def die(msg, code=EX_USAGE):
    out([msg])
    sys.exit(code)


def logfile(tag):
    d = WORK / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{time.strftime('%Y%m%d-%H%M%S')}-{tag}.log"


def sh(args, log, timeout=None, cwd=None, env=None):
    """Run a command, append its output to `log`, return (rc, tail lines). rc=-9 on timeout."""
    with open(log, "ab") as f:
        f.write(f"\n$ {' '.join(map(str, args))}\n".encode())
        try:
            p = subprocess.run([str(a) for a in args], cwd=cwd or ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               timeout=timeout, env=env)
            rc, data = p.returncode, p.stdout
        except subprocess.TimeoutExpired as e:
            rc, data = -9, e.stdout or b""
        f.write(data)
    return rc, data.decode("utf-8", "replace").strip().splitlines()[-6:]


def jload(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def git_changed():
    def g(*a):
        try:
            r = subprocess.run(["git", "-C", str(PLAIN), *a], capture_output=True, text=True)
        except OSError as e:
            die(f"git unavailable: {e}", EX_FAIL)
        if r.returncode:
            die(f"git {' '.join(a)} failed (rc {r.returncode}): {" ".join((r.stderr or r.stdout).split())[:160]}", EX_FAIL)
        return [l.strip().strip('"') for l in r.stdout.splitlines() if l.strip()]
    return sorted(set(g("diff", "--name-only", "HEAD")) | set(g("ls-files", "-o", "--exclude-standard")))


def evidence(key=None, status=None, detail="", log=None):
    p = WORK / "qa" / "evidence.json"
    data = json.loads(p.read_text()) if p.exists() else {}
    if key:
        data[key] = {"status": status, "detail": detail, "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                     "log": _rel(log) if log else None}
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=1))
    return data


# ---------- Prism ----------
def prism_dir():
    return Path(os.environ.get("PH_PRISM_DIR") or Path(os.environ.get("APPDATA", "~")) / "PrismLauncher")


def prism_exe():
    return Path(os.environ.get("PH_PRISM_EXE") or Path(os.environ.get("LOCALAPPDATA", "~")) / "Programs/PrismLauncher/prismlauncher.exe")


def inst_running(name):
    """True if any Minecraft JVM (javaw) is alive. Prism launches with an argument file, so the command line does not name the
    instance; treating any javaw as 'running' also stops QA from launching next to a game the user is playing."""
    r = subprocess.run(["powershell", "-NoProfile", "-Command", "if (Get-Process javaw -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"],
                       stderr=subprocess.DEVNULL)
    return r.returncode == 0


def qa_name():
    n = os.environ.get("PH_QA_INSTANCE", "ProjectHorizon-QA")
    if "QA" not in n:
        die(f"refusing: PH_QA_INSTANCE {n!r} must contain 'QA' (runtime writes stay in QA copies)")
    return n


def qa_instance(must_exist=True):
    n = qa_name()
    inst = prism_dir() / "instances" / n
    if must_exist and not (inst / "minecraft").exists():
        die(f"QA instance {n!r} not found. Create it: python scripts/horizon.py check release")
    return n, inst


def launch_and_watch(name, inst, world, done_rx, timeout, log):
    """Start ONE Prism instance (never stops anything) and watch its log. Returns (exit_code, matching lines)."""
    mc = inst / "minecraft"
    L = mc / "logs" / "latest.log"
    cr = mc / "crash-reports"
    if inst_running(name):
        die(f"{name} is already running - close it first (nothing was stopped)")
    before = set(p.name for p in cr.glob("*")) if cr.exists() else set()
    if L.exists():
        shutil.move(str(L), str(mc / "logs" / "previous-qa.log"))
    args = [str(prism_exe()), "--launch", name] + (["--world", world] if world else [])
    subprocess.Popen(args)
    t0, hits = time.time(), []
    while time.time() - t0 < timeout:
        time.sleep(5)
        text = L.read_text(encoding="utf-8", errors="replace") if L.exists() else ""
        hits = [l for l in text.splitlines() if "[horizon-qa]" in l]
        with open(log, "w", encoding="utf-8") as f:
            f.write("\n".join(hits))
        if re.search(done_rx, text):
            return EX_OK, hits
        if cr.exists() and set(p.name for p in cr.glob("*")) - before:
            return EX_CRASH, hits
        if time.time() - t0 > 90 and int(time.time() - t0) % 30 < 5 and not inst_running(name):
            return EX_CRASH, hits
    return EX_TIMEOUT, hits


# ---------- check ----------
def run_steps(steps, log):
    res = []
    for s in steps:
        t0 = time.time()
        if s == "hq_sim":   # node test of the headquarters ledger core
            nodeexe = shutil.which("node")
            if not nodeexe:
                res.append("SKIP hq_sim (node not installed: headquarters ledger tests NOT run)")
                continue
            rc, tail = sh([nodeexe, "tests/hq_sim.js"], log)
        else:
            rc, tail = sh([sys.executable, f"scripts/{s}.py"] + (["--frozen"] if s == "resolve" else []), log)
        res.append(f"{'ok  ' if rc == 0 else 'FAIL'} {s} ({time.time() - t0:.0f}s)")
        if rc:
            return rc, res + ["  " + t[:160] for t in tail[-4:]]
    return 0, res


def plan_quick(files, net=False, configs=False):
    owned = set()
    for rel in ("datapacks/.generated.json", "datapacks/.generated-hq.json", "kubejs/.generated-assets.json", "kubejs/.generated-hq.json"):
        p = ROOT / rel
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            base = rel.split("/")[0]
            owned |= {f"{base}/{x}" if not x.startswith(base) else x for x in (d if isinstance(d, list) else d.get("files", d))}
    seeds, generated, uncovered = set(), 0, []
    for f in files:
        gen = {f"scripts/{g}.py": g for g in ORDER}.get(f)
        if gen:
            seeds.add(gen)
        elif OUTPUT_RX.match(f) or f in owned or f.startswith("datapacks/") and f in owned:
            generated += 1
        else:
            hit = next((g for rx, g in RULES if re.match(rx, f)), None)
            if hit:
                seeds.update(hit)
            elif f.startswith(("datapacks/", "kubejs/", "config/", "options/", "manifests/")):
                uncovered.append(f)
    if "manifests/roster.json" in files and net:
        seeds.add("resolve")
    if configs:
        seeds.add("patch_configs")
    todo, stack = set(seeds), list(seeds)
    while stack:
        for d in DOWN.get(stack.pop(), []):
            if d not in todo:
                todo.add(d); stack.append(d)
    if "gen_quests" in todo:
        todo.add("audit_quests")
    if "patch_configs" in todo and not configs and "scripts/patch_configs.py" not in files:
        todo.discard("patch_configs")
    steps = (["resolve"] if "resolve" in todo else []) + [s for s in ORDER if s in todo]
    return steps, generated, uncovered


def cmd_check(a):
    if a.mode == "quick":
        files = [f.strip() for f in a.files.split(",") if f.strip()] if a.files else git_changed()
        steps, generated, uncovered = plan_quick(files, a.net, a.configs)
        head = [f"changed {len(files)} (generated outputs ignored: {generated}); plan: {' > '.join(steps) or 'none'}"]
        tail = []
        if uncovered:
            hint = " (hand-written data/scripts: run /horizon-qa loot)" if any(u.startswith(("datapacks/", "kubejs/server", "config/")) for u in uncovered) else ""
            tail.append(f"no generator covers {len(uncovered)}: {', '.join(uncovered[:3])}{'...' if len(uncovered) > 3 else ''}{hint}")
        if "manifests/roster.json" in files and not a.net:
            tail.append("roster changed: run resolve.py --frozen (network) or pass --net")
        log = logfile("check-quick")
        if a.dry or not steps:
            return out(head + tail, log if a.dry else None)
        rc, res = run_steps(steps, log)
        out(head + res + tail, log)
        sys.exit(EX_OK if rc == 0 else EX_FAIL)
    # release: existing full build, then a fresh Prism QA import
    log = logfile("check-release")
    if a.dry:
        return out(["plan: build_all.py --mrpack > import dist/ProjectHorizon-<ver>.mrpack into a fresh Prism QA instance",
                    f"QA instance: {qa_name()} in {prism_dir() / 'instances'}"])
    t0 = time.time()
    rc, tail = sh([sys.executable, "scripts/build_all.py", "--mrpack"] + (["--offline"] if a.offline else []), log, timeout=7200)
    if rc:
        return out([f"FAIL build_all (rc {rc})"] + ["  " + t[:160] for t in tail[-4:]], log) or sys.exit(EX_FAIL if rc > 0 else EX_TIMEOUT)
    pack = ROOT / "dist" / f"ProjectHorizon-{(ROOT / 'VERSION').read_text().strip()}.mrpack"
    code, lines = import_qa(pack, log)
    evidence("release", "pass" if code == EX_OK else "fail", lines[-1], log)
    out([f"build ok ({time.time() - t0:.0f}s) {pack.name}"] + lines, log)
    sys.exit(code)


def verify_candidate(cand, pack, idx):
    """Every index file (sha1 + sha512) and every override in the pack must be in the candidate, byte-exact. Returns bad paths."""
    mc, bad = cand / "minecraft", []
    for f in idx["files"]:
        p = mc / f["path"]
        p = p if p.exists() else p.with_name(p.name + ".disabled")
        if not p.is_file():
            bad.append(f["path"] + " (missing)")
            continue
        data = p.read_bytes()
        if hashlib.sha1(data).hexdigest() != f["hashes"]["sha1"] or hashlib.sha512(data).hexdigest() != f["hashes"]["sha512"]:
            bad.append(f["path"])
    with zipfile.ZipFile(pack) as z:
        for i in z.infolist():
            m = re.match(r"(client-)?overrides/(.+)", i.filename)
            if m and not i.is_dir():
                p = mc / m.group(2)
                if not p.is_file() or p.read_bytes() != z.read(i):
                    bad.append(m.group(2) + " (override)")
    return bad


def import_qa(pack, log, timeout=900, poll=5):
    name = qa_name()
    inst_root = prism_dir() / "instances"
    final = inst_root / name
    if not prism_exe().exists():
        return EX_USAGE, [f"Prism not found at {prism_exe()} (set PH_PRISM_EXE)"]
    if inst_running(name):
        return EX_USAGE, [f"{name} is running - close it first (nothing was stopped)"]
    with zipfile.ZipFile(pack) as z:
        idx = json.loads(z.read("modrinth.index.json"))
    before = {p.name for p in inst_root.iterdir()} if inst_root.exists() else set()
    subprocess.Popen([str(prism_exe()), "--import", str(pack)])
    t0, cand, bad = time.time(), None, ["no new instance appeared"]
    while time.time() - t0 < timeout:
        time.sleep(poll)
        fresh = [p for p in inst_root.iterdir() if p.name not in before and (p / "minecraft").exists()] if inst_root.exists() else []
        if len(fresh) > 1:
            return EX_FAIL, [f"ambiguous import: {len(fresh)} new instances {[p.name for p in fresh][:3]}; existing {name} untouched"]
        if fresh:
            cand = fresh[0]
            bad = verify_candidate(cand, pack, idx)
            if not bad:
                break
    else:
        return EX_TIMEOUT, [f"import not verified in {timeout}s (candidate {cand.name if cand else 'none'}); {name} untouched; bad: {bad[:3]}"]
    # only now, with the exact candidate fully verified, replace the old QA copy (and its disposable worlds)
    if final.exists():
        shutil.rmtree(final)
    cand.rename(final)
    cfg = final / "instance.cfg"
    if cfg.exists():
        cfg.write_text(re.sub(r"(?m)^name=.*$", f"name={name}", cfg.read_text(encoding="utf-8")), encoding="utf-8")
    return EX_OK, [f"import {name}: {len(idx['files'])}/{len(idx['files'])} index hashes + overrides match"]


# ---------- qa ----------
def link_or_copy(src, dst):
    if dst.exists():
        return
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)], capture_output=True)
    else:
        os.symlink(src, dst, target_is_directory=True)
    if not dst.exists():
        shutil.copytree(src, dst)


def qa_server(src):
    src, dst = Path(src), WORK / "qa-server"
    if not (src / "server.properties").exists():
        die(f"{src} is not a server dir (no server.properties). Use --server or PH_SERVER")
    if str(dst) in str(src):
        die("server dir must not be inside .horizon")
    dst.mkdir(parents=True, exist_ok=True)
    for e in src.iterdir():
        t = dst / e.name
        if e.is_dir():
            if e.name in ("mods", "libraries"):
                link_or_copy(e, t)
            elif e.name not in ("logs", "crash-reports", "cache", ".git") and not (e / "level.dat").exists():
                shutil.copytree(e, t, dirs_exist_ok=True)
        else:
            shutil.copy2(e, t)
    for s, d in (("config", "config"), ("kubejs", "kubejs"), ("datapacks", "kubejs/data")):
        shutil.copytree(ROOT / s, dst / d, dirs_exist_ok=True)
    for w in dst.glob("qa-*"):
        if (w / "level.dat").exists():
            shutil.rmtree(w)
    return dst


def pregen_server(src):
    """A throwaway QA server folder with Chunky added (QA only; Chunky is not part of the pack). mods/ is a real copy so the
    shared server dir is never modified."""
    jar = WORK / "dl" / "Chunky-NeoForge-1.4.23.jar"
    if not jar.exists():
        die(f"{jar} missing (download Chunky-NeoForge-1.4.23.jar from Modrinth)")
    qs = qa_server(src)
    dst = WORK / "qa-server-chunky"
    dst.mkdir(parents=True, exist_ok=True)
    for e in qs.iterdir():
        t = dst / e.name
        if e.name in ("logs", "crash-reports", "cache", "mods") or e.name.startswith("qa-"):
            continue
        if e.name == "libraries":
            link_or_copy(e, t)
        elif e.is_dir():
            shutil.copytree(e, t, dirs_exist_ok=True)
        else:
            shutil.copy2(e, t)
    if not (dst / "mods").exists():
        shutil.copytree(Path(src) / "mods", dst / "mods")
    shutil.copy2(jar, dst / "mods" / jar.name)
    return dst


def ensure_world(inst, name, seed, server, fresh, log, pregen=False):
    dst = inst / "minecraft" / "saves" / name
    tpl = WORK / "qa" / f"world-{name}-{hashlib.md5(seed.encode()).hexdigest()[:8]}"   # pristine copy: regenerating it every run costs minutes
    if fresh and dst.exists():
        shutil.rmtree(dst)
    if dst.exists():
        return
    if tpl.exists():
        shutil.copytree(tpl, dst)
        return
    if not server:
        die("no QA world yet: pass --server <dedicated server dir> (used once to generate it) or PH_SERVER")
    qs = pregen_server(server) if pregen else qa_server(server)
    noop = ROOT / "tests/pregen.txt" if pregen else WORK / "qa" / "noop.txt"
    noop.parent.mkdir(parents=True, exist_ok=True)
    if not pregen:
        noop.write_text("# generate world only\n")
    rc, _ = sh([sys.executable, "scripts/server_test.py", qs, "qa-" + name, seed, noop], log, timeout=7200)
    if rc or not (qs / ("qa-" + name) / "level.dat").exists():
        die("QA world generation failed", EX_CRASH)
    shutil.copytree(qs / ("qa-" + name), dst)
    (dst / "session.lock").unlink(missing_ok=True)
    confirm_experimental(dst / "level.dat")
    shutil.copytree(dst, tpl, dirs_exist_ok=True)


def confirm_experimental(level_dat):
    """Pre-accept the "Worlds using Experimental Settings" dialog, which would otherwise wait for a click on every fresh
    QA world copy (modded worlds are flagged experimental). Flips the NBT byte confirmedExperimentalSettings 0 -> 1."""
    import gzip
    raw = gzip.decompress(level_dat.read_bytes())
    key = b"\x01\x00\x1dconfirmedExperimentalSettings"
    i = raw.find(key)
    if i >= 0 and raw[i + len(key)] == 0:
        raw = raw[:i + len(key)] + b"\x01" + raw[i + len(key) + 1:]
        level_dat.write_bytes(gzip.compress(raw))


def kjs_qa(inst, body):
    p = inst / "minecraft" / "kubejs" / "server_scripts" / "zz_horizon_qa.js"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("// QA-only (written by scripts/horizon.py into a QA instance, never shipped)\n" + body, encoding="utf-8")


KJS_RUN = """
const run = (s, c) => { try { return s.runCommandSilent(c) } catch (e) { return 'ERR ' + e } }
const say = (k, v) => console.log('[horizon-qa] ' + k + '=' + v)
let hqaRan = false
"""


def trophy_script(bosses):
    return KJS_RUN + f"""
const BOSSES = {json.dumps(bosses)}
PlayerEvents.loggedIn(ev => {{
  if (hqaRan) return
  hqaRan = true
  const s = ev.server
  s.scheduleInTicks(100, () => {{
    run(s, 'gamemode creative @p')
    BOSSES.forEach(b => {{
      const at = 'execute as @p at @s '
      const sp = '~' + (8 + b.i * 20) + ' ~ ~8'
      run(s, at + 'run summon ' + b.id + ' ' + sp)
      say('summon:' + b.n, run(s, at + 'positioned ' + sp + ' if entity @e[type=' + b.id + ',distance=..6]'))
      say('advancement:' + b.n, run(s, 'advancement grant @p only horizon:legend/' + b.n))
      say('trophy-item:' + b.n, run(s, 'execute as @p if items entity @s container.* horizon:trophy_' + b.n))
      const bp = '~' + (3 + b.i * 20) + ' ~ ~-6'
      run(s, at + 'run setblock ' + bp + ' horizon:trophy_' + b.n)
      say('trophy-block:' + b.n, run(s, at + 'if block ' + bp + ' horizon:trophy_' + b.n))
    }})
    say('done', 1)
  }})
}})
"""


def route_script(route):
    return KJS_RUN + f"""
const ROUTE = {json.dumps(route['waypoints'])}
PlayerEvents.loggedIn(ev => {{
  if (hqaRan) return
  hqaRan = true
  const s = ev.server
  run(s, 'time set day'); run(s, 'weather clear')
  ROUTE.forEach((w, i) => s.scheduleInTicks(100 + i * {route['dwell_ticks']}, () => {{
    run(s, 'gamemode creative @p')
    run(s, 'tp @p ' + w.x + ' ' + w.y + ' ' + w.z + ' ' + w.yaw + ' ' + w.pitch)
    say('waypoint:' + w.name, i + 1 + '/' + ROUTE.length)
    if (i === ROUTE.length - 1) say('done', 1)
  }}))
}})
"""


PERF_SERVER = """
const PT = []
let lastMs = 0
let perfOn = false
ServerEvents.tick(e => {
  const n = Utils.getSystemTime()
  if (perfOn && lastMs) PT.push(n - lastMs)
  lastMs = n
})
const pct = (a, q) => { const b = a.slice().sort((x, y) => x - y); return b.length ? b[Math.min(b.length - 1, Math.floor(q * b.length))] : -1 }
const perfServerSummary = () => {
  say('ticks', PT.length); say('tick_p50', pct(PT, 0.5)); say('tick_p95', pct(PT, 0.95)); say('tick_p99', pct(PT, 0.99))
  say('ticks_over50', PT.filter(x => x > 50).length); say('tick_max', pct(PT, 1))
}
"""

PERF_CLIENT = """
// QA-only frame-time recorder (written by scripts/horizon.py into a QA instance, never shipped). 1 ms clock resolution.
const FT = []
let lastF = 0, on = false, reported = false
const pct = (a, q) => { const b = a.slice().sort((x, y) => x - y); return b.length ? b[Math.min(b.length - 1, Math.floor(q * b.length))] : -1 }
const say = (k, v) => console.log('[horizon-qa] ' + k + '=' + v)
NativeEvents.onEvent(Java.loadClass('net.neoforged.neoforge.client.event.RenderFrameEvent$Pre'), e => {
  const n = Utils.getSystemTime()
  if (on && lastF) FT.push(n - lastF)
  lastF = n
})
NativeEvents.onEvent(Java.loadClass('net.neoforged.neoforge.client.event.ClientChatReceivedEvent'), e => {
  const m = String(e.getMessage().getString())
  if (m.indexOf('HQA-START') >= 0) on = true
  if (m.indexOf('HQA-END') >= 0 && !reported) {
    on = false; reported = true
    say('frames', FT.length); say('frame_p50', pct(FT, 0.5)); say('frame_p95', pct(FT, 0.95))
    say('frame_p99', pct(FT, 0.99)); say('frames_over50', FT.filter(x => x > 50).length); say('frame_max', pct(FT, 1))
    say('perf-done', 1)
  }
})
"""


def perf_route_script(route, dwell):
    n = len(route["waypoints"])
    end = 100 + n * dwell
    return KJS_RUN + PERF_SERVER + f"""
const ROUTE = {json.dumps(route['waypoints'])}
PlayerEvents.loggedIn(ev => {{
  if (hqaRan) return
  hqaRan = true
  const s = ev.server
  run(s, 'time set day'); run(s, 'weather clear')
  s.scheduleInTicks(100, () => {{ perfOn = true; run(s, 'tellraw @a {{"text":"HQA-START"}}') }})
  ROUTE.forEach((w, i) => s.scheduleInTicks(100 + i * {dwell}, () => {{
    run(s, 'gamemode creative @p')
    run(s, 'tp @p ' + w.x + ' ' + w.y + ' ' + w.z + ' ' + w.yaw + ' ' + w.pitch)
    say('waypoint:' + w.name, i + 1 + '/' + ROUTE.length)
  }}))
  s.scheduleInTicks({end}, () => {{ perfOn = false; perfServerSummary(); run(s, 'tellraw @a {{"text":"HQA-END"}}') }})
}})
"""


def cmd_perf(a, inst, n, server, log):
    route = jload("tests/qa_route.json")
    world = "HorizonQA-perf" + ("-pregen" if a.pregen else "")
    ensure_world(inst, world, route["seed"], server, a.fresh, log, pregen=a.pregen)
    cfgd = inst / "minecraft" / "config"
    ip = cfgd / "iris.properties"
    txt = ip.read_text(encoding="utf-8") if ip.exists() else "enableShaders=true\nshaderPack=\n"
    if a.shader == "off":
        txt = re.sub(r"(?m)^enableShaders=.*$", "enableShaders=false", txt)
    else:
        pack = next((x for x in jload("manifests/lock.json")["shaders"] if a.shader in x["slug"]), None)
        if not pack:
            die(f"no shader matching {a.shader!r}")
        txt = re.sub(r"(?m)^shaderPack=.*$", f"shaderPack={pack['file']}", txt)
        txt = re.sub(r"(?m)^enableShaders=.*$", "enableShaders=true", txt)
    ip.write_text(txt, encoding="utf-8")
    op = inst / "minecraft" / "options.txt"   # QA instance only: an unfocused window would otherwise pause the integrated server
    ot = op.read_text(encoding="utf-8") if op.exists() else ""
    ot = re.sub(r"(?m)^pauseOnLostFocus:.*$", "pauseOnLostFocus:false", ot) if re.search(r"(?m)^pauseOnLostFocus:", ot) else ot + "pauseOnLostFocus:false" + chr(10)
    op.write_text(ot, encoding="utf-8")
    wg = cfgd / "voxyworldgenv2.json"
    j = json.loads(wg.read_text(encoding="utf-8"))
    if a.voxy_radius is not None:
        j["generationRadius"] = a.voxy_radius
    if a.voxy_tasks is not None:
        j["maxActiveTasks"] = a.voxy_tasks
    wg.write_text(json.dumps(j, indent=2), encoding="utf-8")
    kjs_qa(inst, perf_route_script(route, a.dwell))
    cs = inst / "minecraft" / "kubejs" / "client_scripts" / "zz_horizon_perf.js"
    cs.write_text(PERF_CLIENT, encoding="utf-8")
    try:
        code, hits = launch_and_watch(n, inst, world, r"\[horizon-qa\] perf-done=1", a.timeout, log)
    finally:
        cs.unlink(missing_ok=True)
    kv = qa_summary(code, hits, log)
    rec = {"label": a.label, "shader": a.shader, "voxy_radius": j["generationRadius"], "voxy_tasks": j["maxActiveTasks"],
           "dwell": a.dwell, "exit": code, **{k: v for k, v in kv.items() if k.startswith(("frame", "tick"))}}
    with open(WORK / "perf_results.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    out([f"perf[{a.label}] exit {code}: " + ", ".join(f"{k}={rec[k]}" for k in rec if k.startswith(("frame", "tick")))], log)
    sys.exit(code)



def qa_summary(code, hits, log):
    kv = {m.group(1): m.group(2) for l in hits for m in [re.search(r"\[horizon-qa\] ([\w.:-]+)=(\S+)", l)] if m}
    return kv


def cmd_qa(a):
    if a.what == "observe":
        d = evidence()
        if a.key not in d:
            die(f"unknown key {a.key!r}; pending: {[k for k, v in d.items() if v['status'] == 'pending-visual'][:6]}")
        evidence(a.key, "observed", a.note or "observed by user", None)
        return out([f"{a.key}: observed"])
    server = a.server or os.environ.get("PH_SERVER")
    log = logfile("qa-" + a.what)
    if a.what == "loot":
        if not server:
            die("pass --server <dedicated server dir> or set PH_SERVER")
        cmds = Path(a.cmds) if a.cmds else ROOT / "tests/server_smoke.txt"
        qs = qa_server(server)
        rc, _ = sh([sys.executable, "scripts/server_test.py", qs, "qa-loot", a.seed, cmds], log, timeout=a.timeout)
        slog = Path(qs) / "logs" / "test-qa-loot.log"   # the server's own console log is the evidence; stdout capture can be empty
        text = log.read_text(encoding="utf-8", errors="replace") + "\n" + (slog.read_text(encoding="utf-8", errors="replace") if slog.exists() else "")
        lines = text.splitlines()
        known = r"wares:chests|Sculk Sensor|incendium:upgrade_elytra"   # docs/KNOWN_ISSUES.md #4 and upstream noise
        bad = [l for l in lines if re.search(r"Failed to (load|parse)|Couldn't parse|Parsing error|SERVER DID NOT START", l) and not re.search(known, l)]
        audits = [l for l in lines if "[horizon-audit]" in l and "tables" in l]
        expected = sum(bool(re.search(r"horizon audit|^LOCATEAUDIT ", c.strip())) for c in cmds.read_text(encoding="utf-8").splitlines() if not c.strip().startswith("#"))
        timed = [l for l in lines if re.match(r"(WAITLOG|LOCATE) .*TIMEOUT", l)]
        code = (EX_TIMEOUT if rc == -9 or timed else EX_CRASH if "SERVER DID NOT START" in text
                else EX_FAIL if rc or bad or expected == 0 or len(audits) < expected else EX_OK)
        if expected == 0:
            bad.append("commands file has no audit command")
        elif len(audits) < expected:
            bad.append(f"audits missing: {len(audits)}/{expected} summaries")
        bad += timed
        evidence("loot", "pass" if code == EX_OK else "fail", f"{len(audits)} audit lines, {len(bad)} load errors", log)
        out([f"loot: {'PASS' if code == EX_OK else 'FAIL'} cmds={cmds.name} seed={a.seed} audit-lines={len(audits)} load-errors={len(bad)}"]
            + [b[:150] for b in bad[:3]] + [l[:150] for l in audits[:3]], log)
        sys.exit(code)
    n, inst = qa_instance()
    if a.what == "trophies":
        world = "HorizonQA-trophies"
        ensure_world(inst, world, a.seed, server, a.fresh, log)
        legends = jload("manifests/legends.json")["bosses"]
        bosses = [{"id": b["id"], "n": b["id"].split(":")[1]} for b in legends if b["id"].split(":")[1] in ("yeti", "sun_spirit")]
        for i, b in enumerate(bosses):
            b["i"] = i
        if len(bosses) != 2:
            die("yeti / sun_spirit missing from manifests/legends.json")
        kjs_qa(inst, trophy_script(bosses))
        deadline = r"\[horizon-qa\] done=1"
        code, hits = launch_and_watch(n, inst, world, deadline, a.timeout, log)
        kv = qa_summary(code, hits, log)
        lines = []
        for b in bosses:
            ok = {k: kv.get(f"{k}:{b['n']}") for k in ("summon", "advancement", "trophy-item", "trophy-block")}
            good = all(v not in (None, "0") and not str(v).startswith("ERR") for v in ok.values())
            evidence(f"trophies:{b['n']}:logic", "pass" if good else "fail", json.dumps(ok), log)
            evidence(f"trophies:{b['n']}:visual", "pending-visual", "trophy plaque emblem + relic tooltip, in game", None)
            lines.append(f"{b['n']}: {'logic PASS' if good else 'logic FAIL ' + json.dumps(ok)}; visual PENDING")
        out([f"trophies: exit {code} world={world}" + (" (left open for the visual check)" if code == EX_OK else "")] + lines
            + ["observe: horizon.py qa observe trophies:<boss>:visual"], log)
        sys.exit(code if code else (EX_OK if all("PASS" in l for l in lines) else EX_FAIL))
    if a.what == "perf":
        return cmd_perf(a, inst, n, server, log)
    # shaders: fixed seed, fixed waypoints, one shader per run; screenshots are taken by the observer
    route = jload("tests/qa_route.json")
    lock = jload("manifests/lock.json")
    pack = next((s for s in lock["shaders"] if a.shader in s["slug"]), None)
    if not pack:
        die(f"no shader matching {a.shader!r}; lock has {[s['slug'] for s in lock['shaders']]}")
    world = "HorizonQA-shaders"
    ensure_world(inst, world, route["seed"], server, a.fresh, log)
    cfg = inst / "minecraft" / "config" / "iris.properties"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    txt = cfg.read_text(encoding="utf-8") if cfg.exists() else "enableShaders=true\nshaderPack=\n"
    txt = re.sub(r"(?m)^shaderPack=.*$", f"shaderPack={pack['file']}", txt)
    cfg.write_text(re.sub(r"(?m)^enableShaders=.*$", "enableShaders=true", txt), encoding="utf-8")
    kjs_qa(inst, route_script(route))
    code, hits = launch_and_watch(n, inst, world, r"\[horizon-qa\] done=1", a.timeout, log)
    kv = qa_summary(code, hits, log)
    seen = [w["name"] for w in route["waypoints"] if f"waypoint:{w['name']}" in kv]
    missing = [w["name"] for w in route["waypoints"] if w["name"] not in seen]
    if code == EX_OK and missing:
        code = EX_FAIL
    evidence(f"shaders:{pack['slug']}:route", "pass" if code == EX_OK and len(seen) == len(route["waypoints"]) else "fail",
             f"{len(seen)}/{len(route['waypoints'])} waypoints", log)
    for w in route["waypoints"]:
        evidence(f"shaders:{pack['slug']}:{w['name']}", "pending-visual", "F2 screenshot; compare Voxy LOD edge, water, shadows against other shader", None)
    out([f"shaders {pack['slug']}: exit {code} route {len(seen)}/{len(route['waypoints'])} seed={route['seed']}",
         *([f"MISSING waypoints: {missing}"] if missing else []),
         f"visual: {len(route['waypoints'])} waypoints PENDING; shots land in the QA instance screenshots/",
         "rerun with --shader <other> then compare; observe: horizon.py qa observe <key>"], log)
    sys.exit(code)


# ---------- crash ----------
def newest_artifact(explicit=None):
    if explicit:
        return Path(explicit)
    cands = []
    try:
        _, inst = qa_instance(False)
        cands += list((inst / "minecraft" / "crash-reports").glob("*.txt")) + [inst / "minecraft/logs/latest.log", inst / "minecraft/logs/previous-qa.log"]
    except SystemExit:
        pass
    qs = WORK / "qa-server"
    cands += list(qs.glob("crash-reports/*.txt")) + list(qs.glob("logs/*.log")) if qs.exists() else []
    cands = [c for c in cands if c.exists()]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def root_error(lines):
    pats = [r"Missing or unsupported mandatory dependencies", r"InvalidMixinException|Mixin (apply|transformation).*failed|Critical injection failure",
            r"^Caused by: ", r"/FATAL\]", r"^[\w.$]+(Exception|Error)\b.*", r"/ERROR\]"]
    for i, p in enumerate(pats):
        idx = [n for n, l in enumerate(lines) if re.search(p, l.strip() if i in (2, 4) else l)]
        if idx:
            n = idx[-1] if i == 2 else idx[0]
            if i == 2:  # deepest "Caused by" of the first contiguous trace
                first = idx[0]
                run = [x for x in idx if x - first < 400]
                n = run[-1]
            return n
    return None


def cmd_crash(a):
    f = newest_artifact(a.path)
    if not f or not f.exists():
        die("no QA log or crash report found (run a /horizon-qa first or pass a path)")
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    n = root_error(lines)
    res = [f"file: {f.name} ({time.strftime('%Y-%m-%d %H:%M', time.localtime(f.stat().st_mtime))})"]
    if n is None:
        return out(res + ["no root error found (no exception, FATAL or ERROR line)", f"full: {f}"])
    res.append("root: " + re.sub(r"^\[[^\]]*\]\s*", "", lines[n].strip())[:200])
    window = "\n".join(lines[max(0, n - 12):n + 14])
    mods = []
    for m in re.finditer(r"^\s*([^\n(]+?) \(([\w.-]+)\), Version: (\S+)", "\n".join(lines), re.M):
        mods.append(f"{m.group(2)} {m.group(3)}")
    if not mods:
        norm = re.sub(r"[^a-z0-9]", "", window.lower())
        for m in jload("manifests/lock.json")["mods"]:
            s = re.sub(r"[^a-z0-9]", "", m["slug"].lower())
            if len(s) >= 4 and s in norm:
                mods.append(f"{m['slug']} {m.get('version', '?')}")
        mods = [x + " (heuristic)" for x in mods[:4]]
    res.append("mods: " + (", ".join(dict.fromkeys(mods[:5])) if mods else "unknown"))
    res += ["  | " + l.strip()[:150] for l in lines[n:n + 4] if l.strip()]
    out(res + [f"full: {f}"])


# ---------- horizon ids ----------
def horizon_items():
    """horizon:* ids are registered by KubeJS/generators, not in ids.json."""
    ids = set()
    for rel in ("manifests/loot_families.json", "manifests/legends.json", "manifests/expeditions.json"):
        ids |= set(re.findall(r"horizon:[a-z0-9_/]+", (ROOT / rel).read_text(encoding="utf-8")))
    ids |= {"horizon:trophy_" + b["id"].split(":")[1] for b in jload("manifests/legends.json")["bosses"]}
    p = ROOT / "kubejs/startup_scripts/horizon_items.js"
    if p.exists():
        ids |= set(re.findall(r"horizon:[a-z0-9_]+", p.read_text(encoding="utf-8")))
    return ids


def bare(i, known=None):
    """'ancient_core' -> 'horizon:ancient_core' when that horizon item exists; anything else is returned unchanged."""
    if ":" in i:
        return i
    return "horizon:" + i if "horizon:" + i in (known or horizon_items()) else i


# ---------- find ----------
def cmd_find(a):
    q = bare(a.query.strip().lower().replace(" ", "_"), horizon_items()) if a.query.strip().lower().replace(" ", "_") in {i.split(":")[1] for i in horizon_items()} else a.query.strip().lower()
    qn = re.sub(r"[\s-]+", "_", q)
    ids = jload("manifests/ids.json")
    legends = jload("manifests/legends.json")["bosses"]
    cands = []
    for b in legends:
        if q in (b["id"].lower(), b["name"].lower()) or qn == b["id"].split(":")[1]:
            cands.append(("boss", b["id"]))
    for kind in ("entity", "item", "structure", "block"):
        for i in ids.get(kind, []):
            if ("boss", i) in cands:
                continue
            p = i.split(":")[-1]
            if i == q or p == qn or (len(qn) > 3 and qn in p):
                cands.append((kind, i))
    if q.startswith("horizon:") and q in horizon_items():
        cands.append(("item", q))
    cands = sorted(set(cands), key=lambda c: (c[1].split(":")[-1] != qn and c[1] != q, ["boss", "entity", "structure", "item", "block"].index(c[0]), len(c[1])))
    if not cands and ":" in q:
        cands = [("id", q)]   # e.g. horizon:* items are registered by KubeJS, not in ids.json
    if not cands:
        die(f"nothing matches {a.query!r} in ids.json/legends.json", EX_FAIL)
    kind, ident = cands[0]
    path = ident.split(":")[-1]
    res = [f"{kind} {ident}" + (f"  (+{len(cands) - 1} more: {', '.join(c[1] for c in cands[1:4])})" if len(cands) > 1 else "")]
    boss = next((b for b in legends if b["id"] == ident), None)
    fam = jload("manifests/loot_families.json")
    exp = (ROOT / "manifests/expeditions.json").read_text(encoding="utf-8")
    hits = {"quests": [], "gen": [], "recipes": []}
    needle = ident.encode()
    for sub, key in (("config/heracles/quests", "quests"), ("datapacks", "gen")):
        for f in (ROOT / sub).rglob("*.json"):
            if f.name.startswith("."):
                continue
            rel = f.relative_to(ROOT).as_posix()
            if needle in f.read_bytes() or (boss and path in f.stem):
                hits["recipes" if "/recipe/" in rel else key].append(rel)
    for f in (ROOT / "kubejs/server_scripts").glob("*.js"):
        for n, l in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if ident in l:
                hits["recipes"].append(f"{f.relative_to(ROOT).as_posix()}:{n}")
    if boss:
        res.append(f"drops: first-kill relic ({'Starforged Heart' if boss['tier'] == 'major' else 'Ancient Core'}) + horizon:trophy_{path}; tier={boss['tier']}"
                   + (f"; repeat={boss['repeat']}" if boss.get("repeat") else ""))
    else:
        tabs = [t for t in jload("manifests/loot_audit.json").get("per_table", {}) if path in t]
        if tabs:
            res.append(f"loot tables ({len(tabs)}): {', '.join(tabs[:2])}")
        if kind == "structure":
            famid = next((f for rx, f in fam["structures"] if re.search(rx, ident)), None)
            res.append(f"loot family: {famid or 'none (unclassified)'}" + (f" -> budget {fam['families'][famid]['budget']}" if famid else ""))
    if any(ident in t for t in re.findall(r'"cost":\s*\{[^}]*\}', exp)):
        res.append("expedition cost ingredient (manifests/expeditions.json trials)")
    for k, label in (("recipes", "recipes/scripts"), ("quests", "quests"), ("gen", "generated data")):
        if hits[k]:
            res.append(f"{label} ({len(hits[k])}): {', '.join(sorted(hits[k])[:3])}")
    src = [m for m in ("legends", "loot_families", "expeditions") if ident in (ROOT / f"manifests/{m}.json").read_text(encoding="utf-8")]
    res.append("edit: " + (", ".join(f"manifests/{m}.json" for m in src) or "no source manifest lists it")
               + ("; kubejs/server_scripts/horizon_recipes.js" if any("horizon_recipes" in r for r in hits["recipes"]) else "")
               + ("; scripts/gen_assets.py (item table)" if kind == "item" and "horizon:" in ident else ""))
    out(res)


# ---------- add ----------
def glyphs():
    t = (ROOT / "scripts/gen_assets.py").read_text(encoding="utf-8")
    blk = t[t.index("GLYPHS = {"):]
    return set(re.findall(r'^    "(\w+)":', blk[:blk.index("\n}")], re.M))


def spec_of(a):
    if not a.spec:
        die("--spec <file.json | inline json> required for this kind")
    s = a.spec.strip()
    return json.loads(s if s.startswith("{") else Path(s).read_text(encoding="utf-8"))


def plan_add(a):
    """Return (manifest rel path, new text, old text, errors, effects)."""
    ids = jload("manifests/ids.json")
    err, fx = [], []

    def need(kind, i):
        if not (i.startswith("horizon:") and kind == "item" or i.startswith("minecraft:") and kind in ("entity", "item")) and i not in ids.get(kind, []):
            err.append(f"unknown {kind} id: {i}")
    if a.kind == "boss":
        if not (a.id and a.name):
            die("boss needs --id ns:entity --name 'Name' [--tier mini|major] [--glyph g] [--palette a,b,c,d]")
        rel = "manifests/legends.json"
        d = jload(rel)
        pal = (a.palette or "1a1a1a,555555,aaaaaa,ffffff").split(",")
        entry = {"id": a.id, "name": a.name, "tier": a.tier, "repeat": None, "palette": pal, "glyph": a.glyph}
        need("entity", a.id)
        if any(b["id"] == a.id for b in d["bosses"]):
            err.append(f"{a.id} already in legends")
        if a.tier not in ("mini", "major"):
            err.append("tier must be mini|major")
        if a.glyph not in glyphs():
            err.append(f"glyph must be one of {sorted(glyphs())}")
        if len(pal) != 4 or not all(re.fullmatch(r"[0-9a-fA-F]{6}", c) for c in pal):
            err.append("palette needs 4 hex colours")
        n = a.id.split(":")[1]
        d["bosses"].append(entry)
        old = (ROOT / rel).read_text(encoding="utf-8")
        new = json.dumps(d, indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
        tiers = {t: sum(b["tier"] == t for b in d["bosses"]) for t in ("mini", "major")}
        fx = [f"reward: first kill -> {'Starforged Heart' if a.tier == 'major' else 'Ancient Core'} + horizon:trophy_{n} (once per player)",
              f"progression: Hall of Legends grows to {len(d['bosses'])} ({tiers['major']} major / {tiers['mini']} mini); new quest 12halloflegends_legend_{n}",
              f"generated: advancement horizon:legend/{n}, reward loot table, trophy block/model/lang, tooltip"]
        return rel, new, old, err, fx
    if a.kind == "expedition":
        sp = spec_of(a)
        rel = "manifests/expeditions.json"
        old = (ROOT / rel).read_text(encoding="utf-8")
        d = json.loads(old)
        for k in ("id", "name", "color", "size", "cost", "waves", "rewards"):
            if k not in sp:
                err.append(f"spec missing {k}")
        if err:
            return rel, old, old, err, fx
        hi = horizon_items()
        sp["cost"] = {bare(i, hi): n for i, n in sp["cost"].items()}
        if any(t["id"] == sp["id"] for t in d["trials"]):
            err.append(f"trial {sp['id']} exists")
        if sp["size"] not in {t["size"] for t in d["trials"]}:
            err.append(f"size must be one of {sorted({t['size'] for t in d['trials']})}")
        if len(sp["cost"]) > 9:
            err.append("cost has > 9 ingredients")
        for i in sp["cost"]:
            need("item", i)
        for w in sp["waves"]:
            for e, _ in w["entities"]:
                need("entity", e)
        tail = "\n  ]\n}"
        if not old.rstrip().endswith(tail):
            err.append("expeditions.json tail not recognised; edit by hand")
        new = old.rstrip()[:-len(tail)] + ",\n    " + json.dumps(sp, ensure_ascii=False) + tail + "\n"
        mobs = sum(n for w in sp["waves"] for _, n in w["entities"])
        old_m = [sum(n for w in t["waves"] for _, n in w["entities"]) for t in d["trials"] if t["size"] == sp["size"]]
        fx = [f"cost: {sum(sp['cost'].values())} items; {len(sp['waves'])} waves / {mobs} mobs (existing {sp['size']} trials: {old_m})",
              f"reward: xp {sp['rewards'].get('xp')}, affix {sp['rewards'].get('affix')}, gems {len(sp['rewards'].get('gems', []))}+{sp['rewards'].get('random_gems', 0)} random",
              "generated: trial recipe/structure data via gen_datapack; budget and salvage reports re-solved"]
        return rel, new, old, err, fx
    sp = spec_of(a)  # loot-family: {"id":..,"family":{...},"structures":[rx..],"tables":[rx..]}
    rel = "manifests/loot_families.json"
    old = (ROOT / rel).read_text(encoding="utf-8")
    d = json.loads(old)
    fid, f = sp.get("id"), sp.get("family", {})
    hi = horizon_items()
    for k in ("icon", "token"):
        if f.get(k):
            f[k] = bare(f[k], hi)
    req = set(next(iter(d["families"].values()))) & {"title", "stage", "icon", "identity", "prep", "signature", "repeat", "connects", "budget"}
    err += [f"family missing {k}" for k in sorted(req - set(f))]
    if not fid or fid in d["families"]:
        err.append(f"family id missing or already used: {fid}")
    if f.get("stage") not in {x["stage"] for x in d["families"].values()}:
        err.append(f"stage must be one of {sorted({x['stage'] for x in d['families'].values()})}")
    for k in ("icon", "token"):
        if f.get(k):
            need("item", f[k])
    match = {}
    for kind, pool in (("structures", ids["structure"] + d["vanilla_structures"]), ("tables", ids["loot_table"])):
        for rx in sp.get(kind, []):
            try:
                match[rx] = sum(bool(re.search(rx, i)) for i in pool)
            except re.error as e:
                err.append(f"bad regex {rx}: {e}")
            else:
                if not match[rx]:
                    err.append(f"{kind[:-1]} pattern matches nothing: {rx}")
    d["families"][fid or "?"] = f
    for kind in ("structures", "tables"):
        d[kind] = [[rx, fid] for rx in sp.get(kind, [])] + d[kind]   # first match wins: new patterns go first
    new = json.dumps(d, indent=2, ensure_ascii=False) + ("\n" if old.endswith("\n") else "")
    fx = [f"progression: stage {f.get('stage')}; budget {f.get('budget')}" + (f"; token {f['token']}" if f.get("token") else ""),
          f"claims {sum(match.values())} id matches ({match}); new patterns precede existing ones (first match wins)",
          "generated: structure tag family/<id>, injected loot, atlas quest, docs/LOOT_BUDGET.md (hard ceilings abort the build)"]
    return rel, new, old, err, fx


def cmd_add(a):
    rel, new, old, err, fx = plan_add(a)
    diff = [l for l in difflib.unified_diff(old.splitlines(), new.splitlines(), rel, rel, lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
    log = logfile("add")
    log.write_text("\n".join(difflib.unified_diff(old.splitlines(), new.splitlines(), rel, rel, lineterm="")), encoding="utf-8")
    head = [f"{'APPLY' if a.apply else 'PREVIEW'} add {a.kind}: {rel} (+{sum(l.startswith('+') for l in diff)}/-{sum(l.startswith('-') for l in diff)} lines)"]
    if err:
        return out(head + ["INVALID:"] + ["  " + e for e in err], log) or sys.exit(EX_FAIL)
    if not a.apply:
        return out(head + fx + ["ids valid. rerun with --apply to write + regenerate"], log)
    (ROOT / rel).write_text(new, encoding="utf-8")
    steps, _, _ = plan_quick([rel])
    rc, res = run_steps(steps, log)
    if rc:
        (ROOT / rel).write_text(old, encoding="utf-8")
        return out(head + res + [f"manifest reverted; generator outputs may be partial - rerun check quick"], log) or sys.exit(EX_FAIL)
    out(head + fx[:2] + res, log)


def main():
    ap = argparse.ArgumentParser(prog="horizon")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("mode", choices=["quick", "release"]); c.add_argument("--files"); c.add_argument("--dry", action="store_true")
    c.add_argument("--net", action="store_true"); c.add_argument("--configs", action="store_true"); c.add_argument("--offline", action="store_true")
    q = sub.add_parser("qa"); q.add_argument("what", choices=["loot", "trophies", "shaders", "perf", "observe"]); q.add_argument("key", nargs="?"); q.add_argument("note", nargs="?")
    q.add_argument("--server"); q.add_argument("--voxy-radius", type=int); q.add_argument("--voxy-tasks", type=int); q.add_argument("--dwell", type=int, default=600); q.add_argument("--label", default="run"); q.add_argument("--cmds"); q.add_argument("--seed", default="horizon-qa-1"); q.add_argument("--shader", default="solas")
    q.add_argument("--fresh", action="store_true"); q.add_argument("--pregen", action="store_true"); q.add_argument("--timeout", type=int, default=900)
    k = sub.add_parser("crash"); k.add_argument("path", nargs="?")
    f = sub.add_parser("find"); f.add_argument("query")
    d = sub.add_parser("add"); d.add_argument("kind", choices=["boss", "expedition", "loot-family"]); d.add_argument("--apply", action="store_true")
    d.add_argument("--id"); d.add_argument("--name"); d.add_argument("--tier", default="mini"); d.add_argument("--glyph", default="skull")
    d.add_argument("--palette"); d.add_argument("--spec")
    a = ap.parse_args()
    if a.cmd == "qa" and a.what == "observe" and not a.key:
        die("usage: qa observe <key> [note]")
    {"check": cmd_check, "qa": cmd_qa, "crash": cmd_crash, "find": cmd_find, "add": cmd_add}[a.cmd](a)


if __name__ == "__main__":
    main()
