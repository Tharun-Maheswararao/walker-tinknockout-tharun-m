#!/usr/bin/env python3
"""Build the film's evidence media from real files only.

stills  -> evidence/B02,B03,B05,B12 composites (3840x2160) + copies at media/Bxx.png
capture -> media/B07.mp4, B09.mp4 (silent, narrated) and B10.mp4 (game audio kept)
All source images are real repo files or real engine renders; this script only
lays them out and adds labels. Usage: make_media.py stills|capture
"""
import json, math, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
PKG = REEL.parents[1]
FONTS = Path('/Users/tharunmaheswararao/Documents/csye7270/_brutalist/runtime/fonts')
SERIF = str(FONTS / 'EB_Garamond/static/EBGaramond-Medium.ttf')
SANS = str(FONTS / 'Inter/static/Inter_28pt-Medium.ttf')
MONO = str(FONTS / 'PT_Mono/PTMono-Regular.ttf')
W, H = 3840, 2160
PAGE, INK, SOFT, RULE = (250, 249, 245), (61, 57, 41), (88, 84, 72), (204, 198, 186)
ACC = (152, 80, 57)          # dark terracotta: passes 4.5:1 on cream
IW, IH, IX, IY = 2944, 1656, 448, 250   # 76.7% inset: labels and game inside title-safe
SP = Path('/private/tmp/claude-501/-Users-tharunmaheswararao-Documents-csye7270/47b09bd5-b171-4f13-af4c-becf94b912c4/scratchpad')


def F(path, size):
    return ImageFont.truetype(path, size)


def canvas():
    return Image.new('RGB', (W, H), PAGE)


def fit(im, box_w, box_h, bg=None):
    im = im.convert('RGBA')
    s = min(box_w / im.width, box_h / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    if bg is not None:
        base = Image.new('RGBA', im.size, bg + (255,))
        base.alpha_composite(im)
        im = base
    return im


def paste_center(c, im, x, y, w, h):
    c.paste(im, (x + (w - im.width) // 2, y + (h - im.height) // 2), im if im.mode == 'RGBA' else None)


def header(d, title, sub=None):
    d.text((192, 96), title, font=F(SERIF, 124), fill=INK)
    if sub:
        d.text((192, 262), sub, font=F(SANS, 54), fill=SOFT)


def footer(d, text):
    d.text((192, H - 170), text, font=F(SANS, 48), fill=SOFT)
    d.text((W - 192, H - 170), '@NikBearBrown', font=F(SERIF, 60), fill=INK, anchor='ra')


def wrap(d, text, font, width):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) <= width:
            line = t
        else:
            if line:
                out.append(line)
            line = w
    out.append(line)
    return out


def frame_at(t):
    out = SP / f'frame-{t:.2f}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t}', '-i', str(REEL / 'capture/fight-4k.mp4'),
                    '-frames:v', '1', str(out)], check=True)
    return Image.open(out)


def save(c, bid, name):
    ev = REEL / 'evidence' / name
    ev.parent.mkdir(exist_ok=True)
    c.save(ev)
    (REEL / 'media').mkdir(exist_ok=True)
    shutil.copyfile(ev, REEL / 'media' / f'{bid}.png')
    print('wrote', ev)


def b02():
    c = canvas(); d = ImageDraw.Draw(c)
    header(d, 'Tin Knockout: Concept and Pillars', 'Bolt (player) vs Rivet (same toy, repainted) · one round in a goldfish bowl, after closing')
    fr = fit(frame_at(3.0), 2100, 1181)
    c.paste(fr, (192, 420), fr)
    d.text((192, 420 + fr.height + 24), 'Real engine frame · fight-4k capture at 0:03 · scripted input', font=F(SANS, 54), fill=SOFT)
    x0, y = 2400, 420
    pillars = [('1  Every move costs wind', 'punch, swing, shot, even walking'),
               ('2  Tin you can hear', 'one material sound per contact'),
               ('3  Read the fight at a glance', 'one pose per state; dials, not numbers'),
               ('4  Toys after closing', 'a shop at night, a music-box waltz')]
    for name, line in pillars:
        d.rectangle([x0, y, W - 192, y + 270], outline=RULE, width=4, fill=(255, 253, 248))
        d.rectangle([x0, y, x0 + 14, y + 270], fill=ACC)
        d.text((x0 + 50, y + 36), name, font=F(SERIF, 76), fill=INK)
        d.text((x0 + 50, y + 156), line, font=F(SANS, 48), fill=SOFT)
        y += 300
    footer(d, 'Source: CONCEPT.md (design pillars) · revision 64c037a')
    save(c, 'B02', 'B02-concept-pillars.png')


