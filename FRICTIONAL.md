# FRICTIONAL — design log, Tin Knockout

Dated entries, written as the work happened. "Human" = Tharun (me). "Claude" = Claude Code (Opus 5.5): plans, prompts, code, code-drawn sketches. "Model" = the generative model named in the entry.

## 2026-10-05 — choosing the game

- **Wanted:** a game for the whole semester, not just this assignment, that is fun to play and where the art, sound and music all come from one idea.
- **Explored:** Claude proposed several directions (a tin wind-up toy, a hermit crab, a lantern moth). I asked about something like a friend's Spider-Man project. Claude pointed out that copyrighted characters are banned by the assignment, so I kept only the swinging *mechanic* as an option (a jumping spider). I then asked for fighting-game ideas, then car ideas, before choosing.
- **Decided:** **Tin Knockout**, a tin wind-up toy fighting game, because the spring-as-stamina idea gives every attack a cost and ties the mechanic to the sound (ratchet, clang) and the music (a music box that winds down). I added **swords, guns and other weapons**; we agreed they must be *tin toy* weapons (cutlass, cork pop-gun) to keep the world coherent, and that weapons are separate sprites so the pose count doesn't multiply.
- **Rejected:** reusing SPROCKET, my code-drawn character from Assignment 1. Claude suggested it for semester continuity; I wanted a more creative, new character. From four new options I chose **Bolt**, a tin deep-sea diver with a porthole face. Claude's argument that a round helmet is easier for an image model to repeat consistently was part of why.
- **Scope decision:** the assignment is due 2026-10-06 23:59, one day away. The slice is cut to Bolt vs a recoloured Rivet, three weapons, one arena. Real AI, more weapons and pickups are next steps.
- **Human / Claude / model:** decisions above are mine; options, trade-offs and the CONCEPT draft are Claude's, approved by me. No generative model used yet.

## 2026-10-05 — design docs before generation

- **Wanted:** a written spec that the generated images and sounds can be judged against.
- **Did:** CONCEPT, STORYBOARD (7 panels), CHARACTER-SHEET (12 poses), CHANGE-BRIEF. Sketches are **code-drawn by Claude** (`design/draw_design.py`), not hand-drawn and not generated; they define proportions, poses, the collision boxes and the palette.
- **Found before generating:** the contrast check (`design/character/contrast-table.md`) shows Rivet's verdigris suit at **1.07:1** against the planned gravel colour, so it would vanish. Bolt's outline and boots are weak (1.5–2.0:1) against the dark bowl. This became predicted failure F4 and a prompt requirement (a lighter background band and rim light).
- **Still unresolved:** whether SDXL-Turbo can hold Bolt's proportions across 11 poses (F1). I expect it won't on plain text prompts, so the plan is one reference image, then img2img or a pose sheet.
