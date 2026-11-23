#!/usr/bin/env python3
"""Build the A7 film's own media from real files, recorded output and real engine captures only.

Every image placed here is a committed fixture strip frame or contact sheet (captures/jab_action/, fixture
godot/previews/jab_preview.tscn, captured by Tharun; sheets assembled by Claude), a committed sprite sheet
(godot/assets/props/), or a frame of one of the two Movie Maker captures made for this film on an isolated copy
of a5978c0 (capture/play-4k60.mp4: the game, scripted input; capture/key-cycle-4k60.mp4: the key_cycle_preview
fixture). Text panels are verbatim lines from repo files at a5978c0 and from logs; every quotation goes through
Q(), which asserts it is verbatim in its source file at a5978c0. This script lays them out, adds provenance labels
and switches highlight states on the spoken cue times written by patch_timing.py. It invents no output.
Helpers copied from the A6 film's make_media.py.

Usage: make_media.py all | B02 B04 ...
"""
import json, re, subprocess, sys
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
REV = 'a5978c0'
RUNS = REEL / 'evidence' / 'runs'
FONTS = Path('/Users/tharunmaheswararao/Documents/csye7270/_brutalist/runtime/fonts')
SERIF = str(FONTS / 'EB_Garamond/static/EBGaramond-Medium.ttf')
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


def badge(d, text):
    d.text((X1, 150), text, font=F(SANSB, 44), fill=ACC, anchor='ra')


def footer(d, text):
    f = F(SANS, 44)
    lines = wrap(d, text, f, 2950)
    y = 2040 - 58 * len(lines)
    for ln in lines:
        d.text((X0, y), ln, font=f, fill=SOFT); y += 58
    d.text((X1, 1984), '@NikBearBrown', font=F(SERIF, 56), fill=INK, anchor='ra')


def label(d, xy, who, path, maxw=None):
    """Provenance label above an embedded image: bold 'who', then the file path (on the next line if needed)."""
    x, y = xy
    d.text((x, y), who, font=F(SANSB, 46), fill=ACC)
    wx = d.textlength(who, font=F(SANSB, 46)) + 24
    if maxw and wx + d.textlength(path, font=F(SANS, 42)) > maxw:
        d.text((x, y + 58), path, font=F(SANS, 42), fill=SOFT)
        return y + 58 + 56
    d.text((x + wx, y + 2), path, font=F(SANS, 42), fill=SOFT)
    return y + 60


def fit(im, bw, bh, nearest=False):
    s = min(bw / im.width, bh / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                     Image.NEAREST if nearest else Image.LANCZOS), s


RECTS = {}          # beat -> image rectangles (real embedded images), for _tools/selfcheck.py masks
CUR = ['']


def put(c, im, xy):
    c.paste(im, xy)
    RECTS.setdefault(CUR[0], set()).add((xy[0], xy[1], xy[0] + im.width, xy[1] + im.height))


def paste_framed(c, d, im, x, y):
    put(c, im, (x, y))
    d.rectangle((x - 2, y - 2, x + im.width + 1, y + im.height + 1), outline=RULE, width=3)


def card(d, xy, title, body, on=False, fsize=46, tsize=48):
    x0, y0, x1 = xy
    ft, fb = F(SANS if any(ch in title for ch in '→≤≥') else SANSB, tsize), F(SANS, fsize)
    lines = []
    for para in body.split('\n'):
        lines += wrap(d, para, fb, x1 - x0 - 70)
    tl = wrap(d, title, ft, x1 - x0 - 70)
    th = int(ft.size * 1.3) * len(tl)
    hgt = 40 + th + int(fb.size * 1.32) * len(lines) + 30
    d.rectangle((x0, y0, x1, y0 + hgt), fill=CARD, outline=ACC if on else RULE, width=6 if on else 3)
    d.rectangle((x0, y0, x0 + 12, y0 + hgt), fill=ACC if on else RULE)
    for k, t in enumerate(tl):
        d.text((x0 + 40, y0 + 26 + k * int(ft.size * 1.3)), t, font=ft, fill=ACC if on else INK)
    y = y0 + 30 + th
    for ln in lines:
        d.text((x0 + 40, y), ln, font=fb, fill=INK); y += int(fb.size * 1.32)
    return y0 + hgt


def quote_card(d, xy, who, text, on=False, fsize=46):
    return card(d, xy, who, '“' + text + '”', on=on, fsize=fsize, tsize=48)


def terminal(d, xy, title, rows, size=40):
    """rows: [(text, colour or None, highlighted)]"""
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=16, fill=TERM)
    d.text((x0 + 30, y0 + 22), title, font=F(SANS, 40), fill=TBLUE)
    fm = F(MONO, size)
    lh = int(fm.size * 1.36)
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


GL_KW = (r'\b(?:extends|const|var|func|if|elif|else|for|in|while|return|and|or|not|true|false|null|'
         r'self|preload|await)\b')
GTOK = re.compile(r'("[^"\n]*"|##?[^\n]*|' + GL_KW + r'|-?\b\d+(?:\.\d+)?\b)')


def gl_line(d, x, y, text, font):
    for s in GTOK.split(text):
        if not s:
            continue
        col = TTEXT
        if s.startswith('#'):
            col = (186, 197, 188)
        elif s[0] == '"':
            col = TYELLOW
        elif re.fullmatch(r'-?\d+(?:\.\d+)?', s):
            col = TGREEN
        elif re.fullmatch(GL_KW, s):
            col = (243, 155, 206)
        d.text((x, y), s, font=font, fill=col)
        x += d.textlength(s, font=font)


@lru_cache(None)
def rev_text(path, rev=REV):
    return subprocess.run(['git', '-C', str(REPO), 'show', f'{rev}:{path}'], capture_output=True, text=True,
                          check=True).stdout


def src_lines(path, a, b, rev=REV):
    return rev_text(path, rev).splitlines()[a - 1:b]


def code_lines(path, a, b, rev=REV):
    return list(zip(range(a, b + 1), src_lines(path, a, b, rev)))


def code_box(d, box, path, rows, active=(), size=46, note=None):
    """rows: [(line_no, text)]; long lines wrap under their number. Returns bottom y."""
    x0, y0, x1, _ = box
    fm = F(MONO, size)
    lh = int(fm.size * 1.42)
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


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('**', '').replace('*', '').replace('`', '')).strip()


def Q(s, *files):
    """Assert a quoted string is verbatim in one of the files at REV ('…' separates verbatim parts). Returns s."""
    texts = [norm(rev_text(f)) for f in files]
    for part in [p.strip(' .') for p in s.split('…')]:
        if part:
            assert any(norm(part) in t for t in texts), ('not verbatim', part[:80], files)
    return s


def lastline(p, pat):
    return [ln for ln in Path(p).read_text().splitlines() if re.search(pat, ln)][-1].strip()


def md_rows(path, start, n_after=40):
    """Markdown table rows (cells, ** and ` stripped) after the line containing `start`, at REV."""
    lines = rev_text(path).splitlines()
    i = next(k for k, ln in enumerate(lines) if start in ln)
    out = []
    for ln in lines[i:i + n_after]:
        if ln.startswith('|') and not re.match(r'\|[-| ]+\|$', ln):
            out.append([norm(c) for c in ln.strip().strip('|').split('|')])
        elif out and not ln.startswith('|'):
            break
    return out


# ================================================================== A7 sources
STRIP = REPO / 'captures' / 'jab_action'
PLAY = WORK / 'play'          # frames decoded from capture/play-4k60.mp4
KEYC = WORK / 'key'           # frames decoded from capture/key-cycle-4k60.mp4
PLOG = RUNS / 'play-capture-log.txt'
KLOG = RUNS / 'key-cycle-capture-log.txt'
OFF = json.loads((RUNS / 'frame-alignment.json').read_text()) if (RUNS / 'frame-alignment.json').exists() else {}
STRIP_CROP = (330, 300, 650, 600)               # r0/r1/r2 window frames (1280x720): Bolt at x 207 view
PZ = (1290, 960, 2730, 1770)                    # 4K zoom on both fighters (view 215..455 x 160..295)


