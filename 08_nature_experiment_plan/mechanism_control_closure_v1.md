# Mechanism Control Closure v1
Date: 2026-07-13

## Purpose

Freeze the current control-family comparison so the manuscript can point to one bounded robustness ladder instead of several ad hoc control statements.

## Source basis

- `mechanism_control_table_v1.csv`
- `multi_region_stratified_control_closure_v1/multi_region_stratified_control_comparison.csv`
- `multi_region_stratified_control_closure_v1/multi_region_stratified_control_report.md`
- `multi_region_technical_validation_v1.md`

## Core result

- The richest constrained control family keeps the reference OR above 1.
- The landcover-size stack is the best frozen control summary on leave-one-out error.
- The full stratified stack does not overturn the signal, but it is not the most stable summary.

## Interpretation

- The result is not explained away by a single land-cover class.
- The result is not just a sparse GNSS-anchor artifact.
- The result remains positive after adding exposure composition and hidden-share controls.

## Manuscript use

- Use the landcover-size stack as the primary control-family evidence.
- Use the full stratified stack as the richer sensitivity check.
- Keep the control/specification case for Rhine explicit and bounded.
