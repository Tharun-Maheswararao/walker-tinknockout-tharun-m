"""GDD raster figures from existing game art and screenshots: python tools/gdd/make_figures.py

Writes design/gdd/{bolt-poses,hud-callouts,style-this-not-that,props-2d,screens-grid}.png.
Only composites and labels existing files; no new art is generated. The SVG figures in
design/gdd/ are hand-written and are not built by this script.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "design/gdd"
FIGHTERS = ROOT / "godot/assets/fighters"
SCREENS = ROOT / "evidence/screens"
NAVY, PANEL, BRASS, GOLD, CREAM, MUTED, RED = "#1B2438", "#26324D", "#C9962B", "#E8C35A", "#F2E6C4", "#A9B4C8", "#C8382E"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def fit(im, w, h):
    im = im.copy(); im.thumbnail((w, h), Image.LANCZOS); return im


def bolt_poses():
    """11 Bolt poses (one per game state) + Rivet's palette swap, 6 x 2, labelled with the state."""
    cells = [("bolt", s, s.upper()) for s in
             ["idle", "walk", "jab", "cutlass", "pop", "block", "rewind", "hurt", "empty", "ko", "win"]]
    cells.append(("rivet", "idle", "RIVET (recolour)"))
    cw, ch, pad = 260, 270, 14
    sheet = Image.new("RGB", (6 * cw + 7 * pad, 2 * ch + 3 * pad), NAVY)
    d = ImageDraw.Draw(sheet)
    for k, (skin, pose, label) in enumerate(cells):
        x, y = pad + (k % 6) * (cw + pad), pad + (k // 6) * (ch + pad)
        d.rounded_rectangle([x, y, x + cw, y + ch], 12, fill=PANEL, outline=BRASS if skin == "bolt" else "#3F8F7A", width=2)
        im = fit(Image.open(FIGHTERS / skin / f"{pose}.png").convert("RGBA"), cw - 20, ch - 50)
        sheet.paste(im, (x + (cw - im.width) // 2, y + ch - 40 - im.height), im)
        d.text((x + cw // 2, y + ch - 20), label, fill=CREAM, font=font(17, True), anchor="mm")
    sheet.save(OUT / "bolt-poses.png")


def hud_callouts():
    """Numbered call-outs on a real gameplay capture, with the legend under the frame."""
    shot = Image.open(SCREENS / "03-jab-hit.png").convert("RGB")
    W, H = shot.size
    legend_h = 190
    im = Image.new("RGB", (W, H + legend_h), NAVY)
    im.paste(shot, (0, 0))
    d = ImageDraw.Draw(im)
    marks = [  # (x, y) on the 1280x720 capture, label
        (500, 66, "Health bar: brass for Bolt, copper for Rivet; empties toward the centre"),
        (128, 131, "Spring dial: the wind left; turns red under 25 %"),
        (1150, 131, "Rivet's spring dial: read it to know when Rivet must stop and rewind"),
        (505, 366, "Hit spark + 0.07 s hitstop + screen shake: the hit reads with the sound off"),
        (612, 352, "Porthole face: eyes show the state (half-closed EMPTY, X at K.O.)"),
        (840, 470, "Winding key on the back: shows facing; spins while rewinding"),
        (420, 300, "Sunken castle: scenery (also a 3D prop from Assignment 3)"),
    ]
    for n, (x, y, _) in enumerate(marks, 1):
        d.ellipse([x - 19, y - 19, x + 19, y + 19], fill=RED, outline=GOLD, width=4)
        d.text((x, y + 1), str(n), fill="#FFF6DA", font=font(22, True), anchor="mm")
    for n, (_, _, text) in enumerate(marks, 1):
        col, row = (n - 1) // 4, (n - 1) % 4
        x, y = 30 + col * 640, H + 26 + row * 40
        d.ellipse([x, y - 13, x + 26, y + 13], fill=RED, outline=GOLD, width=2)
        d.text((x + 13, y + 1), str(n), fill="#FFF6DA", font=font(15, True), anchor="mm")
        d.text((x + 38, y), text, fill=CREAM, font=font(17), anchor="lm")
    im.save(OUT / "hud-callouts.png")


def style_this_not_that():
    """Accepted style next to the rejected photo-real first batch (ASSET-LOG CHAR-REF v1)."""
    w, h = 1100, 520
    im = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(im)
    panels = [
        (30, "#4FB39A", "THIS", "flat, illustrated tin toy: bold dark outline,",
         "enamel colours, helmet about 40 % of height"),
        (570, "#FF8A7A", "NOT THIS", "a photo of a real toy (rejected, CHAR-REF v1):",
         "too detailed to read at 112 px, no eyes, fingers"),
    ]
    for x, col, head, l1, l2 in panels:
        d.rounded_rectangle([x, 30, x + 500, 400], 14, fill="#E9E4D8", outline=col, width=5)
        d.text((x, 428), head, fill=col, font=font(26, True))
        d.text((x, 466), l1, fill=CREAM, font=font(18))
        d.text((x, 492), l2, fill=MUTED, font=font(18))
    bolt = fit(Image.open(FIGHTERS / "bolt/idle.png").convert("RGBA"), 440, 340)
    im.paste(bolt, (30 + (500 - bolt.width) // 2, 385 - bolt.height), bolt)
    photo = Image.open(ROOT / "design/rejected/CHAR-REF-v1.jpg").convert("RGB").crop((800, 8, 1056, 264))
    photo = photo.resize((340, 340), Image.LANCZOS)
    im.paste(photo, (570 + 80, 45))
    im.save(OUT / "style-this-not-that.png")


def props_2d():
    """The four 2D weapon/prop sprites, enlarged, with what each one does."""
    props = [("cutlass.png", 3, "Tin cutlass", "K · −22 wind · 13 dmg"),
             ("popgun.png", 3, "Cork pop-gun", "L · −30 wind · fires a cork"),
             ("cork.png", 6, "Cork", "320 px/s · 10 dmg"),
             ("key-bolt.png", 3, "Winding key (Bolt)", "spins 90° per click"),
             ("key-rivet.png", 3, "Winding key (Rivet)", "recoloured copy")]
    cw, h = 300, 330
    im = Image.new("RGB", (cw * len(props) + 20, h), NAVY)
    d = ImageDraw.Draw(im)
    for k, (f, scale, name, note) in enumerate(props):
        x = 10 + k * cw
        d.rounded_rectangle([x + 8, 10, x + cw - 8, h - 10], 12, fill=PANEL, outline="#3A4766", width=2)
        p = Image.open(ROOT / "godot/assets/props" / f).convert("RGBA")
        p = p.resize((p.width * scale // 2, p.height * scale // 2), Image.LANCZOS)
        p = fit(p, cw - 50, 190)
        im.paste(p, (x + (cw - p.width) // 2, 30 + (190 - p.height) // 2), p)
        d.text((x + cw // 2, 250), name, fill=CREAM, font=font(20, True), anchor="mm")
        d.text((x + cw // 2, 282), note, fill=GOLD, font=font(16), anchor="mm")
    im.save(OUT / "props-2d.png")


def screens_grid():
    """Six real engine captures from the slice, 2 x 3, captioned with the storyboard panel."""
    shots = [("01-title.png", "Title: tin toys fight after closing time"),
             ("02-round-intro.png", "Round intro: ROUND 1, the bell, controls locked"),
             ("03-jab-hit.png", "Jab lands: spark, hitstop, Rivet's bar drops"),
             ("04-rewind.png", "Rewind: Bolt cranks the key, the dial refills"),
             ("05-spring-empty.png", "Spring empty: slumped, stalled, open to a hit"),
             ("07-knockout-win.png", "K.O.: the music stops dead, R for a rematch")]
    tw, th, cap, pad = 640, 360, 44, 16
    im = Image.new("RGB", (2 * tw + 3 * pad, 3 * (th + cap) + 4 * pad), NAVY)
    d = ImageDraw.Draw(im)
    for k, (f, text) in enumerate(shots):
        x, y = pad + (k % 2) * (tw + pad), pad + (k // 2) * (th + cap + pad)
        im.paste(fit(Image.open(SCREENS / f).convert("RGB"), tw, th), (x, y))
        d.rectangle([x, y, x + tw - 1, y + th - 1], outline=BRASS, width=2)
        d.text((x + 4, y + th + cap // 2), text, fill=CREAM, font=font(19), anchor="lm")
    im.save(OUT / "screens-grid.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (bolt_poses, hud_callouts, style_this_not_that, props_2d, screens_grid):
        fn(); print("wrote", fn.__name__)
