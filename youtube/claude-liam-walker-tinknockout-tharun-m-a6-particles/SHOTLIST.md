# SHOTLIST.md — what is on screen in each beat, and where it came from

Generated from beat_sheet.json (measured durations) by _tools/make_shotlist.py. Lane: REMOTION = toolkit composition; OWN = composite of real files / recorded output / real engine captures built by _tools/make_media.py.

| Beat | Act | s | Lane | On screen | Provenance label on screen |
|---|---|---|---|---|---|
| B00 | ASK | 16.90 | REMOTION ClaudeComposerAsk | composer types the reconstructed Walker ask; output lines land | RECONSTRUCTED PROMPT — illustrative, not a transcript |
| B01 | BLUF | 13.58 | REMOTION BrutalistHesitantWriter | writer types the overview; "cost" is struck and corrected to "behaviour" | — |
| B02 | SETUP | 31.29 | OWN setup | two held frames from the film capture (scripted input), each with a zoom of the effect; EFFECT A card lights: job, event, blocked variant; EFFECT B card lights: job, value, condition, mapping | HELD FRAME · MOVIE MAKER CAPTURE · SCRIPTED INPUT; zoom of the same frame |
| B03 | MECHANISM | 37.03 | OWN parts | three columns: one line of godot/effects/impact_effect.tscn each; EMISSION result: r1 frame 10, burst on screen at the trigger frame; PROCESS result: r1 frame 15, shards in a ring below the fist; DRAW result: r1 frame 12, the ADD core brightens the castle; headless fact (CLAUDE.md) lights | SOURCE VIEW; FIXTURE · HELD FRAME (r1) |
| B04 | INTENT | 22.85 | OWN intentA | CHANGE-BRIEF A.2 rows quoted verbatim; Contrast row lights; brief authorship note on the split; Scale and Variation rows light | CHANGE-BRIEF verbatim |
| B05 | MECHANISM | 21.10 | REMOTION GodotDevWorkbench | godot/effects/impact_effect.tscn:77-86 at reading size; line 77: z_index 6: above the star at 5 (A-R6); line 80: Shards material: blend MIX; line 86: amount 16 · lifetime 0.25 · one shot · all at once | Godot editor reconstruction · verbatim at c844ab2 |
| B06 | RESULT | 29.56 | OWN stripA | captures/impact_effect/r0 frames 10, 12, 15, 20, 30, 50 (fixture, held frames, zoom); Tharun's first look, verbatim; frame 15 ringed; Claude's reading: median drop 41; frames 20, 30, 50 marked empty | FIXTURE CAPTURE · HELD FRAMES · captured by Tharun |
| B07 | MECHANISM | 28.24 | OWN revA | git diff 45e986f: impact_effect.tscn Gradient, old line and new lines 8-9; prediction card: frames 10, 12, 15, 20-50; risk line lights: blink out | SOURCE VIEW · git 45e986f |
| B08 | RESULT | 31.40 | OWN cmpA | r0_vs_r1_sheet.png (top r0, bottom r1; frames 10, 12, 15, 20); frame 15 column ringed; row: 41.3 → 105.7, Matches; rows for frames 12 and 10 light; Tharun's verdict, verbatim: Keep | FIXTURE CAPTURES · HELD FRAMES · sheet assembled by Claude |
| B09 | MECHANISM | 27.28 | OWN code | godot/game/main.gd:228-238 at reading size; line 229 highlighted: normal or blocked scene; line 231 highlighted: child of Main at p; line 238 highlighted: restart() after add_child | SOURCE VIEW · not an editor recording |
| B10 | RESULT | 19.65 | OWN playA | capture/play-4k.mp4, the jab sequence at real speed, with a zoom on the hit point and a per-frame readout from the capture log; labelled 0.25x replay | MOVIE MAKER CAPTURE · SCRIPTED INPUT · made for this film; REPLAY labels |
| B11 | INTENT | 32.04 | OWN intentB | CHANGE-BRIEF B.1 rows quoted verbatim; Condition and Mapping rows light; Feature row lights: amount_ratio; B.2 scale row lights | CHANGE-BRIEF verbatim |
| B12 | MECHANISM | 22.49 | OWN codeB | wind_steam.tscn:35-43 beside main.gd:69-70, 241-242; lines 37-38 highlighted: amount 25, amount_ratio 0.0; lines 40, 42 highlighted: lifetime 0.6, local_coords true; main.gd line 70 highlighted; main.gd lines 241-242 highlighted | SOURCE VIEW · c844ab2 |
| B13 | RESULT | 26.94 | OWN stripB | captures/wind_steam/r0 frames 12, 20, 40, 55, 70 (fixture, held frames, zoom); Tharun's first look, verbatim; Claude's measurement: 18 x 27 view px, about 1/4 of Bolt | FIXTURE CAPTURE · HELD FRAMES · captured by Tharun |
| B14 | MECHANISM | 36.64 | OWN revB | Tharun's in-game observation (TEST-REPORT A6-3), verbatim; rewind strip r0 frames 31, 34, 38 (fixture, held frames, zoom); 34 ringed; godot/effects/steam_mount.gd:31-35, lines 33-35 highlighted; prediction card | FIXTURE · HELD FRAMES; SOURCE VIEW |
| B15 | RESULT | 29.14 | OWN cmpB | r0_vs_r1_sheet.png (top r0, bottom r1; frames 28-72); frame 34 column ringed: 1021 px differ; note: 1 of 7 rewind frames caught the key narrow; Tharun's verdict, verbatim: Keep | FIXTURE CAPTURES · HELD FRAMES · sheet assembled by Claude |
| B16 | RESULT | 31.38 | OWN playB | capture/play-4k.mp4 from the 7th jab to the end, zoom on the key, readout of wind, amount_ratio and paused from the capture log; PAUSED in the readout; puffs still move (the only pixels that change); Bolt HURT in the readout; REWIND in the readout; ratio 0.84 -> 0.44 -> 0.04 -> 0 | MOVIE MAKER CAPTURE · SCRIPTED INPUT · made for this film; REPLAY / HELD FRAME labels |
| B17 | MECHANISM | 30.50 | OWN shader | particles_generated.gdshader lines 258, 302, 315 beside CHANGE-BRIEF B.3 rows; line 258 highlighted, linked to spread 30.0; lines 302 and 315 highlighted, linked to gravity (0, -180, 0); Tharun's note: the value lives on the material resource | SOURCE VIEW |
| B18 | TESTS | 39.29 | OWN tests | test counts from the re-run logs (evidence/runs/tests-c844ab2/); mutation table with each FAIL line (evidence/a6/mutations/); M3 row lights: 44 checks, 0 failed, not caught | recorded output, verbatim |
| B19 | TESTS | 38.82 | OWN price | cost_effects_60fps.log table, verbatim; budget card (CHANGE-BRIEF F) and the effects-off Visual Profiler screenshot (Tharun); GPU PRICE: PENDING (not measured) lights | recorded output; OS SCREENSHOT · Tharun; GPU PRICE: PENDING |
| B20 | VERDICT | 45.75 | OWN against | five agent mistakes, each with its record; A6-5c rows: shard size, steam size; Tharun's statement, verbatim; dark-stretch row: corrected after measurement | repository records, verbatim |
| B21 | CREDITS | 36.60 | OWN credits | SOURCES.md "Who did what (A6)" verbatim, two columns; Claude column lights; texture sources (ATTRIBUTION.md) light | SOURCES.md · verbatim |
| B22 | VERDICT | 36.71 | REMOTION ClaudeVerdictArtifact | verdict artifact lines land | — |
| B23 | YOUR_TURN | 27.04 | REMOTION ClaudeComposerAsk | composer types the suggested prompt; prediction rule and credits land | — |
| B24 | OUTRO | 4.69 | REMOTION ClaudeTitleOutro | locked title card | — |

Total 716.91 s.
