# CHANGE-BRIEF — Assignment 6: two particle effects for Tin Knockout

*Version 1 · 2026-11-08 · committed before the first prompt. The A2, A3 and A5 briefs are in history at tags `a3` and `a5`. Later changes go under "A6 revisions" at the bottom, dated, and never rewrite this version.*

> **Authorship:**
> - **Layout:** Claude laid out these headings from the Assignment 6 handout. File:line facts come from `design/a6/BRIEF-FACTS.md`.
> - **Mine:** the choice of both effects (2026-11-08) and every decision and value under the headings. Drafting help is listed below.
> - **Help I asked for:**
>   - 2026-11-08, A.2–A.3, B.1–B.4: Used an external LLM, Claude 3.5 Sonnet, to draft initial structural bullet points for sections A.2, A.3, B.1, B.2, B.3, B.4, C, D, E, F and G, which I subsequently reviewed, corrected against Godot particle behavior, and integrated. The corrections came from Claude Code's reviews: an additive layer cannot draw a dark outline, so the dark edge and the cyan core went on separate MIX and ADD emitters; the scale row mixed view and window pixels; a 0.25 s lifetime leaves strip frames 20, 30 and 50 empty and does not remove the need for a retrigger rule; in A.3, a `Curve` clamps points above `max_value` 1.0 (probed in 4.7.2), `gravity` is a `Vector3`, a 64×64 default gradient made the core about 100 px wide, and the core curve's start disagreed with A.2.
>   - 2026-11-08, A.1: Claude's review of my first draft pointed out that hits already have shake, hitstop, the clang and the star; that `p` is the attack box's centre, not the overlap; and that the star is a static polygon, not debris. I rewrote A.1 with those corrections.

---

## A. Effect A — impact burst

### A.1 The job

| | |
|---|---|
| **What it tells the player, and why they need it** | Rather than confirming that a hit happened—which the current 0.15s camera shake, 0.07s hitstop, tin clang sound (`SFX-JAB`), and star spark already do—Effect A adds visual contrast and variety. The current feedback uses the exact same static star spark for every single connection, which blends in and easily disappears against bright background elements like the castle wall. Effect A gives the hit distinct visual weight and better readability across different arena backgrounds. |
| **Blocked hits** | **Different.** Blocked hits show a smaller, muted grey-tin deflection burst instead of the full Effect A, clearly signaling that the attack was successfully parried or guarded. This needs the `blocked` flag passed from `_on_hit` and `Cork.struck` to `_on_impact` (`main.gd:200-207`; `_on_hit` drops it today, `main.gd:202`). |
| **Event** | Every impact: a melee hit (`Fighter.hit_landed`, `fighter.gd:14`, emitted at `:197`) or a cork hit (`Cork.struck`, `cork.gd:11`, emitted at `:24`). Both already arrive at `main._on_impact(p)` (`main.gd:200, 202-207`). |
| **Position** | `p` from `main._on_impact`. For melee attacks, `p` represents the center of the attacker's 2D attack box (`main.gd:204`), which means it can sit slightly in front of the target sprite rather than at the exact overlap intersection. We will use `p` directly because it provides a reliable, consistent origin point tied to the attack action without requiring extra 2D polygon intersection math between collision boxes. For cork hits, `p` is the cork's position (`main.gd:200`). |
| **The existing hand-drawn sparks** (`main.gd:207, 221-228`) | **Kept.** The existing star spark is not particle debris—it is a single 16-point static star polygon that scales slightly and fades over 0.14s (`main.gd:221-228`). Keep the star spark as the base flash layer and use Effect A to add the dynamic, moving element (burst lines/secondary shapes) on top of it. This builds on the existing impact pop rather than removing working feedback code from `main.gd`. |

### A.2 Intent: how it reads

