#!/usr/bin/env python3
"""Run GATE T's own pixel checks (runtime/scripts/type_check.py functions, unmodified) on this film's
composite beats (typed STILL, so GATE T skips them), at several points of each beat, with the
embedded REAL images (student screenshots, MCP look image, engine renders) masked to the page colour
using the rectangles make_media.py recorded (media/_work/<beat>-masks.json, +24 px for rings/frames).
This checks the film's own typography; the images' diegetic UI text is not film text.
Usage (toolkit venv): .venv/bin/python _tools/selfcheck.py   -> writes _qc/SELFCHECK.md
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import ImageDraw

REEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, '/Users/tharunmaheswararao/Documents/csye7270/_brutalist/runtime/scripts')
import type_check as tc  # noqa: E402

PAGE = (250, 249, 245)
sheet = json.loads((REEL / 'beat_sheet.json').read_text())
rows, bad = [], 0
for b in sheet['beats']:
    if b['shot'].get('type') != 'STILL':
        continue
    bid = b['beat_id']
    v = REEL / 'media' / f'{bid}.mp4'
    masks = json.loads((REEL / 'media' / '_work' / f'{bid}-masks.json').read_text())
    dur = tc.video_duration(v)
    for frac in (0.2, 0.5, 0.97):
        img = tc.extract_frame(v, dur * frac)
        d = ImageDraw.Draw(img)
        for x0, y0, x1, y1 in masks:
            d.rectangle((x0 - 24, y0 - 24, x1 + 24, y1 + 24), fill=PAGE)
        arr = np.array(img)
        pol, bg = tc.detect_polarity(arr)
        res = [('min-size', tc.check_min_size(img, bid, '', polarity=pol)),
               ('overflow', tc.check_overflow(img, bid, polarity=pol, pattern='')),
               ('contrast', tc.check_contrast(img, bid, '', polarity=pol, bg_rgb=bg)),
               ('contrast-local', tc.check_contrast_per_blob(img, polarity=pol)),
               ('bbox-overlap', tc.check_bbox_overlap(img, polarity=pol))]
        for name, (s, m) in res:
            bad += s == 'FAIL'
            rows.append(f'| {bid} | {frac:.2f} | {len(masks)} | {name} | {s} | {m[:140].replace("|", "/")} |')
out = ['# SELFCHECK.md — GATE T functions on the STILL composites (real images masked)', '',
       f'FAILs: {bad}', '', '| beat | t | masks | check | status | detail |', '|---|---|---|---|---|---|'] + rows
(REEL / '_qc').mkdir(exist_ok=True)
(REEL / '_qc' / 'SELFCHECK.md').write_text('\n'.join(out) + '\n')
print('FAILS', bad)
for r in rows:
    if '| FAIL |' in r:
        print(r)
