# Claim Collision Matrix
日期：2026-07-09

## 结论
我们的主张不是“又一篇沉降图”。

本课题要保住的创新边界是：

> **Open InSAR observability bias systematically censors land-subsidence exposure estimates.**

中文：

> **公开 InSAR 产品的可观测性删失会系统性低估沉降暴露。**

这一定义必须和以下已有高水平论文区分开：

## 逐篇撞车审计
### 1. Ao et al., Science 2024, China cities
- 他们做的是 82 个中国主要城市的全国尺度沉降评估。
- 核心是 Sentinel-1 InSAR + GNSS 验证 + P3mm/P10mm/V5th 指标 + 暴露和情景转换。
- 与我们的差异：
  - 他们回答“哪里在沉降、沉降多严重”。
  - 我们回答“公开 InSAR 证据链在哪里可见、哪里被系统性删失，以及这会低估多少暴露”。
- 撞车风险：
  - 很高，如果我们继续写成“多区域沉降图”会直接撞。
- 我们的防撞策略：
  - 保留 `observability_failure` 和 `risk_underestimation_factor`；
  - 主图聚焦 Chao Phraya / Po / Rhone / Japan / Iran 的可观测性与暴露删失，而不是单纯沉降分布。

### 2. Ohenhen et al., Nature 2024, Disappearing cities on US coasts
- 他们把 VLM、LiDAR DEM、SSP sea level、人口、房产、防护设施合成 32 个美国海岸城市的 2050 暴露模型。
- 核心是高分辨率地球物理层 + 情景 hazard model + 暴露与不确定性。
- 与我们的差异：
  - 他们的主问题是“未来海岸城市会怎样消失”。
  - 我们的主问题是“公开 InSAR 观测是否把已存在的暴露系统性删掉”。
- 撞车风险：
  - 高，如果我们只做 coastal exposure。
- 防撞策略：
  - 暴露不只是未来 sea-level scenario，而是 visible-only vs full-deformation counterfactual。

### 3. Ohenhen et al., Nature Cities 2025, US metropolises
- 他们在 28 个美国大城市中估计沉降风险，并转成建筑损伤和人口影响。
- 与我们的差异：
  - 他们是城市风险转译；
  - 我们是产品偏差审计和暴露删失。
- 防撞策略：
  - 不把主线写成 infrastructure risk paper；
  - 把建成区/道路/农业暴露作为 bias 结果，而不是最终结论。

### 4. Ohenhen et al., Nature Communications 2023, US Atlantic coast
- 他们把 vertical land motion 与土地覆盖、海岸脆弱性结合，强调不考虑 VLM 会低估 vulnerability。
- 与我们的差异：
  - 他们是 VLM 对 coastal vulnerability 的修正；
  - 我们是 open-product observability 对 exposure 的删失审计。
- 防撞策略：
  - 继续保留 WorldCover 控制；
  - 但把重点放在 failure mechanism，而不是沿海脆弱性本身。

### 5. Oelbermann et al., Nature Communications 2026, densely populated coasts
- 他们用多源 VLM 数据算人口加权相对海平面变化，强调数据可用性和 VLM 限制。
- 与我们的差异：
  - 他们是 exposure-weighted sea-level rise；
  - 我们是 exposure-weighted observability failure。
- 防撞策略：
  - 我们的 counterfactual 必须是“可见像元”对“全部 strong motion 像元”的暴露差。

### 6. Nicholls et al., Nature Climate Change 2021, global subsidence / flood exposure
- 他们给出全球海岸 subsidence、相对海平面变化和 flood exposure 的大尺度分析。
- 与我们的差异：
  - 他们是 coastal flood exposure 的全球综合；
  - 我们是 open InSAR 产品覆盖偏差和删失机制。
- 撞车风险：
  - 中高，尤其如果我们写成全球 flood exposure 论文。
- 防撞策略：
  - 只把他们作为背景，不作为主竞争对手。

### 7. Wu et al., GRL 2022, subsidence in coastal cities throughout the world observed by InSAR
- 他们是全球海岸城市 InSAR 沉降观测综述/分析。
- 与我们的差异：
  - 他们做“世界各地都在沉降”；
  - 我们做“为什么公开证据链会漏掉沉降暴露”。
- 撞车风险：
  - 中高。

### 8. Science Advances 2024 Iran
- 他们是全国尺度 InSAR 监测、地下水/灌溉机制和开放数据。
- 与我们的差异：
  - 他们是全国沉降研究；
  - 我们把 Iran 作为 no-token 产品谱系扩展和 transfer case。
- 撞车风险：
  - 如果把 Iran 写成主创新，会撞。

### 9. Japan LiCSBAS 2021
- 他们是全国日本城市 deformation monitoring 的产品化流程。
- 与我们的差异：
  - 他们讲可复现产品处理；
  - 我们讲公开产品偏差和暴露删失。
- 防撞策略：
  - Japan 只做 transfer / lineage extension，不做主创新。

### 10. European coastal deformation / similar recent Nature and AGU papers
- 它们多在讲海岸变形、RSL、风险和暴露。
- 与我们的差异：
  - 它们仍然是 hazard / exposure 研究；
  - 我们是 evidence-chain bias study。

## 创新边界
以下表述不要再用：
- “多区域沉降暴露图”
- “全球沉降风险重估”
- “单纯地表覆盖解释沉降”

以下表述应该保留：
- “公开 InSAR 观测的删失机制”
- “observability failure”
- “monitoring debt”
- “risk_underestimation_factor”
- “product-lineage / land-cover / time-sampling transfer function”

## 结论
如果本文写成“沉降在哪里”，会和大量高水平论文撞。

如果本文写成“公开 InSAR 证据链在哪里被系统性删掉，以及这会低估多少暴露”，创新边界才成立。
