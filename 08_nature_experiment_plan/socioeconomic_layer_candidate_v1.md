# Socioeconomic Layer Candidate v1
Date: 2026-07-11

## Candidate Shortlist

### 1. Global Gridded Relative Deprivation Index (GRDI), Version 1
- Source: NASA Earthdata / SEDAC
- Coverage: global, 30 arc-second (~1 km) raster
- Meaning: multidimensional deprivation and poverty, indexed 0 to 100
- Official page details: GRDI v1 is built from sociodemographic and satellite inputs that were spatially harmonized, indexed, and weighted into six main components, with temporal extent 2010-01-01 to 2020-12-31 and global spatial extent.
- Why it is strong:
  - globally harmonized
  - already gridded
  - directly relevant to vulnerability / inequality translation
  - can be aligned with the current raster-based exposure stack

### 2. GDL Vulnerability Index (GVI)
- Source: Global Data Lab
- Coverage: countries and regions, with historical and projected vulnerability values
- Meaning: socioeconomic vulnerability to climate change and related shocks
- Official page details: GVI v1.1 is a composite index designed to monitor and project socioeconomic vulnerability, with historical data and SSP projections available from the Global Data Lab site.
- Why it is useful:
  - directly aligned with the vulnerability translation question
  - public and immediately reachable
  - can act as a more targeted contextual companion than SHDI

### 3. Subnational Human Development Index (SHDI)
- Source: Global Data Lab
- Coverage: subnational administrative units across many countries
- Meaning: education, health, and standard of living dimensions
- Official page details: SHDI v10.2 exposes human development, health index, educational index, income index, and related socioeconomic tables at subnational scale.
- Why it is useful:
  - strong contextual fallback
  - useful when a vulnerability-specific index is not enough or needs backup
  - can support region-level narrative even where pixel matching is weak

### 4. Nightlights as a proxy layer
- Sources: World Bank Open Night Lights / harmonized nightlight products
- Coverage: global, raster, repeatable
- Meaning: proxy for economic activity / electrification / settlement intensity
- Why it is only secondary:
  - it is a proxy, not a direct vulnerability measure
  - useful if GRDI access or harmonization fails

## Recommendation

The preferred next-layer candidate is now GVI, because it is a public vulnerability index and the clearest fit for a decision-facing vulnerability companion layer.

If GVI cannot be integrated cleanly, SHDI should be used as a region-level companion table instead of forcing an unconvincing raster overlay.

GRDI remains the preferred raster upgrade once access permits.

Nightlights should remain a proxy fallback, not the primary socioeconomic layer.

## Nature-Like Use Pattern

The best comparator papers do not simply add another metric. They translate hazard exposure into a vulnerability or inequality context that can be defended in review.

The practical target is therefore:

1. lead-case vulnerability alignment with GVI if feasible,
2. benchmark-region contextual comparison with SHDI if needed,
3. raster upgrade with GRDI if access becomes available,
4. proxy fallback with nightlights only if the stronger options fail.

## Bottom Line

GVI is now the best concrete next candidate for a socioeconomic vulnerability layer. GRDI remains the best raster upgrade, but GVI is the first open layer in this workstream that is clearly tight enough to freeze into the experiment plan.
