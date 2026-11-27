"""Generate the headquarters campaign's data from manifests/headquarters.json (single source of truth).

Owns (listed in datapacks/.generated-hq.json and kubejs/.generated-hq.json, deletes only those):
  datapacks/horizon/advancement/hq/**          ledger mirrors (criterion "ledger" is impossible: only the server
                                               script grants it, after it has recorded the stage in the ledger)
  datapacks/horizon/advancement/realm/*.json   dimension-entry facts for realms that ship no entry advancement
  datapacks/horizon/recipe/hq/*.json           charter, survey blank, Create pressing of Survey Plates, case, lens
  datapacks/horizon/loot_table/hq/service/*    supply crates and survey charts handed out by charter services
  datapacks/horizon/tags/worldgen/structure/hq_chart/*.json
  kubejs/startup_scripts/horizon_hq_data.js    global.HORIZON_HQ for kubejs/server_scripts/horizon_headquarters.js
  schematics/horizon_*.nbt                     optional Create schematics (survival plans), docs/HQ_PLANS.md
  docs/HEADQUARTERS.md                         stage reference generated from the manifest
Validation (aborts the build): unknown ids, cyclic or unreachable stages, an option group whose min exceeds its
options, a relic in any reward / service / supply pool, a cost that a reward of the same stage refunds, a requirement
kind the server script does not implement.

  python scripts/gen_headquarters.py
"""
import gzip, io, json, os, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
HQ = json.loads((ROOT / "manifests/headquarters.json").read_text(encoding="utf-8"))
IDS = {k: set(v) for k, v in json.loads((ROOT / "manifests/ids.json").read_text()).items()}
LEG = json.loads((ROOT / "manifests/legends.json").read_text(encoding="utf-8"))
FAM = json.loads((ROOT / "manifests/loot_families.json").read_text(encoding="utf-8"))
EXP = json.loads((ROOT / "manifests/expeditions.json").read_text(encoding="utf-8"))
DP, KJ = ROOT / "datapacks", ROOT / "kubejs"
OWN_DP, OWN_KJ = DP / ".generated-hq.json", KJ / ".generated-hq.json"
SCHEM = ROOT / "schematics"
RELICS = {"horizon:wayfarer_shard", "horizon:ancient_core", "horizon:starforged_heart"}
KINDS = {"adv", "adv_any", "block_any", "respawn_near"}   # implemented by horizon_headquarters.js
written_dp, written_kj, written_root = [], [], []

HQ_ITEMS = set(HQ["items"]) | set(HQ["blocks"]) | {f"horizon:emblem_{s['id']}" for s in HQ["stages"]}
HORIZON_KNOWN = HQ_ITEMS | RELICS | {f["token"] for f in FAM["families"].values() if f.get("token")} | \
    {"horizon:trophy_" + b["id"].split(":")[1] for b in LEG["bosses"]}
HORIZON_ADV = {f"horizon:legend/{b['id'].split(':')[1]}" for b in LEG["bosses"]} | \
    {f"horizon:atlas/{f}" for f in FAM["families"]} | {f"horizon:trial/{t['id']}" for t in EXP["trials"]} | \
    {f"horizon:realm/{r}" for r in HQ["realm_advancements"]}
HORIZON_LOOT = {f"horizon:rewards/quest/chart_{c}" for c in FAM["clue_maps"]} | {f"horizon:hq/service/{k}" for k in HQ["charts"]} | \
    {f"horizon:hq/service/{k}" for k in HQ["supply"]}


def need(kind, i):
    if i.startswith("#"):
        return i
    if i.endswith("*"):                         # prefix match in the server scan, e.g. horizon:trophy_*
        if not any(x.startswith(i[:-1]) for x in HORIZON_KNOWN | IDS["item"]):
            raise SystemExit(f"prefix {i} matches nothing")
        return i
    if i.startswith("horizon:"):
        ok = {"item": HORIZON_KNOWN, "block": HORIZON_KNOWN, "adv": HORIZON_ADV, "loot": HORIZON_LOOT}[kind]
        if i not in ok:
            raise SystemExit(f"unknown horizon {kind}: {i}")
        return i
    if i.startswith("minecraft:"):
        return i
    pool = {"item": IDS["item"], "block": IDS["item"], "adv": IDS["advancement"], "loot": IDS["loot_table"], "dim": IDS["dimension"]}[kind]
    if i not in pool:
        raise SystemExit(f"unknown {kind}: {i}")
    return i


