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

The Blender numbers were read by a headless script from the saved `.blend` files (`ob.dimensions`), and for castle and windkey also by the MCP's `get_scene_info` in my live session. **Sidebar screenshots:** only the toy box has one (`evidence/blender/05-toybox-after.webp`, Item tab: 1.26 × 0.76 × 0.75 m, scale 1.000). The key also has one: `evidence/blender/06-windkey-sidebar.webp`, my own screenshot. It shows the Item tab at 0.6 × 0.14 × 0.7 m, Scale 1.000, and Statistics *Triangles 192 / 192*. The castle has one too: `evidence/blender/07-castle-sidebar.webp`, my own screenshot. It shows the Item tab at 1.8 × 0.82 × 2.3 m, rotation 0°, Scale 1.000. The Statistics overlay was off in that shot, so the castle's 156 tris come from the script and the MCP `get_scene_info`, not Blender's overlay. The MCP `look` views are in `evidence/blender/03-castle-mcp-look.png`.

## A3-3. Upright and scale
Godot check: every scene and mesh node has scale (1, 1, 1) and rotation 0, and the castle and key are tallest along Y. The castle's door surface and the toy box's latch surface sit at +Z (0.40 and 0.365), so the **front faces a +Z camera**. Prediction A3-F2 did not happen.

## A3-4. Origin
The AABB min Y is 0.0000 for all three, alone and in `prop_room.tscn` (world x ranges −3.10..−1.30, −0.30..0.30, 1.37..2.63). Each prop placed at y = 0 sits on the floor. The render `evidence/godot/prop_room.png` shows the bases on the floor, with shadows touching. Prediction A3-F3 did not happen.

## A3-5. Triangle count
castle 156 / 200 · windkey 192 / 250 · toybox 48 / 100. These were counted by the Blender script (n-gons fan-triangulated) and agree with the Godot check's surface index counts and the MCP's `get_scene_info` tri counts. Blender's Statistics overlay shows *Triangles 192 / 192* for the key in my screenshot `06-windkey-sidebar.webp`.

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
2. **Hand edit in Blender (mine):** I recoloured the toy box band from navy `#23395B` to green `#2E7D32`, in the Material tab → Base Color in Material Preview (`evidence/blender/04-toybox-before.webp`, `05-toybox-after.webp`). The Item tab still showed 1.26 × 0.76 × 0.75 m at scale 1.000. Re-exported; the Godot check reads albedo `#2E7D32` and still passes. The material slot is still *named* `toybox_navy`. **What it taught me (my words):** "Editing the hand taught me that Blender’s interface relies on coordinating specific Properties tabs, color pickers, and viewport shading modes just to see surface changes take effect in real time."

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

---

# Assignment 5 — shaders, materials and the Godot shading language

*Drafted by Claude from the committed logs and captures. Every row says who checked it. Rows marked **Tharun's check** are human checks: Tharun's own words, which Claude does not write.*

- **Source revision:** the game source is as of `2e6946d` (the F9 capture key). Later commits add only evidence and docs; the final `a5` SHA goes in SUBMISSION.md.
- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf.
- **Renderer:** Forward+ on Vulkan (MoltenVK) (`godot/project.godot:15, 31`).
- **Machine:** macOS 15.6, Apple M4.
- **Tests:** all run through `scripts/run-test.sh`, the handout's exact wrapper (`23a0363`).

## A5-1. Baseline (before and after)

| Suite | Before A5 (`23a0363`, 60 fps) | After A5 (60 fps) |
|---|---|---|
| `test_slice.gd` | 25 checks, 0 failed | 25 checks, 0 failed |
| `check_props3d.gd` | 23 PASS, RESULT PASS | RESULT PASS (0 failing). It now prints `albedo=#000000` for `toybox_fresh` (finding M9). |

## A5-2. Shaders parse

| Shader | Author | Evidence |
|---|---|---|
| `rewind_tint.gdshader` | Tharun (colour line suggested by Claude, recorded) | `6ffb7ce`. Import with no SHADER ERROR; uniform list `rewind_amount` (3), `tint_color` (20), `tint_strength` (3); asserted by `test_rewind_tint.gd`. |
| `painted_tin.gdshader` | Tharun (structure and skeleton suggested by Claude, recorded) | `72c4bc1`. Spatial; 3 samplers and 5 uniforms in groups paint and metal; asserted by `test_materials.gd`. |
| `hint_experiment.gdshader` | Tharun | `fab8a41`. Spatial, unshaded; 2 samplers and 1 bool; asserted by `test_materials.gd`. |
| `standard_generated.gdshader` | Godot editor (converted by Tharun) | `c65be67`. Imports with no SHADER ERROR. |

**Mutations** (Tharun edited, Claude ran the test; `evidence/a5/mutations/`):

| Mutation | Test | Result |
|---|---|---|
| m1: semicolon deleted (`rewind_tint` line 3) | `test_rewind_tint.gd 60` | SHADER ERROR "Expected a ';'"; uniform list `[]`; 5 of 50 failed; **exit 1** |
| m2: `rewind_amount` → `rewind_amt` in the shader only (lines 3 and 8) | `test_rewind_tint.gd 60` | No SHADER ERROR; 2 of 50 failed (uniform type and source checks); **exit 2** (the exit code is the failure count, as in `test_slice.gd`; non-zero = fail) |
| m2, first attempt (line 8 only) | same | A parse failure ("Unknown identifier 'rewind_amt'"), not the intended rename. Kept as an attempt. |
| m3: `source_color` deleted from `metal_albedo` (`painted_tin` line 3) | `test_materials.gd 60` | No SHADER ERROR; 1 of 55 failed ("colour sampler metal_albedo has source_color"); **exit 1** |

