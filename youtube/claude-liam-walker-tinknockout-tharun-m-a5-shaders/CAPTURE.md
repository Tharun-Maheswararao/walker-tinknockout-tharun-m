# CAPTURE.md — the one new engine capture in this film (B06)

| Field | Value |
|---|---|
| Game source | commit `2e6946d` (`git archive 2e6946d godot` into a scratch folder) |
| Engine | Godot `4.7.2.stable.official.ed1daf0bf`, Forward+ on Vulkan (MoltenVK), macOS 15.6 (Darwin 24.6.0), Apple M4 |
| Capture | `capture/rewind-4k.mp4` — 221 frames (0–220), 30 fps, 3840×2160, H.264 CRF 14 from the Movie Maker PNG sequence |
| Driver | `_tools/film_rewind.gd`, copied into the copy as `res://film_rewind.gd` (film tool, not part of the game) |
| Log | `evidence/runs/rewind-capture-log.txt` (Bolt's state and `rewind_amount` printed every frame) |

```bash
godot --path <copy>/godot --resolution 3840x2160 --write-movie <dir>/frame.png --fixed-fps 30 --script res://film_rewind.gd
```

Run **windowed**, never `--headless`, after `godot --headless --path <copy>/godot --import` on the copy.

**Isolation.** Captured from a scratch copy, identical to `2e6946d` except the window override in that copy's
`project.godot` (1280×720 → 3840×2160, as in the A3 film's orbit capture). Stretch mode is `canvas_items`, so the 2D
game renders natively at 3840×2160 (not an upscale). The repository was not touched.

**What the script does (SCRIPTED INPUT, labelled on screen).** It instantiates the unchanged `game/main.tscn`, taps
`confirm` through the real input path (`Input.parse_input_event`), waits through the intro, then holds `rewind`
(`Input.action_press`) for 45 frames (1.5 s), releases, waits 30 frames, holds again for 30 frames, releases and quits.
It never sets `rewind_amount`; the game's own `rewind_tint_driver.gd` does. Rivet is the game's own AI; it hit Bolt
during both rewinds (state REWIND → HURT), which shows the vulnerable window and R5 (fade out from the current value).

**Frame alignment.** The log's frame counter runs 2 ahead of the Movie Maker frame index: the tint in movie frames
86–91 matches the logged values at log frames 88–93 (0.2222 … 1.0), measured from Bolt's pixels. B06's readout uses
log frame = movie frame + 2.

**How the film uses it.** B06: frames 0–220 at real speed (7.37 s), then a labelled real-speed replay of frames 72–220,
then a labelled 0.25× replay of frames 84–113 (each frame shown 4×). No other retiming. Movie Maker is an offline
deterministic render, not evidence of real-time frame rate.
