# Full All-Region Hierarchical Closure v1
Date: 2026-07-11

## Purpose
This protocol freezes the next upgrade target suggested by the latest Nature-family comparator scan: a full all-region hierarchical closure that is still prespecified, auditable, and limited to the current frozen evidence stack.

## Why This Is The Right Next Step
The current package already has:
- a lead-case cell-level anchor,
- a blocked/equal-area region-level synthesis,
- a frozen multi-stratum control ladder,
- and a consolidated technical-validation package.

What it still lacks is the final all-region hierarchical fit that a Nature-style reviewer would treat as the top-level evidence closure.

The newest comparator scout also reinforces that this closure should stay tied to the decision-facing exposure matrix and the socioeconomic gradient comparison, because recent Nature-family papers are increasingly framing the main table as a combined exposure + vulnerability + decision-readiness object rather than a single-model result.

## Frozen Candidate Family

The candidate families are fixed in advance and must not be expanded after the next run starts:

1. `summary_only_meta`
2. `blocked_equal_area_synthesis`
3. `hierarchical_anchor_stack`
4. `stratified_control_landcover_size_stack`
5. `full_all_region_hierarchical_fit` if and only if it can be built from the frozen current inputs without opening a new validation split

## Required Inputs
- `03_exposure_closure/multi_region_summary_meta_closure_v1/*`
- `03_exposure_closure/multi_region_blocked_equal_area_closure_v1/*`
- `03_exposure_closure/hierarchical_anchor_closure_v1/*`
- `03_exposure_closure/multi_region_stratified_control_closure_v1/*`
- `08_nature_experiment_plan/multi_region_technical_validation_v1.md`
- `08_nature_experiment_plan/frozen_validation_split_v1.csv`
- `08_nature_experiment_plan/benchmark_sign_unit_audit_v1.md`
- `08_nature_experiment_plan/decision_facing_exposure_matrix_v1.md`
- `08_nature_experiment_plan/socioeconomic_layer_gradient_comparison_v1.md`

## Prespecified Metrics

The next closure should report the following for every candidate family:

- pooled OR
- 95% CI
- leave-one-out MAE on log OR
- leave-one-out max absolute error
- region-specific residuals
- a short note on whether the family is lead-case anchored, region-level only, or fully all-region

## Stop Rules

The next run must stop and be reported as incomplete if any of the following happens:

1. The candidate family list needs to be expanded after seeing the result.
2. A new validation split would need to be opened.
3. The full model relies on missing helper modules rather than frozen evidence.
4. The result cannot be expressed as a fixed comparison against the already-frozen families.

## Success Criteria

The upgrade is successful only if:

1. The all-region hierarchical family is computed from frozen inputs.
2. The family comparison remains prespecified and auditable.
3. The final result is clearly stronger than the summary-only baseline or, if not, that lack of improvement is explicitly reported.
4. The new closure can be folded into the manuscript evidence stack without changing the release story.

## Reporting Rule

If the full all-region hierarchical fit cannot be obtained without violating the stop rules, the correct output is not to invent a better model. The correct output is to keep the current frozen ladder, report the limitation, and move the external benchmark work forward separately.

## Bottom Line
The next Nature-grade gain should come from a fixed all-region hierarchical closure, not from continued tournament expansion. This protocol keeps that next step prespecified and honest.
