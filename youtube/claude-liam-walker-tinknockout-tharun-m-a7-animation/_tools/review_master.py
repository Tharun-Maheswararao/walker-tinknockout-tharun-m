#!/usr/bin/env python3
"""Inspect the actual master: probe, per-beat frames at 50 % (full 4K PNGs for code beats), a contact sheet,
per-beat audio levels (volumedetect), the outro tail, and full decode. Writes _qc/master/ and prints a summary."""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image

REEL = Path(__file__).resolve().parents[1]
mp4 = Path(sys.argv[1])
out = REEL / '_qc' / 'master'
out.mkdir(parents=True, exist_ok=True)
sheet = json.loads((REEL / 'beat_sheet.json').read_text())


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


p = json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate,channels',
                    '-of', 'json', str(mp4)]).stdout)
print('PROBE', json.dumps(p))
t, thumbs = 0.0, []
for b in sheet['beats']:
    bid, d = b['beat_id'], b['actual_duration_s']
    for frac in (0.15, 0.5, 0.92):
        f = out / f'{bid}_{int(frac * 100):02d}.png'
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t + d * frac:.3f}', '-i', str(mp4), '-frames:v', '1', str(f)])
        if frac == 0.5:
            thumbs.append((bid, f))
    a = run(['ffmpeg', '-v', 'info', '-ss', f'{t:.3f}', '-t', f'{d:.3f}', '-i', str(mp4), '-vn', '-af', 'volumedetect', '-f', 'null', '-'])
    mean = re.search(r'mean_volume: ([\-\d.]+) dB', a.stderr)
    mx = re.search(r'max_volume: ([\-\d.]+) dB', a.stderr)
    print(f'{bid} {t:7.2f}s +{d:5.2f}  mean {mean.group(1) if mean else "?"} dB  max {mx.group(1) if mx else "?"} dB')
    t += d
last = sheet['beats'][-1]
a = run(['ffmpeg', '-v', 'info', '-ss', f'{t - 0.9:.3f}', '-t', '0.85', '-i', str(mp4), '-vn', '-af', 'volumedetect', '-f', 'null', '-'])
print('OUTRO TAIL last 0.85 s:', re.search(r'max_volume: ([\-\d.]+) dB', a.stderr).group(0))
cols, tw, th = 4, 960, 540
rows = (len(thumbs) + cols - 1) // cols
cs = Image.new('RGB', (cols * tw, rows * th), 'white')
for k, (bid, f) in enumerate(thumbs):
    cs.paste(Image.open(f).convert('RGB').resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
cs.save(REEL / '_qc' / 'master-contact.png')
dec = run(['ffmpeg', '-v', 'error', '-i', str(mp4), '-f', 'null', '-'])
print('FULL DECODE errors:', repr(dec.stderr.strip()[:300]) or 'none')
print('timeline', round(t, 2))