def put(base, rel, obj, sink):
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, bytes):
        p.write_bytes(obj)
    else:
        p.write_text(obj if isinstance(obj, str) else json.dumps(obj, indent=2) + "\n", encoding="utf-8", newline="\n")
    sink.append(rel)


def clean():
    for own, base in ((OWN_DP, DP), (OWN_KJ, KJ)):
        if own.exists():
            d = json.loads(own.read_text())
            for rel in d["files"]:
                (base / rel).unlink(missing_ok=True)
            for rel in d.get("root_files", []):
                (ROOT / rel).unlink(missing_ok=True)


# ---------------------------------------------------------------- validation
def requirements_of(node):
    for r in node.get("requirements", []):
        yield r


def validate():
    ids = [s["id"] for s in HQ["stages"]]
    assert len(ids) == len(set(ids)), "duplicate stage id"
    seen = set()
    for s in HQ["stages"]:                      # stages are ordered: every prerequisite must come earlier (acyclic)
        for r in s["requires"]:
            if r not in seen:
                raise SystemExit(f"stage {s['id']} requires {r}, which is not an earlier stage (cycle or typo)")
        seen.add(s["id"])
        nodes = [s] + (s["choices"]["options"] if s.get("choices") else [])
        if s.get("choices"):
            ch = s["choices"]
            if ch["min"] > len(ch["options"]) or ch["min"] < 1:
                raise SystemExit(f"{s['id']}: choice min {ch['min']} not satisfiable by {len(ch['options'])} options")
        for n in nodes:
            for r in requirements_of(n):
                if r["kind"] not in KINDS:
                    raise SystemExit(f"{s['id']}/{r['id']}: kind {r['kind']} not implemented by the server script")
                if r["kind"] == "adv":
                    need("adv", r["adv"])
                elif r["kind"] == "adv_any":
                    for a in r["advs"]:
                        need("adv", a)
                    if r["count"] > len(r["advs"]):
                        raise SystemExit(f"{r['id']}: count exceeds alternatives")
                elif r["kind"] == "block_any":
                    for b in r["blocks"]:
                        need("block", b)
            for it, n_ in n.get("cost", []):
                need("item", it)
        for it, n_ in s["rewards"]:
            need("item", it)
            if it in RELICS:
                raise SystemExit(f"{s['id']} rewards relic {it}")
            if it in {c[0] for c in s["cost"]}:
                raise SystemExit(f"{s['id']} rewards {it}, which its own cost consumes")
        for lt in s["reward_loot"]:
            need("loot", lt)
        for sv in s["services"] + [sv for o in (s.get("choices") or {}).get("options", []) for sv in o["services"]]:
            if sv not in HQ["services"]:
                raise SystemExit(f"{s['id']}: unknown service {sv}")
    for k, sv in HQ["services"].items():
        for it, n_ in sv["cost"]:
            need("item", it)
        if sv["kind"] == "loot":
            need("loot", sv["loot"])
    for k, pool in HQ["supply"].items():
        for it, lo, hi in pool:
            need("item", it)
            if it in RELICS:
                raise SystemExit(f"supply pool {k} contains relic {it}")
    for it, n_ in HQ["kit_contents"]:
        need("item", it)
        if it in RELICS:
            raise SystemExit("founding kit contains a relic")
    for r in HQ["recipes"]:
        if r["result"][0] in RELICS:
            raise SystemExit(f"recipe {r['id']} produces a relic")
    for r, dim in HQ["realm_advancements"].items():
        need("dim", dim)


# ---------------------------------------------------------------- datapack
def adv_display(icon, title, desc, frame="task", hidden=False):
    return {"icon": {"id": icon}, "title": {"text": title}, "description": {"text": desc}, "frame": frame,
            "show_toast": False, "announce_to_chat": False, "hidden": hidden}


