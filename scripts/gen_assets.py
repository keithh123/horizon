"""Generate Horizon's custom item/block assets and their KubeJS registration from one source of truth.

Reads  manifests/legends.json (trophies) + the ITEMS table below (relics, regional tokens).
Writes (owned, listed in kubejs/.generated-assets.json):
  kubejs/assets/horizon/textures/item/*.png       16x16 pixel art, drawn procedurally (no third-party art)
  kubejs/assets/horizon/textures/block/*.png      trophy pedestal + per-boss emblem
  kubejs/assets/horizon/models/block/trophy_base.json
  kubejs/assets/horizon/lang/en_us.json
  kubejs/startup_scripts/horizon_items.js         item/block registry (generated - edit this script, not the JS)
  kubejs/client_scripts/horizon_tooltips.js
Pure Python (zlib PNG writer); deterministic output.
"""
import json, math, os, struct, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
KJ = ROOT / "kubejs"
OWNED = KJ / ".generated-assets.json"
LEG = json.loads((ROOT / "manifests/legends.json").read_text(encoding="utf-8"))
written = []

# id, name, rarity, stack, glow, tooltip lines (gray), shape, palette [dark, mid, light, accent]
ITEMS = [
    ("wayfarer_shard", "Wayfarer Shard", "uncommon", 64, False,
     ["Found in roadside ruins, camps, villages and dungeons.", "Warp stones, gem dust, backpack upgrades, salvage."],
     "shard", ["1f5c45", "35a37a", "9cf5cf", "ffffff"]),
    ("ancient_core", "Ancient Core", "rare", 16, False,
     ["Found in temple and landmark treasure rooms; first kill of a mini-boss.", "ME controller, socketing sigils, epic ink, Trials."],
     "core", ["0d3b47", "1f8a96", "8ff0f0", "f2c15a"]),
    ("starforged_heart", "Starforged Heart", "epic", 16, True,
     ["Landmark vaults (rare) and the first kill of a great boss.", "Fusion reactors, 256M storage, enhancement, legendary ink."],
     "heart", ["4a1060", "b33ee0", "ffb8ff", "ffd36a"]),
    ("tidebound_doubloon", "Tidebound Doubloon", "uncommon", 64, False,
     ["Ocean expeditions: wrecks, sunken ruins, pirate ships, monuments.", "Trade 6 for a Lunar or Slipstream gem (Expedition Exchange)."],
     "coin", ["6b4300", "d19a22", "ffe58a", "2f8fd6"]),
    ("cinder_idol", "Cinder Idol", "uncommon", 64, False,
     ["Nether expeditions: Incendium castles, fortresses, bastions.", "Trade 6 for an Inferno, Blood Lord or Molten Breach gem."],
     "idol", ["3a0e05", "9e2f0e", "ff7a2a", "ffe36a"]),
    ("starlit_voidglass", "Starlit Voidglass", "rare", 64, False,
     ["End expeditions: cities, castles, wrecks over the void.", "Trade 6 for an Endersurge or Mageslayer gem."],
     "voidglass", ["120822", "3d1d6b", "9a72e8", "ffffff"]),
    ("skyward_plume", "Skyward Plume", "uncommon", 64, False,
     ["The Aether: ruined portals, dungeons and their guardians.", "Trade 6 for a Solar or Lightning gem."],
     "plume", ["6a6a80", "c8d2f0", "ffffff", "f2c94c"]),
    ("echoing_fossil", "Echoing Fossil", "uncommon", 64, False,
     ["The Deep: Ancient Cities, the Otherside, the Undergarden.", "Trade 6 for a Breach or Guardian gem."],
     "fossil", ["0c2a2e", "2f6b6e", "9fd8cf", "e8fff9"]),
    ("honeyed_seal", "Honeyed Seal", "uncommon", 64, False,
     ["The Bumblezone: solved puzzles, mazes and sanctums.", "Trade 6 for a Verdant Ruin or Splendor gem."],
     "hexseal", ["6b3a00", "d48a14", "ffd36a", "2a1a06"]),
]


