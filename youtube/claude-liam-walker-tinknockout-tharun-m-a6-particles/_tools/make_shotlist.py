#!/usr/bin/env python3
"""Write SHOTLIST.md from beat_sheet.json (measured durations, show events, provenance labels)."""
import json
from pathlib import Path
REEL = Path(__file__).resolve().parents[1]
s = json.loads((REEL / 'beat_sheet.json').read_text())
LAB = {'B02': 'HELD FRAME · MOVIE MAKER CAPTURE · SCRIPTED INPUT; zoom of the same frame',
       'B03': 'SOURCE VIEW; FIXTURE · HELD FRAME (r1)', 'B04': 'CHANGE-BRIEF verbatim',
       'B05': 'Godot editor reconstruction · verbatim at c844ab2', 'B06': 'FIXTURE CAPTURE · HELD FRAMES · captured by Tharun',
       'B07': 'SOURCE VIEW · git 45e986f', 'B08': 'FIXTURE CAPTURES · HELD FRAMES · sheet assembled by Claude',
       'B09': 'SOURCE VIEW · not an editor recording', 'B10': 'MOVIE MAKER CAPTURE · SCRIPTED INPUT · made for this film; REPLAY labels',
       'B11': 'CHANGE-BRIEF verbatim', 'B12': 'SOURCE VIEW · c844ab2', 'B13': 'FIXTURE CAPTURE · HELD FRAMES · captured by Tharun',
       'B14': 'FIXTURE · HELD FRAMES; SOURCE VIEW', 'B15': 'FIXTURE CAPTURES · HELD FRAMES · sheet assembled by Claude',
       'B16': 'MOVIE MAKER CAPTURE · SCRIPTED INPUT · made for this film; REPLAY / HELD FRAME labels',
       'B17': 'SOURCE VIEW', 'B18': 'recorded output, verbatim', 'B19': 'recorded output; OS SCREENSHOT · Tharun; GPU PRICE: PENDING',
       'B20': 'repository records, verbatim', 'B21': 'SOURCES.md · verbatim', 'B00': 'RECONSTRUCTED PROMPT — illustrative, not a transcript'}
rows = ['# SHOTLIST.md — what is on screen in each beat, and where it came from', '',
        'Generated from beat_sheet.json (measured durations) by _tools/make_shotlist.py. Lane: REMOTION = toolkit '
        'composition; OWN = composite of real files / recorded output / real engine captures built by _tools/make_media.py.', '',
        '| Beat | Act | s | Lane | On screen | Provenance label on screen |', '|---|---|---|---|---|---|']
tot = 0
for b in s['beats']:
    sh = b['shot']; rem = sh.get('remotion')
    lane = 'REMOTION ' + rem['pattern'] if rem else 'OWN ' + sh['panel']['kind']
    ev = '; '.join(e['event'] for e in sh['show'])
    rows.append(f"| {b['beat_id']} | {b['act']} | {b['actual_duration_s']:.2f} | {lane} | {ev} | {LAB.get(b['beat_id'], '—')} |")
    tot += b['actual_duration_s']
rows += ['', f'Total {tot:.2f} s.']
(REEL / 'SHOTLIST.md').write_text('\n'.join(rows) + '\n')
print('SHOTLIST', round(tot, 2))
