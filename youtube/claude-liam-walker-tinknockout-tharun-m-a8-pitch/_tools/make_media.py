#!/usr/bin/env python3
"""Build the A8 pitch film's own media (every beat except the two GodotDevWorkbench code views).

Three kinds of picture, each labelled on screen:
  REAL PLAY      frames of capture/play-4k60.mp4: Movie Maker, isolated `git archive a0c95cc` (tag a7) copy,
                 scripted input (_tools/film_a8_play.gd). Readouts come from that run's per-tick log.
  RECORDED OUTPUT count lines read from the test logs re-run for this film (evidence/runs/tests-a0c95cc/).
  CONSTRUCTED    drawings of what does not exist yet (the training room, the frame-data overlay, Fighter.tscn).
Text is short; narration carries the explanation. Numbers shown are read from logs or files here, or are the
EXISTS-FACTS §3 measurements, quoted through Q() (asserted verbatim at their revision). Helpers adapted from the A7
film's make_media.py; its channel footer is removed (no instructor handle or credit line in this film).

Usage: make_media.py all | B00 B03 ...
"""
import json, re, subprocess, sys
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
REV, DOCS = 'a0c95cc', 'fcb873c'
RUNS = REEL / 'evidence' / 'runs'
TESTS = RUNS / 'tests-a0c95cc'
FONTS = Path('/Users/tharunmaheswararao/Documents/csye7270/_brutalist/runtime/fonts')
SERIF = str(FONTS / 'EB_Garamond/static/EBGaramond-Medium.ttf')
SANS = str(FONTS / 'Inter/static/Inter_28pt-Medium.ttf')
SANSB = str(FONTS / 'Lato/static/Lato-Bold.ttf')
MONO = str(FONTS / 'PT_Mono/PTMono-Regular.ttf')
W, H, FPS = 3840, 2160, 30
X0, X1, Y0, Y1 = 192, 3648, 108, 2052          # title-safe (5 %)
PAGE, INK, SOFT, RULE, CARD = (250, 249, 245), (61, 57, 41), (95, 91, 78), (205, 199, 187), (255, 255, 255)
ACC = (150, 72, 48)                             # dark terracotta, text use
RING = (217, 119, 87)                           # spark terracotta, rings/rules only
CON = (36, 84, 140)                             # CONSTRUCTED blue (text use on cream)
CONBG = (226, 234, 246)
TERM, TTEXT, TMUTED, TMARK, TBLUE = (32, 37, 49), (237, 241, 247), (190, 200, 215), (69, 90, 113), (139, 199, 243)
TGREEN, TYELLOW = (174, 231, 209), (236, 224, 161)
WORK = REEL / 'media' / '_work'
PLAY = WORK / 'play'                            # frames decoded from capture/play-4k60.mp4
PLOG = RUNS / 'play-capture-log.txt'
PZ = (1290, 960, 2730, 1770)                    # 4K zoom on both fighters (16:9)
MIN_PT = 44
REAL_LABEL = 'REAL PLAY · tag a7 (a0c95cc) · SCRIPTED INPUT'
REAL_SUB = 'Movie Maker capture, 60 fps, made for this film from an isolated git archive of a7'


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
            line = w
    out.append(line)
    return out


def text_block(d, xy, text, font, width, fill=INK, lh=None):
    x, y = xy
    lh = lh or int(font.size * 1.3)
    for para in text.split('\n'):
        for ln in wrap(d, para, font, width):
            d.text((x, y), ln, font=font, fill=fill); y += lh
    return y


def header(d, title, sub=None):
    d.text((X0, 112), title, font=F(SERIF, 120), fill=INK)
    if sub:
        d.text((X0, 268), sub, font=F(SANS, 48), fill=SOFT)


def footer(d, text):
    f = F(SANS, 44)
    lines = wrap(d, text, f, X1 - X0)
    y = 2040 - 58 * len(lines)
    for ln in lines:
        d.text((X0, y), ln, font=f, fill=SOFT); y += 58


def tag(d, xy, text, fill=ACC, bg=None, size=50, anchor='la'):
    f = F(SANSB, size)
    if bg:
        x, y = xy
        w = d.textlength(text, font=f)
        if anchor == 'ra':
            x -= w
        d.rectangle((x - 22, y - 14, x + w + 22, y + size + 16), fill=bg)
        d.text((x, y), text, font=f, fill=fill)
    else:
        d.text(xy, text, font=f, fill=fill, anchor=anchor)


