# CHECKS-REPORT.md

19 beats (B00–B18), 422.3 s of measured narration (master 422.53 s). 0 slates. GATE V: 0 BLOCKER, 0 MAJOR.

Teaching arc: GAME/STATE/OBJECT ✓ (B02) | Q1 shader ✓ (B03 → B04, B05 → B06) | Q2 material vs shader ✓ (B07 → B08) |
Q3 texture is information ✓ (B09 → B10, B11) | Q4 the language ✓ (B12 → B13) | TESTS + LIMITS ✓ (B13, B14) |
CREDITS verbatim ✓ (B15) | BOOKENDS ✓ (composer → writer → body → verdict → Your Turn → locked outro).

Handout checklist (task brief items 1–7):
1. game, state (REWIND, vulnerable window), object (toy box, prop_room.tscn): B00, B02.
2. Q1 `rewind_tint.gdshader:7-8` (B03); Q2 one shader / two materials (B07); Q3 `painted_tin.gdshader:3-5` + hint
   experiment (B09, B10); Q4 shader_type, hints, built-ins, LANGUAGE-NOTES (B12).
3. colour line in CHANGE-BRIEF A5.2 (B03 note + narration); shader and driver lines (B03, B05); controlled-value
   captures beside predictions (B04); the effect in play (B02 OS screenshot; B06 new windowed Movie Maker capture).
4. hint experiment predicted vs measured (B10); interface sweep (B11); two materials and shader-edit vs material-edit (B08).
5. generated lines 7 and 19 beside painted_tin lines 3 and 4 (B12).
6. test counts (B13); three mutations (B13); headless-facts.txt (B14); TEST-REPORT "Assignment 5" (B13 subtitle, B16).
7. agent mistakes A5-10 (B16); uncertain: M5 and the 1/60 s start delay (B16); one next step (B16, B17); contributions
   verbatim from SOURCES.md (B15); texture source (B00, B09, B15, B17); revision shown 2e6946d (B03–B09, B16, B17).

Code → result: B03 → B04, B05 → B06, B07 → B08, B09 → B10, B12 → B13 (each result is the next beat).
`./art godot-gamedev --check`: PASS (`_qc/GAMEDEV-CHECK.txt`). GATE T: PASS (TYPECHECK.md). Composite selfcheck: 0 FAIL
(`_qc/SELFCHECK.md`).
