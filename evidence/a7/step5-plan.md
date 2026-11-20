# A7 Step 5 plan: wire the clips to one authority (proposed by Claude, not yet approved)

*2026-11-19. The smallest plan I can find that meets `CHANGE-BRIEF.md`. No file has been edited for it. Each step is implemented only after Tharun approves it, then the diff and the test results are shown.*

## 5.1 The named rig and the authority moves (`fighter.gd` `_ready`, `_load_art`, `_apply_pose`; `steam_mount.gd`), with no clips yet

- **`_ready` builds the hierarchy with fixed names** (brief §7, "Fixed node names"):
  - `Fighter` → `FacingPivot` → `BodyPivot` → `sprite`;
  - `BodyPivot` → `KeyMount` → `KeyBob` → `key_sprite` (`z_index` −1, as now);
  - `Fighter` → `weapon`, unchanged in place (see D3).
- **`_load_art` (setup, once):** `key_sprite.texture` = `key-<skin>-sheet.png`, `hframes` 8, `vframes` 1, `scale` = 1/3. Nothing writes the key's scale after setup.
- **`_apply_pose` writes only what the brief gives it:**
  - `FacingPivot.scale.x = facing`;
  - `sprite.texture`, `sprite.scale = (1/3, 1/3)` without facing, `sprite.offset` as now;
  - `KeyMount.position` from `anchors.json` *without* the facing factor;
  - `KeyMount.visible` (false on KO);
  - `weapon` exactly as now.

  It drops the REWIND squash (`fighter.gd:271-273`) and every write to `key_sprite`. `key_spin` stays: it is written in `_rewind` (gameplay) and no longer read.
- **`SteamMount.follow()`** sets its global position to `KeyMount`'s global position, keeps the facing scale, and sets `visible` from `KeyMount.visible`. `z_index` is still copied from `key_sprite` (−1).
- **Expected after 5.1:** every suite at its baseline, except exactly the four brief-predicted assertions:
  - `test_slice` 23/2, lines 182 and 187;
  - `test_wind_steam_state` 35/2, lines 149 and 159.

  `test_a7_pins` stays 49/0, and both read-backs stay green. The key shows frame 0 everywhere until 5.2.

## 5.2 The two players and the clip sync (`fighter.gd` `_ready`, end of `step`, a `state_changed` listener)

- **`_ready`:** `FighterAnimPlayer` and `KeyAnimPlayer`, both direct children of `Fighter` with the default `root_node ".."` (D1), `callback_mode_process` = `ANIMATION_CALLBACK_MODE_PROCESS_MANUAL`. Each loads its clip resource from `godot/animations/` into its library; no track or key is built in code (CLAUDE.md, Ownership).
- **`_sync_clips()`**, called at the very end of `step` (after `_apply_pose`), once in `_ready`, and from a listener on the fighter's own `state_changed`:
  - **JAB:** `FighterAnimPlayer` plays `jab_action` at position `state_t`.
  - **Not JAB:** it seeks `jab_action` to 0, which is key 0 and the rest pose, then `stop(keep_state = true)`, so `current_animation` is `""` and the rig holds rest (D4).
  - **REWIND with wind < 100:** `KeyAnimPlayer` plays `wind_key_cycle` at `fposmod(state_t, 1.0)`.
  - **REWIND at wind 100:** it does nothing, so the key holds its last frame (brief §3).
  - **Any other state:** seek 0 (frame 0), then stop.
- **Why this gives the brief's clock** (§6):
  - the hitstop early return (`fighter.gd:129-131`) and the pause flag both skip `step`, so neither clip moves;
  - the entry tick has `state_t` 0, so the clip is at 0;
  - `state_changed` snaps the rig to rest the moment a hit turns JAB into HURT or KO, even though the next `step` is frozen by hitstop (D2).
- **Expected after 5.2:** the same counts as after 5.1.

## 5.3 The structure and state test, `godot/tests/test_a7_structure.gd` (at 60, also run at 30)

