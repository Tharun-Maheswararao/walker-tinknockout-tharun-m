# CAPTURE.md — the one new engine capture in this film (B18)

| Field | Value |
|---|---|
| Game source | commit `1d93dcb89ebd16f1d09d423b2787087bebcded5a` (`git archive 1d93dcb godot`) |
| Engine | Godot `4.7.2.stable.official.ed1daf0bf`, GL Compatibility, macOS 15.6 (Darwin 24.6.0), Apple M4 |
| Capture | `capture/orbit-4k.mp4` — 840 frames, 30 fps, 3840×2160, H.264 CRF 14 from the Movie Maker PNG sequence |
| Driver | `_tools/film_orbit.gd`, copied into the copy as `res://film_orbit.gd` (film tool, not part of the game) |
| Log | `evidence/runs/orbit-capture-log.txt` ("840 frames at 30 FPS … recorded in 00:02:38") |

```bash
godot --path <copy>/godot --resolution 3840x2160 --write-movie <copy>/orbit/frame.png --fixed-fps 30 --script res://film_orbit.gd
```

**Isolation.** Captured from a scratch copy, identical to 1d93dcb except the window override in that copy's
`project.godot` (1280×720 → 3840×2160); a first attempt without it was clamped to 1280×720 and discarded. The 3D
viewport therefore renders natively at 3840×2160 (not an upscale). The repo is unchanged.

**What the script does.** It instantiates the unchanged `prop_room.tscn`, holds the scene's own saved Camera3D
(0, 1.6, 5.5) for 120 frames (4 s), then moves that same camera on a 5.5 m circle at 1.6 m height, looking at
(0, 0.9, 0), one turn in 720 frames. It never touches the props, light, floor or any resource. There is no player
input: this is a camera move for inspection, not gameplay, and it is **not** the student's look check (labelled on screen).

**How the film uses it.** B18 shows frames 0–629 (0.00–21.00 s, the first 630 of 840) inset at 2944×1656 on cream,
no retiming, no holds, no audio (the scene has none). Movie Maker is an offline deterministic render, not evidence of
real-time frame rate.

## Other engine runs made for the film (isolated copies of 1d93dcb, never the repo)

| Output | What | Result |
|---|---|---|
| `evidence/runs/check_props3d-isolated-1d93dcb.txt` | `godot --headless --path godot --import`, then `timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60` | `RESULT: PASS (0 failing)`, exit 0; identical to `evidence/check_props3d.txt` |
| `evidence/runs/repro-global_transform.txt` | throwaway copy, line 46 `to_root(mi)` → `mi.global_transform` | ERROR `!is_inside_tree()`, every room check PASS with castle x −0.90..0.90, RESULT PASS, exit 0 |
| `evidence/runs/repro-parse-error.txt` | throwaway copy, line 10 `const TOL := 0.01 +` | parse error, no RESULT line, exit 0 |

The `exit N` lines were appended by the film's shell. The two repro outputs are re-creations for this film, labelled
"RE-CREATION FOR THIS FILM" on screen, not the original runs.
