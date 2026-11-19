# A7 brief facts (not the brief)

*Collected by Claude on 2026-11-19 from this repository at `66c8cbc` (tag `a6`), the installed Godot 4.7.2 and three headless probes. It contains facts only. Every choice in CHANGE-BRIEF.md is yours to make: the clips, the routes, the sheet, the phase table, the cycle spec, the authority, the predictions and the evidence split. Where a number below was computed rather than probed, it says so.*

## 1. Starting state (2026-11-19, after A6)

- Tags `a2`, `a3`, `a5`, `a6` (`66c8cbc`). There is no `a4` tag. The working tree is clean and matches `origin/main`.
- `CLAUDE.md` is the A6 version. It imports `@CHANGE-BRIEF.md`, has a "Headless facts" block, protects `godot/shaders/` and `scripts/run-test.sh`, and has no "One authority" section. There is no `AGENTS.md`, so the handout's Step 1 prompt applies as written: **revise** CLAUDE.md.
- `CHANGE-BRIEF.md` holds the A6 brief. The handout says to **replace** it; the A6 version stays in history at tag `a6`.
- `scripts/run-test.sh` is the A6 wrapper (`git show a6:scripts/run-test.sh`). It fails a run on `SHADER ERROR` or `SCRIPT ERROR`, but not on `Failed loading resource`. The A7 wrapper adds that third pattern. **You** replace it and commit it before Step 1; agents never edit that file (CLAUDE.md, Ownership).
- **There is no animation in the project yet.** No `AnimationPlayer`, `AnimationTree`, `AnimatedSprite2D`, `SpriteFrames`, `Skeleton2D` or `Bone2D` node or resource exists in `godot/` (grep, 2026-11-19).
- `claude -p` is still spend-limited until 2026-12-01 (A6 SOURCES, Tools). Unless that changes, agent prompts run in the interactive session again, and the handout's `.jsonl` checks need the same note as in A6.

## 2. Engine and project

| Fact | Where |
|---|---|
| Godot 4.7.2.stable.official.ed1daf0bf | `godot --version` |
| Forward+ on Vulkan (MoltenVK), Apple M4, macOS 15.6 | `godot/project.godot:15, 31`; TEST-REPORT A6 environment line |
| Viewport 640×360, window 1280×720, stretch `canvas_items` | `godot/project.godot:23-27` |
| Physics: 60 ticks per second under any `--fixed-fps` (probe header prints `Engine.physics_ticks_per_second=60` at 60 and 30) | `evidence/a7/probes/probe_phase_ticks_*fps.txt` |
| Main scene is a bare `Node2D`; everything, including both fighters, is built in `main.gd:_ready()` | `godot/game/main.tscn`; `godot/game/main.gd:40-107` |
| Main is `PROCESS_MODE_ALWAYS`; the fighters are `PROCESS_MODE_INHERIT` (0), so they and any child inherit ALWAYS | `main.gd:41`; names probe below |
| Darkest and lightest background stretches (for "Against the background"): x 256–287 (mean luminance 98) and x 192–223 (160) | `design/a6/BRIEF-FACTS.md` §4 |

## 3. The player's state machine (it already exists)

**Owner:** `godot/fighter/fighter.gd`, class `Fighter`. One instance per fighter, with no `.tscn` (`main.gd:53-62`). Bolt is the player, Rivet is driven by `godot/fighter/rivet_brain.gd`.

**States:** `enum S { IDLE, WALK, JAB, CUTLASS, POP, BLOCK, REWIND, HURT, EMPTY, KO, WIN }` (`fighter.gd:19`). `_enter(s)` sets `state`, zeroes `state_t`, and emits `state_changed(fighter, old, new)` only when the state actually changes (`fighter.gd:246-255`).

**Tick:** `main._physics_process` calls `bolt.step(dt)` and `rivet.step(dt)` through `_simulate`, only in FIGHT when not paused, and in KO (`main.gd:143-168, 180-182`). `step` adds `dt` to `state_t` *before* it evaluates the state (`fighter.gd:128-155`).

**Transitions** (from the code):

