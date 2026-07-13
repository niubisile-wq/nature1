# Nature Experiment Completion Audit v1
Date: 2026-07-11

## Scope
This audit compares the experiment plan in `08_nature_experiment_plan` and `experiment_execution_checklist.csv` against current local outputs under `03_exposure_closure`, `04_japan_licsbas_probe`, `05_iran_insar_probe`, `06_egms_query_pack`, `09_figures_v1`, `10_manuscript_skeleton`, and `11_submission_ready_v1`.

## Status Legend
- `complete`: the planned artifact exists and the associated experiment is closed to the level represented in the plan.
- `partial`: the experiment has meaningful outputs, but the plan's final gate is still not closed.
- `missing`: no authoritative local output found for the planned artifact.

## Module-by-Module Audit

| Module | Planned artifact / gate | Local evidence | Status | Remaining gap |
|---|---|---|---|---|
| E0 | `claim_collision_matrix.md` | `08_nature_experiment_plan/claim_collision_matrix.md` | complete | None for the plan-level collision audit. |
| E1 | `dataset_inventory_v1.csv` | `08_nature_experiment_plan/dataset_inventory_v1.csv` | complete | None for the inventory layer. |
| E2 | Observability masks / failure layer | `08_nature_experiment_plan/observability_masks_v1.md`, `08_nature_experiment_plan/observability_masks_v1.csv`, `08_nature_experiment_plan/observability_masks_chao_phraya_v1.tif`, `08_nature_experiment_plan/observability_masks_chao_phraya_v1_georef.tif`, `03_exposure_closure/multi_delta_vlm_exposure_censoring_report.md`, `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/*`, `08_nature_experiment_plan/multi_region_technical_validation_v1.md` | partial | The observability-failure layer now has a note, CSV, reconstructed raster with georeference, and a consolidated multi-region technical validation package, but the final multi-region polygon/equal-area benchmark package is still missing. |
| E3 | Benchmark deformation layers | `04_japan_licsbas_probe/*`, `05_iran_insar_probe/*`, `01_innovation_reports/EGMS实际运行状态_2026-07-09.md`, `08_nature_experiment_plan/benchmark_sign_unit_audit_v1.md`, `08_nature_experiment_plan/multi_region_technical_validation_v1.md` | partial | Japan/Iran probes exist, and the sign/unit audit is now frozen inside a consolidated technical-validation package, but external benchmark closure is still not complete enough to treat the benchmark family as finalized. |
| E4 | `area_weighted_exposure_v1.csv` | `08_nature_experiment_plan/area_weighted_exposure_v1.csv`, `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/*`, `03_exposure_closure/multi_delta_vlm_exposure_censoring_report.md`, `03_exposure_closure/multi_region_blocked_equal_area_closure_v1/*`, `08_nature_experiment_plan/multi_region_exposure_translation_v1.md`, `08_nature_experiment_plan/multi_region_infrastructure_translation_v1.md`, `08_nature_experiment_plan/decision_facing_exposure_matrix_v1.md`, `08_nature_experiment_plan/release_and_decision_gap_memo_v1.md`, `08_nature_experiment_plan/manuscript_ready_decision_release_package_v1.md` | partial | The named area-weighted summary now exists and now has a blocked/equal-area synthesis layer plus consolidated multi-region exposure, infrastructure, decision-facing, release-gap, and manuscript-ready packaging tables, but the final cell-level polygon/equal-area benchmark package is still incomplete. |
| E5 | `hierarchical_model_v1` | `03_exposure_closure/multi_delta_vlm_exposure_censoring_report.md`, `09_figures_v1/fig3_chao_phraya_robustness_grid.*`, `03_exposure_closure/multi_region_blocked_equal_area_closure_v1/*`, `03_exposure_closure/hierarchical_anchor_closure_v1/*`, `03_exposure_closure/multi_region_stratified_control_closure_v1/*`, `03_exposure_closure/hierarchical_model_v1/*`, `03_exposure_closure/full_all_region_hierarchical_closure_v1/*`, `08_nature_experiment_plan/multi_region_exposure_translation_v1.md` | partial | The hierarchy is now anchored by the Chao Phraya cell-level primary model and now has the frozen multi-stratum control ladder promoted into the hierarchical comparison; a closure-by-compilation all-region package now exists, but a fully new all-region cell-level fit is still absent. |
| E6 | `risk_underestimation_v1.csv` | `08_nature_experiment_plan/risk_underestimation_v1.csv`, `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/*`, `03_exposure_closure/multi_delta_vlm_exposure_censoring_report.md` | partial | The named risk-lowballing table now exists, but the final cross-region inferential package is not yet consolidated. |
| E7 | `transfer_validation_v1.md` | `08_nature_experiment_plan/transfer_validation_v1.md`, `04_japan_licsbas_probe/*`, `05_iran_insar_probe/*`, `08_nature_experiment_plan/transfer_validation_scores_v1/*`, `09_figures_v1/fig6_transfer_scope.*`, `08_nature_experiment_plan/multi_region_technical_validation_v1.md` | partial | Transfer evidence is now consolidated and frozen as a scope-extension package, but the validation still lacks external EGMS closure. |
| E8 | `mechanism_control_table_v1.csv` | `08_nature_experiment_plan/mechanism_control_table_v1.csv`, `09_figures_v1/fig5_controls_transfer.*`, WorldCover-adjusted outputs, `03_exposure_closure/multi_region_stratified_control_closure_v1/*`, `08_nature_experiment_plan/multi_region_technical_validation_v1.md` | partial | Mechanism controls are now tabulated, and the new stratified control ladder plus the consolidated technical-validation package add a frozen landcover/exposure/hidden-share robustness layer, but the final multi-stratum control package is still not fully closed. |
| E9 | `robustness_dashboard_v1` | `03_exposure_closure/chao_phraya_robustness_grid/*`, `09_figures_v1/fig3_chao_phraya_robustness_grid.*` | complete | Sensitivity grid and bootstrap outputs are present. |
| E10 | `figure_plan_and_source_data` | `08_nature_experiment_plan/figure_source_map_v1.csv`, `09_figures_v1/fig1..fig7.*`, `11_submission_ready_v1/figures/09_figures_v1/*` | complete | Figure set 1-7 and source mapping are present. |
| E11 | `repository_release_candidate` | `11_submission_ready_v1/repository_release_candidate.md`, `11_submission_ready_v1/submission_checksums_v1.md`, `11_submission_ready_v1/zenodo_metadata_v1.json`, `11_submission_ready_v1/doi_release_checklist_v1.md`, `11_submission_ready_v1/release_maturity_matrix_v1.md`, `11_submission_ready_v1/*`, `11_submission_ready_v1.zip` | partial | Local handoff package and DOI-ready metadata exist, but a public DOI/repository release is not present in the current local evidence. |

