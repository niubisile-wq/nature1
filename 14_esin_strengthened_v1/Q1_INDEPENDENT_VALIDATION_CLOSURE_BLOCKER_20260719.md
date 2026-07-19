# Q1 independent validation closure status

Date: 2026-07-19

## Bottom line

The manuscript cannot truthfully claim a completed Po/Rhone EGMS strong-subsidence independent validation yet.

The current strengthened package has:

- completed Chao Phraya lead exposure closure;
- completed robustness tests;
- completed DWR/TRE--GHSL external positive-control probe;
- completed Cyprus EGMS near-zero boundary control;
- completed Po non-EGMS transfer support;
- prepared EGMS/CLMS scripts and query payloads for Po delta, Po-Venice and Rhone/Camargue.

It does not yet have a downloaded EGMS L3 ORTHO-UP product for Po delta, Po-Venice or Rhone/Camargue.

## Files checked

- `egms_priority_downloads_v1/po_delta_core/l3_ortho_up/DOWNLOAD_HERE.txt`
- `egms_priority_downloads_v1/po_venice_broad/l3_ortho_up/DOWNLOAD_HERE.txt`
- `egms_priority_downloads_v1/rhone_delta_core/l3_ortho_up/DOWNLOAD_HERE.txt`
- `egms_manual_download_preflight_report_v1.json`
- `sourcecoop_public_discovery_20260719/sourcecoop_egms_public_discovery_20260719.md`

All three priority EGMS target folders contain only placeholder files at the time of this audit.

## Why this matters

The Q1-level upgrade requires an independent strong-subsidence closure, not another internal sensitivity test. The missing evidence is a real EGMS/CLMS product file that overlaps a deformation-relevant European delta target and can be intersected with GHSL exposure.

Without that file, the defensible manuscript wording remains:

- DWR/TRE is a completed external positive control;
- Cyprus EGMS is a completed near-zero boundary control and code-path proof;
- Po is a non-EGMS transfer case supported by sparse published geodetic context;
- Po/Rhone EGMS closure is prepared but not claimed.

## Exact completion command after data are added

Place the downloaded EGMS L3 ORTHO-UP 2019-2023 product file in one of these folders:

- `egms_priority_downloads_v1/po_delta_core/l3_ortho_up/`
- `egms_priority_downloads_v1/po_venice_broad/l3_ortho_up/`
- `egms_priority_downloads_v1/rhone_delta_core/l3_ortho_up/`

Then run:

```powershell
py -3 .\preflight_egms_manual_downloads_v1.py
```

If the report lists a ready candidate, run:

```powershell
py -3 .\run_egms_clms_priority_closure_v1.py --local-egms-file .\egms_priority_downloads_v1\po_delta_core\l3_ortho_up\SELECTED_EGMS_FILE.csv --aoi-id po_delta_core --outdir .\egms_priority_benchmark_closure_v1
```

Replace `SELECTED_EGMS_FILE.csv` with the actual file name and change `--aoi-id` if using `po_venice_broad` or `rhone_delta_core`.

## Manuscript rule

Do not add language saying "completed Po/Rhone EGMS validation" until the closure script has produced AOI-specific outputs in `egms_priority_benchmark_closure_v1`.
