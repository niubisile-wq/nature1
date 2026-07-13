# P0 Rerun Manifest v1
Date: 2026-07-13

## Purpose

Define the smallest deterministic rerun path that can rebuild the manuscript-facing Nature evidence package from frozen inputs.

## Scope lock

This manifest applies only to the Nature manuscript line under `Desktop/nature`.

## Current rerunable core

These scripts are currently the cleanest P0 rerun candidates:

- `07_scripts_and_registry/fit_chao_phraya_nature_model_selfcontained.py`
- `07_scripts_and_registry/fit_multi_region_blocked_equal_area_closure.py`
- `07_scripts_and_registry/fit_hierarchical_model_comparison.py`
- `07_scripts_and_registry/build_transfer_validation_scores.py`
- `07_scripts_and_registry/compute_chao_phraya_area_weighted_exposure.py`
- `07_scripts_and_registry/compute_chao_phraya_osm_exposure_censoring.py`
- `07_scripts_and_registry/compute_chao_phraya_robustness_grid.py`

## P0 rerun chain

1. Run the self-contained Chao Phraya model.
2. Rebuild the Chao Phraya exposure closure tables.
3. Rebuild the blocked/equal-area regional synthesis.
4. Rebuild the frozen hierarchical model comparison.
5. Rebuild the transfer score table from the frozen probe outputs.
6. Regenerate the manuscript-critical figures and source-data tables if the upstream tables changed.

## Expected outputs

| step | script | primary outputs | current status |
|---|---|---|---|
| 1 | `fit_chao_phraya_nature_model_selfcontained.py` | Chao Phraya primary report, coefficients, bootstrap table, block-split diagnostics | rerunnable |
| 2 | `compute_chao_phraya_area_weighted_exposure.py` | area-weighted exposure closure tables | rerunnable |
| 2 | `compute_chao_phraya_osm_exposure_censoring.py` | OSM exposure censoring tables | rerunnable |
| 2 | `compute_chao_phraya_robustness_grid.py` | robustness grid and sensitivity summaries | rerunnable |
| 3 | `fit_multi_region_blocked_equal_area_closure.py` | blocked/equal-area region table, meta-regression, leave-one-out table | rerunnable if frozen benchmark CSVs are intact |
| 4 | `fit_hierarchical_model_comparison.py` | hierarchical comparison, coefficients, leave-one-out table | rerunnable if comparison inputs are intact |
| 5 | `build_transfer_validation_scores.py` | transfer validation CSV and MD summary | rerunnable if probe JSON outputs exist |
| 6 | figure scripts `make_figure_1_concept_dataset.py` through `make_figure_7_hierarchical_model.py` | main figure set and source-data exports | rerun only after upstream tables change |

## Known blockers

- `script_dependency_gap_v1.md` still records missing helper modules for the older non-self-contained model stack.
- The self-contained Chao Phraya path is usable now, but the broader all-region model stack is still not fully closed.
- EGMS remains blocked by token access.

## Acceptance criteria

The P0 rerun is acceptable only if all of the following are true:

- the Chao Phraya model reruns without importing missing local helper modules;
- the blocked/equal-area and hierarchical comparison tables can be rebuilt from frozen inputs;
- the transfer-score table can be regenerated from the existing probe outputs;
- any failure is written down with the exact missing file or missing helper name;
- the manifest does not claim that EGMS closure is complete unless local EGMS files exist.

## Evidence tag

This manifest is intended to support the reviewer-facing claim that the Nature package is internally reproducible at the manuscript layer, even though the external EGMS branch remains open.
