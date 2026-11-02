# SOURCES.md — what this film is made from

Film: **Tin Knockout, Shaders and Materials** (`claude-liam-walker-tinknockout-tharun-m-a5-shaders`), CSYE 7270
Assignment 5. Built by Claude (Claude Code, Opus 5.5) on 2026-11-01 with the course Brutalist toolkit
(`_brutalist/`, `godot-gamedev` skill, `walker` modifier). Narration: Liam, Kokoro `am_onyx`, local AI text-to-speech.

## Revision shown

- **Game source:** commit `2e6946d` (the F9 capture key). The shaders, driver and materials shown are byte-identical
  to `2e6946d` (asserted by `_tools/build_sheet.py`).
- **Annotated generated shader:** `godot/shaders/standard_generated.gdshader` as annotated by Tharun in `e4c188f`
  (comments only).
- **Docs and evidence:** read from the working tree at `93aedd9`. The uncommitted FRICTIONAL.md and SUBMISSION.md
  edits are not used.

## Who did what — in the game (A5)

Shown verbatim on screen in B15 from the repository's `SOURCES.md` "Who did what (A5)". The film quotes that section;
it does not restate or extend it. In short, as that file records: Claude proposed the design decisions and the
material plan, and Tharun accepted them. The colour line and the `painted_tin` skeleton were Claude suggestions that
Tharun typed (and whose blanks he filled). Tharun computed the predictions by hand. Claude wrote the driver and test
(agent session), the audit, the captures and the tools.

## Who did what — in this film

- **Claude:** wrote the beat sheet, narration and every tool in `_tools/`; made the one new capture (`capture/`);
  built every composite; rendered and checked the film. Claude chose the Your Turn prompt and the "next step"
  (METALLIC from the wear mask); these are the film's proposals, not recorded student decisions.
- **Tharun:** chose to attempt the film; he watches it and decides whether to submit it. He did not review the script
  before the render.

## Media

| Media | Provenance | Beats |
|---|---|---|
| `evidence/a5/captures/os-screenshot/os_screenshot_rewinding.png` | Tharun's OS screenshot during play | B02 |
| `evidence/a5/captures/bolt_rewind_amount_{0.0,0.5,1.0,2.0}.png`, `pixel-samples.txt` | in-engine captures, scripted input (`tools/a5_capture_run.gd`, F9), by Claude | B04, B14 |
| `capture/rewind-4k.mp4` + `evidence/runs/rewind-capture-log.txt` | Movie Maker capture made for this film, scripted input, isolated copy of `2e6946d` (CAPTURE.md) | B06 |
| `evidence/a5/captures/toybox/toyboxes_side_by_side_crop2x.png`, `edit_checks/*` | in-engine captures (windowed), by Claude; edits by Tharun | B02, B08 |
| `evidence/a5/captures/hint_quads.png`, `hint-samples.txt` | in-engine capture (windowed), by Claude | B10 |
| `evidence/a5/captures/toybox/sweep_contact_sheet.png` | in-engine captures (windowed), by Claude | B11 |
| `logs/*.log`, `evidence/a5/mutations/*`, `evidence/a5/headless-facts.txt` | recorded output, shown verbatim | B13, B14 |
| Godot source files | verbatim at `2e6946d` (`e4c188f` for the annotated generated shader) | B03, B05, B07, B09, B12 |

**Textures in the game:** Poly Haven "Metal Plate" (https://polyhaven.com/a/metal_plate) by Rob Tuytel, CC0
(repository `SOURCES.md`; `godot/assets/textures/metal_plate/ATTRIBUTION.md`).

**New capture hashes (SHA-256):**
- `capture/rewind-4k.mp4`: `3bb750824404078c6fcb256fa2a6b66dde4c5763d452ef87a80c10f285459368`
- `evidence/runs/rewind-capture-log.txt`: `c55284c56de1f1124f18001945fca5c44378cffae6016e1dbc1864f46b1b7c8b`

**Toolkit compositions:** ClaudeComposerAsk (B00, B17), BrutalistHesitantWriter (B01), GodotDevWorkbench (B03, labelled
"Godot editor reconstruction"), ClaudeVerdictArtifact (B16), ClaudeTitleOutro (B18, OUTRO-LOCK).
