# ESIN submission gate status

Date: 2026-07-19

Overall status: `no_egms_credential_submission_route_ready`

## Passed gates

- Manuscript compilation: passed. `ESIN_strengthened_v1.pdf` compiles to 13 pages; latest log scan found no undefined references or LaTeX fatal errors.
- Cyprus EGMS boundary control: passed. The Cyprus run reports 17,340 valid EGMS/GHSL point overlays and 65 strong points at the 5 mm/yr threshold.
- EGMS reader regression: passed. `egms_boundary_control_cyprus_regression_v1` reproduces the Cyprus threshold values after input-reader broadening.
- EGMS input compatibility: passed. `egms_input_compatibility_selftest_v1` accepts `.csv`, `.csv.gz`, `.parquet` and `.pq` files with variant EGMS-style column names.
- Regional non-EGMS strengthening: passed. `regional_non_egms_strengthening_v1.csv` separates local Po/Chao Phraya/Brantas/Rhone/Rhine evidence roles without promoting them to independent EGMS validation.
- No-EGMS-credential route: passed. The manuscript now uses DWR/TRE positive control, Cyprus EGMS boundary control and Po sparse geodetic context instead of claiming Po/Rhone EGMS completion.

## Future upgrade gates

- `po_delta_core`: needs EGMS L3 ORTHO-UP 2019-2023 for bbox `[11.7, 44.35, 12.9, 45.55]`.
- `po_venice_broad`: needs EGMS L3 ORTHO-UP 2019-2023 for bbox `[10.0, 44.0, 13.0, 46.0]`.
- `rhone_delta_core`: needs EGMS L3 ORTHO-UP 2019-2023 for bbox `[4.0, 43.2, 5.15, 44.05]`.

Q1-level independent strong-subsidence validation remains blocked until one of these EGMS products is downloaded or otherwise supplied as a real `.csv`, `.csv.gz`, `.parquet` or `.pq` product file. See `Q1_INDEPENDENT_VALIDATION_CLOSURE_BLOCKER_20260719.md`.

Current preflight status: all three target folders contain only `DOWNLOAD_HERE.txt` placeholders and no ready EGMS product candidates. These are future upgrade hooks, not present-tense manuscript claims.

Official EGMS API endpoint now used by the wrapper:

```text
https://egms.land.copernicus.eu/insar-api/archive
```

## Next commands

After placing downloaded EGMS files in the target folders:

```powershell
py -3 .\preflight_egms_manual_downloads_v1.py
```

Then run each closure, replacing `SELECTED_EGMS_FILE.csv` with the real file name:

```powershell
py -3 .\run_egms_clms_priority_closure_v1.py --local-egms-file .\egms_priority_downloads_v1\po_delta_core\l3_ortho_up\SELECTED_EGMS_FILE.csv --aoi-id po_delta_core --outdir .\egms_priority_benchmark_closure_v1
py -3 .\run_egms_clms_priority_closure_v1.py --local-egms-file .\egms_priority_downloads_v1\po_venice_broad\l3_ortho_up\SELECTED_EGMS_FILE.csv --aoi-id po_venice_broad --outdir .\egms_priority_benchmark_closure_v1
py -3 .\run_egms_clms_priority_closure_v1.py --local-egms-file .\egms_priority_downloads_v1\rhone_delta_core\l3_ortho_up\SELECTED_EGMS_FILE.csv --aoi-id rhone_delta_core --outdir .\egms_priority_benchmark_closure_v1
```

If a CLMS API service key is available, save it as `token.jwt` in the package root and run:

```powershell
py -3 .\run_egms_clms_priority_closure_v1.py --aoi-id po_delta_core --query-kind l3_ortho_up --outdir .\egms_priority_benchmark_closure_v1
```

## Claim boundary

The no-EGMS-credential submission route is ready. Po/Rhone independent EGMS strong-subsidence validation is not claimed; it remains a future upgrade if official EGMS product files or CLMS credentials become available.