# ------------------------------------------------------------------ PNG
def png(path, px):
    h, w = len(px), len(px[0])
    raw = b"".join(b"\x00" + b"".join(bytes(p) for p in row) for row in px)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) + \
        chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    written.append(path.relative_to(KJ).as_posix())


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def canvas():
    return [[(0, 0, 0, 0) for _ in range(16)] for _ in range(16)]


def paint(mask, pal, light=(-0.7, -0.7), outline=True, hi=None):
    """mask: 16x16 bools. Shade by distance along the light direction, add a dark outline and a highlight."""
    dark, mid, lite, acc = (rgb(c) for c in pal)
    img = canvas()
    cells = [(x, y) for y in range(16) for x in range(16) if mask[y][x]]
    if not cells:
        return img
    cx = sum(x for x, _ in cells) / len(cells)
    cy = sum(y for _, y in cells) / len(cells)
    for x, y in cells:
        d = ((x - cx) * light[0] + (y - cy) * light[1]) / 7.0
        c = mix(mid, lite, d) if d > 0 else mix(mid, dark, -d * 0.9)
        img[y][x] = (*c, 255)
    if outline:
        for y in range(16):
            for x in range(16):
                if mask[y][x]:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if not (0 <= nx < 16 and 0 <= ny < 16) or not mask[ny][nx]:
                            img[y][x] = (*mix(dark, (0, 0, 0), 0.35), 255)
                            break
    for (x, y) in (hi or []):
        if 0 <= x < 16 and 0 <= y < 16 and mask[y][x]:
            img[y][x] = (*mix(lite, (255, 255, 255), 0.6), 255)
    return img


def m(fn):
    return [[bool(fn(x + 0.5, y + 0.5)) for x in range(16)] for y in range(16)]


def put(img, pts, col):
    for x, y in pts:
        if 0 <= x < 16 and 0 <= y < 16:
            img[y][x] = (*rgb(col), 255)


