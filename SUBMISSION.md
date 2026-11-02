# SUBMISSION — Assignment 5

*(The Assignment 3 submission note is preserved at tag `a3`; Assignment 2's at tag `a2`.)*

- **Assignment:** Assignment 5 - Shaders, Materials, and the Godot Shading Language
- **Student:** Tharun Maheswararao (maheswararao.t@northeastern.edu)
- **Project name:** walker-tinknockout-tharun-m (Tin Knockout)
- **GitHub repository URL:** https://github.com/Tharun-Maheswararao/walker-tinknockout-tharun-m
- **Git tag and submitted commit SHA:** tag `a5`. The SHA is given in the Canvas copy of this note, because a commit cannot contain its own hash.
- **Game-source revision shown in the film:** `2e6946d`. Later commits change only evidence, docs, one capture tool (`godot/tools/a5_capture_side_by_side.gd`) and the comment annotations in `godot/shaders/standard_generated.gdshader`, which the game does not use (`e4c188f`, comments only, no code line changed). No game code, scene, material or used shader changed after `2e6946d`.
- **Godot version, renderer, and operating system:** Godot 4.7.2.stable.official.ed1daf0bf · Forward+ on Vulkan (MoltenVK) · macOS 15.6 (Darwin 24.6.0), Apple M4
- **Game state the shader from code communicates:** REWIND, the fighter cranking its spring and open to a 1.5× knockdown hit. Each fighter's body sprite fades toward blue (90, 160, 255) at half strength while it rewinds: 0.15 s in, 0.30 s out, extending on retrigger and freezing on pause. The shader is `godot/shaders/rewind_tint.gdshader`, driven by `godot/fighter/rewind_tint_driver.gd`.
- **3D object and scene given the textured shader:** the toy box in `godot/prop_room/prop_room.tscn`, using `godot/shaders/painted_tin.gdshader`. `toybox_fresh.tres` is applied through the glb's Use External; a second toy box carries `toybox_worn.tres` as a surface override.
- **Texture sources and licences:**
  - Poly Haven "Metal Plate" (https://polyhaven.com/a/metal_plate) by Rob Tuytel, CC0, 1k PNG. The `_nor_gl` map is used; `_nor_dx` is for calibration only (`godot/assets/textures/metal_plate/ATTRIBUTION.md`).
  - The 3×1 grey hint texture is written by code (`godot/tools/write_hint_png.gd`).
- **Final film URL and filename:** https://drive.google.com/file/d/1x90bbSlU_QSjNzabapgok6JhSpoYX68V/view?usp=sharing · `claude-liam-walker-tinknockout-tharun-m-a5-shaders.mp4` (4K 3840×2160, 7:02, Brutalist `godot-gamedev` walker workflow, Liam narration; records in `youtube/claude-liam-walker-tinknockout-tharun-m-a5-shaders/`)
- **Final film SHA-256:** `6568f966a28b65ffad73d3aac36430b4f222d5f065af60dfd930946d141b2ed8`
- **Summary of my work:** Throughout Assignment 5, I completed the technical tasks, language notes, and evaluation verdicts through a collaborative workflow where [Claude] proposed core code structures, skeletons, and suggestions, which I integrated, completed, and tested. I filled in the shader logic, answered all conceptual and short-answer questions, and evaluated audit logs and playtest outcomes against rubric guidelines. (Details: SOURCES.md "Who did what (A5)".)
- **Known limitations:**
  - The film was built by a separate Claude film session in about 45 minutes and passed the workflow's checks. I watched it in full before uploading; its narration is Kokoro TTS (Liam).
  - The `claude -p` agent route hit the account's individual spend limit mid-session (until 2026-12-01). The audit, two test-bug fixes and the captures were therefore done in the interactive Claude Code desktop session, with every commit labelled.
  - `painted_tin` writes no METALLIC (MATERIALS.md M5).
  - The fade can start up to 1/60 s after the key press at high frame rates; the fade duration itself is to spec.
  - The captures are scripted-input runs; my playtest is the unscripted check.
- **Changed games since Assignment 2:** no.
