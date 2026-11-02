# _qc/HUMAN-REVIEW.md — review of the actual master (by eye and by measurement)

Reviewer: Claude Code (agent), not a human. Tharun has not yet watched the film.

Master: `exports/landscape/claude-liam-walker-tinknockout-tharun-m-a5-shaders.mp4`
SHA-256 `6568f966a28b65ffad73d3aac36430b4f222d5f065af60dfd930946d141b2ed8` · 422.53 s (7:03) · 3840×2160 H.264
30 fps + AAC 48 kHz stereo · 42.1 MB · receipt `….verified.json` status `ready`, hash matches the file.
Game source 2e6946d.

## Gates (final run, 2026-11-01 19:22 EST)

| Gate | Result |
|---|---|
| `./art godot-gamedev --check` (before render and at handoff) | PASS — 38 source files, 92 exclusions (pre-A5 files asserted byte-identical to 23a0363), 6 components, 1 exact excerpt, 1 checked code→result pair (+4 source-view pairs recorded with hashes) |
| GATE T (`type_check.py`) | PASS, 0 FAILs (advisory §8.10: B16 0.77) |
| Masked GATE T on the 11 STILL composites (`_tools/selfcheck.py`) | 0 FAILs at t = 0.20 / 0.50 / 0.97 (`_qc/SELFCHECK.md`) |
| GATE V (`final_frame_check.py`) | PASS on the third run — 38 frames, 0 BLOCKER, 0 MAJOR (`_qc/REPORT.md`) |
| GATE F (FACTCHECK / SHOTLIST / PROMPTS), slates, sound, decode | passed inside `./art final` |

## The master, inspected (`_tools/review_master.py` → `_qc/master/`, `_qc/master-contact.png`, `_qc/master-review.log`)

- Every beat sampled at 15 / 50 / 92 %: all 19 present in order, nothing clipped, every embedded image carries its
  provenance label (OS SCREENSHOT · Tharun; IN-ENGINE CAPTURE · SCRIPTED INPUT; MOVIE MAKER CAPTURE · SCRIPTED INPUT ·
  made for this film; REPLAY labels; SOURCE VIEW / Godot editor reconstruction; RECONSTRUCTED PROMPT).
- Code at reading size: 48 px mono (4K) in the source views, 28 px (×2) in the B03 workbench; every narrated line visible
  and highlighted on its cue; indentation preserved.
- B06 readout checked against the footage at frames 89 (REWIND, 0.8889) and 106 (HURT, 0.6667).
- Audio: per-beat mean −26.6 to −27.4 dB, peaks −2.8 to −8.8 dB, no clipping; outro tail (last 0.85 s) −54.2 dB, i.e.
  silent; no music, jingle or SFX anywhere (OUTRO-LOCK).
- Outro: exact title "Tin Knockout, Shaders and Materials", @NikBearBrown, slug-seeded mascot, no subline.
- Full decode: no errors.

## Findings and fixes during the build

1. **GodotDevWorkbench clipped long excerpts.** The component has no scrolling (about 13 rows at the minimum font).
   The B05 driver excerpt (lines 17–30) lost lines 26–30, including the narrated lines 27 and 29; the 25-line B09
   excerpt could not fit at all. B05 and B09 were rebuilt as source-view composites (`code_box`, labelled
   "SOURCE VIEW · not an editor recording"), which wrap instead of clipping; every narrated line is visible.
2. **B03's third source note was clipped** at the bottom of the notes dock. Reduced to two notes; code font 28.
3. **Indentation was dropped** in the first source-view composites (the wrap helper stripped leading whitespace), which
   misrepresented the GDScript and shader source. `code_box` now keeps the indentation (tab = 4 spaces).
4. **B11** row label `uv_scale` collided with an explanatory note; the note moved to the footer and the sheet shrank.
5. **B13** used `→` in PT Mono, which has no such glyph; replaced with `->`.
6. **B16 verdict:** with 9 lines the brand label was pushed under the card edge; merged to 8 lines.
7. **B06** first build crashed at frame 221 (the capture has frames 0–220); fixed, and B06 now reads its frames from the
   reel's own `capture/rewind-4k.mp4`.
8. **GATE F** blocked the first `./art final` (no FACTCHECK.md yet); paperwork written, re-run.
9. **GATE V blocked the second final** (2 MAJOR underfill on B01 at 50 %/85 %: 54 % of the safe area, minimum 55 %).
   Type enlarged 104 → 114 px (still inside the right safe edge). Re-run: 0 BLOCKER, 0 MAJOR. No gate was waived.
10. **Fact found while checking:** TEST-REPORT A5-4 says the 1.0 differences are in "exactly the five" half-way channels;
   `pixel-samples.txt` shows four (helmet R predicted 171 from 170.5, captured 171). The film says four. Not edited in
   TEST-REPORT (owned by another session); noted for the student.

## Not verified / limits

- Pronunciation was not checked by ear (no human listen); Kokoro reads "Maheswararao", "Merhaba", "G L S L" as written.
- The composer bookends (B00, B17) use the toolkit's small mono output lines, as in the A3 film; legible at 2160p,
  small at 1080p.
- The narration was not reviewed by Tharun before the render.
- The composer bookend's model chip reads "Fable 5 · High": that is the toolkit component's fixed UI, part of the
  labelled reconstruction, not a record of which model did the A5 work (SOURCES.md records Claude Code, Opus 5.5).
