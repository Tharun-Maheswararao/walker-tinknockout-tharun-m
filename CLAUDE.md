# CLAUDE.md — Tin Knockout (Godot 4, GDScript)

## Project context

- **Engine:** Godot 4.7 (`godot/project.godot:15`, `config/features` "4.7");
  the exact build is 4.7.2.stable (`README.md:8`).
- **Renderer:** Forward+ (`godot/project.godot:15`, "Forward Plus"; there is no
  `rendering_method` line). macOS driver is Vulkan (`godot/project.godot:31`).
  `rendering/viewport/hdr_2d` is not set, so it is off (`godot/project.godot:29-32`).
- **Main scene:** `res://game/main.tscn` (`godot/project.godot:14`). It is one
  `Node2D` with `game/main.gd` attached (`godot/game/main.tscn:5-6`); everything
  else is built in code in `main.gd:_ready()` (`godot/game/main.gd:37-88`).
- **How the shaded object is drawn:** each fighter is a `Fighter` (`Node2D`,
  `godot/fighter/fighter.gd:1-2`) created by `main.gd` (`godot/game/main.gd:50-59`;
  Bolt `skin="bolt"`, Rivet `skin="rivet"`). There is no fighter `.tscn`. The body
  is `var sprite: Sprite2D` (`fighter.gd:64`), created in `_ready()`
  (`fighter.gd:72-74`, `centered = false`). Its texture is swapped per state from
  `res://assets/fighters/<skin>/<pose>.png` (`fighter.gd:84-89, 264-265`), scaled
  `ART_SCALE * facing` for the left-facing flip and offset by `-FEET`
  (`fighter.gd:260-261, 266-267`). `key_sprite` and `weapon` are separate
  `Sprite2D` children (`fighter.gd:65-66, 75-80`) and are not the shaded object.
- **Game state that drives the effect:** `godot/fighter/fighter.gd`, `var state`
  (line 50), enum `S.REWIND` (line 19). REWIND is entered at line 159 and left at
  line 204 (key released), 232 (hit → HURT) and 236 (KO). All transitions go
  through `_enter()` (`fighter.gd:246-255`), which emits `state_changed`.
  Simulation runs in `Fighter.step(dt)` (`fighter.gd:128-155`), called from
  `main.gd:_simulate()` (`godot/game/main.gd:161-163`) only while the round is
  FIGHT and not `main.paused`, or during KO (`godot/game/main.gd:133-146`).
  `main.gd` is `PROCESS_MODE_ALWAYS` (`godot/game/main.gd:38`). The rewind input
  is the `rewind` action, S / ↓ / LB (`godot/game/controls.gd:12, 22`), read
  with `Input.is_action_pressed` (`godot/game/main.gd:158`).
- **3D object for the textured shader:** the `toybox` instance in
  `godot/prop_room/prop_room.tscn:42-43` (at x = 2.0), instancing
  `res://assets/props3d/toybox.glb` (`prop_room.tscn:5`). The A5 plan adds a
  second toy-box instance beside it (`CHANGE-BRIEF.md` A5.5).
- **Where its material comes from today:** embedded in the glb, which holds the
  materials `toybox_red`, `toybox_cream`, `toybox_navy`, `toybox_brass`
  (`godot/assets/props3d/toybox.glb` JSON chunk). Its import file has no
  external-material setup yet: `materials/extract=0`, `_subresources={}`
  (`godot/assets/props3d/toybox.glb.import`). The plan replaces slot
  `toybox_red` via "Use External" with `toybox_fresh.tres`, and gives the second
  instance `toybox_worn.tres` as a surface override (`CHANGE-BRIEF.md` A5.5).
- **Textures:** `godot/assets/textures/metal_plate/` (diff, nor_gl, nor_dx, rough
  1k PNGs, plus `ATTRIBUTION.md`). Import settings already match the brief:
  `compress/mode=2`, `mipmaps/generate=true`, `compress/normal_map=1` on both
  normal maps and `=2` on diff and rough (each `*.png.import`, lines 19, 25, 27).
