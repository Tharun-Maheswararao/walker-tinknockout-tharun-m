# SOURCES.md — Tin Knockout, Three Props in Blender

## Revisions

* **Game source shown:** `1d93dcb89ebd16f1d09d423b2787087bebcded5a` (verified clean clone: `../../../a3-check`; the
  repo's `godot/`, `assets/`, `tools/` are identical, asserted by `_tools/build_sheet.py`).
* **Docs and student evidence:** working tree at `fd99467` — docs-only commits after 1d93dcb:
  * `0bc2b4d` — the student's hand-edit lesson (BLENDER-NOTES.md, FRICTIONAL.md, TEST-REPORT A3-9) and
    `evidence/blender/06-windkey-sidebar.webp`;
  * `fd99467` — `evidence/blender/07-castle-sidebar.webp` (Statistics overlay off).
* Nothing in the repo was edited, committed, tagged or pushed by this build.

## Real images shown (repo files, SHA-256 in `gamedev-evidence.json` where inside godot/; others below)

| File | Provenance label on screen | Beat |
|---|---|---|
| evidence/blender/01-mcp-connected-port-9876.webp | Student's own screenshot | B04 |
| evidence/blender/02-interface.webp | Student's own screenshot | B05 |
| evidence/blender/03-castle-mcp-look.png | Blender MCP look tool, student's live session | B08 |
| evidence/blender/04-toybox-before.webp | Student's own screenshot | B14, B15 |
| evidence/blender/05-toybox-after.webp | Student's own screenshot | B15 |
| evidence/blender/06-windkey-sidebar.webp (0bc2b4d) | Student's own screenshot | B12 |
| evidence/blender/07-castle-sidebar.webp (fd99467) | Student's own screenshot | B10 |
| evidence/godot/prop_room.png | Real engine render · Claude-made (shot_prop_room.gd) | B02 |
| evidence/godot/views/*.png (6) | Claude-made engine renders, not the student's | B24 |
| capture/orbit-4k.mp4 (this film) | REAL ENGINE … camera orbit added by a film script | B18 |

There is no screen recording of the student's Blender session, and the film does not imply one.

## Recorded output shown

`evidence/runs/check_props3d-isolated-1d93dcb.txt`, `repro-global_transform.txt`, `repro-parse-error.txt` (see
CAPTURE.md); `git log --reverse 9788922..1d93dcb` (B03, rendered from the live command).

## Prompt provenance

The castle prompt (B06) is the student's pasted message in the Claude Code session "Castle asset build (Assignment 3)"
(transcript `068f5075-389f-4edd-99d4-87e0ab8b77f8`, 2026-10-16T01:40:25Z), copied verbatim to
`evidence/castle-prompt.txt`. Only that message was extracted. B00's prompt is an illustrative reconstruction (walker
modifier) and is labelled so.

## Tools

| Tool | Version | Use |
|---|---|---|
| Brutalist (course checkout `_brutalist/`, commit 6a8380a) | `godot-gamedev` walker + ai-explainer bookends + OUTRO-LOCK | film pipeline |
| Kokoro (local, `am_onyx`) | kokoro-onnx v1.0 model | narration (Liam, in for Bear); no paid services |
| Remotion | toolkit `runtime/remotion` | ClaudeComposerAsk, BrutalistHesitantWriter, GodotDevWorkbench, ClaudeVerdictArtifact, ClaudeTitleOutro |
| Pillow + FFmpeg | — | `_tools/make_media.py` composites of real files |
| Godot | 4.7.2.stable.official.ed1daf0bf | headless check, repros, Movie Maker orbit |
| Fonts | EB Garamond, Inter, Lato, PT Mono (toolkit `runtime/fonts`) | composites |

Blender 5.2.2 LTS, mcp-for-blender 2.1.9 / add-on 1.8 and Claude Code 2.1.295 were used by the student's sessions
(SOURCES.md at the repo root, "Assignment 3"); this film build did not run Blender.

## Who did what (from the repo's SOURCES.md "Assignment 3", as narrated in B26)

* **Claude:** all Blender code (castle and windkey via the MCP in a separate session; toybox and the first windkey by
  script route), the export script, `prop_room.tscn`, `tests/check_props3d.gd`, the render scripts, and the docs; found
  and fixed its own false-passing check. Also built this film (beat sheet, narration text, composites, capture).
* **Tharun:** chose the three assets (dropped the cork) and the character scale; reviewed and accepted the brief;
  installed/approved tools; did the "Learn the window" session and took the screenshots; ran and approved the MCP
  sessions (including windkey call 0 that auto mode had blocked); made the hand edit; did the Godot look check; wrote
  the hand-edit lesson in his own words.
* **Voice:** Kokoro text-to-speech, `am_onyx`.

## Corrections relative to the stale draft

The earlier draft (tag a3 / f4b5119) was discarded: navy band, "no hand edit", one MCP asset, headless Blender
reconstructions. Every beat, narration line, capture and run was rebuilt from 1d93dcb / fd99467.
