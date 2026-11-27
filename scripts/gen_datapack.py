"""Generate the pack's data overrides into datapacks/ (shipped as kubejs/data).

Inputs (curated):  manifests/loot_families.json, manifests/legends.json, manifests/ids.json,
                   manifests/loot_audit.json (scripts/audit_loot.py), manifests/lock.json
Outputs (owned):   every file listed in datapacks/.generated.json - nothing else under datapacks/
                   is touched, so hand-written data (datapacks/<ns>/...) survives regeneration.
                   manifests/loot_report.json, docs/LOOT_BUDGET.md

1. Ore unification   - disable duplicate ore generators (biome modifiers -> neoforge:none)
2. Structure spacing - re-space selected structure sets (copied from the jar, spacing scaled)
3. Reward families   - classify every loot table into a curated family + role (vault/standard/filler),
                       solve per-table chances from per-structure budgets using real container counts,
                       inject relics/tokens/charts via NeoForge GLMs and family entries into Apotheosis'
                       own affix/gem injectors (first match wins, so they sit before the defaults)
4. Legends           - first-kill advancements (relic + trophy, once per player), repeat-kill drops
5. Atlas             - #horizon:family/<id> structure tags + discovery advancements (retroactive in quests)
6. Safety            - RS modded-loot import blacklist for Horizon items (RS re-rolls vanilla tables
                       through GLMs and would otherwise import Starforged Hearts into "common" RS chests)
Every id is checked against manifests/ids.json; unknown ids abort the build.
"""
import json, math, os, re, statistics, zipfile
from collections import defaultdict
from pathlib import Path
import sys as _sys; _sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)  # Windows long-path prefix \?\ - the repo may live deep on disk
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
OUT = ROOT / "datapacks"
OWNED = OUT / ".generated.json"
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
IDS = json.loads((ROOT / "manifests/ids.json").read_text())
LOCK = json.loads((ROOT / "manifests/lock.json").read_text())
LOCK = __import__('shipped', fromlist=['with_ports']).with_ports(LOCK)   # + shipped port jars (scripts/shipped.py)
FAM = json.loads((ROOT / "manifests/loot_families.json").read_text(encoding="utf-8"))
LEG = json.loads((ROOT / "manifests/legends.json").read_text(encoding="utf-8"))
AUDIT = json.loads((ROOT / "manifests/loot_audit.json").read_text())
EXP = json.loads((ROOT / "manifests/expeditions.json").read_text(encoding="utf-8"))
_CAL = ROOT / "manifests/loot_calibration.json"
CAL = json.loads(_CAL.read_text()) if _CAL.exists() else {}   # real placed structures (scripts/calibrate.py)

VANILLA_CHESTS = ["village/village_" + v for v in ("armorer", "butcher", "cartographer", "desert_house", "fisher", "fletcher", "mason",
                  "plains_house", "savanna_house", "shepherd", "snowy_house", "taiga_house", "tannery", "temple", "toolsmith", "weaponsmith")] + [
    "ruined_portal", "shipwreck_map", "shipwreck_supply", "shipwreck_treasure", "abandoned_mineshaft", "simple_dungeon", "pillager_outpost",
    "igloo_chest", "underwater_ruin_small", "underwater_ruin_big", "stronghold_corridor", "stronghold_crossing", "stronghold_library",
    "bastion_bridge", "bastion_hoglin_stable", "bastion_other", "bastion_treasure", "ancient_city", "ancient_city_ice_box", "woodland_mansion",
    "nether_bridge", "buried_treasure", "jungle_temple", "desert_pyramid", "end_city_treasure"]
IDS["loot_table"] = sorted(set(IDS["loot_table"]) | {f"minecraft:chests/{c}" for c in VANILLA_CHESTS}
                           | {f"minecraft:entities/{e}" for e in ("ender_dragon", "wither", "warden", "elder_guardian")})
IDS["structure"] = sorted(set(IDS["structure"]) | set(FAM["vanilla_structures"]))
HORIZON_ITEMS = {"horizon:wayfarer_shard", "horizon:ancient_core", "horizon:starforged_heart"} | \
                {f["token"] for f in FAM["families"].values() if f.get("token")}
TROPHY = lambda boss: "horizon:trophy_" + boss.split(":")[1]
written = []


def need(kind, i):
    if i.startswith("horizon:"):
        return i
    if i.startswith("minecraft:") and kind in ("entity", "item"):
        return i
    if i not in IDS[kind]:
        raise SystemExit(f"unknown {kind} id: {i}")
    return i


def write(rel, obj):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    text = obj if isinstance(obj, str) else json.dumps(obj, indent=2) + "\n"
    p.write_text(text, encoding="utf-8")
    written.append(rel.replace("\\", "/"))


