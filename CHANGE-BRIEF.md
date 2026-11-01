# CHANGE-BRIEF — Tin Knockout asset slice

*Version 1 · 2026-10-05 · committed before any generation. Predictions are kept even if later refuted; results go in TEST-REPORT.md.*

## 1. Asset list

| ID | What | Source | Storyboard panels |
|---|---|---|---|
| CHAR-REF | Bolt reference / turnaround (P01) | generated | all (consistency) |
| CHAR-IDLE | P02 fight stance | generated, derived from CHAR-REF | 1, 2 |
| CHAR-WALK | P03 walk | generated | 3, 6 |
| CHAR-JAB | P04 jab | generated | 3 |
| CHAR-CUTLASS | P05 cutlass swing (empty hand; blade is WPN-CUTLASS) | generated | 5 |
| CHAR-POP | P06 pop-gun fire (empty hand; gun is WPN-POPGUN) | generated | 6 |
| CHAR-BLOCK | P07 block | generated | — (in slice, not boarded) |
| CHAR-REWIND | P08 rewind | generated | 4, 6 |
| CHAR-HURT | P09 hurt | generated | 3 (Rivet), 5 |
| CHAR-EMPTY | P10 spring empty | generated | 5 |
| CHAR-KO | P11 knocked out | generated | 7 (Rivet) |
| CHAR-WIN | P12 victory | generated | 7 |
| RIVET-* | Rivet versions of every CHAR-* pose | **edit:** palette recolour of the accepted CHAR-* images | 1–7 |
| WPN-CUTLASS | tin cutlass prop | generated | 5 |
| WPN-POPGUN | tin cork pop-gun prop | generated | 6 |
| PROP-CORK | cork projectile | generated (or cropped from WPN-POPGUN) | 6 |
| ENV-BOWL | arena background: inside the empty goldfish bowl, gravel floor, plastic castle, seaweed, moonlit glass | generated | 2, 3, 5, 6 |
| ENV-TITLE | title background: the shop counter with the bowl, from above | generated (stretch: may reuse ENV-BOWL with a title overlay) | 1 |
| SFX-BELL | boxing-ring style bell, small and tinny | generated | 2, 7 |
| SFX-JAB | hollow tin *clang* | generated | 3 |
| SFX-CUTLASS | metallic *shing* plus clank | generated | 5 |
| SFX-POP | cork pop-gun *pop* | generated | 6 |
| SFX-REWIND | one ratchet click (played once per quarter-turn) | generated | 4, 6 |
| SFX-EMPTY | spring unwinding *wrrr-clunk* | generated | 5 |
| MUS-WALTZ | music-box / carnival-organ waltz loop | generated | 1–7 |
| UI-HUD | health bars, spring dial, text | **code-drawn** (not generated; doesn't count toward the requirement) | 2–7 |

## 2. Event-to-sound map

All sounds are played by an `Sfx` helper that **listens** to gameplay signals. Gameplay code never waits on, reads, or depends on audio. Muting just sets the bus volume, so the same signals still fire.

| Sound | Exact trigger (gameplay code that already represents the event) | Double-trigger prevention |
|---|---|---|
| SFX-BELL | `Round` state changes to `FIGHT` (round start) and to `KO` (round end) | Played from the state-*enter* handler only; a transition to the same state is ignored. |
| SFX-JAB | `Fighter.hit_landed(attack="jab")`, emitted when a jab hitbox first overlaps the opponent's hurtbox | Each attack instance has a `has_hit` flag. The first overlap sets it, emits once, and disables the hitbox. Later overlapping frames do nothing. |
| SFX-CUTLASS | `Fighter.hit_landed(attack="cutlass")` | Same `has_hit` flag per swing. |
| SFX-POP | `Fighter.projectile_fired`, when a cork is spawned | Firing uses `is_action_just_pressed` plus an attack lockout. Holding the key fires once; the next shot needs a new press after recovery. |
| SFX-REWIND | `Fighter.rewind_tick`, emitted each time accumulated rewind angle crosses a 90° boundary | Ticks come from a counter, not from frames: at most one per quarter-turn, regardless of frame rate or how long the key is held. |
| SFX-EMPTY | `Fighter` state *enters* `EMPTY` (spring reaches 0) | Edge-triggered on state entry. Staying empty does not re-fire it. |

## 3. Music behaviour

| Situation | Behaviour | How it's implemented |
|---|---|---|
| Round in progress | MUS-WALTZ loops seamlessly | OGG with loop enabled on import, loop point at a bar boundary |
| Bolt's spring < 25 % | Music slows and pitch drops (~0.85×) | Tween `pitch_scale` on the music player; back to 1.0 when wind ≥ 25 % |
| Pause | Quieter (−10 dB) and muffled | Enable a low-pass effect on the Music bus and lower its volume; reverse on unpause |
| Failure (Bolt KO) | Music stops on the KO bell | `stop()` in the KO state handler |
| Success (Rivet KO) | Music stops on the KO bell | Same handler: the end of a round always means silence |
| End of slice / rematch | Silence until R; a rematch restarts the loop from the top | Restart on `Round` entering `FIGHT` |
| Mute | `M` toggles music, `N` toggles effects, separately | Bus mute on `Music` / `SFX` buses |

## 4. Predicted failure cases

| # | Prediction | How I will check it |
|---|---|---|
| F1 | **Pose drift:** SDXL-Turbo poses drift from the reference (helmet too small or too big, two portholes, key missing or on the front). | Scale each pose to 112 px and overlay it on CHAR-REF. Measure the helmet/height ratio (must be 33–47 %). Check consistency rules 2 and 3 for each pose. Rejects go on the contact sheet. |
| F2 | **Hit sound fires more than once per attack** because the hitbox overlaps for several physics frames. | Automated test: a scripted input sequence of N jabs and N cutlass swings into a stationary opponent. Assert `SFX-JAB count == jabs that hit` and the same for the cutlass. |
| F3 | **Music loop clicks at the seam.** | Listen to at least 3 repetitions (human). Plus an automated check on the exported OGG: the sample jump and the RMS difference across the seam must be under a threshold. |
| F4 | **Rivet (copper and verdigris) disappears against the bowl.** The palette check already shows a 1.07:1 contrast between Rivet's suit and the planned gravel. | Measure luminance contrast between each fighter's main colours and the real generated background behind them. Squint test on a muted screenshot. Fix by recolouring Rivet or regenerating the background with a lighter band. |
| F5 | **Rewind clicks fire every frame** while the key is held (a machine-gun buzz). | Automated test: hold Rewind for exactly 2.0 s. Assert ticks == floor(rewound angle / 90°). |
| F6 | **Muted play is unreadable:** you can't tell idle from rewinding, or empty from hurt. | Muted playtest (human) plus side-by-side state screenshots. Each state must be identifiable without sound or HUD text. |
| F7 | **Weapon sprites don't line up with the hand** in generated poses (the anchor moves between poses). | Measure the hand anchor per pose after generation and store the offsets in code. Visually check every weapon pose in-engine. |

## Revision 1 — 2026-10-06 (after building; results in TEST-REPORT.md)

- **New assets:**
  - `PROP-KEY`: the winding key as a separate sprite, see CHARACTER-SHEET revision 1.
  - **Cork impact** reuses SFX-JAB at pitch 1.25. There is no separate generated sound for it.
  - **Blocked hits** play their hit sound at pitch 0.8, still exactly once per hit.
- **Gameplay rule changes found by testing:**
  - a 1.5 s pop-gun cooldown for Rivet at round start;
  - **HURT always returns to IDLE**, which fixes a stun-lock chain at 0 wind;
  - a fighter with 0 wind cannot walk.
- **Facing** follows the walk input (it was "always face the opponent").
- **ENV-TITLE** was not made; the title is an overlay on the arena.
- Predicted failures F1–F7: outcomes are in TEST-REPORT section 10.

---

# Assignment 3 — three 3D props for Tin Knockout

*Version 1 · 2026-10-14 · committed before any asset is built. The Assignment 2 brief above is unchanged. Later changes go under "A3 revisions" below and never rewrite this version.*

> **Authorship:** I chose the three assets, the character scale and the dropped cork. Claude drafted the numbers, colours and failure cases from those choices and from my "Learn the window" session. I reviewed every number below before committing. Changes I made to Claude's draft: **none. I accepted the numbers, colours, budgets and failure cases as Claude drafted them.**

## A3.1 Ground rules

| | |
|---|---|
| **Game scale** | Character scale: **Bolt = 1.80 m tall** (helmet ≈ 0.72 m, 40 %). Everything is sized against him. 1 Blender unit = 1 m = 1 Godot unit, so nothing converts. |
| **Where they appear** | A new Godot 3D "prop room", `godot/prop_room/prop_room.tscn`: a floor, one light, a camera, and the three props side by side. The bowl-floor diorama is not yet connected to the 2D slice. Assignments 4 and 5 reuse it. |
| **Axes** | Blender is Z-up; Godot is Y-up. The glTF exporter's **+Y Up** converts them. Each prop's **front faces Blender −Y**, which arrives as **Godot +Z**, so a Godot camera at +Z looking toward −Z sees the front. |
| **Origin (all three)** | The **centre of the underside, at Blender's world origin (0, 0, 0)**, with the lowest point at Z = 0. Godot places a scene at its origin, so a prop dropped at floor height Y = 0 should sit exactly on the floor. |
| **Build** | Basic shapes only, ≤ 6 per asset, one `execute_blender_code` call per shape. At the end: apply rotation and scale, **join the parts into one object** named after the asset, and set the origin to the base centre. One `.blend` and one `.glb` per asset. |
| **Materials** | Flat colour as the **Principled BSDF Base Color**, roughness 0.5, metallic 0, no textures. (The viewport display colour alone would not survive glTF export.) |
| **Triangle limit** | Course limit ≤ 500 per asset. My own budgets are below and lower. Cylinder/cone segments are set explicitly: a cylinder with *n* sides and n-gon caps is 4*n* − 4 triangles, a cone 2*n* − 2, a cube 12. |
| **Tolerance** | Sizes match the brief within **±0.01 m** in both Blender and Godot. The base sits at height 0 within **±0.005 m**. |

## A3.2 The assets

### ASSET 1 — `castle`: sunken-castle ornament (environment)

| | |
|---|---|
| **In the game** | The plastic castle on the bowl floor, behind the fighters. It is the landmark that says "goldfish bowl" (it appears pink in my A2 background). |
| **Size W × D × H** | **1.80 × 0.82 × 2.30 m** |
| **Why that size** | At 2.30 m it is 1.28 × Bolt's height, so it reads as scenery *behind* him, not a hiding place. It is 1.80 m wide, one Bolt-height. The 0.70 m door is deliberately too small for Bolt: it is an ornament, not a building, which sells the toy-world joke. |
| **Shapes (6)** | Keep: cube 1.20 × 0.80 × 1.40. Two towers: cylinders r 0.30, h 1.80, 12 sides, at X = ±0.60. Two roofs: cones r 0.30, h 0.50, 12 sides, on top of each tower (Z 1.80–2.30). Door: cube 0.40 × 0.04 × 0.70 on the −Y face, protruding 0.02. |
| **Look** | Two towers with pointed roofs and a dark door read as "castle" from any side. **Colours:** faded aquarium pink `#D98BA0` (keep and towers), verdigris teal `#3E8E86` (roofs), dark brown `#3A2A20` (door). |
| **Budget** | **≤ 200 triangles.** Predicted 156: 12 keep + 2 × 44 towers + 2 × 22 roofs + 12 door. It is the biggest prop on screen, but its silhouette is all straight lines and cones, so 12 sides is enough. |

### ASSET 2 — `windkey`: winding key pickup (collectible)

| | |
|---|---|
| **In the game** | A spare brass key lying on the bowl floor. Picking it up would refill Bolt's spring. It is a future mechanic, not in the A2 slice. |
| **Size W × D × H** | **0.60 × 0.14 × 0.70 m** |
| **Why that size** | The same size as the key on Bolt's back, about ⅓ of his height, so the player instantly recognises "that's my key". |
| **Shapes (4)** | Shaft: cylinder r 0.04, h 0.36, 8 sides, standing on Z = 0. Collar: cylinder r 0.07, h 0.04, 12 sides, at Z 0.36–0.40. Two bow lobes: cylinders r 0.15, depth 0.06, 16 sides, **rotated 90° about X** so their round faces point ±Y, centred at X = ±0.15, Z = 0.55. |
| **Look** | The two round lobes on a stem are the key's silhouette, as on Bolt's back. It stands upright, bow on top. **Colours:** polished brass `#C9A23A` (shaft and lobes), dark brass `#8C6A1E` (collar). |
| **Budget** | **≤ 250 triangles.** Predicted 192: 28 shaft + 44 collar + 2 × 60 lobes. The round lobes *are* the recognisable part, so they get the most sides. |
| **Note** | The origin is at the shaft tip, so in-game it can stand or hover. Any hover offset is game code, not the asset. |

### ASSET 3 — `toybox`: toy-box crate (prop)

| | |
|---|---|
| **In the game** | The tin toy box that weapon pickups (cutlass, mallet, shield) come out of, on my A2 "Out" list. |
| **Size W × D × H** | **1.26 × 0.76 × 0.75 m** |
| **Why that size** | At 0.75 m the lid is at Bolt's waist (≈ 0.42 × 1.80 m), so he can reach in. The 1.20 m inner body fits the ~0.9 m cutlass lying flat. |
| **Shapes (4)** | Body: cube 1.20 × 0.70 × 0.65 (Z 0–0.65). Lid: cube 1.26 × 0.76 × 0.10 (Z 0.65–0.75), overhanging 0.03 on each side. Band: cube 1.22 × 0.72 × 0.08 around the body at Z 0.30–0.38, standing in for a lithographed stripe. Latch: cube 0.12 × 0.03 × 0.12 on the −Y face just under the lid. |
| **Look** | A box with an overhanging lid and a brass latch reads as "toy chest". The stripe gives the tin-toy look. **Colours:** tin-toy red `#B5302A` (body), cream `#E8DCC0` (lid), navy `#23395B` (band), brass `#C9A23A` (latch). |
| **Budget** | **≤ 100 triangles.** Predicted 48: 4 cubes × 12. Boxes need nothing more. The spare budget is not a target. |

## A3.3 Predicted failure cases

| # | Prediction | How I will check it |
|---|---|---|
| A3-F1 | **Wrong size by a factor of 2 (or 10).** Blender's default cube is 2 m, not 1 m (seen in my own sidebar). A "scale 0.6" cube becomes 1.2 m, and a size typed in centimetres comes out 100× too big. | Blender sidebar **Dimensions** vs. the brief, ±0.01 m, recorded in TEST-REPORT. The Godot check prints each asset's AABB size for a second comparison. |
| A3-F2 | **Arrives lying on its side or facing backwards.** Caused by exporting with +Y Up off, or by the key's 90° lobe rotation leaking into the whole object. | The Godot check reports which axis is the tallest (it must be Y for the castle and key) and the node rotation (must be 0, 0, 0). A camera at +Z must see the castle door and the toy-box latch. |
| A3-F3 | **Floats or sinks.** The origin stays at the geometric centre, as Blender's primitives create it, so the base is at −H/2 or +H/2. | The check prints each AABB's minimum Y; it must be 0.000 ± 0.005. Human check: each prop placed at Y = 0 visibly sits on the floor, with no gap and no clipping. |
| A3-F4 | **Unapplied scale or rotation.** Blender shows Scale ≠ 1, the glTF node carries it, and Godot shows a scaled node. | Blender sidebar: Rotation 0°, Scale 1.000 before export. The Godot check prints node scale; it must be (1, 1, 1). |
| A3-F5 | **Claude builds more than asked**: default 32-sided cylinders (124 tris each), extra bevels or decorations, or more than 6 shapes. | Blender **Scene Statistics** triangle count vs. my budget (200 / 250 / 100). The Outliner shows the part count before joining. I compare each `execute_blender_code` body with the brief before approving it. |
| A3-F6 | **A colour does not survive export.** It was set only as the viewport colour, or a material slot was lost when joining, so the asset arrives white or single-coloured. | Human check in Godot under one light. The check also prints each surface's material albedo for comparison with the hex codes. |
| A3-F7 | **The MCP route breaks mid-build**: Claude cannot reach port 9876, or a session started before the server cannot see the tools. | The first `get_scene_info` call must return the scene. Record any exact error in FRICTIONAL.md. Time box 2 h, then fall back to the script route (`blender -b --factory-startup --python-exit-code 1 --python …`). |

## A3.4 Planned hand edit

At least one change made by me with the mouse in Blender, recorded in FRICTIONAL.md and the film. Candidate: recolour the toy box's band, or nudge the castle door, then re-check the dimensions in the sidebar. *(I will confirm which while building.)*

## A3 revisions

*(none yet)*

---

# Assignment 5 — a state tint from code, and a textured tin material

*Version 1 · 2026-11-01 · committed before either shader exists and before the first agent prompt. The A2 and A3 briefs above are unchanged. Later changes go under "A5 revisions" below, dated, and never rewrite this version.*

> **Authorship:**
> - **Layout and facts:** Claude laid out these headings from the Assignment 5 handout and filled in the file:line facts from `design/a5/BRIEF-FACTS.md`.
> - **Design decisions:** Claude proposed them on 2026-11-01 and I accepted them all unchanged. They cover the state, tint colour, strength, fade times, rules R1–R6, uniform names, hints and defaults, boundaries, the textured object, the two materials, and the material plan in A5.5 (texture choice, import settings, uniforms, material values, lighting).
> - **Colour line:** I was stuck, so I asked Claude for a suggestion. Claude suggested `COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, rewind_amount * tint_strength);` on 2026-11-01. I typed it in myself and can explain each part: the swizzle keeps alpha, `mix` blends from the sprite's colour to the tint, and the product makes the amount 0 at rest and 0.5 at full.
> - **Mine:** every predicted number and its working (by hand, on paper), the hint-experiment predictions, the failure cases and the short answers.
> - **Review corrections I accepted from Claude:**
>   - the check references in F1–F3 (R3 → R6, "performance throttle" → the R2 test at 30/60/144, R5 → R3);
>   - "unshaded white" → "white … still lit by the scene" in short answer 4.

## A5.1 The state

| | |
|---|---|
| **State** | REWIND |
| **What the effect communicates** | "This fighter is cranking its key and is open." A blue tint fades in while a fighter rewinds and fades out after it stops. |
| **Why the player needs it** | REWIND is the vulnerable window: a hit there does 1.5× damage and causes a knockdown (`fighter.gd:228-230`). The player must see **Rivet** rewinding to punish it, and must notice their own rewind as a risk. Today the only cue is the key pose. |
| **Script and variable** | `godot/fighter/fighter.gd`: `var state` (line 50) equals `S.REWIND` (enum, line 19). Entered at line 159; left at line 204 (key released), line 232 (hit, to HURT) and line 236 (KO). |
| **Object shaded** | Each fighter's body `sprite: Sprite2D` (`fighter.gd:64, 72`). The key and weapon sprites are separate nodes and are not shaded. |

## A5.2 Effect specification

**Shader:** `godot/shaders/rewind_tint.gdshader` · `shader_type canvas_item;` · render_mode: none. It sits on one ShaderMaterial per fighter, on each fighter's body `sprite`.

**Uniforms.** No sampler uniforms; the sprite's own texture arrives in `COLOR`.

| Name | Type | Hint | Default | Set by |
|---|---|---|---|---|
| `rewind_amount` | float | `hint_range(0.0, 1.0)` | `0.0` | the driver, every frame, from `fighter.state == S.REWIND` (0 = no tint, 1 = full) |
| `tint_color` | vec4 | `source_color` | `vec4(0.353, 0.627, 1.0, 1.0)`, i.e. RGB (90, 160, 255) | the material (Inspector), not changed at runtime |
| `tint_strength` | float | `hint_range(0.0, 1.0)` | `0.5` | the material (Inspector), not changed at runtime |

**Colour line,** the one line inside `fragment()` that changes the colour:

```glsl
COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, rewind_amount * tint_strength);
```

**Rules**

| # | Rule | My value | Evidence: headless test or my eyes, and how |
|---|---|---|---|
| R1 | Uniform value when the state begins, and when it ends | When REWIND begins, `rewind_amount` starts rising from its current value (0.0 from rest) to 1.0. When REWIND ends, it falls from its current value to 0.0. Outside REWIND, at rest, it is exactly 0.0. | Headless test: hold `rewind` through the real input path, sample every frame. |
| R2 | How long each change takes in seconds (± one frame period); the same game time at 30, 60 and 144 fps | Linear ramps: **fade-in 0.15 s** (0 → 1, rate 1/0.15 per s) and **fade-out 0.30 s** (1 → 0, rate 1/0.30 per s). Tolerance is one frame period (1/30, 1/60, 1/144 s), with the same game-time duration at 30, 60 and 144 fps. | Headless test at `--fixed-fps` 30, 60 and 144 through the wrapper: game time from the first frame the value moves to the first frame it reaches 1.0 (in) or 0.0 (out). |
| R3 | The state begins again mid-transition: restart, extend or ignore | **Extend:** if REWIND begins again during the fade-out, the value rises from where it is at the fade-in rate. It never drops on re-entry, and it reaches 1.0 after (1 − v) × 0.15 s. | Headless test: release, re-press mid-fade-out, assert no frame-to-frame drop and the time to 1.0. |
| R4a | `Engine.time_scale`: is the duration in scaled or unscaled time? | **Scaled** game time (the frame `delta`), the same clock as the simulation. At `time_scale` 0.5 the fade-in takes 0.30 s of real time and 0.15 s of game time. | Headless test with `Engine.time_scale = 0.5`. |
| R4b | While the tree is paused (the game never does this, `main.gd:38`, but say what happens) | **Freeze:** the value holds while `get_tree().paused` is true and resumes from the same value after. | Headless test: pause the tree mid-fade, assert the value is unchanged over several frames. |
| R4c | While the game's own pause flag is set (`main.paused`, `main.gd:115-117, 134`) | **Freeze:** the value holds while `main.paused` is true, because the state itself is frozen then. It resumes from the same value after unpause. | Headless test: press `pause` (P) mid-fade through real input, assert the value is unchanged. |
| R5 | The state ends before a transition finishes (for example, a hit during the fade-in, `fighter.gd:232`) | **Fade out from the current value**, no snap: from value v the fade-out takes v × 0.30 s. | Headless test: release (or get hit) mid-fade-in, assert the value falls from where it was. |
| R6 | Bolt and Rivet: how each gets its own value | **One ShaderMaterial per fighter**, both using the same shader. Rivet's REWIND never changes Bolt's `rewind_amount`, and vice versa. | Headless test: each sprite's material is a different object with the same shader; Bolt rewinds while Rivet's value stays 0.0. Eyes: in play. |
| Look | The tint is visible on both fighters, the pose details still read, and the key and weapon are untinted | as specified above | **My eyes:** captures at the controlled values (A5.3) and play (Use It). No headless run can judge this. |

**Boundaries.** The handout's list, applied to these files:
- Unchanged:
  - collision and hurtboxes (`fighter.gd:112-125`);
  - movement;
  - input (`game/controls.gd`);
  - the state machine and its timings (`fighter.gd:128-255`);
  - the expectations in `tests/test_slice.gd` and `tests/check_props3d.gd`;
  - every object other than the two fighter body sprites.
- The driver may read `fighter.state`; it never writes game state.

## A5.3 Controlled inputs and predicted values

**Lighting:** the shader is canvas_item, there are no 2D lights, and `rendering/viewport/hdr_2d` is off (not set in `project.godot`). Because there are no 2D lights in the arena and HDR 2D is turned off, the colour line works directly on the original raw pixel colour values from the PNG file, so my predictions apply `mix` to those numbers with no other step in between.

**Pixels.** Measured texels from `design/a5/BRIEF-FACTS.md`. Both are opaque, and the capture position assumes Bolt at his start position (x 200, facing right) in a 1280×720 capture:

The three controlled values are `rewind_amount` = 0.0, 0.5 and 1.0, with `tint_strength` 0.5 and `tint_color` (90, 160, 255), so the mix amount t = `rewind_amount` × 0.5 = 0, 0.25 and 0.5.

| Pixel | Input RGB | Capture px | `rewind_amount` 0.0 (t = 0) | `rewind_amount` 0.5 (t = 0.25) | `rewind_amount` 1.0 (t = 0.5) |
|---|---|---|---|---|---|
| A: Bolt's chest, texel (251, 275) | (217, 87, 64) | (407, 477) | (217, 87, 64) | (185, 105, 112) | (154, 124, 160) |
| B: Bolt's helmet dome, texel (281, 153) | (251, 188, 34) | (427, 396) | (251, 188, 34) | (211, 181, 89) | (171, 174, 145) |

**Working, by hand (2026-11-01), on paper, photographed in `design/a5/predictions-pixelA-0.5-handwritten.jpg`.** Each channel is `c × (1 − t) + tint × t`. Pixel A at `rewind_amount` 0.5 (t = 0.25):
- R = 217 × 0.75 + 90 × 0.25 = 162.75 + 22.5 = 185.25 ≈ **185**
- G = 87 × 0.75 + 160 × 0.25 = 65.25 + 40 = 105.25 ≈ **105**
- B = 64 × 0.75 + 255 × 0.25 = 48 + 63.75 = 111.75 ≈ **112**

*Note (Claude, from checking my arithmetic):* five results at t = 0.5 land exactly on .5 before rounding (A: 153.5, 123.5, 159.5; B: 170.5, 144.5). I rounded them up, so the capture may read one step lower in those channels.

**Contrast against the background** (WCAG relative-luminance ratio, computed 2026-11-01). Pixel A is compared with the background just right of Bolt's chest at his start position: the pink castle, mean RGB (215, 89, 123), measured by Claude (`design/a5/BRIEF-FACTS.md`).

| Pair | Ratio |
|---|---|
| Chest at `rewind_amount` 0, (217, 87, 64), vs castle | **1.04 : 1** |
| Chest at `rewind_amount` 1, (154, 124, 160), vs castle | **1.03 : 1** |

Worked example, the chest at `rewind_amount` 0:
1. Normalise each channel: R = 217/255 ≈ 0.8510, G = 87/255 ≈ 0.3412, B = 64/255 ≈ 0.2510.
2. Linearise (every c > 0.04045, so use ((c + 0.055)/1.055)^2.4): R_lin ≈ 0.6939, G_lin ≈ 0.0953, B_lin ≈ 0.0513.
3. Luminance: L = 0.2126 × 0.6939 + 0.7152 × 0.0953 + 0.0722 × 0.0513 = 0.1475 + 0.0682 + 0.0037 = **0.2194**.

*Note (Claude, from re-checking the arithmetic):*
- Both ratios are correct. The castle's luminance is 0.2302 and the tinted chest's is 0.2382.
- The chest is slightly darker than the castle at 0 and slightly lighter at 1. Somewhere in between, the two have the same luminance, a 1.00 : 1 ratio.
- Against the castle, the tint is therefore a hue cue (red toward violet-blue), not a brightness cue.

## A5.4 Hint experiment predictions

**Setup:** a 3×1 PNG with texels 64, 128 and 192 on two unshaded quads. Quad S samples with `source_color, filter_nearest`; quad D with `filter_nearest` only. Linear tonemap at exposure 1.0, with glow, fog and adjustments off. Forward+ (`project.godot:15`).

| Band (file value) | Quad S displays | Quad D displays |
|---|---|---|
| 64 | 64 | 137 |
| 128 | 128 | 188 |
| 192 | 192 | 225 |

**Working, using the handout's encode(x)**, band 64 on quad D: v = 64/255 = 0.250980 → v^0.41667 = 0.562144 → × 1.055 = 0.593062 → − 0.055 = 0.538062 → × 255 = 137.205906 ≈ **137**. Bands 128 and 192 use the same steps.

**Which quad shows the file's values unchanged, and why:** Quad S shows 64, 128, and 192 unchanged because the texture sampler decodes the sRGB input values into linear space (decode(x)) upon reading, and the output screen stage applies the exact inverse function (encode(x)) upon display, cancelling out both transformations.

## A5.5 Material plan

**Object(s) and scene:** the toy box in `godot/prop_room/prop_room.tscn` ("fresh from the shop"), and a second toy-box instance beside it ("a hundred rounds later"). Two copies of the same mesh, so any difference between them comes from the material, not the shape. The shader replaces the toy box's red body material, slot `toybox_red` (the glb's material names are `toybox_red`, `toybox_cream`, `toybox_navy` and `toybox_brass`, read from `godot/assets/props3d/toybox.glb`'s JSON chunk).

**Lighting I will judge under:** the prop room exactly as A3 left it (`prop_room.tscn`):
- Sun DirectionalLight3D, energy 1.0, shadows on;
- WorldEnvironment: custom background colour, ambient (0.45, 0.5, 0.6) at energy 0.6, default (Linear) tonemap.

SSAO, SSIL, SSR, SDFGI, glow and fog are off, because the Environment never enables them. I compare captures only under this setup, from the scene's Camera3D at (0, 1.6, 5.5).

**Textures.** All four come from Poly Haven "Metal Plate" (https://polyhaven.com/a/metal_plate) by Rob Tuytel, CC0, 1k PNG, 16-bit. Credits and checksums are in `godot/assets/textures/metal_plate/ATTRIBUTION.md`.

| Role | File | What its numbers mean | Sampled as | compress/mode | compress/normal_map | mipmaps/generate |
|---|---|---|---|---|---|---|
| Colour: bare metal under the paint | `metal_plate_diff_1k.png` | sRGB-encoded colour of the bare plate | colour, `source_color` | 2 (VRAM Compressed) | 2 (Disabled) | true |
| Data: normal map | `metal_plate_nor_gl_1k.png` | tangent-space surface direction, x/y/z remapped to 0–1, OpenGL (Y+) green | data, `hint_normal` | 2 (VRAM Compressed) | 1 (Enable) | true |
| Data: roughness, also the wear mask | `metal_plate_rough_1k.png` | 0 = mirror-smooth, 1 = fully rough; the same values decide where the paint wears through first | data, no `source_color` | 2 (VRAM Compressed) | 2 (Disabled) | true |
| Calibration only | `metal_plate_nor_dx_1k.png` | the same normals with DirectX (Y−) green | not bound to any material | 2 (VRAM Compressed) | 1 (Enable) | true |

I also set two more import settings on all four files so the editor has nothing to change later:
- `roughness/mode=1` (Disabled);
- `detect_3d/compress_to=0` (Disabled).

Both labels were read from the Godot 4.7.2 binary.

Import values, read from the Godot 4.7.2 binary's property hints:
- `compress/mode`: 0 Lossless, 1 Lossy, 2 VRAM Compressed, 3 VRAM Uncompressed, 4 Basis Universal
- `compress/normal_map`: 0 Detect, 1 Enable, 2 Disabled
- `mipmaps/generate`: true or false

**Uniforms.** At least four non-texture uniforms, in at least two `group_uniforms` groups:

| Name | Type | Hint and range | Default | Group | What I expect to change on screen across the range |
|---|---|---|---|---|---|
| `paint_color` | vec4 | `source_color` | `#B5302A` (A3's toy-box red) | paint | The hue of the painted areas; bare-metal areas do not change. |
| `paint_roughness` | float | `hint_range(0.0, 1.0)` | 0.35 | paint | At 0, a small sharp highlight from the Sun on the painted areas; at 1, a broad dull sheen. |
| `wear_amount` | float | `hint_range(0.0, 1.0)` | 0.1 | metal | At 0, all paint; rising, bare metal (from the colour texture) shows through where the roughness map is roughest first; at 1, all bare metal. |
| `normal_depth` | float | `hint_range(0.0, 2.0)` | 1.0 | metal | At 0, flat with no dents or scratches; at 2, dents exaggerated. |
| `uv_scale` | float | `hint_range(0.5, 8.0)` | 2.5 | metal | The tile size. The plate is 0.5 m and the box 1.26 m wide, so 2.5 is about life size; at 8 the pattern repeats visibly. |

Samplers: the colour, normal and roughness textures above, each with repeat and linear mipmap filtering. The `_nor_dx` file is not a sampler.

**Two materials:** `godot/prop_room/materials/toybox_fresh.tres` and `godot/prop_room/materials/toybox_worn.tres`, both using the same shader. They share the textures and `paint_color`. Two values differ:
- **fresh:** `wear_amount` 0.05, `paint_roughness` 0.30;
- **worn:** `wear_amount` 0.55, `paint_roughness` 0.70.

The other uniforms stay at their defaults. Why: the same tin toy box before and after a career of fights, which is the game's story in one object.

**Where they attach:** `toybox_fresh.tres` goes behind `toybox.glb`'s per-material "Use External" setting in Advanced Import, because the A3 glbs embed their materials (`CHANGE-BRIEF.md` A3.1). "Use External" binds one material per glb slot for every instance. So the second instance takes `toybox_worn.tres` as a surface material override saved in `prop_room.tscn`, which a reimport also keeps.

## A5.6 Predicted failure cases

| # | Prediction | The check that catches it |
|---|---|---|
| A5-F1 | If Bolt and Rivet accidentally shared a single material instance, Bolt tinting blue during the rewind effect would simultaneously force Rivet to turn blue as well. | The R6 headless test, plus a look check in play. |
| A5-F2 | If the rewind duration logic relied on unscaled delta frames instead of delta time, the rewind effect would speed up or slow down depending on the frame rate. | The R2 test at `--fixed-fps` 30, 60 and 144. |
| A5-F3 | Since the rule is set to extend, if the code incorrectly restarted the rewind timer back to 0 whenever triggered again mid-animation, the rewind effect would abruptly snap and loop from the beginning instead of blending forward. | The R3 retrigger test. |

## A5.7 Short answers

1. **Which renderer does project.godot name, and what does it rule out?** The project uses the Forward Plus (Forward+) renderer (`project.godot:15`, `config/features`; there is no `rendering_method` line). It provides full support for complex lighting and modern shader features without the feature limitations of Mobile or Compatibility modes. However, it rules out running the game on older hardware, web exports (HTML5/WebGL), and low-end mobile devices.
2. **What colour arrives in your fragment function before you change it, and what would the tempting alternative give you?** The COLOR variable in fragment() arrives with the original texture pixel multiplied by the node's modulate colour property. The tempting alternative is sampling the raw texture directly using texture(TEXTURE, UV).
3. **canvas_item: what would `texture(TEXTURE, UV)` give you instead of `COLOR`?** Sampling texture(TEXTURE, UV) directly skips node-level tinting (modulate / self_modulate) as well as vertex colours. You wouldn't notice a difference in this game today, since modulate is white, but using texture(TEXTURE, UV) would break any future adjustments to the node's modulate colour.
4. **spatial: what does `ALBEDO` hold if you never write it, and what does `COLOR` hold?** In spatial shaders, if ALBEDO is never written to, it defaults to white, vec3(1.0, 1.0, 1.0), and is still lit by the scene. The COLOR built-in holds the mesh's vertex colours, which evaluate to solid white vec4(1.0, 1.0, 1.0, 1.0) for my .glb models since they contain no vertex colour data.
5. **How long would a frame-counting version of your effect last at 30, 60 and 144 fps?** If the effect is programmed by counting 9 frames (tuned for 60 fps / 0.15 s), those 9 frames last 0.30 s at 30 fps (running twice as slow) and 0.0625 s at 144 fps (running more than twice as fast). Similarly, a 0.30 s fade-out (18 frames at 60 fps) would take 0.60 s at 30 fps and 0.125 s at 144 fps.
6. **Which resource holds your uniform's default, which holds its current value, and what happens if two objects share the material?** The default parameter value lives in the .gdshader file, while set_shader_parameter() stores the runtime value on the specific ShaderMaterial instance. If two sprites shared a single material, updating the parameter during Bolt's rewind would cause Rivet to mistakenly display the same blue tint simultaneously.
7. **Does `hint_range` clamp a value your driver sets from code?** My prediction: hint_range only constrains the UI slider in the Inspector. It does not clamp values passed programmatically via code, so calling set_shader_parameter() with 2.0 will send 2.0 directly to the shader without being clamped by the range. (Checked in Use It.)

## A5 revisions

- **2026-11-01: shader file names.** Version 1 named only `godot/shaders/rewind_tint.gdshader`. The textured shader is `godot/shaders/painted_tin.gdshader`. The hint-experiment shader will be `godot/shaders/hint_experiment.gdshader`. Its sampler names are `metal_albedo` (colour), `metal_normal` (normal) and `metal_rough` (roughness and wear mask). Claude suggested these names and I used them.