**What the mutations showed:** in m1 and m2, 45 and 48 driver checks still passed. A material readback proves nothing about the shader; only the uniform-list and source-text assertions catch these.

## A5-3. Driver: sampled every frame at 30, 60 and 144 fps through real input

`test_rewind_tint.gd` (agent, `3196f5c`; two test bugs fixed by Claude in `7115992`) gives **50 checks, 0 failed** at each of 30, 60 and 144.
- **Input:** rewind is held with `Input.action_press`, and pause is a parsed input event.
- **Rivet:** acts only through `brain.think`.
- **Sampling:** at `process_priority` 1000.

| Rule | 30 fps | 60 fps | 144 fps | Tolerance |
|---|---|---|---|---|
| R2 fade-in 0→1 (0.15 s) | 0.1667 s | pass | 0.1528 s | ± one frame |
| R2 fade-out 1→0 (0.30 s) | 0.3000 s | pass | 0.3056 s | ± one frame |
| R3 retrigger, extend (from v, (1−v)×0.15 s) | 0.1333 s vs 0.1000 (at the edge of one 1/30 s frame) | pass | 0.0833 s vs 0.0833 | ± one frame |
| R5 release mid fade-in (v×0.30 s) | 0.2667 vs 0.2667 | pass | 0.1736 vs 0.1667 | ± one frame |
| R5 hit mid fade-in (REWIND → HURT) | 0.2667 vs 0.2667 | pass | 0.2014 vs 0.1944 | ± one frame |
| R4a `time_scale` 0.5 (game time 0.15 s, real time 0.30 s) | 9 frames = 0.300 s | 18 frames | 44 frames = 0.306 s | ± one frame |
| R4b tree pause / R4c game pause: value held, resumes from the same value | pass | pass | pass | exact |
| R6 Rivet's value stays 0 while Bolt rewinds, and the reverse | pass | pass | pass | exact |
| Fade start delay after the press (reported, not asserted) | 0.067 s | 0.033 s | 0.021 s | — |

**Why the start delay exists:** REWIND changes on the 60 Hz physics tick (`evidence/a5/headless-facts.txt:12, 23`), so at 144 fps the fade starts up to 1/60 s after the key press. R2 times the fade itself.

## A5-4. Controlled values: HUMAN CHECK

**Evidence (Claude).** Scripted-input windowed run (`tools/a5_capture_run.gd`: confirm, hold rewind, F9):
- in-engine captures `evidence/a5/captures/bolt_rewind_amount_*.png` (1280×720 = 2× game space);
- pixel samples in `evidence/a5/captures/pixel-samples.txt`.

| `rewind_amount` | A (chest): predicted → captured | B (helmet): predicted → captured |
|---|---|---|
| 0.0 | (217, 87, 64) → (217, 87, 64) | (251, 188, 34) → (251, 188, 34) |
| 0.5 | (185, 105, 112) → (185, 105, 112) | (211, 181, 89) → (211, 181, 89) |
| 1.0 | (154, 124, 160) → (153, 123, 159) | (171, 174, 145) → (171, 174, 144) |
| 2.0 (set from code) | → (90, 160, 255) | → (90, 160, 255) |

**Differences:** at 1.0 the only differences are −1, in exactly the five channels whose predicted value was x.5 before rounding (CHANGE-BRIEF A5.3 note).

**`hint_range`:** at 2.0 both pixels are the pure tint, so the shader received 2.0 × 0.5 = 1.0. **`hint_range(0.0, 1.0)` does not clamp a value set from code.** That matches the prediction in A5.7 Q7. A material readback alone could not show this (`headless-facts.txt:9`).

**OS screenshot vs capture** (`evidence/a5/captures/os-screenshot/comparison.txt`):
- The OS screenshot is full-screen Retina (4.725×) and tagged with the "Display" ICC profile.
- Averaged static-background patches differ from the capture by up to (−8, +2, −1), shifted most in red.
- So the capture is the one trusted for predictions.

**Tharun's check (in Tharun's words):** The predictions match the actual pixel values closely. The small off-by-1 difference at rewind_amount = 1.0 is caused by floating-point rounding when mixing color channels. I trust programmatic image capture over OS screenshots because OS grabs include display color profiles, OS compositing, and potential downscaling, whereas direct buffer captures give the exact raw pixel data.

## A5-5. In play: HUMAN CHECK

**Evidence:** OS screenshot during play (`os_screenshot_rewinding.png`) shows Bolt and Rivet both rewinding and both tinted blue.
**Tharun's playtest (2026-11-01, windowed run, `godot --path godot`), in Tharun's words:**
- **Scope:** About 6 minutes, 4 rounds, rewound about 20 times including taps, quick holds, and getting hit.
- **Visual read:** The blue tint reads clearly as an "open, punish now" window on both Bolt and Rivet, making the rewind state immediately distinct during combat.
- **Fade timing:** The fade feels well-tuned and responsive, snapping on quickly to register the action, then easing off at a slower, more readable pace.
- **Exclusions:** The key and weapon correctly remain entirely untinted, keeping props distinct from the character color shifts.
- **Pause check (R4c):** The playtest run paused with P. *(Whether the tint visibly froze is not stated; R4c's hold is covered by the headless test, A5-3.)*
- **Gameplay side-effects:** No unintended changes occurred; movement speed, hit detection, and game timing remained completely consistent throughout long holds, quick taps, hits, and pauses (P).

## A5-6. Hint experiment: HUMAN CHECK

**Evidence (Claude):** `evidence/a5/captures/hint_quads.png` (windowed, Forward+). Band centres sampled in `hint-samples.txt`.

| Band (file) | Quad S (`source_color`): predicted → measured | Quad D (data): predicted → measured |
|---|---|---|
| 64 | 64 → 64 | 137 → 137 |
| 128 | 128 → 128 | 188 → 188 |
| 192 | 192 → 192 | 225 → 225 |

**Tharun's check (in Tharun's words):** The top quad (Quad_S) keeps the values 64, 128, and 192 completely unchanged because the sRGB texture decode and the output screen encode cancel each other out. The bottom quad (Quad_D) appears lighter because the raw data is treated as linear values and encoded once on output, brightening the midtones.