def playlog():
    rows = {}
    rx = re.compile(r'tick (\d+) frame (\d+) round (\d+) bolt (\w+) t ([\d.-]+) x ([\d.-]+) rot ([\d.-]+) '
                    r'bob ([\d.-]+) fa (\S+) fa_pos ([\d.-]+) key (\d+) ka (\S+) wind ([\d.-]+) hitstop ([\d.-]+) '
                    r'rivet (\w+) rwind ([\d.-]+) gap ([\d.-]+) hp ([\d.-]+) canvas ([\d.-]+) ([\d.-]+)')
    txt = PLOG.read_text()
    for m in rx.finditer(txt):
        rows[int(m[1])] = dict(tick=int(m[1]), frame=int(m[2]), bolt=m[4], t=float(m[5]), x=float(m[6]),
                               rot=float(m[7]), bob=float(m[8]), fa=m[9], fa_pos=float(m[10]), key=int(m[11]),
                               ka=m[12], wind=float(m[13]), hitstop=float(m[14]), rivet=m[15], gap=float(m[17]))
    cases = {}
    for m in re.finditer(r'CASE (\d) (\w+): (?:jab on tick (\d+)|S held from tick (\d+) to (\d+))', txt):
        cases[int(m[1])] = dict(name=m[2], e=int(m[3]) if m[3] else int(m[4]), end=int(m[5]) if m[5] else None)
    hits = {int(m[1]): int(m[2]) for m in re.finditer(r'CASE (\d) \w+: .* hit planned on tick (\d+)', txt)}
    return rows, cases, hits


def movie_index(tick, rows):
    """Movie Maker frame index for a physics tick (frame-alignment.json, measured)."""
    return rows[tick]['frame'] - OFF['play_frame_minus_movie']


def play_frame(tick, rows):
    return Image.open(PLAY / f'frame{movie_index(tick, rows):08d}.png').convert('RGB')


def strip_frame(run, f, box=STRIP_CROP, scale=2.0):
    im = Image.open(STRIP / run / f'frame{f:08d}.png').convert('RGB').crop(box)
    return im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)


def striplog(run):
    out = {}
    for ln in (REPO / 'logs' / f'jab_preview_{run}.log').read_text().splitlines():
        m = re.match(r'frame +(\d+) +(\w+) +state_t ([\d.]+) +clip (\S+) +([\d.]+) +x +([\d.-]+) +rot +([\d.-]+) +'
                     r'keybob +([\d.-]+) +box (\S+)', ln)
        if m:
            out[int(m[1])] = dict(state=m[2], t=m[3], clip=m[4], pos=m[5], x=m[6], rot=m[7], bob=m[8], box=m[9],
                                  line=ln.strip())
    return out


# ------------------------------------------------------------------ B02 two clips, two routes
def b02():
    rows, cases, _ = playlog()
    t_lunge = cases[1]['e'] + 6
    t_key = cases[6]['e'] + 40
    clips = md_rows('TEST-REPORT.md', '| Clip | Route | Node | Authority | Loops / commits |')
    hdr, A, Bc = clips[0], clips[1], clips[2]
    ims = []
    for t, z, tag in ((t_lunge, PZ, 'jab_action · active'), (t_key, None, 'wind_key_cycle · REWIND')):
        full = play_frame(t, rows)
        zz = z or key_zoom(rows, t)
        ims.append((t, zz, tag, full.crop(zz).resize((1100, 619), Image.LANCZOS)))

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Two Clips, Two Routes', 'Tin Knockout, Assignment 7 · TEST-REPORT.md "The two clips", verbatim')
        y = 330
        for t, z, tag, im in ims:
            yi = label(d, (X0, y), 'HELD FRAME · SCRIPTED INPUT', f"{tag} · tick {t} · zoom", maxw=1100)
            paste_framed(c, d, im, X0, yi)
            y = yi + 619 + 40
        x = X0 + 1100 + 90
        yy = 360
        for k, (row, name) in enumerate(((A, 'CLIP A · the cycle'), (Bc, 'CLIP B · the committing action'))):
            body = '\n'.join(f'{h}: {v}' for h, v in zip(hdr, row))
            yy = card(d, (x, yy, X1), name, body, on=i == k + 1, fsize=44) + 40
        footer(d, 'Film capture: Bolt through the real input path; Rivet a stand-in plan; isolated copy of a5978c0 '
                  '(CAPTURE.md).')
        return c
    staged('B02', ['a', 'b'], img)


def key_zoom(rows, t):
    """A 16:9 4K box around Bolt's key, from the logged canvas position of Bolt's feet (key anchor ≈ −42, −50)."""
    r = OFF['key_box_play']
    return tuple(r)


# ------------------------------------------------------------------ B04 Q1: mutation M1
def b04():
    MU = REPO / 'evidence' / 'a7' / 'mutations'
    row = Q('Break one track\'s subname: FacingPivot/BodyPivot:rotation → …:rotatoin in jab_action.tres',
            'evidence/a7/mutations/README.md')
    said = Q('M1: nothing about the broken track.', 'evidence/a7/mutations/README.md')
    inert = Q('The game ran with the rotation track inert and no warning: the silent failure the read-back exists for.',
              'evidence/a7/mutations/README.md')
    rb = (MU / 'M1-test_jab_action_readback.log').read_text().splitlines()
    st = (MU / 'M1-test_a7_structure.log').read_text().splitlines()
    rb_f = [ln for ln in rb if ln.startswith('FAIL')]
    st_f = [ln for ln in st if ln.startswith('FAIL')]
    rb_c = lastline(MU / 'M1-test_jab_action_readback.log', r'^\d+ checks')
    st_c = lastline(MU / 'M1-test_a7_structure.log', r'^\d+ checks')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q1 · A Renamed Property')
        badge(d, 'MUTATION M1 · its own git worktree · not in the repo')
        y = code_box(d, (X0, 300, 1780, 0), 'jab_action.tres line 22 · a5978c0', code_lines(
            'godot/animations/jab_action.tres', 22, 22), size=44)
        y = card(d, (X0, y + 40, 1780), 'M1 · evidence/a7/mutations/README.md', row, fsize=44) + 40
        if i >= 1:
            y = quote_card(d, (X0, y, 1780), 'What the engine said on its own', said, on=i == 1, fsize=44) + 30
            quote_card(d, (X0, y, 1780), 'README', inert, on=i == 1, fsize=44)
        if i >= 2:
            rows = [(ln, TRED, False) for ln in rb_f[:6]] + [(rb_c, TYELLOW, True)]
            yy = terminal(d, (1860, 300, X1, 1300), 'M1-test_jab_action_readback.log · exit 8', rows, size=34)
            if i >= 3:
                terminal(d, (1860, 1340, X1, 1900), 'M1-test_a7_structure.log · exit 2 · real Bolt and Rivet',
                         [(ln, TRED, False) for ln in st_f[:2]] + [(st_c, TYELLOW, True)], size=34)
        footer(d, 'Run by Claude in a fresh worktree at b3750b0; the main working tree was never changed '
                  '(mutations README). TEST-REPORT A7-5.')
        return c
    staged('B04', ['silent', 'rb', 'st'], img)


# ------------------------------------------------------------------ B05 Q2: one writer per node
def b05():
    P = 'godot/fighter/fighter.gd'
    act = {0: set(), 1: {67, 69, 70, 73}, 2: {68, 71}, 3: {72}, 4: {306, 313}}

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q2 · One Writer per Node')
        badge(d, f'SOURCE VIEW · godot/fighter/fighter.gd at {REV}')
        y = code_box(d, (X0, 290, X1, 0), 'fighter.gd · lines 64–73 · the rig, one writer each', code_lines(P, 64, 73),
                     act[i], size=44)
        code_box(d, (X0, y + 24, X1, 0), 'fighter.gd · lines 306–315 · _apply_pose', code_lines(P, 306, 315),
                 act[i] if i == 4 else set(), size=44)
        footer(d, Q('SteamMount only reads the key.', 'CLAUDE.md') + ' (A6 steam_mount.gd follows KeyMount; CLAUDE.md, '
                  'One authority.)')
        return c
    staged('B05', ['ap', 'fa', 'ka', '306'], img)


