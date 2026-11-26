"""Jars that ship in the default pack but are not in lock.json: local ports (manifests/ports_lock.json, no variant).

Scanners (index_ids, audit_loot, check_deps, gen_datapack) append these to lock["mods"] so ids, loot tables and dependency
ranges of shipped ports are covered (0.6: Terra Curio moved from the lock to ports/terracurio and must stay indexed).
"file" is an absolute path, so CACHE / entry["file"] resolves to the port jar.
"""
import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))


def port_entries():
    f = ROOT / "manifests/ports_lock.json"
    if not f.exists():
        return []
    out = []
    for p in json.loads(f.read_text())["ports"]:
        if p.get("variant"):
            continue
        out.append({"slug": p.get("replaces_slug") or p["name"], "file": str(ROOT / "ports" / "dist" / p["file"]),
                    "project_id": "port:" + p["name"], "group": "port", "deps": [], "version": "port",
                    "client_side": p["side"]["client"], "server_side": p["side"]["server"], "port": True})
    return out


def with_ports(lock):
    lock["mods"] = lock["mods"] + port_entries()
    return lock
