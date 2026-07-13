# Script Dependency Gap v1
Date: 2026-07-10

## Purpose

Record which model scripts are blocked by missing local helper modules, and what runnable fallback path exists today.

## Direct Failure Observed

Attempted command:

```powershell
py .\fit_delta_binomial_with_worldcover.py --outdir "C:\Users\刘子轩\Desktop\nature\03_exposure_closure\delta_binomial_with_worldcover_v1" --n-bootstrap 200
```

Observed error:

```text
ModuleNotFoundError: No module named 'benchmark_delta_vlm_lisc_observability'
```

## Missing Helper Modules

The following imports are referenced by the model scripts but are not present as local `.py` files in the current `07_scripts_and_registry` tree:

- `benchmark_delta_vlm_lisc_observability`
- `bootstrap_multi_delta_vlm_exposure_censoring`
- `compute_multi_delta_vlm_exposure_censoring`
- `fit_multi_delta_vlm_binomial_observability`
- `fit_multi_delta_vlm_spatial_logit`
- `fit_multi_region_binomial_with_central_valley`
- `probe_candidate_worldcover_landcover`
- `screen_candidate_delta_vlm_binomial`
- `aggregate_central_valley_lisc_annual_observability`

## What Still Runs Today

- `prepare_egms_rescue_queries.py`
- `probe_japan_licsbas_selected_zip.py`
- `probe_iran_insar_zenodo.py`
- `compute_chao_phraya_area_weighted_exposure.py`
- `compute_chao_phraya_osm_exposure_censoring.py`
- `compute_chao_phraya_robustness_grid.py`

## Runnable Fallback Path

Until the missing helper modules are restored or rewritten, the clean path is:

1. Rebuild summary-level evidence tables from current CSV outputs.
2. Use those tables to keep the manuscript and source-data package internally consistent.
3. Treat the missing model scripts as a separate restoration task rather than pretending the model stack is runnable.

## Implication

The main Nature-level evidence gap is no longer data absence alone. It is now also a code completeness gap for the full multi-region model stack.

However, the lead-case Chao Phraya path is restored through a self-contained script and can be used as the current claim-aligned inferential artifact while the broader model stack is rebuilt.
