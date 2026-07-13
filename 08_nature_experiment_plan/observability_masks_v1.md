# Observability Masks v1
Date: 2026-07-10

## Scope
This note consolidates the current observability-failure outputs for the lead Chao Phraya case and the multi-delta screening set.

## Local Sources
- Cell-level Chao Phraya exposure table: `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/chao_phraya_area_weighted_exposure_cells.csv`
- Chao Phraya exposure summary: `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/chao_phraya_area_weighted_exposure_summary.csv`
- Multi-delta exposure summary: `03_exposure_closure/multi_delta_vlm_exposure_censoring_summary.csv`
- Multi-delta report: `03_exposure_closure/multi_delta_vlm_exposure_censoring_report.md`

## What the masks already show
- The Chao Phraya cell table contains `observable_count`, `observable_fraction`, `any_observable`, `majority_observable`, `not_majority_observable`, and `strong_sub_5mm`.
- The VLM-grid closure is already exposure-weighted for population and built-up area.
- The multi-delta summary confirms the same censoring pattern in Po, Chao Phraya, and Brantas.

## Key screening result
- Chao Phraya strong-subsidence cells are frequently not majority observable, and the same pattern persists in the population and built-up overlays.
- The multi-delta report gives the same conclusion at the screening level, with Chao Phraya showing the strongest signal.

## What is still missing
- A single polygon / equal-area mask product per lead region.
- A consolidated `observability_masks_v1.csv` or GeoTIFF package that can be treated as the final export artifact.
- A full multi-region polygon benchmark that matches the final Nature-level gate.

## Conclusion
The observability-failure layer is already real and reproducible in local outputs, but the final exported mask package is still incomplete. The current state is sufficient for manuscript analysis and figure generation, not yet sufficient for a fully published benchmark release.