- **Prop-room lighting:** Sun `DirectionalLight3D` with shadows, WorldEnvironment
  with ambient (0.45, 0.5, 0.6) at 0.6, Camera3D at (0, 1.6, 5.5)
  (`godot/prop_room/prop_room.tscn:13-35`).
- **Tests, always through the wrapper, from the repository root**
  (`scripts/run-test.sh:2`, usage `<test-file.gd> <fps>`; it runs
  `timeout 120 godot --headless --path godot --script res://tests/<file>
  --fixed-fps <fps>`, logs to `logs/<name>_<fps>fps.log`, and fails on
  `SHADER ERROR` or `SCRIPT ERROR` in the log, `scripts/run-test.sh:4-9`):

  ```bash
  scripts/run-test.sh test_slice.gd 60       # 2D slice checks; exit code = failures (godot/tests/test_slice.gd:8, 74)
  scripts/run-test.sh check_props3d.gd 60    # A3 props + prop room; read "RESULT: PASS (0 failing)" (godot/tests/check_props3d.gd:101-102)
  ```

  For the R2 timing rule, run the same test file at 30, 60 and 144
  (`CHANGE-BRIEF.md` A5.2 R2), e.g. `scripts/run-test.sh <file>.gd 30`.
  `timeout` comes from Homebrew coreutils (`README.md:88`). The 3D check expects
  an import first: `godot --headless --path godot --import` (`README.md:90`).
  Tests drive input through the real input path (`Input.action_press`,
  `Input.parse_input_event`, `godot/tests/test_slice.gd:5-7, 32-45`).

## Current change

@CHANGE-BRIEF.md

## Ownership

- Files in `godot/shaders/` are hand-written by the human and are never edited
  by an agent. Do not create, edit, rename, reformat or "fix" them, even to make
  a test pass; report the problem instead.

## Out of scope

This change adds a REWIND tint driven from code and a textured toy-box material.
It must not touch:

- Gameplay: the fighter state machine, its timings and transitions, movement,
  wind/health numbers, hit and hurt boxes (`fighter.gd:25-45, 112-255`).
- Input: `godot/game/controls.gd` and how `main.gd` reads it.
- Round flow, pause and mute logic in `main.gd`, beyond attaching materials or
  a driver. The driver only reads `fighter.state`; it never writes game state.
- Audio (`godot/audio/`), music behaviour, HUD (`godot/ui/`), camera shake/roll,
  sparks.
- Any sprite other than the two fighter body sprites: not the key, weapon, cork,
  background or HUD.
- A single material shared by both fighters: each body sprite gets its own
  ShaderMaterial (R6).
- Existing test expectations in `godot/tests/test_slice.gd` and
  `godot/tests/check_props3d.gd`. New tests may be added; old ones are not
  loosened.
- The A3 props: the `.glb` geometry, the `.blend` sources, castle and windkey,
  the toy box's cream/navy/brass slots, and the prop room's floor, Sun,
  WorldEnvironment and camera.
- `project.godot` settings (renderer, HDR 2D, viewport, autoloads) and the
  texture import settings, which are already set.
- The `metal_plate_nor_dx_1k.png` file is calibration only and is not bound to
  any material.

## Unconfirmed

- `godot/shaders/` does not exist yet, and neither does `rewind_tint.gdshader`
  or the textured shader's file name (the brief does not name it).
- `godot/prop_room/materials/` does not exist yet.
- Where the tint driver will live (a new script, `main.gd`, or `fighter.gd`) is
  not decided in any file I read.
- No A5 test file exists yet in `godot/tests/`; its name is unknown.
- The engine version on this machine: I did not run `godot --version`; 4.7.2 is
  from `README.md:8` only.
- `check_props3d.gd:78` prints `albedo_color` only for `BaseMaterial3D`; with a
  ShaderMaterial on `toybox_red` it will print `#000000` for that surface. It
  does not assert on colour, so it should still pass, but I have not run it.
- `README.md:46` and `README.md:93` give raw `godot` commands; use
  `scripts/run-test.sh` instead. I did not run either test.
