# CAPTURE.md — the two engine captures made for this film (B02, B06, B08, B14, B19, B20)

| Field | Value |
|---|---|
| Game source | commit `a5978c0` (`git archive a5978c0 godot` into a scratch folder) |
| Engine | Godot `4.7.2.stable.official.ed1daf0bf`, Forward+ on Vulkan 1.2.334 (MoltenVK), Apple M4, macOS 15.6 |
| Isolation | identical to `a5978c0` except the window override in the copy's `project.godot` (1280×720 → 3840×2160, as the A3, A5 and A6 films did). Stretch mode `canvas_items`, so the 2D game renders natively at 3840×2160. The repository was not touched. Imported once with `godot --headless --path <copy>/godot --import`. |
| Flags | windowed (never `--headless`), `--disable-vsync --always-on-top --fixed-fps 60` (CLAUDE.md capture rule). 60 fps, as the A7 strips are, so every physics tick is a drawn frame. |

## 1. The game, scripted input — `capture/play-4k60.mp4`

- **SHA-256** `7f76dbd73b2480f1913d8a51c02e079529cf5d1422e76aa69aa52af8faff8020`; 818 frames (0–817), 60 fps,
  3840×2160, H.264 CRF 14, encoded from the Movie Maker PNG sequence. Decoded back to PNG for the composites.
- **Command:** `godot --path <copy>/godot --resolution 3840x2160 --disable-vsync --always-on-top --write-movie <dir>/frame.png --fixed-fps 60 --script res://film_a7_play.gd`
- **Driver:** `_tools/film_a7_play.gd`, copied into the copy as `res://film_a7_play.gd` (a film tool, not part of the game).
- **Movie Maker summary:** `818 frames at 60 FPS (movie length: 00:00:13:38)` — the full count.
- **Log:** `evidence/runs/play-capture-log.txt`, one line per physics tick (817 lines): Bolt's state, `state_t`,
  `BodyPivot` x / rotation, `KeyBob` y, `FighterAnimPlayer` clip and position, `key_sprite.frame`, `KeyAnimPlayer`
  clip, wind, hitstop, Rivet's state and wind, the gap, Bolt's HP and canvas position. A headless trial of the same
  script (`evidence/runs/play-headless-trial-log.txt`) gives identical tick lines except the canvas position (camera
  shake is random).

**What the script does (SCRIPTED INPUT, labelled on screen).** It instantiates the unchanged `game/main.tscn`, taps
`confirm` through the real input path and waits through the intro. Bolt is driven only by key events through
`Input.parse_input_event` (J, S), scheduled one tick ahead as `test_a7_edges.gd` does. Rivet's brain is replaced by a
stand-in with a fixed plan (the edge test's `ScriptBrain` method): idle, except one cutlass request per interrupt case.
**Between cases both fighters stand IDLE and their x is SET** (logged as `SETUP`); the film says so in narration and
on screen. It never writes a clip, a player, the rig or any fighter state other than those x positions.

| Case | Setup | Bolt's jab starts (e) | Logged result |
|---|---|---|---|
| 1 WHIFF | gap 90 | tick 154 | JAB 21 ticks; IDLE on 175; clip at `state_t` every tick |
| 2 LAND | gap 70 | tick 249 | box opens on e+5 (254): Rivet HURT; hitstop; clip position 0.0833 on ticks 254–259, 0.1000 on 260 |
| 3 STARTUP | gap 90, cutlass requested 338 | tick 344 | Bolt HURT on 347 (e+3), no clip, rig 0 / 0 / 0 |
| 4 ACTIVE | gap 90, cutlass requested 437 | tick 439 | Bolt HURT on 446 (e+7), no clip, rig at rest |
| 5 RECOVERY | gap 90, cutlass requested 540 | tick 534 | Bolt HURT on 549 (e+15), no clip, rig at rest |
| 6 REWIND | gap 120, S held 625–775 | — | `wind_key_cycle` from 625; wind 40 → 100 by tick 715 (six clicks, `state_t` 1.5); key holds frame 4 to 774; IDLE and frame 0 on 775 |

The hit ticks match `test_a7_edges.gd` E3's timing (Rivet's cutlass lands on its 9th tick, so a hit on e+k is
requested on e+k−9).

**Frame alignment (measured).** Movie frame index = the `frame` field (process frame) of the tick's log line. The
jab image first differs on movie frame 155 (tick 154, logged frame 155); the +14 px lunge on 160 (tick 159, frame 160);
frame 161 is identical to 160 (the hold). `evidence/runs/frame-alignment.json`.

**Retiming in the film (all labelled).** B19: real speed (every second tick at 30 fps), a 0.5× replay of case 1 (one
tick per film frame) and a 0.25× replay of case 2 (each tick twice). B20: cases 3–5 side by side, synchronised on each
jab's start tick e, at 0.25×, looped with a `repeat` counter; then case 6 at real speed, looped. A segment longer than
its source repeats and says so. B08: nine consecutive ticks as held frames. B02, B06: held frames.

## 2. The key-cycle fixture — `capture/key-cycle-4k60.mp4`

- **SHA-256** `fe5db1fbdb12d6aeb97a2e3fecb5cdcbf303e44e77686c8e4fd8c475ac482c7f`; 380 frames (0–379), 60 fps, 3840×2160.
- **Command:** `godot --path <copy>/godot res://previews/key_cycle_preview.tscn --resolution 3840x2160 --disable-vsync --always-on-top --write-movie <dir>/frame.png --fixed-fps 60 --quit-after 380`
- **FIXTURE, not gameplay** (labelled): the preview holds REWIND from tick 10 and tops wind to 50 every tick, so the
  key never reaches full wind (`key_cycle_preview.gd:1-19`). Its own per-tick log: `evidence/runs/key-cycle-capture-log.txt`
  (six 7 → 0 wraps, at ticks 70, 131, 191, 251, 311, 371).
- **Movie Maker summary (run 2):** `380 frames at 60 FPS (movie length: 00:00:06:20)` — the full count. Every
  key-cell change, and the REWIND pose on tick 10, first differs on the movie frame of the same number.
- **Run 1, discarded:** its summary said `373 frames` for `--quit-after 380`, and movie frames 10–16 repeated the idle
  pose although the log was in REWIND from tick 10 (the stale-frame behaviour CLAUDE.md describes). Its log is kept as
  `evidence/runs/key-cycle-capture-run1-DISCARDED-log.txt`; its frames are not used.
- **B14:** real speed (every second tick), then a labelled 0.25× replay around the fifth wrap.

## Committed fixture strips (not made for this film)

The jab strips (B10, B16, B18) are Tharun's fixture captures in `captures/jab_action/` (`jab_preview.tscn`, x 207,
60 fps, 1280×720), shown as labelled held frames and zooms. None is presented as gameplay.

Movie Maker is an offline deterministic render. It says nothing about the real-time frame rate; the only real-time
clock figure in the film is Tharun's CLOCKS line (TEST-REPORT A7-9e), quoted.
