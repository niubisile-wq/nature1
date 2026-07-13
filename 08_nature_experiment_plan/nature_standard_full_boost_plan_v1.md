# Nature-Standard Full Boost Plan v1
Date: 2026-07-10

## Executive Decision

Current local package is a strong release candidate for a sub-Nature or data/methods journal, but not yet a Nature-main-standard experiment closure. The limiting gaps are not figure rendering or manuscript assembly. They are:

1. incomplete external benchmark closure;
2. incomplete multi-region equal-area/polygon exposure closure;
3. incomplete final hierarchical or blocked statistical model;
4. incomplete transfer-validation decision rule;
5. no public DOI yet.

The next phase should therefore run two tracks in parallel:

- Track A: close the planned evidence gaps with defensible, prespecified experiments.
- Track B: run a controlled module tournament to discover improved model or data-stack combinations without p-hacking.

The tournament may rotate many modules, but it must not repeatedly optimize on the final validation set. All winning combinations must be re-run once on a frozen held-out set and reported with multiple-comparison correction.

## Non-Negotiable Review Rule

Do not "try until significant" on the same data and then report the winning p-value. That is p-hacking and will not survive Nature-level review.

Allowed version:

- define all candidate modules before the tournament;
- split regions/blocks into training, tuning, and frozen validation sets;
- select winners only on tuning performance;
- open the frozen set once;
- report all tried modules in a tournament ledger;
- use FDR, Bonferroni/Holm, or permutation-based family-wise correction;
- treat failed modules as negative results, not as invisible attempts.

## Target Claim After Full Boost

Primary claim:

Open InSAR product observability is not missing at random; it systematically censors land-subsidence exposure estimates, and the resulting exposure underestimation persists after land-cover, exposure, spatial-block, and product-lineage controls.

Secondary claim:

The censoring is strongest and most policy-relevant in the Chao Phraya lead case, transfers directionally across selected deltas and open product lineages, and is bounded by explicit weak-anchor and no-token limitations.

## Current Baseline Evidence

### Benchmark signal

- Chao Phraya: OR 3.56187, bootstrap interval 2.25134-5.78079, strong positive.
- Indus: OR 3.38940, bootstrap interval 2.32898-4.86955, strong positive, weak independent anchor.
- Po: OR 1.32894, bootstrap interval 1.12900-1.55664, positive, EGMS upgrade needed.
- Rhone: OR 1.59178, bootstrap interval 1.23975-2.07457, positive, EGMS upgrade needed.
- Brantas: OR 1.59171, bootstrap interval 1.01473-2.69633, positive, weak independent anchor.
- Rhine: OR 0.810149, bootstrap interval 0.544942-1.26623, inconclusive control/specification case.

### Exposure closure

- Chao Phraya: 17,808 strong subsidence cells; 20.63 million strong-subsidence population; strong-population fraction 0.917; population not-majority observable fraction 0.176; built-up not-majority observable fraction 0.337; strong-vs-nonstrong not-majority OR 5.780.
- Po: 2,013 strong cells; strong-population fraction 0.620; population not-majority observable fraction 0.340; built-up not-majority observable fraction 0.460; OR 2.603.
- Brantas: 991 strong cells; strong-population fraction 0.580; population not-majority observable fraction 0.146; built-up not-majority observable fraction 0.176; OR 2.459.
- Chao Phraya OSM transport: 28 pair-level estimates; hidden strong-subsidence transport fraction range 0.303-0.699, mean 0.534.

### Robustness

- Chao Phraya robustness grid has 27 tested combinations.
- OR range: 0.468-6.601.
- OR > 1 in 21/27 rows.
- Bootstrap q025 < 1 in 7/27 rows.

## Phase 1: Close Existing Planned Gaps

### E2: Multi-Region Observability Mask Closure

Goal:

Produce reviewer-reusable observability masks for all regions, not only Chao Phraya.

Required outputs:

- `observability_masks_multi_region_v1.csv`
- one georeferenced mask package per region;
- mask dictionary with band definitions;
- threshold sensitivity table for coherence or observability thresholds 0.2, 0.3, 0.4;
- temporal-density masks: any observable, majority observable, stable-75, obs < 0.25, never observable.

Acceptance gate:

- every region used in a main result has a mask file and source table;
- mask thresholds are prespecified;
- Chao Phraya result remains directionally positive across the prespecified thresholds;
- weak regions are explicitly labeled instead of forced into a main claim.

