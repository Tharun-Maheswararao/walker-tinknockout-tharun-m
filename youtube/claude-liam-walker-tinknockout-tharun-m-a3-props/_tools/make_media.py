#!/usr/bin/env python3
"""Build this film's own media from real files and recorded output only.

Every image placed here is a real repository file (the student's own Blender screenshots, the
MCP look-tool image from the student's live session, Claude-made Godot renders committed in the
repo), the film's Movie Maker orbit capture (capture/orbit-4k.mp4), or recorded command output
(verbatim lines from evidence/ files). This script lays them out, adds provenance labels and
switches highlight states on the spoken cue times written by patch_timing.py. It draws no asset
and invents no output.

Usage: make_media.py all | B02 B03 ...
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


def webp(name):
    return Image.open(EVB / name).convert('RGB')


# ------------------------------------------------------------------ Blender code panel
PY_KW = r'\b(?:import|from|def|for|in|return|if|else|elif|not|None|True|False|is|and|or|lambda|while)\b'
TOK = re.compile(r'("[^"\n]*"|\'[^\'\n]*\'|#[^\n]*|' + PY_KW + r'|\b\d+(?:\.\d+)?\b)')


def draw_code_line(d, x, y, text, font):
    for s in TOK.split(text):
        if not s:
            continue
        col = TTEXT
        if s.startswith('#'):
            col = (186, 197, 188)
        elif s[0] in '"\'':
            col = TYELLOW
        elif re.fullmatch(r'\d+(?:\.\d+)?', s):
            col = TGREEN
        elif re.fullmatch(PY_KW, s):
            col = (243, 155, 206)
        d.text((x, y), s, font=font, fill=col)
        x += d.textlength(s, font=font)


def code_layout(d, src, notes_n):
    """Pick side notes (code pane 192..2720) or bottom notes (full-width pane), whichever reads larger."""
    best = None
    for mode in ('side', 'bottom'):
        px1 = 2720 if mode == 'side' else X1
        py1 = 1840 if mode == 'side' else 1500
        maxw = px1 - X0 - 150 - 60
        avail = (py1 - 110) - (320 + 140)
        for size in range(80, 43, -2):
            fm = F(MONO, size)
            if len(src) * int(size * 1.42) <= avail and all(d.textlength(t, font=fm) <= maxw for t in src):
                break
        if best is None or size > best[1]:
            best = (mode, size, px1, py1)
    return best


def code_panel(b, active, cue_label):
    p = b['shot']['panel']
    c = canvas(); d = ImageDraw.Draw(c)
    header(d, p['title'])
    d.text((X1, 150), 'SOURCE VIEW · not an editor recording', font=F(SANSB, 44), fill=ACC, anchor='ra')
    src = [ln.replace('\t', '    ') for ln in p['code'].split('\n')]
    mode, size, px1, py1 = code_layout(d, src, len(p['notes']))
    fm = F(MONO, size)
    lh = int(size * 1.42)
    px0, py0 = X0, 320
    if mode == 'bottom':                       # shrink the pane to its content
        py1 = py0 + 140 + len(src) * lh + 120
    d.rounded_rectangle((px0, py0, px1, py1), radius=18, fill=TERM)
    d.rectangle((px0, py0 + 18, px1, py0 + 100), fill=(52, 61, 77))
    d.text((px0 + 36, py0 + 32), f"{p['path']}  ·  lines {p['start_line']}–{p['end_line']}", font=F(MONO, 46), fill=TTEXT)
    y = py0 + 140
    for i, text in enumerate(src):
        no = p['start_line'] + i
        if no in active:
            d.rectangle((px0 + 12, y - 8, px1 - 12, y - 8 + lh), fill=TMARK)
            d.rectangle((px0 + 12, y - 8, px0 + 24, y - 8 + lh), fill=TBLUE)
        d.text((px0 + 40, y + (size - 44) // 2), str(no), font=F(MONO, 44), fill=TMUTED)
        draw_code_line(d, px0 + 150, y, text, fm)
        y += lh
    d.rectangle((px0 + 12, py1 - 98, px1 - 12, py1 - 16), fill=(43, 50, 64))
    d.text((px0 + 40, py1 - 82), cue_label or 'Read the source; the visible result follows.', font=F(SANS, 46), fill=TBLUE)
    if mode == 'side':
        nx, ny = 2810, 320
        d.text((nx, ny), 'Notes · from the brief and docs', font=F(SANSB, 44), fill=ACC)
        ny += 84
        for t, v in p['notes']:
            ny = card(d, (nx, ny, X1), t, v, fsize=44, tsize=44) + 30
    else:
        ny = py1 + 50
        n = len(p['notes'])
        cw = (X1 - X0 - 40 * (n - 1)) // n
        for k, (t, v) in enumerate(p['notes']):
            x = X0 + k * (cw + 40)
            card(d, (x, ny, x + cw), t, v, fsize=54, tsize=54)
    footer(d, p['caption'])
    return c


def make_code(bid):
    b = beat(bid)
    cues = b['shot']['panel']['cues']
    st = [(0.0, code_panel(b, set(), None))]
    for ln, lab in cues:
        st.append((ct(b, ln), code_panel(b, {ln}, f'line {ln}: {lab}')))
    if st[1][0] < 0.4:
        st = [(0.0, st[1][1])] + st[2:]
    states_video(bid, st, nframes(b))


# ------------------------------------------------------------------ B02 assets
def b02():
    render, s = fit(Image.open(EVG / 'prop_room.png').convert('RGB'), 2200, 1238)
    info = [('castle', 'environment', '1.80 × 0.82 × 2.30 m',
             'Sunken-castle ornament on the bowl floor: the landmark behind the fighters that says "goldfish bowl". '
             '2.30 m = 1.28 × Bolt.'),
            ('windkey', 'collectible', '0.60 × 0.14 × 0.70 m',
             "A spare brass winding key that would refill Bolt's spring (a future mechanic). Same size as the key on his back."),
            ('toybox', 'weapon-pickup prop', '1.26 × 0.76 × 0.75 m',
             "The tin toy box that weapon pickups would come out of. Lid at 0.75 m: Bolt's waist.")]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Three Props, Each With a Job',
               'CONCEPT.md: tin wind-up toys fight in an empty goldfish bowl · CHANGE-BRIEF.md "Assignment 3", A3.1–A3.2')
        label(d, (X0, 350), 'Real engine render', 'evidence/godot/prop_room.png · Godot 4.7.2 · Claude-made (shot_prop_room.gd)')
        paste_framed(c, d, render, X0, 430)
        yb = 430 + render.height + 40
        on = i >= 1
        d.text((X0, yb), 'Character scale: Bolt = 1.80 m · 1 Blender unit = 1 m = 1 Godot unit',
               font=F(SANSB if on else SANS, 52), fill=ACC if on else INK)
        y = 350
        for k, (name, job, size, why) in enumerate(info):
            if i >= k + 2:
                y = card(d, (2520, y, X1), f'{name} · {job} · {size}', why, on=(i == k + 2), fsize=44, tsize=44) + 34
        footer(d, 'Sizes, jobs and reasons: CHANGE-BRIEF.md A3.2 (committed as 3ef263b before any building)')
        return c
    staged('B02', ['bolt', 'castle', 'windkey', 'toybox'], img)


# ------------------------------------------------------------------ B03 brief
def b03():
    log = subprocess.run(['git', '-C', str(REPO), 'log', '--reverse', '--format=%h %s', '9788922..1d93dcb'],
                         capture_output=True, text=True, check=True).stdout.strip().splitlines()
    rules = [('Size', 'matches the brief within ±0.01 m, in Blender and Godot'),
             ('Base', 'lowest point at height 0 (±0.005 m); origin at the centre of the underside'),
             ('Budgets', 'castle ≤ 200 · windkey ≤ 250 · toybox ≤ 100 triangles'),
             ('Front', 'faces Blender −Y → arrives as Godot +Z (glTF +Y Up)')]
    fails = ['F1 wrong size by ×2 (or ×10)', 'F2 lying on its side or facing backwards', 'F3 floats or sinks',
             'F4 unapplied scale or rotation', 'F5 Claude builds more than asked', 'F6 a colour does not survive export',
             'F7 the MCP route breaks mid-build']

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Brief Came First', 'git log --reverse 9788922..1d93dcb (the A3 commits, oldest first) · brief: bottom of CHANGE-BRIEF.md')
        rows = [(ln[:72] + ('…' if len(ln) > 72 else ''), TYELLOW if ln.startswith(('3ef263b', 'bec93b5')) else None,
                 i >= 1 and ln.startswith('3ef263b')) for ln in log]
        terminal(d, (X0, 340, 2280, 1130), '$ git log --reverse --format="%h %s" 9788922..1d93dcb', rows, size=38)
        y = 1170
        if i >= 1:
            d.text((X0, y), '3ef263b (the A3 brief) is committed before bec93b5, the first build commit.', font=F(SANSB, 46), fill=ACC)
            y += 74
        if i >= 2:
            y = text_block(d, (X0, y), 'Authorship (brief header): Tharun chose the assets, the scale and the dropped cork. '
                           'Claude drafted numbers, colours and failure cases. Changes Tharun made to the draft: none.',
                           F(SANS, 44), 2090) + 20
        if i >= 3:
            d.text((X0, y), 'A3.1 ground rules the checks test later', font=F(SANSB, 46), fill=ACC); y += 72
            for k, v in rules:
                d.text((X0, y), k, font=F(SANSB, 44), fill=INK)
                d.text((X0 + 230, y), v, font=F(SANS, 44), fill=INK); y += 62
        if i >= 4:
            fx, yy = 2400, 340
            d.text((fx, yy), 'A3.3 predicted failures', font=F(SANSB, 48), fill=ACC); yy += 86
            for f in fails:
                yy = card(d, (fx, yy, X1), f[:2], f[3:], fsize=44, tsize=44) + 16
        footer(d, 'Sources: the repository git log · CHANGE-BRIEF.md "Assignment 3" A3.1 and A3.3')
        return c
    staged('B03', ['log', 'author', 'rules', 'fails'], img)


# ------------------------------------------------------------------ B04 setup
def b04():
    shot = webp('01-mcp-connected-port-9876.webp')
    im, s = fit(shot, 1700, 1105)
    items = [('1  Register the MCP server', 'claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender',
              'Invalid environment variable format: blender', 'Fix: name first: claude mcp add blender -e DISABLE_TELEMETRY=true -- …'),
             ('2  Install the add-on', 'uvx mcp-for-blender install-addon', 'Could not find a Blender user addons directory.',
              'Fix: open Blender once, then retry'),
             ('3  Enable it', 'Preferences → Interface: MCP for Blender',
              "Add-on not loaded: \"blender_mcp\", cause: No module named 'blender_mcp'", 'Fix: quit Blender completely and reopen')]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Setup: Three Fixes, Then a Retry', 'FRICTIONAL.md, Assignment 3 · 2026-10-14 and the castle session · error text quoted from the log')
        label(d, (X0, 340), "Student's own screenshot", '01-mcp-connected-port-9876.webp · Oct 14, 9:54 PM')
        paste_framed(c, d, im, X0, 420)
        if i >= 4:
            ring(d, (1294, 240, 1592, 272), s, X0, 420)
            z = shot.crop((1284, 196, 1604, 304)).resize((1120, 378), Image.LANCZOS)
            put(c, z, (X0, 1580)); d.rectangle((X0, 1580, X0 + 1120, 1958), outline=RING, width=6)
            text_block(d, (X0 + 1170, 1590), 'zoom of the same screenshot. Claude checked with lsof: '
                       'Blender listens on 127.0.0.1:9876 only.', F(SANS, 44), 520)
        x, y = 2000, 340
        fm = F(MONO, 42)
        for k, (t, cmd, err, fix) in enumerate(items[:min(i, 3)]):
            on = i == k + 1
            d.text((x, y), t, font=F(SANSB, 50), fill=ACC if on else INK); y += 70
            for ln in wrap(d, cmd, fm, X1 - x):
                d.text((x, y), ln, font=fm, fill=SOFT); y += 56
            for ln in wrap(d, err, fm, X1 - x - 30):
                d.rectangle((x, y - 6, X1, y + 52), fill=(246, 232, 226)); d.text((x + 14, y), ln, font=fm, fill=(122, 40, 30)); y += 58
            for ln in wrap(d, fix, F(SANS, 44), X1 - x):
                d.text((x, y), ln, font=F(SANS, 44), fill=INK); y += 58
            y += 26
        if i >= 5:
            d.text((x, y), '4  First get_scene_info (castle session, 21:40)', font=F(SANSB, 50), fill=ACC); y += 70
            d.rectangle((x, y - 6, X1, y + 52), fill=(246, 232, 226))
            d.text((x + 14, y), 'Could not connect to Blender. Make sure the …', font=fm, fill=(122, 40, 30)); y += 64
            d.text((x, y), 'Retried about 4 minutes later (21:45): it worked.', font=F(SANS, 44), fill=INK)
        footer(d, 'Versions: Blender 5.2.2 LTS · mcp-for-blender 2.1.9 · add-on 1.8 · Claude Code 2.1.295 (SOURCES.md "Assignment 3")')
        return c
    staged('B04', ['f1', 'f2', 'f3', 'shot', 'retry'], img)


# ------------------------------------------------------------------ B05 window
def b05():
    shot = webp('02-interface.webp')
    im, s = fit(shot, 2350, 1527)
    scale_box, dims_box = (1292, 510, 1592, 588), (1292, 618, 1592, 696)
    crop = shot.crop((1284, 450, 1604, 705))
    zs = 1000 / crop.width
    zoom = crop.resize((1000, round(crop.height * zs)), Image.LANCZOS)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Learning the Window: the 2 m Cube', 'BLENDER-NOTES.md §5 Sidebar (N) · FRICTIONAL.md 2026-10-14 ~22:50')
        label(d, (X0, 330), "Student's own screenshot", '02-interface.webp · Oct 14, 10:47 PM')
        paste_framed(c, d, im, X0, 410)
        zx = 2648
        if i >= 1:
            bx = scale_box if i == 1 else dims_box
            ring(d, bx, s, X0, 410)
            put(c, zoom, (zx, 410)); d.rectangle((zx, 410, zx + zoom.width, 410 + zoom.height), outline=INK, width=3)
            ring(d, (bx[0] - 1284, bx[1] - 450, bx[2] - 1284, bx[3] - 450), zs, zx, 410, pad=4)
            y = 410 + zoom.height + 50
            d.text((zx, y), 'Scale 1.000', font=F(SERIF, 80), fill=ACC if i == 1 else INK); y += 110
            if i >= 2:
                d.text((zx, y), 'Dimensions 2 m', font=F(SERIF, 80), fill=ACC); y += 130
            if i >= 3:
                text_block(d, (zx, y), 'Predicted failure A3-F1: wrong size by a factor of 2. "Scale 1" does not mean "1 metre".',
                           F(SANS, 46), X1 - zx)
        footer(d, 'Claude pointed out the 2 m default in this session; it became A3-F1 in CHANGE-BRIEF A3.3')
        return c
    staged('B05', ['scale', 'dims', 'f1'], img)


# ------------------------------------------------------------------ B06 prompt
def b06():
    text = (REEL / 'evidence' / 'castle-prompt.txt').read_text().rstrip('\n').split('\n')
    groups = {1: [2, 3], 2: [7, 8], 3: [9, 10, 11, 12, 13], 4: [13, 16, 17], 5: [18]}

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Prompt Tharun Pasted', 'Real, verbatim · castle build session, 2026-10-15 21:40 EDT · line breaks as pasted')
        x0, y0, x1, y1 = X0, 340, X1, 1900
        d.rounded_rectangle((x0, y0, x1, y1), radius=28, fill=CARD, outline=(229, 226, 217), width=3)
        fm = F(MONO, 54)
        lh = 82
        y = y0 + 50
        hl = groups.get(i, [])
        for k, ln in enumerate(text, start=1):
            if k in hl:
                d.rectangle((x0 + 30, y - 10, x1 - 30, y - 10 + lh), fill=(248, 232, 222))
                d.rectangle((x0 + 30, y - 10, x0 + 44, y - 10 + lh), fill=RING)
            d.text((x0 + 80, y), ln, font=fm, fill=INK)
            y += lh
        assert y <= y1, y
        footer(d, 'Source: Tharun\'s message in the "Castle asset build (Assignment 3)" Claude Code session transcript; '
                  'copied verbatim to evidence/castle-prompt.txt in this reel')
        return c
    staged('B06', ['brief', 'propose', 'calls', 'end', 'verify'], img)


# ------------------------------------------------------------------ B08 look
def b08():
    look = Image.open(EVB / '03-castle-mcp-look.png').convert('RGB')
    im, s = fit(look, 1560, 1560)
    calls = [('keep', 'pink keep · call 1', (120, 160, 265, 330)),
             ('towers', 'two 12-sided towers · calls 2–3 · teal cone roofs · calls 4–5', (90, 60, 295, 330)),
             ('door', 'dark door on the front · call 6', (165, 240, 218, 330))]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Result: What the Look Tool Saw')
        label(d, (X0, 280), "Blender MCP look tool, student's live session", 'evidence/blender/03-castle-mcp-look.png')
        paste_framed(c, d, im, X0, 370)
        if 1 <= i <= 3:
            ring(d, calls[i - 1][2], s, X0, 370)
        x, y = 1900, 370
        for k, (_, t, _) in enumerate(calls):
            if i >= k + 1:
                d.text((x, y), t, font=F(SANSB if i == k + 1 else SANS, 50), fill=ACC if i == k + 1 else INK); y += 92
        if i >= 4:
            y += 40
            d.text((x, y), 'Reported in the session (FRICTIONAL.md)', font=F(SANSB, 46), fill=ACC); y += 80
            d.text((x, y), '1.80 × 0.82 × 2.30 m', font=F(SERIF, 104), fill=INK); y += 150
            d.text((x, y), '156 triangles  ≤  budget 200', font=F(SERIF, 88), fill=INK); y += 140
            text_block(d, (x, y), 'Views: front, side, top and an angle, as the look tool returned them. '
                       'Each part\'s get_scene_info showed rotation 0 and scale 1.', F(SANS, 44), X1 - x)
        footer(d, 'Code: tools/blender/build_castle.py calls 0–7 (1d93dcb) · ran via mcp-for-blender 2.1.9 in Blender 5.2.2, 2026-10-15 21:45–21:46')
        return c
    staged('B08', ['keep', 'towers', 'door', 'numbers'], img)


# ------------------------------------------------------------------ sidebar results (B10, B12, B14)
def sidebar_result(bid, file, when, title, rings, side, keys, foot, crops):
    shot = webp(file)
    im, s = fit(shot, 1900, 1234)
    ZX, ZW = 2140, 620
    zooms, zy = [], 370
    for cb in crops:
        cr = shot.crop(cb)
        zs = ZW / cr.width
        zooms.append((cb, cr.resize((ZW, round(cr.height * zs)), Image.LANCZOS), zs, zy))
        zy += round(cr.height * zs) + 60

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, title)
        label(d, (X0, 280), "Student's own screenshot", f'evidence/blender/{file} · {when}')
        paste_framed(c, d, im, X0, 370)
        for cb, z, zs, y in zooms:
            paste_framed(c, d, z, ZX, y)
            d.rectangle((X0 + int(cb[0] * s), 370 + int(cb[1] * s), X0 + int(cb[2] * s), 370 + int(cb[3] * s)), outline=SOFT, width=3)
        d.text((ZX, zooms[-1][3] + zooms[-1][1].height + 14), 'zoom, same screenshot', font=F(SANS, 44), fill=SOFT)
        for bx in (rings[i - 1] if i >= 1 else []):
            ring(d, bx, s, X0, 370)
            for cb, z, zs, y in zooms:
                if bx[0] >= cb[0] and bx[2] <= cb[2] and bx[1] >= cb[1] and bx[3] <= cb[3]:
                    ring(d, (bx[0] - cb[0], bx[1] - cb[1], bx[2] - cb[0], bx[3] - cb[1]), zs, ZX, y, pad=4)
        x, y = 2840, 370
        for k, (t, body) in enumerate(side):
            if i >= k + 1:
                y = card(d, (x, y, X1), t, body, on=(i == k + 1), fsize=46, tsize=48) + 30
        footer(d, foot)
        return c
    staged(bid, keys, img)


def b10():
    sidebar_result('B10', '07-castle-sidebar.webp', 'commit fd99467', "Result: the Castle in Tharun's Blender",
                   [[(1290, 225, 1592, 302), (1290, 335, 1592, 410), (1290, 472, 1592, 550)],
                    [(1290, 580, 1592, 658)], [(870, 440, 926, 490)], []],
                   [('Transform', 'location 0 · rotation 0°\nscale 1.000'), ('Dimensions', '1.8 × 0.82 × 2.3 m\n= the brief'),
                    ('Origin', 'at the base centre,\nthe world origin (call 7)'),
                    ('Not in this shot', 'Statistics overlay off: the\n156 tris come from the\nscript and get_scene_info')],
                   ['xform', 'dims', 'origin', 'stats'],
                   'MCP-built castle (tools/blender/build_castle.py) · screenshot added in docs-only commit fd99467 · Solid view',
                   [(1284, 160, 1600, 665)])


def b12():
    sidebar_result('B12', '06-windkey-sidebar.webp', 'commit 0bc2b4d', "Result: the Key in Tharun's Blender",
                   [[(1290, 335, 1592, 410), (1290, 472, 1592, 550), (1290, 580, 1592, 658)],
                    [(85, 318, 240, 340)], [], []],
                   [('Transform', 'rotation 0° · scale 1.000\n0.6 × 0.14 × 0.7 m'), ('Statistics', 'Triangles 192 / 192\n(budget 250)'),
                    ('Auto mode denied call 0', 'it deletes every object and saves over\nwindkey.blend; Tharun approved it\n(FRICTIONAL.md, 16:09)'),
                    ('Same numbers', 'the superseded script-route key\n(build_windkey_script_route.py)\ngave identical numbers')],
                   ['xform', 'tris', 'denied', 'same'],
                   'MCP-built windkey (tools/blender/build_windkey.py, 2026-10-16 session) · screenshot added in docs-only commit 0bc2b4d · Material Preview',
                   [(1284, 300, 1600, 665), (80, 220, 250, 345)])


def b14():
    sidebar_result('B14', '04-toybox-before.webp', 'Oct 15, 11:46 PM', "Result: the Box in Tharun's Blender",
                   [[(700, 545, 942, 575)], [(1810, 585, 1925, 660), (1810, 700, 1925, 780)], [(1500, 125, 1605, 153)]],
                   [('Band', 'navy #23395B, from line 12'), ('Transform', 'rotation 0° · scale 1.000'),
                    ('Viewport shading', 'Solid (the second sphere)')],
                   ['band', 'xform', 'solid'],
                   'Script-route toybox.blend, before the hand edit · the band slot is named toybox_navy',
                   [(660, 440, 980, 650), (1700, 570, 1990, 790), (1490, 120, 1630, 160)])


# ------------------------------------------------------------------ B15 hand edit
def b15():
    a, b5 = webp('04-toybox-before.webp'), webp('05-toybox-after.webp')
    ia, sa = fit(a, 1690, 1098)
    ib, sb = fit(b5, 1690, 1098)
    check = next(l.strip() for l in (RUNS / 'check_props3d-isolated-1d93dcb.txt').read_text().splitlines() if 'toybox_navy' in l)
    xa, xb, yy = X0, X1 - 1690, 420

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Hand Edit: Navy to Green', "Tharun's edit, in Blender's window · FRICTIONAL.md 2026-10-16 00:05–00:25 · TEST-REPORT A3-9")
        label(d, (xa, 340), "Student's own screenshot", '04 · before · Oct 15, 11:46 PM')
        label(d, (xb, 340), "Student's own screenshot", '05 · after · Oct 16, 12:11 AM')
        paste_framed(c, d, ia, xa, yy)
        paste_framed(c, d, ib, xb, yy)
        y = yy + 1098 + 40
        notes = []
        if i >= 1:
            ring(d, (1500, 125, 1605, 153), sb, xb, yy)
            ring(d, (1150, 200, 1255, 310), sb, xb, yy, width=5)
            notes.append(('Viewport: Material Preview', 'after first mistaking the X/Y/Z gizmo (thin ring) for the shading buttons'))
        if i >= 2:
            ring(d, (1703, 473, 1942, 497), sb, xb, yy)
            ring(d, (1700, 745, 1950, 770), sb, xb, yy)
            notes.append(('Material tab', 'slot toybox_navy · Base Color #23395B → #2E7D32'))
        if i >= 3:
            ring(d, (1290, 620, 1592, 696), sb, xb, yy)
            ring(d, (1290, 510, 1592, 588), sb, xb, yy, width=5)
            notes.append(('Unchanged', '1.26 × 0.76 × 0.75 m · scale 1.000'))
        for t, v in notes:
            d.text((X0, y), t, font=F(SANSB, 48), fill=ACC)
            d.text((X0 + 900, y), v, font=F(SANS, 46), fill=INK); y += 76
        if i >= 4:
            d.rounded_rectangle((X0, y + 10, 2600, y + 120), radius=12, fill=TERM)
            d.text((X0 + 36, y + 36), check, font=F(MONO, 48), fill=TGREEN)
            d.text((2650, y + 40), 're-exported · commit 08f96cd · headless', font=F(SANS, 44), fill=SOFT)
        footer(d, 'Saved at 00:11; Claude re-checked the saved .blend headless (size, origin, scale, 48 tris unchanged) and re-exported the .glb')
        return c
    staged('B15', ['shade', 'mat', 'size', 'check'], img)


# ------------------------------------------------------------------ B16 lesson
def b16():
    quote = ('Editing the hand taught me that Blender’s interface relies on coordinating specific Properties tabs, '
             'color pickers, and viewport shading modes just to see surface changes take effect in real time.')
    src = (REPO / 'BLENDER-NOTES.md').read_text()
    assert quote in src, 'quote not verbatim in BLENDER-NOTES.md'
    check = next(l.strip() for l in (RUNS / 'check_props3d-isolated-1d93dcb.txt').read_text().splitlines() if 'toybox_navy' in l)
    code = (REPO / 'tools/blender/build_toybox.py').read_text().splitlines()

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What the Edit Taught, and Left Behind')
        d.text((X0, 300), "Tharun's own words", font=F(SANSB, 50), fill=ACC)
        d.text((X0 + 470, 304), 'BLENDER-NOTES.md · docs-only commit 0bc2b4d', font=F(SANS, 44), fill=SOFT)
        d.rectangle((X0, 390, X0 + 14, 920), fill=ACC)
        y = text_block(d, (X0 + 70, 390), '“' + quote + '”', F(SERIF_I, 106), 3300, fill=INK, lh=134)
        d.text((X0 + 70, y + 20), '— Tharun Maheswararao', font=F(SERIF, 72), fill=SOFT)
        y = 1250
        if i >= 1:
            d.text((X0, y), "Two loose ends — Claude's observations, not Tharun's", font=F(SANSB, 50), fill=ACC)
        y += 90
        if i >= 2:
            d.text((X0, y), 'The slot name still says navy, though the colour is green:', font=F(SANS, 46), fill=INK)
            terminal(d, (X0, y + 64, X1, y + 230), 'check_props3d.gd output (headless, 1d93dcb)', [(check, TGREEN, i == 2)], size=44)
        y += 270
        if i >= 3:
            d.text((X0, y), 'The build script still says navy, so re-running it would save navy back over the edit:',
                   font=F(SANS, 46), fill=INK)
            rows = [(f'12  {code[11]}', TYELLOW, True), (f'17  {code[16]}', None, False)]
            terminal(d, (X0, y + 64, X1, y + 300), 'tools/blender/build_toybox.py (1d93dcb)', rows, size=44)
        footer(d, 'The green lives in assets/blender/toybox.blend and godot/assets/props3d/toybox.glb (08f96cd), not in the build script')
        return c
    staged('B16', ['loose', 'slot', 'script'], img)


# ------------------------------------------------------------------ B18 orbit capture
IW, IH, IX, IY = 2944, 1656, 448, 250


def b18():
    b = beat('B18')
    n = nframes(b)
    ov = Image.new('RGBA', (W, H), PAGE + (255,))
    d = ImageDraw.Draw(ov)
    d.rectangle([IX, IY, IX + IW - 1, IY + IH - 1], fill=(0, 0, 0, 0))
    d.text((IX, 180), 'REAL ENGINE · Godot 4.7.2 Movie Maker, native 3840×2160 · prop_room.tscn unchanged · isolated copy of 1d93dcb',
           font=F(SANS, 46), fill=INK, anchor='lm')
    d.text((IX, 1972), "0–4 s: the scene's saved Camera3D · then a film script orbits that camera · not Tharun's look check",
           font=F(SANS, 46), fill=SOFT, anchor='lm')
    d.text((X1, 2040), '@NikBearBrown', font=F(SERIF, 56), fill=INK, anchor='rd')
    WORK.mkdir(parents=True, exist_ok=True)
    ovp = WORK / 'B18-overlay.png'
    ov.save(ovp)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(REEL / 'capture/orbit-4k.mp4'), '-i', str(ovp),
                    '-filter_complex', f'[0:v]scale={IW}:{IH}:flags=lanczos,pad={W}:{H}:{IX}:{IY}:color=0xFAF9F5[g];[g][1:v]overlay=0:0,format=yuv420p[v]',
                    '-map', '[v]', '-frames:v', str(n), '-r', str(FPS), '-c:v', 'libx264', '-preset', 'medium',
                    '-crf', '14', '-an', str(REEL / 'media/B18.mp4')], check=True)
    sh = sheet()
    for bb in sh['beats']:
        if bb['beat_id'] == 'B18':
            bb['shot']['capture_window_s'] = [0.0, round(n / FPS, 3)]
    (REEL / 'beat_sheet.json').write_text(json.dumps(sh, indent=1, ensure_ascii=False) + '\n')
    print('wrote media/B18.mp4', n, 'frames (first', n, 'of 840 capture frames, no retiming)')


# ------------------------------------------------------------------ B20 headless
def b20():
    out = (RUNS / 'check_props3d-isolated-1d93dcb.txt').read_text()
    blocks = {m.group(1): m.group(2) for m in re.finditer(r'== (\w+)  \(res[^\n]*\n(.*?)(?=\n== |\Z)', out, re.S)}
    room = dict((m[0], m[1]) for m in re.findall(r'PASS  (\w+) sits on the floor in the room \(world min_y [\d.\-]+, world x ([^)]*)\)', out))
    brief = {'castle': ('1.80 × 0.82 × 2.30', 200), 'windkey': ('0.60 × 0.14 × 0.70', 250), 'toybox': ('1.26 × 0.76 × 0.75', 100)}
    band = next(l.strip() for l in out.splitlines() if 'toybox_navy' in l)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Result: Headless Numbers Beside the Brief')
        d.text((X0, 262), 'HEADLESS', font=F(SANSB, 46), fill=ACC)
        d.text((X0 + 260, 264), 'timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60',
               font=F(MONO, 42), fill=SOFT)
        d.text((X0, 330), 'isolated copy of 1d93dcb (git archive) · Godot 4.7.2 · output identical to the recorded evidence/check_props3d.txt',
               font=F(SANS, 42), fill=SOFT)
        cols = [X0, 700, 1500, 2500, 2960]
        heads = ['asset', 'brief W × D × H (m)', 'Godot AABB X × Y × Z', 'min_y', 'tris ≤ budget']
        y = 450
        for k, (x, h) in enumerate(zip(cols, heads)):
            d.text((x, y), h, font=F(SANSB, 48), fill=ACC if (i == 2 and k == 2) else SOFT)
        y += 84
        d.line((X0, y - 12, X1, y - 12), fill=RULE, width=3)
        for name in ('castle', 'windkey', 'toybox'):
            blk = blocks[name]
            aabb = re.search(r'aabb size=\(([^)]*)\)\s+min_y=([\d.\-]+)', blk)
            tris = re.search(r'triangles (\d+) <= budget (\d+)', blk)
            vals = [name, brief[name][0], aabb.group(1).replace(', ', ' × '), aabb.group(2), f'{tris.group(1)} ≤ {tris.group(2)}']
            for k, (x, v) in enumerate(zip(cols, vals)):
                d.text((x, y), v, font=F(SERIF, 78) if k == 0 else F(MONO, 60), fill=ACC if (i == 2 and k == 2) else INK)
            y += 124
        d.text((X0, y), "Godot is Y-up: its middle number is the height (the brief's last number).", font=F(SANS, 46),
               fill=ACC if i == 2 else INK)
        y += 96
        rows = [(f'{n:8s} world x {room[n]}   world min_y 0.0000', None, i == 3) for n in ('castle', 'windkey', 'toybox')]
        y = terminal(d, (X0, y, 2300, y + 330), 'in prop_room.tscn (same run)', rows, size=46) + 40
        terminal(d, (X0, y, 2300, y + 200), 'albedo, surface 2', [(band, TGREEN, i == 4)], size=46)
        if i >= 1:
            d.rounded_rectangle((2420, 1340, X1, 1560), radius=16, fill=TERM)
            d.text((2470, 1400), 'RESULT: PASS (0 failing)', font=F(MONO, 76), fill=TGREEN)
            text_block(d, (2420, 1600), 'Also printed: scale (1,1,1) and rotation 0, tallest axis Y, door and latch at +Z, '
                       'every albedo hex.', F(SANS, 44), X1 - 2420)
        footer(d, 'Full output: evidence/runs/check_props3d-isolated-1d93dcb.txt (this film) · evidence/check_props3d.txt (repo)')
        return c
    staged('B20', ['pass', 'yup', 'room', 'band'], img)


# ------------------------------------------------------------------ B22 repro
def b22():
    rg = (RUNS / 'repro-global_transform.txt').read_text().splitlines()
    i0 = rg.index('== prop_room.tscn')
    left = rg[i0:i0 + 2] + ['   … (backtrace: world_aabb, check_props3d.gd:46)'] + \
        [l for l in rg[i0:] if 'castle sits' in l] + ['  … (the same ERROR, then PASS, for windkey and toybox)'] + \
        [l for l in rg if l.startswith(('RESULT', 'exit'))]
    fixed = next(l for l in (RUNS / 'check_props3d-isolated-1d93dcb.txt').read_text().splitlines() if 'castle sits on the floor' in l)
    rp = [l for l in (RUNS / 'repro-parse-error.txt').read_text().splitlines() if l.strip() and not l.startswith('Godot Engine')]

    def col(l):
        return TYELLOW if l.lstrip().startswith(('ERROR', 'SCRIPT ERROR')) else (TGREEN if 'PASS' in l else None)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Result: a Pass That Tested Nothing')
        d.text((X0, 268), 'RE-CREATION FOR THIS FILM, on throwaway copies of 1d93dcb · not the original runs',
               font=F(SANSB, 46), fill=ACC)
        rows = [(l, col(l), (i == 1 and 'ERROR' in l) or (i == 2 and 'castle sits' in l)) for l in left]
        y = terminal(d, (X0, 360, 2080, 1500), 'line 46 swapped back to mi.global_transform', rows, size=40)
        if i >= 2:
            terminal(d, (X0, 1540, 2080, 1860), 'the fixed check (to_root), same castle line', [(fixed, TGREEN, True)], size=40)
        if i >= 3:
            terminal(d, (2160, 360, X1, 1200), 'line 10 given a syntax error', [(l, col(l), False) for l in rp[:-1]] +
                     [('', None, False), ('(no RESULT line)', TMUTED, False), (rp[-1], TRED, True)], size=40)
            text_block(d, (2160, 1260), 'Godot exits 0 even when the check script does not parse. Read the RESULT line, '
                       'not the exit code (TEST-REPORT A3-6).', F(SANS, 48), X1 - 2160)
        footer(d, 'Outputs: evidence/runs/repro-global_transform.txt and repro-parse-error.txt · "exit N" lines appended by the film\'s shell')
        return c
    staged('B22', ['errors', 'castle', 'parse'], img)


# ------------------------------------------------------------------ B23 two more
def b23():
    code = (REPO / 'godot/tools/shot_prop_views.gd').read_text().splitlines()

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Two More Mistakes', 'From TEST-REPORT.md A3-7 and FRICTIONAL.md (castle session, from the transcript)')
        x0, x1, y = X0, 1860, 400
        if i >= 1:
            d.text((x0, y), '1 · The render script', font=F(SANSB, 56), fill=ACC if i == 1 else INK)
            y2 = text_block(d, (x0, y + 100), 'Same "Node not inside tree" mistake as the check: look_at ran before the room '
                            'was in the tree, so the first view used the wrong camera. Fixed and re-rendered with no errors.',
                            F(SANS, 48), x1 - x0)
            terminal(d, (x0, y2 + 40, x1, y2 + 420), 'godot/tools/shot_prop_views.gd (1d93dcb)',
                     [(f'{n}  {code[n - 1].strip()}', None, n in (21, 23)) for n in (21, 22, 23)], size=40)
        if i >= 2:
            x0, x1 = 1980, X1
            d.text((x0, y), '2 · The proposal nobody saw', font=F(SANSB, 56), fill=ACC)
            y2 = text_block(d, (x0, y + 100), "The prompt said: propose the steps, do not build yet. Claude's proposal never "
                            'appeared in the chat; the build session admitted it later.', F(SANS, 48), x1 - x0) + 40
            d.text((x0, y2), "Tharun's reply, quoted in FRICTIONAL.md:", font=F(SANS, 46), fill=SOFT)
            text_block(d, (x0 + 30, y2 + 80), '“Approved. Build the castle as proposed … Don\'t save or export.”',
                       F(SERIF_I, 70), x1 - x0 - 30, lh=92)
            text_block(d, (x0, y2 + 330), 'The 8 calls did follow the brief (21:45–21:46).', F(SANS, 46), x1 - x0)
        footer(d, 'Both recorded by Claude in the repository docs; nothing here is reconstructed')
        return c
    staged('B23', ['render', 'proposal'], img)


# ------------------------------------------------------------------ B24 look check
def b24():
    views = ['front_wide', 'behind_wide', 'below_wide', 'castle_close', 'windkey_close', 'toybox_close']
    ims = [Image.open(EVG / 'views' / f'{v}.png').convert('RGB').resize((800, 450), Image.LANCZOS) for v in views]
    gx, gy = 1180, 430

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, "The Look: Tharun's Check, Claude's Renders")
        d.text((X0, 300), "Tharun's look check", font=F(SANSB, 50), fill=ACC)
        y = text_block(d, (X0, 380), 'Opened prop_room.tscn in the Godot editor, orbited the props, ran it with F6.',
                       F(SANS, 46), 880)
        y = text_block(d, (X0, y + 30), '“everything works fine”', F(SERIF_I, 84), 900, lh=100)
        y = text_block(d, (X0, y + 20), 'TEST-REPORT A3-7. He took no screenshot.', F(SANS, 46), 880, fill=SOFT if i < 1 else ACC)
        label(d, (gx, 300), 'Claude-made engine renders', 'not the student\'s · godot/tools/shot_prop_views.gd → evidence/godot/views/')
        for k, (v, im) in enumerate(zip(views, ims)):
            x, yy = gx + (k % 3) * 830, gy + (k // 3) * 540
            put(c, im, (x, yy)); d.rectangle((x - 2, yy - 2, x + 801, yy + 451), outline=RULE, width=3)
            d.text((x, yy + 462), v.replace('_', ' '), font=F(SANS, 44), fill=SOFT)
        s = 800 / 1280
        if i >= 2:
            ring(d, (480, 262, 790, 345), s, gx + 2 * 830, gy + 540)
        if i >= 3:
            ring(d, (600, 365, 680, 440), s, gx, gy)
        y = 1560
        if i >= 2:
            d.text((gx, y), "Claude's observations", font=F(SANSB, 48), fill=ACC); y += 76
            d.text((gx, y), 'the cream lid (#E8DCC0) reads near-white under this light', font=F(SANS, 46), fill=INK); y += 66
        if i >= 3:
            d.text((gx, y), "the key is small beside the castle: right for the brief's sizes;", font=F(SANS, 46), fill=INK); y += 66
            d.text((gx, y), 'whether it reads at game size is untested', font=F(SANS, 46), fill=INK)
        footer(d, 'Source: TEST-REPORT.md A3-7 · the six renders are 1280×720 engine output committed in 1ab2086')
        return c
    staged('B24', ['noshot', 'lid', 'key'], img)


MAKERS = {'B02': b02, 'B03': b03, 'B04': b04, 'B05': b05, 'B06': b06, 'B07': lambda: make_code('B07'), 'B08': b08,
          'B09': lambda: make_code('B09'), 'B10': b10, 'B11': lambda: make_code('B11'), 'B12': b12,
          'B13': lambda: make_code('B13'), 'B14': b14, 'B15': b15, 'B16': b16, 'B18': b18, 'B20': b20, 'B22': b22,
          'B23': b23, 'B24': b24}

if __name__ == '__main__':
    want = sys.argv[1:] or ['all']
    for bid, fn in MAKERS.items():
        if 'all' in want or bid in want:
            fn()
