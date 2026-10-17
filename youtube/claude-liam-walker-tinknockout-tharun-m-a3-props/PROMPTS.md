# PROMPTS.md — Tin Knockout, Three Props in Blender

## B00 — the opening ask (RECONSTRUCTED)

**Illustrative reconstruction, not a saved transcript.** Labelled on the card ("RECONSTRUCTED PROMPT — illustrative,
not a transcript") and in the narration. Required by the walker modifier ("Please use Walker to convert my game design
document about …").

> Please use Walker to convert my game design document about tin wind-up toys boxing in an empty goldfish bowl into
> three 3D props for my Godot game: a sunken-castle ornament, a spare winding key and a tin toy box, sized against Bolt
> at 1.80 m.

Card output lines are checkable facts (sizes/tris from evidence/check_props3d.txt; routes from SOURCES.md "Assignment 3").

## B06 — the real castle prompt (VERBATIM)

The prompt Tharun pasted into the castle build session ("Castle asset build (Assignment 3)", Claude Code session
transcript `068f5075-389f-4edd-99d4-87e0ab8b77f8`, message at 2026-10-16T01:40:25Z = 2026-10-15 21:40 EDT), copied
byte-for-byte to `evidence/castle-prompt.txt` and shown with its pasted line breaks:

```
We are using Walker's Game brief → Build → Playtest → Inspect → Revise → Export
workflow. Use the Blender MCP tools in my open Blender session. Read
CHANGE-BRIEF.md first (the "Assignment 3" section at the bottom).
Task: build only this asset: castle (ASSET 1), exactly as the brief specifies
(size in metres, origin, materials, triangle budget, 12-sided cylinders/cones).
Start from an empty scene with metric units; Blender is Z-up.
First call get_scene_info and tell me what is in the scene, then propose the
steps. Do not build yet.
After I approve: one execute_blender_code call per object. After each, call
get_scene_info with the location, size, rotation and scale fields and report
them. At the end, join the parts into one object named "castle", set its origin
to the base centre at (0,0,0), apply rotation and scale. Then show me the result
with the look tool, and report the triangle count.
Copy every execute_blender_code body, in order, into tools/blender/build_castle.py.
Add *.blend1 to .gitignore.
Do not use Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Hunyuan3D or Tripo,
and do not call generate_3d, search_assets or import_asset. Do not export
yet. Say what you could not verify.
```

Only this prompt was read from the transcript; no other transcript content is shown.

## B26 — Your Turn (read aloud)

> Please use Walker to add one check to check_props3d.gd that compares every surface's albedo with the hex colours in
> CHANGE-BRIEF.md A3.2, and tell me which surface you predict will fail before you run it.

Why this one: the brief's A3.2 still lists the band as navy `#23395B` and its "A3 revisions" section says "(none yet)",
while the hand edit made the exported band `#2E7D32` (check output, surface 2 `toybox_navy`). Every other surface's
albedo equals its brief hex (evidence/check_props3d.txt). So the stated prediction is "the toy box band", and the
viewer then makes a human decision: revise the brief or revert the edit. One bounded change, one test, one prediction.

## Narration

All narration is in `beat_sheet.json` (`narration_text`), voiced locally by Kokoro `am_onyx` (Liam, in for Bear).
B16 reads the student's own sentence (BLENDER-NOTES.md, docs-only commit 0bc2b4d) verbatim, attributed to him.