def constructed_badge(d, xy, text='CONSTRUCTED · a proposal · does not exist yet', anchor='la', size=52):
    tag(d, xy, text, fill=CON, bg=CONBG, size=size, anchor=anchor)


RECTS = {}
CUR = ['']


def put(c, im, xy):
    c.paste(im, xy)
    RECTS.setdefault(CUR[0], set()).add((xy[0], xy[1], xy[0] + im.width, xy[1] + im.height))


def card(d, xy, title, body, on=False, fsize=50, tsize=56, col=None):
    x0, y0, x1 = xy
    col = col or ACC
    ft, fb = F(SANSB, tsize), F(SANS, fsize)
    lines = []
    for para in body.split('\n'):
        lines += wrap(d, para, fb, x1 - x0 - 80) if para else ['']
    tl = wrap(d, title, ft, x1 - x0 - 80)
    th = int(ft.size * 1.3) * len(tl)
    hgt = 44 + th + int(fb.size * 1.36) * len(lines) + (34 if lines else 0)
    d.rectangle((x0, y0, x1, y0 + hgt), fill=CARD, outline=col if on else RULE, width=6 if on else 3)
    d.rectangle((x0, y0, x0 + 14, y0 + hgt), fill=col if on else RULE)
    for k, t in enumerate(tl):
        d.text((x0 + 46, y0 + 28 + k * int(ft.size * 1.3)), t, font=ft, fill=col if on else INK)
    y = y0 + 34 + th
    for ln in lines:
        d.text((x0 + 46, y), ln, font=fb, fill=INK); y += int(fb.size * 1.36)
    return y0 + hgt


def terminal(d, xy, title, rows, size=48):
    """rows: [(text, colour or None, highlighted)]"""
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=18, fill=TERM)
    d.text((x0 + 34, y0 + 24), title, font=F(SANS, 44), fill=TBLUE)
    fm = F(MONO, size)
    lh = int(fm.size * 1.4)
    y = y0 + 110
    for text, col, hi in rows:
        lines = wrap(d, text, fm, x1 - x0 - 90) if text else ['']
        if hi:
            d.rectangle((x0 + 12, y - 8, x1 - 12, y - 8 + lh * len(lines)), fill=TMARK)
            d.rectangle((x0 + 12, y - 8, x0 + 24, y - 8 + lh * len(lines)), fill=TBLUE)
        for ln in lines:
            d.text((x0 + 44, y), ln, font=fm, fill=col or TTEXT); y += lh
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
    if len(st) > 1 and st[1][0] < 0.4:
        st = [(0.0, st[1][1])] + st[2:]
    states_video(bid, st, nframes(b))


@lru_cache(None)
def rev_text(path, rev):
    return subprocess.run(['git', '-C', str(REPO), 'show', f'{rev}:{path}'], capture_output=True, text=True,
                          check=True).stdout


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('**', '').replace('*', '').replace('`', '')).strip()


def Q(s, rev, *files):
    """Assert a quoted string is verbatim in one of the files at rev ('…' separates verbatim parts). Returns s."""
    texts = [norm(rev_text(f, rev)) for f in files]
    for part in [p.strip(' .') for p in s.split('…')]:
        if part:
            assert any(norm(part) in t for t in texts), ('not verbatim', part[:80], files)
    return s


def count_line(log):
    """The suite's own count line, read from the log re-run for this film."""
    lines = [ln.strip() for ln in (TESTS / log).read_text().splitlines() if re.search(r'\d+ checks, \d+ failed', ln)]
    assert len(lines) == 1, (log, lines)
    return lines[0]


