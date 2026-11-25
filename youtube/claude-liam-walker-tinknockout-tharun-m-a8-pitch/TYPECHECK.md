# TYPECHECK.md — GATE T

Reel: `claude-liam-walker-tinknockout-tharun-m-a8-pitch`  |  Checked: 2026-11-24T17:10  |  Overall: PASS  |  Beats checked: 16  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | ? | — | no video | SKIP | — |
| B01 | ? | — | no video | SKIP | — |
| B02 | ? | light | no-wordy-card §8.5: 2 element(s), 12 words — within budget. Detail: 2 output lines (12 wor… | PASS | — |
| B03 | ? | — | no video | SKIP | — |
| B04 | ? | — | no video | SKIP | — |
| B05 | ? | — | no video | SKIP | — |
| B06 | ? | — | no video | SKIP | — |
| B07 | ? | — | no video | SKIP | — |
| B08 | ? | — | no video | SKIP | — |
| B09 | ? | — | no video | SKIP | — |
| B10 | ? | — | no video | SKIP | — |
| B11 | ? | light | no-wordy-card §8.5: 2 element(s), 12 words — within budget. Detail: 2 output lines (12 wor… | PASS | — |
| B12 | ? | — | no video | SKIP | — |
| B13 | ? | — | no video | SKIP | — |
| B14 | ? | — | no video | SKIP | — |
| B15 | ? | — | no video | SKIP | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 2 | 0 |
| min-size §8.1 | 2 | 0 |
| overflow §8.2 | 2 | 0 |
| contrast §8.3 | 2 | 0 |
| contrast-local §8.3b | 2 | 0 |
| bbox-overlap §8.6b | 2 | 0 |
| card-clip §8.13 | 2 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