# ------------------------------------------------------------------ B06 Q2 result: the source scan
def b06():
    L = RUNS / 'tests-a5978c0' / 'test_a7_structure_60fps.log'
    lines = L.read_text().splitlines()
    i0 = next(k for k, ln in enumerate(lines) if ln.startswith('-- A. one authority'))
    sec = [ln for ln in lines[i0 + 1:i0 + 8] if ln.strip() and not ln.startswith('rig writes found')]
    found = re.findall(r'"fighter/fighter.gd:(\d+) (\w+) ([\w.]+)"', next(ln for ln in lines if ln.startswith('rig writes found')))
    from collections import Counter
    byfn = Counter(f for _, f, _ in found)
    per = ['fighter.gd:%s %s %s' % w for w in found if w[1] == '_apply_pose']
    gap = next(ln for ln in lines if 'largest gap' in ln and ln.startswith('PASS  one authority'))
    count = lastline(L, r'^\d+ checks')
    rows, cases, _ = playlog()
    t = cases[1]['e'] + 5
    r = rows[t]
    im = play_frame(t, rows).crop(PZ).resize((1300, 731), Image.LANCZOS)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q2 · The Source Scan', 'test_a7_structure.gd, section A · re-run for this film on a clean copy of '
                                         'a5978c0')
        trows = ([(f'rig writes found: {len(found)} — ' + ', '.join(f'{k} {v}' for k, v in byfn.items()), TMUTED, False)]
                 + [('  ' + w, None, i == 1) for w in per] + [('', None, False)]
                 + [(ln, TGREEN, i == 1 and 'after setup' in ln) for ln in sec])
        y = terminal(d, (X0, 340, 2240, 1640), 'test_a7_structure_60fps.log · section A (list counted by function; '
                     '_apply_pose entries verbatim)', trows, size=44)
        label(d, (2320, 340), 'HELD FRAME · SCRIPTED INPUT', f'film capture tick {t} (e+5)')
        paste_framed(c, d, im, 2320, 410)
        card(d, (2320, 410 + 731 + 40, X1), 'Logged pose, this tick',
             f'BodyPivot x {r["x"]:+.2f} · rotation {r["rot"]:+.3f}\nKeyBob y {r["bob"]:+.2f}\n'
             f'jab_action at {r["fa_pos"]:.4f} = state_t {r["t"]:.4f}', on=i >= 2, fsize=46)
        terminal(d, (X0, 1680, 2240, 2000), count, [(gap, TGREEN, i >= 2)], size=44)
        return c
    staged('B06', ['after', 'gap'], img)


# ------------------------------------------------------------------ B08 Q3 result: hitstop hold + CLOCKS
def b08():
    rows, cases, _ = playlog()
    e = cases[2]['e']
    ticks = list(range(e + 4, e + 13))
    crops = []
    for t in ticks:
        full = play_frame(t, rows)
        crops.append(full.crop((1500, 960, 2160, 1800)).resize((330, 420), Image.LANCZOS))
    clocks = Q('CLOCKS: display 129 fps, physics 60 ticks/s; drawn frames per tick { 0: 11, 1: 12, 2: 440, 3: 136, 4: 2 }; '
               'clip vs state_t on 279 JAB ticks: largest gap 0.000000 s', 'TEST-REPORT.md')
    trail = Q('each drawn frame shows the last completed tick, so the picture trails gameplay by less than one tick',
              'TEST-REPORT.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q3 · One Clock, Measured')
        label(d, (X0, 290), 'MOVIE MAKER CAPTURE · SCRIPTED INPUT', f'case 2 (jab lands) · ticks e+4 … e+12 · one '
                                                                     'drawn frame per tick (60 fps) · zoom on Bolt')
        x = X0
        for k, t in enumerate(ticks):
            r = rows[t]
            held = 5 <= t - e <= 10
            xx = X0 + k * (330 + 52)
            paste_framed(c, d, crops[k], xx, 370)
            if i >= 1 and held:
                d.rectangle((xx - 12, 358, xx + 330 + 11, 370 + 420 + 11), outline=RING, width=10)
            d.text((xx, 810), f'e+{t - e}', font=F(SANSB, 48), fill=ACC if (i >= 1 and held) else INK)
            d.text((xx, 870), r['bolt'], font=F(SANS, 44), fill=INK)
            d.text((xx, 930), f't {r["t"]:.4f}', font=F(MONO, 44), fill=INK)
            d.text((xx, 990), f'clip {r["fa_pos"]:.4f}' if r['fa'] != '-' else 'clip —', font=F(MONO, 44), fill=INK)
            d.text((xx, 1050), f'stop {max(r["hitstop"], 0):.3f}', font=F(MONO, 44), fill=SOFT)
        d.text((X0, 1140), 'Log lines from evidence/runs/play-capture-log.txt (t = state_t, clip = '
                           'FighterAnimPlayer position, stop = hitstop left).', font=F(SANS, 44), fill=SOFT)
        if i >= 2:
            terminal(d, (X0, 1250, X1, 1640), 'Measured windowed by Tharun · jab_preview -- --loop --clocks · '
                                              'TEST-REPORT A7-9e, verbatim', [(clocks, TGREEN, True)], size=44)
            card(d, (X0, 1680, X1), 'Picture vs gameplay (A7-9e)', trail + '.', fsize=46)
        return c
    staged('B08', ['hold', 'meas'], img)


# ------------------------------------------------------------------ B09 Q4: phase table beside key times
def b09():
    ph = md_rows('CHANGE-BRIEF.md', '| Phase | Frames (at 60 fps) |')
    keys = md_rows('evidence/a7/jab_action_keys.md', '| Key | Source frame (§4) |')
    float_note = Q('Time = frame ÷ 60, stored in the .tres as a 32-bit float (CLAUDE.md, Headless facts), so the '
                   'read-back compares within half a frame (1/120 s).', 'evidence/a7/jab_action_keys.md')
    hi = {0: set(), 1: set(), 2: {'1'}, 3: {'2', '3'}, 4: {'4'}, 5: set()}

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q4 · Feel in Frames')
        badge(d, f'CHANGE-BRIEF.md §4 · evidence/a7/jab_action_keys.md · {REV} · verbatim')
        y = 300
        d.text((X0, y), 'The phase table (Tharun, 60 fps)', font=F(SANSB, 52), fill=INK)
        y += 80
        cols = [0, 1, 2]
        widths = [700, 900, 900]
        f = F(SANS, 46)
        for k, row in enumerate(ph):
            xx = X0
            hb = k == 0
            d.rectangle((X0, y, X0 + sum(widths) + 40, y + 74), fill=(238, 234, 224) if hb else CARD, outline=RULE,
                        width=2)
            for ci, wdt in zip(cols, widths):
                d.text((xx + 20, y + 14), row[ci], font=F(SANSB, 44) if hb else f, fill=INK)
                xx += wdt
            y += 74
        y += 50
        on = i >= 1
        d.text((X0, y), 'Each key\'s time in jab_action.tres (Claude, from §4)', font=F(SANSB, 52),
               fill=ACC if i == 1 else INK)
        y += 80
        kc = [0, 1, 2, 3, 5, 6, 7]
        kw = [170, 300, 760, 420, 520, 540, 520]
        for k, row in enumerate(keys):
            if not on:
                break
            hb = k == 0
            h = hi[i] if i in hi else set()
            sel = not hb and row[0] in h
            txt = [row[ci] for ci in kc]
            if not hb:
                txt = [re.sub(r' \(was .*\)$', '', t) for t in txt]
            lines = max(len(wrap(d, t, F(SANS, 42), w - 30)) for t, w in zip(txt, kw))
            rh = 30 + 56 * lines
            d.rectangle((X0, y, X0 + sum(kw), y + rh), fill=(238, 234, 224) if hb else CARD,
                        outline=ACC if sel else RULE, width=6 if sel else 2)
            xx = X0
            for t, w in zip(txt, kw):
                yy = y + 14
                for ln in wrap(d, t, F(SANS, 42), w - 30):
                    d.text((xx + 16, yy), ln, font=F(SANSB, 42) if hb else F(SANS, 42), fill=INK); yy += 56
                xx += w
            y += rh
        if i >= 5:
            card(d, (X0, y + 30, X1), 'Why "within half a frame"', float_note, on=True, fsize=44)
        return c
    staged('B09', ['keys', 'f3', 'f5', 'f11', 'float'], img)


