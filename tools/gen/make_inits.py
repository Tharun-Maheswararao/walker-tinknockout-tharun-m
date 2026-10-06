"""Render the Claude-drawn pose sketches (design/draw_design.py) as 512x512 img2img
init images on a flat light-grey background: raw/inits[-ref]/<pose>.png

Also writes meta.json: for each pose, where Bolt's feet are (x, y) and how many
image pixels his standing height (H=112 game px) occupies. img2img keeps the
init's layout, so the sprite processor uses this to put every pose at the same
scale and anchor (feet) in-game.
"""
import json
import sys
from pathlib import Path
from PIL import Image
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "design"))
import draw_design as dd

REF = "--ref" in sys.argv
out = REPO / "raw" / ("inits-ref" if REF else "inits"); out.mkdir(parents=True, exist_ok=True)
SCALE = 3.4
meta = {}
for pose in dd.POSES:
    lay = dd.bolt_layer(pose, scale=SCALE, ref=REF)
    cx, feet = lay.width / 2, lay.height - 4
    l, t, r, b = lay.getbbox(); lay = lay.crop((l, t, r, b))
    w0 = lay.width
    lay.thumbnail((440, 440))
    f = lay.width / w0
    can = Image.new("RGBA", (512, 512), "#D6D6D6")
    px, py = (512 - lay.width) // 2, 512 - 30 - lay.height
    can.alpha_composite(lay, (px, py))
    can.convert("RGB").save(out / f"{pose}.png")
    meta[pose] = {"feet_x": px + (cx - l) * f, "feet_y": py + (feet - t) * f, "height_px": dd.H * SCALE * f}
(out / "meta.json").write_text(json.dumps(meta, indent=1))
print("inits:", sorted(meta), "->", out)
