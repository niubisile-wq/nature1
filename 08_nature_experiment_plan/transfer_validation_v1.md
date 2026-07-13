# Transfer Validation v1
Date: 2026-07-10

## Purpose
This note consolidates the current transfer evidence for the observability-bias claim across product lineages and regions.

## Evidence Set
- Japan LiCSBAS selective probe: `04_japan_licsbas_probe/japan_licsbas_selected_probe_report.md`
- Iran nationwide InSAR probe: `05_iran_insar_probe/iran_insar_zenodo_probe_report.md`
- Transfer-scope figure: `09_figures_v1/fig6_transfer_scope.*`
- Canonical claim boundary and benchmark framing: `08_nature_experiment_plan/claim_collision_matrix.md`

## What Is Already Established

### Japan
- The Japan Zenodo record can be selectively ingested without downloading the full archive.
- The Niigata sample is present locally and has been parsed into `cum.h5` and `cum_filt.h5`.
- This supports a non-US / non-Europe public deformation-product extension.

### Iran
- The Iran Zenodo companion dataset is present locally as rate, seasonal-amplitude, and mask GeoTIFFs.
- The product is a strict no-token, nationwide processed InSAR layer.
- The local probe confirms the data are usable as a product-lineage extension rather than as an independent truth layer.

### EGMS
- The EGMS rescue query pack exists and is reproducible.
- The no-token route is explicitly blocked at the API level without a CLMS token.

## Transfer Interpretation
- The current evidence supports the claim that the observability-bias framework is not limited to a single geography.
- Japan and Iran are both useful as lineage extensions, but neither should be overclaimed as independent truth benchmarks.
- The transfer story is currently strongest as a scope-extension argument, not as a fully closed cross-product inferential test.

## What Is Still Missing
- A frozen pass/fail rule for train-on-delta / test-on-Japan / test-on-Iran that can be executed once and recorded.
- A leave-one-region-out summary table that is separated from figure narration.
- A final EGMS benchmark run with the required token path, if that path becomes available.

## Frozen Decision Rule

### Training Set

- Chao Phraya
- Brantas
- Po

### Frozen Validation Set

- Rhone
- Rhine
- held-out Chao Phraya spatial blocks

### External Transfer Set

- Japan Niigata
- Iran nationwide InSAR

### Pass Criteria

The transfer claim is considered supported if all of the following are true:

1. The selected candidate stack keeps the same effect direction on the frozen validation set as on the tuning set.
2. The frozen validation set does not invert the main observability-bias claim.
3. Japan and Iran preserve the direction of the product-lineage extension argument, even if the effect size changes.
4. Control/specification cases remain distinct from the lead case.

### Fail Criteria

The transfer claim is considered not supported if any of the following are true:

1. The frozen validation set flips the sign of the main effect.
2. The winning stack only works on the tuning set and collapses on the frozen set.
3. Japan or Iran behave like independent truth benchmarks when they are only product-lineage extensions.
4. Rhine or another control/specification region reproduces the lead-case pattern.

## Current Conclusion
Transfer evidence is present and supportive, but the experiment is only partially closed. The local package can already justify a transfer-scope figure and manuscript discussion, but not yet a fully finalized transfer validation appendix.

## Current Use
- Use this document as the protocol for the next validation run.
- Do not modify the pass/fail rule after opening the frozen validation set.

## Frozen Scores
- `08_nature_experiment_plan/transfer_validation_scores_v1/transfer_validation_scores_v1.csv`
- `08_nature_experiment_plan/transfer_validation_scores_v1/transfer_validation_scores_v1.md`
