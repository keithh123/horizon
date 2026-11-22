"""Build every locally produced jar described in ports/*/port.json -> ports/dist/, and record
exact hashes in manifests/ports_lock.json (consumed by build.py for instances, servers and .mrpack).

Kinds:
  repack  - download an upstream jar (pinned URL + sha512), apply exact text edits to named entries,
            and write a deterministic jar (sorted entries, fixed timestamps) so the hash is reproducible.
  wrap    - turn an upstream datapack/resource zip into a NeoForge mod jar by adding a neoforge.mods.toml
            (+ pack.mcmeta untouched). Deterministic like repack.
  gradle  - compile a source port in ports/<name>/src with its Gradle wrapper (ModDevGradle) and copy
            the built jar. Requires network on first run (Gradle/NeoForge artifacts).

Every port.json must carry license, upstream, attribution and what was changed. Never used to
change version metadata as a claim of compatibility: repacks only fix loader metadata that blocks
loading; each port is tested in game (docs/PORTS.md).

  python scripts/build_ports.py [name ...]
"""
import hashlib, io, json, os, shutil, subprocess, sys, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORTS = ROOT / "ports"
DIST = PORTS / "dist"
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
UA = {"User-Agent": "project-horizon-builder/0.3"}
EPOCH = (1980, 2, 1, 0, 0, 0)


def fetch(url, sha512):
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / url.rsplit("/", 1)[1].replace("%20", " ")
    if not (dest.exists() and hashlib.sha512(dest.read_bytes()).hexdigest() == sha512):
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
            data = r.read()
        if hashlib.sha512(data).hexdigest() != sha512:
            raise SystemExit(f"hash mismatch for {url}")
        dest.write_bytes(data)
    return dest


def write_deterministic(entries: dict, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, entries[name])


def read_zip(path):
    with zipfile.ZipFile(path) as z:
        return {i.filename: z.read(i) for i in z.infolist() if not i.is_dir()}


def build(name, spec):
    out = DIST / spec["output"]
    kind = spec["kind"]
    if kind in ("repack", "wrap"):
        src = fetch(spec["upstream"]["url"], spec["upstream"]["sha512"])
        entries = read_zip(src)
        prefix = spec.get("strip_prefix", "")
        if prefix:
            entries = {k[len(prefix):]: v for k, v in entries.items() if k.startswith(prefix)}
        for e in spec.get("drop", []):
            entries.pop(e, None)
        for path, edits in spec.get("edits", {}).items():
            text = entries[path].decode("utf-8")
            for old, new in edits:
                if text.count(old) != 1:
                    raise SystemExit(f"{name}: edit {old!r} matched {text.count(old)} times in {path}")
                text = text.replace(old, new)
            entries[path] = text.encode("utf-8")
        for path, rel in spec.get("add", {}).items():
            entries[path] = (PORTS / name / rel).read_bytes()
        write_deterministic(entries, out)
    elif kind == "gradle":
        src = PORTS / name / "src"
        gradlew = src / ("gradlew.bat" if os.name == "nt" else "gradlew")
        subprocess.run([str(gradlew), "build", "--no-daemon", "-q"], cwd=src, check=True)
        built = src / "build" / "libs" / spec["built_jar"]
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built, out)
    else:
        raise SystemExit(f"{name}: unknown kind {kind}")
    data = out.read_bytes()
    return {"name": name, "file": out.name, "kind": kind, "side": spec["side"], "license": spec["license"],
            "replaces_slug": spec.get("replaces_slug"), "upstream": spec.get("upstream", {}).get("page") or spec.get("source"),
            "size": len(data), "hashes": {"sha1": hashlib.sha1(data).hexdigest(), "sha512": hashlib.sha512(data).hexdigest()}}


def main():
    only = set(sys.argv[1:])
    lock_path = ROOT / "manifests/ports_lock.json"
    lock = {p["name"]: p for p in json.loads(lock_path.read_text())["ports"]} if lock_path.exists() else {}
    for d in sorted(PORTS.glob("*/port.json")):
        name = d.parent.name
        if only and name not in only:
            continue
        spec = json.loads(d.read_text(encoding="utf-8"))
        if spec.get("disabled"):
            lock.pop(name, None)
            continue
        lock[name] = build(name, spec)
        print(f"{name:28} {lock[name]['file']:50} {lock[name]['hashes']['sha512'][:16]}")
    lock_path.write_text(json.dumps({"ports": sorted(lock.values(), key=lambda p: p["name"])}, indent=2))


if __name__ == "__main__":
    main()
