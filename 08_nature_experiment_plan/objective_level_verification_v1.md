# Objective-Level Verification v1
Date: 2026-07-13

## Original objective

Strictly follow the plan. Finish every step to its required standard. Then compare the Nature package against the other five packages in the workspace, namely the three `Second Batch` / `Third Batch` papers plus `power_se` and the battery / distribution-network package. Do not work on those five packages themselves; only compare against them. The end goal is to improve the Nature package so it can beat the five.

## Requirement-level status

### 1. Nature must be improved through the planned experiment / release steps

Status: mostly complete

Evidence:
- `08_nature_experiment_plan/completion_audit_v1.md`
- `08_nature_experiment_plan/cross_paper_final_status_audit_v1.md`
- `11_submission_ready_v1/repository_release_candidate.md`
- `11_submission_ready_v1/release_and_decision_gap_memo_v1.md`
- `11_submission_ready_v1/manuscript_ready_decision_release_package_v1.md`

What is still open:
- Public DOI / repository minting
- Explicit final external release

### 2. The five peer packages must be used only for comparison, not modification

Status: complete

Evidence:
- The comparison files only read peer-package status files:
  - `cross_paper_scorecard_v2.md`
  - `cross_paper_evidence_matrix_v1.md`
  - `cross_paper_gap_to_win_v2.md`
  - `cross_paper_reviewer_appendix_index_v1.md`
  - `cross_paper_final_status_audit_v1.md`
- No peer-package source files were rewritten.

### 3. Nature must be compared against all five packages

Status: complete

Evidence:
- `cross_paper_scorecard_v2.md`
- `cross_paper_evidence_matrix_v1.md`
- `cross_paper_reviewer_appendix_index_v1.md`
- `cross_paper_final_status_audit_v1.md`

### 4. The comparison must support the claim that Nature beats the five

Status: not yet fully proven

Why:
- Nature is already the strongest scientific package in the comparison set.
- The reviewer-facing comparison package is complete.
- But the package is still DOI-staged rather than DOI-minted.
- The all-region hierarchy is still closure-by-compilation rather than a new fit.
- Those facts keep the overall win from being fully unconditional.

## Current objective verdict

The Nature package now satisfies the comparison and packaging parts of the objective. It has not yet fully satisfied the final unconditional "beat the five" condition because the external release mint is still missing.

## Next concrete action

1. Mint the public DOI and version-specific repository URL.
2. Replace the placeholders in `Data Availability` and `Code Availability`.
3. Keep the all-region hierarchy explicitly labeled as closure-by-compilation.
4. Re-evaluate the overall win condition after minting.
