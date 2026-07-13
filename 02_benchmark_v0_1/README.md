# Open InSAR Observability Bias and Exposure Benchmark v0.1

## Scope

This is a local, reproducible benchmark scaffold for testing whether open InSAR observability gaps censor land-subsidence exposure estimates.
It is not yet a final Nature-grade dataset because dense independent EGMS benchmark closure is still pending.

## Core metrics

- `observability_bias_signal`: land-cover-adjusted strong-subsidence effect on public-product failure probability.
- `bias_or_minus_one_proxy`: first-pass proxy for extra observability failure associated with strong subsidence.
- `independent_anchor_status`: whether sparse NGL GNSS anchors exist in the AOI.
- `egms_status`: whether a high-density European EGMS benchmark query is ready.
- `nature_readiness`: current publication-readiness classification.

## Current result

- Primary regions assessed: `6`
- Positive or strong-positive observability-bias signals: `5`
- Conditional Nature leads after EGMS closure: `2`
- External expansion candidates: `4`

## Files

- `benchmark_region_evidence_v0_1.csv`: one row per primary delta/case.
- `benchmark_external_candidates_v0_1.csv`: NGL-screened expansion cases plus selected Japan probe status.
- `benchmark_dataset_inventory_v0_1.csv`: source and derived dataset inventory.
- `benchmark_manifest_v0_1.json`: machine-readable provenance and gate status.
- `benchmark_v0_1_report.md`: human-readable decision report.

## Immediate blocker

Nature-level closure requires executing the prepared EGMS API queries with a CLMS token and adding the resulting EGMS L3 ORTHO-UP product manifests and derived validation layers.