def shape(kind, pal):
    if kind == "shard":   # tilted crystal
        def f(x, y):
            u, v = (x - 8) * 0.8 + (y - 8) * 0.6, -(x - 8) * 0.6 + (y - 8) * 0.8
            big = abs(u) / 8.2 + abs(v) / 3.6 <= 1.0
            u2, v2 = (x - 11) * 0.95 + (y - 5) * 0.3, -(x - 11) * 0.3 + (y - 5) * 0.95
            small = abs(u2) / 2.2 + abs(v2) / 4.2 <= 1.0
            return big or small
        img = paint(m(f), pal, hi=[(5, 6), (6, 7), (4, 5), (11, 3)])
        return img
    if kind == "core":
        img = paint(m(lambda x, y: (x - 8) ** 2 + (y - 8) ** 2 <= 30), pal, hi=[(6, 5), (5, 6), (6, 6)])
        for x in range(2, 14):   # golden equatorial band
            y = round(8 + (x - 8) * 0.25)
            if img[y][x][3]:
                img[y][x] = (*rgb(pal[3]), 255)
        put(img, [(8, 8), (9, 8), (8, 9), (9, 9)], "ffffff")
        return img
    if kind == "heart":   # four-point star with a hot core
        def f(x, y):
            dx, dy = abs(x - 8), abs(y - 8)
            return ((dx ** 0.5 + dy ** 0.5) <= 3.45 and max(dx, dy) < 7.6) or (dx ** 2 + dy ** 2) <= 12
        img = paint(m(f), pal, hi=[(7, 3), (6, 6), (5, 7)])
        put(img, [(7, 6), (8, 6), (6, 7), (7, 7), (8, 7), (9, 7), (6, 8), (7, 8), (8, 8), (9, 8), (7, 9), (8, 9)], pal[3])
        put(img, [(7, 7), (8, 8)], "ffffff")
        return img
    if kind == "coin":
        img = paint(m(lambda x, y: (x - 8) ** 2 + (y - 8) ** 2 <= 36), pal, hi=[(5, 5), (6, 4)])
        rim = [(x, y) for y in range(16) for x in range(16) if 22 <= (x + .5 - 8) ** 2 + (y + .5 - 8) ** 2 <= 30]
        put(img, rim, pal[0])
        put(img, [(5, 9), (6, 8), (7, 9), (8, 8), (9, 9), (10, 8)], pal[3])   # wave
        put(img, [(5, 10), (7, 10), (9, 10)], pal[3])
        return img
    if kind == "idol":
        def f(x, y):
            return ((x - 8) ** 2 / 9 + (y - 5) ** 2 / 9 <= 1) or (4.5 <= x <= 11.5 and 7 <= y <= 14) or (3 <= x <= 13 and 13 <= y <= 15)
        img = paint(m(f), pal, hi=[(6, 3)])
        put(img, [(6, 5), (10, 5)], pal[3])
        put(img, [(7, 10), (8, 10), (9, 10)], pal[2])
        return img
    if kind == "voidglass":
        def f(x, y):
            return abs(x - 8) / 4.6 + abs(y - 8) / 7.3 <= 1.0
        img = paint(m(f), pal, hi=[(7, 4), (7, 5)])
        put(img, [(11, 3), (12, 2), (13, 3), (12, 4), (12, 3)], "ffffff")   # sparkle
        put(img, [(3, 12), (4, 12)], pal[2])
        return img
    if kind == "plume":
        def f(x, y):
            t = (x + y - 4) / 24
            cx = 3 + t * 10
            return 0 <= t <= 1 and abs((x - y) / 1.414) <= 2.6 * math.sin(math.pi * min(1, t * 1.1)) + 0.4
        img = paint(m(f), pal, hi=[(6, 7), (8, 9)])
        put(img, [(i, i) for i in range(3, 14)], pal[0])
        put(img, [(13, 13), (14, 14)], pal[3])
        return img
    if kind == "fossil":
        img = paint(m(lambda x, y: (x - 8) ** 2 + (y - 8) ** 2 <= 34), pal, hi=[(5, 5)])
        for i in range(90):   # spiral groove
            a = i * 0.22
            r = 0.3 + a * 0.62
            x, y = round(8 + r * math.cos(a)), round(8 + r * math.sin(a))
            if 0 <= x < 16 and 0 <= y < 16 and img[y][x][3]:
                img[y][x] = (*rgb(pal[0]), 255)
        return img
    if kind == "hexseal":
        def f(x, y):
            dx, dy = abs(x - 8), abs(y - 8)
            return dy <= 6.5 and dx <= 7 - dy * 0.5 + 3.2 * 0 and dx * 0.866 + dy * 0.5 <= 6.2
        img = paint(m(f), pal, hi=[(6, 4), (5, 5)])
        for y in (6, 9, 12):
            for x in range(16):
                if img[y][x][3] and abs(x - 8) < 5:
                    img[y][x] = (*rgb(pal[3]), 255)
        return img
    raise SystemExit(kind)


