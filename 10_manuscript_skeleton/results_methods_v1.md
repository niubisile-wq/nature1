# Results and Methods Draft v1
Date: 2026-07-09

## Results

### Result 1. Benchmark construction and region inventory
To establish whether open InSAR observability is biased rather than merely incomplete, we first assembled a benchmark that separates lead cases, control cases and transfer cases across regions and product families. The regional inventory shows that the effect is not confined to a single delta: Po, Chao Phraya, Rhone and Rhine all carry independent-anchor and product-status metadata that makes them useful for bias testing, while Indus and Brantas provide weaker-anchor controls.

### Result 2. Lead-case area-weighted exposure closure in Chao Phraya
To test whether observability censoring changes exposure accounting, we next performed an area-weighted closure in Chao Phraya rather than relying on center-point sampling. This lead case shows that strongly deforming cells still contain substantial hidden population, built-up land and transport infrastructure, so the exposure summary changes once observability is treated as part of the accounting problem.

### Result 3. Robustness screening across threshold and block-size choices
To check whether the lead-case result depends on a single threshold choice, we varied observability thresholds, strong-motion thresholds and block sizes. The resulting grid keeps the main censoring direction visible while also defining the boundary of the claim: the signal is robust in the main regime but should not be overstated as universal across every weak-motion cutoff.

### Result 4. Exposure-to-risk translation across population, built-up land and transport
To translate the lead-case censoring result into policy-relevant quantities, we then summarized visible and hidden exposure across population, built-up area and transport infrastructure. This step shows why the argument matters: the observability problem is not abstract, because the missing exposure is concentrated in quantities that decision makers actually care about.

### Result 5. Controls and transfer across product families
To test whether the effect is specific to one land-cover setting or one public product lineage, we next examined land-cover controls and transfer cases. The controls show that the signal is not a simple artifact of one land-cover class, while Japan LiCSBAS and Iran nationwide public InSAR extend the same censoring question to other public product families.

### Result 6. Scope limits and upgrade path
To define the boundary of the current claim, we separate the no-token benchmark from the Europe-scale upgrade path. The current work establishes the mechanism and the exposure consequence without EGMS credentials; the dense European closure remains the obvious next benchmark once access is available.

## Methods

### Method 1. Benchmark design and region selection
We defined the benchmark around three region roles: lead cases for the strongest signal, control cases for specificity, and transfer cases for product-family generalization. Region metadata include frame identifiers, LiCS pair counts, cell counts, dominant land cover, independent-anchor status, NGL station count and EGMS availability status.

### Method 2. Area-weighted exposure closure
For the lead case, exposure is computed by equal-area or polygon overlap weighting rather than by point sampling. This prevents the result from depending on an arbitrary center pixel and makes the exposure summaries align with the actual footprint of the strongly deforming cells.

### Method 3. Observability censoring and threshold definitions
We define observability censoring using the share of cells that are not majority observable under a chosen threshold. Strong-motion exposure is evaluated under multiple cutoffs so that the analysis does not depend on a single deformation threshold.

### Method 4. Robustness grid
We varied observability threshold, strong-motion threshold and block size to test whether the censoring signal changes under reasonable alternative settings. The robustness grid is a screening analysis rather than a full spatial causal model.

### Method 5. Transfer probes
Japan LiCSBAS was used as a non-Europe public-product transfer case, and the Iran nationwide InSAR product was used as a second no-token companion extension. These probes test whether the observability question survives product-lineage changes.

### Method 6. Scope boundary
We treat EGMS as an upgrade path rather than a prerequisite for the current claim. The current manuscript therefore stays within the no-token evidence boundary and uses EGMS only as a documented future benchmark route.

## Section outline
- Results 1: benchmark and inventory.
- Results 2: Chao Phraya lead-case closure.
- Results 3: robustness grid.
- Results 4: exposure translation.
- Results 5: controls and transfer.
- Results 6: scope limits.
- Methods 1: benchmark design.
- Methods 2: area-weighted closure.
- Methods 3: censoring definitions.
- Methods 4: robustness grid.
- Methods 5: transfer probes.
- Methods 6: scope boundary.

## Claim-evidence map
- Claim: benchmark spans multiple region roles | Evidence: region inventory and source map | Status: supported
- Claim: area-weighted closure changes the exposure result | Evidence: Chao Phraya summary tables | Status: supported
- Claim: robustness matters but does not overturn the main signal | Evidence: threshold/block grid | Status: supported
- Claim: Japan and Iran extend the product-family question | Evidence: Japan HDF5 summary and Iran probe report | Status: supported
- Claim: EGMS is a future upgrade path, not a current dependency of the main claim | Evidence: query pack and token-required status | Status: supported

## Assumptions or missing inputs
- A formal Methods section will still need precise variable names, formulas and file paths for publication.
- The Results prose still needs explicit numeric values inserted sentence by sentence.
- If the final journal is Scientific Data/ESSD, the Results/Methods split should be compressed into a data descriptor structure.

## Why this structure
- The Results section follows the evidence ladder already present in the figure sequence.
- The Methods section stays close to the reproducible modules already built in the workspace.
- Each subsection opening sentence is written to be easy to expand into full prose later.

## To redirect me
If you want a different journal shape, say so explicitly and I will reframe the same evidence into a data descriptor, mechanisms paper, or shorter Nat Commun structure.
