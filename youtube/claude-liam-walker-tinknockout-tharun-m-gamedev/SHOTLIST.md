# SHOTLIST.md — Tin Knockout, Taken Apart

Revision demonstrated: `64c037a` · 16 beats · 6:46.1 (406.10 s) · landscape 3840×2160 @ 30 fps · no captions

Durations are the measured narration (or, for B10, the source clip) rounded up to whole frames — the same
`render_duration_s` the compiler uses.

| # | Start | Dur | Act | Source | What is on screen | Label |
|---|---|---|---|---|---|---|
| B00 | 0:00.00 | 17.90 | ASK | Remotion `ClaudeComposerAsk` | Walker prompt describing this game; answered output lines | "RECONSTRUCTED PROMPT — illustrative, not a transcript" |
| B01 | 0:17.90 | 11.87 | BLUF | Remotion `BrutalistHesitantWriter` | Summary typed; "Sound decides the fight" corrected to "Sound follows the fight" | — |
| B02 | 0:29.77 | 31.60 | CONCEPT | still `evidence/B02-concept-pillars.png` | Real 4K engine frame (fight-4k 0:03) + the four CONCEPT.md pillars | "Real engine frame · scripted input" |
| B03 | 1:01.37 | 41.60 | ASSET TRACE | still `evidence/B03-jab-asset-trace.png` | CHAR-JAB: spec → init → candidates → raw → edited → in engine; prompt, model settings, edits, rejects | "(posed)" on the engine panel |
| B04 | 1:42.97 | 19.73 | CODE | Remotion `GodotDevWorkbench` | `fighter/fighter.gd` 71–74; cues on 72, 73 | "Godot editor reconstruction" + path/lines |
| B05 | 2:02.70 | 21.33 | RESULT | still `evidence/B05-before-after.png` | Same posed jab, before vs after the anchor fix, F1 hurtbox overlay | "POSED … F1 hitbox overlay" |
| B06 | 2:24.03 | 19.53 | CODE | Remotion `GodotDevWorkbench` | `fighter/fighter.gd` 202–214 (`_rewind`); cues 208, 211, 213, 206 | "Godot editor reconstruction" |
| B07 | 2:43.57 | 13.03 | RESULT | `media/B07.mp4` = fight-4k 10.50–23.51 s | Bolt REWIND at the wall, HURT, both rewinding, walk in, KO | "SCRIPTED INPUT · real engine capture" |
| B08 | 2:56.60 | 20.77 | CODE | Remotion `GodotDevWorkbench` | `audio/sfx.gd` 30–36 (`watch`); cues 31, 32, 33, 35 | "Godot editor reconstruction" |
| B09 | 3:17.37 | 17.13 | RESULT | `media/B09.mp4` = fight-4k 1.80–18.93 s | Opening exchange: JAB, BLOCK, HURT, POP, EMPTY tag; announces B10 | "SCRIPTED INPUT · real engine capture" |
| **B10** | **3:34.50** | **24.43** | **GAME AUDIO** | `media/B10.mp4` = fight-4k 0.00–24.43 s **with its own audio** | Full scripted round, title to KO; **no narration** | "GAME AUDIO — NO NARRATION · SCRIPTED INPUT" + sfx log line |
| B11 | 3:58.93 | 17.03 | CODE | Remotion `GodotDevWorkbench` | `tests/test_slice.gd` 207–212; cues 208, 209, 212 | "Godot editor reconstruction" |
| B12 | 4:15.97 | 27.97 | RESULT | still `evidence/B12-test-output.png` | Recorded test output (25/0) + `check_seam.py` + first-run note | "isolated copy of 64c037a" |
| B13 | 4:43.93 | 62.57 | VERDICT | Remotion `ClaudeVerdictArtifact` | Tested (incl. Tharun's playtest, TEST-REPORT.md) / uncertain / models | "VERDICT · revision 64c037a" |
| B14 | 5:46.50 | 55.10 | YOUR TURN | Remotion `ClaudeComposerAsk` | Walker prompt read aloud, prediction, credits | — |
| B15 | 6:41.60 | 4.50 | OUTRO | Remotion `ClaudeTitleOutro` | Locked card: exact title, @NikBearBrown, seeded mascot | voiced title + 1.0 s silent tail, no game audio |

## Code → result pairs (teaching contract `code-then-result-v1`)

| Code | Result | What the result shows |
|---|---|---|
| B04 fighter.gd 71–74 | B05 | Art drawn up-left of its hurtbox before; inside it after |
| B06 fighter.gd 202–214 | B07 | REWIND locks Bolt in place while the dial climbs |
| B08 sfx.gd 30–36 | B09 (+ heard in B10) | One event → one signal → one sound |
| B11 test_slice.gd 207–212 | B12 | 25 checks, 0 failed; muted == unmuted |
