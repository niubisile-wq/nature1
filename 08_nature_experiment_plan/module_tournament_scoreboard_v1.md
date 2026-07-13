# Frozen Module Tournament Scoreboard v1

This scoreboard is computed only from already frozen outputs and does not open any new validation split.

## Ranking

| rank | stack | pooled OR | loo min OR | loo > 1 | effect stability | hidden exposure | transfer score | composite |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | hybrid_cell_anchored | 1.9646 | 1.5622 | 1.000 | 0.982 | 0.631 | 0.795 | 0.861 |
| 2 | summary_only | 1.7702 | 1.5450 | 1.000 | 0.885 | 0.631 | 0.873 | 0.842 |
| 3 | blocked_equal_area | 1.7702 | 1.3280 | 1.000 | 0.885 | 0.631 | 0.750 | 0.817 |

## Guardrails

- The ranking is a deterministic summary of frozen outputs, not a fresh hyperparameter search.
- It does not open the frozen validation set for new fitting.
- The single-figure take-away is that the hybrid cell-anchored stack is the strongest of the currently frozen cross-region syntheses.
