# Credits — godot/assets/props/ (A7 wind-key sheets)

| File | Size | Made from | How |
|---|---|---|---|
| `key-bolt-sheet.png` | 672 × 60 (8 × 1 cells of 84 × 60) | `key-bolt.png` (committed, unchanged) | `godot/tools/generate_key_sheets.gd` (written by Claude, 2026-11-19), the recipe in `CHANGE-BRIEF.md` §2 |
| `key-rivet-sheet.png` | 672 × 60 (8 × 1 cells of 84 × 60) | `key-rivet.png` (committed, unchanged) | same script |

- **Source art:** `key-bolt.png` and `key-rivet.png` were generated in Assignment 2 with SDXL-Turbo (`stabilityai/sdxl-turbo`, revision `71153311d3dbb46851df1931d3ca6e939de83304`), run locally, from a prompt by Tharun: `ASSET-LOG.md` row PROP-KEY v1, seed 3 accepted; `key-rivet.png` is its recolour (`SOURCES.md`, "Generative models").
- **Licence:** Stability AI Non-Commercial Research Community License, the same terms as all of this project's SDXL-Turbo art (`SOURCES.md`). Each sheet is a derivative of its source key, made by resizing and mirroring only. Date checked: 2026-11-19.
- **The original files** the sheets are made from are committed next to them, unchanged. The script is the sheets' provenance: rerun it to reproduce them.

```bash
godot --headless --path godot --script res://tools/generate_key_sheets.gd
```
```bash
godot --headless --path godot --import
```

- **Slicing** (`CHANGE-BRIEF.md` §2): cell 84 × 60, `hframes` 8, `vframes` 1; cell k is the key turned k × 45°, width factor max(0.15, |cos θ|), cells 3–5 mirrored.

The other files in this folder (`cork.png`, `cutlass.png`, `popgun.png`, `key-bolt.png`, `key-rivet.png`) are A2 art; their credits are in `SOURCES.md`.
