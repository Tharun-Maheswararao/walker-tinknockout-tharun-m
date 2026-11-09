#!/usr/bin/env python3
"""Build the A6 film's own media from real files, recorded output and real engine captures only.

Every image placed here is a committed fixture strip frame or comparison sheet (captures/, fixture scenes in
godot/previews/, fixed seed, captured by Tharun; sheets assembled by Claude), Tharun's Visual Profiler screenshot
(evidence/a6/), or a frame of the film's Movie Maker capture (capture/play-4k.mp4, scripted input, isolated copy of
c844ab2). Text panels are verbatim lines from repo files and logs; every quotation goes through Q(), which asserts it
is verbatim in its source file. This script lays them out, adds provenance labels and switches highlight states on the
spoken cue times written by patch_timing.py. It invents no output. Helpers copied from the A5 film's make_media.py.

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


# ================================================================== A6
STRIP = REPO / 'captures'
PLAY = REEL / 'media' / '_work' / 'play'          # frames decoded from capture/play-4k.mp4 (0..381)
LOG = REEL / 'evidence' / 'runs' / 'play-capture-log.txt'
NAMES = {0: 'IDLE', 1: 'WALK', 2: 'JAB', 3: 'CUTLASS', 4: 'POP', 5: 'BLOCK', 6: 'REWIND', 7: 'HURT', 8: 'EMPTY',
         9: 'KO', 10: 'WIN'}
A_CROP = (340, 380, 540, 530)       # around the hit point (209, 227) view = (418, 454) window
B_CROP = (470, 400, 630, 520)       # around the key, both steam fixtures
ZA = (1000, 1050, 1800, 1500)       # 4K zoom on the hit point in the film capture
ZB = (590, 1221, 1190, 1559)        # 4K zoom on Bolt's key (keypos-headless-replay-log.txt: key x 840-940, y 1400-1530)


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('**', '').replace('`', '').replace('_(', '(').replace(')_', ')')).strip()


def Q(s, *files):
    """Assert a quoted string is verbatim in one of the files ('…' separates verbatim parts). Returns s."""
    texts = [norm((REPO / f).read_text()) for f in files]
    for part in [p.strip(' .') for p in s.split('…')]:
        if part:
            assert any(norm(part) in t for t in texts), ('not verbatim', part[:80], files)
    return s


def playlog():
    out = {}
    for ln in LOG.read_text().splitlines():
        m = re.match(r'frame (\d+) bolt (\d+) rivet (\d+) wind ([\d.]+) ratio ([\d.]+) rivet_ratio ([\d.]+) '
                     r'bursts (\d+) blocked (\d+) keyx ([\d.-]+) paused (\w+)', ln)
        if m:
            out[int(m[1])] = dict(bolt=int(m[2]), rivet=int(m[3]), wind=float(m[4]), ratio=float(m[5]),
                                  rratio=float(m[6]), n=int(m[7]), nb=int(m[8]), paused=m[10] == 'true')
    jabs = {int(m[1]): int(m[2]) for m in re.finditer(r'JAB (\d+) pressed at frame (\d+)', LOG.read_text())}  # jab n -> log frame
    return out, jabs


def strip_crop(run, f, box, w, h):
    im = Image.open(STRIP / run / f'frame{f:08d}.png').convert('RGB').crop(box)
    return im.resize((w, h), Image.LANCZOS)


def quote_card(d, xy, who, text, on=False, fsize=46):
    return card(d, xy, who, '“' + text + '”', on=on, fsize=fsize, tsize=48)


def code_lines(path, a, b):
    return list(zip(range(a, b + 1), src_lines(path, a, b)))


# ------------------------------------------------------------------ B02 two effects, two jobs
def b02():
    fa, fb = 141, 252
    rows = []
    for f, z, tag in ((fa, ZA, 'Effect A'), (fb, ZB, 'Effect B')):
        full = Image.open(PLAY / f'frame{f:08d}.png').convert('RGB')
        rows.append((f, z, tag, full.resize((1060, 596), Image.LANCZOS), full.crop(z).resize((1000, 596), Image.LANCZOS)))
    A = Q('Effect A gives the hit distinct visual weight and better readability across different arena backgrounds.',
          'CHANGE-BRIEF.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Two Effects, Two Jobs', 'Tin Knockout, Assignment 6: what each effect tells the player, and what drives it')
        y = 360
        for f, z, tag, im, zm in rows:
            cap_label(d, X0, y, 'HELD FRAME · MOVIE MAKER CAPTURE · SCRIPTED INPUT',
                      f'{tag} · play-4k.mp4 frame {f} · right: zoom')
            paste_framed(c, d, im, X0, y + 70)
            s = 1060 / 3840
            d.rectangle((X0 + int(z[0] * s), y + 70 + int(z[1] * s), X0 + int(z[2] * s), y + 70 + int(z[3] * s)),
                        outline=RING, width=6)
            paste_framed(c, d, zm, X0 + 1100, y + 70)
            y += 70 + 596 + 70
        x = 2420
        yy = card(d, (x, 360, X1), 'EFFECT A · impact burst',
                  'Job (brief A.1): “' + A[9:] + '”\n'
                  'Event: every impact. Fighter.hit_landed or Cork.struck → main._on_impact(p, blocked).\n'
                  'Blocked hits: a smaller grey burst (impact_effect_blocked.tscn).', on=i == 1, fsize=44)
        card(d, (x, yy + 40, X1), 'EFFECT B · wind steam',
             'Job: a feedback loop at the fighter\'s back key.\nValue: Fighter.wind, 0–100.\n'
             'Condition: wind below 25.\nMapping: amount_ratio = clamp((25 − wind) / 25, 0, 1).\n'
             'One per fighter (main.gd steam_ratio).', on=i == 2, fsize=44)
        footer(d, 'Film capture: Bolt driven by scripted input through the real input path; Rivet is the game\'s own '
                  'brain (CAPTURE.md). Isolated copy of c844ab2.')
        return c
    staged('B02', ['a', 'b'], img)


# ------------------------------------------------------------------ B03 emission / process / draw
def b03():
    P = 'godot/effects/impact_effect.tscn'
    cols = [('EMISSION', [(86, 86)], 'how many are born, and when', 10,
             'r1 frame 10: the trigger frame. The burst is already on screen.'),
            ('PROCESS', [(28, 28)], 'how each particle moves over its life', 15,
             'r1 frame 15: shards in a ring below and beside the fist.'),
            ('DRAW', [(36, 37)], 'how each particle is painted', 12,
             'r1 frame 12: the ADD core can only brighten the castle.')]
    crops = [strip_crop('impact_effect/r1', f, A_CROP, 880, 660) for _, _, _, f, _ in cols]
    fact1 = Q('A headless run uses a dummy renderer: it draws no particles and runs no GPU particle process.',
              'CLAUDE.md')
    fact2 = Q("A GPU effect's headless CPU price is near zero by construction.", 'CLAUDE.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Emission · Process · Draw')
        d.text((X1, 150), 'SOURCE VIEW · godot/effects/impact_effect.tscn at c844ab2', font=F(SANSB, 44), fill=ACC,
               anchor='ra')
        w = (X1 - X0 - 2 * 72) // 3
        ytop = 0
        for k, (name, segs, what, f, res) in enumerate(cols):
            a, b = segs[0]
            ytop = max(ytop, code_box(ImageDraw.Draw(canvas()), (0, 470, w, 0), 'x', code_lines(P, a, b), size=44))
        for k, (name, segs, what, f, res) in enumerate(cols):
            x = X0 + k * (w + 72)
            on = i == k + 1
            d.text((x, 300), name, font=F(SANSB, 64), fill=ACC if on else INK)
            d.text((x, 386), what, font=F(SANS, 46), fill=SOFT)
            a, b = segs[0]
            code_box(d, (x, 470, x + w, 0), f'line{"s" if a != b else ""} {a}{"–" + str(b) if a != b else ""}',
                     code_lines(P, a, b), active={b} if on or i > k + 1 else set(), size=44)
            y = ytop
            if i >= k + 1:
                cap_label(d, x, y + 34, 'FIXTURE · HELD FRAME', f'r1 frame {f} · zoom')
                paste_framed(c, d, crops[k], x, y + 100)
                text_block(d, (x, y + 100 + 660 + 16), res, F(SANS, 44), w, fill=INK)
        if i >= 4:
            d.rectangle((X0, 1830, X1, 1985), fill=CARD, outline=ACC, width=6)
            d.text((X0 + 40, 1848), 'CLAUDE.md, headless facts: “' + fact1 + '”', font=F(SANS, 44), fill=INK)
            d.text((X0 + 40, 1910), '“' + fact2 + '”', font=F(SANS, 44), fill=INK)
        else:
            footer(d, 'Strip frames: fixture capture captures/impact_effect/r1 (godot/previews/impact_preview.tscn, fixed '
                      'seed, captured by Tharun). Line 37 is the Core\'s draw material; blend_mode 1 is ADD.')
        return c
    staged('B03', ['emit', 'proc', 'draw', 'head'], img)


def brief_rows(section_start, labels):
    """Verbatim cells of a two-column brief table: {label: text}."""
    txt = (REPO / 'CHANGE-BRIEF.md').read_text().split(section_start, 1)[1]
    out = {}
    for ln in txt.splitlines():
        m = re.match(r'\| \*\*(.+?)\*\*[^|]*\| (.+) \|$', ln)
        if m and m[1] in labels and m[1] not in out:
            out[m[1]] = norm(m[2])
    return out


def table(d, y, rows, on, fsize=44, lw=560):
    f, fl = F(SANS, fsize), F(SANSB, fsize + 2)
    lh = int(fsize * 1.34)
    for lab, text in rows:
        lines = wrap(d, text, f, X1 - X0 - lw - 60)
        h = 30 + lh * len(lines) + 20
        hi = lab in on
        d.rectangle((X0, y, X1, y + h), fill=CARD, outline=ACC if hi else RULE, width=6 if hi else 3)
        d.text((X0 + 30, y + 24), lab, font=fl, fill=ACC if hi else INK)
        yy = y + 24
        for ln in lines:
            d.text((X0 + lw, yy), ln, font=f, fill=INK); yy += lh
        y += h + 16
    return y


# ------------------------------------------------------------------ B04 Effect A intent
def b04():
    labs = ['Timing phases', 'Contrast', 'Scale', 'Variation']
    r = brief_rows('### A.2 Intent: how it reads', labs)
    split = Q('an additive layer cannot draw a dark outline, so the dark edge and the cyan core went on separate MIX and '
              'ADD emitters', 'CHANGE-BRIEF.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect A · The Intent', 'CHANGE-BRIEF.md A.2 · version 1, 2026-11-08, written before the build · verbatim')
        on = {0: set(), 1: {'Contrast'}, 2: {'Scale', 'Variation'}}[i]
        y = table(d, 360, [(l, r[l]) for l in labs], on, fsize=52, lw=600)
        if i >= 1:
            card(d, (X0, y + 20, X1), 'From the brief\'s authorship block: a correction from Claude Code\'s review',
                 '“' + split + '”', on=i == 1, fsize=52, tsize=54)
        footer(d, 'Tharun\'s values; drafted with Claude 3.5 Sonnet and corrected from Claude Code\'s reviews (brief '
                  'authorship block).')
        return c
    staged('B04', ['contrast', 'scale'], img)


# ------------------------------------------------------------------ B06 Effect A first strip
def b06():
    fr = [10, 12, 15, 20, 30, 50]
    cw, chh = 700, 525
    crops = {f: strip_crop('impact_effect/r0', f, A_CROP, cw, chh) for f in fr}
    look1 = Q('The brightest thing and its colour: the core flash, bright cyan.', 'TUNING.md')
    look2 = Q("The dark shards against the castle: a bit hard to make out individually because they're small (8×8 px) "
              'and charcoal against the light stone background.', 'TUNING.md')
    read = Q('But they are faint: median drop 41, read as translucent pinkish bits against the pink castle. The colour '
             'ramp fades alpha linearly from 1 to 0, so at two-thirds of life about one-third of the alpha is left.',
             'TUNING.md')
    empty = Q('Matches: pixel-identical to the empty background.', 'TUNING.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect A · The First Strip')
        cap_label(d, X0, 280, 'FIXTURE CAPTURE · HELD FRAMES', 'impact_preview.tscn · fixed seed · captured by Tharun · '
                  'captures/impact_effect/r0 · zoom ×3.5')
        for k, f in enumerate(fr):
            x = X0 + (k % 3) * (cw + 40)
            y = 420 + (k // 3) * (chh + 120)
            d.text((x, y), f'frame {f}', font=F(SANSB, 48), fill=ACC if (i >= 2 and f == 15) or (i >= 3 and f >= 20) else INK)
            paste_framed(c, d, crops[f], x, y + 70)
            if i >= 2 and f == 15:
                d.rectangle((x - 10, y + 60, x + cw + 9, y + 70 + chh + 9), outline=RING, width=10)
            if i >= 3 and f >= 20:
                d.text((x + 30, y + 70 + chh - 80), 'empty', font=F(SANSB, 56), fill=(255, 255, 255), stroke_width=4,
                       stroke_fill=INK)
        x = X0 + 3 * (cw + 40) + 30
        y = 420
        if i >= 1:
            y = quote_card(d, (x, y, X1), 'Tharun · first look, before Claude read any strip', look1 + ' … ' + look2,
                           on=i == 1, fsize=44) + 30
        if i >= 2:
            y = quote_card(d, (x, y, X1), 'Claude · reading of frame 15', read, on=i == 2, fsize=44) + 30
        if i >= 3:
            quote_card(d, (x, y, X1), 'Claude · frames 20, 30, 50', empty, on=i == 3, fsize=44)
        footer(d, 'Burst at frame 10, a second at 11 (brief D.1). Median drop: luminance darkening of shard pixels against the same frame\'s empty background (frame '
                  '20), in levels of 255 (TUNING.md).')
        return c
    staged('B06', ['look', 'read', 'empty'], img)


# ------------------------------------------------------------------ B07 Effect A revision 1
def b07():
    P = 'godot/effects/impact_effect.tscn'
    old = subprocess.run(['git', '-C', str(REPO), 'show', '45e986f^:' + P], capture_output=True, text=True,
                         check=True).stdout.splitlines()[6:8]
    preds = [Q('10: unchanged. Alpha starts at 1.0 in both ramps, and the core still covers the shards.', 'TUNING.md'),
             Q('12: almost unchanged. … Darker-pixel median drop rises from 20 to about 25–30.', 'TUNING.md'),
             Q('15: the visible difference. … Darker-pixel median drop rises from 41 to 90 or more. The darker-pixel '
               'count stays about the same (≈ 950)', 'TUNING.md'),
             Q('20, 30, 50: still empty.', 'TUNING.md')]
    risk = Q('the fade is squeezed into the last 0.075 s (about 2 frames at 30 fps, 9 at 120 Hz). The shards may look '
             'like they blink out rather than fade.', 'TUNING.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect A · Revision 1', 'One setting: the Shards color_ramp (TUNING.md, approved by Tharun)')
        d.text((X1, 150), 'SOURCE VIEW · git 45e986f', font=F(SANSB, 44), fill=ACC, anchor='ra')
        w = 1900
        y = code_box(d, (X0, 340, X0 + w, 0), 'before · r0 · impact_effect.tscn lines 7–8',
                     list(zip((7, 8), old)), size=50)
        code_box(d, (X0, y + 50, X0 + w, 0), 'after · r1 · c844ab2 · lines 7–9', code_lines(P, 7, 9), {8, 9}, size=50,
                 note='new point at 0.7: (0.25, 0.25, 0.28, 1.0), still fully opaque')
        x = X0 + w + 80
        if i >= 1:
            yy = card(d, (x, 340, X1), 'Claude · prediction, before any change', '\n'.join('“' + p + '”' for p in preds),
                      on=i == 1, fsize=50, tsize=52)
            if i >= 2:
                quote_card(d, (x, yy + 30, X1), 'Claude · the risk', risk, on=True, fsize=50)
        footer(d, 'Same seed, so the same shard paths. Effect A\'s normal scene only; the blocked scene is unchanged '
                  '(TUNING.md).')
        return c
    staged('B07', ['pred', 'risk'], img)


# ------------------------------------------------------------------ B08 Effect A r0 vs r1
def b08():
    sh = Image.open(STRIP / 'impact_effect' / 'r0_vs_r1_sheet.png').convert('RGB')
    im, s = fit(sh, 2140, 1070)
    rows = [('15', Q('Median 41.3 → 105.7, max 119 → 215; darker pixels 965 → 1121', 'TUNING.md') + ' · ' +
             Q('The median matches. … The count does not match: it rose by 16 %.', 'TUNING.md')),
            ('12', Q('Darker pixels 365 → 420, median 19.6 → 21.4, max 100 → 136', 'TUNING.md') + ' · ' +
             Q('Direction right, size wrong.', 'TUNING.md')),
            ('10', Q('Almost. … I had assumed age 0.', 'TUNING.md'))]
    v1 = Q('The end: they faded out smoothly, no snap or blink.', 'TUNING.md')
    v2 = Q('shards were easier to make out against the bright castle as solid dark flecks.', 'TUNING.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect A · Before and After')
        cap_label(d, X0, 280, 'FIXTURE CAPTURES · HELD FRAMES', 'captures/impact_effect/r0_vs_r1_sheet.png · top r0, '
                  'bottom r1 · frames 10, 12, 15, 20 · sheet assembled by Claude')
        paste_framed(c, d, im, X0, 360)
        for k, f in enumerate((10, 12, 15, 20)):
            d.text((X0 + int(k * 368 * s) + 20, 360 + im.height + 20), f'frame {f}', font=F(SANSB, 46),
                   fill=ACC if (f == 15 and i >= 1) else INK)
        d.text((X0 + im.width + 24, 360 + int(140 * s)), 'r0', font=F(SANSB, 52), fill=INK)
        d.text((X0 + im.width + 24, 360 + int(510 * s)), 'r1', font=F(SANSB, 52), fill=INK)
        if i >= 1:
            ring(d, (736, 0, 1100, 736), s, X0, 360, width=10)
        x = X0 + 2140 + 140
        y = 360
        for k, (f, t) in enumerate(rows):
            if i >= (1 if k == 0 else 2):
                y = card(d, (x, y, X1), f'frame {f} · Claude\'s comparison', t, on=(i == 1 and k == 0) or (i == 2 and k),
                         fsize=44) + 24
        if i >= 3:
            card(d, (X0, 360 + im.height + 110, X0 + 2140), 'Tharun · in the running game, 1280×720',
                 '“' + v2 + '”\n“' + v1 + '”\nVerdict: Keep.', on=True, fsize=46)
        else:
            footer(d, 'Each frame measured against its own run\'s empty frame 20 (TUNING.md).')
        return c
    staged('B08', ['f15', 'f12', 'verdict'], img)


# ------------------------------------------------------------------ source-view code beat (B09)
def b09():
    b = beat('B09'); p = b['shot']['panel']
    a, z = p['segments'][0]
    rows = code_lines(p['path'], a, z)
    cues = p['cues']

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, p['title'])
        d.text((X1, 150), 'SOURCE VIEW · not an editor recording', font=F(SANSB, 44), fill=ACC, anchor='ra')
        act = {cues[i - 1][0]} if i else set()
        code_box(d, (X0, 300, 2700, 0), f'{p["path"]}  ·  lines {a}–{z}  ·  c844ab2', rows, act, size=46)
        y = 300
        for k, (ln, lab) in enumerate(cues):
            y = card(d, (2780, y, X1), f'line {ln}', lab, on=i == k + 1, fsize=44) + 30
        for lab, val in p['notes']:
            y = card(d, (2780, y, X1), lab, val, fsize=44) + 30
        footer(d, 'Called from main._on_impact(p, blocked), which still draws the star, shakes and rolls the camera '
                  '(main.gd:217-222).')
        return c
    staged('B09', [str(ln) for ln, _ in cues], img)


# ------------------------------------------------------------------ motion beats (B10, B16)
def motion(bid, segs, title, zoom, zlabel, readout, footer_text):
    """segs: [(start_frame_in_beat, src_a, src_b, repeat, label)]; each runs until the next start; when its source
    runs out the last frame is held and labelled HELD FRAME. Readout values from the capture log (log = movie + 1)."""
    b = beat(bid); n = nframes(b)
    log, jabs = playlog()
    seq = []
    for k, (t0, a, z, rep, lab) in enumerate(segs):
        t1 = segs[k + 1][0] if k + 1 < len(segs) else n
        srcs = [f for f in range(a, z + 1) for _ in range(rep)]
        for j in range(t1 - t0):
            seq.append((srcs[j], lab) if j < len(srcs) else (z, 'HELD FRAME · movie frame %d' % z))
    VW, VH = 2304, 1296
    base = canvas(); d = ImageDraw.Draw(base)
    header(d, title)
    cap_label(d, X0, 280, 'MOVIE MAKER CAPTURE · SCRIPTED INPUT',
              'made for this film · isolated copy of c844ab2 · capture/play-4k.mp4')
    d.rectangle((X0 - 2, 358, X0 + VW + 1, 360 + VH + 1), outline=RULE, width=3)
    px = X0 + VW + 70
    pw = X1 - px
    ZH = round(pw * 9 / 16)
    d.text((px, 300), zlabel, font=F(SANSB, 44), fill=ACC)
    d.rectangle((px - 2, 358, X1 + 1, 360 + ZH + 1), outline=RULE, width=3)
    footer(d, footer_text)
    RECTS.setdefault(bid, set()).update({(X0, 360, X0 + VW, 360 + VH), (px, 360, X1, 360 + ZH)})
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / f'{bid}-masks.json').write_text(json.dumps(sorted(RECTS[bid])))
    out = REEL / 'media' / f'{bid}.mp4'
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                           '-pix_fmt', 'yuv420p', '-an', str(out)], stdin=subprocess.PIPE)
    cache = {}
    s = VW / 3840
    for k, (src, mode) in enumerate(seq):
        if src not in cache:
            cache.clear()
            full = Image.open(PLAY / f'frame{src:08d}.png').convert('RGB')
            cache[src] = (full.resize((VW, VH), Image.LANCZOS), full.crop(zoom).resize((pw, ZH), Image.LANCZOS))
        c = base.copy(); dd = ImageDraw.Draw(c)
        c.paste(cache[src][0], (X0, 360))
        c.paste(cache[src][1], (px, 360))
        dd.rectangle((X0 + int(zoom[0] * s), 360 + int(zoom[1] * s), X0 + int(zoom[2] * s), 360 + int(zoom[3] * s)),
                     outline=RING, width=5)
        L = log.get(src + 1, {})
        y = 360 + ZH + 50
        for key, val, big in readout(L, src, jabs):
            dd.text((px, y), key, font=F(SANS, 44), fill=SOFT)
            dd.text((px + 520, y - (14 if big else 0)), val, font=F(SANSB, 64 if big else 48), fill=ACC if big else INK)
            y += 84 if big else 68
        y += 10
        for ln in wrap(dd, mode, F(SANSB, 46), pw):
            dd.text((px, y), ln, font=F(SANSB, 46), fill=ACC if ('REPLAY' in mode or 'HELD' in mode) else SOFT); y += 60
        pr.stdin.write(c.tobytes())
    pr.stdin.close(); pr.wait()
    print('wrote', out, n, 'frames')


def b10():
    b = beat('B10'); slow = round(ct(b, 'slow') * FPS)

    def ro(L, src, jabs):
        done = sum(1 for f in jabs.values() if f <= src + 1)
        return [('movie frame', str(src), False), ('Bolt', NAMES.get(L.get('bolt'), '?'), False),
                ('Rivet', NAMES.get(L.get('rivet'), '?'), False), ('jabs pressed', f'{done} of 8', False),
                ('bursts alive', f'{L.get("n", 0)} normal · {L.get("nb", 0)} blocked', True)]
    motion('B10', [(0, 92, 300, 1, 'REAL SPEED · movie frames 92–300'),
                   (209, 92, 200, 2, 'REPLAY · 0.5× speed (each frame shown 2×)'),
                   (slow, 136, 178, 4, 'REPLAY · 0.25× speed (each frame shown 4×)')],
           'Effect A · In Play', ZA, 'ZOOM · the hit point, same frame', ro,
           'Script: confirm, then tap jab whenever Bolt is IDLE, 8 jabs. Rivet blocks every other visible jab (his '
           'brain); his hits on Bolt burst too. Readout: _tools/film_play.gd log, node counts (log frame = movie frame + 1).')


def b16():
    b = beat('B16'); n = nframes(b)
    tp, tr = round(ct(b, 'pause') * FPS), round(ct(b, 'rew') * FPS)

    def ro(L, src, jabs):
        st = 'PAUSED' if L.get('paused') else NAMES.get(L.get('bolt'), '?')
        return [('movie frame', str(src), False), ('Bolt', st, False), ('Bolt wind', f'{L.get("wind", 0):.0f}', False),
                ('amount_ratio', f'{L.get("ratio", 0):.2f}', True)]
    motion('B16', [(0, 200, 381, 1, 'REAL SPEED · movie frames 200–381'),
                   (183, 205, 258, 2, 'REPLAY · 0.5× speed (each frame shown 2×)'),
                   (tp, 250, 305, 6, 'REPLAY · 1/6 speed (each frame shown 6×): pause, then Rivet\'s hit'),
                   (tr, 300, 381, 3, 'REPLAY · 1/3 speed (each frame shown 3×): rewind')],
           'Effect B · In Play', ZB, 'ZOOM · Bolt\'s key, same frame', ro,
           'Pause dims the screen; while paused, the only pixels that change are a 110×140 box at the key '
           '(frames 262–287). Readout: _tools/film_play.gd log (log frame = movie frame + 1).')


# ------------------------------------------------------------------ B11 Effect B intent
def b11():
    labs = ['What it tells the player, and why they need it', 'Value', 'Condition', 'Mapping',
            "Feature Effect A doesn't use"]
    r = brief_rows('### B.1 The job', labs)
    sc = brief_rows('### B.2 Intent: how it reads', ['Scale'])['Scale']
    short = {'What it tells the player, and why they need it': 'Why', "Feature Effect A doesn't use": 'Feature A lacks'}
    rows = [(short.get(l, l), r[l]) for l in labs] + [('Scale (B.2)', sc)]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect B · The Intent', 'CHANGE-BRIEF.md B.1 and B.2 · version 1 · verbatim')
        on = {0: set(), 1: {'Condition', 'Mapping'}, 2: {'Feature A lacks'}, 3: {'Scale (B.2)'}}[i]
        table(d, 340, rows, on, fsize=44, lw=500)
        footer(d, 'Claude Code\'s review note (brief B.1): amount_ratio is the one on the handout\'s list; continuous '
                  'emission and local_coords are node settings.')
        return c
    staged('B11', ['cond', 'feat', 'scale'], img)


# ------------------------------------------------------------------ B12 Effect B scene + mapping
def b12():
    WS, MG = 'godot/effects/wind_steam.tscn', 'godot/game/main.gd'

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect B · The Scene and the Mapping')
        d.text((X1, 150), 'SOURCE VIEW · c844ab2', font=F(SANSB, 44), fill=ACC, anchor='ra')
        act = {1: {37, 38}, 2: {40, 42}}.get(i, set())
        code_box(d, (X0, 300, 1700, 0), 'wind_steam.tscn · lines 35–43', code_lines(WS, 35, 43), act, size=52)
        act2 = {3: {70}, 4: {241, 242}}.get(i, set())
        y = code_box(d, (1780, 300, X1, 0), 'main.gd · lines 69–70 · attach and drive', code_lines(MG, 69, 70), act2,
                     size=52)
        code_box(d, (1780, y + 50, X1, 0), 'main.gd · lines 241–242 · the mapping', code_lines(MG, 241, 242), act2,
                 size=52)
        footer(d, 'Code may instance a scene, start it, and set amount_ratio; it does not set emission, process or draw '
                  'values (CLAUDE.md, Ownership). LOW_WIND = 25 (main.gd:15).')
        return c
    staged('B12', ['amt', 'life', '70', '241'], img)


# ------------------------------------------------------------------ B13 Effect B first strip
def b13():
    fr = [12, 20, 40, 55, 70]
    cw, chh = 660, 495
    crops = {f: strip_crop('wind_steam/r0', f, (490, 410, 610, 500), cw, chh) for f in fr}
    look = [Q('What I see and its colour: fine white misty trails rising upward, reading bright and semi-translucent '
              'against the darker background.', 'TUNING.md'),
            Q("Size compared with Bolt and his key: the entire steam rise is tall, roughly half of Bolt's height and "
              'noticeably larger than his key.', 'TUNING.md')]
    meas = Q("Measured afterwards at frame 40: the plume is 18 × 27 view px, about ¼ of Bolt's 112 px height",
             'TEST-REPORT.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect B · The First Strip')
        cap_label(d, X0, 280, 'FIXTURE CAPTURE · HELD FRAMES', 'steam_preview.tscn · fixed seed · captured by Tharun · '
                  'captures/wind_steam/r0 · zoom ×5.75')
        for k, f in enumerate(fr):
            x = X0 + k * (cw + 39)
            d.text((x, 400), f'frame {f}', font=F(SANSB, 48), fill=ACC if (i >= 2 and f == 40) else INK)
            paste_framed(c, d, crops[f], x, 470)
            if i >= 2 and f == 40:
                d.rectangle((x - 10, 460, x + cw + 9, 470 + chh + 9), outline=RING, width=10)
        y = 470 + chh + 70
        if i >= 1:
            y = card(d, (X0, y, X1), 'Tharun · first look, before Claude read the strip',
                     '\n'.join('“' + t + '”' for t in look), on=i == 1, fsize=46) + 30
        if i >= 2:
            card(d, (X0, y, X1), 'Claude · measured afterwards (TEST-REPORT A6-5c)', '“' + meas + '”  ·  Disagree on '
                 'size, by about 2× (A6-5c).', on=True, fsize=46)
        footer(d, 'amount_ratio 1.0 from frame 10, 0.0 at frame 50. Key over the darkest stretch, x 256–287 (brief D.2). Same real level art and camera as the game.')
        return c
    staged('B13', ['look', 'meas'], img)


# ------------------------------------------------------------------ B14 Effect B revision 1
def b14():
    fr = [31, 34, 38]
    cw, chh = 660, 495
    crops = {f: strip_crop('wind_steam_rewind/r0', f, B_CROP, cw, chh) for f in fr}
    obs = Q('the steam emission stopped abruptly and cut out immediately upon triggering the rewind state, rather than '
            'tapering off with a smooth fade.', 'TUNING.md')
    r34 = Q('The whole plume collapses to a thin vertical sliver, including puffs emitted before the rewind',
            'TUNING.md')
    pred = [Q('every r1 frame equals r0 wherever the key was full width in r0', 'TUNING.md'),
            Q("34: the visible difference. r0's sliver becomes a full-width plume at the key's rewind position, while "
              'the key itself is still drawn narrow.', 'TUNING.md')]
    choice = Q('fix the squash in the wiring, not with a scene setting.', 'TUNING.md')
    SM = 'godot/effects/steam_mount.gd'

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect B · Revision 1')
        y = quote_card(d, (X0, 280, X1), 'Tharun · in the running game (TEST-REPORT A6-3)', obs, on=i == 0, fsize=50)
        y += 40
        if i >= 1:
            cap_label(d, X0, y, 'FIXTURE · HELD FRAMES', 'steam_rewind_preview.tscn · rewind r0 · zoom ×4.1')
            for k, f in enumerate(fr):
                x = X0 + k * (cw + 30)
                d.text((x, y + 66), f'frame {f}', font=F(SANSB, 46), fill=ACC if f == 34 else INK)
                paste_framed(c, d, crops[f], x, y + 130)
                if f == 34:
                    d.rectangle((x - 10, y + 120, x + cw + 9, y + 130 + chh + 9), outline=RING, width=10)
            text_block(d, (X0, y + 130 + chh + 30), 'Claude, frame 34: “' + r34 + '”', F(SANS, 50), 3 * cw + 60)
        x = X0 + 3 * cw + 150
        if i >= 2:
            yy = code_box(d, (x, y, X1, 0), 'steam_mount.gd · 31–35 · Claude', code_lines(SM, 31, 35),
                          {33, 34, 35}, size=44)
            yy = text_block(d, (x, yy + 24), 'Tharun\'s choice: “' + choice + '” A holder, not local_coords = false.',
                            F(SANS, 46), X1 - x)
            if i >= 3:
                card(d, (x, yy + 24, X1), 'Claude · r1 prediction, written first',
                     '\n'.join('“' + p + '”' for p in pred), on=True, fsize=44)
        return c
    staged('B14', ['strip', 'fix', 'pred'], img)


# ------------------------------------------------------------------ B15 Effect B r0 vs r1
def b15():
    sh = Image.open(STRIP / 'wind_steam_rewind' / 'r0_vs_r1_sheet.png').convert('RGB')
    im, s = fit(sh, 3360, 840)
    fr = [28, 31, 34, 38, 46, 53, 60, 72]
    row34 = Q("1021 px differ, all in a 41 × 46 px box above the key; by eye, a full, soft plume where r0 had a sliver; "
              'the key still narrow', 'TUNING.md')
    under = Q('only 1 of the 7 strip frames taken during the rewind (34) catches the key narrow', 'TUNING.md')
    v = Q('Starting to rewind: it kept going and tapered off smoothly instead of cutting out.', 'TUNING.md')
    v2 = Q('Anything wrong: no, the steam stayed correctly anchored to the key without drifting away.', 'TUNING.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Effect B · Before and After')
        cap_label(d, X0, 280, 'FIXTURE CAPTURES · HELD FRAMES', 'captures/wind_steam_rewind/r0_vs_r1_sheet.png · top r0, '
                  'bottom r1 · sheet assembled by Claude')
        paste_framed(c, d, im, X0, 360)
        cw = im.width / 8
        for k, f in enumerate(fr):
            d.text((X0 + int(k * cw) + 20, 360 + im.height + 16), f'{f}', font=F(SANSB, 46),
                   fill=ACC if (f == 34 and i >= 1) else INK)
        d.text((X0 + im.width + 20, 360 + int(im.height * 0.2)), 'r0', font=F(SANSB, 48), fill=INK)
        d.text((X0 + im.width + 20, 360 + int(im.height * 0.7)), 'r1', font=F(SANSB, 48), fill=INK)
        if i >= 1:
            d.rectangle((X0 + int(2 * cw) - 8, 352, X0 + int(3 * cw) + 8, 368 + im.height), outline=RING, width=10)
        y = 360 + im.height + 110
        w2 = (X1 - X0 - 60) // 2
        card(d, (X0, y, X0 + w2), 'Claude · frame 34', '“' + row34 + '”\nEvery other frame: 0 px differ. Matches.',
             on=i == 1, fsize=44)
        if i >= 2:
            yy = quote_card(d, (X0 + w2 + 60, y, X1), 'Claude · what the strip under-shows', under, on=i == 2, fsize=44)
            if i >= 3:
                card(d, (X0 + w2 + 60, yy + 30, X1), 'Tharun · in the running game',
                     '“' + v + '”\n“' + v2 + '”\nVerdict: Keep.', on=True, fsize=44)
        return c
    staged('B15', ['f34', 'under', 'verdict'], img)


# ------------------------------------------------------------------ B17 the process shader
def b17():
    PS = 'godot/shaders/particles_generated.gdshader'
    sp = Q('7 (uniform float spread; declaration) and 258 (used with get_random_direction_from_spread), matching the '
           'brief setting B.3 spread = 30.0.', 'TEST-REPORT.md')
    gr = Q('43 (declaration), 302 (force = gravity;), and 315 (USERDATA1.xyz += force * DELTA; where velocity is '
           'actually updated)', 'TEST-REPORT.md')
    lives = Q('Note that this numeric value lives on the particle material resource, not directly hardcoded inside '
              'this shader file.', 'TEST-REPORT.md')
    briefs = {'spread': Q('spread | 30.0° | Godot 4 treats spread as a half-angle', 'CHANGE-BRIEF.md'),
              'gravity': Q('gravity | Vector3(0.0, -180.0, 0.0) local (−60 px/s² on screen)', 'CHANGE-BRIEF.md')}

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Process Shader', 'godot/shaders/particles_generated.gdshader · Effect B\'s ParticleProcessMaterial, '
                                       'converted in the editor by Tharun (490095f) · not used by the game')
        d.text((X1, 150), 'SOURCE VIEW', font=F(SANSB, 44), fill=ACC, anchor='ra')
        w = 2300
        y = code_box(d, (X0, 360, X0 + w, 0), 'lines 7 and 258 · spread', code_lines(PS, 7, 7) + code_lines(PS, 258, 258),
                     {258} if i >= 1 else set(), size=44)
        card(d, (X0 + w + 80, 360, X1), 'CHANGE-BRIEF B.3', briefs['spread'].replace(' | ', '  ·  '), on=i == 1, fsize=44)
        y2 = code_box(d, (X0, y + 60, X0 + w, 0), 'lines 43, 302 and 315 · gravity',
                      code_lines(PS, 43, 43) + code_lines(PS, 302, 302) + code_lines(PS, 315, 315),
                      {302, 315} if i >= 2 else set(), size=44)
        card(d, (X0 + w + 80, y + 60, X1), 'CHANGE-BRIEF B.3', briefs['gravity'].replace(' | ', '  ·  '), on=i == 2, fsize=44)
        if i >= 1:
            y3 = card(d, (X0, y2 + 50, X1), 'Tharun · line references (TEST-REPORT, "The process shader")',
                      'spread: “' + sp + '”\ngravity: “' + gr + '”', fsize=44)
            if i >= 3:
                quote_card(d, (X0, y3 + 30, X1), 'Tharun', lives, on=True, fsize=44)
        return c
    staged('B17', ['258', '302', 'mat'], img)


def lastline(p, pat):
    return [ln for ln in Path(p).read_text().splitlines() if re.search(pat, ln)][-1].strip()


# ------------------------------------------------------------------ B18 tests and mutations
def b18():
    R = REEL / 'evidence' / 'runs' / 'tests-c844ab2'
    cnt = [(t, lastline(R / f'{t}_60fps.log', r'^\d+ checks')) for t in
           ('test_impact_effect_config', 'test_wind_steam_config', 'test_impact_effect_state', 'test_wind_steam_state')]
    MU = REPO / 'evidence' / 'a6' / 'mutations'
    muts = [('M1 · Godot 3 name: initial_velocity_min to initial_velocity', 'm1-godot3-name.log'),
            ('M2 · value drift: Shards amount 16 to 12', 'm2-value-drift.log'),
            ('M4 · main.gd never frees the burst', 'state-m4-no-queue-free.log'),
            ('M5 · main.gd sets amount instead of amount_ratio', 'steam-m5-sets-amount.log'),
            ('M6 · SteamMount copies the key\'s squash', 'steam-m6-mount-copies-squash.log'),
            ('M3 · emitting = true before add_child', 'state-m3-emitting-before-tree.log')]
    rows = []
    for lab, f in muts:
        t = (MU / f).read_text()
        fails = [ln.strip() for ln in t.splitlines() if ln.startswith('FAIL')]
        rows.append((lab, fails[0] if fails else 'no FAIL line', lastline(MU / f, r'^\d+ checks')))
    spread = lastline(R / 'test_wind_steam_config_60fps.log', r'spread 30')
    grav = lastline(R / 'test_wind_steam_config_60fps.log', r'gravity \(0, -180')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What the Tests Proved', 'Re-run for this film on a clean copy of c844ab2, through scripts/run-test.sh')
        trows = [(f'{a}  {b}', TGREEN, False) for a, b in cnt] + [('', None, False), (spread, None, False),
                                                                     (grav, None, False)]
        terminal(d, (X0, 340, 1640, 1120), 'evidence/runs/tests-c844ab2/ · 60 fps', trows, size=38)
        if i >= 1:
            y = 340
            x = 1720
            d.text((x, y), 'Mutations · evidence/a6/mutations/ (Tharun ran M1, M2)', font=F(SANSB, 48), fill=INK)
            y += 80
            for k, (lab, fl, ct_) in enumerate(rows):
                last = k == len(rows) - 1
                hi = last and i >= 2
                body = (fl + '\n' if not last else '') + ct_ + ('  ·  not caught: the predicted failure did not '
                                                               'happen' if last else '')
                y = card(d, (x, y, X1), lab, body, on=hi, fsize=40, tsize=44) + 14
        card(d, (X0, 1180, 1640), 'M1: nothing else showed it', Q('Godot loaded the scene without a warning', 'TEST-REPORT.md')
             + '; ' + Q('the read-back is the only check that caught it.', 'TEST-REPORT.md'), on=False, fsize=44)
        text_block(d, (X0, 1480), 'State tests drive Bolt through the real Input path; Rivet is a stand-in brain there '
                   '(TEST-REPORT A6-2, A6-3). Each mutation was restored byte for byte.', F(SANS, 44), 1640 - X0, fill=SOFT)
        d.text((X1, 1984), '@NikBearBrown', font=F(SERIF, 56), fill=INK, anchor='ra')
        return c
    staged('B18', ['mut', 'm3'], img)


# ------------------------------------------------------------------ B19 two prices, one budget
def b19():
    log = (REPO / 'evidence' / 'a6' / 'cost' / 'cost_effects_60fps.log').read_text().splitlines()
    keep = [ln.split('   proc')[0] for ln in log if re.match(r'(empty|game_off|a_peak|b_heavy) +wall', ln)] + \
           [ln for ln in log if re.match(r'(game_off|a_peak|b_heavy) +- \S+ +wall:', ln)]
    vp = Image.open(REPO / 'evidence' / 'a6' / 'visual-profiler-vulkan.webp').convert('RGB').crop((430, 800, 830, 1210))
    vim, _ = fit(vp, 900, 930)
    bud = Q('< 0.55 ms peak for 4 concurrent bursts', 'CHANGE-BRIEF.md')
    bud2 = Q('< 0.20 ms combined for both active fighter streams, compared on GPU time', 'CHANGE-BRIEF.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Two Prices, One Budget')
        rows = [(ln, (TGREEN if ' - ' in ln else None), (' - ' in ln and ln.startswith(('a_peak', 'b_heavy'))))
                for ln in keep]
        terminal(d, (X0, 300, 2500, 1000), 'HEADLESS PRICE · evidence/a6/cost/cost_effects_60fps.log · wall clock',
                 rows, size=36)
        text_block(d, (X0, 1020), 'proc and phys (Performance.TIME_PROCESS / TIME_PHYSICS_PROCESS) read 0.0000 in every '
                   'case, so only the wall clock is used.', F(SANS, 42), 2500 - X0, fill=SOFT)
        if i >= 1:
            y = card(d, (X0, 1160, 2500), 'GPU BUDGETS · CHANGE-BRIEF F',
                     f'Effect A: {bud}\nEffect B: {bud2}\nEffects-off reference: Render Viewport 0.97 ms GPU / 0.11 ms CPU '
                     '(2026-11-08)', on=i == 1, fsize=44)
            cap_label(d, 2600, 300, 'OS SCREENSHOT · Tharun', 'effects off · crop')
            paste_framed(c, d, vim, 2600, 370)
            if i >= 2:
                d.rectangle((X0, y + 40, 2500, y + 300), fill=CARD, outline=ACC, width=8)
                d.text((X0 + 40, y + 70), 'GPU PRICE: PENDING · not measured', font=F(SANSB, 64), fill=ACC)
                d.text((X0 + 40, y + 170), 'Visual Profiler, off vs on at heaviest, per effect, in gpu_price.tscn; '
                                           'FPS with vsync off (F10) (TEST-REPORT A6-5: open).', font=F(SANS, 42), fill=INK)
        footer(d, 'Headless: the dummy renderer neither simulates nor draws GPU particles, so all that is left is node '
                  'work (TEST-REPORT A6-4). This film shows no GPU number for either effect.')
        return c
    staged('B19', ['budget', 'pending'], img)


# ------------------------------------------------------------------ B20 Claude checked, Claude overruled
def b20():
    mistakes = [('cork handler line', Q("the cork's struck handler is at main.gd:199, not 200", 'CHANGE-BRIEF.md'),
                 'CHANGE-BRIEF A6 revisions'),
                ('rewind key', Q("Claude's first key list said R for rewind; rewind is S.", 'TEST-REPORT.md'), 'A6-3'),
                ('watch loop', Q('The first loop I watched ran about 4× too fast (the loop counted display frames at '
                                 'about 120 fps)', 'TUNING.md'), 'TUNING, Effect B first look'),
                ('state test', Q('a bug in the test: it compared two bursts after both were freed', 'TEST-REPORT.md'),
                 'A6-2'),
                ('F2 probe', Q("The brief's A.4 note and the CLAUDE.md line state the probe more broadly than this result "
                               'supports.', 'TEST-REPORT.md'), 'A6-2')]
    stmt = Q('On the steam size and shard scale disagreements, I accept the objective pixel measurements—the plume is a '
             'quarter of Bolt\'s height, and the shard scale remained unchanged at 0.8–1.2. However, I keep my visual '
             'observation for gameplay evaluation: in active motion, the extended opacity timing makes the effects feel '
             'larger and more readable to the player on screen.', 'TEST-REPORT.md')
    dis = [('Effect A r1', Q('they also looked bigger on screen, even though the scale is unchanged', 'TEST-REPORT.md'),
            'Claude: scale unchanged (0.8–1.2); only opacity changed'),
           ('Effect B r0', Q("the entire steam rise is tall, roughly half of Bolt's height", 'TEST-REPORT.md'),
            'Claude: 18 × 27 view px, about ¼ of Bolt')]
    other = Q('Disagreed at first; my answer was corrected after Claude\'s measurement', 'TEST-REPORT.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Claude, Checked · Claude, Overruled')
        x0, x1 = X0, 1700
        d.text((x0, 290), 'Agent mistakes caught', font=F(SANSB, 56), fill=ACC if i == 0 else INK)
        y = 380
        for lab, q, src in mistakes:
            y = card(d, (x0, y, x1), f'{lab} · {src}', '“' + q + '”', fsize=42, tsize=44) + 18
        x = 1780
        if i >= 1:
            d.text((x, 290), 'Where Tharun\'s verdict differs (A6-5c)', font=F(SANSB, 56), fill=ACC if i == 1 else INK)
            y = 380
            for lab, q, cl in dis:
                y = card(d, (x, y, X1), lab, 'Tharun: “' + q + '”\n' + cl, on=i == 1, fsize=42, tsize=44) + 18
            if i >= 2:
                y = quote_card(d, (x, y, X1), 'Tharun · his statement, verbatim', stmt, on=i == 2, fsize=42) + 18
            if i >= 3:
                card(d, (x, y, X1), 'The other way · Effect A over the dark stretch',
                     'Tharun first: “flecks pop cleanly” · Claude measured 42 vs 105 · “' + other + '”', on=True,
                     fsize=42, tsize=44)
        return c
    staged('B20', ['diff', 'words', 'other'], img)


# ------------------------------------------------------------------ B21 credits (verbatim SOURCES.md)
def b21():
    txt = (REPO / 'SOURCES.md').read_text()
    sec = txt.split('**Who did what (A6):**', 1)[1]
    clean = lambda s: s.replace('**', '').replace('`', '')
    me, cl, cur = [], [], None
    for ln in sec.splitlines():
        if ln.startswith('- **Me (Tharun):**'):
            cur = me; continue
        if ln.startswith('- **Claude Code:**'):
            cur = cl; continue
        if cur is not None and ln.strip().startswith('- '):
            cur.append('• ' + clean(ln.strip()[2:]))
    tex = Q('Both are written by code; nothing is sourced or model-generated.', 'SOURCES.md')
    tex2 = Q("Effect A's core uses an in-scene GradientTexture2D.", 'SOURCES.md')
    help_ = Q('2026-11-08, an external LLM, Claude 3.5 Sonnet: used to draft initial bullet points for brief sections '
              'A.1–G.', 'SOURCES.md')

    def col(d, x, x1, title, items, on):
        d.text((x, 300), title, font=F(SANSB, 56), fill=ACC if on else INK)
        y = 390
        f = F(SANS, 42)
        for it in items:
            for k, ln in enumerate(wrap(d, it, f, x1 - x - 40)):
                d.text((x + (0 if k == 0 else 34), y), ln, font=f, fill=INK); y += 54
            y += 12
        assert y < 1700, ('credits overflow', title, y)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Who Did What (A6)')
        d.text((X1, 150), 'SOURCES.md · verbatim', font=F(SANSB, 44), fill=ACC, anchor='ra')
        col(d, X0, 1880, 'Tharun (human)', me, i == 0)
        col(d, 1960, X1, 'Claude Code (AI)', cl, i == 1)
        card(d, (X0, 1720, X1), 'Textures (SOURCES.md, A6) · Drafting help', f'{tex} {tex2} (ATTRIBUTION.md)  ·  {help_}', on=i == 2,
             fsize=42, tsize=44)
        return c
    staged('B21', ['claude', 'tex'], img)


BUILD = {'B02': b02, 'B03': b03, 'B04': b04, 'B06': b06, 'B07': b07, 'B08': b08, 'B09': b09, 'B10': b10,
         'B11': b11, 'B12': b12, 'B13': b13, 'B14': b14, 'B15': b15, 'B16': b16, 'B17': b17, 'B18': b18,
         'B19': b19, 'B20': b20, 'B21': b21}

if __name__ == '__main__':
    todo = list(BUILD) if sys.argv[1:] == ['all'] else sys.argv[1:]
    for bid in todo:
        BUILD[bid]()
