# A7 finding: the key cycle's seam glitched after the first wrap (found and fixed in Use It)

*Claude, 2026-11-22. Fix approved by Tharun the same day.*

- **How it was found:** the first headless run of `godot/previews/key_cycle_preview.tscn`, built for the Use It seam check, logged the key's frame on every tick. Every wrap after the first went **7 → 1 → 0**: frame 1 for one tick, then frame 0 for six.
- **Cause:** `Fighter._sync_clips` put the key clip at `fposmod(state_t, 1.0)` with `seek()`. After the first turn, `state_t` accumulates 1/60 per tick to 1.99999… rather than 2.0, so the clip was sought to 0.99999, the end of the loop (frame 7), and on the next tick **backwards** to 0.017. When Godot seeks a discrete value track backwards it shows the next key (frame 1, at 0.125 s). The first wrap was clean only because `state_t` happened to land on exactly 1.0 there.
- **Why the suite was green:**
  - the structure test's REWIND (B5) stopped at 1.5 turns, before the second wrap;
  - the read-back played the clip with `advance()`, which only moves forward.
- **Fix:** `_sync_clips` moves the key clip **forward** to `state_t` mod 1 s with `advance()`; it no longer seeks across the wrap. The invariant (clip position = `state_t` mod length, `CHANGE-BRIEF.md` §6) is unchanged.
- **Regression test:** `test_a7_structure.gd` B7, six turns with wind held low (SETUP):
  - **before the fix:** 57 checks, 3 failed (`structure_before_fix_60fps.log`): out of order `7>1, 1>0` at five wraps; only 1 clean wrap; a 1-tick hold;
  - **after the fix:** 57/0 at 60 and 30 (`structure_after_fix_60fps.log`);
  - **every suite after the fix:** `after-fix-all/SUMMARY.txt`, all at their counts.
- **The jab clip is not affected:** within JAB, `state_t` only increases, and hitstop and pause hold it still, so `jab_action` is never sought backwards (`test_a7_structure.gd` B1–B3 and `test_a7_edges.gd` compare the clip position with `state_t` on every tick).