## Direct Evidence of Closed Items
- `E0` and `E1` are materialized as standalone plan files.
- `E9` is materialized as the Chao Phraya robustness grid CSV and report.
- `E10` is materially complete: Fig. 1 through Fig. 7 are rendered in PDF/SVG/TIFF form and copied into the submission-ready package.
- `dataset_manifest.json` and `source_data_manifest_v1.csv` now exist as local reproducibility indexes.
- `repository_release_candidate.md` now exists as the local handoff summary.
- `module_tournament_contract_v1.md`, `module_tournament_ledger_v1.csv`, and `frozen_validation_split_v1.csv` now exist as the frozen module-tournament scaffold.
- `module_tournament_candidate_registry_v1.csv` now exists as the candidate stack registry for future module rotation.
- `module_tournament_scoreboard_v1.csv` and `module_tournament_scoreboard_v1.md` now summarize the currently frozen stack ranking without opening a new validation split.
- `hierarchical_model_v1/` now contains a frozen hierarchical comparison that makes the E5 model-family choice auditable rather than narrative-only.
- `full_all_region_hierarchical_closure_v1/` now contains the closure-by-compilation all-region package built only from frozen inputs.
- `benchmark_deformation_layers_v1.csv` and `benchmark_sign_unit_audit_v1.md` now exist as the E3 deformation-layer audit scaffold.
- `transfer_validation_v1.md` now contains a frozen decision rule for the next validation run.
- `transfer_validation_scores_v1/` now contains a frozen score table for Japan, Iran, and the current benchmark transfer set without opening a new validation split.
- `multi_region_exposure_closure_v1.csv` now consolidates the current multi-region exposure closure summary into a machine-readable table.
- `multi_region_exposure_translation_v1.md` and `multi_region_exposure_translation_v1.csv` now translate the exposure evidence into a reviewer-facing population / built-up / transport table.
- `multi_region_exposure_closure_v1.md` and `rebuild_multi_region_exposure_closure.py` now make the multi-region closure reproducible from current summary files.
- `03_exposure_closure/multi_region_summary_meta_closure_v1/` now contains a region-level random-effects meta-analysis, meta-regression, and leave-one-out closure.
- `03_exposure_closure/multi_region_blocked_equal_area_closure_v1/` now contains a blocked/equal-area region-level synthesis with leave-one-out validation and a ridge meta-regression.
- `03_exposure_closure/hierarchical_anchor_closure_v1/` now contains a hybrid hierarchical synthesis that freezes a Chao Phraya cell-level anchor and pools it with the region-level evidence set.
- `03_exposure_closure/multi_region_stratified_control_closure_v1/` now contains a frozen multi-stratum control ladder with landcover composition, exposure composition, hidden-share summaries, and cell-level anchor code.
- `multi_region_technical_validation_v1.md` now consolidates observability, sign/unit, blocked/equal-area, stratified-control, and transfer evidence into one reviewer-facing note.
- `multi_region_infrastructure_translation_v1.md` now makes the lead-case roads/rail layer explicit and keeps the non-lead regions labeled as not yet translated.
- `decision_facing_exposure_matrix_v1.md` now consolidates population, built-up, infrastructure, and transfer status into one main-table candidate.
- `release_and_decision_gap_memo_v1.md` now keeps the release story honest by separating DOI-ready metadata from a minted DOI.
- `manuscript_ready_decision_release_package_v1.md` now states how the evidence should be grouped in the paper.
- `release_maturity_matrix_v1.md` now maps Nature / Scientific Data release expectations to local evidence and remaining mint gaps.
- `script_dependency_gap_v1.md` now documents the missing helper modules that block the main model scripts.
- `03_exposure_closure/socioeconomic_layer_trial_v1/` now contains frozen GVI country-level vulnerability and subnational-spread tables for the single-country cases, SHDI contextual backup tables, a GVI-vs-SHDI gradient comparison table, and an explicit unresolved marker for Rhine.
- `socioeconomic_layer_trial_plan_v1.md` now records the executed GVI vulnerability fallback, the SHDI backup context, the visible subnational gradients, the gradient comparison table, and the remaining GRDI upgrade path.
- `03_exposure_closure/chao_phraya_nature_model_v1/chao_phraya_nature_model_primary_report.md` now contains a claim-aligned lead-case statistical model with block bootstrap.
- `11_submission_ready_v1/source_data/chao_phraya_nature_model_v1/` now mirrors the self-contained lead-case model outputs into the submission package.
- `03_exposure_closure/multi_region_summary_meta_closure_v1/` now contains a self-contained region-level meta-analysis and leave-one-out closure.
- `11_submission_ready_v1/source_data/multi_region_summary_meta_closure_v1/` now mirrors the region-level meta-analysis into the submission package.
- `11_submission_ready_v1/source_data/README.md` now documents the source-data mirror.
- `11_submission_ready_v1/source_data/multi_region_closure_summary_v1.md` now consolidates the multi-region lead/control story.
- `11_submission_ready_v1/source_data_inventory_v1.csv` now inventories the full handoff package.
- `11_submission_ready_v1/zenodo_metadata_v1.json`, `11_submission_ready_v1/doi_release_checklist_v1.md`, and `11_submission_ready_v1/release_maturity_matrix_v1.md` now define the DOI-ready release metadata, upload checklist, and release readiness mapping.
- `submission_checksums_v1.md` now locks the current package hashes.
- `submission_archive_hash_v1.md` now records the current zip hash outside the archive to avoid self-reference.

