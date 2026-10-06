"""Turn accepted generated poses into game sprites (every step is a logged edit).

For each pose:
 1. rembg (u2net) removes the flat grey background            -> RGBA
 2. paint two eyes on the helmet glass (consistency rule 2)    -> tools/edit/paint_eyes.py logic
 3. scale so Bolt's standing height = 336 px (3 x 112 game px) and put his feet
    at (240, 435) of a 480x450 canvas, using the init layout recorded in
    raw/inits-ref/meta.json (img2img at strength 0.6 keeps that layout)
 4. Rivet = palette recolour of Bolt (hue rotate brass->copper, red->verdigris)
 5. write anchors.json: key, hand, muzzle positions per pose in game px from the feet

  python tools/edit/process_sprites.py idle=raw/CHAR-IDLE/CHAR-IDLE_v2-st0.6_s43.png walk=...
"""
from __future__ import annotations

import colorsys
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from rembg import new_session, remove

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "design"))
import draw_design as dd  # noqa: E402

OUT = REPO / "godot" / "assets" / "fighters"
META = json.loads((REPO / "raw" / "inits-ref" / "meta.json").read_text())
SCALE = 3.4
CANVAS, FEET, STAND = (480, 450), (240, 435), 336.0


def sketch_points(pose: str) -> dict:
    """Key, hand, muzzle and glass centre in INIT-image pixels, replicating
    draw_design.bolt_layer's geometry (lean + KO rotation, crop, thumbnail)."""
    h = dd.H * SCALE
    lay = dd.bolt_layer(pose, scale=SCALE, ref=True)
    w_img, h_img = lay.size
    cx, feet = w_img / 2, h_img - 4
    lean, fa, _ba, _stride, extra = dd.POSES[pose]
    hip = feet - h * 0.26
    tw, th = h * 0.42, h * 0.32
    sx, sy = cx, hip - th * 0.80
    ex, ey = cx + fa[0] * h, hip + fa[1] * h
    L = math.hypot(ex - sx, ey - sy)
    if L > h * 0.34:
        ex, ey = sx + (ex - sx) * h * 0.34 / L, sy + (ey - sy) * h * 0.34 / L
    hr = h * 0.20
    hx, hy = cx + h * 0.02, hip - th - hr * 0.85
    pts = {"key": (cx - tw / 2 - h * 0.17, hip - th * 0.55), "hand": (ex, ey),
           "muzzle": (ex + h * 0.30, ey - h * 0.015), "glass": (hx + hr * 0.30, hy)}

    def rot(p, c, deg, t=(0, 0)):
        a = math.radians(deg)
        dx, dy = p[0] - c[0], p[1] - c[1]
        return (c[0] + dx * math.cos(a) + dy * math.sin(a) + t[0], c[1] - dx * math.sin(a) + dy * math.cos(a) + t[1])

    pts = {k: rot(v, (cx, hip), -lean) for k, v in pts.items()}
    if extra == "ko":
        pts = {k: rot(v, (cx, feet), 80, (h * 0.45, -h * 0.05)) for k, v in pts.items()}
    l, t, r, b = lay.getbbox()
    f = min(440 / (r - l), 440 / (b - t), 1.0)
    tw_, th_ = int((r - l) * f), int((b - t) * f)
    px, py = (512 - tw_) // 2, 512 - 30 - th_
    return {k: (px + (x - l) * f, py + (y - t) * f) for k, (x, y) in pts.items()}


