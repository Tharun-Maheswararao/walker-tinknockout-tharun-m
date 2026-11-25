#!/usr/bin/env python3
"""Write SHOTLIST.md from beat_sheet.json (measured durations, show events, provenance labels on screen)."""
import json
from pathlib import Path
REEL = Path(__file__).resolve().parents[1]
s = json.loads((REEL / 'beat_sheet.json').read_text())
REAL = 'REAL PLAY · tag a7 (a0c95cc) · SCRIPTED INPUT; REPLAY / repeat labels; positions SET disclosed'
LAB = {'B00': REAL, 'B01': 'CONSTRUCTED · a proposal · does not exist yet; NOT BUILT YET stamp',
       'B02': 'Godot editor reconstruction · verbatim at a7 (a0c95cc)', 'B03': REAL,
       'B04': 'RECORDED OUTPUT · re-run on a7 (a0c95cc); WILL card',
       'B05': 'CONSTRUCTED OVERLAY · does not exist yet (over a REAL PLAY a7 frame); real command, recorded output',
       'B06': 'Named only, no footage or art', 'B07': REAL,
       'B08': 'Steps marked WILL; TODAY: recorded output', 'B09': 'tags and TEST-REPORT ids',
       'B10': 'OUT / IN · will / FIRST · will', 'B11': 'Godot editor reconstruction · verbatim at a7 (a0c95cc)',
       'B12': 'RECORDED OUTPUT · re-run on a7 (a0c95cc); WILL card', 'B13': 'tags', 'B14': 'tags; WILL EXIST column',
       'B15': 'title card'}
rows = ['# SHOTLIST.md — what is on screen in each beat, and where it came from', '',
        'Generated from beat_sheet.json (measured durations) by _tools/make_shotlist.py. Lane: REMOTION = toolkit '
        'composition; OWN = composite built by _tools/make_media.py.', '',
        '| Beat | Act | s | Lane | On screen | Provenance label on screen |', '|---|---|---|---|---|---|']
tot = 0
for b in s['beats']:
    sh = b['shot']; rem = sh.get('remotion')
    lane = 'REMOTION ' + rem['pattern'] if rem else 'OWN'
    ev = '; '.join(e['event'] for e in sh['show'])
    rows.append(f"| {b['beat_id']} | {b['act']} | {b['actual_duration_s']:.2f} | {lane} | {ev} | {LAB[b['beat_id']]} |")
    tot += b['actual_duration_s']
rows += ['', f'Total {tot:.2f} s.']
(REEL / 'SHOTLIST.md').write_text('\n'.join(rows) + '\n')
print('SHOTLIST', round(tot, 2))
