#!/usr/bin/env python3
"""Build the A5 film's own media from real files, recorded output and real engine captures only.

Every image placed here is a committed in-engine capture (evidence/a5/captures/, windowed,
scripted input, Claude-made), Tharun's OS screenshot, or the film's Movie Maker capture
(capture/rewind-4k.mp4, scripted input, isolated copy of 2e6946d). Text panels are verbatim
lines from repo files and logs. This script lays them out, adds provenance labels and switches
highlight states on the spoken cue times written by patch_timing.py. It invents no output.
Helpers adapted from the A3 film's _tools/make_media.py.

Usage: make_media.py all | B02 B04 ...
"""
import json, math, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
RUNS = REEL / 'evidence' / 'runs'
EVB = REPO / 'evidence' / 'blender'
EVG = REPO / 'evidence' / 'godot'
FONTS = Path('/Users/tharunmaheswararao/Documents/csye7270/_brutalist/runtime/fonts')
SERIF = str(FONTS / 'EB_Garamond/static/EBGaramond-Medium.ttf')
SERIF_I = str(FONTS / 'EB_Garamond/static/EBGaramond-Italic.ttf')
SANS = str(FONTS / 'Inter/static/Inter_28pt-Medium.ttf')
SANSB = str(FONTS / 'Lato/static/Lato-Bold.ttf')
MONO = str(FONTS / 'PT_Mono/PTMono-Regular.ttf')
W, H, FPS = 3840, 2160, 30
X0, X1, Y0, Y1 = 192, 3648, 108, 2052          # title-safe (5 %)
PAGE, INK, SOFT, RULE, CARD = (250, 249, 245), (61, 57, 41), (95, 91, 78), (205, 199, 187), (255, 255, 255)
ACC = (150, 72, 48)                             # dark terracotta, ≥4.5:1 on cream (text use)
RING = (217, 119, 87)                           # the spark terracotta, for rings/rules only
TERM, TTEXT, TMUTED, TMARK, TBLUE = (32, 37, 49), (237, 241, 247), (190, 200, 215), (69, 90, 113), (139, 199, 243)
TGREEN, TYELLOW, TRED = (174, 231, 209), (236, 224, 161), (255, 170, 160)
WORK = REEL / 'media' / '_work'
MIN_PT = 44


def F(path, size):
    return ImageFont.truetype(path, max(size, MIN_PT))


def canvas():
    return Image.new('RGB', (W, H), PAGE)


def wrap(d, text, font, width):
    out, line = [], ''
    for w in text.split(' '):
        t = (line + ' ' + w) if line else w
        if d.textlength(t, font=font) <= width:
            line = t
        else:
            if line:
                out.append(line)
            while d.textlength(w, font=font) > width:
                k = len(w)
                while k > 1 and d.textlength(w[:k], font=font) > width:
                    k -= 1
                out.append(w[:k]); w = w[k:]
            line = w
    out.append(line)
    return out


def text_block(d, xy, text, font, width, fill=INK, lh=None):
    x, y = xy
    lh = lh or int(font.size * 1.32)
    for para in text.split('\n'):
        for ln in wrap(d, para, font, width):
            d.text((x, y), ln, font=font, fill=fill); y += lh
    return y


def header(d, title, sub=None):
    d.text((X0, 112), title, font=F(SERIF, 108), fill=INK)
    if sub:
        d.text((X0, 252), sub, font=F(SANS, 44), fill=SOFT)


def footer(d, text):
    f = F(SANS, 44)
    lines = wrap(d, text, f, 2950)
    y = 2040 - 58 * len(lines)
    for ln in lines:
        d.text((X0, y), ln, font=f, fill=SOFT); y += 58
    d.text((X1, 1984), '@NikBearBrown', font=F(SERIF, 56), fill=INK, anchor='ra')


def label(d, xy, who, path):
    """Provenance label above an embedded image: bold 'who', then the file path."""
    x, y = xy
    d.text((x, y), who, font=F(SANSB, 46), fill=ACC)
    d.text((x + d.textlength(who, font=F(SANSB, 46)) + 24, y + 2), path, font=F(SANS, 42), fill=SOFT)


def fit(im, bw, bh):
    s = min(bw / im.width, bh / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS), s


RECTS = {}          # beat -> image rectangles (real embedded images), for _tools/selfcheck.py masks
CUR = ['']


def put(c, im, xy):
    c.paste(im, xy)
    RECTS.setdefault(CUR[0], set()).add((xy[0], xy[1], xy[0] + im.width, xy[1] + im.height))


