# TEST-REPORT — Tin Knockout asset slice

- **Source revision tested:** `64c037a` (game code frozen here for the film)
- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility, macOS 15.6 (Darwin 24.6.0), Apple M4
- **Date:** 2026-10-06

## 1. Startup and controls (fresh copy)

| Check | Result |
|---|---|
| Fresh clone from GitHub at `f155d18` → import → tests | ✅ 2026-10-06 ~20:15: `git clone` into an empty folder, `godot --headless --path godot --import`, then `test_slice.gd` **25/25** and `check_seam.py` **2/2**. All 22 fighter sprites (11 Bolt + 11 Rivet), 6 SFX, the music, the background and 5 props are present. *Re-run on the final submitted commit before the Canvas upload.* |
| Enter → "ROUND 1" → bell → FIGHT | ✅ automated: `fresh()` in every test; screenshot `evidence/screens/02-round-intro.png` |
| A/D move, J jab, K cutlass, L pop-gun, I block, S rewind, Esc pause, M/N mute, R rematch, F1 hitboxes | ✅ automated input path for move, jab, cutlass, pop, rewind and pause (section 7). Block, mute keys, F1 and rematch are exercised by `godot/tools/shots.gd` and the capture driver. |
| Every state reachable by input | ✅ `evidence/screens/` (some shots **posed**: fighters placed, then a real key press; see `godot/tools/shots.gd`) |

## 2. Character against the sheet

**Sheet vs. in-engine poses:** `design/character/pose-targets.png` (spec) vs. `design/character/generated-poses.png` (the shipped sprites at game scale with the hurtbox drawn on).

| Rule (CHARACTER-SHEET) | Result |
|---|---|
| 1. Helmet ≈ 40 % of height | ✅ All 11 poses come from inits drawn at the spec proportions. Strength 0.6 keeps that layout. Visually ~38–42 %. |
| 2. One window, two eyes | ✅ after an edit: SDXL-Turbo lost the eyes at strength 0.6, so they are **painted on every pose** (logged). |
| 3. Key on the back | ⚠️ **Changed.** The generated art has a black nozzle where the key should be, so the key is now a separate prop (`PROP-KEY`) attached at the back anchor and spun by code during rewind. |
| 4. Outline weight | ✅ consistent within the s43 set |
| 5. Brass helmet, red riveted tin suit | ✅ |
| 6. Mitten gloves, no fingers | ✅ |
| 7. Profile facing right; left = runtime flip | ✅ automated: `walking left flips Bolt's sprite`; screenshot `state-walk-left-flipped.png` |

**Collision:**
- `evidence/screens/03b-jab-hit-boxes.png` and `state-cutlass-boxes.png` show the F1 overlay: green = 50×106 hurtbox, red = active hitbox.
- **Bug found and fixed here:** `evidence/screens/before-fix/03b-jab-hit-boxes-sprite-offset-bug.png` shows the sprites drawn about 80 px up and left of their hurtboxes. `Sprite2D` was centred *and* offset by the feet anchor. Fixed with `sprite.centered = false` (commit `d9c248d`).
- **Art beyond the box:** the antennae (about 12 px above), the extended jab glove and the cutlass reach past the hurtbox, as the sheet says. The KO pose's hurtbox is irrelevant because no hit registers during KO.

**Silhouette re-test with generated art:**
- `design/character/silhouette-generated-in-game.png`: the helmet, antennae and boots read at 112 px.
- ⚠️ **Facing is weaker than in the v1 silhouette.** Because the key is now a separate sprite, the solid-black shape only shows facing through the small back nozzle and the helmet bulge. The key prop restores the cue in play.

## 3. Storyboard against the slice

