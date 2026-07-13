# Multi-Region Exposure Closure v1

This file is generated from `benchmark_region_evidence_v0_1.csv` and `multi_delta_vlm_exposure_censoring_summary.csv`.

| region | signal | anchor | landcover | OR | strong cells | strong pop fraction | pop not-majority | built not-majority | risk proxy | readiness |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Po | positive | sparse_gnss_anchor | cropland | 1.32894 | 2013 | 0.6197120668793455 | 0.34034723087055835 | 0.4603312851822799 | 0.328935 | conditional_nature_go_after_egms |
| Chao Phraya | strong_positive | sparse_gnss_anchor | cropland | 3.56187 | 17808 | 0.916922753226613 | 0.17590364553974555 | 0.3372472125343407 | 2.56187 | benchmark_v0_landed_needs_dense_truth |
| Indus | strong_positive | weak_or_missing_gnss_anchor | water_wetland_mangrove | 3.3894 |  |  |  |  | 2.3894 | statistical_signal_needs_independent_anchor |
| Rhone | positive | sparse_gnss_anchor | vegetation_non_crop | 1.59178 |  |  |  |  | 0.591777 | conditional_nature_go_after_egms |
| Brantas | positive | weak_or_missing_gnss_anchor | built_up | 1.59171 | 991 | 0.5795511443436998 | 0.1459028285078172 | 0.17599259551502697 | 0.591713 | statistical_signal_needs_independent_anchor |
| Rhine | inconclusive | sparse_gnss_anchor | vegetation_non_crop | 0.810149 |  |  |  |  | -0.189851 | control_or_specification_case |