def paste_framed(c, d, im, x, y):
    put(c, im, (x, y))
    d.rectangle((x - 2, y - 2, x + im.width + 1, y + im.height + 1), outline=RULE, width=3)


def ring(d, box, s, ox, oy, width=9, pad=6):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((ox + int(x0 * s) - pad, oy + int(y0 * s) - pad, ox + int(x1 * s) + pad, oy + int(y1 * s) + pad),
                        radius=10, outline=RING, width=width)


def card(d, xy, title, body, on=False, fsize=46, tsize=48):
    x0, y0, x1 = xy
    ft, fb = F(SANSB, tsize), F(SANS, fsize)
    lines = []
    for para in body.split('\n'):
        lines += wrap(d, para, fb, x1 - x0 - 70)
    hgt = 40 + int(tsize * 1.3) + int(fsize * 1.32) * len(lines) + 30
    d.rectangle((x0, y0, x1, y0 + hgt), fill=CARD, outline=ACC if on else RULE, width=6 if on else 3)
    d.rectangle((x0, y0, x0 + 12, y0 + hgt), fill=ACC if on else RULE)
    d.text((x0 + 40, y0 + 26), title, font=ft, fill=ACC if on else INK)
    y = y0 + 30 + int(tsize * 1.3)
    for ln in lines:
        d.text((x0 + 40, y), ln, font=fb, fill=INK); y += int(fsize * 1.32)
    return y0 + hgt


def terminal(d, xy, title, rows, size=40):
    """rows: [(text, colour or None, highlighted)]"""
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=16, fill=TERM)
    d.text((x0 + 30, y0 + 22), title, font=F(SANS, 40), fill=TBLUE)
    fm = F(MONO, size)
    lh = int(size * 1.36)
    y = y0 + 100
    for text, col, hi in rows:
        lines = wrap(d, text, fm, x1 - x0 - 80) if text else ['']
        if hi:
            d.rectangle((x0 + 10, y - 6, x1 - 10, y - 6 + lh * len(lines)), fill=TMARK)
            d.rectangle((x0 + 10, y - 6, x0 + 20, y - 6 + lh * len(lines)), fill=TBLUE)
        for ln in lines:
            d.text((x0 + 38, y), ln, font=fm, fill=col or TTEXT); y += lh
    assert y <= y1 + 4, ('terminal overflow', title, y, y1)
    return y


def sheet():
    return json.loads((REEL / 'beat_sheet.json').read_text())


def beat(bid):
    return next(b for b in sheet()['beats'] if b['beat_id'] == bid)


def nframes(b):
    return round(b['actual_duration_s'] * FPS)


def ct(b, key):
    return b['shot']['cue_times'][str(key)]


def states_video(bid, states, n):
    """states: [(t_start_s, PIL image)], first at 0. Hard cuts on the cue times."""
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / f'{bid}-masks.json').write_text(json.dumps(sorted(RECTS.get(bid, []))))
    lst = WORK / f'{bid}.txt'
    starts = [max(0, round(t * FPS)) for t, _ in states] + [n]
    rows = []
    for k, (t, im) in enumerate(states):
        p = WORK / f'{bid}-{k}.png'
        im.save(p)
        m = starts[k + 1] - starts[k]
        if m > 0:
            rows.append(f"file '{p}'\nduration {m / FPS:.6f}\n")
    rows.append(f"file '{WORK / f'{bid}-{len(states) - 1}.png'}'\n")
    lst.write_text(''.join(rows))
    out = REEL / 'media' / f'{bid}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst),
                    '-vf', f'fps={FPS},format=yuv420p', '-frames:v', str(n), '-r', str(FPS),
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-an', str(out)], check=True)
    print('wrote', out, n, 'frames', len(states), 'states')


def staged(bid, keys, img):
    """img(i) for state i (0 = before the first cue); state i>0 starts at cue keys[i-1]."""
    CUR[0] = bid
    b = beat(bid)
    st = [(0.0, img(0))] + [(ct(b, k), img(i + 1)) for i, k in enumerate(keys)]
    if st[1][0] < 0.4:
        st = [(0.0, st[1][1])] + st[2:]
    states_video(bid, st, nframes(b))



# ================================================================== A5
CAP = REPO / 'evidence' / 'a5' / 'captures'
SP_MOVIE = REEL / 'media' / '_work' / 'rewind'   # frames decoded from capture/rewind-4k.mp4 (0..220)
GL_KW = (r'\b(?:shader_type|render_mode|uniform|group_uniforms|void|float|vec2|vec3|vec4|ivec2|sampler2D|'
         r'return|if|else|for|var|const|func|extends|preload|true|false)\b')
