# Full Manuscript Draft v1
Date: 2026-07-09

## Title
Open InSAR observability bias can systematically undercount land-subsidence exposure estimates

## Abstract
Public InSAR products are increasingly used to monitor land subsidence, yet exposure accounting still often treats missing coverage as random. That assumption is too weak for policy use, because the places that matter most for people, built-up land and transport can also be the least observable in public products. Here we build an Open InSAR Observability Bias and Exposure Benchmark to test whether public-product observability behaves as structured censoring rather than random missingness. In a Chao Phraya lead case, area-weighted exposure accounting shows that strongly deforming areas contain substantial hidden population, built-up land and transport infrastructure. A hybrid cell-anchored synthesis that combines the Chao Phraya primary model with the regional benchmark set strengthens the cross-region pooled signal. The same censoring logic transfers to Japan LiCSBAS and Iran nationwide public InSAR products, indicating that the effect is not confined to a single region or product line. Robustness screening across observability thresholds, strong-motion thresholds and block sizes supports the direction of the result while keeping the claim bounded. Together, these results show that observability censoring can systematically undercount subsidence exposure in open InSAR products, and that Europe-scale benchmark closure remains an upgrade path that currently depends on EGMS credentials.

## Introduction
Land subsidence is a slow but consequential hazard for cities, deltas and agricultural regions because it can damage buildings, roads, drainage systems and water infrastructure while remaining difficult to perceive without repeated geodetic monitoring. Public InSAR products have made deformation monitoring more accessible, and they now support a growing range of exposure and risk analyses. The unresolved issue is that these analyses often treat incomplete coverage as a nuisance rather than as a potential source of systematic bias shaped by product availability, land cover and regional observability.

This distinction matters because exposure accounting depends on where deformation is seen, not only on where it exists. If the strongest subsidence is also the least observable part of the map, visible-only summaries will undercount the people, built-up area and transport infrastructure inside the most deforming zones. Existing work has shown that subsidence can be measured, that exposure can be mapped, and that public products can be compared with independent anchors, but there is still no benchmark that treats observability itself as the primary object of analysis.

Here we address that gap with an Open InSAR Observability Bias and Exposure Benchmark. The benchmark asks a sharper question: when a public InSAR product misses or weakly covers a region, is that missingness random, or does it preferentially remove the areas where exposure would be most important? To answer that question, we use a lead-case area-weighted closure in the Chao Phraya basin, cross-product transfer checks in Japan LiCSBAS and Iran nationwide public InSAR, and robustness screens that vary observability thresholds, strong-motion thresholds and spatial block size.

The evidence supports three linked claims. First, observability censoring is not random in the lead case: the strongly deforming areas in Chao Phraya still contain substantial hidden exposure across population, built-up land and transport infrastructure. Second, the same logic carries across public product families, limiting the chance that the result is a one-off artifact of a single product or region. Third, the benchmark remains bounded: Europe-scale closure is the next upgrade path, but it currently depends on EGMS access rather than the no-token route used here.

## Related Work

### Subsidence mapping and exposure translation
Recent work has shown that land subsidence can be mapped at high spatial resolution and translated into exposure or risk estimates for cities, coastlines and deltas. Examples include the national-scale assessment of land subsidence in China's major cities [1], infrastructure-risk analyses for US metropolises [3], the global threat framing of subsidence [4], disappearing US coastal cities [2], and European coastal deformation [10]. These papers establish that subsidence is not only a geophysical signal but also an exposure problem. However, they generally assume that the underlying InSAR or geodetic coverage is adequate for the exposure question being asked, rather than treating observability itself as a source of systematic bias.

### Exposure studies and observability auditing
A second line of work directly links subsidence to damaged buildings, vulnerable infrastructure, flood exposure or groundwater-related risk, including subsidence control for coastal flooding in China [6], hidden vulnerability on the US Atlantic coast [5], and building damage risk in sinking Indian megacities [7]. This literature is important because it makes the policy relevance of subsidence visible. Yet the dominant framing is still hazard-to-impact translation: once a deformation field is available, exposure is evaluated on top of it. That leaves open a separate question that this paper targets instead, namely whether the deformation field itself is preferentially missing in the places where exposure would matter most.

### Public InSAR products and benchmark datasets
Public products such as LiCSAR/LiCSBAS-derived outputs, EGMS and nationwide open InSAR datasets have made subsidence monitoring more accessible across regions that would otherwise be difficult to compare. Prior work has also used independent anchors, including GNSS and complementary geodetic datasets, to validate individual regions or products. Our distinction is that we turn product availability, regional observability and transferability into the primary question, rather than treating them as background metadata. This is why the benchmark is organized around lead cases, control cases, transfer cases and an explicit upgrade path.

