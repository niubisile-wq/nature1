# Final Multi-Region Equal-Area Closure v1
Date: 2026-07-13

This package tightens the benchmark by making the multi-region weighting status explicit. It is the final equal-area / polygon-facing closure layer for the current manuscript evidence stack.

## Region Table

| region | role | product_family | overlay_method | cell_count | strong_cell_count | observable_fraction | hidden_population | hidden_built_up_area | hidden_transport_or_infrastructure | weighting_status | claim_status |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| Po | supporting_case | open_delta_vlm_benchmark | equal_area_cell_overlap_proxy | 2255 | 2013 | 0.172380 | 23045.123 | 11.984 |  | area_weighted_proxy | supporting_case |
| Chao Phraya | lead_case | open_delta_vlm_benchmark | equal_area_cell_overlap | 18077 | 17808 | 0.293071 | 3629023.570 | 422.781 | mean=0.001; median=0.001; min=0.000; max=0.003 | area_weighted_closed | lead_case |
| Indus | transfer_case | open_delta_vlm_transfer | proxy_only | 7087 |  |  |  |  |  | proxy_only | transfer_case |
| Rhone | transfer_case | open_delta_vlm_transfer | proxy_only | 3392 |  |  |  |  |  | proxy_only | transfer_case |
| Brantas | supporting_case | open_delta_vlm_benchmark | equal_area_cell_overlap_proxy | 1320 | 991 | 0.533804 | 472517.157 | 34.062 |  | area_weighted_proxy | supporting_case |
| Rhine | control_case | open_delta_vlm_control | proxy_only | 9011 |  |  |  |  |  | proxy_only | control_case |

## Transport Anchor

- Chao Phraya transport hidden fraction mean: 0.001
- median: 0.001
- min: 0.000
- max: 0.003

## Bottom Line

Chao Phraya is the only lead case with a closed equal-area / polygon-facing exposure package. Po and Brantas remain supporting area-weighted proxies. Indus, Rhone, and Rhine stay explicit proxy or control cases and are not silently promoted to lead status.
