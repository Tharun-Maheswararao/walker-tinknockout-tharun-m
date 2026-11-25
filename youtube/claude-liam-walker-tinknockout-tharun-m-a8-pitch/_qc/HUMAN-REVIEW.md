# HUMAN-REVIEW.md — inspection of the A8 pitch master

Inspected by the Claude Code film session on 2026-11-24, by looking at the actual master's frames (not only the
probe). This is the agent's inspection. Tharun has not watched the film yet; his check is the list at the end.

## The master

- `exports/landscape/claude-liam-walker-tinknockout-tharun-m-a8-pitch.mp4`
- **SHA-256** `190ed4b2491eb0d0f70284ff7fb30a94624c87ef4dbdc0fb754a2fa9fc072cdc` (matches `.verified.json`)
- **221.57 s (3:41.6)**, 3840×2160, H.264, 30 fps, AAC 48 kHz stereo. Full decode: no errors.
- Footage revision: tag `a7` (`a0c95cc`), shown on screen on every real-play beat.

## Gates (render 4, the master)

| Gate | Result | Record |
|---|---|---|
| GATE T (`type_check.py`, run by `./art final`) | PASS, 0 FAIL | `TYPECHECK.md` |
| GATE T pixel checks on the 14 composites (`_tools/selfcheck.py`, real images masked) | 0 FAIL | `_qc/SELFCHECK.md` |
| GATE V (`final_frame_check.py`, run by `./art final`) | 0 BLOCKER, 0 MAJOR | `_qc/REPORT.md` |
| GATE F paperwork (FACTCHECK, SHOTLIST, PROMPTS) | present | reel folder |
| `./art godot-gamedev --check` | PASS: 9 source files, 164 exclusions, 4 components, 2 exact excerpts, 2 code→result pairs | `_qc/GAMEDEV-CHECK.txt` |
| Skin lint (warnings, not failures) | B00 not a Claude composer; B15 not `ClaudeTitleOutro` | deliberate: see BUILD-PROMPT "Departures" |

## Render history (corrections, recorded honestly)

1. **Render 1, refused by GATE V** (no file written): 2 MAJOR `underfill` on B15, a text-only title card filling 19 %
   of the safe area. Fixed by redesigning B15 around a large real a7 frame. `_qc/REPORT-render1-REFUSED.md`.
2. **Render 2, passed, superseded:** inspection found the compile's first-beat name overlay under B00's footer
   (below title-safe) and the game's own "rewinding" label clipped by B07's zoom. Removed the overlay
   (`channel_title` empty) and widened B07's zoom (same 16:9).
3. **Render 3, passed, superseded:** inspection found no on-screen disclosure that the first-person voice is
   synthetic. Added it to B00's footer and B15.
4. **Render 4: the master.**

Earlier, before any render: B01's sprite was drawn far too large and two captions collided (fixed); B10's FIRST column
used present tense for something that does not exist (reworded to "will"); B11's third source note ran into the panel
edge (dropped); the toolkit's `GodotDevWorkbench` stamps the instructor's handle in its corner, masked on B02 and B11
by `_tools/mask_handle.py` (the toolkit was not edited); the first test loop passed one argument per run and loaded
nothing (discarded, re-run with two).

## What I looked at, beat by beat (4K frames at 15 / 50 / 92 % in `_qc/master/`)

| Beat | Seen |
|---|---|
| B00 | Real play, label REAL PLAY · tag a7 (a0c95cc) · SCRIPTED INPUT; real-speed pass then 0.25× replay of the landed jab (Rivet HURT); SET positions and TTS voice disclosed in the footer. |
| B01 | CONSTRUCTED badge; training-room window drawing with the real Bolt idle sprite, a drawn dummy and overlay bar; scene-tree drawing; NOT BUILT YET stamp on "Neither exists yet"; caption says the nodes are built in code today. |
| B02 | Code view `fighter.gd:41-45` at a7, lines 42 then 43 highlighted on cue; measured ticks as a source note; no handle. |
| B03 | 0.5× whiff, 0.25× landed jab (readout: phase ACTIVE, hitstop HOLD), 0.5× cutlass; readouts from the capture log. |
| B04 | Terminal: the three count lines (49, 57, 70, 0 failed) read from the re-run logs; WILL card on cue. |
| B05 | CONSTRUCTED OVERLAY drawn inside a real a7 frame (jab tick 7, box live), cell 7 ringed; then the real command and "70 checks, 0 failed". |
| B06 | Two cards; Street Fighter 6 and Tekken 8 named only; footer: no footage or art from either. |
| B07 | Real play: Bolt in REWIND with the A5 tint, the game's "rewinding" label whole, wind readout climbing to 100. |
| B08 | Role and reader; four WILL steps light in turn; TODAY terminal line. |
| B09 | Four ledger rows lighting in turn with tags and TEST-REPORT ids; "Will add" footer. |
| B10 | OUT / IN · will / FIRST · will. |
| B11 | Code view `main.gd:180-182`, line 181 highlighted; lines 61 and 80–81 as source notes; no handle. |
| B12 | Pins at 60 and 30 (49 / 0 each), WILL rule card, renderer-risk card on cue. |
| B13 | HAVE (tags) / NEW TO ME / DON'T KNOW YET. |
| B14 | EXISTS TODAY with tags / WILL EXIST. |
| B15 | Real a7 frame of the jab landing (A6 impact burst visible), title, name, course, "Everything else: will", voice disclosure. |

**Audio:** every beat's narration mean −26.8 to −27.5 dB, peaks −2.9 to −10.4 dB (`_qc/master-review.log`); no music
or effects; the last 0.85 s is silent (−57.8 dB). I can read the levels; I cannot hear the voice's pronunciation.

## For Tharun to check when he watches

1. **The voice.** A synthetic male voice (Kokoro `am_onyx`) says "I'm Tharun Maheswararao" and speaks for you; the
   film says it is text-to-speech (B00 footer, B15). Check you are comfortable with that, and listen for
   mispronunciations: your name, "Fighter dot T S C N", "main dot G D", "a seven", "Forward plus", "Tekken eight".
2. **Every sentence is yours to stand behind.** The script follows PROJECT-BRIEF in order and shortens it. One wording
   differs on purpose: B09 says shaders and particles "read the fighter's state and signals, and never write it";
   the brief says they "listen to the state machine's signals". The A5 tint reads `fighter.state` each frame rather
   than listening to a signal (`rewind_tint_driver.gd`), so the film uses the accurate wording.
3. **The cutlass in B03** lands nine ticks after K is pressed (logged), and B08's step 4 promises its "different
   timing" in the overlay. Check that matches how you want to describe K.
4. **The CONSTRUCTED pictures** (B01, B05) show a training room, dummy and overlay you have not built. Check the
   labels are as clear to you as they are meant to be.
5. **Pace.** 703 words in 3:41; the beats are back to back with no pauses. If it feels rushed, the fix is cutting
   words, not adding gaps (the brief's content is all there).
6. **The film says nothing about** a build running, any build frame rate, other players, or GPU time.
