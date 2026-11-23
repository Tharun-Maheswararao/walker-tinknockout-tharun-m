# FACTCHECK.md — every spoken and on-screen claim, with its source

Game source and docs shown: commit `a5978c0`. `_tools/build_sheet.py` asserts every shown file and folder
(`godot/animations`, `fighter.gd`, the generator, `assets/props`, `previews`, `tests`, `main.gd`, the seven docs,
`captures/jab_action`, `evidence/a7`, `logs`) is identical to `a5978c0` in the working tree, and reads every excerpt
from `git show a5978c0:<path>`. Every on-screen quotation in the composites passes `Q()` in `_tools/make_media.py`,
which asserts it is verbatim in its source file at `a5978c0` (normalisation: `*`, `**`, backticks removed, whitespace
collapsed; `…` separates verbatim parts). Table cells are parsed from the files (`md_rows`), not retyped.

| Beat | Claim | Source / verification |
|---|---|---|
| B00 | tin wind-up toys boxing in an empty goldfish bowl | the A3, A5, A6 films (same wording); `main.gd:1-3` ("empty goldfish bowl") |
| B00, B26 | prompts are an illustrative reconstruction / a suggestion | stated on screen and in narration; PROMPTS.md |
| B01, B07 | both clips run on the physics tick, put at `state_t` | `fighter.gd:339` (MANUAL), `:346-356`, `:197`; CHANGE-BRIEF §6 |
| B02 | every attack spends wind | `fighter.gd:42-44` (`cost`), `_spend` `:284-286` |
| B02 | routes, nodes, authority, loops / commits of both clips | TEST-REPORT "The two clips" table, verbatim cells on screen |
| B02 | one turn a second | README A7 ("one turn per second"); CHANGE-BRIEF §3 |
| B02 | nothing the player presses can stop the jab | CHANGE-BRIEF §4 "What the player may do: Nothing"; TEST-REPORT A7-7 (move, block, rewind ignored) |
| B03 | lines 22, 26, 27, 29 of `jab_action.tres` | file at `a5978c0`, checked excerpt (gamedev check) |
| B03 | nothing checks the path when the file loads | mutations README: M1, "nothing about the broken track" |
| B04 | rotatoin; engine silent; game ran with the track inert; exits 8 and 2; 8 of 48 failed | `evidence/a7/mutations/README.md` and its two M1 logs, verbatim on screen |
| B05 | one writer per rig node | `fighter.gd:64-73` comments; CLAUDE.md "One authority" table |
| B05 | line 306 facing on FacingPivot; 313 anchor without facing | `fighter.gd:306, 313` |
| B06 | the source scan and its PASS lines; 13 writes (6 `_ready`, 4 `_load_art`, 3 `_apply_pose`); largest gap 0.00000 | `evidence/runs/tests-a5978c0/test_a7_structure_60fps.log` (re-run); the count is of the logged list |
| B06 | held frame: x +14.00, rot +0.120, KeyBob −2.00, clip 0.0833 = state_t | film capture log, tick 159 |
| B07 | line 339 MANUAL; 347 at the end of step; 351 JAB only; 354 seek to `state_t` clamped | `fighter.gd` at `a5978c0`, checked excerpt 346–356 |
| B08 | jab lands on e+5; clip 0.0833 held five ticks, then 0.1000 | film capture log ticks 249–262 |
| B08 | CLOCKS line; 129 fps; 279 JAB ticks; gap 0; picture trails by under one tick | TEST-REPORT A7-9e, verbatim (measured by Tharun) |
| B09 | phase table rows; key table rows; −6 / +14 / frame 11; 32-bit floats, half a frame | CHANGE-BRIEF §4, `evidence/a7/jab_action_keys.md`, verbatim cells |
| B10 | fixture at x 207, jab on frame 10, 60 fps, captured by Tharun | CHANGE-BRIEF §9; TEST-REPORT A7-8 |
| B10 | frame 15 the largest move | TUNING.md r0 reading ("a 15 px jump in one frame, the largest move in the clip") |
| B10 | pose under each frame | `logs/jab_preview_r0.log` |
| B10 | Tharun's first look | TUNING.md, verbatim |
| B11 | recipe; lines 39, 44, 47 | CHANGE-BRIEF §2; `generate_key_sheets.gd:37-47` |
| B12 | 672 × 60, 8 × 1; cells 2 and 6 at the 0.15 minimum | ATTRIBUTION.md table; generator `MIN_W` and θ = k·45° |
| B12 | centred at 41.5 or 42.0 of 84 | TEST-REPORT A7-9c, verbatim |
| B12, B24, B26 | SDXL-Turbo, Tharun's prompt, Stability AI Non-Commercial Research Community License, resize and mirror only | ATTRIBUTION.md; SOURCES.md A7, verbatim |
| B13 | lines 5, 6, 7, 11, 15, 17 of `wind_key_cycle.tres`; continuous sweeps through every cell; no key at length | file at `a5978c0`; CHANGE-BRIEF §11 answer 2 and §3, verbatim |
| B14 | wind topped to 50 each tick; one turn a second; seven or eight ticks per cell | `key_cycle_preview.gd:6-11`; capture log (cells change every 7 or 8 ticks) |
| B14 | Tharun's seam check | TEST-REPORT A7-9a, verbatim |
| B15 | Claude's reading of r0; the one change; the prediction | TUNING.md revision 1, verbatim; git `8a9dbed^` vs `a5978c0` line 15 |
| B16 | log exactly those values; frames byte-identical; Keep; opens revision 2 | TUNING.md r1 comparison and Tharun's verdict, verbatim |
| B17 | from Tharun's play; r0 reading had not flagged it | TEST-REPORT A7-9f, verbatim row |
| B17 | frames 10 → 11; −23 window px; about 2.5; +12 / 0.10 / −1.75; predictions −8 and 4.3 | TUNING.md revision 2, verbatim; git `a1d6072^` vs `a5978c0` lines 17, 29, 41 |
| B18 | −7.7; 3.4 to 4.3, mean 3.9; about 10 %; −30.1 (r1 −28.4) | TUNING.md r2 comparison, verbatim cells |
| B18 | Tharun's observation after r2 | TUNING.md, verbatim |
| B18 | "Recorded verdict: keep" | TEST-REPORT A7-8 "Verdict (Tharun)" column (Keep); FRICTIONAL "my verdict: keep (a1d6072)". TUNING.md's revision-2 section has no separate "Verdict:" line |
| B19, B20 | the scripted-input capture, cases, ticks, SETUP | CAPTURE.md; `evidence/runs/play-capture-log.txt` |
| B19 | gap 90 whiffs (reach 54), cutlass reach 78 on its 9th tick | `test_a7_edges.gd:188` comment; log |
| B20 | hits on e+3, e+7, e+15; rig at rest, no clip on the hit tick | capture log ticks 347, 446, 549; TEST-REPORT A7-7 |
| B20 | wind 40, six clicks, a turn and a half, holds, frame 0 on release | capture log ticks 625–776; `fighter.gd:31` (10 wind per click) |
| B21 | 26, 58, 57 (60 and 30), 70, 49 (60 and 30), all 0 failed | `evidence/runs/tests-a5978c0/` (re-run on a clean copy) |
| B21 | M1 8 and 2; M2 2; M3 5 and the plain ERROR; M4 passed, nothing imported | TEST-REPORT A7-5, verbatim cells |
| B21 | a headless run draws nothing | CLAUDE.md Headless facts, verbatim |
| B21 | the four planned pin updates; test_slice 25/0, test_wind_steam_state 37/0 | TEST-REPORT A7-3; re-run logs |
| B22 | the mistakes; the seam bug's cause and why the suite was green; 3 failed before, 0 after | TEST-REPORT A7-11, A7-9a, verbatim; `evidence/a7/seam/structure_*_fix_60fps.log` |
| B23 | Claude's reading vs Tharun in play | TEST-REPORT A7-9f rows, verbatim |
| B23 | Tharun's checks and his "In my words" | TEST-REPORT A7-9b, c, d; FRICTIONAL.md, verbatim (narration quotes A7-9b's and A7-9d's opening words) |
| B24 | who did what; the brief's drafting | SOURCES.md "Who did what (A7)" and "Drafting help for the brief", verbatim on screen |
| B25 | counts; Keep, Keep; jab picture five frames early; one idle frame between mashed jabs; rewind fills within 2.5 turns; a startup image | TEST-REPORT A7-1..A7-12 (A7-12 for the findings and "Fixing it needs a startup image (drawing)") |
| B26 | the suggested prompt | not run; PROMPTS.md |
| B27 | exact title, @NikBearBrown | OUTRO-LOCK |
