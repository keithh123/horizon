"""Downscale QA screenshots for review / evidence: python tests/client_qa/thumbs.py <instance> <out_dir> <name> [name...]
Each name is qa_<name>.png in the instance's screenshots/; output <out_dir>/<name>.jpg (1280 px wide).
With --grid, the named images are tiled 2 per row into <out_dir>/<first>_grid.jpg."""
import os, sys
from pathlib import Path
from PIL import Image

args = sys.argv[1:]
grid = "--grid" in args
args = [a for a in args if a != "--grid"]
inst, out, names = args[0], Path(args[1]), args[2:]
src = Path(os.environ["APPDATA"]) / "PrismLauncher/instances" / inst / "minecraft/screenshots"
out.mkdir(parents=True, exist_ok=True)
ims = []
for n in names:
    im = Image.open(src / f"qa_{n}.png").convert("RGB")
    im.thumbnail((1280 if not grid else 800, 720))
    ims.append(im)
    if not grid:
        im.save(out / f"{n}.jpg", quality=82)
if grid:
    w, h = ims[0].size
    cols = 2
    rows = (len(ims) + 1) // 2
    g = Image.new("RGB", (w * cols, h * rows))
    for i, im in enumerate(ims):
        g.paste(im, ((i % cols) * w, (i // cols) * h))
    g.save(out / f"{names[0]}_grid.jpg", quality=80)
print("ok")
