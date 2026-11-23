# BUILD-PROMPT.md — how this reel is produced (paste-ready)

Skill: course-provided Brutalist `godot-gamedev` with the `walker` modifier, ai-explainer bookends, OUTRO-LOCK card.
Modelled on the A6 film (`../claude-liam-walker-tinknockout-tharun-m-a6-particles/`).

```text
godot-gamedev walker /Users/tharunmaheswararao/Documents/csye7270/walker-tinknockout-tharun-m
Reel: youtube/claude-liam-walker-tinknockout-tharun-m-a7-animation  ·  game source and docs a5978c0
Never edit godot/, CHANGE-BRIEF, TUNING, TEST-REPORT, FRICTIONAL, SOURCES, README, CLAUDE.md or scripts/;
no commit, tag, push, upload or publish. Tharun's verdicts are quoted as his; on the brief's drafting say only
what SOURCES.md A7 says.
```

## Order of operations (REEL = the reel folder; toolkit commands from `_brutalist/`)

1. Read `skills/make/godot-gamedev/SKILL.md`, `references/evidence.md`, `OUTRO-LOCK.md`, `RENDER-4K-AND-UPLOAD.md`,
   `CLAUDE-CODE-VISUAL-QC-CHECK.md`, the A7 sources, and the A6 reel's tools and records.
2. Isolated copy: `git archive a5978c0 godot | tar -x -C <scratch>/copy`; window override 3840×2160; `--import`.
   Headless trial of `_tools/film_a7_play.gd` (`--fixed-fps 60`), then the windowed Movie Maker run with
   `--disable-vsync --always-on-top --fixed-fps 60` (CAPTURE.md). Check the summary says 818 frames. Encode to
   `capture/play-4k60.mp4`; log → `evidence/runs/play-capture-log.txt`.
3. `key_cycle_preview.tscn` windowed Movie Maker run, `--quit-after 380`; the summary must say 380 (run 1 said 373 and
   was discarded). Encode to `capture/key-cycle-4k60.mp4`; log → `evidence/runs/key-cycle-capture-log.txt`.
   Measure the alignments → `evidence/runs/frame-alignment.json`.
4. Tests: `git archive a5978c0 godot scripts` into a second copy, import, then `./scripts/run-test.sh <test> <fps>`
   (two arguments; a single quoted "test fps" argument silently loads nothing) for the A7 suites at 60 (structure and
   pins also at 30), `test_slice` and `test_wind_steam_state` → `evidence/runs/tests-a5978c0/`.
5. `python3 REEL/_tools/build_sheet.py` → `beat_sheet.json` (asserts the shown files equal a5978c0; excerpts from git).
6. `.venv/bin/python runtime/scripts/generate_audio_kokoro.py REEL` (Kokoro am_onyx), then
   `python3 REEL/_tools/patch_timing.py`.
7. `.venv/bin/python runtime/scripts/remotion_scenes.py REEL --only B03` (pilot), then the other Remotion beats.
   `ffmpeg -i capture/<cap>.mp4 -start_number 0 media/_work/<play|key>/frame%08d.png`, then
   `python3 REEL/_tools/make_media.py all` (every quotation asserted verbatim by `Q()`).
8. `.venv/bin/python REEL/_tools/selfcheck.py` (GATE T functions on the composites, real images masked) → `_qc/SELFCHECK.md`.
9. `python3 REEL/_tools/make_shotlist.py`; `python3 REEL/_tools/make_evidence.py`;
   `./art godot-gamedev --check REEL --game ../walker-tinknockout-tharun-m/godot`.
10. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape` (with `.venv/bin` first on PATH).
11. `python3 REEL/_tools/review_master.py <master>`; look at the frames → `_qc/HUMAN-REVIEW.md`.
