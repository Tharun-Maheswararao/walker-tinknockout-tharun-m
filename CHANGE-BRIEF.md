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