Priority:

1. Chao Phraya already done; audit and freeze as lead.
2. Po and Brantas from existing exposure closure.
3. Rhone and Rhine to strengthen positive-control and negative/specification-control contrast.
4. Indus only if anchor status is clearly stated.

### E3: Benchmark Deformation Layer Closure

Goal:

Each deformation benchmark must have sign, unit, projection, resolution, provenance, and independent-anchor status audited.

Required outputs:

- `benchmark_deformation_layers_v1.csv`
- `benchmark_sign_unit_audit_v1.md`
- one short audit section for delta VLM, Japan LiCSBAS, Iran InSAR, EGMS DOI-only line, and NGL GNSS.

Acceptance gate:

- no product is treated as independent truth unless it really is independent;
- Japan and Iran are labeled product-lineage extensions;
- Po/Rhone/Rhine EGMS remains an upgrade path unless actual EGMS files are downloaded;
- DOI-only EGMS citation is not represented as completed EGMS validation.

### E4: Equal-Area / Polygon Exposure Overlay Closure

Goal:

Move from center-sampled exposure to area-weighted or polygon-intersection exposure for all lead regions.

Required outputs:

- `multi_region_area_weighted_exposure_v1.csv`
- `multi_region_exposure_uncertainty_v1.csv`
- `exposure_overlay_methods_v1.md`

Exposure layers:

- GHSL population;
- GHSL built-up;
- OSM major roads;
- OSM railways;
- WorldCover cropland;
- optional irrigation proxy.

Acceptance gate:

- Chao Phraya has population, built-up, roads, rail, cropland;
- Po and Brantas have population and built-up at minimum;
- Rhone/Rhine have at least population and built-up if retained in main figure;
- exposure uncertainty includes alignment/resolution sensitivity;
- visible-only versus complete-coverage counterfactual is reported for each lead layer.

### E5: Final Statistical Model Closure

Goal:

Produce one final statistical model family that can be defended as the paper's inferential backbone.

Minimum model:

`failure ~ strong_deformation + landcover + exposure_z + region + product_lineage + temporal_density + strong_deformation:landcover + strong_deformation:region`

Required model families:

- binomial logistic with spatial-block bootstrap;
- beta-binomial or quasi-binomial overdispersion check;
- leave-one-region-out validation;
- region-blocked permutation null;
- simple transparent baseline model for interpretability.

Required outputs:

- `hierarchical_model_v1_results.csv`
- `hierarchical_model_v1_coefficients.csv`
- `hierarchical_model_v1_diagnostics.md`
- `leave_one_region_out_v1.csv`
- `spatial_block_permutation_v1.csv`

Acceptance gate:

- main strong-deformation coefficient remains positive in the final prespecified model;
- Chao Phraya lead effect remains positive after controls;
- negative/specification control does not falsely produce the same claim;
- confidence intervals and uncertainty are shown, not only point estimates;
- model diagnostics report overdispersion, spatial autocorrelation risk, and sensitivity to block size.

### E6: Risk Underestimation Closure

Goal:

Translate observability failure into a reviewer-readable risk-underestimation metric.

Core metrics:

- visible-only exposure;
- complete strong-deformation exposure;
- hidden strong-deformation exposure;
- risk underestimation factor;
- hidden exposure share;
- exposure-weighted observability.

Required outputs:

- `risk_underestimation_multi_region_v1.csv`
- `risk_underestimation_ci_v1.csv`
- `risk_underestimation_methods_v1.md`

Acceptance gate:

- Chao Phraya has a policy-relevant hidden exposure result with uncertainty;
- the metric is reproduced for at least two non-lead regions;
- weak-anchor regions are reported as sensitivity rather than proof.

### E7: Transfer Validation Closure

Goal:

Make transfer testing honest: demonstrate transfer where it exists and bound it where it fails.

Transfer designs:

- train on Chao Phraya + Po + Brantas, test on Rhone/Rhine;
- train on delta VLM products, test on Japan LiCSBAS product-lineage extension;
- compare Iran InSAR mask/rate behavior as a no-token arid-groundwater extension;
- leave-one-region-out across all available regions.

Required outputs:

- `transfer_validation_decision_rule_v1.md`
- `transfer_validation_scores_v1.csv`
- `product_lineage_transfer_v1.csv`

Acceptance gate:

