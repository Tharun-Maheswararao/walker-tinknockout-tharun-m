# Step 3b plan — Effect B wiring (Claude's proposal for `prompts/prompt-3b.txt`, 2026-11-08)

`claude -p` is spend-limited until 2026-12-01, so the prompt ran in the interactive Claude Code session. No file is edited until Tharun approves a step.

## Step 1: `godot/game/main.gd`, about 10 lines, presentation only

Where the driver lives was left open by CHANGE-BRIEF C. The proposal puts it in `main.gd`, beside where each fighter's A5 tint driver is attached (`main.gd:56-66`), because the whole driver is one signal connection.

1. A new constant, `WIND_STEAM := preload("res://effects/wind_steam.tscn")`.
2. In the `for f in [bolt, rivet]` loop, after `add_child(f)`, when `f.key_sprite` exists:
   - instance the scene and add it as a child of `f.key_sprite` (B.3);
   - connect `f.wind_changed` to a lambda that sets that instance's `amount_ratio` to `steam_ratio(w)`.
3. A new `static func steam_ratio(w: float) -> float`, which returns `clampf((LOW_WIND - w) / LOW_WIND, 0.0, 1.0)`. It reuses the existing `LOW_WIND` 25 (`main.gd:15`).
   - wind ≥ 25 gives 0.0, and wind 0 gives 1.0, linearly in between (B.1, B-R3).

What the code does and does not do:
- It sets only `amount_ratio`. It never touches `amount`, `emitting` or any process value (CLAUDE.md, Ownership; B-R2).
- It reads `wind` only through the signal the fighter already emits:
  - `_spend` on every attack and every walking frame (`fighter.gd:242-244`);
  - each rewind click (`:211-212`);
  - `reset` (`:107`), which sets wind to 100 at round start and rematch (B-R6).
- It writes no game state.
- The scene already starts at `amount_ratio` 0.0, so nothing emits on load (B-R6).
- The pause rule needs no code (B-R4): the steam inherits `PROCESS_MODE_ALWAYS` through Main → Fighter → key_sprite.
- The hidden rule needs no code either (B-R5): KO hides `key_sprite` (`fighter.gd:274`), and the steam is its child.

Not touched: fighter.gd, input, round flow, pause and mute logic, the music's low-wind cue, Effect A, the existing tests and `godot/shaders/`.

## Step 2: `godot/tests/test_wind_steam_state.gd`, run at 60 fps

- **Helpers:** the same as `test_impact_effect_state.gd`. Bolt is driven through `Input.action_press`/`release` and parsed pause and rematch events. Rivet is frozen by a stand-in brain (SETUP).
- **Finding the steam:** the test finds each fighter's steam as the child of `key_sprite` whose `scene_file_path` is `wind_steam.tscn`. main.gd needs no test hook.
- **Setting wind:** wind is never set directly in the assertions' path. The test moves it only with real jabs and real rewinding.

Wind path (the jabs whiff at range, so Rivet's state doesn't interfere):

| Input | Wind | Expected `amount_ratio` |
|---|---|---|
| Round start | 100 | 0.0 |
| 6 jabs (12 each, `fighter.gd:42`) | 28 | 0.0, still above 25 |
| 7th jab | 16 | 0.36 |
| 8th jab | 4 | 0.84 |
| Rewind, 2 clicks (+10 each) | 24 | 0.04: `amount × amount_ratio` = 1.0, the F5 threshold |
| Rewind, 1 more click | 34 | 0.0 |

| # | Assertion | Rule |
|---|---|---|
| 1 | After load and round start, both fighters' steam: `amount_ratio` 0.0, `emitting` true, `amount` 25 | B-R6 |
| 2 | Bolt's ratio stays 0.0 through wind 28, then is > 0 at the first jab below 25 | B-R1 |
| 3 | Ratio 0.36 at wind 16 and 0.84 at wind 4; `amount` stays 25 at every value | B-R3 (two values; `amount_ratio` changes, `amount` doesn't) |
| 4 | Rivet's ratio stays 0.0 while Bolt's rises | one per fighter (B.1) |
| 5 | At wind 24, `amount × amount_ratio` = 1.0 | F5 |
| 6 | Rewinding past 25 returns the ratio to 0.0, and `emitting` is still true | B-R2 |
| 7 | At wind 4, pause (real event) and press keys while paused: wind, ratio, `emitting` and `speed_scale` unchanged; the steam `can_process()` | B-R4 |
| 8 | Rivet at 5 hp (SETUP), Bolt jabs, Rivet is KO: Rivet's `key_sprite` is hidden, and his steam is not `is_visible_in_tree()` | B-R5 |
| 9 | After the KO, with Bolt's ratio > 0, a real rematch event: both ratios 0.0 again, from `reset`'s `wind_changed` | B-R6 |

Then all tests run through the wrapper:
- the new test at 60;
- `test_wind_steam_config` at 60;
- both Effect A tests at 60;
- `test_slice` at 60;
- `check_props3d` at 60;
- `test_rewind_tint` at 30, 60 and 144;
- `test_materials` at 60.

`git diff scripts/run-test.sh godot/shaders` must be empty.

## What the test proves, and what it cannot

- **Proves:** which `amount_ratio` the code sets for each wind value reached through real play; that it never changes `amount`; when emission is allowed to start and stop; per-fighter independence; that it holds while paused; that it is hidden on KO; and the reset on rematch.
- **Cannot prove**, because a headless run draws nothing (strip or eyes checks):
  - how the steam looks, and whether it fades smoothly after the ratio drops (B-R2's look);
  - whether a hidden emitter keeps simulating, and what shows when it reappears (B-R5, CLAUDE.md Unconfirmed);
  - that it draws behind the body and squashes during REWIND;
  - when the first visible puff actually appears (F5's eyes half).
