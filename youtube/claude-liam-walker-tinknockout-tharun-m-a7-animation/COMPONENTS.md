# COMPONENTS.md — what the film explains, component by component

Coverage ledger: `gamedev-evidence.json` (the A7 files of `git diff 66c8cbc..a5978c0 -- godot`, `.uid` identifiers
excepted, in 6 components; every other file excluded only if byte-identical to tag `a6`, `66c8cbc`). Teaching contract
`code-then-result-v1`: two checked excerpt pairs (B03 → B04, B07 → B08) and six source-view pairs (B05 → B06,
B09 → B10, B11 → B12, B13 → B14, B15 → B16, B17 → B18).

| Component | Files | Beats | Code shown | Visible result |
|---|---|---|---|---|
| Clip A, `wind_key_cycle` (the cycle) | `animations/wind_key_cycle.tres` | B02, B13, B14, B20 | `wind_key_cycle.tres:3-19` | the key turning in the fixture (six wraps) and in the game (REWIND, then the hold at full wind) |
| Clip B, `jab_action` (the committing action) | `animations/jab_action.tres` | B02–B04, B09, B10, B15–B20 | `jab_action.tres:22-30`; line 15 (revision 1); lines 17, 29, 41 (revision 2) | M1's silent failure; the r0 strip at each phase boundary; r1, r2; whiff, landed hit, interrupts in play |
| Rig, authority and clock | `fighter/fighter.gd`, `effects/steam_mount.gd` | B05–B08, B19, B20, B22 | `fighter.gd:64-73, 306-315, 346-356` (339 in the notes) | the source scan; the clip frozen with `state_t` through hitstop; Tharun's CLOCKS line |
| The sheet | `tools/generate_key_sheets.gd`, `assets/props/key-*-sheet.png(.import)`, `assets/props/ATTRIBUTION.md` | B11, B12, B24 | `generate_key_sheets.gd:37-47` | both sheets sliced 8 × 1; cell centres; source and licence |
| Fixtures | `previews/jab_preview.*`, `previews/key_cycle_preview.*` | B10, B14, B16, B18 | — | every strip and the preview capture labelled FIXTURE |
| Tests | `tests/test_a7_*.gd`, `test_*_readback.gd`, `test_slice.gd`, `test_wind_steam_state.gd` | B04, B06, B21, B22 | — | re-run counts; M1–M4; the seam regression before / after |

## One complete input → state → output trace

B19 / B08, from the film capture log: a J key event (`Input.parse_input_event`) → `main._read_player` sets
`intent.jab` → `Fighter._neutral` spends 12 wind and `_enter(S.JAB)` (state_t 0) → `step` → `_sync_clips` plays
`jab_action` and seeks it to `state_t` → `BodyPivot` x −6.00 on e+3, +14.00 on e+5 → the jab box overlaps Rivet's
hurtbox on e+5 → `receive_hit`, hitstop 0.07 → `step` returns early for five ticks → clip position stays 0.0833 →
the picture holds the lunge (B08 strip).

## Design choices and one trade-off each (as recorded)

- **Both clips on AnimationPlayer, the key as a Sprite2D frame track** (CHANGE-BRIEF §1): read-backs inspect the
  `Animation` resources directly; the trade-off (§11 answer 1) is that an `AnimatedSprite2D` would need its own
  `SpriteFrames` read-back instead.
- **MANUAL players put at `state_t`** (§6): no clock disagreement and a free freeze through pause and hitstop; the cost
  was a seek-direction bug at the wrap, found by a fixture log and fixed (A7-9a).
- **Keys as resource text** (§1, A7-5 M4): nothing is imported, so an empty cache cannot drop `loop_mode`; the cost is
  that the loader checks no track path (M1).
