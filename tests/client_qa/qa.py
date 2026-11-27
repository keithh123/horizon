"""Send one action batch to the client QA harness (tests/client_qa/zz_horizon_qa.js) and print its result.

usage: python tests/client_qa/qa.py <instance-name> "action" ["action" ...] [--timeout 300]
Writes <instance>/minecraft/horizon_qa/cmd.json with a fresh id and waits until out.json reports that id done.
Test instances only.
"""
import json, os, sys, time
from pathlib import Path

args = sys.argv[1:]
timeout = 300
if "--timeout" in args:
    i = args.index("--timeout"); timeout = int(args[i + 1]); del args[i:i + 2]
inst, actions = args[0], args[1:]
d = Path(os.environ["APPDATA"]) / "PrismLauncher/instances" / inst / "minecraft/horizon_qa"
d.mkdir(parents=True, exist_ok=True)
bid = int(time.time() * 1000) % 1_000_000_000
(d / "cmd.json").write_text(json.dumps({"id": bid, "actions": actions}), encoding="utf-8")
t0 = time.time()
while time.time() - t0 < timeout:
    try:
        o = json.loads((d / "out.json").read_text(encoding="utf-8"))
        if int(o.get("last", -1)) == bid and any(str(l).startswith("done") for l in o["lines"]):
            print("\n".join(o["lines"]))
            sys.exit(0)
    except (OSError, ValueError):
        pass
    time.sleep(1)
print(f"TIMEOUT after {timeout}s (batch {bid})")
sys.exit(1)
