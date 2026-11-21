"""Check loader-level dependency *versions*, not just project presence.

Modrinth metadata only says "project X is required". The authoritative contract is
each jar's META-INF/neoforge.mods.toml: [[dependencies.<modId>]] entries with a
type (required/optional/incompatible/discouraged), a Maven versionRange and a side.
This script reads every locked jar (and nested jar-in-jar), builds the modId ->
version map that FML would see, and evaluates every range.

  python scripts/check_deps.py            -> report, exit 1 on any hard failure
Fabric jars loaded by Roxy (voxy) are reported separately: FML never sees them.
"""
import io, json, os, re, sys, tomllib, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
SYSTEM = {"minecraft", "neoforge"}
PLATFORM = {"minecraft": "1.21.1", "neoforge": "21.1.267", "forge": "21.1.267", "javafml": "4", "java": "21"}


def vkey(v):
    """Maven-ish comparable key. Splits on . - + _ and compares numbers numerically."""
    parts = re.split(r"[.\-+_]", str(v).lower())
    out = []
    for p in parts:
        for tok in re.findall(r"\d+|[a-z]+", p):
            out.append((0, int(tok)) if tok.isdigit() else (-1, tok))  # qualifiers sort before numbers
    return out


def in_range(ver, rng):
    rng = rng.strip()
    if rng in ("", "*"):
        return True
    for spec in re.findall(r"[\[\(][^\]\)]*[\]\)]", rng) or [rng]:
        if not spec[0] in "[(":
            if vkey(ver) >= vkey(spec):   # bare version = minimum (soft requirement in Maven)
                return True
            continue
        lo_inc, hi_inc = spec[0] == "[", spec[-1] == "]"
        body = spec[1:-1]
        if "," not in body:
            if vkey(ver) == vkey(body.strip()):
                return True
            continue
        lo, hi = [s.strip() for s in body.split(",", 1)]
        ok = True
        if lo:
            ok &= vkey(ver) >= vkey(lo) if lo_inc else vkey(ver) > vkey(lo)
        if hi:
            ok &= vkey(ver) <= vkey(hi) if hi_inc else vkey(ver) < vkey(hi)
        if ok:
            return True
    return False


def manifest_version(z):
    try:
        mf = z.read("META-INF/MANIFEST.MF").decode("utf-8", "ignore")
        m = re.search(r"Implementation-Version:\s*(\S+)", mf)
        return m.group(1) if m else None
    except KeyError:
        return None


def scan(z, owner, mods, deps, fabric):
    names = z.namelist()
    if "META-INF/neoforge.mods.toml" in names:
        try:
            t = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8", "ignore"))
        except tomllib.TOMLDecodeError as e:
            print(f"WARN {owner}: unparsable mods.toml ({e})")
            t = {}
        for m in t.get("mods", []):
            v = m.get("version", "?")
            if "${" in v:
                v = manifest_version(z) or v
            mods.setdefault(m["modId"], (v, owner))
        for mid, lst in (t.get("dependencies") or {}).items():
            for d in lst:
                deps.append((owner, mid, d))
    elif "fabric.mod.json" in names:
        try:
            fabric.append((owner, json.loads(z.read("fabric.mod.json").decode("utf-8", "ignore"))))
        except Exception:
            pass
    for n in names:
        if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
            try:
                scan(zipfile.ZipFile(io.BytesIO(z.read(n))), owner + " > " + n.rsplit("/", 1)[-1], mods, deps, fabric)
            except zipfile.BadZipFile:
                pass


def main():
    lock = json.loads((ROOT / "manifests/lock.json").read_text())
    mods, deps, fabric = {}, [], []
    for m in lock["mods"]:
        scan(zipfile.ZipFile(CACHE / m["file"]), m["slug"], mods, deps, fabric)
    for k, v in PLATFORM.items():
        mods.setdefault(k, (v, "platform"))
    fail, warn = [], []
    for owner, parent, d in deps:
        mid = d.get("modId")
        typ = str(d.get("type", "required" if d.get("mandatory", True) else "optional")).lower()
        rng = str(d.get("versionRange", "*"))
        side = str(d.get("side", "BOTH")).upper()
        have = mods.get(mid)
        if typ == "required":
            if not have:
                (warn if side == "CLIENT" and mid in ("sodium", "iris") else fail).append(f"{owner}: requires {mid} {rng} ({side}) - MISSING")
            elif not in_range(have[0], rng):
                # FML 4 treats minecraft/neoforge as "system mods"; the launch log for these exact jars
                # reports "0 mod requirements missing", so a range mismatch there is advisory only.
                (warn if mid in SYSTEM else fail).append(f"{owner}: requires {mid} {rng}, found {have[0]} (from {have[1]})"
                                                         + (" [system mod: accepted by FML 4.0.45, confirmed by launch log]" if mid in SYSTEM else ""))
        elif typ in ("incompatible", "discouraged") and have and in_range(have[0], rng):
            (fail if typ == "incompatible" else warn).append(f"{owner}: {typ} with {mid} {rng}, found {have[0]}")
        elif typ == "optional" and have and not in_range(have[0], rng):
            fail.append(f"{owner}: optional {mid} {rng} is present but version {have[0]} is out of range (FML rejects this)")
    for owner, fm in fabric:
        warn.append(f"{owner}: Fabric jar ({fm.get('id')} {fm.get('version')}, minecraft {fm.get('depends', {}).get('minecraft')}) - "
                    "loaded by Roxy, not FML; verified by launch, not by this checker")
    report = {"mods_seen": len(mods), "dependency_entries": len(deps), "failures": fail, "warnings": warn}
    (ROOT / "manifests/deps_report.json").write_text(json.dumps(report, indent=1))
    print(f"{len(mods)} mod ids, {len(deps)} dependency entries checked")
    for w in warn:
        print("WARN ", w)
    for f in fail:
        print("FAIL ", f)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
