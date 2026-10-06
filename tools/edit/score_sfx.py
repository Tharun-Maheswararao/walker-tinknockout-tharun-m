"""Score trimmed SFX candidates against the CHANGE-BRIEF description of each event.
This is Claude's signal analysis, NOT a listening test. Features per file:
  attack_ms   onset -> peak (sharp hit = small)
  decay_ms    peak -> envelope below -20 dB of peak (one-shot length)
  hits        separate transients (envelope peaks > -12 dB, >= 40 ms apart); a one-shot wants 1
  flatness    spectral flatness 0..1 (1 = noise/hiss, low = tonal/ringing metal)
  centroid    brightness in Hz
  pitch_drop  centroid(first 40%) / centroid(last 40%)  (>1 = falls in pitch, wanted for EMPTY)
  python tools/edit/score_sfx.py raw/audition
"""
import sys
from pathlib import Path
import numpy as np
import soundfile as sf

def env(x, sr, win=0.005):
    n = max(1, int(win * sr)); k = np.ones(n) / n
    return np.convolve(np.abs(x), k, mode="same")

def feats(path):
    x, sr = sf.read(path, dtype="float32")
    e = env(x, sr); pk = int(np.argmax(e)); P = e[pk] + 1e-9
    on = int(np.argmax(e > P * 10 ** (-30 / 20)))
    after = np.where(e[pk:] < P * 10 ** (-20 / 20))[0]
    decay = (after[0] if len(after) else len(e) - pk) / sr * 1000
    thr = P * 10 ** (-12 / 20); gap = int(0.04 * sr); hits = 0; last = -gap
    for i in range(1, len(e) - 1):
        if e[i] > thr and e[i] >= e[i - 1] and e[i] >= e[i + 1] and i - last >= gap:
            hits += 1; last = i
    S = np.abs(np.fft.rfft(x * np.hanning(len(x)))) + 1e-9
    flat = float(np.exp(np.mean(np.log(S))) / np.mean(S))
    f = np.fft.rfftfreq(len(x), 1 / sr); cen = float((S * f).sum() / S.sum())
    def c(seg):
        s = np.abs(np.fft.rfft(seg)) + 1e-9; ff = np.fft.rfftfreq(len(seg), 1 / sr); return (s * ff).sum() / s.sum()
    n = len(x); drop = c(x[: int(n * .4)]) / c(x[int(n * .6):])
    return dict(attack_ms=(pk - on) / sr * 1000, decay_ms=decay, hits=hits, flatness=flat, centroid=cen, pitch_drop=drop, dur=n / sr)

# what each event should be (from CHANGE-BRIEF / the user's descriptions)
def score(kind, f):
    s = 0.0
    if kind in ("SFX-JAB", "SFX-CUTLASS", "SFX-POP", "SFX-REWIND"):
        s -= f["attack_ms"] / 10            # sharp onset
        s -= abs(f["hits"] - 1) * 3         # exactly one hit
    if kind == "SFX-JAB":     s += (1 - f["flatness"]) * 6 - abs(f["decay_ms"] - 200) / 100 - abs(f["centroid"] - 2500) / 1500
    if kind == "SFX-CUTLASS": s += (1 - f["flatness"]) * 6 - abs(f["decay_ms"] - 350) / 120 + min(f["centroid"], 5000) / 2000
    if kind == "SFX-POP":     s += -abs(f["decay_ms"] - 60) / 30 + f["flatness"] * 2
    if kind == "SFX-REWIND":  s += -abs(f["decay_ms"] - 25) / 10 + min(f["centroid"], 5000) / 2000
    if kind == "SFX-EMPTY":   s += (f["pitch_drop"] - 1) * 6 + min(f["dur"], 1.4) - f["flatness"] * 2
    if kind == "SFX-BELL":    s += (1 - f["flatness"]) * 8 - f["attack_ms"] / 20 + min(f["decay_ms"], 900) / 300 - abs(f["hits"] - 1) * 2
    return s

root = Path(sys.argv[1])
for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("SFX")):
    rows = sorted(((score(d.name, f), w.stem, f) for w in sorted(d.glob("*.wav")) for f in [feats(w)]), reverse=True)
    print(f"\n== {d.name}")
    for s, n, f in rows:
        print(f"  {s:6.2f}  {n:22s} attack {f['attack_ms']:5.0f}ms decay {f['decay_ms']:5.0f}ms hits {f['hits']:2d} flat {f['flatness']:.3f} cen {f['centroid']:5.0f} drop {f['pitch_drop']:.2f}")
