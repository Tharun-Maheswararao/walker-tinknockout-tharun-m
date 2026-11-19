# CLAUDE.md — Tin Knockout (Godot 4, GDScript)

## Project context

- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf (`godot --version`, `evidence/a5/headless-facts.txt:1`); `config/features` "4.7" (`godot/project.godot:15`).
- **Renderer:** Forward+ (`godot/project.godot:15`, "Forward Plus"). macOS driver Vulkan (`godot/project.godot:31`). Viewport 640×360, window 1280×720, stretch `canvas_items` (`godot/project.godot:23-27`).
- **Main scene:** `res://game/main.tscn` (`godot/project.godot:14`), one `Node2D` running `game/main.gd`; everything else, both fighters included, is built in code in `main.gd:_ready()` (`godot/game/main.gd:40-107`). Main is `PROCESS_MODE_ALWAYS` (`main.gd:41`); the fighters inherit it.
- **Pause** is a game flag, not a tree pause: `var paused` (`main.gd:22`), toggled at `main.gd:134-136`; while it is set, FIGHT skips `_simulate` (`main.gd:152-156`). `get_tree().paused` is never set.
- **The player's state machine** is `Fighter` in `godot/fighter/fighter.gd`, one per fighter, no `.tscn` (`main.gd:53-62`). States `enum S` (`fighter.gd:19`); `step(dt)` adds `dt` to `state_t`, then runs the state (`fighter.gd:128-155`); `_enter(s)` zeroes `state_t` and emits `state_changed` only on a change (`fighter.gd:246-255`). Attack phases in seconds (`fighter.gd:41-45`); the attack box is live while `startup <= state_t < startup + active` (`fighter.gd:117-125`). Hitstop returns from `step` before anything else (`fighter.gd:129-131`).
- **Clock:** `main._physics_process` (`main.gd:143-168`) calls `step` for both fighters through `_simulate` (`main.gd:180-182`), at 60 ticks per second under any `--fixed-fps` (`evidence/a7/probes/probe_phase_ticks_60fps.txt`, `_30fps.txt`). Measured: jab 5 / 6 / 10 ticks, back to IDLE on tick 21; a landed hit adds 5 hitstop ticks (same files; `design/a7/BRIEF-FACTS.md` §4).
- **Presentation today:** `Fighter._apply_pose()` (`fighter.gd:263-289`), called from `step` (`:155`) and `_ready` (`:82`), writes the body `sprite`, `key_sprite` and `weapon`, which `_ready` creates unnamed (`fighter.gd:71-80`; names like `@Sprite2D@5`, `design/a7/BRIEF-FACTS.md` §6). No `AnimationPlayer`, `AnimationTree` or `AnimatedSprite2D` exists yet (`design/a7/BRIEF-FACTS.md` §1).
- **Clip A, `wind_key_cycle` (the cycle)** (`CHANGE-BRIEF.md` §1–3): route **Sprite2D + AnimationPlayer frame track**. Node `key_sprite` (`Sprite2D`, `hframes` 8) at `Fighter/FacingPivot/BodyPivot/KeyMount/KeyBob/key_sprite`; player `KeyAnimPlayer`; clip `godot/animations/wind_key_cycle.tres`; plays in REWIND below wind 100. Sheets from `godot/tools/generate_key_sheets.gd` (`CHANGE-BRIEF.md` §2). All planned; none exists yet.
- **Clip B, `jab_action` (the committing action)** (`CHANGE-BRIEF.md` §1, §4): route **cutout rig keyed as resource text**. Nodes `BodyPivot` and `KeyBob` (`Node2D`); player `FighterAnimPlayer`; clip `godot/animations/jab_action.tres`; plays in JAB, at 60 fps with `step` 1/60. Planned; none exists yet.
- **Clock for both clips:** `callback_mode_process` MANUAL, clip position equal to `state_t` after every `step` (`CHANGE-BRIEF.md` §6).
- **Scenes the clips appear in:** the game, `res://game/main.tscn` (fighters built in code, above), and the fixture `godot/previews/jab_preview.tscn` (planned, `CHANGE-BRIEF.md` §9).
- **A6 effects still live:** impact bursts `godot/effects/impact_effect.tscn` / `_blocked.tscn`, spawned by `main._spawn_impact` (`main.gd:228-238`); wind steam `godot/effects/wind_steam.tscn` on a `SteamMount` per fighter (`main.gd:69-70`), which copies `key_sprite`'s local position, the facing scale and `visible` every physics tick (`godot/effects/steam_mount.gd:28-35`). The A5 tint driver sets each body `sprite.material` (`godot/fighter/rewind_tint_driver.gd:21`, attached `main.gd:71-74`).
- **Tests, always through the wrapper, from the repository root** (`scripts/run-test.sh:2`: `<test-file.gd> <fps|realtime> [timeout-seconds]`). A number runs headless with `--fixed-fps <n>`, log `logs/<name>_<n>fps.log`; `realtime` runs without `--fixed-fps`, log `logs/<name>_realtime.log` (`scripts/run-test.sh:5-11`). Timeout defaults to 120 s (`:11`). Exits 1 if the log contains `SHADER ERROR`, `SCRIPT ERROR` or `Failed loading resource` (`:13`). Run `godot --headless --path godot --import` once after cloning (`README.md:120`).

  ```bash
  ./scripts/run-test.sh test_slice.gd 60                  # "N checks, N failed" (godot/tests/test_slice.gd:73)
  ./scripts/run-test.sh check_props3d.gd 60               # "RESULT: PASS (0 failing)" (godot/tests/check_props3d.gd:101)
  ./scripts/run-test.sh test_rewind_tint.gd 30            # also 60 and 144 (godot/tests/test_rewind_tint.gd:158)
  ./scripts/run-test.sh test_materials.gd 60              # (godot/tests/test_materials.gd:42)
  ./scripts/run-test.sh test_impact_effect_config.gd 60   # (godot/tests/test_impact_effect_config.gd:145)
  ./scripts/run-test.sh test_impact_effect_state.gd 60    # (godot/tests/test_impact_effect_state.gd:113)
  ./scripts/run-test.sh test_wind_steam_config.gd 60      # (godot/tests/test_wind_steam_config.gd:92)
  ./scripts/run-test.sh test_wind_steam_state.gd 60       # (godot/tests/test_wind_steam_state.gd:172)
  ./scripts/run-test.sh cost_effects.gd 60 300            # "cost_effects done, N setup problems" (godot/tests/cost_effects.gd:171)
  ./scripts/run-test.sh <new_test>.gd realtime            # only for a test that waits on audio; no current test does
  ```

  These modes match `README.md:120-137, 189-203`. Baseline counts at the A7 wrapper: `evidence/a7/baseline/SUMMARY.txt`. A test file name that does not exist still exits 0 ("Can't load script" matches none of the patterns): read the count line, not only the exit code.