# ------------------------------------------------------------------ the capture
def playlog():
    rows = {}
    rx = re.compile(r'tick (\d+) frame (\d+) round (\d+) bolt (\w+) t ([\d.-]+) x ([\d.-]+) rot ([\d.-]+) '
                    r'bob ([\d.-]+) fa (\S+) fa_pos ([\d.-]+) key (\d+) ka (\S+) wind ([\d.-]+) hitstop ([\d.-]+) '
                    r'rivet (\w+) rwind ([\d.-]+) gap ([\d.-]+) hp ([\d.-]+)')
    txt = PLOG.read_text()
    for m in rx.finditer(txt):
        rows[int(m[1])] = dict(frame=int(m[2]), bolt=m[4], t=float(m[5]), fa=m[9], key=int(m[11]),
                               wind=float(m[13]), hitstop=float(m[14]), rivet=m[15], gap=float(m[17]))
    cases = {}
    for m in re.finditer(r'CASE (\d) [A-Z ]+: (?:press on tick|S held from tick) (\d+)', txt):
        cases[int(m[1])] = int(m[2])
    fight = int(re.search(r'FIGHT at tick (\d+)', txt)[1])
    return rows, cases, fight


ATT = {'JAB': (0.07, 0.10, 0.18), 'CUTLASS': (0.14, 0.12, 0.30)}   # fighter.gd:42-43 at a7 (checked below)


def phase(r):
    """The phase the game itself uses: box live while startup <= state_t < startup + active (fighter.gd:158-166)."""
    if r['bolt'] not in ATT:
        return '—'
    s, a, _ = ATT[r['bolt']]
    t = r['t'] + 1e-6
    return 'startup' if t < s else ('ACTIVE · box live' if t < s + a else 'recovery')


def movie(bid, segs, title, readout, zoom=PZ, overlay=None, big_label=True, foot=None):
    """Real-play beat. segs: [(start_s, [ticks], mode label)]; a segment longer than its ticks repeats them
    (labelled 'repeat'). The zoom is the picture; readout(tick) -> [(key, value, big)] at the right."""
    CUR[0] = bid
    rows, _, _ = playlog()
    b = beat(bid); n = nframes(b)
    starts = [round(s * FPS) for s, _, _ in segs] + [n]
    seq = []
    for k, (_, ticks, lab) in enumerate(segs):
        for j in range(starts[k + 1] - starts[k]):
            rep = j // len(ticks)
            seq.append((ticks[j % len(ticks)], lab + (f' · repeat {rep}' if rep else '')))
    VW, VH = 2560, 1440
    vx, vy = X0, 400
    base = canvas(); d = ImageDraw.Draw(base)
    header(d, title)
    tag(d, (X1, 150), REAL_LABEL, anchor='ra', size=50)
    d.text((X1, 222), REAL_SUB, font=F(SANS, 44), fill=SOFT, anchor='ra')
    d.rectangle((vx - 3, vy - 3, vx + VW + 2, vy + VH + 2), outline=RULE, width=3)
    if foot:
        footer(d, foot)
    RECTS.setdefault(bid, set()).add((vx, vy, vx + VW, vy + VH))
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / f'{bid}-masks.json').write_text(json.dumps(sorted(RECTS[bid])))
    out = REEL / 'media' / f'{bid}.mp4'
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                           '-pix_fmt', 'yuv420p', '-an', str(out)], stdin=subprocess.PIPE)
    px = vx + VW + 80
    cache = {}
    for tick, mode in seq:
        fr = rows[tick]['frame']
        if fr not in cache:
            cache.clear()
            cache[fr] = Image.open(PLAY / f'frame{fr:08d}.png').convert('RGB').crop(zoom).resize((VW, VH),
                                                                                              Image.LANCZOS)
        c = base.copy(); dd = ImageDraw.Draw(c)
        c.paste(cache[fr], (vx, vy))
        if overlay:
            overlay(c, dd, tick, rows[tick], (vx, vy, VW, VH))
        y = vy
        for key_, val, big in readout(tick, rows[tick]):
            dd.text((px, y), key_, font=F(SANS, 46), fill=SOFT)
            y += 60
            dd.text((px, y), val, font=F(SANSB, 76 if big else 56), fill=ACC if big else INK)
            y += 112 if big else 86
        y += 10
        for ln in wrap(dd, mode, F(SANSB, 46), X1 - px):
            dd.text((px, y), ln, font=F(SANSB, 46), fill=ACC if ('REPLAY' in mode or 'repeat' in mode) else SOFT)
            y += 60
        pr.stdin.write(c.tobytes())
    pr.stdin.close(); pr.wait()
    assert pr.returncode == 0
    print('wrote', out, n, 'frames')


