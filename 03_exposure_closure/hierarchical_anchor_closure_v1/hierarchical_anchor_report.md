# Hierarchical Anchor Closure v1

This artifact upgrades the multi-region closure by anchoring the Chao Phraya region to the cell-level primary model and pooling it with frozen region-level estimates.

## Chao Phraya Cell-Level Anchor

- Primary strong-subsidence OR: `6.0194`
- 95% CI: `4.5506-7.9623`
- Block-bootstrap median: `5.7988`
- Block-bootstrap 95% interval: `3.5995-10.4431`

## Pooled Results

- Benchmark summary-only random-effects OR: `1.7702`
- Hybrid cell-anchored random-effects OR: `1.9646`
- Blocked equal-area proxy random-effects OR: `1.7702`

## Hybrid Meta-Regression

| term | beta | se | z | OR | 95% CI |
|---|---:|---:|---:|---:|---:|
| intercept | -1.1821 | 1.0271 | -1.1508 | 0.3066 | 0.0410-2.2959 |
| cell_level | 0.6000 | 0.3660 | 1.6393 | 1.8221 | 0.8892-3.7336 |
| signal_code | 0.6462 | 0.1858 | 3.4773 | 1.9082 | 1.3257-2.7467 |
| anchor_code | 0.1569 | 0.2203 | 0.7125 | 1.1699 | 0.7597-1.8016 |
| log1p_n_cells | 0.1107 | 0.1235 | 0.8958 | 1.1170 | 0.8768-1.4230 |

## Leave-One-Out

| left_out_region | observed OR | pooled OR | 95% CI |
|---|---:|---:|---:|
| Po | 1.3289 | 2.1294 | 1.0570-4.2897 |
| Chao Phraya | 3.5619 | 1.5622 | 1.0800-2.2598 |
| Indus | 3.3894 | 1.7632 | 0.9385-3.3125 |
| Rhone | 1.5918 | 2.0478 | 0.9962-4.2093 |
| Brantas | 1.5917 | 2.0424 | 1.0766-3.8747 |
| Rhine | 0.8101 | 2.3302 | 1.2704-4.2741 |

## Sensitivity

| scheme | pooled OR | 95% CI |
|---|---:|---:|
| benchmark_summary_only | 1.7702 | 1.2119-2.5859 |
| hybrid_with_chao_cell_level | 1.9646 | 1.1206-3.4444 |
| blocked_equal_area_proxy | 1.7702 | 1.2119-2.5859 |

## Interpretation Guardrail

- This is a hybrid hierarchical synthesis, not a full Bayesian cell-level model across all regions.
- It makes the cell-level Chao Phraya anchor explicit and freezes the cross-region pooling rule.
- It is intended as the strongest self-contained cross-region synthesis available from the current local evidence.
