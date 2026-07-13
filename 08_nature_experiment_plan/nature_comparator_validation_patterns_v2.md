# Nature Comparator Validation Patterns v2
Date: 2026-07-11

## Purpose
This note translates the newest Nature-family comparator papers into concrete validation patterns that can be copied into the current experiment stack.

## Comparator Set

- [GNSS land subsidence observations along the northern coastline of Java, Indonesia](https://www.nature.com/articles/s41597-023-02274-0)
- [DeltaDTM: A global coastal digital terrain model](https://www.nature.com/articles/s41597-024-03091-9)
- [Hidden vulnerability of US Atlantic coast to sea-level rise due to vertical land motion](https://www.nature.com/articles/s41467-023-37853-7)
- [Establishing flood thresholds for sea level rise impact communication](https://www.nature.com/articles/s41467-024-48545-1)
- [Land subsidence risk to infrastructure in US metropolises](https://www.nature.com/articles/s44284-025-00240-y)
- [Present-day land subsidence risk in the metropolitan cities of Italy](https://www.nature.com/articles/s41598-025-18941-8)
- [Building damage risk in sinking Indian megacities](https://www.nature.com/articles/s41893-025-01663-0)
- [Global subsidence of river deltas](https://www.nature.com/articles/s41586-025-09928-6)
- [Satellite-based vertical land motion for infrastructure monitoring](https://www.nature.com/articles/s41598-025-01970-8)

## What These Papers Standardize

### 1. Technical validation should be external and metric-driven
Scientific Data descriptors and validation-heavy papers do not stop at narrative reassurance. They show:
- the reference frame or reference dataset used,
- explicit technical validation metrics,
- per-area or per-land-cover performance,
- and a clear code / data availability path.

### 2. Exposure translation should be multi-level
Nature-family risk papers do not stop at a subsidence raster.
They translate the hazard into:
- population exposed,
- buildings or infrastructure exposed,
- land-cover-specific vulnerability,
- and future or scenario-based risk.

The newest delta-scale paper also shows that multi-delta comparison is now a standard way to argue that the signal is structural rather than local.

### 3. Land-cover stratification is not optional
The strongest underestimation claims are usually supported by:
- explicit land-cover classes,
- majority / not-majority or similar thresholded exposure states,
- and a comparison between simple and stratified views.

### 4. Validation should separate lead cases from transfer cases
The comparator papers keep a lead region or lead case, then distinguish:
- direct validation,
- lineage extensions,
- and external reference checks.

### 5. Public release is part of the result
Scientific Data especially treats the release package, metadata, and technical validation as part of the contribution, not an afterthought.

## Mapping To Our Stack

| comparator pattern | current stack | gap to close |
|---|---|---|
| External technical validation | `multi_region_technical_validation_v1.md` | Expand to a publishable all-region validation appendix and keep the reference frame / sign / unit conventions explicit |
| Per-land-cover validation | `multi_region_stratified_control_closure_v1` | Promote the landcover and exposure strata into the manuscript as a fixed validation family |
| Multi-city exposure translation | `multi_region_exposure_closure_v1.csv`, `risk_underestimation_v1.csv` | Add a cleaner population / building / infrastructure table across regions |
| Lead vs transfer separation | `transfer_validation_v1.md`, `transfer_validation_scores_v1/*` | Keep Japan / Iran as lineage extensions and do not relabel them as independent truth |
| Release package clarity | `zenodo_metadata_v1.json`, `doi_release_checklist_v1.md` | Keep the repo release candidate ready for DOI minting |
| Multi-delta comparative validation | `full_all_region_hierarchical_closure_v1.md` | Compare regions with a frozen model family instead of a single lead case |
| Infrastructure monitoring roadmap | `benchmark_sign_unit_audit_v1.md` + `multi_region_technical_validation_v1.md` | Keep the operational roadmap explicit and reproducible |

## Highest-Value Next Upgrades

1. Build a full all-region hierarchical closure that uses the frozen control ladder and the blocked/equal-area synthesis as fixed candidates.
2. Expand the multi-region exposure table to include population, built-up area, and infrastructure counts in one consistent schema.
3. Keep the technical validation package as a reviewer-facing appendix with explicit sign/unit/provenance notes.
4. Preserve the external benchmark path as a separate upgrade route instead of inflating the current transfer evidence.

## Bottom Line
The newest comparator papers support a strategy that is already partly in place here: multi-region exposure translation, explicit validation, and strict separation of lead cases from lineage extensions. The next real gain is to turn the frozen evidence into a full all-region hierarchical closure with a clean technical-validation appendix.
