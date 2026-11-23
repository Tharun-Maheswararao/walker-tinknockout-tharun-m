# TYPECHECK.md — GATE T

Reel: `claude-liam-walker-tinknockout-tharun-m-a7-animation`  |  Checked: 2026-11-22T21:46  |  Overall: PASS  |  Beats checked: 28  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

> **§8.10 REDUNDANCY (advisory — does not block cut):**
> Narration should DISCUSS on-screen text, not recite it.
> Exception: LITERAL beats (viewer types/copies/runs the text) are exempt.

> - §8.10 [B25] narration recites the card (0.85) — discuss it, don't read it

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B01 | ? | light | min-size §8.1: min text-run height 97px >= floor 41px | PASS | — |
| B02 | ? | — | no video | SKIP | — |
| B03 | ? | light | no-wordy-card §8.5: 2 element(s), 8 words — within budget. Detail: 2 output lines (8 words… | PASS | — |
| B04 | ? | — | no video | SKIP | — |
| B05 | ? | — | no video | SKIP | — |
| B06 | ? | — | no video | SKIP | — |
| B07 | ? | light | no-wordy-card §8.5: 2 element(s), 8 words — within budget. Detail: 2 output lines (8 words… | PASS | — |
| B08 | ? | — | no video | SKIP | — |
| B09 | ? | — | no video | SKIP | — |
| B10 | ? | — | no video | SKIP | — |
| B11 | ? | — | no video | SKIP | — |
| B12 | ? | — | no video | SKIP | — |
| B13 | ? | — | no video | SKIP | — |
| B14 | ? | — | no video | SKIP | — |
| B15 | ? | — | no video | SKIP | — |
| B16 | ? | — | no video | SKIP | — |
| B17 | ? | — | no video | SKIP | — |
| B18 | ? | — | no video | SKIP | — |
| B19 | ? | — | no video | SKIP | — |
| B20 | ? | — | no video | SKIP | — |
| B21 | ? | — | no video | SKIP | — |
| B22 | ? | — | no video | SKIP | — |
| B23 | ? | — | no video | SKIP | — |
| B24 | ? | — | no video | SKIP | — |
| B25 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeVerdictArtifact) — §8.1 hachure/crossbar fragment… | PASS | — |
| B26 | ? | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| B27 | ? | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 2 | 0 |
| min-size §8.1 | 7 | 0 |
| overflow §8.2 | 7 | 0 |
| contrast §8.3 | 7 | 0 |
| contrast-local §8.3b | 7 | 0 |
| bbox-overlap §8.6b | 7 | 0 |
| card-clip §8.13 | 7 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 1 | 1 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
