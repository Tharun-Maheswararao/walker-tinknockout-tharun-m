"""Trim a generated SFX to a game-ready one-shot (logged edit).
v2 (2026-10-06): start just before the LOUDEST transient (walk back from the peak
until the envelope is 24 dB below it, max 150 ms) instead of the first sample
above -30 dBFS - v1 often started on low-level noise far ahead of the real hit.
Keep at most MAX seconds, 30 ms fade-out, peak-normalise to -1 dBFS.
  python tools/edit/trim_sfx.py IN.wav OUT.wav MAX_SECONDS
"""
import sys
import numpy as np
import soundfile as sf

src, dst, mx = sys.argv[1], sys.argv[2], float(sys.argv[3])
x, sr = sf.read(src, dtype="float32")
if x.ndim > 1:
    x = x.mean(axis=1)
n = max(1, int(0.005 * sr))
e = np.convolve(np.abs(x), np.ones(n) / n, mode="same")
pk = int(np.argmax(e))
start = pk
floor = e[pk] * 10 ** (-24 / 20)
while start > 0 and pk - start < int(0.15 * sr) and e[start] > floor:
    start -= 1
start = max(0, start - int(0.003 * sr))
y = x[start:start + int(mx * sr)].copy()
fade = min(len(y), int(0.03 * sr))
y[-fade:] *= np.linspace(1, 0, fade)
y *= 10 ** (-1 / 20) / (np.max(np.abs(y)) + 1e-9)
sf.write(dst, y, sr)
print(f"{src} -> {dst}: start {start / sr * 1000:.0f} ms, len {len(y) / sr:.2f} s")