def emit_datapack():
    # Mirrors. show_toast/announce off: the commissioning cue (title + sound from the server script) owns the notification.
    root = {"display": dict(adv_display("horizon:survey_charter", "The Lantern Line",
                                        "Headquarters campaign: plant a Survey Charter and commission six stations."),
                            background="minecraft:textures/block/spruce_planks.png"),
            "criteria": {"ledger": {"trigger": "minecraft:impossible"}}}
    put(DP, "horizon/advancement/hq/root.json", root, written_dp)
    parent = "horizon:hq/root"
    for s in HQ["stages"]:
        adv = {"parent": parent, "display": adv_display(s["icon"], f"{s['numeral']}. {s['title']}", s["summary"],
                                                        "challenge" if s["id"] == "observatory" else "goal"),
               "criteria": {"ledger": {"trigger": "minecraft:impossible"}}}
        put(DP, f"horizon/advancement/hq/{s['id']}.json", adv, written_dp)
        for o in (s.get("choices") or {}).get("options", []):
            put(DP, f"horizon/advancement/hq/{s['id']}/{o['id']}.json",
                {"parent": f"horizon:hq/{s['id']}", "display": adv_display(o["icon"], o["title"], o["summary"]),
                 "criteria": {"ledger": {"trigger": "minecraft:impossible"}}}, written_dp)
        parent = f"horizon:hq/{s['id']}"
    for r, dim in sorted(HQ["realm_advancements"].items()):
        put(DP, f"horizon/advancement/realm/{r}.json", {"criteria": {"entered": {"trigger": "minecraft:location", "conditions": {"player": [
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"location": {"dimension": dim}}}]}}}}, written_dp)
    for r in HQ["recipes"]:
        res = {"id": r["result"][0], "count": r["result"][1]}
        ing = lambda x: {"tag": x[1:]} if x.startswith("#") else {"item": need("item", x)}
        if r["type"] == "shaped":
            body = {"type": "minecraft:crafting_shaped", "category": "misc", "pattern": r["pattern"],
                    "key": {k: ing(v) for k, v in r["key"].items()}, "result": res}
        elif r["type"] == "shapeless":
            body = {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [ing(x) for x in r["ingredients"]], "result": res}
        elif r["type"] == "create:pressing":
            body = {"type": "create:pressing", "ingredients": [ing(x) for x in r["ingredients"]], "results": [res]}
        else:
            raise SystemExit(f"recipe type {r['type']}")
        put(DP, f"horizon/recipe/hq/{r['id']}.json", body, written_dp)
    for k, pool in sorted(HQ["supply"].items()):
        put(DP, f"horizon/loot_table/hq/service/{k}.json", {"type": "minecraft:chest", "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": it, "functions": [
                {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]}]} for it, lo, hi in pool]}, written_dp)
    for k, c in sorted(HQ["charts"].items()):
        for f in c["families"]:
            if f not in FAM["families"]:
                raise SystemExit(f"chart {k}: unknown family {f}")
        put(DP, f"horizon/tags/worldgen/structure/hq_chart/{k}.json",
            {"replace": False, "values": [{"id": f"#horizon:family/{f}", "required": False} for f in c["families"]]}, written_dp)
        put(DP, f"horizon/loot_table/hq/service/{k}.json", {"type": "minecraft:chest", "pools": [{"rolls": 1, "entries": [
            {"type": "minecraft:item", "name": "minecraft:map", "functions": [
                {"function": "minecraft:exploration_map", "destination": f"horizon:hq_chart/{k}", "decoration": c["decoration"],
                 "zoom": 2, "search_radius": c["search_radius"], "skip_existing_chunks": True},
                {"function": "minecraft:set_name", "target": "item_name", "name": {"text": c["name"], "color": "aqua", "italic": False}}]}]}]}, written_dp)
    put(DP, "horizon/tags/item/hq_emblems.json", {"replace": False, "values": sorted(f"horizon:emblem_{s['id']}" for s in HQ["stages"])}, written_dp)


# ---------------------------------------------------------------- server data
def emit_server_data():
    data = {"schema": HQ["schema"], "ledger_version": HQ["ledger_version"], "charter": HQ["charter"],
            "stages": [{k: s.get(k) for k in ("id", "numeral", "title", "summary", "log", "why", "requires", "requirements",
                                               "choices", "cost", "rewards", "reward_loot", "services", "unlocks", "next")} for s in HQ["stages"]],
            "services": HQ["services"], "kit": HQ["kit_contents"],
            "facts": sorted({a for s in HQ["stages"] for n in [s] + ((s.get("choices") or {}).get("options", []))
                             for r in n.get("requirements", []) for a in ([r["adv"]] if r["kind"] == "adv" else r.get("advs", []))})}
    hdr = "// GENERATED by scripts/gen_headquarters.py from manifests/headquarters.json - edit the manifest, not this file.\n"
    put(KJ, "startup_scripts/horizon_hq_data.js", hdr + "global.HORIZON_HQ = " + json.dumps(data, indent=1, sort_keys=True) + "\n", written_kj)
    return len(data["facts"])