def clean_previous():
    """Delete only files this script wrote last time. Legacy: if no manifest exists yet, the 0.1.0 layout
    (fully generated) is removed per known subtree, never datapacks/ as a whole."""
    if OWNED.exists():
        for rel in json.loads(OWNED.read_text())["files"]:
            (OUT / rel).unlink(missing_ok=True)
    else:
        legacy = ["horizon/loot_modifiers", "horizon/loot_table/inject", "horizon/tags/worldgen/structure/arise_any.json",
                  "neoforge/loot_modifiers/global_loot_modifiers.json", "modern_industrialization/neoforge", "powah/neoforge",
                  "apotheosis/worldgen", "dungeons_arise/worldgen", "mowziesmobs/worldgen"]
        for rel in legacy:
            p = OUT / rel
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                for f in sorted(p.rglob("*"), reverse=True):
                    f.unlink() if f.is_file() else f.rmdir()
                p.rmdir()
    for d in sorted((p for p in OUT.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()


def jar_json(ns_path):  # "ns:worldgen/structure_set/x" -> parsed json from whichever jar has it
    ns, path = ns_path.split(":")
    name = f"data/{ns}/{path}.json"
    for m in LOCK["mods"]:
        with zipfile.ZipFile(CACHE / m["file"]) as z:
            if name in z.namelist():
                return json.loads(z.read(name))
    raise SystemExit(f"not found in jars: {name}")


# ---------------------------------------------------------------- 1. ores
DISABLE_ORES = [
    *(f"modern_industrialization:{p}ore_generator_{o}" for o in ("tin", "lead", "uranium") for p in ("", "deepslate_")),
    "powah:uraninite_ore", "powah:uraninite_ore_dense", "powah:uraninite_ore_poor",
]
# ------------------------------------------------------- 2. structure spacing
STRUCTURE_SETS = [
    ("dungeons_arise:major_structures", 44, 30, "rare/legendary landmarks (was 60/44; nearest landmark was 1.9-4.0 km from spawn on 3 seeds)"),
    ("mowziesmobs:frostmaw_spawns", 40, 16, "rare mini-boss"),
    ("mowziesmobs:monasteries", 36, 14, "rare mini-boss"),
    ("mowziesmobs:umvuthana_groves", 36, 14, "rare mini-boss"),
    ("mowziesmobs:wrought_chambers", 24, 10, "uncommon mini-boss"),
    ("apotheosis:towers", 32, 20, "uncommon boss tower"),
    # 0.3.0 expansion: boss arenas join the mini-boss tiers; dense sets thinned next to YUNG's mineshafts
    ("bosses_of_mass_destruction:gauntlet_arena", 40, 16, "rare mini-boss (was 32/16)"),
    ("block_factorys_bosses:yeti_hideout", 40, 20, "rare mini-boss (was 30/25)"),
    ("spider_overhaul:birch_spidernest", 28, 12, "spider nests were 8/6 (near-every-region)"),
    ("mmr:mesa_mineshaft", 40, 20, "extra mineshafts next to YUNG's Better Mineshafts (was 12/4)"),
    ("mmr:mushroom_mineshaft", 40, 20, "extra mineshafts next to YUNG's Better Mineshafts (was 16/6)"),
    ("mmr:deep_dark_mineshaft", 40, 20, "extra mineshafts next to YUNG's Better Mineshafts (was 20/10)"),
]


# ------------------------------------------------------- 3. reward families
def first(rules, key):
    for rx, fam in rules:
        if re.search(rx, key):
            return fam
    return None


def role_of(table):
    path = table.split(":", 1)[1]
    if re.search(FAM["roles"]["skip"], path):
        return None
    for role in ("vault", "filler"):
        if re.search(FAM["roles"][role], path):
            return role
    return "standard"


def is_container_table(t):
    ns, path = t.split(":", 1)
    if path.startswith(("entities/", "entity/", "blocks/", "block/", "gameplay/", "equipment/", "shearing/", "archaeology/")):
        return False
    return True


def classify_all():
    out = {}
    for t in IDS["loot_table"]:
        if not is_container_table(t):
            continue
        fam = first(FAM["tables"], t)
        if not fam:
            continue
        role = role_of(t)
        if role:
            out[t] = (fam, role)
    return out


TWO_LEVEL = {"repurposed_structures", "ctov", "towns_and_towers", "kaisyn", "minecraft", "mmr"}   # <category>/<variant>/... layouts
_SPATHS = defaultdict(list)
for _s in IDS["structure"]:
    _SPATHS[_s.split(":")[0]].append(_s.split(":")[1])


def group_key(tpl):
    """Template -> the structure it belongs to. Flat template names (Cataclysm: acropolis_30, frosted_prison_bottom_7,
    ruined_citadel15) map to the longest structure id of the same namespace they start with; nested layouts use folders."""
    ns, p = tpl.split(":", 1)
    seg = p.split("/")
    cands = [s for s in _SPATHS.get(ns, []) if "/" not in s and (seg[0] == s or (seg[0].startswith(s) and len(s) >= 5))]
    if cands:
        return ns + ":" + max(cands, key=len)
    return ns + ":" + "/".join(seg[:2] if ns in TWO_LEVEL and len(seg) > 2 else seg[:1])


# 0.3.0 expansion namespaces: their structures only constrain their OWN tables. Grim Kingdoms (vanilla chest
# tables only) and others reusing foreign tables therefore keep the calibrated vanilla/baseline chances unchanged.
OWN_TABLES_ONLY = {"mmr", "grim_kingdoms", "homesteads", "bosses_of_mass_destruction", "block_factorys_bosses",
                   "companions", "spider_overhaul"}
VERSIONED = {"mmr": "mmr:1_21_0/"}   # Moog's versioned pool elements: 1.21.1 resolves to the 1_21_0 templates


def groups_from_audit():
    """template group (ns:first path segment) -> {table: containers}. Every template counted once (upper bound
    for unique pieces; jigsaw repeats of the same piece make real totals higher, see in-game samples)."""
    g = defaultdict(lambda: defaultdict(int))
    for tpl, counts in AUDIT["templates"].items():
        ns = tpl.split(":", 1)[0]
        if ns in VERSIONED and not tpl.startswith(VERSIONED[ns]):
            continue        # template for another Minecraft version (never placed on 1.21.1)
        key = group_key(tpl)
        for tb, n in counts.items():
            if ns in OWN_TABLES_ONLY and not tb.startswith(ns + ":"):
                continue    # 0.3.0 additions must not lower the calibrated chances of tables they merely reuse
            g[key][tb] += n
    for st, c in CAL.items():          # measured container counts replace the unique-template estimate
        g[st] = defaultdict(int, c["tables"])
    return g


def solve(classes):
    """Per table and reward kind: chance = min over structure groups using the table of
    budget * normalized_role_share / containers_of_that_role_in_group."""
    groups = groups_from_audit()
    split, cap = FAM["split"], FAM["max_chance"]
    kinds = list(split)
    chance = defaultdict(dict)        # table -> kind -> p
    used_in = defaultdict(set)
    group_family = {}
    for gk, tabs in groups.items():
        fams = defaultdict(int)
        for tb, n in tabs.items():
            if tb in classes:
                fams[classes[tb][0]] += n
        if not fams:
            continue
        group_family[gk] = max(fams, key=fams.get)
        for tb in tabs:
            if tb in classes:
                used_in[tb].add(gk)
    # reference size for tables never seen in a template (placed by code/processors)
    fam_sizes = defaultdict(list)
    for gk, tabs in groups.items():
        f = group_family.get(gk)
        if f:
            fam_sizes[f].append({r: sum(n for tb, n in tabs.items() if classes.get(tb, (None,))[0] == f and classes[tb][1] == r)
                                 for r in ("vault", "standard", "filler")})
    ref = {f: {r: max(1.0, statistics.median([s[r] for s in v] or [4])) for r in ("vault", "standard", "filler")} for f, v in fam_sizes.items()}

    def share(kind, role, present):
        tot = sum(split[kind].get(r, 0) for r in present)
        return split[kind].get(role, 0) / tot if tot else 0.0

    for tb, (fam, role) in classes.items():
        budget = FAM["families"][fam]["budget"]
        for kind in kinds:
            b = budget.get(kind, 0)
            if b <= 0:
                continue
            cands = []
            for gk in used_in.get(tb, ()):
                tabs = groups[gk]
                cnt = defaultdict(int)
                for t2, n in tabs.items():
                    if t2 in classes and classes[t2][0] == fam:
                        cnt[classes[t2][1]] += n
                present = [r for r in cnt if cnt[r] > 0]
                s = share(kind, role, present)
                if s and cnt[role]:
                    cands.append(b * s / (cnt[role] * MEAN_COUNT.get(kind, 1.0)))
            if not used_in.get(tb):
                r = ref.get(fam, {"vault": 4, "standard": 6, "filler": 6})
                s = share(kind, role, [x for x in ("vault", "standard", "filler") if r.get(x)])
                if s:
                    cands.append(b * s / (r[role] * MEAN_COUNT.get(kind, 1.0)))
            if cands:
                p = min(min(cands), cap[kind])
                if p >= 0.004:
                    chance[tb][kind] = round(p, 3)
    return chance, groups, group_family


MEAN_COUNT = {"token": 1.5}


def chance_entry(item, p, count=(1, 1), extra_fn=None):
    fns = []
    if count != (1, 1):
        fns.append({"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": count[0], "max": count[1]}})
    if extra_fn:
        fns = extra_fn + fns
    return {"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": p}],
            "entries": [{"type": "minecraft:item", "name": item, **({"functions": fns} if fns else {})}]}


