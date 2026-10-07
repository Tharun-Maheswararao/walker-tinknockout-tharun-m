# FACTCHECK.md — Tin Knockout, Taken Apart

Every claim spoken or shown traces to one of: the game source at revision `64c037a` (the `godot/` folder is
unchanged at HEAD `5b3fa9f`; `git diff --stat 64c037a -- godot` is empty), the repo documents (CONCEPT.md,
STORYBOARD.md, CHARACTER-SHEET.md, CHANGE-BRIEF.md, ASSET-LOG.md, SOURCES.md, TEST-REPORT.md), committed
evidence under `evidence/`, the capture input log `evidence/film/fight-inputs.jsonl`, or a test run made for
this film on an isolated copy (output reproduced in `evidence/B12-test-output.png`).

| Beat | Claim | Source |
|---|---|---|
| B00 | Prompt on screen is an illustrative reconstruction | Stated on card and in narration; no transcript claimed |
| B00 | Bolt vs Rivet in a goldfish bowl after the shop closes | CONCEPT.md "The game in two sentences" |
| B00 | Rivet is a pattern, not AI | `fighter/rivet_brain.gd` header: "pattern-driven controller (not real AI)" |
| B01 | The fight drives the sounds, not the reverse | `fighter.gd` lines 5–8 (never plays audio); `audio/sfx.gd` lines 1–3; test "muted run == unmuted run" |
| B02 | Every punch, cutlass swing, pop-gun shot and walking unwinds the spring | `fighter.gd` ATTACKS cost 12/22/30 (42–44); `WALK_DRAIN` 3.0/s (29, 175) |
| B02 | One click per quarter turn = 10 wind; rewinding locks you in place | `fighter.gd` 31, 208–213; REWIND state has no movement (`_rewind` only cranks) |
| B02 | At 0 the toy stalls (EMPTY); a hit while rewinding or empty is a knockdown | `fighter.gd` 176–177, 200, 228–230 (`KNOCKDOWN_TIME`) |
| B02 | Four pillars | CONCEPT.md "Design pillars" |
| B02 | Frame is real engine output | `capture/fight-4k.mp4` at 3.0 s (transcode of `film/capture/fight-4k.avi`) |
| B03 | Spec P04 jab drawn by Claude in code; storyboard panel 3 | `design/character/pose-targets.png` caption "Claude-drawn spec, NOT generated art"; `design/storyboard/03-core-action.png` |
| B03 | Prompt text, SDXL-Turbo img2img, strength 0.6, 8 steps, seed 43, 512², cfg 0 | ASSET-LOG.md row CHAR-JAB v2-st0.6 (accepted s43) |
| B03 | Raw output | `raw/CHAR-JAB/CHAR-JAB_v2-st0.6_s43.png` (sha256 7e284c8b…) |
| B03 | First pose batch drifted (F1), rejected | ASSET-LOG.md CHAR-JAB v1 "F1 drift; jab pose ignored"; `design/rejected/CHAR-JAB.jpg` |
| B03 | Reference picked by Tharun from four finalists | `design/rejected/CHAR-REF-finalists.jpg`; task brief (human chose s40) |
| B03 | Edits: rembg, two painted eyes, 336 px tall, feet (240,435), Rivet recolour | `tools/edit/process_sprites.py`; `fighter.gd` 260–261 (ART_SCALE note "Bolt = 336 px", FEET) |
| B04 | Line 72 creates the sprite; 73 sets `centered = false`; 267 `offset = -FEET` | `fighter.gd` 72, 73, 267 (excerpt verbatim, hash-checked) |
| B04 | 480×450 canvas, feet (240,435) | `fighter.gd` 261 comment and value |
| B05 | Before: both toys drawn ~80 px up-left of their hurtboxes; keys stay | `evidence/screens/before-fix/03b-jab-hit-boxes-sprite-offset-bug.png` (visible) |
| B05 | Both shots posed; F1 overlay; jab hitbox not active in these frames | `tools/shots.gd` header (POSED); the red box is absent in both images, so the narration names only the green hurtboxes |
| B06 | 360°/s crank, +10 per 90°, `rewind_tick` per click, stops when full | `fighter.gd` 30–31, 206–213 |
| B07 | Bolt holds S, locked in place, Rivet's hits land; both rewind side by side | fight-4k frames 10.5–23.5 s; input log `rewind` press/release at 12.117–18.117 s; "rewinding" tags visible |
| B08 | sfx.gd line-by-line mapping; gameplay never calls this node | `audio/sfx.gd` 1–4, 30–36 |
| B08 notes | Music pitch 0.85 below 25 %, low-pass on pause, stops on KO | `audio/music.gd` 9, 34–50; `main.gd` 15, 75–77, 117, 141 |
| B09 | Jab exchange, sparks/hitstop, pop-gun shot then EMPTY | fight-4k frames 2–8 s; inputs `pop` at 6.2 s; "EMPTY!" tag visible ~7.5 s; `HITSTOP` 0.07 s (`fighter.gd` 37) |
| B10 | Game audio, no narration, scripted input | `media/B10.mp4` audio = Movie Maker PCM mix of the game (AAC 192k); beat has no `narration_text` |
| B10 | sfx log: bell 2 · jab 13 · cutlass 3 · pop 1 · rewind 26 · empty 1 · Rivet wins | `evidence/film/fight-inputs.jsonl` summary line |
| B11 | Same scripted fight twice, unmuted/muted, must be identical | `tests/test_slice.gd` 190–212 |
| B12 | 25 checks, 0 failed; end states equal | fresh run 2026-10-06 on isolated `git archive 64c037a godot` copy |
| B12 | First run 8 failures; setup order; 1.5 s pop-gun cooldown; no expected value changed | `evidence/tests/run-01-setup-bug.txt` header; `rivet_brain.gd` `pop_cd := 1.5` |
| B12 | Seam check PASS (jump 0.0057 < p99 0.1176; +0.77 dB) | `tools/edit/check_seam.py` run 2026-10-06 |
| B13 | Sounds picked by signal analysis because Tharun asked; Claude cannot hear | TEST-REPORT.md §"limitations" item 1; `evidence/sfx-scores*.txt` |
| B13 | Background seen from outside the bowl though concept says inside | CONCEPT.md ("at the bottom of an empty goldfish bowl") vs `assets/env/bowl.png` (bowl drawn from outside) |
| B13 | Eyes hand-painted on every pose; win pose different seed | ASSET-LOG.md / CHARACTER-SHEET.md revisions |
| B13 | 4K take differs from headless dry run (physics stepping under --fixed-fps) | CAPTURE.md here; task brief |
| B13 | Tharun's own playtest (2026-10-06), sound on and muted, is recorded in TEST-REPORT.md: music fine alone, muted slice still readable, game and characters "very simple", mix "full of metal sounds" traced to the dense tin SFX (rewind clicks, clangs), not the music | Facts relayed by the coordinating session from Tharun's playtest record (TEST-REPORT.md); no further quotation used. No gameplay in this film is that playtest — all footage is scripted input |
| B14 | Tharun's next step: quieter rewind click / lower SFX mix, richer character art | same playtest record |
| B13 | Models and licences | repo SOURCES.md model table |
| B14 | Bounded change targets real code | `rivet_brain.gd` 28–34: retreating Rivet rewinds when `dist >= 170` or when cornered at the arena edge |
| B14 | Credits | task brief / repo SOURCES.md and CHANGE-BRIEF.md; Claude's SFX picks stated as signal analysis |
| B14 | Revision 64c037a | `git log` |
| B15 | Exact title, spoken, no game audio | OUTRO-LOCK.md |

## Corrections made while building

* B05 first draft said "red is the jab's hitbox". Looking at the actual screenshots, no red box is drawn in
  either frame (the jab's active window was not on that frame). Narration and on-image legend were changed to
  name only the green hurtboxes, and B05 was re-voiced.
* An early script said the human playtest was not part of the film because TEST-REPORT.md §8 was still PENDING. During the build the coordinating session reported that Tharun's playtest had happened and relayed its findings; B13 and B14 were rewritten, re-voiced and re-rendered to state them.
