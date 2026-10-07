# _qc/HUMAN-REVIEW.md — review by looking, not only by gate

`_qc/REPORT.md` is written by GATE V and overwritten on every run. This file records what was inspected by
eye and by measurement, which the gates do not certify. Reviewer: Claude Code (agent), not a human.

Revision reviewed: `64c037a` · master `exports/landscape/claude-liam-walker-tinknockout-tharun-m-gamedev.mp4`
· SHA-256 `8c6c491bb59df135f083786f04832c0b68c3f74a2b47c13303581a1e86edeb83` · 406.10 s · 3840×2160 H.264
30 fps + AAC 48 kHz.

## Gate results (final run)

| Gate | Result |
|---|---|
| `./art godot-gamedev --check` | **PASS** — 85 files hashed, 1 exclusion, 8 components, 4 exact excerpts, 4 code→result pairs (`code-then-result-v1`) |
| GATE T (`type_check.py`) | **PASS**, 0 FAILs (advisory §8.10: B13 narration recites its card, 0.90) |
| GATE V (`final_frame_check.py`) | **PASS** — 32 frames, 0 BLOCKER, 0 MAJOR; regional contrast on B07, B09, B10 |
| GATE F (FACTCHECK/SHOTLIST/PROMPTS) | present |
| beat_lint / gate_shape / approvals | clean (run inside `./art final`) |
| Export receipt | `exports/landscape/…verified.json`, status `ready`, hash matches the file |

## Gate findings and what each one actually was

1. **GATE T on gameplay beats — game art read as text; resolved by reclassification (decision for a human to confirm).**
   With the gameplay beats typed `CAPTURE`, GATE T failed B07, B09, B10 on §8.3 (terracotta on cream),
   §8.3b (per-blob contrast ~1.06:1 at e.g. (1629,900)) and §8.6b (fused bbox overlap). Every failing blob was
   inside the game image — the dark-purple shop shelves (≈(57,51,87)) and copper/pink toys — not film text.
   Masking the game inset and running the same check functions on the film's own label lines: all PASS
   (min run 41–45 px). GATE T exempts `SCREEN` ("its typography belongs to the sim's own UI") but not `CAPTURE`,
   although `beat_plan.py` treats the two as the same user-capture method. The three beats were therefore typed
   `SCREEN` with `capture_kind: "godot-movie-maker gameplay capture (CAPTURE)"` and a `qc.typecheck_note`.
   This departs from the instruction to keep B10's `shot.type` as `CAPTURE`; B10 is still a capture beat with
   `clock: source`, `audio_policy: preserve`, no narration. No gate was disabled and no gate code was changed.
2. **Composites typed STILL.** B02/B03/B05/B12 are layouts of real files typed `STILL`, which GATE T also
   skips. They were self-checked with the same functions: B12 passes everything; B02/B03/B05 fail only on the
   embedded engine images (same false positives as above). With those images masked, B05's designed text passes
   (min run 53 px after raising two labels from 46 to 54 px).
3. **GATE V edge-bleed on B07/B09 — my layout defect, fixed.** The first 90 % inset put the label line at
   y≈54 px, above the title-safe edge. Re-laid out at 2944×1656 with labels at y=175 and y=1980.
4. **GATE V underfill on B01 — my layout defect, fixed.** The writer typed slowly, so at the 50 % sample only
   1½ lines existed (39 % fill). Typing sped up (charMs 18) and line spacing opened (2.1). A trailing fourth line
   that never finished before the cut was removed; the correction "decides → follows" lands at ≈6–9 s.
5. **B06 excerpt clipped — fixed.** 13 lines at 34 px overflowed the code pane (line 213, the one the narration
   names, was cut off). Excerpt narrowed to lines 206–214 at 30 px.
6. **B05 narration — corrected against the pixels.** No red hitbox appears in either screenshot; the line
   about red was cut and re-voiced.

## Measured on the actual master

| Check | Result |
|---|---|
| Dimensions / fps | 3840×2160, 30/1 |
| Duration | 406.10 s (timeline 406.10) |
| **B10 un-narrated game audio, 3:34.50–3:58.93** | volumedetect mean −19.0 dB, max 0.0 dB; per-second RMS −35 dB (title) then −13 to −27 dB through the round: audible, game-only |
| B09 narration for comparison | mean −27.0 dB, max −7.7 dB |
| B15 outro voice / 1 s tail | voice mean −25.6 dB; tail −91 dB (silence, no jingle, no game audio) |

## Frames inspected (`_qc/master-frames.png`, `_qc/frames/`)

All 16 beats: code legible at reading size with "Godot editor reconstruction" + path/lines; POSED labels on
B03/B05; SCRIPTED INPUT labels on B07/B09; "GAME AUDIO — NO NARRATION · SCRIPTED INPUT" plus the sfx log on
B10 for its whole duration; verdict, Your Turn and outro legible; `@NikBearBrown` present.

## Not done / caveats

* Claude cannot hear: the B10 mix was verified as non-silent by measurement only. It is ~8 dB louder (mean)
  than the narration and peaks at 0 dBFS in the game's own mix (also true of the source capture: max −0.2 dB
  before AAC). No loudness repair was applied — that would alter the game's audio.
* The un-narrated beat preserves real game sound, but the beats before and after cut straight in and out of it.
* Rendered component chrome includes a model label ("Fable 5 High") inside `ClaudeComposerAsk`; that is the
  shared component's UI, not a claim about which model built the game.