## Headless facts (measured on this Mac: `evidence/a5/headless-facts.txt`)

- A headless run draws nothing, yet still reports `vulkan` / `forward_plus` (line 3); no headless test can judge a colour.
- A shader that fails to parse prints `SHADER ERROR` and returns an empty `get_shader_uniform_list()` (lines 6-7).
- `set_shader_parameter` raises no error for an undeclared name and reads back whatever was set (lines 9-10): a readback proves nothing about the shader.
- Physics runs at 60 ticks per game second under any `--fixed-fps` (lines 12, 23). At `--fixed-fps 30` each process frame runs two ticks (`evidence/a7/probes/probe_phase_ticks_30fps.txt`).
- A headless run uses a dummy renderer: no particles are drawn or simulated. Node state is observable; the look is not.
- Capture with `--disable-vsync --always-on-top` as well as `--fixed-fps`. Without them, Movie Maker on this Mac sometimes writes copies of an earlier frame: the summary reports fewer frames than `--quit-after`. Check the summary line says the full count (2026-11-08).

## Current change

@CHANGE-BRIEF.md

## Ownership

- Files in `godot/shaders/` are hand-written by the human and are never edited by an agent. Do not create, edit, rename, reformat or "fix" them, even to make a test pass; report the problem instead.
- `scripts/run-test.sh` is the handout's wrapper; agents never edit it (`git diff scripts/run-test.sh` is checked after every session).
- Clips live as resources in `godot/animations/` (or in the scene that owns them) and are never built in code at runtime. Code may create an `AnimationPlayer`, load a clip resource into it, play, stop and seek; it never adds tracks or keys. A clip-baking tool script that saves a `.tres` with `ResourceSaver.save()` is allowed and committed.
- Effect settings live in scene files in `godot/effects/`, not in code.

