# FRICTIONAL — design log, Tin Knockout

Dated entries, written as the work happened. "Human" = Tharun (me). "Claude" = Claude Code (Opus 5.5): plans, prompts, code, code-drawn sketches. "Model" = the generative model named in the entry.

## 2026-10-05 — choosing the game

- **Wanted:** a game for the whole semester, not just this assignment, that is fun to play and where the art, sound and music all come from one idea.
- **Explored:** Claude proposed several directions (a tin wind-up toy, a hermit crab, a lantern moth). I asked about something like a friend's Spider-Man project. Claude pointed out that copyrighted characters are banned by the assignment, so I kept only the swinging *mechanic* as an option (a jumping spider). I then asked for fighting-game ideas, then car ideas, before choosing.
- **Decided:** **Tin Knockout**, a tin wind-up toy fighting game, because the spring-as-stamina idea gives every attack a cost and ties the mechanic to the sound (ratchet, clang) and the music (a music box that winds down). I added **swords, guns and other weapons**; we agreed they must be *tin toy* weapons (cutlass, cork pop-gun) to keep the world coherent, and that weapons are separate sprites so the pose count doesn't multiply.
- **Rejected:** reusing SPROCKET, my code-drawn character from Assignment 1. Claude suggested it for semester continuity; I wanted a more creative, new character. From four new options I chose **Bolt**, a tin deep-sea diver with a porthole face. Claude's argument that a round helmet is easier for an image model to repeat consistently was part of why.
- **Scope decision:** the assignment is due 2026-10-06 23:59, one day away. The slice is cut to Bolt vs a recoloured Rivet, three weapons, one arena. Real AI, more weapons and pickups are next steps.
- **Human / Claude / model:** decisions above are mine; options, trade-offs and the CONCEPT draft are Claude's, approved by me. No generative model used yet.

## 2026-10-05 — design docs before generation

- **Wanted:** a written spec that the generated images and sounds can be judged against.
- **Did:** CONCEPT, STORYBOARD (7 panels), CHARACTER-SHEET (12 poses), CHANGE-BRIEF. Sketches are **code-drawn by Claude** (`design/draw_design.py`), not hand-drawn and not generated; they define proportions, poses, the collision boxes and the palette.
- **Found before generating:** the contrast check (`design/character/contrast-table.md`) shows Rivet's verdigris suit at **1.07:1** against the planned gravel colour, so it would vanish. Bolt's outline and boots are weak (1.5–2.0:1) against the dark bowl. This became predicted failure F4 and a prompt requirement (a lighter background band and rim light).
- **Still unresolved:** whether SDXL-Turbo can hold Bolt's proportions across 11 poses (F1). I expect it won't on plain text prompts, so the plan is one reference image, then img2img or a pose sheet.

## 2026-10-06 — Bolt's reference image (ASSET-LOG CHAR-REF v1–v7)

- **Wanted:** one image of Bolt that passes the sheet's consistency rules (brass helmet ≈ 40 %, one window with two eyes, key on the back, mitten gloves) and reads as a flat illustrated tin toy, not a photo.
- **Asked / got:** SDXL-Turbo, txt2img, 4 steps, cfg 0.
  - **v1:** a long prompt gave **photos of real toys**. The prompt was over CLIP's 77-token limit, so "plain light grey background" was silently dropped. One seed came out solid black (an fp16 NaN on the Mac GPU).
  - **v2:** a shorter prompt with the style words first gave the right cartoon style, but **red helmets and no eyes**.
  - **v3:** adding "porthole" put the **whole picture inside a porthole frame**.
  - **v4:** "face window" made **the whole suit gold**.
  - **v5–v7:** I switched to **img2img from Claude's code-drawn spec sketch**. v5 strengths 0.5/0.6/0.7 gave identical images, because turbo runs int(steps × strength) = 2 steps for all three (a setting mistake, caught by comparing the outputs).
- **Decided:** Claude put up 4 finalists against the rules. **I chose s40 (v6, strength 0.75):** it passes 5 of 6 rules, fails only the eyes, and adds two antennae. Edit: eyes painted on the glass (`tools/edit/paint_eyes.py`). The "key" in the generated art reads as a black nozzle, so the key became a separate prop that code spins during rewind (pillar 1).
- **Human / Claude / model:** the choice was mine; the prompts, finalists and edit script were Claude's; the pixels came from SDXL-Turbo.
- **Still unresolved:** the reference has richer paint than the poses that came after it (next entry).

