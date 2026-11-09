# TUNING — Assignment 6

Every revision records Claude's prediction, the strips before and after, Claude's comparison, and my verdict in the running game. Preview captures are **fixture** captures (`godot/previews/`), not the running game.

## 2026-11-08 — Effect A, first look (before Claude read any strip)

Fixture: `godot/previews/impact_preview.tscn` (commit `0e50fa0`), windowed at the project's 1280×720, watched with `-- --loop` (fixed seed) and `-- --loop --random`. Effect not yet wired into gameplay.

What I saw:
1. The brightest thing and its colour: the core flash, bright cyan.
2. The dark shards against the castle: a bit hard to make out individually because they're small (8×8 px) and charcoal against the light stone background.
3. Size: roughly the size of Bolt's fist, and smaller than his helmet.
4. Does it read as a hit landed? Yes, it reads as a sharp, snappy impact spark.
5. The one thing to change first: make the dark shards slightly larger or punchier in contrast so they stand out more clearly against the bright castle background.

## 2026-11-08 — Effect A, revision 1: Claude's reading of r0 and prediction (before any change)

Prompt: `prompts/prompt-4-tune.txt`, filled with Tharun's first look above. Strip `captures/impact_effect/r0/` (fixture, fixed seed, burst at frame 10, retrigger at 11, 30 fps). Zoomed sheet: `captures/impact_effect/r0_sheet.png` (frames 10, 12, 15 top; 20, 30, 50 bottom; 3× around the impact point). Pixel counts compare each frame with frame 20, which is the same background with nothing drawn.

| Frame | Brief (D.1, A.2) | r0 |
|---|---|---|
| 10 | Instant spawn | Matches: the burst is on screen in frame 10 itself. A cyan-white core about 45 px wide (window pixels) covers Bolt's fist. Shards: almost nothing; 155 pixels darker than the background, median luminance drop 18 of 255. They are under the ADD core. |
| 12 | Bright cyan core and dark debris | Core matches. Debris barely: 365 darker pixels, median drop 20, only at the core's lower-left edge. |
| 15 | Shards 8–14 px out, sagging, scale falling; burst 2 overlapping | Spread and sag match: the shards fill a 47 × 59 px area below and beside the fist. **But they are faint:** median drop 41, read as translucent pinkish bits against the pink castle. The colour ramp fades alpha linearly from 1 to 0, so at two-thirds of life about one-third of the alpha is left. This is what Tharun saw ("a bit hard to make out"). |
| 20, 30, 50 | Empty | Matches: pixel-identical to the empty background. |

Also seen: the shards' 1 px dark rim cannot be told from their interior at this size. The ramp's dark colour multiplies the whole texture, so every shard is dark all over.

**Proposed change (one setting): the Shards `color_ramp`** in `impact_effect.tscn`. Effect A's normal scene only; the blocked scene is untouched.

| | Points (offset: colour) |
|---|---|
| Old | 0.0: (0.25, 0.25, 0.28, 1.0) → 1.0: (0.1, 0.1, 0.1, 0.0) |
| New | 0.0: (0.25, 0.25, 0.28, 1.0) → **0.7: (0.25, 0.25, 0.28, 1.0)** → 1.0: (0.1, 0.1, 0.1, 0.0) |

Fully opaque charcoal for the first 70 % of each shard's life (0.175 s), then a fade to transparent over the last 30 % (0.075 s). Same colours, same lifetime.

**Prediction, frame by frame** (same seed, so the same shard paths):
- **10:** unchanged. Alpha starts at 1.0 in both ramps, and the core still covers the shards.
- **12:** almost unchanged. The shards at the core's edge go from about 0.73 alpha to 1.0, so they are slightly darker. Darker-pixel median drop rises from 20 to about 25–30.
- **15:** the visible difference. Both bursts are inside the opaque 70 % (burst 1 at 67 % of life, burst 2 at 53 %). The shards draw as solid dark flecks in the same positions as r0. Darker-pixel median drop rises from 41 to **90 or more**. The darker-pixel count stays about the same (≈ 950), since the shard paths and sizes do not change.
- **20, 30, 50:** still empty. The lifetime is unchanged and both bursts end by frame 18.

**Risk:** the fade is squeezed into the last 0.075 s (about 2 frames at 30 fps, 9 at 120 Hz). The shards may look like they blink out rather than fade. That is the in-game check.

The change waits for Tharun's approval. After it: the same edit in the config test's expected Shards ramp; the config test at 60; then Tharun recaptures r1.

## 2026-11-08 — Effect A, revision 1: change made, r1 captured, Claude's comparison

**Change (approved by Tharun):** Shards `color_ramp` in `godot/effects/impact_effect.tscn` gets a middle point, 0.7: (0.25, 0.25, 0.28, 1.0). The config test's expected ramp was updated to match: 136 checks, 0 failed at 60. The blocked scene is unchanged.

**r1:** captured by Tharun with the same fixture, seed and command as r0. `captures/impact_effect/r1/` holds frames 10, 12, 15, 20, 30 and 50. Side by side: `captures/impact_effect/r0_vs_r1_sheet.png` (top row r0, bottom row r1; frames 10, 12, 15, 20).

