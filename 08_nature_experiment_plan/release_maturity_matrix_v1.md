# Release Maturity Matrix v1
Date: 2026-07-11

## Purpose
This matrix maps the current release package to the Nature / Scientific Data expectations that matter most for review: minimum dataset access, technical validation, code availability, persistent repository metadata, and transparent versioning.

## Comparator Anchors
- Nature Portfolio reporting standards require explicit data, material, code, and protocol availability statements.
- Nature support guidance says a data availability statement should describe how the supporting data can be accessed, including persistent identifiers where available.
- Scientific Data requires Technical Validation for Data Descriptors and expects live data to be available for peer review.
- Scientific Data repository guidance emphasizes persistent, long-term access for published datasets.

## Release Matrix

| requirement | Nature source | current local evidence | status | blocking gap |
|---|---|---|---|---|
| Minimum dataset for review | Nature reporting standards; Nature support data-availability guidance | `11_submission_ready_v1/source_data/` contains the benchmark inventories, closure tables, figure source data, validation notes, and runbooks needed to interpret the manuscript | local complete, public mint pending | public DOI and version-specific repository URL |
| Technical validation | Scientific Data submission guidelines; Scientific Data for referees | `multi_region_technical_validation_v1.md` consolidates observability, sign/unit, blocked/equal-area, stratified control, and transfer evidence | complete locally | public deposit not yet minted |
| Code availability | Nature reporting standards; Nature Communications policy language | analysis and figure scripts are stored in the submission package, and the release finalizers / validators are included | local complete, public URL pending | version-specific repository URL |
| Persistent repository metadata | Scientific Data repository guidance | `zenodo_metadata_v1.json`, `zenodo_deposit_preview_v1.json`, `doi_release_checklist_v1.md`, and `zenodo_submission_runbook_v1.md` are frozen and DOI-ready | DOI-ready, not minted | public DOI and repository record |
| Figure source data | Nature reporting standards | `figures/09_figures_v1/` and the mirrored figure assets are in the release package | complete locally | public hosting / mint record |
| Reproducibility indexes | Nature-family review norms | `source_data_inventory_v1.csv`, `submission_checksums_v1.md`, and `submission_archive_hash_v1.md` are synchronized with the package | complete locally | none locally |
| External benchmark closure | Nature-family exposure / validation papers | EGMS/CLMS remains token-blocked; Japan and Iran are explicitly labeled lineage extensions | partial | external token access and live benchmark closure |
| Decision-facing release story | Nature-family exposure / infrastructure papers | `decision_facing_exposure_matrix_v1`, `multi_region_infrastructure_translation_v1`, and `manuscript_ready_decision_release_package_v1` are frozen | complete locally | public release identifiers still pending |

## Reading the Matrix

1. The package is already strong on local completeness.
2. The remaining release weakness is external, not internal: DOI and repository URL are still missing.
3. Scientific Data-style reviewer scrutiny is already addressed locally through technical validation and persistent indexes.
4. The manuscript should describe the release as DOI-ready rather than DOI-minted until the external identifiers exist.

## Bottom Line
The release package now matches the structure expected by Nature-family journals: minimum dataset, code, technical validation, reproducibility indexes, and a clear distinction between local readiness and public minting.