## A5-7. Interface sweep: HUMAN CHECK

**Evidence (Claude):** `evidence/a5/captures/toybox/sweep_contact_sheet.png`.
- Each `painted_tin` uniform is set at runtime on the fresh material only, to its minimum, the shader default and its maximum; nothing is saved.
- The worn box stays unchanged in every row.
- Lighting: the prop room as A3 left it (Sun energy 1.0 with shadows, ambient 0.6, Linear tonemap; SSAO, SSIL, SDFGI, glow and fog off).

**Tharun's check (in Tharun's words; revised after comparing the first draft with the contact sheet):**
- `paint_color`: Sweeps from black (min) to bright red (default) to pure white (max), changing overall brightness and tint rather than shifting through a range of red hues.
- `paint_roughness`: No noticeable visual difference between min, default, and max at this camera distance (connecting to finding M5, as the lack of metallic variation makes roughness changes subtle).
- `wear_amount`: Cleanly reveals the underlying metal through the worn paint mask, with max showing the entire box covered in dark bare metal.
- `normal_depth`: Controls the intensity of the surface dents; max increases the depth and contrast of the indentations cleanly without causing normal stretching on UV seams.
- `uv_scale`: At min (0.5), the texture pattern creates large, smeared dents that break the realistic scale; at max (8.0), the pattern becomes very fine and almost disappears into a smooth surface.

## A5-8. One shader, two materials: HUMAN CHECK

**Evidence (Claude, measured)** from `evidence/a5/captures/toybox/edit_checks/README.txt`:
- **Side by side:** `toyboxes_side_by_side.png`.
- **Shader edit** (Tharun: `uv_scale` default 2.5 → 6.0): both boxes changed (fresh 88 px, worn 1622 px; castle 0).
- **Material edit** (Tharun: worn `wear_amount` 0.55 → 0.2): only the worn box changed (6698 px; the fresh box unchanged except the worn box's edge at x 885–888).
- Both edits were restored.

**Tharun's check (in Tharun's words):** Editing the parameter directly in the .gdshader file updated both toy boxes simultaneously because they share the same shader definition, whereas editing a value in a specific .tres material file only updated that individual toy box instance, confirming parameter inheritance and instance separation work correctly.

## A5-9. Material wiring and texture data

- `test_materials.gd 60`: **55 checks, 0 failed**. After deleting `godot/.godot` and reimporting, still **55/55** (`97be9e1`, `logs/test_materials_60fps_fresh_cache.log`).
- m3 (`source_color` removed) makes it exit 1 (A5-2).
- **Curl ratio** (stride 4; calibration `logs/calibrate_normal_map_60fps.log`):
  - `nor_gl` (bound): GL 0.0658, DX 1.9342;
  - `nor_dx`: GL 1.9342, DX 0.0658.
  - The sign convention is not reversed; the threshold is < 0.5.
