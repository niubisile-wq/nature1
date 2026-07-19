# EGMS manual download manifest

Date: 2026-07-19

Purpose: define the exact files still needed to complete the A-priority independent EGMS benchmark for the ESIN/Nature-strengthening package.

## Required products

Download EGMS Ortho vertical point products from CLMS/EGMS Explorer or API. Use release `2019-2023` and product type `ORTHO-UP` wherever the interface exposes these choices.

| Priority | AOI id | Region | Bbox lon/lat | Required product | Target folder |
|---|---|---|---|---|---|
| A1 | `po_delta_core` | Po delta core | `[11.7, 44.35, 12.9, 45.55]` | EGMS L3 ORTHO-UP 2019-2023 | `egms_priority_downloads_v1/po_delta_core/l3_ortho_up/` |
| A2 | `po_venice_broad` | Po Basin and Venice | `[10.0, 44.0, 13.0, 46.0]` | EGMS L3 ORTHO-UP 2019-2023 | `egms_priority_downloads_v1/po_venice_broad/l3_ortho_up/` |
| A3 | `rhone_delta_core` | Rhone/Camargue | `[4.0, 43.2, 5.15, 44.05]` | EGMS L3 ORTHO-UP 2019-2023 | `egms_priority_downloads_v1/rhone_delta_core/l3_ortho_up/` |

Optional products for later sensitivity checks:

| AOI id | Optional product | Use |
|---|---|---|
| `po_delta_core` | EGMS L3 ORTHO-EAST 2019-2023 | Horizontal-component sanity check |
| `po_venice_broad` | EGMS L3 ORTHO-EAST 2019-2023 | Horizontal-component sanity check |
| `rhone_delta_core` | EGMS L3 ORTHO-EAST 2019-2023 | Horizontal-component sanity check |
| any A-priority AOI | EGMS L2B calibrated | Product-lineage sensitivity, not required for first closure |

## Accepted local input formats

The local closure script can read `.csv`, `.parquet`, `.pq` and compressed CSV files if the installed Python stack supports them. If CLMS returns `.zip` or `.gpkg`, extract or convert the EGMS point table first, then rerun with `--local-egms-file`.

Minimum required content:

- point coordinates: recognized columns include common longitude/latitude names such as `lon`, `longitude`, `lat`, `latitude`, `easting`, `northing`, or geometry-backed parquet fields;
- vertical velocity: recognized by the closure script from EGMS-style velocity columns such as `velocity`, `mean_velocity`, `v`, `vel`, `up`, or similar numeric fields after inspection;
- enough point density inside the AOI to support threshold summaries at 1, 2, 5 and 10 mm/yr.

## Preflight commands

After placing files in the target folders, run:

```powershell
py -3 .\preflight_egms_manual_downloads_v1.py
```

Then run the closure for each readable file, for example:

```powershell
py -3 .\run_egms_clms_priority_closure_v1.py `
  --local-egms-file .\egms_priority_downloads_v1\po_delta_core\l3_ortho_up\SELECTED_EGMS_FILE.csv `
  --aoi-id po_delta_core `
  --outdir .\egms_priority_closure_outputs_v1
```

## Promotion rule

Only promote an AOI into the manuscript as completed independent EGMS validation after:

1. `egms_benchmark_closure_thresholds_v1.csv` exists for the AOI;
2. the `-5 mm/yr` threshold has a non-trivial strong-subsidence sample or is explicitly interpreted as a negative/control result;
3. `egms_benchmark_closure_meta_v1.json` records the local file provenance;
4. the result has been compared against the current Po/Rhone local regional synthesis rather than substituted for it.
