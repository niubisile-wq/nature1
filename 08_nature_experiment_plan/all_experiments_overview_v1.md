# All Experiments Overview v1
Date: 2026-07-11

## Purpose
This note gives a single-page view of the current experiment stack, the strongest completed evidence, and the remaining Nature-level gaps.

## High-Level Status

| Layer | Artifact / question | Status | Main evidence |
|---|---|---|---|
| E0 | Claim collision audit | complete | `claim_collision_matrix.md` |
| E1 | Dataset inventory | complete | `dataset_inventory_v1.csv`, `dataset_manifest.json` |
| E2 | Observability / failure layer | partial | `observability_masks_v1.md`, `observability_masks_v1.csv`, reconstructed mask raster, consolidated multi-region technical validation package |
| E3 | Benchmark deformation layers | partial | Japan LiCSBAS probe, Iran InSAR probe, deformation-layer audit scaffold, frozen sign/unit package |
| E4 | Area-weighted exposure overlay | partial | `area_weighted_exposure_v1.csv`, Chao Phraya exposure closure, multi-region summary closure, blocked/equal-area synthesis, final equal-area closure package, multi-region exposure translation package, infrastructure translation package, decision-facing exposure matrix, release-gap memo, manuscript-ready package |
| E5 | Statistical core model | partial | lead-case self-contained model, multi-region summary meta-closure, blocked/equal-area synthesis, hybrid hierarchical anchor synthesis, multi-stratum control ladder, hierarchical comparison with stratified controls, closure-by-compilation all-region package, explicit no-fit justification |
| E6 | Risk underestimation | partial | risk table and closure summaries exist, not yet fully consolidated across all regions |
| E7 | Transfer validation | partial | Japan/Iran probe evidence, frozen decision rule, frozen transfer scores, and the technical-validation package; EGMS closure still open |
| E8 | Mechanism controls | partial | `mechanism_control_table_v1.csv`, Figure 5 control story, stratified control ladder, technical-validation package |
| E9 | Robustness / sensitivity | complete | Chao Phraya robustness grid and bootstrap outputs (`fig4_chao_phraya_robustness_grid.*`) |
| E10 | Figures / source data | complete | Fig. 1-7, manuscript draft, source-data mirrors |
| E11 | Repository release / DOI | partial | local release candidate exists, DOI-ready metadata exists, public DOI still pending |

## What Is Already Strong

### 1. Lead-case closure
- Chao Phraya self-contained model is in place.
- Primary binary censoring model:
  - `not_majority_observable ~ Binomial(1, p)`
  - `logit(p) ~ strong_sub_5mm + row + col`
- Reported strong-subsidence effect is large and stable across bootstrap and block splits.
- Output:
  - `03_exposure_closure/chao_phraya_nature_model_v1/chao_phraya_nature_model_primary_report.md`

### 2. Multi-region summary closure
- Region-level random-effects meta-analysis and meta-regression exist.
- Leave-one-out analysis keeps the pooled OR above 1 across regions.
- Output:
  - `03_exposure_closure/multi_region_summary_meta_closure_v1/`

### 3. Blocked / equal-area synthesis
- A second region-level synthesis now freezes the area-weighted and leave-one-out structure more explicitly.
- The ridge meta-regression is stable under standardized predictors.
- Output:
  - `03_exposure_closure/multi_region_blocked_equal_area_closure_v1/`

### 4. Hybrid hierarchical anchor
- The Chao Phraya region is now anchored to the cell-level primary model and pooled with the regional benchmark set.
- The hybrid pooled OR is higher than the summary-only meta-analysis and remains >1 in leave-one-out checks.
- Output:
  - `03_exposure_closure/hierarchical_anchor_closure_v1/`

### 5. Frozen multi-stratum control ladder
- A dedicated control ladder now checks whether the pooled signal remains > 1 after adding landcover composition, exposure composition, hidden-share summaries, and cell-level anchor code.
- The richest control stack still keeps the reference OR above 1 and reduces leave-one-out error relative to the simpler stacks.
- Output:
  - `03_exposure_closure/multi_region_stratified_control_closure_v1/`

### 6. Frozen module tournament scoreboard
- The pre-frozen candidate stacks have now been scored without opening a new validation split.
- The current ranking places the hybrid cell-anchored stack ahead of the summary-only and blocked/equal-area stacks.
- Output:
  - `08_nature_experiment_plan/module_tournament_scoreboard_v1.csv`
  - `08_nature_experiment_plan/module_tournament_scoreboard_v1.md`