GLYPHS = {  # 8x8 emblems drawn on the trophy plaque
    "skull": ["..####..", ".######.", "##.##.##", "########", ".######.", "..#..#..", "..####..", "........"],
    "flame": ["...#....", "...##...", "..###.#.", ".#####..", ".######.", "########", ".######.", "..####.."],
    "eye":   ["........", "..####..", ".#....#.", "#..##..#", "#..##..#", ".#....#.", "..####..", "........"],
    "wave":  ["........", "..##....", ".#..#...", "#....#..", "......#.", "..##...#", ".#..#...", "#....###"],
    "sun":   ["#..#..#.", ".#.#.#..", "..###...", "#######.", "..###...", ".#.#.#..", "#..#..#.", "........"],
    "gear":  ["..#..#..", ".######.", "##....##", ".#.##.#.", ".#.##.#.", "##....##", ".######.", "..#..#.."],
    "anvil": ["........", "########", ".######.", "...##...", "...##...", "..####..", ".######.", "........"],
    "wing":  ["#.......", "##......", "###.....", "####....", ".#####..", "..######", "...#####", ".....###"],
    "flake": ["...#....", ".#.#.#..", "..###...", "#######.", "..###...", ".#.#.#..", "...#....", "........"],
    "crown": ["........", "#..#..#.", "##.#.##.", "#######.", "#######.", "#.#.#.#.", "#######.", "........"],
    "star":  ["...#....", "...#....", "..###...", "#######.", ".#####..", "..#.#...", ".#...#..", "........"],
}


def trophy_emblem(b):
    dark, mid, lite, acc = (rgb(c) for c in b["palette"])
    gold, gold_d = rgb("e8c15a"), rgb("7a5a14")
    img = canvas()
    for y in range(16):
        for x in range(16):
            edge = x in (0, 15) or y in (0, 15)
            if edge:
                img[y][x] = (*gold_d, 255)
            elif x in (1, 14) or y in (1, 14):
                img[y][x] = (*gold, 255)
            else:
                t = ((x - 8) ** 2 + (y - 8) ** 2) / 72
                img[y][x] = (*mix(mid, dark, t), 255)
    g = GLYPHS[b["glyph"]]
    for gy, row in enumerate(g):
        for gx, ch in enumerate(row):
            if ch == "#":
                x, y = 4 + gx, 4 + gy
                img[y][x] = (*mix(lite, acc, gy / 10), 255)
    return img


def pedestal():
    stone, stone_d, stone_l = rgb("5b5763"), rgb("34313a"), rgb("8a8592")
    gold = rgb("d9b24a")
    img = canvas()
    for y in range(16):
        for x in range(16):
            n = ((x * 7 + y * 13) % 5) / 10
            c = mix(stone, stone_l if (x + y) % 3 == 0 else stone_d, n)
            if y in (0, 15):
                c = gold
            img[y][x] = (*c, 255)
    return img