| Panel | Slice equivalent | Match / difference |
|---|---|---|
| 01 Closing time (wide, high angle, design) | `01-title.png` | **Different.** The slice title is a dimmed overlay on the arena at eye level, not a high-angle shot of the counter. ENV-TITLE was a stretch goal and wasn't made. |
| 02 Round start (gameplay) | `02-round-intro.png`, `02b-fight-idle.png` | ✅ ROUND 1 → FIGHT!, bell, full bars and dials. **Difference:** the arena is inside the bowl on the counter seen from outside, not the bowl's interior (see ASSET-LOG ENV-BOWL v2). |
| 03 Jab lands (gameplay) | `03-jab-hit.png`, `03b-jab-hit-boxes.png` | ✅ jab pose, spark, Rivet hurt, Rivet's bar drops, Bolt's dial ticks down |
| 04 Rewind close-up (design, low angle) | `04-rewind.png` | Gameplay shows it at medium distance (the gameplay camera never zooms). The key-spin is visible as the key narrowing and widening. |
| 05 Spring runs dry (gameplay, Dutch roll) | `05-spring-empty.png`, `05b-knockdown-hurt.png` | ✅ EMPTY! label, slump pose, knockdown. The camera roll (5°) happens on a knockdown. |
| 06 Back off and rewind (gameplay) | capture `fight-4k` + `06b-popgun-cork.png` | ✅ |
| 07 Knockout (design, low angle) | `07-knockout-win.png`, `07b-knockout-lose.png` | ✅ K.O., winner text, R to rematch, music stops. Shot at eye level, not low angle. |

## 4. Sound events: exactly one sound per occurrence (automated, `godot/tests/test_slice.gd`)

| Event | Check | Result |
|---|---|---|
| SFX-JAB | 8 presses in range → 8 hits, 8 sounds | ✅ |
| SFX-JAB, held | J held 1.5 s → 1 attack, 1 sound | ✅ |
| SFX-CUTLASS | 5 swings → 5 hits, 5 sounds | ✅ |
| SFX-POP | L held 1 s → 1 cork, 1 sound | ✅ |
| SFX-REWIND | held 2.0 s from 40 wind → exactly 6 clicks (one per 10 wind); no clicks after full | ✅ |
| SFX-EMPTY | once on entering EMPTY, not repeated while stalled | ✅ |
| SFX-BELL | once at round start, once at KO, not repeated on the KO screen | ✅ |

**Captured real play:** `evidence/film/fight-inputs.jsonl`. A 24.4 s scripted round produced bell 2, jab 13, cutlass 3, pop 1, rewind 26, empty 1.

## 5. Music

| Check | Result |
|---|---|
| Seam (automated, `tools/edit/check_seam.py`) | ✅ seam sample jump 0.0057 < 99th percentile of normal steps 0.1176; level change +0.77 dB |
| Loop flag on, playing during fight | ✅ automated |
| Spring < 25 % → slows (pitch 0.85) | ✅ automated |
| Pause → low-pass + −10 dB; unpause restores it | ✅ automated (bus effect state) |
| KO → stops | ✅ automated |
| **Human: loop over repeated plays** | ✅ Tharun: "music alone is fine" (section 8). He did not report a click; he didn't count repetitions explicitly. |

## 6. Muted play

- ✅ automated: **sound never decides state.** The same scripted fight run muted and unmuted ends in the identical state `[62.5, 83.0, 30.7, 23.0, 191.69, 287.03, 2]` (hp, wind, x positions, round state).
- Visual cues that replace sound:
  - HUD spring dials (they turn red below 25 %)
  - EMPTY! / rewinding / FULL / block labels above the fighters
  - a distinct pose for every state
  - hit sparks, hitstop and screen shake
  - K.O. text
- ✅ human muted playtest: "the muted also works good" (section 8)

## 7. Automated checks

**Command:**
```bash
godot --headless --path godot --script res://tests/test_slice.gd
```

**Result at `64c037a`: 25 checks, 0 failed.**
- The first run had **8 failures**: `evidence/tests/run-01-setup-bug.txt`.
- **Cause, from a frame trace:** the test froze Rivet's brain 3 frames *after* the round started. In those frames Rivet fired a cork that interfered with every test.
- **Fixed in the test** (freeze before the round). I also added a gameplay change: a 1.5 s pop-gun cooldown at round start, because a cork on frame 1 felt cheap.
- No assertion or expected value was changed between the two runs.

