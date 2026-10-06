"""Contact sheet of generated images: python tools/gen/contact.py OUT.png img1 img2 ... [--thumb 256]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

args = sys.argv[1:]
thumb = 256
if "--thumb" in args:
    i = args.index("--thumb"); thumb = int(args[i + 1]); del args[i:i + 2]
out, files = args[0], args[1:]
cols = min(4, len(files)); rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (thumb + 8) + 8, rows * (thumb + 30) + 8), "white")
d = ImageDraw.Draw(sheet)
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
for k, p in enumerate(files):
    im = Image.open(p).convert("RGB"); im.thumbnail((thumb, thumb))
    x, y = 8 + (k % cols) * (thumb + 8), 8 + (k // cols) * (thumb + 30)
    sheet.paste(im, (x, y)); d.text((x, y + thumb + 4), Path(p).stem, fill="black", font=f)
Path(out).parent.mkdir(parents=True, exist_ok=True); sheet.save(out); print("wrote", out)
