"""Draws the pre-generation design sketches for Tin Knockout (storyboard
thumbnails, silhouette test, collision overlay, palette, pose targets).

These are Claude-written, code-drawn diagrams. They are the SPECIFICATION the
generated art must meet; they are not generated assets and do not count toward
the generative-model requirement.

Run:  python design/draw_design.py   (needs Pillow)
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SB = ROOT / "storyboard"
CH = ROOT / "character"
SB.mkdir(exist_ok=True)
CH.mkdir(exist_ok=True)

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size: int, bold: bool = False):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT, size)
    except OSError:
        return ImageFont.load_default(size)


# ---------------------------------------------------------------- palette
PAL = {
    "brass": "#C9962B",     # helmet
    "enamel": "#C8382E",    # suit
    "glass": "#F2E6C4",     # porthole / eyes background
    "steel": "#5B6770",     # boots, gloves
    "key": "#E8C35A",       # winding key highlight
    "outline": "#1E1A16",   # outline / eyes
}
RIVET = {
    "brass": "#B5652F",     # copper helmet
    "enamel": "#3F8F7A",    # verdigris suit
    "glass": "#F2E6C4",
    "steel": "#4A4F55",
    "key": "#D9A066",
    "outline": "#1E1A16",
}
ENV = {
    "deep": "#1F3A5A",      # moonlit water-blue of the empty bowl interior
    "glass_hi": "#9FC6D9",  # glass reflection
    "gravel": "#6F7F8C",
    "counter": "#4B3526",
}

# On-screen size: 640x360 viewport, Bolt is 112 px tall (x2 at 1280x720 window).
H = 112


# ---------------------------------------------------------------- Bolt figure
POSES = {
    #            lean  front arm (dx,dy)  back arm (dx,dy)  stride  extra
    "idle":     (0,    (0.30, -0.62),     (0.20, -0.58),     0.00, None),
    "walk":     (4,    (0.26, -0.60),     (0.10, -0.55),     0.22, None),
    "jab":      (8,    (0.62, -0.60),     (0.12, -0.60),     0.14, None),
    "cutlass":  (10,   (0.56, -0.48),     (-0.04, -0.52),    0.20, "cutlass"),
    "pop":      (-4,   (0.60, -0.64),     (0.36, -0.62),     0.10, "popgun"),
    "block":    (-2,   (0.22, -0.74),     (0.18, -0.70),     0.06, None),
    "rewind":   (14,   (0.20, -0.40),     (-0.38, -0.52),    0.10, "crank"),
    "hurt":     (-16,  (-0.02, -0.80),    (-0.20, -0.74),    0.10, "spark"),
    "empty":    (22,   (0.14, -0.20),     (0.02, -0.18),     0.00, "droop"),
    "ko":       (0,    (0.10, -0.40),     (-0.10, -0.40),    0.00, "ko"),
    "win":      (-6,   (0.12, -1.08),     (0.24, -0.60),     0.06, None),
}


def bolt_layer(pose: str, pal=PAL, scale: float = 1.0, silhouette: bool = False, ref: bool = False):
    """Return an RGBA image of Bolt facing RIGHT with feet at bottom-centre.

    ref=True (added 2026-10-06, after CHAR-REF was accepted): draw the img2img
    init version, which copies the accepted reference's extra features (two
    antennae, yellow gloves, grey glass) and omits weapon props, which are
    separate sprites. The default output (the v1 spec sketches) is unchanged."""
    if ref:
        pal = dict(pal, steel_glove="#E8B830", glass="#B9C0C6")
    h = H * scale
    w_img, h_img = int(h * 2.2), int(h * 1.6)
    img = Image.new("RGBA", (w_img, h_img), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lean, fa, ba, stride, extra = POSES[pose]
    cx, feet = w_img / 2, h_img - 4
    ow = max(2, int(h * 0.025))

    def c(key):
        return "#000000" if silhouette else pal[key]

    ol = "#000000" if silhouette else pal["outline"]
    # boots + legs
    for side in (-1, 1):
        bx = cx + side * h * (0.10 + stride * 0.5 * (1 if side > 0 else 1)) * (1 if side > 0 else 1)
        bx = cx + side * h * 0.09 + (stride * h * 0.5 if side > 0 else -stride * h * 0.3)
        d.rectangle([bx - h * 0.05, feet - h * 0.28, bx + h * 0.05, feet - h * 0.08], fill=c("enamel"), outline=ol, width=ow)
        d.rounded_rectangle([bx - h * 0.09, feet - h * 0.10, bx + h * 0.11, feet], radius=h * 0.03, fill=c("steel"), outline=ol, width=ow)
    # torso + head are drawn on a sub-layer so they can lean
    up = Image.new("RGBA", img.size, (0, 0, 0, 0))
    u = ImageDraw.Draw(up)
    hip = feet - h * 0.26
    tw, th = h * 0.42, h * 0.32
    # winding key (behind the back = left side when facing right)
    kx, ky = cx - tw / 2, hip - th * 0.55
    u.line([kx, ky, kx - h * 0.12, ky], fill=ol, width=int(h * 0.05))
    u.ellipse([kx - h * 0.22, ky - h * 0.08, kx - h * 0.12, ky + h * 0.08], fill=c("key"), outline=ol, width=ow)
    u.ellipse([kx - h * 0.21, ky - h * 0.04, kx - h * 0.15, ky + h * 0.04], fill=(0, 0, 0, 0) if not silhouette else "#000000", outline=ol, width=ow)
    # air hose from helmet back to key
    u.arc([kx - h * 0.08, hip - th - h * 0.20, cx, hip - th * 0.3], 160, 260, fill=ol if silhouette else "#3a3a3a", width=int(h * 0.03))
    # back arm
    sx, sy = cx, hip - th * 0.80

    def arm(dx, dy, front):
        ex, ey = cx + dx * h, hip + dy * h
        L = math.hypot(ex - sx, ey - sy)
        if L > h * 0.34:  # arms are short tin tubes: clamp reach
            ex, ey = sx + (ex - sx) * h * 0.34 / L, sy + (ey - sy) * h * 0.34 / L
        u.line([sx, sy, ex, ey], fill=ol, width=int(h * 0.09))
        u.line([sx, sy, ex, ey], fill=c("enamel"), width=int(h * 0.06))
        r = h * 0.065
        u.ellipse([ex - r, ey - r, ex + r, ey + r], fill=pal.get("steel_glove", c("steel")) if not silhouette else ol, outline=ol, width=ow)
        return ex, ey

    arm(*ba, front=False)
    # torso
    u.rounded_rectangle([cx - tw / 2, hip - th, cx + tw / 2, hip], radius=h * 0.08, fill=c("enamel"), outline=ol, width=ow)
    for i in range(3):  # rivets on the belt seam
        rx = cx - tw * 0.3 + i * tw * 0.3
        u.ellipse([rx - 2, hip - th * 0.25 - 2, rx + 2, hip - th * 0.25 + 2], fill=ol)
    # helmet
    hr = h * 0.20
    hx, hy = cx + h * 0.02, hip - th - hr * 0.85
    if ref:  # the accepted reference's two antennae: short brass stalk + taller red-ball stalk
        u.line([hx - hr * 0.35, hy - hr * 0.8, hx - hr * 0.6, hy - hr * 1.35], fill=ol, width=int(h * 0.04))
        u.ellipse([hx - hr * 0.75, hy - hr * 1.5, hx - hr * 0.45, hy - hr * 1.2], fill="#E8B830", outline=ol, width=ow)
        u.line([hx + hr * 0.1, hy - hr * 0.95, hx + hr * 0.1, hy - hr * 1.6], fill=ol, width=int(h * 0.04))
        u.ellipse([hx - hr * 0.1, hy - hr * 1.85, hx + hr * 0.3, hy - hr * 1.45], fill="#D8262B", outline=ol, width=ow)
    u.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=c("brass"), outline=ol, width=ow)
    pr = hr * 0.55
    px = hx + hr * 0.30
    u.ellipse([px - pr, hy - pr, px + pr, hy + pr], fill=c("glass"), outline=ol, width=ow * 2)
    if not silhouette:
        if extra == "ko":
            for ex in (px - pr * 0.35, px + pr * 0.35):
                u.line([ex - 3, hy - 3, ex + 3, hy + 3], fill=ol, width=2)
                u.line([ex - 3, hy + 3, ex + 3, hy - 3], fill=ol, width=2)
        elif extra == "droop":
            for ex in (px - pr * 0.35, px + pr * 0.35):
                u.line([ex - 3, hy + 1, ex + 3, hy + 1], fill=ol, width=2)
        else:
            for ex in (px - pr * 0.35, px + pr * 0.35):
                u.ellipse([ex - 2.5, hy - 3, ex + 2.5, hy + 3], fill=ol)
    fx, fy = arm(*fa, front=True)
    # weapon / extras
    if extra == "cutlass" and not ref:
        u.line([fx, fy, fx + h * 0.45, fy - h * 0.18], fill=ol, width=int(h * 0.05))
        u.line([fx, fy, fx + h * 0.45, fy - h * 0.18], fill="#000" if silhouette else "#C9CED4", width=int(h * 0.03))
    if extra == "popgun" and not ref:
        u.rectangle([fx - h * 0.02, fy - h * 0.05, fx + h * 0.28, fy + h * 0.02], fill=c("steel"), outline=ol, width=ow)
        if not silhouette:
            u.ellipse([fx + h * 0.30, fy - h * 0.05, fx + h * 0.38, fy + h * 0.02], fill="#B98A52", outline=ol)
    up = up.rotate(-lean, center=(cx, hip), resample=Image.BICUBIC)
    img.alpha_composite(up)
    if extra == "ko":
        img = img.rotate(80, center=(cx, feet), resample=Image.BICUBIC, translate=(h * 0.45, -h * 0.05))
    return img


def place(canvas: Image.Image, layer: Image.Image, x: float, feet_y: float, facing: int = 1):
    if facing < 0:
        layer = layer.transpose(Image.FLIP_LEFT_RIGHT)
    canvas.alpha_composite(layer, (int(x - layer.width / 2), int(feet_y - layer.height + 4)))


# ---------------------------------------------------------------- environment sketch
def bowl_bg(w=640, h=360, angle="eye"):
    img = Image.new("RGBA", (w, h), ENV["counter"])
    d = ImageDraw.Draw(img)
    if angle == "high":
        d.rectangle([0, 0, w, h], fill="#2a2230")
        d.rectangle([60, 40, 300, 150], fill="#3d5f86")  # shop window
        d.line([180, 40, 180, 150], fill="#2a2230", width=4)
        d.rectangle([0, 200, w, h], fill=ENV["counter"])
        d.ellipse([230, 150, 470, 330], fill=ENV["deep"], outline=ENV["glass_hi"], width=4)
        d.ellipse([270, 230, 430, 315], fill=ENV["gravel"])
        return img
    d.rectangle([0, 0, w, h], fill=ENV["deep"])
    d.arc([-200, -260, w + 200, h + 140], 200, 340, fill=ENV["glass_hi"], width=6)  # bowl curve
    d.rectangle([0, 292, w, h], fill=ENV["gravel"])
    for i in range(0, w, 14):
        d.ellipse([i, 292 + (i * 7) % 9, i + 9, 300 + (i * 7) % 9], fill="#808f9b")
    d.polygon([(470, 292), (470, 210), (490, 210), (490, 225), (505, 225), (505, 210), (525, 210), (525, 292)], fill="#c7a7b4", outline="#1e1a16")
    for sx in (60, 90, 580):
        d.line([sx, 292, sx - 8, 230, sx + 4, 190], fill="#3f7a4e", width=6, joint="curve")
    return img


def frame_label(img, n, title, shot):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 22], fill=(0, 0, 0, 170))
    d.text((8, 3), f"{n:02d}  {title}", fill="white", font=font(14, True))
    d.text((img.width - 8, 4), shot, fill="#ffd27a", font=font(12), anchor="ra")
    d.rectangle([0, 0, img.width - 1, img.height - 1], outline="#111", width=3)


def arrow(d, a, b, col="#ffd27a", w=4):
    d.line([a, b], fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (2.6, -2.6):
        d.line([b, (b[0] + 14 * math.cos(ang + s), b[1] + 14 * math.sin(ang + s))], fill=col, width=w)


def hud(d, bolt_wind=0.8, bolt_hp=1.0, rivet_hp=1.0):
    d.rectangle([16, 32, 216, 44], fill="#222", outline="#111")
    d.rectangle([16, 32, 16 + 200 * bolt_hp, 44], fill="#e0c060")
    d.rectangle([424, 32, 624, 44], fill="#222", outline="#111")
    d.rectangle([624 - 200 * rivet_hp, 32, 624, 44], fill="#d07a3a")
    d.ellipse([16, 50, 50, 84], fill="#3a2e1c", outline=PAL["brass"], width=3)
    a = math.radians(-90 + 360 * bolt_wind)
    d.line([33, 67, 33 + 13 * math.cos(a), 67 + 13 * math.sin(a)], fill="#ffd27a", width=3)


# ---------------------------------------------------------------- storyboard panels
def storyboard():
    F = 300  # gameplay floor y
    # 01 title: wide, high angle, design view
    img = bowl_bg(angle="high")
    d = ImageDraw.Draw(img)
    small = bolt_layer("idle", scale=0.35)
    place(img, small, 320, 300)
    place(img, bolt_layer("idle", RIVET, scale=0.35), 380, 300, -1)
    d.text((320, 70), "TIN KNOCKOUT", fill="#ffd27a", font=font(40, True), anchor="mm")
    d.text((320, 112), "press ENTER", fill="white", font=font(16), anchor="mm")
    frame_label(img, 1, "Closing time", "WIDE · HIGH ANGLE · DESIGN (title)")
    img.convert("RGB").save(SB / "01-title.png")

    # 02 round start: wide/medium, eye level, gameplay
    img = bowl_bg(); d = ImageDraw.Draw(img)
    place(img, bolt_layer("idle"), 200, F)
    place(img, bolt_layer("idle", RIVET), 440, F, -1)
    hud(d)
    d.text((320, 150), "ROUND 1", fill="#ffd27a", font=font(34, True), anchor="mm")
    frame_label(img, 2, "Ding! Round start", "MEDIUM-WIDE · EYE LEVEL · GAMEPLAY")
    img.convert("RGB").save(SB / "02-round-start.png")

    # 03 core action: medium, eye level, gameplay
    img = bowl_bg(); d = ImageDraw.Draw(img)
    place(img, bolt_layer("jab"), 290, F)
    place(img, bolt_layer("hurt", RIVET), 380, F, -1)
    d.regular_polygon((352, 205, 16), 8, fill="#fff2a0")
    hud(d, bolt_wind=0.55, rivet_hp=0.8)
    arrow(d, (230, 120), (330, 120))
    frame_label(img, 3, "Jab lands - clang", "MEDIUM · EYE LEVEL · GAMEPLAY")
    img.convert("RGB").save(SB / "03-core-action.png")

    # 04 close-up on the key, low angle, design view
    img = Image.new("RGBA", (640, 360), ENV["deep"]); d = ImageDraw.Draw(img)
    big = bolt_layer("rewind", scale=3.2)
    place(img, big, 470, 560)
    d.arc([40, 60, 240, 260], 200, 330, fill="#ffd27a", width=5)
    arrow(d, (210, 90), (232, 130))
    d.text((60, 300), "click . click . click  (one per quarter turn)", fill="white", font=font(16))
    frame_label(img, 4, "Rewind - count the clicks", "CLOSE-UP · LOW ANGLE · DESIGN")
    img.convert("RGB").save(SB / "04-rewind-closeup.png")

    # 05 failure: medium, Dutch angle (knockdown camera roll), gameplay
    img = bowl_bg(); d = ImageDraw.Draw(img)
    place(img, bolt_layer("empty"), 300, F)
    place(img, bolt_layer("cutlass", RIVET), 400, F, -1)
    hud(d, bolt_wind=0.0, bolt_hp=0.35, rivet_hp=0.8)
    d.text((300, 120), "EMPTY!", fill="#ff6a5a", font=font(28, True), anchor="mm")
    img = img.rotate(6, resample=Image.BICUBIC, fillcolor="#111")
    frame_label(img, 5, "Spring runs dry - punished", "MEDIUM · DUTCH ANGLE · GAMEPLAY")
    img.convert("RGB").save(SB / "05-failure.png")

    # 06 recovery: wide, eye level, gameplay
    img = bowl_bg(); d = ImageDraw.Draw(img)
    place(img, bolt_layer("rewind"), 130, F)
    place(img, bolt_layer("idle", RIVET), 500, F, -1)
    hud(d, bolt_wind=0.6, bolt_hp=0.35, rivet_hp=0.8)
    arrow(d, (250, 330), (150, 330))
    d.text((320, 120), "back off - rewind at range", fill="white", font=font(18), anchor="mm")
    frame_label(img, 6, "Recover and retry", "WIDE · EYE LEVEL · GAMEPLAY")
    img.convert("RGB").save(SB / "06-recovery.png")

    # 07 success / end: medium, low angle, design view
    img = Image.new("RGBA", (640, 360), ENV["deep"]); d = ImageDraw.Draw(img)
    d.rectangle([0, 300, 640, 360], fill=ENV["gravel"])
    place(img, bolt_layer("win", scale=1.6), 230, 340)
    place(img, bolt_layer("ko", RIVET, scale=1.2), 470, 330, -1)
    d.text((470, 90), "K.O.", fill="#ffd27a", font=font(56, True), anchor="mm")
    d.text((470, 140), "R - rematch", fill="white", font=font(16), anchor="mm")
    frame_label(img, 7, "Knockout - session ends", "MEDIUM · LOW ANGLE · DESIGN")
    img.convert("RGB").save(SB / "07-knockout.png")

    # contact sheet
    files = sorted(SB.glob("0*.png"))
    sheet = Image.new("RGB", (640 * 2 + 30, 370 * 4 + 10), "#ddd")
    for i, f in enumerate(files):
        sheet.paste(Image.open(f), (10 + (i % 2) * 650, 10 + (i // 2) * 370))
    sheet.save(SB / "contact-sheet.png")


# ---------------------------------------------------------------- character sheet images
HURTBOX = (50, 106)  # w, h in viewport px, bottom-centred on the feet


def character():
    # silhouette at actual size on a game-sized frame, plus 4x zoom
    img = bowl_bg(); d = ImageDraw.Draw(img)
    place(img, bolt_layer("idle", silhouette=True), 200, 300)
    place(img, bolt_layer("idle", RIVET, silhouette=True), 440, 300, -1)
    d.text((320, 40), "Silhouette test at real size: 640x360 viewport, 112 px tall", fill="white", font=font(14, True), anchor="mm")
    img.convert("RGB").save(CH / "silhouette-in-game.png")

    row = Image.new("RGBA", (1100, 230), "white")
    for i, p in enumerate(["idle", "jab", "cutlass", "pop", "block", "rewind", "hurt", "empty", "win"]):
        place(row, bolt_layer(p, silhouette=True), 60 + i * 120, 200)
        ImageDraw.Draw(row).text((60 + i * 120, 215), p, fill="black", font=font(13), anchor="mm")
    row.convert("RGB").save(CH / "silhouette-row.png")

    # pose targets (12 incl. turnaround)
    poses = list(POSES.keys())
    sheet = Image.new("RGBA", (6 * 190, 2 * 230 + 40), "white")
    sd = ImageDraw.Draw(sheet)
    sd.text((10, 8), "Pose targets (Claude-drawn spec, NOT generated art) - Bolt faces right; left = runtime flip", fill="black", font=font(15, True))
    for i, p in enumerate(poses):
        x, y = 95 + (i % 6) * 190, 220 + (i // 6) * 230
        place(sheet, bolt_layer(p), x, y)
        sd.text((x, y + 6), f"P{i + 2:02d} {p}", fill="black", font=font(14, True), anchor="mt")
    sheet.convert("RGB").save(CH / "pose-targets.png")

    # turnaround target: front, three-quarter, side, back with height bar
    ta = Image.new("RGBA", (820, 220), "white"); td = ImageDraw.Draw(ta)
    side = bolt_layer("idle")
    front = Image.new("RGBA", side.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(front)
    cx, feet = side.width / 2, side.height - 4
    for img_, label, x in [(front, "front", 160), (side, "three-quarter", 330), (side, "side", 500), (front, "back", 670)]:
        pass
    # front/back drawn as simple symmetric figure
    def sym(back=False):
        im = Image.new("RGBA", side.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        h = H; ol = PAL["outline"]
        for s in (-1, 1):
            bx = cx + s * h * 0.10
            dd.rectangle([bx - h * .05, feet - h * .28, bx + h * .05, feet - h * .08], fill=PAL["enamel"], outline=ol, width=2)
            dd.rounded_rectangle([bx - h * .07, feet - h * .10, bx + h * .07, feet], radius=3, fill=PAL["steel"], outline=ol, width=2)
            dd.line([cx + s * h * .2, feet - h * .52, cx + s * h * .3, feet - h * .32], fill=PAL["enamel"], width=7)
            dd.ellipse([cx + s * h * .3 - 7, feet - h * .32 - 7, cx + s * h * .3 + 7, feet - h * .32 + 7], fill=PAL["steel"], outline=ol)
        dd.rounded_rectangle([cx - h * .21, feet - h * .58, cx + h * .21, feet - h * .26], radius=8, fill=PAL["enamel"], outline=ol, width=2)
        hr = h * .2; hy = feet - h * .58 - hr * .85
        dd.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=PAL["brass"], outline=ol, width=2)
        if back:
            dd.ellipse([cx - 12, feet - h * .47 - 12, cx + 12, feet - h * .47 + 12], fill=PAL["key"], outline=ol, width=2)
        else:
            pr = hr * .6
            dd.ellipse([cx - pr, hy - pr, cx + pr, hy + pr], fill=PAL["glass"], outline=ol, width=4)
            for ex in (cx - 5, cx + 5):
                dd.ellipse([ex - 2.5, hy - 3, ex + 2.5, hy + 3], fill=ol)
        return im
    place(ta, sym(), 150, 200)
    place(ta, bolt_layer("idle").resize((side.width, side.height)), 330, 200)
    place(ta, bolt_layer("idle"), 500, 200)
    place(ta, sym(back=True), 670, 200)
    for x, l in [(150, "front"), (330, "3/4 (approx.)"), (500, "side"), (670, "back")]:
        td.text((x, 206), l, fill="black", font=font(13), anchor="mt")
    td.line([40, 200, 40, 200 - H], fill="black", width=3)
    for k in range(5):
        y = 200 - H * k / 4
        td.line([34, y, 46, y], fill="black", width=2)
    td.text((52, 200 - H), f"{H} px", fill="black", font=font(12))
    td.text((52, 200 - H * 0.6 - 6), "helmet 40%", fill="black", font=font(11))
    ta.convert("RGB").save(CH / "turnaround-target.png")

    # collision overlay on every pose at the same scale
    cs = Image.new("RGBA", (6 * 190, 2 * 230 + 60), "white"); cd = ImageDraw.Draw(cs)
    cd.text((10, 8), f"Collision: green = hurtbox {HURTBOX[0]}x{HURTBOX[1]} px (bottom-centred). red = attack hitbox (active frames only).", fill="black", font=font(14, True))
    hitboxes = {"jab": (24, -76, 30, 22), "cutlass": (20, -98, 58, 40), "pop": None}
    for i, p in enumerate(poses[1:] + ["idle"]):
        if i >= 11:
            break
        x, y = 95 + (i % 6) * 190, 230 + (i // 6) * 230
        place(cs, bolt_layer(p), x, y)
        w, h = HURTBOX
        if p == "ko":
            cd.rectangle([x - h / 2, y - w, x + h / 2, y], outline="#13a34a", width=2)
        else:
            cd.rectangle([x - w / 2, y - h, x + w / 2, y], outline="#13a34a", width=2)
        hb = hitboxes.get(p)
        if hb:
            cd.rectangle([x + hb[0], y + hb[1], x + hb[0] + hb[2], y + hb[1] + hb[3]], outline="#dc2626", width=2)
        if p == "pop":
            cd.rectangle([x + 70, y - 80, x + 80, y - 70], outline="#dc2626", width=2)
            cd.text((x + 60, y - 96), "cork 10x10", fill="#dc2626", font=font(11))
        cd.text((x, y + 6), p, fill="black", font=font(13, True), anchor="mt")
    cs.convert("RGB").save(CH / "collision-overlay.png")

    # palette swatches + contrast check against the planned environment colours
    def lum(hexc):
        r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
        f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

    def contrast(a, b):
        la, lb = sorted([lum(a), lum(b)], reverse=True)
        return (la + 0.05) / (lb + 0.05)

    pimg = Image.new("RGB", (900, 330), "white"); pd = ImageDraw.Draw(pimg)
    pd.text((10, 8), "Palette (hex) and luminance contrast vs. planned environment colours", fill="black", font=font(15, True))
    lines = []
    for row, (name, pal) in enumerate([("Bolt", PAL), ("Rivet", RIVET)]):
        for i, (k, v) in enumerate(pal.items()):
            x, y = 10 + i * 145, 40 + row * 140
            pd.rectangle([x, y, x + 130, y + 60], fill=v, outline="black")
            c1 = contrast(v, ENV["deep"]); c2 = contrast(v, ENV["gravel"])
            pd.text((x, y + 64), f"{name} {k}\n{v}\nvs bowl {c1:.1f}:1\nvs gravel {c2:.1f}:1", fill="black", font=font(12))
            lines.append(f"| {name} | {k} | `{v}` | {c1:.2f}:1 | {c2:.2f}:1 |")
    pimg.save(CH / "palette.png")
    (CH / "contrast-table.md").write_text(
        "| Fighter | Role | Hex | vs bowl `#1F3A5A` | vs gravel `#6F7F8C` |\n|---|---|---|---|---|\n" + "\n".join(lines) + "\n"
    )


if __name__ == "__main__":
    storyboard()
    character()
    print("design sketches written to", ROOT)