def rng(a, z, step=1, rep=1):
    return [t for t in range(a, z + 1, step) for _ in range(rep)]


# ================================================================== beats
def b00():
    rows, cases, fight = playlog()
    e2 = cases[2]
    first = rng(cases[1] - 20, cases[4] + 180, 2)
    segs = [(0.0, first, 'REAL SPEED · jab, jab, cutlass, rewind · every 2nd tick'),
            (len(first) / FPS, rng(e2 - 6, e2 + 26, 1, 2), 'REPLAY · 0.25× · the jab lands, hitstop holds')]

    def ro(t, r):
        return [('Bolt', r['bolt'], True), ('Rivet', r['rivet'], False)]
    movie('B00', segs, 'Tin Knockout Fighter Kit', ro,
          foot='Voice: Kokoro text-to-speech reading my script, in the first person. Fighters’ x positions are SET '
               'between the scripted cases (the edge test’s method). Log: evidence/runs/play-capture-log.txt.')


def b01():
    CUR[0] = 'B01'
    bolt = Image.open(REPO / 'godot/assets/fighters/bolt/idle.png').convert('RGBA')
    tree = [(0, 'Fighter.tscn', True), (1, 'FacingPivot', False), (2, 'BodyPivot', False), (3, 'sprite', False),
            (3, 'KeyMount', False), (4, 'KeyBob', False), (5, 'key_sprite', False), (1, 'weapon', False),
            (1, 'FighterAnimPlayer', False), (1, 'KeyAnimPlayer', False)]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What It Will Be')
        constructed_badge(d, (X1, 150), anchor='ra')
        # left: the training-room build (a window, drawn)
        lx0, ly0, lx1, ly1 = X0, 420, 2240, 1800
        d.rounded_rectangle((lx0, ly0, lx1, ly1), radius=26, fill=CARD, outline=CON, width=6)
        d.rectangle((lx0 + 6, ly0 + 6, lx1 - 6, ly0 + 110), fill=CONBG)
        for k in range(3):
            d.ellipse((lx0 + 40 + k * 64, ly0 + 38, lx0 + 80 + k * 64, ly0 + 78), outline=CON, width=5)
        d.text((lx0 + 260, ly0 + 30), 'Training Room · macOS build', font=F(SANSB, 54), fill=CON)
        fy = ly1 - 240
        d.line((lx0 + 80, fy, lx1 - 80, fy), fill=CON, width=6)
        bb = bolt.crop(bolt.getchannel('A').getbbox())
        sc = 820 / bb.height
        bi = bb.resize((round(bb.width * sc), 820), Image.LANCZOS)
        bx, by = lx0 + 300, fy - bi.height
        c.paste(bi, (bx, by), bi)
        RECTS.setdefault('B01', set()).add((bx, by, bx + bi.width, by + bi.height))
        dx = lx1 - 760
        d.rounded_rectangle((dx, fy - 560, dx + 260, fy), radius=30, outline=CON, width=8)
        d.text((dx + 130, fy - 300), 'DUMMY', font=F(SANSB, 52), fill=CON, anchor='mm')
        # overlay bar (drawn)
        oy = ly0 + 170
        d.text((lx0 + 80, oy), 'JAB', font=F(SANSB, 52), fill=CON)
        cx = lx0 + 260
        cw = (lx1 - 120 - cx) // 21
        for k in range(21):
            col = (240, 200, 120) if k < 5 else ((220, 110, 90) if k < 11 else (150, 180, 220))
            d.rectangle((cx + k * cw, oy, cx + (k + 1) * cw - 8, oy + 60), fill=col)
        d.text((cx, oy + 80), 'startup 5 · active 6 · recovery 10', font=F(SANS, 48), fill=CON)
        # right: Fighter.tscn (a scene tree, drawn)
        rx0 = 2400
        d.rounded_rectangle((rx0, ly0, X1, ly1), radius=26, fill=CARD, outline=CON, width=6)
        d.rectangle((rx0 + 6, ly0 + 6, X1 - 6, ly0 + 110), fill=CONBG)
        d.text((rx0 + 50, ly0 + 30), 'Reusable scene', font=F(SANSB, 54), fill=CON)
        y = ly0 + 160
        for depth, name, root in tree:
            d.text((rx0 + 70 + depth * 64, y), ('' if root else '· ') + name, font=F(MONO, 52),
                   fill=CON if root else INK)
            y += 98
        text_block(d, (X0, 1860), 'Bolt\u2019s idle art is the real a2 sprite; the room, the dummy and the overlay are '
                   'drawn. Today the scene\u2019s nodes are built in code by fighter.gd (lines 88–119); there is no '
                   'Fighter.tscn and no exported build.', F(SANS, 46), X1 - X0, fill=SOFT)
        if i >= 1:
            st = 'NOT BUILT YET'
            f = F(SANSB, 150)
            w = d.textlength(st, font=f)
            cxm, cym = W // 2, 1090
            d.rectangle((cxm - w / 2 - 60, cym - 120, cxm + w / 2 + 60, cym + 120), fill=PAGE, outline=CON, width=12)
            d.text((cxm, cym), st, font=f, fill=CON, anchor='mm')
        return c
    staged('B01', ['stamp'], img)


