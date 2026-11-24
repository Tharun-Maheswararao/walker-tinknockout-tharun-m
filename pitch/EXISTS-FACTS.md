# Pitch facts (not the pitch)

*Collected by Claude on 2026-11-24 from the repository at tag `a7` (`a0c95cc`), for option (c), a gameplay system: the fighter controller and its animation state machine. Facts only, each with the tag, commit or file where a reviewer can see it. Every pitch choice in `PROJECT-BRIEF.md` is Tharun's: what the project is, who it is for, the comparables, what it proves, the scope, the risk, and why. Anything not listed here does not exist yet and must be pitched as "will".*

## 1. Tags a reviewer can check out

| Tag | Commit | Date | What it adds | Film |
|---|---|---|---|---|
| `a2` | `9788922` | 2026-10-07 | A playable one-round slice: title → intro → fight → KO → rematch, Bolt (player) vs Rivet (pattern controller), generated art and audio, GDD | `README.md` "Final film" (line 78) |
| `a3` | `fcb6ea7` | 2026-10-17 | Three Blender props in a 3D prop room (not used by the fight) | `README.md` "A3 film" |
| `a5` | `f4dda68` | 2026-11-01 | REWIND tint shader driven from code, painted-tin material, material audit | `README.md` "A5 film" |
| `a6` | `66c8cbc` | 2026-11-09 | Impact burst and wind steam particles, headless CPU cost | `README.md` "A6 film" |
| `a7` | `a0c95cc` | 2026-11-22 | The key cycle and the cutout-rig jab, one authority per animated node, pins, edges, mutations, two tuning revisions | `README.md` "A7 film" (SHA `0318373f…46bd`) |

## 2. What exists of the system (option c), at `a7`

**The controller and state machine:** `godot/fighter/fighter.gd`, class `Fighter`, 385 lines, one per fighter, built in code (no `.tscn`).
- **States:** `enum S` with 11 states: IDLE, WALK, JAB, CUTLASS, POP, BLOCK, REWIND, HURT, EMPTY, KO, WIN (`fighter.gd:19`).
- **One tick:** `step(dt)` on the 60 Hz physics tick, called by `main._physics_process` (`godot/game/main.gd`).
- **Attacks:** a table of startup / active / recovery seconds per attack (`fighter.gd:41-45`).
- **Systems:** hitboxes and hurtboxes, hitstop, the wind (spring) meter, health, blocking, rewinding.
- **The controller seam:** every tick something writes an `intent` dictionary (move, jab, cutlass, pop, block, rewind). For the player that's `main._read_player()`, from input actions registered in `godot/game/controls.gd` (keyboard and gamepad). For Rivet it's `godot/fighter/rivet_brain.gd`, 59 lines: deterministic distance and wind rules, no randomness; its header calls it "not real AI".
- **Signals out:** `state_changed`, `hit_landed`, `projectile_fired`, `rewind_tick`, `wind_changed` (`fighter.gd:13-17`). Audio, music, HUD and both A6 effects listen to these; the fighter never calls them.

**The animation layer (A7):**
- **The rig:** named, `FacingPivot/BodyPivot/{sprite, KeyMount/KeyBob/key_sprite}`.
- **The players:** `FighterAnimPlayer` (`jab_action`, cutout rig, 60 fps, keys at every phase boundary) and `KeyAnimPlayer` (`wind_key_cycle`, 8-frame sheet, loops).
- **The clock:** both players are MANUAL and are put at `state_t` at the end of each physics step (`_sync_clips`), so they freeze with hitstop and pause.
- **Clip files:** `godot/animations/*.tres`, hand-written resource text.

**Tests a stranger can rerun**, all through `scripts/run-test.sh`, counts at `a7` (TEST-REPORT A7-1, A7-9; verified on a fresh GitHub clone 2026-11-22):

| Test | What it pins | Count |
|---|---|---|
| `test_slice.gd` 60 | the A2 slice: hit sounds once per attack, rewind clicks, music cues, muted run = unmuted run, facing | 25/0 |
| `test_a7_pins.gd` 60 and 30 | behaviour before and after A7: one scripted run's transitions, jab 5/6/10 ticks, cutlass 9/7/18, hitstop +5, the tick-21 press lost, hits in each phase, pause, rewind clicks, EMPTY 97 ticks | 49/0 |
| `test_a7_structure.gd` 60 and 30 | the rig, both players, `track_problems` on the real rig, one authority from the source, the state table with real input, six key turns | 57/0 |
| `test_a7_edges.gd` 60 | a jab press and a hit one tick before, on and after every phase boundary; pause on each | 70/0 |
| `test_jab_action_readback.gd` 60 | the jab clip's structure | 58/0 |
| `test_wind_key_cycle_readback.gd` 60 | the cycle clip and its sheet | 26/0 |