# ---------------------------------------------------------------- schematics (Create / vanilla structure NBT)
def nbt(tag, name, val):
    out = io.BytesIO()
    def w(t, v):
        if t == 1: out.write(struct.pack(">b", v))
        elif t == 3: out.write(struct.pack(">i", v))
        elif t == 8:
            b = v.encode("utf-8"); out.write(struct.pack(">H", len(b))); out.write(b)
        elif t == 9:
            et, items = v
            out.write(struct.pack(">bi", et if items else 0, len(items)))
            for it in items: w(et, it)
        elif t == 10:
            for k in sorted(v):                  # sorted keys: deterministic bytes
                tt, vv = v[k]
                out.write(struct.pack(">b", tt)); w(8, k); w(tt, vv)
            out.write(b"\x00")
    out.write(struct.pack(">b", tag)); w(8, name); w(tag, val)
    return out.getvalue()


class Plan:
    def __init__(self, sx, sy, sz):
        self.size, self.b = (sx, sy, sz), {}

    def set(self, x, y, z, block, **props):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]:
            self.b[(x, y, z)] = (block, tuple(sorted(props.items())))

    def box(self, x0, y0, z0, x1, y1, z1, block, hollow=False, **p):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    if hollow and x0 < x < x1 and z0 < z < z1 and y0 < y < y1:
                        continue
                    self.set(x, y, z, block, **p)

    def walls(self, x0, z0, x1, z1, y0, y1, block, corner=None, **p):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                for z in (z0, z1):
                    self.set(x, y, z, block, **p)
            for z in range(z0, z1 + 1):
                for x in (x0, x1):
                    self.set(x, y, z, block, **p)
        if corner:
            for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
                for y in range(y0, y1 + 1):
                    self.set(x, y, z, corner, axis="y")

    def clear(self, x0, y0, z0, x1, y1, z1):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    self.b.pop((x, y, z), None)

    def bytes(self):
        pal, idx, blocks = [], {}, []
        for pos in sorted(self.b, key=lambda p: (p[1], p[2], p[0])):
            key = self.b[pos]
            if key not in idx:
                idx[key] = len(pal); pal.append(key)
            blocks.append({"pos": (9, (3, list(pos))), "state": (3, idx[key])})
        palette = []
        for name, props in pal:
            e = {"Name": (8, name)}
            if props:
                e["Properties"] = (10, {k: (8, str(v)) for k, v in props})
            palette.append(e)
        root = {"DataVersion": (3, 3955), "size": (9, (3, list(self.size))), "palette": (9, (10, palette)),
                "blocks": (9, (10, blocks)), "entities": (9, (10, []))}
        raw = nbt(10, "", root)
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:   # mtime=0: byte-identical rebuilds
            g.write(raw)
        return buf.getvalue()

    def bill(self):
        out = {}
        for name, props in self.b.values():
            item = {"minecraft:wall_torch": "minecraft:torch", "minecraft:water": None}.get(name, name)
            if item and not (name.endswith("_bed") and dict(props).get("part") == "head"):
                out[item] = out.get(item, 0) + 1
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def roof(p, x0, z0, x1, z1, y, block):
    """Stepped gable along x: stairs facing out on both slopes, ridge slab."""
    depth = (z1 - z0) // 2
    for i in range(depth + 1):
        for x in range(x0, x1 + 1):
            if z0 + i < z1 - i:
                p.set(x, y + i, z0 + i, block + "_stairs", facing="south", half="bottom")
                p.set(x, y + i, z1 - i, block + "_stairs", facing="north", half="bottom")
            else:
                p.set(x, y + i, z0 + i, block + "_slab", type="bottom")


def door(p, x, y, z, facing="south"):
    p.set(x, y, z, "minecraft:spruce_door", facing=facing, half="lower", hinge="left", open="false", powered="false")
    p.set(x, y + 1, z, "minecraft:spruce_door", facing=facing, half="upper", hinge="left", open="false", powered="false")


def bed(p, x, y, z):
    p.set(x, y, z, "minecraft:red_bed", facing="north", part="foot", occupied="false")
    p.set(x, y, z - 1, "minecraft:red_bed", facing="north", part="head", occupied="false")


