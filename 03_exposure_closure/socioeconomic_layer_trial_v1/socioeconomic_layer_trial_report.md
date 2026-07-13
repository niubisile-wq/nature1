# Socioeconomic Layer Trial Report v1

This report is a frozen scaffold for the socioeconomic trial. It records which regions can be matched immediately to GVI / SHDI-style contextual data and which regions remain access-gated for GRDI raster upgrades.

## Region Access Matrix

| region | preferred source | secondary source | country / area | trial mode | country ISO | access status | notes |
|---|---|---|---|---|---|---|---|
| Chao_Phraya | GVI | SHDI | Thailand | region_level_context | THA | ready_for_gvi_trial | GVI is a public vulnerability index and is the preferred socioeconomic context layer for the current trial. |
| Po | GVI | SHDI | Italy | region_level_context | ITA | ready_for_gvi_trial | GVI is a public vulnerability index and is the preferred socioeconomic context layer for the current trial. |
| Brantas | GVI | SHDI | Indonesia | region_level_context | IDN | ready_for_gvi_trial | GVI is a public vulnerability index and is the preferred socioeconomic context layer for the current trial. |
| Indus | GVI | SHDI | Pakistan_or_India_basin_context | multi_country_context | IND | ready_for_gvi_trial | GVI is a public vulnerability index and is the preferred socioeconomic context layer for the current trial. |
| Rhone | GVI | SHDI | France | region_level_context | FRA | ready_for_gvi_trial | GVI is a public vulnerability index and is the preferred socioeconomic context layer for the current trial. |
| Rhine | GVI | SHDI | Multi_country_basin_context | multi_country_context |  | ready_for_gvi_trial | GVI is a public vulnerability index and is the preferred socioeconomic context layer for the current trial. |

## GVI Country Context Layer

This layer is built from public Global Data Lab GVI table pages. It is intentionally country-level context rather than pixel-level truth, because the current trial is a conservative fallback.

| region | country / area | country ISO | GVI label | latest year | latest GVI | status | notes |
|---|---|---|---|---:|---:|---|---|
| Po | Italy | ITA | Italy | 2013 | 25.2 | retrieved_from_public_table | National GVI row fetched from the public Global Data Lab table page (ITAt: Italy). |
| Chao Phraya | Thailand | THA | Total | 2013 | 32.3 | retrieved_from_public_table | National GVI row fetched from the public Global Data Lab table page (THAt: Total). |
| Brantas | Indonesia | IDN | Total | 2013 | 39.5 | retrieved_from_public_table | National GVI row fetched from the public Global Data Lab table page (IDNt: Total). |
| Indus | Pakistan_or_India_basin_context | IND | Total | 2013 | 48.3 | retrieved_from_public_table | National GVI row fetched from the public Global Data Lab table page (INDt: Total). |
| Rhone | France | FRA | France | 2013 | 23.6 | retrieved_from_public_table | National GVI row fetched from the public Global Data Lab table page (FRAt: France). |
| Rhine | Multi_country_basin_context |  |  |  |  | multi_country_context_unresolved | No single-country context mapping was frozen for this multi-country basin context. |

## GVI Subnational Spread Summary

This summary shows the within-country spread of the public GVI table pages. It is useful because it makes the vulnerability gradient visible rather than collapsing the layer to a single number.

| region | country / area | country ISO | year | national GVI | subnational count | subnational min | subnational median | subnational max | note |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Po | Italy | ITA | 2013 | 25.2 | 20 | 20.9 | 26.9 | 33.1 | retrieved_from_public_table |
| Chao Phraya | Thailand | THA | 2013 | 32.3 | 4 | 31.0 | 34.9 | 35.4 | retrieved_from_public_table |
| Brantas | Indonesia | IDN | 2013 | 39.5 | 28 | 30.1 | 41.4 | 56.1 | retrieved_from_public_table |
| Indus | Pakistan_or_India_basin_context | IND | 2013 | 48.3 | 35 | 34.4 | 45.1 | 60.9 | retrieved_from_public_table |
| Rhone | France | FRA | 2013 | 23.6 | 26 | 15.5 | 28.1 | 35.2 | retrieved_from_public_table |
| Rhine | Multi_country_basin_context |  |  |  |  |  |  |  | multi_country_context_unresolved |

