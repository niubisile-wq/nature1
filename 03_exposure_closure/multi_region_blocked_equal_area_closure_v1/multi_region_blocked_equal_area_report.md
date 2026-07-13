# Multi-Region Blocked Equal-Area Closure v1

This artifact is a self-contained region-level blocked synthesis that upgrades the current multi-region evidence layer.
It combines regional benchmark ORs, area-weighted exposure summaries, and frozen leave-one-region-out validation.

## Region-Level Inputs

| region | signal | anchor | OR | 95% CI | n_cells | strong_cells | readiness |
|---|---|---|---:|---:|---:|---:|---|
| Po | positive | sparse_gnss_anchor | 1.3289 | 1.1290-1.5566 | 2255 | 2013 | conditional_nature_go_after_egms |
| Chao Phraya | strong_positive | sparse_gnss_anchor | 3.5619 | 2.2513-5.7808 | 18077 | 17808 | benchmark_v0_landed_needs_dense_truth |
| Indus | strong_positive | weak_or_missing_gnss_anchor | 3.3894 | 2.3290-4.8696 | 7087 |  | statistical_signal_needs_independent_anchor |
| Rhone | positive | sparse_gnss_anchor | 1.5918 | 1.2397-2.0746 | 3392 |  | conditional_nature_go_after_egms |
| Brantas | positive | weak_or_missing_gnss_anchor | 1.5917 | 1.0147-2.6963 | 1320 | 991 | statistical_signal_needs_independent_anchor |
| Rhine | inconclusive | sparse_gnss_anchor | 0.8101 | 0.5449-1.2662 | 9011 |  | control_or_specification_case |

## Core Synthesis

- Random-effects pooled OR: `1.7702`
- Random-effects 95% CI: `1.2119-2.5859`
- Heterogeneity I^2: `0.881`
- Equal-area proxy OR by cell count: `2.2059`
- Equal-area proxy OR by strong-cell count: `3.1161`
- Population-weighted signal proxy OR: `2.1404`

## Blocked Meta-Regression

| term | beta | se | z | OR | 95% CI |
|---|---:|---:|---:|---:|---:|
| intercept | 0.5696 | 0.0730 | 7.8031 | 1.7676 | 1.5320-2.0395 |
| signal_code_z | 0.4374 | 0.1003 | 4.3616 | 1.5486 | 1.2723-1.8849 |
| anchor_code_z | 0.0711 | 0.0867 | 0.8197 | 1.0737 | 0.9059-1.2725 |
| log1p_cells_z | 0.1120 | 0.0825 | 1.3581 | 1.1185 | 0.9516-1.3148 |

## Leave-One-Out Blocked Validation

| left_out_region | observed OR | predicted OR | predicted 95% CI | residual log OR |
|---|---:|---:|---:|---:|
| Po | 1.3289 | 1.5745 | 1.1465-2.1624 | -0.1696 |
| Chao Phraya | 3.5619 | 3.3033 | 1.7062-6.3953 | 0.0754 |
| Indus | 3.3894 | 4.0623 | 2.1088-7.8255 | -0.1811 |
| Rhone | 1.5918 | 1.4056 | 1.2178-1.6224 | 0.1244 |
| Brantas | 1.5917 | 1.3280 | 0.7496-2.3529 | 0.1811 |
| Rhine | 0.8101 | 2.4414 | 0.2505-23.7969 | -1.1031 |

## Blocked Split View

| split | n_regions | pooled OR |
|---|---:|---:|
| signal_positive | 5 | 2.0471 |
| control_specification | 1 | 0.8101 |
| sparse_anchor | 4 | 1.5401 |
| weak_anchor | 2 | 2.3642 |

## Interpretation Guardrail

- This is a summary-level blocked/equal-area closure, not a replacement for a full cell-level hierarchical model.
- It does tighten the current multi-region package by making the region-size and validation structure explicit.
- The remaining Nature-grade gap is the cell-level equal-area benchmark and external EGMS closure.