def plans():
    P = {}
    # I. Outpost: 9x8x9 timber cabin on a stone footing. Entrance south. The copper plinth marks the charter spot.
    o = Plan(9, 8, 9)
    o.box(0, 0, 0, 8, 0, 8, "minecraft:stone_bricks")
    o.walls(0, 0, 8, 8, 1, 3, "minecraft:spruce_planks", corner="minecraft:spruce_log")
    for x in (2, 6):
        o.set(x, 2, 0, "minecraft:glass_pane"); o.set(x, 2, 8, "minecraft:glass_pane")
    o.set(0, 2, 4, "minecraft:glass_pane"); o.set(8, 2, 4, "minecraft:glass_pane")
    door(o, 4, 1, 8)
    o.box(0, 4, 0, 8, 4, 8, "minecraft:spruce_planks")
    roof(o, 0, -1, 8, 9, 5, "minecraft:spruce")
    bed(o, 1, 1, 2)
    o.set(7, 1, 1, "minecraft:chest", facing="west", type="single", waterlogged="false")
    o.set(7, 1, 2, "minecraft:barrel", facing="up", open="false")
    o.set(1, 1, 6, "minecraft:cartography_table"); o.set(2, 1, 6, "minecraft:crafting_table")
    o.set(4, 1, 4, "minecraft:waxed_cut_copper")
    o.set(4, 3, 4, "minecraft:lantern", hanging="false", waterlogged="false")
    P["outpost"] = o
    # Ruined outpost (flavor): the same footprint, half fallen. Restore it to the outpost above.
    r = Plan(9, 5, 9)
    r.box(0, 0, 0, 8, 0, 8, "minecraft:mossy_stone_bricks")
    for x in range(0, 9, 2):
        r.set(x, 0, 0, "minecraft:cracked_stone_bricks")
    r.walls(0, 0, 8, 8, 1, 2, "minecraft:mossy_cobblestone", corner="minecraft:stripped_spruce_log")
    r.clear(3, 1, 0, 6, 2, 0); r.clear(8, 2, 3, 8, 2, 7); r.clear(0, 2, 5, 0, 2, 8)
    for x, z in ((0, 0), (8, 0), (0, 8)):
        r.set(x, 3, z, "minecraft:stripped_spruce_log", axis="y")
    r.set(2, 1, 2, "minecraft:cobweb"); r.set(6, 1, 6, "minecraft:cobweb")
    r.set(7, 1, 1, "minecraft:barrel", facing="up", open="false")
    r.set(4, 1, 4, "minecraft:weathered_cut_copper")
    P["ruined_outpost"] = r
    # II. Workshop: 11x8x9 open-fronted press shed in andesite casing and spruce. Press over depot at the centre bay.
    w = Plan(11, 8, 9)
    w.box(0, 0, 0, 10, 0, 8, "minecraft:polished_andesite")
    w.walls(0, 0, 10, 8, 1, 4, "minecraft:spruce_planks", corner="create:andesite_casing")
    w.clear(3, 1, 8, 7, 3, 8)                    # wide south opening for belts and carts
    for x in (2, 5, 8):
        w.set(x, 3, 0, "minecraft:glass_pane")
    w.box(0, 5, 0, 10, 5, 8, "create:andesite_casing")
    roof(w, 0, -1, 10, 9, 6, "minecraft:dark_oak")
    w.set(5, 1, 3, "create:depot"); w.set(2, 1, 1, "create:schematic_table", facing="south")
    w.set(8, 1, 1, "minecraft:crafting_table"); w.set(9, 1, 1, "minecraft:barrel", facing="up", open="false")
    w.set(5, 4, 4, "minecraft:lantern", hanging="false", waterlogged="false")
    P["workshop"] = w
    # III. Expedition Hall: 13x9x11 stone hall, timber frame, archive wall, bench, display plinths.
    h = Plan(13, 10, 11)
    h.box(0, 0, 0, 12, 0, 10, "minecraft:polished_deepslate")
    h.walls(0, 0, 12, 10, 1, 5, "minecraft:stone_bricks", corner="minecraft:spruce_log")
    for y in (1, 2, 3):
        for x in range(2, 11):
            h.set(x, y, 0, "minecraft:bookshelf")
    h.set(6, 1, 1, "minecraft:lectern", facing="south", has_book="false", powered="false")
    h.set(1, 1, 5, "minecraft:smithing_table"); h.set(1, 1, 6, "minecraft:grindstone", face="floor", facing="east")
    for x in (4, 8):
        h.set(x, 1, 6, "minecraft:polished_andesite"); h.set(x, 1, 7, "minecraft:polished_andesite")
    for z in (3, 7):
        h.set(0, 3, z, "minecraft:glass_pane"); h.set(12, 3, z, "minecraft:glass_pane")
    door(h, 6, 1, 10)
    h.box(0, 6, 0, 12, 6, 10, "minecraft:spruce_planks")
    roof(h, 0, -1, 12, 11, 7, "minecraft:deepslate_brick")
    for x in (3, 9):
        h.set(x, 5, 5, "minecraft:lantern", hanging="false", waterlogged="false")
    P["hall"] = h
    # IV. Conservatory: 11x10x11 glass-roofed study around a central ritual plinth.
    c = Plan(11, 10, 11)
    c.box(0, 0, 0, 10, 0, 10, "minecraft:polished_blackstone_bricks")
    c.box(3, 0, 3, 7, 0, 7, "minecraft:amethyst_block")
    c.walls(0, 0, 10, 10, 1, 4, "minecraft:calcite", corner="minecraft:dark_oak_log")
    for x in (2, 4, 6, 8):
        for y in (2, 3):
            c.set(x, y, 0, "minecraft:tinted_glass"); c.set(x, y, 10, "minecraft:tinted_glass")
            c.set(0, y, x, "minecraft:tinted_glass"); c.set(10, y, x, "minecraft:tinted_glass")
    c.clear(5, 1, 10, 5, 2, 10); door(c, 5, 1, 10)
    for i in range(4):
        c.box(i, 5 + i, i, 10 - i, 5 + i, 10 - i, "minecraft:glass", hollow=False)
        c.clear(i + 1, 5 + i, i + 1, 9 - i, 5 + i, 9 - i)
    c.box(4, 9, 4, 6, 9, 6, "minecraft:glass")
    c.set(5, 1, 5, "minecraft:polished_blackstone"); c.set(5, 0, 5, "minecraft:lodestone")
    for x, z in ((2, 2), (8, 2), (2, 8), (8, 8)):
        c.set(x, 1, z, "minecraft:amethyst_cluster", facing="up", waterlogged="false")
    P["conservatory"] = c
    # V. Foundry: 13x9x13 brick bay with an iron gallery, chimney and machine floor.
    f = Plan(13, 12, 13)
    f.box(0, 0, 0, 12, 0, 12, "minecraft:smooth_stone")
    f.walls(0, 0, 12, 12, 1, 6, "minecraft:bricks", corner="create:brass_casing")
    f.clear(4, 1, 12, 8, 4, 12)
    for x in (3, 6, 9):
        f.set(x, 4, 0, "minecraft:iron_bars", east="false", north="false", south="false", west="false", waterlogged="false")
    for x in range(1, 12):
        f.set(x, 4, 1, "minecraft:iron_block") if x in (1, 11) else f.set(x, 4, 1, "minecraft:smooth_stone_slab", type="top")
    f.box(0, 7, 0, 12, 7, 12, "minecraft:bricks")
    f.box(9, 8, 9, 11, 11, 11, "minecraft:bricks", hollow=True)
    f.clear(10, 8, 10, 10, 11, 10)
    for x, z in ((3, 3), (9, 3), (3, 9), (9, 9)):
        f.set(x, 6, z, "minecraft:lantern", hanging="true", waterlogged="false")
    P["foundry"] = f
    # VI. Observatory: 9x17x9 stone tower, spiral landings, glass crown; the lens sits on the top-floor plinth.
    t = Plan(9, 17, 9)
    t.box(0, 0, 0, 8, 0, 8, "minecraft:polished_andesite")
    t.walls(0, 0, 8, 8, 1, 11, "minecraft:stone_bricks", corner="create:brass_casing")
    for y in (3, 7, 11):
        t.box(1, y, 1, 7, y, 7, "minecraft:spruce_planks")
        t.clear(1, y, 1, 2, y, 2)                # stair well
    for y in range(1, 12):
        t.set(1, y, 1, "minecraft:ladder", facing="south", waterlogged="false")
    for y in (5, 9):
        for x in (2, 6):
            t.set(x, y, 0, "minecraft:glass_pane"); t.set(x, y, 8, "minecraft:glass_pane")
    t.clear(4, 1, 8, 4, 2, 8); door(t, 4, 1, 8)
    t.box(0, 12, 0, 8, 12, 8, "minecraft:polished_andesite")
    t.walls(1, 1, 7, 7, 13, 15, "minecraft:glass")
    t.box(1, 16, 1, 7, 16, 7, "minecraft:glass")
    t.set(4, 13, 4, "minecraft:polished_blackstone")   # lens plinth: place the Observatory Lens on top (y 14)
    P["observatory"] = t
    return P


