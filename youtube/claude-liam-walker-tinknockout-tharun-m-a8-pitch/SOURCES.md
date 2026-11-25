# SOURCES.md — the A8 pitch film

## What is on screen, and where it came from

- **Real play:** `capture/play-4k60.mp4`, a Movie Maker capture made for this film from an isolated
  `git archive a0c95cc` copy of the game (tag `a7`), scripted input (`_tools/film_a8_play.gd`). Method, hash and
  frame count in `CAPTURE.md`; per-tick log in `evidence/runs/play-capture-log.txt`.
- **Recorded output:** the three A7 suites re-run for this film on a second isolated copy of `a0c95cc`
  (`evidence/runs/tests-a0c95cc/`).
- **Code views:** `godot/fighter/fighter.gd:41-45` and `godot/game/main.gd:180-182` at `a0c95cc`, verbatim, in the
  toolkit's `GodotDevWorkbench` (a labelled Godot editor reconstruction), checked by `./art godot-gamedev --check`.
- **Constructed pictures:** the training room, the frame-data overlay and the `Fighter.tscn` scene tree are drawings
  made in code by `_tools/make_media.py`, labelled CONSTRUCTED on screen. Bolt's idle sprite in B01 is the A2 game
  art (`godot/assets/fighters/bolt/idle.png`, SDXL-Turbo, Stability AI Non-Commercial Research Community License).
- **Words:** `pitch/PROJECT-BRIEF.md` (Tharun's seven answers) and `pitch/EXISTS-FACTS.md` at `fcb873c`;
  measurements quoted from `TEST-REPORT.md` A7-9e at `a0c95cc`.
- **Comparable games:** Street Fighter 6 and Tekken 8 are named in narration and text only. No footage, art,
  logos or music from them.

## Tools and licences

- Godot 4.7.2.stable.official.ed1daf0bf (Forward+, Vulkan/MoltenVK), macOS 15.6, Apple M4. Movie Maker for the
  capture.
- Brutalist toolkit (`_brutalist/`): Kokoro-82M TTS (`am_onyx`, local, free), Remotion (`GodotDevWorkbench`),
  ffmpeg, and its gates (GATE T `type_check.py`, GATE V `final_frame_check.py`, `godot-gamedev --check`).
- Fonts: EB Garamond, Inter, Lato, PT Mono (SIL Open Font License, shipped with the toolkit).
- No music, no sound effects, no generated images or video.

## Who did what

- **Tharun:** every pitch choice (in `PROJECT-BRIEF.md`, which he reviewed and approved), and the game work shown.
- **Claude (this session):** the script adapted from the brief, the capture driver, the captures, the test re-runs,
  the composites and the render. Nothing in the repository outside this folder and the listed `pitch/` records was
  changed. Nothing was committed, pushed, uploaded or published.
