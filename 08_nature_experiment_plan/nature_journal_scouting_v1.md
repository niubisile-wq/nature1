# Nature Journal Scouting v1
Date: 2026-07-11

## Purpose
This note compares the current experiment stack against current Nature Portfolio standards and closely related high-impact papers. The goal is to turn external publication standards into concrete experimental upgrades.

## Current Nature-Level Baseline

### 1. Data and code must be explicit
- Nature Portfolio requires a data availability statement and a code availability statement for original research.
- Scientific Data Data Descriptors require datasets to be available at submission and accompanied by methods, data records, and technical validation.
- Code used in the paper must be accessible to editors and referees before publication, and the final release should point to a persistent repository.

### 2. Reviewer-reusable evidence must be visible
- The minimum dataset needed to interpret, verify, and extend the article must be transparent.
- Public release should happen on publication, not after it.
- For dataset-oriented work, technical validation is not optional; the release needs to show how the dataset was checked.

### 3. Nature-family subsidence/exposure papers share a pattern
- Use high-resolution geodetic or InSAR products.
- Validate or cross-check against an independent source where possible.
- Translate deformation into policy-relevant exposure or risk metrics.
- Add uncertainty bounds, scenario translation, or leave-one-out checks.
- Make limitations explicit when independent validation is unavailable.

## Comparator Papers

| Paper | What they emphasize | What to copy |
|---|---|---|
| [Disappearing cities on US coasts](https://www.nature.com/articles/s41586-024-07038-3) | High-resolution VLM, LiDAR DEMs, sea-level scenarios, census/property exposure, GNSS validation | Keep a high-resolution geophysical layer, explicit exposure translation, and independent validation. |
| [Land subsidence risk to infrastructure in US metropolises](https://www.nature.com/articles/s44284-025-00240-y) | Multi-city subsidence mapping and infrastructure risk translation | Add a multi-region infrastructure or building-risk layer, not just a regional signal table. |
| [Hidden vulnerability of US Atlantic coast to sea-level rise due to vertical land motion](https://www.nature.com/articles/s41467-023-37853-7) | Land-cover stratification plus underestimation claim | Keep land-cover stratification and show how subsidence changes exposure by cover class. |
| [Subsidence more than doubles sea-level rise today along densely populated coasts](https://www.nature.com/articles/s41467-026-72293-z) | Diverse VLM data, exposure-weighted comparison, explicit data limitations | Use a clear weighted baseline and be explicit about coverage limits. |
| [Uncovering the impacts of depleting aquifers: A remote sensing analysis of land subsidence in Iran](https://www.science.org/doi/10.1126/sciadv.adk3039) | Nationwide InSAR processing and groundwater mechanism framing | Keep the product-lineage extension framing for Iran; do not overclaim it as independent truth. |
| [Nationwide urban ground deformation monitoring in Japan using Sentinel-1 LiCSAR products and LiCSBAS](https://link.springer.com/article/10.1186/s40645-020-00402-7) | Fully documented processing chain, QC, masking, filtering | Keep the Japan transfer path as a reproducible lineage extension with clear QC thresholds. |
| [Global land subsidence mapping reveals widespread loss of aquifer storage](https://www.nature.com/articles/s41467-023-41933-z) | Multi-region aggregation and training-data transparency | Use multi-region aggregation only when the underlying provenance is explicit. |

## Gaps Relative to the Comparators

1. The current stack is still stronger at lead-case closure than at full all-region closure.
2. The region-level and cell-level evidence is frozen, but a full all-region cell-level hierarchical model is still missing.
3. Multi-stratum controls exist now, but they still need to be integrated into a final manuscript-grade model family comparison.
4. The current package is DOI-ready, but the public repository DOI and version URL are still external-state blockers.
5. EGMS remains an upgrade path until a real CLMS token or equivalent external benchmark is available.

## Concrete Experiment Upgrades

### Priority 1: Final all-region hierarchical closure
- Freeze one model family ladder that includes summary-only, blocked/equal-area, hybrid anchor, and multi-stratum control variants.
- Report leave-one-out error and pooled OR for every family.
- Keep the candidate list fixed before the comparison.

### Priority 2: Multi-region technical validation
- Add region-by-region technical validation notes for observability masks, sign/unit, and provenance.
- Preserve weak-anchor and no-token labels instead of forcing them into the main claim.
- Make the mask thresholds and exposure cutoffs prespecified and reproducible.

### Priority 3: Exposure translation
- Expand the exposure story from counts to policy-facing metrics: people, built-up area, transport links, and infrastructure where available.
- Keep the land-cover stratification that Nature-family papers expect.

### Priority 4: External benchmark closure
- Treat EGMS/CLMS as the external gold-standard upgrade path.
- Do not label DOI-only citations as completed benchmark validation.
- If token access becomes available, use leave-one-region-out validation against the external benchmark.

## Bottom Line
- Nature-level standards are mostly about transparency, external validation, and a reproducible evidence ladder.
- Our current work is already past the “single-case only” stage.
- The next strengthening steps are to close the final all-region hierarchical model, tighten the technical validation story, and keep the external benchmark path explicit rather than implied.
