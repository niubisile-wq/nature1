# Nature Cities Sprint Plan v1
Date: 2026-07-13

## Purpose

This note converts the current manuscript stack into a Nature Cities-targeted sprint plan. The target is not a generic Nature-family paper. The paper must read as an urban exposure, infrastructure, inequality, and monitoring-governance contribution, with InSAR as the enabling measurement system rather than the headline field.

## External Source Basis

- Nature Cities aims and scope: urban research with practical and policy relevance, including hazards, infrastructure, transportation, resilience, urban science, equity and justice. URL: `https://www.nature.com/natcities/aims`
- Nature Cities publishing options: primary research can use the traditional subscription route or gold open access after acceptance. URL: `https://www.nature.com/natcities/submission-guidelines/publishing-options`
- Nature Cities presubmission enquiries: available for scope checks using an abstract, not a full manuscript. URL: `https://www.nature.com/natcities/submission-guidelines/presubmission-enquiries`
- Comparator 1: `Land subsidence risk to infrastructure in US metropolises`, Nature Cities 2025. URL: `https://www.nature.com/articles/s44284-025-00240-y`
- Comparator 2: `Partial flood defenses shift risks and amplify inequality in a core-periphery city`, Nature Cities 2025. URL: `https://www.nature.com/articles/s44284-025-00299-7`
- Comparator 3: `Human-centric characterization of life activity flood exposure shifts focus from places to people`, Nature Cities 2024. URL: `https://www.nature.com/articles/s44284-024-00043-7`
- Comparator 4: `Global urban structural growth shows a profound shift from spreading out to building up`, Nature Cities 2024. URL: `https://www.nature.com/articles/s44284-024-00100-1`
- Comparator 5: `Mapping urban slums and their inequality in sub-Saharan Africa`, Nature Cities 2025. URL: `https://www.nature.com/articles/s44284-025-00276-0`

## Current Local Source Basis

- `10_manuscript_skeleton/full_manuscript_draft_v3.md`
- `08_nature_experiment_plan/figure_outline_v2.md`
- `08_nature_experiment_plan/decision_facing_exposure_matrix_v1.md`
- `08_nature_experiment_plan/multi_region_exposure_translation_v1.md`
- `03_exposure_closure/final_multi_region_equal_area_closure_v1/final_multi_region_equal_area_closure_report.md`
- `03_exposure_closure/chao_phraya_area_weighted_exposure_censoring/*`
- `03_exposure_closure/chao_phraya_osm_exposure_censoring/*`
- `11_submission_ready_v1/source_data/completion_audit_v1.md`

## Editorial Diagnosis

### Bottom line

Nature Cities is a defensible stretch target, but the current manuscript should not be submitted in its present form. It is too InSAR-method-led and too benchmark-internal. The Nature Cities version needs a sharper urban claim:

> Open subsidence-monitoring products can systematically hide the urban people, built land and transport infrastructure that need monitoring most.

The paper should be positioned as an urban exposure-accounting and monitoring-governance problem, not as an InSAR product benchmarking paper.

### Main opportunity

The strongest existing Nature Cities subsidence comparator maps subsidence and infrastructure risk across 28 US cities. Our paper should not compete by making another subsidence-risk map. It should differentiate by asking whether public/open monitoring coverage itself creates a blind spot in exposure accounting.

### Main risk

The current lead case is Chao Phraya. That is relevant to Bangkok and urban delta risk, but the manuscript still reads as a basin/delta benchmark. Nature Cities will expect the city, infrastructure and people implications to appear in the first paragraph, first result, and first figure.

## What Nature Cities Articles Do Well

| Pattern | What strong Nature Cities papers do | Implication for our manuscript |
|---|---|---|
| Urban problem first | Lead with people, infrastructure, neighborhoods, or governance. | Move `InSAR observability` from title-front to mechanism; foreground `urban exposure undercount`. |
| Quantified headline | Abstracts contain concrete numbers: people affected, area, buildings, damages, inequality metrics, city counts. | Add one defensible headline number from Chao Phraya and one compact multi-region statistic. |
| City-scale relevance | Even technical papers explain why the finding changes urban planning, infrastructure adaptation or equity. | Reframe the discussion around monitoring debt, infrastructure triage and exposure-accounting bias. |
| Counterfactual logic | Papers compare observed vs corrected, protected vs unprotected, place-based vs people-based, or lateral vs vertical growth. | Make `visible-only exposure` versus `observability-adjusted exposure` the central comparison. |
| Human-centric exposure | Exposure is not only pixels or land; it includes population, mobility, dwell time, buildings, income or vulnerability. | Keep people, built-up area and transport in the main text; add vulnerability only where defensible. |
| Inequality or distributional burden | Strong papers show who benefits, who is missed, or whose risk is shifted. | Add a monitoring-equity angle: public-product gaps can shift apparent priority away from under-observed urban zones. |
| Reproducible data products | Data and code availability are explicit and versioned. | Use the GitHub/Zenodo release as a credibility layer, not as a main scientific result. |

