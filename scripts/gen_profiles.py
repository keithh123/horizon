"""Expand each profile's shader preset into concrete Iris option values (profiles/shader_options.json).

Complementary defines its presets (POTATO..COMPLEMENTARY) in shaders/shaders.properties as option lists.
0.1.0's profiles only *named* a preset and the switcher never wrote options, so the shader ran its own
defaults. apply-profile.ps1 now writes shaderpacks/<zip>.txt (Iris' per-pack options file) from this file.
"""
import json, os, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = chr(92) * 2 + '?' + chr(92)
if os.name == "nt" and not str(ROOT).startswith(LONG):
    ROOT = Path(LONG + str(ROOT))
CACHE = Path(os.environ.get("PH_CACHE", Path.home() / ".cache" / "project-horizon" / "jars"))
LOCK = json.loads((ROOT / "manifests/lock.json").read_text())


def main():
    out = {}
    for prof in sorted((ROOT / "profiles").glob("*.json")):
        if prof.name in ("shader_options.json", "effects.json"):
            continue
        p = json.loads(prof.read_text())
        sh = p["shader"]
        if sh["pack"] == "none":
            continue
        zipname = next(s["file"] for s in LOCK["shaders"] if s["file"].startswith(sh["pack"]))
        props = zipfile.ZipFile(CACHE / zipname).read("shaders/shaders.properties").decode("utf-8", "ignore")
        m = re.search(rf"(?m)^\s*profile\.{sh['preset']}\s*=\s*(.+)$", props)
        if not m:
            raise SystemExit(f"{prof.name}: preset {sh['preset']} not in {zipname}")
        opts = dict(kv.split("=", 1) for kv in m.group(1).split())
        out[prof.stem] = {"pack_file": zipname, "preset": sh["preset"], "options": opts}
    (ROOT / "profiles/shader_options.json").write_text(json.dumps(out, indent=1) + "\n")
    print({k: (v["pack_file"], v["preset"], len(v["options"])) for k, v in out.items()})


if __name__ == "__main__":
    main()