def emit_plans():
    P = plans()
    rows = ["# Headquarters plans (optional)", "",
            "GENERATED by scripts/gen_headquarters.py. Each plan is a Create schematic in `schematics/` (ships with the pack).",
            "Plans are suggestions: commissioning checks only the listed workstations near your charter, never the shape of the room.", "",
            "**Survival assembly:** craft a Schematic Table, Schematicannon and Schematic and Quill (Workshop reward). Put a plan in",
            "the table to write it onto an Empty Schematic, place it with the hologram (rotate/mirror freely), then either build by",
            "hand following the hologram or let a Schematicannon print it from the materials below. The cannon never replaces",
            "blocks you placed unless you set it to; the default `Do not Replace` mode is recommended.", "",
            "**Orientation:** every plan's entrance faces south (+Z) as saved. The waxed copper block in the Outpost marks a good",
            "charter spot. The Observatory's lens plinth is the polished blackstone block on the top floor.", ""]
    for pl in HQ["plans"]:
        p = P[pl["id"]]
        put(ROOT, f"schematics/{pl['file']}", p.bytes(), written_root)
        bill = p.bill()
        rows += [f"## {pl['title']} (stage {next(s['numeral'] for s in HQ['stages'] if s['id'] == pl['stage'])})", "",
                 f"`schematics/{pl['file']}` - {p.size[0]} x {p.size[1]} x {p.size[2]} (W x H x D), {sum(bill.values())} blocks.", "",
                 "| Material | Count |", "|---|---|"] + [f"| `{k}` | {v} |" for k, v in bill.items()] + [""]
    put(ROOT, "docs/HQ_PLANS.md", "\n".join(rows) + "\n", written_root)
    return len(HQ["plans"])


