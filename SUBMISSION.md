# SUBMISSION — Assignment 6

*(The Assignment 5 submission note is preserved at tag `a5`; Assignment 3's at `a3`; Assignment 2's at `a2`.)*

- **Assignment:** Assignment 6 - Creating Particle Effects with Godot and Claude
- **Student:** Tharun Maheswararao (maheswararao.t@northeastern.edu)
- **Project name:** walker-tinknockout-tharun-m (Tin Knockout)
- **GitHub repository URL:** https://github.com/Tharun-Maheswararao/walker-tinknockout-tharun-m
- **Git tag and submitted commit SHA:** tag `a6`. The SHA is given in the Canvas copy of this note, because a commit cannot contain its own hash.
- **Game-source revision shown in the film:** `c844ab2`. Later commits change only the film's records (`youtube/…-a6-particles/`), `.gitignore`, README / TEST-REPORT text (the GPU-price status and the film link) and this note. No game code, scene, test or shader changed after `c844ab2`.
- **Godot version, renderer, and operating system:** Godot 4.7.2.stable.official.ed1daf0bf · Forward+ on Vulkan 1.2.334 (MoltenVK) · macOS 15.6 (Darwin 24.6.0)
- **GPU used for the GPU price:** Apple M4 (integrated). The GPU price itself was **not measured**: I chose to skip it (2026-11-09). The fixture is `godot/previews/gpu_price.tscn` (TEST-REPORT A6-5).
- **Effect A: event, node type, retrigger rule:** an impact burst on every hit, melee (`Fighter.hit_landed`) and cork (`Cork.struck`), both arriving at `main._on_impact(p, blocked)`. Two one-shot `GPUParticles2D` emitters in `godot/effects/impact_effect.tscn`: Shards (MIX, dark tin, code-written texture) and Core (ADD, cyan radial gradient), 0.25 s, on top of the kept star spark. Blocked hits spawn a smaller grey `impact_effect_blocked.tscn`. Retrigger: a fresh instance per impact, so bursts overlap (peak 4 bursts, 96 particles), each freed on `finished`.
- **Effect B: job, condition, node type, feature Effect A doesn't use:** a feedback loop following `Fighter.wind` (0–100) on both fighters: steam from the wind-up key when wind is below 25, `amount_ratio = (25 − wind) / 25`, 0 at wind ≥ 25. One continuous `GPUParticles2D` in `godot/effects/wind_steam.tscn`, on a `SteamMount` that follows the key but not its rewind squash. Feature Effect A doesn't use: `amount_ratio` (also continuous emission and `local_coords = true`).
- **Budgets, and the price each is compared on:** GPU time in the Visual Profiler, against the 0.97 ms effects-off Render Viewport baseline: Effect A < 0.55 ms at 4 concurrent bursts; Effect B < 0.20 ms for both fighters at ratio 1.0. Both are **unchecked** (GPU price not measured). Headless CPU price (`cost_effects.gd`, wall clock): both effects within the spread of the effects-off game (a_peak 0.0289 ± 0.0157 ms, b_heavy 0.0223 ± 0.0022 ms vs game_off 0.0230 ± 0.0066 ms), as predicted; near zero by construction, because the dummy renderer does not run GPU particles.
- **Texture sources and licences (or model, version, and terms):** no third-party or model-generated textures. `shard_8.png` and `steam_32.png` are written by committed scripts (`godot/tools/generate_shard_texture.gd`, `generate_steam_texture.gd`), under the repository's own licence; Effect A's core uses an in-scene `GradientTexture2D` (`godot/effects/textures/ATTRIBUTION.md`).
- **Final film URL and filename:** https://drive.google.com/file/d/10_Dj02-oApqbA52NZSiLufxgmR-TbomC/view?usp=sharing · `claude-liam-walker-tinknockout-tharun-m-a6-particles.mp4` (4K 3840×2160, 11:57, Brutalist `godot-gamedev` walker workflow, Liam narration; records in `youtube/claude-liam-walker-tinknockout-tharun-m-a6-particles/`)
- **Final film SHA-256:** `04d435e30352681ac1bfecd855072acf700a9afc3a02cc5e601407e4b010630a`
- **Summary of my work:** From SOURCES.md "Who did what (A6)": I chose both effects and every value in CHANGE-BRIEF.md (with the drafting help listed there) and wrote every dated revision; ran every Movie Maker capture and both Step 2 mutations; approved each wiring step and tuning change, choosing the holder fix for Effect B; gave the first-look notes, human checks and in-game verdicts in TUNING.md and TEST-REPORT.md; and converted the process shader in the editor and wrote its line references. Claude Code wrote the facts file and probes, built both effect scenes, the texture scripts, the tests, the preview fixtures, the wiring and `SteamMount`, the cost script, the F10 key and the GPU-price fixture, read and measured the strips, and drafted the docs.
- **Known limitations:**
  - The GPU price was not measured, so the GPU budgets are unchecked; no GPU number is claimed.
  - Rivet's steam rarely shows: his pattern brain rewinds as soon as his wind drops below 25, the same threshold where the steam starts (TEST-REPORT A6-3; probe: steam on 7 s of 30, max ratio 0.29).
  - Effect A's dark shards are weak over the dark stretch of the background; the cyan core still reads (A6-5a).
  - The in-play human check is partial: landed jab, block, cork and pause for A; low wind and rewind for B (A6-5).
  - Headless, the engine's process and physics time monitors read 0, so only the wall clock is used for the CPU price.
  - `claude -p` hit the account's spend limit (until 2026-12-01), so every agent prompt ran in the interactive Claude Code session.
  - The film was built by a separate Claude film session and passed the workflow's checks; I watched it in full before uploading. Narration is Kokoro TTS (Liam).
- **Changed games since Assignment 2:** no.

