# ESIN Strengthening Changelog

Date: 2026-07-19

## Completed This Pass

- Created `14_esin_strengthened_v1` from `13_esin_submission_v1`.
- Replaced placeholder corresponding-author email with the author email available in the local TGRS manuscript.
- Replaced placeholder affiliations with the local author affiliations available in the local TGRS manuscript.
- Replaced funding placeholder with a no-specific-funding statement.
- Upgraded the Cyprus EGMS result from a generic smoke run to a boundary control in the manuscript text.
- Added exact Cyprus EGMS boundary-control values at the -5 mm/yr threshold:
  - 17,340 valid EGMS/GHSL point overlays;
  - 65 strong points;
  - 0.31% of EGMS-point-supported population;
  - 0.34% of EGMS-point-supported built-up sample;
  - median velocity -0.200 mm/yr.
- Reframed Po delta / Po-Venice and Rhone/Camargue as execution-ready, product-access-pending A-priority benchmarks.
- Added EGMS scripts, AOI registry, query payloads, Cyprus closure outputs and point overlay sample to the strengthened package.
- Added `A_PRIORITY_EGMS_EXECUTION_RUNBOOK_20260719.md`.
- Added `discover_sourcecoop_egms_public.py` and `EGMS_DATA_SOURCE_PROVENANCE_20260719.md`.
- Ran public Source Cooperative discovery. The public L2a parquet mirror exposed Cyprus (`CY`) objects but did not expose Italy (`IT`) or France (`FR`) objects under the listed public prefix.
- Added `regional_non_egms_strengthening_v1.csv` and `regional_non_egms_strengthening_v1.md` to separate local Po/Brantas/Rhone/Rhine regional strengthening from independent EGMS validation.
- Added `EGMS_MANUAL_DOWNLOAD_MANIFEST_20260719.md`, `preflight_egms_manual_downloads_v1.py` and `egms_manual_download_preflight_report_v1.json` so manually downloaded Po/Rhone EGMS files can be checked before closure execution.
- Added stable target folders under `egms_priority_downloads_v1/` for Po delta core, Po-Venice broad and Rhone delta core EGMS L3 ORTHO-UP products.
- Broadened `build_egms_benchmark_closure_v1.py` input handling for `.pq`, `.csv.gz` and normalized EGMS-style column names, then verified the Cyprus boundary-control outputs by regression in `EGMS_CLOSURE_SCRIPT_REGRESSION_20260719.md`.
- Added `selftest_egms_input_compatibility_v1.py` and `EGMS_INPUT_COMPATIBILITY_SELFTEST_20260719.md`; the self-test verifies `.csv`, `.csv.gz`, `.parquet` and `.pq` inputs with non-exact EGMS-style column names.
- Added `ESIN_SUBMISSION_GATE_STATUS_20260719.json` and `ESIN_SUBMISSION_GATE_STATUS_20260719.md` to make completed gates, pending EGMS gates and post-download commands explicit.
- Aligned `run_egms_clms_priority_closure_v1.py` with the official EGMS API notebook endpoint and download-link pattern; documented this in `EGMS_OFFICIAL_API_ALIGNMENT_20260719.md`.
- Added `NO_EGMS_CREDENTIAL_SUBMISSION_ROUTE_20260719.md` and revised the manuscript to use the no-credential validation stack: DWR/TRE positive control, Cyprus EGMS boundary control, Po non-EGMS transfer with sparse published GNSS/InSAR context, and EGMS as a future hook rather than a present claim.
- Added ESIN submission support files: `ESIN_COVER_LETTER_20260719.md`, `ESIN_HIGHLIGHTS_20260719.md`, `ESIN_DECLARATIONS_CHECKLIST_20260719.md` and `ESIN_SUBMISSION_README_20260719.md`.
- Added Q1-style reviewer-defence experiment layer: `Q1_STYLE_EXPERIMENT_STRENGTHENING_20260719.csv`, `Q1_STYLE_EXPERIMENT_STRENGTHENING_20260719.md` and a manuscript failure-mode audit table.

## Not Completed Because External Input Is Missing

- Po delta / Po-Venice EGMS strong-subsidence closure was not executed because no EGMS/CLMS credential, manually downloaded Po/Rhone EGMS product file, or public Source Cooperative Italy/France parquet object was present.
- No new strong-subsidence EGMS values were invented.

## Next Gate

Run the A-priority EGMS closure after obtaining one of:

- CLMS/EGMS bearer token;
- CLMS service-key JSON;
- manually downloaded EGMS L3 ORTHO-UP csv/parquet for Po delta, Po-Venice or Rhone/Camargue.

After placing a manual product file in `egms_priority_downloads_v1/`, run `py -3 .\preflight_egms_manual_downloads_v1.py` before the closure command.