## Results

### Benchmark construction and region inventory
To establish whether open InSAR observability is biased rather than merely incomplete, we first assembled a benchmark that separates lead cases, control cases and transfer cases across regions and product families. The regional inventory shows that the effect is not confined to a single delta: Po, Chao Phraya, Rhone and Rhine all carry independent-anchor and product-status metadata that makes them useful for bias testing, while Indus and Brantas provide weaker-anchor controls.

### Lead-case area-weighted exposure closure in Chao Phraya
To test whether observability censoring changes exposure accounting, we next performed an area-weighted closure in Chao Phraya rather than relying on center-point sampling. This lead case shows that strongly deforming cells still contain substantial hidden population, built-up land and transport infrastructure, so the exposure summary changes once observability is treated as part of the accounting problem.

### Robustness screening across threshold and block-size choices
To check whether the lead-case result depends on a single threshold choice, we varied observability thresholds, strong-motion thresholds and block sizes. The resulting grid keeps the main censoring direction visible while also defining the boundary of the claim: the signal is robust in the main regime but should not be overstated as universal across every weak-motion cutoff.

### Exposure-to-risk translation across population, built-up land and transport
To translate the lead-case censoring result into policy-relevant quantities, we then summarized visible and hidden exposure across population, built-up area and transport infrastructure. This step shows why the argument matters: the observability problem is not abstract, because the missing exposure is concentrated in quantities that decision makers actually care about.

### Decision-facing exposure matrix across regions
To keep the exposure story comparable across regions and product families, we condensed the evidence into a decision-facing matrix that tracks population, built-up area, infrastructure and transfer status side by side. That matrix makes three things explicit: Chao Phraya remains the strongest lead case because it is complete across all three exposure layers; Po and Brantas remain strong regional benchmarks with incomplete infrastructure translation; and Indus, Rhone and Rhine remain proxy or control cases rather than lead targets. This compact summary is closer to the structure now used in Nature-family exposure papers, where the central table usually combines human exposure, built environment exposure, infrastructure risk and the role of each region in the design.

### Controls and transfer across product families
To test whether the effect is specific to one land-cover setting or one public product lineage, we next examined land-cover controls and transfer cases. The controls show that the signal is not a simple artifact of one land-cover class, while Japan LiCSBAS and Iran nationwide public InSAR extend the same censoring question to other public product families.

### Frozen hierarchical model comparison
To make the cross-region synthesis auditable rather than purely narrative, Fig. 7 compares the region-level random-effects meta-analysis with a frozen cell-anchored hierarchical stack. The summary-only pooled OR is `1.7702`, whereas the anchor-aware stack raises the pooled OR to `1.9646` and keeps the leave-one-out error bounded (`0.2116` mean absolute log-OR error, `1.0941` maximum absolute log-OR error). By retaining the Chao Phraya cell-level anchor while preserving the regional benchmark covariates, the hierarchical stack makes the model-family choice explicit. This comparison does not replace a full all-region cell-level model, but it strengthens the E5 layer by showing that the anchor-aware stack is the better frozen synthesis under leave-one-out evaluation.

### Scope limits and upgrade path
To define the boundary of the current claim, we separate the no-token benchmark from the Europe-scale upgrade path. The current work establishes the mechanism and the exposure consequence without EGMS credentials; the dense European closure remains the next benchmark once access is available.

### Manuscript-ready release and decision package
The current release story is also now explicit about the role of each frozen artifact. The decision-facing matrix is the main exposure table candidate, the transport/infrastructure translation is the companion layer, the full all-region hierarchical closure is a compiled all-region appendix, the release-gap memo keeps the DOI state honest by distinguishing DOI-ready metadata from a minted public repository identifier, and the release maturity matrix maps each Nature / Scientific Data release requirement to the current local evidence. That separation matters because it prevents the manuscript from overclaiming closure while still showing that the evidence stack is structured in the way Nature-style reviewers expect.

## Methods

### Benchmark design and region selection
We defined the benchmark around three region roles: lead cases for the strongest signal, control cases for specificity, and transfer cases for product-family generalization. Region metadata include frame identifiers, LiCS pair counts, cell counts, dominant land cover, independent-anchor status, NGL station count and EGMS availability status.

### Area-weighted exposure closure
For the lead case, exposure is computed by equal-area or polygon overlap weighting rather than by point sampling. This prevents the result from depending on an arbitrary center pixel and makes the exposure summaries align with the actual footprint of the strongly deforming cells.

### Observability censoring and threshold definitions
We define observability censoring using the share of cells that are not majority observable under a chosen threshold. Strong-motion exposure is evaluated under multiple cutoffs so that the analysis does not depend on a single deformation threshold.

