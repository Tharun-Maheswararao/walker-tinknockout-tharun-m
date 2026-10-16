# SUBMISSION — Assignment 3

*(The Assignment 2 submission note is preserved at tag `a2`, commit `9788922`.)*

- **Assignment:** Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender
- **Student:** Tharun Maheswararao (maheswararao.t@northeastern.edu)
- **Project name:** walker-tinknockout-tharun-m (Tin Knockout)
- **GitHub repository URL:** https://github.com/Tharun-Maheswararao/walker-tinknockout-tharun-m
- **Git tag and submitted commit SHA:** tag `a3`; the SHA is given in the Canvas copy of this note (a commit cannot contain its own hash).
- **Game-source revision shown in the film:** no A3 film was made (see Known limitations).
- **Godot version, Blender version, and operating system:** Godot 4.7.2.stable.official.ed1daf0bf · Blender 5.2.2 LTS · macOS 15.6 (Darwin 24.6.0), Apple M4
- **The three assets and what each is for:**
  - `castle`: the sunken-castle ornament on the goldfish-bowl floor; the environment landmark behind the fighters. 1.80 × 0.82 × 2.30 m.
  - `windkey`: a spare brass winding key; a collectible that would refill Bolt's spring. 0.60 × 0.14 × 0.70 m.
  - `toybox`: the tin toy box that future weapon pickups come out of; a prop. 1.26 × 0.76 × 0.75 m.
- **MCP project and version, or "script route":** MCP for Blender (`mcp-for-blender` 2.1.9, Blender add-on 1.8) for **castle**. **Script route** (headless Blender) for **windkey** and **toybox**, because time ran out, not because the MCP failed.
- **My hand edit in Blender:** recoloured the toy box band from navy `#23395B` to green `#2E7D32` in the Material tab (Base Color) in Material Preview; size and scale unchanged; re-exported (before/after screenshots in `evidence/blender/`).
- **Checks run (command and result):**
  - `godot --headless --path godot --import`: no errors.
  - `timeout 120 godot --headless --path godot --script res://tests/check_props3d.gd --fixed-fps 60`: `RESULT: PASS (0 failing)`. Size within ±0.01 m of the brief, base at y = 0, scale 1 and rotation 0, upright, front at +Z, triangles within budget, all three on the floor in `prop_room.tscn`. Output in `evidence/check_props3d.txt`.
  - Headless re-run of `tools/blender/build_castle.py` and inspection of each `.blend`: dimensions, origin, scale and colours match the brief.
- **Final film URL and filename:** none; not made.
- **Final film SHA-256:** n/a
- **Summary of my changes:** an A3 brief committed before building; Blender MCP set up (with three setup fixes logged); castle built through the MCP, key and box by script route; three `.glb` files, a Godot prop room, and a headless check that Claude first wrote wrongly (false pass) and then fixed; interface notes and an A3 test report.
- **Known limitations:** only one asset used the MCP route (the rubric asks for two). **No Brutalist film was made**, because the deadline arrived first. The cream lid reads near-white under the scene light (TEST-REPORT A3-7). The prop room is not connected to the 2D game. Godot exits 0 even when a check script fails to parse, so the RESULT line is the evidence.
- **Changed games since Assignment 2:** no.
