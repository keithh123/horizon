"""Drive the headless NeoForge test server through its console (no player needed).

  python scripts/server_test.py <server_dir> <world_name> <seed> <commands_file> [--keep]

Starts ONLY the java process it launches (never touches other javaw/java processes), waits for
"Done (", sends each line of <commands_file> (lines starting with '#' are comments; 'WAIT <s>' sleeps;
'WAITLOG <regex> <timeout>' waits for a log line), then 'stop'. The world lives in <server_dir>/<world_name>
and is kept for inspection; other worlds in the directory are untouched. Writes the full console log to
<server_dir>/logs/test-<world_name>.log and prints errors + all lines tagged [horizon...].
"""
import os, re, subprocess, sys, threading, time
from pathlib import Path


def main():
    sdir, world, seed, cmdfile = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
    props = sdir / "server.properties"
    text = props.read_text()
    text = re.sub(r"(?m)^level-name=.*$", f"level-name={world}", text)
    text = re.sub(r"(?m)^level-seed=.*$", f"level-seed={seed}", text)
    for k, v in (("enable-command-block", "true"), ("spawn-protection", "0"), ("max-tick-time", "-1")):
        text = re.sub(rf"(?m)^{k}=.*$", f"{k}={v}", text) if re.search(rf"(?m)^{k}=", text) else text + f"\n{k}={v}\n"
    props.write_text(text)
    args = (sdir / "user_jvm_args.txt").read_text().split()
    cmd = ["java", *args, "@libraries/net/neoforged/neoforge/21.1.267/win_args.txt", "nogui"]
    log = (sdir / "logs" / f"test-{world}.log")
    log.parent.mkdir(exist_ok=True)
    out = open(log, "w", encoding="utf-8", errors="replace")
    p = subprocess.Popen(cmd, cwd=sdir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace", bufsize=1)
    lines = []
    lock = threading.Lock()

    def pump():
        for line in p.stdout:
            out.write(line); out.flush()
            with lock:
                lines.append(line)
    threading.Thread(target=pump, daemon=True).start()

    def wait_for(rx, timeout, since=0):
        t0 = time.time()
        seen = since
        while time.time() - t0 < timeout:
            with lock:
                cur = lines[seen:]
                seen = len(lines)
            for l in cur:
                if re.search(rx, l):
                    return l
            if p.poll() is not None:
                return None
            time.sleep(0.5)
        return None

    t0 = time.time()
    if not wait_for(r"Done \(", 900):
        print("SERVER DID NOT START"); p.kill(); sys.exit(2)
    print(f"started in {time.time() - t0:.0f}s")
    def send(c):
        p.stdin.write(c + "\n"); p.stdin.flush()
    for raw in cmdfile.read_text(encoding="utf-8").splitlines():
        c = raw.strip()
        if not c or c.startswith("#"):
            continue
        if c.startswith("WAITLOG "):
            _, rx, to = c.split(" ", 2)
            print("WAITLOG", rx, "->", (wait_for(rx, float(to)) or "TIMEOUT").strip()[:200])
            continue
        if c.startswith("LOCATEAUDIT "):
            # LOCATEAUDIT <structure> <radius> <rolls>: find a naturally generated instance, load it, audit its containers
            _, sid, rad, rolls = c.split()
            send(f"say [horizon-test] locate {sid}")
            with lock:
                mark = len(lines)
            send(f"locate structure {sid}")
            hit = wait_for(r"(The nearest .* is at \[|Could not find a structure|Incorrect argument|Unknown)", 300, mark)
            m = re.search(r"\[(-?\d+), (~|-?\d+), (-?\d+)\]", hit or "")
            print("LOCATE", sid, "->", (hit or "TIMEOUT").strip()[-160:])
            if m:
                x, z = int(m.group(1)), int(m.group(3))
                r = int(rad)
                send(f"forceload add {x - r} {z - r} {x + r} {z + r}")
                time.sleep(25)
                send(f"execute positioned {x} 64 {z} run horizon audit {r} {rolls}")
                time.sleep(6)
                send("forceload remove all")
            continue
        if c.startswith("SAY "):
            send("say [horizon-test] " + c[4:]); time.sleep(0.5); continue
        if c.startswith("WAIT "):
            time.sleep(float(c.split()[1])); continue
        send(c)
        time.sleep(1.5)
    send("stop")
    try:
        p.wait(timeout=600)
    except subprocess.TimeoutExpired:
        p.kill()
    out.close()
    full = log.read_text(encoding="utf-8", errors="replace").splitlines()
    for l in full:
        if re.search(r"\[horizon|/ERROR\]|Exception|FATAL|Failed to|Couldn't", l) and "horizon-audit] tables" not in l:
            print(l[:400])
    print("exit", p.returncode, "log:", log)


if __name__ == "__main__":
    main()
