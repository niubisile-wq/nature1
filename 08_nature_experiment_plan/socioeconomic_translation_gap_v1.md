# Socioeconomic Translation Gap v1
Date: 2026-07-11

## Why This Gap Matters
Recent Nature-family papers increasingly show that hazard exposure alone is not enough. The strongest papers now combine physical risk with socioeconomic inequality, human development, infrastructure access, or vulnerability-to-displacement style measures.

## Comparator Signals
- `Inequality in human development amplifies climate-related disaster risk` shows that lower human development is associated with disproportionately higher human losses and relative economic losses in climate disasters.
- `Socioeconomic predictors of vulnerability to flood-induced displacement` shows that vulnerability varies by orders of magnitude within and between countries, and that socioeconomic predictors matter at national and subnational scale.
- `Inequality in infrastructure access and its association with health` emphasizes that infrastructure inequality is itself a measurable exposure dimension.
- `Global patterns of inequality in pedestrian shade provision` shows how Nature-family work increasingly connects built-environment structure to social inequality.

## Current Local State
- The current stack is strong on:
  - population exposure,
  - built-up exposure,
  - transport / infrastructure translation,
  - transfer / control status,
  - technical validation,
  - and release readiness.
- The current stack now includes a frozen GVI country-level vulnerability table for the single-country cases, plus SHDI as a contextual backup.
- The current stack still does **not** include a true raster-level socioeconomic vulnerability layer.
- The dataset inventory currently includes GHSL, WorldCover, OSM infrastructure, GNSS, LiCSAR/LiCSBAS probes, and release scaffolding, but no dedicated socioeconomic deprivation / HDI / wealth / inequality raster or harmonized subnational table.

## Nature-Like Upgrade Target
Add a socioeconomic translation layer that can be attached to the decision-facing exposure matrix:

1. Prefer a spatially harmonized socioeconomic dataset if a matched open source can be obtained.
2. If only coarse administrative data are available, keep it as a clearly labeled contextual layer rather than pretending it is pixel-accurate.
3. Use it as a vulnerability companion to the existing population / built-up / infrastructure exposure stack.
4. Keep lead case, benchmark case, and control case labels explicit.

## Next Concrete Actions
1. Decide whether the GVI country-level companion should remain the fallback or be upgraded into a finer subnational / raster layer.
2. Try to resolve the Rhine multi-country basin policy before forcing a basin-level socioeconomic summary.
3. If a matched open raster source can be obtained, treat it as the upgrade path; otherwise keep GVI as the conservative vulnerability layer and SHDI as the contextual backup.
4. Keep the gap memo explicit if the layer remains only country-level, so the manuscript does not overclaim social vulnerability coverage.

## Bottom Line
The next Nature-grade strengthening opportunity is not another deformation metric. It is to upgrade the now-frozen GVI country-vulnerability layer into a finer socioeconomic vulnerability translation layer, or to explicitly document why the country-context fallback is the strongest defensible option.
