# EGMS input compatibility self-test

Date: 2026-07-19

Purpose: verify that the EGMS closure script can ingest common manual-download variants before the Po/Rhone official EGMS products are available.

## Command

```powershell
py -3 .\selftest_egms_input_compatibility_v1.py
```

## Covered cases

The self-test generated the same five-point EGMS-like table in four formats:

- `.csv`
- `.csv.gz`
- `.parquet`
- `.pq`

It used non-exact column names:

- longitude: `Lon Deg`
- latitude: `Lat Deg`
- vertical velocity: `V_UP mm yr`
- temporal coherence: `Temp Coh`
- amplitude dispersion: `Amp Dispersion`

## Result

All four input formats were accepted by `build_egms_benchmark_closure_v1.py`. The script detected the intended coordinate, velocity and optional quality columns in each case. Each run produced five valid closure rows and two strong points at the 5 mm/yr threshold.

The machine-readable report is:

- `egms_input_compatibility_selftest_v1/egms_input_compatibility_selftest_report_v1.json`

This self-test verifies input compatibility only. It does not add Po/Rhone EGMS scientific evidence.