| From | To | Condition | Where |
|---|---|---|---|
| IDLE, WALK | REWIND | `intent.rewind` held | `fighter.gd:158-160` |
| IDLE, WALK | BLOCK | `intent.block` held | `:161-163` |
| IDLE, WALK | JAB / CUTLASS / POP | that attack just pressed and `wind > 0`; checked in that order; wind is spent on entry | `:164-168` |
| IDLE | WALK | `intent.move ≠ 0` and `wind > 0` | `:169-180` |
| WALK | EMPTY | wind reaches 0 while walking | `:176-178` |
| WALK | IDLE | no move input | `:181-182` |
| JAB, CUTLASS, POP | IDLE (or EMPTY if wind ≤ 0) | `state_t ≥ startup + active + recovery` | `:199-200` |
| BLOCK | IDLE | block released | `:141-143` |
| REWIND | IDLE | rewind released (at full wind it stays, with no clicks) | `:202-207` |
| HURT | IDLE | `state_t ≥ stun` (0.32 s, or 0.80 s if hit while REWIND or EMPTY) | `:146-148, 230` |
| EMPTY | IDLE | `state_t ≥ 1.60 s` | `:149-151` |
| any but KO, WIN | HURT | an unblocked hit (`receive_hit`) | `:217-232` |
| any | KO | `hp ≤ 0` after a hit | `:234-236` |
| any | WIN | `win()`, called by main on the other fighter's KO | `:239-240`; `main.gd:157-159` |
| any | IDLE | `reset()` at round start | `:97-107` |

**What the player can do during an attack:** nothing. `_attack` reads no intent (`fighter.gd:184-200`), and `just_pressed` is not buffered, so a press during an attack is lost. The only things that interrupt an attack are a hit (→ HURT), a KO, hitstop (it freezes `state_t`, §5), and the game's pause flag. What an "interrupt in each phase" does is a brief decision; this is what the code does today.

**Attack table** in seconds (`fighter.gd:41-45`): jab 0.07 / 0.10 / 0.18; cutlass 0.14 / 0.12 / 0.30; pop 0.10 / 0 / 0.35. The live attack box exists only while `startup ≤ state_t < startup + active` (`fighter.gd:117-125`). The hit is checked on the same tick (`:192-198`).

## 4. Measured: the tick each phase starts on

`evidence/a7/probes/probe_phase_ticks.gd`: the real `main.tscn` in FIGHT, Rivet's brain frozen, the key injected with `Input.parse_input_event` (an `InputEventKey` with `physical_keycode`, as `controls.gd` binds). It logs after main's physics step on every tick. Outputs: `probe_phase_ticks_60fps.txt`, `probe_phase_ticks_30fps.txt`.

Counting the tick on which the state becomes JAB as tick 0:

| Attack | Startup | Active (box live) | Recovery | Back to IDLE on | Whole action |
|---|---|---|---|---|---|
| Jab, whiff | ticks 0–4 (5) | ticks 5–10 (6) | ticks 11–20 (10) | tick 21 | 21 ticks = 0.350 s |
| Cutlass, whiff | ticks 0–8 (9) | ticks 9–15 (7) | ticks 16–33 (18) | tick 34 | 34 ticks = 0.567 s |
| Jab that lands on tick 5 | 0–4 | live from tick 5; `state_t` frozen for ticks 6–10 by hitstop, then live again for 5 more | | tick 26 | 26 ticks: **5 ticks longer than a whiff** |

- The seconds in the attack table are not whole ticks (jab startup 0.07 s = 4.2 ticks). The game rounds them up because it compares `state_t ≥ startup` after adding `dt`, so the box opens on the first tick at or past the boundary.
- **The same counts at 30 and 60 fps.** At `--fixed-fps 30` each process frame runs two physics ticks (the `f` column repeats). The press lands one tick later, but the durations are identical.
- **At 30 fps the boundaries fall between drawn frames.** In 30 fps frames, the jab's boundaries sit at 2.5, 5.5 and 10.5, and the cutlass's at 4.5, 8 and 17 (computed: ticks ÷ 2). A 30 fps strip shows every second tick, so whether a boundary tick is drawn depends on the parity of the tick the press landed on.
- Pop was not probed. Its startup, 0.10 s, is exactly 6 ticks, so whether the cork fires on tick 6 or 7 depends on float rounding. Measure it if you use it.

## 5. Clocks, pause and hitstop (what any clip has to agree with)

| Fact | Where |
|---|---|
| Gameplay reads every phase on the **physics tick** (60 Hz) | `main.gd:143-168`; §4 |
| `AnimationPlayer.callback_mode_process` defaults to `ANIMATION_CALLBACK_MODE_PROCESS_IDLE` (1), the process tick; `PHYSICS` is 0 and `MANUAL` is 2. Same default on `AnimationTree` | API probe in `probe_phase_ticks_60fps.txt` |
| `AnimatedSprite2D` has no `callback_mode_process` (probed: `false`); it advances on the process tick | same |
| **Pause is a flag, not a tree pause.** While `main.paused` is set, `step` is not called, so `state_t` and the pose freeze (`main.gd:152-156`). A node under a fighter inherits `PROCESS_MODE_ALWAYS`, so an `AnimationPlayer` there **keeps playing** during pause unless something stops it | `main.gd:22, 41, 134-136` (CLAUDE.md still says 133-135: one line out since the A6 wiring) |
| **Hitstop** freezes both fighters for 5 ticks per landed hit: `step` returns before `_apply_pose`, so `state_t` and the pose stop (`fighter.gd:129-131`; set at `:198` and `:233`). A clip on its own clock keeps going through those ticks | §4, the landing jab |
| INTRO does not call `step` (`main.gd:146-151`); KO does (`:163-165`) | |
| Method tracks are deferred (handout); they cannot make the clocks agree | handout |

