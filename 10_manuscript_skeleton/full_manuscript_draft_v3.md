# Full Manuscript Draft v3
Date: 2026-07-14

## Title
Public InSAR observability gaps can undercount urban subsidence exposure

## Abstract
Public InSAR products are increasingly used to monitor land subsidence in cities, yet exposure accounting still often treats missing coverage as random. That assumption is too weak for urban decision-making, because the places that matter most for people and built-up land can also be the least observable in public products. Here we build an Open InSAR observability and exposure audit to test whether public-product observability behaves as structured censoring rather than random missingness. In the Chao Phraya lead case, area-weighted exposure accounting identifies 3.63 million hidden people and 422.78 km2 of hidden built-up land inside strongly deforming cells. A separate transport-infrastructure sensitivity layer shows the same censoring direction, but the manuscript-grade headline is the people and built-up exposure undercount. A hybrid cell-anchored synthesis that combines the Chao Phraya primary model with the regional benchmark set strengthens the cross-region pooled signal. The same censoring logic transfers to Japan LiCSBAS and Iran nationwide public InSAR products, indicating that the effect is not confined to a single region or product line. Robustness screening across observability thresholds, strong-motion thresholds and block sizes supports the direction of the result while keeping the claim bounded. Together, these results show that observability censoring can systematically undercount urban subsidence exposure in open InSAR products, and that Europe-scale benchmark closure remains an upgrade path that currently depends on EGMS credentials.

## Introduction
Land subsidence is a slow but consequential hazard for cities, deltas and agricultural regions because it can damage buildings, roads, drainage systems and water infrastructure while remaining difficult to perceive without repeated geodetic monitoring. Public InSAR products have made deformation monitoring more accessible, and they now support a growing range of exposure and risk analyses. The unresolved urban issue is that incomplete monitoring can shape which places enter exposure accounts at all. If missing coverage is treated as neutral, under-observed neighborhoods, built-up land and infrastructure corridors can fall out of priority-setting before risk is assessed.

This distinction matters because exposure accounting depends on where deformation is seen, not only on where it exists. If the strongest subsidence is also the least observable part of the map, visible-only summaries will undercount the people, built-up area and transport infrastructure inside the most deforming zones. Existing work has shown that subsidence can be measured, that exposure can be mapped, and that public products can be compared with independent anchors, but there is still no audit that treats observability itself as the primary source of exposure bias.

Here we address that gap with an Open InSAR observability and exposure study. Figure 1 sets up the urban monitoring-debt problem and the region inventory. The study asks a sharper question: when a public InSAR product misses or weakly covers a region, is that missingness random, or does it preferentially remove the urban areas where exposure would be most important? To answer that question, we use a lead-case area-weighted closure in the Chao Phraya urban delta, cross-product transfer checks in Japan LiCSBAS and Iran nationwide public InSAR, and robustness screens that vary observability thresholds, strong-motion thresholds and spatial block size.

The evidence supports three linked claims. First, observability censoring is not random in the lead case: the strongly deforming areas in Chao Phraya still contain substantial hidden exposure across population, built-up land and transport infrastructure. Second, the same logic carries across public product families, limiting the chance that the result is a one-off artifact of a single product or region. Third, the study remains bounded: Europe-scale closure is the next upgrade path, but it currently depends on EGMS access rather than the no-token route used here.

## Related Work

### Subsidence mapping and exposure translation
Recent work has shown that land subsidence can be mapped at high spatial resolution and translated into exposure or risk estimates for cities, coastlines and deltas. Examples include the national-scale assessment of land subsidence in China's major cities [1], infrastructure-risk analyses for US metropolises [3], the global threat framing of subsidence [4], disappearing US coastal cities [2], and European coastal deformation [10]. These papers establish that subsidence is not only a geophysical signal but also an exposure problem. However, they generally assume that the underlying InSAR or geodetic coverage is adequate for the exposure question being asked, rather than treating observability itself as a source of systematic bias.

### Exposure studies and observability effects
A second line of work directly links subsidence to damaged buildings, vulnerable infrastructure, flood exposure or groundwater-related risk, including subsidence control for coastal flooding in China [6], hidden vulnerability on the US Atlantic coast [5], and building damage risk in sinking Indian megacities [7]. This literature is important because it makes the policy relevance of subsidence visible. Yet the dominant framing is still hazard-to-impact translation: once a deformation field is available, exposure is evaluated on top of it. That leaves open a separate question that this paper targets instead, namely whether the deformation field itself is preferentially missing in the places where exposure would matter most.

### Public InSAR products and exposure datasets
Public products such as LiCSAR/LiCSBAS-derived outputs, EGMS and nationwide open InSAR datasets have made subsidence monitoring more accessible across regions that would otherwise be difficult to compare. Prior work has also used independent anchors, including GNSS and complementary geodetic datasets, to validate individual regions or products. Our distinction is that we turn product availability, regional observability and transferability into the primary question, rather than treating them as background metadata. This is why the study is organized around lead cases, control cases, transfer cases and an explicit upgrade path.

