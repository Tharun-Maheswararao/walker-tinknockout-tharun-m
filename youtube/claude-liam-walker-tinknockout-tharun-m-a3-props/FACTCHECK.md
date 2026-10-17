# FACTCHECK.md — every on-screen and spoken claim, with its source

Game source shown: commit `1d93dcb`. Docs/evidence: working tree at `fd99467` (docs-only commits 0bc2b4d and fd99467
after 1d93dcb; `git diff --stat 1d93dcb fd99467 -- godot assets tools` is empty, asserted by `_tools/build_sheet.py`).

| Beat | Claim | Source / verification |
|---|---|---|
| B00 | Tin wind-up toys boxing in an empty goldfish bowl | CONCEPT.md "The game in two sentences" |
| B00, B02 | castle 1.80×0.82×2.30 m 156 tris; windkey 0.60×0.14×0.70 m 192; toybox 1.26×0.76×0.75 m 48 | CHANGE-BRIEF A3.2; evidence/check_props3d.txt; re-run today (evidence/runs/check_props3d-isolated-1d93dcb.txt, identical) |
| B00 | routes: castle + windkey Blender MCP, toybox script route | SOURCES.md "Assignment 3"; SUBMISSION.md; FRICTIONAL.md 2026-10-16 15:50 entry |
| B01 | the headless check proves measurements, not looks | tests/check_props3d.gd lines 6–7 ("What it does NOT show") |
| B02 | Bolt = 1.80 m; jobs and reasons for each prop; lid at Bolt's waist | CHANGE-BRIEF A3.1, A3.2 |
| B02 | prop_room.png is a real engine render, Claude-made | evidence/godot/prop_room.png; godot/tools/shot_prop_room.gd header; SOURCES.md A3 |
| B03 | 3ef263b (brief) precedes bec93b5 (first build commit) | `git log --reverse 9788922..1d93dcb` (rendered on screen from the live command) |
| B03 | Tharun chose assets/scale/dropped cork; Claude drafted; changes to draft: none | CHANGE-BRIEF A3 authorship note |
| B03 | A3.1 rules and A3.3 F1–F7 | CHANGE-BRIEF A3.1, A3.3 |
| B04 | `claude mcp add -e …` failed ("Invalid environment variable format: blender"); fix = name first | FRICTIONAL.md A3, 2026-10-14 tool setup |
| B04 | install-addon failed until Blender opened once | same entry |
| B04 | add-on needed a full restart ("No module named 'blender_mcp'") | same entry |
| B04 | Connected on port 9876; lsof: 127.0.0.1:9876 only | screenshot 01 (student's own); FRICTIONAL.md |
| B04 | first get_scene_info "Could not connect to Blender" at 21:40; worked at 21:45 (~4 min) | FRICTIONAL.md 2026-10-15 castle session (from transcript) |
| B05 | default cube Scale 1.000, Dimensions 2 m; became A3-F1 | screenshot 02 (student's own); FRICTIONAL.md ~22:50; CHANGE-BRIEF A3-F1 |
| B06 | the castle prompt text | session transcript, verbatim → evidence/castle-prompt.txt (see PROMPTS.md) |
| B07, B09 | code and line numbers | tools/blender/build_castle.py at 1d93dcb, verbatim (asserted in `_tools/make_evidence.py`) |
| B08 | four-view image from the MCP look tool in the student's live session | evidence/blender/03-castle-mcp-look.png; FRICTIONAL.md ("The look tool's four views are saved as …") |
| B08 | session reported 1.80×0.82×2.30 m, 156 tris; each part rotation 0, scale 1 | FRICTIONAL.md castle session; TEST-REPORT A3-2, A3-5 |
| B10 | castle Item tab: location 0, rotation 0°, scale 1.000, 1.8×0.82×2.3 m; Statistics overlay OFF | screenshot 07 (student's own, fd99467); TEST-REPORT A3-2 at fd99467 |
| B11 | lobe code lines 98–103 | tools/blender/build_windkey.py at 1d93dcb, verbatim |
| B12 | windkey: rotation 0°, scale 1.000, 0.6×0.14×0.7 m, Triangles 192/192, Material Preview | screenshot 06 (student's own, 0bc2b4d); TEST-REPORT A3-2/A3-5 at 0bc2b4d |
| B12 | auto mode denied call 0; Tharun approved it (16:09); numbers identical to script-route key | FRICTIONAL.md 2026-10-16 15:50–16:15 |
| B13 | toybox code, line 12 navy #23395B, line 17 save | tools/blender/build_toybox.py at 1d93dcb |
| B14 | navy band, rotation 0°, scale 1.000, Solid shading | screenshot 04 (student's own, Oct 15 11:46 PM) |
| B15 | Material Preview after first mistaking the X/Y/Z gizmo; slot toybox_navy; #23395B → #2E7D32; size unchanged; saved 00:11; Claude re-checked and re-exported | FRICTIONAL.md 2026-10-16 00:05–00:25; TEST-REPORT A3-9; screenshots 04/05 |
| B15, B16, B20 | check reads `surface 2 toybox_navy albedo=#2E7D32` | evidence/check_props3d.txt; re-run today; commit 08f96cd message |
| B16 | the student's sentence, verbatim | BLENDER-NOTES.md (0bc2b4d), also FRICTIONAL.md and TEST-REPORT A3-9 (asserted verbatim in make_media.py) |
| B16 | slot still named navy; build_toybox.py line 12 still navy so a re-run would save navy over the edit | Claude's observation, labelled as such; derived from build_toybox.py lines 12 and 17 |
| B17 | prop_room.tscn lines 33–43: camera (0,1.6,5.5), castle x −2.2, windkey origin, toybox x 2.0 | godot/prop_room/prop_room.tscn at 1d93dcb |
| B17 | export_yup=True | tools/blender/export_glb.py line 6 |
| B18 | real engine output, Movie Maker 3840×2160 from an isolated copy, scene unchanged; camera orbit added by a film script | CAPTURE.md; capture log evidence/runs/orbit-capture-log.txt |
| B19 | check lines 83–90 and header lines 6–7 | godot/tests/check_props3d.gd at 1d93dcb |
| B20 | RESULT: PASS (0 failing), identical to recorded output; room x ranges; Y = height | evidence/runs/check_props3d-isolated-1d93dcb.txt vs evidence/check_props3d.txt (diff empty, blank lines aside) |
| B21 | first check used global_transform outside the tree, got identity, falsely passed; fix to_root() | check_props3d.gd lines 30–40 comment; TEST-REPORT A3-8; FRICTIONAL.md ~23:15 |
| B22 | re-created bug: castle x −0.90..0.90, ERROR !is_inside_tree, RESULT PASS, exit 0 | evidence/runs/repro-global_transform.txt (throwaway copy, line 46 swapped) — labelled RE-CREATION |
| B22 | parse error → no RESULT line, exit 0 | evidence/runs/repro-parse-error.txt (throwaway copy, line 10 broken); TEST-REPORT A3-6 |
| B23 | render script hit the same not-inside-tree mistake; first view wrong camera; fixed | TEST-REPORT A3-7; shot_prop_views.gd lines 21–23 |
| B23 | proposal never appeared, yet "Approved. Build the castle as proposed … Don't save or export." | FRICTIONAL.md castle session (from transcript) |
| B24 | Tharun opened prop_room.tscn in the editor, orbited, F6, "everything works fine"; no screenshot | TEST-REPORT A3-7; FRICTIONAL.md 00:05–00:25 |
| B24 | six angles are Claude's renders; lid near-white; key small beside castle | TEST-REPORT A3-7 (Claude's observations) |
| B25 | checked/uncertain/next step | TEST-REPORT A3-2…A3-10; next step "a darker cream, or less sun energy" (A3-7) |
| B26 | credits | SOURCES.md "Assignment 3" — Who did what |
| B26 | prediction: band fails (brief navy vs .glb green) | CHANGE-BRIEF A3.2 + "A3 revisions (none yet)" vs check output; labelled a prediction |

## Corrections applied while building

* The stale draft (tag a3 / f4b5119) said "no hand edit", showed a navy band and one MCP asset; all of it was discarded.
* B01's first correction was authored as the phrase "look right"; the component only matches single words, so it never
  fired (seen in sampled frames). Changed to the single word `look` → `measure`; final sentence "The check proves they
  measure right." Typing sped up and type enlarged after GATE V flagged underfill (see _qc/HUMAN-REVIEW.md).
* B10 says the castle screenshot has the Statistics overlay off and takes no triangle count from it.
* The castle MCP-session numbers are attributed to "the session" (FRICTIONAL.md), not to a screenshot.
* No lesson is narrated as Tharun's except his own quoted sentence (0bc2b4d).
