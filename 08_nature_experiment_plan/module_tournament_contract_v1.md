# Module Tournament Contract v1
Date: 2026-07-10

## Purpose

This contract freezes the candidate-module tournament before any additional optimization runs are performed. The goal is to improve the Nature-standard evidence stack without p-hacking or hidden validation leakage.

## Fixed Rules

1. Candidate families must be listed before running the tournament.
2. Training, tuning, and frozen validation sets must remain fixed during a tournament round.
3. Any winner chosen on tuning data must be re-evaluated once on the frozen validation set.
4. Every attempt must be logged, including rejected variants and null outcomes.
5. Final reporting must include corrected p-values or permutation-adjusted family-wise error control.

## Frozen Region Roles

### Discovery

- Chao Phraya
- Brantas

### Tuning

- Po
- Held-out Chao Phraya spatial blocks

### Frozen Validation

- Rhone
- Rhine
- Held-out Chao Phraya spatial blocks not used in tuning

### External Transfer

- Japan Niigata
- Iran nationwide InSAR

## Frozen Candidate Families

### Observability

- threshold: 0.2
- threshold: 0.3
- threshold: 0.4
- rule: any observable
- rule: majority observable
- rule: stable-75
- rule: obs fraction < 0.25
- rule: never observable

### Deformation

- strong threshold: 3 mm/yr
- strong threshold: 5 mm/yr
- strong threshold: 10 mm/yr
- signed subsidence only
- absolute motion magnitude

### Exposure

- population
- built-up
- roads
- rail
- cropland
- irrigation proxy

### Control

- WorldCover only
- WorldCover + population density
- WorldCover + built-up
- WorldCover + temporal density
- product-lineage random intercept

### Spatial

- no block
- 5-cell block
- 10-cell block
- 25-cell block
- AOI-level bootstrap

### Transfer

- leave-one-region-out
- train on delta VLM, test on Japan
- train on delta VLM, test on Iran
- product-lineage split

## Acceptance Thresholds

The tournament is not considered successful unless at least one candidate stack satisfies all of the following:

- positive effect direction in tuning;
- non-degenerate frozen validation result;
- no control/specification case that reproduces the same claim;
- corrected significance or clearly bounded uncertainty;
- reproducible source-data ledger row.

## Reporting Boundary

No winner may be presented as a Nature-level final result until the frozen validation set has been opened and recorded in the ledger.
