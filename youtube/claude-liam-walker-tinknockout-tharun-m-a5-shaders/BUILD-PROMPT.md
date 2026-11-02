# BUILD-PROMPT.md — how this reel is produced (paste-ready)

Skill: course-provided Brutalist `godot-gamedev` with the `walker` modifier, ai-explainer bookends, OUTRO-LOCK card.
Modelled on the A3 film (`../claude-liam-walker-tinknockout-tharun-m-a3-props/`).

```text
godot-gamedev walker /Users/tharunmaheswararao/Documents/csye7270/walker-tinknockout-tharun-m
Reel: youtube/claude-liam-walker-tinknockout-tharun-m-a5-shaders  ·  game source 2e6946d  ·  docs 93aedd9
Never edit godot/ (game, shaders), CHANGE-BRIEF, FRICTIONAL, SUBMISSION, README, TEST-REPORT, SOURCES or
LANGUAGE-NOTES; no commit, tag, push, upload or publish.
```

## Order of operations (REEL = the reel folder; toolkit commands from `_brutalist/`)

1. Read `godot-gamedev/SKILL.md`, `references/evidence.md`, `OUTRO-LOCK.md`, `RENDER-4K-AND-UPLOAD.md`,
   `CLAUDE-CODE-VISUAL-QC-CHECK.md`, and the A3 reel's tools and records.
2. Isolated copy: `git archive 2e6946d godot | tar -x -C <scratch>/copy`; set the copy's window override to
   3840×2160; `godot --headless --path <copy>/godot --import`; Movie Maker run of `_tools/film_rewind.gd`
   (windowed; CAPTURE.md) → `capture/rewind-4k.mp4`, `evidence/runs/rewind-capture-log.txt`.
3. `python3 REEL/_tools/build_sheet.py` → `beat_sheet.json` (asserts the shown source equals 2e6946d; excerpts verbatim).
4. `.venv/bin/python runtime/scripts/generate_audio_kokoro.py REEL` (Kokoro am_onyx), then `python3 REEL/_tools/patch_timing.py`.
5. `.venv/bin/python runtime/scripts/remotion_scenes.py REEL` (pilot B03 first) and `python3 REEL/_tools/make_media.py all`
   (B06 decodes `capture/rewind-4k.mp4` into `media/_work/rewind/` first:
   `ffmpeg -i capture/rewind-4k.mp4 -start_number 0 media/_work/rewind/frame%08d.png`).
6. `.venv/bin/python REEL/_tools/selfcheck.py` (GATE T functions on the composites, real images masked) → `_qc/SELFCHECK.md`.
7. `python3 REEL/_tools/make_evidence.py`; `./art godot-gamedev --check REEL --game ../walker-tinknockout-tharun-m/godot`.
8. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape` (with `.venv/bin` first on PATH).
9. `python3 REEL/_tools/review_master.py <master>`; look at the frames → `_qc/HUMAN-REVIEW.md`.
