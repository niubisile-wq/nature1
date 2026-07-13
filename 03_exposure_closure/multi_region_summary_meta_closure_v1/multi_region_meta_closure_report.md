# Multi-Region Summary Meta-Closure v1

This artifact is a self-contained summary-level closure over the regional benchmark evidence.
It is not a replacement for the full cell-level hierarchical model, but it closes the current region-level evidence layer without missing helper modules.

## Region-Level Evidence

| region | signal | anchor | OR | 95% CI | weight |
|---|---|---|---:|---:|---:|
| Po | positive | sparse_gnss_anchor | 1.3289 | 1.1290-1.5566 | 148.95 |
| Chao Phraya | strong_positive | sparse_gnss_anchor | 3.5619 | 2.2513-5.7808 | 17.28 |
| Indus | strong_positive | weak_or_missing_gnss_anchor | 3.3894 | 2.3290-4.8696 | 28.25 |
| Rhone | positive | sparse_gnss_anchor | 1.5918 | 1.2397-2.0746 | 57.97 |
| Brantas | positive | weak_or_missing_gnss_anchor | 1.5917 | 1.0147-2.6963 | 16.09 |
| Rhine | inconclusive | sparse_gnss_anchor | 0.8101 | 0.5449-1.2662 | 21.62 |

## Meta-Analysis

- Regions: `6`
- Fixed-effect pooled OR: `1.5580`
- Fixed-effect 95% CI: `1.3887-1.7480`
- Random-effect pooled OR: `1.7702`
- Random-effect 95% CI: `1.2119-2.5859`
- Heterogeneity Q: `41.9237`
- Tau^2: `0.188553`
- I^2: `0.881`

## Subgroups

- Lead/positive subgroup pooled OR: `2.0471`
- Sparse-anchor subgroup pooled OR: `1.5401`
- Weak-anchor subgroup pooled OR: `2.3642`
- Control/specification subgroup pooled OR: `0.8101`

## Meta-Regression

| term | beta | se | z | OR | 95% CI |
|---|---:|---:|---:|---:|---:|
| intercept | -0.5185 | 0.6490 | -0.7989 | 0.5954 | 0.1669-2.1246 |
| anchor_code | 0.0525 | 0.3102 | 0.1692 | 1.0539 | 0.5737-1.9359 |
| signal_code | 0.8564 | 0.2167 | 3.9523 | 2.3546 | 1.5398-3.6004 |
| cropland_fraction | -0.4734 | 0.3489 | -1.3565 | 0.6229 | 0.3143-1.2344 |
| built_up_fraction | 0.2857 | 0.6782 | 0.4213 | 1.3307 | 0.3522-5.0277 |
| log1p_ngl_station_count | 0.1088 | 0.1966 | 0.5532 | 1.1149 | 0.7584-1.6390 |

## Leave-One-Out

The leave-one-out table is written to CSV and lets the reader see whether any single region dominates the pooled result.

## Interpretation Guardrail

- This is a summary-level closure over the current regional evidence set.
- It does not replace the cell-level lead-case model already recovered for Chao Phraya.
- It does close the region-level inference layer that was previously only documented narratively.
