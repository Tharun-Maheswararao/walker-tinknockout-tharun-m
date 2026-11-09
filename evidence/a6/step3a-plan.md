# Step 3a plan — Effect A wiring (Claude's proposal for `prompts/prompt-3a.txt`, 2026-11-08)

`claude -p` is spend-limited until 2026-12-01, so the prompt ran in the interactive Claude Code session. No file is edited until Tharun approves a step.

## Step 1: `godot/game/main.gd` (about 20 lines, presentation only)

1. Pass `blocked` through, as the brief allows (CHANGE-BRIEF C):
   - `main.gd:199`: `c.struck.connect(func(cork, blocked): _on_impact(cork.position, blocked))`. `cork.position` is read when `struck` is emitted, before the cork's `queue_free()` (`cork.gd:24-25`), as A-R4 requires.
   - `main.gd:202`: rename `_blocked` to `blocked` and pass it on: `_on_impact(p, blocked)`.
2. `_on_impact(p: Vector2, blocked := false)`: the existing three lines stay unchanged (star spark, shake, roll). One new call, `_spawn_impact(p, blocked)`.
3. A new `_spawn_impact(p, blocked)`, with two preloaded constants: `IMPACT_FX` (`impact_effect.tscn`) and `IMPACT_FX_BLOCKED` (`impact_effect_blocked.tscn`).
   - Instance the scene for the `blocked` flag (A-R5).
   - Set `position = p` (Main sits at the origin, so this is also the global position) (A-R2).
   - `add_child` it to Main (A-R4).
   - **Then** call `restart()` on each emitter, so that `finished` fires (the probe in the brief's A.4 review note and F2).
   - Count the emitters' `finished` signals in an Array; when both have fired, `queue_free()` the burst.
   - **Retrigger rule A-R3, overlap:** each impact makes a fresh instance and never touches an earlier one, so a second hit inside 0.25 s adds a second burst rather than restarting the first.
   - No effect values are set in code (CLAUDE.md, Ownership).
   - The burst inherits `PROCESS_MODE_ALWAYS` from Main (A-R7). Hitstop does not freeze it (hitstop is fighter state; the burst is presentation).

Not touched: fighter.gd, cork.gd, input, round flow, pause or mute logic, the star, shake, roll, audio, HUD, existing tests and `godot/shaders/`.

## Step 2: `godot/tests/test_impact_effect_state.gd`, run at 60 fps

The test copies `test_slice.gd`'s helpers.
- **Input:** Bolt is driven by `Input.action_press`/`release`. Rivet is frozen by a stand-in brain, the same SETUP pattern as test_slice's `FrozenBrain`.
- **Counting:** the test counts bursts through `main.child_entered_tree`, so main.gd needs no test hook.
- **Expected positions:** the test recomputes each expected `p` itself. For melee, it reads the attack box when `hit_landed` arrives. For corks, it reads the cork's position when `struck` arrives. It never calls `_on_impact` or `_spawn_impact`.

| # | Scenario, real input | Assertions | Rule |
|---|---|---|---|
| 1 | Scene load, TITLE → INTRO → FIGHT, no input | 0 bursts | A-R1 (never on load) |
| 2 | Six jabs in range | 6 `hit_landed` → 6 bursts, each `ImpactEffect`, each at the attack box centre | A-R1, A-R2, A-R5 (unblocked) |
| 3 | Jabs out of range, walking and rewinding | 0 bursts | A-R1 (never otherwise) |
| 4 | Pop-gun from range: Bolt presses P, and the cork flies and hits | 1 burst at the cork's position; the cork is freed; the burst is still in the tree afterwards and later frees itself | A-R2, A-R4 |
| 5 | **Two impacts inside one lifetime** (see the note) | Both bursts are in the tree at the same time; they are distinct instances at their own `p`; both later free themselves | A-R3 overlap |
| 6 | Rivet holds block (stand-in brain sets `intent.block`); Bolt jabs | `hit_landed(blocked = true)` → an `ImpactEffectBlocked` burst | A-R5 (blocked) |
| 7 | An impact, then pause (real `pause` event) on the next frame | `main.paused` is true; the burst `can_process()`; it still frees itself within lifetime + margin | A-R7 |
| 8 | End of each scenario | Burst count returns to 0 after the lifetime | F2 (no leak) |

**Two impacts inside 0.25 s need both fighters.** Bolt alone cannot land them:
- A jab is 0.35 s from press to idle, plus 0.07 s hitstop (`fighter.gd:37, 42`).
- A pop is 0.45 s.
- A hit puts the victim into HURT, which cancels its own attack, so two point-blank attacks cannot both land.

The test therefore uses two corks fired from range:
- Bolt at x 150 presses P (real input).
- Rivet at x 450 fires through its intent (the stand-in brain sets `intent.pop` for one frame, 6 frames later).
- The corks pass each other, because a cork only checks its target's hurtbox.
- They land 6 frames apart, inside the 15-frame lifetime.

Rivet is driven through its `intent`, the same path `rivet_brain.gd` uses in the real game. Rivet has no keyboard input in the game.

## Step 3: run the tests through the wrapper

- New: `test_impact_effect_state.gd` at 60.
- Existing:
  - `test_slice` at 60;
  - `check_props3d` at 60;
  - `test_rewind_tint` at 30, 60 and 144;
  - `test_materials` at 60;
  - `test_impact_effect_config` at 60.
- Real output shown; `git diff scripts/run-test.sh godot/shaders` must be empty.

## What the test proves, and what it cannot

- **Proves:** when bursts are created; which scene is used; where each burst is placed; how many exist; when they are freed; that they keep processing under `main.paused`. Headless runs do emit `finished` (probed).
- **Cannot prove** (human or strip checks):
  - how the burst looks (A-Look);
  - that it draws above the star and fighters on screen (A-R6, beyond the `z_index` value the config test reads);
  - that the star still shows alongside it;
  - contrast against the castle.

  A headless run draws nothing (CLAUDE.md, Headless facts).
