# FACTCHECK.md — every on-screen and spoken claim, with its source

Game source shown: commit `2e6946d`. Docs and evidence read from the working tree at `93aedd9` (plus the uncommitted
FRICTIONAL.md / SUBMISSION.md edits, which this film does not use). Between `2e6946d` and `93aedd9` the only `godot/`
changes are the comment-only annotation of `standard_generated.gdshader` (`e4c188f`, Tharun) and the capture tool
`a5_capture_side_by_side.gd` (`b2b8780`); `_tools/build_sheet.py` asserts this and that the shown game files are
identical to `2e6946d`.

| Beat | Claim | Source / verification |
|---|---|---|
| B00 | tin wind-up toys boxing in an empty goldfish bowl | CONCEPT.md; A3 film (same wording) |
| B00 | prompt on screen is an illustrative reconstruction | stated on screen and in narration; no saved Walker transcript is shown |
| B00, B09, B17 | textures: Poly Haven "Metal Plate", Rob Tuytel, CC0 | SOURCES.md line 87; CHANGE-BRIEF A5.5 |
| B01 | headless tests prove the fade timing, not the look | TEST-REPORT A5-13; CLAUDE.md "Headless facts" |
| B02 | REWIND: cranks key and is open; a hit does 1.5× damage | CHANGE-BRIEF A5.1 (`fighter.gd:228-230`) |
| B02 | OS screenshot is Tharun's, during play, both fighters tinted | SOURCES.md "Who did what (A5)" (took the OS screenshot); TEST-REPORT A5-5 |
| B02 | OS screenshot carries the display colour profile; predictions checked against captures | evidence/a5/captures/os-screenshot/comparison.txt; TEST-REPORT A5-4 |
| B02 | the object is the toy box in `godot/prop_room/prop_room.tscn` | CHANGE-BRIEF A5.5; CLAUDE.md "3D object for the textured shader" |
| B03 | lines 3, 7, 8 of `rewind_tint.gdshader` | file at `2e6946d`, verbatim (GodotDevWorkbench props built from the file) |
| B03 | colour line is in CHANGE-BRIEF A5.2, written before the shader | CHANGE-BRIEF A5.2 "Colour line"; brief version note ("committed before either shader exists") |
| B03 | Claude suggested the colour line, Tharun typed it | SOURCES.md "Agent suggestions I adopted"; CHANGE-BRIEF A5 authorship note |
| B04 | captures are in-engine, scripted input | TEST-REPORT A5-4; `godot/tools/a5_capture_run.gd` header |
| B04 | predictions by hand, on paper | CHANGE-BRIEF A5.3 "Working, by hand"; SOURCES.md (computed the 18 pixel predictions by hand on paper) |
| B04 | 0.0 and 0.5: all 12 channels exact | evidence/a5/captures/pixel-samples.txt rows 0.0/0.5 (diff 0,0,0) |
| B04 | 1.0: four channels −1, all among the five half-way cases | pixel-samples.txt: A (−1,−1,−1), B (0,0,−1); CHANGE-BRIEF A5.3 note lists five .5 cases (A: 153.5, 123.5, 159.5; B: 170.5, 144.5). B's 170.5 read 171, so 4 of the 5 read one lower. **Note:** TEST-REPORT A5-4 says "exactly the five channels"; the samples show four. The film states four. |
| B04, B14 | at 2.0, both pixels pure tint (90, 160, 255): hint_range does not clamp a value set from code | pixel-samples.txt rows 2.0; TEST-REPORT A5-4 |
| B05 | driver lines 19, 27, 29 | `godot/fighter/rewind_tint_driver.gd` at `2e6946d`, verbatim |
| B05 | Claude wrote the driver in an agent session from a prompt Tharun approved | SOURCES.md "Agent sessions: ran sessions 1 and 2 (CLAUDE.md draft; driver and test). Drafted the implement prompt, which I approved." |
| B05 | fade-in 0.15 s, fade-out 0.30 s | CHANGE-BRIEF A5.2 R2; driver lines 9–10 |
| B06 | scripted-input capture made for this film; tint rises, Rivet's hit ends REWIND, tint fades | CAPTURE.md; evidence/runs/rewind-capture-log.txt (state 6 → 7 at log frame 106–108; value 1.0 → 0.6667 → 0.2222 → 0) |
| B06 | fade-out over three tenths of a second | brief R2; log: from 1.0 at frame ~106 to 0 within 9–10 frames at 30 fps |
| B06 | readout = value the driver set on each frame | film_rewind.gd prints `get_shader_parameter("rewind_amount")` each frame; offset (log = movie + 2) verified against Bolt's pixels, frames 86–91 |
| B07 | painted_tin lines 8–13 declare the uniforms; both .tres point at the shader on line 11 and differ on lines 15–16 | files at `2e6946d`, verbatim |
| B08 | shader edit uv_scale 2.5 → 6.0: both boxes changed (88 px, 1622 px), castle 0 | evidence/a5/captures/toybox/edit_checks/README.txt; 1_shader_edit.diff |
| B08 | material edit wear_amount 0.55 → 0.2: only the worn box changed (6698 px) | same README; 2_material_edit.diff |
| B08 | edits by Tharun; captures and measurements by Claude | edit_checks/README.txt; SOURCES.md (made the shader edit and the material edit) |
| B09 | lines 3, 4, 5, 20 of painted_tin | file at `2e6946d`, verbatim |
| B09 | skeleton suggested by Claude; Tharun typed the file and filled every blank | SOURCES.md "painted_tin.gdshader structure" |
| B09 | normal map is `_nor_gl` | SOURCES.md line 87; toybox_*.tres line 5 |
| B10 | 3×1 PNG 64/128/192, two quads, S source_color, D no hint | CHANGE-BRIEF A5.4 setup |
| B10 | predicted S 64/128/192, D 137/188/225 (by hand) | CHANGE-BRIEF A5.4; SOURCES.md (six hint-experiment predictions) |
| B10 | measured: the same six numbers | evidence/a5/captures/hint-samples.txt; TEST-REPORT A5-6 |
| B11 | sweep: each uniform of the fresh material at min/default/max; worn box unchanged | TEST-REPORT A5-7 |
| B11 | Tharun's read: paint_roughness no noticeable difference; others each do a visible job | TEST-REPORT A5-7 (Tharun's words) |
| B12 | generated lines 7 and 19, annotations by Tharun | `standard_generated.gdshader` at `93aedd9` (annotated in `e4c188f`, "Annotate the generated shader (Tharun): 9 lines, comments only") |
| B12 | equivalents: painted_tin lines 3 and 4 | LANGUAGE-NOTES.md Q6 |
| B12 | shader_type, hints, built-ins | LANGUAGE-NOTES.md Part A, Q1, Q3, Q4 |
| B13 | test_rewind_tint 50/50 at 30, 60, 144 | logs/test_rewind_tint_{30,60,144}fps.log (last lines, shown verbatim); TEST-REPORT A5-3 |
| B13 | test_materials 55/55, also after a fresh cache | logs/test_materials_60fps.log, logs/test_materials_60fps_fresh_cache.log; TEST-REPORT A5-9 |
| B13 | baselines: test_slice 25 checks 0 failed; check_props3d RESULT PASS | logs/test_slice_60fps.log; logs/check_props3d_60fps.log; TEST-REPORT A5-1 |
| B13 | mutations: semicolon 5 failed, rename 2 failed, source_color 1 failed | evidence/a5/mutations/*.log (FAIL lines shown verbatim); TEST-REPORT A5-2 |
| B13 | Tharun made the mutations and restored the shaders each time | SOURCES.md "Mutations: ran all three, and restored the shaders each time." (TEST-REPORT A5-2 says Claude ran the test; the film does not say who ran the test) |
| B13 | 45 and 48 driver checks still passed in m1, m2 | TEST-REPORT A5-2 "What the mutations showed"; 50 − 5, 50 − 2 |
| B14 | headless probe: set 2.0 → readback 2.0; headless runs draw nothing | evidence/a5/headless-facts.txt lines 3, 9; CLAUDE.md "Headless facts"; TEST-REPORT A5-13, A5-14 (dummy renderer) |
| B15 | contributions | SOURCES.md "Who did what (A5)", shown verbatim on screen; narration is a faithful shortening |
| B16 | fades, extend, both pauses, own material, at 30/60/144 | TEST-REPORT A5-3 |
| B16 | 18 hand predictions: 14 exact, 4 off by one | pixel-samples.txt (2 pixels × 3 values × 3 channels) |
| B16 | six agent mistakes caught, incl. the `--fixed-fps` cmdline bug | TEST-REPORT A5-10 (six rows) |
| B16 | uncertain: no METALLIC (M5); start up to 1/60 s late | godot/MATERIALS.md M5; TEST-REPORT A5-3 "Why the start delay exists", A5-14 |
| B16, B17 | next step / Your Turn: write METALLIC from the wear mask | film's proposal (Claude), following M5; not a recorded student decision |
| B17 | revision shown 2e6946d; voice is Kokoro TTS | this build (metadata.game.revision) |
