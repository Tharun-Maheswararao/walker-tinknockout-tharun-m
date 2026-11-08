# A6 brief facts (not the brief)

*Collected by Claude on 2026-10-29 from this repository, the installed Godot 4.7.2 and the Godot docs; re-checked against the code at tag `a5` on 2026-11-07 (line numbers, starting state, baseline, free keys). It contains facts only. Every effect choice, value, intent, prediction and budget in CHANGE-BRIEF.md is yours to make.*

## 1. Starting state (2026-11-07, after A5)

- Tags `a2`, `a3` and `a5` (`f4dda68`). There is no `a4` tag.
- `CLAUDE.md` exists (A5 version, 114 lines). It imports `@CHANGE-BRIEF.md`, has a "Headless facts" block, and its Ownership section protects `godot/shaders/` and `scripts/run-test.sh`. There is no `AGENTS.md`. So the handout's Step 1 prompt applies as written: **revise** CLAUDE.md.
- `CHANGE-BRIEF.md` holds the A2, A3 and A5 briefs one after another. The handout says to **replace** its contents with the A6 brief; the A5 version stays in history at tag `a5`.
- `godot/shaders/` holds A5's hand-written `rewind_tint.gdshader`, `painted_tin.gdshader`, `hint_experiment.gdshader` and the generated `standard_generated.gdshader`. `git diff --stat godot/shaders/` must print nothing after every A6 agent session. Step 6 adds `particles_generated.gdshader`, saved by you from the editor.
- `scripts/run-test.sh` is the A6 wrapper again (commit `8731c5c`; A5 had swapped in its own at `23a0363`).
- The A5 REWIND tint is live: `godot/fighter/rewind_tint_driver.gd`, attached per fighter in `main.gd:61`. An Effect B on REWIND would sit on top of a sprite that is already tinting blue.
- **Renderer switched from GL Compatibility to Forward+ on 2026-10-29, before the brief** (your decision; Claude made the edit).
  - Reason: Godot's docs say the Visual Profiler is not supported with Compatibility on macOS, so the GPU price was impossible on this Mac.
  - Evidence: `evidence/a6/renderer-switch/`. The 2D game's still frames are identical under both renderers (max difference 1/255). The A3 3D prop room renders darker under Forward+.
- **macOS driver set to Vulkan on 2026-10-29** (your decision; Claude made the edit).
  - Reason: under Forward+ on Metal, your Visual Profiler showed GPU 0.0 ms on every row, and Claude's probe read 0 ms too. Under Vulkan the probe reads about 0.55 ms per frame.
  - Frames are pixel-identical between Metal and Vulkan. Evidence: `evidence/a6/renderer-switch/gpu-driver.txt`.

## 2. Engine and project

| Fact | Where |
|---|---|
| Godot 4.7.2.stable.official.ed1daf0bf, at `/opt/homebrew/bin/godot` | `godot --version` |
| Renderer Forward+: `config/features` says "Forward Plus". The editor drops `rendering_method="forward_plus"` because it is the default. | `godot/project.godot:15` |
| Driver on macOS: Vulkan (MoltenVK), adapter "Apple M4" | `godot/project.godot:31` (`rendering_device/driver.macos="vulkan"`); `evidence/a6/renderer-switch/gpu-driver.txt` |
| Vsync: enabled (default mode 1; the project does not override it) | ProjectSettings default |
| Viewport 640×360, window 1280×720 (2×), stretch `canvas_items` | `godot/project.godot:23-27` |
| Camera2D at (320, 180), zoom 1 | `godot/game/main.gd:39-41` |
| Background `res://assets/env/bowl.png` (768×432), scaled to 640×360, z −10 | `godot/game/main.gd:42-47` |
| Floor y = 292; arena x = 132–500 | `godot/game/main.gd:12-13` |
| Fighter hurtbox 50×106 px, bottom-centred on the feet (about 29 % of screen height) | `godot/fighter/fighter.gd:38` |
| Main scene is a bare root; everything is built in `main.gd` | `godot/game/main.tscn` |

## 3. Events and conditions you could drive effects from

| Signal or value | Declared | Emitted or held |
|---|---|---|
| `Fighter.hit_landed(attacker, attack, blocked)` | `fighter.gd:14` | `fighter.gd:197` |
| `Cork.struck(cork, blocked)` | `cork.gd:11` | `cork.gd:24`; **the cork frees itself on the same frame** (`cork.gd:25`) |
| `Fighter.wind_changed(fighter, wind)`, wind 0–100 (`MAX_WIND`) | `fighter.gd:17` | `fighter.gd:107, 212, 244` |
| `Fighter.rewind_tick(fighter)`, one per 10 wind | `fighter.gd:16` | `fighter.gd:213` |
| `Fighter.state_changed(fighter, old, new)`, edge-triggered | `fighter.gd:13` | `fighter.gd:255` |
| `Fighter.projectile_fired(fighter)` | `fighter.gd:15` | `fighter.gd:189` |
| `Main.round_changed(state)` (TITLE, INTRO, FIGHT, KO) | `main.gd:9` | `main.gd:112` |
| `Main.LOW_WIND = 25.0` (music slows below it) | `main.gd:15` | |

