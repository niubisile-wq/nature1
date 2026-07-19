# EGMS Data Source Provenance

Date: 2026-07-19

## Authoritative Sources Checked

1. Copernicus Land Monitoring Service EGMS Ortho product page:
   `https://land.copernicus.eu/en/products/european-ground-motion-service/egms-ortho`

   Relevant facts recorded from the page:
   - EGMS Ortho 2019-2023 is validated.
   - Ortho Vertical DOI is listed by CLMS.
   - EGMS Explorer is the route for exploring and downloading the latest product releases.
   - CLMS links to the official EGMS API notebook.

2. EEA geospatial catalogue record for EGMS Ortho Vertical Component 2019-2023:
   `https://sdi.eea.europa.eu/catalogue/srv/api/records/9abe5dd1-3639-4aeb-a8de-ec2eb2f7fc93?language=all`

   Relevant facts recorded from the catalogue:
   - The product is the third EGMS product level, Ortho.
   - It provides purely vertical displacement on a 100 m grid.
   - It is distributed as vector measurement points in comma-separated values format.
   - The online resource notes that download requires authentication.

3. Source Cooperative public cloud-native EGMS mirror:
   `https://source.coop/youssef-harby/egms-copernicus`

   Relevant facts recorded from the page:
   - The repository is public.
   - The source data came from Copernicus EGMS zipped CSV files.
   - The converted formats include Parquet Geo and PMTiles.
   - The page provides a working example for a Cyprus L2a parquet file.

## Local Discovery Result

The packaged script `discover_sourcecoop_egms_public.py` was used to list public objects under:

`https://data.source.coop/youssef-harby/egms-copernicus/?list-type=2&prefix=L2a/parquet/`

Result:

- Public L2a parquet object count found: 48.
- Country-level directory found: `CY`.
- No `IT` or `FR` parquet directory was found under the public L2a parquet prefix.

## Consequence for the Manuscript

- Cyprus can be used as a public, reproducible EGMS boundary-control run.
- Po delta, Po-Venice and Rhone/Camargue cannot be claimed as completed from the public Source Cooperative mirror.
- A-priority strong-subsidence closure still requires authenticated CLMS/EGMS product download or a manually supplied product file.

This provenance note supports the manuscript wording: "execution-ready; product access pending."
