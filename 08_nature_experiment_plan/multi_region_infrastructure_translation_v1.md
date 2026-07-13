# Multi-Region Infrastructure Translation v1
Date: 2026-07-11

## Purpose
This note freezes the current infrastructure-exposure evidence and makes the lead-case transport layer explicit. It follows the Nature-family pattern that subsidence should be translated into buildings, roads, rail, and decision-facing exposure, not just deformation rates.

## Comparator Pattern
- Nature Cities now regularly turns subsidence into infrastructure damage risk.
- Scientific Reports infrastructure-roadmap papers now present a meter-scale or tens-of-meter-scale VLM product plus a decision-oriented roadmap.
- The strongest comparator papers keep the transport/infrastructure layer separate from population exposure and make the risk translation explicit.

## Evidence Used
- `03_exposure_closure/chao_phraya_osm_exposure_censoring/chao_phraya_osm_exposure_censoring_summary.csv`
- `03_exposure_closure/chao_phraya_osm_exposure_censoring/chao_phraya_osm_exposure_censoring_report.md`
- `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/chao_phraya_area_weighted_exposure_report.md`
- `08_nature_experiment_plan/multi_region_exposure_translation_v1.csv`
- `08_nature_experiment_plan/benchmark_sign_unit_audit_v1.md`
- `08_nature_experiment_plan/multi_region_technical_validation_v1.md`

## Infrastructure Translation Table

| region | infrastructure layer | key infrastructure metric | interpretation |
|---|---|---|---|
| Chao Phraya | available | transport_hidden_fraction_mean `0.534`; median `0.531`; min `0.303`; max `0.699`; major roads `17457`; railways `1353` | The lead case now has a measurable transport infrastructure layer, and more than half of the transport exposure is hidden on average by observability censoring. |
| Po | not yet translated | infrastructure proxy missing | The signal is present in population and built-up area, but the transport layer has not yet been built with the same rigor. |
| Brantas | not yet translated | infrastructure proxy missing | Built-up and population exposure exist, but a transport-risk layer is still missing. |
| Indus | not yet translated | infrastructure proxy missing | Statistical signal exists, but the infrastructure layer is still incomplete. |
| Rhone | not yet translated | infrastructure proxy missing | Candidate upgrade case only. |
| Rhine | not yet translated | infrastructure proxy missing | Control/specification case. |

## Why This Matters

The current package now matches the comparator logic more closely:

1. Nature-style infrastructure risk papers do not stay at a general subsidence raster; they name the buildings or transport assets exposed.
2. Our lead case now does the same for roads and rail.
3. Keeping the other regions marked as not yet translated is better than inflating the claim.

## Next Upgrade

- Expand the infrastructure layer beyond Chao Phraya if equivalent asset data become available.
- Keep the current transport summary frozen as the lead-case infrastructure anchor.
- Fold this note into the manuscript exposure discussion as the infrastructure-specific companion to the population / built-up translation.