Existing hit feedback:
- Hand-drawn star "sparks", 0.14 s, at the impact point (`main.gd:206-207`, drawn in `main.gd:221-228`).
- Melee hits use the centre of the attacker's attack box (`main.gd:202-204`); cork hits use the cork's position, read in the `struck` handler before the cork frees itself (`main.gd:199`; corrected from 200 on 2026-11-08).
- Camera shake lasts 0.15 s (`main.gd:208`), and hitstop is 0.07 s (`fighter.gd:37`).
- Your boundaries section has to say whether Effect A replaces the sparks or sits beside them. Removing them changes `main.gd`.

**Pause is a game flag, not a tree pause.**
- Esc/P toggles `main.paused` (`main.gd:123-125`), and the fight loop skips simulation while it is set (`main.gd:141-142`).
- `get_tree().paused` is never set.
- `Main` runs with `PROCESS_MODE_ALWAYS` (`main.gd:38`), so particles under it inherit that and keep simulating during the game's pause unless something stops them.
- Your brief's pause rule has to say which pause it means.

## 4. Background contrast (measured, not judged)

Rec. 709 luminance of `bowl.png` scaled to 640×360, 0–255, in the band where hits land (y 186–292):

| x range | mean | min | max |
|---|---|---|---|
| 128–159 | 115 | 38 | 219 |
| 160–191 | 121 | 45 | 229 |
| **192–223 (lightest)** | **160** | 91 | 238 |
| 224–255 | 136 | 52 | 254 |
| **256–287 (darkest)** | **98** | 49 | 253 |
| 288–319 | 107 | 46 | 199 |
| 320–511 | 111–126 | 59–75 | 193–225 |

- Upper water (y 20–186): mean 93.
- Sand floor (y 292–360): mean 131.
- README limitation 5 already notes low contrast against the pink castle near Bolt's start.
- This is a number, not your eyes. The human check over the darkest and lightest stretches is still required.

## 5. Particle API in 4.7.2 (probed with ClassDB)

| | GPUParticles2D | CPUParticles2D |
|---|---|---|
| `amount_ratio` | yes | **no** (use `speed_scale` or another parameter for a feedback loop) |
| `use_fixed_seed`, `seed` | yes | yes |
| `visibility_rect` | yes, default `Rect2(-100, -100, 200, 200)` | n/a |
| `trail_enabled` | yes (supported in Forward+; it was not in Compatibility) | no |
| `sub_emitter` | yes | no |
| `restart(keep_seed)` | yes | yes |
| Process settings live on | `process_material` (ParticleProcessMaterial) | the node itself (`scale_amount_min`, not `scale_min`) |

- `ParticlesMaterial` does not exist (`ClassDB.class_exists` returns false).
- **Godot 3 names in 4.7.2.** `ParticleProcessMaterial` has editor-only Vector2 properties named `initial_velocity`, `scale`, `angle`, `damping` and `hue_variation`, each holding (min, max). They are not stored in files.
  - `set("initial_velocity", 120.0)` leaves min and max at 0, silently.
  - `set("initial_velocity", Vector2(30, 90))` sets min = 30 and max = 90.
  - So a scene file line in the float form drops the value. The Vector2 form would actually work. Check this yourself in the Step 2 mutation.
- `GPUParticlesAttractor2D` and `GPUParticlesCollision2D` do not exist. Attractors are 3D only, and 2D collision goes through `LightOccluder2D`.
- `CanvasItemMaterial` has `blend_mode`, `particles_animation`, `particles_anim_h_frames`, `particles_anim_v_frames` and `particles_anim_loop`.

## 6. Renderer limits (Godot docs)

The project now runs Forward+, so these Compatibility limits no longer apply. They are kept here because they are why the renderer changed.

- **Particle trails** and **particle SDF collision** are "Not supported" in Compatibility. They are supported in Forward+. Source: the [renderer comparison](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html).
- **`emit_particle()`** is only supported on Forward+ and Mobile ([GPUParticles2D](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html)), so it is now available.
- **Visual Profiler:** "not supported when using the Compatibility renderer on macOS" ([debugger panel docs](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html)). The same page says it otherwise works with any renderer.
  - On this Mac, Forward+ on **Metal** gives a GPU column of all zeros. Forward+ on **Vulkan** gives real GPU times, but so far only through Claude's probe.
  - **Confirmed by Tharun on 2026-11-08** in the editor (Forward+, Vulkan 1.2.334, Apple M4), with the game running a fight before any A6 effect existed. The GPU column is non-zero: Render Viewport 0.97 ms GPU / 0.11 ms CPU, Prepare Render 0.06 ms GPU. Screenshot: `evidence/a6/visual-profiler-vulkan.webp`.
- Turbulence and sub-emitters: no renderer restriction found in the docs. Confirm them on screen like every other feature.

## 7. Instruments and environment

