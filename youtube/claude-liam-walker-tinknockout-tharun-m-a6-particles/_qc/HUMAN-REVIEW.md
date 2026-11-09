# _qc/HUMAN-REVIEW.md — review of the actual master (by eye and by measurement)

Reviewer: Claude Code (agent), not a human. Tharun has not yet watched the film.

Master: `exports/landscape/claude-liam-walker-tinknockout-tharun-m-a6-particles.mp4`
SHA-256 `04d435e30352681ac1bfecd855072acf700a9afc3a02cc5e601407e4b010630a` · 717.27 s (11:57) · 3840×2160 H.264 30 fps
+ AAC 48 kHz stereo · 81.9 MB · receipt `….verified.json`: status `ready`, and its hash matches the file.
Game source and docs shown: c844ab2.

## Gates (final run, 2026-11-09 12:17 EST)

| Gate | Result |
|---|---|
| `./art godot-gamedev --check` (before render and at handoff) | PASS: 27 source files, 129 exclusions (pre-A6 files asserted byte-identical to tag a5, f4dda68), 6 components, 1 exact excerpt, 1 checked code→result pair (+5 source-view pairs recorded with hashes) |
| GATE T (`type_check.py`) | PASS (TYPECHECK.md; advisory §8.10 B22 0.66) |
| Masked GATE T on the STILL composites (`_tools/selfcheck.py`) | 0 FAILs at t = 0.20 / 0.50 / 0.97 (`_qc/SELFCHECK.md`) |
| GATE V (`final_frame_check.py`) | PASS on the second final run: 50 frames, 0 BLOCKER, 0 MAJOR (`_qc/REPORT.md`) |
| GATE F, slates, sound, decode | passed inside `./art final` |
| Game tests on a clean copy of c844ab2 | 136/0, 33/0, 44/0, 37/0; cost script exit 0 (`evidence/runs/tests-c844ab2/`) |

## The master, inspected (`_tools/review_master.py` → `_qc/master/`, `_qc/master-contact.png`, `_qc/master-review.log`)

- **Beats and labels:** every beat was sampled at 15 / 50 / 92 %. All 25 are present in order and nothing is clipped.
  Every embedded image carries its provenance label: FIXTURE CAPTURE / HELD FRAMES (captured by Tharun); MOVIE MAKER
  CAPTURE · SCRIPTED INPUT · made for this film; REPLAY and HELD FRAME labels; OS SCREENSHOT · Tharun; SOURCE VIEW /
  Godot editor reconstruction; RECONSTRUCTED PROMPT.
- **Readouts:** B10's readout was checked against the log at movie frames 178 (jab 5, one normal burst) and 194
  (6 of 8 jabs, one blocked burst). B16's was checked at 264 (PAUSED, wind 4, ratio 0.84) and 326 (REWIND, wind 34,
  ratio 0).
- **GPU price:** no GPU number for either effect appears anywhere. B19 and B22 say it is pending (not measured).
- **Audio:** per-beat mean −26.7 to −27.7 dB, peaks −3.0 to −9.1 dB, no clipping. The outro tail (last 0.85 s) is
  −50.3 dB, i.e. silent. There is no music, jingle or SFX anywhere (OUTRO-LOCK).
- **Outro:** exact title "Tin Knockout, Particle Effects", @NikBearBrown, slug-seeded mascot, no subline.
- **Full decode:** no errors.

## Findings and fixes during the build

1. **GodotDevWorkbench clipped B05** (lines 76–88: line 79 wraps, and line 86 and below were lost). Narrowed to
   lines 77–86 at font 28; all lines are visible.
2. **B01's correction never landed.** The writer's triggers match single tokens, so the phrase trigger "what they
   cost" never fired. Rewritten as "Headless tests prove their cost." → "behaviour" (narration and audio
   regenerated). The correction is on screen at about 11 s of 13.6 s.
3. **B10's jab counter was wrong** (key and value swapped when parsing the log; it showed "8 of 8" at frame 194).
   Fixed; it now matches the log.
4. **B16 narration** said the rewind followed the pause. The log shows Rivet hit Bolt first (log frame 291).
   Corrected before the audio was generated.
5. **Layout:**
   - B02: a label ran under the card.
   - B03: the DRAW frame was pushed into the headless band.
   - B06 and B13: labels ran past the safe edge.
   - B13: the steam crops were too small.
   - B18: Lato has no "→" glyph, and a card overlapped the footer.
   - B19: a note ran under the screenshot.
   - B04, B07 and B12: too much empty space.

   All were fixed in `_tools/make_media.py` and re-rendered.
6. **GATE V blocked the first final** (1 MAJOR: B14 underfill, 54 % of the safe area at 50 %, minimum 55 %). B14's
   frames and text were enlarged. Two edge clips that change exposed were fixed, and so was the zoom label (×4.1).
   Re-run: 0 BLOCKER, 0 MAJOR. No gate was waived.
7. **One render was stopped at Tharun's request** (he took an OA) and then re-run from the start.

## Not verified / limits

- Pronunciation was not checked by ear (no human listen). Kokoro reads "Maheswararao", "Hola" and
  "c eight four four a b two" as written.
- The narration was not reviewed by Tharun before the render. He has not watched the film.
- The composer bookends (B00, B23) show the toolkit component's fixed model chip "Fable 5 · High". That is part of
  the labelled reconstruction, not a record of which model did the A6 work. SOURCES.md records Claude Code (Claude
  Opus 5.5).
- The B10 counter counts burst nodes, which stay alive a few frames after they stop being visible.
- The film's capture is Movie Maker output: deterministic and offline. It says nothing about the real-time frame
  rate or the GPU price.
- The film is long (11:57) because the handout's Ship It list is long. No beat was cut to meet a preset length.
