# SOURCES.md — what this film is made from

Film: **Tin Knockout, Animation** (`claude-liam-walker-tinknockout-tharun-m-a7-animation`), CSYE 7270 Assignment 7.
Built by Claude (Claude Code, Opus 5.5) on 2026-11-22 with the course Brutalist toolkit (`_brutalist/`,
`godot-gamedev` skill, `walker` modifier), modelled on the A6 film's tools and records. Narration: Liam, Kokoro
`am_onyx`, local AI text-to-speech.

## Revision shown

- **Game source, docs and evidence:** commit `a5978c0` (`a5978c099fbfa10159730c6aae3cc194943ff9ea`, HEAD of `main`,
  unpushed, when the film was built). `_tools/build_sheet.py` asserts every shown file and folder is unchanged against
  it in the working tree, and every excerpt and quotation is read from `git show a5978c0:<path>`.
- Earlier blobs shown as "before": `jab_action.tres` at `8a9dbed^` (revision 1) and `a1d6072^` (revision 2), labelled.

## Who did what — in the game (A7)

Shown verbatim on screen in B24 from the repository's `SOURCES.md` "Who did what (A7)". The film quotes that
section; it does not restate or extend it. On how the brief was drafted, the film says only what SOURCES.md
"Assignment 7" says ("Drafting help for the brief", quoted verbatim in B24).

Tharun's observations and verdicts (TUNING.md "A7 jab_action" first look and verdicts, TEST-REPORT A7-9a–d, FRICTIONAL
"In my words", the CLOCKS line he measured) appear only as quotations marked as his.

## Who did what — in this film

- **Claude (this film session):** wrote the beat sheet and narration, the two film capture scripts / runs, the
  composites, the evidence ledger and these records; re-ran the A7 tests on a clean copy; ran every check below.
- **Tharun:** none of this film's build. His words appear only as quotations from the repository files. He has not yet
  watched the film or reviewed the narration.

## Engine captures made for this film

See `CAPTURE.md`. Both on isolated `git archive a5978c0` copies; the repository was not touched.

| File | SHA-256 | What |
|---|---|---|
| `capture/play-4k60.mp4` | see `gamedev-evidence.json` `engine_captures` | the game (`main.tscn`), scripted input, 818 frames at 60 fps |
| `capture/key-cycle-4k60.mp4` | see `gamedev-evidence.json` `engine_captures` | `previews/key_cycle_preview.tscn` (FIXTURE) |

## Committed images shown (not made for this film)

- `captures/jab_action/r0`, `r1`, `r2` frames and the contact sheets `r1_recovery_sheet.png`, `r1_vs_r2_sheet.png`:
  fixture captures of `godot/previews/jab_preview.tscn` run by Tharun (TEST-REPORT A7-8); the sheets assembled by
  Claude (SOURCES.md A7, Python with Pillow).
- `godot/assets/props/key-bolt-sheet.png`, `key-rivet-sheet.png`: written by `generate_key_sheets.gd` (Claude) from the
  A2 key art, SDXL-Turbo, Stability AI Non-Commercial Research Community License (ATTRIBUTION.md, SOURCES.md A7).

## Recorded output shown

- `evidence/runs/tests-a5978c0/`: the A7 suites plus `test_slice` and `test_wind_steam_state`, re-run for this film
  through `scripts/run-test.sh` on a clean `git archive a5978c0 godot scripts` copy (all at TEST-REPORT's counts).
- `evidence/a7/mutations/`, `evidence/a7/seam/`, `logs/jab_preview_r0.log`: committed logs at `a5978c0`, verbatim.

## Toolkit

`runtime/scripts/generate_audio_kokoro.py` (am_onyx), `runtime/scripts/remotion_scenes.py` (ClaudeComposerAsk,
BrutalistHesitantWriter, GodotDevWorkbench, ClaudeVerdictArtifact, ClaudeTitleOutro), `./art godot-gamedev --check`,
`./art final --height 2160 --fps 30`. Fonts: EB Garamond, Inter, Lato, PT Mono (toolkit `runtime/fonts`).
No upstream documentation was consulted for this film. No secrets or `.env` contents are shown.
