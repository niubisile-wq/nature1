# Multi-Region Exposure Translation v1
Date: 2026-07-11

## Purpose
This note converts the current exposure evidence into a reviewer-facing multi-level translation table. It follows the Nature-family pattern that subsidence claims should be expressed not only as rates, but as people, built-up area, and infrastructure exposure.

## Frozen Inputs
- `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/chao_phraya_area_weighted_exposure_summary.csv`
- `03_exposure_closure/chao_phraya_osm_exposure_censoring/chao_phraya_osm_exposure_censoring_summary.csv`
- `08_nature_experiment_plan/multi_region_exposure_closure_v1.csv`
- `08_nature_experiment_plan/risk_underestimation_v1.csv`
- `08_nature_experiment_plan/benchmark_sign_unit_audit_v1.md`
- `08_nature_experiment_plan/multi_region_technical_validation_v1.md`

## Exposure Translation Table

| region | population layer | built-up layer | infrastructure layer | key exposure metric | interpretation |
|---|---|---|---|---|---|
| Po | available | available | not yet translated | population not-majority observable fraction `0.340347`; built-up not-majority observable fraction `0.460331` | Strong-motion exposure is already measurable in people and built-up area, but transport/infrastructure still needs the same treatment. |
| Chao Phraya | available | available | available | population not-majority observable fraction `0.170`; built-up not-majority observable fraction `0.326`; transport hidden fraction median `0.531` | This is the lead-case multi-level exposure translation: people, built-up area, and transport infrastructure all remain materially hidden by observability censoring. |
| Brantas | available | available | not yet translated | population not-majority observable fraction `0.145903`; built-up not-majority observable fraction `0.175993` | The positive signal survives on the population and built-up layers, but infrastructure translation is still missing. |
| Indus | partial / proxy only | partial / proxy only | not yet translated | risk proxy `2.3894` | Statistical signal exists, but the exposure translation needs a cleaner population/building schema before it can be treated as manuscript-grade. |
| Rhone | partial / proxy only | partial / proxy only | not yet translated | risk proxy `0.591777` | Useful as a conditional upgrade case, but exposure translation is not yet as complete as the lead case. |
| Rhine | proxy / control | proxy / control | not yet translated | risk proxy `-0.189851` | Control/specification case; it should stay in the manuscript as a non-reproducing comparator. |

## Transport Summary For Chao Phraya

- Overpass endpoint: `https://overpass-api.de/api/interpreter`
- Major road ways: `17457`
- Railway ways: `1353`
- Segments tested / used: `288588 / 166367`
- Hidden transport fraction across `transport_total` pairs:
  - mean `0.534`
  - median `0.531`
  - min `0.303`
  - max `0.699`

## Why This Matters

Nature-family comparators now repeatedly translate subsidence into human and infrastructure exposure, not just deformation rates. This table makes the current stack match that expectation more closely:

1. The lead case now carries people, built-up area, and transport infrastructure.
2. The cross-region table keeps the strongest regions visible while explicitly marking where infrastructure translation is still incomplete.
3. The control case remains a control, not a forced positive.

## What Remains To Close

- Add a cleaner infrastructure layer for the non-lead regions where available.
- Expand the exposure schema into a single manuscript-ready table with consistent units.
- Keep the lead/transfer/control labels separate from the exposure translation itself.