## Direct Evidence of Still-Open Items
- `observability_masks_v1` is present as local note, CSV, and reconstructed raster with georeference, but the final multi-region polygon/equal-area benchmark package is still absent.
- The socioeconomic translation layer now has a frozen GVI country-level vulnerability fallback with subnational gradients, plus a SHDI contextual backup and a GVI-vs-SHDI gradient comparison, but it is not yet a raster-level socioeconomic layer and Rhine remains a multi-country unresolved context.
- A public repository DOI is absent from the current local evidence.
- A narrowed local search of `.config`, `.codex`, Desktop, Downloads, and Documents found no `token.jwt` file.
- EGMS still depends on a CLMS token for the official download path.

## Bottom Line
The plan has moved well beyond concept stage: the manuscript package, figures, core benchmark, and robustness checks exist locally. The remaining work is not broad ideation, but consolidation of the last missing experiment artifacts and the external benchmark-release path.

## Post-Transfer Reassessment
- `E7` is now stronger because the transfer evidence is frozen as a score table and clearly labels Japan/Iran as lineage extensions, not independent truth.
- `E5` is stronger because the current cross-region synthesis is now backed by a frozen model-family comparison and the multi-stratum control ladder is promoted into the hierarchical comparison, and a closure-by-compilation all-region package now exists, but a fully new all-region cell-level fit is still absent.
- `E8` is stronger because the mechanism-control layer now has a dedicated stratified robustness package, a consolidated technical-validation note, an explicit infrastructure translation layer, a decision-facing exposure matrix, a release-gap memo, and a manuscript-ready packaging note.
- `E8` is also stronger because the socioeconomic fallback layer is now frozen at country-context level via GVI for the single-country cases, with visible subnational gradients, SHDI as backup, and a GVI-vs-SHDI gradient comparison, even though a raster upgrade is still absent.
- `E11` is still not complete because the package is DOI-ready but no public DOI/repository release has been minted, even though the new release maturity matrix shows the local package already satisfies the internal release-plumbing requirements.
