# Risk-Targeted Experiment Boost Plan v1
Date: 2026-07-13

## Scope lock

This plan applies only to the Nature manuscript line under:

- `Desktop/nature`

No files outside this Nature directory are in scope.

## One-sentence objective

Strengthen the current Open InSAR Observability Bias and Exposure Benchmark by converting the remaining partial experiment layers into reproducible, reviewer-auditable closure packages, while keeping EGMS as the explicit external upgrade path.

## Source basis

- `11_submission_ready_v1/manuscript/full_manuscript_draft_v3.md`
- `11_submission_ready_v1/source_data/all_experiments_overview_v1.md`
- `11_submission_ready_v1/source_data/completion_audit_v1.md`
- `11_submission_ready_v1/claim_evidence_map_v1.md`
- `11_submission_ready_v1/notes/review_risk_audit_v1.md`
- `11_submission_ready_v1/notes/final_consistency_audit_v1.md`
- `08_nature_experiment_plan/script_dependency_gap_v1.md`
- `11_submission_ready_v1/source_data/external_release_readiness_audit_v1.md`

## Current diagnosis

The manuscript is past the discovery stage. The core claim is supported locally by the Chao Phraya lead-case model, the multi-region blocked/equal-area synthesis, transfer probes, robustness screens, and the frozen hierarchical comparison.

The remaining risk is not that the paper has no result. The risk is that several important layers are still documented as `partial`, which gives reviewers clear openings:

- the final multi-region polygon/equal-area benchmark package is incomplete;
- EGMS external closure is unavailable without CLMS token access;
- the all-region package is closure-by-compilation rather than a full cell-level hierarchical fit;
- risk-underestimation evidence is not consolidated across all regions;
- the mechanism-control and socioeconomic layers remain useful but secondary;
- the broader model stack has a code-completeness gap because helper modules are missing;
- the public DOI/repository release has not been minted.

## Priority order

### P0. Code-rerun rescue for the experiment stack

Reviewer risk addressed:

- A reviewer or editor asks whether the main experiment stack can be rerun from the released scripts.
- `script_dependency_gap_v1.md` currently records missing helper modules for the multi-region model stack.

Experiment action:

- Build a self-contained rerun path for the manuscript-facing experiment stack rather than relying on missing historical helper modules.
- Keep the already runnable Chao Phraya scripts as the anchor.
- Rebuild region-level and hierarchical summaries from frozen CSV inputs.
- Add one deterministic runner for P0 outputs only.

Target outputs:

- `07_scripts_and_registry/run_p0_nature_experiment_stack.ps1`
- `08_nature_experiment_plan/p0_rerun_manifest_v1.md`
- `08_nature_experiment_plan/p0_rerun_manifest_v1.csv`
- `08_nature_experiment_plan/p0_rerun_log_v1.md`

Pass condition:

- A clean local run regenerates the Chao Phraya primary model summary, multi-region blocked/equal-area report, hierarchical comparison table, transfer-score table, and figure source-data tables used by the manuscript.

Stop condition:

- If a missing raw input prevents full rerun, record the exact missing input and freeze a partial rerun manifest. Do not imply full code reproducibility.

### P0. Final multi-region polygon/equal-area closure

Reviewer risk addressed:

- The current area-weighted/equal-area story is strong but still has an explicit missing gate: the final cell-level polygon/equal-area benchmark package.

Experiment action:

- Convert the current region-level equal-area synthesis into a final cell/polygon audit package.
- For each region, record whether the exposure overlay is true polygon/equal-area, cell-count proxy, or unavailable.
- Separate lead-case closure from control/transfer summaries.
- Make the exact weighting method explicit for population, built-up land, and transport/infrastructure.

Target outputs:

- `03_exposure_closure/final_multi_region_equal_area_closure_v1/`
- `08_nature_experiment_plan/final_multi_region_equal_area_closure_v1.md`
- `08_nature_experiment_plan/final_multi_region_equal_area_closure_v1.csv`
- `11_submission_ready_v1/source_data/final_multi_region_equal_area_closure_v1/`

Minimum table columns:

- `region`
- `role`
- `product_family`
- `overlay_method`
- `cell_count`
- `strong_cell_count`
- `observable_fraction`
- `hidden_population`
- `hidden_built_up_area`
- `hidden_transport_or_infrastructure`
- `weighting_status`
- `claim_status`

Pass condition:

