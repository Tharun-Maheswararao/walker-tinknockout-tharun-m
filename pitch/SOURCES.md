# SOURCES — final project pitch (A8)

## What the pitch uses

- **The game itself**, at tag `a7` (`a0c95cc`) and earlier tags. Every existing piece is listed with its tag in `EXISTS-FACTS.md`.
- **Game art and audio:** all generated in A2 with local models, under their own licences:
  - art: SDXL-Turbo, Stability AI Non-Commercial Research Community License;
  - sound effects: AudioLDM 2, CC BY-NC-SA 4.0;
  - music: MusicGen-small, CC BY-NC 4.0.

  Model names, revisions and every prompt are in the repository's `SOURCES.md` and `ASSET-LOG.md`. **No new art, audio or model** was used for the pitch.
- **The A7 key sheets** are derivatives of the A2 key art (`godot/assets/props/ATTRIBUTION.md`).
- **No third-party characters, brands, music or footage.** The comparable games, Street Fighter 6 and Tekken 8, are named only in narration and text, as games Tharun has played. No footage or art from them appears.

## Tools

- Godot 4.7.2.stable (Forward+, Vulkan/MoltenVK), macOS 15.6, Apple M4. Movie Maker for the gameplay captures.
- The course's Brutalist toolkit (`_brutalist/`), free local pipeline: Kokoro TTS narration, Remotion, ffmpeg, and the toolkit's own quality gates.
- Claude Code (Claude Opus 5.5) in the interactive desktop session. `claude -p` was spend-limited until 2026-12-01.

## What Tharun decided and did

- Chose the project direction, option (c): a gameplay system built on Tin Knockout, not a new game.
- Chose the comparables, from games he has played: Street Fighter 6 and Tekken 8.
- Chose the target role (gameplay programmer), the export target (macOS desktop) and the honest framing of "why" (a mix of new and existing skills).
- Reviewed the brief and the film, and is responsible for both (`FRICTIONAL.md`).

## What Claude contributed

- `EXISTS-FACTS.md`: the facts and their sources.
- `PROJECT-BRIEF.md`: the draft of the seven answers, from Tharun's choices and the facts file.
- This folder's `README.md`, `SOURCES.md` and the factual entries in `FRICTIONAL.md` (Tharun's own lines are marked).
- **The film:** script, beat sheet, captures and render, built by a separate Claude Code session with the Brutalist workflow. Its records are in `youtube/claude-liam-walker-tinknockout-tharun-m-a8-pitch/`, and its prompts are in `BUILD-PROMPT.md`.
- **The game work the pitch shows** (A2–A7) has its own who-did-what in the repository's `SOURCES.md`.
