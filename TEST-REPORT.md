# TEST-REPORT — Tin Knockout asset slice

- **Source revision tested:** `64c037a` (game code frozen here for the film)
- **Engine:** Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility, macOS 15.6 (Darwin 24.6.0), Apple M4
- **Date:** 2026-10-06

## 1. Startup and controls (fresh copy)

| Check | Result |
|---|---|
| Fresh clone → `godot --path godot` runs the title screen | ⏳ **to be confirmed on a fresh clone at submission** (section 9) |
| Enter → "ROUND 1" → bell → FIGHT | ✅ automated: `fresh()` in every test; screenshot `evidence/screens/02-round-intro.png` |
| A/D move, J jab, K cutlass, L pop-gun, I block, S rewind, Esc pause, M/N mute, R rematch, F1 hitboxes | ✅ automated input path for move, jab, cutlass, pop, rewind and pause (section 7). Block, mute keys, F1 and rematch are exercised by `godot/tools/shots.gd` and the capture driver. |
| Every state reachable by input | ✅ `evidence/screens/` (some shots **posed**: fighters placed, then a real key press; see `godot/tools/shots.gd`) |

## 2. Character against the sheet

**Sheet vs. in-engine poses:** `design/character/pose-targets.png` (spec) vs. `design/character/generated-poses.png` (the shipped sprites at game scale with the hurtbox drawn on).

| Rule (CHARACTER-SHEET) | Result |
|---|---|
| 1. Helmet ≈ 40 % of height | ✅ All 11 poses come from inits drawn at the spec proportions. Strength 0.6 keeps that layout. Visually ~38–42 %. |
| 2. One window, two eyes | ✅ after an edit: SDXL-Turbo lost the eyes at strength 0.6, so they are **painted on every pose** (logged). |
| 3. Key on the back | ⚠️ **Changed.** The generated art has a black nozzle where the key should be, so the key is now a separate prop (`PROP-KEY`) attached at the back anchor and spun by code during rewind. |
| 4. Outline weight | ✅ consistent within the s43 set |
| 5. Brass helmet, red riveted tin suit | ✅ |
| 6. Mitten gloves, no fingers | ✅ |
| 7. Profile facing right; left = runtime flip | ✅ automated: `walking left flips Bolt's sprite`; screenshot `state-walk-left-flipped.png` |

**Collision:**
- `evidence/screens/03b-jab-hit-boxes.png` and `state-cutlass-boxes.png` show the F1 overlay: green = 50×106 hurtbox, red = active hitbox.
- **Bug found and fixed here:** `evidence/screens/before-fix/03b-jab-hit-boxes-sprite-offset-bug.png` shows the sprites drawn about 80 px up and left of their hurtboxes. `Sprite2D` was centred *and* offset by the feet anchor. Fixed with `sprite.centered = false` (commit `d9c248d`).
- **Art beyond the box:** the antennae (about 12 px above), the extended jab glove and the cutlass reach past the hurtbox, as the sheet says. The KO pose's hurtbox is irrelevant because no hit registers during KO.

**Silhouette re-test with generated art:**
- `design/character/silhouette-generated-in-game.png`: the helmet, antennae and boots read at 112 px.
- ⚠️ **Facing is weaker than in the v1 silhouette.** Because the key is now a separate sprite, the solid-black shape only shows facing through the small back nozzle and the helmet bulge. The key prop restores the cue in play.

## 3. Storyboard against the slice

| Panel | Slice equivalent | Match / difference |
|---|---|---|
| 01 Closing time (wide, high angle, design) | `01-title.png` | **Different.** The slice title is a dimmed overlay on the arena at eye level, not a high-angle shot of the counter. ENV-TITLE was a stretch goal and wasn't made. |
| 02 Round start (gameplay) | `02-round-intro.png`, `02b-fight-idle.png` | ✅ ROUND 1 → FIGHT!, bell, full bars and dials. **Difference:** the arena is inside the bowl on the counter seen from outside, not the bowl's interior (see ASSET-LOG ENV-BOWL v2). |
| 03 Jab lands (gameplay) | `03-jab-hit.png`, `03b-jab-hit-boxes.png` | ✅ jab pose, spark, Rivet hurt, Rivet's bar drops, Bolt's dial ticks down |
| 04 Rewind close-up (design, low angle) | `04-rewind.png` | Gameplay shows it at medium distance (the gameplay camera never zooms). The key-spin is visible as the key narrowing and widening. |
| 05 Spring runs dry (gameplay, Dutch roll) | `05-spring-empty.png`, `05b-knockdown-hurt.png` | ✅ EMPTY! label, slump pose, knockdown. The camera roll (5°) happens on a knockdown. |
| 06 Back off and rewind (gameplay) | capture `fight-4k` + `06b-popgun-cork.png` | ✅ |
| 07 Knockout (design, low angle) | `07-knockout-win.png`, `07b-knockout-lose.png` | ✅ K.O., winner text, R to rematch, music stops. Shot at eye level, not low angle. |

## 4. Sound events: exactly one sound per occurrence (automated, `godot/tests/test_slice.gd`)

| Event | Check | Result |
|---|---|---|
| SFX-JAB | 8 presses in range → 8 hits, 8 sounds | ✅ |
| SFX-JAB, held | J held 1.5 s → 1 attack, 1 sound | ✅ |
| SFX-CUTLASS | 5 swings → 5 hits, 5 sounds | ✅ |
| SFX-POP | L held 1 s → 1 cork, 1 sound | ✅ |
| SFX-REWIND | held 2.0 s from 40 wind → exactly 6 clicks (one per 10 wind); no clicks after full | ✅ |
| SFX-EMPTY | once on entering EMPTY, not repeated while stalled | ✅ |
| SFX-BELL | once at round start, once at KO, not repeated on the KO screen | ✅ |

