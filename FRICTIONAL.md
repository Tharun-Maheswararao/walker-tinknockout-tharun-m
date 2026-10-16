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

## 2026-10-06 — Bolt's reference image (ASSET-LOG CHAR-REF v1–v7)

- **Wanted:** one image of Bolt that passes the sheet's consistency rules (brass helmet ≈ 40 %, one window with two eyes, key on the back, mitten gloves) and reads as a flat illustrated tin toy, not a photo.
- **Asked / got:** SDXL-Turbo, txt2img, 4 steps, cfg 0.
  - **v1:** a long prompt gave **photos of real toys**. The prompt was over CLIP's 77-token limit, so "plain light grey background" was silently dropped. One seed came out solid black (an fp16 NaN on the Mac GPU).
  - **v2:** a shorter prompt with the style words first gave the right cartoon style, but **red helmets and no eyes**.
  - **v3:** adding "porthole" put the **whole picture inside a porthole frame**.
  - **v4:** "face window" made **the whole suit gold**.
  - **v5–v7:** I switched to **img2img from Claude's code-drawn spec sketch**. v5 strengths 0.5/0.6/0.7 gave identical images, because turbo runs int(steps × strength) = 2 steps for all three (a setting mistake, caught by comparing the outputs).
- **Decided:** Claude put up 4 finalists against the rules. **I chose s40 (v6, strength 0.75):** it passes 5 of 6 rules, fails only the eyes, and adds two antennae. Edit: eyes painted on the glass (`tools/edit/paint_eyes.py`). The "key" in the generated art reads as a black nozzle, so the key became a separate prop that code spins during rewind (pillar 1).
- **Human / Claude / model:** the choice was mine; the prompts, finalists and edit script were Claude's; the pixels came from SDXL-Turbo.
- **Still unresolved:** the reference has richer paint than the poses that came after it (next entry).

## 2026-10-06 — deriving 11 poses (CHAR-* v1, v2, v3)

- **Wanted:** the same Bolt in 11 poses (sheet P02–P12) at the same scale, so they line up with one hurtbox.
- **Got:** v1, with the plain sketch as init, made **a different diver for every seed**. This is predicted failure **F1, confirmed** (`design/rejected/CHAR-JAB.jpg`).
- **Changed:** the inits now copy the accepted reference's features (antennae, yellow gloves, grey glass), use 8 steps, and run at strengths 0.6 and 0.7.
  - v2 at 0.6 held the identity, but looked flatter.
  - v3 (0.75 and 0.85) brought back the rich paint *and* the drift.
- **Decided (Claude, by the sheet's rules; I didn't review each pose):**
  - **Consistency over detail:** 0.6 with seed 43 for every pose, because detail is lost at 112 px and drift is not.
  - The win pose at s43 had no raised fist, so I used s42.
  - The eyes were lost at 0.6, so they are painted on every pose, at a position computed from the sketch geometry.
- **Human / Claude / model:** the selection rule and code were Claude's; the outputs were SDXL-Turbo's. I did not review the pose picks one by one.
- **Still unresolved:** the poses are flatter than the reference image, and only 4 seeds were tried per pose.

## 2026-10-06 — sounds and music (SFX-*, MUS-WALTZ)

- **Wanted:** six one-shots that match "Tin you can hear" (clang, shing, pop, one click, wind-down, ding) and a waltz loop without a click.
- **Got:** AudioLDM 2 needed a compatibility patch to run with transformers 5. It filled every clip with several seed-shaped hits. Claude checked the patch didn't break prompt conditioning (two prompts on the same seed: correlation 0.21).
- **Decided:** I was asked to listen and pick, and **I asked Claude to pick for me.** Claude cannot hear, so it scored each candidate on attack, decay, number of hits, tonality and pitch drop (`tools/edit/score_sfx.py`, `evidence/sfx-scores*.txt`).
  - It re-trimmed every clip from the loudest hit, because v1 trims started on noise.
  - **It overrode its own scorer twice:**
    - cutlass `v2_s5` was a 13 ms tick, not a shing, so it took `s2`;
    - the bell's 25 "hits" were its shimmer, so it took `v2_s13`.
  - No EMPTY candidate fell in pitch, so it applied a pitch-fall edit.
  - Music: s2 had the cleanest 8-bar seam.
- **Human / Claude / model:** **the sound choices are Claude's analysis, not my ears.** I say this plainly here and in SOURCES. The outputs were AudioLDM 2 and MusicGen.
- **Still unresolved:** whether they *sound* right. That's my listening check in TEST-REPORT section 8.