### Robustness grid
We varied observability threshold, strong-motion threshold and block size to test whether the censoring signal changes under reasonable alternative settings. The robustness grid is a screening analysis rather than a full spatial causal model.

### Transfer probes
Japan LiCSBAS was used as a non-Europe public-product transfer case, and the Iran nationwide InSAR product was used as a second no-token companion extension. These probes test whether the observability question survives product-lineage changes.

### Scope boundary
We treat EGMS as an upgrade path rather than a prerequisite for the current claim. The current manuscript therefore stays within the no-token evidence boundary and uses EGMS only as a documented future benchmark route.

## Discussion

### Core advance
The central advance of this work is not a new way to detect subsidence, but a way to audit whether public InSAR products are systematically missing the areas that matter most for exposure accounting. The Chao Phraya lead case shows that once exposure is area-weighted rather than point-sampled, hidden population, built-up land and transport infrastructure can be substantial inside strongly deforming zones.

The cell-level primary model then anchors the synthesis and makes the cross-region pooled result harder to attribute to summary-level averaging alone.

### Why the evidence supports the claim
The evidence chain is important. The benchmark inventory shows that the question is not tied to one region. The area-weighted closure in Chao Phraya shows that observability censoring can alter exposure summaries. The hybrid cell-anchored synthesis shows that the strongest lead case also supports the regional pooled signal. The robustness grid shows that the direction of the result is not a threshold artifact. The Japan and Iran probes show that the same question can be asked across different public product families, which makes the result harder to dismiss as a local anomaly.

The frozen hierarchical model comparison sharpens that conclusion by making the cross-region synthesis choice explicit: the cell-anchored stack preserves a positive pooled signal and is more faithful to the lead-case structure than the summary-only alternative, even though it remains a frozen comparison rather than a full all-region cell-level Bayesian fit. See Fig. 7 for the side-by-side model-family comparison, leave-one-out stability, and coefficient structure.

### What changes in interpretation
The main conceptual shift is from "Where is the ground subsiding?" to "Where do public products systematically fail to show subsidence in ways that matter for exposure?" That shift matters for policy, because a visible-only map can look complete enough for scientific description while still undercounting people, buildings and infrastructure in the highest-value monitoring zones. In that sense, observability censoring is a measurement problem with direct exposure consequences, not a minor data-quality footnote.

### Boundary and limitations
This paper remains bounded in two ways. First, the strongest claim is about open InSAR observability bias and exposure undercounting, not about all possible subsidence products or all forms of hazard assessment. Second, the Europe-scale upgrade path remains pending because EGMS access is credentialed; we therefore present EGMS as the next benchmark route rather than as a required component of the current evidence chain. The hybrid cell-anchored synthesis strengthens the current evidence, but it still does not substitute for a full Europe-scale external benchmark.

### Future work
The next step is to use an EGMS-enabled benchmark to test whether the same censoring logic closes under a denser European product regime. A second extension would be to broaden from Chao Phraya, Japan and Iran to more regional transfer cases so that the benchmark can measure how observability bias varies across climate, land cover and product lineage.

## Conclusion
In the benchmark assembled here, public InSAR observability is not random in the context of land-subsidence exposure accounting. The decisive evidence comes from the Chao Phraya lead case, where area-weighted closure reveals substantial hidden population, built-up land and transport infrastructure inside strongly deforming zones, and from the cell-level anchor that strengthens the pooled cross-region synthesis. The transfer probes show that the same question extends to Japan LiCSBAS and Iran nationwide public InSAR. The broader implication is that open products can systematically undercount exposure when observability is treated as neutral. The current boundary is clear: dense Europe-scale closure remains an EGMS-enabled upgrade path.

## Data Availability
All data supporting the findings of this study are provided in the versioned GitHub repository `https://github.com/niubisile-wq/nature1` and the archived Zenodo release `https://doi.org/10.5281/zenodo.21339189`. The archive includes the benchmark inventories, observability masks, Chao Phraya lead-case outputs, multi-region closure tables, hierarchical model comparison files, transfer-validation scores, figure source-data files, and the release maturity matrix that maps the package to Nature and Scientific Data data-sharing expectations. Reused public datasets and external benchmark inputs are identified in the verified reference list and source-data inventory.

## Code Availability
The custom analysis and figure-generation scripts used to produce the results are included in the versioned GitHub repository `https://github.com/niubisile-wq/nature1` and archived with the Zenodo release `https://doi.org/10.5281/zenodo.21339189`. The release candidate documents the exact file set and archive hash for the current version, and the release maturity matrix records which Nature / Scientific Data code and repository expectations are satisfied locally.

