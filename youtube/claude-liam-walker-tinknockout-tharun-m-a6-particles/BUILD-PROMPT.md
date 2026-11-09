# BUILD-PROMPT.md — how this reel is produced (paste-ready)

Skill: course-provided Brutalist `godot-gamedev` with the `walker` modifier, ai-explainer bookends, OUTRO-LOCK card.
Modelled on the A5 film (`../claude-liam-walker-tinknockout-tharun-m-a5-shaders/`).

```text
godot-gamedev walker /Users/tharunmaheswararao/Documents/csye7270/walker-tinknockout-tharun-m
Reel: youtube/claude-liam-walker-tinknockout-tharun-m-a6-particles  ·  game source and docs c844ab2
Never edit godot/, CHANGE-BRIEF, TUNING, TEST-REPORT, FRICTIONAL, SOURCES, README or CLAUDE.md;
no commit, tag, push, upload or publish. The GPU price is pending: never invent it.
```

## Order of operations (REEL = the reel folder; toolkit commands from `_brutalist/`)

1. Read `godot-gamedev/SKILL.md`, `references/evidence.md`, `OUTRO-LOCK.md`, `RENDER-4K-AND-UPLOAD.md`,
   `CLAUDE-CODE-VISUAL-QC-CHECK.md`, the A6 sources, and the A5 reel's tools and records.
2. Isolated copy: `git archive c844ab2 godot | tar -x -C <scratch>/copy`. Set the copy's window override to
   3840×2160, then `godot --headless --path <copy>/godot --import`. Make a headless trial of `_tools/film_play.gd`,
   then a windowed Movie Maker run with `--disable-vsync --always-on-top --fixed-fps 30` (CAPTURE.md). Check the
   summary reports 382 frames. Encode to `capture/play-4k.mp4` and copy the log to `evidence/runs/play-capture-log.txt`.
   Key positions: run `_tools/film_play_pos.gd` headless → `evidence/runs/keypos-headless-replay-log.txt`.
3. Tests: `git archive c844ab2 godot scripts` into a second copy, import, then `./scripts/run-test.sh` for the four
   A6 tests at 60 and `cost_effects.gd 60 300` → `evidence/runs/tests-c844ab2/`.
4. `python3 REEL/_tools/build_sheet.py` → `beat_sheet.json` (asserts the shown files equal c844ab2; excerpts verbatim).
5. `.venv/bin/python runtime/scripts/generate_audio_kokoro.py REEL` (Kokoro am_onyx), then
   `python3 REEL/_tools/patch_timing.py`.
6. `.venv/bin/python runtime/scripts/remotion_scenes.py REEL --only B05` (pilot), then the other Remotion beats.
   `ffmpeg -i capture/play-4k.mp4 -start_number 0 media/_work/play/frame%08d.png`, then
   `python3 REEL/_tools/make_media.py all` (every quotation asserted verbatim by `Q()`).
7. `.venv/bin/python REEL/_tools/selfcheck.py` (GATE T functions on the composites, real images masked) → `_qc/SELFCHECK.md`.
8. `python3 REEL/_tools/make_shotlist.py`; `python3 REEL/_tools/make_evidence.py`;
   `./art godot-gamedev --check REEL --game ../walker-tinknockout-tharun-m/godot`.
9. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape` (with `.venv/bin` first on PATH).
10. `python3 REEL/_tools/review_master.py <master>`; look at the frames → `_qc/HUMAN-REVIEW.md`.