# ---------------------------------------------------------------- docs
def fmt_cost(c):
    return ", ".join(f"{n}x `{i}`" for i, n in c) or "none"


def req_line(r):
    return f"- **{r['text']}** (`{r['id']}`, {r['kind']}) - proves: {r['proves']}"


def emit_doc():
    L = ["# Headquarters campaign reference", "",
         "GENERATED by scripts/gen_headquarters.py from `manifests/headquarters.json`. Design and state rules: docs/PROGRESSION.md.", "",
         "> " + " ".join(HQ["fiction"]["premise"]), ""]
    for s in HQ["stages"]:
        L += [f"## {s['numeral']}. {s['title']} (`{s['id']}`)", "", s["summary"], "",
              f"*Survey log:* {s['log']}", "",
              f"- **Requires:** {', '.join(s['requires']) or 'nothing (place a Survey Charter)'}",
              f"- **Commission at:** the bound Survey Charter (right-click it; act within {HQ['charter']['interaction_radius']} blocks)",
              f"- **Contribution consumed once:** {fmt_cost(s['cost'])}",
              f"- **Unlocks:** {s['unlocks']}",
              f"- **Services:** {', '.join(HQ['services'][x]['title'] for x in s['services']) or 'none'}",
              f"- **Physical expression:** Station Emblem {s['numeral']} (`horizon:emblem_{s['id']}`)",
              f"- **Next:** {s['next']}", "", "Requirements:", ""]
        L += [req_line(r) for r in s["requirements"]] or ["- none beyond the choice below"]
        ch = s.get("choices")
        if ch:
            L += ["", f"**{ch['title']}: complete {ch['min']} of {len(ch['options'])}.** {ch['text']}", ""]
            for o in ch["options"]:
                L += [f"- **{o['title']}** (`{o['id']}`): {o['summary']} Contribution: {fmt_cost(o['cost'])}. {o['contribution']}"]
                L += ["  " + req_line(r) for r in o["requirements"]]
        L.append("")
    L += ["## Services", "", "| Service | Scope | Cooldown | Cost | What it does |", "|---|---|---|---|---|"]
    for k, sv in HQ["services"].items():
        L.append(f"| {sv['title']} (`{k}`) | {sv['scope']} | {sv['cooldown_ticks'] // 1200} min | {fmt_cost(sv['cost'])} | {sv['text']} |")
    put(ROOT, "docs/HEADQUARTERS.md", "\n".join(L) + "\n", written_root)


# ---------------------------------------------------------------- progression graph: alternatives and luck bottlenecks
def family_sizes():
    out = {}
    for f in FAM["families"]:
        t = DP / "horizon/tags/worldgen/structure/family" / f"{f}.json"   # written by gen_datapack.py (runs first)
        out[f] = len(json.loads(t.read_text())["values"]) if t.exists() else 0
    return out


