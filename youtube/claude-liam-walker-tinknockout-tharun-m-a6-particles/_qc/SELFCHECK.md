# SELFCHECK.md — GATE T functions on the STILL composites (real images masked)

FAILs: 0

| beat | t | masks | check | status | detail |
|---|---|---|---|---|---|
| B02 | 0.20 | 4 | min-size | PASS | min text-run height 45px >= floor 41px |
| B02 | 0.20 | 4 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.20 | 4 | contrast | PASS | contrast 8.16:1 >= 4.5:1 |
| B02 | 0.20 | 4 | contrast-local | PASS | per-blob contrast min 9.62:1 >= 3.0:1 (2 blobs) |
| B02 | 0.20 | 4 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B02 | 0.50 | 4 | min-size | PASS | min text-run height 45px >= floor 41px |
| B02 | 0.50 | 4 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.50 | 4 | contrast | PASS | contrast 8.16:1 >= 4.5:1 |
| B02 | 0.50 | 4 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (2 blobs) |
| B02 | 0.50 | 4 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B02 | 0.97 | 4 | min-size | PASS | min text-run height 45px >= floor 41px |
| B02 | 0.97 | 4 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.97 | 4 | contrast | PASS | contrast 8.16:1 >= 4.5:1 |
| B02 | 0.97 | 4 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (2 blobs) |
| B02 | 0.97 | 4 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B03 | 0.20 | 3 | min-size | PASS | min text-run height 46px >= floor 41px |
| B03 | 0.20 | 3 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.20 | 3 | contrast | PASS | contrast 12.79:1 >= 4.5:1 |
| B03 | 0.20 | 3 | contrast-local | PASS | per-blob contrast min 10.22:1 >= 3.0:1 (5 blobs) |
| B03 | 0.20 | 3 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(2544,470)–(3648,888) h=418px (1.8×med) |
| B03 | 0.50 | 3 | min-size | PASS | min text-run height 46px >= floor 41px |
| B03 | 0.50 | 3 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.50 | 3 | contrast | PASS | contrast 11.55:1 >= 4.5:1 |
| B03 | 0.50 | 3 | contrast-local | PASS | per-blob contrast min 10.19:1 >= 3.0:1 (5 blobs) |
| B03 | 0.50 | 3 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(2544,470)–(3648,888) h=418px (1.8×med) |
| B03 | 0.97 | 3 | min-size | PASS | min text-run height 46px >= floor 41px |
| B03 | 0.97 | 3 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.97 | 3 | contrast | PASS | contrast 11.07:1 >= 4.5:1 |
| B03 | 0.97 | 3 | contrast-local | PASS | per-blob contrast min 10.19:1 >= 3.0:1 (5 blobs) |
| B03 | 0.97 | 3 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(2544,470)–(3648,888) h=418px (1.8×med) |
| B04 | 0.20 | 0 | min-size | PASS | min text-run height 44px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.20 | 0 | contrast | PASS | contrast 9.99:1 >= 4.5:1 |
| B04 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.50 | 0 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.50 | 0 | contrast | PASS | contrast 9.10:1 >= 4.5:1 |
| B04 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.97 | 0 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.97 | 0 | contrast | PASS | contrast 9.36:1 >= 4.5:1 |
| B04 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.20 | 6 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.20 | 6 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.20 | 6 | contrast | PASS | contrast 7.68:1 >= 4.5:1 |
| B06 | 0.20 | 6 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.20 | 6 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.50 | 6 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.50 | 6 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.50 | 6 | contrast | PASS | contrast 8.57:1 >= 4.5:1 |
| B06 | 0.50 | 6 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.50 | 6 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.97 | 6 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.97 | 6 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.97 | 6 | contrast | PASS | contrast 8.59:1 >= 4.5:1 |
| B06 | 0.97 | 6 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.97 | 6 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.20 | 0 | min-size | PASS | min text-run height 383px >= floor 41px |
| B07 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.20 | 0 | contrast | PASS | contrast 11.63:1 >= 4.5:1 |
| B07 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 10.61:1 >= 3.0:1 (2 blobs) |
| B07 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B07 | 0.50 | 0 | min-size | PASS | min text-run height 383px >= floor 41px |
| B07 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.50 | 0 | contrast | PASS | contrast 11.54:1 >= 4.5:1 |
| B07 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 10.54:1 >= 3.0:1 (2 blobs) |
| B07 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B07 | 0.97 | 0 | min-size | PASS | min text-run height 383px >= floor 41px |
| B07 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.97 | 0 | contrast | PASS | contrast 11.54:1 >= 4.5:1 |
| B07 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 10.61:1 >= 3.0:1 (2 blobs) |
| B07 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B08 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.20 | 1 | contrast | PASS | contrast 7.91:1 >= 4.5:1 |
| B08 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.50 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.50 | 1 | contrast | PASS | contrast 7.91:1 >= 4.5:1 |
| B08 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.97 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.97 | 1 | contrast | PASS | contrast 8.78:1 >= 4.5:1 |
| B08 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.20 | 0 | contrast | PASS | contrast 12.96:1 >= 4.5:1 |
| B09 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.50 | 0 | contrast | PASS | contrast 13.47:1 >= 4.5:1 |
| B09 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.97 | 0 | contrast | PASS | contrast 13.47:1 >= 4.5:1 |
| B09 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.20 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.20 | 2 | contrast | PASS | contrast 7.10:1 >= 4.5:1 |
| B10 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.50 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.50 | 2 | contrast | PASS | contrast 7.04:1 >= 4.5:1 |
| B10 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.97 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.97 | 2 | contrast | PASS | contrast 7.04:1 >= 4.5:1 |
| B10 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.20 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B11 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B11 | 0.20 | 0 | contrast | PASS | contrast 10.06:1 >= 4.5:1 |
| B11 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B11 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.50 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B11 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B11 | 0.50 | 0 | contrast | PASS | contrast 9.35:1 >= 4.5:1 |
| B11 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B11 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B11 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B11 | 0.97 | 0 | contrast | PASS | contrast 9.62:1 >= 4.5:1 |
| B11 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B11 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.20 | 0 | min-size | PASS | min text-run height 389px >= floor 41px |
| B12 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B12 | 0.20 | 0 | contrast | PASS | contrast 13.20:1 >= 4.5:1 |
| B12 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 13.57:1 >= 3.0:1 (2 blobs) |
| B12 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B12 | 0.50 | 0 | min-size | PASS | min text-run height 389px >= floor 41px |
| B12 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B12 | 0.50 | 0 | contrast | PASS | contrast 13.18:1 >= 4.5:1 |
| B12 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 10.58:1 >= 3.0:1 (2 blobs) |
| B12 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B12 | 0.97 | 0 | min-size | PASS | min text-run height 389px >= floor 41px |
| B12 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B12 | 0.97 | 0 | contrast | PASS | contrast 12.80:1 >= 4.5:1 |
| B12 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.15:1 >= 3.0:1 (2 blobs) |
| B12 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B13 | 0.20 | 5 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.20 | 5 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.20 | 5 | contrast | PASS | contrast 7.80:1 >= 4.5:1 |
| B13 | 0.20 | 5 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.20 | 5 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.50 | 5 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.50 | 5 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.50 | 5 | contrast | PASS | contrast 8.07:1 >= 4.5:1 |
| B13 | 0.50 | 5 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.50 | 5 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.97 | 5 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.97 | 5 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.97 | 5 | contrast | PASS | contrast 8.44:1 >= 4.5:1 |
| B13 | 0.97 | 5 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.97 | 5 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.20 | 3 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.20 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.20 | 3 | contrast | PASS | contrast 7.84:1 >= 4.5:1 |
| B14 | 0.20 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.20 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.50 | 3 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.50 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.50 | 3 | contrast | PASS | contrast 9.69:1 >= 4.5:1 |
| B14 | 0.50 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.50 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.97 | 3 | min-size | PASS | min text-run height 542px >= floor 41px |
| B14 | 0.97 | 3 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B14 | 0.97 | 3 | contrast | PASS | contrast 9.95:1 >= 4.5:1 |
| B14 | 0.97 | 3 | contrast-local | PASS | per-blob contrast min 10.13:1 >= 3.0:1 (1 blobs) |
| B14 | 0.97 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.20 | 1 | contrast | PASS | contrast 9.05:1 >= 4.5:1 |
| B15 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.50 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.50 | 1 | contrast | PASS | contrast 8.15:1 >= 4.5:1 |
| B15 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.97 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.97 | 1 | contrast | PASS | contrast 8.86:1 >= 4.5:1 |
| B15 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B16 | 0.20 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B16 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B16 | 0.20 | 2 | contrast | PASS | contrast 7.10:1 >= 4.5:1 |
| B16 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B16 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B16 | 0.50 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B16 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B16 | 0.50 | 2 | contrast | PASS | contrast 7.05:1 >= 4.5:1 |
| B16 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B16 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B16 | 0.97 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B16 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B16 | 0.97 | 2 | contrast | PASS | contrast 7.10:1 >= 4.5:1 |
| B16 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B16 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B17 | 0.20 | 0 | min-size | PASS | min text-run height 356px >= floor 41px |
| B17 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B17 | 0.20 | 0 | contrast | PASS | contrast 13.47:1 >= 4.5:1 |
| B17 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 13.65:1 >= 3.0:1 (2 blobs) |
| B17 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B17 | 0.50 | 0 | min-size | PASS | min text-run height 356px >= floor 41px |
| B17 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B17 | 0.50 | 0 | contrast | PASS | contrast 11.88:1 >= 4.5:1 |
| B17 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 10.69:1 >= 3.0:1 (2 blobs) |
| B17 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B17 | 0.97 | 0 | min-size | PASS | min text-run height 356px >= floor 41px |
| B17 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B17 | 0.97 | 0 | contrast | PASS | contrast 10.62:1 >= 4.5:1 |
| B17 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 10.56:1 >= 3.0:1 (2 blobs) |
| B17 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B18 | 0.20 | 0 | min-size | PASS | min text-run height 780px >= floor 41px |
| B18 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B18 | 0.20 | 0 | contrast | PASS | contrast 14.03:1 >= 4.5:1 |
| B18 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B18 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B18 | 0.50 | 0 | min-size | PASS | min text-run height 780px >= floor 41px |
| B18 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B18 | 0.50 | 0 | contrast | PASS | contrast 13.90:1 >= 4.5:1 |
| B18 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B18 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B18 | 0.97 | 0 | min-size | PASS | min text-run height 780px >= floor 41px |
| B18 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B18 | 0.97 | 0 | contrast | PASS | contrast 13.66:1 >= 4.5:1 |
| B18 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B18 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B19 | 0.20 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B19 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B19 | 0.20 | 1 | contrast | PASS | contrast 11.68:1 >= 4.5:1 |
| B19 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (1 blobs) |
| B19 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B19 | 0.50 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B19 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B19 | 0.50 | 1 | contrast | PASS | contrast 11.81:1 >= 4.5:1 |
| B19 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (1 blobs) |
| B19 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B19 | 0.97 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B19 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B19 | 0.97 | 1 | contrast | PASS | contrast 11.53:1 >= 4.5:1 |
| B19 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (1 blobs) |
| B19 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B20 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B20 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B20 | 0.20 | 0 | contrast | PASS | contrast 10.20:1 >= 4.5:1 |
| B20 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B20 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B20 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B20 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B20 | 0.50 | 0 | contrast | PASS | contrast 9.22:1 >= 4.5:1 |
| B20 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B20 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B20 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B20 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B20 | 0.97 | 0 | contrast | PASS | contrast 10.12:1 >= 4.5:1 |
| B20 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B20 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B21 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B21 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B21 | 0.20 | 0 | contrast | PASS | contrast 10.26:1 >= 4.5:1 |
| B21 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B21 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B21 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B21 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B21 | 0.50 | 0 | contrast | PASS | contrast 10.26:1 >= 4.5:1 |
| B21 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B21 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B21 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B21 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B21 | 0.97 | 0 | contrast | PASS | contrast 9.58:1 >= 4.5:1 |
| B21 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B21 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