## SHDI Backup Layer

The SHDI fallback remains available as a country-context backup for the single-country cases and may be used if the GVI route ever proves unsuitable.

| region | country / area | country ISO | SHDI label | latest year | latest SHDI | status | notes |
|---|---|---|---|---:|---:|---|---|
| Po | Italy | ITA | Italy | 2023 | 0.915 | retrieved_from_public_table | National SHDI row fetched from the public Global Data Lab table page (ITAt: Italy). |
| Chao Phraya | Thailand | THA | Total | 2023 | 0.798 | retrieved_from_public_table | National SHDI row fetched from the public Global Data Lab table page (THAt: Total). |
| Brantas | Indonesia | IDN | Total | 2023 | 0.728 | retrieved_from_public_table | National SHDI row fetched from the public Global Data Lab table page (IDNt: Total). |
| Indus | Pakistan_or_India_basin_context | IND | Total | 2023 | 0.685 | retrieved_from_public_table | National SHDI row fetched from the public Global Data Lab table page (INDt: Total). |
| Rhone | France | FRA | France | 2023 | 0.920 | retrieved_from_public_table | National SHDI row fetched from the public Global Data Lab table page (FRAt: France). |
| Rhine | Multi_country_basin_context |  |  |  |  | multi_country_context_unresolved | No single-country context mapping was frozen for this multi-country basin context. |

## SHDI Subnational Spread Summary

This summary shows the within-country spread of the public SHDI table pages. It is kept as a backup comparator against the GVI layer.

| region | country / area | country ISO | year | national SHDI | subnational count | subnational min | subnational median | subnational max | note |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Po | Italy | ITA | 2023 | 0.915 | 20 | 0.9 | 0.9 | 0.9 | retrieved_from_public_table |
| Chao Phraya | Thailand | THA | 2023 | 0.798 | 4 | 0.8 | 0.8 | 0.8 | retrieved_from_public_table |
| Brantas | Indonesia | IDN | 2023 | 0.728 | 29 | 0.5 | 0.7 | 0.8 | retrieved_from_public_table |
| Indus | Pakistan_or_India_basin_context | IND | 2023 | 0.685 | 35 | 0.6 | 0.7 | 0.8 | retrieved_from_public_table |
| Rhone | France | FRA | 2023 | 0.920 | 26 | 0.8 | 0.9 | 1.0 | retrieved_from_public_table |
| Rhine | Multi_country_basin_context |  |  |  |  |  |  |  | multi_country_context_unresolved |

## Trial Logic

1. GVI is the first executable socioeconomic vulnerability layer because it is public and more directly aligned with the climate-vulnerability question.
2. SHDI remains the secondary fallback because it is a public contextual layer but is less directly vulnerability-specific than GVI.
3. GRDI remains the preferred raster upgrade, but it is access-gated and should be attempted only after the contextual route is frozen.
4. Nightlights remains a last-resort proxy only.

## Current Status

- GVI country-level vulnerability values are now computed directly from public Global Data Lab table pages for the single-country regions.
- GVI subnational spreads are now computed from the same public table pages, so the vulnerability layer has visible internal gradients instead of a single collapsed number.
- SHDI country-level context values are also computed as a backup from the same source family, and SHDI subnational spreads are available for comparison.
- Multi-country basin contexts remain unresolved until a basin aggregation policy is frozen.
- The access matrix and region mapping are explicit, so a raster upgrade or finer-grained SHDI/GVI ingestion can be added without redesigning the workflow.