**Seam check:** `python tools/edit/check_seam.py` → 2/2 PASS.

## 8. Human playtest (Tharun) — sound on, then muted

**Session 1, 2026-10-06 ~20:00, revision `64c037a`, sound on.** Tharun's own words, as given:

> "I have played the game but it is very simple the characters are so simple and music too when the music plays it's like full of metal sounds"

- **Characters "so simple":** this matches a known trade-off. The pose pass chose consistency (img2img strength 0.6, flatter look) over the richer paint of the reference (strength 0.75+ drifted between poses; FRICTIONAL, CHAR-* v3). Not fixed in this slice. Next step: a stronger model or a pose-conditioning method that keeps identity at higher detail.
- **Music "full of metal sounds":** asked to listen with effects muted (N), Tharun reported **"music alone is fine"**. So the metallic wall comes from the **sound-effect layer**, not the music: rewind clicks fire 4 per second while held (26 in the 24 s captured round), plus the tin clangs.
  - Warmer music candidates (MUS-WALTZ v2) had been started as a precaution; they were stopped unused.
  - **Not fixed** in this slice: the game source is frozen at `64c037a` for the film.
  - **Next step:** a quieter, lower-pitched rewind click (or one click per half-turn) and the SFX bus at about −6 dB under the music.
- **Muted session** (M + N): Tharun reported **"the muted also works good"**. The fight stayed readable without sound.
- **Overall:** "very simple". Recorded as a limitation (section 11).

## 9. Inspect → revise cycles (driven by observations)

| Observation | Evidence | Revision |
|---|---|---|
| Text-only prompts couldn't hold Bolt's identity (photoreal, porthole framing, colour bleed) | `design/rejected/CHAR-REF-v1…v4.jpg` | Switched to img2img from the spec sketch (v5–v7) |
| **F1 confirmed:** pose drift with plain sketch inits | `design/rejected/CHAR-JAB.jpg` | Inits copy the accepted reference's features; one seed for all poses (v2) |
| Sprite drawn off its hurtbox | `before-fix/…offset-bug.png` → `03b-jab-hit-boxes.png` | `sprite.centered = false` |
| SFX v1 trims started on noise; multi-hit clips | `evidence/sfx-scores.txt` → `sfx-scores-v2.txt` | Trim from the loudest transient |
| No generated EMPTY candidate falls in pitch | `sfx-scores-v2.txt` pitch_drop ≈ 1.0 | Pitch-fall edit, pitch_drop 1.18 |
| **Stun-lock:** EMPTY fired 6× in one dry-run round; a 0-wind fighter could be chain-stalled to KO | capture dry runs (FRICTIONAL) | HURT → IDLE always; 0-wind fighters can't walk; dry run → 1 EMPTY |
| **F4 partly refuted:** Rivet suit 2.35:1 vs real background (predicted 1.07:1) — but Bolt's yellow helmet vs the pink castle behind his start position is 1.02:1 luminance | `evidence/contrast-F4-recheck.txt` | **Not fixed.** Bolt stays readable by hue and the dark outline. Next step: move the start positions off the castle, or darken the castle |

## 10. Predicted failures (CHANGE-BRIEF section 4): outcomes

| # | Prediction | Outcome |
|---|---|---|
| F1 | Pose drift | **Confirmed**, then mitigated (ref-matched inits, one seed, painted eyes) |
| F2 | Hit sound fires twice | **Refuted** by test (the `has_hit` flag works) |
| F3 | Music loop clicks | **Refuted:** the automated seam check passes, and the human found the music alone fine |
| F4 | Rivet vanishes on the background | **Partly refuted** (2.35:1); a new low-contrast spot was found for Bolt |
| F5 | Rewind clicks every frame | **Refuted** by test |
| F6 | Unreadable muted | **Refuted:** state identical muted (automated), and the human muted session "works good" |
| F7 | Weapons don't sit in the hand | **Partly.** Cutlass and pop-gun attach at the computed hand anchor; the grip offsets were set by eye from one screenshot each, not measured per pose |

