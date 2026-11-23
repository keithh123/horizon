"""Remove Visual Overhaul 5.2.1's first-launch resource-pack mixin (client crash at Options.loadSelectedResourcePacks).

`MixinResourcePackManager.setDefaultEnabledPacks` runs inside PackRepository.setSelected during `new Minecraft()`,
reads the static `VOConfig.firstLaunch` (default true) and calls `VOConfig.write("visualoverhaul")`. VOConfig is only
registered with MidnightLib from the mod constructor, which races the main thread, so when the main thread wins,
`MidnightConfig.write` does `configClass.get(modid).writeChanges(...)` on a null entry -> NullPointerException
(crash 22 Nov 2026 21:48, even with config/visualoverhaul.json seeded: the seed is never read before the hook fires).
Seeding the config therefore only worked when the race went the other way.

The patch drops that one mixin from `visualoverhaul-neoforge.mixins.json`. Cost: Visual Overhaul no longer auto-enables
its built-in packs (visualoverhaul:rounddiscs, :fancyfurnace) on a fresh install; enable them once in Resource Packs
(or ship them in options.txt `resourcePacks`). Everything else in the mod is untouched.

  python scripts/patch_visualoverhaul.py <original.jar> <patched.jar>
Deterministic (fixed timestamps) and idempotent.
"""
import json, sys, zipfile

CFG = "visualoverhaul-neoforge.mixins.json"
DROP = "MixinResourcePackManager"


def patch(src, dst):
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
        for info in zi.infolist():
            data = zi.read(info)
            if info.filename == CFG:
                cfg = json.loads(data)
                cfg["client"] = [m for m in cfg.get("client", []) if m != DROP]
                data = (json.dumps(cfg, indent=2) + "\n").encode()
            ni = zipfile.ZipInfo(info.filename, date_time=(1980, 1, 1, 0, 0, 0))
            ni.compress_type = info.compress_type
            ni.external_attr = info.external_attr
            zo.writestr(ni, data)


if __name__ == "__main__":
    patch(sys.argv[1], sys.argv[2])
    print("patched", sys.argv[2])
