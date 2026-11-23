# SELFCHECK.md — GATE T functions on the STILL composites (real images masked)

FAILs: 0

| beat | t | masks | check | status | detail |
|---|---|---|---|---|---|
| B06 | 0.20 | 1 | min-size | PASS | min text-run height 320px >= floor 41px |
| B06 | 0.20 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.20 | 1 | contrast | PASS | contrast 14.26:1 >= 4.5:1 |
| B06 | 0.20 | 1 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B06 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.50 | 1 | min-size | PASS | min text-run height 320px >= floor 41px |
| B06 | 0.50 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.50 | 1 | contrast | PASS | contrast 12.17:1 >= 4.5:1 |
| B06 | 0.50 | 1 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B06 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.97 | 1 | min-size | PASS | min text-run height 320px >= floor 41px |
| B06 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.97 | 1 | contrast | PASS | contrast 13.57:1 >= 4.5:1 |
| B06 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 11.50:1 >= 3.0:1 (1 blobs) |
| B06 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.20 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.20 | 2 | contrast | PASS | contrast 7.33:1 >= 4.5:1 |
| B12 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.50 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.50 | 2 | contrast | PASS | contrast 7.40:1 >= 4.5:1 |
| B12 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.97 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.97 | 2 | contrast | PASS | contrast 8.27:1 >= 4.5:1 |
| B12 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.20 | 0 | min-size | PASS | min text-run height 232px >= floor 41px |
| B15 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B15 | 0.20 | 0 | contrast | PASS | contrast 12.60:1 >= 4.5:1 |
| B15 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 13.01:1 >= 3.0:1 (2 blobs) |
| B15 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B15 | 0.50 | 0 | min-size | PASS | min text-run height 232px >= floor 41px |
| B15 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B15 | 0.50 | 0 | contrast | PASS | contrast 12.60:1 >= 4.5:1 |
| B15 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 13.09:1 >= 3.0:1 (2 blobs) |
| B15 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B15 | 0.97 | 0 | min-size | PASS | min text-run height 232px >= floor 41px |
| B15 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B15 | 0.97 | 0 | contrast | PASS | contrast 12.35:1 >= 4.5:1 |
| B15 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 10.89:1 >= 3.0:1 (2 blobs) |
| B15 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B17 | 0.20 | 0 | min-size | PASS | min text-run height 356px >= floor 41px |
| B17 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B17 | 0.20 | 0 | contrast | PASS | contrast 12.92:1 >= 4.5:1 |
| B17 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 13.56:1 >= 3.0:1 (2 blobs) |
| B17 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B17 | 0.50 | 0 | min-size | PASS | min text-run height 356px >= floor 41px |
| B17 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B17 | 0.50 | 0 | contrast | PASS | contrast 12.92:1 >= 4.5:1 |
| B17 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 13.56:1 >= 3.0:1 (2 blobs) |
| B17 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B17 | 0.97 | 0 | min-size | PASS | min text-run height 356px >= floor 41px |
| B17 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B17 | 0.97 | 0 | contrast | PASS | contrast 11.13:1 >= 4.5:1 |
| B17 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.41:1 >= 3.0:1 (2 blobs) |
| B17 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B20 | 0.20 | 4 | min-size | PASS | min text-run height 46px >= floor 41px |
| B20 | 0.20 | 4 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B20 | 0.20 | 4 | contrast | PASS | contrast 7.83:1 >= 4.5:1 |
| B20 | 0.20 | 4 | contrast-local | PASS | per-blob contrast min 9.54:1 >= 3.0:1 (1 blobs) |
| B20 | 0.20 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B20 | 0.50 | 4 | min-size | PASS | min text-run height 46px >= floor 41px |
| B20 | 0.50 | 4 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B20 | 0.50 | 4 | contrast | PASS | contrast 7.55:1 >= 4.5:1 |
| B20 | 0.50 | 4 | contrast-local | PASS | per-blob contrast min 9.54:1 >= 3.0:1 (1 blobs) |
| B20 | 0.50 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B20 | 0.97 | 4 | min-size | PASS | min text-run height 46px >= floor 41px |
| B20 | 0.97 | 4 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B20 | 0.97 | 4 | contrast | PASS | contrast 8.09:1 >= 4.5:1 |
| B20 | 0.97 | 4 | contrast-local | PASS | per-blob contrast min 9.54:1 >= 3.0:1 (1 blobs) |
| B20 | 0.97 | 4 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
