# Q1-style experiment strengthening

Date: 2026-07-19

Purpose: consolidate the reviewer-facing experimental defences needed to make the ESIN submission more robust under higher-standard review.

## Added defence layer

The new defence table maps likely reviewer concerns to the exact experiment that addresses each concern:

- threshold artefact;
- grid/exposure allocation artefact;
- MAUP/reporting-partition artefact;
- random hidden-mask artefact;
- decision irrelevance;
- false universal positive;
- land-cover confounding;
- external-product overclaim.

## Key values promoted

- Threshold stress surface: hidden population remains between 1.33 and 5.36 million people, and hidden built-up area remains between 140.44 and 523.64 km2.
- Native-pixel allocation: 3.63 million hidden people and 404.77 km2 hidden built-up area.
- MAUP sensitivity: strong hidden population fraction remains 0.182735 and built-up fraction remains 0.337248 under tested block sizes and shifted origins.
- Placebo randomization: strong-not-majority OR is 5.78 versus a global-null mean of 1.01 and a spatial-null mean of 3.38; random hidden-mask models do not show the observed result is an upper-tail exposure artefact.
- Decision consequence: at a 500-cell inspection budget, observability-aware ranking adds 41,009.8 hidden people and 0.640 km2 hidden built-up in aware-only cells.
- Rhine negative/specification control: OR 0.810149, retained as a non-positive control case.

## Manuscript integration

The manuscript now includes a compact failure-mode audit table in the Results section. This table is intended to answer reviewer concerns without overclaiming dense independent validation.

## Boundary

This strengthening makes the paper more robust for ESIN and lower-tier remote-sensing/informatics venues. It still does not create a completed dense independent Po/Rhone EGMS validation.
