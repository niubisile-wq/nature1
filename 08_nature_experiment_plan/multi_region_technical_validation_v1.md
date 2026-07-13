# Multi-Region Technical Validation v1
Date: 2026-07-11

## Purpose
This note compiles the frozen technical-validation evidence into a reviewer-facing package. It does not open a new validation split or introduce new model families. It only consolidates what is already frozen on disk.

## Frozen Inputs Used
- `08_nature_experiment_plan/observability_masks_v1.csv`
- `08_nature_experiment_plan/benchmark_sign_unit_audit_v1.md`
- `03_exposure_closure/multi_region_blocked_equal_area_closure_v1/*`
- `03_exposure_closure/multi_region_stratified_control_closure_v1/*`
- `03_exposure_closure/hierarchical_model_v1/*`
- `08_nature_experiment_plan/transfer_validation_scores_v1/*`
- `08_nature_experiment_plan/multi_region_exposure_closure_v1.csv`
- `08_nature_experiment_plan/risk_underestimation_v1.csv`

## Validation Ledger

| layer | frozen artifact | status | key frozen result | reviewer meaning | remaining gap |
|---|---|---|---|---|---|
| Observability masks | `observability_masks_v1.csv` + reconstructed Chao Phraya mask | partial but reproducible | Chao Phraya strong-subsidence cells are mostly not majority observable; the same pattern is also visible in Po and Brantas | The hidden-exposure story is not a single-case artifact | Final polygon/equal-area export package still missing |
| Sign and unit audit | `benchmark_sign_unit_audit_v1.md` | complete for local package | `mm/yr` is frozen; negative means subsidence; Japan and Iran are explicitly lineage extensions, not truth benchmarks | Prevents sign or unit drift in the manuscript | External benchmark closure remains open |
| Blocked / equal-area synthesis | `multi_region_blocked_equal_area_closure_v1` | frozen summary-level closure | Random-effects pooled OR `1.7702`; equal-area proxy OR by cell count `2.2059`; by strong-cell count `3.1161`; I^2 `0.881` | The multi-region signal survives area-weighted blocking and leave-one-out checks | Full cell-level equal-area benchmark still absent |
| Stratified control ladder | `multi_region_stratified_control_closure_v1` | frozen robustness ladder | `landcover_size_stack` pooled OR `1.7903`; LOO MAE `0.2036`; `full_stratified_control_stack` keeps OR `>1` | The claim survives richer landcover/exposure/hidden-share controls | Final manuscript integration still pending |
| Hierarchical comparison | `hierarchical_model_v1` | frozen model-family comparison | `summary_only_meta` `1.7702`; `hierarchical_anchor_stack` `1.9646`; `stratified_control_landcover_size_stack` `1.7903` | The model-family choice is auditable rather than narrative-only | Full all-region cell-level hierarchical fit still absent |
| Transfer validation | `transfer_validation_scores_v1/*` | frozen scope-extension summary | Japan Niigata and Iran nationwide InSAR are both scored as supported lineage extensions; EGMS remains token-blocked | Transfer is a scope-extension argument, not independent truth closure | EGMS/CLMS closure pending token access |
| Risk translation | `multi_region_exposure_closure_v1.csv` + `risk_underestimation_v1.csv` | partially consolidated | Chao Phraya `OR 3.56187`; Indus `3.3894`; Rhone `1.59178`; Rhine `0.810149` | The exposure / risk story is multi-region, not just lead-case | Final cross-region inferential package still needs polishing |

## Region Notes

| region | signal | anchor | key frozen evidence | technical interpretation |
|---|---|---|---|---|
| Po | positive | sparse_gnss_anchor | strong-subsidence fraction `0.892683`; not-majority observable fraction `0.827620`; population not-majority fraction `0.340347`; OR `1.32894` | Positive support, but still conditional on external EGMS closure |
| Chao Phraya | strong_positive | sparse_gnss_anchor | strong-subsidence fraction `0.985119`; not-majority observable fraction `0.706929`; population not-majority fraction `0.175904`; OR `3.56187` | Lead case with the strongest hidden-exposure signal and the strongest frozen anchor |
| Indus | strong_positive | weak_or_missing_gnss_anchor | OR `3.3894`; exposure translation remains strong but the anchor is weak | Strong statistical signal, but the benchmark is not independently closed |
| Rhone | positive | sparse_gnss_anchor | OR `1.59178`; transfer is treated as a conditional upgrade path | Supportive regional signal; candidate for external benchmark upgrade |
| Brantas | positive | weak_or_missing_gnss_anchor | strong-subsidence fraction `0.750758`; not-majority observable fraction `0.466196`; OR `1.59171` | Positive support with weak-anchor sensitivity |
| Rhine | inconclusive | sparse_gnss_anchor | OR `0.810149`; readiness remains `control_or_specification_case` | Control/specification case, not a lead-case reproduction |

## What This Package Demonstrates

1. The observability-failure layer is real and reproducible across the lead case and the screening set.
2. The sign and unit conventions are frozen and traceable.
3. The multi-region signal survives area-weighted blocking and a constrained control ladder.
4. The hierarchical comparison is now auditable rather than narrative-only.
5. Japan and Iran are treated as lineage extensions, not independent truth benchmarks.

## What This Package Does Not Claim

- It does not claim EGMS closure.
- It does not claim a public DOI or repository URL.
- It does not replace a full all-region cell-level hierarchical fit.
- It does not open a new validation split.

## Bottom Line
The current evidence stack is materially stronger than a single-case result: the hidden-exposure pattern survives region-level blocking, richer controls, and frozen transfer logic. The remaining Nature-grade gaps are external benchmark closure, a full all-region cell-level hierarchical fit, and public release metadata.
