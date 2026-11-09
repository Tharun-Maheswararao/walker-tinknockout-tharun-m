# FACTCHECK.md — every on-screen and spoken claim, with its source

Game source and docs shown: commit `c844ab2` (HEAD of `main` when the film was built). `_tools/build_sheet.py`
asserts that every shown file and folder (`godot/effects`, `main.gd`, the generated shader, the six docs,
`captures/`, `evidence/a6/`, `logs/`) is identical to `c844ab2` in the working tree. Every on-screen quotation
in the composites passes `Q()` in `_tools/make_media.py`, which asserts it is verbatim in its source file. The only
normalisation is `**`/backticks removed and whitespace collapsed. `…` separates verbatim parts.

| Beat | Claim | Source / verification |
|---|---|---|
| B00 | tin wind-up toys boxing in an empty goldfish bowl | CONCEPT.md; A3 and A5 films (same wording) |
| B00 | the prompt on screen is an illustrative reconstruction | stated on screen and in narration; no saved Walker transcript is shown |
| B00, B21, B23 | textures written by code, no third-party art | SOURCES.md "Assignment 6", Textures; `godot/effects/textures/ATTRIBUTION.md` |
| B01 | headless tests prove behaviour; not the look or the GPU cost | CLAUDE.md "Headless facts"; TEST-REPORT A6-2, A6-3 ("What the state test cannot show"), A6-4 |
| B02 | every attack spends wind | CHANGE-BRIEF B.1 Value (`_spend`, `fighter.gd:242-244`); `fighter.gd` ATTACKS `cost` |
| B02 | A's job: "gives the hit distinct visual weight and better readability across different arena backgrounds" | CHANGE-BRIEF A.1, verbatim |
| B02 | A's event: melee or cork hit, both to `main._on_impact(p, blocked)` | CLAUDE.md Effect A bullets; `main.gd:217-222` |
| B02 | B: feedback loop at the back key; condition wind < 25; mapping clamp((25 − wind)/25, 0, 1) | CHANGE-BRIEF B.1; `main.gd:241-242`; README A6 |
| B02, B10, B16 | the film capture: scripted input, isolated copy, frames 141 and 252 | CAPTURE.md; `evidence/runs/play-capture-log.txt` |
| B03 | `impact_effect.tscn` lines 86, 28, 36–37 | file at `c844ab2`, verbatim (code_box reads the file) |
| B03 | blend_mode 1 is ADD; line 37 is the Core's draw material | `impact_effect.tscn:36-37, 90` (Core `material = SubResource("CanvasItemMaterial_bp8ig")`); config test log "Core draw material CanvasItemMaterial, blend ADD" |
| B03 | burst on screen in frame 10 itself | TUNING.md Effect A r0 table, frame 10 ("Matches: the burst is on screen in frame 10 itself") |
| B03 | shards in a ring below and beside the fist | TUNING.md r1 comparison, frame 15 |
| B03 | dummy renderer, no GPU particle process; headless price near zero by construction | CLAUDE.md "Headless facts", verbatim on screen |
| B04 | A.2 rows, the MIX/ADD split from Claude Code's review | CHANGE-BRIEF A.2 and authorship block, verbatim |
| B05 | lines 77–86 of `impact_effect.tscn` | GodotDevWorkbench props built from the file; `gamedev-evidence.json` excerpt (checked) |
| B05 | z_index 6 above the star at 5 | `impact_effect.tscn:77`; CLAUDE.md (`fx` at z_index 5, `main.gd:97-100`) |
| B05 | Shards material blends MIX | `impact_effect.tscn:5, 80` (CanvasItemMaterial with no blend_mode = MIX); config test "blend MIX" |
| B05 | Claude built the scene unedited; values from Tharun's brief; no code sets them | FRICTIONAL A6 ("Claude built Effect A unedited"); SOURCES.md A6 Who did what; CLAUDE.md Ownership |
| B06 | fixture, fixed seed, bursts at 10 and 11 | CHANGE-BRIEF D.1; `impact_preview.gd` header |
| B06 | Tharun looked first; his words | TUNING.md "Effect A, first look (before Claude read any strip)", verbatim |
| B06 | median drop 41; linear alpha fade leaves about a third | TUNING.md r0 reading, frame 15, verbatim |
| B06 | frames 20, 30, 50 empty | TUNING.md r0 table |
| B07 | before lines 7–8 / after lines 7–9 | `git show 45e986f^:godot/effects/impact_effect.tscn` and the file at `c844ab2` |
| B07 | prediction 10 / 12 / 15 / 20–50, and the risk | TUNING.md "revision 1: Claude's reading of r0 and prediction", verbatim |
| B07 | Tharun approved the change | TUNING.md ("Change (approved by Tharun)") |
| B08 | r1 captured by Tharun, same fixture and seed | TUNING.md r1 section |
| B08 | 41.3 → 105.7; count +16 %; frame 12 "Direction right, size wrong"; frame 10 "Almost … I had assumed age 0" | TUNING.md comparison table, verbatim |
| B08 | Tharun: faded smoothly, no snap or blink; Keep | TUNING.md "my verdict in the running game (Tharun)", verbatim |
| B08, B15 | comparison sheets assembled by Claude | TUNING.md (sheets named in Claude's readings); SOURCES.md A6 (Claude read and measured every strip; Pillow for strip trimming) |
| B09 | `main.gd:228-238`; star, shake, roll kept | file at `c844ab2`; `main.gd:217-222` |
| B09 | Claude wrote it from plan step3a, approved step by step | TEST-REPORT A6-2; `evidence/a6/step3a-plan.md`; SOURCES.md A6 |
| B10 | 8 jabs; every other jab blocked → grey burst; Rivet's hits burst | `evidence/runs/play-capture-log.txt` SPAWN lines (blocked at 116, 155, 191, 229) |
| B10 | Rivet's brain blocks every other visible attack | `godot/fighter/rivet_brain.gd` (block_toggle) |
| B10 | counter = live burst nodes | `_tools/film_play.gd` `bursts()`; nodes stay alive until freed after `finished`, longer than they are visible |
| B11 | B.1 and B.2 rows, verbatim | CHANGE-BRIEF B.1, B.2 |
| B11 | amount_ratio is the feature Effect A doesn't use | CHANGE-BRIEF B.1 and Claude's review note there |
| B12 | `wind_steam.tscn:35-43`; `main.gd:69-70, 241-242` | files at `c844ab2`, verbatim |
| B12 | the only effect value code sets is amount_ratio | CLAUDE.md Ownership; TEST-REPORT A6-3 ("Nothing else is set from code") |
| B13 | D.2 schedule: ratio 1 at 10, 0 at 50; frames 12–70 | CHANGE-BRIEF D.2; `captures/wind_steam/r0` |
| B13 | Tharun's first look (half of Bolt's height) | TUNING.md "Effect B, first look", verbatim |
| B13 | 18 × 27 view px, about ¼ of Bolt's 112 px | TEST-REPORT A6-5c, verbatim |
| B14 | "cut out immediately upon triggering the rewind state" | TUNING.md Effect B rev 1 (quoting TEST-REPORT A6-3), verbatim |
| B14 | rewind fixture added; frame 34 sliver; x scale to 15 % | TUNING.md r0 reading (`fighter.gd:272-273`); CHANGE-BRIEF revision D.3 |
| B14 | Tharun chose a holder over local_coords = false | TUNING.md "the change (Tharun's choice)"; FRICTIONAL A6 |
| B14 | `steam_mount.gd:31-35` | file at `c844ab2`, verbatim |
| B14 | Claude's prediction for r1 | TUNING.md, verbatim |
| B15 | 0 / 0 / 1021 / 0 … px; 1 of 7 rewind frames narrow; Tharun: tapered off smoothly; Keep | TUNING.md r1 comparison and verdict, verbatim |
| B16 | wind 16 → 0.36, 4 → 0.84; pause; Rivet's hit; 0.44, 0.04, 0 | `evidence/runs/play-capture-log.txt` (log frames 213, 227, 259–289, 291, 311, 319, 326) |
| B16 | steam keeps rising while paused; the only thing that moves | measured pixel difference, CAPTURE.md "Pause check" |
| B16 | process mode always from Main | CLAUDE.md (`main.gd:41`); CHANGE-BRIEF B-R4; TEST-REPORT A6-3 (pause row) |
| B16 | puffs fade over their life instead of vanishing | B-R2; TEST-REPORT A6-3 note (puffs keep drawing 13 frames after ratio 0); seen in the capture (frames 310–334) |
| B17 | converted in the editor by Tharun (490095f); not used by the game | TEST-REPORT "The process shader"; README A6; FRICTIONAL A6 |
| B17 | lines 7, 43, 258, 302, 315 | file at `c844ab2`, verbatim |
| B17 | B.3 spread 30.0° half-angle; gravity (0, −180, 0) | CHANGE-BRIEF B.3, verbatim (table cells, `|` shown as `·`) |
| B17 | value lives on the material resource | TEST-REPORT "The process shader", Tharun's note, verbatim |
| B18 | 136/0, 33/0, 44/0, 37/0 | re-run for this film, `evidence/runs/tests-c844ab2/*.log`; matches README A6 and TEST-REPORT A6-5 |
| B18 | spread 30 / gravity read back | `test_wind_steam_config_60fps.log` PASS lines |
| B18 | M1, M2 (Tharun ran them), M4, M5, M6 FAIL lines and counts; M3 not caught | `evidence/a6/mutations/*.log`; TEST-REPORT A6-1, A6-2, A6-3; SOURCES.md A6 ("ran both Step 2 mutations") |
| B18 | M1: no warning, effect still fired | TEST-REPORT A6-1, verbatim |
| B19 | cost table and comparisons | `evidence/a6/cost/cost_effects_60fps.log`, verbatim lines (case lines shown up to the wall clock) |
| B19 | two engine timers read 0 | same log (`proc`, `phys` 0.0000); TEST-REPORT A6-4 |
| B19 | GPU budgets A < 0.55 ms, B < 0.20 ms; reference 0.97 ms GPU / 0.11 ms CPU | CHANGE-BRIEF F, verbatim |
| B19 | screenshot is Tharun's, effects off | CHANGE-BRIEF F (`evidence/a6/visual-profiler-vulkan.webp`); SOURCES.md A6 ("took the Visual Profiler screenshot") |
| B19, B22 | GPU price not measured | TEST-REPORT A6-5 "GPU price (HUMAN CHECK) — open"; no GPU number for either effect is shown |
| B20 | five agent mistakes | CHANGE-BRIEF A6 revisions (main.gd:199); TEST-REPORT A6-3 (R vs S); TUNING Effect B first look (4× loop); TEST-REPORT A6-2 (test bug; F2 stated too broadly) |
| B20 | readings where Tharun's verdict differs; his statement | TEST-REPORT A6-5c, verbatim |
| B20 | dark stretch: "flecks pop cleanly", 42 vs 105, corrected | TEST-REPORT A6-5a and A6-5c |
| B21 | Who did what (A6) | SOURCES.md, verbatim on screen |
| B21 | drafting help: Claude 3.5 Sonnet | SOURCES.md A6; CHANGE-BRIEF authorship block |
| B22 | 5 mutations caught, 1 not | M1, M2, M4, M5, M6 failed; M3 passed (TEST-REPORT A6-2) |
| B22 | checked by eye: first looks, verdicts, backgrounds, scene load, walls | TUNING.md; TEST-REPORT A6-5a, A6-5b |
| B22 | uncertain: shards faint over dark (42 vs 105); Rivet rarely steams; hidden emitter not checked | TEST-REPORT A6-5a "Finding"; README A6 Known limitations; CLAUDE.md "Unconfirmed" (B-R5) |
| B22 | next step: GPU price per effect in gpu_price.tscn | TEST-REPORT A6-5 (open row); README A6 "GPU price" |
| B23 | Your Turn prompt and its prediction rule | written for this film (PROMPTS.md); the current values 42 / 105 are TEST-REPORT A6-5a |
| B22, B23 | revision c844ab2 | `git rev-parse HEAD` = c844ab2c13eda0288d0cee63e1789a0efcbd84f5 |
| B24 | title, @NikBearBrown | OUTRO-LOCK.md |

## Corrections made while building

- The first B16 narration had the rewind follow the pause directly. The log shows Rivet hit Bolt as play resumed
  (log frame 291, Bolt HURT) and REWIND began at 304. The narration now says so.
- B05's first excerpt (lines 76–88) clipped in GodotDevWorkbench (line 79 wraps). It is now 77–86, all visible.
- B10's counter counts burst **nodes**, which stay alive until freed (about 7 frames after the effect is no longer
  visible). The narration says "how many are alive" and does not claim two visible bursts overlap.
