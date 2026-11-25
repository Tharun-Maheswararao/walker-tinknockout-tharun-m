# SELFCHECK.md — GATE T functions on the STILL composites (real images masked)

FAILs: 0

| beat | t | masks | check | status | detail |
|---|---|---|---|---|---|
| B00 | 0.20 | 1 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B00 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B00 | 0.20 | 1 | contrast | PASS | contrast 7.30:1 >= 4.5:1 |
| B00 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B00 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B00 | 0.50 | 1 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B00 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B00 | 0.50 | 1 | contrast | PASS | contrast 7.35:1 >= 4.5:1 |
| B00 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B00 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B00 | 0.97 | 1 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B00 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B00 | 0.97 | 1 | contrast | PASS | contrast 7.32:1 >= 4.5:1 |
| B00 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B00 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B01 | 0.20 | 1 | min-size | PASS | min text-run height 47px >= floor 41px (individual-char fallback at 2×) |
| B01 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B01 | 0.20 | 1 | contrast | PASS | contrast 8.01:1 >= 4.5:1 |
| B01 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B01 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B01 | 0.50 | 1 | min-size | PASS | min text-run height 47px >= floor 41px (individual-char fallback at 2×) |
| B01 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B01 | 0.50 | 1 | contrast | PASS | contrast 8.01:1 >= 4.5:1 |
| B01 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B01 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B01 | 0.97 | 1 | min-size | PASS | min text-run height 51px >= floor 41px (individual-char fallback at 2×) |
| B01 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B01 | 0.97 | 1 | contrast | PASS | contrast 7.98:1 >= 4.5:1 |
| B01 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B01 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B03 | 0.20 | 1 | min-size | PASS | min text-run height 51px >= floor 41px |
| B03 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.20 | 1 | contrast | PASS | contrast 7.10:1 >= 4.5:1 |
| B03 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 10.15:1 >= 3.0:1 (1 blobs) |
| B03 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B03 | 0.50 | 1 | min-size | PASS | min text-run height 51px >= floor 41px |
| B03 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.50 | 1 | contrast | PASS | contrast 7.12:1 >= 4.5:1 |
| B03 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 10.15:1 >= 3.0:1 (1 blobs) |
| B03 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B03 | 0.97 | 1 | min-size | PASS | min text-run height 51px >= floor 41px |
| B03 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B03 | 0.97 | 1 | contrast | PASS | contrast 7.08:1 >= 4.5:1 |
| B03 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 10.15:1 >= 3.0:1 (1 blobs) |
| B03 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.20 | 0 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.20 | 0 | contrast | PASS | contrast 12.51:1 >= 4.5:1 |
| B04 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.50 | 0 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.50 | 0 | contrast | PASS | contrast 12.51:1 >= 4.5:1 |
| B04 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B04 | 0.97 | 0 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B04 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B04 | 0.97 | 0 | contrast | PASS | contrast 12.48:1 >= 4.5:1 |
| B04 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B04 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.20 | 1 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.20 | 1 | contrast | PASS | contrast 7.64:1 >= 4.5:1 |
| B05 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.50 | 1 | min-size | PASS | min text-run height 50px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.50 | 1 | contrast | PASS | contrast 7.64:1 >= 4.5:1 |
| B05 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.97 | 1 | min-size | PASS | min text-run height 430px >= floor 41px |
| B05 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B05 | 0.97 | 1 | contrast | PASS | contrast 12.09:1 >= 4.5:1 |
| B05 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 13.08:1 >= 3.0:1 (1 blobs) |
| B05 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.20 | 0 | min-size | PASS | min text-run height 51px >= floor 41px |
| B06 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.20 | 0 | contrast | PASS | contrast 10.24:1 >= 4.5:1 |
| B06 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 10.49:1 >= 3.0:1 (1 blobs) |
| B06 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.50 | 0 | min-size | PASS | min text-run height 51px >= floor 41px |
| B06 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.50 | 0 | contrast | PASS | contrast 10.24:1 >= 4.5:1 |
| B06 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 10.49:1 >= 3.0:1 (1 blobs) |
| B06 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.97 | 0 | min-size | PASS | min text-run height 51px >= floor 41px |
| B06 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.97 | 0 | contrast | PASS | contrast 9.12:1 >= 4.5:1 |
| B06 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 10.49:1 >= 3.0:1 (1 blobs) |
| B06 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.20 | 1 | min-size | PASS | min text-run height 51px >= floor 41px |
| B07 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.20 | 1 | contrast | PASS | contrast 7.04:1 >= 4.5:1 |
| B07 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (1 blobs) |
| B07 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.50 | 1 | min-size | PASS | min text-run height 51px >= floor 41px |
| B07 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.50 | 1 | contrast | PASS | contrast 7.11:1 >= 4.5:1 |
| B07 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (1 blobs) |
| B07 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B07 | 0.97 | 1 | min-size | PASS | min text-run height 51px >= floor 41px |
| B07 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B07 | 0.97 | 1 | contrast | PASS | contrast 7.11:1 >= 4.5:1 |
| B07 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 9.73:1 >= 3.0:1 (1 blobs) |
| B07 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.20 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.20 | 0 | contrast | PASS | contrast 9.90:1 >= 4.5:1 |
| B08 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.50 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.50 | 0 | contrast | PASS | contrast 9.57:1 >= 4.5:1 |
| B08 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.97 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.97 | 0 | contrast | PASS | contrast 12.78:1 >= 4.5:1 |
| B08 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.20 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.20 | 0 | contrast | PASS | contrast 9.00:1 >= 4.5:1 |
| B09 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.50 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.50 | 0 | contrast | PASS | contrast 9.21:1 >= 4.5:1 |
| B09 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.97 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B09 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B09 | 0.97 | 0 | contrast | PASS | contrast 9.00:1 >= 4.5:1 |
| B09 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B09 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.20 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.20 | 0 | contrast | PASS | contrast 9.52:1 >= 4.5:1 |
| B10 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.52:1 >= 3.0:1 (1 blobs) |
| B10 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.50 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.50 | 0 | contrast | PASS | contrast 9.63:1 >= 4.5:1 |
| B10 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.52:1 >= 3.0:1 (1 blobs) |
| B10 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.97 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.97 | 0 | contrast | PASS | contrast 9.36:1 >= 4.5:1 |
| B10 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.20 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.20 | 0 | contrast | PASS | contrast 12.61:1 >= 4.5:1 |
| B12 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.50 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.50 | 0 | contrast | PASS | contrast 12.52:1 >= 4.5:1 |
| B12 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.97 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.97 | 0 | contrast | PASS | contrast 12.52:1 >= 4.5:1 |
| B12 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.20 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.20 | 0 | contrast | PASS | contrast 9.84:1 >= 4.5:1 |
| B13 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.50 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.50 | 0 | contrast | PASS | contrast 9.57:1 >= 4.5:1 |
| B13 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.97 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B13 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B13 | 0.97 | 0 | contrast | PASS | contrast 9.31:1 >= 4.5:1 |
| B13 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B13 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.20 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.20 | 0 | contrast | PASS | contrast 9.73:1 >= 4.5:1 |
| B14 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.50 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.50 | 0 | contrast | PASS | contrast 9.73:1 >= 4.5:1 |
| B14 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.97 | 0 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.97 | 0 | contrast | PASS | contrast 9.60:1 >= 4.5:1 |
| B14 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.20 | 1 | min-size | PASS | min text-run height 46px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.20 | 1 | contrast | PASS | contrast 8.24:1 >= 4.5:1 |
| B15 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.50 | 1 | min-size | PASS | min text-run height 46px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.50 | 1 | contrast | PASS | contrast 8.24:1 >= 4.5:1 |
| B15 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.97 | 1 | min-size | PASS | min text-run height 46px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.97 | 1 | contrast | PASS | contrast 8.24:1 >= 4.5:1 |
| B15 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
