# COMPONENTS.md — what the film explains, component by component

Coverage ledger: `gamedev-evidence.json` (27 A6 files in 6 components; 129 pre-A6 files excluded, each asserted
byte-identical to tag `a5`, `f4dda68`). Teaching contract `code-then-result-v1`: one checked excerpt pair (B05 → B06)
and five source-view pairs (B07 → B08, B09 → B10, B12 → B13, B14 → B15, B17 → B18). B03 shows each line and its strip
result in the same beat.

| Component | Files | Beats | Code shown | Visible result |
|---|---|---|---|---|
| Effect A, impact burst | `effects/impact_effect.tscn`, `impact_effect_blocked.tscn`, `game/main.gd` | B02–B10 | `impact_effect.tscn:28, 36-37, 77-86`, `7-9` (revision 1); `main.gd:228-238` | r0 / r1 fixture strips; the burst in play, including rapid repeats and the blocked variant |
| Effect B, wind steam | `effects/wind_steam.tscn`, `effects/steam_mount.gd`, `game/main.gd` | B02, B11–B16 | `wind_steam.tscn:35-43`; `main.gd:69-70, 241-242`; `steam_mount.gd:31-35` | D.2 strip; rewind r0 / r1; steam in play: start, pause, stop |
| Textures | `tools/generate_shard_texture.gd`, `generate_steam_texture.gd`, `effects/textures/*` | B21, B23 | — (credits only) | ATTRIBUTION.md quoted |
| Fixtures | `previews/*`, `game/debug_vsync.gd` | B06, B13, B14, B19, B22 | — | every strip is labelled FIXTURE; `gpu_price.tscn` and F10 named for the open GPU price |
| Process shader | `shaders/particles_generated.gdshader` | B17 | lines 7, 43, 258, 302, 315 | config test read-back of spread and gravity (B18) |
| Tests | `tests/test_impact_effect_*`, `test_wind_steam_*`, `cost_effects.gd` | B18, B19 | — | re-run counts; mutation FAIL lines; headless cost table |

## One complete input → state → output trace

B16, from the film capture log: jab input (`Input.parse_input_event`) → `Fighter._spend` lowers wind to 16 →
`wind_changed` → `main.gd:70` sets `amount_ratio = steam_ratio(16)` = 0.36 → steam appears at the key (zoom).
Rewind input → wind 14 / 24 / 34 → ratio 0.44 / 0.04 / 0 → the live puffs fade.

## Design choices and one trade-off each (as recorded)

- **A fresh burst per hit** (A-R3): overlapping hits never cut each other off. The cost is node instancing per hit,
  which the headless cost script measures as within the spread (B19).
- **SteamMount over `local_coords = false`** (Tharun's choice, TUNING): it keeps the key's 1/3 scale and follows Bolt.
  The cost is one more node and a copy of the key's transform every tick.
- **Shards opaque to 0.7** (revision 1): solid flecks over the castle. The cost: the fade is squeezed into the last
  frames (Tharun saw no blink), and the shards stay faint over the dark stretch (A6-5a; open).

## Not explained (and why)

- `impact_effect_blocked.tscn`'s values are not shown line by line. The blocked variant is shown in play (B10) and
  described in B02.
- `debug_vsync.gd` (F10) is named only in B19, as part of the open GPU-price check.
