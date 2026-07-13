# Related Work and Discussion Draft v1
Date: 2026-07-09

## Related Work

### Topic 1. Subsidence mapping has moved from local case studies to city-, national- and delta-scale exposure analyses
Recent work has shown that land subsidence can be mapped at high spatial resolution and translated into exposure or risk estimates for cities, coastlines and deltas. Examples include national-scale urban assessments in China (Science, 2024), infrastructure-risk analyses for US metropolises (Nature, 2025), global or multi-country subsidence mapping, and delta-focused vulnerability studies that emphasize the consequences of relative sea-level rise and flood exposure. These papers establish that subsidence is not only a geophysical signal but also an exposure problem. However, they generally assume that the underlying InSAR or geodetic coverage is adequate for the exposure question being asked, rather than treating observability itself as a source of systematic bias.

### Topic 2. Exposure studies are strong on hazard translation, but weak on observability auditing
A second line of work directly links subsidence to damaged buildings, vulnerable infrastructure, flood exposure or groundwater-related risk. This literature is important because it makes the policy relevance of subsidence visible. Yet the dominant framing is still hazard-to-impact translation: once a deformation field is available, exposure is evaluated on top of it. That leaves open a separate question that this paper targets instead, namely whether the deformation field itself is preferentially missing in the places where exposure would matter most.

### Topic 3. Public InSAR products and benchmark datasets enable broad coverage, but product lineage is rarely treated as the object of analysis
Public products such as LiCSAR/LiCSBAS-derived outputs, EGMS and nationwide open InSAR datasets have made subsidence monitoring more accessible across regions that would otherwise be difficult to compare. Prior work has also used independent anchors, including GNSS and complementary geodetic datasets, to validate individual regions or products. Our distinction is that we turn product availability, regional observability and transferability into the primary question, rather than treating them as background metadata. This is why the benchmark is organized around lead cases, control cases, transfer cases and an explicit upgrade path.

## Discussion

### Core advance
The central advance of this work is not a new way to detect subsidence, but a way to audit whether public InSAR products are visibly missing the very areas that matter for exposure accounting. The Chao Phraya lead case shows that once exposure is area-weighted rather than point-sampled, hidden population, built-up land and transport infrastructure can be substantial inside strongly deforming zones.

### Why the evidence supports the claim
The evidence chain matters. The benchmark inventory shows that the question is not tied to one region. The area-weighted closure in Chao Phraya shows that observability censoring can alter exposure summaries. The robustness grid shows that the direction of the result is not a threshold artifact. The Japan and Iran probes show that the same question can be asked across different public product families, which makes the result harder to dismiss as a local anomaly.

### What changes in interpretation
The main conceptual shift is from "Where is the ground subsiding?" to "Where do public products systematically fail to show subsidence in ways that matter for exposure?" That shift matters for policy, because a visible-only map can look complete enough for scientific description while still undercounting people, buildings and infrastructure in the highest-value monitoring zones. In that sense, observability censoring is a measurement problem with direct exposure consequences, not a minor data-quality footnote.

### Boundary and limitations
This paper remains bounded in two ways. First, the strongest claim is about open InSAR observability bias and exposure undercounting, not about all possible subsidence products or all forms of hazard assessment. Second, the Europe-scale upgrade path remains pending because EGMS access is credentialed; we therefore present EGMS as the next benchmark route rather than as a required component of the current evidence chain.

### Future work
The next step is to use an EGMS-enabled benchmark to test whether the same censoring logic closes under a denser European product regime. A second extension would be to broaden from Chao Phraya, Japan and Iran to more regional transfer cases so that the benchmark can measure how observability bias varies across climate, land cover and product lineage.

## Section outline
- Related Work 1: subsidence mapping and exposure translation.
- Related Work 2: exposure studies and observability auditing gap.
- Related Work 3: public products, anchors and product lineage.
- Discussion 1: core advance.
- Discussion 2: why the evidence supports the claim.
- Discussion 3: what changes in interpretation.
- Discussion 4: boundary and limitations.
- Discussion 5: future work.

## Claim-evidence map
- Claim: subsidence work has scaled from local to city/national/delta analyses | Evidence: current literature and the benchmark inventory | Status: supported
- Claim: exposure translation is strong but observability auditing is missing | Evidence: current literature positioning | Status: supported
- Claim: the benchmark should be organized around product lineage and transfer cases | Evidence: current evidence stack and figure sequence | Status: supported
- Claim: the current work is about observability bias, not a new subsidence detector | Evidence: abstract/introduction and current figures | Status: supported

## Assumptions or missing inputs
- Formal citations still need to be formatted and inserted in the manuscript body.
- If you want the final target to be Scientific Data or ESSD, this section should be shortened substantially and reoriented toward data descriptor style.

## Why this structure
- Related work is grouped by technical role, not by publication year.
- Discussion starts from the main advance, then tightens to evidence, implication and boundary.
- The section keeps the comparison axis aligned with the paper's actual novelty: observability auditing.

## To redirect me
If you want, I can next turn this into full prose for the manuscript body or keep building the manuscript section by section.