def alternatives(adv, fams):
    """How many distinct world destinations can satisfy one advancement (structures for atlas, 1 for a boss/realm)."""
    if adv.startswith("horizon:atlas/"):
        return fams.get(adv.split("/")[1], 0), "structures"
    if adv.startswith("horizon:legend/"):
        return 1, "boss"
    if adv.startswith("horizon:trial/"):
        return 1, "trial (crafted gate, not luck)"
    if adv.startswith("horizon:realm/") or "enter" in adv:
        return 1, "realm"
    return 1, "crafted/processing (deterministic)"


def emit_graph():
    fams = family_sizes()
    rows = ["# Headquarters progression graph", "",
            "GENERATED by scripts/gen_headquarters.py. Every requirement with the number of world destinations that can satisfy it.",
            "Rule enforced at build time: a required discovery must have at least 3 eligible destinations, either inside one family",
            "(many structures) or across the alternatives of an any-of requirement / choice group. Deterministic steps (crafting,",
            "processing, building a room) are not luck and need no alternatives. Structure counts are registry counts, not density:",
            "observed travel time and density are recorded in docs/VALIDATION_REPORT.md where measured.", "",
            "```", "charter -> " + " -> ".join(f"{s['numeral']}.{s['id']}" for s in HQ["stages"]) + " -> post-campaign (Gauntlet, Hall of Legends)", "```", ""]
    bad = []
    for s in HQ["stages"]:
        rows += [f"## {s['numeral']}. {s['title']}", "", "| Requirement | Kind | Eligible destinations | Luck? |", "|---|---|---|---|"]
        groups = [("", s["requirements"])] + [(o["title"] + ": ", o["requirements"]) for o in (s.get("choices") or {}).get("options", [])]
        for prefix, reqs in groups:
            for r in reqs:
                if r["kind"] in ("block_any", "respawn_near"):
                    rows.append(f"| {prefix}{r['text']} | build at home | - | no |"); continue
                advs = [r["adv"]] if r["kind"] == "adv" else r["advs"]
                tot, kinds = 0, set()
                for a in advs:
                    n, k = alternatives(a, fams); tot += n; kinds.add(k)
                luckless = kinds <= {"crafted/processing (deterministic)", "trial (crafted gate, not luck)"}
                need = 1 if r["kind"] == "adv" else r["count"]
                spare = tot - need
                in_choice = bool(prefix)
                if not luckless and tot < 3 and not in_choice:
                    bad.append(f"{s['id']}/{r['id']}: only {tot} eligible destination(s)")
                rows.append(f"| {prefix}{r['text']} | {', '.join(sorted(kinds))} | {tot} for {need} needed (spare {spare})"
                            f"{' + other choices' if in_choice else ''} | {'no' if luckless else 'exploration'} |")
        if s.get("choices"):
            ch = s["choices"]
            rows.append(f"\n{ch['title']}: {ch['min']} of {len(ch['options'])} - {len(ch['options']) - ch['min']} spare route(s).")
        rows.append("")
    hearts = sum(1 for b in LEG["bosses"] if b["tier"] == "major")
    rows += ["## Relic gates", "",
             f"- Ancient Core (Expedition Hall High Landmarks route, Conservatory): first kill of any of {sum(1 for b in LEG['bosses'] if b['tier'] == 'mini')} mini-bosses, "
             "temple/landmark treasure rooms, and repeat kills of great legends (legends.json `repeat`).",
             f"- Starforged Heart (Observatory Lens, once): first kill of any of {hearts} great legends per player, or landmark vaults.",
             "- No stage reward, service, supply crate or founding kit contains a relic (validated); services that cost Wayfarer Shards",
             "  return maps, never relics, so no loop mints relics.", ""]
    put(ROOT, "docs/HQ_GRAPH.md", "\n".join(rows) + "\n", written_root)
    if bad:
        raise SystemExit("luck-only bottlenecks: " + "; ".join(bad))
    return fams


def main():
    validate()
    clean()
    emit_datapack()
    nf = emit_server_data()
    np_ = emit_plans()
    emit_doc()
    emit_graph()
    OWN_DP.write_text(json.dumps({"generator": "scripts/gen_headquarters.py", "files": sorted(written_dp)}, indent=1) + "\n", newline="\n")
    OWN_KJ.write_text(json.dumps({"generator": "scripts/gen_headquarters.py", "files": sorted(written_kj),
                                  "root_files": sorted(written_root)}, indent=1) + "\n", newline="\n")
    print(f"headquarters: {len(HQ['stages'])} stages, {sum(len((s.get('choices') or {}).get('options', [])) for s in HQ['stages'])} options, "
          f"{len(HQ['services'])} services, {nf} tracked facts, {np_} plans, {len(written_dp)} datapack files")


if __name__ == "__main__":
    main()