## One authority

Exactly one node writes to each animated node. Never add a second writer to a node that already has one; if the brief's authority conflicts with something in the code, say so and stop. Per `CHANGE-BRIEF.md` §1 and §7:

| Node | The one writer | What it writes |
|---|---|---|
| `FacingPivot` | `Fighter._apply_pose()` | `scale.x` = `facing` |
| `BodyPivot` | `FighterAnimPlayer` (`jab_action`) | `position:x`, `rotation` |
| `sprite` (body) | `Fighter._apply_pose()` | `texture`, `scale` (no facing), `offset` (no facing); `material` is set once by the A5 tint driver, and no clip keys this node |
| `KeyMount` | `Fighter._apply_pose()` | `position` (anchor, no facing), `visible` (false on KO) |
| `KeyBob` | `FighterAnimPlayer` (`jab_action`) | `position:y` |
| `key_sprite` | `KeyAnimPlayer` (`wind_key_cycle`) | `frame`; nothing writes its `scale` any more |
| `weapon` | `Fighter._apply_pose()` | as today (`fighter.gd:275-289`) |

`SteamMount` only reads the key. Rest pose on entry to any state but JAB is the clip owner's job (snap to rest), not `_apply_pose`'s.

## Godot 4 names

- Use Godot 4 names for 4.7.2, never Godot 3 names. Probed in 4.7.2 (`design/a7/BRIEF-FACTS.md` §7): `Animation.loop_mode` (`LOOP_NONE` / `LOOP_LINEAR` / `LOOP_PINGPONG`), not a boolean `loop`; `AnimationPlayer.speed_scale`, not `playback_speed`; `AnimatedSprite2D` with `sprite_frames`, not `AnimatedSprite` / `frames`. The current clip is `AnimationPlayer.current_animation` (and `AnimatedSprite2D.animation`).
- `callback_mode_process` constants live on `AnimationMixer`: `ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS` 0, `_IDLE` 1 (the default), `_MANUAL` 2. `Animation.step` defaults to 1/30 s; a new value track defaults to `UPDATE_CONTINUOUS` (same probe).
- Particles (A6): `ParticleProcessMaterial`, `initial_velocity_min` / `_max`, `scale_min` / `_max`.
- If you are unsure a property exists in this version, say so instead of guessing, or check it with `ClassDB` / `in` in a headless script and report the result.

## Out of scope

This change adds two clips as presentation. It must not touch (`CHANGE-BRIEF.md` §7):

- Gameplay in `fighter.gd`: the state machine, its transitions and timings, movement, wind and health numbers, attacks, hit and hurt boxes, hitstop. Presentation may read `state`, `state_t`, `wind` and `facing`; it never writes game state. The only `fighter.gd` edits are `_ready` (named nodes and the hierarchy), `_apply_pose`, and the clip sync at the end of `step`.
- Input (`godot/game/controls.gd`), round flow, pause and mute logic, body separation (`main.gd:184-190`).
- The A5 shaders and tint; the A6 effects, except that `SteamMount` follows `KeyMount` (`godot/effects/steam_mount.gd`).
- Existing tests and their expectations, except the four assertions the brief names (`test_wind_steam_state.gd:149, 159`; `test_slice.gd:182, 187`), changed in their own commit after the wiring. New tests are added; old ones are not loosened.
- `godot/shaders/`, `godot/project.godot`, the A3 props and prop room, existing texture files and their import settings, and the source key PNGs.

## Unconfirmed

- None of the A7 nodes, players, clips, sheets or the preview exist yet; the paths above are the brief's plan, and `fighter.gd` line numbers will move when they are added.
- The brief does not say who sets `key_sprite.texture` and `hframes` at setup (one write in `_ready` / `_load_art`), nor whether `weapon` moves under `FacingPivot` or stays a direct child of `Fighter`.
- The brief does not give `BodyPivot`'s origin. At (0, 0) it pivots at the feet (`fighter.gd:261`), so the lean rotates about the feet.
- How the clip is held at `state_t` (`seek(state_t, true)` or another call) is not fixed by the brief; only the invariant is (`CHANGE-BRIEF.md` §6).
- Whether `key_sprite` (`z_index` −1, `fighter.gd:76`) still draws behind the body once it sits under `BodyPivot` is a strip or eyes check.
- No new A7 test file names are fixed by the brief.
