# 继续侦察：统一模型与 WorldCover 地表解释

日期：2026-07-09

## 结论先行

本轮把 Rhone、Rhine、Indus 三个候选 delta 纳入原有 Po、Chao Phraya、Brantas、Central Valley 的统一 pair-count binomial 交互模型，并对候选区补做 ESA WorldCover 2021 v200 地表覆盖 proxy 探针。

当前判断：

1. G5 有实质推进，但仍不能写成“强沉降区全球普遍更不可见”的统一主效应。
2. 更稳妥的主张是：开放 InSAR 可见性删失存在明显区域/地表条件异质性，且在若干 delta 中强沉降像元的 pair-level 不可见 odds 显著升高。
3. Rhone 和 Indus 的正向信号继续成立；Rhine 在单独筛选中跨 1，但在统一模型中转为正向，需要作为“待复核候选”，不能直接当强证据。
4. WorldCover 探针显示 cropland、水体/湿地、建成区在不同 delta 中对应完全不同的 failure 结构，说明下一步必须把 land-cover proxy 纳入模型解释异质性。

## 一、统一七区域 Binomial 模型

新增脚本：

`C:\Users\刘子轩\科研侦察报告_待上传\雷达方向_Nature正刊级选题侦察\fit_extended_region_binomial_with_candidates.py`

输出目录：

`C:\Users\刘子轩\radar_outputs\extended_region_binomial_with_candidates`

模型：

`failure_count_i ~ Binomial(n_pairs_i, p_i)`

`logit(p_i) ~ strong_subsidence + exposure_z + region_fixed_effect + strong_subsidence:region + strong_subsidence:exposure_z`

参数：

- coherence threshold：`0.3`
- bootstrap：`1000`
- seed：`20260709`
- observations：`96,533`
- spatial clusters：`703`
- bootstrap failures：`0`

强沉降边际效应：

| region | clustered OR | clustered 95% CI | bootstrap median | bootstrap 95% interval | 判断 |
|---|---:|---:|---:|---:|---|
| Po | 1.041 | 0.890-1.217 | 1.050 | 0.872-1.228 | 跨 1，不支持稳定正向 |
| Brantas | 12.917 | 6.423-25.974 | 12.658 | 5.993-25.940 | 强正向 |
| Central Valley | 0.805 | 0.634-1.023 | 0.800 | 0.627-1.032 | 跨 1，且方向偏负 |
| Chao Phraya | 13.222 | 7.002-24.968 | 13.524 | 7.078-27.084 | 强正向 |
| Indus | 4.358 | 2.979-6.375 | 4.327 | 2.784-6.197 | 正向复现 |
| Rhine | 1.622 | 1.084-2.427 | 1.617 | 1.092-2.485 | 统一模型正向，但需复核 |
| Rhone | 1.515 | 1.166-1.967 | 1.504 | 1.147-1.979 | 正向复现 |

暴露交互：

| effect | clustered OR | bootstrap 95% interval | 解释 |
|---|---:|---:|---|
| strong x population_z | 0.294 | 0.237-0.368 | 人口高值区反而降低强沉降 failure odds，可能反映城市硬化地表更可见 |
| strong x builtup_z | 1.477 | 1.219-1.732 | 建成区与强沉降交互提高 failure odds，可能反映密集/混合地表或局部几何效应 |

核心解释：

统一模型支持“异质性删失校正框架”，不支持单一全球机制。Chao Phraya、Brantas、Indus、Rhone 是当前最重要的正向候选；Po 和 Central Valley 不支持；Rhine 从单独筛选跨 1 变成统一模型正向，说明它对模型规格敏感。

## 二、WorldCover 地表覆盖 proxy 探针

新增脚本：

`C:\Users\刘子轩\科研侦察报告_待上传\雷达方向_Nature正刊级选题侦察\probe_candidate_worldcover_landcover.py`

输出目录：

`C:\Users\刘子轩\radar_outputs\candidate_worldcover_landcover_probe`

数据源：

- ESA WorldCover 2021 v200
- AWS S3 COG map tiles，无授权下载
- overview level：`4`
- overview shape：`2250 x 2250`
- 候选区：Rhone、Rhine、Indus

已下载/复用 tile：

| region | tile | bytes |
|---|---|---:|
| Rhone | N42E003 | 69,615,796 |
| Rhine | N51E003 | 54,556,617 |
| Indus | N21E066 | 10,192,573 |
| Indus | N24E066 | 96,971,395 |

官方可用性核验：

- ESA WorldCover 页面说明 2021 v200 为 10 m、11 类全球 land-cover 产品，CC BY 4.0，可通过 AWS S3 获取。
- ESA 数据下载说明给出 `aws s3 sync s3://esa-worldcover/v200/2021/map ... --no-sign-request`。
- Google Earth Engine 目录列出 11 个类别：tree cover、shrubland、grassland、cropland、built-up、bare/sparse vegetation、snow/ice、permanent water、herbaceous wetland、mangroves、moss/lichen。

## 三、候选区地表解释结果

### Rhone

| group | cell fraction | strong share | failure rate | strong failure | nonstrong failure |
|---|---:|---:|---:|---:|---:|
| cropland | 0.211 | 0.719 | 0.789 | 0.825 | 0.696 |
| built_up | 0.053 | 0.067 | 0.251 | 0.522 | 0.232 |
| water/wetland/mangrove | 0.334 | 0.274 | 0.883 | 0.914 | 0.871 |
| wetland/mangrove | 0.151 | 0.348 | 0.880 | 0.937 | 0.851 |
| vegetation_non_crop | 0.374 | 0.291 | 0.741 | 0.849 | 0.696 |

