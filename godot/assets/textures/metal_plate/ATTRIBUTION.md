# Metal Plate texture set: provenance

| | |
|---|---|
| **Asset** | Metal Plate (`metal_plate`) |
| **Source** | Poly Haven: https://polyhaven.com/a/metal_plate |
| **Author and role** | Rob Tuytel, credited for "All" (every map) by the Poly Haven API (`https://api.polyhaven.com/info/metal_plate`) |
| **Licence** | CC0 1.0 (public domain dedication). Poly Haven's licence page (https://polyhaven.com/license) says "Our assets are all licensed as CC0". No credit is required; the course requires provenance anyway. |
| **Date checked** | 2026-11-01, by Claude Code for Tharun Maheswararao |
| **Downloaded** | 2026-11-01 from `https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/metal_plate/<file>` |
| **Real-world size** | 0.5 × 0.5 m (Poly Haven `dimensions` 500 × 500 mm) |

## Files

The source PNGs are kept unmodified. Each is 1024 × 1024 and 16 bits per channel. The SHA-256 of each file as downloaded:

| File | Role in this project | SHA-256 |
|---|---|---|
| `metal_plate_diff_1k.png` | Colour (sampled with `source_color`) | `00401b4ce56f0ffa8b2c1e10366fa36a7a9b839199b3abac2678790a9883c2e9` |
| `metal_plate_nor_gl_1k.png` | Normal map, **OpenGL convention** (the one Godot expects), sampled with `hint_normal` | `d858021ebc0a2a01ec13e574bc47ed58795e129904cda2868b3fb2dfd02d6741` |
| `metal_plate_rough_1k.png` | Roughness and wear mask, sampled as data (no `source_color`) | `aa6e4947c33559a7012e275d1600bfa6e00c2824271726a94de69f1a7b7fed2e` |
| `metal_plate_nor_dx_1k.png` | **DirectX** convention. Calibration only, for the curl check in `godot/tests/normal_map_check.gd`. Not bound to any material. | `2585efa45e5c2794150082b05fd177d25c67aadd18411fd06648705f1536bb43` |

The normal map used in materials is `_nor_gl`.
