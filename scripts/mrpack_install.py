"""Headless .mrpack install for QA (the Modrinth pack format, as a launcher applies it) - NOT a Prism import.

  python scripts/mrpack_install.py <pack.mrpack> <target_dir> [--side client|server]

Downloads every index file whose env for that side is not "unsupported" (from its URL, sha1 + sha512 checked; the jar cache
of build.py is reused when the hash matches), then extracts overrides/ and, for clients, client-overrides/. Writes
<target>/minecraft/... (the same layout Prism uses) and verifies the result with horizon.py's verify_candidate.
Exit 1 on any hash mismatch or missing file.
"""
import hashlib, json, os, sys, urllib.request, zipfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
UA = {"User-Agent": "project-horizon-builder/0.1"}


def fetch(f):
    name = f["path"].rsplit("/", 1)[1].removesuffix(".disabled")
    c = CACHE / name
    if c.exists() and hashlib.sha512(c.read_bytes()).hexdigest() == f["hashes"]["sha512"]:
        return c.read_bytes()
    with urllib.request.urlopen(urllib.request.Request(f["downloads"][0], headers=UA), timeout=120) as r:
        return r.read()


def main():
    pack, target = Path(sys.argv[1]), Path(sys.argv[2])
    side = sys.argv[sys.argv.index("--side") + 1] if "--side" in sys.argv else "client"
    mc = target / "minecraft"
    with zipfile.ZipFile(pack) as z:
        idx = json.loads(z.read("modrinth.index.json"))
        files = [f for f in idx["files"] if f["env"][side] != "unsupported"]
        bad = []
        for f in files:
            data = fetch(f)
            if hashlib.sha1(data).hexdigest() != f["hashes"]["sha1"] or hashlib.sha512(data).hexdigest() != f["hashes"]["sha512"]:
                bad.append(f["path"])
                continue
            p = mc / f["path"]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        roots = ["overrides/"] + (["client-overrides/"] if side == "client" else ["server-overrides/"])
        n = 0
        for root in roots:
            for i in z.infolist():
                if i.filename.startswith(root) and not i.is_dir():
                    p = mc / i.filename[len(root):]
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(z.read(i))
                    n += 1
    if side == "client":
        from horizon import verify_candidate
        bad += verify_candidate(target, pack, idx)
    jars = sorted(x.name for x in (mc / "mods").iterdir()) if (mc / "mods").exists() else []
    print(f"{pack.name} -> {target} ({side}): {len(files)} index files, {n} override files, {len(jars)} entries in mods/, "
          f"{sum(1 for j in jars if j.endswith('.disabled'))} disabled; {len(bad)} problems")
    for b in bad[:20]:
        print("  BAD", b)
    (target / "install-report.json").write_text(json.dumps({"pack": pack.name, "side": side, "index_files": len(files),
                                                           "overrides": n, "mods": jars, "problems": bad}, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
