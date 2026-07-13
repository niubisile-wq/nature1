# Decision-Facing Exposure Matrix v1
Date: 2026-07-11

## Purpose
This note consolidates the current exposure evidence into one decision-facing matrix. It is meant to match the current Nature pattern: translate subsidence into people, built-up area, and infrastructure exposure, then state where transfer and benchmark closure remain open.

## Comparator Pattern
- European coastal deformation work now combines land motion with land-cover and population/socioeconomic exposure.
- Infrastructure-focused Nature Cities work translates subsidence into buildings and damage-risk classes.
- The stronger papers keep lead case, transfer case, and control case separate.

## Decision Matrix

| region | population | built-up | infrastructure | transfer status | decision readiness | key frozen evidence |
|---|---|---|---|---|---|---|
| Chao Phraya | available | available | available | lead case | strongest current case | population not-majority observable `0.170`; built-up not-majority observable `0.326`; transport hidden fraction median `0.531`; transport mean hidden fraction `0.534` |
| Po | available | available | not yet translated | regional benchmark | conditional go after EGMS | population not-majority observable `0.340347`; built-up not-majority observable `0.460331`; OR `1.32894` |
| Brantas | available | available | not yet translated | regional benchmark | statistical signal, infrastructure gap remains | population not-majority observable `0.145903`; built-up not-majority observable `0.175993`; OR `1.59171` |
| Indus | proxy only | proxy only | not yet translated | regional benchmark | statistical signal, weak anchor | OR `3.3894`; risk proxy `2.3894` |
| Rhone | proxy only | proxy only | not yet translated | regional benchmark | conditional upgrade case | OR `1.59178`; risk proxy `0.591777` |
| Rhine | proxy only | proxy only | not yet translated | control/specification | control / negative case | OR `0.810149`; risk proxy `-0.189851` |

## Exposure Completeness Score

This score is a simple bookkeeping aid, not a statistical metric.

- Chao Phraya: `3 / 3`
- Po: `2 / 3`
- Brantas: `2 / 3`
- Indus: `1 / 3`
- Rhone: `1 / 3`
- Rhine: `1 / 3`

## Socioeconomic Context Snapshot

This companion snapshot is not a substitute for the exposure matrix. It records the frozen GVI vulnerability layer and its internal spread so the decision-facing table can be read together with a socioeconomic context layer.

| region | GVI national | GVI spread | GVI rel. spread | SHDI national | socioeconomic note |
|---|---|---|---|---|---|
| Chao Phraya | `32.3` | `4.4` | `13.6%` | `0.798` | lead-case vulnerability context is relatively compact |
| Po | `25.2` | `12.2` | `48.4%` | `0.915` | stable benchmark with moderate internal spread |
| Brantas | `39.5` | `26.0` | `65.8%` | `0.728` | stronger vulnerability gradient than Po |
| Indus | `48.3` | `26.5` | `54.9%` | `0.685` | higher vulnerability context, still treated as proxy |
| Rhone | `23.6` | `19.7` | `83.5%` | `0.920` | wide internal spread despite low national mean |
| Rhine | unresolved | unresolved | unresolved | unresolved | multi-country basin context remains open |

## Why This Matters

1. The matrix makes explicit which regions already support the people + built-up story.
2. It also shows which regions still lack a transport/infrastructure layer.
3. It now also shows a vulnerability context layer, which is closer to the current Nature papers than keeping exposure evidence split across separate memos.

## Next Upgrade

- Add a socioeconomic layer if a frozen source becomes available.
- Keep the transfer and control labels explicit so the matrix does not overclaim.
- Keep the GVI-vs-SHDI gradient comparison attached to this matrix so the vulnerability layer reads as part of the evidence stack.
- Add an explicit structural-vulnerability gap note so the GVI / SHDI context is not mistaken for a closed inequality layer.
- Keep infrastructure-access inequality as a separate gap, not a synonym for socioeconomic context.
- Use `structural_vulnerability_candidate_shortlist_v1` as the next explicit upgrade entry point if a defensible source can be trialed.
- Use `structural_vulnerability_trial_plan_v1` and `structural_vulnerability_access_matrix_v1` to keep the next trial prespecified and globally defensible.
- Use `structural_vulnerability_trial_report_v1` as the current probe result: reachable archive and numeric summaries.
- Use `structural_vulnerability_proxy_summary_v1` as the current numeric proxy layer.
- Use `structural_vulnerability_region_proxy_trial_v1` as the current region-aware proxy layer, but keep the approximation caveat explicit.
- Treat the critical-infrastructure source as numeric-proxy-usable and region-proxy-trialed, but not yet finalized as an official polygon-level layer.
- Use this note as the main table for exposure-related Results/Extended Data drafting.

## Structural Vulnerability Update

The critical-infrastructure source is now best treated as the current region-aware structural-vulnerability companion layer. It has crossed from archive-readiness to numeric proxy to approximate region-proxy trial, and the approximation caveat should stay explicit until official polygons are available.