def b03():
    rows, cases, _ = playlog()
    e1, e2, e3 = cases[1], cases[2], cases[3]
    b = beat('B03')
    segs = [(0.0, rng(e1 - 10, e1 + 26, 1), 'REPLAY · 0.5× · the jab, missing'),
            (ct(b, 'land'), rng(e2 - 4, e2 + 30, 1, 2), 'REPLAY · 0.25× · the jab lands: hitstop'),
            (ct(b, 'k'), rng(e3 - 4, e3 + 40, 1), 'REPLAY · 0.5× · K, the cutlass')]

    def ro(t, r):
        e = e3 if t >= e3 - 10 else (e2 if t >= e2 - 10 else e1)
        return [('tick since the press', f'{t - e:+d}', False), ('Bolt', r['bolt'], True),
                ('phase (from state_t)', phase(r), True), ('state_t', f'{r["t"]:.4f} s', False),
                ('hitstop', 'HOLD' if r['hitstop'] > 0 else '—', False)]
    movie('B03', segs, 'The Frames, In Play', ro,
          foot='Readout: the capture’s per-tick log; phase computed as the game does (fighter.gd:158-166). '
               'Gap 0.000000 s over 279 JAB ticks: TEST-REPORT A7-9e, windowed, Apple M4.')


def b04():
    CUR[0] = 'B04'
    tests = [('test_a7_pins.gd 60', 'test_a7_pins_60fps.log'),
             ('test_a7_structure.gd 60', 'test_a7_structure_60fps.log'),
             ('test_a7_edges.gd 60', 'test_a7_edges_60fps.log')]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Checked, Not Eyeballed')
        tag(d, (X1, 150), 'RECORDED OUTPUT · re-run on a7 (a0c95cc)', anchor='ra')
        rows = []
        for cmd, log in tests:
            rows += [('$ ./scripts/run-test.sh ' + cmd, TBLUE, False), (count_line(log), TGREEN, True), ('', None, False)]
        y = terminal(d, (X0, 400, X1, 1560), 'isolated git archive of a0c95cc · Godot 4.7.2 headless · 2026-11-24',
                     rows, size=60)
        if i >= 1:
            card(d, (X0, 1640, X1), 'WILL', 'Every new move joins the same suites: an edge test and a tuning entry each.',
                 on=True, col=CON)
        footer(d, 'Logs: evidence/runs/tests-a0c95cc/. Counts match TEST-REPORT A7 (49, 57, 70).')
        return c
    staged('B04', ['will'], img)


