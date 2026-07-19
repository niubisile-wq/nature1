# EGMS closure script regression

Date: 2026-07-19

Purpose: verify that the broadened EGMS input reader does not change the existing Cyprus boundary-control result.

## Change tested

`build_egms_benchmark_closure_v1.py` was updated to:

- support `.pq` and `.csv.gz` inputs in addition to `.parquet`, `.csv` and `.txt`;
- normalize column names before matching longitude, latitude, velocity and optional quality columns;
- add common EGMS-style vertical velocity aliases such as `v_up`, `vu`, `ortho_up` and `mean_velocity_mm_yr`;
- return clearer column-missing errors with an available-column preview.

## Regression command

```powershell
py -3 .\build_egms_benchmark_closure_v1.py `
  --input .\egms_boundary_control_inputs\EGMS_L2a_087_0205_IW2_VV_2019_2023_1.parquet `
  --outdir .\egms_boundary_control_cyprus_regression_v1 `
  --aoi-id cyprus_regression `
  --product-label EGMS_L2a_CYPRUS_REGRESSION `
  --thresholds 1,2,5,10
```

## Result

The regression output exactly reproduces the current Cyprus boundary-control threshold values:

| threshold mm/yr | valid points | strong points | strong population share | strong built-up share |
|---:|---:|---:|---:|---:|
| 1 | 17,340 | 3,079 | 0.1355886603 | 0.1468295034 |
| 2 | 17,340 | 886 | 0.0360154608 | 0.0394727111 |
| 5 | 17,340 | 65 | 0.0031145048 | 0.0033876641 |
| 10 | 17,340 | 2 | 0.0000007320 | 0.0000026342 |

No scientific result was changed by the input-compatibility update.
