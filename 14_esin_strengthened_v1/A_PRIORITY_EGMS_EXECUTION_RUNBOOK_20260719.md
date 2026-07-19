# A-Priority EGMS Execution Runbook

Date: 2026-07-19

## Purpose

This runbook executes the independent strong-subsidence EGMS benchmark planned for the ESIN manuscript.

The current strengthened package contains:

- completed Cyprus EGMS boundary-control closure;
- frozen Po delta, Po-Venice and Rhone/Camargue AOI payloads;
- local closure scripts for EGMS/GHSL point-support exposure accounting.

It does not contain an authenticated CLMS/EGMS token or a local Po/Rhone EGMS product file. Do not describe the Po/Rhone benchmark as completed until one of the commands below has been executed and its output has been inspected.

Public Source Cooperative discovery was also attempted. The public mirror lists Cyprus L2a parquet objects, but no Italy or France parquet objects were found under the public `L2a/parquet/` prefix during this pass. Therefore the Po/Rhone benchmark still depends on CLMS/EGMS authenticated access or a manually supplied EGMS product file.

## Credential Inputs Accepted

Use one of:

- `$env:EGMS_ACCESS_TOKEN`
- `$env:CLMS_ACCESS_TOKEN`
- `$env:EGMS_SERVICE_KEY_JSON`
- `$env:CLMS_SERVICE_KEY_JSON`
- local EGMS csv/parquet downloaded manually from CLMS

Current environment check on 2026-07-19: no EGMS/CLMS credential variables were present.

The download wrapper follows the official EGMS API notebook endpoint:

- `https://egms.land.copernicus.eu/insar-api/archive/search`
- `https://egms.land.copernicus.eu/insar-api/archive/download/{filename}?id={query_id}`

Place the CLMS API service key as `token.jwt` in this package root, or pass it with `--service-key-json`. Do not include `token.jwt` in any public submission archive.

## Priority 1: Po Delta Core

```powershell
python .\run_egms_clms_priority_closure_v1.py `
  --payloads .\egms_query_payloads.json `
  --aoi-id po_delta_core `
  --query-kind l3_ortho_up `
  --outdir .\egms_priority_benchmark_closure_v1 `
  --download-dir .\egms_priority_downloads_v1
```

If a product was downloaded manually:

```powershell
python .\build_egms_benchmark_closure_v1.py `
  --input .\egms_priority_downloads_v1\po_delta_core\SELECTED_EGMS_FILE.parquet `
  --outdir .\egms_priority_benchmark_closure_v1\po_delta_core `
  --aoi-id po_delta_core `
  --product-label EGMS_L3_ORTHO_UP_2019_2023 `
  --thresholds 1,2,5,10
```

## Priority 2: Po-Venice Broad

```powershell
python .\run_egms_clms_priority_closure_v1.py `
  --payloads .\egms_query_payloads.json `
  --aoi-id po_venice_broad `
  --query-kind l3_ortho_up `
  --outdir .\egms_priority_benchmark_closure_v1 `
  --download-dir .\egms_priority_downloads_v1
```

## Priority 3: Rhone/Camargue

```powershell
python .\run_egms_clms_priority_closure_v1.py `
  --payloads .\egms_query_payloads.json `
  --aoi-id rhone_delta_core `
  --query-kind l3_ortho_up `
  --outdir .\egms_priority_benchmark_closure_v1 `
  --download-dir .\egms_priority_downloads_v1
```

## Acceptance Criteria

A completed A-priority benchmark must include:

- local EGMS product file with provenance;
- threshold closure CSV for 1, 2, 5 and 10 mm/yr;
- metadata JSON identifying lon/lat/velocity columns and source file;
- point overlay sample CSV;
- short report distinguishing point-support exposure closure from areal observability-mask closure.

## Manuscript Integration Rule

- If Po or Rhone produces a strong-subsidence closure, promote it into the Results as an independent EGMS benchmark.
- If it produces near-zero strong-subsidence exposure, keep it as a boundary/control case.
- If product access is unavailable, keep the manuscript wording as "execution-ready; product access pending."