## 11. Honest limitations

1. **Sound effects and music were picked by Claude's signal analysis, not by listening,** because Tharun asked Claude to choose. The human listening check is section 8.
2. The background shows the bowl from outside; the concept said "inside the bowl".
3. Rivet is a deterministic pattern, not AI.
4. The eyes are hand-painted on every pose, and the win pose uses seed 42 rather than 43.
5. The 4K capture take differs from the 720p dry run, because `--fixed-fps 30` changes physics stepping. Both are genuine runs.
6. Low luminance contrast between Bolt's helmet and the pink castle (section 9).
7. **Playtester verdict: "very simple"** characters and game. The effects mix is dense with metal sounds (section 8).
8. Only one human playtester, and that is me, the developer.

---

# Assignment 3 — 3D props (castle, windkey, toybox)

*Blender 5.2.2 LTS · Godot 4.7.2.stable.official.ed1daf0bf · macOS 15.6 (Apple M4) · MCP for Blender package 2.1.9 / add-on 1.8 · 2026-10-15*

**Route per asset:** `castle` and `windkey` were built **through the Blender MCP**, in a separate Claude Code session driving my open Blender (code in `tools/blender/build_castle.py` and `build_windkey.py`). `toybox` was built by the **script route** (`tools/blender/build_toybox.py`, headless Blender). The first windkey was also script-route (`build_windkey_script_route.py`, kept for comparison); it was rebuilt through the MCP on 2026-10-16 and gave identical numbers. All three were exported by `tools/blender/export_glb.py` (glTF Binary, +Y Up on).

## A3-1. Interface notes
Six parts in BLENDER-NOTES.md, with my own screenshots `evidence/blender/01-mcp-connected-port-9876.webp` and `02-interface.webp`. The descriptions are Claude-drafted and labelled as such; the "What I noticed" lines are my observations.

## A3-2. Size: brief vs Blender vs Godot (metres, W × D × H; Godot reports X × Y × Z, so its Y is height)

| Asset | Brief | Blender (saved .blend, `dimensions`) | Godot AABB (headless) | Result |
|---|---|---|---|---|
| castle | 1.80 × 0.82 × 2.30 | 1.80 × 0.82 × 2.30 | 1.80 × 2.30 × 0.82 | match |
| windkey | 0.60 × 0.14 × 0.70 | 0.60 × 0.14 × 0.70 | 0.60 × 0.70 × 0.14 | match |
| toybox | 1.26 × 0.76 × 0.75 | 1.26 × 0.76 × 0.75 | 1.26 × 0.75 × 0.76 | match |

The Blender numbers were read by a headless script from the saved `.blend` files (`ob.dimensions`), not from the sidebar. **Still to do:** my own sidebar screenshot per asset.

## A3-3. Upright and scale
Godot check: every scene and mesh node has scale (1, 1, 1) and rotation 0, and the castle and key are tallest along Y. The castle's door surface and the toy box's latch surface sit at +Z (0.40 and 0.365), so the **front faces a +Z camera**. Prediction A3-F2 did not happen.

## A3-4. Origin
The AABB min Y is 0.0000 for all three, alone and in `prop_room.tscn` (world x ranges −3.10..−1.30, −0.30..0.30, 1.37..2.63). Each prop placed at y = 0 sits on the floor. The render `evidence/godot/prop_room.png` shows the bases on the floor, with shadows touching. Prediction A3-F3 did not happen.

## A3-5. Triangle count
castle 156 / 200 · windkey 192 / 250 · toybox 48 / 100. These were counted by the Blender script (n-gons fan-triangulated) and agree with the Godot check's surface index counts. **Still to do:** Blender's Scene Statistics screenshot.

## A3-6. Imports and appears
`godot --headless --path godot --import` gave no errors. The check `timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60` gives **RESULT: PASS (0 failing)**, exit 0. Full output: `evidence/check_props3d.txt`. The render `evidence/godot/prop_room.png` shows all three side by side: floor, one DirectionalLight3D, one camera.

