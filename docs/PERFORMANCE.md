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
