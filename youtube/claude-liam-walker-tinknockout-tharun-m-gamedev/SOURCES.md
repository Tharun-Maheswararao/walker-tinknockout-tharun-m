# SOURCES.md — render and asset sources for this film

## Source revision

* Game package `walker-tinknockout-tharun-m`, Godot project folder `godot/`, revision **`64c037a`**
  ("Add slice tests, capture tools and evidence; 25/25 checks pass"). HEAD at film time is `5b3fa9f`
  (documents only; `git diff --stat 64c037a -- godot` is empty). Every file under `godot/` is hashed in
  `gamedev-evidence.json` (85 files + 1 exclusion).
* Engine: Godot `4.7.2.stable.official.ed1daf0bf`, macOS, Apple M4.

## Native engine capture

| File | SHA-256 | Notes |
|---|---|---|
| `film/capture/fight-4k.avi` (repo, git-ignored) | `389d530aefdd03f39139f34f97d85853524bca1f13d7144a81274f3370a411a8` | 3840×2160 MJPEG 30 fps + PCM 48 kHz stereo, 24.43 s, Godot Movie Maker |
| `capture/fight-4k.mp4` (this reel, git-ignored) | `f73be6c50469717d62b28c750216ca84320b8593a39913b75929602489253f4b` | H.264 CRF 16, 30 fps, AAC 192k transcode of the AVI |
| `evidence/film/fight-inputs.jsonl` (repo) | `885e4907393e9581fb9140f49a6513984c752b995050f47ced4d7af6052d71cf` | input edges + summary (winner rivet, sfx counts) |

Method and isolation: see `CAPTURE.md`.

## Real engine screenshots and design files used

| File | SHA-256 |
|---|---|
| `evidence/screens/03b-jab-hit-boxes.png` | `a968dcfa98f3d997ec0d0a8f49fcdfbfa804ad326120f2eac431563ab93f13e0` |
| `evidence/screens/before-fix/03b-jab-hit-boxes-sprite-offset-bug.png` | `0c9270b0650d708383301a779ac340c0de266fb76b1fa4f68a26593388f5b168` |
| `design/character/pose-targets.png` | `f4e53cc60efb7d9e5a2fe951c9c63392195b87e951f8c4e55f8af6c890a52a3d` |
| `design/storyboard/03-core-action.png` | `6a98de58f5d0dbb88a4a714765b3062675395871b2759f907a73760729bc0b1e` |
| `raw/inits-ref/jab.png` | `b32783388e6197b5bda97745f4e1cdda578a2cc05baf68a5892c9c216f25d257` |
| `design/rejected/poses-v2-a.jpg` | `5ae70543c66e1eddb594b3dfe3051c7f030305bb55bb0d681b7a1615dda33d1b` |
| `raw/CHAR-JAB/CHAR-JAB_v2-st0.6_s43.png` | `7e284c8b9ba8555814e84e2962416944371e824cf426888184ed4e2d9b2c21ff` |
| `godot/assets/fighters/bolt/jab.png` | `7a4e513e4c86c623efa2134aca398202c66b2eccb2c81f1e6ee78d5b6c730a2d` |
| `godot/assets/fighters/rivet/jab.png` | `40442e170983a9860fe0792f40e688b2ae662162779f116e0914b3620e66c6cb` |
| `evidence/tests/run-01-setup-bug.txt` | `58927a4568b33c10f20018de4fc8d5df88606e467bd5ce8847fe693d4e6bf3a2` |

The composites `evidence/B02…B12-*.png` are layouts of these files built by `_tools/make_media.py` (labels
only; no pixel of the source images is redrawn). Their hashes for B05/B12 are in `gamedev-evidence.json`.

## Runtime-tree note

`game/main.tscn` contains only the root `Main` node; fighters, sprites, HUD, sfx, music, camera and FX are
created in `main.gd`/`fighter.gd` `_ready()`. The film therefore shows code, not a saved scene tree, and
claims no Inspector values (the workbench side panel is labelled "Source notes — not Inspector values").

## Models and licences (from the repo SOURCES.md)

| Model | Produced | Licence |
|---|---|---|
| SDXL-Turbo (`stabilityai/sdxl-turbo`), local, Apple M4 | all art: Bolt reference + poses (Rivet = recolour), bowl, props | Stability AI Non-Commercial Research Community License |
| AudioLDM 2, local | the six SFX (bell, jab, cutlass, pop, rewind, empty) | CC BY-NC-SA 4.0 |
| MusicGen-small, local | the waltz loop | CC BY-NC 4.0 |
| Kokoro (`am_onyx`), local | this film's narration (Liam) | toolkit default voice |

## Toolkit

Course-provided Brutalist toolkit (`_brutalist`), skills `godot-gamedev` (walker modifier) and `ai-explainer`
bookends; Remotion components `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDevWorkbench`,
`ClaudeVerdictArtifact`, `ClaudeTitleOutro`. No upstream web documentation was consulted.
