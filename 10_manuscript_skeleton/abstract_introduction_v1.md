# Abstract and Introduction Draft v1
Date: 2026-07-09

## Abstract
Public InSAR products are increasingly used to monitor land subsidence, but exposure accounting still treats missing coverage as if it were random. That assumption is too weak for policy use, because the areas that matter most for people, built-up land and transport can also be the least observable in public products. Here we build an Open InSAR Observability Bias and Exposure Benchmark and use it to test whether public-product observability is structured censoring rather than random missingness. In a Chao Phraya lead case, area-weighted exposure accounting shows that strongly deforming areas contain substantial hidden population, built-up land and transport infrastructure. The same censoring logic transfers to Japan LiCSBAS and Iran nationwide public InSAR products, indicating that the effect is not confined to a single region or product line. Robustness screening across observability thresholds, strong-motion thresholds and block sizes supports the direction of the result while keeping the claim bounded. Together, these results show that observability censoring can systematically undercount subsidence exposure in open InSAR products, and that Europe-scale benchmark closure remains an upgrade path that currently depends on EGMS credentials.

## Introduction
Land subsidence is a slow but consequential hazard for cities, deltas and agricultural regions because it can damage buildings, roads, drainage systems and water infrastructure while remaining difficult to perceive without repeated geodetic monitoring. Public InSAR products have made deformation monitoring more accessible, and they now support a growing range of exposure and risk analyses. The remaining problem is that these analyses often assume that public coverage is merely incomplete, rather than structurally biased by product availability, land cover and regional observability.

This distinction matters because exposure accounting depends on where the deformation is seen, not only on where it exists. If the strongest subsidence is also the least observable part of the map, then visible-only summaries will undercount the people, built-up area and transport infrastructure that sit inside the most deforming zones. Existing work has shown that subsidence can be measured, that exposure can be mapped, and that public products can be compared to independent anchors, but there is still no benchmark that treats observability itself as the object of analysis.

Here we address that gap with an Open InSAR Observability Bias and Exposure Benchmark. The benchmark is designed to ask a simple but sharper question: when a public InSAR product misses or weakly covers a region, is that missingness random, or does it preferentially remove the areas where exposure would be most important? To answer that question, we use a lead-case area-weighted closure in the Chao Phraya basin, cross-product transfer checks in Japan LiCSBAS and Iran nationwide public InSAR, and robustness screens that vary observability thresholds, strong-motion thresholds and spatial block size.

The resulting evidence supports three linked claims. First, observability censoring is not random in the lead case: the strongly deforming areas in Chao Phraya still contain substantial hidden exposure across population, built-up land and transport infrastructure. Second, the same logic carries across public product families, which limits the chance that the result is a one-off artifact of a single product or region. Third, the benchmark remains intentionally bounded: Europe-scale closure is the next upgrade path, but it currently depends on EGMS access rather than the no-token route used here.

## Section outline
- Paragraph 1: field importance and why exposure accounting matters for subsidence monitoring.
- Paragraph 2: why visible-only or incomplete coverage is not enough for exposure inference.
- Paragraph 3: the benchmark question and the lead-case / transfer design.
- Paragraph 4: the three claims and the scope boundary.

## Assumptions or missing inputs
- Full citations are still to be inserted in the prose.
- The manuscript is currently framed as a research article with a data-enabled mechanism story; if the final target becomes Scientific Data or ESSD, the abstract should be shortened and re-centered on the benchmark product.

## Claim-evidence map
- Claim: public InSAR products are increasingly used for subsidence monitoring | Evidence: benchmark framing and assembled dataset inventory | Status: supported
- Claim: missing coverage should not be treated as random for exposure accounting | Evidence: Chao Phraya exposure closure, cross-product transfer, robustness screening | Status: supported by current evidence
- Claim: hidden exposure is substantial in Chao Phraya | Evidence: area-weighted GHSL and transport summaries | Status: supported
- Claim: the censoring logic transfers to Japan LiCSBAS and Iran | Evidence: Japan Niigata HDF5 summary and Iran nationwide probe | Status: supported but still needs formal citations in the manuscript
- Claim: Europe-scale benchmark closure remains an EGMS-dependent upgrade path | Evidence: EGMS query pack and token-required status | Status: supported

## Why this structure
- The abstract follows the challenge -> contribution -> result -> transfer -> boundary pattern.
- The introduction opens with application relevance, then tightens to the observability problem rather than repeating a general subsidence review.
- Each paragraph does one job so the claim chain stays readable and reviewable.

## Chinese notes
- 这版不是“沉降区很多”的常规写法，而是把主问题定成“公开 InSAR 可观测性是否结构性删失暴露”。
- 结尾边界没有写成失败，而是写成后续升级路径，避免把 no-token 路线说死。
- 现在最需要补的是正式引用和最终 target journal 的口径微调。

## To redirect me
指出哪一段的主张、力度或边界不对，我只改那一段，不重写整篇。
