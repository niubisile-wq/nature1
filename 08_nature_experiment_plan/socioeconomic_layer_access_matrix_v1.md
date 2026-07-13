# Socioeconomic Layer Access Matrix v1
Date: 2026-07-11

## Purpose
Record how the candidate socioeconomic layers can actually be accessed, so the next experiment step is executable rather than aspirational.

## Access Matrix

| candidate | official source | public access signal | practical access mode | trial role |
|---|---|---|---|---|
| GVI v1.1 | Global Data Lab | public table routes are visible from the official site and the table pages render historical values directly | direct public table path | preferred vulnerability companion layer, immediately executable |
| GRDI v1 | NASA Earthdata / SEDAC | official catalog page is public and exposes DOI, docs, and Earthdata Search / URS links; the catalog page itself is not the data file | likely Earthdata Search / EDL authenticated download path | preferred raster upgrade, but access-gated |
| SHDI v10.2 | Global Data Lab | public table and download routes are visible from the official site | direct public table / download path | immediate contextual backup layer |
| Nightlights | World Bank / harmonized nightlight products | proxy datasets are widely public, but they are not the preferred socioeconomic measure | proxy download or API path depending on product | last-resort fallback only |

## Trial Order
1. Use GVI first to build an immediately executable vulnerability companion table.
2. Keep SHDI as the contextual backup if the vulnerability layer needs a secondary comparison.
3. Keep GRDI as the preferred raster upgrade and prepare it for Earthdata Search / login-based access.
4. Use nightlights only if GVI, SHDI, and GRDI fail to produce a defensible layer.

## What This Changes
- The socioeconomic upgrade is no longer only a candidate list.
- It now has a practical access ranking.
- The trial can start immediately at the GVI level while the SHDI and GRDI paths remain as backup and upgrade.

## Bottom Line
The current best move is to execute the GVI vulnerability layer first, because it is publicly reachable now and is better aligned with the vulnerability translation question. SHDI remains a strong backup, and GRDI remains the higher-value raster target once the Earthdata access path is available.