# ------------------------------------------------------------------ B10 Q4 result: r0 strip
def b10():
    fr = [9, 10, 13, 14, 15, 20, 21, 31]
    lg = striplog('r0')
    crops = {f: strip_frame('r0', f, scale=2.25) for f in fr}         # 720 x 675
    cw, chh = crops[9].size
    look = Q("The fighter's whole body leans back first, then pushes forward with the punch arm already extended as "
             "part of the jab picture, holds briefly, and pulls back to the starting stance.", 'TUNING.md')
    ring_at = {1: 13, 2: 15, 3: 20, 4: 21, 5: 31}
    phase = {9: 'idle', 10: 'startup · frame 0', 13: 'coil · frame 3', 14: 'startup · frame 4',
             15: 'ACTIVE · frame 5', 20: 'active · frame 10', 21: 'recovery · frame 11', 31: 'IDLE · frame 21'}

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Q4 · The Strip, r0')
        label(d, (X0, 270), 'FIXTURE CAPTURE · HELD FRAMES', 'jab_preview.tscn · x 207, light stretch · 60 fps · '
                                                            'captured by Tharun · captures/jab_action/r0 · zoom ×2.25')
        sw = 600
        for k, f in enumerate(fr):
            x = X0 + (k % 4) * (sw + 44) + 10
            y = 360 + (k // 4) * (round(sw * chh / cw) + 200)
            sm = crops[f].resize((sw, round(sw * chh / cw)), Image.LANCZOS)
            paste_framed(c, d, sm, x, y + 60)
            hot = ring_at.get(i) == f
            d.text((x, y), f'frame {f} · {phase[f]}', font=F(SANSB, 44), fill=ACC if hot else INK)
            r = lg.get(f, {})
            d.text((x, y + 60 + sm.height + 8), f'x {r.get("x", "")} rot {r.get("rot", "")}', font=F(MONO, 44),
                   fill=SOFT)
            if hot:
                d.rectangle((x - 12, y + 48, x + sm.width + 11, y + 60 + sm.height + 11), outline=RING, width=10)
        if i >= 6:
            quote_card(d, (X0 + 4 * (sw + 44) + 40, 360, X1), 'Tharun · first look, before Claude read any strip '
                       '(TUNING.md)', look, on=True, fsize=46)
        if True:
            footer(d, 'Pose under each frame from logs/jab_preview_r0.log (view px / rad). r0 is the strip before '
                      'either revision. The jab on capture frame 10 is clip frame 0 (CHANGE-BRIEF §9).')
        return c
    staged('B10', ['f13', 'f15', 'f20', 'f21', 'f31', 'look'], img)


# ------------------------------------------------------------------ B11 the generator
def b11():
    P = 'godot/tools/generate_key_sheets.gd'
    act = {0: set(), 1: {38, 39, 40}, 2: {43, 44, 45}, 3: {46, 47}}

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Sheet · Its Recipe')
        badge(d, f'SOURCE VIEW · {P} at {REV}')
        y = code_box(d, (X0, 300, 2700, 0), 'generate_key_sheets.gd · lines 37–47', code_lines(P, 37, 47), act[i],
                     size=46)
        yy = 300
        for lab, val in (('Recipe', 'CHANGE-BRIEF §2 (Tharun): 8 cells of 84 × 60 in one row; '
                                    'w = max(0.15, |cos θ|); cells 3–5 mirrored'),
                         ('Written by', 'Claude Code (A7 Step 3); the source PNGs are never modified (lines 1–17)'),
                         ('Filter', 'Lanczos: Claude\'s choice; the brief does not name one (line 14)')):
            yy = card(d, (2780, yy, X1), lab, val, fsize=44) + 30
        footer(d, Q('godot --headless --path godot --script res://tools/generate_key_sheets.gd',
                    'godot/assets/props/ATTRIBUTION.md') + '  ·  rerun it to reproduce the sheets (ATTRIBUTION.md)')
        return c
    staged('B11', ['39', '44', '47'], img)


# ------------------------------------------------------------------ B12 the sheet itself
def b12():
    sheets = [('key-bolt-sheet.png', Image.open(REPO / 'godot/assets/props/key-bolt-sheet.png').convert('RGBA')),
              ('key-rivet-sheet.png', Image.open(REPO / 'godot/assets/props/key-rivet-sheet.png').convert('RGBA'))]
    meas = Q('every cell is centred at x 41.5 or 42.0 of 84, a half-pixel difference for the odd-width cells, 0.17 '
             'view px at the key\'s 1/3 scale.', 'TEST-REPORT.md')
    src = Q('key-bolt.png and key-rivet.png were generated in Assignment 2 with SDXL-Turbo', 'godot/assets/props/ATTRIBUTION.md')
    lic = Q('Licence: Stability AI Non-Commercial Research Community License, the same terms as all of this project\'s '
            'SDXL-Turbo art (SOURCES.md). Each sheet is a derivative of its source key, made by resizing and mirroring '
            'only.', 'godot/assets/props/ATTRIBUTION.md')
    S = 5
    ims = []
    for name, im in sheets:
        bg = Image.new('RGBA', im.size, (32, 37, 49, 255))
        bg.alpha_composite(im)
        ims.append((name, bg.convert('RGB').resize((im.width * S, im.height * S), Image.NEAREST)))

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Sheet · Sliced 8 × 1')
        y = 300
        for name, im in ims:
            label(d, (X0, y), 'COMMITTED SPRITE SHEET', f'godot/assets/props/{name} · 672 × 60 · shown ×5, '
                                                       'nearest neighbour, on a dark backdrop')
            paste_framed(c, d, im, X0, y + 70)
            for k in range(9):
                xx = X0 + k * 84 * S
                d.line((xx, y + 70, xx, y + 70 + im.height), fill=ACC, width=4)
            for k in range(8):
                xx = X0 + k * 84 * S
                d.text((xx + 14, y + 70 + im.height + 10), f'{k} · {k * 45}°', font=F(SANSB, 44),
                       fill=ACC if (i >= 1 and k in (2, 6)) else INK)
                if i >= 1 and k in (2, 6):
                    d.rectangle((xx - 4, y + 62, xx + 84 * S + 4, y + 78 + im.height), outline=RING, width=10)
            y += 70 + im.height + 110
        if i >= 2:
            y = card(d, (X0, y + 10, X1), 'Registration, measured (Claude, evidence/a7/sheets/; TEST-REPORT A7-9c)',
                     meas, on=i == 2, fsize=46) + 30
        if i >= 3:
            card(d, (X0, y, X1), 'Source and licence (godot/assets/props/ATTRIBUTION.md)', src + ' … from a prompt by '
                 'Tharun.\n' + lic, on=True, fsize=46)
        footer(d, 'Cell k is the key turned k × 45° (generate_key_sheets.gd:38-39); cells 3–5 are mirrored (lines 44-45). '
                  'KeyAnimPlayer\'s frame track picks one cell per key.')
        return c
    staged('B12', ['edge', 'meas', 'src'], img)


# ------------------------------------------------------------------ B13 the frame track
def b13():
    P = 'godot/animations/wind_key_cycle.tres'
    act = {0: set(), 1: {6, 7}, 2: {11}, 3: {17}, 4: {5, 15}}
    ans2 = Q('Sprite2D.frame is an integer property, so leaving a frame track on UPDATE_CONTINUOUS does not blend '
             'textures; instead, linear interpolation sweeps rapidly through every intermediate cell between the two '
             'keyed frames.', 'CHANGE-BRIEF.md')
    seam = Q('Frame 0 is not duplicated at t = length (1.000 s); the trailing gap from the last key (7 / 8.0 = 0.875 s) '
             'to length (1.000 s) equals one frame interval (1 / 8.0 = 0.125 s)', 'CHANGE-BRIEF.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'The Cycle · Its Frame Track')
        badge(d, f'SOURCE VIEW · {P} at {REV}')
        code_box(d, (X0, 300, 2500, 0), 'wind_key_cycle.tres · lines 3–19', code_lines(P, 3, 19), act[i], size=46)
        y = 300
        if i >= 3:
            y = quote_card(d, (2580, y, X1), 'CHANGE-BRIEF §11, answer 2', ans2, on=i == 3, fsize=44) + 30
        if i >= 4:
            quote_card(d, (2580, y, X1), 'CHANGE-BRIEF §3, the seam rule', seam, on=True, fsize=44)
        footer(d, 'loop_mode 1 = Animation.LOOP_LINEAR; update 1 = UPDATE_DISCRETE (CHANGE-BRIEF §3).')
        return c
    staged('B13', ['6', '11', '17', '15'], img)


# ------------------------------------------------------------------ motion beats (B14, B19, B20)
def motion(bid, segs, title, src_dir, zoom_of, readout, cap_label, footer_text, overlay=None):
    """segs: [(start_s, [source movie indices], label)]; a segment shorter than its slot repeats its sequence
    (label '· repeat'). zoom_of(src) -> 4K box. readout(src) -> [(key, value, big)]. The ZOOM is the big view;
    the whole frame is shown small with the zoom box ringed."""
    CUR[0] = bid
    b = beat(bid); n = nframes(b)
    starts = [round(s * FPS) for s, _, _ in segs] + [n]
    seq = []
    for k, (_, srcs, lab) in enumerate(segs):
        for j in range(starts[k + 1] - starts[k]):
            rep = j // len(srcs)
            seq.append((srcs[j % len(srcs)], lab + (f' · repeat {rep}' if rep else ''), k))
    VW, VH = 2304, 1296
    base = canvas(); d = ImageDraw.Draw(base)
    header(d, title)
    label(d, (X0, 280), cap_label[0], cap_label[1])
    d.rectangle((X0 - 2, 358, X0 + VW + 1, 360 + VH + 1), outline=RULE, width=3)
    px = X0 + VW + 70
    pw = X1 - px
    ZH = round(pw * 9 / 16)
    d.text((px, 300), 'WHOLE FRAME · zoom box ringed', font=F(SANSB, 44), fill=ACC)
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
    s = pw / 3840
    for src, mode, k in seq:
        z = zoom_of(src)
        key = (src, z)
        if key not in cache:
            cache.clear()
            full = Image.open(src_dir / f'frame{src:08d}.png').convert('RGB')
            cache[key] = (full.crop(z).resize((VW, VH), Image.LANCZOS), full.resize((pw, ZH), Image.LANCZOS))
        c = base.copy(); dd = ImageDraw.Draw(c)
        c.paste(cache[key][0], (X0, 360))
        c.paste(cache[key][1], (px, 360))
        dd.rectangle((px + int(z[0] * s), 360 + int(z[1] * s), px + int(z[2] * s), 360 + int(z[3] * s)),
                     outline=RING, width=5)
        y = 360 + ZH + 40
        for key_, val, big in readout(src):
            dd.text((px, y), key_, font=F(SANS, 44), fill=SOFT)
            dd.text((px + 420, y - (12 if big else 0)), val, font=F(SANSB, 60 if big else 46), fill=ACC if big else INK)
            y += 78 if big else 62
        y += 10
        for ln in wrap(dd, mode, F(SANSB, 46), pw):
            dd.text((px, y), ln, font=F(SANSB, 46), fill=ACC if ('REPLAY' in mode or 'HELD' in mode or 'SETUP' in mode)
                    else SOFT); y += 60
        if overlay:
            overlay(c, dd, src, k)
        pr.stdin.write(c.tobytes())
    pr.stdin.close(); pr.wait()
    print('wrote', out, n, 'frames')


def keylog():
    out = {}
    for ln in KLOG.read_text().splitlines():
        m = re.match(r'frame +(\d+) +(\w+) +state_t ([\d.]+) +key frame (\d) +wraps (\d+)', ln)
        if m:
            out[int(m[1])] = dict(state=m[2], t=float(m[3]), key=int(m[4]), wraps=int(m[5]))
    return out


def b14():
    b = beat('B14')
    kl = keylog()
    off = OFF['key_tick_minus_movie']          # preview log tick = movie index + off
    last = max(int(p.stem[5:]) for p in KEYC.glob('frame*.png'))
    zb = tuple(OFF['key_box_preview'])
    look = Q('Over five or more turns in preview and while holding S at low wind in game, the key rotation stays '
             'continuous across the wrap without a visible jump at the seam.', 'TEST-REPORT.md')
    # the first wrap after the 5th (7 -> 0): replay around it at 0.25x (each 60 fps frame twice at 30 fps)
    w5 = min(t for t, r in kl.items() if r['wraps'] >= 5)
    a = w5 - off - 20
    segs = [(0.0, list(range(0, last + 1, 2)), 'REAL SPEED · every 2nd tick of a 60 fps capture'),
            (ct(b, 'wrap'), [f for f in range(a, a + 36) for _ in range(2)], 'REPLAY · 0.25× (each tick shown twice) '
                                                                            '· a wrap, 7 to 0')]

    def ro(src):
        r = kl.get(src + off, {})
        return [('tick', str(src + off), False), ('state', r.get('state', '—'), False),
                ('state_t', f'{r.get("t", 0):.4f}', False), ('key frame', str(r.get('key', '—')), True),
                ('wraps 7 → 0', str(r.get('wraps', '—')), True)]

    def ov(c, dd, src, k):
        if src + off >= 0 and beat_t[0] >= ct(b, 'check'):
            pass
    beat_t = [0]
    motion('B14', segs, 'The Cycle · Turning', KEYC, lambda s: zb, ro,
           ('FIXTURE · MOVIE MAKER CAPTURE', 'key_cycle_preview.tscn · made for this film'),
           'Isolated copy of a5978c0; the fixture tops wind to 50 each tick. Readout: its per-tick log. Tharun (TEST-REPORT '
           'A7-9a): “' + look + '”')


def b19():
    b = beat('B19')
    rows, cases, _ = playlog()
    by_frame = {movie_index(t, rows): t for t in rows}
    fight = int(re.search(r'FIGHT at tick (\d+)', PLOG.read_text())[1])

    def rng(a, z, step=1, rep=1):
        return [movie_index(t, rows) for t in range(a, z + 1, step) for _ in range(rep)]
    e1, e2 = cases[1]['e'], cases[2]['e']
    segs = [(0.0, rng(fight, e2 + 50, 2), 'REAL SPEED · from FIGHT through cases 1 and 2 · every 2nd tick'),
            (ct(b, 'whiff'), rng(e1 - 4, e1 + 24, 1), 'REPLAY · 0.5× (one tick per film frame) · case 1, whiff at gap 90'),
            (ct(b, 'land'), rng(e2 - 4, e2 + 30, 1, 2), 'REPLAY · 0.25× (each tick shown twice) · case 2, lands at gap 70')]

    def ro(src):
        t = by_frame.get(src)
        r = rows.get(t, {})
        e = e2 if t is not None and t >= e2 - 40 else e1
        rel = f'e{t - e:+d}' if t is not None and t >= e1 - 24 else 'before case 1'
        return [('tick', f'{t} ({rel})', False), ('Bolt', r.get('bolt', '—'), True),
                ('state_t', f'{r.get("t", 0):.4f}', False),
                ('clip', f'{r["fa"]} {r["fa_pos"]:.4f}' if r.get('fa', '-') != '-' else 'none · rig at rest', False),
                ('BodyPivot x', f'{r.get("x", 0):+.2f}', False),
                ('hitstop', 'yes' if r.get('hitstop', 0) > 0 else 'no', False)]
    motion('B19', segs, 'Both Clips in Play · The Jab', PLAY, lambda s: PZ, ro,
           ('MOVIE MAKER CAPTURE · SCRIPTED INPUT', 'made for this film · isolated copy of a5978c0 · 60 fps'),
           'capture/play-4k60.mp4. Bolt: key events through Input.parse_input_event. Rivet: a stand-in plan '
           '(test_a7_edges.gd\'s method). Positions SET between cases (SETUP). Readout: _tools/film_a7_play.gd log.')


def b20():
    """Cases 3-5 side by side, synchronised on each jab's start tick e, at 0.25x and looped (labelled); then case 6
    (REWIND) as a single zoomed view at real speed."""
    CUR[0] = 'B20'
    b = beat('B20'); n = nframes(b)
    rows, cases, hits = playlog()
    by_frame = {movie_index(t, rows): t for t in rows}
    lab = {3: 'startup', 4: 'active', 5: 'recovery'}
    rel = list(range(-6, 24))                    # e-6 .. e+23, each tick twice: 0.25x
    seq_rel = [r for r in rel for _ in range(2)]
    t_rew = round(ct(b, 'rew') * FPS)
    s6 = cases[6]['e']
    rew_src = [movie_index(t, rows) for t in range(s6 - 10, cases[6]['end'] + 21, 2)]
    kz = tuple(OFF['key_box_play'])
    cues = [ct(b, k) for k in ('start', 'act', 'rec', 'each')]
    PW, PH = 1100, 1100                         # square crops around the two fighters
    CB = (1560, 900, 2580, 1920)               # 4K box, 1020 x 1020: Bolt at x 300 (1800), Rivet at 390 (2340)
    base = canvas(); d = ImageDraw.Draw(base)
    header(d, 'Both Clips in Play · Interrupts and Rewind')
    label(d, (X0, 280), 'MOVIE MAKER CAPTURE · SCRIPTED INPUT', 'made for this film · isolated copy of a5978c0 · 60 fps '
                                                               '· capture/play-4k60.mp4')
    footer(d, 'Rivet\'s cutlass (reach 78) lands on its 9th tick, so it is requested on e+k−9 (test_a7_edges.gd E3). '
              'Positions SET between cases. Readout: _tools/film_a7_play.gd log.')
    WORK.mkdir(parents=True, exist_ok=True)
    xs = [X0 + 24 + k * (PW + 66) for k in range(3)]     # rings (x − 14) stay inside the title-safe edge
    RECTS['B20'] = {(x, 440, x + PW, 440 + PH) for x in xs} | {(X0, 360, X0 + 2304, 360 + 1296)}
    (WORK / 'B20-masks.json').write_text(json.dumps(sorted(RECTS['B20'])))
    out = REEL / 'media' / 'B20.mp4'
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                           '-pix_fmt', 'yuv420p', '-an', str(out)], stdin=subprocess.PIPE)
    cache = {}

    def get(src, box, size):
        k = (src, box, size)
        if k not in cache:
            if len(cache) > 12:
                cache.clear()
            cache[k] = Image.open(PLAY / f'frame{src:08d}.png').convert('RGB').crop(box).resize(size, Image.LANCZOS)
        return cache[k]
    rew_base = canvas(); rd = ImageDraw.Draw(rew_base)
    header(rd, 'Both Clips in Play · Interrupts and Rewind')
    label(rd, (X0, 280), 'MOVIE MAKER CAPTURE · SCRIPTED INPUT', 'case 6 · S held · zoom on Bolt\'s key · REAL SPEED, '
                                                                'every 2nd tick')
    footer(rd, 'Bolt\'s wind 40 after five jabs; each ratchet click adds 10 (fighter.gd:31). Readout: _tools/film_a7_play.gd log.')
    for j in range(n):
        ts = j / FPS
        if j < t_rew:
            c = base.copy(); dd = ImageDraw.Draw(c)
            r_ = seq_rel[j % len(seq_rel)]
            loop = j // len(seq_rel)
            on = sum(1 for q in cues if ts >= q)
            for k, cs in enumerate((3, 4, 5)):
                e, h = cases[cs]['e'], hits[cs]
                t = e + r_
                x = xs[k]
                c.paste(get(movie_index(t, rows), CB, (PW, PH)), (x, 440))
                hot = (on == k + 1) or on >= 4
                dd.rectangle((x - 2, 438, x + PW + 1, 440 + PH + 1), outline=RULE, width=3)
                if hot:
                    dd.rectangle((x - 14, 426, x + PW + 13, 440 + PH + 13), outline=RING, width=10)
                dd.text((x, 370), f'case {cs} · hit on e+{h - e} · {lab[cs]}', font=F(SANSB, 46),
                        fill=ACC if hot else INK)
                r = rows[t]
                y = 440 + PH + 30
                dd.text((x, y), f'e{r_:+d}   Bolt {r["bolt"]}', font=F(SANSB, 50), fill=ACC if r['bolt'] == 'HURT' else INK)
                dd.text((x, y + 70), (f'clip {r["fa_pos"]:.4f}  x {r["x"]:+.2f}' if r['fa'] != '-' else
                                      'no clip · rig at rest 0 / 0 / 0'), font=F(MONO, 44), fill=INK)
            dd.text((X0, 1800), 'REPLAY · 0.25× (each tick shown twice), all three synchronised on their own jab start e'
                    + (f' · repeat {loop}' if loop else ''), font=F(SANSB, 46), fill=ACC)
        else:
            c = rew_base.copy(); dd = ImageDraw.Draw(c)
            k = (j - t_rew) % len(rew_src)
            src = rew_src[k]
            t = by_frame[src]
            r = rows[t]
            c.paste(get(src, kz, (2304, 1296)), (X0, 360))
            RECTS['B20'].add((X0, 360, X0 + 2304, 360 + 1296))
            dd.rectangle((X0 - 2, 358, X0 + 2305, 360 + 1297), outline=RULE, width=3)
            px = X0 + 2304 + 80
            y = 380
            for key_, val, big in (('tick', str(t), False), ('Bolt', r['bolt'], True), ('wind', f'{r["wind"]:.0f}', True),
                                   ('key frame', str(r['key']), True),
                                   ('key clip', 'wind_key_cycle' if r['ka'] != '-' else 'none · frame 0', False)):
                dd.text((px, y), key_, font=F(SANS, 44), fill=SOFT)
                dd.text((px, y + 56), val, font=F(SANSB, 64 if big else 46), fill=ACC if big else INK)
                y += 170
            if (j - t_rew) >= len(rew_src):
                dd.text((px, y), f'repeat {(j - t_rew) // len(rew_src)}', font=F(SANSB, 46), fill=ACC)
        pr.stdin.write(c.tobytes())
    pr.stdin.close(); pr.wait()
    print('wrote', out, n, 'frames')


