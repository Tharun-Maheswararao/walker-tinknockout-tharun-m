# SHOTLIST.md — what is on screen in each beat, and where it came from

Generated from beat_sheet.json (measured durations). Lane: REMOTION = toolkit composition; OWN = composite of real files / recorded output / real engine captures built by `_tools/make_media.py`.

| Beat | Act | s | Lane | On screen | Provenance label on screen |
|---|---|---|---|---|---|
| B00 | ASK | 17.19 | REMOTION ClaudeComposerAsk | composer types the reconstructed Walker ask; output lines land | RECONSTRUCTED PROMPT — illustrative, not a transcript |
| B01 | BLUF | 12.51 | REMOTION BrutalistHesitantWriter | writer types the overview; "looks" is struck and corrected to "fades" | — |
| B02 | SETUP | 19.69 | OWN setup | OS screenshot during play (Tharun) beside three cards; STATE card lights: REWIND, the vulnerable window, 1.5x damage; ring on the two blue fighters; OBJECT card lights: toy box in prop_room.tscn, in-engine capture | OS SCREENSHOT · Tharun, during play; IN-ENGINE CAPTURE |
| B03 | MECHANISM | 21.23 | REMOTION GodotDevWorkbench | godot/shaders/rewind_tint.gdshader:1-9 at reading size; line 3: rewind_amount: 0 to 1, set from outside; line 7: fragment(): runs once per pixel; line 8: the colour line: mix toward the tint | Godot editor reconstruction · verbatim at 2e6946d |
| B04 | RESULT | 22.85 | OWN pixels | four in-engine captures (scripted input) with pixel A and B marked; columns 0.0 and 0.5 light: predicted = captured; column 1.0 lights: four channels −1; column 2.0 lights: pure tint (90, 160, 255) | IN-ENGINE CAPTURE · SCRIPTED INPUT |
| B05 | MECHANISM | 20.12 | OWN code | godot/fighter/rewind_tint_driver.gd:17-30 at reading size; line 19 highlighted: one ShaderMaterial per fighter (R6); line 27 highlighted: target: 1 in REWIND, else 0; line 29 highlighted: move_toward at 1/0.15 or 1/0.30 per s × delta | SOURCE VIEW · not an editor recording |
| B06 | RESULT | 16.32 | OWN motion | capture/rewind-4k.mp4 frames 70–220 at real speed, logged rewind_amount readout; labelled 0.25× replay of frames 82–122 | MOVIE MAKER CAPTURE · SCRIPTED INPUT · made for this film; REPLAY labels |
| B07 | MECHANISM | 18.75 | OWN materials | painted_tin.gdshader:7-14 beside toybox_fresh.tres:9-16 and toybox_worn.tres:9-16; shader lines 8–13 highlighted; line 11 of both .tres highlighted; lines 15–16 of both .tres highlighted | SOURCE VIEW · not an editor recording |
| B08 | RESULT | 21.23 | OWN edits | before: fresh and worn boxes side by side (in-engine capture); after shader edit lights: both changed (88 px, 1622 px); after material edit lights: worn only (6698 px) | IN-ENGINE CAPTURES · windowed |
| B09 | MECHANISM | 26.68 | OWN code | godot/shaders/painted_tin.gdshader:1-5, 16-25 at reading size; line 3 highlighted: colour: source_color, decoded from sRGB; line 4 highlighted: normal map: hint_normal, directions; line 5 highlighted: roughness: plain data, no colour hint; line 20 highlighted: roughness becomes the wear mask | SOURCE VIEW · not an editor recording |
| B10 | RESULT | 21.31 | OWN hint | hint_quads.png (in-engine capture) beside the prediction table; predicted column lights; measured column lights: 6 of 6 equal | IN-ENGINE CAPTURE · windowed, Forward+ |
| B11 | RESULT | 17.60 | OWN sweep | sweep_contact_sheet.png (in-engine captures, windowed); paint_roughness row ringed | IN-ENGINE CAPTURES · windowed |
| B12 | MECHANISM | 29.80 | OWN language | shader_type / hints / built-ins cards (LANGUAGE-NOTES.md); standard_generated.gdshader lines 7 and 19 with Tharun's annotations; painted_tin.gdshader lines 3 and 4 linked to them | SOURCE VIEW · not an editor recording |
| B13 | TESTS | 34.19 | OWN tests | test counts (TEST-REPORT Assignment 5); mutation diffs and their FAIL lines (evidence/a5/mutations/); "45 and 48 driver checks still passed" highlighted | recorded output, verbatim |
| B14 | TESTS | 15.70 | OWN headless | evidence/a5/headless-facts.txt lines 1–12; line 9 highlighted: set 2.0 -> readback 2.0; capture at 2.0 beside it | headless-facts.txt; WINDOWED CAPTURE |
| B15 | CREDITS | 35.88 | OWN credits | SOURCES.md "Who did what (A5)" verbatim, two columns; Claude column lights | SOURCES.md · verbatim |
| B16 | VERDICT | 36.94 | REMOTION ClaudeVerdictArtifact | verdict artifact lines land | — |
| B17 | YOUR_TURN | 29.28 | REMOTION ClaudeComposerAsk | composer types the suggested prompt; prediction and credits land | — |
| B18 | OUTRO | 5.01 | REMOTION ClaudeTitleOutro | locked title card | — |

Total 422.28 s.
