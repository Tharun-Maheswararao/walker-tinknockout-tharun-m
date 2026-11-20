# A7 Step 6 mutations

*Run by Claude, 2026-11-20. Each mutation ran in a fresh git worktree, `git worktree add ../a7-mutate HEAD` at `b3750b0`; the worktree was imported, mutated, tested through `./scripts/run-test.sh <test> 60`, then removed. The main working tree was never changed. Logs are next to this file; `SUMMARY.txt` is the raw run output.*

| # | Mutation (clip only) | Test | Exit | What caught it |
|---|---|---|---|---|
| M1 | Break one track's subname: `FacingPivot/BodyPivot:rotation` → `…:rotatoin` in `jab_action.tres` | `test_jab_action_readback.gd` | **8** (48 checks, 8 failed) | `track_problems`: "BodyPivot has no property rotatoin"; the path is not one the brief names; and the poses at frames 3, 5, 10, 11 no longer match |
| M1 | same | `test_a7_structure.gd` | **2** (54 checks, 2 failed) | `track_problems` on the **real** Bolt and Rivet |
| M2 | Flip the cycle's loop mode: `loop_mode = 1` → `0` (`Animation.LOOP_NONE`) in `wind_key_cycle.tres` | `test_wind_key_cycle_readback.gd` | **2** (26 checks, 2 failed) | "loop_mode is Animation.LOOP_LINEAR (got 0)"; played headless it showed 8 frames and stopped instead of 5 turns |
| M3 | Key a cell the sheet does not have: last frame key 7 → 8 (= hframes × vframes) | `test_wind_key_cycle_readback.gd` | **5** (26 checks, 5 failed) | the frame-range check, "every frame key is inside the sheet: 0 <= frame < 8"; the value list and the playback order |
| M4 | Delete `godot/.godot`, run `--import`, run the read-backs | `test_jab_action_readback.gd`, `test_wind_key_cycle_readback.gd`, `test_a7_structure.gd` | **0, 0, 0** (58/0, 26/0, 54/0) | **Did not fail, as expected for this route** (below) |

**Why M4 did not fail.** The rig is a keyed cutout rig, not an imported one. Both clips are hand-written `Animation` resources in `godot/animations/`, so `loop_mode` and every key live in the committed `.tres` text, with no importer and no `.import` file involved. An empty cache cannot drop them. What M4 does show: the project rebuilds from an empty cache, with the sheets reimported, `SteamMount` registered and both clips loading, and all three tests pass on it.

**What the engine said on its own:**
- **M1:** nothing about the broken track. The only engine lines in the M1 structure log, 21 × `Index p_track = 4294967295 is out of bounds`, come from the test itself looking the old track name up in the clip (`find_track` returns −1). The game ran with the rotation track inert and no warning: the silent failure the read-back exists for.
- **M3:** Godot printed `ERROR: Index p_frame = 8 is out of bounds (vframes * hframes = 8)` when the fixture played the bad key. That is a plain `ERROR:` line, which the wrapper does not fail on (it greps for `SHADER ERROR`, `SCRIPT ERROR` and `Failed loading resource`). Without the frame-range check, the run would have passed.
