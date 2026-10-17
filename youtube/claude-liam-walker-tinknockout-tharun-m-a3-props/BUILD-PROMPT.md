# BUILD-PROMPT.md — how this reel is produced (paste-ready)

Skill: course-provided Brutalist `godot-gamedev` with the `walker` modifier, ai-explainer bookends, OUTRO-LOCK card.

```text
godot-gamedev walker /Users/tharunmaheswararao/Documents/csye7270/walker-tinknockout-tharun-m
Reel: youtube/claude-liam-walker-tinknockout-tharun-m-a3-props  ·  game source 1d93dcb  ·  docs fd99467
Never edit godot/, assets/, tools/, evidence/ or the A3 docs; no commit, tag, push, upload or publish.
```

## Order of operations (run from `_brutalist/`; REEL = the reel folder)

1. Read `godot-gamedev/SKILL.md`, `references/evidence.md`, `ai-explainer`, `riff`, `godot-waikthrough` capture
   contract, `RENDER-TARGETS.md`, `docs/PIPELINE-SAFETY.md`, `OUTRO-LOCK.md`; `./art scenes "Godot editor code scene tree inspector assets"`.
2. Isolated copy: `git archive 1d93dcb godot | tar -x -C <scratch>/check`; `godot --headless --path godot --import`;
   `timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60` → `evidence/runs/`.
3. Throwaway copies for the two re-creations (line 46 global_transform; line 10 parse error) → `evidence/runs/`.
4. Movie Maker orbit (CAPTURE.md) → `capture/orbit-4k.mp4`.
5. `python3 REEL/_tools/build_sheet.py` → `beat_sheet.json` (asserts the source is unchanged; excerpts verbatim).
6. `.venv/bin/python runtime/scripts/generate_audio_kokoro.py REEL` (Kokoro am_onyx), then `python3 REEL/_tools/patch_timing.py`.
7. `python3 REEL/_tools/make_media.py all` (composites of real files + B18 capture cut); pilot GodotDevWorkbench (B17)
   with `runtime/scripts/remotion_scenes.py REEL --only B17`, inspect, then the remaining Remotion beats.
8. `.venv/bin/python REEL/_tools/selfcheck.py` (GATE T functions on the STILL composites, real images masked) → `_qc/SELFCHECK.md`.
9. `python3 REEL/_tools/make_evidence.py`; `./art godot-gamedev --check REEL --game ../walker-tinknockout-tharun-m/godot`.
10. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape` (with `.venv/bin` first on PATH).
11. Inspect the master (frames at code reading size, labels, outro, audio levels) → `_qc/HUMAN-REVIEW.md`; re-run the check.
