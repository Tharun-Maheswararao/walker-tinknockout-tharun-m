#!/usr/bin/env python3
"""Bind Remotion durations and code-line cues to the measured narration.

Cue times = (word index of the spoken anchor phrase / total words) x measured
duration, a proportional estimate of when Liam says that line number.
Also pads the outro narration with the OUTRO-LOCK 1.0 s silent tail.
"""
import json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
ANCHORS = {
    'B04': {72: 'line seventy-two', 73: 'seventy-three sets'},
    'B06': {208: 'two oh eight', 211: 'two eleven', 213: 'two thirteen', 206: 'two oh seven'},
    'B08': {31: 'thirty-one', 32: 'thirty-two', 33: 'thirty-three', 35: 'thirty-four'},
    'B11': {208: 'two oh eight', 209: 'two oh nine', 212: 'two twelve'},
}


def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


sheet = json.loads((REEL / 'beat_sheet.json').read_text())
for b in sheet['beats']:
    bid = b['beat_id']
    if bid == 'B15':
        src = REEL / 'mp3' / 'beat-B15.mp3'
        raw = REEL / 'mp3' / 'beat-B15.voice.mp3'
        if not raw.exists():
            src.rename(raw)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'apad=pad_dur=1.0',
                        '-c:a', 'libmp3lame', '-b:a', '192k', str(src)], check=True)
        b['actual_duration_s'] = round(probe(src), 2)
        b['outro_tail_s'] = 1.0
    rem = (b.get('shot') or {}).get('remotion')
    if not rem or 'actual_duration_s' not in b:
        continue
    dur = b['actual_duration_s']
    rem['props']['durationSeconds'] = dur
    if bid in ANCHORS:
        words = b['narration_text'].split()
        text = ' '.join(words).lower()
        cues = []
        for line, phrase in ANCHORS[bid].items():
            i = text.find(phrase.lower())
            assert i >= 0, (bid, phrase)
            at = len(text[:i].split()) / len(words) * dur
            lab = next(c['label'] for c in rem['props']['cues'] if c['line'] == line)
            cues.append({'at': round(max(0.0, at - 0.3), 2), 'line': line, 'label': lab})
        rem['props']['cues'] = sorted(cues, key=lambda c: c['at'])
(REEL / 'beat_sheet.json').write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
for b in sheet['beats']:
    print(b['beat_id'], b.get('actual_duration_s'), [(c['at'], c['line']) for c in ((b['shot'].get('remotion') or {}).get('props', {}).get('cues') or [])])