**What the check does NOT show:** whether the props look right, read as what they are, or suit Tin Knockout's style or lighting. **Also:** Godot exited 0 even when the check script failed to parse, so a 0 exit code alone is not proof. Read the `RESULT:` line.

## A3-7. HUMAN CHECK: look
**My check (2026-10-16, after the hand edit):** I opened `prop_room.tscn` in the Godot editor, walked the camera around the three props, and ran the scene with F6. My verdict: **"everything works fine"**: they read as what they are, with no problems I noticed. I did not take a screenshot.

**Claude's renders, for evidence (not my screenshots):** `godot/tools/shot_prop_views.gd` rendered the scene from six angles into `evidence/godot/views/` (`contact_sheet.png`: front, behind, below, and a close-up of each prop). Claude's observations:
- Front: the door and latch face the camera; the green band shows.
- Behind: no holes; the back of the castle is plain (the door is front only).
- Below, through the one-sided floor: every base is closed; no missing faces.
- The **cream lid (`#E8DCC0`) reads as near-white** under this light. Next step: a darker cream, or less sun energy.
- The key is small beside the castle, which is correct for the brief's sizes.
- In the key close-up the castle looks tilted. That is wide-angle perspective at close range, not geometry; the castle close-up shows it upright.

The first run of this render script hit the same `Node not inside tree` mistake as the check (`look_at` before the room was in the tree), so its first view used the wrong camera. It was fixed (`look_at_from_position` after one frame) and re-rendered with no errors.

## A3-8. What Claude got wrong
**Claude's first Godot check passed when it should not have.** It called `global_transform` on nodes not yet inside the scene tree. Godot logged `Condition "!is_inside_tree()" is true. Returning: Transform3D()` and returned the identity, so "toybox sits on the floor in the room" was computed as if every prop stood at the origin, and printed PASS without testing placement. This is the same kind of error as the Module 3 floor check. **Fix:** compute transforms from local transforms up to the root (`to_root()`). The rerun reports real world positions (castle x −3.10..−1.30) and no engine errors. The second attempt also hit a GDScript parse error, and Godot still exited 0; see A3-6.

## A3-9. Inspect → revise
1. **Check revised from an observation** (A3-8): the engine ERROR lines showed the room check proved nothing. The transform maths was rewritten and the check rerun.
2. **Hand edit in Blender (mine):** I recoloured the toy box band from navy `#23395B` to green `#2E7D32`, in the Material tab → Base Color in Material Preview (`evidence/blender/04-toybox-before.webp`, `05-toybox-after.webp`). The Item tab still showed 1.26 × 0.76 × 0.75 m at scale 1.000. Re-exported; the Godot check reads albedo `#2E7D32` and still passes. The material slot is still *named* `toybox_navy`.

## A3-10. Predicted failures A3-F1 … F7: outcomes
| # | Outcome |
|---|---|
| F1 wrong size ×2/×10 | Did not happen. All three match within ±0.01 m in Blender and Godot. The castle code avoided the 2 m default cube by using `size=1.0` and scale, then applying. |
| F2 lying on side / backwards | Did not happen (A3-3). |
| F3 floats/sinks | Did not happen (A3-4). |
| F4 unapplied scale/rotation | Did not happen. Node scale (1,1,1), rotation 0. The key's lobes are rotated 90° per part and applied before joining. |
| F5 too detailed | Did not happen. Segment counts are as specified, and all three are under budget. |
| F6 colour lost | Not lost: Godot albedo hex values equal the Blender values (e.g. castle `#D98BA0`, `#3E8E86`, `#3A2A20`; band `#2E7D32` after my edit). But the cream lid *reads* near-white under the sun light (A3-7), so a colour can survive export and still not look right. |
| F7 MCP breaks | Partly. Setup needed three fixes (FRICTIONAL.md). The first `get_scene_info` returned `Could not connect to Blender`; it worked 4 minutes later. Then the MCP built the castle and, on 2026-10-16, the key (after the auto-mode safety check blocked a scene-clearing call and I approved it). The toy box stayed script-route. |