def main():
    if OWNED.exists():
        for rel in json.loads(OWNED.read_text())["files"]:
            (KJ / rel).unlink(missing_ok=True)
    lang, tips, js = {}, {}, []
    for iid, name, rarity, stack, glow, tip, kind, pal in ITEMS:
        png(KJ / f"assets/horizon/textures/item/{iid}.png", shape(kind, pal))
        lang[f"item.horizon.{iid}"] = name
        tips[iid] = tip
        js.append(f"  event.create('horizon:{iid}').texture('horizon:item/{iid}').rarity('{rarity}').maxStackSize({stack})"
                  + (".glow(true)" if glow else "") + "\n")
    png(KJ / "assets/horizon/textures/block/trophy_pedestal.png", pedestal())
    model = {"parent": "minecraft:block/block", "textures": {"particle": "#base"},
             "display": {"gui": {"rotation": [30, 225, 0], "translation": [0, 1, 0], "scale": [0.8, 0.8, 0.8]}},
             "elements": [
                 {"from": [2, 0, 2], "to": [14, 3, 14], "faces": {f: {"texture": "#base"} for f in ("down", "up", "north", "south", "east", "west")}},
                 {"from": [4, 3, 4], "to": [12, 5, 12], "faces": {f: {"texture": "#base"} for f in ("up", "north", "south", "east", "west")}},
                 {"from": [3, 5, 7], "to": [13, 15, 9], "faces": {"north": {"texture": "#emblem"}, "south": {"texture": "#emblem"},
                                                                 "east": {"texture": "#base"}, "west": {"texture": "#base"},
                                                                 "up": {"texture": "#base"}}}]}
    p = KJ / "assets/horizon/models/block/trophy_base.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(model, indent=1), encoding="utf-8")
    written.append(p.relative_to(KJ).as_posix())
    blocks = []
    for b in LEG["bosses"]:
        bid = "trophy_" + b["id"].split(":")[1]
        png(KJ / f"assets/horizon/textures/block/{bid}.png", trophy_emblem(b))
        lang[f"block.horizon.{bid}"] = f"Trophy: {b['name']}"
        tips[bid] = [("Awarded for the first defeat of " + b["name"] + "."), "A display piece for the Hall of Legends."]
        rarity = "epic" if b["tier"] == "major" else "rare"
        blocks.append(f"  event.create('horizon:{bid}').displayName(Text.translate('block.horizon.{bid}'))"
                      f".parentModel('horizon:block/trophy_base').textures({{base: 'horizon:block/trophy_pedestal', emblem: 'horizon:block/{bid}'}})"
                      f".box(2, 0, 2, 14, 15, 14).notSolid().defaultCutout().hardness(1.5).resistance(6).stoneSoundType()"
                      f".lightLevel(0.4).item(i => i.rarity('{rarity}').maxStackSize(1))\n")
    for k, v in tips.items():
        for n, line in enumerate(v):
            lang[f"tooltip.horizon.{k}.{n}"] = line
    lang["itemGroup.horizon"] = "Project Horizon"
    lp = KJ / "assets/horizon/lang/en_us.json"
    lp.write_text(json.dumps(lang, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    written.append(lp.relative_to(KJ).as_posix())
    hdr = "// GENERATED by scripts/gen_assets.py - edit the generator, not this file.\n"
    sp = KJ / "startup_scripts/horizon_items.js"
    sp.write_text(hdr + "// Exploration relics, regional expedition tokens and boss trophies. None of these can be crafted from\n"
                  "// renewable inputs: relics/tokens come from structure loot, trophies from first-kill advancements.\n"
                  "StartupEvents.registry('item', event => {\n" + "".join(js) + "})\n\n"
                  "StartupEvents.registry('block', event => {\n" + "".join(blocks) + "})\n", encoding="utf-8")
    written.append(sp.relative_to(KJ).as_posix())
    cp = KJ / "client_scripts/horizon_tooltips.js"
    cp.write_text(hdr + "// Where each Horizon item comes from and what it is for, on the item itself.\n"
                  "ItemEvents.modifyTooltips(event => {\n"
                  + "".join(f"  event.add('horizon:{k}', [" + ", ".join(f"Text.translate('tooltip.horizon.{k}.{n}').gray()" for n in range(len(v))) + "])\n"
                            for k, v in tips.items()) + "})\n", encoding="utf-8")
    written.append(cp.relative_to(KJ).as_posix())
    data = {"partyRadius": LEG["party_radius"],
            "legends": {b["id"]: {"path": b["id"].split(":")[1], "tier": b["tier"], "name": b["name"]} for b in LEG["bosses"]},
            "tiers": {"horizon:wayfarer_shard": 1, "horizon:ancient_core": 2, "horizon:starforged_heart": 3,
                      **{f"horizon:{it[0]}": 1 for it in ITEMS[3:]}},
            "names": {f"horizon:{it[0]}": it[1] for it in ITEMS}}
    dp = KJ / "startup_scripts/horizon_data.js"
    dp.write_text(hdr + "// Data shared with server/client scripts (global may only be assigned in startup scripts).\n"
                  "global.HORIZON = " + json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    written.append(dp.relative_to(KJ).as_posix())
    OWNED.write_text(json.dumps({"generator": "scripts/gen_assets.py", "files": sorted(written)}, indent=1) + "\n")
    print(f"{len(ITEMS)} items, {len(LEG['bosses'])} trophies, {len(written)} files")


if __name__ == "__main__":
    main()