def b05():
    """CONSTRUCTED overlay over a real frame; then the real command."""
    CUR[0] = 'B05'
    rows, cases, _ = playlog()
    e1 = cases[1]
    tick = e1 + 7                                     # the whiffed jab, box live
    r = rows[tick]
    assert r['bolt'] == 'JAB' and phase(r).startswith('ACTIVE'), r
    full = Image.open(PLAY / f'frame{r["frame"]:08d}.png').convert('RGB')
    VW, VH = 2560, 1440
    pic = full.crop(PZ).resize((VW, VH), Image.LANCZOS)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What It Will Give You')
        put(c, pic, (X0, 400))
        d.rectangle((X0 - 3, 397, X0 + VW + 2, 400 + VH + 2), outline=RULE, width=3)
        # the drawn overlay, inside the picture
        ox0, oy0 = X0 + 60, 400 + 60
        ow = VW - 120
        d.rectangle((ox0 - 20, oy0 - 20, ox0 + ow + 20, oy0 + 300), fill=CONBG, outline=CON, width=6)
        d.text((ox0 + 10, oy0), 'CONSTRUCTED OVERLAY · does not exist yet', font=F(SANSB, 52), fill=CON)
        cw = ow // 21
        for k in range(21):
            col = (240, 200, 120) if k < 5 else ((220, 110, 90) if k < 11 else (150, 180, 220))
            d.rectangle((ox0 + k * cw, oy0 + 90, ox0 + (k + 1) * cw - 8, oy0 + 170), fill=col)
        k = 7
        d.rectangle((ox0 + k * cw - 6, oy0 + 80, ox0 + (k + 1) * cw - 2, oy0 + 180), outline=INK, width=8)
        d.text((ox0 + 10, oy0 + 196), 'JAB  startup 5 · active 6 · recovery 10   (frame 7: active)', font=F(SANS, 50),
               fill=CON)
        px = X0 + VW + 80
        text_block(d, (px, 420), 'Under the overlay: a real frame of the jab at a7, tick 7 of the press, box live.',
                   F(SANS, 48), X1 - px, fill=SOFT)
        tag(d, (px, 760), 'REAL PLAY · a7', size=48)
        if i >= 1:
            y = 1000
            tag(d, (px, y), 'TODAY · real command', size=48)
            terminal(d, (px, y + 90, X1, y + 520), 'repository root', [
                ('./scripts/run-test.sh', TBLUE, False), ('  test_a7_edges.gd 60', TBLUE, False),
                (count_line('test_a7_edges_60fps.log'), TGREEN, True)], size=50)
        footer(d, 'Overlay counts are the measured jab ticks (EXISTS-FACTS §3). Fighters’ positions SET by the '
                  'scripted capture.')
        return c
    staged('B05', ['cmd'], img)


def b06():
    CUR[0] = 'B06'

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Different From What I Play')
        mid = W // 2
        card(d, (X0, 460, mid - 60), 'Street Fighter 6 · Tekken 8',
             'Far larger, finished games.\nI have played both.\n\nTheir frame data: something the player reads.',
             fsize=62, tsize=72)
        card(d, (mid + 60, 460, X1), 'Tin Knockout Fighter Kit',
             'Not a competitor as a game.\n\nOpen the state machine that makes the frames.\nRerun the tests that '
             'prove them.', on=i >= 1, fsize=62, tsize=72)
        footer(d, 'Named only, as games I have played. No footage or art from either game appears in this film.')
        return c
    staged('B06', ['here'], img)


def b07():
    rows, cases, _ = playlog()
    s = cases[4]
    def ro(t, r):
        return [('Bolt', r['bolt'], True), ('wind', f'{r["wind"]:.0f} / 100', True), ('key frame', str(r['key']),
                                                                                       False)]
    first = rng(s - 16, s + 190, 2)
    segs = [(0.0, first, 'REAL SPEED · Bolt holds S, then lets go · every 2nd tick'),
            (len(first) / FPS, rng(s, s + 170, 1), 'REPLAY · 0.5× · the crank')]
    movie('B07', segs, 'Its Own Mechanic', ro, zoom=(1148, 820, 2872, 1790),   # wider: keeps the game's REWIND label
          foot='Wind after the jab, the jab and the cutlass in this capture; S held 150 ticks. Readout: the capture log.')


def b08():
    CUR[0] = 'B08'
    steps = ['Double-click the macOS build', 'Land in the training room, no menu', 'Press J: the overlay counts the jab',
             'Press K: the cutlass’s different timing']

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The First Sixty Seconds')
        d.text((X0, 330), 'Target role: gameplay programmer  ·  Reader: a lead gameplay engineer or hiring manager',
               font=F(SANS, 56), fill=INK)
        cw = (X1 - X0 - 3 * 50) // 4
        for k, s in enumerate(steps):
            x = X0 + k * (cw + 50)
            on = i == k + 1
            card(d, (x, 520, x + cw), f'{k + 1} · WILL', s, on=on, fsize=60, tsize=60, col=CON)
        if i >= 5:
            tag(d, (X0, 1240), 'TODAY · a second path that works now (recorded output, a7)', size=52)
            terminal(d, (X0, 1330, X1, 1820), 'repository root', [
                ('$ ./scripts/run-test.sh test_a7_edges.gd 60', TBLUE, False),
                (count_line('test_a7_edges_60fps.log'), TGREEN, True)], size=64)
        footer(d, 'Steps 1–4 describe the planned build (CONSTRUCTED plan). The command and its count line are real.')
        return c
    staged('B08', ['s1', 's2', 's3', 's4', 'today'], img)