## Direct Comparison Against Our Current Stack

| Dimension | Nature Cities expectation | Current status | Gap | Sprint action |
|---|---|---|---|---|
| Journal fit | Cities, infrastructure, hazards, transport, resilience, equity. | The topic fits, but the framing is geodetic and benchmark-led. | Medium-high. | Rewrite title, abstract, intro and first results around urban exposure undercount. |
| Novelty against existing Nature Cities subsidence paper | Must not duplicate `where subsidence threatens infrastructure`. | Current draft is adjacent to the 28-US-city subsidence paper. | High. | State the distinction: previous work maps risk; this paper audits whether open monitoring hides exposure. |
| Quantified headline | Concrete, memorable numbers in abstract. | Draft uses qualitative phrases such as `substantial hidden exposure`. | High. | Use final equal-area closure numbers: Chao Phraya hidden population `3.63 million`, hidden built-up area `422.78 km2`, plus carefully audited transport fraction. |
| Exposure accounting | People, built-up area and infrastructure should be central. | Chao Phraya has all three; Po and Brantas have people and built-up; other regions are proxy/transfer. | Medium. | Make Chao Phraya lead case explicit and avoid implying equal completeness across regions. |
| Urban boundary | City or metropolitan boundary should be visible. | Chao Phraya is still framed as basin/delta. | High. | Add a Bangkok/urban-built-up mask or explicitly subset the Chao Phraya closure to urban/built-up cells. |
| Inequality/vulnerability | Nature Cities often rewards distributional interpretation. | GVI/SHDI context exists, but not a clean raster-level structural vulnerability layer. | Medium-high. | Keep vulnerability as context unless a defensible urban layer is added; do not overclaim. |
| Mechanism | The mechanism should be intuitive to urban readers. | Observability censoring is clear but technical. | Medium. | Explain as `monitoring debt`: visible maps can make priority zones look safer than they are. |
| Validation | Need robustness and limits. | Robustness grid, hierarchical stack and transfer probes exist. | Medium. | Compress into one robustness figure and one extended-data table. |
| Figure economy | Main figures should tell one clean urban story. | Current plan has 6-7 figures and some technical/internal panels. | High. | Reduce to 4 main figures plus Extended Data. |
| Reproducibility | Versioned data/code are expected. | GitHub and Zenodo DOI now exist. | Low. | Update stale local audits and keep DOI in Data/Code Availability only. |

## Target Article Shape

### Working title options

1. `Open subsidence-monitoring gaps can hide urban exposure in sinking delta cities`
2. `Public InSAR observability gaps can undercount urban subsidence exposure`
3. `Monitoring debt in open InSAR products hides urban subsidence exposure`

Preferred title for Nature Cities:

> Public InSAR observability gaps can undercount urban subsidence exposure

Reason: it keeps the technical novelty, but the object of concern is `urban subsidence exposure`, not the product benchmark itself.

### Revised abstract contract

The abstract should contain five moves:

1. Urban relevance: sinking cities depend on public/open monitoring products for exposure accounting.
2. Gap: missing InSAR coverage is often treated as neutral, but it can be structured.
3. Lead evidence: Chao Phraya/Bangkok-delta closure reveals hidden population, built-up area and transport exposure.
4. Transfer: Po and Brantas support people/built-up transfer; Japan/Iran show product-lineage extension, with clear limits.
5. Implication: visible-only subsidence maps can undercount urban exposure and create monitoring debt.

### Figure plan for Nature Cities

| Figure | Main conclusion | Source |
|---|---|---|
| Fig. 1 | Public-product missingness can become urban monitoring debt, not random noise. | Concept plus benchmark inventory. |
| Fig. 2 | In Chao Phraya/Bangkok-delta, observability-adjusted accounting reveals hidden people and built-up area in strong subsidence zones. | `final_multi_region_equal_area_closure_v1` and Chao Phraya area-weighted outputs. |
| Fig. 3 | Visible-only accounting versus corrected accounting changes exposure estimates for population, built land and transport. | `decision_facing_exposure_matrix_v1`, `multi_region_exposure_translation_v1`, OSM transport summary. |
| Fig. 4 | The signal is not only a local artifact: robustness, region roles and transfer probes define where the claim holds and where it remains bounded. | robustness grid, hierarchical model, transfer validation scores. |

Extended Data:

- Full region-role table.
- Threshold and block-size robustness grid.
- Transfer probe audit for Japan and Iran.
- Repository/Zenodo reproducibility manifest.
- Vulnerability-context table, if kept.

## Fourteen-Day Sprint

### Day 1: Lock the Nature Cities claim

