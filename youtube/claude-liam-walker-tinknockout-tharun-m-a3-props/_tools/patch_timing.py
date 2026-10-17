#!/usr/bin/env python3
"""Bind visuals to the measured narration (run after generate_audio_kokoro.py).

Cue time = (word index of the beat's spoken anchor phrase / total words) x voice duration
(+ baked lead silence) - 0.3 s, so a highlight lands as the words are said. Proportional
estimate; no speech recognition. Writes shot.cue_times, Remotion durationSeconds and
GodotDevWorkbench cue times. Audio edits (each keeps the untouched voice file as
beat-Bxx.voice.mp3 and is idempotent):
  * B01: the 0.8 s lead silence is baked into the file (compile.py does not apply it);
  * B18: silence padded to 21.0 s so the real orbit reaches the back of the room while held
    (no retiming of the capture);
  * outro: the OUTRO-LOCK 1.0 s silent tail.
"""
import json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
PAD_TO = {'B18': 21.0}


def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def ff(src, dst, af):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-af', af, '-c:a', 'libmp3lame', '-b:a', '192k',
                    str(dst)], check=True)


sheet = json.loads((REEL / 'beat_sheet.json').read_text())
for b in sheet['beats']:
    bid = b['beat_id']
    if 'audio_file' not in b:
        continue
    out = REEL / 'mp3' / f'beat-{bid}.mp3'
    raw = REEL / 'mp3' / f'beat-{bid}.voice.mp3'
    lead = 0.0
    if b.get('kind') == 'outro_voice' or b.get('lead_silence_s') or bid in PAD_TO:
        if not raw.exists():
            out.rename(raw)
        voice = probe(raw)
        if b.get('kind') == 'outro_voice':
            ff(raw, out, 'apad=pad_dur=1.0'); b['outro_tail_s'] = 1.0
        elif b.get('lead_silence_s'):
            lead = b['lead_silence_s']
            ff(raw, out, f'adelay={int(lead * 1000)}:all=1'); b['lead_silence_baked'] = True
        else:
            ff(raw, out, f'apad=whole_dur={PAD_TO[bid]}'); b['silence_pad_to_s'] = PAD_TO[bid]
        b['voice_duration_s'] = round(voice, 2)
    else:
        voice = probe(out)
    b['actual_duration_s'] = round(probe(out), 2)
    dur = b['actual_duration_s']
    times = {}
    words = b['narration_text'].split()
    text = ' '.join(words).lower()
    for key, phrase in b['shot'].get('anchors', []):
        i = text.find(phrase.lower())
        assert i >= 0, (bid, phrase)
        times[key] = round(max(0.0, lead + len(text[:i].split()) / len(words) * voice - 0.3), 2)
    if times:
        b['shot']['cue_times'] = times
    rem = b['shot'].get('remotion')
    if rem:
        rem['props']['durationSeconds'] = dur
        if rem['pattern'] == 'GodotDevWorkbench':
            labels = {c['line']: c['label'] for c in rem['props']['cues']}
            rem['props']['cues'] = sorted(({'at': times[str(k)], 'line': k, 'label': v} for k, v in labels.items()),
                                          key=lambda c: c['at'])
(REEL / 'beat_sheet.json').write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
for b in sheet['beats']:
    print(b['beat_id'], b.get('actual_duration_s'), b['shot'].get('cue_times'))
