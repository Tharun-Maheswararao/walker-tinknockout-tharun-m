# walker-tinknockout-tharun-m — Tin Knockout

Tin wind-up toys box in a glass bowl in a toy shop after closing. You play **Bolt**, a tin deep-sea-diver toy. Every punch, cutlass swing and cork-gun shot unwinds your spring, and rewinding leaves you open.

This repository is the **CSYE 7270 Assignment 2 asset slice**: generated art, sound effects and music, proven together in one small playable Godot scene.

- **Started from:** an empty Godot 4.7 project. Patterns (viewport, input-driven tests, capture contract) come from my Assignment 1, [walker-jumpman-tharun-m @ bb63748](https://github.com/Tharun-Maheswararao/walker-jumpman-tharun-m), which extends [nikbearbrown/walker-jumpman @ 9387542](https://github.com/nikbearbrown/walker-jumpman). No game code was reused. See [SOURCES.md](SOURCES.md).
- **Engine:** Godot 4.7.2.stable (GL Compatibility). Tested on macOS 15.6, Apple M4.

## Run

```bash
git clone https://github.com/Tharun-Maheswararao/walker-tinknockout-tharun-m.git
cd walker-tinknockout-tharun-m
godot --path godot          # or open godot/project.godot in the Godot editor and press F5
```

## Controls

| Key | Action | Pad |
|---|---|---|
| Enter / Space | start | A |
| A / D or ← / → | walk (Bolt turns to face the way he walks) | D-pad |
| J | jab (12 wind) | X |
| K | tin cutlass (22 wind) | Y |
| L | cork pop-gun (30 wind) | B |
| I or ↑ (hold) | block (in front only) | RB |
| S or ↓ (hold) | rewind the spring (one click = 10 wind) | LB |
| Esc / P | pause (music muffles) | Start |
| **M** | **mute / unmute music** | |
| **N** | **mute / unmute effects** | |
| R | rematch after K.O. | Back |
| F1 | show hurtboxes (green) and hitboxes (red) | |

## What the slice demonstrates

- **Character:** 11 generated static poses, one per state, swapped on state change, flipped at runtime for left-facing, and anchored to a 50×106 hurtbox. Rivet is a palette swap.
- **Environment:** a generated toy-shop / glass-bowl background, plus generated props (key, cutlass, pop-gun, cork).
- **Sound:** 6 generated event sounds (bell, jab, cutlass, pop, rewind click, spring-empty). Each fires once per event from gameplay signals. Gameplay never calls audio.
- **Music:** a generated waltz loop. It slows below 25 % spring, muffles on pause, and stops on K.O.
- **Readable muted:** spring dials, state labels, distinct poses, hit sparks, hitstop and K.O. text.

## Tests

```bash
godot --headless --path godot --script res://tests/test_slice.gd   # 25 checks
python tools/edit/check_seam.py                                     # music loop seam
```

## Documents

| File | Contents |
|---|---|
| [CONCEPT.md](CONCEPT.md) | concept, core loop, pillars, art and audio direction |
| [STORYBOARD.md](STORYBOARD.md) | 7 panels |
| [CHARACTER-SHEET.md](CHARACTER-SHEET.md) | the character spec |
| [CHANGE-BRIEF.md](CHANGE-BRIEF.md) | plan and predictions (committed before generation) |
| [ASSET-LOG.md](ASSET-LOG.md) | every generation: prompt, seed, outcome, edits |
| [SOURCES.md](SOURCES.md) | models, licenses, who did what |
| [TEST-REPORT.md](TEST-REPORT.md) | results |
| [FRICTIONAL.md](FRICTIONAL.md) | design log |
| [SUBMISSION.md](SUBMISSION.md) | Canvas submission |

## Known limitations

1. The sound effects and music were picked by Claude's signal analysis, not by ear (see SOURCES / TEST-REPORT).
2. The background shows the bowl from outside.
3. Rivet follows a fixed pattern, not AI.
4. Bolt's eyes are hand-painted on every pose.
5. Bolt's yellow helmet has low luminance contrast against the pink castle at his start position.
6. Only one round; there are no weapon pickups yet.

## Film

**Final film:** *link and SHA-256 added in SUBMISSION.md once rendered and uploaded* (MP4s are kept out of GitHub).
