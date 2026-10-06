"""Hand edit (logged in SOURCES.md): paint Bolt's two eyes onto the empty helmet
glass of a generated image. Consistency rule 2 requires two eyes in the window.
Usage: python tools/edit/paint_eyes.py IN.png OUT.png CX CY [SPACING] [SIZE] [MOOD]
MOOD: open (default) | half | x
"""
import sys
from PIL import Image, ImageDraw

src, dst, cx, cy = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
sp = float(sys.argv[5]) if len(sys.argv) > 5 else 13
sz = float(sys.argv[6]) if len(sys.argv) > 6 else 7
mood = sys.argv[7] if len(sys.argv) > 7 else "open"
im = Image.open(src).convert("RGBA")
d = ImageDraw.Draw(im)
ink = (30, 26, 22, 255)
for ex in (cx - sp, cx + sp):
    if mood == "x":
        d.line([ex - sz, cy - sz, ex + sz, cy + sz], fill=ink, width=4)
        d.line([ex - sz, cy + sz, ex + sz, cy - sz], fill=ink, width=4)
    elif mood == "half":
        d.chord([ex - sz, cy - sz * 1.3, ex + sz, cy + sz * 1.3], 0, 180, fill=ink)
        d.line([ex - sz - 2, cy, ex + sz + 2, cy], fill=ink, width=3)
    else:
        d.ellipse([ex - sz, cy - sz * 1.3, ex + sz, cy + sz * 1.3], fill=ink)
        d.ellipse([ex - sz * 0.15, cy - sz * 0.95, ex + sz * 0.45, cy - sz * 0.35], fill=(255, 255, 255, 255))
im.save(dst)
print("wrote", dst)
