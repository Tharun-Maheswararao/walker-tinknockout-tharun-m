# CAPTURE.md — how this film's gameplay was recorded

## Build under capture

| Field | Value |
|---|---|
| Game | walker-tinknockout-tharun-m |
| Revision | `64c037a` |
| Engine | `4.7.2.stable.official.ed1daf0bf` |
| Host | macOS (Darwin 24.6.0), Apple M4 |
| Capture | `film/capture/fight-4k.avi`, sha256 `389d530aefdd03f39139f34f97d85853524bca1f13d7144a81274f3370a411a8` |

## Method

Godot **Movie Maker** (`--write-movie … --fixed-fps 30`), an offline deterministic render of the real
viewport **and the game's own audio mix** (PCM 48 kHz). This is not evidence of real-time frame rate.

```bash
godot --path <isolated-copy>/godot --resolution 3840x2160 --write-movie fight-4k.avi --fixed-fps 30 \
      --script res://tools/capture_film.gd -- fight
```

Transcoded for the film to H.264 CRF 16, 30 fps, AAC 192k (`capture/fight-4k.mp4`).

## Isolation

Captured from `/private/tmp/claude-501/filmwork/godot`, identical to `64c037a` except the window override in
`project.godot` (1280×720 → 3840×2160). The project's logical viewport is 640×360, so 3840×2160 is an exact
6× render, not an upscale. The submitted project is unchanged.

## Input integrity — SCRIPTED INPUT

`godot/tools/capture_film.gd` presses keys only through `Input.action_press` / `Input.action_release` and
parsed input events. It observes positions, wind and states to decide *when* to press (a scripted player), and
never writes position, velocity, state, hp or wind. Rivet is driven by its normal `rivet_brain.gd`. Every input
edge is in `evidence/film/fight-inputs.jsonl`; summary: Rivet wins by KO, Bolt hp 0, Rivet hp 60.2, sfx counts
bell 2, jab 13, cutlass 3, pop 1, rewind 26, empty 1.

## How the film uses it

| Beat | Interval (s) | Audio | Framing |
|---|---|---|---|
| B07 | 10.50–23.51 | removed (narrated) | inset 2944×1656 on cream, label lines above/below |
| B09 | 1.80–18.93 | removed (narrated) | same |
| B10 | 0.00–24.43 (whole take) | **game audio preserved, no narration** | same, label "GAME AUDIO — NO NARRATION · SCRIPTED INPUT" |

No retiming, no held frames, no reordering. The 76.7 % inset (2944×1656, downscaled from native 3840×2160) keeps the game HUD and the film's own labels inside title-safe; a first 90 % layout put the label line above the safe box and GATE V blocked it (edge-bleed).

Shot type: these beats are typed `SCREEN` (same user-capture method as `CAPTURE` in `beat_plan.py`) with `capture_kind` recording that they are Godot Movie Maker gameplay; see `_qc/HUMAN-REVIEW.md` for why.

## Caveat

This 4K take is not frame-identical to the headless dry run: physics stepping changes under `--fixed-fps`, so
the scripted player's decisions land on different frames and the round plays out differently. The film shows
the 4K take as recorded.