Older suites still pass at their counts: `test_rewind_tint` 50/0 at 30/60/144, the A6 impact and steam tests, `test_materials`, `check_props3d`.

**Process records:**
- `TUNING.md` "A7 jab_action": a first look, two revisions, each with a prediction, two strips and a verdict. Revision 2 came from Tharun's play observation.
- `TEST-REPORT.md` A7-5: mutations run in git worktrees.
- `evidence/a7/seam/`: a seam bug found by a fixture log, after the suite had passed it.
- `evidence/a7/step5-plan.md`: an approved agent plan.

**Fixtures:** `godot/previews/jab_preview.tscn` (scripted jab, per-frame log, `--clocks`) and `key_cycle_preview.tscn`.

## 3. Measurements that exist (and their limits)

- **Phase ticks, measured headless** on the real game (`evidence/a7/probes/probe_phase_ticks_*.txt`): jab 5 / 6 / 10 ticks; cutlass 9 / 7 / 18.
- **Two clocks, measured windowed** on an Apple M4, macOS 15.6, Godot 4.7.2 Forward+ on Vulkan (TEST-REPORT A7-9e): display 129 fps, physics 60 ticks/s, clip vs `state_t` gap 0.000000 s over 279 jab ticks.
- **Headless CPU cost** of the A6 effects (TEST-REPORT A6-4).
- **Not measured:** GPU time (A6 skipped it); any frame rate on another machine; any build's frame rate. "Runs at 60 fps" is not a measurement that exists. What exists is 60 physics ticks per second and 129 drawn frames per second on one Apple M4.

## 4. What does not exist (must be "will", or left out)

- **No build:** there is no `godot/export_presets.cfg` and no exported executable. Today the game runs only from the Godot editor or `godot --path godot`.
- **The renderer is Forward+ (Vulkan)**, chosen in A6 for the Visual Profiler. A web export would need the Compatibility renderer.
- **Not reusable yet:** `Fighter` has no `.tscn`. It loads its art by skin name from fixed paths (`res://assets/fighters/<skin>/`, `anchors.json`, `res://assets/props/key-<skin>-sheet.png`). It needs `main.gd` to set `opponent`, `spawn_cork` and to call `step()`. There is no demo scene that hosts one fighter on its own, and no plugin or addon packaging.
- **Only one action is animated.** `jab_action` is the only rig clip; CUTLASS, POP, BLOCK, HURT, WALK and the rest are one image per state, swapped by `_apply_pose`. The jab image appears on the first JAB tick, five frames before the hitbox (TEST-REPORT A7-12).
- **No AnimationTree, no input buffering:** a press during an attack is lost (pinned by `test_a7_pins` P5 and `test_a7_edges` E1). No cancels, no combos beyond Rivet's scripted jab-jab-cutlass.
- **One opponent behaviour:** `rivet_brain.gd`, deterministic rules.
- **No playtest with other people** is recorded anywhere. Every human check in the record is Tharun's own.
- **Known since before A7:** Rivet is drawn facing right on the title and intro until the first FIGHT tick.

## 5. Stack, as it stands

Godot 4.7.2.stable.official.ed1daf0bf, GDScript, Forward+ on Vulkan (MoltenVK), macOS 15.6, Apple M4, viewport 640×360, window 1280×720, physics 60 ticks/s. Claude Code for agent work (`claude -p` spend-limited until 2026-12-01). Export target: **none yet**. The pitch has to name one (`PROJECT-BRIEF.md`), and the target decides what the renderer can do.

## 6. What PROJECT-BRIEF.md needs (structure only, from the handout)

1. **What is it:** one sentence, then the artifact and its form when done.
2. **Why care:** the unique value.
3. **Different from what exists:** one or two real comparable games or tools Tharun actually played or used, and what this does that they don't.
4. **Who opens it:** the target role and the reader, and the first sixty seconds.
5. **What it proves:** the course skills, and the evidence that will back them.
6. **In, out, first:** one thing it will deliberately not do; the first piece that will run, and how anyone would know it ran.
7. **What could sink it:** one concrete risk, and what to do about it.
8. **Why this project:** new skills vs existing ones, with evidence for the existing ones.
9. **Two closing lists:** exists today (with the tag or commit for each) and will exist.
