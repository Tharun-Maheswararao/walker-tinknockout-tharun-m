"""Turn accepted prop/environment generations into game assets (logged edits).
  python tools/edit/process_props.py
Every step: rembg background removal, rotate/flip to the in-game orientation,
crop to content, scale to the size in CHARACTER-SHEET (stored at 3x game size).
"""
from pathlib import Path
from PIL import Image
from rembg import new_session, remove

REPO = Path(__file__).resolve().parents[2]
A = REPO / "godot" / "assets"
sess = new_session("u2net")

def cut(src, crop=None):
    im = Image.open(REPO / src).convert("RGB")
    if crop:
        im = im.crop(crop)
    return remove(im, session=sess)

def fit(im, w=None, h=None):
    im = im.crop(im.getbbox())
    s = (w / im.width) if w else (h / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)

# ENV-BOWL: kept at generated 768x432 (Godot scales it to the 640x360 viewport)
Image.open(REPO / "raw/ENV-BOWL/ENV-BOWL_v2_s4.png").convert("RGB").save(A / "env/bowl.png")
# PROP-KEY: loops were on top; rotate 90 deg CCW so loops point away from the back, shaft into the body
key = fit(cut("raw/PROP-KEY/PROP-KEY_s3.png").rotate(90, expand=True), h=60)
key.save(A / "props/key-bolt.png")
# Rivet's key: same image, copper-ish (darker) - reuse fighter recolour
import sys; sys.path.insert(0, str(REPO / "tools" / "edit"))
from process_sprites import recolour_rivet
recolour_rivet(key).save(A / "props/key-rivet.png")
# WPN-CUTLASS: hilt bottom-left, tip top-right (~40 deg); rotate 40 deg CW -> blade points right; 0.45 x 112 x 3 long
fit(cut("raw/WPN-CUTLASS/WPN-CUTLASS_s3.png").rotate(-40, expand=True, resample=Image.BICUBIC), w=151).save(A / "props/cutlass.png")
# WPN-POPGUN: barrels pointed left; mirror so they point right (facing direction); 0.30 x 112 x 3 long
fit(cut("raw/WPN-POPGUN/WPN-POPGUN_s4.png").transpose(Image.FLIP_LEFT_RIGHT), w=100).save(A / "props/popgun.png")
# PROP-CORK: model drew a bottle every time; crop the cork out of the bottle neck
fit(cut("raw/PROP-CORK/PROP-CORK_s4.png", crop=(200, 25, 320, 120)), w=30).save(A / "props/cork.png")
for p in sorted((A / "props").glob("*.png")):
    print(p.name, Image.open(p).size)