def map_entry(clue, p, name):
    cm = FAM["clue_maps"][clue]
    fn = [{"function": "minecraft:exploration_map", "destination": f"horizon:clue/{clue}", "decoration": cm["decoration"],
           "zoom": 2, "search_radius": cm["search_radius"], "skip_existing_chunks": True},
          {"function": "minecraft:set_name", "target": "item_name", "name": {"text": name, "color": "gold", "italic": False}}]
    return {"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": p}],
            "entries": [{"type": "minecraft:item", "name": "minecraft:map", "functions": fn}]}


def emit_families(classes, chance, groups, group_family):
    items = FAM["items"]
    inject = {}          # signature -> (table name, pools)
    members = defaultdict(list)
    for tb in sorted(classes):
        fam, role = classes[tb]
        f = FAM["families"][fam]
        c = chance.get(tb, {})
        pools, sig = [], []
        for kind in ("shard", "core", "heart"):
            if kind in c:
                pools.append(chance_entry(need("item", items[kind]), c[kind]))
                sig.append((kind, c[kind]))
        if "token" in c and f.get("token"):
            pools.append(chance_entry(f["token"], c["token"], (1, 2)))
            sig.append(("token", c["token"]))
        for ex in f.get("extras", []):
            if re.search(ex["match"], tb.split(":", 1)[1]):
                kind, ref = ex["entry"].split(":", 1)
                if kind == "map":
                    pools.append(map_entry(ref.split("/")[-1], ex["chance"], ex["name"]))
                else:
                    pools.append(chance_entry(need("item", ref), ex["chance"], tuple(ex.get("count", (1, 1)))))
                sig.append((ex["entry"], ex["chance"]))
        if not pools:
            continue
        key = (fam, role, tuple(sig))
        if key not in inject:
            name = f"{fam}/{role}_{len([k for k in inject if k[0] == fam and k[1] == role])}"
            inject[key] = (name, pools)
        members[inject[key][0]].append(tb)
    mods = []
    for key, (name, pools) in sorted(inject.items(), key=lambda kv: kv[1][0]):
        write(f"horizon/loot_table/inject/{name}.json", {"type": "minecraft:chest", "pools": pools})
        mname = "family_" + name.replace("/", "_")
        write(f"horizon/loot_modifiers/{mname}.json", {
            "type": "neoforge:add_table",
            "conditions": [{"condition": "minecraft:any_of", "terms": [{"condition": "neoforge:loot_table_id", "loot_table_id": t}
                                                                        for t in sorted(members[name])]}],
            "table": f"horizon:inject/{name}"})
        mods.append(f"horizon:{mname}")
    return mods, members


