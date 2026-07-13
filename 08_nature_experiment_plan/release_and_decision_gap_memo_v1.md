# Release and Decision Gap Memo v1
Date: 2026-07-11

## Purpose
This memo converts the latest Nature-family scouting into a small set of concrete upgrades for the current manuscript package.

## What The New Comparator Set Emphasizes

### 1. Decision-facing exposure matrices
Recent Nature papers increasingly combine land motion with:
- population exposure,
- building exposure,
- infrastructure exposure,
- and a clear control/transfer status.

### 2. Release and technical validation are part of the contribution
Scientific Data and validation-heavy papers make the release package part of the scientific result:
- technical validation,
- reproducible metadata,
- clear versioning,
- and explicit data availability statements.

### 3. Multi-level exposure is now the norm
The strongest papers do not stop at:
- deformation rate,
- or even population-only exposure.
They extend to buildings, transport, and scenario-facing policy language.

## Gaps In Our Current Stack

| gap | current state | Nature-like target | next action |
|---|---|---|---|
| Decision-facing main table | exposure, infrastructure, and transfer pieces are separate | one main table that summarizes population, built-up, infrastructure, and transfer status | use `decision_facing_exposure_matrix_v1` as the main Results candidate |
| Explicit release statement | DOI-ready metadata exists, but the public DOI is not minted | release and versioning visible in the final data/code availability text | keep the finalizer ready and avoid hardcoding a fake DOI |
| Full all-region fit | closure-by-compilation exists | a true all-region cell-level fit or, failing that, a transparent limitation statement | keep the frozen closure-by-compilation package visible and separately label it |
| Infrastructure translation | lead-case transport is explicit, other regions remain incomplete | a clear infrastructure layer for the lead case with honest non-lead limitations | keep the lead-case roads/rail layer as the infrastructure anchor |
| Socioeconomic translation | GVI country-level vulnerability context is now frozen for the single-country cases, with SHDI as a contextual backup; a raster layer is still absent | a harmonized vulnerability / inequality companion layer | keep GVI as the conservative vulnerability fallback; use SHDI as backup; use GRDI first if access permits; nightlights remains proxy only |
| Socioeconomic gradient visibility | internal vulnerability spread is visible in the new comparison table | a reviewer-facing spread comparison across countries and layers | keep the GVI-vs-SHDI gradient comparison visible and cite the subnational spread summaries |
| Socioeconomic decision-facing table | GVI and SHDI are visible, but still split across trial files | one reviewer-facing comparison that makes the vulnerability gradient and country spread obvious | keep `socioeconomic_layer_gradient_comparison_v1` linked to the main decision-facing matrix and trial report |
| Structural vulnerability gap | GVI / SHDI capture contextual vulnerability, but not a separate structural-vulnerability layer | an explicit structural-vulnerability / inequality layer or an explicit gap statement | keep the new structural-vulnerability gap visible instead of folding it into GVI / SHDI context |
| Infrastructure-access inequality gap | Lead-case infrastructure translation exists, but no harmonized inequality layer is frozen | a separate access-inequality layer or an explicit gap note | keep the access-inequality gap separate from generic exposure or socioeconomic context |
| Structural vulnerability candidate shortlist | structural vulnerability is now a distinct comparator pattern, but no defensible layer is frozen | a short list of candidate sources / composites that could be trialed next | keep `structural_vulnerability_candidate_shortlist_v1` visible as the next upgrade entry point |
| Structural vulnerability trial plan | candidate sources exist, but the trial sequence is not yet executed | a prespecified trial plan and access matrix for globally harmonizable candidates | keep `structural_vulnerability_trial_plan_v1` and `structural_vulnerability_access_matrix_v1` visible as the next explicit work items |
| Structural vulnerability probe result | the global critical-infrastructure dataset is reachable but not yet decodable with the current lightweight stack | a geospatial parser or preprocessed region overlay | keep `structural_vulnerability_trial_report_v1` explicit as the current probe result |
| Structural vulnerability proxy summary | finite raster statistics are now extractable from the global critical-infrastructure dataset | a compact numeric proxy summary that can sit beside the decision-facing matrix | keep `structural_vulnerability_proxy_summary_v1` visible as the current numeric proxy layer |

