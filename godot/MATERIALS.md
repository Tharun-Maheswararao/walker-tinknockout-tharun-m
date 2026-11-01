# MATERIALS.md: A5 materials audit

*Audit by Claude Code (Opus 5.5), 2026-11-01. The task is the one in `prompts/a5/prompt-3-audit.txt`. It was run in the interactive desktop session, because `claude -p` was blocked by the account's spend limit (see `evidence/a5/session-2-implement.jsonl`). No `.gdshader`, material, scene or `.import` file was changed by this audit. Every number below was printed by `godot/tests/test_materials.gd` (`logs/test_materials_60fps.log`) or read from the file and line cited.*

## 1. Materials

| Resource | Shader | Uniform values it sets | Textures it binds |
|---|---|---|---|
| `prop_room/materials/toybox_fresh.tres` | `res://shaders/painted_tin.gdshader` | `wear_amount` 0.05, `paint_roughness` 0.3. `paint_color`, `normal_depth` and `uv_scale` are unset, so the shader defaults apply. | `metal_albedo` → `metal_plate_diff_1k.png`; `metal_normal` → `metal_plate_nor_gl_1k.png`; `metal_rough` → `metal_plate_rough_1k.png` |
| `prop_room/materials/toybox_worn.tres` | `res://shaders/painted_tin.gdshader` | `wear_amount` 0.55, `paint_roughness` 0.7. The other three are unset, as above. | the same three textures |
| `hint_experiment/hint_source_color.tres` | `res://shaders/hint_experiment.gdshader` | `use_colour_sampler` true | `grey_as_colour` and `grey_as_data` → both `hint_greys_3x1.png` |
| `hint_experiment/hint_data.tres` | `res://shaders/hint_experiment.gdshader` | `use_colour_sampler` false | the same PNG to both samplers |

Where they are used:
- `toybox_fresh` is on surface 0 of every `toybox.glb` instance, through the glb's Use External (`assets/props3d/toybox.glb.import`, `_subresources` → `materials/toybox_red`).
- `toybox_worn` is a surface override on `toybox_worn/toybox` in `prop_room/prop_room.tscn`.
- The hint materials are the `material_override` of `Quad_S_source_color` and `Quad_D_data` in `hint_experiment/hint_experiment.tscn`.

## 2. Samplers

| Shader | Sampler | Hints as written | Bound texture (all materials) | compress/mode | compress/normal_map | mipmaps/generate | Imported format (measured) |
|---|---|---|---|---|---|---|---|
| painted_tin (line 3) | `metal_albedo` | `source_color, filter_linear_mipmap, repeat_enable` | `metal_plate_diff_1k.png` | 2 (VRAM Compressed) | 2 (Disabled) | true | 17 = DXT1, 1024², mipmaps |
| painted_tin (line 4) | `metal_normal` | `hint_normal, filter_linear_mipmap, repeat_enable` | `metal_plate_nor_gl_1k.png` | 2 | 1 (Enable) | true | 21 = RGTC_RG, 1024², mipmaps |
| painted_tin (line 5) | `metal_rough` | `filter_linear_mipmap, repeat_enable` | `metal_plate_rough_1k.png` | 2 | 2 | true | 17 = DXT1, 1024², mipmaps |
| hint_experiment (line 4) | `grey_as_colour` | `source_color, filter_nearest` | `hint_greys_3x1.png` | 0 (Lossless) | 2 | false | 4 = RGB8, 3×1, no mipmaps |
| hint_experiment (line 5) | `grey_as_data` | `filter_nearest` | `hint_greys_3x1.png` | 0 | 2 | false | 4 = RGB8 |
| (none) | — | — | `metal_plate_nor_dx_1k.png`, calibration only | 2 | 1 | true | 21 = RGTC_RG |

All five texture imports also set `detect_3d/compress_to=0` and `roughness/mode=1`.

**Enum labels:**
- The import labels come from the property hint strings in the Godot 4.7.2 binary: "Lossless,Lossy,VRAM Compressed,VRAM Uncompressed,Basis Universal" and "Detect,Enable,Disabled".
- The format numbers are `Image.FORMAT_DXT1` = 17, `FORMAT_RGTC_RG` = 21 and `FORMAT_RGB8` = 4, printed by Godot itself.

The uniform list reports all five samplers only as type 24 with hint_string `Texture2D`. **The sampler hints are therefore readable only from the source text,** which is why the test reads them with a regex.

## 3. Lights and environment that change the look

| Scene | Setting | Value | Evidence |
|---|---|---|---|
| prop_room | Sun (DirectionalLight3D) | energy 1.00, shadows on | `prop_room.tscn:30-32`; printed by the test |
| prop_room | Background | custom colour (0.12, 0.15, 0.22) | `prop_room.tscn:15-16` |
| prop_room | Ambient light | colour (0.45, 0.5, 0.6), energy 0.6 | `prop_room.tscn:17-19` |
| prop_room | Tonemap and exposure | 0 = `TONE_MAPPER_LINEAR`, exposure 1.00. Engine defaults, not written in the file. | printed by the test |
| prop_room | SSAO, SSIL, SDFGI, glow, fog | all off (defaults; not written in the file) | asserted by the test |
| hint_experiment | Tonemap and exposure | `TONE_MAPPER_LINEAR` (0), exposure 1.0 | asserted by the test. Set by name in `tools/make_hint_scene.gd`; not written in the `.tscn` because they equal the defaults. |
| hint_experiment | Glow, fog, volumetric fog, adjustments | all off | asserted by the test |
| hint_experiment | Lights | none; both quads are `render_mode unshaded` | `hint_experiment.gdshader:2` |
| hint_experiment | Camera | orthographic, size 2.6, at (0, 0, 5) | `hint_experiment.tscn` |

