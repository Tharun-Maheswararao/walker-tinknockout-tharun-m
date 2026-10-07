# BUILD-PROMPT.md — how this reel was produced

Skill: `godot-gamedev` with the `walker` modifier, from the course-provided Brutalist toolkit (`_brutalist`),
with `ai-explainer` bookends and the OUTRO-LOCK card.

```text
godot-gamedev walker /Users/tharunmaheswararao/Documents/csye7270/walker-tinknockout-tharun-m
```

## Order of operations

1. Read `godot-gamedev/SKILL.md`, `references/evidence.md`, `scripts/verify_gamedev.py`, `ai-explainer/SKILL.md`
   (bookends), `OUTRO-LOCK.md`, `docs/PIPELINE-SAFETY.md`, `RENDER-TARGETS.md`, the `GodotDevWorkbench` source;
   ran `./art scenes "Godot editor code scene tree inspector assets"`.
2. Read every runtime script under `godot/` and the repo design documents; watched the 4K capture as frame strips.
3. Ran `tests/test_slice.gd` on an isolated `git archive 64c037a godot` copy (25 checks, 0 failed) and
   `tools/edit/check_seam.py` (PASS).
4. `_tools/build_sheet.py` → `beat_sheet.json` (excerpts read verbatim from the frozen files).
5. `runtime/scripts/generate_audio_kokoro.py REEL` (Kokoro `am_onyx`); audio durations set the clock.
6. `_tools/patch_timing.py`: Remotion `durationSeconds` = measured narration; code-line cues placed where the
   line number is spoken; outro padded with the OUTRO-LOCK 1.0 s silent tail.
7. `_tools/make_media.py stills|capture`: composites of real files (B02, B03, B05, B12) and frame-exact capture
   cuts (B07, B09 silent; B10 with the game's audio).
8. Piloted one `GodotDevWorkbench` beat (B04), inspected the frame, then `runtime/scripts/remotion_scenes.py REEL`.
9. `_tools/make_evidence.py` → `gamedev-evidence.json`; `./art godot-gamedev --check REEL --game godot`.
10. `./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape`.
11. Inspected the master (frames, volumedetect over B10, dimensions) — `_qc/HUMAN-REVIEW.md`.

No game file was edited, nothing was committed or pushed, nothing was uploaded.

## Gates

godot-gamedev --check PASS · GATE T PASS · GATE V PASS (0 BLOCKER, 0 MAJOR) · export receipt `ready`. Details and the SCREEN-type decision: `_qc/HUMAN-REVIEW.md`.
