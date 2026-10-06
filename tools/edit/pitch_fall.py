"""Edit: make a sound 'wind down' - playback speed glides from 1.0 to END over the
clip (pitch and tempo fall together, like a spring running out). Used on SFX-EMPTY
because no generated candidate fell in pitch (evidence/sfx-scores-v2.txt, pitch_drop ~1.0).
  python tools/edit/pitch_fall.py IN.wav OUT.wav END_SPEED
"""
import sys
import numpy as np
import soundfile as sf

src, dst, end = sys.argv[1], sys.argv[2], float(sys.argv[3])
x, sr = sf.read(src, dtype="float32")
speed = np.linspace(1.0, end, len(x))
pos = np.cumsum(speed)
pos = pos[pos < len(x) - 1]
y = np.interp(pos, np.arange(len(x)), x).astype(np.float32)
fade = int(0.05 * sr)
y[-fade:] *= np.linspace(1, 0, fade)
sf.write(dst, y, sr)
print(f"{dst}: {len(x) / sr:.2f}s -> {len(y) / sr:.2f}s, speed 1.0 -> {end}")