| | |
|---|---|
| **Timing phases** (rough durations) | Total lifetime is 0.25 seconds (staying safely below the ~0.4s maximum jab cycle to prevent visual clutter), beginning with an instant 0.05s snap expansion, followed by a 0.20s smooth fade-out and gentle contraction. |
| **Contrast** against the named background | A dark edge and a bright core, on separate emitters: the shards use `MIX` blend with a dark-rimmed tin shard texture to ensure a visible dark edge against bright castle backgrounds; the core/dust uses `ADD` blend with a soft radial gradient to provide the glowing cyan core. Readable against both the darkest (x 256–287, mean luminance 98) and lightest (x 192–223, mean luminance 160) sections of the background (`design/a6/BRIEF-FACTS.md` §4). |
| **Scale** against the character | Spans approximately 60 pixels wide in the 1280×720 window (representing roughly 70% of a fighter's helmet height). |
| **Change over life** (colour, alpha, scale) | Starts at full scale and 100% opacity, expands by 20% to 50% (`1.0` to `1.2–1.5`) during the active phase. The shards fade from dark charcoal to transparent; the core ramp transitions from bright cyan (`0, 1, 1`) through deep blue (`0, 0.3, 0.7`) to transparent. |
| **Variation** | Randomizes shard ejection angle (full 360 degrees), initial velocity speed (±20%), and particle rotation so rapid repeated hits never look stamped or repetitive. |
| **Emitters**, each with its job | Two emitters alongside the retained static star flash (`main.gd:221-228`): **Shards** (`MIX`, dark-rimmed tin shard texture), a fast outer ring of tiny tin shards; **Core/Dust** (`ADD`, soft radial gradient), a slower, soft-fading cyan glow at the impact center. Blocked hits: the smaller, muted grey-tin burst above. |

### A.3 Settings

Scene: `godot/effects/impact_effect.tscn`, one root node with the two emitters below. Blocked hits use `godot/effects/impact_effect_blocked.tscn` (A.3c).

**Both emitters** (node settings)

| Setting | Value | Why |
|---|---|---|
| Node type | `GPUParticles2D`, process settings in a `ParticleProcessMaterial` | Same node type as Effect B; calculations processed on the GPU. |
| one_shot | true | _(it is a burst)_ |
| explosiveness | 1.0 | Forces every particle to emit instantaneously on frame 1, creating the sharp "snap" required for an impact hit. |
| lifetime | 0.25 s | A.2 timing phases. |
| local_coords | false | Ensures particles stay anchored in world space at impact point `p` even if the fighters move or get knocked back during the hitstop. |
| visibility_rect | default `Rect2(-100, -100, 200, 200)`, read back by the config test | The default 200×200 box is more than large enough to safely bound a 30 px burst without risking culling bugs. |
| preprocess | 0.0 | Instantaneous impact burst. |

**A.3a Shards emitter**

| Setting | Value | Why |
|---|---|---|
| amount | 16 | Provides enough individual fragments for a crisp debris feel without cluttering the screen or impacting performance. |
| emission shape | Point (`EMISSION_SHAPE_POINT`) | |
| initial_velocity_min / max | 60.0 / 90.0 px/s | Speeds designed to push tin fragments outward into the ~15 px radius ring. |
| spread | 180.0° | Full omnidirectional burst. |
| angle_min / max | -180.0 / 180.0° | Fully randomized shard rotation. |
| gravity | `Vector3(0, 400, 0)` | Gives the tiny tin fragments physical weight so they arc downward like real debris. |
| damping_min / max | 100.0 / 150.0 | Rapid deceleration so debris stays clustered near the impact point `p`. |
| color_ramp | `Color(0.25, 0.25, 0.28, 1.0)` → `Color(0.1, 0.1, 0.1, 0.0)` | Dark charcoal fading to transparent. |
| scale_min / max | 0.8 / 1.2 | |
| scale_curve | 1.0 at 0.0 → 1.2 at 0.2 (0.05 s) → 0.4 at 1.0 (0.25 s); curve `max_value` 2.0 | `max_value` 2.0 prevents default 1.0 clamping on scale points > 1.0. |
| texture | 8 × 8 px PNG written by a committed script, `tools/generate_shard_texture.gd` | Provides a custom dark-rimmed tin shard texture since none exists in the base repository. |
| draw material | `CanvasItemMaterial`, `blend_mode` MIX | Dark edge against bright backgrounds (A.2). |

**A.3b Core emitter**

| Setting | Value | Why |
|---|---|---|
| amount | 8 | Keeps the glowing impact flash dense enough to read as a solid core without oversaturating the blend mode. |
| emission shape | Point (`EMISSION_SHAPE_POINT`) | |
| initial_velocity_min / max | 10.0 / 20.0 px/s | Slow, controlled energy expansion. |
| spread | 180.0° | |
| gravity | `Vector3(0, 0, 0)` | Keeps the energy flash expanding symmetrically around the impact point `p`. |
| damping_min / max | 50.0 / 80.0 | |
| color_ramp | `Color(0.0, 1.0, 1.0, 1.0)` at 0.0 → `Color(0.0, 0.3, 0.8, 0.8)` at 0.5 → `Color(0.0, 0.3, 0.7, 0.0)` | Bright cyan, transitions to deep blue, and fades out. |
| scale_min / max | 1.0 / 1.2 | |
| scale_curve | 1.0 at 0.0 → 1.5 at 0.2 (0.05 s) → 0.2 at 1.0 (0.25 s); curve `max_value` 2.0 | Rapid flash expansion. |
| texture | `GradientTexture2D`, `fill` radial, centred _(fill_from (0.5, 0.5))_; explicit size 16 × 16 px (instead of the 64×64 default) so the core particles remain tightly scaled within the 30 px total effect scope | Generates a smooth soft radial gradient purely in engine resources without needing an external image asset file. |
| draw material | `CanvasItemMaterial`, `blend_mode` ADD | Glowing cyan core (A.2). |

**A.3c Blocked burst** — `godot/effects/impact_effect_blocked.tscn`

A second small scene file. Keeps scene settings declarative and clean per course preference, cleanly separating the grey muted deflection values from the full unblocked effect scene. Values: the shards' colour ramp is replaced with muted grey-tin `Color(0.5, 0.5, 0.5, 1.0)` fading to `Color(0.5, 0.5, 0.5, 0.0)` at the end, matching the unblocked shards so the blocked burst fades out smoothly rather than snapping out abruptly; the core's cyan/blue ramp is replaced with a faint desaturated grey-white ADD flash, `Color(0.6, 0.6, 0.6, 0.8)` fading to alpha `0.0`, so the blocked hit is fully muted across both layers; `amount = 8` for shards, `amount = 4` for core; `scale_min = 0.5`, `scale_max = 0.7`. Everything else as A.3a/A.3b.

> **Shard motion (my decision on Claude's review note, 2026-11-08):** Keep it as it is. The downward gravitational sag (~12 px) and the 10–19 px dispersal radius give the tin debris a physical, heavy feel while relying on the scale curve for the visual snap.

### A.4 Observable rules

| # | Rule | Evidence: headless test, frame strip, or my eyes, and how |
|---|---|---|
| A-R1 | Fires on every event the retrigger rule allows, never otherwise, including on scene load. | Headless state test driving automated combat inputs, counting spawned effect instances against `hit_landed` and `struck` event signals to verify it fires on every impact and never otherwise, and asserting that the instance count is strictly `0` immediately upon scene load. |
| A-R2 | Fires at the event's position `p`. | Headless position assertion test verifying that every spawned effect instance's global position precisely matches the impact coordinate `p` passed from `main._on_impact`. |
| A-R3 | **Overlap.** Instantiate a fresh `impact_effect.tscn` per impact, connected to free itself via the `finished` signal. Most bursts alive at once: `4` bursts (96 particles max), accounting for the worst-case overlap where both fighters' melee hits and in-flight corks land within the same 0.25s window. | Headless retrigger test invoking two impacts within a single 0.25s lifetime using count tracking to verify that the overlap rule correctly spawns distinct instances without silent instance accumulation or premature cutting. |
| A-R4 | Spawn the effect as a child of `Main` at position `p` (captured before `cork.queue_free()`, `main.gd:200`), ensuring freeing the cork mid-flight has zero impact on the running animation. | Headless position assertion test verifying the effect node persists independently of the freed cork entity. |
| A-R5 | Blocked hit scene selection: unblocked hits spawn `impact_effect.tscn`; blocked hits spawn `impact_effect_blocked.tscn`. | Headless scene-type check verifying file paths match the incoming `blocked` flag. |
| A-R6 | Draw order: the effect node's `z_index = 6`, to draw cleanly above the existing star layer (`z_index = 5`, `main.gd:88`). | Visual check in running game. |
| A-R7 | Pause: keep `PROCESS_MODE_ALWAYS` (inherited from Main, `main.gd:38`) so the short 0.25s burst finishes its animation naturally even if pause (`main.paused`) is toggled. | Headless pause state assertion test. |
| A-Look | Reads as the intent above, on screen. | Frame strip verification confirming that frames 10, 12, and 15 show the active burst expansion and fading while frames 20, 30, and 50 are completely empty, backed by a visual run-through at 1280×720 to verify high readability and contrast against both the darkest and lightest stretches of the castle background. |

> **Review note (Claude, 2026-11-08):**
> - Probed in 4.7.2 (headless and windowed, 30 fps): a one-shot `GPUParticles2D` started with `restart()` after it is in the tree emits `finished` about 7 frames (0.23 s) later. In a probe that set `emitting = true` before the node had processed a frame, `finished` never fired, so a burst freed by `finished` would never be freed.

---

## B. Effect B — wind feedback loop

### B.1 The job

| | |
|---|---|
| **What it tells the player, and why they need it** | While the HUD dial displays exact wind values, players fighting at high speed cannot afford to look away from the character sprites to check UI meters. Effect B places a visceral exhaustion cue directly on the fighter's back (at the key sprite), giving peripheral spatial awareness of critical wind depletion and impending stall states without breaking visual focus. |
| **Job** | Feedback loop following a game value. |
| **Value** | `Fighter.wind` (0–100, `fighter.gd:27, 49`), announced by `Fighter.wind_changed(fighter, wind)` (`fighter.gd:17`). It drains 3/s while walking (`:29`) and on each attack (`_spend`, `:242-244`), and rises 10 per ratchet click while rewinding (`:31, 211-212`). |
| **Which fighters** | One per fighter (both Bolt and Rivet). Applying it to both fighters allows the player to read Rivet's wind status directly during combat, creating clear tactical opportunities to predict and punish low-wind vulnerabilities or incoming rewinds. |
| **Condition** | It triggers dynamically as wind drops, activating specifically when wind falls below the 25 threshold (matching the musical slowdown cue, `main.gd:15`), signaling an active warning state before hitting the 1.6s defenceless EMPTY stall (`fighter.gd:35`). |
| **Mapping** | Ramp only below 25. The effect remains entirely dormant (`amount_ratio = 0.0`) while wind is ≥ 25, and scales linearly from `0.0` at wind 25 to `1.0` at wind 0. This matches the existing music slowdown cue and keeps the exhaustion steam hidden during normal high-wind combat. |
| **Feature Effect A doesn't use** | `amount_ratio` (dynamically scaling active particle density without triggering a system restart), continuous emission (`one_shot = false` instead of a one-shot burst), and local coordinates (`local_coords = true` so the steam/pressure puffs track and move naturally with the fighter's back key sprite). |

> **Review note (Claude, 2026-11-08):**
> - The handout's candidates for this feature are process or draw features; `amount_ratio` is the one on its list. Continuous emission and `local_coords` are node settings.


### B.2 Intent: how it reads

| | |
|---|---|
| **Timing** (start, steady state, stop) | Continuous emission begins emitting as wind drops below 25, subject to particle pool threshold (noted as potential failure case F2: slight delay before first visible puff appears); maintains steady-state output proportional to the exact wind level; and stops smoothly over one particle lifetime (when emission cuts via `amount_ratio = 0`) as wind recovers above 25 or during rewind recovery steps. |
| **Contrast** against the named background | Utilizes a semi-transparent grey-white steam texture with a dark core/outline, ensuring high legibility and contrast against both the bright castle background (mean luminance 160) and dark water/fighter clothing. |
| **Scale** against the character | Puffs start small (~5 pixels) right at the key sprite's mount point and expand to roughly 15–20 pixels wide, keeping them proportional (about half the width) to the 35–40 view-pixel key sprite on the fighter's back. |
| **Change over life** | Alpha fades smoothly from 0.8 down to 0.0, the core diffuses outward, and particle scale expands from about 5 px to 15–20 px (a ~3× growth factor matching natural steam expansion) over each puff's individual lifespan as the steam dissipates. |
| **Variation** | Randomizes initial emission angle (±30° cone), initial velocity, particle rotation, and lifespan variance (`lifetime_randomness = 0.3`) so the continuous steam flow looks natural and organic rather than mechanically uniform. |
| **Emitters**, each with its job | Uses a single dedicated emitter (`GPUParticles2D`) configured for continuous steam exhaust, driving its density adjustments entirely through real-time `amount_ratio` scaling. |

### B.3 Settings

Scene: `godot/effects/wind_steam.tscn`, one emitter, one instance per fighter, parented to each fighter's `key_sprite`.

**Scale rule:** `key_sprite` is scaled to 1/3 (`ART_SCALE`, `fighter.gd:260, 273`). To compensate, we multiply base velocities by ×3 so they resolve to the intended on-screen sizes and speeds. Lengths in this table are in `key_sprite`'s local units; on screen they are 1/3.

| Setting | Value | Why |
|---|---|---|
| Node type | `GPUParticles2D`, `ParticleProcessMaterial` | `amount_ratio` exists only on the GPU node in 4.7 (`design/a6/BRIEF-FACTS.md` §5). |
| amount (fixed, the maximum) | 25 | Maximum active particle pool scaled dynamically via `amount_ratio`. |
| one_shot | false | Continuous emission. |
| explosiveness | 0.0 | Continuous steam exhaust requires an even, steady stream of particles over time rather than a single frame burst (`explosiveness = 1.0`). |
| lifetime | 0.6 s | |
| lifetime_randomness (on the process material) | 0.3 | Lifespan variance (B.2). In Godot, randomness only shortens individual particle lives, ensuring frame 70 remains strictly empty. |
| emission shape | Point (`EMISSION_SHAPE_POINT`) positioned directly at the fighter's back key sprite | |
| direction | `Vector3(0, -1, 0)` | Combined with gravity, to ensure the steam properly rises upward from the back key. |
| initial_velocity_min / max | 60.0 / 120.0 local (20 / 40 px/s on screen) | |
| spread | 30.0° | Godot 4 treats spread as a half-angle, yielding the correct ±30° cone. |
| gravity | `Vector3(0.0, -180.0, 0.0)` local (−60 px/s² on screen) | Negative Y for rising steam/exhaust. |
| damping_min / max | 90.0 / 150.0 local (30 / 50 on screen) | |
| color_ramp (colour and alpha) | `Color(0.85, 0.85, 0.85, 0.8)` → `Color(0.9, 0.9, 0.9, 0.0)` | Soft grey-white fading out to transparent; starting alpha unified at 0.8 with B.2. |
| scale_min / max | 0.2 / 0.8 | With the 32×32 texture and `key_sprite`'s 1/3: 2–8.5 px on screen at the start (about 5), 6–26 px at the end (about 16), so puffs start small at ~5 px and expand toward 15–20 px. Not multiplied by 3 again. |
| scale_curve | 1.0 → 3.0 over lifetime, curve `max_value = 3.0` | Preventing default 1.0 clamping. |
| texture | 32 × 32 px PNG written by a committed script, `tools/generate_steam_texture.gd`: a soft steam puff with a darker core/outline | Prevents it from washing out against bright backgrounds (B.2 contrast). |
| draw material, blend | `CanvasItemMaterial`, `blend_mode` MIX | |
| local_coords | true | So the steam/pressure puffs track and move naturally with the fighter's back key sprite. |
| parent and flip | Parented directly to the fighter's `key_sprite` node, automatically inheriting position and scale flips when the fighter changes direction (facing left/right). This automatically handles position tracking and ensures the steam correctly hides on KO (`fighter.gd:274`). Consequences: it draws behind the body (`key_sprite.z_index = -1`, `fighter.gd:76`) and squashes horizontally with the spinning key during REWIND (`fighter.gd:272-273`). | |
| visibility_rect | `Rect2(-150, -150, 300, 300)` local (±50 px on screen) | Unscaled, ±17 px on screen would cull puffs that rise 25–30 px. |
| preprocess | 0.0 | Dormant at round start when wind is 100. |

**Mapping:** wind ≥ 25 → `amount_ratio` 0.0; wind 25 → 0 maps linearly to `amount_ratio` 0.0 → 1.0 (B.1).

### B.4 Observable rules

| # | Rule | Evidence |
|---|---|---|
| B-R1 / B-R2 | Activates when wind drops below 25 (`amount_ratio > 0`). Stops smoothly by returning `amount_ratio` to `0.0` while `emitting` stays `true`, allowing existing puffs to fade out naturally over one particle lifetime (0.6s) during wind recovery or rewind. | **Headless:** driving combat attacks to drop wind below 25, then triggering a rewind to raise wind back above 25, asserts that `amount_ratio` transitions from `0` to active (>0) and back down to `0` while `emitting` remains `true`. **Strip / eyes:** verifies the smooth 0.6s particle fade-out without abrupt visual cuts. |
| B-R3 | `amount_ratio` scales linearly below wind 25: `amount_ratio = (25 − wind) / 25`, while the base `amount` property remains permanently locked at `25`. | **Headless:** real game input (exact jab attacks, each costing 12 wind, `fighter.gd:41`) drops wind from 100 down to 16 and 4 through the live game loop; asserts `amount_ratio` is `0.36` at wind 16 and `0.84` at wind 4, and `amount == 25`. |
| B-R4 | Inherits `PROCESS_MODE_ALWAYS` from Main, keeping the particle simulation active during game pauses (`main.paused`) so ongoing exhaust puffs complete their natural lifecycle without freezing mid-air. `get_tree().paused`: the game never sets it, but because of `PROCESS_MODE_ALWAYS`, the effect also keeps running under tree pauses unless explicitly overridden. | **Headless:** asserts `can_process() == true` via `PROCESS_MODE_ALWAYS`, that `emitting` and `speed_scale` are unchanged, and that the ratio holds steady while `main.paused = true`. **Strip / eyes:** verifies that particle motion and puff traversal continue uninterrupted during pause. |
| B-R5 | Automatically hides when parent `key_sprite` is hidden (such as on fighter KO via `fighter.gd:274`), preventing orphaned steam effects from floating in space. | Headless KO state test asserting that when the fighter's state shifts to KO, the key sprite and its particle child inherit hidden visibility. |
| B-R6 | Wind initializes at 100 on scene load and round restarts (`fighter.gd:101`), forcing `amount_ratio = 0` on frame 1 so zero particles spawn on startup regardless of preprocess settings. | **Headless:** asserts `amount_ratio == 0` on frame 1 of scene load. **Strip / eyes:** confirms zero visible puffs are rendered on startup. |

---

## C. Boundaries

This section defines the strict architectural line between presentation updates and core game simulation rules, establishing what is permitted to change and what must remain untouched.

**May change (presentation only):**
- **Combat feedback & impact routing:** modifying `main.gd` (`_on_hit`, struck handlers, and `_on_impact`) to pass the blocked flag and spawn `impact_effect.tscn` or `impact_effect_blocked.tscn` (while keeping the existing star layer intact).
- **Wind steam integration:** code that attaches a `wind_steam.tscn` instance to each fighter's `key_sprite` and drives `amount_ratio` dynamically from `wind_changed` signals (housed either directly in `main.gd` where the A5 tint driver lived, or via a dedicated driver script).
- **Assets & tooling:** the new effect scenes, automated state/headless tests, preview scenes, and procedural texture generation scripts (`tools/generate_shard_texture.gd`, `tools/generate_steam_texture.gd`, and their corresponding PNGs).
- **Debugging utilities:** a vsync debug key (F10–F12).

**Must not change (core engine & simulation):**
- **Core physics & mechanics:** collision boxes, hurtboxes, movement physics, input handling (`controls.gd`), the fighter state machine and its internal timings, and base wind/health arithmetic (`fighter.gd`).
- **Existing infrastructure:** existing test expectations, the A5 shaders located in `godot/shaders/`, `project.godot`, the base star spark, camera shake, and hitstop logic.
- **Read-only boundary rule:** presentation code is strictly permitted to read game state variables (such as wind, blocked status, and impact position `p`); it must never write to or modify core game state simulation variables.

## D. Frame strips

All preview captures are **fixture** captures. Each preview instance has `use_fixed_seed` on; the effect scenes never do.

### D.1 Effect A: impact burst preview (`godot/previews/impact_preview.tscn`)

- **Background setup:** positioned over the light castle stretch (x = 192–223, mean luminance 160) to rigorously test the dark-rimmed shards and bright cyan core contrast against a high-luminance background where the original star spark vanished.
- **Trigger:** frame 10. **Retrigger setup:** fires a second impact at frame 11 to demonstrate the `A-R3` overlap rule; the second burst completes its 0.25s lifetime by frame 18.5.
- **Frame-by-frame predictions (30 fps):**
  - **Frame 10 (trigger):** instantaneous spawn. Particles may first appear on frame 11; I'll record it once if so.
  - **Frame 12 (0.067 s):** just past the scale peak. Shards have expanded outward by 4–6 px. Ramps are roughly 25% through their life, displaying the bright cyan core and dark-rimmed debris.
  - **Frame 15 (0.167 s):** shards have traveled 8–14 px out with noticeable downward gravitational sag. Scale is falling toward 0.4 / 0.2. Simultaneously, the second burst overlaps here: burst 1 is at 67% of its life (fading, scale falling toward 0.4), while burst 2 (triggered at frame 11) is at 53% of its life (past its scale peak, actively dispersing).
  - **Frames 20, 30 and 50:** completely empty, confirming the 0.25 s lifetime concludes cleanly for both bursts.

### D.2 Effect B: wind steam preview (`godot/previews/steam_preview.tscn`)

- **Rig setup:** uses a stand-in `key_sprite` at scale `1/3` to accurately reflect parent scaling, rendered with `use_fixed_seed` enabled on the preview instance and `--quit-after 80` specified for the Movie Maker capture run.
- **Wind/ratio schedule:** condition starts at frame 10 (setting `amount_ratio = 1.0`), runs at steady state until frame 50, and cuts emission at frame 50 (`amount_ratio = 0.0`, `emitting` stays true, B-R2).
- **Background setup:** x = 256–287 (the darkest water/castle boundary stretch, mean luminance 98), to verify steam legibility.
- **Frame-by-frame predictions (30 fps):**
  - **Frame 12:** initial emission beginning; small initial puffs (~5 px) emerge upward from the key anchor point.
  - **Frame 20:** rising exhaust plume establishing density and vertical travel along the `Vector3(0, -1, 0)` direction vector.
  - **Frame 40:** fully established steady-state stream (exceeding one 0.6 s / 18-frame lifetime). Displays a continuous column of rising steam puffs expanding from ~5 px to ~16 px with soft edges and visible contrast against the background.
  - **Frame 55:** emission has ceased (ended at frame 50), leaving the remaining active tail-end puffs floating upward and fading out.
  - **Frame 70:** completely empty, confirming all active particles have completed their lifetime and cleared out.

## E. Predicted failures

| # | Prediction | The check that catches it |
|---|---|---|
| F1 | **Scale curve clamping (Effect A & B):** default `Curve` max value is `1.0`. Setting scale points above 1.0 (such as the core's 1.5 or B's 3.0) is silently clamped to 1.0, flattening growth. | Automated configuration test reading back the curve's control points directly (verifying that the core's control point at x = 0.2 retains its value of 1.5 and Effect B's point at x = 1.0 retains its value of 3.0). |
| F2 | **Finished signal dropout / instance leak (Effect A):** if `emitting = true` is set before a one-shot `GPUParticles2D` node enters the tree or processes its first frame, the `finished` signal never fires, causing instances freed on completion to pile up silently. | Headless instance count tracking test verifying that instance counts return to zero after particle lifetimes expire. |
| F3 | **Visibility rect culling (Effect B):** default bounding boxes cull steam puffs as they rise and expand, causing particles to pop out abruptly near the edges. | Visual strip inspection and bounds assertion verifying `visibility_rect` (`Rect2(-150, -150, 300, 300)`). |
| F4 | **Godot 3 property name legacy (config check):** using outdated Godot 3 syntax (e.g., `initial_velocity`) silently leaves velocity min/max at zero. | Property validation test scanning scene files for valid Godot 4 property names (`initial_velocity_min` / `initial_velocity_max`), catching silent Godot 3 legacy failures; the configuration test's read-back of both values fails too (Step 2 mutation). |
| F5 | **Delayed first puff (Effect B):** Effect B does not emit its first visible puff immediately at wind 25 because `amount_ratio` yields a fractional particle count until wind drops slightly lower (around wind 24). | **Headless node-state check:** automated test verifying that the calculated particle emission threshold (`amount × amount_ratio`) reaches ≥ 1.0 at wind = 24 (25 × 0.04 = 1.0). **Strip / eyes:** visual frame strip inspection to record the exact frame where the first visible puff physically emerges from the key sprite. |

## F. Price predictions and budget

The effects-off reference: Visual Profiler, Render Viewport 0.97 ms GPU / 0.11 ms CPU (2026-11-08, `evidence/a6/visual-profiler-vulkan.webp`).

| | Effect A (impact burst) | Effect B (wind steam) |
|---|---|---|
| Peak particle count | 4 concurrent bursts × 24 particles = 96 particles max | 2 fighters × 25 base amount = 50 particles max at `amount_ratio = 1.0` |
| Predicted headless CPU price | Near zero for the particle simulation itself (the dummy headless renderer skips GPU particle updates); Effect A's dynamic instancing/freeing (up to 4 scenes per window) incurs minimal CPU instantiation overhead. Within the empty-scene control's spread (±0.03 ms). | Near zero for the particle simulation itself. Within the empty-scene control's spread (±0.03 ms). |
| Predicted GPU time | ∼0.12 ms per active burst | ∼0.08 ms per fighter at full ratio |
| Budget, and which price | < 0.55 ms peak for 4 concurrent bursts (comfortably accommodating the 4 × 0.12 ms = 0.48 ms predicted worst case), compared on GPU time against the 0.97 ms baseline | < 0.20 ms combined for both active fighter streams, compared on GPU time |

## G. Short answers

1. **Node types & property mutations:** both Effect A and Effect B use `GPUParticles2D`. When configuring them, Godot 4 property name mutations must be respected—specifically using `initial_velocity_min` and `initial_velocity_max` instead of outdated Godot 3 names, which fail silently. `GPUParticles2D` in Godot 4 contains all features required by this brief—including `amount_ratio`, custom scale/color curves, `lifetime_randomness`, `visibility_rect`, and `restart()`. Features that 2D particle nodes lack compared to 3D (such as 3D particle colliders and vector attractors) are not required or used by either effect in this brief.
2. **Local coordinates (`local_coords`):** setting `local_coords = false` on Effect A anchors impact bursts in world space at position `p` so they don't drift if fighters move; setting `local_coords = true` on Effect B ensures steam puffs inherit the `key_sprite`'s motion trail.
3. **Peak burst concurrency:** peak concurrency for Effect A is capped at n = 4 bursts (96 particles) to accommodate overlapping melee hits and in-flight corks within the 0.25s lifetime window.
4. **Price measurement & headless limits:** a headless run reports strictly CPU time because the dummy renderer skips the GPU particle simulation pass entirely, meaning CPU metrics omit the GPU rendering workload. With Vsync enabled, FPS reads identically (pinned to the monitor's refresh rate, e.g., 60 Hz) whether the effect is toggled off or on, proving that frame rate alone cannot measure GPU overhead and requiring direct viewport profiler timestamps instead.
5. **Lifecycle rules (pause, hidden, load):**
   - Pause: inherits `PROCESS_MODE_ALWAYS` from Main, keeping simulation active during `main.paused`.
   - Hidden: automatically hidden when parent `key_sprite` hides on fighter KO (`fighter.gd:274`).
   - Scene load: initializes at wind 100 (`amount_ratio = 0`), ensuring zero particles spawn on frame 1.
6. **Setting categorization:**
   - Emission: `amount`, `amount_ratio`, `emission_shape`, `one_shot`, `preprocess`, `lifetime`, `explosiveness`.
   - Process (`ParticleProcessMaterial`): `initial_velocity_min`/`max`, `gravity`, `damping_min`/`max`, `spread`, `angle_min`/`max`, `scale_min`/`max`, `lifetime_randomness`, color ramp, and scale curve.
   - Draw: `texture`, `visibility_rect`, `z_index`, and blend mode.

## A6 revisions

- **2026-11-08:** the cork's `struck` handler is at `main.gd:199`, not 200 (line 200 is `corks.append(c)`). Applies to A.1 and A-R4; no rule or value changes.
- 2026-11-08: A.3a Shards `color_ramp` updated with a mid-point keyframe at `0.7: Color(0.25, 0.25, 0.28, 1.0)`, keeping dark charcoal shards fully opaque through 70% of their lifetime before fading out. This resolves castle background contrast issues (TUNING.md revision 1; verdict: keep). Blocked variant remains unchanged.
- 2026-11-08: F2 particle leak did not reproduce under `main.gd` setup (verified by state test M3); existing state test (M4) continues to catch particle leaks when triggered.
- 2026-11-08: D.3 rewind strip for Effect B tuning: `godot/previews/steam_rewind_preview.tscn`, wind 4 at frame 10, rewind held from frame 30; frames 28, 31, 34, 38, 46, 53, 60, 72; `--quit-after 100`. Reason: the in-game steam cut out on rewind, and D.2 never rewinds.
- 2026-11-08: B.3 parent/flip configuration updated: steam now sits on a `SteamMount` node that tracks the key's position, facing, and visibility, but explicitly bypasses its rewind spin-squash. Reason: direct parenting caused the steam plume to prematurely truncate/cut out on rewind (TUNING Effect B rev 1; verdict: keep). No scene values changed.