- Every region in the benchmark has an explicit weighting status, and no region is silently treated as equivalent to the Chao Phraya lead case.

Stop condition:

- If true polygon/equal-area data are unavailable for a region, label it as `proxy_only` and keep it out of the lead-case claim.

### P0. All-region cell-level hierarchical fit or formal no-fit justification

Reviewer risk addressed:

- The manuscript currently has a strong frozen hierarchical comparison, but the audit still says the all-region package is closure-by-compilation rather than a full new all-region cell-level fit.

Experiment action:

- Try one full all-region cell-level hierarchical fit using only frozen inputs and a pre-declared model.
- If raw cell-level inputs are incomplete across regions, produce a formal no-fit justification and keep the current hybrid anchor as the primary synthesis.

Pre-declared model:

- Outcome: non-majority observability or hidden-exposure indicator, depending on available region-level cell data.
- Main predictor: strong-subsidence indicator.
- Controls: region fixed effect, land-cover composition if available, exposure layer if available.
- Validation: leave-one-region-out and Chao Phraya holdout sensitivity.

Target outputs:

- `03_exposure_closure/all_region_cell_level_hierarchical_fit_v1/`
- `08_nature_experiment_plan/all_region_cell_level_hierarchical_fit_v1.md`
- `08_nature_experiment_plan/all_region_cell_level_hierarchical_fit_v1.csv`
- `08_nature_experiment_plan/all_region_cell_level_no_fit_justification_v1.md`, only if the fit cannot be run honestly.

Pass condition:

- Either the all-region cell-level model runs and its effect direction remains positive, or the manuscript has a documented reason for not claiming that model.

Stop condition:

- Do not tune model families after seeing the result. If the pre-declared fit fails or is under-identified, report that and keep the current cell-anchored synthesis.

### P0. EGMS closure branch

Reviewer risk addressed:

- Europe-scale closure is the clearest external benchmark gap.

Experiment action:

- Maintain two branches:
  - `token_available`: download/query EGMS, run sign/unit audit, then run European closure for Po/Rhone/Rhine or the available subset.
  - `token_unavailable`: freeze the EGMS query protocol, expected files, processing script, and post-token validation checklist.

Target outputs:

- `06_egms_query_pack/egms_query_protocol_v1.md`
- `06_egms_query_pack/egms_expected_file_manifest_v1.csv`
- `06_egms_query_pack/egms_post_token_validation_checklist_v1.md`
- `03_exposure_closure/egms_external_closure_v1/`, only if access becomes available.

Pass condition:

- If token access is available, EGMS closure produces a European external benchmark table with sign/unit audit and region-specific closure status.
- If token access is not available, the manuscript keeps the statement `Dense Europe-scale closure requires EGMS` and does not overclaim external closure.

Stop condition:

- No EGMS-derived claim enters the manuscript unless the EGMS data files are locally present and checksummed.

### P1. Cross-region risk-underestimation consolidation

Reviewer risk addressed:

- The manuscript argues that observability affects exposure accounting, but the current risk-underestimation layer is not fully consolidated across regions.

Experiment action:

- Build one consolidated table that translates the observability gap into exposure-underestimation quantities.
- Keep the table separate from causal risk claims.
- Use region role labels to avoid treating weak-anchor controls as full validation cases.

Target outputs:

- `08_nature_experiment_plan/risk_underestimation_consolidated_v1.md`
- `08_nature_experiment_plan/risk_underestimation_consolidated_v1.csv`
- `11_submission_ready_v1/source_data/risk_underestimation_consolidated_v1.csv`

Minimum table columns:

- `region`
- `role`
- `observable_exposure`
- `hidden_exposure`
- `hidden_share`
- `strong_motion_threshold`
- `observability_threshold`
- `anchor_status`
- `claim_role`

Pass condition:

- The table can support the Results phrase `exposure accounting changes` without implying causal damage risk.

Stop condition:

- If a region lacks exposure inputs, mark it `not_translated` instead of imputing values.

### P1. Mechanism-control closure

Reviewer risk addressed:

- A reviewer may argue that the signal is only land-cover composition, product availability, or one regional artifact.

Experiment action:

- Freeze the mechanism-control stack as a compact table: base model, land-cover adjusted model, exposure-composition adjusted model, hidden-share adjusted model, and cell-anchor model.
- Report effect direction, OR, CI, and leave-one-out error where available.

Target outputs:

