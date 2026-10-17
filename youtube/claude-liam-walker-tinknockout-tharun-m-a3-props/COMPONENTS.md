# COMPONENTS.md — what the film explains, and where it lives

Source: commit `1d93dcb` (game) · docs/evidence at `fd99467`. Ledger: `gamedev-evidence.json` (schema 1,
`code-then-result-v1`), `--game` = the repo's `godot/` folder.

## Godot components (checked by `./art godot-gamedev --check`)

| Component | Files (godot/) | Beats | Mechanism shown | Trade-off named |
|---|---|---|---|---|
| props-glb | `assets/props3d/{castle,windkey,toybox}.glb` + `.import` | B17, B18, B20 | glTF with `export_yup=True`: Blender Z-up arrives as Godot Y-up; root scale 1.0 | binary .glb carries the hand edit; the build script does not (B16) |
| prop-room | `prop_room/prop_room.tscn` | B17 → B18 | saved camera, light, floor, three instances at x −2.2 / 0 / 2.0 | a test room, not yet connected to the 2D game |
| check | `tests/check_props3d.gd` | B19 → B20, B21 → B22 | size vs brief ±0.01 m, base y = 0, scale/rotation, upright, tris, albedo, front at +Z; `to_root()` placement | measures, cannot judge the look; exits 0 even on a parse error |
| render-tools | `tools/shot_prop_room.gd`, `tools/shot_prop_views.gd` | B02, B23, B24 | Claude-made engine renders used as evidence | renders are Claude's, not the student's look check |

Code → visible result pairs (machine-checked): B17 → B18 (orbit capture), B19 → B20 (headless output), B21 → B22
(re-created false pass + parse error).

Excluded (86 files): every Assignment 2 slice file under `godot/` — `make_evidence.py` asserts each is byte-identical to
A2 revision `64c037a`. The A2 film explains them; the A3 props are not yet connected to the 2D game.

## Blender components (outside `godot/`, so recorded in `blender_code_result_pairs`, not machine-checked)

| Component | File | Beats | Mechanism | Result shown |
|---|---|---|---|---|
| castle (Blender MCP) | `tools/blender/build_castle.py` lines 47–52, 171–180 | B07 → B08, B09 → B10 | size-1 cube + scale + apply (dodges the 2 m default, A3-F1); join, origin to the world origin, apply | MCP look tool image (student's live session); student's own sidebar screenshot 07 |
| windkey (Blender MCP) | `tools/blender/build_windkey.py` lines 98–103 | B11 → B12 | lobe rotated 90° about X, rotation applied per part before the join (A3-F2/F4) | student's own screenshot 06 (rotation 0, scale 1, Triangles 192/192) |
| toybox (script route) | `tools/blender/build_toybox.py` lines 9–17 (+ `_common.py` box()) | B13 → B14 | four boxes, flat Principled Base Color; line 12 navy band | student's own screenshot 04 (navy band) |
| hand edit (student) | `assets/blender/toybox.blend`, `toybox.glb` (08f96cd) | B15, B16 | Material Preview → Material tab → Base Color #23395B → #2E7D32 | screenshots 04/05; check albedo #2E7D32 |

`build_windkey_script_route.py` (superseded first key) and `export_glb.py` are named, not excerpted.
