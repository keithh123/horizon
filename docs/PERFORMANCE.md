# Performance

## Profiles

Switch with the game closed: open the instance's `minecraft/horizon-profiles` folder and run
`powershell -ExecutionPolicy Bypass -File apply-profile.ps1 <performance|balanced|cinematic>`.
The script edits `options.txt`, `config/voxy-config.json`, `config/iris.properties` and the Prism
instance's memory/JVM settings. It writes UTF-8 without a BOM.

| | Performance | **Balanced (default)** | Cinematic |
|---|---|---|---|
| Target | GTX 1660 / 4–6 cores / 12–16 GB | RTX 3060 / 6 cores / 16+ GB | RTX 4070+ / 8 cores / 32 GB |
| Heap (min/max) | 3 / 7 GB | 4 / 10 GB | 6 / 14 GB |
| Render / simulation distance | 8 / 6 | 12 / 8 | 16 / 10 |
| Voxy section distance / threads | 8 / 2 | 16 / 3 | 32 / 4 |
| Shader | off | Complementary Reimagined | Complementary Unbound |

JVM: generational ZGC (`-XX:+UseZGC -XX:+ZGenerational`) for low pause times, which smooths frame pacing.

## Measured (Balanced, 2026-11-21)

Machine: Ryzen 5 9600X (6C/12T), 32 GB RAM, RTX 5070 (driver 621.24), 2560×1417, Windows 11.
Measured in the dev instance after joining a fresh world, with Voxy World Gen generating in the background.

| Metric | Value |
|---|---|
| Startup to title screen (ModernFix) | 30–45 s (112 mods) |
| Title screen → in world (existing world) | ~5 s |
| FPS with shaders (F3) | 80 average, p98 48, p99.5 39. GPU at 100%, so GPU-bound at this resolution. |
| Integrated server tick | 14.6 ms average (budget 50 ms), while Voxy World Gen ran at about 15 chunks/s |
| Heap | 7.9 / 10 GB used during world generation, allocation rate ~2.3 GB/s |

Not measured (see VALIDATION_REPORT.md): Performance and Cinematic frame rates, long sessions,
large factories, Spark profiles.

## Tuning notes

- Voxy World Gen is the largest background cost. It queued about 51K chunks for the default radius and works through them at 15 c/s. That's fine for the CPU budget, but expect the full horizon to fill in over the first hour of a new world. Lower its radius in its config on weaker CPUs.
- Voxy uses a sparse 4 GB geometry buffer on NVIDIA (driver-managed). VRAM usage depends on how far the horizon has been generated.
- With shaders on, Create's Flywheel falls back from instanced rendering to `off`. This is expected Iris behaviour, so very large contraption farms cost more FPS with shaders on.
- Lithium and ModernFix both patch `SortedArraySet.removeIf`. The log reports an overwrite conflict, both mods handle it, and no functional impact was seen.

## 0.3.0 expansion (preliminary, not a matched comparison)

In world, Balanced profile, Iris + Complementary Reimagined, Voxy on, 2560x1417, RTX 5070 / Ryzen 5 9600X:
51 fps (p50 49, p99.5 21), integrated server 9.6 ms/tick. Caveats: Voxy World Gen was still generating
(3.1k done / 48k queued), heap capped at 7 GB (another Minecraft instance was using RAM), LAN open. A matched 0.2.0 vs
0.3.0 run (same seed, position, warm cache, 10 GB) has **not** been done. Dedicated server with the expansion: 20 TPS,
1.4-3.7 ms/tick overall during structure location and boss tests.

New profile-controlled costs (profiles/effects.json): Better Clouds (off in Performance), Cozy Critters caps,
Windy, Cave Dust density, Interactive Foliage waving, Effectual trails, Streams Reflowing particle scan
(512 blocks / 1000 per tick by default -> 96/150 Performance, 192/400 Balanced, 320/700 Cinematic).

## 0.3.2 candidate: measured route comparison (2026-11-22, one run per row)