- **Import settings:** the editor rewrote no `.import` file. `git status` after Tharun's first editor session (the StandardMaterial3D conversion) showed only the new shader. The fresh-cache reimport rewrote nothing either.
- **Audit:** `godot/MATERIALS.md` (agent `cc28ecd`; Tharun's review and correction `b5f35c2`).

## A5-10. Agent mistakes caught

| Mistake | Who caught it, and how |
|---|---|
| The CLAUDE.md draft cited `README.md:8` for the engine. That README line says Forward+ applies "from Assignment 6 on", which is stale. It also left the engine version unconfirmed. | Claude's reference check; Tharun's review (`e5d77af`). |
| The driver test read `--fixed-fps` from `OS.get_cmdline_args()`, which the engine consumes, so the period was always 1/60. | The 30 and 144 fps runs failed. Fixed in `7115992`. |
| The test's R4c lookup returned −1 at 30 fps, and `samples[-1]` silently read the last sample. | The 30 fps failure; fixed in `7115992` (now asserts that the sample was found). |
| Claude's first fix for the period used `root.get_process_delta_time()` too early (it read 1/24 at 30 fps). | A rerun still failed; fixed in the same commit. |
| MATERIALS.md cited `prop_room.tscn:30-32` for the Sun's energy, but that is the engine default and is not in the file. | Tharun's review (`b5f35c2`); Claude spotted it while recording the review. |
| The headless ResourceSaver wrote `= null` for unset uniforms. | Claude's inspection of the `.tres` (`ceaece8`, finding M4). |

## A5-11. Inspect → revise cycles

1. The test failed at 30 and 144 fps. Inspecting the log showed "(60 fps)" printed at every rate, so the bug was in the test, not the driver. The period was then measured from the delta: the first attempt was wrong, the second right (`7115992`).
2. The second mutation's first attempt failed for the wrong reason, a parse error instead of a rename. Inspecting the SHADER ERROR line ("Unknown identifier") showed line 3 was unchanged. Tharun renamed both lines, and it then failed the uniform-list check as intended.

## A5-12. Predicted failures (CHANGE-BRIEF A5.6): outcomes

| # | Outcome |
|---|---|
| A5-F1: Bolt and Rivet sharing one material | Did not happen. R6 assertions pass at all three rates: separate material objects, and Rivet stays 0 while Bolt rewinds and the reverse. The OS screenshot shows both tinted independently. |
| A5-F2: the duration depends on frame rate | Did not happen. The driver uses `delta`; durations are within one frame at 30, 60 and 144. |
| A5-F3: retrigger restarts from 0 | Did not happen. R3 "no frame-to-frame drop" passes at all three rates. |

## A5-13. What no headless run shows

Nothing headless says how anything looks (`evidence/a5/headless-facts.txt:3`). The look checks are A5-4 to A5-8, from windowed captures and Tharun's own eyes.

## A5-14. Limitations

- `claude -p` hit the account's spend limit mid-session (until 2026-12-01). The audit, test fixes and captures therefore ran in the interactive desktop session; see SOURCES.md.
- The captures are scripted-input runs, labelled as such. Tharun's playtest is the unscripted check.
- `painted_tin` writes no `METALLIC` (M5), so the worn bare metal is shaded as a non-metal.
- A dummy-renderer teardown ERROR appears in headless logs that free a ShaderMaterial mesh (M1). It prints after the result line, and the wrapper ignores it.
- The A5 film was built by a Claude film session; Tharun watched it before uploading. File `claude-liam-walker-tinknockout-tharun-m-a5-shaders.mp4`, SHA-256 `6568f966a28b65ffad73d3aac36430b4f222d5f065af60dfd930946d141b2ed8` (SUBMISSION.md).

---

# Assignment 6 — particle effects

*Sections drafted by Claude from the logs named in each row; Tharun's own observations are marked "(Tharun)".*

**Environment for every A6 result:** Godot 4.7.2.stable.official.ed1daf0bf; Forward+ on Vulkan 1.2.334 (MoltenVK); GPU Apple M4; macOS 15.6. Window 1280×720, viewport 640×360. Source revisions: each section names its commit; the Use It table below names the revision it was checked at.

## A6-1. Config test: mutations (Step 2)

`godot/tests/test_impact_effect_config.gd` reads every setting the brief names (A.3a–A.3c) back from the loaded scenes. Unmutated: `135 checks, 0 failed`, exit 0 (`logs/test_impact_effect_config_60fps.log`, rerun after each restore). Each mutation was made by hand in `godot/effects/impact_effect.tscn`, run once, then undone with `git checkout`.

| # | Mutation | Test result | Log |
|---|---|---|---|
| M1 | Godot 3 name: Shards line 25 `initial_velocity_min = 60.0` → `initial_velocity = 60.0` | `FAIL  Shards initial_velocity 60 / 90 (got 0.0 / 90.0)`; `135 checks, 1 failed`; exit 1 | `evidence/a6/mutations/m1-godot3-name.log` |
| M2 | Value drift: Shards line 81 `amount = 16` → `amount = 12`, brief unchanged | `FAIL  Shards amount 16 (got 12)`; `135 checks, 1 failed`; exit 1 | `evidence/a6/mutations/m2-value-drift.log` |

**M1, what else showed it: nothing.** Godot loaded the scene without a warning; the M1 log has no line containing "warn", "error", "unknown" or "invalid". The unknown float line was dropped and `initial_velocity_min` stayed at its default 0.0, as probed earlier (`design/a6/BRIEF-FACTS.md` §5). This is CHANGE-BRIEF prediction F4, confirmed: the read-back is the only check that caught it.

**M1, does the effect still fire?** Yes. With the mutated file, the windowed preview (`impact_preview.tscn -- --loop`, real time, about 120 fps) fired and finished both bursts on every one of 16 loops ("burst 1 fired at frame 10 … finished at frame 31–48"), with no error printed.

**M1, how it looked (Tharun):** Watching the run with min speed dropped to zero, I saw most shards still fly outward near their usual distance, but a noticeable cluster fell short and pooled closer to the center origin.
_(From the single M1 preview run above, written down after the restore and after Claude had stated the expected result: speed random in 0–90 instead of 60–90, so about half the shards keep roughly their normal reach.)_

**M2:** a wrong number in the scene is caught even though it is a valid Godot 4 name; the test's expected values are the brief's, so the test catches drift between brief and scene.

## A6-2. Effect A wired: state test (Step 3)

Plan: `evidence/a6/step3a-plan.md`, approved step by step. Wiring: `godot/game/main.gd` passes `blocked` to `_on_impact`, which keeps the star, shake and roll and calls `_spawn_impact`: a fresh instance of the normal or blocked scene per impact, a child of Main at `p`, `restart()` after `add_child`, freed when both emitters emit `finished`.

`godot/tests/test_impact_effect_state.gd`, through the wrapper at a fixed 60 fps (it does not wait on audio): **44 checks, 0 failed**, exit 0 (`logs/test_impact_effect_state_60fps.log`). Bolt is driven through the real Input path; Rivet's block and pop come from a stand-in brain that sets his `intent` (SETUP, like test_slice's `FrozenBrain`), because the game has no keys for Rivet. The test never calls the spawn code; bursts are counted as they enter Main's tree.

