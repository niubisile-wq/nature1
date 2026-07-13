# Chao Phraya area-weighted GHSL exposure censoring

This report transfers GHSL population and built-up totals onto the Chao Phraya VLM grid using exact cell-overlap area weights, then applies LiCSAR coherence observability on the same VLM cells.

## Core Summary

- Frame ID: `062D_07629_131313`
- Coherence threshold: `0.3`
- LiCSAR pairs: `28`
- Valid VLM cells: `18077`
- Covered VLM cells: `18077`

## Exposure Closure

| metric | population | built-up km2 |
|---|---:|---:|
| total | 22499201.1 | 1253.623 |
| strong subsidence | 20644645.9 | 1200.223 |
| strong and not majority observable | 0.0 | 0.000 |
| strong and never observable | 0.0 | 0.000 |

## Visibility Share

- Population weighted mean observability: `0.999`
- Built-up weighted mean observability: `0.999`
- Population not majority observable fraction: `0.000`
- Built-up not majority observable fraction: `0.000`

## Interpretation

- This version is area-weighted at the GHSL-to-VLM transfer step, so it is stronger than the earlier center-sampled closure.
- Observability is still evaluated at VLM-cell centers from the LiCSAR coherence stack.
- The result is intended to support the paper's core claim that exposure underestimation is a product of observability censoring, not just a sampling artifact.
