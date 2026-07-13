# Japan Niigata Sign and Unit Audit
日期：2026-07-09

## 证据来源
- Zenodo record: [4243151](https://zenodo.org/records/4243151)
- PEPS paper PDF summary: GSI presentation PDF and Zenodo description
- Local selected probe: `151_Niigata_039A_05193_040711_TS_GEOCml1.zip`
- Local HDF5 inspection: `cum.h5`, `cum_filt.h5`

## 结论
Niigata 选择性样本的 LiCSBAS `vel` 层应按 **mm/yr** 处理，而不是 cm/yr。

理由：
1. GSI paper explicitly states LiCSBAS can derive displacement velocities with accuracy of about `~2 mm/yr`.
2. Local HDF5 `vel` values are in the order of `-39` to `+13`, which is physically reasonable in `mm/yr` but not in `cm/yr`.
3. The Zenodo dataset description says the package contains LOS velocities and decomposed vertical/EW velocities.

## Sign convention
Working convention for the current benchmark:
- negative velocity = subsiding / downward tendency
- positive velocity = uplifting / upward tendency

This is consistent with the Niigata sample:
- `cum_filt.h5` median `vel` = `-0.409` mm/yr
- `cum.h5` median `vel` = `-1.016` mm/yr

The sign convention should still be cross-checked against the full paper figure legend before the manuscript is finalized, but the working convention is coherent with the observed subsiding Niigata case.

## Data type audit
- `cum.h5`: raw time-series summary
- `cum_filt.h5`: filtered time-series summary
- `vel`: velocity grid, mm/yr
- `vintercept`: intercept grid, same spatial units as velocity product convention
- `gap`: integer gap mask
- `ref_area`: `217:218/69:70` in the sample metadata

## Parameters that matter for the paper
- `n_im = 111`
- `n_ifg = 324`
- `filtwidth_km = 2`
- `pixel_spacing_r = 87.82 m`
- `pixel_spacing_a = 110.95 m`
- reference areas differ across processing steps and must be documented

## What to do with this in the paper
- Use Niigata as a product-lineage extension case.
- Do not call it independent truth.
- Do not convert the values to cm/yr in any figure source table.
- Put the `mm/yr` unit explicitly in the data dictionary.
