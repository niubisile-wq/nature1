# EGMS official API alignment

Date: 2026-07-19

The EGMS download wrapper was aligned with the official Copernicus Land EGMS API notebook.

## Official API behavior

The official notebook uses:

- API endpoint: `https://egms.land.copernicus.eu/insar-api/archive`
- Search endpoint: `/search`
- Download URL pattern: `/download/{filename}?id={query_id}`
- Authentication: CLMS service-key JSON saved as `token.jwt`

The wrapper now constructs download links from the EGMS API search response using the `hits[*].filename` values and the returned query `id`.

## Credential requirement

No credential is stored in this package. To execute authenticated search/download:

1. Log in to CLMS.
2. Generate a personal API token/service key.
3. Save it as `token.jwt` in this package root or pass it with `--service-key-json`.
4. Run `run_egms_clms_priority_closure_v1.py`.

Do not include `token.jwt` in a submission archive or share it publicly.

## Verification

The wrapper passed Python compilation and a local dry run against the existing Cyprus parquet input:

```powershell
py -3 .\run_egms_clms_priority_closure_v1.py `
  --local-egms-file .\egms_boundary_control_inputs\EGMS_L2a_087_0205_IW2_VV_2019_2023_1.parquet `
  --aoi-id cyprus_dryrun `
  --outdir .\egms_priority_benchmark_closure_v1 `
  --dry-run
```

Authenticated EGMS search/download was not executed because no `token.jwt`, service key or bearer token is present locally.
