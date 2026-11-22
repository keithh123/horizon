"""Probe every active entry of the compatibility audit against Modrinth for the exact target.

  python scripts/probe_expansion.py <audit.json>   -> manifests/expansion_probe.json

For each entry: all neoforge+1.21.1 versions (newest first), primary file, declared deps
(resolved to slugs), sides, license, source URL; for misses, the project's loaders and
latest game versions. Read-only; re-run any time (idempotent output).
"""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "project-horizon-builder/0.3 (modpack build script)"}
API = "https://api.modrinth.com/v2"
_cache = {}


def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    if url in _cache:
        return _cache[url]
    for _ in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                _cache[url] = json.load(r)
                return _cache[url]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(4)
    raise RuntimeError(url)


def slug_of(pid):
    p = get(f"/project/{pid}")
    return p["slug"] if p else pid


def main():
    audit = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "manifests/lock.json").read_text())
    locked = {m["project_id"]: m for m in lock["mods"]}
    rows = [dict(r, _src="row") for r in audit["rows"]] + [dict(a, requested=a["project"], status="addon", _src="addon") for a in audit["animation_addons"]]
    out = []
    for r in rows:
        slug = r.get("slug") or ""
        e = {"requested": r["requested"], "slug": slug, "audit_status": r["status"], "audit_version": r.get("version"), "kind": r.get("kind")}
        if not slug or slug.startswith("CF:"):
            e["platform"] = "curseforge" if slug else "none"
            out.append(e); continue
        p = get(f"/project/{slug}")
        if not p:
            e["platform"] = "missing"; out.append(e); continue
        e.update(project_id=p["id"], title=p["title"], project_type=p["project_type"], client=p["client_side"], server=p["server_side"],
                 license=p["license"]["id"], source=p.get("source_url"), issues=p.get("issues_url"),
                 loaders=p["loaders"], game_versions_tail=p["game_versions"][-6:], already_locked=p["id"] in locked)
        if p["project_type"] in ("resourcepack", "shader"):
            vs = get(f"/project/{p['id']}/version", game_versions=json.dumps(["1.21.1"])) or []
        else:
            vs = get(f"/project/{p['id']}/version", loaders=json.dumps(["neoforge"]), game_versions=json.dumps(["1.21.1"])) or []
        e["versions"] = []
        for v in vs[:6]:
            f = next((x for x in v["files"] if x["primary"]), v["files"][0])
            e["versions"].append({"id": v["id"], "number": v["version_number"], "type": v["version_type"], "date": v["date_published"][:10],
                                  "loaders": v["loaders"], "file": f["filename"], "size": f["size"],
                                  "deps": [{"slug": slug_of(d["project_id"]) if d["project_id"] else None, "version_id": d["version_id"],
                                            "type": d["dependency_type"]} for d in v["dependencies"]]})
        if not vs:  # what does exist
            allv = get(f"/project/{p['id']}/version") or []
            e["other_builds"] = sorted({f"{l}:{g}" for v in allv for l in v["loaders"] for g in v["game_versions"] if g.startswith("1.21")})[:30]
        out.append(e)
        time.sleep(0.05)
    (ROOT / "manifests/expansion_probe.json").write_text(json.dumps(out, indent=1))
    for e in out:
        v = (e.get("versions") or [{}])[0]
        print(f"{e['requested'][:30]:30} {e['slug'][:34]:34} {('LOCKED ' if e.get('already_locked') else '')}{v.get('number','-')[:34]:34} {v.get('type','')[:4]} "
              f"{e.get('client','')}/{e.get('server','')} {e.get('license','')} deps={[d['slug']+':'+d['type'][0] for d in v.get('deps',[])]}"
              + (f" OTHER={e['other_builds'][:8]}" if e.get('other_builds') else "") + (f" [{e['platform']}]" if e.get('platform') else ""))


if __name__ == "__main__":
    main()
