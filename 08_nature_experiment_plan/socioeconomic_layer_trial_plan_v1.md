# Socioeconomic Layer Trial Plan v1
Date: 2026-07-11

## Objective
Test whether a harmonized socioeconomic vulnerability layer can be attached to the current decision-facing exposure matrix without overclaiming resolution or reviewability.

## Preferred Candidate
- Primary: GVI v1.1 from Global Data Lab.
- Fallback: SHDI v10.2 from Global Data Lab.
- Raster upgrade: GRDI v1 from NASA Earthdata / SEDAC.
- Proxy fallback only: nightlights.

## Trial Design

### Phase 1: Raster harmonization
1. Download or stage the GRDI raster.
2. Reproject to the same equal-area grid used for exposure closure.
3. Compute region-level summaries for the current region set.
4. Compute strong-subsidence-cell summaries for the lead case.
5. Compare the socioeconomic score against population, built-up, and infrastructure exposure.

### Phase 2: Defensive fallback
1. If GRDI harmonization is weak, use GVI as the primary public vulnerability companion table.
2. If GVI is too coarse or unavailable for a basin context, use SHDI as a region-level contextual backup.
3. Keep the table at country / subnational-unit scale rather than forcing a pixel map.
4. Use nightlights only as a last-resort proxy if neither GVI nor SHDI is clean enough.

### Phase 3: Manuscript integration rule
Only add the socioeconomic layer to the main evidence stack if:
- the source can be cited cleanly,
- the harmonization is reproducible,
- the layer can be labeled honestly as raster or contextual,
- and the trial improves the decision-facing story rather than bloating it.

## Executed Outputs
- `socioeconomic_layer_access_matrix_v1.csv`
- `socioeconomic_layer_region_map_v1.csv`
- `socioeconomic_layer_gvi_country_context.csv`
- `socioeconomic_layer_gvi_subnational_spread.csv`
- `socioeconomic_layer_shdi_country_context.csv`
- `socioeconomic_layer_shdi_subnational_spread.csv`
- `socioeconomic_layer_gradient_comparison_v1.csv`
- `socioeconomic_layer_gradient_comparison_v1.md`
- `socioeconomic_layer_trial_report.md`
- `socioeconomic_layer_trial_meta.json`
- mirrored copies in `11_submission_ready_v1/source_data/socioeconomic_layer_trial_v1/`

## Result Summary
- GVI country-level vulnerability values were successfully retrieved from the public Global Data Lab table pages for the single-country cases.
- GVI subnational spread summaries were also retrieved, so the vulnerability layer now shows within-country gradients rather than only national points.
- SHDI country-level context was successfully retrieved from the public Global Data Lab table pages for the single-country cases:
  - Italy, Thailand, Indonesia, India basin proxy, France
- SHDI subnational spread summaries were also retrieved as a backup comparison layer.
- The country-level GVI values are now frozen into the trial report and the release bundle mirror.
- The country-level SHDI values remain as a secondary contextual backup.
- The gradient comparison table now makes the vulnerability spread explicit by reporting national values, subnational min/median/max, and relative spread for both GVI and SHDI.
- Rhine remains unresolved as a multi-country basin context and is deliberately not forced into a fake single-country mapping.
- GRDI is still the preferred raster upgrade, but it remains access-gated and is not required for the current trial to be useful.

## Remaining Gaps
- Multi-country basin aggregation policy for Rhine remains unresolved.
- GVI still has only country-level values here; it is not yet a basin-specific socioeconomic raster.
- GRDI raster ingestion remains future work.
- Nightlights remains a fallback only if a future upgrade needs a simpler proxy layer.

## Expected Outputs
- `socioeconomic_layer_trial_report_v1.md`
- `socioeconomic_layer_trial_report_v1.csv`
- optional figure / appendix note if the trial is strong enough

## Decision Rule
- If GRDI aligns cleanly, promote it as the raster socioeconomic upgrade.
- If GVI is the strongest publicly reachable option, use it as the preferred vulnerability companion table.
- If only SHDI is workable, keep the layer as region-level context and do not present it as pixel-level truth.
- If neither layer is defensible, keep `socioeconomic_translation_gap_v1` explicit and do not fake closure.

## Bottom Line
The trial now has a frozen GVI country-level vulnerability result, an SHDI country-context backup, and subnational spread summaries for both, so it is no longer a blank scaffold.
The new gradient comparison table makes the vulnerability translation more Nature-like by exposing within-country spread rather than only national means.
GRDI remains the concrete raster upgrade target, but the current socioeconomic companion layer is already usable as a conservative vulnerability/context fallback rather than a pretend pixel truth.