Deliverables:

- One revised title.
- One 150-word editorial summary.
- One paragraph explicitly differentiating from the 2025 Nature Cities US subsidence-infrastructure paper.

Pass condition:

- The paper can be summarized without saying `benchmark` in the first sentence.

### Days 2-3: Audit headline numbers

Deliverables:

- `nature_cities_headline_numbers_v1.csv`
- `nature_cities_headline_numbers_v1.md`

Numbers to reconcile:

- Chao Phraya final equal-area closure: hidden population `3.63 million`; hidden built-up area `422.78 km2`.
- Earlier decision matrix: population not-majority observable `0.170`; built-up not-majority observable `0.326`; transport hidden fraction median `0.531`.
- New final closure: transport hidden fraction mean/median around `0.001`.

Pass condition:

- The abstract uses only one internally consistent number set.

Stop condition:

- If transport definitions cannot be reconciled, remove transport from the headline and keep it as a Methods/Extended Data sensitivity result.

### Days 3-5: Make the lead case urban, not only delta-scale

Deliverables:

- Bangkok/urban-built-up subset, or a defensible built-up-cell-only Chao Phraya subset.
- Map showing strong subsidence, observability and built-up/transport exposure.
- Short note explaining the geographic boundary.

Pass condition:

- A Nature Cities editor can see a city/metropolitan exposure problem in Fig. 2 without reading methods.

### Days 5-6: Build the visible-only versus corrected exposure contrast

Deliverables:

- Paired table and figure source data for visible-only exposure, hidden exposure and observability-adjusted total exposure.
- One `monitoring debt` metric: hidden exposure / visible exposure or hidden exposure / total exposure.

Pass condition:

- The central result is a counterfactual comparison, not a static map.

### Days 6-8: Harden multi-region support without overclaiming

Deliverables:

- Final region-role table: lead, supporting, transfer, control.
- Po and Brantas people/built-up support carried into Extended Data.
- Indus, Rhone and Rhine clearly labeled as proxy/control.

Pass condition:

- No region is silently promoted to lead-case status.

### Days 8-9: Add or bound vulnerability/equity

Deliverables:

- Decide between two routes:
  - route A: add defensible urban vulnerability or settlement layer;
  - route B: keep GVI/SHDI as contextual only and state the structural-vulnerability gap.

Pass condition:

- The manuscript does not mistake country-level vulnerability context for city-level inequality evidence.

### Days 9-11: Rebuild the main figures

Deliverables:

- Four main figure drafts.
- One figure-source map specific to Nature Cities.
- Extended Data table list.

Pass condition:

- Every figure has one urban conclusion and one sentence answer to `so what for cities?`.

### Days 11-13: Rewrite manuscript

Deliverables:

- Revised title, abstract, introduction and results order.
- Discussion rewritten around monitoring debt, urban exposure accounting and governance of open monitoring systems.
- Methods moved later and tightened.

Pass condition:

- The first 1,000 words contain people, infrastructure, cities and policy relevance before product lineage details.

### Day 14: Submission decision package

Deliverables:

- Presubmission enquiry abstract, even if the final decision is full submission.
- Cover-letter novelty bullets.
- Reviewer-risk memo.
- Final go/no-go table.

Pass condition:

- The package can answer: why Nature Cities, why now, why not the existing US subsidence paper, why this is urban science.

## Go/No-Go Conditions

Submit to Nature Cities only if all five conditions are met:

1. One headline number set is internally consistent and traceable to frozen source data.
2. The first figure and abstract are urban-exposure-led, not InSAR-method-led.
3. The novelty against the 2025 Nature Cities US subsidence paper is explicit.
4. The lead case has a visible urban/built-up boundary or an honest built-up-cell substitute.
5. The paper does not overclaim transfer cases or vulnerability evidence.

If any of conditions 1-3 fail, do not submit to Nature Cities yet.

If condition 4 fails but conditions 1-3 pass, send a presubmission enquiry first.

If condition 5 fails, revise before any submission because it creates avoidable reviewer rejection risk.

## Recommended Sprint Priority

P0:

- Reconcile headline numbers.
- Reframe title/abstract/intro around urban exposure undercount.
- Create urban/built-up lead-case view.
- Differentiate from the existing Nature Cities subsidence-infrastructure article.

P1:

- Compress figures to four main figures.
- Close region-role table.
- Update stale release audit with the minted GitHub and Zenodo DOI.

P2:

- Add vulnerability/equity only if it can be defended at urban or subnational scale.
- Keep EGMS as future external closure, not a current claim.

## Final Position

This is not ready for immediate Nature Cities submission, but it is a credible stretch after a focused sprint. The strongest route is to make the article about urban monitoring debt and exposure-accounting bias. The weakest route is to keep it as an open InSAR benchmark with a city example attached.
