# Benchmark Sign and Unit Audit v1
Date: 2026-07-10

## Purpose

This note freezes the sign and unit conventions for all deformation layers used in the current manuscript package.

## Working Conventions

1. All delta VLM / LiCSBAS velocity layers are stored in `mm/yr`.
2. Negative velocity means subsidence or downward motion.
3. Positive velocity means uplift or upward motion.
4. No product is treated as independent truth unless an external anchor exists and is documented.
5. Product-lineage extensions must not be mislabeled as independent benchmarks.

## Region-by-Region Audit

### Po

- Source: delta VLM benchmark.
- Unit: `mm/yr`.
- Sign: negative indicates subsidence.
- Current interpretation: positive observability-bias signal, but EGMS closure still pending.

### Chao Phraya

- Source: delta VLM benchmark.
- Unit: `mm/yr`.
- Sign: negative indicates subsidence.
- Current interpretation: primary lead case with strong positive signal and high hidden-exposure share.

### Indus

- Source: delta VLM benchmark.
- Unit: `mm/yr`.
- Sign: negative indicates subsidence.
- Current interpretation: strong statistical signal, but weak independent anchor.

### Rhone

- Source: delta VLM benchmark.
- Unit: `mm/yr`.
- Sign: negative indicates subsidence.
- Current interpretation: positive signal and a candidate EGMS upgrade path.

### Brantas

- Source: delta VLM benchmark.
- Unit: `mm/yr`.
- Sign: negative indicates subsidence.
- Current interpretation: positive signal with weak-anchor sensitivity.

### Rhine

- Source: delta VLM benchmark.
- Unit: `mm/yr`.
- Sign: negative indicates subsidence.
- Current interpretation: control/specification case.

### Japan Niigata

- Source: LiCSBAS selective probe.
- Unit: `mm/yr`.
- Sign: negative indicates subsidence.
- Current interpretation: product-lineage extension only.

### Iran nationwide InSAR

- Source: processed Zenodo InSAR companion dataset.
- Unit: `mm/yr` for the rate layer, pending full legend cross-check.
- Sign: the readable rate file is not yet fully cross-checked against the paper legend; do not overstate sign semantics.
- Current interpretation: product-lineage extension only.

### EGMS Rescue Pack

- Source: API query pack.
- Unit: not applicable.
- Sign: not applicable.
- Current interpretation: ready for execution once CLMS credentials are available.

## Manuscript Rule

When a result is presented in the paper, its unit and sign convention must be traceable to one of the audited layers above. If the convention is still ambiguous, the result stays in the supplement until resolved.
