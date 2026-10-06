"""Automated loop-seam check for the shipped music (CHANGE-BRIEF F3).
Decodes godot/assets/music/waltz.ogg as Godot will play it and compares the jump
across the seam (last sample -> first sample) with the track's own sample-to-sample
movement. PASS if the seam jump is below the 99th percentile of normal steps, and
the RMS level across the seam changes by < 3 dB. Exit code 1 on FAIL.
This does not replace listening to >= 3 repetitions (human check in TEST-REPORT).
"""
import sys
import numpy as np
import soundfile as sf

path = sys.argv[1] if len(sys.argv) > 1 else "godot/assets/music/waltz.ogg"
y, sr = sf.read(path, dtype="float32")
if y.ndim > 1:
    y = y.mean(axis=1)
steps = np.abs(np.diff(y))
p99 = float(np.percentile(steps, 99))
jump = abs(float(y[0] - y[-1]))
w = int(0.1 * sr)
db = 20 * np.log10((np.sqrt(np.mean(y[:w] ** 2)) + 1e-9) / (np.sqrt(np.mean(y[-w:] ** 2)) + 1e-9))
ok1, ok2 = jump < p99, abs(db) < 3.0
print(f"{path}: {len(y) / sr:.2f} s @ {sr} Hz")
print(f"{'PASS' if ok1 else 'FAIL'}  seam sample jump {jump:.4f} < p99 of normal steps {p99:.4f}")
print(f"{'PASS' if ok2 else 'FAIL'}  level change across seam {db:+.2f} dB (limit 3 dB)")
sys.exit(0 if ok1 and ok2 else 1)
