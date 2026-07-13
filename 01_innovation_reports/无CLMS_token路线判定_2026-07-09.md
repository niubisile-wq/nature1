# 无 CLMS token 路线判定
日期：2026-07-09

## 结论
如果 CLMS / EGMS token 现实上拿不到，就不要继续把 EGMS 作为硬前提。

路线应改为：

**严格无 token 的 Open InSAR Observability Bias and Exposure Benchmark**

目标期刊定位也要同步调整：
- Nature 正刊：降为高风险冲刺，不再作为唯一目标；
- Nature Communications：可作为主攻；
- Scientific Data / ESSD：数据集版本可作为稳妥目标；
- Remote Sensing of Environment / ISPRS：方法与遥感产品偏差路线可作为备选。

## 为什么不能继续卡 EGMS
官方 EGMS API 已验证无 token 返回：

```json
{"status": false, "message": "Please log in to perform archive API calls."}
```

GEONET 也不能当完全无授权替代。GSI 页面说明外国研究者要提交申请表和 PC IP，等待 FTP 获取方式。因此 Japan GEONET 只能作为可申请增强源，不属于当前严格 no-token 主线。

## 新主线
主张不变，但证据结构调整：

> Public InSAR-derived subsidence knowledge is not missing at random; open-product observability and product availability censor exposure estimates in ways that depend on land cover, region, and product lineage.

中文：

> 公开 InSAR 沉降知识并非随机缺失；公开产品的可观测性和可获得性会按地表覆盖、区域和产品谱系系统性删失暴露估计。

## 严格 no-token 数据组合
### 已经本地落地
| 数据源 | 状态 | 用途 |
|---|---|---|
| LiCSAR / Nature 2026 delta VLM | 已跑多 delta 模型 | 主可观测性偏差证据 |
| WorldCover | 已纳入模型 | 解释地表覆盖混杂 |
| GHSL population / built-up | 已跑 VLM-grid exposure closure | 暴露闭环 |
| NGL MIDAS GNSS | 已下载并筛选 | 稀疏独立垂向运动锚点 |
| Japan LiCSBAS Zenodo | 已下载 Niigata 样本并解析 HDF5 | 非欧美公开产品扩展 |
| Iran nationwide InSAR Zenodo | 已下载 4 文件，rate/mask 栅格可读 | 干旱地下水沉降 benchmark 扩展 |

### 刚新增的 Iran 数据
输出目录：
`C:\Users\刘子轩\radar_outputs\iran_insar_zenodo_probe`

文件：
- `Iran_subsidence_rate_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.tif`
- `Iran_subsidence_rate_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.jpg`
- `Iran_subsidence_seasonal_amplitude_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.tif`
- `Iran_subsidence_mask_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.tif`

审计结果：
- rate GeoTIFF shape：17945 x 24060
- rate 有效像元：7,842,872
- rate median：1.80
- rate p95：10.30
- rate max：37.00
- mask GeoTIFF shape：17945 x 24060
- seasonal amplitude GeoTIFF 当前 `tifffile` 读取 offset 失败，需用 GDAL/rioxarray 复核

注意：Iran rate 的正负号约定必须回读论文/元数据后再写入 manuscript；当前不能直接用 `< -5 mm/yr` 当沉降阈值。

## 当前 lead cases
### 1. Chao Phraya
优势：
- WorldCover-adjusted OR = 3.56
- bootstrap CI = 2.25-5.78
- NGL stations = 6
- strong-subsidence population ≈ 20.63 million
- strong built-up ≈ 1200 km2

用途：
无 token 主线的最强实证 lead。

### 2. Po / Rhone
优势：
- Po OR = 1.33，CI = 1.13-1.56
- Rhone OR = 1.59，CI = 1.24-2.07
- 都有 NGL 锚点

限制：
没有 EGMS 时，欧洲高密度独立 benchmark 不闭环。

用途：
保留为 secondary lead，不再把它们作为 Nature 唯一主线。

### 3. Japan Niigata
优势：
- Zenodo 数据已选择性下载
- HDF5 `cum_filt.h5` 可读
- 111 时间点，2015-04-30 至 2020-02-09
- velocity 有效像元 34,000

限制：
LiCSAR/LiCSBAS 派生产品，不是独立真值。

用途：
产品谱系扩展，而不是独立验证。

### 4. Iran
优势：
- Science Advances 配套全国数据
- Zenodo 开放、无需 token
- 文件体量小，已下载本地
- 干旱地下水沉降主题强

限制：
不是独立真值；与地下水沉降文献高度重叠；符号约定需核实。

用途：
干旱地下水 no-token benchmark 扩展。

## 新 Go/No-Go
**Nature 正刊：No-token route = HIGH-RISK / not primary target.**

理由：
- 没有 EGMS 或等价高密度独立 benchmark；
- GEONET 也需要申请，不是 strict no-token；
- no-token 证据更适合证明“公开产品偏差数据集”，而不是 Nature 正刊级全球风险重估。

**Nature Communications / Scientific Data：GO。**

理由：
- 创新点已经落地；
- 多区域模型已跑；
- 暴露闭环已跑；
- Japan 和 Iran 新数据源已实际下载/解析；
- 可形成可仓储 benchmark 数据产品。

## 下一步
1. 把 Chao Phraya 作为 no-token 主图 lead。
2. 把 Japan Niigata 和 Iran 作为产品谱系扩展。
3. 把 Po / Rhone 保留为 EGMS 可用时升级的欧洲 lead。
4. 继续做 equal-area / polygon area-weighted exposure overlay。
5. 准备 Scientific Data / Nature Communications 双版本文章框架。