def emit_apotheosis(classes, chance):
    """Family-aware entries placed BEFORE Apotheosis' defaults in its own injectors (first match wins).
    Tables in a family always get an explicit entry, which also covers namespaces whose paths do not start
    with 'chests' (Incendium, Terralith, Structory, Towns & Towers, Bumblezone) and were previously skipped."""
    base_affix = jar_json("apotheosis:loot_modifiers/affix_loot_injection")
    base_gem = jar_json("apotheosis:loot_modifiers/gem_loot_injection")
    buckets_a, buckets_g = defaultdict(list), defaultdict(list)
    for tb, (fam, role) in classes.items():
        f = FAM["families"][fam]
        c = chance.get(tb, {})
        ns, path = tb.split(":", 1)
        rar = tuple(f.get("apotheosis_vault_rarities", [])) if role == "vault" else ()
        gems = tuple(f.get("apotheosis_gems", []))
        buckets_a[(ns, round(c.get("affix", 0.0), 2), rar)].append(path)
        buckets_g[(ns, round(c.get("gem", 0.0), 2), gems)].append(path)

    def entries(buckets, extra_key):
        out = []
        for (ns, p, extra), paths in sorted(buckets.items()):
            e = {"chance": p, "pattern": {"domain": ns, "path_regex": "(?:" + "|".join(re.escape(x) for x in sorted(paths)) + ")"}}
            if extra:
                e[extra_key] = list(extra)
            out.append(e)
        return out
    for g in (FAM["families"][f].get("apotheosis_gems", []) for f in FAM["families"]):
        for gem in g:
            if f"data/{gem.split(':')[0]}/gems/{gem.split(':')[1]}.json" not in jar_index():
                raise SystemExit(f"unknown apotheosis gem {gem}")
    a = dict(base_affix); a["entries"] = entries(buckets_a, "rarities") + base_affix["entries"]
    g = dict(base_gem); g["entries"] = entries(buckets_g, "gems") + base_gem["entries"]
    write("apotheosis/loot_modifiers/affix_loot_injection.json", a)
    write("apotheosis/loot_modifiers/gem_loot_injection.json", g)
    return len(a["entries"]) - len(base_affix["entries"]), len(g["entries"]) - len(base_gem["entries"])


_JI = None


def jar_index():
    global _JI
    if _JI is None:
        _JI = set()
        for m in LOCK["mods"]:
            with zipfile.ZipFile(CACHE / m["file"]) as z:
                _JI.update(z.namelist())
    return _JI