# ------------------------------------------------------------------ B15 revision 1: reading, change, prediction
def b15():
    P = 'godot/animations/jab_action.tres'
    before = src_lines(P, 15, 15, '8a9dbed^')[0]
    after = src_lines(P, 15, 15)[0]
    r1 = Q('The recovery ends in a stall, then a pop. The ease-out (0.5) from frame 11 covers most of the distance by '
           'frame 26. Frames 27–30 barely move, then frame 31 swaps to the idle image, so the return reads as stop, '
           'then snap.', 'TUNING.md')
    chg = Q('key 4 (frame 11), outgoing transition 0.5 (ease-out) → 1.0 (linear), on all three tracks. No key time or '
            'value changes.', 'TUNING.md')
    pred = Q('Frames 22–30: x = 7.2, 6.4, 5.6, 4.8, 4.0, 3.2, 2.4, 1.6, 0.8 px (r0: 6.48, 5.12, 3.92, 2.88, 2.00, '
             '1.28, 0.72, 0.32, 0.08). Frame 26 is still visibly forward (4.0 px, was 2.0), and the body is still moving '
             'on frame 30.', 'TUNING.md')
    lg = striplog('r0')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Revision 1 · Claude\'s Reading', 'TUNING.md "A7 jab_action, revision 1" · written before any change')
        quote_card(d, (X0, 340, 1880), 'Claude · reading of r0 (a claim, not a check)', r1, on=i == 0, fsize=44)
        terminal(d, (X0, 900, 1880, 1990), 'logs/jab_preview_r0.log · frames 21–31 · columns frame, state, x, rot',
                 [(f'frame {f}  {lg[f]["state"]:<5} x {lg[f]["x"]:>5}  rot {lg[f]["rot"]}', TGREEN if 27 <= f <= 30 else None,
                   27 <= f <= 30) for f in range(21, 32)], size=44)
        x = 1960
        y = 340
        y = code_box(d, (x, y, X1, 0), 'jab_action.tres line 15 · before (8a9dbed^)', [(15, before)], size=36)
        y = code_box(d, (x, y + 20, X1, 0), f'after (8a9dbed, still at {REV})', [(15, after)], {15} if i >= 1 else set(),
                     size=36)
        if i >= 1:
            y = quote_card(d, (x, y + 30, X1), 'The one change (approved by Tharun)', chg, on=i == 1, fsize=42) + 30
        if i >= 2:
            quote_card(d, (x, y, X1), 'Claude · prediction for r1, before the edit', pred, on=True, fsize=42)
        return c
    staged('B15', ['chg', 'pred'], img)