- decision rule is frozen before opening final validation scores;
- performance is directional and interpretable, not just significant;
- product-lineage extensions are not mislabeled as independent truth.

### E8: Mechanism and Control Closure

Goal:

Rule out the simplest reviewer objection: "this is only land cover or water/wetland masking."

Control blocks:

- WorldCover class;
- built-up fraction;
- cropland fraction;
- water/wetland/mangrove fraction;
- slope/DEM if available;
- population density;
- temporal sampling density;
- product lineage;
- region fixed or random effects.

Required outputs:

- `mechanism_control_table_v2.csv`
- `landcover_stratified_effects_v1.csv`
- `negative_control_summary_v1.md`

Acceptance gate:

- strong-deformation effect remains positive within at least the main land-cover strata or the paper is reframed as product-land-cover censoring;
- Rhine or another control/specification case does not support an overgeneralized claim;
- effect heterogeneity is reported, not hidden.

### E11: DOI and FAIR Release Closure

Goal:

Turn the local release candidate into a public, citable source-data package.

Required outputs:

- Zenodo/Dryad/OSF DOI;
- release README;
- data dictionary;
- source-data inventory;
- code manifest;
- checksums;
- clear license;
- Data Availability statement.

Acceptance gate:

- every central claim maps to one public file;
- every figure panel has source data;
- DOI is included in manuscript and repository release notes;
- no secrets, tokens, or private credentials are included.

## Phase 2: Controlled Module Tournament

## Purpose

Find a genuinely stronger module stack without inflating significance by repeated untracked trials.

The tournament optimizes robustness, transfer, and effect stability, not only nominal p-values.

## Frozen Data Partitions

Use three partitions:

- Discovery set: module development and debugging.
- Tuning set: model selection and module ranking.
- Frozen validation set: opened once after choosing the final stack.

Recommended first split:

- Discovery: Chao Phraya blocks plus Brantas.
- Tuning: Po plus selected Chao Phraya held-out spatial blocks.
- Frozen validation: Rhone/Rhine and held-out Chao Phraya spatial blocks.

If EGMS data later becomes available:

- EGMS Po/Rhone/Rhine becomes the highest-value frozen external validation set.

## Tournament Ledger

Every module run must write one row to:

- `module_tournament_ledger_v1.csv`

Required fields:

- run_id;
- timestamp;
- code commit or script hash;
- data manifest hash;
- candidate stack;
- train regions;
- tuning regions;
- frozen validation used: yes/no;
- primary metric;
- secondary metrics;
- uncorrected p-values;
- corrected p-values;
- failure reason if rejected.

## Candidate Module Families

### A. Observability Module

Candidate variants:

- coherence threshold: 0.2, 0.3, 0.4;
- observability rule: any, majority, stable-75, obs < 0.25, never;
- temporal window: all pairs, seasonal subsets, early/late period;
- spatial aggregation: native grid, 500 m, 1 km, 2 km;
- missingness rule: conservative, balanced, permissive.

Ranking metrics:

- effect direction stability;
- hidden-exposure share;
- transfer score;
- false-positive behavior in control/specification region.

### B. Deformation Module

Candidate variants:

- strong threshold: 3, 5, 10 mm/yr;
- signed subsidence only versus absolute motion;
- continuous VLM magnitude;
- quantile-defined strong-deformation class;
- GNSS-anchored sanity subset;
- product-lineage-specific threshold.

Ranking metrics:

- coefficient stability;
- exposure relevance;
- agreement with independent or semi-independent anchors;
- sensitivity to sign/unit assumptions.

### C. Exposure Module

Candidate variants:

- population;
- built-up;
- roads;
- railways;
- cropland;
- irrigation proxy;
- combined exposure index;
- exposure-weighted observability.

Ranking metrics:

- policy relevance;
- hidden exposure share;
- reproducibility;
- cross-region availability.

### D. Control Module

Candidate variants:

- WorldCover only;
- WorldCover + population density;
- WorldCover + built-up;
- WorldCover + temporal density;
- WorldCover + region fixed effects;
- region random intercept;
- product-lineage interaction;
- land-cover-stratified models.

Ranking metrics:

- reduced confounding;
- interpretability;
- coefficient stability;
- AIC/BIC or cross-validated log loss;
- no overfitting on control cases.

### E. Spatial Module

Candidate variants:

- no block;
- 5-cell block;
- 10-cell block;
- 25-cell block;
- AOI-level bootstrap;
- spatial permutation;
- leave-cluster-out validation.

