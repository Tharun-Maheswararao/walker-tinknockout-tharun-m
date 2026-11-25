# CAPTURE.md — the engine capture made for this film (B00, B03, B05, B07)

| Field | Value |
|---|---|
| Game source | tag `a7`, commit `a0c95cc` (`git archive a0c95cc godot` into a scratch folder); `godot/` and `scripts/` are byte-identical to `a5978c0`, the A7 film's source |
| Engine | Godot `4.7.2.stable.official.ed1daf0bf`, Forward+ on Vulkan (MoltenVK), Apple M4, macOS 15.6 |
| Isolation | identical to `a0c95cc` except the window override in the copy's `project.godot` (1280×720 → 3840×2160), as the A3–A7 films did; stretch `canvas_items`, so the 2D game renders natively at 4K. Imported once with `--headless --import`. The repository was not touched. |
| Flags | windowed (never `--headless`), `--disable-vsync --always-on-top --fixed-fps 60`: every physics tick is a drawn frame |

## `capture/play-4k60.mp4` — the game, SCRIPTED INPUT

- **SHA-256** `fbca3cb03290047e52934054bb87c5cdbc461530e5bb8ab560ff4d6e1a4838e2`; 628 frames (0–627), 60 fps, 3840×2160,
  H.264 CRF 14 from the Movie Maker PNG sequence; decoded back to PNG for the composites.
- **Command:** `godot --path <copy>/godot --resolution 3840x2160 --disable-vsync --always-on-top --write-movie <dir>/frame.png --fixed-fps 60 --script res://film_a8_play.gd`
- **Movie Maker summary:** `628 frames at 60 FPS (movie length: 00:00:10:28)` — the full count (the log's last line is
  process frame 627).
- **Driver:** `_tools/film_a8_play.gd` (a film tool, not part of the game), adapted from the A7 film's driver. It runs
  the unchanged `game/main.tscn`, confirms through the title and intro, and drives Bolt only with key events through
  `Input.parse_input_event` (J, K, S). Rivet's brain is replaced by a stand-in that stays idle. **Between cases both
  fighters stand IDLE and their x is SET** (logged `SETUP`, stated on screen). It writes no clip, player, rig or
  fighter state other than those x positions.
- **Log:** `evidence/runs/play-capture-log.txt`, one line per physics tick. The headless trial
  (`evidence/runs/play-headless-trial-log.txt`) gives identical tick lines except the canvas position (camera shake).

| Case | Setup | Press (e) | Logged result |
|---|---|---|---|
| 1 JAB WHIFF | gap 90 | J on tick 154 | JAB 21 ticks, IDLE on 175 |
| 2 JAB LAND | gap 70 | J on tick 249 | box opens on e+5 (254): Rivet HURT, hitstop 5 ticks, state_t held at 0.0833 through 259 |
| 3 CUTLASS LAND | gap 70 | K on tick 344 | lands on e+9 (353), hitstop |
| 4 REWIND | gap 120 | S held 435–585 | `wind_key_cycle` plays; wind 54 → 100; IDLE on release |

**Frame alignment (measured):** movie frame index = the log's `frame` field. Bolt's region first changes on movie
frame 155 (tick 154, logged frame 155) and holds from 160 to 161, as in the A7 film.

**Retiming (all labelled on screen):** "REAL SPEED · every 2nd tick" (30 fps from 60), "REPLAY · 0.5×" (one tick per
film frame), "REPLAY · 0.25×" (each tick twice); a segment shorter than its slot repeats and says "repeat".

Movie Maker is an offline deterministic render. It says nothing about any real-time frame rate; the only clock
figures in the film are TEST-REPORT A7-9e's, quoted with the machine named.

## Test re-runs — `evidence/runs/tests-a0c95cc/`

Second isolated copy (`git archive a0c95cc godot scripts`), imported, then from its root with two arguments each:
pins 60 and 30 (49 / 0), structure 60 and 30 (57 / 0), edges 60 (70 / 0). A first loop passed "test fps" as one
argument (zsh does not split words), which loads nothing and exits 0; its logs were discarded and the runs repeated.
