# P0 Rerun Log v1

Date: 2026-07-13

## Status

- P0 script chain executed in this pass.
- The script is intentionally narrow: it only covers the manuscript-facing Nature rerun chain.

## Steps

- Chao Phraya self-contained model: "07_scripts_and_registry/fit_chao_phraya_nature_model_selfcontained.py"
- Chao Phraya area-weighted exposure: "07_scripts_and_registry/compute_chao_phraya_area_weighted_exposure.py"
- Chao Phraya OSM exposure censoring: "07_scripts_and_registry/compute_chao_phraya_osm_exposure_censoring.py"
- Chao Phraya robustness grid: "07_scripts_and_registry/compute_chao_phraya_robustness_grid.py"
- Blocked equal-area closure: "07_scripts_and_registry/fit_multi_region_blocked_equal_area_closure.py"
- Hierarchical model comparison: "07_scripts_and_registry/fit_hierarchical_model_comparison.py"
- Transfer validation scores: "07_scripts_and_registry/build_transfer_validation_scores.py"

## Notes

- `fit_chao_phraya_nature_model_selfcontained.py` completed and refreshed the lead-case model outputs.
- `compute_chao_phraya_area_weighted_exposure.py` completed with the tiled-window reader path and refreshed the area-weighted exposure bundle.
- `compute_chao_phraya_osm_exposure_censoring.py` completed in midpoint-screening mode and refreshed the transport-exposure bundle.
- `compute_chao_phraya_robustness_grid.py` completed and refreshed the threshold/block bootstrap grid.
- This runner stops on the first failure.
- It does not attempt EGMS closure, which remains token-gated.
- It does not touch other manuscripts.