## 2026-10-06 — deriving 11 poses (CHAR-* v1, v2, v3)

- **Wanted:** the same Bolt in 11 poses (sheet P02–P12) at the same scale, so they line up with one hurtbox.
- **Got:** v1, with the plain sketch as init, made **a different diver for every seed**. This is predicted failure **F1, confirmed** (`design/rejected/CHAR-JAB.jpg`).
- **Changed:** the inits now copy the accepted reference's features (antennae, yellow gloves, grey glass), use 8 steps, and run at strengths 0.6 and 0.7.
  - v2 at 0.6 held the identity, but looked flatter.
  - v3 (0.75 and 0.85) brought back the rich paint *and* the drift.
- **Decided (Claude, by the sheet's rules; I didn't review each pose):**
  - **Consistency over detail:** 0.6 with seed 43 for every pose, because detail is lost at 112 px and drift is not.
  - The win pose at s43 had no raised fist, so I used s42.
  - The eyes were lost at 0.6, so they are painted on every pose, at a position computed from the sketch geometry.
- **Human / Claude / model:** the selection rule and code were Claude's; the outputs were SDXL-Turbo's. I did not review the pose picks one by one.
- **Still unresolved:** the poses are flatter than the reference image, and only 4 seeds were tried per pose.

## 2026-10-06 — sounds and music (SFX-*, MUS-WALTZ)

- **Wanted:** six one-shots that match "Tin you can hear" (clang, shing, pop, one click, wind-down, ding) and a waltz loop without a click.
- **Got:** AudioLDM 2 needed a compatibility patch to run with transformers 5. It filled every clip with several seed-shaped hits. Claude checked the patch didn't break prompt conditioning (two prompts on the same seed: correlation 0.21).
- **Decided:** I was asked to listen and pick, and **I asked Claude to pick for me.** Claude cannot hear, so it scored each candidate on attack, decay, number of hits, tonality and pitch drop (`tools/edit/score_sfx.py`, `evidence/sfx-scores*.txt`).
  - It re-trimmed every clip from the loudest hit, because v1 trims started on noise.
  - **It overrode its own scorer twice:**
    - cutlass `v2_s5` was a 13 ms tick, not a shing, so it took `s2`;
    - the bell's 25 "hits" were its shimmer, so it took `v2_s13`.
  - No EMPTY candidate fell in pitch, so it applied a pitch-fall edit.
  - Music: s2 had the cleanest 8-bar seam.
- **Human / Claude / model:** **the sound choices are Claude's analysis, not my ears.** I say this plainly here and in SOURCES. The outputs were AudioLDM 2 and MusicGen.
- **Still unresolved:** whether they *sound* right. That's my listening check in TEST-REPORT section 8.

## 2026-10-06 — building and testing the slice

- **Sprite / hurtbox:** the first screenshots showed the sprites about 80 px off their hurtboxes (`evidence/screens/before-fix/`). Cause: a centred sprite *plus* a feet offset. Fixed with `sprite.centered = false`.
- **Tests:** the first run had **8 of 24 failing** (`evidence/tests/run-01-setup-bug.txt`).
  - A frame trace showed the cause: my test froze Rivet's brain 3 frames after the round started, and Rivet shot a cork in that window.
  - Fixed the test order. No expected value changed. I also added a 1.5 s pop-gun cooldown at round start.
  - Now 25/25.
- **Stun-lock (found by the film dry run):** EMPTY fired 6 times in one round. A hit at 0 wind went HURT → EMPTY → hit again, until KO. That's a real design bug, not a test artefact. **Rule change:** HURT always returns to IDLE, and a 0-wind toy can't walk, only rewind. Now 1 EMPTY per round.
- **F4 re-check on the real background:** Rivet's suit is 2.35:1 (better than predicted). But Bolt's yellow helmet against the pink castle at his start position is 1.02:1 luminance. **Not fixed**; recorded as a limitation and a next step.
- **Human / Claude:** all code and tests were Claude's. These observations come from Claude's screenshots and test runs.

## 2026-10-06 — scope and time (retrospective note)

The Claude app was closed overnight for longer than either of us realised. Work resumed at about 15:50 with 8 hours left. To fit the deadline, the film was handed to a separate Claude agent working from a written brief, while the docs were written in parallel. My own playtest and listening check happened (or didn't) as recorded in TEST-REPORT section 8.
