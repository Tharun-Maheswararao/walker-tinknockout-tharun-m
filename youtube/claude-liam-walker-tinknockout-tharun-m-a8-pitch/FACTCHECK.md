# FACTCHECK.md — every claim in the A8 pitch film, with its source

Sources: `pitch/PROJECT-BRIEF.md` and `pitch/EXISTS-FACTS.md` at `fcb873c`; the game at tag `a7` (`a0c95cc`);
`TEST-REPORT.md` at `a0c95cc`; this film's own captures and test re-runs (`evidence/runs/`). Tense rule: past or
present tense only for what exists at a named tag; "will" for everything else. Pictures of things that do not exist
carry a CONSTRUCTED label on screen.

| Beat | Claim (narration or screen) | Status | Source |
|---|---|---|---|
| B00 | A fighter controller and animation state machine for Godot 4; moves written in frames, pinned by tests a stranger can rerun | exists (the controller, the frames, the tests) | BRIEF §1; EXISTS-FACTS §2 |
| B00 | "This is my game at tag a7, from scripted input" | real capture | `CAPTURE.md`; `evidence/runs/play-capture-log.txt` |
| B01 | macOS training-room build with a dummy and a frame-data overlay; reusable `Fighter.tscn` | **will** — picture labelled CONSTRUCTED, "Neither exists yet" said and stamped | BRIEF §1; EXISTS-FACTS §4 (no build, no `.tscn`) |
| B01 | Today the rig nodes are built in code (`fighter.gd` 88–119) | exists | `fighter.gd` at `a0c95cc`; CLAUDE.md "The rig" |
| B02 | Line 42 jab 0.07 / 0.10 / 0.18 s; line 43 cutlass 0.14 / 0.12 / 0.30 s | exists, verbatim excerpt (checked) | `godot/fighter/fighter.gd:41-45` at `a0c95cc` |
| B02 | Measured 5 / 6 / 10 ticks (jab), 9 / 7 / 18 (cutlass) | measured, headless | EXISTS-FACTS §3; `evidence/a7/probes/probe_phase_ticks_*.txt` |
| B03 | Box opens on the jab's fifth tick; landed, hitstop holds both fighters, the clip holds | observed in this capture's log (tick e+5, hitstop 5 ticks) | `evidence/runs/play-capture-log.txt`; TEST-REPORT A7 pins |
| B03 | Gap measured 0 s on my Apple M4 | measured, windowed (machine named) | TEST-REPORT A7-9e CLOCKS line (quoted via `Q()`) |
| B03 | K: the cutlass lands nine ticks in | observed in this capture's log (hitstop starts on e+9) | `evidence/runs/play-capture-log.txt` |
| B04 | Re-run on a clean copy of a7: pins 49, structure 57, edges 70, none failed | recorded output, re-run 2026-11-24 | `evidence/runs/tests-a0c95cc/` |
| B04 | Every new move will join the same tests | **will** | BRIEF §2 |
| B05 | Overlay drawing the jab's frames as they happen | **will** — CONSTRUCTED overlay drawn over a real a7 frame, labelled in the picture | BRIEF §3; EXISTS-FACTS §4 |
| B05 | One command confirms the frames: `test_a7_edges.gd 60` → "70 checks, 0 failed" | exists, recorded output | `evidence/runs/tests-a0c95cc/test_a7_edges_60fps.log` |
| B06 | Tharun has played Street Fighter 6 and Tekken 8; far larger finished games; frame data the player reads vs a state machine and tests a programmer opens | Tharun's comparison (named only, no footage or art) | BRIEF §4; `pitch/SOURCES.md` |
| B07 | Wind-up spring drained by every move; rewind by holding S; open while cranking | exists (game mechanic), real capture | BRIEF §4; `godot/game/controls.gd` (rewind = S); capture log (wind climbs while REWIND) |
| B08 | Target role gameplay programmer; reader a lead gameplay engineer or hiring manager; four first-minute steps | role/reader: Tharun's choice; steps: **will** (labelled WILL) | BRIEF §5 |
| B08 | One command prints "70 checks, 0 failed" today | exists, recorded output | `evidence/runs/tests-a0c95cc/` |
| B09 | One authority per animated node, clips synced to state_t (A7-6); pins before/after (A7-2); edges (A7-7); mutations in worktrees (A7-5); seam bug caught by a fixture log (A7-9a) | exists at a7 | BRIEF §6; TEST-REPORT A7 |
| B09 | Two clocks on Apple M4: display 129 fps, physics 60 ticks/s, gap 0.000000 s | measured (TEST-REPORT A7-9e, quoted via `Q()`) | EXISTS-FACTS §3 |
| B09 | Shaders and particles that read the fighter, never write it (a5, a6) | exists. Wording note: the A5 tint reads `fighter.state` each frame and the A6 effects listen to `hit_landed` / `wind_changed`; BRIEF says "listens to the state machine's signals", so the film says "read the fighter's state and signals" | `rewind_tint_driver.gd`, `main.gd:63-74` at `a0c95cc` |
| B09 | Will add an edge suite and tuning entry per move, a reusable-scene test, a measured build frame rate | **will** | BRIEF §6 |
| B10 | Out / In / First, and how anyone will know it ran (49, 57, 70 against the new scene) | **will** (counts are the a7 counts) | BRIEF §7 |
| B11 | main.gd drives the fighter: line 181 calls its step; main sets opponent (80–81) and spawn_cork (61) | exists, verbatim excerpt (checked) + source notes | `godot/game/main.gd` at `a0c95cc` |
| B12 | Pins lock the boundaries at 60 and 30 (49/0 each, re-run); the refactor will not be committed unless they pass with identical logs | re-run output exists; the rule is **will** | `evidence/runs/tests-a0c95cc/`; BRIEF §7 |
| B12 | Forward+ on Vulkan; the macOS build will be tested on the M4 before any claim; no web build | renderer exists; the rest **will** | EXISTS-FACTS §4–5; BRIEF §7 |
| B13 | Have: shaders (a5), particles with measured cost (a6), pinned state machine (a7), directing an agent (every a7 commit). New: reusable scene, input buffer, overlay, export with frame-rate measurement. Unknown: AnimationTree, cutlass both ways | Tharun's account; tags checked | BRIEF §8 |
| B14 | Exists today / will exist lists | as BRIEF's two lists, with tags | BRIEF "Exists today" / "Will exist"; EXISTS-FACTS §1 |
| B15 | Title, student, a real a7 frame (the jab landing), "Exists at tag a7; everything else: will", the TTS voice disclosure | real capture frame; disclosure true | `CAPTURE.md`; this file |
| B00 | Footer: the voice is Kokoro text-to-speech reading my script | true | `beat_sheet.json` (engine kokoro, am_onyx) |

## Not claimed anywhere in the film

No build exists and none is shown running; no frame rate for any build; no playtest by anyone else; no players,
quotes, studios or results; no GPU time; no footage or art from Street Fighter 6 or Tekken 8; no Claude response
(none is shown); no instructor name, persona, handle or credit line.
