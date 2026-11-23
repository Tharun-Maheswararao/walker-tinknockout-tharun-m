#!/usr/bin/env python3
"""Write SHOTLIST.md from beat_sheet.json (measured durations, show events, provenance labels)."""
import json
from pathlib import Path
REEL = Path(__file__).resolve().parents[1]
s = json.loads((REEL / 'beat_sheet.json').read_text())
LAB = {'B00': 'RECONSTRUCTED PROMPT — illustrative, not a transcript',
       'B02': 'HELD FRAME · MOVIE MAKER CAPTURE · SCRIPTED INPUT (zoom); TEST-REPORT verbatim',
       'B03': 'Godot editor reconstruction · verbatim at a5978c0',
       'B04': 'MUTATION M1 (worktree, not in the repo); recorded logs verbatim',
       'B05': 'SOURCE VIEW · a5978c0', 'B06': 'recorded output (re-run), verbatim; HELD FRAME · SCRIPTED INPUT',
       'B07': 'Godot editor reconstruction · verbatim at a5978c0',
       'B08': 'MOVIE MAKER CAPTURE · SCRIPTED INPUT (one frame per tick); recorded CLOCKS line (Tharun), verbatim',
       'B09': 'CHANGE-BRIEF §4 and jab_action_keys.md, verbatim',
       'B10': 'FIXTURE CAPTURE · HELD FRAMES · captured by Tharun; first look verbatim',
       'B11': 'SOURCE VIEW · a5978c0', 'B12': 'COMMITTED SPRITE SHEET (enlarged, nearest); ATTRIBUTION verbatim',
       'B13': 'SOURCE VIEW · a5978c0', 'B14': 'FIXTURE · MOVIE MAKER CAPTURE · made for this film; REPLAY label',
       'B15': 'SOURCE VIEW · git 8a9dbed; log and TUNING verbatim',
       'B16': 'FIXTURE CAPTURE · HELD FRAMES · captured by Tharun; TUNING verbatim',
       'B17': 'SOURCE VIEW · git a1d6072; TUNING verbatim',
       'B18': 'FIXTURE CAPTURES · HELD FRAMES · captured by Tharun; TUNING / TEST-REPORT verbatim',
       'B19': 'MOVIE MAKER CAPTURE · SCRIPTED INPUT · made for this film; REPLAY labels; SETUP disclosed',
       'B20': 'MOVIE MAKER CAPTURE · SCRIPTED INPUT · made for this film; REPLAY labels; SETUP disclosed',
       'B21': 'recorded output (re-run), verbatim', 'B22': 'TEST-REPORT and seam logs, verbatim',
       'B23': 'TEST-REPORT / FRICTIONAL, verbatim', 'B24': 'SOURCES.md · verbatim'}
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
