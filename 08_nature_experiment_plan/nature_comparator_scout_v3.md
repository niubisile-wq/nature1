# Nature Comparator Scout v3
Date: 2026-07-11

## Why this scout

This note refreshes the comparator set with the newest Nature-family and Scientific Data papers that are most relevant to the current exposure/subsidence manuscript stack. The goal is not just to cite them, but to convert their patterns into concrete experiment upgrades.

## Comparator patterns from the newest papers

### 1. Decision-facing tables are now the core deliverable
Recent Nature-family papers increasingly make the main table do more than report a signal. They translate motion or hazard into:
- population exposure,
- built-up exposure,
- infrastructure/building risk,
- transfer or control status,
- and a clear policy-facing interpretation.

This is visible in:
- `European coastal deformation drives unequal exposure to climate hazards`
- `Land subsidence risk to infrastructure in US metropolises`
- `Building damage risk in sinking Indian megacities`
- `Global subsidence of river deltas`

### 2. Vulnerability and inequality are now explicit, not implied
The strongest recent comparator papers do not stop at physical hazard translation. They explicitly connect exposure to:
- socioeconomic inequality,
- human development,
- vulnerability gradients,
- and differential burden across places or groups.

This is visible in:
- `Inequality in human development amplifies climate-related disaster risk`
- `Multi-hazard exposure disproportionately affects vulnerable ...`
- `A vulnerability perspective on loss and damage`
- `The geography of structural vulnerability`

### 3. Infrastructure translation is now a reviewer expectation
The infrastructure-oriented papers now make the hazard-to-relevant-asset step explicit:
- buildings,
- roads,
- rail,
- levees,
- reservoirs,
- or other decision-facing infrastructure classes.

This is visible in:
- `Land subsidence risk to infrastructure in US metropolises`
- `Present-day land subsidence risk in the metropolitan cities of Italy`
- `Satellite-based vertical land motion for infrastructure monitoring`
- `Coastal land subsidence accelerates timelines for future flood ...`

### 4. Data and release transparency are part of the scientific contribution
The strongest validation/data papers treat release and metadata as first-class scientific outputs:
- technical validation,
- reproducible provenance,
- versioning,
- repository-ready data packaging,
- and explicit data availability statements.

This is visible in Scientific Data papers such as:
- `Projections of climate change vulnerability along the Shared Socioeconomic Pathways`
- `GNSS land subsidence observations along the northern coastline of Java, Indonesia`
- `DeltaDTM: A global coastal digital terrain model`
- `Seismic resilience of urban networks: dataset for infrastructure ...`

## What these patterns mean for the current stack

### A. The decision-facing exposure matrix should remain the main table
The current `decision_facing_exposure_matrix_v1` is aligned with the newest comparator pattern, but it should keep the socioeconomic snapshot attached so the exposure story is not separated from vulnerability.

### B. The socioeconomic layer is now a real companion layer, not a side note
The frozen GVI / SHDI comparison and the GVI gradient comparison are now sufficient to justify a reviewer-facing socioeconomic context block. The current state still does not support a full raster upgrade, so the manuscript should continue to label GRDI as the preferred future upgrade rather than implied current coverage.

### C. Infrastructure translation should stay lead-case only
The current infrastructure layer is strongest for the lead case. That is consistent with the comparator literature, which usually keeps the infrastructure layer explicit and limited rather than pretending every region has the same support.

### D. Full all-region closure still needs honest labeling
The current closure-by-compilation package is valuable, but it is not equivalent to a fresh all-region cell-level fit. The comparator set reinforces the need to keep that limitation explicit.

## Concrete upgrade actions

1. Keep `decision_facing_exposure_matrix_v1` as the main Results/Extended Data candidate.
2. Keep `socioeconomic_layer_gradient_comparison_v1` attached to the decision-facing matrix so the vulnerability gradient is visible in the same evidence stack.
3. Preserve `multi_region_infrastructure_translation_v1` as the lead-case infrastructure companion table.
4. Keep `full_all_region_hierarchical_closure_v1` explicitly labeled as closure-by-compilation until a true all-region cell-level fit exists.
5. Continue to treat GRDI as the preferred socioeconomic raster upgrade, but keep SHDI and GVI as the current honest operational layers.
6. Keep the release package DOI-ready, not DOI-minted, until the external publication step is complete.
7. Treat EGMS/CLMS as a separate external benchmark closure path, not as something that DOI alone can replace.

## Most relevant comparator links

- [Inequality in human development amplifies climate-related disaster risk](https://www.nature.com/articles/s41467-026-73873-9)
- [European coastal deformation drives unequal exposure to climate hazards](https://www.nature.com/articles/s43247-026-03190-y)
- [Land subsidence risk to infrastructure in US metropolises](https://www.nature.com/articles/s44284-025-00240-y)
- [Multi-hazard exposure disproportionately affects vulnerable ...](https://www.nature.com/articles/s43247-026-03652-3)
- [Projections of climate change vulnerability along the Shared Socioeconomic Pathways](https://www.nature.com/articles/s41597-025-05732-z)
- [Global subsidence of river deltas](https://www.nature.com/articles/s41586-025-09928-6)
- [Building damage risk in sinking Indian megacities](https://www.nature.com/articles/s41893-025-01663-0)
- [The geography of structural vulnerability](https://www.nature.com/articles/s42949-025-00264-2)

## Bottom line

The newest comparator set reinforces the same strategic direction: the current package is strongest when it is framed as a decision-facing exposure story with a visible socioeconomic gradient, explicit infrastructure translation, and honest release status. The remaining work is not to add more vague layers, but to close the true all-region fit, preserve the lead-case infrastructure translation, and keep the socioeconomic gradient comparison attached to the main matrix so it reads as evidence rather than decoration.
