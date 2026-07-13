# Chao Phraya Nature-Standard Lead-Case Model v1

This is a self-contained binomial logistic model built directly from the lead-case cell table, without external helper modules.

## Model

`observable_count ~ Binomial(n_pairs, p)`

`logit(p) ~ strong_sub_5mm + log1p(population_weighted) + log1p(builtup_m2_weighted) + row + col + strong:population + strong:builtup`

- Cells: `18077`
- Spatial block size: `5`
- Blocks: `797`
- Bootstrap replicates: `200`
- Converged: `True` in `8` iterations

## Main Coefficients

| term | OR | 95% CI | bootstrap median | bootstrap 95% interval |
|---|---:|---:|---:|---:|
| strong_sub_5mm | 1.4754 | 1.2527-1.7378 | 1.4638 | 0.7193-7.2320 |
| log1p_population_weighted_z | 1.9617 | 1.6195-2.3762 | 1.9060 | 0.4991-6.8602 |
| log1p_builtup_m2_weighted_z | 12.8168 | 8.8738-18.5117 | 13.1215 | 1.2216-503.5279 |

## Leave-One-Block-Out

- Block leave-one-out rows: `797`
- Bootstrap failures: `0`

## Region Context

- Chao Phraya summary OR: `5.779728413225441`
- Po summary OR: `2.603371017471737`

## Interpretation Guardrail

- This model is a lead-case model, not the final multi-region hierarchical closure.
- It is stronger than a hand-waved narrative because it is a real fit on cell-level data with block bootstrap.
- The final Nature-level model still needs the missing helper-module stack or an equivalent multi-region self-contained rewrite.

## Binary Sensitivity Model

`not_majority_observable ~ Binomial(1, p)`

`logit(p) ~ strong_sub_5mm + row + col`

- strong OR: `6.0194`
- strong 95% CI: `4.5506-7.9623`
- bootstrap median: `5.9320`
- bootstrap 95% interval: `3.6018-11.2822`