## 6. Who writes each fighter node today (the one-authority map)

All writes come from `Fighter._apply_pose()` (`fighter.gd:263-289`), called once per `step` (`:155`) and once in `_ready` (`:82`), i.e. on the physics tick:

| Node | Properties written | Line |
|---|---|---|
| `sprite` (body) | `texture` (one PNG per state), `scale` (×facing), `offset` | `fighter.gd:264-267` |
| `key_sprite` | `position` (from `anchors.json`), `scale` (REWIND spin squash), `visible` (hidden on KO) | `:268-274` |
| `weapon` | `visible`, `texture`, `position`, `offset`, `scale`, `rotation` (cutlass and pop only) | `:275-289` |

Other writers and readers:
- `rewind_tint_driver.gd:21` sets `sprite.material` once, then writes its shader parameter (A5).
- `SteamMount` reads `key_sprite` (A6).
- `debug_capture.gd` and tests only read.
- **Any clip that keys one of these properties adds a second authority over that node,** unless the brief moves the property from `_apply_pose` to the clip.

**Node names are not stable.** The fighters and their sprites are created with `.new()` and never named. The names probe gave Bolt `@Node2D@4` with children `@Sprite2D@5`, `@Sprite2D@6`, `@Sprite2D@7` and `SteamMount`, and Rivet `@Node2D@9` with `@Sprite2D@10…12`. An animation track path names nodes, so a clip cannot point at these until they have fixed names. That is a code change in `fighter.gd`'s presentation, which the brief would have to name.

**Clips are never built in code at runtime** (handout, CLAUDE.md rule to add). Because `Fighter` has no scene, a fighter clip would live as a resource in `godot/animations/` (an `Animation` or `AnimationLibrary` `.tres`). Creating the `AnimationPlayer` node in code and loading that resource is not building the clip at runtime; writing its keys in code is.

## 7. Animation API in 4.7.2 (probed)

| Question | Answer |
|---|---|
| `Animation.step` default | 0.033333 (1/30 s) |
| `Animation.length` default | 1.0 s |
| `Animation.loop_mode` default | `LOOP_NONE` (0); `LOOP_LINEAR` 1, `LOOP_PINGPONG` 2 |
| A new value track's update mode | `UPDATE_CONTINUOUS` (0); `UPDATE_DISCRETE` 1, `UPDATE_CAPTURE` 2 |
| `AnimationTree.advance_expression_base_node` default | `"."`, the AnimationTree node itself. An advance expression that reads the fighter's state would need it pointed at the fighter |
| Godot 3 names | `loop` on Animation: absent. `playback_speed`: absent (`speed_scale` present). `frames` on AnimatedSprite2D: absent (`sprite_frames` present). Class `AnimatedSprite`: does not exist |
| Current clip | `AnimationPlayer.current_animation` exists; `AnimatedSprite2D.animation` exists, and it has no `current_animation` |

A Godot 3 name set in a `.tres` or `.tscn` loads without an error and is ignored. This is the handout's warning; the read-back is what catches it.

## 8. Input path (for the pins)

- The player is read by **polling** in physics: `Input.is_action_just_pressed` / `is_action_pressed` in `main._read_player` (`main.gd:170-178`). Pause, confirm, rematch, mute and F1 go through `_unhandled_input` (`main.gd:125-141`).
- Actions are registered at startup from physical keycodes (`godot/game/controls.gd:5-37`), e.g. jab J, cutlass K, pop L, block I, rewind S.
- **`Input.parse_input_event` reaches the jab:** in the probe, a parsed J press turned IDLE into JAB on the next tick.
- **The existing tests mostly use `Input.action_press`** (`test_slice.gd:5, 33, 93…`; `test_impact_effect_state.gd:6`). That reaches polled actions but never `_input` or `_unhandled_input`, so those tests parse real events only for pause. The handout makes `parse_input_event` the default for A7 pins.

## 9. Art you have, and what is missing

