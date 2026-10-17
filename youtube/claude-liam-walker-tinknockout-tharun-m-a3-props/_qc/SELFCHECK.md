# SELFCHECK.md — GATE T functions on the STILL composites (real images masked)

FAILs: 0

| beat | t | masks | check | status | detail |
|---|---|---|---|---|---|
| B02 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B02 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B02 | 0.20 | 1 | contrast | PASS | contrast 7.88:1 >= 4.5:1 |
| B02 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B02 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B02 | 0.50 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B02 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B02 | 0.50 | 1 | contrast | PASS | contrast 7.59:1 >= 4.5:1 |
| B02 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B02 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B02 | 0.97 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B02 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B02 | 0.97 | 1 | contrast | PASS | contrast 8.17:1 >= 4.5:1 |
| B02 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B02 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B03 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B03 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.20 | 0 | contrast | PASS | contrast 13.55:1 >= 4.5:1 |
| B03 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B03 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B03 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B03 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.50 | 0 | contrast | PASS | contrast 13.38:1 >= 4.5:1 |
| B03 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B03 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B03 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B03 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.97 | 0 | contrast | PASS | contrast 13.39:1 >= 4.5:1 |
| B03 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B03 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.20 | 2 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.20 | 2 | contrast | PASS | contrast 7.76:1 >= 4.5:1 |
| B04 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.50 | 2 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.50 | 2 | contrast | PASS | contrast 8.43:1 >= 4.5:1 |
| B04 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.97 | 2 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.97 | 2 | contrast | PASS | contrast 8.37:1 >= 4.5:1 |
| B04 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.20 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B05 | 0.20 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B05 | 0.20 | 2 | contrast | PASS | contrast 7.74:1 >= 4.5:1 |
| B05 | 0.20 | 2 | contrast-local | PASS | per-blob contrast min 9.64:1 >= 3.0:1 (2 blobs) |
| B05 | 0.20 | 2 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B05 | 0.50 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B05 | 0.50 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B05 | 0.50 | 2 | contrast | PASS | contrast 8.24:1 >= 4.5:1 |
| B05 | 0.50 | 2 | contrast-local | PASS | per-blob contrast min 9.64:1 >= 3.0:1 (2 blobs) |
| B05 | 0.50 | 2 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B05 | 0.97 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B05 | 0.97 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B05 | 0.97 | 2 | contrast | PASS | contrast 8.24:1 >= 4.5:1 |
| B05 | 0.97 | 2 | contrast-local | PASS | per-blob contrast min 9.66:1 >= 3.0:1 (2 blobs) |
| B05 | 0.97 | 2 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B06 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B06 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.20 | 0 | contrast | PASS | contrast 10.01:1 >= 4.5:1 |
| B06 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 10.27:1 >= 3.0:1 (1 blobs) |
| B06 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B06 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.50 | 0 | contrast | PASS | contrast 9.82:1 >= 4.5:1 |
| B06 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 10.27:1 >= 3.0:1 (1 blobs) |
| B06 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B06 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.97 | 0 | contrast | PASS | contrast 10.04:1 >= 4.5:1 |
| B06 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 10.27:1 >= 3.0:1 (1 blobs) |
| B06 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.20 | 0 | min-size | PASS | min text-run height 42px >= floor 41px (individual-char fallback at 2×) |
| B07 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B07 | 0.20 | 0 | contrast | PASS | contrast 13.81:1 >= 4.5:1 |
| B07 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B07 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.50 | 0 | min-size | PASS | min text-run height 42px >= floor 41px (individual-char fallback at 2×) |
| B07 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B07 | 0.50 | 0 | contrast | PASS | contrast 12.79:1 >= 4.5:1 |
| B07 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B07 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.97 | 0 | min-size | PASS | min text-run height 42px >= floor 41px (individual-char fallback at 2×) |
| B07 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B07 | 0.97 | 0 | contrast | PASS | contrast 12.79:1 >= 4.5:1 |
| B07 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B07 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px |
| B08 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B08 | 0.20 | 1 | contrast | PASS | contrast 7.84:1 >= 4.5:1 |
| B08 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 10.27:1 >= 3.0:1 (1 blobs) |
| B08 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.50 | 1 | min-size | PASS | min text-run height 46px >= floor 41px |
| B08 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B08 | 0.50 | 1 | contrast | PASS | contrast 8.16:1 >= 4.5:1 |
| B08 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 10.45:1 >= 3.0:1 (1 blobs) |
| B08 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.97 | 1 | min-size | PASS | min text-run height 44px >= floor 41px |
| B08 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B08 | 0.97 | 1 | contrast | PASS | contrast 8.92:1 >= 4.5:1 |
| B08 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 10.45:1 >= 3.0:1 (2 blobs) |
| B08 | 0.97 | 1 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B09 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.20 | 0 | contrast | PASS | contrast 13.31:1 >= 4.5:1 |
| B09 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.50 | 0 | contrast | PASS | contrast 13.32:1 >= 4.5:1 |
| B09 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.97 | 0 | contrast | PASS | contrast 13.32:1 >= 4.5:1 |
| B09 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.20 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.20 | 2 | contrast | PASS | contrast 7.98:1 >= 4.5:1 |
| B10 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.50 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.50 | 2 | contrast | PASS | contrast 8.07:1 >= 4.5:1 |
| B10 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.97 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.97 | 2 | contrast | PASS | contrast 8.57:1 >= 4.5:1 |
| B10 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B11 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B11 | 0.20 | 0 | contrast | PASS | contrast 13.49:1 >= 4.5:1 |
| B11 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.89:1 >= 3.0:1 (1 blobs) |
| B11 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B11 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B11 | 0.50 | 0 | contrast | PASS | contrast 12.63:1 >= 4.5:1 |
| B11 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.99:1 >= 3.0:1 (1 blobs) |
| B11 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B11 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B11 | 0.97 | 0 | contrast | PASS | contrast 12.76:1 >= 4.5:1 |
| B11 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.99:1 >= 3.0:1 (1 blobs) |
| B11 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.20 | 3 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.20 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.20 | 3 | contrast | PASS | contrast 7.73:1 >= 4.5:1 |
| B12 | 0.20 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.20 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.50 | 3 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.50 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.50 | 3 | contrast | PASS | contrast 8.01:1 >= 4.5:1 |
| B12 | 0.50 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.50 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.97 | 3 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.97 | 3 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.97 | 3 | contrast | PASS | contrast 8.64:1 >= 4.5:1 |
| B12 | 0.97 | 3 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.97 | 3 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.20 | 0 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.20 | 0 | contrast | PASS | contrast 13.81:1 >= 4.5:1 |
| B13 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.50 | 0 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.50 | 0 | contrast | PASS | contrast 13.11:1 >= 4.5:1 |
| B13 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.97 | 0 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.97 | 0 | contrast | PASS | contrast 13.11:1 >= 4.5:1 |
| B13 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.20 | 4 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.20 | 4 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.20 | 4 | contrast | PASS | contrast 8.08:1 >= 4.5:1 |
| B14 | 0.20 | 4 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.20 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.50 | 4 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.50 | 4 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.50 | 4 | contrast | PASS | contrast 7.95:1 >= 4.5:1 |
| B14 | 0.50 | 4 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.50 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.97 | 4 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.97 | 4 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.97 | 4 | contrast | PASS | contrast 8.24:1 >= 4.5:1 |
| B14 | 0.97 | 4 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.97 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.20 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.20 | 2 | contrast | PASS | contrast 7.69:1 >= 4.5:1 |
| B15 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.50 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.50 | 2 | contrast | PASS | contrast 7.90:1 >= 4.5:1 |
| B15 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.97 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.97 | 2 | contrast | PASS | contrast 11.97:1 >= 4.5:1 |
| B15 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B16 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px |
| B16 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B16 | 0.20 | 0 | contrast | PASS | contrast 9.06:1 >= 4.5:1 |
| B16 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 5.38:1 >= 3.0:1 (4 blobs) |
| B16 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B16 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px |
| B16 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B16 | 0.50 | 0 | contrast | PASS | contrast 8.92:1 >= 4.5:1 |
| B16 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 5.38:1 >= 3.0:1 (4 blobs) |
| B16 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B16 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px |
| B16 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B16 | 0.97 | 0 | contrast | PASS | contrast 12.49:1 >= 4.5:1 |
| B16 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 5.38:1 >= 3.0:1 (5 blobs) |
| B16 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(192,1674)–(3648,1910) h=236px (5.2×med) |
| B20 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B20 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B20 | 0.20 | 0 | contrast | PASS | contrast 13.73:1 >= 4.5:1 |
| B20 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.32:1 >= 3.0:1 (4 blobs) |
| B20 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(192,1002)–(2300,1528) h=526px (2.4×med) |
| B20 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B20 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B20 | 0.50 | 0 | contrast | PASS | contrast 13.66:1 >= 4.5:1 |
| B20 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.32:1 >= 3.0:1 (4 blobs) |
| B20 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(192,1002)–(2300,1528) h=526px (2.4×med) |
| B20 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B20 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B20 | 0.97 | 0 | contrast | PASS | contrast 13.02:1 >= 4.5:1 |
| B20 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.32:1 >= 3.0:1 (4 blobs) |
| B20 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(192,1002)–(2300,1528) h=526px (2.4×med) |
| B22 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B22 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B22 | 0.20 | 0 | contrast | PASS | contrast 14.25:1 >= 4.5:1 |
| B22 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B22 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B22 | 0.50 | 0 | min-size | PASS | min text-run height 320px >= floor 41px |
| B22 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B22 | 0.50 | 0 | contrast | PASS | contrast 13.05:1 >= 4.5:1 |
| B22 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 11.74:1 >= 3.0:1 (1 blobs) |
| B22 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B22 | 0.97 | 0 | min-size | PASS | min text-run height 320px >= floor 41px |
| B22 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B22 | 0.97 | 0 | contrast | PASS | contrast 13.71:1 >= 4.5:1 |
| B22 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 11.74:1 >= 3.0:1 (2 blobs) |
| B22 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B23 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B23 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B23 | 0.20 | 0 | contrast | PASS | contrast 10.53:1 >= 4.5:1 |
| B23 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.72:1 >= 3.0:1 (2 blobs) |
| B23 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B23 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B23 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B23 | 0.50 | 0 | contrast | PASS | contrast 10.50:1 >= 4.5:1 |
| B23 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (2 blobs) |
| B23 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B23 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B23 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B23 | 0.97 | 0 | contrast | PASS | contrast 10.50:1 >= 4.5:1 |
| B23 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (2 blobs) |
| B23 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B24 | 0.20 | 6 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B24 | 0.20 | 6 | overflow | PASS | no text-run blobs above noise threshold |
| B24 | 0.20 | 6 | contrast | PASS | contrast 8.08:1 >= 4.5:1 |
| B24 | 0.20 | 6 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B24 | 0.20 | 6 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B24 | 0.50 | 6 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B24 | 0.50 | 6 | overflow | PASS | no text-run blobs above noise threshold |
| B24 | 0.50 | 6 | contrast | PASS | contrast 8.06:1 >= 4.5:1 |
| B24 | 0.50 | 6 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B24 | 0.50 | 6 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B24 | 0.97 | 6 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B24 | 0.97 | 6 | overflow | PASS | no text-run blobs above noise threshold |
| B24 | 0.97 | 6 | contrast | PASS | contrast 8.44:1 >= 4.5:1 |
| B24 | 0.97 | 6 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B24 | 0.97 | 6 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