def paint_eyes(im: Image.Image, c, size: float, mood: str) -> None:
    d = ImageDraw.Draw(im)
    ink = (30, 26, 22, 255)
    sp, sz = size * 0.42, size * 0.22
    for ex in (c[0] - sp, c[0] + sp):
        if mood == "x":
            d.line([ex - sz, c[1] - sz, ex + sz, c[1] + sz], fill=ink, width=max(3, int(sz * 0.5)))
            d.line([ex - sz, c[1] + sz, ex + sz, c[1] - sz], fill=ink, width=max(3, int(sz * 0.5)))
        elif mood == "half":
            d.chord([ex - sz, c[1] - sz * 1.3, ex + sz, c[1] + sz * 1.3], 0, 180, fill=ink)
            d.line([ex - sz - 2, c[1], ex + sz + 2, c[1]], fill=ink, width=3)
        else:
            d.ellipse([ex - sz, c[1] - sz * 1.3, ex + sz, c[1] + sz * 1.3], fill=ink)
            d.ellipse([ex - sz * 0.1, c[1] - sz * 0.95, ex + sz * 0.5, c[1] - sz * 0.35], fill=(255, 255, 255, 255))


def recolour_rivet(im: Image.Image) -> Image.Image:
    """Palette swap: brass/yellow -> copper, red enamel -> verdigris; leaves greys/outline."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32) / 255.0
    rgb, alpha = a[..., :3], a[..., 3:]
    out = rgb.copy()
    flat = rgb.reshape(-1, 3)
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in flat]).reshape(rgb.shape)
    hh, ss, vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    red = ((hh < 0.04) | (hh > 0.93)) & (ss > 0.35)
    yel = (hh >= 0.07) & (hh < 0.18) & (ss > 0.35)
    hh2 = np.where(red, 0.45, np.where(yel, 0.065, hh))      # verdigris / copper hues
    ss2 = np.where(red, ss * 0.55, np.where(yel, ss * 0.85, ss))
    vv2 = np.where(red, np.minimum(1, vv * 0.95), np.where(yel, vv * 0.82, vv))
    m = red | yel
    conv = np.array([colorsys.hsv_to_rgb(*p) for p in np.stack([hh2, ss2, vv2], -1).reshape(-1, 3)]).reshape(rgb.shape)
    out[m] = conv[m]
    return Image.fromarray((np.concatenate([out, alpha], -1) * 255).astype(np.uint8), "RGBA")


def main() -> None:
    picks = dict(a.split("=", 1) for a in sys.argv[1:])
    sess = new_session("u2net")
    (OUT / "bolt").mkdir(parents=True, exist_ok=True)
    (OUT / "rivet").mkdir(parents=True, exist_ok=True)
    anchors = {}
    moods = {"ko": "x", "empty": "half"}
    for pose, src in picks.items():
        raw = Image.open(REPO / src).convert("RGB")
        cut = remove(raw, session=sess)                         # 1. background removal
        pts = sketch_points(pose)
        glass_r = META[pose]["height_px"] * 0.20 * 0.55   # helmet radius 0.20 H, glass 0.55 of it
        paint_eyes(cut, pts["glass"], glass_r, moods.get(pose, "open"))  # 2. eyes
        s = STAND / META[pose]["height_px"]                     # 3. scale + anchor
        big = cut.resize((round(cut.width * s), round(cut.height * s)), Image.LANCZOS)
        fx, fy = META[pose]["feet_x"] * s, META[pose]["feet_y"] * s
        can = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        can.alpha_composite(big, (round(FEET[0] - fx), round(FEET[1] - fy)))
        can.save(OUT / "bolt" / f"{pose}.png")
        recolour_rivet(can).save(OUT / "rivet" / f"{pose}.png")  # 4. Rivet
        anchors[pose] = {k: [round((x - META[pose]["feet_x"]) * s / 3, 1), round((y - META[pose]["feet_y"]) * s / 3, 1)]
                         for k, (x, y) in pts.items() if k != "glass"}
        anchors[pose]["weapon_deg"] = -18.0 if pose == "cutlass" else 0.0
        anchors[pose]["source"] = src
        print("sprite", pose, "<-", src)
    path = OUT / "anchors.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    old.update(anchors)
    path.write_text(json.dumps(old, indent=1))


if __name__ == "__main__":
    main()