## 2026-10-06 — building and testing the slice

- **Sprite / hurtbox:** the first screenshots showed the sprites about 80 px off their hurtboxes (`evidence/screens/before-fix/`). Cause: a centred sprite *plus* a feet offset. Fixed with `sprite.centered = false`.
- **Tests:** the first run had **8 of 24 failing** (`evidence/tests/run-01-setup-bug.txt`).
  - A frame trace showed the cause: my test froze Rivet's brain 3 frames after the round started, and Rivet shot a cork in that window.
  - Fixed the test order. No expected value changed. I also added a 1.5 s pop-gun cooldown at round start.
  - Now 25/25.
- **Stun-lock (found by the film dry run):** EMPTY fired 6 times in one round. A hit at 0 wind went HURT → EMPTY → hit again, until KO. That's a real design bug, not a test artefact. **Rule change:** HURT always returns to IDLE, and a 0-wind toy can't walk, only rewind. Now 1 EMPTY per round.
- **F4 re-check on the real background:** Rivet's suit is 2.35:1 (better than predicted). But Bolt's yellow helmet against the pink castle at his start position is 1.02:1 luminance. **Not fixed**; recorded as a limitation and a next step.
- **Human / Claude:** all code and tests were Claude's. These observations come from Claude's screenshots and test runs.

## 2026-10-06 — scope and time (retrospective note)