- **Fighter art:** one PNG per state per fighter in `godot/assets/fighters/{bolt,rivet}/`, each a 480×450 canvas at 3× game size, with the feet at (240, 435) (`fighter.gd:260-261`). Per-pose anchors for key, hand, muzzle and weapon angle are in `godot/assets/fighters/anchors.json`. **These are single poses, not frames of a cycle.**
- **Props:** `godot/assets/props/` holds the key (84×60), cork, cutlass and popgun.
- **Provenance:** all game art was generated with SDXL-Turbo, revision `71153311…`, under the Stability AI Non-Commercial licence (`SOURCES.md:12-16`), with every prompt in `ASSET-LOG.md`. The handout says generated sprites follow A2's rules.
- **`raw/sheets/*.png` are review contact sheets** of candidate generations (CHAR-*, PROP-*, `sprites-all.png` 1870×170), not animation cycles. `raw/` is gitignored (`.gitignore:19`).
- **No course sprite set was found on this Mac.** The handout's `<path to course sprites>` and `<course sprite set licence>` are placeholders, so get both from Canvas if you want that route. The other routes the handout allows: any found sheet whose licence allows a public repository and a published film, recorded in ATTRIBUTION.md with the original file committed; a sheet written by committed code; or a generated sheet under A2's rules.
- **No imported 3D rig:** `castle.glb`, `toybox.glb` and `windkey.glb` each instance to a single `MeshInstance3D`, with no `Skeleton3D` and no `AnimationPlayer` (glb probe, 2026-11-19). The imported-rig route would need a new rigged asset in the A3 prop room. The cutout route needs Node2D pivots, or Bone2D under a Skeleton2D, with stable names (§6).

## 10. Existing tests (A6 counts, verified on a fresh clone of `66c8cbc`, A6 wrapper)

| Test | Mode | Result |
|---|---|---|
| `test_slice.gd` | 60 | 25 checks, 0 failed |
| `check_props3d.gd` | 60 | RESULT: PASS (0 failing) |
| `test_rewind_tint.gd` | 30, 60, 144 | 50 checks, 0 failed each |
| `test_materials.gd` | 60 | 55 checks, 0 failed |
| `test_impact_effect_config.gd` | 60 | 136 checks, 0 failed |
| `test_impact_effect_state.gd` | 60 | 44 checks, 0 failed |
| `test_wind_steam_config.gd` | 60 | 33 checks, 0 failed |
| `test_wind_steam_state.gd` | 60 | 37 checks, 0 failed |
| `cost_effects.gd` | 60, timeout 300 | exit 0, 0 setup problems |

The **A7 baseline** is these, re-run through the A7 wrapper once you have committed it. Not yet run.

## 11. What CHANGE-BRIEF.md needs (structure only, from the handout)

1. The two clips. For each: what it communicates and why the player needs it, the object, the route and why, the authority and the script and state or signal it reads, and whether it is the cycle or the committing action.
2. The sheet: source, author, licence, date checked, cell size, grid (hframes × vframes), frame order per clip, and the path of the original file.
3. The cycle spec: frame count, frame rate, loop mode as the Godot 4 constant, and the seam rule for its track type.
4. The phase table: frames at a stated rate, the frame each phase begins on, what the player may do and what the game reads in each phase, and the `Animation.step` you will set.
5. The state machine: states, transitions, the clip each state plays, and the condition for each transition. For an AnimationTree, also its `advance_expression_base_node` and each transition's `advance_mode`.
6. The two clocks: `callback_mode_process` for every AnimationPlayer or AnimationTree, the AnimatedSprite2D note if used, and the tick gameplay reads each keyed fact on.
7. Boundaries.
8. The evidence split: for each rule, read-back, pin, strip or eyes, and how.
9. The frame strip: background, trigger frame, the frames to read, and what each shows, at 30 fps.
10. At least three predicted failures, each with its check.
11. The seven short answers.

## 12. Order of work (from the handout)

1. You: replace the wrapper, commit; Claude: run the baseline through it.
2. You: write and commit CHANGE-BRIEF.md, before any setup prompt.
3. Step 1 (CLAUDE.md): Claude drafts, you commit the draft unedited, then review it and add the Headless-facts lines in a separate commit.
4. Step 2: the pins, committed before Step 5.
5. Steps 3–4: the sprite clip and the rig clip, each with its read-back.
6. Step 5: plan, approve, wire one authority, structure test.
7. Step 6: edges, re-pins, four mutations in worktrees.
8. Step 7: your capture, your first look, then one change at a time.
9. Use It, the film, the docs, tag `a7`, verify from a fresh clone, submit.