# ---------------------------------------------------------------- 4. legends
def emit_legends():
    mods = []
    items = FAM["items"]
    for b in LEG["bosses"]:
        ent = need("entity", b["id"])
        ns, p = ent.split(":")
        relic = items["heart"] if b["tier"] == "major" else items["core"]
        write(f"horizon/loot_table/rewards/legend/{p}.json", {"type": "minecraft:advancement_reward", "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": relic}]},
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": TROPHY(ent)}]}]})
        write(f"horizon/advancement/legend/{p}.json", {
            "criteria": {
                "kill": {"trigger": "minecraft:player_killed_entity",
                         "conditions": {"entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": ent}}]}},
                "party": {"trigger": "minecraft:impossible"}},
            "requirements": [["kill", "party"]],
            "rewards": {"loot": [f"horizon:rewards/legend/{p}"], "function": f"horizon:fx/legend_{b['tier']}"}})
        table = f"{ns}:entities/{p}"
        if b["repeat"] and table in IDS["loot_table"]:
            write(f"horizon/loot_table/inject/legend_repeat/{p}.json", {"type": "minecraft:entity", "pools": [
                {"rolls": 1, "conditions": [{"condition": "minecraft:killed_by_player"}],
                 "entries": [{"type": "minecraft:item", "name": items[b["repeat"]]}]}]})
            write(f"horizon/loot_modifiers/legend_repeat_{p}.json", {
                "type": "neoforge:add_table",
                "conditions": [{"condition": "neoforge:loot_table_id", "loot_table_id": table}],
                "table": f"horizon:inject/legend_repeat/{p}"})
            mods.append(f"horizon:legend_repeat_{p}")
    # feedback functions (advancement rewards run as the player, at the player). Viewers who ran
    # "/horizon fx quiet" carry the tag horizon_fx_quiet and see/hear nothing.
    write("horizon/function/fx/legend_major.mcfunction",
          "particle minecraft:totem_of_undying ~ ~1.2 ~ 0.7 1.0 0.7 0.35 70 normal @a[distance=..48,tag=!horizon_fx_quiet]\n"
          "particle minecraft:end_rod ~ ~1.2 ~ 0.4 1.4 0.4 0.05 30 normal @a[distance=..48,tag=!horizon_fx_quiet]\n"
          "execute as @a[distance=..48,tag=!horizon_fx_quiet] at @s run playsound horizon:cue.trophy player @s ~ ~ ~ 1 1\n"
          "title @s[tag=!horizon_fx_quiet] actionbar {\"text\":\"Legend defeated - a Starforged Heart and a trophy are yours\",\"color\":\"light_purple\"}\n")
    write("horizon/function/fx/legend_mini.mcfunction",
          "particle minecraft:end_rod ~ ~1.2 ~ 0.4 1.0 0.4 0.04 24 normal @a[distance=..48,tag=!horizon_fx_quiet]\n"
          "execute as @a[distance=..48,tag=!horizon_fx_quiet] at @s run playsound horizon:cue.legend_slain player @s ~ ~ ~ 1 1\n"
          "title @s[tag=!horizon_fx_quiet] actionbar {\"text\":\"Foe vanquished - an Ancient Core and a trophy are yours\",\"color\":\"aqua\"}\n")
    write("horizon/function/fx/discover.mcfunction",
          "execute at @s[tag=!horizon_fx_quiet] run playsound horizon:cue.rare_loot player @s ~ ~ ~ 1 1\n")
    return mods


# ---------------------------------------------------------------- dead loot-table references
FALLBACK_KINDS = {   # keyword in the table path -> kind; first match wins
    "scholar": r"(wizard|occultist|scribe|library|book|alchemist|monk|obelisk|shrine|jewel)",
    "arms": r"(gunsmith|barracks|archery|smith|hunter|miner|mechanic|engineer)",
    "pantry": r"(tavern|cooker|kennel|butcher|horticulturist|botanist|oceanograph|netherolog|climatolog|petshop|gazebo|windmill|scavenger)",
}
FALLBACK_POOLS = {
    "house": [("minecraft:bread", 1, 4, 8), ("minecraft:apple", 1, 3, 6), ("minecraft:emerald", 1, 3, 5), ("minecraft:torch", 2, 8, 6), ("minecraft:paper", 1, 4, 4), ("minecraft:iron_ingot", 1, 2, 3)],
    "scholar": [("minecraft:paper", 2, 6, 8), ("minecraft:book", 1, 2, 6), ("minecraft:lapis_lazuli", 2, 6, 5), ("minecraft:experience_bottle", 1, 1, 2), ("minecraft:emerald", 1, 2, 4)],
    "arms": [("minecraft:iron_nugget", 3, 9, 8), ("minecraft:arrow", 4, 12, 6), ("minecraft:leather", 1, 3, 5), ("minecraft:iron_ingot", 1, 3, 4), ("minecraft:emerald", 1, 2, 4)],
    "pantry": [("minecraft:bread", 2, 5, 8), ("minecraft:cooked_beef", 1, 3, 5), ("minecraft:carrot", 2, 6, 6), ("minecraft:baked_potato", 1, 4, 5), ("minecraft:emerald", 1, 2, 3)],
}


