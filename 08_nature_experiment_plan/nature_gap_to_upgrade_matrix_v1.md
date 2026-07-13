# Nature Gap-to-Upgrade Matrix v1
Date: 2026-07-11

## Purpose
This matrix converts the current Nature scouting notes into concrete experiment upgrades. It is meant to keep the work aligned with Nature-family standards instead of drifting into ad hoc expansion.

## Comparator Pattern Summary
- High-resolution geophysical layer
- Independent validation where possible
- Exposure / risk translation
- Land-cover or settlement stratification
- Uncertainty bounds and leave-one-out checks
- Transparent data and code release
- Technical validation for dataset-oriented work

## Current Gaps and Upgrades

| Gap area | Nature-family standard | Current local status | Upgrade to do next | Priority |
|---|---|---|---|---|
| Full all-region hierarchical closure | Compare candidate model families with prespecified validation and report the strongest family with leave-one-out error | `hierarchical_model_v1` exists, and a closure-by-compilation package now exists in `full_all_region_hierarchical_closure_v1` | Keep the family list frozen, mirror the closure-by-compilation package, and note explicitly that a new all-region fit is still not yet available | P1 |
| Multi-stratum controls | Show that the claim survives land-cover, built-up, hidden-share, and anchor controls | A frozen control ladder now exists in `multi_region_stratified_control_closure_v1` | Promote the stratified control ladder into the manuscript evidence stack and make it part of the main model-family comparison | P1 |
| Multi-region technical validation | Provide reviewer-reusable technical validation for dataset-like artifacts | Observability masks and sign/unit audits now exist inside a consolidated technical-validation package | Keep the package fixed, add it to the manuscript evidence stack, and preserve weak-anchor labels explicitly | P1 |
| Exposure translation breadth | Translate the hazard into people, infrastructure, built-up area, or policy-facing exposure metrics | Lead-case exposure, building/transport, and region-level exposure summaries exist | Promote the new multi-region exposure translation package, infrastructure translation package, and decision-facing exposure matrix into the manuscript evidence stack | P1 |
| External benchmark closure | Use an independent benchmark when available, and state limitations if not | EGMS/CLMS remains blocked by token access | Keep EGMS as the external upgrade path and ensure DOI-only citation is not mistaken for benchmark closure | P1 |
| Publication-ready data release | Provide persistent data and code access, with a clear minimum dataset | DOI-ready metadata and finalizer exist; public DOI is still external | Keep the repository release candidate ready, pair it with the release-gap memo, and group the evidence with a manuscript-ready package note | P1 |
| Socioeconomic vulnerability translation | Add vulnerability / inequality context if a clean public layer can be harmonized | No frozen socioeconomic layer is currently present in the local stack | Identify a harmonized socioeconomic layer or keep the gap explicit if only coarse context is available | P2 |
| Socioeconomic vulnerability translation | Add vulnerability / inequality context if a clean public layer can be harmonized | GVI country-level vulnerability context has now been frozen for the single-country cases, with SHDI as a contextual backup and visible subnational gradients, but a raster layer is still absent | Upgrade the GVI fallback into a finer subnational or raster layer only if a clean public source can be defended | P2 |
| Socioeconomic layer candidate selection | Prefer a globally harmonized raster layer before a coarse contextual fallback | GVI has been identified as a strong public vulnerability candidate, with GRDI as the raster upgrade and SHDI/nightlights as fallbacks | Trial GVI first; if needed, use SHDI for context and nightlights only as proxy | P2 |
| Socioeconomic layer trial | Test whether the GVI/SHDI/GRDI layer can be attached without overclaiming | Trial plan is frozen, and GVI country-level vulnerability values plus subnational gradients have now been retrieved from the public Global Data Lab table pages | Execute the GRDI matching test and keep the outcome either as an attached layer or an explicit gap | P2 |
| Socioeconomic layer access matrix | Distinguish immediately reachable sources from access-gated upgrades | GVI is reachable now; SHDI is the contextual backup; GRDI is preferred but access-gated via Earthdata Search / EDL | Start with GVI as executable fallback, keep SHDI as backup, then upgrade to GRDI once access is available | P2 |
| Socioeconomic gradient comparison | Show internal vulnerability spread instead of only national means | A reviewer-facing GVI-vs-SHDI gradient comparison table now exists | Keep the gradient comparison visible and use it to justify the vulnerability-layer choice | P2 |

## Evidence-Rich Patterns To Copy

### 1. Nature Communications coastal subsidence papers
- Use geophysical measurements plus explicit exposure translation.
- Add uncertainty bounds and scenario framing.
- Make validation and limitations visible.

### 2. Scientific Data descriptors
- Provide methods, technical validation, and a release package that reviewers can inspect.
- Keep the data and code statements explicit and persistent.

### 3. Multi-city / multi-region risk papers
- Do not stop at a single lead case.
- Add a region-level or city-level comparison that shows the result is not a local artifact.

### 4. Comparator refresh v3
- The newest comparator set again reinforces the same pattern: the main deliverable is a decision-facing exposure table, not a standalone hazard raster.
- The socioeconomic gradient should sit next to the exposure matrix so reviewers can see the vulnerability context rather than infer it from prose.
- Infrastructure translation should remain explicit and limited to what is actually frozen.

### 5. Comparator refresh v4
- The newest comparator set pushes one layer deeper: vulnerability is increasingly treated as structural, not merely socioeconomic.
- Infrastructure access inequality is now a distinct discussion from generic exposure.
- The current GVI / SHDI layer should therefore be treated as vulnerability context, not as a fully closed structural-vulnerability layer.

### 6. Comparator refresh v5
- The newest comparator scan now makes the missing structural-vulnerability layer explicit.
- A structural-vulnerability context gap should be tracked separately from the GVI / SHDI context layer.
- Infrastructure-access inequality should stay a separate candidate, not a hidden synonym for socioeconomic context.

## What This Means For Our Stack
- The current stack already satisfies the single-case plus robustness baseline.
- The current stack should keep `decision_facing_exposure_matrix_v1` and `socioeconomic_layer_gradient_comparison_v1` attached, because the latest comparator set makes vulnerability context part of the main evidence stack rather than a separate appendix.
- The current stack should also carry an explicit structural-vulnerability gap note, because the latest comparator set makes structural vulnerability and infrastructure access inequality distinct from the current GVI / SHDI context layer.
- The current stack should carry a dedicated structural-vulnerability context gap note, because the latest comparator set makes structural vulnerability and infrastructure access inequality distinct from the current GVI / SHDI context layer.
- The next real strength gain comes from a full all-region hierarchical closure and the integrated control ladder.
- The work should stay prespecified: no repeated optimization on the same validation set, and no hidden p-hacking through uncontrolled module rotation.

## Next Execution Steps
1. Fold `multi_region_stratified_control_closure_v1` into the manuscript evidence stack.
2. Build the final all-region hierarchical closure from the frozen model families already on disk, following `full_all_region_hierarchical_closure_v1.md`; keep the closure-by-compilation package visible until a true all-region fit exists.
3. Add region-by-region technical validation notes for observability masks and provenance.
4. Keep the EGMS external benchmark path explicit and separate from completed internal validation.

## Structural Vulnerability Update

The structural-vulnerability source is now beyond the original probe and proxy-summary stages: it can be cropped into approximate region windows and treated as a frozen region-proxy trial. The remaining gap is official polygon geometry, not basic readability or numeric extractability. Keep the approximation caveat explicit if this layer is discussed in the manuscript.