- `timeout` is installed (`/opt/homebrew/bin/timeout`), so `scripts/run-test.sh` works on macOS.
- The game binds A, D, ←, →, J, K, L, I, ↑, S, ↓, Esc, P, Enter, Space, R, M, N and F1 (`godot/game/controls.gd:6-18`). **F9 is taken** since A5: it is the debug-build capture key (`godot/game/debug_capture.gd:18`, `README.md:116`). F10, F11 and F12 are unbound in the game's code; pick one for the vsync debug key and name it in the README.
- Example 09 (the chapter's cost script) is still not on this machine (searched `csye7270/` on 2026-11-07). `prompts/prompt-7.txt` has a placeholder for its path.
- **Wrapper caveat (found 2026-11-07):** if the test file name doesn't exist, `scripts/run-test.sh` exits 0. Godot prints "Can't load script", which matches neither `SCRIPT ERROR` nor `SHADER ERROR`. Read the count line, not just the exit code. Also, in zsh an unquoted `$var` holding "file.gd 60" is passed as one argument; Claude's first baseline loop hit exactly this.

## 8. Baseline (2026-11-07, at `a5` plus the A6 wrapper, before any A6 change)

Claude ran these through the A6 wrapper (`8731c5c`), each in the mode the A5 README gives (`README.md:120-135`):

| Test | Mode | Result | Log |
|---|---|---|---|
| `test_slice.gd` | 60 | 25 checks, 0 failed, exit 0 | `logs/test_slice_60fps.log` |
| `check_props3d.gd` | 60 | 23 PASS, `RESULT: PASS (0 failing)`, exit 0 | `logs/check_props3d_60fps.log` |
| `test_rewind_tint.gd` | 30 / 60 / 144 | 50 checks, 0 failed, exit 0, at each rate | `logs/test_rewind_tint_{30,60,144}fps.log` |
| `test_materials.gd` | 60 | 55 checks, 0 failed, exit 0 | `logs/test_materials_60fps.log` |

- No log contains `SCRIPT ERROR` or `SHADER ERROR`. They end with Godot's usual "resources still in use at exit" lines; `check_props3d` and `test_materials` also print `Parameter "material" is null`, which already appeared at A5 (`evidence/a5/mutations/m3-source_color_test_materials_60fps.log:72`).
- These are the counts your TEST-REPORT "before" column needs. Run them again yourself after the A6 work.
- The 2026-10-29 baseline (before A5) was `test_slice` 25/25 realtime and `check_props3d` 23/23 at 60, under both renderers.

## 9. What CHANGE-BRIEF.md needs (structure only, from the assignment)

For each effect:
- **The job:** what it tells the player and why; the script and signal or variable; for B, its job and the feature A doesn't use.
- **The intent block:** timing phases; contrast against the named background; scale against the character; change over life; variation; each emitter's job.
- **The settings:**
  - node type and why;
  - emission: amount, one_shot, explosiveness, lifetime, shape;
  - process: velocity, spread, gravity, damping, and the colour, alpha and scale curves;
  - draw: texture, material, blend;
  - local_coords and why;
  - visibility_rect, generated or set and checked;
  - preprocess.
- **Observable rules:**
  - A: fires on every allowed event, never otherwise, at the event's position; its retrigger rule; what happens if its parent is freed.
  - B: starts and stops with its condition; behaviour while paused and while hidden; the value-to-`amount_ratio` mapping.
- **Boundaries.**
- **The evidence split:** headless test, strip, or eyes, for each rule.
- **The frame strip:**
  - background;
  - trigger frame;
  - frames to read: for A, the trigger frame and +2, +5, +10, +20 and +40 at 30 fps; for B, start, steady state and after the condition ends.

For the whole brief:
- at least three predicted failures, each with the check that catches it;
- per effect: peak particle count, predicted headless CPU price, predicted GPU time, and a budget with the price it is compared on;
- answers to the six short questions.

## 10. Order of work

1. ~~Commit the A6 `scripts/run-test.sh` with the baseline counts~~: done in `8731c5c` (Claude, 2026-11-07). The renderer switch was committed during A5 (`aec645e` and earlier).
2. ~~Confirm the Visual Profiler shows non-zero GPU times under Vulkan~~: done 2026-11-08 (section 6).
3. Write the A6 `CHANGE-BRIEF.md` yourself, replacing the file's contents, and commit it before any prompt is sent.
4. Run Step 1 with `prompts/prompt-1.txt` (now the handout's text: revise CLAUDE.md). From the repository root:

   ```bash
   claude -p "$(cat prompts/prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Glob,Grep,Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(ls:*)" --max-turns 40 --output-format stream-json --verbose > prompts/session-1.jsonl
   ```

   - During A5, `claude -p` hit an individual spend limit that lasts until 2026-12-01. If it still refuses, run the same prompt in an interactive session and save its transcript, as you did for A5. Record which route you used in FRICTIONAL.md.
   - Commit the draft unedited, review it, then commit your review separately.
5. For Steps 2, 3, 5 and 7, use the scoped command in the assignment with `prompts/prompt-<N>.txt` and `prompts/session-<N>.jsonl`.
   - Steps 3 and 4 plan and then wait for your approval, so run them interactively in `claude`.
   - After every session, read the final `result` event, then run `git diff --stat godot/shaders/` and `git diff scripts/run-test.sh`.
6. You run every Movie Maker capture and every check in the running game.
