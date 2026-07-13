# Figure Outline v1
日期：2026-07-09

## Fig. 1 Concept and dataset map
- Panel A: Open InSAR observability bias concept diagram.
- Panel B: Global map of current regions and data sources.
- Panel C: Definition of `observability_failure`, `monitoring_debt`, `risk_underestimation_factor`.
- Source data: `benchmark_manifest_v0_1.json`, `benchmark_region_evidence_v0_1.csv`.

## Fig. 2 Chao Phraya lead case
- Panel A: VLM map.
- Panel B: observability failure map.
- Panel C: GHSL population and built-up overlays.
- Panel D: missed exposure counterfactual.
- Source data: multi-delta exposure closure outputs and regional VLM grids.

## Fig. 3 Multi-region model
- Panel A: land-cover-adjusted odds ratios by region.
- Panel B: bootstrap confidence intervals.
- Panel C: leave-one-region-out sensitivity.
- Panel D: control/specification case for Rhine.
- Source data: `delta_worldcover_avg_strong_effects.csv`, bootstrap files.

## Fig. 4 Bias to risk translation
- Panel A: visible-only vs full exposure.
- Panel B: underestimation factor by region.
- Panel C: population and built-up missed under strong motion.
- Panel D: roads/rail or irrigation exposure once available.
- Source data: `multi_delta_vlm_exposure_censoring_summary.csv`, future overlay tables.

## Fig. 5 Mechanism controls
- Panel A: WorldCover class-stratified failure rates.
- Panel B: product lineage comparison.
- Panel C: threshold sensitivity.
- Panel D: time-sampling sensitivity.
- Source data: landcover summaries, robustness grid.

## Fig. 6 Transfer and extension
- Panel A: Japan Niigata LiCSBAS summary.
- Panel B: Iran nationwide InSAR summary.
- Panel C: NGL anchor coverage map.
- Panel D: transfer-performance or domain-limits statement.
- Source data: `h5_velocity_summary.json`, `tif_inspection.json`, NGL screens.

## Fig. 7 Frozen hierarchical comparison
- Panel A: summary-only meta-analysis versus cell-anchored hierarchical stack.
- Panel B: leave-one-out absolute log-OR error by region.
- Panel C: hierarchical coefficient forest plot.
- Source data: `hierarchical_model_comparison.csv`, `hierarchical_model_leave_one_out.csv`, `hierarchical_model_coefficients.csv`.

## Extended Data
- Threshold sensitivity table.
- Block bootstrap table.
- Sign/unit audit table.
- Dataset inventory and license table.
- Source data per panel.

## Next artwork rule
Each figure panel must answer one sentence only:
1. What is observed?
2. Why is it important?
3. How much does it change the exposure estimate?
