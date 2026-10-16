# SOURCES — Tin Knockout

## What this project started from

- **An empty Godot 4.7 project.** No game code was copied from walker-jumpman or from my Assignment 1.
- **Patterns borrowed (not code):** from my Assignment 1, [walker-jumpman-tharun-m @ bb63748](https://github.com/Tharun-Maheswararao/walker-jumpman-tharun-m), itself an extension of [nikbearbrown/walker-jumpman @ 9387542](https://github.com/nikbearbrown/walker-jumpman):
  - the 640×360 viewport scaled to 1280×720 (×6 = 3840×2160 for film capture)
  - tests as `SceneTree` scripts that drive the game through the real `Input` path
  - capture scripts that never write gameplay state
- **Planned vs. actual:** the plan was to start from walker-jumpman/A1. Once the game became a fighting game, none of the platformer code applied, so I credit the empty project plus these patterns.

## Generative models (all run locally on an Apple M4, 16 GB, no paid services, no API keys)

| Model | Version (Hugging Face revision) | Used for | Where it ran | License / terms |
|---|---|---|---|---|
| **SDXL-Turbo**, `stabilityai/sdxl-turbo` | `71153311d3dbb46851df1931d3ca6e939de83304`, fp16 weights | All art: Bolt reference + 11 poses (Rivet is a recolour), environment, 4 props | local, PyTorch 2.14.1 MPS, diffusers 0.40.0 | **Stability AI Non-Commercial Research Community License** (`sai-nc-community`, [LICENSE.md](https://huggingface.co/stabilityai/sdxl-turbo/blob/main/LICENSE.md)). Non-commercial: acceptable for coursework, stated here. |
| **AudioLDM 2**, `cvssp/audioldm2` | `c8e7e189d324425c05c4c2f81214041ef4107983` | All 6 sound effects | local CPU, diffusers 0.40.0 `AudioLDM2Pipeline` (+ a small compatibility patch, see below) | **CC BY-NC-SA 4.0** (non-commercial, attribution, share-alike) |
| **MusicGen-small**, `facebook/musicgen-small` | `4c8334b02c6ec4e8664a91979669a501ec497792` | Music loop | local CPU, transformers 5.18.0 | **CC BY-NC 4.0** (non-commercial, attribution) |

**Attribution:** sound effects generated with AudioLDM 2 (Liu et al., CVSSP, University of Surrey). Music generated with MusicGen (Meta AI). Art generated with SDXL-Turbo (Stability AI).

**Compatibility patch:** transformers 5 removed `GenerationMixin` from `GPT2Model`, which AudioLDM 2 relies on. `tools/gen/gen_audio.py` binds that one helper back onto the model instance. I checked that this doesn't break prompt conditioning: two different prompts with the same seed give outputs with correlation 0.21, i.e. clearly different.

**No reference images, artist names, brands, copyrighted characters or existing recordings were used in any prompt.** Every prompt is in [ASSET-LOG.md](ASSET-LOG.md).

## Asset log

**[ASSET-LOG.md](ASSET-LOG.md)** has one row per generation batch (284 generations, 62 batches). Each row has the exact prompt, seeds, settings and init image, plus the outcome, the reason, and the edits applied. It is built from the machine-written `tools/gen/gen-log.jsonl`. Rejected outputs are in `design/rejected/` as contact sheets.

**To reproduce a row**, for example the accepted jab pose:

```bash
python tools/gen/make_inits.py --ref        # rebuild the init sketches
python tools/gen/gen_image.py --id CHAR-JAB --tag v2-st0.6 --init raw/inits-ref/jab.png --strength 0.6 --steps 8 --seeds 43 \
  --prompt "throwing a straight punch forward, 2d cartoon game sprite of a tin wind-up toy deep sea diver, polished brass helmet with two antennae, red enamel tin suit with rivets, yellow mitten gloves, steel boots, bold black outline, cel shaded, plain light grey background"
python tools/edit/process_sprites.py jab=raw/CHAR-JAB/CHAR-JAB_v2-st0.6_s43.png
```

Seeds use a CPU `torch.Generator`, so the latent noise is reproducible. On another GPU or another library version, pixels can differ slightly.

## Tools

| Tool | Version | License | Used for |
|---|---|---|---|
| Godot Engine | 4.7.2.stable.official.ed1daf0bf | MIT | the slice |
| rembg (u2net model) | 2.0.85 | MIT (u2net: Apache-2.0) | background removal |
| diffusers / transformers / PyTorch | 0.40.0 / 5.18.0 / 2.14.1 | Apache-2.0 / Apache-2.0 / BSD | running the models |
| Pillow, NumPy, soundfile (libsndfile) | — | HPND / BSD / BSD | sketches, edits, OGG Vorbis export |
| ffmpeg | Homebrew | LGPL/GPL | film assembly |
| Brutalist (course-provided) | course checkout `_brutalist/` | course terms | explainer film |

## Who did what

| | Human (Tharun) | Claude Code (Opus 5.5) | Generative models |
|---|---|---|---|
| **Concept** | Chose the game out of several directions (rejected Spider-Man, spider, cars); added weapons; rejected reusing A1's SPROCKET; picked Bolt from 4 options; approved CONCEPT | Proposed the options and trade-offs; wrote the CONCEPT / STORYBOARD / CHARACTER-SHEET / CHANGE-BRIEF drafts | — |
| **Design images** | Approved | Code-drawn storyboard thumbnails, pose targets, silhouette, collision, palette (`design/draw_design.py`) | — |
| **Prompts** | Approved direction | Wrote and revised every prompt (logged) | — |
| **Art** | **Chose the reference image** (s40 of 4 finalists) | Picked poses by the character-sheet rules (one seed for consistency; win pose s42); wrote all edit scripts | SDXL-Turbo produced every pixel of the character, environment and props, before edits |
| **Sound / music** | Asked Claude to pick (could not spend the time to listen); **listening check in the playtest** — see TEST-REPORT | Picked by **signal analysis, not listening** (`tools/edit/score_sfx.py`, `evidence/sfx-scores*.txt`); trim / pitch / loop edits | AudioLDM 2 (6 SFX), MusicGen (music) |
| **Code** | Playtested | Wrote all GDScript, tests, capture tools | — |
| **Verification** | Human playtest, sound on and muted | Automated tests, seam check, screenshots | — |
| **Film** | Watch-and-listen check of the export | Beat sheet, script, captures, assembly via Brutalist | Narration: local TTS voice (see film credits) |

---

## Assignment 3 — 3D props

| Tool | Version | Use |
|---|---|---|
| Blender | 5.2.2 LTS (Homebrew cask), macOS 15.6 Apple M4 | Modelling, .blend sources, glTF export |
| MCP for Blender ("mcp-for-blender", the community project the syllabus names) | package **2.1.9** via `uvx`; Blender add-on **1.8** | Claude Code driving my open Blender for the **castle**. Telemetry off (`DISABLE_TELEMETRY=true`; add-on consent off). Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Hunyuan3D and Tripo left off; no `generate_3d`, `search_assets` or `import_asset` calls. |
| uv | 0.13.1 (Homebrew) | runs the MCP server |
| Godot | 4.7.2.stable.official.ed1daf0bf | glTF import, `prop_room.tscn`, headless check |
| Claude Code (Claude Opus 5.5) | 2.1.295, in the Claude desktop app | see below |

**Geometry:** all three props are built from Blender primitives by code in `tools/blender/`. No downloaded or AI-generated meshes. Colours are hex values chosen in CHANGE-BRIEF.md; there is no external colour source.

**Who did what (A3):**
- **Me:** chose the three assets (dropped the cork) and character scale; reviewed and accepted the brief; installed/approved tools; did the "Learn the window" session and screenshots; ran the MCP build session for the castle and saved `castle.blend`. *Hand edit and human look-check: see FRICTIONAL.md for whether done.*
- **Claude:** drafted CHANGE-BRIEF A3 (numbers, colours, failure cases), BLENDER-NOTES descriptions, and the "What I noticed" sentences from options I picked. Wrote all Blender code: the castle via MCP in a separate session, windkey/toybox by script route. Wrote the export script, `prop_room.tscn`, `tests/check_props3d.gd` and `tools/shot_prop_room.gd`, and this session's docs. Found and fixed its own false-passing check.