Prompt: `prompts/prompt-4-compare.txt`. The measurements are the same as for r0, each frame against its own run's empty frame 20.

| Frame | Prediction | r0 → r1 | Verdict |
|---|---|---|---|
| 10 | Unchanged | Darker pixels 155 → 161, median drop 17.6 → 18.0. A 25 × 24 px patch under the core differs. | **Almost.** Not pixel-identical, as I had said it would be. Likely explanation: the particles are already one frame (0.033 s, 13 % of life) old when frame 10 is captured, so in r0 their alpha had already dropped to about 0.87. In r1 it is 1.0. I had assumed age 0. |
| 12 | Slightly darker edges; median drop 20 → 25–30 | Darker pixels 365 → 420, median 19.6 → 21.4, max 100 → 136 | **Direction right, size wrong.** The edges are darker and there are more of them, but the median rose less than I predicted. Most darker pixels at frame 12 sit at the core's rim, where the ADD glow still lightens them. |
| 15 | Solid dark flecks in the same places; median drop 41 → 90 or more; count about the same (≈ 950) | Median 41.3 → **105.7**, max 119 → 215; darker pixels 965 → **1121** | **The median matches.** The flecks are solid charcoal in the same pattern, in a ring below and beside the fist. **The count does not match:** it rose by 16 %. Likely explanation: in r0, the faintest shard pixels darkened the background by less than the 12-level threshold and were not counted; opaque, they now are. A few of the lowest flecks still look lighter. This is a guess: they are the smallest (the scale curve falls toward 0.4), so filtering mixes in more background. |
| 20, 30, 50 | Empty | Pixel-identical to the empty background; frame 20 is identical in r0 and r1 | **Matches** |

**Not answered by the strip:** whether the shards blink out rather than fade (the risk named in the prediction). The fade now happens between frames 16 and 18, which the strip does not keep. That is for the in-game verdict.

## 2026-11-08 — Effect A, revision 1: my verdict in the running game (Tharun)

Windowed run, `godot --path godot`, 1280×720; landed jabs over the castle. The window closed with no errors.

- **Visibility:** shards were easier to make out against the bright castle as solid dark flecks. They also looked bigger on screen, even though the scale is unchanged.
- **The end:** they faded out smoothly, no snap or blink.
- **Verdict: Keep.**

## 2026-11-08 — Effect B, first look (before Claude read any strip)

Fixture: `godot/previews/steam_preview.tscn`, windowed at the project's 1280×720, watched with `-- --loop` (fixed seed; 11 cycles of 2.67 s: steam on for 1.33 s per cycle). The first loop I watched ran about 4× too fast (the loop counted display frames at about 120 fps); Claude fixed the loop to count real time before this look. The capture was not affected. The effect is not yet wired into gameplay.

What I saw:
1. What I see and its colour: fine white misty trails rising upward, reading bright and semi-translucent against the darker background.
2. Size compared with Bolt and his key: the entire steam rise is tall, roughly half of Bolt's height and noticeably larger than his key.
3. Steam or exhaustion? It reads clearly as rising steam or heat dissipation rather than heavy physical exhaustion.
4. What to change first: tweak the particle drift and fade timing so it feels more like heavy panting/exhaustion rather than steady, continuous chimney steam.

## 2026-11-08 — Effect B, revision 1: Claude's reading of the rewind strip r0 (before any change)

Observation driving it (Tharun, in game, TEST-REPORT A6-3): "the steam emission stopped abruptly and cut out immediately upon triggering the rewind state, rather than tapering off with a smooth fade." The D.2 strip never rewinds, so a rewind fixture was added (`godot/previews/steam_rewind_preview.tscn`, brief revision D.3). It uses Bolt's real `step()` and the game's own `steam_ratio()` mapping: wind 4 at frame 10 (ratio 0.84), rewind held from frame 30, then the ratio is 0.44 at frame 38, 0.04 at 46 and 0 at 53.

Strip `captures/wind_steam_rewind/r0/`, captured by Tharun with `--disable-vsync --always-on-top`. All 100 frames match Claude's clean trial capture. Zoomed sheet: `captures/wind_steam_rewind/r0_sheet.png` (top row 28, 31, 34, 38; bottom row 46, 53, 60, 72). Read by eye from the sheet.

| Frame | State | r0 |
|---|---|---|
| 28 | Wind 4, before rewind | A pale plume above the key, faint against the dark blue |
| 31 | Rewind just started | The key jumps to its rewind anchor (up and toward the body); the plume is full width |
| 34 | Key spin at its narrowest | **The whole plume collapses to a thin vertical sliver**, including puffs emitted before the rewind |
| 38 | Key full width; ratio 0.44 | Plume broad again |
| 46 | Ratio 0.04 | Plume thinner, still visible |
| 53 | Ratio 0 | Faint remnants |
| 60 | | Almost nothing |
| 72 | | Empty (key squashed) |

