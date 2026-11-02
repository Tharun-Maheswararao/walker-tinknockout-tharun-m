# SELFCHECK.md — GATE T functions on the STILL composites (real images masked)

FAILs: 0

| beat | t | masks | check | status | detail |
|---|---|---|---|---|---|
| B02 | 0.20 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B02 | 0.20 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.20 | 2 | contrast | PASS | contrast 8.04:1 >= 4.5:1 |
| B02 | 0.20 | 2 | contrast-local | PASS | per-blob contrast min 9.95:1 >= 3.0:1 (1 blobs) |
| B02 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B02 | 0.50 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B02 | 0.50 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.50 | 2 | contrast | PASS | contrast 8.04:1 >= 4.5:1 |
| B02 | 0.50 | 2 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B02 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B02 | 0.97 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B02 | 0.97 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.97 | 2 | contrast | PASS | contrast 7.77:1 >= 4.5:1 |
| B02 | 0.97 | 2 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B02 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.20 | 4 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.20 | 4 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.20 | 4 | contrast | PASS | contrast 9.01:1 >= 4.5:1 |
| B04 | 0.20 | 4 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.20 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.50 | 4 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.50 | 4 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.50 | 4 | contrast | PASS | contrast 8.61:1 >= 4.5:1 |
| B04 | 0.50 | 4 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.50 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.97 | 4 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.97 | 4 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.97 | 4 | contrast | PASS | contrast 8.61:1 >= 4.5:1 |
| B04 | 0.97 | 4 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.97 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.20 | 0 | contrast | PASS | contrast 14.18:1 >= 4.5:1 |
| B05 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.50 | 0 | contrast | PASS | contrast 13.81:1 >= 4.5:1 |
| B05 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.97 | 0 | contrast | PASS | contrast 13.79:1 >= 4.5:1 |
| B05 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.20 | 1 | contrast | PASS | contrast 7.28:1 >= 4.5:1 |
| B06 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.50 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.50 | 1 | contrast | PASS | contrast 7.27:1 >= 4.5:1 |
| B06 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.97 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.97 | 1 | contrast | PASS | contrast 7.21:1 >= 4.5:1 |
| B06 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B07 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.20 | 0 | contrast | PASS | contrast 13.87:1 >= 4.5:1 |
| B07 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (3 blobs) |
| B07 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B07 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px |
| B07 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.50 | 0 | contrast | PASS | contrast 11.29:1 >= 4.5:1 |
| B07 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (3 blobs) |
| B07 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B07 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px |
| B07 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.97 | 0 | contrast | PASS | contrast 13.16:1 >= 4.5:1 |
| B07 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (3 blobs) |
| B07 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B08 | 0.20 | 3 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.20 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.20 | 3 | contrast | PASS | contrast 8.45:1 >= 4.5:1 |
| B08 | 0.20 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.20 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.50 | 3 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.50 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.50 | 3 | contrast | PASS | contrast 8.55:1 >= 4.5:1 |
| B08 | 0.50 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.50 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.97 | 3 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.97 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.97 | 3 | contrast | PASS | contrast 8.55:1 >= 4.5:1 |
| B08 | 0.97 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.97 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B09 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B09 | 0.20 | 0 | contrast | PASS | contrast 14.20:1 >= 4.5:1 |
| B09 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.97:1 >= 3.0:1 (1 blobs) |
| B09 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B09 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B09 | 0.50 | 0 | contrast | PASS | contrast 13.46:1 >= 4.5:1 |
| B09 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 10.00:1 >= 3.0:1 (1 blobs) |
| B09 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B09 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B09 | 0.97 | 0 | contrast | PASS | contrast 13.82:1 >= 4.5:1 |
| B09 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 10.00:1 >= 3.0:1 (1 blobs) |
| B09 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.20 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B10 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B10 | 0.20 | 1 | contrast | PASS | contrast 8.13:1 >= 4.5:1 |
| B10 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 9.97:1 >= 3.0:1 (1 blobs) |
| B10 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.50 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B10 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B10 | 0.50 | 1 | contrast | PASS | contrast 7.65:1 >= 4.5:1 |
| B10 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 9.97:1 >= 3.0:1 (1 blobs) |
| B10 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.97 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B10 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B10 | 0.97 | 1 | contrast | PASS | contrast 7.32:1 >= 4.5:1 |
| B10 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 9.97:1 >= 3.0:1 (1 blobs) |
| B10 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.20 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B11 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B11 | 0.20 | 1 | contrast | PASS | contrast 7.67:1 >= 4.5:1 |
| B11 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 9.13:1 >= 3.0:1 (1 blobs) |
| B11 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.50 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B11 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B11 | 0.50 | 1 | contrast | PASS | contrast 7.68:1 >= 4.5:1 |
| B11 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 9.04:1 >= 3.0:1 (1 blobs) |
| B11 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.97 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B11 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B11 | 0.97 | 1 | contrast | PASS | contrast 7.50:1 >= 4.5:1 |
| B11 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 9.04:1 >= 3.0:1 (1 blobs) |
| B11 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.20 | 0 | contrast | PASS | contrast 13.84:1 >= 4.5:1 |
| B12 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.50 | 0 | contrast | PASS | contrast 13.84:1 >= 4.5:1 |
| B12 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.97 | 0 | contrast | PASS | contrast 10.46:1 >= 4.5:1 |
| B12 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.20 | 0 | contrast | PASS | contrast 14.45:1 >= 4.5:1 |
| B13 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.50 | 0 | contrast | PASS | contrast 14.45:1 >= 4.5:1 |
| B13 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.97 | 0 | contrast | PASS | contrast 13.22:1 >= 4.5:1 |
| B13 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.20 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B14 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B14 | 0.20 | 1 | contrast | PASS | contrast 14.41:1 >= 4.5:1 |
| B14 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 9.30:1 >= 3.0:1 (1 blobs) |
| B14 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.50 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B14 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B14 | 0.50 | 1 | contrast | PASS | contrast 13.75:1 >= 4.5:1 |
| B14 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 9.30:1 >= 3.0:1 (1 blobs) |
| B14 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.97 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B14 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B14 | 0.97 | 1 | contrast | PASS | contrast 13.75:1 >= 4.5:1 |
| B14 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 9.20:1 >= 3.0:1 (1 blobs) |
| B14 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.20 | 0 | contrast | PASS | contrast 9.89:1 >= 4.5:1 |
| B15 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.50 | 0 | contrast | PASS | contrast 9.90:1 >= 4.5:1 |
| B15 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.97 | 0 | contrast | PASS | contrast 9.90:1 >= 4.5:1 |
| B15 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
