"""Disable the Voxy integration of 'Make it Compatible: Immersive Portals' 1.0.0 (no build matches Voxy 0.2.16-beta).

The add-on's `micimmptl.voxy.mixins.json` targets an older Voxy architecture. Against Voxy 0.2.16-beta (Roxy 0.4.2.1,
Sodium 0.8.13) the client crashes on world join (22 Nov 2026, 11:37 and 11:45 logs):
  * RenderSectionManagerVoxyFeedGateMixin: no @MixinSquared handler `voxy$clearBoundOnSectionRemoved`
  * ChunkBoundRendererOncePerFrameMixin:   @Shadow field `ChunkBoundRenderer.delayQueueIndex` does not exist
    (0.2.16 uses addQueue/remQueue sets and a Viewport<?> / AbstractRenderPipeline API)
No upstream build was found (Modrinth/GitHub lookups returned nothing), and every Voxy-touching class lives in that one
config, so the patch empties its `client` mixin list. Everything else the add-on does (Immersive Portals x Sodium 0.8
fixes, chunk stability) is untouched, and Voxy itself is not modified: it renders the main view as before. Voxy LODs
are NOT drawn inside portal views while this patch is in place.

  python scripts/patch_micimmptl.py <original.jar> <patched.jar>
Deterministic (fixed timestamps) and idempotent.
"""
import json, sys, zipfile

CFG = "micimmptl.voxy.mixins.json"


def patch(src, dst):
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
        for info in zi.infolist():
            data = zi.read(info)
            if info.filename == CFG:
                cfg = json.loads(data)
                cfg["client"] = []
                data = (json.dumps(cfg, indent=4) + "\n").encode()
            ni = zipfile.ZipInfo(info.filename, date_time=(1980, 1, 1, 0, 0, 0))
            ni.compress_type = info.compress_type
            ni.external_attr = info.external_attr
            zo.writestr(ni, data)


if __name__ == "__main__":
    patch(sys.argv[1], sys.argv[2])
    print("patched", sys.argv[2])
