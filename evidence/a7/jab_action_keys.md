# jab_action: each key's time beside the frame it comes from

*Written by Claude (A7 Step 4), from `CHANGE-BRIEF.md` §4 at 60 fps. Clip: `godot/animations/jab_action.tres`. Time = frame ÷ 60, stored in the `.tres` as a 32-bit float (`CLAUDE.md`, Headless facts), so the read-back compares within half a frame (1/120 s).*

| Key | Source frame (§4) | Phase boundary | Time in `.tres` (s) | Exact frame ÷ 60 (s) | `BodyPivot:position:x` | `BodyPivot:rotation` | `KeyBob:position:y` | Outgoing transition |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | startup begins (entry, rest) | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.5 (ease-out) |
| 1 | 3 | inside startup: coil peak | 0.05 | 0.050000 | −6.0 | −0.10 | +2.0 | 2.0 (ease-in) |
| 2 | 5 | **active begins** | 0.0833333 | 0.083333… | +14.0 | +0.12 | −2.0 | 1.0 (linear, hold) |
| 3 | 10 | last active frame | 0.1666667 | 0.166666… | +14.0 | +0.12 | −2.0 | 1.0 (linear) |
| 4 | 11 | **recovery begins** | 0.1833333 | 0.183333… | +8.0 | +0.05 | −1.0 | 1.0 (linear; was 0.5 ease-out until revision 1, 2026-11-22) |
| 5 | 21 | **end: back to IDLE, rest** | 0.35 | 0.350000 | 0.0 | 0.0 | 0.0 | 1.0 (no segment after) |

- **Clip:** `length` 0.35 s (21 frames), `step` 0.0166667 (1/60 s), `loop_mode` absent, so `LOOP_NONE` (0, the default).
- **Tracks:** three value tracks, linear interpolation (`interp = 1`), continuous updates (`update = 0`), all with the same six key times. Paths are relative to `Fighter`, assuming `FighterAnimPlayer` is a direct child of `Fighter` with `root_node ".."`; the brief does not say where the player sits (Step 5 plan).
- **Transitions:** Godot eases each segment with the *outgoing* key's transition, `ease(t, transition)`: below 1 starts fast (ease-out), above 1 starts slow (ease-in). These are the brief's values; Claude added none.
- **Frame 10's key** is there so the extension holds through the whole active window (§4: 14 at frame 5 and frame 10).