def emit_fallbacks():
    """Village-house and shop templates from other mods reference loot tables that no installed jar defines (80 ids in
    0.3.1), so every such chest was empty. Define each missing id as a small themed table (+ a modest Wayfarer Shard chance)."""
    kinds = defaultdict(int)
    for k, entries in FALLBACK_POOLS.items():
        write(f"horizon/loot_table/fallback/{k}.json", {"type": "minecraft:chest", "pools": [
            {"rolls": {"min": 2, "max": 4}, "entries": [
                {"type": "minecraft:item", "name": n, "weight": w, "functions": [{"function": "minecraft:set_count", "count": {"min": lo, "max": hi}}]}
                for n, lo, hi, w in entries]},
            {"rolls": 1, "conditions": [{"condition": "minecraft:random_chance", "chance": 0.12}],
             "entries": [{"type": "minecraft:item", "name": FAM["items"]["shard"]}]}]})
    for t in sorted(AUDIT["per_table"]):
        if t in IDS["loot_table"] or not is_container_table(t) or not role_of(t) or t.startswith("wares:"):
            continue
        ns, path = t.split(":", 1)
        kind = next((k for k, rx in FALLBACK_KINDS.items() if re.search(rx, path)), "house")
        write(f"{ns}/loot_table/{path}.json", {"type": "minecraft:chest", "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:loot_table", "value": f"horizon:fallback/{kind}"}]}]})
        kinds[kind] += 1
    return dict(kinds)


# ---------------------------------------------------------------- 5. atlas
def emit_atlas():
    fam_structs = defaultdict(list)
    for s in IDS["structure"]:
        f = first(FAM["structures"], s)
        if f:
            fam_structs[f].append(s)
    for f, ss in sorted(fam_structs.items()):
        write(f"horizon/tags/worldgen/structure/family/{f}.json", {"replace": False, "values": sorted(ss)})
        write(f"horizon/advancement/atlas/{f}.json", {
            "criteria": {"found": {"trigger": "minecraft:location", "conditions": {"player": [
                {"condition": "minecraft:entity_properties", "entity": "this",
                 "predicate": {"location": {"structures": f"#horizon:family/{f}"}}}]}}},
            "rewards": {"function": "horizon:fx/discover"}})
    for clue, cm in FAM["clue_maps"].items():
        vals = sorted({s for f in cm["from"] for s in fam_structs.get(f, [])})
        write(f"horizon/tags/worldgen/structure/clue/{clue}.json", {"replace": False, "values": vals})
    # legacy tag kept for quests / docs (any When Dungeons Arise structure)
    write("horizon/tags/worldgen/structure/arise_any.json", {"values": sorted(s for s in IDS["structure"] if s.startswith("dungeons_arise:"))})
    return {f: len(v) for f, v in fam_structs.items()}


# ---------------------------------------------------------------- expeditions: exchange, salvage, trials
def jar_files(prefix_re):
    out = {}
    for m in LOCK["mods"]:
        with zipfile.ZipFile(CACHE / m["file"]) as z:
            for n in z.namelist():
                if re.match(prefix_re, n) and n.endswith(".json"):
                    try:
                        out[n] = json.loads(z.read(n))
                    except Exception:
                        pass
    return out


def expand_tag(tag, tagfiles, seen=None):
    ns, p = tag.split(":")
    seen = seen or set()
    vals = []
    for n, d in tagfiles.items():
        if n in (f"data/{ns}/tags/item/{p}.json", f"data/{ns}/tags/items/{p}.json"):
            for v in d.get("values", []):
                v = v["id"] if isinstance(v, dict) else v
                if v.startswith("#"):
                    if v not in seen:
                        seen.add(v)
                        vals += expand_tag(v[1:], tagfiles, seen)
                else:
                    vals.append(v)
    return sorted(set(vals))


def craftable_outputs():
    outs = set()
    for n, d in jar_files(r"data/[^/]+/recipes?/").items():
        res = d.get("result") or d.get("output") or d.get("results") or []
        for r in (res if isinstance(res, list) else [res]):
            if isinstance(r, str):
                outs.add(r)
            elif isinstance(r, dict):
                i = r.get("id") or r.get("item")
                if isinstance(i, str):
                    outs.add(i)
    return outs


def gem_min_purity(gem):
    ns, p = gem.split(":")
    for m in LOCK["mods"]:
        with zipfile.ZipFile(CACHE / m["file"]) as z:
            n = f"data/{ns}/gems/{p}.json"
            if n in z.namelist():
                return json.loads(z.read(n)).get("min_purity", "chipped")
    raise SystemExit(f"unknown gem {gem}")


def gem_stack(gem, purity):
    return {"id": "apotheosis:gem", "count": 1, "components": {"apotheosis:gem": gem, "apotheosis:purity": purity}}