| Scenario | Result | Rule |
|---|---|---|
| Scene load, round to FIGHT | 0 bursts | A-R1 |
| 6 landed jabs | 6 `impact_effect.tscn` bursts, each at the attack-box centre (339, 227), under Main | A-R1, A-R2, A-R4, A-R5 |
| Whiffed jabs and cutlass, walking, rewinding | 0 bursts | A-R1 |
| Bolt's cork hits Rivet | 1 burst at the cork's position; the cork frees itself; the burst is still under Main afterwards and frees itself 15 frames later | A-R2, A-R4 |
| Bolt's and Rivet's corks land 5 frames apart | 2 distinct bursts alive at once, each at its own cork's position | A-R3 |
| Rivet blocks a jab | `impact_effect_blocked.tscn` at the attack-box centre | A-R5 |
| Pause (real event) right after a hit | the burst still processes and frees itself while paused (13 frames) | A-R7 |
| End of every scenario | live bursts back to 0 | F2 |

All existing tests unchanged after the wiring: `test_slice` 60 25/0; `check_props3d` 60 PASS; `test_rewind_tint` 30/60/144 50/0 each; `test_materials` 60 55/0; `test_impact_effect_config` 60 135/0. `git diff scripts/run-test.sh godot/shaders` empty.

**Does the state test catch failures?** (logs in `evidence/a6/mutations/`)

| Run | What changed | Result |
|---|---|---|
| First run | none; a bug in the test: it compared two bursts after both were freed, and freed objects cannot be told apart | `44 checks, 1 failed` (`state-run1-test-bug.log`); fixed by recording each burst's instance id at spawn |
| M3 | main.gd temporarily set `emitting = true` before `add_child` instead of `restart()` after it | `44 checks, 0 failed` (`state-m3-emitting-before-tree.log`): **not caught, because the predicted failure did not happen**: `finished` still fired and every burst freed itself |
| M4 | main.gd temporarily never freed the burst | `44 checks, 5 failed`: the four F2 checks and the A-R7 free check (`state-m4-no-queue-free.log`) |

main.gd was restored byte for byte after M3 and M4.

