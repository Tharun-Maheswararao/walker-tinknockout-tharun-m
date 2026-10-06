"""Cut a seamless music loop from a generated track (logged edit).

1. estimate the beat period from the onset-envelope autocorrelation (waltz: 3 beats/bar)
2. for loop lengths of 4/8 bars and every start in the first half, compare the audio
   just after the loop end with the audio just after the loop start (where playback
   jumps back to). Pick the pair with the smallest spectral difference.
3. snap both cut points to the nearest zero crossings, 8 ms equal-power crossfade of the
   tail into the head, export OGG (Godot loops OGG directly) + a 3-repetition WAV for
   listening, and print a seam metric.
  python tools/edit/cut_loop.py IN.wav OUT.ogg
"""
import subprocess
import sys

import numpy as np
import soundfile as sf

src, dst = sys.argv[1], sys.argv[2]
x, sr = sf.read(src, dtype="float32")
if x.ndim > 1:
    x = x.mean(axis=1)
hop = 512
frames = len(x) // hop
rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) for i in range(frames)])
onset = np.maximum(0, np.diff(rms, prepend=rms[0]))
ac = np.correlate(onset - onset.mean(), onset - onset.mean(), "full")[frames - 1:]
lo, hi = int(0.3 * sr / hop), int(1.0 * sr / hop)     # beats between 60 and 200 bpm
beat = (lo + int(np.argmax(ac[lo:hi]))) * hop
bar = beat * 3
print(f"beat {beat / sr:.3f} s ({60 * sr / beat:.0f} bpm), bar {bar / sr:.2f} s")

def spec(a):
    return np.log1p(np.abs(np.fft.rfft(a * np.hanning(len(a)))))

w = int(0.25 * sr)
best = None
for bars in (8, 4):
    L = bars * bar
    for s in range(int(0.5 * sr), len(x) - L - w, beat // 4):
        d = np.mean((spec(x[s:s + w]) - spec(x[s + L:s + L + w])) ** 2)
        lvl = abs(np.sqrt(np.mean(x[s:s + w] ** 2)) - np.sqrt(np.mean(x[s + L:s + L + w] ** 2)))
        score = d + 40 * lvl
        if best is None or score < best[0]:
            best = (score, s, L, bars)
    if best and best[0] < 0.35:
        break
score, s, L, bars = best

def zc(i):
    j = i
    while j < len(x) - 1 and not (x[j] <= 0 < x[j + 1]):
        j += 1
    return j

a, b = zc(s), zc(s + L)
loop = x[a:b].copy()
xf = int(0.008 * sr)
t = np.linspace(0, np.pi / 2, xf)
tail = x[b:b + xf]
loop[:xf] = loop[:xf] * np.sin(t) + tail * np.cos(t)   # tail fades into head: the jump back is continuous
loop *= 10 ** (-1.5 / 20) / (np.max(np.abs(loop)) + 1e-9)
jump = abs(float(loop[-1] - loop[0]))
seam = np.concatenate([loop[-w:], loop[:w]])
print(f"loop: {bars} bars from {a / sr:.2f} s to {b / sr:.2f} s ({len(loop) / sr:.2f} s), spectral score {score:.3f}")
print(f"seam: sample jump {jump:.4f} (full scale 1.0), level before/after "
      f"{np.sqrt(np.mean(loop[-w:] ** 2)):.3f}/{np.sqrt(np.mean(loop[:w] ** 2)):.3f}")
tmp = dst.replace(".ogg", ".wav")
sf.write(tmp, loop, sr)
sf.write(dst, loop, sr, format="OGG", subtype="VORBIS")   # libsndfile Vorbis (this ffmpeg has no libvorbis)
sf.write(dst.replace(".ogg", "-x3-listen.wav"), np.tile(loop, 3), sr)
print("wrote", dst)
