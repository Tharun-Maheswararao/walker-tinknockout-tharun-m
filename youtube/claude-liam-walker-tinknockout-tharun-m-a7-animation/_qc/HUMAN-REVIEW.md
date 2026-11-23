# HUMAN-REVIEW.md — Claude's inspection of the actual master (not Tharun's review)

Master: `exports/landscape/claude-liam-walker-tinknockout-tharun-m-a7-animation.mp4`
SHA-256 `0318373f1799c3629c910038feb023871aa5eefdf6fdf4ee6d88a873776046bd` · 717.50 s (11:57.5) · 3840×2160 · 30 fps
H.264 + AAC 48 kHz stereo · revision shown `a5978c0`. Inspected by Claude, 2026-11-22, from `_tools/review_master.py`
(frames at 15 / 50 / 92 % of every beat in `_qc/master/`, contact sheet `_qc/master-contact.png`, per-beat audio levels in
`_qc/master-review.log`). Tharun has not watched it yet.

## Probe and audio

- Full decode: no errors. Beat timeline 717.17 s + container 717.50 s.
- Every beat has narration: mean −26.6 to −27.6 dB, peaks −2.9 to −7.8 dB. No beat is silent; no clipping.
- Outro: the last 0.85 s peaks at −51.2 dB, the OUTRO-LOCK 1.0 s silent tail. No jingle, music or SFX anywhere.

## What I looked at, beat by beat

| Beats | Looked for | Seen |
|---|---|---|
| B00, B26 | composer, prompt labelled reconstructed / suggested | correct; output lines legible. The composer chip shows "Fable 5 · High": the ClaudeComposerAsk component's own default model chip, not a claim about which model did the A7 work (SOURCES.md A7: Claude Opus 5.5) |
| B01 | "display" struck and corrected to "physics" | correction lands; three lines, serif, no overflow |
| B02 | held frames labelled SCRIPTED INPUT; TEST-REPORT table cells | correct; both cards legible |
| B03, B07 | code at reading size, highlighted lines, editor-reconstruction disclosure | B03 lines 22–30 and B07 lines 346–356 all visible (B07 at codeFontSize 24 after the first render cut off line 354); highlights on 22/26/27/29 and 347/351/354 |
| B04–B06 | M1 logs verbatim; source scan; held lunge frame | legible; terminal text at the 44 px floor |
| B08 | nine consecutive ticks e+4..e+12, held ticks ringed, CLOCKS line | the impact burst (A6) visible on e+5..e+10, clip 0.0833 on each; CLOCKS line verbatim |
| B09–B13 | phase / key tables; r0 strip with ring per boundary; sheets sliced 8 × 1; frame track | correct; B12 sheets on a dark backdrop (GATE V low-contrast fix) |
| B14 | key turning, FIXTURE label, wrap readout, 0.25× replay label | correct; key cells visibly change; `repeat` counter shown where a segment loops |
| B15–B18 | revisions: reading, diff (before / after commits labelled), prediction, result, verdict | correct; Tharun's words in quote cards marked as his |
| B19 | real speed, 0.5× case 1, 0.25× case 2, SETUP disclosed | correct. The real-speed segment loops three times (labelled `repeat`) and includes the SETUP cut between cases |
| B20 | three interrupts side by side, synchronised, 0.25×; then REWIND zoom | correct: HURT on e+3, e+7, e+15 with "no clip · rig at rest 0 / 0 / 0"; REWIND shows wind and key frame, loops (labelled). The REWIND zoom is soft (a 768 × 432 crop of the 4K frame) |
| B21–B24 | counts, mutation table, mistakes, seam logs, A7-9f, human checks, credits | all verbatim; no overflow |
| B25 | verdict lines | correct |
| B27 | locked outro: exact title, @NikBearBrown, one mascot, no subline | correct |

## Gate results

- `./art godot-gamedev --check`: PASS (21 source files, 152 exclusions, 6 components, 2 exact excerpts, code-then-result-v1).
- GATE T: PASS. `_tools/selfcheck.py` (GATE T functions on the 21 composites, real images masked): 0 FAIL.
- GATE V (`final_frame_check.py`, 56 frames): 0 BLOCKER, 0 MAJOR. The first render was refused with 5 MAJOR (B06, B15,
  B17 underfill at mid-beat; B12 low contrast); fixed by showing the right-hand panels from the start, adding footers,
  and a dark sheet backdrop. Not fixed, because the gate does not sample them: some beats are sparse in their first
  seconds by design (progressive reveal), e.g. B09, B22, B23 at 15 %.

## For Tharun to check when he watches

1. **B18 "Recorded verdict: keep" (revision 2).** TUNING.md's revision-2 section has your in-game paragraph but no
   separate "Verdict: Keep" line; the film takes "Keep" from TEST-REPORT A7-8's "Verdict (Tharun)" column and
   FRICTIONAL ("my verdict: keep"). Confirm that is your verdict.
2. **B19 / B20 are scripted input, not your play.** Bolt is driven by key events; Rivet by a stand-in plan (the edge
   test's method); positions are set between cases. All labelled — check the labels read clearly to you.
3. **B23 narration** quotes the opening of your A7-9b and A7-9d checks and your FRICTIONAL "In my words" line; check
   the cut points keep your meaning.
4. **B24** says only what SOURCES.md A7 says about how the brief was drafted.
5. **The composer's "Fable 5" chip** in B00 / B26 is the toolkit component's default, inside a labelled reconstruction.
6. Pronunciation: Kokoro reads "a five nine seven eight c zero", "rotatoin", "SDXL Turbo"; listen once.

## Tharun's review (2026-11-22)

In chat, after watching the master (SHA-256 `0318373f…46bd`), verbatim: "watched the film it's all good".
Recorded as given; no change was made to the film after it.

## Upload (Tharun, 2026-11-22)

Uploaded by Tharun to Google Drive: https://drive.google.com/file/d/1gdxG-RNG4bh9KgMArhkk_oH-PP5GQH_9/view?usp=sharing
The link was given in chat; Claude did not open it, so it has not been checked that the uploaded file is the master above.