### 7. Technical validation package
- The observability, sign/unit, blocked/equal-area, stratified-control, and transfer evidence are now consolidated in a reviewer-facing technical-validation note.
- Output:
  - `08_nature_experiment_plan/multi_region_technical_validation_v1.md`
  - `08_nature_experiment_plan/multi_region_technical_validation_v1.csv`

### 8. Robustness
- Chao Phraya robustness grid is already frozen and exported.
- Figure set 1-6 exists in PDF/SVG/TIFF.

### 9. Hierarchical model comparison
- The region-level meta-analysis and the cell-anchored stack now have an auditable frozen comparison with leave-one-out error.
- The hierarchical comparison now also includes the multi-stratum control ladder promoted from the gap-to-upgrade matrix.
- This makes the E5 model-family choice explicit rather than narrative-only.
- Output:
  - `03_exposure_closure/hierarchical_model_v1/`

### 10. Closure-by-compilation all-region package
- The frozen hierarchical comparison is now compiled together with the new multi-region exposure translation table into a reviewer-facing all-region closure note.
- Output:
  - `03_exposure_closure/full_all_region_hierarchical_closure_v1/`

### 11. Final equal-area closure package
- The reviewer-facing final equal-area closure now makes the multi-region weighting status explicit and keeps proxy-only rows separate from the lead case.
- Output:
  - `03_exposure_closure/final_multi_region_equal_area_closure_v1/`

### 12. All-region no-fit justification
- The formal no-fit note now records why a new all-region cell-level fit is not being claimed.
- Output:
  - `08_nature_experiment_plan/all_region_cell_level_no_fit_justification_v1.md`

### 13. Infrastructure translation package
- The lead-case transport infrastructure layer is now explicit, with roads and rail hidden fractions frozen from the OSM exposure summary.
- Output:
  - `08_nature_experiment_plan/multi_region_infrastructure_translation_v1.md`
  - `08_nature_experiment_plan/multi_region_infrastructure_translation_v1.csv`

### 12. Decision-facing exposure matrix
- Population, built-up, infrastructure, and transfer status are now consolidated into one main-table candidate.
- Output:
  - `08_nature_experiment_plan/decision_facing_exposure_matrix_v1.md`
  - `08_nature_experiment_plan/decision_facing_exposure_matrix_v1.csv`

### 13. Release-gap memo
- The release story is now explicit about what is DOI-ready versus what is DOI-minted.
- Output:
  - `08_nature_experiment_plan/release_and_decision_gap_memo_v1.md`
  - `08_nature_experiment_plan/release_and_decision_gap_memo_v1.csv`

### 14. Release maturity matrix
- The local package now also has a Nature / Scientific Data release-readiness mapping that separates local completeness from public minting.
- Output:
  - `08_nature_experiment_plan/release_maturity_matrix_v1.md`
  - `08_nature_experiment_plan/release_maturity_matrix_v1.csv`

### 15. Manuscript-ready decision and release package
- The evidence has now been grouped into a manuscript-ready set of main table / companion table / appendix roles.
- Output:
  - `08_nature_experiment_plan/manuscript_ready_decision_release_package_v1.md`
  - `08_nature_experiment_plan/manuscript_ready_decision_release_package_v1.csv`

### 16. Socioeconomic translation gap
- The current stack now explicitly tracks the next possible upgrade: a socioeconomic vulnerability companion layer, and the GVI country-level fallback has already been frozen in the trial report with SHDI as backup and subnational gradients visible.
- Output:
  - `08_nature_experiment_plan/socioeconomic_translation_gap_v1.md`
  - `08_nature_experiment_plan/socioeconomic_translation_gap_v1.csv`

### 17. Socioeconomic layer candidate
- GVI is now frozen as the preferred vulnerability companion candidate, with GRDI as the preferred raster upgrade and SHDI/nightlights kept as fallback paths.
- Output:
  - `08_nature_experiment_plan/socioeconomic_layer_candidate_v1.md`
  - `08_nature_experiment_plan/socioeconomic_layer_candidate_v1.csv`

