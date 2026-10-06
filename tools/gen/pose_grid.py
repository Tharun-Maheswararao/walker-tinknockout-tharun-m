"""One row per pose: init sketch + every v2 candidate, labelled. python tools/gen/pose_grid.py OUT.png pose..."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
out, poses = sys.argv[1], sys.argv[2:]
T = 130
rows = []
for p in poses:
    ID = f"CHAR-{p.upper()}"
    files = [Path(f"raw/inits-ref/{p}.png")] + sorted(Path(f"raw/{ID}").glob(f"{ID}_v2*.png"))
    rows.append((p, files))
W = max(len(f) for _, f in rows) * (T + 4) + 70
sheet = Image.new("RGB", (W, len(rows) * (T + 18)), "white")
d = ImageDraw.Draw(sheet)
for r, (p, files) in enumerate(rows):
    y = r * (T + 18)
    d.text((4, y + T // 2), p, fill="black", font=F)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB"); im.thumbnail((T, T))
        sheet.paste(im, (70 + i * (T + 4), y))
        lab = "init" if i == 0 else f.stem.split("_v2-")[1].replace("st", "").replace("_s", " s")
        d.text((70 + i * (T + 4), y + T + 2), lab, fill="black", font=F)
sheet.save(out); print("wrote", out)
