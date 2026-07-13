# Chao Phraya OSM transport exposure censoring

This prototype uses no-auth OpenStreetMap Overpass data for major roads and railways.
It estimates transport-infrastructure exposure that falls on Chao Phraya strong-subsidence pixels but is hidden by LiCSAR coherence censoring.

- Coherence observability threshold: `0.3`
- Overpass endpoint: `https://overpass-api.de/api/interpreter`
- OSM way counts: `{"major_road": 17460, "railway": 1353}`
- Segments tested / used: `287760` / `166057`

| pair | exposed transport on strong subsidence (km) | hidden strong-subsidence transport (km) | hidden fraction |
|---|---:|---:|---:|
| 20160120_20160320 | 9707.10 | 17.40 | 0.002 |
| 20160507_20160519 | 9707.10 | 3.49 | 0.000 |
| 20160823_20160928 | 9707.10 | 20.27 | 0.002 |
| 20161127_20161221 | 9707.10 | 5.01 | 0.001 |
| 20170126_20170327 | 9707.10 | 6.34 | 0.001 |
| 20170514_20170830 | 9707.10 | 14.07 | 0.001 |
| 20170911_20171017 | 9707.10 | 23.22 | 0.002 |
| 20171204_20171216 | 9707.10 | 3.51 | 0.000 |
| 20180202_20180214 | 9707.10 | 0.00 | 0.000 |
| 20180608_20190311 | 9707.10 | 19.81 | 0.002 |
| 20180912_20190329 | 9707.10 | 25.19 | 0.003 |
| 20181217_20190110 | 9707.10 | 17.45 | 0.002 |
| 20190122_20190203 | 9707.10 | 5.08 | 0.001 |
| 20190428_20190510 | 9707.10 | 2.56 | 0.000 |
| 20190901_20190907 | 9707.10 | 0.00 | 0.000 |
| 20191124_20191224 | 9707.10 | 14.46 | 0.001 |
| 20200105_20200111 | 9707.10 | 2.44 | 0.000 |
| 20200329_20200919 | 9707.10 | 21.06 | 0.002 |
| 20200907_20200919 | 9707.10 | 6.34 | 0.001 |
| 20201212_20201218 | 9707.10 | 1.08 | 0.000 |
| 20210111_20210129 | 9707.10 | 1.83 | 0.000 |
| 20210405_20210429 | 9707.10 | 12.68 | 0.001 |
| 20210902_20220325 | 9707.10 | 18.09 | 0.002 |
| 20211213_20211231 | 9707.10 | 7.87 | 0.001 |
| 20220205_20220406 | 9707.10 | 22.11 | 0.002 |
| 20220325_20220909 | 9707.10 | 12.78 | 0.001 |
| 20220711_20220828 | 9707.10 | 13.03 | 0.001 |
| 20221003_20221027 | 9707.10 | 12.64 | 0.001 |

## Interpretation

- This is an exposure-censoring estimate, not an asset-level engineering risk model.
- Road and railway lengths are assigned to the VLM grid by one midpoint per original OSM way segment.
- The result is a minimum infrastructure-exposure layer for testing whether LiCSAR observability censoring affects risk estimates, not just area estimates.