### 18. Socioeconomic layer trial plan
- The GVI/SHDI/GRDI matching test is now frozen as a concrete trial plan, and GVI country-level vulnerability values plus subnational gradients have now been retrieved from the public Global Data Lab table pages.
- Output:
  - `08_nature_experiment_plan/socioeconomic_layer_trial_plan_v1.md`
  - `08_nature_experiment_plan/socioeconomic_layer_trial_plan_v1.csv`

### 19. Socioeconomic layer access matrix
- The access ranking is now frozen: GVI is immediately reachable, SHDI is the contextual backup, and GRDI is the preferred but access-gated upgrade.
- Output:
  - `08_nature_experiment_plan/socioeconomic_layer_access_matrix_v1.md`
  - `08_nature_experiment_plan/socioeconomic_layer_access_matrix_v1.csv`

### 20. Socioeconomic trial harness
- A reusable harness now exists for ingesting GVI, SHDI, or GRDI once the files are staged, and it can now retrieve GVI vulnerability context, GVI subnational spread, and SHDI country-level context directly from the public table pages.
  - Output:
  - `07_scripts_and_registry/build_socioeconomic_layer_trial.py`
  - `11_submission_ready_v1/source_data/build_socioeconomic_layer_trial.py`
  - `03_exposure_closure/socioeconomic_layer_trial_v1/`
  - `11_submission_ready_v1/source_data/socioeconomic_layer_trial_v1/`

### 21. Socioeconomic gradient comparison
- The GVI-vs-SHDI gradient comparison table now makes the within-country vulnerability spread explicit and is frozen as a reviewer-facing comparison artifact.
  - Output:
  - `08_nature_experiment_plan/socioeconomic_layer_gradient_comparison_v1.csv`
  - `08_nature_experiment_plan/socioeconomic_layer_gradient_comparison_v1.md`

### 22. Structural vulnerability reviewer appendix
- The structural-vulnerability boundary is now frozen as reviewer-safe wording that keeps the region-proxy trial separate from any final polygon-level claim.
  - Output:
  - `08_nature_experiment_plan/structural_vulnerability_reviewer_appendix_v1.md`

## What Still Blocks a Nature-Grade Closure

1. Final multi-region polygon / equal-area benchmark package is now closed at reviewer-facing level, but true polygon-native source for every region is still missing.
2. EGMS external benchmark closure is still open because CLMS token access is unavailable.
3. The final all-region cell-level hierarchical model is still absent; the current stack now has a closure-by-compilation all-region package rather than a full new all-region Bayesian fit, and the no-fit boundary is now explicit.
4. The public DOI/repository release is not yet present.
5. A socioeconomic vulnerability layer is not yet frozen and would require a clean public source before it could be added.
6. GRDI is the preferred next candidate, but it is not yet processed into the evidence stack.
7. The GRDI/SHDI matching trial is defined, but the actual raster/context comparison has not yet been run.
8. SHDI is the immediately executable fallback if the GRDI access path is not yet available.
9. The trial harness is ready, but no socioeconomic data file has yet been staged into it.

## Practical Interpretation

- If the goal is a strong, defensible submission package, the current stack is already beyond a draft.
- If the goal is Nature main-text standard, the remaining work is consolidation, not discovery:
  - keep the final equal-area closure visible,
  - freeze the blocked validation rule,
  - complete DOI/repository release,
  - and close the external benchmark path if access becomes available.

## Supporting Files
- `08_nature_experiment_plan/completion_audit_v1.md`
- `08_nature_experiment_plan/nature_standard_full_boost_plan_v1.md`
- `08_nature_experiment_plan/module_tournament_contract_v1.md`
- `08_nature_experiment_plan/frozen_validation_split_v1.csv`
- `08_nature_experiment_plan/benchmark_sign_unit_audit_v1.md`
- `08_nature_experiment_plan/transfer_validation_v1.md`
- `08_nature_experiment_plan/multi_region_exposure_closure_v1.md`
- `08_nature_experiment_plan/multi_region_exposure_translation_v1.md`
- `08_nature_experiment_plan/multi_region_technical_validation_v1.md`
- `11_submission_ready_v1/zenodo_metadata_v1.json`
- `11_submission_ready_v1/doi_release_checklist_v1.md`
- `08_nature_experiment_plan/script_dependency_gap_v1.md`
- `08_nature_experiment_plan/structural_vulnerability_reviewer_appendix_v1.md`
