# PROMPTS.md — Tin Knockout, Taken Apart

## B00 — the opening ask (RECONSTRUCTED)

**Illustrative reconstruction, not a saved transcript.** Labelled on the card and in narration.

> Please use Walker to convert my game design document about a tin wind-up deep-sea-diver toy who boxes his
> repainted twin in an empty goldfish bowl after the toy shop closes, where every move unwinds his spring,
> into a playable Godot slice.

Card output lines (checkable against the repository):

```
■ walker-tinknockout-tharun-m  ·  Godot 4.7.2  ·  64c037a
  PLAYER   Bolt  ·  OPPONENT  Rivet (pattern, not AI)
  SPRING   every move costs wind  ·  hold S to rewind
  ASSETS   SDXL-Turbo art · AudioLDM 2 SFX · MusicGen waltz
  RECONSTRUCTED PROMPT — illustrative, not a transcript
```

## B03 — the asset prompt shown (real, from ASSET-LOG.md)

> throwing a straight punch forward, 2d cartoon game sprite of a tin wind-up toy deep sea diver, polished brass
> helmet with two antennae, red enamel tin suit with rivets, yellow mitten gloves, steel boots, bold black
> outline, cel shaded, plain light grey background

SDXL-Turbo img2img, strength 0.6, 8 steps, seed 43, 512×512, cfg 0, init `raw/inits-ref/jab.png`.

## B14 — Your Turn (read aloud)

> Please use Walker to change rivet_brain.gd so a cornered Rivet blocks instead of rewinding when Bolt is
> closer than 170 px, add one test for it, and state your prediction before you run it.

Why this one: `rivet_brain.gd` lines 28–34 make a retreating Rivet rewind either when Bolt is 170 px or more
away **or** when Rivet is pinned at the arena edge, even with Bolt in range — that second branch is what lets a
cornered Rivet be hit while rewinding (a knockdown, `fighter.gd` 228–230). The change is bounded (one branch,
one test) and the prediction is checkable with the existing scripted-test style: fewer Rivet knockdowns while
rewinding, longer rounds. It is a step toward the full game's real opponent AI; weapon pickups from the toy box
are the other named next step.

## Narration

All narration is in `beat_sheet.json` (`narration_text`), voiced locally by Kokoro `am_onyx`. B10 has no
narration by design.