def b03():
    c = canvas(); d = ImageDraw.Draw(c)
    header(d, 'One Asset, Traced: the Jab (CHAR-JAB)')
    panels = [
        ('1 SPEC', [Image.open(PKG / 'design/character/pose-targets.png').crop((420, 95, 565, 245)),
                    Image.open(PKG / 'design/storyboard/03-core-action.png')],
         'P04 pose (Claude-drawn) + storyboard 3'),
        ('2 INIT SKETCH', [Image.open(PKG / 'raw/inits-ref/jab.png')], 'raw/inits-ref/jab.png'),
        ('3 CANDIDATES', [Image.open(PKG / 'design/rejected/poses-v2-a.jpg').crop((57, 254, 1100, 380))], 'poses-v2-a.jpg jab row (init + 8); 0.6 s43 kept'),
        ('4 RAW OUTPUT', [Image.open(PKG / 'raw/CHAR-JAB/CHAR-JAB_v2-st0.6_s43.png')], 'raw/CHAR-JAB, v2 · st 0.6 · s43'),
        ('5 EDITED', [Image.open(PKG / 'godot/assets/fighters/bolt/jab.png'), Image.open(PKG / 'godot/assets/fighters/rivet/jab.png')],
         'bolt/jab.png + rivet/jab.png'),
        ('6 IN ENGINE', [Image.open(PKG / 'evidence/screens/03b-jab-hit-boxes.png').crop((380, 200, 900, 600))],
         '03b-jab-hit-boxes.png (posed)'),
    ]
    pw, gap, top, ph = 548, 34, 300, 700
    for i, (lab, ims, cap) in enumerate(panels):
        x = 192 + i * (pw + gap)
        d.text((x, top), lab, font=F(SANS, 54), fill=ACC)
        d.rectangle([x, top + 80, x + pw, top + 80 + ph], outline=RULE, width=4, fill=(255, 253, 248))
        n = len(ims)
        if lab.startswith('3'):
            strip = ims[0]; cw = strip.width / 9
            grid = Image.new('RGB', (round(cw * 3), strip.height * 3), (255, 253, 248))
            for k in range(9):
                cell = strip.crop((round(k * cw), 0, round((k + 1) * cw), strip.height))
                grid.paste(cell, (round((k % 3) * cw), (k // 3) * strip.height))
            im = fit(grid, pw - 24, ph - 24)
            paste_center(c, im, x, top + 80, pw, ph)
        else:
            for k, im in enumerate(ims):
                sh = (ph - 24) // n
                im2 = fit(im, pw - 24, sh - 12, bg=(214, 214, 214) if lab.startswith('5') else None)
                paste_center(c, im2, x, top + 80 + 12 + k * sh, pw, sh)
        for j, ln in enumerate(wrap(d, cap, F(SANS, 44), pw)):
            d.text((x, top + 80 + ph + 20 + j * 56), ln, font=F(SANS, 44), fill=SOFT)
        if i < len(panels) - 1:
            ax = x + pw + 4
            d.polygon([(ax, top + 420), (ax + 26, top + 440), (ax, top + 460)], fill=ACC)
    y = 1310
    d.text((192, y), 'PROMPT (ASSET-LOG.md / gen-log.jsonl)', font=F(SANS, 50), fill=ACC)
    prompt = ('"throwing a straight punch forward, 2d cartoon game sprite of a tin wind-up toy deep sea diver, '
              'polished brass helmet with two antennae, red enamel tin suit with rivets, yellow mitten gloves, '
              'steel boots, bold black outline, cel shaded, plain light grey background"')
    for j, ln in enumerate(wrap(d, prompt, F(MONO, 52), W - 384)):
        d.text((192, y + 80 + j * 70), ln, font=F(MONO, 52), fill=INK)
    y2 = y + 80 + 3 * 70 + 40
    rows = [('MODEL', 'SDXL-Turbo img2img · strength 0.6 · 8 steps · seed 43 · 512×512 · cfg 0'),
            ('EDITS', 'tools/edit/process_sprites.py: rembg cut-out · two eyes painted on the glass · 336 px tall, feet at (240, 435) · Rivet = palette recolour'),
            ('REJECTED', 'v1 poses drifted off-model (predicted failure F1) · reference tries v1 photoreal, v3 porthole, v4 gold; human picked s40 of 4 finalists')]
    for k, v in rows:
        d.text((192, y2), k, font=F(SANS, 48), fill=ACC)
        lines = wrap(d, v, F(SANS, 48), W - 384 - 330)
        for j, ln in enumerate(lines):
            d.text((520, y2 + j * 60), ln, font=F(SANS, 48), fill=INK)
        y2 += 60 * len(lines) + 22
    save(c, 'B03', 'B03-jab-asset-trace.png')


def b05():
    c = canvas(); d = ImageDraw.Draw(c)
    header(d, 'Result: the Art Now Stands on Its Hurtbox',
           'Real engine renders (tools/shots.gd) · POSED: fighters placed, then a real jab input · F1 hitbox overlay')
    crop = (380, 160, 940, 620)
    shots = [('BEFORE · centred AND offset by -FEET', PKG / 'evidence/screens/before-fix/03b-jab-hit-boxes-sprite-offset-bug.png'),
             ('AFTER · sprite.centered = false (fighter.gd:73)', PKG / 'evidence/screens/03b-jab-hit-boxes.png')]
    for i, (lab, p) in enumerate(shots):
        x = 192 + i * (1728 + 0)
        im = Image.open(p).crop(crop).convert('RGB')
        im = im.resize((1680, round(1680 * im.height / im.width)), Image.NEAREST)
        d.text((x, 400), lab, font=F(SANS, 60), fill=ACC if i == 0 else INK)
        c.paste(im, (x, 490))
    d.text((192, 490 + 1379 + 10 if False else 1890), 'green = hurtboxes (feet-anchored; the jab hitbox is not active in these frames)  ·  crops of 1280×720 screenshots, scaled 3×',
           font=F(SANS, 54), fill=SOFT)
    save(c, 'B05', 'B05-before-after.png')


def b12():
    c = canvas(); d = ImageDraw.Draw(c)
    header(d, 'Result: the Recorded Test Output')
    d.text((192, 262), 'godot --headless --path godot --script res://tests/test_slice.gd  (isolated copy of 64c037a, 2026-10-06)',
           font=F(SANS, 46), fill=SOFT)
    raw = (SP / 'test-output.txt').read_text().splitlines()
    keep = [l for l in raw if l.strip() and not l.startswith('Godot Engine')]
    term = (192, 350, 2700, H - 120)
    d.rectangle(term, fill=(32, 37, 49))
    fm = F(MONO, 40)
    y = term[1] + 26
    for l in keep:
        col = (174, 231, 209) if l.startswith('PASS') else (236, 224, 161) if ('WARNING' in l or 'ERROR' in l) else (237, 241, 247)
        d.text((term[0] + 30, y), l.rstrip(), font=fm, fill=col)
        y += 50
    x = 2760
    yy = 350
    d.text((x, yy), 'tools/edit/check_seam.py', font=F(SANS, 48), fill=ACC); yy += 70
    for l in (SP / 'seam-output.txt').read_text().splitlines():
        for ln in wrap(d, l.strip(), F(MONO, 40), W - 192 - x):
            d.text((x, yy), ln, font=F(MONO, 40), fill=INK); yy += 52
        yy += 14
    yy += 40
    d.text((x, yy), 'First run (recorded)', font=F(SANS, 48), fill=ACC); yy += 70
    for ln in wrap(d, '8 FAILs: test froze Rivet 3 frames after the round began; a cork hit Bolt mid-test. '
                   'Fixed setup order + 1.5 s pop-gun cooldown. No expected value changed.', F(SANS, 44), W - 192 - x):
        d.text((x, yy), ln, font=F(SANS, 44), fill=INK); yy += 58
    yy += 30
    for ln in wrap(d, 'evidence/tests/run-01-setup-bug.txt', F(MONO, 38), W - 192 - x):
        d.text((x, yy), ln, font=F(MONO, 38), fill=SOFT); yy += 50
    save(c, 'B12', 'B12-test-output.png')


def label_overlay(top, bottom):
    """Full-frame PNG: cream ground with a transparent 90% hole for the capture."""
    ov = Image.new('RGBA', (W, H), PAGE + (255,))
    d = ImageDraw.Draw(ov)
    iw, ih, x0, y0 = IW, IH, IX, IY
    d.rectangle([x0, y0, x0 + iw - 1, y0 + ih - 1], fill=(0, 0, 0, 0))
    d.text((x0, 175), top, font=F(SANS, 64), fill=INK, anchor='lm')
    if bottom:
        d.text((x0, 1980), bottom, font=F(SANS, 52), fill=SOFT, anchor='lm')
    return ov


def make_clip(bid, start, dur, top, bottom, keep_audio):
    ovp = SP / f'overlay-{bid}.png'
    label_overlay(top, bottom).save(ovp)
    frames = math.ceil(dur * 30 - 1e-8)
    out = REEL / 'media' / f'{bid}.mp4'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{start:.3f}', '-i', str(REEL / 'capture/fight-4k.mp4'), '-i', str(ovp),
           '-filter_complex', f'[0:v]scale={IW}:{IH},pad=3840:2160:{IX}:{IY}:color=0xFAF9F5[g];[g][1:v]overlay=0:0,format=yuv420p[v]',
           '-map', '[v]', '-frames:v', str(frames), '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14']
    if keep_audio:
        cmd += ['-map', '0:a', '-c:a', 'aac', '-b:a', '192k', '-t', f'{frames / 30:.4f}']
    else:
        cmd += ['-an']
    subprocess.run(cmd + [str(out)], check=True)
    print('wrote', out, frames, 'frames')


def capture():
    sheet = json.loads((REEL / 'beat_sheet.json').read_text())
    beats = {b['beat_id']: b for b in sheet['beats']}
    total = 24.433
    for bid in ('B07', 'B09'):
        b = beats[bid]
        dur = b['actual_duration_s']
        start = b['shot']['capture_window_s'][0]
        if start + dur > total - 0.05:
            start = max(0.0, total - 0.05 - dur)
        b['shot']['capture_window_s'] = [round(start, 3), round(start + dur, 3)]
        make_clip(bid, start, dur, f'SCRIPTED INPUT · real engine capture (Godot Movie Maker) · fight-4k {start:.1f}–{start + dur:.1f} s',
                  'Narrated: game audio is not in this beat; the full take with its own sound follows.', False)
    make_clip('B10', 0.0, total, 'GAME AUDIO — NO NARRATION · SCRIPTED INPUT',
              'fight-4k full take, 24.4 s · sfx log: bell 2 · jab 13 · cutlass 3 · pop 1 · rewind 26 · empty 1 · Rivet wins by KO', True)
    (REEL / 'beat_sheet.json').write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'stills':
        b02(); b03(); b05(); b12()
    elif what == 'capture':
        capture()
    elif what == 'b10':
        make_clip('B10', 0.0, 24.433, 'GAME AUDIO — NO NARRATION · SCRIPTED INPUT',
                  'fight-4k full take, 24.4 s · sfx log: bell 2 · jab 13 · cutlass 3 · pop 1 · rewind 26 · empty 1 · Rivet wins by KO', True)