Method: `python scripts/horizon.py qa perf` (see docs/BUILDING.md). Fresh copy of the fixed-seed world, shaders as listed, 4 teleports 30 s apart
(first visit to ungenerated terrain, so this is a cold-worldgen worst case), ~2 min recorded. Client frames are the gap between render-frame events;
"server ticks" are the gap between integrated-server tick events (1 ms clock, so ~50 ms is a healthy tick and only values well above 50 are lag).
Ryzen 5 9600X / RTX 5070, 1 run per row: differences of ~10% are inside run-to-run noise (not measured yet).

| Config | Frame p50 / p95 / p99 (ms) | Frames > 50 ms | Tick-gap p95 / p99 / max (ms) |
|---|---|---|---|
| Shaders off, Voxy WG r128 / 6 tasks (current default) | 7 / 22 / 34 | 59 | 75 / 203 / 9499 |
| Shaders off, r128 / 2 tasks | 7 / 21 / 33 | 36 | 75 / 153 / 6205 |
| Shaders off, r64 / 2 tasks | 7 / 20 / 32 | 38 | 68 / 222 / 6016 |
| Solas, r128 / 6 tasks | 10 / 28 / 37 | 26 | 73 / 243 / 10911 |

No configuration reached the 25% p99 or 50% fewer slow frames target, and none was adopted. The large tick gaps (6-11 s) happen on arrival
at each teleport target (synchronous chunk generation), which a walking player would meet far less abruptly. Not measured: time until the
horizon fills in, warm Voxy data, a river/village or factory scene, Streams/particles/Flywheel profiling, repeat runs for noise.

### Chunky pre-generation experiment (QA only; Chunky is not in the pack)

Same route and settings as the first row above (shaders off, Voxy WG r128 / 6 tasks), but on a world whose route area (x -700..900,
z -500..900, 8,989 chunks, 4 min 24 s at ~34 chunks/s) was pre-generated headlessly with Chunky 1.4.23 first. One run each.

| Config | Frame p50 / p95 / p99 (ms) | Frames > 50 ms (max) | Tick-gap p95 / p99 / max (ms) |
|---|---|---|---|
| Baseline (generate on arrival) | 7 / 22 / 34 | 59 (163 ms) | 75 / 203 / 9499 |
| Chunky pre-generated | 8 / 27 / 43 | 66 (2798 ms) | 75 / 210 / 1744 |

Pre-generation removed the multi-second server stalls (worst tick gap 9.5 s -> 1.7 s) but not the routine tick jitter (p95/p99 unchanged),
and frames got slightly worse (p99 34 -> 43 ms, one 2.8 s hitch), plausibly because Voxy now ingests thousands of existing chunks. A 4.5 minute
per-world pre-generation is not something the pack can ask of a player, and the effect on typical ticks is nil in this test.

## 0.6 headquarters: cost model and what was (not) measured

- The charter does work **only on a player action**: one bounded scan of 21 x 13 x 21 blocks (5 733 block reads,
  loaded chunks only) per panel/commission click, rate-limited to one action per player per 10 ticks. Nothing runs per tick,
  no chunk is force-loaded, no entity or block entity ticks were added (charter, emblems, case, lens and beacon are plain
  blocks; the beacon's light is a static light level).
- The ledger is one compound in `kubejs_persistent_data.nbt`, one JSON string per headquarters (kilobytes).
- Facts are read from at most 54 advancements per member, at login and on charter use.
- Dedicated server (this container, 4 vCPU): boot to "Done" 108-115 s with 188 server jars; no per-tick cost to measure.
- **Not measured in 0.6:** client frame times (p50/p95/p99), memory/GC, a developed-headquarters scene, fresh-chunk vs
  pre-generated travel, Voxy world generation under Create load. No GPU client was available. The 0.5 numbers above remain
  the latest measurements; FramedBlocks/Handcrafted/Create Deco scenes are unmeasured.