**Reading:** what looks like "cut out on rewind" is the plume being squashed with the key. While rewinding, `key_sprite.scale.x` swings between full width and 15 % about eight times a second (`fighter.gd:272-273`). The steam is its child in local coordinates, so every live puff narrows with it. The emission itself stops later and fades, as B-R2 intends: the ratio reaches 0 at frame 53, and puffs are still drawn until about frame 60.

## 2026-11-08 — Effect B, revision 1: the change (Tharun's choice) and Claude's prediction

**Choice (Tharun):** fix the squash in the wiring, not with a scene setting. The alternative, `local_coords = false`, would also have stopped the squash. But world-space particles most likely ignore the key's 1/3 scale (not verified in 4.7.2), which would make the puffs about 3× bigger and the rise and damping about 3× stronger. It would also stop the steam following Bolt as he walks.

**Change:** a new `godot/effects/steam_mount.gd` (`SteamMount`, a `Node2D` on the fighter). Every physics tick it copies the key's position, facing and visibility, and its `z_index`, but not the key's spin squash. `main.gd` and both steam fixtures mount the steam through `SteamMount.attach()` instead of under `key_sprite`. **No value in `wind_steam.tscn` changed.**

**Checks after the change:**
- The state test now finds the steam on the mount and adds three checks, at 60: **37 checks, 0 failed**:
  - while rewinding, the key squashed to |scale.x| 0.050;
  - the steam stayed at 0.333;
  - the steam stayed on the key, at 0.000 px offset.
- With the mount temporarily copying the key's squashed scale: 1 failed (`evidence/a6/mutations/steam-m6-mount-copies-squash.log`).
- All other tests are unchanged.
- **D.2 strip unchanged:** a fresh D.2 capture through the mount is pixel-identical to the committed `captures/wind_steam/r0` at frames 12, 20, 40, 55 and 70. With no rewind, the mount is exactly where the key's transform was.

**Prediction for the rewind strip r1** (same fixture, seed and frames; written after the code change, before any r1 frame was looked at):
- The simulation is unchanged: in local coordinates the key's squash only changed how the puffs were drawn, not where they are. So **every r1 frame equals r0 wherever the key was full width in r0**, and the plume is wider by exactly the key's squash factor wherever it was narrower.
- **28:** identical to r0 (before the rewind). Already confirmed in a trial capture.
- **31:** almost identical; the spin has only just begun, so the plume is at most slightly wider than r0's.
- **34:** the visible difference. r0's sliver becomes a full-width plume at the key's rewind position, while the key itself is still drawn narrow.
- **38, 46, 53, 60:** identical to r0 where the key is near full width in r0, otherwise wider. The fade still follows the ratio: 0.44 at 38, 0.04 at 46, 0 at 53, remnants at 60.
- **72:** identical to r0: no steam, and the key is still narrow (the key's own squash is unchanged; only the steam no longer follows it).

What r1 cannot show is how it reads at game speed: whether the plume now tapers off on rewind as Tharun expected. That is the in-game verdict.

## 2026-11-08 — Effect B, revision 1: r1 captured, Claude's comparison

**r1:** captured by Tharun with the same fixture, seed and flags as r0. It reported 100 frames, and every frame matches Claude's trial. Kept frames: 28, 31, 34, 38, 46, 53, 60, 72. Side by side: `captures/wind_steam_rewind/r0_vs_r1_sheet.png` (top row r0, bottom row r1, frames left to right).

Prompt: `prompts/prompt-4-compare.txt`. Pixels counted where r0 and r1 differ by more than 10 levels.

| Frame | Prediction | r0 → r1 | Verdict |
|---|---|---|---|
| 28 | Identical | 0 px differ | **Matches** |
| 31 | Almost identical, at most slightly wider | 0 px differ | **Matches, more exactly than predicted:** the key is at full width in this frame, so nothing to correct |
| 34 | r0's sliver becomes a full-width plume; the key itself still drawn narrow | 1021 px differ, all in a 41 × 46 px box above the key; by eye, a full, soft plume where r0 had a sliver; the key still narrow | **Matches** |
| 38, 46, 53, 60 | Identical where r0's key is full width, otherwise wider | 0 px differ in all four (the key is full width in each) | **Matches**; the fade follows the ratio as before |
| 72 | Identical; no steam; key narrow | 0 px differ | **Matches** |

**What explains the result:** with local coordinates, the squash only changed how the puffs were drawn, never their simulation. So r1 differs from r0 exactly in the squashed frames and nowhere else.

**What the strip under-shows:** only 1 of the 7 strip frames taken during the rewind (34) catches the key narrow; the others happen to fall where the spinning key is at or near full width. In the game at about 120 Hz, every squash is drawn, so the old flicker was far more visible than this strip suggests. That is consistent with Tharun's in-game "cut out".

## 2026-11-08 — Effect B, revision 1: my verdict in the running game (Tharun)

Windowed run, `godot --path godot`, 1280×720. I whiffed jabs to bring Bolt's wind low, then held S to rewind. The window closed with no errors.

- **Starting to rewind:** it kept going and tapered off smoothly instead of cutting out.
- **Anything wrong:** no, the steam stayed correctly anchored to the key without drifting away.
- **Verdict: Keep.**
