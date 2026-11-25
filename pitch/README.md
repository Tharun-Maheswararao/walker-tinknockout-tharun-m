# Final project pitch — Tin Knockout Fighter Kit

- **Name:** Tharun Maheswararao (CSYE 7270, Fall 2026)
- **Working title:** Tin Knockout Fighter Kit: a frame-exact fighter controller and animation state machine for Godot 4
- **Target role:** gameplay programmer
- **Runtime:**
  - **Game:** Godot 4.7.2.stable, GDScript, Forward+ on Vulkan (MoltenVK), macOS 15.6 on an Apple M4. Export target: macOS desktop (no export exists yet; `pitch/EXISTS-FACTS.md` §4).
  - **Film:** 3:41 (221.6 s), 4K 3840×2160, 30 fps.
- **Film:** [claude-liam-walker-tinknockout-tharun-m-a8-pitch.mp4](https://drive.google.com/file/d/1mN8WBEmDE0O2L-2lBtXl5eUDFAqixRTb/view?usp=sharing) (Google Drive) · SHA-256 `190ed4b2491eb0d0f70284ff7fb30a94624c87ef4dbdc0fb754a2fa9fc072cdc` · gameplay footage from tag `a7` (`a0c95cc`), labelled scripted input; constructed pictures labelled as proposals. The MP4 is not in GitHub.

## What is here

| File | What it is |
|---|---|
| `PROJECT-BRIEF.md` | the seven answers, with the exists-today and will-exist lists |
| `EXISTS-FACTS.md` | every existing piece with the tag or commit where it can be seen, the measurements and their limits, and what does not exist |
| `beat_sheet.json` | the film's narration and visual plan |
| `BUILD-PROMPT.md` | the prompts and commands that rebuild the film |
| `SOURCES.md` | what was used, made and contributed, and the licences |
| `FRICTIONAL.md` | dated entries as the pitch was made |
| `gate-reports/` | the Brutalist toolkit's quality-gate reports |

## Rebuild the film

The film was built with the course's Brutalist toolkit (free local pipeline: Kokoro narration, Remotion, ffmpeg; no paid generation, no API keys). `BUILD-PROMPT.md` has the exact prompts and commands, and the film's full working folder (tools, evidence ledger, QC records) is `youtube/claude-liam-walker-tinknockout-tharun-m-a8-pitch/`. The rendered MP4 is not in GitHub; it is linked above.

## Run what exists

From the repository root, after `godot --headless --path godot --import`:
```bash
godot --path godot
```
```bash
./scripts/run-test.sh test_a7_edges.gd 60
```
The first opens the game (Enter, then J to jab). The second prints "70 checks, 0 failed" at tag `a7`.