The Claude app was closed overnight for longer than either of us realised. Work resumed at about 15:50 with 8 hours left. To fit the deadline, the film was handed to a separate Claude agent working from a written brief, while the docs were written in parallel. My own playtest and listening check happened (or didn't) as recorded in TEST-REPORT section 8.

## 2026-10-06 ~20:00 — my playtest

- **Played** a sound-on round, then a muted round (M + N).
- **What I found:** the game and the characters feel **very simple**, and with sound on it was "full of metal sounds". With effects off (N) **the music alone is fine**, so the problem is the dense tin effects, mostly the rewind clicks (4 per second while held), not the music. **Muted, it still works**: I could follow the fight.
- **Decided:** not to change the game tonight, because the film is built on the frozen revision `64c037a`. Claude had started warmer music candidates before I narrowed it down; we stopped them once I said the music was fine.
- **Next:** a quieter, lower rewind click (or one per half-turn), effects about 6 dB under the music, and richer character art. The simplicity is the cost of choosing consistency over detail in the pose pass.
- **Human / Claude:** the observations are mine; Claude recorded them and proposed the next steps.

---

# Assignment 3 — 3D assets with Claude, the Blender MCP and Blender

## 2026-10-14 — tool setup (run by Claude at my request; I approved each install)

- **Installed:** `brew install uv coreutils` → uv 0.13.1, coreutils (gives `timeout` on PATH). `brew install --cask blender` → **Blender 5.2.2 LTS**, not the chapter's 5.1.2. Godot was already 4.7.2.stable.official.ed1daf0bf.
- **MCP package:** `uvx` resolved `mcp-for-blender` **2.1.9**, the version the assignment describes.
- **Registering the server failed as the chapter wrote it.** `claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender` gave: `Invalid environment variable format: blender, environment variables should be added as: -e KEY1=value1 -e KEY2=value2`. Claude Code 2.1.295 reads `-e` as taking several values, so it swallowed the server name. **Fix:** put the name first: `claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender`. `claude mcp get blender` then showed local scope (this project only), `DISABLE_TELEMETRY=true`, Status ✔ Connected. That status only means the server process starts; it does not show the add-on in Blender is reachable.
- **`claude` was not on PATH.** This machine runs Claude Code inside the desktop app, so Claude called the app's bundled CLI by its full path.
- **`uvx mcp-for-blender install-addon` failed:** `Could not find a Blender user addons directory. Set BLENDERMCP_ADDONS_DIR to your Blender scripts/addons path, or install addon.py manually from the repo.` Likely cause: Blender had just been installed and never opened, so its user folder did not exist yet. Next: open Blender once, then retry.
- **Retry after I opened Blender once:** `install-addon` succeeded and wrote `~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py`. So the first failure was the missing user folder, as guessed.
- **Claude read the add-on before I enabled it** (6,441 lines). It binds `localhost:9876`. `auto_start_server` defaults to **True**, which confirms the assignment's warning: the socket opens every time Blender starts while the add-on is enabled. Poly Haven, Hyper3D, Hunyuan3D, Sketchfab, Tripo, Poly Pizza and telemetry consent all default to **False**. The add-on's own `bl_info` version is **1.8**, not the package's 2.1.9, so SOURCES should give both.
- **Enabling it in the Blender that was already open failed.** I ticked *Interface: MCP for Blender* and got `Add-on not loaded: "blender_mcp", cause: No module named 'blender_mcp'`. Preferences still listed it (version 1.8, Legacy (User)). **Diagnosis, by Claude:** that Blender started before `scripts/addons` existed, so the folder was not on its Python `sys.path`. A fresh headless Blender (`blender -b --python-expr …`) had the folder on `sys.path`, enabled the add-on without error (`ENABLED True (1, 8)`), and reported port 9876 with auto-start on. **Fix:** quit Blender completely and reopen it, then enable. The install-addon message's "or restart Blender" was the step that mattered; disable/enable alone was not enough.
- **After I quit (⌘Q) and reopened Blender, it worked.** The add-on enabled with no error. My screenshot (`evidence/blender/01-mcp-connected-port-9876.webp`, 21:54) shows the N-panel tab *MCP for Blender*: "Connected on port 9876", a **Disconnect** button, and "Addon 1.8 · up to date". Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin and Tencent Hunyuan 3D are all unticked. The panel is a fourth wording: the README's *Start MCP Server* / *Connect to Claude* and the code's *Connect to MCP server* were all claims, and since it auto-started I never saw a start button. **Claude's independent check:** `lsof` shows Blender (pid 11697) listening on **127.0.0.1:9876 only**, not on all interfaces. This proves the socket is up on localhost; it does not yet prove Claude Code can drive Blender. That needs a real `get_scene_info` call from a new session.

## 2026-10-14 ~22:50 — learning the window, and choosing the assets

- **My session:** I looked around Blender, opened the N sidebar's Item tab, and took `evidence/blender/02-interface.webp` (22:47). Claude pointed out the default cube reads Scale 1.000 but Dimensions 2 m. That feeds my "wrong size" prediction.
- **BLENDER-NOTES.md:** I asked Claude to write the six descriptions. Claude drafted them and labelled them as its own, because the assignment asks for my own words. The "What I noticed" lines are left for me to fill in.
- **Assets (my decision):** I first picked four: sunken-castle ornament, winding key pickup, cork harpoon ammo, toy-box crate. The assignment allows three, so **I dropped the cork**, Claude's suggestion. At one or two shapes it would show the least about the workflow. The three are the **sunken-castle ornament** (environment), the **winding key pickup** (collectible) and the **toy-box crate** (prop).
- **Scale (my decision):** character scale, **Bolt = 1.8 m**, so normal Godot camera and physics ranges apply. I chose it over real toy scale (~0.2 m).

## 2026-10-15 — building the castle through the MCP (separate Claude Code session)

- **What the record shows:** the build session committed `tools/blender/build_castle.py` (8 `execute_blender_code` bodies, calls 0–7) and `.gitignore` `*.blend1` (`bec93b5`), then `assets/blender/castle.blend` (`c9b71fa`). *(Corrected 2026-10-16 from the session transcript: I did not save it by hand. I typed "save the blend", and Claude saved it through the MCP to `assets/blender/` at 23:11, choosing that folder over `blender/` so Godot would not auto-import the .blend.)*
- **Claude's independent check (this session):** re-running `build_castle.py` headless rebuilt the castle at 1.80 × 0.82 × 2.30 m, 156 tris. Opening the saved `castle.blend` headless showed the same numbers, origin (0,0,0), scale 1, and the three brief colours. So the saved file is the MCP-built asset and matches the brief.
- **From the session transcript** (added 2026-10-16; Claude read the saved transcript of session "Castle asset build (Assignment 3)" because I had not written these down):
  - **`get_scene_info` did not work first time.** At 21:40 both `get_addon_status` and `get_scene_info` returned `Could not connect to Blender. Make sure the Blender addon is running.` About 4 minutes later I wrote "Blender is open and the MCP server is connected. Call get_scene_info again". At 21:45 it worked: add-on 1.8, protocol 13 of 13, scene "1 camera, 1 light, 1 mesh | active Cube | (unsaved)".
  - **I did not change or reject anything.** I replied "Approved. Build the castle as proposed … Don't save or export." The build session later admitted that **its step-by-step proposal never actually appeared in the chat**, so I approved a plan I had not seen. The calls did follow the brief (8 calls, 21:45–21:46), and the code is in `build_castle.py`. Lesson: check that the proposal is on screen before saying "approved".
  - **Nothing else went wrong in the build.** Each part's `get_scene_info` showed rotation 0 and scale 1. The join gave 1.80 × 0.82 × 2.30 m and 156 tris. The `look` tool's four views are saved as `evidence/blender/03-castle-mcp-look.png`. Blender 5.2 printed a deprecation warning: `Material.use_nodes` goes away in 6.0.

## 2026-10-15 ~23:15 — deadline: windkey and toybox by script route

- **Decision (mine):** with ~40 minutes left, I asked Claude to finish. Claude built `windkey` and `toybox` by the **script route** (headless Blender) in this session, because this session cannot see the MCP tools. This is a time decision, not an MCP failure; the castle shows the MCP route worked. I accept that this earns less than "MCP for at least two assets".
- **Results:** windkey 0.60 × 0.14 × 0.70 m, 192 tris; toybox 1.26 × 0.76 × 0.75 m, 48 tris. Both have origin at the base and scale 1. All three exported with `export_glb.py` (+Y Up).
- **Claude's own check was wrong at first:** the first `check_props3d.gd` printed PASS for "sits on the floor in the room" while Godot logged `!is_inside_tree()` errors. `global_transform` returned the identity, so placement was never tested. Claude rewrote the transform maths; the rerun shows real positions. A second edit hit a GDScript parse error, **and Godot still exited 0**. Lesson: read the RESULT line, not the exit code. Output: `evidence/check_props3d.txt`.

## 2026-10-15 ~23:20 — what was not done, and why

- I asked Claude to "do everything", including the hand edit and the checks. Claude did the build, export, Godot and docs work, but declined three items that the assignment defines as mine: **the hand edit in Blender's window** (a scripted edit would not be a hand edit), **the HUMAN CHECK: look**, and **my account of the MCP build session**. At submission all three are **not done / not recorded**. Nothing here is written as if they happened.
- The planned hand edit (CHANGE-BRIEF A3.4, recolour the toy box band) is therefore not in this submission.

## 2026-10-16 00:05–00:25 — the deadline moved: hand edit and look check

- **Decision (mine):** submit a day late (10 % penalty) so the film and my own parts can be done. Claude stopped the film agent, which had started from the old `a3` (navy band, "no hand edit"), so the film will be made from the final source. The two "not done" entries above are now superseded for the hand edit and the look check.
- **Hand edit (mine, in Blender's window):** I opened `toybox.blend` and switched the viewport to Material Preview (third shading sphere; I first mistook the X/Y/Z gizmo for it). In the Material tab I chose slot `toybox_navy` and changed Base Color to `#2E7D32` green, then saved at 00:11. Claude checked the saved file headless: size, origin, scale and 48 tris were unchanged. It re-exported the .glb, and the check passed with albedo `#2E7D32` (`08f96cd`). The slot name still says "navy".
- **Look check (mine):** I opened `prop_room.tscn` in the Godot editor, orbited the props and ran it with F6. Everything looked fine to me. I forgot to take a screenshot, so Claude rendered six angles (`evidence/godot/views/`) and noted the near-white lid; that observation is Claude's.

## 2026-10-16 15:50–16:15 — windkey rebuilt through the MCP

- **Why:** the rubric's full MCP credit needs at least two assets. Claude (this session) asked the castle session, which has the MCP tools, to rebuild `windkey` per the brief. The script-route version was renamed `build_windkey_script_route.py` and kept for comparison.
- **What went wrong:** Claude Code's auto-mode safety check **denied call 0** ("Irreversible Local Destruction"). That call deletes every object in the open Blender (which had my `toybox.blend` open) and saves over `windkey.blend`. Before stopping, the session checked that `toybox.blend` had no unsaved changes (`is_dirty False`). **I approved call 0 myself** in that session at 16:09 ("Yes, I approve call 0 …").
- **Result:** 4 parts, rotation 0 and scale 1 on every `get_scene_info` row. Joined `windkey` is 0.60 × 0.14 × 0.70 m, Z 0..0.70, 192 tris, 0 non-manifold edges. Claude reopened the saved `.blend` headless and got the same numbers. Exported; the Godot check passes. These are identical to the script-route numbers, so the route changed and the asset did not.
- **Screenshot attempt:** Claude tried to capture my Blender window with `screencapture`. It got only the desktop wallpaper, because the app lacks macOS Screen Recording permission, and Claude did not change that setting. The sidebar screenshot is mine to take.
