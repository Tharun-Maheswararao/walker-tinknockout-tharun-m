# walker-tinknockout-tharun-m — Tin Knockout

Tin wind-up toys box in a glass bowl in a toy shop after closing. You play **Bolt**, a tin deep-sea-diver toy. Every punch, cutlass swing and cork-gun shot unwinds your spring, and rewinding leaves you open.

This repository is the **CSYE 7270 Assignment 2 asset slice**: generated art, sound effects and music, proven together in one small playable Godot scene.

- **Started from:** an empty Godot 4.7 project. Patterns (viewport, input-driven tests, capture contract) come from my Assignment 1, [walker-jumpman-tharun-m @ bb63748](https://github.com/Tharun-Maheswararao/walker-jumpman-tharun-m), which extends [nikbearbrown/walker-jumpman @ 9387542](https://github.com/nikbearbrown/walker-jumpman). No game code was reused. See [SOURCES.md](SOURCES.md).
- **Engine:** Godot 4.7.2.stable, Forward+ on Vulkan (MoltenVK on macOS) from Assignment 5 on; Assignments 2 and 3 used GL Compatibility. Tested on macOS 15.6, Apple M4.

## Run

```bash
git clone https://github.com/Tharun-Maheswararao/walker-tinknockout-tharun-m.git
cd walker-tinknockout-tharun-m
godot --path godot          # or open godot/project.godot in the Godot editor and press F5
```

## Controls

| Key | Action | Pad |
|---|---|---|
| Enter / Space | start | A |
| A / D or ← / → | walk (Bolt turns to face the way he walks) | D-pad |
| J | jab (12 wind) | X |
| K | tin cutlass (22 wind) | Y |
| L | cork pop-gun (30 wind) | B |
| I or ↑ (hold) | block (in front only) | RB |
| S or ↓ (hold) | rewind the spring (one click = 10 wind) | LB |
| Esc / P | pause (music muffles) | Start |
| **M** | **mute / unmute music** | |
| **N** | **mute / unmute effects** | |
| R | rematch after K.O. | Back |
| F1 | show hurtboxes (green) and hitboxes (red) | |
| F9 | (debug builds) A5 in-engine tint captures | |
| **F10** | **(debug builds) toggle vsync, for the A6 GPU-price FPS comparison** | |

## What the slice demonstrates

- **Character:** 11 generated static poses, one per state, swapped on state change, flipped at runtime for left-facing, and anchored to a 50×106 hurtbox. Rivet is a palette swap.
- **Environment:** a generated toy-shop / glass-bowl background, plus generated props (key, cutlass, pop-gun, cork).
- **Sound:** 6 generated event sounds (bell, jab, cutlass, pop, rewind click, spring-empty). Each fires once per event from gameplay signals. Gameplay never calls audio.
- **Music:** a generated waltz loop. It slows below 25 % spring, muffles on pause, and stops on K.O.
- **Readable muted:** spring dials, state labels, distinct poses, hit sparks, hitstop and K.O. text.

## Tests

```bash
godot --headless --path godot --script res://tests/test_slice.gd   # 25 checks
python tools/edit/check_seam.py                                     # music loop seam
```

## Documents

| File | Contents |
|---|---|
| [GDD.md](GDD.md) ([PDF](GDD.pdf)) | game design document for the full game; figures in `design/gdd/`, PDF built by `tools/gdd/build_pdf.py` |
| [CONCEPT.md](CONCEPT.md) | concept, core loop, pillars, art and audio direction |
| [STORYBOARD.md](STORYBOARD.md) | 7 panels |
| [CHARACTER-SHEET.md](CHARACTER-SHEET.md) | the character spec |
| [CHANGE-BRIEF.md](CHANGE-BRIEF.md) | plan and predictions (committed before generation) |
| [ASSET-LOG.md](ASSET-LOG.md) | every generation: prompt, seed, outcome, edits |
| [SOURCES.md](SOURCES.md) | models, licenses, who did what |
| [TEST-REPORT.md](TEST-REPORT.md) | results |
| [FRICTIONAL.md](FRICTIONAL.md) | design log |
| [SUBMISSION.md](SUBMISSION.md) | Canvas submission |

## Known limitations

1. The sound effects and music were picked by Claude's signal analysis, not by ear (see SOURCES / TEST-REPORT).
2. The background shows the bowl from outside.
3. Rivet follows a fixed pattern, not AI.
4. Bolt's eyes are hand-painted on every pose.
5. Bolt's yellow helmet has low luminance contrast against the pink castle at his start position.
6. Only one round; there are no weapon pickups yet.

## Film

**Final film:** [claude-liam-walker-tinknockout-tharun-m-gamedev.mp4](https://drive.google.com/file/d/1vp5DGYY0RXe-cttXE4endf4W7YCuIrck/view?usp=sharing) (Google Drive, 4K, 6:46). SHA-256 `8c6c491bb59df135f083786f04832c0b68c3f74a2b47c13303581a1e86edeb83`. Shows source revision `64c037a`. The MP4 is kept out of GitHub; the reel's beat sheet, evidence ledger and QC records are in `youtube/claude-liam-walker-tinknockout-tharun-m-gamedev/`.

---

## Assignment 3 — three 3D props (tag `a3`)

**Added:** a small Godot 3D scene `godot/prop_room/prop_room.tscn` (floor, one light, a camera) with three props at character scale (Bolt = 1.80 m): the **sunken-castle ornament** (environment), the **winding key** pickup (collectible) and the **toy box** (prop). Built in Blender from primitives, exported as `.glb` to `godot/assets/props3d/`, with `.blend` sources in `assets/blender/` and build code in `tools/blender/`.

**Versions:** Godot 4.7.2.stable · Blender 5.2.2 LTS · MCP for Blender 2.1.9 (add-on 1.8) · macOS 15.6.

**Routes:** castle and windkey = Blender MCP; toybox = script route (headless Blender). See TEST-REPORT.md "Assignment 3".

**Run the check** (from the repo root; `timeout` is from Homebrew coreutils):
```bash
godot --headless --path godot --import
```
```bash
timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60
```
Expect `RESULT: PASS (0 failing)`. Read that line: Godot exits 0 even if the script fails to parse.

**Open the scene:** `godot --path godot -e`, then open `res://prop_room/prop_room.tscn` and press F6.

**Rebuild an asset:** `blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_<asset>.py`, then `blender -b assets/blender/<asset>.blend --python-exit-code 1 --python tools/blender/export_glb.py -- godot/assets/props3d/<asset>.glb`.

**Known limitations (A3):** the toy box used the script route, not the MCP. The cream lid reads near-white under the scene light. The prop room is not connected to the 2D game. 

**A3 film:** [claude-liam-walker-tinknockout-tharun-m-a3-props.mp4](https://drive.google.com/file/d/1l_fboMP7sHmJDt0vd_IM93I63KSMIbgk/view?usp=sharing) · SHA-256 `007d0d984c9a34eb36d3d741db9ebbe062b661158db73b57ffa9557b87630b5e` · 4K, 9:28 · shows game source `1d93dcb`. Beat sheet, script, evidence ledger and QC records: `youtube/claude-liam-walker-tinknockout-tharun-m-a3-props/` (the MP4 itself is not in GitHub).

Docs for A3: CHANGE-BRIEF.md (bottom), BLENDER-NOTES.md, TEST-REPORT.md (bottom), FRICTIONAL.md (bottom), SOURCES.md (bottom).

---

## Assignment 5 — shaders, materials and the shading language (tag `a5`)

**Added:**
- **REWIND tint, a shader from code:** `godot/shaders/rewind_tint.gdshader`, hand-written. Each fighter's body sprite fades toward blue while that fighter rewinds its spring (the vulnerable state): 0.15 s in, 0.30 s out, using one ShaderMaterial per fighter. The driver is `godot/fighter/rewind_tint_driver.gd`.
- **Painted-tin textured shader:** `godot/shaders/painted_tin.gdshader`, hand-written, with Poly Haven "Metal Plate" (CC0) colour, normal and roughness textures. Two materials, `toybox_fresh` and `toybox_worn`, sit on two toy boxes in `prop_room.tscn`.
- **Hint experiment:** `godot/shaders/hint_experiment.gdshader`, hand-written, in `godot/hint_experiment/hint_experiment.tscn`. It reads the same 3×1 grey PNG as colour and as data.
- **Generated shader:** `godot/shaders/standard_generated.gdshader`, converted from a StandardMaterial3D and annotated. Nothing in the game uses it.
- **F9:** a debug-build in-engine capture key (`godot/game/debug_capture.gd`).

**Run the tests** from the repo root, always through the handout's wrapper (`timeout` is from Homebrew coreutils). Run `godot --headless --path godot --import` once after cloning, then:
```bash
./scripts/run-test.sh test_slice.gd 60
```
```bash
./scripts/run-test.sh check_props3d.gd 60
```
```bash
./scripts/run-test.sh test_rewind_tint.gd 30
```
```bash
./scripts/run-test.sh test_rewind_tint.gd 60
```
```bash
./scripts/run-test.sh test_rewind_tint.gd 144
```
```bash
./scripts/run-test.sh test_materials.gd 60
```

Expected results:
- `test_slice`: 25 checks, 0 failed;
- `check_props3d`: RESULT PASS;
- `test_rewind_tint`: 50 checks, 0 failed at each rate;
- `test_materials`: 55 checks, 0 failed.

**See it:**
- The tint: `godot --path godot`, then press Enter and hold **S**.
- The hint quads: open `res://hint_experiment/hint_experiment.tscn` in the editor and press F6.
- The toy boxes: open `res://prop_room/prop_room.tscn` and press F6.

**Docs for A5:**
- CLAUDE.md (agent context; imports CHANGE-BRIEF.md);
- CHANGE-BRIEF.md ("Assignment 5");
- godot/MATERIALS.md (the audit);
- LANGUAGE-NOTES.md;
- TEST-REPORT.md ("Assignment 5");
- FRICTIONAL.md;
- SOURCES.md;
- evidence/a5/ (headless facts, session transcripts, mutations, captures).

**Known limitations (A5):**
- `painted_tin` writes no METALLIC, so worn bare metal is shaded as a non-metal (MATERIALS.md M5).
- Bolt's tint starts up to one physics tick (1/60 s) after the key press at high frame rates.
- The `claude -p` sessions hit the account's spend limit, so the later agent work ran in the interactive session (SOURCES.md).
- The film's narration and visuals were built by a Claude film session (Brutalist `godot-gamedev` workflow); I watched it in full before uploading.

**A5 film:** [claude-liam-walker-tinknockout-tharun-m-a5-shaders.mp4](https://drive.google.com/file/d/1x90bbSlU_QSjNzabapgok6JhSpoYX68V/view?usp=sharing) · SHA-256 `6568f966a28b65ffad73d3aac36430b4f222d5f065af60dfd930946d141b2ed8` · 4K 3840×2160, 7:02 · shows game source `2e6946d`. Beat sheet, script, evidence ledger and QC records: `youtube/claude-liam-walker-tinknockout-tharun-m-a5-shaders/` (the MP4 itself is not in GitHub).


---

## Assignment 6 — particle effects (tag `a6`)

**Started from:** tag `a5` (`f4dda68`). Godot 4.7.2.stable, Forward+ on Vulkan (MoltenVK), Apple M4, window 1280×720 (viewport 640×360, `canvas_items`).

**Added:**
- **Effect A, impact burst** (`godot/effects/impact_effect.tscn`, plus `impact_effect_blocked.tscn` for blocked hits). It fires on every melee or cork impact through `main._on_impact`:
  - two GPUParticles2D emitters: dark tin shards (MIX) and a cyan core (ADD), drawn above the kept star spark;
  - a fresh instance per hit, so bursts overlap, each freed on `finished`;
  - blocked hits get a smaller grey burst.
- **Effect B, wind steam** (`godot/effects/wind_steam.tscn`). One emitter per fighter at the back key, on `godot/effects/steam_mount.gd`, which follows the key but not its rewind spin squash. `amount_ratio` follows wind: 0 at 25 and above, rising to 1 at 0.
- **Textures written by code:** `godot/tools/generate_shard_texture.gd` and `generate_steam_texture.gd` (credits: `godot/effects/textures/ATTRIBUTION.md`).
- **Generated process shader:** `godot/shaders/particles_generated.gdshader`, Effect B's ParticleProcessMaterial converted in the editor. Nothing in the game uses it.
- **Fixtures, not part of the game,** in `godot/previews/`:
  - `impact_preview`, `steam_preview` and `steam_rewind_preview` for the frame strips;
  - `gpu_price` for the Visual Profiler.
- **F10:** a debug-build vsync toggle (`godot/game/debug_vsync.gd`).

**Run the tests** from the repo root, through the wrapper. Run `godot --headless --path godot --import` once after cloning (it also registers the `SteamMount` class):
```bash
./scripts/run-test.sh test_impact_effect_config.gd 60
```
```bash
./scripts/run-test.sh test_impact_effect_state.gd 60
```
```bash
./scripts/run-test.sh test_wind_steam_config.gd 60
```
```bash
./scripts/run-test.sh test_wind_steam_state.gd 60
```
```bash
./scripts/run-test.sh cost_effects.gd 60 300
```

Expected results:
- `test_impact_effect_config`: 136 checks, 0 failed;
- `test_impact_effect_state`: 44 checks, 0 failed;
- `test_wind_steam_config`: 33 checks, 0 failed;
- `test_wind_steam_state`: 37 checks, 0 failed;
- `cost_effects`: a table of the four cases, exit 0.

The A5 commands above still give their baseline counts.

**See it:**
- **In the game:** `godot --path godot`, Enter. Jab Rivet (J) for Effect A. Whiff 7–8 jabs to bring Bolt's wind under 25 for Effect B, then hold S to rewind.
- **Strip fixtures** (capture commands are at the top of each script):
  ```bash
  godot --path godot res://previews/impact_preview.tscn -- --loop
  ```
  ```bash
  godot --path godot res://previews/steam_preview.tscn -- --loop
  ```
  ```bash
  godot --path godot res://previews/steam_rewind_preview.tscn -- --loop
  ```
- **GPU price:** open `res://previews/gpu_price.tscn` in the editor and press F6. Keys: **0** off, **1** Effect A at 4 bursts, **2** Effect B at full ratio on both fighters, **9** remove the steam, **F10** vsync. Read Debugger → Visual Profiler.
- **Captures:** use `--disable-vsync --always-on-top`. Without them, Movie Maker can write repeated frames (TEST-REPORT A6-3).

**Docs for A6:**
- CLAUDE.md (reviewed; imports the brief);
- CHANGE-BRIEF.md (v1 plus dated revisions);
- TUNING.md (both tuning loops);
- TEST-REPORT.md ("Assignment 6", "The process shader");
- FRICTIONAL.md;
- SOURCES.md;
- `godot/effects/textures/ATTRIBUTION.md`;
- `evidence/a6/` (plans, mutation logs, probes, cost log, profiler screenshot);
- `captures/` (strip frames);
- `prompts/`.

**Known limitations (A6):**
- Rivet's steam rarely shows. His pattern brain retreats and rewinds as soon as his wind drops below 25, the same threshold where the steam starts (TEST-REPORT A6-3).
- The headless price is near zero by construction (the dummy renderer). Two engine timing monitors read 0 headless, so only the wall clock is used.
- The GPU price was not measured (skipped, 2026-11-09), so the GPU budgets in CHANGE-BRIEF F are unchecked. The fixture `gpu_price.tscn` is there to measure it later (TEST-REPORT A6-5).
- `claude -p` was spend-limited until 2026-12-01, so all agent prompts ran in the interactive Claude Code session (SOURCES.md).

**A6 film:** claude-liam-walker-tinknockout-tharun-m-a6-particles.mp4 (_link to be added after upload_) · SHA-256 `04d435e30352681ac1bfecd855072acf700a9afc3a02cc5e601407e4b010630a` · 4K 3840×2160, 11:57 · shows game source `c844ab2`. Watched in full by Tharun on 2026-11-09. Beat sheet, script, evidence ledger and QC records: `youtube/claude-liam-walker-tinknockout-tharun-m-a6-particles/` (the MP4 itself is not in GitHub).
