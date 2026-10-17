# _qc/HUMAN-REVIEW.md — review of the actual master (by eye and by measurement)

Reviewer: Claude Code (agent), not a human. `_qc/REPORT.md` is GATE V's own output and is overwritten on each run.

Master: `exports/landscape/claude-liam-walker-tinknockout-tharun-m-a3-props.mp4`
SHA-256 `007d0d984c9a34eb36d3d741db9ebbe062b661158db73b57ffa9557b87630b5e` · 568.37 s (9:28) · 3840×2160 H.264
30 fps + AAC 48 kHz stereo · receipt `….verified.json` status `ready`, hash matches the file. Game source 1d93dcb.

## Gates (final run, 2026-10-17 00:16 EDT)

| Gate | Result |
|---|---|
| `./art godot-gamedev --check` (before render and at handoff) | PASS — 10 source files, 86 exclusions (A2 files asserted byte-identical to 64c037a), 4 components, 3 exact excerpts, 3 code→result pairs |
| GATE T (`type_check.py`) | PASS, 0 FAILs (advisory §8.10: B25 0.65) |
| Masked GATE T on the 19 STILL composites (`_tools/selfcheck.py`) | 0 FAILs at t = 0.20 / 0.50 / 0.97 (`_qc/SELFCHECK.md`) |
| GATE V (`final_frame_check.py`) | PASS — 56 frames, 0 BLOCKER, 0 MAJOR; regional contrast on B18 |
| FACTCHECK / SHOTLIST / PROMPTS, approvals, slates, sound, decode | passed inside `./art final` (no approval subjects for this non-fellows reel) |

## Findings and fixes during the build

1. **B01 correction never fired.** The writer only matches single words; the phrase trigger "look right" did nothing
   (sampled frames showed the uncorrected sentence to the cut). Fixed to `look` → `measure`; the final frame reads
   "The check proves they measure right."
2. **GATE V blocked the first final** (2 MAJOR underfill on B01 at 50 %/85 %: slow typing, small text). Typing sped up
   (charMs 10) and type enlarged (108 px, spacing 2.6); a 120 px try crossed the right safe edge after the longer
   correction and was rejected. Re-run: 0 BLOCKER, 0 MAJOR. No gate was disabled or changed.
3. **GodotDevWorkbench code clipped** in B17/B19/B21 at 29–30 px (lines 40–43 of prop_room.tscn hidden). Excerpts
   narrowed / font 24–25 px (48–50 px at 4K); every narrated line is now visible.
4. **Masked self-check** first failed on terracotta card borders (#D97757 on cream read as accent text) and on the
   italic quote's x-height (38 px). Card borders changed to dark terracotta; quote enlarged to 106 px.
5. **Orbit capture** first came out 1280×720 (window override); re-captured natively at 3840×2160 (CAPTURE.md).
6. Render-provenance stamps were lost when the sheet was rebuilt; those Remotion beats were re-rendered so every
   stamp is real.

## Inspected on the master (`_qc/master-contact.png`, `_qc/frames/master/` at 15/50/92 % of every beat)

* All 28 beats in order; code at reading size (native 4K crops of B13 and B21 are crisp); every Blender code panel says
  "SOURCE VIEW · not an editor recording", every Godot one "Godot editor reconstruction" with path, lines and 1d93dcb.
* Labels: "Student's own screenshot" on 01, 02, 04, 05, 06, 07; "Blender MCP look tool, student's live session" on 03;
  "Claude-made" on the Godot renders; "REAL ENGINE … camera orbit added by a film script · not Tharun's look check" on
  B18; "RE-CREATION FOR THIS FILM" on B22; "RECONSTRUCTED PROMPT" on B00; B06 "Real, verbatim".
* Outro: exact title "Tin Knockout, Three Props in Blender.", `@NikBearBrown`, one crisp mascot, no subline.

## Audio (volumedetect per beat, `_qc/master-review.log`)

Narration on every beat: mean −26.8 to −28.3 dB, max −2.8 to −8.5 dB; no silent beat. B27 outro voice mean −26.8 dB;
last 0.85 s of the card max −51.8 dB (the silent 1.0 s tail; no jingle, no game audio). Full decode: no errors.
Claude cannot hear: pronunciation (e.g. "Merhaba", "Maheswararao", spoken hex codes) was not verified by ear.

## Caveats

* The master is 0.41 s longer than the summed beat clock (568.37 vs 567.96 s): per-beat frame rounding in the compiler.
* Composite beats are typed STILL (as in the A2 reel), so GATE T skips them; the masked self-check is the substitute.
* The ClaudeComposerAsk chrome shows a "Fable 5 · High" model chip; that is component UI, not a claim about which model built anything.