## What To Do Next

1. Treat `decision_facing_exposure_matrix_v1` as the main exposure table candidate.
2. Keep `multi_region_infrastructure_translation_v1` as the infrastructure companion table.
3. Keep the closure-by-compilation package explicit, but do not pretend it is a new all-region fit.
4. Preserve the release package as DOI-ready, not DOI-minted.
5. Use `release_maturity_matrix_v1` to keep the Nature / Scientific Data release requirements explicit and auditable.
6. Use `socioeconomic_layer_candidate_v1` as the concrete shortlist for the next vulnerability-layer trial.
7. Use `socioeconomic_layer_trial_plan_v1` to define the actual GVI/SHDI/GRDI matching test before any manuscript integration.
8. Use `socioeconomic_layer_access_matrix_v1` to keep the access ranking honest: GVI is immediately reachable; SHDI is the contextual backup; GRDI is the preferred but access-gated upgrade.
9. Use `build_socioeconomic_layer_trial.py` as the executable scaffold that can ingest GVI or SHDI from public table pages or GRDI once files are staged.
10. Use `socioeconomic_layer_gradient_comparison_v1` to show the internal vulnerability gradient rather than only a national mean.
11. Use `structural_vulnerability_region_proxy_trial_v1` as the current region-aware structural-vulnerability proxy layer, but keep the approximation caveat explicit.

## Latest Structural-Vulnerability Status

- The critical-infrastructure source is now region-proxy-trialed with approximate frozen windows.
- The approximation caveat remains explicit and should stay visible until official polygons are available.
- This is still a proxy layer, not a final polygon-level closure.

## Bottom Line
The newest comparator papers make a simple point: Nature-ready exposure stories are not just about finding a signal, but about translating it into decision-facing tables and releasing it with a transparent validation story. The current package is close on translation, and `release_maturity_matrix_v1` shows that the local package is already strong on release plumbing, but public minting is still the only missing external step. `socioeconomic_layer_candidate_v1` now makes GVI the first concrete vulnerability-layer candidate to try, `socioeconomic_layer_trial_plan_v1` defines how that trial should be run, `socioeconomic_layer_access_matrix_v1` makes clear that GVI is immediately executable while SHDI is the backup and GRDI is access-gated, `socioeconomic_layer_gradient_comparison_v1` now makes the internal vulnerability gradient visible, and `build_socioeconomic_layer_trial.py` now actually retrieves GVI vulnerability context and SHDI country-level context from the public Global Data Lab table pages when requested. That comparison should stay attached to the decision-facing matrix so the socioeconomic layer reads as a reviewer-facing evidence block rather than a detached appendix. The newest comparator round also suggests that GVI / SHDI should not be treated as the final answer on vulnerability, because structural vulnerability and infrastructure-access inequality are now separate patterns in the literature. The right action is to keep them as explicit gaps unless a defensible public source can be trialed. The `structural_vulnerability_candidate_shortlist_v1` now gives the next upgrade step concrete candidate directions rather than leaving the gap abstract, and `structural_vulnerability_trial_plan_v1` with `structural_vulnerability_access_matrix_v1` turns that direction into a prespecified test rather than a vague future idea. The `structural_vulnerability_trial_report_v1` now records the first probe result: the dataset is reachable and globally relevant, but the current lightweight stack cannot yet decode its raster payloads into a usable region overlay. `structural_vulnerability_proxy_summary_v1` then moves that source one step further: it can produce finite numeric raster summaries, so it is now a real proxy candidate rather than just a downloadable archive. Until a geospatial parser or preprocessed overlay is added, that source should remain a numeric proxy layer rather than being promoted into the main evidence stack.
