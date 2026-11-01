# A5 brief facts (Claude, facts only)

*Gathered by Claude Code on 2026-11-01 from the files and one PIL measurement. These are inputs for Tharun's CHANGE-BRIEF. There are no predictions, no colour line and no design choices here. Each fact cites the file and line it comes from.*

## Engine and renderer

- Godot 4.7.2.stable.official.ed1daf0bf, from `godot --version`.
- `godot/project.godot:15` is `config/features=PackedStringArray("4.7", "Forward Plus")`. There is no `rendering/renderer/rendering_method` line. The editor removed it as a default value on 2026-10-29; see `evidence/a6/renderer-switch/`.
- `godot/project.godot:31`: `rendering_device/driver.macos="vulkan"`, which is MoltenVK on macOS.
- `rendering/viewport/hdr_2d` is not set in `project.godot`, so it is off (default `false`).
- Viewport is 640×360, the window is 1280×720 and stretch is `canvas_items` (`project.godot:23-27`).
- No `texture_filter`, `modulate` or `material` is set on any 2D node in `godot/` (grep, 2026-11-01).

## The object a canvas_item shader would go on

- Each fighter's body is `var sprite: Sprite2D` (`fighter/fighter.gd:64`), created in code at `fighter.gd:72-74`.
- Its texture is swapped per state (`fighter.gd:265`), scaled ±1/3 with a flip for facing (`fighter.gd:260, 266`), and offset by `-FEET` = (240, 435) (`fighter.gd:261, 267`).
- The wind key and the weapon are separate `Sprite2D`s (`fighter.gd:75-80`). A material on `sprite` does not reach them.
- There are two instances, `bolt` and `rivet`, both `Fighter.new()` (`game/main.gd:50-53`). Each has its own `sprite`.
- Pose textures are 480×450 RGBA (`assets/fighters/<skin>/<pose>.png`). They are imported with `compress/mode=0`, `mipmaps/generate=false` (`bolt/rewind.png.import`).

## The REWIND state

| Fact | Where |
|---|---|
| `var state: int`, enum value `S.REWIND` | `fighter.gd:50`, `fighter.gd:19` |
| Entered from IDLE/WALK when `intent.rewind` is true | `fighter.gd:158-159` |
| Left to IDLE on the first tick the key is up | `fighter.gd:203-204` |
| Left to HURT if hit while rewinding (knockdown, `KNOCKDOWN_TIME` 0.80 s), or to KO | `fighter.gd:228-236`, `fighter.gd:33` |
| At full wind it **stays** in REWIND with the key held (no more ticks) | `fighter.gd:206-207` |
| Re-entering REWIND resets `crank_deg`; `state_changed` fires on real changes only | `fighter.gd:252-255` |
| Bolt's input: S or ↓ (`rewind` action), read with `Input.is_action_pressed` | `game/controls.gd:12`, `main.gd:158` |
| Rivet's AI rewinds when wind < 25 and stops at ≥ 90 | `fighter/rivet_brain.gd:26-33` |

## Time, pause and frame rate

- The simulation runs in `main.gd:_physics_process(dt)` (`main.gd:124`). `physics/common/physics_ticks_per_second` is not set, so the default of 60 applies.
- **Pause is a game flag, not tree pause.** Esc or P toggles `main.paused` during FIGHT only (`main.gd:19, 115-117`). While it is set, `_read_player`, the AI and `_simulate` are skipped (`main.gd:134-137`), so `fighter.state` keeps its value.
- `Main` is `PROCESS_MODE_ALWAYS` (`main.gd:38`). `get_tree().paused` is never used.
- **Hitstop:** `fighter.step` returns early while `hitstop > 0` (`fighter.gd:129-131`), which is 0.07 s on every hit (`fighter.gd:37`). The state does not change during hitstop.
- `Engine.time_scale` is not used anywhere in the project (grep, 2026-11-01).
- **Existing tests use real input:** `Input.action_press`/`action_release` and `Input.parse_input_event` (`tests/test_slice.gd:5, 33-44`).

## Camera (matters for pixel captures)

- The camera sits at (320, 180) (`main.gd:40`).
- On impacts, `shake` gives a random ±3 px offset for 0.15 s (`main.gd:200, 207`).
- On a knockdown or KO, `roll` gives up to a 5° tilt for 0.45 s (`main.gd:142, 202, 208`).
- A capture taken during either one moves every pixel.

## Measured pixel candidates (texel values only, not predictions)

The texels were measured with PIL from `rewind.png`. All four are fully opaque over the 7×7 texels around them, so the background does not mix in. "Spread" is the largest channel difference inside that 7×7 block. The sprite is drawn at 1/3 scale with the default linear filter, so a displayed pixel is a blend of neighbouring texels, and a small spread keeps that blend close to the texel.

| Name | Texel (x, y) | Bolt RGB | Rivet RGB | Spread (Bolt) | Game px, Bolt at start (x 200, facing right) | 1280×720 capture px |
|---|---|---|---|---|---|---|
| A: chest, left of the button | (251, 275) | (217, 87, 64) | (126, 206, 182) | 3 | (203.7, 238.7) | (407, 477) |
| B: helmet dome, above the porthole | (281, 153) | (251, 188, 34) | (205, 113, 54) | 4 | (213.7, 198.0) | (427, 396) |
| C: helmet, below the porthole | (279, 237) | (211, 152, 29) | — | 4 | (213.0, 226.0) | (426, 452) |
| D: porthole frame | (287, 197) | (30, 26, 22) | (30, 26, 22) | 1 | (215.7, 212.7) | (431, 425) |

- **Screen mapping:** `game px = (fighter.x + facing·(tx − 240)/3, 292 + (ty − 435)/3)`. It comes from `fighter.gd:260-267` and `FLOOR_Y` at `main.gd:12`. Bolt resets to x 200 facing right and Rivet to x 440 facing left (`main.gd:95-96`).
- **Unconfirmed:** that `get_viewport().get_texture().get_image()` returns 1280×720 under `canvas_items` stretch. Check the first capture's size.
- Marked image: `design/a5/bolt_rewind_marked.png`.

**Background beside Bolt's chest** (measured 2026-11-01). Source: `assets/env/bowl.png`, resized to 640×360 as `main.gd:47` draws it, counting only pixels the rewind pose does not cover:

| Patch (game px) | What it is | Mean RGB | Std dev |
|---|---|---|---|
| right of the chest, x 238–247, y 232–245 (140 px) | the pink castle | (215, 89, 123) | (9, 23, 12) |
| left of the chest, x 166–175, y 240–253 (133 px) | dark water | (68, 60, 92) | (26, 15, 12) |

## 3D scene for the textured shader (from A3)

- `godot/prop_room/prop_room.tscn` contains WorldEnvironment, a Floor plane with StandardMaterial3D, Sun (DirectionalLight3D with shadows), Camera3D at (0, 1.6, 5.5), and `castle.glb`, `windkey.glb` and `toybox.glb`.
- The glb materials are embedded flat-colour Principled BSDF (`CHANGE-BRIEF.md` A3.1). Material counts: castle 3, toybox 4, windkey 2.
- The glbs have UVs (TEXCOORD_0) but no TANGENT attribute. Godot's importer generates tangents by default; this is unconfirmed for these files.
- Under Forward+ the prop room renders darker than it did under Compatibility (`evidence/a6/renderer-switch/compare.txt`).