- `08_nature_experiment_plan/mechanism_control_closure_v1.md`
- `08_nature_experiment_plan/mechanism_control_closure_v1.csv`

Pass condition:

- The richest defensible control stack keeps the reference OR above 1, or the manuscript narrows the claim accordingly.

Stop condition:

- Do not add controls that are missing for most regions if they make the benchmark appear more complete than it is.

### P1. Transfer-probe hardening

Reviewer risk addressed:

- Japan and Iran currently support product-lineage extension, not independent truth. That distinction must be hard to miss.

Experiment action:

- Add a transfer-probe audit sheet that records data source, token status, independent-truth status, sign/unit checks, and what claim each probe is allowed to support.

Target outputs:

- `08_nature_experiment_plan/transfer_probe_audit_v1.md`
- `08_nature_experiment_plan/transfer_probe_audit_v1.csv`

Pass condition:

- The transfer layer supports `same censoring question across public product families` and does not imply independent validation.

Stop condition:

- If a probe lacks reproducible ingest metadata, keep it as narrative support only.

### P2. Socioeconomic companion layer

Reviewer risk addressed:

- The current vulnerability context is useful but can distract from the core measurement-bias paper if it becomes a new unsupported claim.

Experiment action:

- Keep GVI/SHDI/GRDI as a companion layer only.
- Run the executable SHDI fallback if data are staged.
- Do not promote socioeconomic vulnerability to a main-text result unless a clean public source and reproducible matching table exist.

Target outputs:

- `08_nature_experiment_plan/socioeconomic_companion_decision_v1.md`
- `08_nature_experiment_plan/socioeconomic_companion_decision_v1.csv`

Pass condition:

- The manuscript either keeps socioeconomic context as a bounded companion layer or removes it from the main claim.

Stop condition:

- No raster-level socioeconomic claim without a staged raster/context input and matching report.

### P2. Public release and DOI finalization

Reviewer risk addressed:

- This is not a scientific experiment, but it is a submission gate for reproducibility and data availability.

Action:

- Mint or confirm the public DOI.
- Replace `[DOI]` and `[REPOSITORY_URL]`.
- Run the post-mint validation scripts.
- Refresh checksums and archive hash after replacement.

Target outputs:

- updated `11_submission_ready_v1/manuscript/full_manuscript_draft_v3.md`
- updated `11_submission_ready_v1/repository_release_candidate.md`
- updated `11_submission_ready_v1/submission_checksums_v1.md`
- updated `11_submission_ready_v1/submission_archive_hash_v1.md`

Pass condition:

- Data Availability and Code Availability no longer contain placeholders.

Stop condition:

- Do not publish placeholder DOI or repository URL values.

## Execution sequence

1. Restore the P0 rerun path.
2. Close the final multi-region equal-area package.
3. Attempt the pre-declared all-region cell-level hierarchical fit.
4. Run the EGMS branch if token access is available; otherwise freeze the no-token protocol branch.
5. Consolidate risk-underestimation and mechanism-control tables.
6. Harden transfer-probe audit language.
7. Decide whether the socioeconomic companion layer stays, moves to supplement/source data, or is removed from the main claim.
8. Mint DOI/repository release after the experiment artifacts are frozen.

## Main-text impact rules

- If P0 equal-area closure succeeds: strengthen the Results sentence on multi-region exposure closure.
- If the all-region cell-level fit succeeds: promote it into the Results model-comparison paragraph and keep the hybrid anchor as a robustness comparison.
- If the all-region cell-level fit fails: keep the current Results language and cite the no-fit justification in Methods or source data.
- If EGMS closure succeeds: replace `Dense Europe-scale closure requires EGMS` with a region-specific EGMS closure sentence.
- If EGMS remains unavailable: keep the current boundary language unchanged.
- If risk-underestimation consolidation succeeds: add one compact Results sentence and keep causal damage-risk language out.
- If socioeconomic matching remains partial: keep it as context, not a main contribution.

## Minimum deliverable for the next experiment sprint

The next sprint should produce, at minimum:

- `p0_rerun_manifest_v1.md`
- `final_multi_region_equal_area_closure_v1.md`
- either `all_region_cell_level_hierarchical_fit_v1.md` or `all_region_cell_level_no_fit_justification_v1.md`
- `egms_query_protocol_v1.md`
- `risk_underestimation_consolidated_v1.csv`

These five files would convert the most visible reviewer risks into either completed experiments or explicit, defensible boundaries.
