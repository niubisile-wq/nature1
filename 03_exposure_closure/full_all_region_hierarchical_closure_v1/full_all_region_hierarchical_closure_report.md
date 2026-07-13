# Full All-Region Hierarchical Closure v1
Date: 2026-07-11

This artifact compiles the frozen hierarchical comparison, the new multi-region exposure translation table, and the technical-validation package into a reviewer-facing closure note.

## Frozen Comparison

| family | pooled OR | 95% CI | loo MAE | loo max abs error | category |
|---|---:|---:|---:|---:|---|
| stratified_control_landcover_size_stack | 1.7903 | 1.5330-2.0909 | 0.2036 | 0.3812 | stratified_control |
| hierarchical_anchor_stack | 1.9646 | 1.1206-3.4444 | 0.6111 | 1.0941 | cell_anchored |
| summary_only_meta | 1.7702 | 1.2119-2.5859 |  |  | summary_only |
| full_all_region_hierarchical_fit | 1.7903 | 1.5330-2.0909 | 0.2036 | 0.3812 | conditional_full_all_region |

## Exposure Translation Anchor

| region | population layer | built-up layer | infrastructure layer | key metric | interpretation |
|---|---|---|---|---|---|
| Po | available | available | not_yet_translated | population_not_majority_observable_fraction=0.340347; built_up_not_majority_observable_fraction=0.460331 | Strong-motion exposure is measurable in people and built-up area, but transport/infrastructure still needs the same treatment. |
| Chao_Phraya | available | available | available | population_not_majority_observable_fraction=0.170; built_up_not_majority_observable_fraction=0.326; transport_hidden_fraction_median=0.531 | Lead-case multi-level exposure translation with materially hidden people, built-up area, and transport infrastructure. |
| Brantas | available | available | not_yet_translated | population_not_majority_observable_fraction=0.145903; built_up_not_majority_observable_fraction=0.175993 | Positive signal survives on population and built-up layers, but infrastructure translation is still missing. |
| Indus | partial_proxy_only | partial_proxy_only | not_yet_translated | risk_proxy=2.3894 | Statistical signal exists, but exposure translation needs a cleaner population/building schema. |
| Rhone | partial_proxy_only | partial_proxy_only | not_yet_translated | risk_proxy=0.591777 | Useful as a conditional upgrade case, but exposure translation is not yet as complete as the lead case. |
| Rhine | proxy_control | proxy_control | not_yet_translated | risk_proxy=-0.189851 | Control/specification case; it should stay in the manuscript as a non-reproducing comparator. |

## Transport Anchor

- transport_hidden_fraction_mean=0.534; transport_hidden_fraction_median=0.531; min=0.303; max=0.699
- Lead-case transport exposure remains materially hidden and therefore belongs in the full all-region closure story.

## Validation Guardrails

- Technical validation source: `08_nature_experiment_plan\multi_region_technical_validation_v1.md`
- Sign/unit audit source: `08_nature_experiment_plan\benchmark_sign_unit_audit_v1.md`
- Protocol source: `08_nature_experiment_plan\full_all_region_hierarchical_closure_v1.md`

## No-Fit Boundary

The current workspace does not contain a harmonized all-region cell-level response matrix for all benchmark regions. Accordingly, this closure remains a frozen synthesis of the available region-level and anchored evidence rather than a new all-region cell-level fit.

## Bottom Line

The full all-region hierarchical closure is now assembled from frozen inputs only. It is still a closure-by-compilation rather than a new validation split, and the no-fit boundary is explicit so the manuscript can defend the strongest honest synthesis without overclaiming a new fit.