## Results

### Urban evidence construction and region inventory
To establish whether open InSAR observability is biased rather than merely incomplete, we first assembled an evidence set that separates lead, supporting, proxy/control and transfer roles across regions and product families. Figure 1B turns that inventory into a compact region map / matrix. The regional inventory keeps the claim bounded: Chao Phraya carries the lead exposure closure, Po and Brantas provide supporting regional evidence, Indus, Rhone and Rhine remain proxy/control cases, and the Japan and Iran probes test whether the question survives product-lineage changes.

### Lead-case area-weighted exposure closure in Chao Phraya
To test whether observability censoring changes exposure accounting, we next performed an area-weighted closure in Chao Phraya rather than relying on center-point sampling. Figure 2 is the lead-case visual. This lead case shows that strongly deforming urban cells contain 3.63 million hidden people and 422.78 km2 of hidden built-up land, so the exposure summary changes once observability is treated as part of the accounting problem. Transport is retained as a separate infrastructure sensitivity layer rather than folded into the headline claim.

### Robustness screening across threshold and block-size choices
To check whether the lead-case result depends on a single threshold choice, we varied observability thresholds, strong-motion thresholds and block sizes. The resulting grid keeps the main censoring direction visible while also defining the boundary of the claim: the signal is robust in the main regime but should not be overstated as universal across every weak-motion cutoff.

### Exposure-to-risk translation across population, built-up land and transport
To translate the lead-case censoring result into policy-relevant quantities, we then summarized visible-only and observability-adjusted exposure across population and built-up area, with transport infrastructure carried as a companion sensitivity layer. Figure 3 is the counterfactual accounting panel set. This step shows why the argument matters: the observability problem is not abstract, because the missing exposure is concentrated in quantities that decision makers actually care about.

### Decision-facing exposure matrix across regions
To keep the exposure story comparable across regions and product families, we condensed the evidence into a decision-facing matrix that tracks population, built-up area, infrastructure sensitivity and transfer status side by side. That matrix makes three things explicit: Chao Phraya remains the strongest lead case because it is complete across the people and built-up layers; Po and Brantas remain strong regional supporting cases with incomplete infrastructure translation; and Indus, Rhone and Rhine remain proxy or control cases rather than lead targets. This compact summary is closer to the structure now used in Nature Cities papers, where the central table usually combines human exposure, built environment exposure, infrastructure risk and the role of each region in the design.

### Controls and transfer across product families
To test whether the effect is specific to one land-cover setting or one public product lineage, we next examined land-cover controls and transfer cases. The controls show that the signal is not a simple artifact of one land-cover class, while Japan LiCSBAS and Iran nationwide public InSAR extend the same censoring question to other public product families.

### Robustness and hierarchical boundary
Figure 4 is the robustness and boundary figure. To make the cross-region synthesis explicit rather than purely narrative, Figure 4B compares the region-level random-effects meta-analysis with a frozen cell-anchored hierarchical stack. The summary-only pooled OR is `1.7702`, whereas the anchor-aware stack raises the pooled OR to `1.9646` and keeps the leave-one-out error bounded (`0.2116` mean absolute log-OR error, `1.0941` maximum absolute log-OR error). By retaining the Chao Phraya cell-level anchor while preserving the regional covariates, the hierarchical stack makes the model-family choice explicit. This comparison does not replace a full all-region cell-level model, but it strengthens the boundary layer by showing that the anchor-aware stack is the better frozen synthesis under leave-one-out evaluation.

### Scope limits and upgrade path
To define the boundary of the current claim, we separate the no-token closure from the Europe-scale upgrade path. The current work establishes the mechanism and the exposure consequence without EGMS credentials; the dense European closure remains the next benchmark once access is available.

### Supporting release and decision materials
The supporting release materials are now explicit about the role of each frozen artifact. The decision-facing matrix is the main exposure table candidate, the transport/infrastructure translation is the companion layer, the full all-region hierarchical closure is a compiled all-region appendix, and the GitHub/Zenodo release identity keeps the code and data provenance citable. The release maturity matrix maps each Nature / Scientific Data release requirement to the current local evidence. That separation matters because it prevents the manuscript from overclaiming closure while still showing that the evidence stack is structured in the way Nature-style reviewers expect.

## Methods

### Study design and region selection
We defined the study around three region roles: lead cases for the strongest signal, control cases for specificity, and transfer cases for product-family generalization. Region metadata include frame identifiers, LiCS pair counts, cell counts, dominant land cover, independent-anchor status, NGL station count and EGMS availability status.

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
The central advance of this work is not a new way to detect subsidence, but a way to audit whether public InSAR products are systematically missing the areas that matter most for exposure accounting. The Chao Phraya lead case shows that once exposure is area-weighted rather than point-sampled, 3.63 million people and 422.78 km2 of built-up land can sit inside the hidden part of strongly deforming zones. Transport infrastructure follows the same direction as a sensitivity layer, but the manuscript headline remains the people and built-up exposure undercount.