def b09():
    CUR[0] = 'B09'
    rows = [('Animation and state', 'One authority per animated node; clips synced to state_t.', 'a7 · TEST-REPORT A7-6'),
            ('Verification', 'Pins before and after a change (A7-2) · edge tests at every boundary (A7-7) · mutations '
                             'in git worktrees (A7-5) · a seam bug a fixture log caught after the suite passed (A7-9a).',
             'a7'),
            ('Profiling', 'Two clocks, Apple M4: display 129 fps, physics 60 ticks/s, clip vs state_t gap 0.000000 s.',
             'a7 · A7-9e'),
            ('Shaders and particles', 'Presentation that reads the fighter’s state and signals, and never writes it.',
             'a5 f4dda68 · a6 66c8cbc')]
    Q('clip vs state_t on 279 JAB ticks: largest gap 0.000000 s', REV, 'TEST-REPORT.md')
    Q('display 129 fps, physics 60 ticks/s', REV, 'TEST-REPORT.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What It Proves')
        y = 420
        for k, (a, b_, t) in enumerate(rows):
            on = k == i
            y = card(d, (X0, y, X1), f'{a}   ·   {t}', b_, on=on, fsize=56, tsize=60) + 40
        footer(d, 'Will add: an edge suite and a tuning entry for every new move; a test that the reusable scene keeps '
                  'every pinned number; a measured frame rate for the build on the M4.')
        return c
    staged('B09', ['v', 'p', 's'], img)


def columns(bid, title, cols, keys, foot):
    CUR[0] = bid

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, title)
        n = len(cols)
        cw = (X1 - X0 - (n - 1) * 60) // n
        for k, (head, body, col) in enumerate(cols):
            x = X0 + k * (cw + 60)
            card(d, (x, 430, x + cw), head, body, on=(k <= i), fsize=58, tsize=66, col=col)
        footer(d, foot)
        return c
    staged(bid, keys, img)


def b10():
    columns('B10', 'In, Out, First', [
        ('OUT', 'Online or local multiplayer netcode\nA second character’s art\nMore than one arena\nA save system', ACC),
        ('IN · will', 'Reusable Fighter.tscn\nAnimated cutlass, block, hurt\nA short input buffer\nFrame-data overlay\n'
                      'Training room\nmacOS export', CON),
        ('FIRST · will', 'The fighter will run as its own scene against a still dummy.\n\nProof it ran: pins 49, '
                         'structure 57 and edges 70 will pass, 0 failed, against the new scene, unchanged.', CON)],
        ['in', 'first'], 'Counts are the a7 counts (TEST-REPORT A7).')


def b12():
    CUR[0] = 'B12'

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What I Will Do About It')
        tag(d, (X1, 150), 'RECORDED OUTPUT · re-run on a7 (a0c95cc)', anchor='ra')
        terminal(d, (X0, 400, X1, 1200), 'the pins drive the real main.tscn through the input path', [
            ('$ ./scripts/run-test.sh test_a7_pins.gd 60', TBLUE, False),
            (count_line('test_a7_pins_60fps.log'), TGREEN, True),
            ('$ ./scripts/run-test.sh test_a7_pins.gd 30', TBLUE, False),
            (count_line('test_a7_pins_30fps.log'), TGREEN, True)], size=60)
        card(d, (X0, 1270, X1), 'WILL · the rule', 'The refactor is not committed unless the pins pass with identical '
             'logs.', on=True, col=CON, fsize=58, tsize=60)
        if i >= 1:
            card(d, (X0, 1580, X1), 'A smaller risk', 'Forward+ on Vulkan: the macOS build will be tested on the M4 '
                 'before anything is claimed about it. No web build.', on=True, fsize=58, tsize=60)
        return c
    staged('B12', ['vk'], img)