def emit_expeditions():
    order = ["cracked", "chipped", "flawed", "normal", "flawless", "perfect"]
    ex = EXP["exchange"]
    n_ex = 0
    for token, gems in ex["offers"].items():
        for gem in gems:
            pur = max("flawed", gem_min_purity(gem), key=order.index)
            write(f"horizon/recipe/exchange/{token.split(':')[1]}_{gem.split('/')[-1]}.json", {
                "type": "minecraft:crafting_shapeless", "category": "misc", "group": "horizon_exchange",
                "ingredients": [{"item": token}] * ex["cost"] + [{"item": "apotheosis:gem_dust"}] * ex["dust"],
                "result": gem_stack(gem, pur)})
            n_ex += 1
    tagfiles = jar_files(r"data/[^/]+/tags/items?/")
    crafted = craftable_outputs()
    n_salv, salvaged = 0, {}
    for sv in EXP["salvage"]:
        items = [i for i in expand_tag(sv["tag"], tagfiles) if i not in sv["exclude"] and i not in crafted]
        dropped = [i for i in expand_tag(sv["tag"], tagfiles) if i in crafted and i not in sv["exclude"]]
        salvaged[sv["name"]] = {"items": len(items), "excluded_craftable": dropped, "excluded_manual": sv["exclude"]}
        for i in items:
            need("item", i)
        for o in sv["outputs"]:
            need("item", o[0])
        write(f"horizon/recipe/salvaging/{sv['name']}.json", {
            "type": "apotheosis:salvaging", "input": [{"item": i} for i in items],
            "outputs": [{"min_count": o[1], "max_count": o[2], "stack": {"id": o[0], "count": 1}} for o in sv["outputs"]]})
        n_salv += 1
    for t in EXP["trials"]:
        waves = []
        for w in t["waves"]:
            waves.append({"entities": [{"entity": need("entity", e), "count": c} for e, c in w["entities"]],
                          "modifiers": [], "rewards": [], "max_wave_time": w["time"], "setup_time": 160})
        rw = t["rewards"]
        rewards = [{"type": "gateways:counted", "count": rw["affix_count"], "reward": {"type": "apotheosis:affix_item", "rarities": rw["affix"]}}]
        if rw.get("affix2"):
            rewards.append({"type": "apotheosis:affix_item", "rarities": rw["affix2"]})
        if rw.get("gems"):
            for g in rw["gems"]:
                gem_min_purity(g)
            rewards.append({"type": "apotheosis:gem", "gems": rw["gems"], "purities": rw["purities"]})
        if rw.get("random_gems"):
            rewards.append({"type": "gateways:counted", "count": rw["random_gems"],
                            "reward": {"type": "apotheosis:true_random_gem", "purities": rw["purities"]}})
        rewards.append({"type": "gateways:experience", "experience": rw["xp"], "orb_size": 50})
        write(f"horizon/gateways/trial/{t['id']}.json", {"size": t["size"], "color": t["color"], "waves": waves, "rewards": rewards})
        # granted by kubejs/server_scripts/horizon_events.js on GateEvent$Completed (everyone near the gate)
        write(f"horizon/advancement/trial/{t['id']}.json", {"criteria": {"done": {"trigger": "minecraft:impossible"}},
                                                           "rewards": {"function": "horizon:fx/legend_mini"}})
        ing = []
        for item, n in t["cost"].items():
            ing += [{"item": need("item", item)}] * n
        if len(ing) > 9:
            raise SystemExit(f"trial {t['id']}: recipe has {len(ing)} > 9 ingredients")
        write(f"horizon/recipe/trial/{t['id']}.json", {
            "type": "minecraft:crafting_shapeless", "category": "misc", "group": "horizon_trials",
            "ingredients": ing + [{"item": "minecraft:ender_pearl"}] * (1 if len(ing) < 9 else 0),
            "result": {"id": "gateways:gate_pearl", "count": 1, "components": {"gateways:gateway": f"horizon:trial/{t['id']}"}}})
    (ROOT / "manifests/salvage_report.json").write_text(json.dumps(salvaged, indent=1))
    return n_ex, n_salv, len(EXP["trials"])


