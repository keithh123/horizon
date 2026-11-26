import os
"""Resolve manifests/roster.json against the Modrinth API.

Produces manifests/lock.json (exact versions, hashes, deps, sides, licenses)
and reports: missing required deps, declared incompatibilities, duplicate
projects. Re-run to update; pass --frozen to keep versions already in lock.json.
"""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix \?\ - the repo may live deep on disk
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
UA = {"User-Agent": "project-horizon-builder/0.1 (modpack build script)"}
API = "https://api.modrinth.com/v2"
RANK = {"release": 0, "beta": 1, "alpha": 2}


def get(path, **params):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429:
                time.sleep(5)
                continue
            raise
    raise RuntimeError(url)


def pick(versions, allow):
    ok = [v for v in versions if RANK[v["version_type"]] <= RANK[allow]]
    ok.sort(key=lambda v: (RANK[v["version_type"]], v["date_published"]), reverse=False)
    # newest of the most stable channel available
    if not ok:
        return None
    best = min(RANK[v["version_type"]] for v in ok)
    return max((v for v in ok if RANK[v["version_type"]] == best), key=lambda v: v["date_published"])


def main():
    roster = json.loads((ROOT / "manifests/roster.json").read_text())
    mc, loader = roster["minecraft"], roster["loader"]
    frozen = {}
    if "--frozen" in sys.argv and (ROOT / "manifests/lock.json").exists():
        frozen = {m["project_id"]: m["version_id"] for m in json.loads((ROOT / "manifests/lock.json").read_text())["mods"]}

    entries = [(g, e) for g, items in roster["groups"].items() for e in items]
    queue = [(g, e, None) for g, e in entries]
    resolved, problems, incompat = {}, [], []

    while queue:
        group, entry, parent = queue.pop(0)
        key = entry.get("project_id") or entry["slug"]
        proj = get(f"/project/{key}")
        if proj is None:
            problems.append(f"project not found: {key} (needed by {parent})")
            continue
        pid = proj["id"]
        if pid in resolved:
            if parent:
                resolved[pid]["required_by"].append(parent)
            continue
        if pid in frozen or entry.get("pin"):
            v = get(f"/version/{entry.get('pin') or frozen[pid]}")  # an explicit roster pin beats the frozen lock
        else:
            lds = [entry.get("loader_override", loader)]
            vs = get(f"/project/{pid}/version", loaders=json.dumps(lds), game_versions=json.dumps([mc])) or []
            v = pick(vs, entry.get("allow", "beta" if parent else "release"))
        if v is None:
            problems.append(f"no {loader} {mc} version for {proj['slug']} (needed by {parent or 'roster'})")
            continue
        f = next((x for x in v["files"] if x["primary"]), v["files"][0])
        resolved[pid] = {
            "slug": proj["slug"], "title": proj["title"], "project_id": pid,
            "version_id": v["id"], "version": v["version_number"], "channel": v["version_type"],
            "published": v["date_published"][:10], "loaders": v["loaders"], "game_versions": v["game_versions"],
            "file": f["filename"], "url": f["url"], "size": f["size"], "hashes": f["hashes"],
            "client_side": entry.get("side", {}).get("client", proj["client_side"]),
            "server_side": entry.get("side", {}).get("server", proj["server_side"]),
            "license": proj["license"]["id"], "group": group if not parent else "dependency",
            "why": entry.get("why", f"Required dependency of {parent}"),
            "disabled_by_default": bool(entry.get("disabled_by_default", False)) and not parent,
            "required_by": [parent] if parent else [],
            "deps": [{"project_id": d["project_id"], "version_id": d["version_id"], "type": d["dependency_type"]} for d in v["dependencies"]],
        }
        for d in v["dependencies"]:
            if d["dependency_type"] == "required" and d["project_id"] and d["project_id"] not in entry.get("skip_deps", []):
                queue.append(("dependency", {"project_id": d["project_id"]}, proj["slug"]))
            elif d["dependency_type"] == "incompatible" and d["project_id"]:
                incompat.append((proj["slug"], d["project_id"]))
        time.sleep(0.05)

    for a, b in incompat:
        if b in resolved:
            problems.append(f"INCOMPATIBLE: {a} declares {resolved[b]['slug']} incompatible")

    shaders = []
    for s in roster.get("shaders", []):
        vs = get(f"/project/{s['slug']}/version") or []
        v = next((x for x in vs if x["version_number"] == s["version_number"]), None)
        if not v:
            problems.append(f"shader version missing {s}")
            continue
        f = next((x for x in v["files"] if x["primary"]), v["files"][0])
        shaders.append({"slug": s["slug"], "version": v["version_number"], "version_id": v["id"], "file": f["filename"],
                        "url": f["url"], "size": f["size"], "hashes": f["hashes"], "why": s["why"]})

    packs = []  # resource packs: exact version pinned in the roster, applied in roster order (first = lowest priority)
    for s in roster.get("resourcepacks", []):
        v = get(f"/version/{s['pin']}")
        if not v:
            problems.append(f"resource pack version missing {s}")
            continue
        f = next((x for x in v["files"] if x["primary"]), v["files"][0])
        proj = get(f"/project/{v['project_id']}")
        packs.append({"slug": s["slug"], "title": proj["title"], "project_id": v["project_id"], "version": v["version_number"],
                      "version_id": v["id"], "file": f["filename"], "url": f["url"], "size": f["size"], "hashes": f["hashes"],
                      "license": proj["license"]["id"], "pack_format_note": s.get("note", ""), "why": s["why"],
                      "enabled_by_default": s.get("enabled_by_default", True)})

    mods = sorted(resolved.values(), key=lambda m: (m["group"], m["slug"]))
    lock = {"minecraft": mc, "loader": loader, "loader_version": roster["loader_version"],
            "generated": time.strftime("%Y-%m-%d"), "mods": mods, "shaders": shaders, "resourcepacks": packs, "problems": problems}
    (ROOT / "manifests/lock.json").write_text(json.dumps(lock, indent=2))
    print(f"{len(mods)} mods ({sum(1 for m in mods if m['group']=='dependency')} deps), {len(shaders)} shaders, {len(packs)} resource packs")
    for m in mods:
        if m["group"] == "dependency":
            print(f"  dep {m['slug']:32} {m['version']:34} <- {', '.join(sorted(set(m['required_by'])))}")
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
