# SELFCHECK.md — GATE T functions on the STILL composites (real images masked)

FAILs: 0

| beat | t | masks | check | status | detail |
|---|---|---|---|---|---|
| B02 | 0.20 | 2 | min-size | PASS | min text-run height 45px >= floor 41px |
| B02 | 0.20 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.20 | 2 | contrast | PASS | contrast 8.63:1 >= 4.5:1 |
| B02 | 0.20 | 2 | contrast-local | PASS | per-blob contrast min 9.62:1 >= 3.0:1 (2 blobs) |
| B02 | 0.20 | 2 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B02 | 0.50 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B02 | 0.50 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.50 | 2 | contrast | PASS | contrast 8.64:1 >= 4.5:1 |
| B02 | 0.50 | 2 | contrast-local | PASS | per-blob contrast min 9.62:1 >= 3.0:1 (2 blobs) |
| B02 | 0.50 | 2 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B02 | 0.97 | 2 | min-size | PASS | min text-run height 46px >= floor 41px |
| B02 | 0.97 | 2 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B02 | 0.97 | 2 | contrast | PASS | contrast 8.47:1 >= 4.5:1 |
| B02 | 0.97 | 2 | contrast-local | PASS | per-blob contrast min 9.62:1 >= 3.0:1 (2 blobs) |
| B02 | 0.97 | 2 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B04 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B04 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B04 | 0.20 | 0 | contrast | PASS | contrast 11.98:1 >= 4.5:1 |
| B04 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.95:1 >= 3.0:1 (2 blobs) |
| B04 | 0.20 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B04 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B04 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B04 | 0.50 | 0 | contrast | PASS | contrast 13.68:1 >= 4.5:1 |
| B04 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (2 blobs) |
| B04 | 0.50 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B04 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B04 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B04 | 0.97 | 0 | contrast | PASS | contrast 13.74:1 >= 4.5:1 |
| B04 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (3 blobs) |
| B04 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance / §8.6c ADVISORY: possible fused run(s) — blob@(1860,1340)–(3648,1900) h=560px (1.9×med) |
| B05 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.20 | 0 | contrast | PASS | contrast 12.53:1 >= 4.5:1 |
| B05 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.50 | 0 | contrast | PASS | contrast 13.57:1 >= 4.5:1 |
| B05 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B05 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B05 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B05 | 0.97 | 0 | contrast | PASS | contrast 13.23:1 >= 4.5:1 |
| B05 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B05 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.20 | 1 | contrast | PASS | contrast 14.29:1 >= 4.5:1 |
| B06 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.50 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B06 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B06 | 0.50 | 1 | contrast | PASS | contrast 11.66:1 >= 4.5:1 |
| B06 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B06 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B06 | 0.97 | 1 | min-size | PASS | min text-run height 320px >= floor 41px |
| B06 | 0.97 | 1 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B06 | 0.97 | 1 | contrast | PASS | contrast 13.57:1 >= 4.5:1 |
| B06 | 0.97 | 1 | contrast-local | PASS | per-blob contrast min 11.50:1 >= 3.0:1 (1 blobs) |
| B06 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.20 | 9 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.20 | 9 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.20 | 9 | contrast | PASS | contrast 8.21:1 >= 4.5:1 |
| B08 | 0.20 | 9 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.20 | 9 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.50 | 9 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.50 | 9 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.50 | 9 | contrast | PASS | contrast 11.57:1 >= 4.5:1 |
| B08 | 0.50 | 9 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.50 | 9 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B08 | 0.97 | 9 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B08 | 0.97 | 9 | overflow | PASS | no text-run blobs above noise threshold |
| B08 | 0.97 | 9 | contrast | PASS | contrast 11.57:1 >= 4.5:1 |
| B08 | 0.97 | 9 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B08 | 0.97 | 9 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B09 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B09 | 0.20 | 0 | contrast | PASS | contrast 9.74:1 >= 4.5:1 |
| B09 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B09 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B09 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B09 | 0.50 | 0 | contrast | PASS | contrast 9.56:1 >= 4.5:1 |
| B09 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B09 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B09 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B09 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B09 | 0.97 | 0 | contrast | PASS | contrast 9.16:1 >= 4.5:1 |
| B09 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B09 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.20 | 8 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.20 | 8 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.20 | 8 | contrast | PASS | contrast 7.61:1 >= 4.5:1 |
| B10 | 0.20 | 8 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.20 | 8 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.50 | 8 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.50 | 8 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.50 | 8 | contrast | PASS | contrast 7.53:1 >= 4.5:1 |
| B10 | 0.50 | 8 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.50 | 8 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B10 | 0.97 | 8 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B10 | 0.97 | 8 | overflow | PASS | no text-run blobs above noise threshold |
| B10 | 0.97 | 8 | contrast | PASS | contrast 7.95:1 >= 4.5:1 |
| B10 | 0.97 | 8 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B10 | 0.97 | 8 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B11 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B11 | 0.20 | 0 | contrast | PASS | contrast 14.00:1 >= 4.5:1 |
| B11 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B11 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B11 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B11 | 0.50 | 0 | contrast | PASS | contrast 12.28:1 >= 4.5:1 |
| B11 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B11 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B11 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B11 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B11 | 0.97 | 0 | contrast | PASS | contrast 12.28:1 >= 4.5:1 |
| B11 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B11 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.20 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.20 | 2 | contrast | PASS | contrast 7.56:1 >= 4.5:1 |
| B12 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.50 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.50 | 2 | contrast | PASS | contrast 7.46:1 >= 4.5:1 |
| B12 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B12 | 0.97 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B12 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B12 | 0.97 | 2 | contrast | PASS | contrast 8.46:1 >= 4.5:1 |
| B12 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B12 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.20 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B13 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B13 | 0.20 | 0 | contrast | PASS | contrast 13.37:1 >= 4.5:1 |
| B13 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B13 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.50 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B13 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B13 | 0.50 | 0 | contrast | PASS | contrast 13.64:1 >= 4.5:1 |
| B13 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B13 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B13 | 0.97 | 0 | min-size | PASS | min text-run height 46px >= floor 41px |
| B13 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B13 | 0.97 | 0 | contrast | PASS | contrast 12.95:1 >= 4.5:1 |
| B13 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.91:1 >= 3.0:1 (1 blobs) |
| B13 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.20 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.20 | 2 | contrast | PASS | contrast 7.05:1 >= 4.5:1 |
| B14 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.50 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.50 | 2 | contrast | PASS | contrast 7.05:1 >= 4.5:1 |
| B14 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B14 | 0.97 | 2 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B14 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B14 | 0.97 | 2 | contrast | PASS | contrast 7.05:1 >= 4.5:1 |
| B14 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B14 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.20 | 0 | contrast | PASS | contrast 12.42:1 >= 4.5:1 |
| B15 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B15 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B15 | 0.50 | 0 | contrast | PASS | contrast 12.42:1 >= 4.5:1 |
| B15 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B15 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B15 | 0.97 | 0 | min-size | PASS | min text-run height 232px >= floor 41px |
| B15 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B15 | 0.97 | 0 | contrast | PASS | contrast 12.35:1 >= 4.5:1 |
| B15 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 10.89:1 >= 3.0:1 (2 blobs) |
| B15 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B16 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B16 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B16 | 0.20 | 1 | contrast | PASS | contrast 7.60:1 >= 4.5:1 |
| B16 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B16 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B16 | 0.50 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B16 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B16 | 0.50 | 1 | contrast | PASS | contrast 8.51:1 >= 4.5:1 |
| B16 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B16 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B16 | 0.97 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B16 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B16 | 0.97 | 1 | contrast | PASS | contrast 9.08:1 >= 4.5:1 |
| B16 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B16 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B17 | 0.20 | 0 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B17 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B17 | 0.20 | 0 | contrast | PASS | contrast 9.47:1 >= 4.5:1 |
| B17 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B17 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B17 | 0.50 | 0 | min-size | PASS | min text-run height 43px >= floor 41px (individual-char fallback at 2×) |
| B17 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B17 | 0.50 | 0 | contrast | PASS | contrast 9.47:1 >= 4.5:1 |
| B17 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B17 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B17 | 0.97 | 0 | min-size | PASS | min text-run height 356px >= floor 41px |
| B17 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B17 | 0.97 | 0 | contrast | PASS | contrast 11.28:1 >= 4.5:1 |
| B17 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 9.41:1 >= 3.0:1 (2 blobs) |
| B17 | 0.97 | 0 | bbox-overlap | PASS | no text-run bbox overlaps above 10% tolerance |
| B18 | 0.20 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B18 | 0.20 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B18 | 0.20 | 1 | contrast | PASS | contrast 8.34:1 >= 4.5:1 |
| B18 | 0.20 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B18 | 0.20 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B18 | 0.50 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B18 | 0.50 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B18 | 0.50 | 1 | contrast | PASS | contrast 8.68:1 >= 4.5:1 |
| B18 | 0.50 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B18 | 0.50 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B18 | 0.97 | 1 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B18 | 0.97 | 1 | overflow | PASS | no text-run blobs above noise threshold |
| B18 | 0.97 | 1 | contrast | PASS | contrast 8.56:1 >= 4.5:1 |
| B18 | 0.97 | 1 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B18 | 0.97 | 1 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B19 | 0.20 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B19 | 0.20 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B19 | 0.20 | 2 | contrast | PASS | contrast 7.36:1 >= 4.5:1 |
| B19 | 0.20 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B19 | 0.20 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B19 | 0.50 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B19 | 0.50 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B19 | 0.50 | 2 | contrast | PASS | contrast 7.33:1 >= 4.5:1 |
| B19 | 0.50 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B19 | 0.50 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B19 | 0.97 | 2 | min-size | PASS | min text-run height 41px >= floor 41px (individual-char fallback at 2×) |
| B19 | 0.97 | 2 | overflow | PASS | no text-run blobs above noise threshold |
| B19 | 0.97 | 2 | contrast | PASS | contrast 7.36:1 >= 4.5:1 |
| B19 | 0.97 | 2 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B19 | 0.97 | 2 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
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
| B21 | 0.20 | 0 | min-size | PASS | min text-run height 840px >= floor 41px |
| B21 | 0.20 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B21 | 0.20 | 0 | contrast | PASS | contrast 13.93:1 >= 4.5:1 |
| B21 | 0.20 | 0 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B21 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B21 | 0.50 | 0 | min-size | PASS | min text-run height 840px >= floor 41px |
| B21 | 0.50 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B21 | 0.50 | 0 | contrast | PASS | contrast 13.78:1 >= 4.5:1 |
| B21 | 0.50 | 0 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B21 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B21 | 0.97 | 0 | min-size | PASS | min text-run height 840px >= floor 41px |
| B21 | 0.97 | 0 | overflow | PASS | all text runs inside safe area (192,108)→(3648,2052) |
| B21 | 0.97 | 0 | contrast | PASS | contrast 13.45:1 >= 4.5:1 |
| B21 | 0.97 | 0 | contrast-local | PASS | per-blob contrast min 14.46:1 >= 3.0:1 (1 blobs) |
| B21 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B22 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B22 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B22 | 0.20 | 0 | contrast | PASS | contrast 7.68:1 >= 4.5:1 |
| B22 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B22 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B22 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B22 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B22 | 0.50 | 0 | contrast | PASS | contrast 9.51:1 >= 4.5:1 |
| B22 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B22 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B22 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B22 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B22 | 0.97 | 0 | contrast | PASS | contrast 13.90:1 >= 4.5:1 |
| B22 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B22 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B23 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B23 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B23 | 0.20 | 0 | contrast | PASS | contrast 8.65:1 >= 4.5:1 |
| B23 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B23 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B23 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B23 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B23 | 0.50 | 0 | contrast | PASS | contrast 8.63:1 >= 4.5:1 |
| B23 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B23 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B23 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B23 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B23 | 0.97 | 0 | contrast | PASS | contrast 9.89:1 >= 4.5:1 |
| B23 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B23 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B24 | 0.20 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B24 | 0.20 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B24 | 0.20 | 0 | contrast | PASS | contrast 10.29:1 >= 4.5:1 |
| B24 | 0.20 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B24 | 0.20 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B24 | 0.50 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B24 | 0.50 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B24 | 0.50 | 0 | contrast | PASS | contrast 10.29:1 >= 4.5:1 |
| B24 | 0.50 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B24 | 0.50 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
| B24 | 0.97 | 0 | min-size | PASS | min text-run height 45px >= floor 41px (individual-char fallback at 2×) |
| B24 | 0.97 | 0 | overflow | PASS | no text-run blobs above noise threshold |
| B24 | 0.97 | 0 | contrast | PASS | contrast 9.66:1 >= 4.5:1 |
| B24 | 0.97 | 0 | contrast-local | PASS | no text-run blobs found for per-blob check |
| B24 | 0.97 | 0 | bbox-overlap | PASS | fewer than 2 text-run blobs — no overlaps possible |