def b13():
    columns('B13', 'Why This Project', [
        ('HAVE · with evidence', 'Shaders driven by game state (a5)\nParticles with a measured cost (a6)\nA pinned '
                                 'animation state machine (a7)\nDirecting an agent with scoped plans and approvals '
                                 '(every a7 commit)', ACC),
        ('NEW TO ME', 'A reusable scene\nAn input buffer\nA frame-data overlay\nA desktop export with a frame-rate '
                      'measurement', CON),
        ('DON’T KNOW YET', 'Would an AnimationTree simplify it?\n\nBuild the cutlass both ways in a branch; keep '
                               'whichever passes the same edge tests with fewer authorities.', CON)],
        ['new', 'unk'], 'Tags: a5 f4dda68 · a6 66c8cbc · a7 a0c95cc.')


def b14():
    columns('B14', 'Exists Today · Will Exist', [
        ('EXISTS TODAY', 'Playable slice, title to KO to rematch · a2 9788922\n11-state fighter, intent seam, five '
                         'signals · a7\nAnimated jab and key cycle, one authority each · a7\nTests 0 failed: pins 49, '
                         'structure 57, edges 70 · a7\nTuning log, mutations, seam fix, clock measurement · a7\n'
                         'Shaders a5 f4dda68 · particles a6 66c8cbc', ACC),
        ('WILL EXIST', 'Fighter.tscn usable without main.gd, and the training room\nAnimated cutlass, block and hurt, '
                       'each with an edge suite\nAn input buffer, with its own pins\nThe frame-data overlay\nA macOS '
                       'export, frame rate measured on the M4\nAn AnimationTree comparison on the cutlass', CON)],
        ['will'], 'a7 = a0c95cc. Every "exists" line can be checked out at its tag.')


def b15():
    CUR[0] = 'B15'
    rows, cases, _ = playlog()
    r = rows[cases[2] + 5]                                   # the jab landing, real play
    assert r['bolt'] == 'JAB' and r['rivet'] == 'HURT', r
    pic = Image.open(PLAY / f'frame{r["frame"]:08d}.png').convert('RGB').crop(PZ).resize((2304, 1296), Image.LANCZOS)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        put(c, pic, (X0, 300))
        d.rectangle((X0 - 3, 297, X0 + 2304 + 2, 300 + 1296 + 2), outline=RULE, width=3)
        tag(d, (X0, 1650), REAL_LABEL, size=48)
        d.text((X0, 1720), 'the jab landing, case 2 of the film capture', font=F(SANS, 44), fill=SOFT)
        px = X0 + 2304 + 110
        y = text_block(d, (px, 300), 'Tin Knockout Fighter Kit', F(SERIF, 150), X1 - px, lh=170)
        d.line((px, y + 40, X1, y + 40), fill=RING, width=6)
        y = text_block(d, (px, y + 100), 'Tharun Maheswararao', F(SANSB, 76), X1 - px, fill=ACC)
        y = text_block(d, (px, y + 30), 'CSYE 7270 · final project pitch', F(SANS, 56), X1 - px, fill=SOFT)
        text_block(d, (px, 1380), 'Exists at tag a7 (a0c95cc).\nEverything else: will.', F(SANS, 52), X1 - px, fill=INK)
        text_block(d, (px, 1620), 'Voice: Kokoro text-to-speech (am_onyx) reading Tharun’s script.', F(SANS, 44),
                   X1 - px, fill=SOFT)
        return c
    staged('B15', [], img)


BUILD = {'B00': b00, 'B01': b01, 'B03': b03, 'B04': b04, 'B05': b05, 'B06': b06, 'B07': b07, 'B08': b08,
         'B09': b09, 'B10': b10, 'B12': b12, 'B13': b13, 'B14': b14, 'B15': b15}

if __name__ == '__main__':
    src = rev_text('godot/fighter/fighter.gd', REV).splitlines()
    assert '"startup": 0.07, "active": 0.10, "recovery": 0.18' in src[41], src[41]
    assert '"startup": 0.14, "active": 0.12, "recovery": 0.30' in src[42], src[42]
    which = sys.argv[1:] or ['all']
    for bid in (BUILD if which == ['all'] else which):
        BUILD[bid]()