# ---------------------------------------------------------------- report
def report(classes, chance, groups, group_family, members):
    rows = []
    for gk, tabs in groups.items():
        f = group_family.get(gk)
        if not f:
            continue
        exp = defaultdict(float)
        p0 = 1.0
        n = 0
        for tb, cnt in tabs.items():
            if tb not in classes:
                continue
            n += cnt
            c = chance.get(tb, {})
            for k, p in c.items():
                mult = MEAN_COUNT.get(k, 1.0)
                exp[k] += cnt * p * mult
            p0 *= (1 - c.get("heart", 0)) ** cnt
        rows.append({"group": gk, "family": f, "containers": n, "calibrated": gk in CAL, **{k: round(v, 2) for k, v in exp.items()},
                     "p_heart_ge1": round(1 - p0, 2)})
    rows.sort(key=lambda r: (r["family"], -r["containers"]))
    fams = sorted({r["family"] for r in rows})
    unassigned = sorted(t for t in AUDIT["per_table"] if t not in classes and is_container_table(t) and role_of(t))
    out = {"tables_classified": len(classes), "inject_tables": len(members),
           "by_family": {f: sum(1 for t in classes.values() if t[0] == f) for f in fams},
           "placed_but_unassigned": unassigned, "groups": rows}
    (ROOT / "manifests/loot_report.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    old = (ROOT / "manifests/loot_tiers.json")
    if old.exists():
        old.unlink()  # superseded by loot_report.json
    md = ["# Loot budget report (generated)", "",
          "Expected Horizon rewards for one full clear of each structure group, computed by `scripts/gen_datapack.py` from the",
          "real container counts in the structure templates (`scripts/audit_loot.py`). Each template is counted once; jigsaw",
          "structures that repeat a piece have more containers, so treat these as per-unique-layout figures. Apotheosis' affix",
          "and gem numbers are the expected count of injected affix items / gems on top of each structure's own loot.",
          "Rows marked **(measured)** use container counts from real placed structures (`scripts/calibrate.py`), which include",
          "repeated jigsaw pieces; the solver budgets those structures from the measured counts.", "",
          f"Tables classified: {len(classes)} - inject tables: {len(members)} - placed but unassigned (no Horizon injection): {len(unassigned)}", ""]
    for f in fams:
        fr = [r for r in rows if r["family"] == f]
        md += [f"## {FAM['families'][f]['title']} (`{f}`) - {len(fr)} structure groups", "",
               "| Structure group | Containers | Shards | Cores | Hearts | P(>=1 heart) | Tokens | Affix items | Gems |",
               "|---|---|---|---|---|---|---|---|---|"]
        for r in sorted(fr, key=lambda r: (not r.get("calibrated"), -r["containers"]))[:25]:
            md.append(f"| `{r['group']}`{' **(measured)**' if r.get('calibrated') else ''} | {r['containers']} | {r.get('shard', 0)} | {r.get('core', 0)} | {r.get('heart', 0)} | "
                      f"{r['p_heart_ge1']} | {r.get('token', 0)} | {r.get('affix', 0)} | {r.get('gem', 0)} |")
        if len(fr) > 25:
            md.append(f"| ... {len(fr) - 25} smaller groups | | | | | | | | |")
        md.append("")
    (ROOT / "docs/LOOT_BUDGET.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return rows


def assert_budgets(rows):
    """Hard ceilings so a curation mistake cannot silently re-create the 0.1.0 flood."""
    limits = {"heart": 2.0, "core": 5.0, "shard": 12.0, "token": 6.0}
    bad = [(r["group"], k, r[k]) for r in rows for k, lim in limits.items() if r.get(k, 0) > lim * 1.001]
    if bad:
        raise SystemExit("budget exceeded: " + "; ".join(f"{g} {k}={v}" for g, k, v in bad[:20]))


def main():
    clean_previous()
    for bm in DISABLE_ORES:
        need("biome_modifier", bm)
        ns, p = bm.split(":")
        write(f"{ns}/neoforge/biome_modifier/{p}.json", {"type": "neoforge:none"})
    for sid, spacing, sep, why in STRUCTURE_SETS:
        need("structure_set", sid)
        d = jar_json(sid.replace(":", ":worldgen/structure_set/"))
        d["placement"]["spacing"], d["placement"]["separation"] = spacing, sep
        ns, p = sid.split(":")
        write(f"{ns}/worldgen/structure_set/{p}.json", d)

    classes = classify_all()
    chance, groups, group_family = solve(classes)
    mods, members = emit_families(classes, chance, groups, group_family)
    na, ng = emit_apotheosis(classes, chance)
    mods += emit_legends()
    atlas = emit_atlas()
    fb = emit_fallbacks()
    print("fallback loot tables:", fb)
    nx, ns_, nt = emit_expeditions()
    write("neoforge/loot_modifiers/global_loot_modifiers.json", {"replace": False, "entries": mods})
    for clue in FAM["clue_maps"]:   # quest-reward charts (Heracles loot-table reward)
        write(f"horizon/loot_table/rewards/quest/chart_{clue}.json", {"type": "minecraft:chest", "pools": [map_entry(clue, 1.0, "Surveyor's Chart")]})
    tokens = sorted(f["token"] for f in FAM["families"].values() if f.get("token"))
    write("horizon/tags/item/tokens.json", {"replace": False, "values": tokens})
    write("horizon/tags/item/relics.json", {"replace": False, "values": sorted(FAM["items"].values())})
    write("horizon/tags/item/trophies.json", {"replace": False, "values": sorted(TROPHY(b["id"]) for b in LEG["bosses"])})
    write("repurposed_structures/tags/item/blacklisted_from_modded_loot_importing.json",
          {"replace": False, "values": sorted(HORIZON_ITEMS | {TROPHY(b["id"]) for b in LEG["bosses"]})})
    rows = report(classes, chance, groups, group_family, members)
    assert_budgets(rows)
    OWNED.write_text(json.dumps({"generator": "scripts/gen_datapack.py", "files": sorted(written)}, indent=1) + "\n")
    print(f"ores disabled: {len(DISABLE_ORES)} | structure sets: {len(STRUCTURE_SETS)} | tables classified: {len(classes)} "
          f"| inject tables: {len(members)} | GLMs: {len(mods)} | apotheosis entries: +{na} affix, +{ng} gem "
          f"| atlas families: {len(atlas)} | exchanges: {nx} | salvage recipes: {ns_} | trials: {nt} | files: {len(written)}")


if __name__ == "__main__":
    main()