# ------------------------------------------------------------------ B16 revision 1 result
def b16():
    sh = Image.open(STRIP / 'r1_recovery_sheet.png').convert('RGB')
    im, s = fit(sh, X1 - X0, 560)
    rows = md_rows('TUNING.md', '| Prediction | r1 | Match |')
    keep = Q('Revision 1 verdict: Keep. The return carries into the stance.', 'TUNING.md')
    opens = Q('Opens revision 2: The retraction pop is still noticeable—especially up close—and mashing J to chain jabs '
              'feels abrupt alongside the image swaps into and out of the jab pose.', 'TUNING.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Revision 1 · Result')
        label(d, (X0, 270), 'FIXTURE CAPTURE · HELD FRAMES', 'captures/jab_action/r1_recovery_sheet.png · frames 21–31 '
                                                            '· captured by Tharun · sheet assembled by Claude')
        paste_framed(c, d, im, X0, 340)
        y = 340 + im.height + 50
        if i >= 1:
            for r in (rows[1], rows[4]):
                y = card(d, (X0, y, 2300), 'Claude\'s comparison · ' + r[2], 'Predicted: ' + r[0] + '\nr1: ' + r[1],
                         on=i == 1, fsize=40, tsize=44) + 14
        x = 2380
        yy = 340 + im.height + 50
        if i >= 2:
            yy = quote_card(d, (x, yy, X1), 'Tharun · in the running game', keep, on=i == 2, fsize=46) + 30
        if i >= 3:
            quote_card(d, (x, yy, X1), 'Tharun · the same note', opens, on=True, fsize=46)
        return c
    staged('B16', ['cmp', 'verdict', 'open'], img)