解释：

Rhone 的强沉降像元高度富集在 cropland，且水体/湿地/植被区 failure rate 很高；built-up 区整体 failure rate 很低。这支持“地表条件驱动可见性删失”的解释，而不是“强沉降本身导致不可见”。

### Rhine

| group | cell fraction | strong share | failure rate | strong failure | nonstrong failure |
|---|---:|---:|---:|---:|---:|
| cropland | 0.302 | 0.331 | 0.849 | 0.868 | 0.839 |
| built_up | 0.164 | 0.063 | 0.781 | 0.948 | 0.769 |
| water/wetland/mangrove | 0.115 | 0.128 | 0.992 | 0.976 | 0.994 |
| vegetation_non_crop | 0.417 | 0.163 | 0.865 | 0.909 | 0.857 |

解释：

Rhine 整体 failure rate 已经很高，水体/湿地几乎全不可见；cropland 中 strong share 较高。统一模型的正向结果可能来自控制人口/建成区后的结构变化，但因为单独筛选曾跨 1，必须复跑 controlled annual sampling，暂列待复核。

### Indus

| group | cell fraction | strong share | failure rate | strong failure | nonstrong failure |
|---|---:|---:|---:|---:|---:|
| cropland | 0.218 | 0.312 | 0.818 | 0.842 | 0.807 |
| built_up | 0.006 | 0.186 | 0.380 | 0.514 | 0.350 |
| water/wetland/mangrove | 0.507 | 0.093 | 0.628 | 0.687 | 0.622 |
| wetland/mangrove | 0.120 | 0.005 | 0.521 | 0.618 | 0.521 |
| bare_sparse | 0.189 | 0.080 | 0.444 | 0.649 | 0.426 |

解释：

Indus 的强沉降像元相对富集在 cropland，而不是 wetland/mangrove；cropland failure rate 明显高于 bare sparse 和 built-up。该结果提示 Indus 的正向删失可能与农业/灌溉地表和相干性变化有关。

## 四、对创新主张的影响

当前更安全的 Nature 级主张边界：

**开放 InSAR 产品的可见性删失不是随机缺失，而是与区域、地表覆盖、人口/建成区暴露和强沉降场共同耦合；这种耦合会改变公开沉降暴露估计。**

仍不能写：

1. 强沉降区在全球普遍更不可见。
2. 低可见性一定由地下水或沉降机制直接导致。
3. WorldCover 2021 overview 已经解释了全部异质性。
4. Rhine 已经完成正向复现。

可以写成下一轮假设：

1. Cropland / irrigation surfaces may mediate positive observability censoring in Rhone and Indus.
2. Water / wetland / mangrove surfaces can raise baseline failure rates, but may not coincide with strong subsidence in all deltas.
3. Built-up surfaces may either improve observability or interact with local geometry; this needs region-specific modeling.

## 五、下一步

优先级 1：把 WorldCover group 加入统一 binomial 模型。

模型建议：

`failure_count_i ~ Binomial(n_pairs_i, p_i)`

`logit(p_i) ~ strong_subsidence * landcover_group + exposure_z + region_fixed_effect + strong_subsidence:region`

目标：检验 Rhone/Indus 的正向效应是否被 cropland / wetland / water proxy 吸收。

优先级 2：对 Rhone、Indus、Rhine 复跑 controlled annual sampling。

原因：候选区当前使用本地已有下载目录，虽然 pair 数足够，但仍来自候选聚合任务，不应直接作为最终论文抽样设计。

优先级 3：把 WorldCover 探针扩展到 Chao Phraya、Brantas、Po。

原因：只有候选区 land-cover proxy 还不能解释原始三 delta 中 Chao Phraya/Brantas 强正向与 Po 不稳健的差异。

优先级 4：继续核验 Nature 2026 `gridVLM.zip` 的 GeoTIFF 单位和 1 km 降采样说明。

原因：当前仍按 raw value x10 转换到 mm/yr；虽然量级与 supplementary table 对齐，但正式稿需要数据源说明或作者文档支撑。

## 六、来源与本地文件

本地主要输出：

- `C:\Users\刘子轩\radar_outputs\extended_region_binomial_with_candidates\extended_region_binomial_report.md`
- `C:\Users\刘子轩\radar_outputs\candidate_worldcover_landcover_probe\candidate_worldcover_landcover_report.md`
- `C:\Users\刘子轩\radar_outputs\candidate_worldcover_landcover_probe\candidate_worldcover_landcover_group_summary.csv`
- `C:\Users\刘子轩\radar_outputs\candidate_worldcover_landcover_probe\candidate_worldcover_tile_access.csv`

外部数据源：

- ESA WorldCover data access: https://esa-worldcover.org/en/data-access
- ESA WorldCover AWS Open Data Registry: https://registry.opendata.aws/esa-worldcover-vito/
- ESA WorldCover v200 class table: https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200
- Copernicus Global Land Cover 100 m alternative source: https://land.copernicus.eu/en/products/global-dynamic-land-cover/copernicus-global-land-service-land-cover-100m-collection-3-epoch-2015-2019-globe