| Assertion | Brief rule |
|---|---|
| The real fighters have every named node, in the brief's parentage; both players are MANUAL | §7 fixed names, §6, B-R2 |
| Every clip name `fighter.gd` requests exists in its player's library | B-R1 (library existence) |
| `track_problems` finds nothing **on the real Bolt and Rivet** (closes the Step 3 and 4 fixture limit) | A-R2, B-R1 |
| `key_sprite` uses the skin's sheet, `hframes` 8, `vframes` 1 | A-R1 |
| Real J press: `FighterAnimPlayer.current_animation == "jab_action"` only in JAB, position equals `state_t` (with tolerance) on every tick 0..20, `""` and rest pose after | B-R2, §5 state table |
| Landed jab: position and pose frozen on e+6..e+10; pause: frozen | B-R2, §4 interrupts |
| A hit in startup, active or recovery: rest pose on the same tick as HURT | B-R3 |
| Real S held from wind 40: `KeyAnimPlayer` plays `wind_key_cycle`, frames 0..7 in order, held at full wind, frame 0 and `""` after release | A-R3 (headless part) |
| `FacingPivot.scale.x` has the sign of `facing`; `sprite.scale.x > 0`; Rivet's jab goes to −x | §1 facing, B-R4 (headless part) |
| `_apply_pose` writes none of the clip-owned properties: after a step in JAB, `BodyPivot`/`KeyBob` equal the clip's values at `state_t`; and `_apply_pose`'s source names no `BodyPivot`, `KeyBob` or `key_sprite` | one authority, §10 failure 3 |

Every input goes through `Input.parse_input_event`, and the current clip is read with `current_animation`. **Only a human can check:**
- whether the jab reads;
- whether the turn reads, and the seam over five wraps;
- registration;
- both backgrounds;
- that the key still draws behind the body.

## 5.4 The four planned pin updates (Tharun's own commit, after 5.1–5.3)

| File:line | Replacement |
|---|---|
| `test_wind_steam_state.gd:149` | key squash → `hframes == 8` and `wind_key_cycle` playing in REWIND |
| `test_wind_steam_state.gd:159` | `key_sprite.visible` → `not key_sprite.is_visible_in_tree()` |
| `test_slice.gd:182, 187` | `sprite.scale.x` sign → the `FacingPivot.scale.x` sign |

Each replacement is the one written in brief §7.

## Decisions for Tharun

- **D1. Where the players sit:** both as direct children of `Fighter`, default `root_node ".."`. The clips' paths already assume this (`evidence/a7/jab_action_keys.md`). The brief does not say.
- **D2. Rest snap on a hit, and the hitstop freeze frame:** the brief says the rig snaps to rest *on entry* to HURT or KO. But today a hit freezes the defender's whole look for 5 ticks (hitstop returns before `_apply_pose`), so the body texture stays the JAB pose during those ticks. Following the brief, the rig snaps to rest while the texture still shows JAB, for 5 ticks. The alternative is to snap on the first unfrozen step, keeping the freeze frame whole. **I recommend following the brief as written.** If play shows the mismatch, that's a tuning revision.
- **D3. `weapon` stays a direct child of `Fighter`:** the jab hides it, and the cutlass and pop poses play with the rig at rest, so nothing changes for them. Moving it under `FacingPivot` would change `_apply_pose`'s weapon writes for no visible gain.
- **D4. How "rest" is held:** `jab_action`'s key 0 is the rest pose, so outside JAB the player seeks it to 0 and stops. The same works for frame 0 of the key cycle. No extra RESET clip.

## Side effects to know about

- The A6 steam previews (`steam_preview.gd`, `steam_rewind_preview.gd`) build a real `Fighter`, so they get the new rig. Their committed A6 strips stay as history; a recapture would show the turning key instead of the squash.
- `fighter.gd` line numbers in CLAUDE.md move. I update the cited lines after 5.2, in its own small commit.
