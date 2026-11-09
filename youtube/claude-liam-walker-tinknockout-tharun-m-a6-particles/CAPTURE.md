# CAPTURE.md — the one new engine capture in this film (B02, B10, B16)

| Field | Value |
|---|---|
| Game source | commit `c844ab2` (`git archive c844ab2 godot` into a scratch folder) |
| Engine | Godot `4.7.2.stable.official.ed1daf0bf`, Forward+ on Vulkan 1.2.334 (MoltenVK), Apple M4, macOS 15.6 |
| Capture | `capture/play-4k.mp4`: 382 frames (0–381), 30 fps, 3840×2160, H.264 CRF 14, encoded from the Movie Maker PNG sequence |
| Driver | `_tools/film_play.gd`, copied into the copy as `res://film_play.gd` (a film tool, not part of the game) |
| Log | `evidence/runs/play-capture-log.txt`: every frame's Bolt/Rivet state, Bolt's wind, both `amount_ratio`s, live burst nodes, key `scale.x`, `paused` |

```bash
godot --path <copy>/godot --resolution 3840x2160 --disable-vsync --always-on-top --write-movie <dir>/frame.png --fixed-fps 30 --script res://film_play.gd
```

The capture ran **windowed**, never `--headless`, after `godot --headless --path <copy>/godot --import` on the copy.
The flags `--disable-vsync --always-on-top --fixed-fps 30` follow CLAUDE.md's capture rule.

**Frame count.** Movie Maker's summary: `382 frames at 30 FPS (movie length: 00:00:12:22)`. The script logged frame
382 as its last frame, so the full count was written. Frames identical to the frame before are the title screen
(frames 1–52) and short moments where nothing on screen moves (fighters in static poses, no burst alive). They match
the log's own static stretches. They are not Movie Maker duplicates. The summary's "GPU render time" line is Movie
Maker's own report for a 4K offline render. It is **not** the A6 GPU price and the film does not use it.

**Isolation.** Captured from a scratch copy, identical to `c844ab2` except the window override in that copy's
`project.godot` (1280×720 → 3840×2160, as the A3 and A5 films did). Stretch mode is `canvas_items`, so the 2D game
renders natively at 3840×2160 (not an upscale). The repository was not touched.

**What the script does (SCRIPTED INPUT, labelled on screen).** It instantiates the unchanged `game/main.tscn`, taps
`confirm` through the real input path (`Input.parse_input_event`) and waits through the intro. It waits until Rivet
(the game's own brain) is within 78 px. It taps `jab` each time Bolt is IDLE, until 8 jabs have started. Then it
waits 1 s, taps `pause`, waits about 1 s, taps `pause` again, holds `rewind` (`Input.action_press`) for 45 frames,
releases it, and quits after 36 more frames. It never touches an effect, its values or `amount_ratio`. The game's
`main._spawn_impact` and `steam_ratio` do that.

**What happened (from the log).**
- Jabs 1, 3, 5 and 7 landed and spawned `impact_effect.tscn`. Jabs 2, 4, 6 and 8 were blocked by Rivet (his brain
  blocks every other visible jab startup) and spawned `impact_effect_blocked.tscn`.
- Rivet's own hits on Bolt spawned normal bursts at log frames 125, 162, 200, 237 and 291.
- Bolt's wind: 100 → 88 → … → 28 after jab 6; jab 7 → 16 (ratio 0.36); jab 8 → 4 (ratio 0.84).
- Paused for log frames 259–289. Rivet hit Bolt right after the pause ended.
- REWIND from log frame 304. Ratio 0.44 at 311, 0.04 at 319, 0 at 326.

**Frame alignment.** A burst first shows in movie frame N − 1 for a spawn logged at frame N (spawns at log 102, 125
and 141 first show cyan pixels in movie frames 101, 124 and 140). So the readouts use **log frame = movie frame + 1**.

**Pause check (measured).** Between movie frames 262, 272, 282 and 287 (all paused), the only pixels that change by
more than 10 levels lie in a box of about 110 × 140 px at Bolt's key (x 805–917, y 1317–1467): the steam. The fight
is frozen.

**Zoom position.** The B16 zoom (4K box x 590–1190, y 1221–1559) covers Bolt's key throughout. Its screen position
came from a headless replay of the same script that also printed the key's canvas position
(`_tools/film_play_pos.gd`, `evidence/runs/keypos-headless-replay-log.txt`). All 382 of its state lines are
identical to the 4K run's, so the replay is the same sequence.

**How the film uses it.**
- **B02:** held frames 141 (a landed jab's burst) and 252 (steam at wind 4), each with a zoom of the same frame.
- **B10:** frames 92–300 at real speed, then a labelled 0.5× replay of 92–200, then a labelled 0.25× replay of
  136–178.
- **B16:** frames 200–381 at real speed, then labelled 0.5×, 1/6 and 1/3 replays of the start, the pause and the
  rewind. A segment that runs out of source frames holds its last frame, labelled HELD FRAME.

No other retiming. Movie Maker is an offline deterministic render. It says nothing about the real-time frame rate or
the GPU price.

## Fixture strips (not made for this film)

Every strip frame and comparison sheet shown (B03, B06, B08, B13, B14, B15) is a committed **fixture** capture from
`captures/` (scenes in `godot/previews/`, fixed seed, captured by Tharun with Movie Maker). The comparison sheets were
assembled by Claude. The film shows them as labelled held frames and zooms. None is presented as gameplay.
