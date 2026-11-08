# CLAUDE.md — Tin Knockout (Godot 4, GDScript)

## Project context

- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf (`godot --version`, `evidence/a5/headless-facts.txt:1`); `config/features` "4.7" (`godot/project.godot:15`).
- **Renderer:** Forward+ (`godot/project.godot:15`, "Forward Plus"; there is no `rendering_method` line). macOS driver is Vulkan (`godot/project.godot:31`). Viewport 640×360, window 1280×720, stretch `canvas_items` (`godot/project.godot:23-27`).
- **Main scene:** `res://game/main.tscn` (`godot/project.godot:14`), one `Node2D` running `game/main.gd`; everything else is built in code in `main.gd:_ready()` (`godot/game/main.gd:37-96`). Main is `PROCESS_MODE_ALWAYS` (`main.gd:38`), so its children inherit it.
- **Pause** is a game flag, not a tree pause: `var paused` (`main.gd:19`), toggled at `main.gd:123-125`; the fight loop skips simulation while it is set (`main.gd:141-142`). `get_tree().paused` is never set.
- **Effect A, impact burst** (`CHANGE-BRIEF.md` A): `GPUParticles2D` emitters (Shards and Core) in `godot/effects/impact_effect.tscn`, plus `godot/effects/impact_effect_blocked.tscn` for blocked hits. Neither exists yet.
  - Event: melee hits, `Fighter.hit_landed(attacker, attack, blocked)` (declared `godot/fighter/fighter.gd:14`, emitted `:197`), connected to `_on_hit` (`main.gd:60, 202-204`); cork hits, `Cork.struck(cork, blocked)` (declared `godot/fighter/cork.gd:11`, emitted `:24`; the cork frees itself at `:25`), connected at `main.gd:199`.
  - Both arrive at `main._on_impact(p)` (`main.gd:206-210`), which today drops `blocked` (`main.gd:199, 202`) and draws the kept star spark (`main.gd:207, 221-228`) on the `fx` node at `z_index` 5 (`main.gd:87-90`).
  - Bursts are instanced per impact as children of Main (overlap), freed on `finished` (`CHANGE-BRIEF.md` A-R3, A-R4).
- **Effect B, wind steam** (`CHANGE-BRIEF.md` B): `GPUParticles2D` in `godot/effects/wind_steam.tscn` (not yet created), one per fighter, parented to that fighter's `key_sprite` (`fighter.gd:65, 75-77`).
  - Value: `Fighter.wind`, 0–100 (`fighter.gd:27, 49`), announced by `wind_changed(fighter, wind)` (declared `fighter.gd:17`, emitted `:107, 212, 244`). It drains on walking and attacks (`fighter.gd:29, 41-43, 242-244`) and rises 10 per rewind click (`fighter.gd:31, 211-213`).
  - `key_sprite` is scaled `ART_SCALE` = 1/3 × facing, pulses in x during REWIND, has `z_index` −1, and is hidden on KO (`fighter.gd:76, 260, 269-274`).
  - The existing low-wind listener is the music, Bolt only (`main.gd:83-85`, `LOW_WIND` 25 at `main.gd:15`).
- **Fighters:** two `Fighter` nodes (no `.tscn`), created and connected in `main.gd:50-64`. The A5 tint driver is attached per fighter at `main.gd:61-64` (`godot/fighter/rewind_tint_driver.gd`); the F9 capture key at `main.gd:65-68` (`godot/game/debug_capture.gd`).
- **Tests, always through the wrapper, from the repository root** (`scripts/run-test.sh:2`: `<test-file.gd> <fps|realtime> [timeout-seconds]`). A number runs headless with `--fixed-fps <n>` and logs to `logs/<name>_<n>fps.log`; `realtime` runs without `--fixed-fps` and logs to `logs/<name>_realtime.log` (`scripts/run-test.sh:5-11`). The timeout defaults to 120 s (`:11`). It exits 1 if the log contains `SHADER ERROR` or `SCRIPT ERROR` (`:13`). Run `godot --headless --path godot --import` once after cloning (`README.md:118`).

  ```bash
  ./scripts/run-test.sh test_slice.gd 60          # "N checks, N failed" (godot/tests/test_slice.gd:73)
  ./scripts/run-test.sh check_props3d.gd 60       # "RESULT: PASS (0 failing)" (godot/tests/check_props3d.gd:101)
  ./scripts/run-test.sh test_rewind_tint.gd 30    # also 60 and 144 (godot/tests/test_rewind_tint.gd:158)
  ./scripts/run-test.sh test_materials.gd 60      # (godot/tests/test_materials.gd:42)
  ./scripts/run-test.sh <new_test>.gd realtime    # only for a test that waits on audio
  ```

  These modes match `README.md:120-135`. A test file name that does not exist still exits 0 ("Can't load script" matches neither pattern; `design/a6/BRIEF-FACTS.md` §7): read the count line, not only the exit code.

