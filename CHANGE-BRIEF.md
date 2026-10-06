# CHANGE-BRIEF — Tin Knockout asset slice

*Version 1 · 2026-10-05 · committed before any generation. Predictions are kept even if later refuted; results go in TEST-REPORT.md.*

## 1. Asset list

| ID | What | Source | Storyboard panels |
|---|---|---|---|
| CHAR-REF | Bolt reference / turnaround (P01) | generated | all (consistency) |
| CHAR-IDLE | P02 fight stance | generated, derived from CHAR-REF | 1, 2 |
| CHAR-WALK | P03 walk | generated | 3, 6 |
| CHAR-JAB | P04 jab | generated | 3 |
| CHAR-CUTLASS | P05 cutlass swing (empty hand; blade is WPN-CUTLASS) | generated | 5 |
| CHAR-POP | P06 pop-gun fire (empty hand; gun is WPN-POPGUN) | generated | 6 |
| CHAR-BLOCK | P07 block | generated | — (in slice, not boarded) |
| CHAR-REWIND | P08 rewind | generated | 4, 6 |
| CHAR-HURT | P09 hurt | generated | 3 (Rivet), 5 |
| CHAR-EMPTY | P10 spring empty | generated | 5 |
| CHAR-KO | P11 knocked out | generated | 7 (Rivet) |
| CHAR-WIN | P12 victory | generated | 7 |
| RIVET-* | Rivet versions of every CHAR-* pose | **edit:** palette recolour of the accepted CHAR-* images | 1–7 |
| WPN-CUTLASS | tin cutlass prop | generated | 5 |
| WPN-POPGUN | tin cork pop-gun prop | generated | 6 |
| PROP-CORK | cork projectile | generated (or cropped from WPN-POPGUN) | 6 |
| ENV-BOWL | arena background: inside the empty goldfish bowl, gravel floor, plastic castle, seaweed, moonlit glass | generated | 2, 3, 5, 6 |
| ENV-TITLE | title background: the shop counter with the bowl, from above | generated (stretch: may reuse ENV-BOWL with a title overlay) | 1 |
| SFX-BELL | boxing-ring style bell, small and tinny | generated | 2, 7 |
| SFX-JAB | hollow tin *clang* | generated | 3 |
| SFX-CUTLASS | metallic *shing* plus clank | generated | 5 |
| SFX-POP | cork pop-gun *pop* | generated | 6 |
| SFX-REWIND | one ratchet click (played once per quarter-turn) | generated | 4, 6 |
| SFX-EMPTY | spring unwinding *wrrr-clunk* | generated | 5 |
| MUS-WALTZ | music-box / carnival-organ waltz loop | generated | 1–7 |
| UI-HUD | health bars, spring dial, text | **code-drawn** (not generated; doesn't count toward the requirement) | 2–7 |

## 2. Event-to-sound map

All sounds are played by an `Sfx` helper that **listens** to gameplay signals. Gameplay code never waits on, reads, or depends on audio. Muting just sets the bus volume, so the same signals still fire.

| Sound | Exact trigger (gameplay code that already represents the event) | Double-trigger prevention |
|---|---|---|
| SFX-BELL | `Round` state changes to `FIGHT` (round start) and to `KO` (round end) | Played from the state-*enter* handler only; a transition to the same state is ignored. |
| SFX-JAB | `Fighter.hit_landed(attack="jab")`, emitted when a jab hitbox first overlaps the opponent's hurtbox | Each attack instance has a `has_hit` flag. The first overlap sets it, emits once, and disables the hitbox. Later overlapping frames do nothing. |
| SFX-CUTLASS | `Fighter.hit_landed(attack="cutlass")` | Same `has_hit` flag per swing. |
| SFX-POP | `Fighter.projectile_fired`, when a cork is spawned | Firing uses `is_action_just_pressed` plus an attack lockout. Holding the key fires once; the next shot needs a new press after recovery. |
| SFX-REWIND | `Fighter.rewind_tick`, emitted each time accumulated rewind angle crosses a 90° boundary | Ticks come from a counter, not from frames: at most one per quarter-turn, regardless of frame rate or how long the key is held. |
| SFX-EMPTY | `Fighter` state *enters* `EMPTY` (spring reaches 0) | Edge-triggered on state entry. Staying empty does not re-fire it. |

## 3. Music behaviour

| Situation | Behaviour | How it's implemented |
|---|---|---|
| Round in progress | MUS-WALTZ loops seamlessly | OGG with loop enabled on import, loop point at a bar boundary |
| Bolt's spring < 25 % | Music slows and pitch drops (~0.85×) | Tween `pitch_scale` on the music player; back to 1.0 when wind ≥ 25 % |
| Pause | Quieter (−10 dB) and muffled | Enable a low-pass effect on the Music bus and lower its volume; reverse on unpause |
| Failure (Bolt KO) | Music stops on the KO bell | `stop()` in the KO state handler |
| Success (Rivet KO) | Music stops on the KO bell | Same handler: the end of a round always means silence |
| End of slice / rematch | Silence until R; a rematch restarts the loop from the top | Restart on `Round` entering `FIGHT` |
| Mute | `M` toggles music, `N` toggles effects, separately | Bus mute on `Music` / `SFX` buses |

## 4. Predicted failure cases

| # | Prediction | How I will check it |
|---|---|---|
| F1 | **Pose drift:** SDXL-Turbo poses drift from the reference (helmet too small or too big, two portholes, key missing or on the front). | Scale each pose to 112 px and overlay it on CHAR-REF. Measure the helmet/height ratio (must be 33–47 %). Check consistency rules 2 and 3 for each pose. Rejects go on the contact sheet. |
| F2 | **Hit sound fires more than once per attack** because the hitbox overlaps for several physics frames. | Automated test: a scripted input sequence of N jabs and N cutlass swings into a stationary opponent. Assert `SFX-JAB count == jabs that hit` and the same for the cutlass. |
| F3 | **Music loop clicks at the seam.** | Listen to at least 3 repetitions (human). Plus an automated check on the exported OGG: the sample jump and the RMS difference across the seam must be under a threshold. |
| F4 | **Rivet (copper and verdigris) disappears against the bowl.** The palette check already shows a 1.07:1 contrast between Rivet's suit and the planned gravel. | Measure luminance contrast between each fighter's main colours and the real generated background behind them. Squint test on a muted screenshot. Fix by recolouring Rivet or regenerating the background with a lighter band. |
| F5 | **Rewind clicks fire every frame** while the key is held (a machine-gun buzz). | Automated test: hold Rewind for exactly 2.0 s. Assert ticks == floor(rewound angle / 90°). |
| F6 | **Muted play is unreadable:** you can't tell idle from rewinding, or empty from hurt. | Muted playtest (human) plus side-by-side state screenshots. Each state must be identifiable without sound or HUD text. |
| F7 | **Weapon sprites don't line up with the hand** in generated poses (the anchor moves between poses). | Measure the hand anchor per pose after generation and store the offsets in code. Visually check every weapon pose in-engine. |
