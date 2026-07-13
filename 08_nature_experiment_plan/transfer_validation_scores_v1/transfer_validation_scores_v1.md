# Transfer Validation Scores v1

This artifact freezes the current transfer evidence without opening any new validation split.

## Frozen Decision Rule

A transfer target is marked supported only when the evidence shows a readable, reproducible lineage extension and does not claim independent truth.

## Score Table

| scope | target | status | readable | directional support | independent truth | token required | notes |
|---|---|---|---:|---:|---:|---:|---|
| regional_benchmark | Po | supported | 1 | 1 | 0 | 1 | conditional_nature_go_after_egms |
| regional_benchmark | Chao Phraya | partial | 1 | 0 | 0 | 0 | benchmark_v0_landed_needs_dense_truth |
| regional_benchmark | Indus | partial | 1 | 0 | 0 | 0 | statistical_signal_needs_independent_anchor |
| regional_benchmark | Rhone | supported | 1 | 1 | 0 | 1 | conditional_nature_go_after_egms |
| regional_benchmark | Brantas | partial | 1 | 0 | 0 | 0 | statistical_signal_needs_independent_anchor |
| regional_benchmark | Rhine | control | 1 | 0 | 0 | 1 | control_or_specification_case |
| external_transfer | Japan Niigata | supported | 1 | 1 | 0 | 0 | n_time_steps=111; fraction_lt_minus_5=0.188 |
| external_transfer | Iran nationwide InSAR | supported | 1 | 1 | 0 | 0 | rate_median=1.800; mask_median=0.0 |

## Summary

- Frozen transfer support score: `0.500`
- Japan is scored as a public product-lineage extension after selective ingest, not independent truth.
- Iran is scored as a no-token processed InSAR extension, not independent truth.
- EGMS remains token-blocked, so no new external truth benchmark is claimed.

## Guardrail

- This is a frozen validation summary, not a fresh hyperparameter search.
- It supports the manuscript's scope-extension language while keeping the Nature-grade boundary explicit.
