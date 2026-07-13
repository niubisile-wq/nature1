# 创新点落地状态：Open InSAR Observability Benchmark v0.1
日期：2026-07-09

## 现在做的方向
方向已经从普通沉降制图转为：公开 InSAR 产品的可观测性删失是否会系统性低估沉降暴露。

核心数据产品名：
**Open InSAR Observability Bias and Exposure Benchmark**

## v0.1 已落地内容
- 多 delta LiCSAR 可观测性与强沉降关系已经统一进一张证据表。
- WorldCover 地表覆盖控制已经纳入主模型。
- NGL GNSS 独立锚点已经接入，用于判断每个区域是否有外部垂向运动约束。
- EGMS API 查询包已经生成，等待 CLMS token 后即可跑欧洲高密度 benchmark。
- 数据源 inventory 已经按 Nature 数据可用性要求分清复用数据、派生数据和本地分析输出。

## 主结果判定

| Region | Signal | OR | Boot 95% CI | NGL stations | EGMS | Readiness |
|---|---|---:|---|---:|---|---|
| Po | positive | 1.32894 | 1.129–1.55664 | 8 | query_pack_ready_token_required | conditional_nature_go_after_egms |
| Chao Phraya | strong_positive | 3.56187 | 2.25134–5.78079 | 6 | not_applicable | benchmark_v0_landed_needs_dense_truth |
| Indus | strong_positive | 3.3894 | 2.32898–4.86955 | 1 | not_applicable | statistical_signal_needs_independent_anchor |
| Rhone | positive | 1.59178 | 1.23975–2.07457 | 6 | query_pack_ready_token_required | conditional_nature_go_after_egms |
| Brantas | positive | 1.59171 | 1.01473–2.69633 | 1 | not_applicable | statistical_signal_needs_independent_anchor |
| Rhine | inconclusive | 0.810149 | 0.544942–1.26623 | 40 | query_pack_ready_token_required | control_or_specification_case |

## 现在能不能说创新点落地
**可以说 v0.1 落地，但不能说 Nature 正刊证据最终落地。**

已经落地的是机制框架和可复现实证骨架：强沉降、公开产品失败概率、地表覆盖、GNSS 锚点和 EGMS 查询路径已经进入同一数据产品。
还没落地的是 Nature 级的高密度独立 benchmark 闭环，也就是 EGMS 下载和对齐。

## 当前 lead cases
- `Po`：统计信号 + NGL 锚点 + EGMS 查询包齐备，等 EGMS token 后优先闭环。
- `Rhone`：统计信号 + NGL 锚点 + EGMS 查询包齐备，等 EGMS token 后优先闭环。

## 无 EGMS 也能继续推进的 v0 cases
- `Chao Phraya`：已有统计信号和 GNSS 锚点，但仍缺高密度独立 benchmark。

## 外部扩展候选

| Candidate | Priority | NGL stations | Median up mm/yr | Role |
|---|---:|---:|---:|---|
| Japan_Kanto | A | 230 | 5.606 | japan_licsbas_extension_case / - |
| Japan_Niigata | A | 78 | 3.811 | japan_licsbas_extension_case / niigata_h5_velocity_ingested |
| Mexico_City | A | 25 | -1.737 | extreme_subsidence_anchor_case / - |
| Jakarta | C | 3 | -0.951 | secondary_candidate / - |

## 下一步
1. 拿到 CLMS `token.jwt` 后执行 EGMS 查询包。
2. 对 Po、Rhone、Rhine/Netherlands 下载 L3 ORTHO-UP，并转成统一网格 benchmark。
3. 用 GHSL built-up、GHSL population、OSM/建筑物层做 area-weighted exposure overlay。
4. 输出 figure source data 和仓储 README，准备 Zenodo/Dryad/PANGAEA 记录。
