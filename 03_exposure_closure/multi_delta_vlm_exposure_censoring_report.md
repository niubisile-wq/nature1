# Multi-delta VLM-grid exposure censoring

This report places Nature 2026 VLM, LiCSAR observability, GHSL population, and GHSL built-up on the VLM grid.

## Strong-Subsidence Exposure Closure

| delta | strong cells | strong pop | pop not majority | pop not stable-75 | strong built-up km2 | built-up not majority | built-up not stable-75 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Po | 2013 | 67711 | 0.340 | 0.500 | 18.432 | 0.460 | 0.638 |
| Chao Phraya | 17808 | 20630705 | 0.176 | 0.247 | 1200.223 | 0.337 | 0.431 |
| Brantas | 991 | 3238571 | 0.146 | 0.192 | 122.085 | 0.176 | 0.230 |

## Strong-vs-Nonstrong Cell Test

| delta | strong not majority | nonstrong not majority | odds ratio |
|---|---:|---:|---:|
| Po | 0.828 | 0.649 | 2.603 |
| Chao Phraya | 0.707 | 0.294 | 5.780 |
| Brantas | 0.466 | 0.261 | 2.459 |

## Interpretation

- This is a same-grid exposure closure, not just a frame-level exposure observability summary.
- Population and built-up weights are sampled from GHSL at VLM grid-cell centers; this is stronger than separate frame-level summaries but still not a polygon area-weighted overlay.
- The odds ratio is a screening statistic, not a spatially autocorrelation-corrected inferential model.
