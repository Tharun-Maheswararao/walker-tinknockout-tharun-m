# CHECKS-REPORT.md

25 beats (B00–B24), 716.9 s of measured narration (master 717.27 s). 0 slates. GATE V: 0 BLOCKER, 0 MAJOR.

Ship It checklist (task brief):
1. **Game, both effects, jobs, event and condition:** B00, B02.
2. **Emission / process / draw**, one scene line each (`impact_effect.tscn:86, 28, 37`) with its strip result; why
   the headless price is near zero: B03 (again in B19).
3. **Effect A:**
   - intent block: B04;
   - first strip r0: B05 → B06;
   - revision 1, prediction: B07;
   - revision 1, before / after and verdict: B08;
   - in play, with rapid repeats and the blocked variant: B09 → B10.
4. **Effect B:**
   - intent, including amount_ratio, the feature A doesn't use: B11;
   - scene and mapping: B12;
   - first strip: B13;
   - revision 1, prediction: B14;
   - before / after and verdict: B15;
   - in play, start / pause / stop: B16.
5. **Two annotated generated-shader lines beside the brief settings:** 258 (spread 30.0) and 302 / 315 (gravity
   (0, −180, 0)), with Tharun's line references: B17.
6. **Tests:**
   - counts (re-run) and mutations (M1, M2, M4, M5, M6 caught; M3 not): B18;
   - both prices against the budget, with the GPU price shown as PENDING: B19;
   - what no headless run shows: B01, B03, B19.
7. **Agent mistakes:** five (B20).
8. **Claude's readings Tharun overruled**, with his statement verbatim: B20.
9. **Still uncertain:** B22.
10. **One next step:** the GPU price per effect (B22).
11. **Contributions:** verbatim from SOURCES.md (B21).
12. **Texture sources:** written by code (B00, B21, B23).
13. **Revision shown:** c844ab2 (B05, B07, B09, B12, B22, B23).
14. **Bookends:** composer → writer → body → verdict → Your Turn → locked outro.
15. **Labels:** fixtures, scripted input and held frames are labelled throughout.

Code → result: B05 → B06 (checked), B07 → B08, B09 → B10, B12 → B13, B14 → B15, B17 → B18. B03 shows each line and
its result in the same beat.

`./art godot-gamedev --check`: PASS (`_qc/GAMEDEV-CHECK.txt`). GATE T: PASS (TYPECHECK.md). Composite selfcheck: 0 FAIL
(`_qc/SELFCHECK.md`). Master review: `_qc/HUMAN-REVIEW.md`.