**F2, outcome:** the brief predicts that a burst started with `emitting = true` before its first frame never emits `finished` (from Claude's earlier probe). In main.gd's setup, headless, that did not reproduce (M3). The leak itself is caught when it happens (M4). The brief's A.4 note and the CLAUDE.md line state the probe more broadly than this result supports.

**What the state test cannot show:** how the burst looks, its draw order on screen beyond the `z_index` value, and its contrast against the castle; a headless run draws nothing.

### HUMAN CHECK: in the running game (Tharun, 2026-11-08)

Windowed run, `godot --path godot`, 1280×720; closed with no `ERROR` or `SCRIPT ERROR` in the terminal.

| Check | What I saw |
|---|---|
| Landed jab | The bright cyan core flash and dark charcoal shards burst right over the yellow star, and they were distinct enough to tell apart from the background flash. |
| Blocked hit | Didn't catch Rivet in a block state during this run, so I didn't see the blocked variant. |
| Cork hit | Didn't see a cork actually connect with Rivet, so I can't confirm the world-space anchor by eye. |
| Pause | Didn't pause at the exact frame of impact, so I didn't verify the unpaused continuation visually. |

**Second run, same day** (`godot --path …/godot`, windowed; closed with no `ERROR` or `SCRIPT ERROR`), aimed at the three checks missed above:

| Check | What I saw |
|---|---|
| Cork hit | Yes, a cork connected squarely against the target. Because of the world-space anchoring (local_coords = false), the impact burst appeared right at the precise point of contact and stayed cleanly pinned in space, holding its position even after the cork projectile itself vanished. |
| Blocked jab | Rivet successfully threw up his guard for a block. That hit looked distinct—instantly reading as a scaled-down, muted grey spark rather than the bright cyan and charcoal flash of a normal, unblocked hit, providing immediate visual feedback of the deflection. |
| Pause right after a hit | Pressing pause right on the frame of impact felt smooth and deliberate. While the rest of the game paused instantly, the impact effect didn't freeze mid-air; it continued its animation sequence naturally and finished its lifecycle cleanly. |

## A6-3. Effect B built and wired: config and state tests (Step 5)

Build (`d3f20d6`): `godot/tools/generate_steam_texture.gd` writes `steam_32.png`; `godot/effects/wind_steam.tscn` holds one emitter with the B.3 values, dormant (`amount_ratio` 0, `emitting` true). `godot/tests/test_wind_steam_config.gd` at 60: **33 checks, 0 failed**, including `amount_ratio`, continuous emission, `local_coords` and the unclamped scale point 3.0 (F1).

Wiring (plan `evidence/a6/step3b-plan.md`, approved step by step): `godot/game/main.gd` adds one steam instance under each fighter's `key_sprite` and connects `wind_changed` to `amount_ratio = steam_ratio(wind)` = clamp((25 − wind) / 25, 0, 1). Nothing else is set from code.

`godot/tests/test_wind_steam_state.gd`, through the wrapper at a fixed 60 fps: **34 checks, 0 failed**, exit 0 (`logs/test_wind_steam_state_60fps.log`). Bolt's wind moves only through real jabs and real rewinding; Rivet is frozen by a stand-in brain (SETUP).

| Real input | Wind | Result | Rule |
|---|---|---|---|
| Load, round start | 100 | both ratios 0, `emitting` on, `amount` 25 | B-R6 |
| 6 jabs | 28 | ratio 0 | B-R1 |
| 7th jab | 16 | ratio 0.36, `amount` 25 | B-R1, B-R3 |
| 8th jab | 4 | ratio 0.84, `amount` 25; Rivet's ratio still 0 | B-R3, one per fighter |
| Pause, then keys pressed | 4 | wind, ratio, `emitting`, `speed_scale` unchanged; the steam still processes | B-R4 |
| Rewind, 2 clicks | 24 | ratio 0.04: `amount × amount_ratio` = 1.00 | F5 |
| Rewind, 1 more click | 34 | ratio 0, `emitting` still true | B-R2 |
| Jab at Rivet on 5 hp | | Rivet KO; his key and steam hidden; Bolt's visible | B-R5 |
| Rematch event | 100 | both ratios 0; no extra steam nodes | B-R6 |

**Does it catch failures?** M5: main.gd temporarily set `amount` instead of `amount_ratio` → **34 checks, 11 failed** (`evidence/a6/mutations/steam-m5-sets-amount.log`). main.gd was restored byte for byte.

All tests after the wiring, through the wrapper: both Effect B tests and both Effect A tests at 60 (34/0, 33/0, 44/0, 136/0); `test_slice` 60 25/0; `check_props3d` 60 PASS; `test_rewind_tint` 30/60/144 50/0 each; `test_materials` 60 55/0. No SCRIPT or SHADER ERROR; `git diff scripts/run-test.sh godot/shaders godot/fighter` empty.

**What the state test cannot show:** how the steam looks and whether it fades smoothly when the ratio drops (B-R2's look); whether a hidden emitter keeps simulating and what shows when the key reappears (B-R5); that it draws behind the body and squashes while rewinding; and the frame on which the first puff becomes visible (F5's eyes half).

### HUMAN CHECK: in the running game (Tharun, 2026-11-08)

Two windowed runs, `godot --path godot`, 1280×720; both closed with no `ERROR` or `SCRIPT ERROR`. (Claude's first key list said R for rewind; rewind is S. The second run used S.)

| Check | What I saw |
|---|---|
| Low wind (7–8 whiffed jabs) | Yes, steam vented directly from Bolt's back key as his wind depleted. It rendered as a semi-translucent, rising white plume puffing upward from the key housing. |
| Rewind (hold S) | The steam emission stopped abruptly and cut out immediately upon triggering the rewind state, rather than tapering off with a smooth fade. |
| Rivet | No steam appeared on Rivet when his wind dropped. |

**Claude's notes on the last two rows** (facts from the code and a probe, not observations):
- *Rivet.* The wiring gives Rivet his own steam (the state test finds it under his key). Tharun's answer also said the effect "is anchored specifically to Bolt's key mechanism"; that explanation is not what the code does, so it is left out of the row above. A headless probe of the real game with Rivet's real brain for 30 s (`evidence/a6/probes/probe_rivet_steam.gd`, output `probe_rivet_steam.txt`): Rivet's steam was on for 7.0 s and visible the whole time, but his wind never went below 17.7, so the ratio peaked at 0.29 and was usually 0.01–0.04, at most 1 puff at a time. Rivet's brain backs off and rewinds as soon as his wind falls below 25 (`rivet_brain.gd:26-27`), the same threshold where the steam starts. Seeing almost no steam on him is consistent with that. This affects B.1's stated purpose (reading Rivet's wind).
- *Rewind.* Pressing S does not change the ratio at once: from wind 4 the first click comes after 0.25 s (ratio 0.84 → 0.44), the second at 0.5 s (0.04) and the third at 0.75 s (0). Setting the ratio to 0 does not delete live puffs either: in the fixture capture they keep drawing for 13 frames (0.43 s) after the ratio drops to 0 at frame 50. What does change the moment REWIND starts is the key itself: `key_sprite.scale.x` swings between full width and 15 % as the key spins (`fighter.gd:272-273`), and the steam, a child in local coordinates, is squashed with it (predicted in B.3, "parent and flip"). That squash is a likely cause of the abrupt look; it has not been checked frame by frame.

### A6-3 follow-up: rewind squash fixed (TUNING.md Effect B revision 1)

The in-game "cut out on rewind" was the key's spin squash narrowing every live puff (rewind strip r0, frame 34). The steam now rides `godot/effects/steam_mount.gd` (`SteamMount`), which follows the key's position, facing and visibility but not its squash. `main.gd` and both fixtures use it; `wind_steam.tscn` is unchanged.

- `test_wind_steam_state.gd` at 60: **37 checks, 0 failed**. The three new checks: while rewinding, the key reached |scale.x| 0.050, the steam stayed at 0.333, and the steam stayed on the key (0.000 px).
- M6: the mount temporarily copying the key's squashed scale → 1 failed (`evidence/a6/mutations/steam-m6-mount-copies-squash.log`).
- All other tests are unchanged: Effect B config 33/0; Effect A 44/0 and 136/0; `test_slice` 25/0; `check_props3d` PASS; `test_rewind_tint` 30/60/144 50/0; `test_materials` 55/0.
- D.2 strip unchanged: pixel-identical to `captures/wind_steam/r0`.
- Rewind strip r1: differs from r0 only at frame 34, as predicted.
- In game (Tharun): it tapered off smoothly on rewind and stayed anchored to the key. Keep.

**Capture note:** Movie Maker can write copies of an earlier frame while its window is not being drawn. The summary then reports fewer frames than requested. That is what spoiled the first Effect B r0 and the first rewind r0. Every strip since was captured with `--disable-vsync --always-on-top`, reported the full frame count, and was checked frame by frame against a clean trial.

## The process shader

File: godot/shaders/particles_generated.gdshader (Effect B's ParticleProcessMaterial, converted in the editor, commit 490095f).

| What | Line(s) |
|---|---|
| shader_type | 3 |
| start() | 219 |
| process() | 269 |
| initial velocity set from its min and max | 10, 11, 139 |
| gravity changes velocity | 43 (declaration), 302 (force = gravity;), and 315 (USERDATA1.xyz += force * DELTA; where velocity is actually updated) |
| colour over life sampled | 44 (declaration), 161 (sampled in process_display_param) |
| scale over life applied | 45 (declaration), 160 (sampled) and 351–353 (applied to particle transform from process() at line 336) |
| a line tied to a brief setting (name the setting and its value) | 7 (uniform float spread; declaration) and 258 (used with get_random_direction_from_spread), matching the brief setting B.3 spread = 30.0. Note that this numeric value lives on the particle material resource, not directly hardcoded inside this shader file. |

Which of my brief's settings live in this shader, and which belong to the draw step instead:
Shader vs. Draw/Node Step Allocation (B.3 Table Sort)
Lives in the Process Shader (particles_generated.gdshader):

Lifetime & Velocity Dynamics: lifetime, initial velocity (initial_linear_velocity_min/max), gravity, radial/tangential forces, and acceleration curves.

Particle Lifecycle Ramps: color_ramp and scale_curve calculations over normalized lifetime.

Spread & Randomness: spread and lifetime_randomness logic.

Lives in the Material (Draw Step / Material Property):

Texture Asset & Blend Mode: The source particle sprite texture and blend modes (e.g., MIX or ADD) are handled by the material configuration wrapping the draw pass, not the process shader math.

Lives on the GPUParticles2D Node:

Emission & Bounds: amount (particle count cap), local_coords (world vs. local space anchoring), and visibility_rect (culling bounds) are node-level operational configurations.

## A6-4. Headless price (Step 7)

`godot/tests/cost_effects.gd`, through the wrapper: `./scripts/run-test.sh cost_effects.gd 60 300`, exit 0 (log `logs/cost_effects_60fps.log`, copy in `evidence/a6/cost/`). Example 09's script was not available on this machine, so the script was written from the handout's description. Each case runs in a fresh scene: 60 warm-up frames, then 600 measured frames.

| Case | What runs | Wall time per frame, mean ± sd (median, p95) |
|---|---|---|
| empty (**control**) | a bare `Node2D` | 0.0028 ± 0.0014 ms (0.003, 0.003) |
| game_off | `main.tscn` in FIGHT, Rivet frozen, no input; steam emitters freed, no bursts | 0.0230 ± 0.0066 ms (0.021, 0.029) |
| a_peak | game_off + 4 fresh impact bursts every 15 ticks (mean 4.26 alive per frame; 8 for a frame at each refresh, while the old four free themselves) | 0.0289 ± 0.0157 ms (0.024, 0.080) |
| b_heavy | game_off but both steam emitters kept at `amount_ratio` 1.0 | 0.0223 ± 0.0022 ms (0.022, 0.024) |

**Read against the control:**
- **The wall clock works.** game_off − empty = +0.0202 ms, about 3× the larger spread, so the script can see real per-frame work and is not only measuring itself.
- **Neither effect is distinguishable from the game without it:**
  - a_peak − game_off = +0.0059 ms, inside a spread of 0.0157;
  - b_heavy − game_off = −0.0007 ms, inside a spread of 0.0066.

  This matches CHANGE-BRIEF F's prediction, "near zero … within the empty-scene control's spread". It does so by construction: the dummy renderer neither simulates nor draws GPU particles, so all that is left is node work (instancing and freeing bursts, and steam nodes that do nothing).
- **Two clocks are dead here.** `Performance.TIME_PROCESS` and `TIME_PHYSICS_PROCESS` read 0.0000 in every case, including game_off, whose logic clearly costs 0.02 ms on the wall clock. The script prints them so this is visible, and its own comparison flags them as "WITHIN the spread: these two cases read the same". They are not used for any conclusion.
- **What this does not show:** any GPU cost. The budgets in CHANGE-BRIEF F are GPU budgets (A < 0.55 ms for 4 bursts, B < 0.20 ms for both streams, against the 0.97 ms Render Viewport baseline), and are measured windowed in the Visual Profiler (Use It).

## A6-5. Use It: checklist

Checked at revision `f825d97` (plus the docs commit after it). Godot 4.7.2.stable, Forward+, Vulkan, Apple M4.

| Check | Status | Where |
|---|---|---|
| Baseline, before and after | **done**: test_slice 60 25/0; check_props3d 60 PASS; test_rewind_tint 30/60/144 50/0; test_materials 60 55/0, before (`8731c5c`) and after every A6 change | A6-2, A6-3 |
| Configuration | **done**: Effect A 136/0, Effect B 33/0; both Effect A mutations exit 1 | A6-1, A6-3 |
| State | **done**: Effect A 44/0 at 60, including two impacts inside one lifetime; Effect B 37/0 at 60 | A6-2, A6-3 |
| Frame strips (fixture) | **done**: `captures/impact_effect/r0`, `r1`; `captures/wind_steam/r0`; `captures/wind_steam_rewind/r0`, `r1` | TUNING.md |
| In play (HUMAN CHECK) | **partly**: landed jab, block, cork and pause for A; low wind and rewind for B; boundaries held | A6-2, A6-3 |
| Against the background (HUMAN CHECK) | _open: each effect over the darkest and lightest stretch_ | |
| Edge of screen (HUMAN CHECK) | _open: a large effect near the screen edge does not pop out_ | |
| Scene load (HUMAN CHECK) | _open: Effect B on the first frames after load (headless: ratio 0 on load, B-R6)_ | |
| Claude against you | _open: each of Claude's strip readings beside Tharun's verdict, and at least one disagreement or "none"_ | TUNING.md |
| Headless CPU price | **done**: both effects within the spread of game_off; empty-scene control included | A6-4 |
| GPU price (HUMAN CHECK) | **open**: Visual Profiler GPU time, off vs on at heaviest, per effect; FPS with vsync off (F10); compare against CHANGE-BRIEF F budgets (A < 0.55 ms, B < 0.20 ms). One unlabelled screenshot so far (Render Viewport 0.33 ms, Update GPU particles 0.02 ms, case unknown) | fixture `godot/previews/gpu_price.tscn` |
| Process shader | **done**: line references checked by Claude | "The process shader" |
| No agent session changed `godot/shaders/` | **done**: the only A6 file there, `particles_generated.gdshader`, was saved by Tharun from the editor (`490095f`) | |
| Every texture credited | **done**: `godot/effects/textures/ATTRIBUTION.md` | |

### A6-5a. HUMAN CHECK: against the background (Tharun, 2026-11-09)

Fixture captures, watched windowed at 1280×720 with `-- --loop --random`. Same real level art (`bowl.png`) and camera as the game. New switches `--dark` (impact preview) and `--light` (steam preview) move the effect to the other extreme stretch (design/a6/BRIEF-FACTS.md §4: lightest x 192–223, mean luminance 160; darkest x 256–287, mean 98).

| Effect, stretch | What I saw |
|---|---|
| A, light castle (x 209) | Shards clear, core stands out against the bright stone background. |
| A, dark stretch (x 271) | Core stands out brightly, but the charcoal shards are much fainter and harder to make out against the dark background. |
| B, dark stretch (key x 271) | Steam clearly visible as bright rising plumes against the darker backdrop. |
| B, light stretch (key x 207) | Steam slightly softer against the bright castle walls, but still easily readable from the key. |

**Measurement (Claude), Effect A at frame 15:** the median shard darkening is 105 luminance levels over the castle (background 174 under the shards), but **42 over the dark stretch** (background 102). Trial capture with the `--dark` switch. This agrees with the corrected row above. Tharun's first answer for this row said the flecks "pop cleanly"; after Claude's measurement, Tharun corrected it.

**Finding:** Effect A's dark shards lose most of their contrast over the dark stretch; there, the core carries the hit. This is a candidate for a further tuning revision (a lighter shard rim or interior on dark backgrounds), not done in A6.

### A6-5b. HUMAN CHECK: scene load and edge of screen (Tharun, 2026-11-09)

Windowed run of the game, `godot --path godot`, 1280×720; closed with no `ERROR` or `SCRIPT ERROR`.

| Check | What I saw |
|---|---|
| Scene load (Effect B) | None. Both fighters' keys remained completely still and free of steam throughout the title screen and the "ROUND 1" intro sequence until wind was actually consumed. |
| Edge: steam at the left arena wall, low wind | The steam rising at the left arena wall faded out smoothly over its lifespan without popping, clipping, or cutting off early at the boundary. |
| Edge: impact bursts near the walls | The jab impact bursts landed cleanly near the arena walls with no sudden vanishing or clipped edges. |

**Context (Claude):** the arena walls are at x 132 and 500 of the 640-px view (`main.gd` `ARENA`), so neither effect can reach the screen edge itself. The wall is the nearest test there is. The steam's `visibility_rect` is ±150 local units, ±50 px on screen around the key, against a plume that rises about 30 px. The bursts use the default ±100 rect against a spread of about 20 px. Headless, scene load gives ratio 0 for both fighters (B-R6, `test_wind_steam_state.gd`).

### A6-5c. Claude against me

Each of Claude's strip readings beside my verdict. The left two columns quote TUNING.md and this report. Claude laid out the table; the last line is mine.

| Strip / check | Claude's reading | My verdict | Agree? |
|---|---|---|---|
| Effect A r0 | The shards are faint at frame 15 (median darkening 41): a linear alpha fade leaves about ⅓ alpha | First look, before Claude read it: "a bit hard to make out" | Agree |
| Effect A r1 (ramp opaque to 0.7) | Frame 15 median darkening 106: solid flecks; **scale unchanged** (0.8–1.2) | "easier to make out … solid dark flecks"; "**they also looked bigger on screen, even though the scale is unchanged**" | **Partly:** I saw them as bigger; Claude's settings and pixel counts say only their opacity changed (the darker-pixel count rose 16 %, because faint edge pixels now pass the threshold) |
| Effect B r0 (D.2) | Not read for size before my first look. Measured afterwards at frame 40: the plume is 18 × 27 view px, **about ¼ of Bolt's 112 px height** | First look: "the entire steam rise is tall, **roughly half of Bolt's height**" | **Disagree** on size, by about 2× |
| Effect B rewind r0 | The "cut" is the key's spin squash narrowing the whole plume (frame 34) | In game: "cut out immediately upon triggering the rewind state" | Agree (same event, explained) |
| Effect B rewind r1 (SteamMount) | Differs from r0 only at frame 34, as predicted | In game: "tapered off smoothly … stayed correctly anchored" | Agree |
| Background, Effect A dark stretch | Shard darkening 42 here, against 105 on the castle | First: "flecks pop cleanly"; corrected: "charcoal shards are much fainter and harder to make out" | Disagreed at first; my answer was corrected after Claude's measurement |

**My statement on where we disagreed:** On the steam size and shard scale disagreements, I accept the objective pixel measurements—the plume is a quarter of Bolt's height, and the shard scale remained unchanged at 0.8–1.2. However, I keep my visual observation for gameplay evaluation: in active motion, the extended opacity timing makes the effects feel larger and more readable to the player on screen. That live perceptual impact is what matters most for feel and feedback.