GTOK = re.compile(r'("[^"\n]*"|//[^\n]*|##?[^\n]*|' + GL_KW + r'|\b\d+(?:\.\d+)?\b)')


def gl_line(d, x, y, text, font):
    for s in GTOK.split(text):
        if not s:
            continue
        col = TTEXT
        if s.startswith('//') or s.startswith('#'):
            col = (186, 197, 188)
        elif s[0] == '"':
            col = TYELLOW
        elif re.fullmatch(r'\d+(?:\.\d+)?', s):
            col = TGREEN
        elif re.fullmatch(GL_KW, s):
            col = (243, 155, 206)
        d.text((x, y), s, font=font, fill=col)
        x += d.textlength(s, font=font)


def src_lines(path, a, b):
    return (REPO / path).read_text().splitlines()[a - 1:b]


def code_box(d, box, path, rows, active=(), size=46, note=None):
    """rows: [(line_no, text)]; long lines wrap under their number. Returns bottom y."""
    x0, y0, x1, _ = box
    fm = F(MONO, size)
    lh = int(size * 1.42)
    lay = []
    for no, text in rows:
        text = text.replace('\t', '    ')
        body = text.lstrip(' ')
        iw = d.textlength(' ' * (len(text) - len(body)), font=fm)    # keep the source indentation
        parts = wrap(d, body, fm, x1 - x0 - 210 - iw) if body else ['']
        lay.append((no, iw, parts))
    h = 130 + sum(len(p) for _, _, p in lay) * lh + 40 + (90 if note else 0)
    d.rounded_rectangle((x0, y0, x1, y0 + h), radius=18, fill=TERM)
    d.rectangle((x0, y0 + 18, x1, y0 + 96), fill=(52, 61, 77))
    d.text((x0 + 36, y0 + 30), path, font=F(MONO, 44), fill=TTEXT)
    y = y0 + 124
    for no, iw, parts in lay:
        if no in active:
            d.rectangle((x0 + 12, y - 8, x1 - 12, y - 8 + lh * len(parts)), fill=TMARK)
            d.rectangle((x0 + 12, y - 8, x0 + 24, y - 8 + lh * len(parts)), fill=TBLUE)
        if no is not None:
            d.text((x0 + 40, y + (size - 44) // 2), str(no), font=F(MONO, 44), fill=TMUTED)
        for p in parts:
            gl_line(d, x0 + 170 + iw, y, p, fm); y += lh
    if note:
        d.text((x0 + 40, y + 14), note, font=F(SANS, 44), fill=TBLUE)
    return y0 + h


def cap_label(d, x, y, who, path):
    label(d, (x, y), who, path)


# ------------------------------------------------------------------ B02 game / state / object
def b02():
    os_im = Image.open(CAP / 'os-screenshot' / 'os_screenshot_rewinding.png').convert('RGB').crop((0, 95, 3024, 1795))
    im, s = fit(os_im, 2150, 1209)
    side = Image.open(CAP / 'toybox' / 'toyboxes_side_by_side_crop2x.png').convert('RGB')
    tb, _ = fit(side, 1150, 420)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Game · State · Object', 'Tin Knockout, Assignment 5: what the tint says, and what gets the texture')
        cap_label(d, X0, 360, 'OS SCREENSHOT · Tharun, during play', 'evidence/a5/captures/os-screenshot/')
        paste_framed(c, d, im, X0, 430)
        if i >= 2:
            for box in ((700, 590, 1030, 1330), (1450, 750, 1830, 1330)):
                ring(d, box, s, X0, 430, width=10, pad=10)
        x = 2440
        y = card(d, (x, 360, X1), 'GAME', 'Tin Knockout: two tin wind-up toys box in an empty goldfish bowl.')
        y = card(d, (x, y + 36, X1), 'STATE · REWIND',
                 'A fighter cranks its key and is open: a hit does 1.5× damage. The vulnerable window.', on=i >= 1)
        y = card(d, (x, y + 36, X1), 'OBJECT · the toy box',
                 'godot/prop_room/prop_room.tscn gets the textured shader painted_tin.', on=i >= 3)
        cap_label(d, x, y + 40, 'IN-ENGINE CAPTURE', 'fresh + worn')
        paste_framed(c, d, tb, x, y + 110)
        footer(d, 'Screenshot: full-screen Retina with the display colour profile, so predictions are checked against '
                  'in-engine captures instead (TEST-REPORT A5-4).')
        return c
    staged('B02', ['state', 'shot', 'object'], img)


# ------------------------------------------------------------------ B04 controlled values
PIX = {'A': (407, 477), 'B': (427, 396)}
PRED = {'0.0': {'A': (217, 87, 64), 'B': (251, 188, 34)}, '0.5': {'A': (185, 105, 112), 'B': (211, 181, 89)},
        '1.0': {'A': (154, 124, 160), 'B': (171, 174, 145)}, '2.0': None}


def samples():
    out = {}
    for ln in (CAP / 'pixel-samples.txt').read_text().splitlines():
        m = re.match(r'([\d.]+) \| ([AB]) \| \(\d+,\d+\) \| \((\d+), (\d+), (\d+)\)', ln)
        if m:
            out[(m.group(1), m.group(2))] = tuple(int(v) for v in m.group(3, 4, 5))
    return out


def b04():
    S = samples()
    crop = (280, 250, 580, 620)
    crops = {}
    for v in PRED:
        im = Image.open(CAP / f'bolt_rewind_amount_{v}.png').convert('RGB').crop(crop)
        crops[v], sc = fit(im, 790, 975)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Colour Line, Measured', 'Hand predictions (CHANGE-BRIEF A5.3, Tharun) vs in-engine captures')
        cap_label(d, X0, 330, 'IN-ENGINE CAPTURE · SCRIPTED INPUT', 'tools/a5_capture_run.gd · evidence/a5/captures/')
        on = {0: set(), 1: {'0.0', '0.5'}, 2: {'1.0'}, 3: {'2.0'}}[i]
        for k, v in enumerate(PRED):
            x = X0 + k * (790 + 99)
            im = crops[v]
            d.text((x, 410), f'rewind_amount {v}', font=F(SANSB, 50), fill=ACC if v in on else INK)
            paste_framed(c, d, im, x, 480)
            for nm, (px, py) in PIX.items():
                cx, cy = x + (px - crop[0]) * sc, 480 + (py - crop[1]) * sc
                d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=(255, 255, 255), width=6)
                d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), outline=INK, width=3)
                d.text((cx + 34, cy - 30), nm, font=F(SANSB, 52), fill=(255, 255, 255), stroke_width=4, stroke_fill=INK)
            y0 = 480 + im.height + 40
            if PRED[v]:
                body = '\n'.join(f'{nm}  predicted {PRED[v][nm]}\n     captured {S[(v, nm)]}' for nm in 'AB')
                t = {'0.0': 'exact', '0.5': 'exact', '1.0': '4 channels −1'}[v]
            else:
                body = '\n'.join(f'{nm}  captured {S[(v, nm)]}' for nm in 'AB') + '\nset from code: pure tint'
                t = 'not clamped'
            card(d, (x, y0, x + 790), t, body, on=v in on, fsize=44, tsize=48)
        footer(d, 'A = Bolt\'s chest, B = helmet. Crops of the 1280×720 captures; pixel-samples.txt. '
                  'tint (90, 160, 255) · strength 0.5')
        return c
    staged('B04', ['half', 'one', 'two'], img)