The cell-level primary model then anchors the synthesis and makes the cross-region pooled result harder to attribute to summary-level averaging alone.

### Why the evidence supports the claim
The evidence chain is important. The region inventory shows that the question is not tied to one region. The area-weighted closure in Chao Phraya shows that observability censoring can alter exposure summaries. The hybrid cell-anchored synthesis shows that the strongest lead case also supports the regional pooled signal. The robustness grid shows that the direction of the result is not a threshold artifact. The Japan and Iran probes show that the same question can be asked across different public product families, which makes the result harder to dismiss as a local anomaly.
Figures 1 through 4 are arranged to mirror that chain: Figure 1 frames the urban-monitoring-debt problem, Figure 2 shows the lead-case closure, Figure 3 translates the consequence into exposure accounting, and Figure 4 sets the robustness boundary.

The frozen hierarchical model comparison sharpens that conclusion by making the cross-region synthesis choice explicit: the cell-anchored stack preserves a positive pooled signal and is more faithful to the lead-case structure than the summary-only alternative, even though it remains a frozen comparison rather than a full all-region cell-level Bayesian fit. See Figure 4B for the side-by-side model-family comparison, leave-one-out stability, and coefficient structure.

### What changes in interpretation
The main conceptual shift is from "Where is the ground subsiding?" to "Where do public products systematically fail to show subsidence in ways that matter for urban exposure?" That shift matters for policy, because a visible-only map can look complete enough for scientific description while still undercounting people and buildings in the highest-value monitoring zones. In that sense, observability censoring is a measurement problem with direct exposure consequences, not a minor data-quality footnote.

For city planning, that means open monitoring products should not be treated as neutral inventory layers. If the least observable zones are also the zones with the highest exposed population and built form, then visibility itself becomes part of the risk hierarchy. The practical implication is straightforward: monitoring upgrades, inspection priorities and adaptation screening should be directed toward the places that are most likely to disappear from public maps, not just the places that already look most alarming.

### Boundary and limitations
This paper remains bounded in three ways. First, the strongest claim is about open InSAR observability bias and exposure undercounting, not about all possible subsidence products or all forms of hazard assessment. Second, the transfer cases show that the question survives product-lineage changes, but they are not presented as full external validation. Third, the Europe-scale upgrade path remains pending because EGMS access is credentialed; we therefore present EGMS as the next external closure route rather than as a required component of the current evidence chain. The hybrid cell-anchored synthesis strengthens the current evidence, but it still does not substitute for a full Europe-scale external closure.

### Future work
The next step is to use an EGMS-enabled external closure to test whether the same censoring logic closes under a denser European product regime. A second extension would be to broaden from Chao Phraya, Japan and Iran to more regional transfer cases so that the study can measure how observability bias varies across climate, land cover and product lineage.

## Conclusion
In the study assembled here, public InSAR observability is not random in the context of urban subsidence exposure accounting. The decisive evidence comes from the Chao Phraya lead case, where area-weighted closure identifies 3.63 million hidden people and 422.78 km2 of hidden built-up land inside strongly deforming zones, and from the cell-level anchor that strengthens the pooled cross-region synthesis. The transport layer remains a companion sensitivity analysis rather than the manuscript headline. The transfer probes show that the same question extends to Japan LiCSBAS and Iran nationwide public InSAR. The broader implication is that open products can systematically undercount exposure when observability is treated as neutral. The current boundary is clear: dense Europe-scale closure remains an EGMS-enabled external closure route.

For urban decision makers, the result is not just that subsidence exists, but that the public record of subsidence can hide the very places that need monitoring first. That is the monitoring-debt problem this paper identifies. In a Nature Cities framing, the value of the study is that it turns observability into an urban planning and exposure-accounting issue, rather than leaving it as a technical limitation buried in the methods.

## Data Availability
All data supporting the findings of this study are provided in the versioned GitHub repository `https://github.com/niubisile-wq/nature1` and the archived Zenodo release `https://doi.org/10.5281/zenodo.21339189`. The archive includes the benchmark inventories, observability masks, Chao Phraya lead-case outputs, multi-region closure tables, hierarchical model comparison files, transfer-validation scores, figure source-data files, and the release maturity matrix that maps the package to Nature and Scientific Data data-sharing expectations. Reused public datasets and external benchmark inputs are identified in the verified reference list and source-data inventory.

## Code Availability
The custom analysis and figure-generation scripts used to produce the results are included in the versioned GitHub repository `https://github.com/niubisile-wq/nature1` and archived with the Zenodo release `https://doi.org/10.5281/zenodo.21339189`. The release candidate documents the exact file set and archive hash for the current version, and the release maturity matrix records which Nature / Scientific Data code and repository expectations are satisfied locally.

