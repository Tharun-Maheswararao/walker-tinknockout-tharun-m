# SUBMISSION — Assignment 7

*(The Assignment 6 submission note is preserved at tag `a6`; Assignment 5's at `a5`; Assignment 3's at `a3`; Assignment 2's at `a2`.)*

- **Assignment:** Assignment 7 - Doing Animation with Claude and Godot
- **Student:** Tharun Maheswararao (maheswararao.t@northeastern.edu)
- **Project name:** walker-tinknockout-tharun-m (Tin Knockout)
- **GitHub repository URL:** https://github.com/Tharun-Maheswararao/walker-tinknockout-tharun-m
- **Git tag and submitted commit SHA:** tag `a7`. The SHA is given in the Canvas copy of this note, because a commit cannot contain its own hash.
- **Game-source revision shown in the film:** `a5978c0`. Later commits add only the film's records (`youtube/claude-liam-walker-tinknockout-tharun-m-a7-animation/`), the README film link and this note. Nothing under `godot/` or `scripts/` changed after `a5978c0`.
- **Godot version, renderer, and operating system:** Godot 4.7.2.stable.official.ed1daf0bf · Forward+ on Vulkan 1.2.334 (MoltenVK) · macOS 15.6 (Darwin 24.6.0), Apple M4
- **Sprite clip: route, node, scene, frame rate:** `wind_key_cycle` (`godot/animations/wind_key_cycle.tres`). Route: Sprite2D + AnimationPlayer frame track (discrete). Node: `key_sprite` (Sprite2D, `hframes` 8) at `Fighter/FacingPivot/BodyPivot/KeyMount/KeyBob/key_sprite`, on both fighters. Scene: the game, `res://game/main.tscn` (fighters built in code by `godot/fighter/fighter.gd`). 8 fps, `step` 1/8, 8 frames, `LOOP_LINEAR`.
- **Rig clip: route, rig source, node, scene, frame rate:** `jab_action` (`godot/animations/jab_action.tres`). Route: cutout rig keyed as resource text. Rig source: the fighter's own art parts under named Node2D pivots built in `fighter.gd` (`FacingPivot/BodyPivot/{sprite, KeyMount/KeyBob/key_sprite}`). Nodes: `BodyPivot` (`position:x`, `rotation`) and `KeyBob` (`position:y`). Scene: `res://game/main.tscn`. 60 fps, `step` 1/60, 21 frames: startup 0–4, active 5–10, recovery 11–20.
- **Which clip loops and which commits:** `wind_key_cycle` loops (the key turning while the fighter rewinds); `jab_action` commits (the jab).
- **The one authority over each animated node:**
  - `KeyAnimPlayer` → `key_sprite.frame`;
  - `FighterAnimPlayer` → `BodyPivot` and `KeyBob`;
  - `Fighter._apply_pose()` → `FacingPivot.scale.x`, the body `sprite`, `KeyMount` and `weapon`.

  Both players are MANUAL and are put at `state_t` at the end of each physics step (`godot/tests/test_a7_structure.gd` checks the writers from the source and the behaviour).
- **Sprite sheet source and licence (or model, version, and terms):**
  - Sheets: `godot/assets/props/key-bolt-sheet.png` and `key-rivet-sheet.png`, written by `godot/tools/generate_key_sheets.gd` from the committed A2 key art.
  - Source art: SDXL-Turbo (`stabilityai/sdxl-turbo`, revision `71153311d3dbb46851df1931d3ca6e939de83304`), run locally, prompt row PROP-KEY in `ASSET-LOG.md`.
  - Licence: Stability AI Non-Commercial Research Community License.
  - Credits: `godot/assets/props/ATTRIBUTION.md`.
- **Final film URL and filename:** https://drive.google.com/file/d/1gdxG-RNG4bh9KgMArhkk_oH-PP5GQH_9/view?usp=sharing · `claude-liam-walker-tinknockout-tharun-m-a7-animation.mp4` (4K 3840×2160, 11:57, 30 fps; Brutalist `godot-gamedev` walker workflow, Liam narration; records in `youtube/claude-liam-walker-tinknockout-tharun-m-a7-animation/`)
- **Final film SHA-256:** `0318373f1799c3629c910038feb023871aa5eefdf6fdf4ee6d88a873776046bd`
- **Summary of my work:** From SOURCES.md "Who did what (A7)": I chose both clips, the routes, the 60 fps phase table with its poses and easing, the 8 fps cycle and its sheet recipe, the authority layout and the interrupt rules, and wrote the two dated brief revisions; swapped in the A7 wrapper; reviewed CLAUDE.md and added the Headless-facts lines; approved the Step 5 plan, its four decisions and the seam fix, and committed the four planned pin updates; ran every Movie Maker capture; wrote the first look before Claude read the strip and both in-game verdicts (revision 2 came from my own play observation); and did the Use It human checks and the two-clocks run. Claude Code wrote the facts file and probes, the sheet generator, both clip resources, the read-backs, the pins, the wiring in `fighter.gd` and `steam_mount.gd`, the structure, state and edge tests and both previews; ran the mutations in worktrees; found and fixed (with my approval) the seam bug; read and measured the strips; and drafted the docs. A separate Claude session built the film, which I watched in full before uploading.
- **Known limitations:**
  - The fighter's jab picture appears on the first JAB tick, five frames before the hitbox, and swaps back on the IDLE tick; mashing J shows the idle picture for one frame between jabs. Both come from the A2 art per state, not the clips (TEST-REPORT A7-12).
  - Rivet is drawn facing right on the title and intro until the first FIGHT tick. This was there before A7.
  - In the game a single rewind reaches full wind after at most 2.5 turns of the key, which then holds; the five-wrap seam check used the key-cycle fixture as well as repeated low-wind rewinds.
  - The edge tests run at 60 fps only: at 30 fps, input can only arrive on a frame's first tick.
  - `claude -p` was spend-limited until 2026-12-01, so every agent prompt ran in the interactive Claude Code session (`prompts/a7/`).
  - The film was built by a separate Claude film session and passed the workflow's checks; I watched it in full before uploading.
- **Changed games since Assignment 2:** no.
