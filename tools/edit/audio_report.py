"""Visual + numeric screen of generated audio candidates (does NOT replace listening).

For each WAV: waveform + spectrogram, onset (first sample above -30 dBFS),
length above -40 dBFS, peak, and spectral centroid. Writes one PNG sheet.
  python tools/edit/audio_report.py OUT.png raw/SFX-JAB/*.wav
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)


def stats(x, sr):
    x = x if x.ndim == 1 else x.mean(axis=1)
    peak = float(np.max(np.abs(x)) + 1e-9)
    env = np.abs(x)
    on = np.argmax(env > peak * 10 ** (-30 / 20)) / sr
    above = np.where(env > peak * 10 ** (-40 / 20))[0]
    body = (above[-1] - above[0]) / sr if len(above) else 0
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    freqs = np.fft.rfftfreq(len(x), 1 / sr)
    cent = float((spec * freqs).sum() / (spec.sum() + 1e-9))
    return x, dict(dur=len(x) / sr, onset_ms=on * 1000, body_s=body, peak_db=20 * np.log10(peak), centroid=cent)


def panel(x, sr, w=520, h=150):
    im = Image.new("RGB", (w, h * 2), "white")
    d = ImageDraw.Draw(im)
    n = len(x)
    cols = np.array_split(x, w)
    for i, c in enumerate(cols):
        a = float(np.max(np.abs(c))) if len(c) else 0
        d.line([i, h / 2 - a * h / 2, i, h / 2 + a * h / 2], fill="#334")
    hop, win = max(1, n // w), 512
    S = []
    for i in range(w):
        seg = x[i * hop:i * hop + win]
        seg = np.pad(seg, (0, win - len(seg)))
        S.append(np.abs(np.fft.rfft(seg * np.hanning(win)))[:256])
    S = np.log10(np.array(S).T + 1e-6)
    S = (255 * (S - S.min()) / (S.max() - S.min() + 1e-9)).astype(np.uint8)[::-1]
    im.paste(Image.fromarray(S).resize((w, h)).convert("RGB"), (0, h))
    return im


def main():
    out, files = sys.argv[1], sys.argv[2:]
    rows = []
    for f in files:
        x, sr = sf.read(f, dtype="float32")
        x, s = stats(x, sr)
        p = panel(x, sr)
        lab = Image.new("RGB", (p.width, 40), "white")
        ImageDraw.Draw(lab).text((4, 4), f"{Path(f).stem}   dur {s['dur']:.2f}s  onset {s['onset_ms']:.0f}ms  body {s['body_s']:.2f}s\n"
                                          f"peak {s['peak_db']:.1f} dBFS  centroid {s['centroid']:.0f} Hz", fill="black", font=F)
        rows.append((lab, p))
        print(Path(f).stem, {k: round(v, 2) for k, v in s.items()})
    W = 540 * min(3, len(rows))
    H = (rows[0][1].height + 44) * ((len(rows) + 2) // 3)
    sheet = Image.new("RGB", (W, H), "#ddd")
    for i, (lab, p) in enumerate(rows):
        x, y = (i % 3) * 540 + 10, (i // 3) * (p.height + 44)
        sheet.paste(lab, (x, y)); sheet.paste(p, (x, y + 40))
    sheet.save(out)


if __name__ == "__main__":
    main()
