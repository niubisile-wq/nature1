# EGMS rescue query pack

This pack turns the Nature rescue route into reproducible EGMS API queries.
The default run is credential-free and only writes query payloads; pass an access token to execute searches.

## Decision use

- Primary goal: close the independent benchmark gap for the open-InSAR observability-bias claim.
- Fastest Nature rescue: EGMS L3 ORTHO-UP over Po/Venice, Netherlands lowlands, Rhone, and Rhine controls.
- Parser-only smoke test: Cyprus, because a Source Cooperative EGMS sample exists there.

## AOIs

| AOI | Priority | Role | BBox |
|---|---:|---|---|
| po_venice_broad | A | EGMS benchmark for Po/Venice LiCSAR observability bias | 10.0, 44.0, 13.0, 46.0 |
| po_delta_core | A | Core positive-control delta benchmark | 11.7, 44.35, 12.9, 45.55 |
| netherlands_lowlands | A | Independent EGMS lowland benchmark | 3.2, 50.7, 7.2, 53.8 |
| rhine_core | B | Specificity control | 3.2, 51.0, 5.2, 52.35 |
| rhone_delta_core | A | Land-cover mediated delta benchmark | 4.0, 43.2, 5.15, 44.05 |
| cyprus_sourcecoop_smoke | C | Cloud-native EGMS format smoke test | 32.0, 34.4, 34.8, 35.8 |

## Query kinds

| Query kind | Levels | Product type | Purpose |
|---|---|---|---|
| l3_ortho_up | L3 | ORTHO-UP | Primary vertical-motion benchmark for exposure and observability closure. |
| l3_ortho_east | L3 | ORTHO-EAST | Optional horizontal component sanity check for coastal/delta deformation interpretation. |
| l2b_calibrated | L2B |  | Optional calibrated-track product for product-bias transfer-function tests. |

## Files

- `egms_rescue_aoi_registry.csv`: AOI table.
- `egms_query_payloads.json`: machine-readable payloads.
- `egms_query_payloads.csv`: compact payload table.

## Next command with credentials

```powershell
py prepare_egms_rescue_queries.py --token-jwt C:\path\to\token.jwt
```

Or, if a short-lived bearer token is already available:

```powershell
py prepare_egms_rescue_queries.py --access-token $env:EGMS_ACCESS_TOKEN
```