## 4. Findings

| # | Finding | Evidence |
|---|---|---|
| M1 | **A headless teardown error appears in every log that frees a ShaderMaterial on a MeshInstance3D:** `ERROR: Parameter "material" is null` at `material_get_instance_shader_parameters (servers/rendering/dummy/storage/material_storage.cpp:264)`. It prints after the result line, so no check depends on it, and the wrapper does not count it (it is not SHADER/SCRIPT ERROR). | Absent from the baseline `check_props3d` log (`23a0363`); present since the toy box got a ShaderMaterial (`ceaece8`); present in `logs/test_materials_60fps.log`. |
| M2 | **Tonemap and exposure in both scenes are engine defaults, not values written in the scene file.** A future engine default would change the look without a file diff. | `hint_experiment.tscn:6-8` and `prop_room.tscn:14-19` have no tonemap line. The test pins both at load. |
| M3 | **The four `.tres` files have no `uid=` lines.** They were saved headlessly by `tools/make_toybox_materials.gd` and `tools/make_hint_scene.gd`, and they reference resources by path. The editor will add UIDs on its first save, which will show as a diff (expected). | the `.tres` headers |
| M4 | **The headless save wrote `shader_parameter/<name> = null` for every unset uniform,** because headless Godot cannot read defaults. Claude deleted those lines in `ceaece8`, so the files list only what each material sets. | commit `ceaece8`; `evidence/a5/headless-facts.txt:5` |
| M5 | **`painted_tin` never writes `METALLIC`,** so worn (bare-metal) areas are shaded as a non-metal: colour from the plate texture, roughness from the map, metallic 0. CHANGE-BRIEF A5.5 does not mention metallic, so this is not a spec violation, but it may make "bare metal" read as grey paint. A look question for the interface sweep. | `painted_tin.gdshader:16-25` |
| M6 | **`metal_rough` is sampled once and used twice:** as `ROUGHNESS` where worn, and as the wear mask in `step(1.0 - wear_amount, rough)`. This is intended (A5.5: "the same values decide where the paint wears through first"). | `painted_tin.gdshader:19-22` |
| M7 | **`metal_plate_nor_dx_1k.png` is imported (VRAM, mipmaps) but bound to no material.** Intended (calibration only, A5.5), but it is an import nobody renders. | ATTRIBUTION.md; the test's import table |
| M8 | **All four Metal Plate sources are 16-bit PNGs,** imported to 8-bit block compression (DXT1, RGTC_RG). The curl check reads the source files with `Image.load_from_file` (RGB8 after loading), not the compressed imports. | the test's format lines; `logs/calibrate_normal_map_60fps.log` |
| M9 | **`check_props3d.gd` now prints `albedo=#000000` for `toybox_fresh`** (it reads `albedo_color` only from BaseMaterial3D). It does not assert on colour, so it still passes. | `check_props3d.gd:78`; `logs/check_props3d_60fps.log` |
| M10 | **The materials leave `uv_scale`, `normal_depth` and `paint_color` unset.** Editing one of those defaults in `painted_tin.gdshader` therefore changes both toy boxes, and editing a value in one `.tres` changes only that box. This is what the "one shader, two materials" human check needs. | section 1 |

Nothing in sections 1–3 is inconsistent with CHANGE-BRIEF A5.4 and A5.5, apart from the open look question M5.

## 5. Attribution (exactly as in CHANGE-BRIEF A5.5)

- Poly Haven "Metal Plate" (https://polyhaven.com/a/metal_plate) by Rob Tuytel, CC0, 1k PNG, 16-bit. Credits and checksums: `godot/assets/textures/metal_plate/ATTRIBUTION.md`.
- The normal map bound to materials is `_nor_gl` (OpenGL, what Godot expects). `_nor_dx` is calibration only.
- `hint_greys_3x1.png` is written by code: `godot/tools/write_hint_png.gd`.

## 6. Texture data: curl ratio (stride 4)

| File | GL convention | DX convention | Reading |
|---|---|---|---|
| `metal_plate_nor_gl_1k.png` (bound) | **0.0658** | 1.9342 | real surface, right convention for Godot |
| `metal_plate_nor_dx_1k.png` (calibration) | 1.9342 | **0.0658** | real surface, other convention |

The threshold (< 0.5 = real map in this convention) is set from this known-good pair (`logs/calibrate_normal_map_60fps.log`), not by feel. The sign convention is not reversed.

## 7. What this audit cannot establish headlessly

A headless run draws nothing (`evidence/a5/headless-facts.txt`). This audit therefore says nothing about:
- how either toy box looks;
- whether `source_color` changes the displayed greys;
- whether the worn box reads as worn;
- whether the normal map's dents face the right way under the Sun.

Each of those is a human check in TEST-REPORT ("Use It").