Ranking metrics:

- uncertainty calibration;
- robustness under spatial autocorrelation;
- conservative confidence intervals.

### F. Transfer Module

Candidate variants:

- leave-one-region-out;
- train-deltas-test-Japan;
- train-wet-deltas-test-Iran;
- train-high-exposure-test-low-exposure;
- product-lineage split.

Ranking metrics:

- directional accuracy;
- calibration;
- external validity;
- honest failure diagnosis.

## Primary Tournament Score

Use a composite score instead of only p-value:

`score = 0.35 * effect_stability + 0.25 * hidden_exposure_relevance + 0.20 * transfer_score + 0.10 * control_specificity + 0.10 * reproducibility_score`

Definitions:

- effect_stability: same positive direction across thresholds, blocks, and leave-one-region-out.
- hidden_exposure_relevance: hidden exposure share and affected population/built-up/transport magnitude.
- transfer_score: directional success on tuning transfer set.
- control_specificity: does not produce the same claim in Rhine/control cases.
- reproducibility_score: all source files, scripts, and hashes exist.

## Statistical Guardrails

Required corrections:

- Benjamini-Hochberg FDR for families of related module tests;
- Holm correction for final small set of confirmatory hypotheses;
- permutation-based family-wise correction for the final model if many stacks are tried.

Required final reporting:

- total number of candidate stacks tried;
- number of rejected stacks;
- final stack selection criterion;
- uncorrected and corrected p-values;
- frozen validation result;
- all negative or null results in supplementary tables.

## Phase 3: Figure and Manuscript Upgrade

### Main Figures After Full Boost

Figure 1:

Concept and dataset map: open InSAR observability bias, regions, product lineages, and evidence hierarchy.

Figure 2:

Chao Phraya lead case: strong subsidence, observability failure, and exposure censoring.

Figure 3:

Final model: controlled effect estimates, spatial-block uncertainty, leave-one-region-out validation.

Figure 4:

Risk translation: visible-only versus complete strong-deformation exposure for population, built-up, roads, rail, cropland.

Figure 5:

Mechanism controls and negative/specification cases: land cover, exposure, product lineage, Rhine/control.

Figure 6:

Transfer and generality: Japan/Iran product-lineage extensions, Po/Rhone/Brantas/Indus scope, EGMS upgrade path.

Extended Data:

- threshold sensitivity;
- sign/unit audits;
- source data manifest;
- model diagnostics;
- module tournament ledger;
- negative/null modules.

## Phase 4: Decision Gates

### Nature-main go/no-go

Go only if all conditions hold:

- external benchmark closure exists, preferably EGMS or equivalent;
- final model survives land-cover, exposure, region, product, and spatial controls;
- risk underestimation is shown in multiple regions or one lead plus strong external validation;
- transfer validation has prespecified success criteria;
- public DOI exists;
- source data and scripts are reproducible.

If these conditions are not met, do not frame as Nature-main complete.

### Nature Communications / ESSD / Scientific Data go/no-go

Go if:

- DOI exists;
- source data package is complete;
- Chao Phraya lead case is strong;
- multi-region support is transparent and not overclaimed;
- EGMS is presented as an official upgrade path rather than a completed result.

## Immediate Next Actions

1. User creates DOI for the current local release candidate.
2. Update all manuscript and release files with DOI.
3. Generate `module_tournament_ledger_v1.csv` and freeze module candidate list.
4. Build multi-region equal-area exposure overlays.
5. Run final blocked/hierarchical model family.
6. Run controlled tournament on discovery/tuning sets.
7. Open frozen validation once.
8. Rebuild figures and submission package.

## First 72-Hour Execution Plan

Day 1:

- freeze DOI package and source-data inventory;
- create tournament ledger;
- define final validation split;
- finish benchmark sign/unit audit v1.

Day 2:

- build multi-region area-weighted exposure tables;
- extend observability masks beyond Chao Phraya where data permits;
- implement visible-only versus complete-exposure counterfactual.

Day 3:

- run blocked/binomial baseline model;
- run first controlled module tournament batch;
- write decision report identifying winners, losers, and remaining blockers.

## Bottom Line

The right next move is not blind significance chasing. The right move is a controlled, logged module tournament layered on top of a completed DOI/source-data release and the missing multi-region/model/transfer closures. This can produce a stronger paper without creating an invalid inference trail.