## Headless facts (measured on this Mac: `evidence/a5/headless-facts.txt`)

- A headless run draws nothing, yet still reports `vulkan` / `forward_plus` (line 3); no headless test can judge a colour.
- A shader that fails to parse prints `SHADER ERROR` and returns an empty `get_shader_uniform_list()` (lines 6-7). Listed types: float = 3, `vec4 : source_color` = 20 (line 4).
- Defaults are not reported (`shader_get_parameter_default` is null, line 5): read them from the `.gdshader` text.
- `set_shader_parameter` raises no error for an undeclared name and reads back whatever was set, even 2.0 on `hint_range(0, 1)` (lines 9-10): a readback proves nothing about the shader.
- Physics runs at 60 ticks per game second under any `--fixed-fps` (lines 12, 23). REWIND starts and stops in physics, so at 144 fps a `_process` driver sees it up to 1/60 s late.

## Current change

@CHANGE-BRIEF.md

## Ownership

- Files in `godot/shaders/` are hand-written by the human and are never edited by an agent. Do not create, edit, rename, reformat or "fix" them, even to make a test pass; report the problem instead. (`particles_generated.gdshader` is saved there by the human from the editor.)
- `scripts/run-test.sh` is the handout's wrapper; agents never edit it (`git diff scripts/run-test.sh` is checked after every session).
- Effect settings live in scene files in `godot/effects/`, not in code. Code may instance a scene, start it, and set `amount_ratio`; it does not set emission, process or draw values.

## Godot 4 names

- Use Godot 4 class and property names for 4.7.2, never Godot 3 names: `ParticleProcessMaterial`, not `ParticlesMaterial`; `initial_velocity_min` / `initial_velocity_max`, not `initial_velocity`; `scale_min` / `scale_max`, not `scale` / `scale_random`.
- If you are unsure a property exists in this version, say so instead of guessing, or check it with `ClassDB` / `in` in a headless script and report the result.
- Facts already probed in 4.7.2 (`design/a6/BRIEF-FACTS.md` §5; `CHANGE-BRIEF.md` A.3–A.4, E):
  - `gravity` and `direction` are `Vector3`; +y is down in 2D. `spread` is a half-angle.
  - A `Curve`'s `max_value` defaults to 1.0 and silently clamps higher points; set it when a curve peaks above 1.
  - `amount_ratio` exists on `GPUParticles2D`, not `CPUParticles2D`. `lifetime_randomness` is on the process material. `GradientTexture2D` defaults to 64×64.
  - A one-shot burst started with `restart()` after it is in the tree emits `finished`; one set `emitting = true` before its first frame did not.

## Out of scope

This change adds two particle effects as presentation. It must not touch:

- Gameplay in `godot/fighter/fighter.gd`: the state machine and its timings, movement, wind and health numbers, attacks, hit and hurt boxes. Presentation may read `wind`, `state` and `key_sprite`; it never writes game state.
- Input (`godot/game/controls.gd`), round flow, pause and mute logic in `main.gd`. Allowed in `main.gd`: passing `blocked` through `_on_hit` and the `struck` handler to `_on_impact`, spawning the effect scenes there, and attaching and driving Effect B (`CHANGE-BRIEF.md` C).
- The star spark, camera shake and roll, hitstop, audio, music and HUD.
- Existing tests and their expectations (`godot/tests/`); new tests are added, old ones are not loosened.
- `godot/shaders/`, `godot/project.godot`, the A3 props and prop room, and existing texture files and their import settings.

## Unconfirmed

- None of `godot/effects/`, `godot/previews/`, `tools/generate_shard_texture.gd` or `tools/generate_steam_texture.gd` exists yet.
- Where Effect B's driver lives (in `main.gd` or a new script) is left open by `CHANGE-BRIEF.md` C.
- The brief cites `main.gd:200` for the cork's `struck` handler; the handler is at `main.gd:199`.
- No new test file names are fixed by the brief; the handout's pattern is `godot/tests/test_<effect>_config.gd`.
- Whether a hidden `GPUParticles2D` keeps simulating, and what shows when it reappears, is not observable headlessly; it is a strip or eyes check (`CHANGE-BRIEF.md` B-R5).
