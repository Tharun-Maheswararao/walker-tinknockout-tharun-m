# COMPONENTS.md — what the film explains, and where it lives

Source: `godot/` at `64c037a`. Ledger: `gamedev-evidence.json` (schema 1, `code-then-result-v1`).

| Component | Files | Beats | Mechanism shown | Trade-off named |
|---|---|---|---|---|
| fighter | `fighter/fighter.gd` | B04, B06, B07 | Code-created `Sprite2D`, `centered = false` + `offset = -FEET`; `_rewind` crank → +10 wind per 90° → `rewind_tick` | One feet anchor for every pose keeps hurtboxes honest, but every pose must be drawn on the same 480×450 canvas |
| sfx | `audio/sfx.gd`, `assets/sfx/*` | B08, B09, (B10 heard) | `watch()` connects to `hit_landed`, `projectile_fired`, `rewind_tick`, `state_changed` | Listener-only audio is testable (muted == unmuted) but any new event needs a new signal |
| music | `audio/music.gd`, `assets/music/waltz.ogg`, `default_bus_layout.tres` | B08 notes, B12, B13 | pitch 0.85 below 25 % spring, PauseMuffle low-pass, stop on KO; loop seam checked | — |
| fighter-art | `assets/fighters/**`, `anchors.json` | B03, B05 | SDXL-Turbo pose → edits → 480×450, feet (240,435); Rivet recolour | eyes hand-painted on every pose |
| props-env | `assets/props/*`, `assets/env/bowl.png` | B02, B03 | bowl and props | bowl seen from outside, concept says inside |
| round-flow | `game/main.gd`, `game/main.tscn`, `game/controls.gd`, `project.godot`, `ui/hud.gd`, `fighter/rivet_brain.gd`, `fighter/cork.gd` | B02, B07, B09, B14 | round states, input read, HUD spring dials, Rivet's pattern | Rivet is a deterministic pattern, not AI (B14 proposes one change) |
| tests | `tests/test_slice.gd` | B11, B12 | 25 checks through real input; muted vs unmuted end state | cannot prove a person reads the fight with sound off |
| film-tools | `tools/capture_film.gd`, `tools/shots.gd` | B05, B07, B09 | scripted-input Movie Maker capture; posed screenshots | scripted player ≠ human player |

Excluded: `godot/.gitignore` (VCS ignore list, not loaded by the engine).

Saved vs runtime: `main.tscn` saves only the root `Main` node. Everything else is created in code at `_ready()`,
so the film shows scripts, not an Inspector, and invents no exported properties (the only `@export` is
`Fighter.skin`).