# ------------------------------------------------------------------ B06 motion (Movie Maker capture)
def b06():
    b = beat('B06'); n = nframes(b)
    log = {int(m.group(1)): (int(m.group(2)), float(m.group(3))) for m in
           re.finditer(r'frame (\d+) state (\d+) rewind_amount ([\d.]+)',
                       (REEL / 'evidence' / 'runs' / 'rewind-capture-log.txt').read_text())}
    names = {0: 'IDLE', 1: 'WALK', 2: 'JAB', 3: 'CUTLASS', 4: 'POP', 5: 'BLOCK', 6: 'REWIND', 7: 'HURT'}
    slow = round(ct(b, 'slow') * FPS)
    seq = []
    for k in range(n):
        if k < 221:
            seq.append((k, 'REAL SPEED · frames 0–220'))
        elif k < slow:
            seq.append((min(72 + (k - 221), 220), 'REPLAY · real speed'))
        else:
            seq.append((min(84 + (k - slow) // 4, 220), 'REPLAY · 0.25× speed (each frame shown 4×)'))
    VW, VH = 2720, 1530
    base = canvas(); d = ImageDraw.Draw(base)
    header(d, 'The Tint in Play')
    cap_label(d, X0, 300, 'MOVIE MAKER CAPTURE · SCRIPTED INPUT',
              'made for this film · isolated copy of 2e6946d · capture/rewind-4k.mp4')
    d.rectangle((X0 - 2, 378, X0 + VW + 1, 380 + VH + 1), outline=RULE, width=3)
    footer(d, 'Script: confirm, then hold rewind 1.5 s, release, hold 1 s. Rivet is the game\'s own AI. '
              'Values: printed by _tools/film_rewind.gd each frame (log frame = movie frame + 2).')
    RECTS.setdefault('B06', set()).add((X0, 380, X0 + VW, 380 + VH))
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / 'B06-masks.json').write_text(json.dumps(sorted(RECTS['B06'])))
    out = REEL / 'media' / 'B06.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                          '-pix_fmt', 'yuv420p', '-an', str(out)], stdin=subprocess.PIPE)
    cache = {}
    px = X0 + VW + 80
    for k, (src, mode) in enumerate(seq):
        if src not in cache:
            cache.clear()
            cache[src] = Image.open(SP_MOVIE / f'frame{src:08d}.png').convert('RGB').resize((VW, VH), Image.LANCZOS)
        c = base.copy(); dd = ImageDraw.Draw(c)
        c.paste(cache[src], (X0, 380))
        st, val = log.get(src + 2, (0, 0.0))
        dd.text((px, 400), 'rewind_amount', font=F(MONO, 48), fill=SOFT)
        dd.text((px, 470), f'{val:.4f}', font=F(MONO, 104), fill=ACC)
        bw = X1 - px
        dd.rectangle((px, 620, X1, 680), outline=RULE, width=3)
        dd.rectangle((px, 620, px + int(bw * min(val, 1.0)), 680), fill=(90, 160, 255))
        dd.text((px, 740), 'Bolt state', font=F(MONO, 48), fill=SOFT)
        dd.text((px, 810), names.get(st, str(st)), font=F(SANSB, 80), fill=INK)
        dd.text((px, 960), 'movie frame', font=F(MONO, 48), fill=SOFT)
        dd.text((px, 1030), str(src), font=F(MONO, 80), fill=INK)
        y = 1200
        for ln in wrap(dd, mode, F(SANSB, 46), bw):
            dd.text((px, y), ln, font=F(SANSB, 46), fill=ACC if 'REPLAY' in mode else SOFT); y += 62
        p.stdin.write(c.tobytes())
    p.stdin.close(); p.wait()
    print('wrote', out, n, 'frames')


# ------------------------------------------------------------------ B07 one shader, two materials
def b07():
    sh = 'godot/shaders/painted_tin.gdshader'
    fr = 'godot/prop_room/materials/toybox_fresh.tres'
    wo = 'godot/prop_room/materials/toybox_worn.tres'

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q2 · One Shader, Two Materials')
        d.text((X1, 150), 'SOURCE VIEW · not an editor recording', font=F(SANSB, 44), fill=ACC, anchor='ra')
        act = set(range(8, 14)) if i == 1 else set()
        y = code_box(d, (X0, 300, X1, 0), f'{sh}  ·  lines 7–14  ·  the program and its knobs',
                     list(zip(range(7, 15), src_lines(sh, 7, 14))), act, size=48)
        act2 = {11} if i == 2 else ({15, 16} if i == 3 else set())
        w2 = (X1 - X0 - 60) // 2
        for k, path in enumerate((fr, wo)):
            x = X0 + k * (w2 + 60)
            code_box(d, (x, y + 50, x + w2, 0), path.split('/')[-1] + '  ·  lines 9–16  ·  one set of values',
                     list(zip(range(9, 17), src_lines(path, 9, 16))), act2, size=44)
        footer(d, 'Both .tres files: godot/prop_room/materials/. Values from the brief (CHANGE-BRIEF A5.5): '
                  'fresh wear 0.05, roughness 0.30 · worn wear 0.55, roughness 0.70.')
        return c
    staged('B07', ['knobs', 'shader', 'values'], img)


# ------------------------------------------------------------------ B08 edit checks
def b08():
    ec = CAP / 'toybox' / 'edit_checks'
    ims = [fit(Image.open(ec / f).convert('RGB'), 1131, 410)[0] for f in
           ('0_before_edits_crop2x.png', '1_after_shader_edit_crop2x.png', '2_after_material_edit_crop2x.png')]
    info = [('Before the edits', 'Left: fresh box (toybox_fresh). Right: worn box (toybox_worn). One shader.'),
            ('After the SHADER edit',
             'Tharun: painted_tin.gdshader line 13, uv_scale default 2.5 → 6.0.\nfresh 88 px · worn 1622 px · '
             'castle 0 px changed.\nBOTH boxes changed.'),
            ('After the MATERIAL edit',
             'Tharun: toybox_worn.tres, wear_amount 0.55 → 0.2 (shader restored).\nworn 6698 px · fresh unchanged · '
             'castle 0 px.\nONLY the worn box changed.')]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Shader Edit vs Material Edit', 'One shader, two materials: which objects does each edit reach?')
        cap_label(d, X0, 330, 'IN-ENGINE CAPTURES · windowed', 'tools/a5_capture_side_by_side.gd · '
                                                              'evidence/a5/captures/toybox/edit_checks/')
        for k, im in enumerate(ims):
            x = X0 + k * (1131 + 31)
            paste_framed(c, d, im, x, 420)
            card(d, (x, 900, x + 1131), info[k][0], info[k][1], on=(k == i and k > 0), fsize=46, tsize=50)
        footer(d, 'Crops at 2×; "changed" = a pixel differing by more than 8 levels (edit_checks/README.txt). '
                  'Measurements by Claude; both edits restored.')
        return c
    staged('B08', ['shader', 'material'], img)


# ------------------------------------------------------------------ B10 hint experiment
def b10():
    im, s = fit(Image.open(CAP / 'hint_quads.png').convert('RGB'), 2050, 1153)
    meas = (CAP / 'hint-samples.txt').read_text().splitlines()

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Hint Experiment', 'One 3×1 PNG (64, 128, 192), two quads, two hints (CHANGE-BRIEF A5.4)')
        cap_label(d, X0, 330, 'IN-ENGINE CAPTURE · windowed, Forward+', 'evidence/a5/captures/hint_quads.png')
        paste_framed(c, d, im, X0, 410)
        for nm, yy in (('S · source_color', 194), ('D · data (no hint)', 526)):
            d.text((X0 + 40, 410 + yy * s - 205), nm, font=F(SANSB, 54), fill=(255, 255, 255))
        x = X0 + 2050 + 90
        y = card(d, (x, 410, X1), 'PREDICTED · Tharun, by hand',
                 'S displays  64 · 128 · 192\nD displays  137 · 188 · 225', on=i >= 1, fsize=50, tsize=50)
        y = card(d, (x, y + 40, X1), 'MEASURED · hint-samples.txt',
                 'S displays  64 · 128 · 192\nD displays  137 · 188 · 225\n6 of 6 equal', on=i >= 2, fsize=50, tsize=50)
        d.text((x, y + 50), 'Why S is unchanged: sRGB decode', font=F(SANS, 44), fill=SOFT)
        d.text((x, y + 110), 'on sampling, encode on output.', font=F(SANS, 44), fill=SOFT)
        footer(d, meas[1].split('->')[0].strip() + ' · ' + 'D band 64: encode(64/255) × 255 = 137.2 → 137')
        return c
    staged('B10', ['pred', 'meas'], img)


# ------------------------------------------------------------------ B11 sweep
def b11():
    sheet_im = Image.open(CAP / 'toybox' / 'sweep_contact_sheet.png').convert('RGB')
    im, s = fit(sheet_im, 2600, 1440)
    rows = ['paint_color', 'paint_roughness', 'wear_amount', 'normal_depth', 'uv_scale']

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Interface Sweep')
        cap_label(d, X0, 260, 'IN-ENGINE CAPTURES · windowed', 'tools/a5_capture_toybox.gd · sweep_contact_sheet.png')
        x0, y0 = X1 - im.width, 420
        paste_framed(c, d, im, x0, y0)
        for k, nm in enumerate(('min', 'default', 'max')):
            cx = x0 + (170 + 585 * k + 292) * s
            d.text((cx, 350), nm, font=F(SANSB, 50), fill=INK, anchor='ma')
        for k, nm in enumerate(rows):
            cy = y0 + (45 + 207 * k + 100) * s
            on = i == 1 and nm == 'paint_roughness'
            d.text((X0, cy - 30), nm, font=F(MONO, 50), fill=ACC if on else INK)
        if i == 1:
            ring(d, (165, 45 + 207, 1905, 45 + 2 * 207), s, x0, y0, width=10, pad=4)
        footer(d, 'Left box in each cell: fresh, one uniform at min / default / max. Right box: worn, the control. '
                  'Tharun\'s read (TEST-REPORT A5-7): paint_roughness shows no noticeable difference at this distance, '
                  'linked to M5 (no METALLIC).')
        return c
    staged('B11', ['rough'], img)


# ------------------------------------------------------------------ B12 the language
def b12():
    gen = 'godot/shaders/standard_generated.gdshader'
    pt = 'godot/shaders/painted_tin.gdshader'

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q4 · The Godot Shading Language')
        d.text((X1, 150), 'SOURCE VIEW · not an editor recording', font=F(SANSB, 44), fill=ACC, anchor='ra')
        cw = (X1 - X0 - 80) // 3
        for k, (t, body) in enumerate((
                ('shader_type', 'picks the pipeline: canvas_item (rewind_tint line 1), spatial (painted_tin line 1)'),
                ('hints', 'tell the engine how to feed a uniform: source_color, hint_normal, hint_range'),
                ('built-ins', 'arrive ready: COLOR, UV, ALBEDO, ROUGHNESS, NORMAL_MAP'))):
            x = X0 + k * (cw + 40)
            card(d, (x, 300, x + cw), t, body, fsize=46, tsize=50)
        y = code_box(d, (X0, 700, X1, 0), f'{gen}  ·  Godot-generated, annotated by Tharun (e4c188f)',
                     [(7, src_lines(gen, 7, 7)[0]), (None, '…'), (19, src_lines(gen, 19, 19)[0])],
                     {7, 19} if i >= 1 else set(), size=46,
                     note='line 7: albedo sampled as colour · line 19: normal map sampled as data')
        code_box(d, (X0, y + 50, X1, 0), f'{pt}  ·  the same two jobs',
                 [(3, src_lines(pt, 3, 3)[0]), (4, src_lines(pt, 4, 4)[0])],
                 {3, 4} if i >= 2 else set(), size=46,
                 note='line 3 ↔ generated line 7 · line 4 ↔ generated line 19 (LANGUAGE-NOTES Q6)')
        footer(d, 'LANGUAGE-NOTES.md (Tharun): Part A line numbers; Q1 shader_type, Q3 built-ins, Q4 hints.')
        return c
    staged('B12', ['left', 'right'], img)


# ------------------------------------------------------------------ B13 tests + mutations
def lastline(p, pat):
    return [ln for ln in (REPO / p).read_text().splitlines() if re.search(pat, ln)][-1]


def b13():
    L = REPO / 'logs'
    rows_l = []
    for f in ('test_rewind_tint_30fps', 'test_rewind_tint_60fps', 'test_rewind_tint_144fps',
              'test_materials_60fps', 'test_materials_60fps_fresh_cache', 'test_slice_60fps', 'check_props3d_60fps'):
        rows_l.append((f'logs/{f}.log', TBLUE, False))
        rows_l.append(('  ' + lastline(f'logs/{f}.log', r'checks,|RESULT'), TGREEN, False))
    M = 'evidence/a5/mutations/'
    muts = [('m1 · semicolon deleted, rewind_tint line 3', 'm1-semicolon_test_rewind_tint_60fps.log'),
            ('m2 · rewind_amount -> rewind_amt (lines 3, 8)', 'm2-rename_test_rewind_tint_60fps.log'),
            ('m3 · source_color removed, painted_tin line 3', 'm3-source_color_test_materials_60fps.log')]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What the Tests Proved', 'Recorded output, verbatim · TEST-REPORT "Assignment 5" A5-1 to A5-3')
        terminal(d, (X0, 340, 1880, 1900), 'after A5 · scripts/run-test.sh', rows_l, size=44)
        rows = []
        for t, f in muts:
            txt = (REPO / M / f).read_text().splitlines()
            fails = [ln for ln in txt if ln.startswith('FAIL') or ln.startswith('SHADER ERROR')][:2]
            rows.append((t, TYELLOW, i >= 1))
            rows += [('  ' + ln, TRED, False) for ln in fails]
            rows.append(('  ' + [ln for ln in txt if 'checks,' in ln][-1], TRED, i >= 1))
        rows.append(('', None, False))
        rows.append(('m1, m2: 45 and 48 driver checks still passed;', TTEXT, i >= 2))
        rows.append(('only uniform-list and source checks failed.', TTEXT, i >= 2))
        terminal(d, (1960, 340, X1, 1900), 'mutations · evidence/a5/mutations/', rows, size=40)
        footer(d, 'Tharun made each mutation and restored the shaders each time (SOURCES.md). Exit code = failure count.')
        return c
    staged('B13', ['mut', 'caught'], img)


# ------------------------------------------------------------------ B14 headless limits
def b14():
    hf = (REPO / 'evidence' / 'a5' / 'headless-facts.txt').read_text().splitlines()[:12]
    im, s = fit(Image.open(CAP / 'bolt_rewind_amount_2.0.png').convert('RGB').crop((280, 250, 580, 620)), 900, 1110)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What No Headless Run Shows')
        rows = [(f'{k + 1:>2}  {ln}', None, (k + 1 == 9 and i >= 1) or (k + 1 == 3 and i >= 1)) for k, ln in enumerate(hf)]
        terminal(d, (X0, 300, 2560, 1900), 'evidence/a5/headless-facts.txt · lines 1–12', rows, size=40)
        if i >= 2:
            cap_label(d, 2660, 300, 'WINDOWED CAPTURE', 'rewind_amount 2.0')
            paste_framed(c, d, im, 2660, 380)
            d.text((2660, 380 + im.height + 30), 'Both pixels: (90, 160, 255),', font=F(SANS, 46), fill=INK)
            d.text((2660, 380 + im.height + 92), 'the pure tint.', font=F(SANS, 46), fill=INK)
        footer(d, 'Line 3: reports vulkan / forward_plus, yet a headless run draws nothing. Line 9: a readback stores '
                  'the number and proves nothing about a pixel (CLAUDE.md, headless facts).')
        return c
    staged('B14', ['read', 'win'], img)


# ------------------------------------------------------------------ B15 credits (verbatim SOURCES.md)
def b15():
    txt = (REPO / 'SOURCES.md').read_text()
    sec = txt.split('**Who did what (A5):**', 1)[1].strip().split('\n\n')[0]
    clean = lambda s: s.replace('**', '').replace('`', '')
    me, cl, cur = [], [], None
    for ln in sec.splitlines():
        if ln.startswith('- **Me (Tharun):**'):
            cur = me; continue
        if ln.startswith('- **Claude:**'):
            cur = cl; continue
        if cur is not None and ln.strip().startswith('- '):
            cur.append('• ' + clean(ln.strip()[2:]))

    def col(d, x, x1, title, items, on):
        d.text((x, 330), title, font=F(SANSB, 56), fill=ACC if on else INK)
        y = 420
        f = F(SANS, 44)
        for it in items:
            for k, ln in enumerate(wrap(d, it, f, x1 - x - 40)):
                d.text((x + (0 if k == 0 else 34), y), ln, font=f, fill=INK); y += 56
            y += 14
        assert y < 1960, ('credits overflow', title, y)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Who Did What (A5)')
        d.text((X1, 150), 'SOURCES.md · verbatim', font=F(SANSB, 44), fill=ACC, anchor='ra')
        col(d, X0, 1960, 'Tharun (human)', me, i == 0)
        col(d, 2040, X1, 'Claude (AI)', cl, i == 1)
        footer(d, 'Textures: Poly Haven "Metal Plate" by Rob Tuytel, CC0 (SOURCES.md). Voice: Kokoro am_onyx, AI text-to-speech.')
        return c
    staged('B15', ['claude'], img)


# ------------------------------------------------------------------ source-view code beats (B05, B09)
def code_beat(bid):
    b = beat(bid); p = b['shot']['panel']
    rows = []
    for k, (a, e) in enumerate(p['segments']):
        if k:
            rows.append((None, '…'))
        rows += list(zip(range(a, e + 1), src_lines(p['path'], a, e)))
    cues = p['cues']

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, p['title'])
        d.text((X1, 150), 'SOURCE VIEW · not an editor recording', font=F(SANSB, 44), fill=ACC, anchor='ra')
        act = {cues[i - 1][0]} if i else set()
        lab = f'line {cues[i - 1][0]}: {cues[i - 1][1]}' if i else 'Read the source; the visible result follows.'
        segs = ', '.join(f'{a}–{e}' for a, e in p['segments'])
        code_box(d, (X0, 300, 2640, 0), f"{p['path']}  ·  lines {segs}  ·  2e6946d", rows, act, size=48, note=lab)
        y = 300
        d.text((2720, y), 'Notes · from the brief and SOURCES', font=F(SANSB, 44), fill=ACC)
        y += 84
        for n in p['notes']:
            y = card(d, (2720, y, X1), n['label'], n['value'], fsize=44, tsize=44) + 30
        footer(d, f"Verbatim from {p['path']} at revision 2e6946d.")
        return c
    staged(bid, [str(ln) for ln, _ in cues], img)


MAKERS = {'B05': lambda: code_beat('B05'), 'B09': lambda: code_beat('B09'), 'B02': b02, 'B04': b04, 'B06': b06, 'B07': b07, 'B08': b08, 'B10': b10, 'B11': b11, 'B12': b12,
          'B13': b13, 'B14': b14, 'B15': b15}

if __name__ == '__main__':
    todo = list(MAKERS) if sys.argv[1:] in ([], ['all']) else sys.argv[1:]
    for bid in todo:
        CUR[0] = bid
        MAKERS[bid]()
