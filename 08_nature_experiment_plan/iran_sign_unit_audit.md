# Iran Sign and Unit Audit
日期：2026-07-09

## 证据来源
- Zenodo record: [10815578](https://zenodo.org/records/10815578)
- Local probe output: `Iran_subsidence_rate_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.tif`
- Zenodo description for the dataset
- Science Advances companion paper snippet

## 结论
Iran rate layer should be treated as **cm/yr**.

Reasoning:
1. The Zenodo record description calls the file an annual rate of land subsidence projected from LOS to vertical.
2. The Science Advances record snippet reports a median subsidence rate of `1.8 cm/year`.
3. Local GeoTIFF statistics after nodata removal give median `1.8`, p95 `10.3`, max `37.0`, which is numerically consistent with `cm/yr`, not `mm/yr`.

## Sign convention
Working convention for the current benchmark:
- positive rate = subsidence / downward deformation
- mask value `1` = subsidence class
- mask value `0` = non-subsidence or excluded

This convention is supported by the local inspection:
- rate median = `1.8`
- rate max = `37.0`
- mask median = `0.0`

The seasonal amplitude raster still needs a GDAL/rioxarray read to avoid the `tifffile` offset issue.

## Data type audit
- `Iran_subsidence_rate_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.tif`: annual rate, `cm/yr`
- `Iran_subsidence_seasonal_amplitude_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.tif`: seasonal amplitude, same spatial footprint
- `Iran_subsidence_mask_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.tif`: binary subsidence mask

## Paper usage rule
- Do not mix the Iran values with LiCSBAS `mm/yr` values without unit conversion.
- Always convert explicitly if a cross-region comparison table uses a single unit.
- State the sign convention in figure captions and data dictionary.

## What is still unresolved
- Confirm whether the seasonal amplitude raster uses the same sign basis as the rate layer.
- If a single comparison table is used across Japan/Iran/delta cases, convert everything to `mm/yr` or `cm/yr` consistently and document the conversion.
