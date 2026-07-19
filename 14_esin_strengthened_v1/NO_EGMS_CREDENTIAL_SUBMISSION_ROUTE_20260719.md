# No-EGMS-credential submission route

Date: 2026-07-19

Purpose: define the fallback validation strategy when CLMS/EGMS credentials or manually downloaded Po/Rhone EGMS L3 ORTHO-UP files are unavailable.

## Submission strategy

The manuscript should not claim a completed Po/Rhone EGMS strong-subsidence benchmark. Instead, it uses a completed non-EGMS validation stack:

1. DWR/TRE--GHSL Central Valley: completed strong-subsidence external positive control.
2. Cyprus EGMS/source.coop: completed near-zero EGMS boundary control.
3. Po delta: completed local European transfer case with population and built-up exposure closure, supported by sparse published GNSS/InSAR geodetic context.
4. Japan/Iran product-lineage checks: completed parsing/portability tests.

## Claim boundary

This route is appropriate for an Earth-science informatics submission because the paper is framed as an audit workflow and exposure-translation method. It is not equivalent to a dense independent EGMS strong-subsidence validation, and the text should not imply otherwise.

## Manuscript changes made

- Replaced language describing Po/Rhone EGMS as the decisive pending benchmark with language describing it as a future hook.
- Reframed Po as a non-EGMS European transfer case rather than an execution-ready EGMS benchmark.
- Added sparse published Po River Delta GNSS/InSAR context through `cenni2021po_delta_geodetic`.
- Revised the validation table to distinguish completed positive control, boundary control, non-EGMS transfer and future EGMS hooks.
- Revised limitations to state that EGMS closure is not claimed without credentialed access or manually downloaded product files.

## Remaining future upgrade

If CLMS/EGMS access becomes available later, run the prepared Po/Rhone closure scripts and promote the result only after inspecting the threshold CSV, metadata JSON and point overlay sample.