# ------------------------------------------------------------------ B17 revision 2: Tharun's observation
def b17():
    P = 'godot/animations/jab_action.tres'
    obs = Q('The retraction pop is still noticeable—especially up close', 'TUNING.md')
    where = Q('clip frames 10 → 11 (capture frames 20 → 21). In one frame the body drops from +14 px to +8 px and the '
              'lean from 0.12 to 0.05 rad; in r1 the helmet centre moved −23 window px on frame 21 (measured), against '
              'about 2.5 per frame through the rest of the recovery.', 'TUNING.md')
    pred = Q('Frame 21: pose +12 px / 0.10 rad; the helmet centre steps about −8 window px (r1: −23), so the release '
             'reads as a short step, not a jump.', 'TUNING.md')
    pred2 = Q('the helmet steps about 4.3 window px each frame (r1: about 2.5)', 'TUNING.md')
    ln = (17, 29, 41)
    before = [(n, src_lines(P, n, n, 'a1d6072^')[0]) for n in ln]
    after = [(n, src_lines(P, n, n)[0]) for n in ln]
    disagree = md_rows('TEST-REPORT.md', "| Claude's reading | Tharun in play | Agreed? |")[1]

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Revision 2 · Tharun\'s Observation')
        y = quote_card(d, (X0, 300, 1880), 'Tharun · in play, after revision 1 (TUNING.md)', obs, on=i == 0, fsize=50) + 30
        y = card(d, (X0, y, 1880), 'TEST-REPORT A7-9f · Agreed?', disagree[2], on=i == 0, fsize=42) + 30
        if i >= 1:
            quote_card(d, (X0, y, 1880), 'Claude · where the pop comes from', where, on=i == 1, fsize=42)
        x = 1960
        yy = 300
        yy = code_box(d, (x, yy, X1, 0), 'jab_action.tres · values · before (a1d6072^)', before, size=34)
        yy = code_box(d, (x, yy + 20, X1, 0), f'after (a1d6072, still at {REV}) · key 4 = frame 11', after,
                      set(ln) if i >= 2 else set(), size=34)
        if i >= 3:
            quote_card(d, (x, yy + 30, X1), 'Claude · prediction for r2, before the edit', pred + ' … ' + pred2,
                       on=True, fsize=42)
        footer(d, 'Key 4 is clip frame 11 = strip capture frame 21 (CHANGE-BRIEF §4, §9). Source: TUNING.md "A7 jab_action, '
                  'revision 2", written before the edit; approved by Tharun.')
        return c
    staged('B17', ['trace', 'chg', 'pred'], img)


# ------------------------------------------------------------------ B18 revision 2 result
def b18():
    sh = Image.open(STRIP / 'r1_vs_r2_sheet.png').convert('RGB')
    im, s = fit(sh, 2000, 1000)
    rows = md_rows('TUNING.md', '| Prediction | r2 (measured) | Match |')
    obs = Q('Up close against Rivet, the retraction feels less jarring and less like a sudden snap-back than before, '
            'while the underlying jab pose swaps, close-quarters hit/rewind transitions, and spring depletion/KO flow '
            'still read brisk and punchy.', 'TUNING.md')
    a78 = md_rows('TEST-REPORT.md', '| Revision | Driven by | Change |')
    keep2 = a78[2][-1]
    pick = {1: 1, 2: 3, 3: 5}

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Revision 2 · Result')
        label(d, (X0, 270), 'FIXTURE CAPTURES · HELD FRAMES', 'captures/jab_action/r1_vs_r2_sheet.png · top r1, bottom '
                                                             'r2 · captured by Tharun · sheet assembled by Claude')
        paste_framed(c, d, im, X0, 340)
        if i >= 1:
            cw = im.width / 5
            d.rectangle((X0 + int(cw) - 8, 332, X0 + int(2 * cw) + 8, 348 + im.height), outline=RING, width=10)
        x = X0 + im.width + 70
        y = 340
        for k in (1, 2, 3):
            if i >= k:
                r = rows[pick[k]]
                y = card(d, (x, y, X1), 'Claude · ' + r[2].split(':')[0], 'Predicted: ' + r[0] + '\nr2: ' + r[1],
                         on=i == k, fsize=40, tsize=44) + 16
        if i >= 4:
            yy = 340 + im.height + 60
            quote_card(d, (X0, yy, X0 + im.width), 'Tharun · in the running game, after r2 (TUNING.md)', obs, on=True,
                       fsize=44)
            card(d, (x, max(y, yy), X1), 'Verdict (Tharun) · TEST-REPORT A7-8', keep2, on=True, fsize=56, tsize=44)
        return c
    staged('B18', ['f21', 'steps', 'cost', 'tharun'], img)