**Captured real play:** `evidence/film/fight-inputs.jsonl`. A 24.4 s scripted round produced bell 2, jab 13, cutlass 3, pop 1, rewind 26, empty 1.

## 5. Music

| Check | Result |
|---|---|
| Seam (automated, `tools/edit/check_seam.py`) | ✅ seam sample jump 0.0057 < 99th percentile of normal steps 0.1176; level change +0.77 dB |
| Loop flag on, playing during fight | ✅ automated |
| Spring < 25 % → slows (pitch 0.85) | ✅ automated |
| Pause → low-pass + −10 dB; unpause restores it | ✅ automated (bus effect state) |
| KO → stops | ✅ automated |
| **Human: ≥ 3 repetitions without a click** | ⏳ **PENDING: Tharun's listening check** (section 8) |

## 6. Muted play

- ✅ automated: **sound never decides state.** The same scripted fight run muted and unmuted ends in the identical state `[62.5, 83.0, 30.7, 23.0, 191.69, 287.03, 2]` (hp, wind, x positions, round state).
- Visual cues that replace sound:
  - HUD spring dials (they turn red below 25 %)
  - EMPTY! / rewinding / FULL / block labels above the fighters
  - a distinct pose for every state
  - hit sparks, hitstop and screen shake
  - K.O. text
- ⏳ **PENDING: human muted playtest** (section 8)

## 7. Automated checks

**Command:**
```bash
godot --headless --path godot --script res://tests/test_slice.gd
```

**Result at `64c037a`: 25 checks, 0 failed.**
- The first run had **8 failures**: `evidence/tests/run-01-setup-bug.txt`.
- **Cause, from a frame trace:** the test froze Rivet's brain 3 frames *after* the round started. In those frames Rivet fired a cork that interfered with every test.
- **Fixed in the test** (freeze before the round). I also added a gameplay change: a 1.5 s pop-gun cooldown at round start, because a cork on frame 1 felt cheap.
- No assertion or expected value was changed between the two runs.

**Seam check:** `python tools/edit/check_seam.py` → 2/2 PASS.

## 8. Human playtest (Tharun) — sound on, then muted

> ⏳ **PENDING.** This section must contain Tharun's own observations: music loop over ≥ 3 repetitions, whether each sound fits, low-spring slowdown, pause muffle, muted readability, anything confusing. **It is not filled in by Claude and no playtester is invented.** If it's still empty at submission, that is a known limitation, recorded in SUBMISSION.md.

## 9. Inspect → revise cycles (driven by observations)

| Observation | Evidence | Revision |
|---|---|---|
| Text-only prompts couldn't hold Bolt's identity (photoreal, porthole framing, colour bleed) | `design/rejected/CHAR-REF-v1…v4.jpg` | Switched to img2img from the spec sketch (v5–v7) |
| **F1 confirmed:** pose drift with plain sketch inits | `design/rejected/CHAR-JAB.jpg` | Inits copy the accepted reference's features; one seed for all poses (v2) |
| Sprite drawn off its hurtbox | `before-fix/…offset-bug.png` → `03b-jab-hit-boxes.png` | `sprite.centered = false` |
| SFX v1 trims started on noise; multi-hit clips | `evidence/sfx-scores.txt` → `sfx-scores-v2.txt` | Trim from the loudest transient |
| No generated EMPTY candidate falls in pitch | `sfx-scores-v2.txt` pitch_drop ≈ 1.0 | Pitch-fall edit, pitch_drop 1.18 |
| **Stun-lock:** EMPTY fired 6× in one dry-run round; a 0-wind fighter could be chain-stalled to KO | capture dry runs (FRICTIONAL) | HURT → IDLE always; 0-wind fighters can't walk; dry run → 1 EMPTY |
| **F4 partly refuted:** Rivet suit 2.35:1 vs real background (predicted 1.07:1) — but Bolt's yellow helmet vs the pink castle behind his start position is 1.02:1 luminance | `evidence/contrast-F4-recheck.txt` | **Not fixed.** Bolt stays readable by hue and the dark outline. Next step: move the start positions off the castle, or darken the castle |

## 10. Predicted failures (CHANGE-BRIEF section 4): outcomes

| # | Prediction | Outcome |
|---|---|---|
| F1 | Pose drift | **Confirmed**, then mitigated (ref-matched inits, one seed, painted eyes) |
| F2 | Hit sound fires twice | **Refuted** by test (the `has_hit` flag works) |
| F3 | Music loop clicks | **Automated check passes**; human listening pending |
| F4 | Rivet vanishes on the background | **Partly refuted** (2.35:1); a new low-contrast spot was found for Bolt |
| F5 | Rewind clicks every frame | **Refuted** by test |
| F6 | Unreadable muted | **Automated:** state is identical muted. Human check pending |
| F7 | Weapons don't sit in the hand | **Partly.** Cutlass and pop-gun attach at the computed hand anchor; the grip offsets were set by eye from one screenshot each, not measured per pose |

## 11. Honest limitations

1. **Sound effects and music were picked by Claude's signal analysis, not by listening,** because Tharun asked Claude to choose. The human listening check is section 8.
2. The background shows the bowl from outside; the concept said "inside the bowl".
3. Rivet is a deterministic pattern, not AI.
4. The eyes are hand-painted on every pose, and the win pose uses seed 42 rather than 43.
5. The 4K capture take differs from the 720p dry run, because `--fixed-fps 30` changes physics stepping. Both are genuine runs.
6. Low luminance contrast between Bolt's helmet and the pink castle (section 9).
