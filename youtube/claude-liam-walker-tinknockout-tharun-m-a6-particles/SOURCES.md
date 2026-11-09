# SOURCES.md — what this film is made from

Film: **Tin Knockout, Particle Effects** (`claude-liam-walker-tinknockout-tharun-m-a6-particles`), CSYE 7270
Assignment 6. Built by Claude (Claude Code, Opus 5.5) on 2026-11-09 with the course Brutalist toolkit (`_brutalist/`,
`godot-gamedev` skill, `walker` modifier), modelled on the A5 film's tools and records. Narration: Liam, Kokoro
`am_onyx`, local AI text-to-speech.

## Revision shown

- **Game source, docs and evidence:** commit `c844ab2` (`c844ab2c13eda0288d0cee63e1789a0efcbd84f5`, HEAD of `main`).
  `_tools/build_sheet.py` asserts every shown file is unchanged against it in the working tree.
- The only untracked path in the repository when the film was built was the A5 reel's `_qc/master/` folder (not
  used here).

## Who did what — in the game (A6)

Shown verbatim on screen in B21 from the repository's `SOURCES.md` "Who did what (A6)". The film quotes that section;
it does not restate or extend it. Drafting help (Claude 3.5 Sonnet, an external LLM) is quoted from the same file.

## Who did what — in this film

- **Claude (this film session):** wrote the beat sheet and narration, the film capture script and capture, the
  composites, the evidence ledger and these records; ran the tests on a clean copy; ran every check below.
- **Tharun:** none of this film's build. His words appear only as quotations from the repository files. He has not
  yet watched the film or reviewed the narration.

## Inputs (all from the repository at c844ab2 unless named)

| Input | Used in | Provenance |
|---|---|---|
| `CHANGE-BRIEF.md` (v1 + A6 revisions) | B02, B04, B07, B11, B17, B19 | Tharun (drafted with Claude 3.5 Sonnet; corrections from Claude Code reviews) |
| `TUNING.md` | B06–B08, B13–B15 | Claude's readings, predictions and comparisons; Tharun's first looks and verdicts |
| `TEST-REPORT.md` A6-1 … A6-5c, "The process shader" | B13, B17–B20, B22 | drafted by Claude; Tharun's observations marked |
| `FRICTIONAL.md`, `SOURCES.md`, `README.md`, `CLAUDE.md` | B03, B05, B21, B22 | as recorded in each |
| `captures/impact_effect/r0`, `r1`, `r0_vs_r1_sheet.png` | B03, B06, B08 | fixture strips, captured by Tharun; sheet assembled by Claude |
| `captures/wind_steam/r0` | B13 | fixture strip, captured by Tharun |
| `captures/wind_steam_rewind/r0`, `r0_vs_r1_sheet.png` | B14, B15 | fixture strips, captured by Tharun; sheet assembled by Claude |
| `evidence/a6/mutations/*.log`, `cost/cost_effects_60fps.log` | B18, B19 | recorded output |
| `evidence/a6/visual-profiler-vulkan.webp` | B19 | Tharun's OS screenshot (effects-off reference), cropped |
| `godot/` source excerpts | B03, B05, B07, B09, B12, B14, B17 | verbatim, hashed in `gamedev-evidence.json` |
| `capture/play-4k.mp4` (this reel) | B02, B10, B16 | Movie Maker, scripted input, isolated copy of c844ab2 (CAPTURE.md); SHA-256 in `gamedev-evidence.json` |
| `evidence/runs/tests-c844ab2/` (this reel) | B18 | the four A6 tests and the cost script re-run on a clean copy of c844ab2 |

The cost script re-run (`evidence/runs/tests-c844ab2/cost_effects_60fps.log`) gave different wall-clock numbers
from the committed log, as a wall clock does: it ran while the 4K Movie Maker capture was running. The conclusion was
the same (both effects within the spread of game_off). The film shows the committed log, which TEST-REPORT A6-4 cites.

## Toolkit

`ClaudeComposerAsk` (B00, B23), `BrutalistHesitantWriter` (B01), `GodotDevWorkbench` (B05), `ClaudeVerdictArtifact`
(B22) and `ClaudeTitleOutro` (B24), rendered through `runtime/scripts/remotion_scenes.py`. Every other beat is an
own composite from `_tools/make_media.py` (PIL + ffmpeg). Fonts: EB Garamond, Inter, Lato and PT Mono, bundled in
`_brutalist/runtime/fonts`. No music, no sound effects, no paid service and no network call.

## Not used

- No GPU price number. TEST-REPORT A6-5 lists it as open, and the film says so (B19, B22).
- No game audio. The capture's `frame.wav` was discarded.
- No upstream documentation was consulted for this film. Godot facts are the repository's own probed facts
  (CLAUDE.md, `design/a6/BRIEF-FACTS.md` as cited by the brief).