# ------------------------------------------------------------------ B21 tests + mutations + the limit
def b21():
    R = RUNS / 'tests-a5978c0'
    cnt = [(f'{t} {fps}', lastline(R / f'{t}_{fps}fps.log', r'^\d+ checks')) for t, fps in
           (('test_wind_key_cycle_readback', 60), ('test_jab_action_readback', 60), ('test_a7_structure', 60),
            ('test_a7_structure', 30), ('test_a7_edges', 60), ('test_a7_pins', 60), ('test_a7_pins', 30))]
    mut = md_rows('TEST-REPORT.md', '| # | Mutation | Test, exit | Caught by |')
    pins = [lastline(R / f'{t}_60fps.log', r'^\d+ checks') for t in ('test_slice', 'test_wind_steam_state')]
    limit = Q('A headless run advances clips and reads their structure. It draws nothing, so whether the motion reads '
              'is not observable here.', 'CLAUDE.md')
    m3 = Q('M3: a plain ERROR: Index p_frame = 8 is out of bounds, which the wrapper does not fail on. Only the '
           'read-back caught it.', 'TEST-REPORT.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'What the Tests Proved', 'Re-run for this film on a clean copy of a5978c0, through scripts/run-test.sh')
        terminal(d, (X0, 340, 1640, 1180), 'evidence/runs/tests-a5978c0/', [(f'{a}: {b}', TGREEN, False) for a, b in cnt],
                 size=38)
        if i >= 1:
            x, y = 1720, 340
            d.text((x, y), 'Mutations · TEST-REPORT A7-5 (evidence/a7/mutations/)', font=F(SANSB, 48), fill=INK)
            y += 80
            for r in mut[1:]:
                last = r[0] == 'M4'
                y = card(d, (x, y, X1), f'{r[0]} · {r[1]}', f'{r[2]} · {r[3]}', on=(last and i >= 2),
                         fsize=38, tsize=42) + 14
        if i >= 1:
            card(d, (X0, 1230, 1640), 'What the engine said (A7-5)', m3, fsize=42)
        if i >= 3:
            card(d, (X0, 1640, X1), 'What no headless run can show (CLAUDE.md, Headless facts)', limit, on=True,
                 fsize=48)
        else:
            footer(d, 'The four planned pin updates (test_wind_steam_state.gd:149, 159; test_slice.gd:182, 187) went in '
                      f'their own commit (A7-3). Re-run here: test_slice {pins[0]}; test_wind_steam_state {pins[1]}.')
        return c
    staged('B21', ['mut', 'm4', 'limit'], img)


# ------------------------------------------------------------------ B22 agent mistakes, the seam bug
def b22():
    mistakes = [Q("Claude's expectations in the pins were wrong twice (defender hitstop e+29, EMPTY 97 ticks).",
                  'TEST-REPORT.md'),
                Q('The pins first hard-coded the scheduled ticks and failed at 30 fps.', 'TEST-REPORT.md'),
                Q('flagged a read of key_sprite.texture as a write', 'TEST-REPORT.md'),
                Q('The edge test expected the row before a hit on e+21 to be IDLE. The jab ends and the hit lands on the '
                  'same tick.', 'TEST-REPORT.md'),
                Q("Claude's revision 2 prediction overestimated the helmet steps by about 10 %.", 'TEST-REPORT.md')]
    seam = [Q('the first run of godot/previews/key_cycle_preview.tscn, which holds REWIND with wind kept low so the key '
              'turns non-stop, logged 7 → 1 → 0 at every wrap after the first.', 'TEST-REPORT.md'),
            Q('Cause: _sync_clips sought the clip backwards across the wrap (float rounding put state_t at 1.99999…), '
              'and a backward seek on a discrete track shows the next key.', 'TEST-REPORT.md'),
            Q('Why the suite was green: the structure test stopped at 1.5 turns, and the read-back used advance().',
              'TEST-REPORT.md')]
    SE = REPO / 'evidence' / 'a7' / 'seam'
    bef = [ln for ln in (SE / 'structure_before_fix_60fps.log').read_text().splitlines() if ln.startswith('FAIL')]
    bc = lastline(SE / 'structure_before_fix_60fps.log', r'^\d+ checks')
    ac = lastline(SE / 'structure_after_fix_60fps.log', r'^\d+ checks')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Claude, Checked', 'TEST-REPORT A7-11 and A7-9a · verbatim')
        y = 340
        for m in mistakes:
            y = card(d, (X0, y, 1700), 'Agent mistake · caught', m, on=i == 0, fsize=40, tsize=40) + 14
        x = 1780
        if i >= 1:
            yy = 340
            yy = card(d, (x, yy, X1), 'The seam bug (fix approved by Tharun, b4046b1)', '\n'.join(seam), on=i == 1,
                      fsize=40, tsize=44) + 24
            if i >= 2:
                terminal(d, (x, yy, X1, 1960), 'evidence/a7/seam/ · test_a7_structure B7, six turns',
                         [('before the fix:', TMUTED, False)] + [(ln, TRED, False) for ln in bef[:3]] +
                         [(bc, TYELLOW, False), ('after the fix:', TMUTED, False), (ac, TGREEN, True)], size=32)
        return c
    staged('B22', ['seam', 'reg'], img)


# ------------------------------------------------------------------ B23 Claude overruled; Tharun's checks
def b23():
    rows = md_rows('TEST-REPORT.md', "| Claude's reading | Tharun in play | Agreed? |")
    chk = [('A7-9b · the action in play', Q('Startup, hold, and return read as distinct moments including when getting '
                                             'hit mid-jab cuts cleanly into the hit/reaction state rather than feeling '
                                             'stuck, and when close-range jabbing, rewinding, or KO transitions occur.',
                                             'TEST-REPORT.md')),
           ('A7-9c · registration', Q('Zoomed in on the key within its spot, the pivot/anchor stays locked in place '
                                      'with no noticeable drift or wandering relative to its mount.', 'TEST-REPORT.md')),
           ('A7-9d · against the background', Q('Both clips remain readable over both light and dark backgrounds, with '
                                                'clear enough contrast to follow the motion without losing the '
                                                'silhouette.', 'TEST-REPORT.md'))]
    words = Q('Writing my first look before reading the strip taught me how easy it is to project motion that isn\'t '
              'actually drawn, like thinking the key spun or the arm extended separately.', 'FRICTIONAL.md')

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Claude, Overruled', 'TEST-REPORT A7-9f · HUMAN CHECKS (Tharun) · FRICTIONAL.md · verbatim')
        y = 340
        for r in rows[1:]:
            y = card(d, (X0, y, 1700), r[2], 'Claude: ' + r[0] + '\nTharun: ' + r[1], on=i == 0 and r is rows[1],
                     fsize=40, tsize=42) + 16
        x = 1780
        if i >= 1:
            yy = 340
            for lab, q in chk:
                yy = quote_card(d, (x, yy, X1), 'Tharun · HUMAN CHECK · ' + lab, q, on=i == 1, fsize=40) + 16
            if i >= 2:
                quote_card(d, (x, yy + 10, X1), 'Tharun · FRICTIONAL.md, In my words', words, on=True, fsize=40)
        return c
    staged('B23', ['checks', 'words'], img)


# ------------------------------------------------------------------ B24 credits (verbatim SOURCES.md)
def b24():
    txt = rev_text('SOURCES.md')
    sec = txt.split('**Who did what (A7):**', 1)[1]
    me_s, cl_s = sec.split('- **Claude Code:**', 1)
    me = [norm(ln.strip()[2:]) for ln in me_s.splitlines() if ln.strip().startswith('- **') and 'Me (Tharun)' not in ln]
    cl = [norm(ln.strip()[2:]) for ln in cl_s.splitlines() if ln.strip().startswith('- **')]
    draft = Q('Drafted and refined across four review rounds with Claude Code in the terminal, cross-checking the facts '
              'sheet and headless Godot probe outputs (ba0c012) against the codebase to catch conflicts like duplicate '
              'KeyMount.position writers, facing handling, and entry-tick offsets before committing (18a3d78).',
              'SOURCES.md')
    lic = Q('Licence: Stability AI Non-Commercial Research Community License, as all of this project\'s SDXL-Turbo art.',
            'SOURCES.md')

    def col(d, x, x1, title, items, on):
        d.text((x, 300), title, font=F(SANSB, 56), fill=ACC if on else INK)
        y = 390
        f = F(SANS, 40)
        for it in items:
            for k, ln in enumerate(wrap(d, it, f, x1 - x - 40)):
                d.text((x + (0 if k == 0 else 34), y), ln, font=f, fill=INK); y += 52
            y += 12
        assert y < 1560, ('credits overflow', title, y)

    def img(i):
        c = canvas(); d = ImageDraw.Draw(c)
        header(d, 'Who Did What (A7)')
        badge(d, 'SOURCES.md · verbatim')
        col(d, X0, 1880, 'Tharun (human)', me, i == 0)
        col(d, 1960, X1, 'Claude Code (AI)', cl, i == 1)
        card(d, (X0, 1580, X1), 'Drafting help for the brief (SOURCES.md, A7) · Sprite sheet licence',
             draft + '\n' + lic, on=i == 2, fsize=38, tsize=42)
        return c
    staged('B24', ['claude', 'brief'], img)


BUILD = {'B02': b02, 'B04': b04, 'B05': b05, 'B06': b06, 'B08': b08, 'B09': b09, 'B10': b10, 'B11': b11,
         'B12': b12, 'B13': b13, 'B14': b14, 'B15': b15, 'B16': b16, 'B17': b17, 'B18': b18, 'B19': b19,
         'B20': b20, 'B21': b21, 'B22': b22, 'B23': b23, 'B24': b24}

if __name__ == '__main__':
    todo = list(BUILD) if sys.argv[1:] == ['all'] else sys.argv[1:]
    for bid in todo:
        BUILD[bid]()
