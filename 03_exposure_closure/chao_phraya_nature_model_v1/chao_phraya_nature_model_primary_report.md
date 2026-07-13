# Chao Phraya Lead-Case Primary Model
Date: 2026-07-10

## Primary Result

This lead-case model uses the binary censoring outcome:

`not_majority_observable ~ Binomial(1, p)`

with the prespecified spatial adjustment:

`logit(p) ~ strong_sub_5mm + row + col`

### Strong-subsidence effect

- Odds ratio: `6.0194`
- 95% CI: `4.5506-7.9623`
- Block-bootstrap median: `5.7988`
- Block-bootstrap 95% interval: `3.5995-10.4431`

## Interpretation

Strong subsidence cells are substantially more likely to fall into the not-majority-observable regime, which is the direction required by the observability-bias claim.

## Auxiliary Model

The self-contained binomial count model on `observable_count / n_pairs` is retained as an auxiliary diagnostic.
It is useful for checking sensitivity to the response definition, but it is not the primary claim-aligned artifact.

## Why This Is the Right Lead-Case Artifact

- It directly targets the censoring event used in the benchmark summaries.
- It preserves a spatial adjustment without overfitting the lead case into an unreadable feature stack.
- It matches the summary-level evidence that strong cells carry more not-majority-observable exposure.
