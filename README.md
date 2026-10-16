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

**Final film:** [claude-liam-walker-tinknockout-tharun-m-gamedev.mp4](https://drive.google.com/file/d/1vp5DGYY0RXe-cttXE4endf4W7YCuIrck/view?usp=sharing) (Google Drive, 4K, 6:46). SHA-256 `8c6c491bb59df135f083786f04832c0b68c3f74a2b47c13303581a1e86edeb83`. Shows source revision `64c037a`. The MP4 is kept out of GitHub; the reel's beat sheet, evidence ledger and QC records are in `youtube/claude-liam-walker-tinknockout-tharun-m-gamedev/`.

---

## Assignment 3 — three 3D props (tag `a3`)

**Added:** a small Godot 3D scene `godot/prop_room/prop_room.tscn` (floor, one light, a camera) with three props at character scale (Bolt = 1.80 m): the **sunken-castle ornament** (environment), the **winding key** pickup (collectible) and the **toy box** (prop). Built in Blender from primitives, exported as `.glb` to `godot/assets/props3d/`, with `.blend` sources in `assets/blender/` and build code in `tools/blender/`.

**Versions:** Godot 4.7.2.stable · Blender 5.2.2 LTS · MCP for Blender 2.1.9 (add-on 1.8) · macOS 15.6.

**Routes:** castle = Blender MCP; windkey and toybox = script route (headless Blender). See TEST-REPORT.md "Assignment 3".

**Run the check** (from the repo root; `timeout` is from Homebrew coreutils):
```bash
godot --headless --path godot --import
```
```bash
timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60
```
Expect `RESULT: PASS (0 failing)`. Read that line: Godot exits 0 even if the script fails to parse.

**Open the scene:** `godot --path godot -e`, then open `res://prop_room/prop_room.tscn` and press F6.

**Rebuild an asset:** `blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_<asset>.py`, then `blender -b assets/blender/<asset>.blend --python-exit-code 1 --python tools/blender/export_glb.py -- godot/assets/props3d/<asset>.glb`.

**Known limitations (A3):** only the castle went through the MCP; the other two used the script route. The prop room is not connected to the 2D game. Look-checks from behind and below are recorded in TEST-REPORT A3-7. The A3 film: see SUBMISSION.md.

Docs for A3: CHANGE-BRIEF.md (bottom), BLENDER-NOTES.md, TEST-REPORT.md (bottom), FRICTIONAL.md (bottom), SOURCES.md (bottom).
