# RIFF.md — observations → interpretation → narration

| Artifact + time | Visible observation | Interpretation (source) | Narration (gist) | Next experiment |
|---|---|---|---|---|
| B04 screenshot 01 | "Connected on port 9876", Disconnect button, asset libraries unticked | the socket is up on localhost; not yet proof Claude can drive Blender (FRICTIONAL) | three fixes, then a failed first get_scene_info, retry 4 min later | — |
| B05 screenshot 02 | Scale 1.000, Dimensions 2 m | scale is a multiplier, not a size (A3-F1) | "Scale one does not mean one metre." | — |
| B08 look image | keep, two 12-sided towers, cone roofs, door on one face | matches calls 1–6 and the brief's shapes | session reported 1.80×0.82×2.30 m, 156 tris | — |
| B10 screenshot 07 | location 0, rotation 0°, scale 1.000, 1.8×0.82×2.3 m; no stats overlay | call 7's origin and apply worked; tris not visible here | tris come from the session, not this picture | — |
| B12 screenshot 06 | rotation 0°, scale 1.000, 0.6×0.14×0.7 m, Triangles 192/192 | per-part rotation apply kept the key upright (A3-F2/F4 did not happen) | auto mode denied call 0; Tharun approved | — |
| B14/B15 screenshots 04/05 | Solid view navy band → Material Preview green band; slot toybox_navy; size unchanged | a colour edit needs the Material tab and Material Preview to be seen | Tharun's edit; gizmo confusion first | — |
| B16 | slot name and build script still say navy | the edit lives in the .blend/.glb only (Claude's observation) | re-running the script would undo it | update the brief or the script deliberately |
| B18 orbit 0–21 s | bases meet floor and shadows; door/latch face front; castle back plain | placement and orientation as the check says; the look is a human call | not the look check | — |
| B20 headless output | RESULT PASS, sizes = brief, min_y 0, room x ranges, band #2E7D32 | numbers verified; looks not | Y is height | — |
| B22 re-creation | ERROR lines yet PASS; castle at the origin; parse error exits 0 | a pass can test nothing; read RESULT, not exit code | "It tested nothing." | add a check that fails on engine ERROR lines |
| B24 six renders | lid near-white; key small beside castle | Claude's observations; readability at game size untested | Tharun: "everything works fine" | darker cream lid, then look again |
