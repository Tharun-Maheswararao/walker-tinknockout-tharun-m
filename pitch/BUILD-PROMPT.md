# BUILD-PROMPT.md — how the A8 pitch film is built (paste-ready)

Toolkit: the course-provided Brutalist toolkit (`_brutalist/`), `godot-gamedev` workflow with the `walker` modifier,
adapted for a pitch (see "Departures" below). Mechanics modelled on the A7 film
(`youtube/claude-liam-walker-tinknockout-tharun-m-a7-animation/`). Built by a Claude Code session (Claude Opus 5.5,
desktop app) on 2026-11-24, started from the main A8 session.

## The prompt

```text
Build Tharun's Assignment 8 final-project pitch film with the course-provided Brutalist toolkit, then place its
required records in the repo's pitch/ folder.

Read first: the repo at commit fcb873c: pitch/PROJECT-BRIEF.md (the script's source: the seven answers, in Tharun's
voice), pitch/EXISTS-FACTS.md, pitch/README.md, pitch/SOURCES.md. Toolkit: _brutalist/ (README,
skills/make/godot-gamedev/SKILL.md). Use the godot workflow with the walker modifier and keep beats simple: one
picture, one idea per beat, minimal on-screen text, narration carrying the explanation. Model the mechanics on the
A7 reel (its BUILD-PROMPT.md, _tools/, capture and gate steps).

The film: 2–4 minutes, landscape, native 4K through ./art final … --height 2160 --fps 30, all of the toolkit's
quality gates passed. Reel folder: youtube/claude-liam-walker-tinknockout-tharun-m-a8-pitch/. Narration (Kokoro)
speaks as Tharun in the first person; never use the instructor's name, persona or credit line. Answer the seven
questions in PROJECT-BRIEF order, and end with exists-today vs will-exist.

Honesty rule: past tense only for what exists at a named tag; everything else is "will". Gameplay footage is real
captured play from tag a7 (a0c95cc), from an isolated git archive copy with Movie Maker
(--disable-vsync --always-on-top --fixed-fps 60), revision named on screen, scripted input labelled SCRIPTED INPUT.
The training room, the frame-data overlay and Fighter.tscn do not exist: any picture of them is labelled
CONSTRUCTED. No invented players, quotes, metrics, studios or results; only EXISTS-FACTS §3 measurements, machine
named. No Claude response unless actually received. Never claim a build, a build frame rate, or playtests by others.

Rules: never edit godot/, scripts/, the root docs or pitch/PROJECT-BRIEF.md. No commit, tag, push, upload or publish.
```

## Order of operations (REEL = the reel folder; toolkit commands from `_brutalist/`)

1. Read the brief, the facts, `skills/make/godot-gamedev/SKILL.md` and `references/evidence.md`, `OUTRO-LOCK.md`,
   and the A7 reel's tools and records.
2. Isolated copy: `git archive a0c95cc godot | tar -x -C <scratch>/copy`; in the copy only, the window override
   1280×720 → 3840×2160 (as the A3–A7 films did); `godot --headless --path <copy>/godot --import`.
3. Copy `REEL/_tools/film_a8_play.gd` into the copy as `res://film_a8_play.gd`. Headless trial
   (`--fixed-fps 60 --script res://film_a8_play.gd` → `evidence/runs/play-headless-trial-log.txt`), then the
   windowed Movie Maker run:
   `godot --path . --resolution 3840x2160 --disable-vsync --always-on-top --write-movie <dir>/frame.png --fixed-fps 60 --script res://film_a8_play.gd`
   → `evidence/runs/play-capture-log.txt`. Check the Movie Maker summary gives the full frame count (CAPTURE.md).
   Encode the PNGs to `capture/play-4k60.mp4` (H.264 CRF 14); decode back to `media/_work/play/frame%08d.png`.
4. Tests: `git archive a0c95cc godot scripts` into a second copy, `--import`, then from its root
   `./scripts/run-test.sh test_a7_pins.gd 60`, `… 30`, `test_a7_structure.gd 60`, `… 30`, `test_a7_edges.gd 60`
   (two arguments each) → `evidence/runs/tests-a0c95cc/`.
5. `python3 REEL/_tools/build_sheet.py` → `beat_sheet.json`.
6. `.venv/bin/python runtime/scripts/generate_audio_kokoro.py REEL` (Kokoro `am_onyx`), then
   `python3 REEL/_tools/patch_timing.py` (cue times; 1.0 s silent tail on the last beat).
7. `.venv/bin/python runtime/scripts/remotion_scenes.py REEL --only B02` (pilot, inspect), then `--only B11`
   (`--force` to re-render). Then `python3 REEL/_tools/mask_handle.py B02 B11`: `GodotDevWorkbench.tsx` hardcodes the
   instructor's channel handle in the bottom-right corner; the tool keeps the untouched render as
   `media/_work/<id>.remotion.mp4` and paints only that empty corner the page colour.
8. `python3 REEL/_tools/make_media.py all` (composites; quotations asserted verbatim by `Q()`, count lines read
   from the logs).
9. `.venv/bin/python REEL/_tools/selfcheck.py` → `_qc/SELFCHECK.md` (GATE T pixel checks on the composites, real
   images masked).
10. `python3 REEL/_tools/make_shotlist.py`; `python3 REEL/_tools/make_evidence.py`;
    `./art godot-gamedev --check REEL --game ../walker-tinknockout-tharun-m/godot` → `_qc/GAMEDEV-CHECK.txt`.
11. `PATH=.venv/bin:$PATH ./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`
    (GATE T → `TYPECHECK.md`; GATE V final-frame check → `_qc/REPORT.md`).
12. `python3 REEL/_tools/review_master.py <master>`; look at the frames → `_qc/HUMAN-REVIEW.md`.

## Departures from the walker bookends (and why)

- **No reconstructed Claude prompt/response cold open.** The A8 honesty rule allows no Claude response that was not
  actually received; the pitch opens on real play and the one-sentence answer instead.
- **No "Your Turn" Walker prompt.** A pitch ends on exists-today vs will-exist.
- **No `ClaudeTitleOutro`.** That card hardcodes the instructor's handle and its spoken line names the instructor;
  the task forbids both. The film closes on its own title card (title, student, course), spoken, no music, 1.0 s
  silent tail. `compile.py`'s skin lint reports this as a warning, not a failure.
- **Handle masked on the two code views** (step 7), for the same reason. The shared toolkit was not edited.
- **Tests run with two explicit arguments.** A zsh `for` loop over "test fps" strings passes one argument, which
  loads nothing and exits 0; that first loop's logs were discarded.

## Result (2026-11-24)

Master `exports/landscape/claude-liam-walker-tinknockout-tharun-m-a8-pitch.mp4`, SHA-256
`190ed4b2491eb0d0f70284ff7fb30a94624c87ef4dbdc0fb754a2fa9fc072cdc`, 221.57 s, 3840×2160, 30 fps. Render 4 of 4:
render 1 was refused by GATE V (B15 underfill) and fixed; renders 2 and 3 passed and were superseded after frame
inspection (name overlay and clipped HUD label; then the TTS voice disclosure). Gates and the inspection are in
`_qc/HUMAN-REVIEW.md`; copies of the gate reports are in `pitch/gate-reports/`.
