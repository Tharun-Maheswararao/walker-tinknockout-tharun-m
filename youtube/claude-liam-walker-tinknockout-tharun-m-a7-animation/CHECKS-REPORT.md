# CHECKS-REPORT.md

28 beats (B00–B27), 717.17 s of measured narration (master 717.50 s). 0 slates. GATE T PASS; GATE V 0 BLOCKER, 0 MAJOR.

The handout's list, and where each item is:
1. **Game, both clips, routes, which loops and which commits:** B00, B02 (TEST-REPORT "The two clips", verbatim).
2. **The four questions, each at a real line:**
   - what a clip is: `jab_action.tres:22-30` (B03, checked excerpt) → M1, the renamed property failing silently (B04);
   - one authority: `fighter.gd:64-73, 306-315` (B05) → the structure test's source scan, re-run (B06);
   - the two clocks: `_sync_clips`, `fighter.gd:346-356`, MANUAL at 339 (B07, checked excerpt) → the clip frozen with
     `state_t` through hitstop in play, and Tharun's CLOCKS line (B08);
   - feel in frames: CHANGE-BRIEF §4 phase table beside `evidence/a7/jab_action_keys.md` (B09) → the r0 strip (B10).
3. **The sheet, its slicing, the frame track that reads it:** generator 37–47 (B11) → both sheets 8 × 1, cell centres,
   source and licence (B12); `wind_key_cycle.tres:3-19` (B13) → the key turning, fixture capture (B14).
4. **Phase table beside key times; strip at each boundary; two revisions with prediction vs result and Tharun's
   verdicts:** B09, B10 (r0), B15–B16 (revision 1, r1), B17–B18 (revision 2, r1 vs r2).
5. **Both clips in real play, an interrupt in each jab phase:** B19 (whiff, landed hit with hitstop), B20 (cutlass
   hits in startup e+3, active e+7, recovery e+15; the key turning in REWIND and holding at full wind). Labels:
   SCRIPTED INPUT, FIXTURE, REPLAY, `repeat`, SETUP.
6. **What the read-backs proved, the mutations, what no headless run shows:** B21 (re-run counts; A7-4, A7-5; CLAUDE.md
   headless fact).
7. **Agent mistakes (A7-11, seam bug A7-9a):** B22. **Claude's reading Tharun overruled (A7-9f):** B17, B23.
   **Uncertain (A7-12) and one next step:** B25. **Human and AI contributions (SOURCES.md A7), sheet source and
   licence:** B24, B12, B26. **Revision shown (`a5978c0`):** B00, B25, B26, and on every source view.

Runs and gates: tests re-run on a clean copy (`evidence/runs/tests-a5978c0/SUMMARY.txt`, all at TEST-REPORT's counts);
`./art godot-gamedev --check` PASS (`_qc/GAMEDEV-CHECK.txt`); `_qc/SELFCHECK.md` 0 FAIL (+ `SELFCHECK-*.md` for the
re-made beats); GATE T PASS and GATE V clean (`_qc-final.log`, `_qc/REPORT.md`); master inspection `_qc/HUMAN-REVIEW.md`.

Corrections made during the build (recorded honestly):
- The first test loop passed "test fps" as one argument, which loads nothing and still exits 0 (the CLAUDE.md warning);
  re-run with two arguments. Only the second run's logs are kept.
- The key-cycle fixture's first Movie Maker run reported 373 of 380 frames (stale frames 10–16); discarded and
  re-captured (CAPTURE.md).
- B03 and B07 code panels first cut off their key line; ranges / font size adjusted and re-rendered.
- The first `./art final` was refused by GATE V (5 MAJOR); fixed and re-rendered.
- B14 narration first said "five times" while six wraps are on screen; reworded and re-voiced.

Nothing was committed, tagged, pushed, uploaded or published. The reel folder is untracked. Decoded capture frames
(`media/_work/play`, `media/_work/key`, 4.4 GB) were deleted after the render; `BUILD-PROMPT.md` step 7 regenerates them
from the hashed captures.
