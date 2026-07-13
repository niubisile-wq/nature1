# Multi-Region Stratified Control Closure v1

This artifact freezes a compact family of region-level control models and checks whether the pooled signal remains > 1 under progressively richer controls.

## Model Family Comparison

| family | reference OR | 95% CI | loo MAE (log OR) | loo max abs error | terms |
|---|---:|---:|---:|---:|---:|
| landcover_size_stack | 1.7903 | 1.5330-2.0909 | 0.2036 | 0.3812 | 9 |
| full_stratified_control_stack | 1.7903 | 1.5330-2.0909 | 0.3336 | 0.6014 | 16 |
| exposure_composition_stack | 1.7903 | 1.5330-2.0909 | 0.4609 | 0.9400 | 7 |
| hidden_stratified_stack | 1.7903 | 1.5330-2.0909 | 0.5480 | 1.3278 | 7 |
| summary_only_meta | 1.7702 | 1.2119-2.5859 | nan | nan | 0 |

## Interpretation

- The comparison is frozen: the candidate families were defined up front from the available region tables.
- The richer control stacks add landcover composition, exposure composition, hidden-share summaries, and the cell-level anchor code.
- If the reference OR stays above 1 across the control stacks, the core lowballing signal is not an artifact of one narrow specification.

## Guardrail

- This is not a search over unlimited model variants.
- It is a constrained robustness ladder intended to strengthen the current Nature-level evidence package.
