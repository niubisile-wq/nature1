# Hierarchical Model Comparison v1

This artifact compares the current region-level meta-analysis against a frozen cell-anchored hierarchical stack.

## Model Family Comparison

| model | pooled OR | 95% CI | loo MAE (log OR) | loo max abs error |
|---|---:|---:|---:|---:|
| summary_only_meta | 1.7702 | 1.2119-2.5859 | nan | nan |
| hierarchical_anchor_stack | 1.9646 | 1.1206-3.4444 | 0.6111 | 1.0941 |
| stratified_control_landcover_size_stack | 1.7903 | 1.5330-2.0909 | 0.2036 | 0.3812 |

## Hierarchical Coefficients

| term | beta | se | z | OR | 95% CI |
|---|---:|---:|---:|---:|---:|
| intercept | -1.1819 | 1.0271 | -1.1507 | 0.3067 | 0.0410-2.2962 |
| signal_code | 0.6461 | 0.1858 | 3.4772 | 1.9082 | 1.3257-2.7466 |
| anchor_code | 0.1570 | 0.2203 | 0.7127 | 1.1700 | 0.7598-1.8016 |
| n_cells_log | 0.1106 | 0.1235 | 0.8956 | 1.1170 | 0.8768-1.4230 |
| cell_level | 0.0754 | 0.4141 | 0.1820 | 1.0783 | 0.4789-2.4277 |

## Interpretation Guardrail

- This is a frozen comparison, not a search over arbitrarily many model families.
- The model uses the existing cell-level Chao Phraya anchor plus the regional benchmark covariates.
- It improves the E5 layer by making the model-family decision auditable rather than purely narrative.
