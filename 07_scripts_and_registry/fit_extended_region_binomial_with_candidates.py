from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import numpy as np

from aggregate_central_valley_lisc_annual_observability import FRAME_ID
from benchmark_delta_vlm_lisc_observability import download_grid_zip, fetch_zenodo_record
from bootstrap_multi_delta_vlm_exposure_censoring import prepare_delta
from compute_multi_delta_vlm_exposure_censoring import CONFIGS, DEFAULT_BUILT_TIF, DEFAULT_POP_TIF
from fit_multi_delta_vlm_binomial_observability import (
    clustered_covariance,
    fit_binomial_logit,
    linear_combo_row,
)
from fit_multi_delta_vlm_spatial_logit import (
    build_delta_rows,
    concatenate_tables,
    fmt,
    make_cluster_ids,
    quantile_summary,
    write_csv,
    z_standardize,
)
from fit_multi_region_binomial_with_central_valley import build_central_valley_table
from screen_candidate_delta_vlm_binomial import CANDIDATES, prepare_candidate


BASELINE_REGION = "Po"


def term_slug(label: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z]+", "_", label.strip().lower()).strip("_")
    return slug or "region"


def design_matrix(table: dict[str, np.ndarray]) -> tuple[np.ndarray, dict[str, Any]]:
    region = table["delta"].astype(str)
    regions = sorted(set(region))
    if BASELINE_REGION not in regions:
        raise ValueError(f"baseline region {BASELINE_REGION!r} is absent")
    ordered_regions = [BASELINE_REGION] + [item for item in regions if item != BASELINE_REGION]

    strong = table["strong"].astype(float)
    pop_z, pop_mean, pop_std = z_standardize(np.log1p(table["population"].astype(float)))
    built_z, built_mean, built_std = z_standardize(np.log1p(table["builtup"].astype(float)))

    terms = ["intercept", "strong_subsidence", "log1p_population_z", "log1p_builtup_z"]
    columns = [
        np.ones(region.shape[0], dtype=float),
        strong,
        pop_z,
        built_z,
    ]
    region_term_by_label: dict[str, str] = {}
    interaction_term_by_label: dict[str, str] = {}
    for label in ordered_regions[1:]:
        slug = term_slug(label)
        dummy = (region == label).astype(float)
        region_term = f"region_{slug}"
        interaction_term = f"strong_x_{slug}"
        terms.append(region_term)
        columns.append(dummy)
        region_term_by_label[label] = region_term
        terms.append(interaction_term)
        columns.append(strong * dummy)
        interaction_term_by_label[label] = interaction_term

    terms.extend(["strong_x_population_z", "strong_x_builtup_z"])
    columns.extend([strong * pop_z, strong * built_z])
    return np.column_stack(columns), {
        "terms": terms,
        "regions": ordered_regions,
        "baseline_region": BASELINE_REGION,
        "region_term_by_label": region_term_by_label,
        "interaction_term_by_label": interaction_term_by_label,
        "population_log1p_mean": pop_mean,
        "population_log1p_std": pop_std,
        "builtup_log1p_mean": built_mean,
        "builtup_log1p_std": built_std,
    }


def coefficient_rows(beta: np.ndarray, cov: np.ndarray, terms: list[str]) -> list[dict[str, Any]]:
    rows = []
    se = np.sqrt(np.maximum(np.diag(cov), 0.0))
    for idx, term in enumerate(terms):
        b = float(beta[idx])
        s = float(se[idx])
        z = b / s if s > 0 else float("nan")
        rows.append(
            {
                "term": term,
                "beta": b,
                "cluster_se": s,
                "z": z,
                "odds_ratio": float(np.exp(b)),
                "odds_ratio_ci_low": float(np.exp(b - 1.96 * s)) if s > 0 else float("nan"),
                "odds_ratio_ci_high": float(np.exp(b + 1.96 * s)) if s > 0 else float("nan"),
            }
        )
    return rows


def strong_effect_weights(region: str, design_meta: dict[str, Any]) -> np.ndarray:
    terms = design_meta["terms"]
    weights = np.zeros(len(terms), dtype=float)
    weights[terms.index("strong_subsidence")] = 1.0
    interaction = design_meta["interaction_term_by_label"].get(region)
    if interaction is not None:
        weights[terms.index(interaction)] = 1.0
    return weights


def marginal_rows(beta: np.ndarray, cov: np.ndarray, design_meta: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for region in design_meta["regions"]:
        rows.append(
            linear_combo_row(
                f"strong_subsidence_at_mean_exposure:{region}",
                strong_effect_weights(region, design_meta),
                beta,
                cov,
            )
        )
    return rows


def count_summary(table: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows = []
    regions = sorted(set(table["delta"].astype(str)))
    for region in regions + ["ALL"]:
        mask = np.ones(len(table["delta"]), dtype=bool) if region == "ALL" else table["delta"].astype(str) == region
        strong = table["strong"][mask] == 1.0
        failures = table["failure_count"][mask].astype(float)
        trials = table["n_pairs"][mask].astype(float)
        rows.append(
            {
                "region": region,
                "n_cells": int(mask.sum()),
                "n_blocks": int(len(set(make_cluster_ids({key: value[mask] for key, value in table.items()})))),
                "failure_rate": float(np.sum(failures) / np.sum(trials)),
                "strong_share": float(np.mean(strong)),
                "strong_failure_rate": float(np.sum(failures[strong]) / np.sum(trials[strong])) if np.any(strong) else float("nan"),
                "nonstrong_failure_rate": float(np.sum(failures[~strong]) / np.sum(trials[~strong])) if np.any(~strong) else float("nan"),
                "mean_observable_pairs": float(np.mean(table["observable_count"][mask])),
                "mean_pairs": float(np.mean(trials)),
            }
        )
    return rows


def normalize_table(table: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    if "y" in table:
        return table
    out = dict(table)
    out["y"] = (out["observable_count"].astype(float) < np.ceil(out["n_pairs"].astype(float) / 2.0)).astype(float)
    return out


def bootstrap_effects(
    x: np.ndarray,
    failures: np.ndarray,
    trials: np.ndarray,
    table: dict[str, np.ndarray],
    design_meta: dict[str, Any],
    n_bootstrap: int,
    rng: np.random.Generator,
) -> tuple[list[dict[str, Any]], int]:
    regions = table["delta"].astype(str)
    clusters = make_cluster_ids(table)
    block_rows: dict[str, list[np.ndarray]] = {}
    for region in sorted(set(regions)):
        region_mask = regions == region
        region_clusters = sorted(set(clusters[region_mask].astype(str)))
        block_rows[region] = [np.where(clusters == cluster)[0] for cluster in region_clusters]

    effects = list(design_meta["regions"]) + ["strong_x_population_z", "strong_x_builtup_z"]
    estimates: dict[str, list[float]] = {effect: [] for effect in effects}
    failures_count = 0
    for _ in range(n_bootstrap):
        sampled_indices = []
        for region, blocks in block_rows.items():
            sampled = rng.integers(0, len(blocks), size=len(blocks))
            sampled_indices.extend(blocks[int(idx)] for idx in sampled)
        idx = np.concatenate(sampled_indices)
        try:
            fit = fit_binomial_logit(x[idx], failures[idx], trials[idx])
            beta = fit["beta"]
            if not np.all(np.isfinite(beta)):
                failures_count += 1
                continue
            for region in design_meta["regions"]:
                estimates[region].append(float(np.exp(strong_effect_weights(region, design_meta) @ beta)))
            for effect in ["strong_x_population_z", "strong_x_builtup_z"]:
                estimates[effect].append(float(np.exp(beta[design_meta["terms"].index(effect)])))
        except (FloatingPointError, ValueError, np.linalg.LinAlgError):
            failures_count += 1

    rows = []
    for effect, values in estimates.items():
        q = quantile_summary(values)
        rows.append(
            {
                "effect": effect,
                "n_success": len(values),
                "n_failed": failures_count,
                "odds_ratio_boot_mean": q["mean"],
                "odds_ratio_boot_q025": q["q025"],
                "odds_ratio_boot_q50": q["q50"],
                "odds_ratio_boot_q975": q["q975"],
            }
        )
    return rows, failures_count


def write_markdown(
    path: Path,
    summary: list[dict[str, Any]],
    coef: list[dict[str, Any]],
    marginal: list[dict[str, Any]],
    boot: list[dict[str, Any]],
    meta: dict[str, Any],
) -> None:
    boot_by_effect = {row["effect"]: row for row in boot}
    lines = [
        "# Extended multi-region pair-count binomial observability model",
        "",
        "This model combines the original Po/Chao Phraya/Brantas/Central Valley set with the Rhone/Rhine/Indus candidate screen.",
        "",
        "`failure_count_i ~ Binomial(n_pairs_i, p_i)`",
        "",
        "`logit(p_i) ~ strong_subsidence + exposure_z + region_fixed_effect + strong_subsidence:region + strong_subsidence:exposure_z`",
        "",
        f"Bootstrap replicates: `{meta['n_bootstrap']}`, seed `{meta['seed']}`.",
        "",
        "## Strong-Subsidence Effect",
        "",
        "| region | clustered OR | clustered 95% CI | bootstrap OR median | bootstrap 95% interval |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in marginal:
        region = row["effect"].split(":", 1)[1]
        b = boot_by_effect[region]
        lines.append(
            f"| {region} | {fmt(row['odds_ratio'])} | {fmt(row['odds_ratio_ci_low'])}-{fmt(row['odds_ratio_ci_high'])} | "
            f"{fmt(b['odds_ratio_boot_q50'])} | {fmt(b['odds_ratio_boot_q025'])}-{fmt(b['odds_ratio_boot_q975'])} |"
        )
    lines.extend(["", "## Exposure Interactions", "", "| effect | clustered OR | clustered 95% CI | bootstrap median | bootstrap 95% interval |", "|---|---:|---:|---:|---:|"])
    for effect in ["strong_x_population_z", "strong_x_builtup_z"]:
        row = next(item for item in coef if item["term"] == effect)
        b = boot_by_effect[effect]
        lines.append(
            f"| {effect} | {fmt(row['odds_ratio'])} | {fmt(row['odds_ratio_ci_low'])}-{fmt(row['odds_ratio_ci_high'])} | "
            f"{fmt(b['odds_ratio_boot_q50'])} | {fmt(b['odds_ratio_boot_q025'])}-{fmt(b['odds_ratio_boot_q975'])} |"
        )
    lines.extend(["", "## Count Summary", "", "| region | cells | blocks | failure rate | strong share | strong failure | nonstrong failure | mean observable pairs | mean pairs |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"])
    for row in summary:
        lines.append(
            f"| {row['region']} | {row['n_cells']} | {row['n_blocks']} | {fmt(row['failure_rate'])} | "
            f"{fmt(row['strong_share'])} | {fmt(row['strong_failure_rate'])} | {fmt(row['nonstrong_failure_rate'])} | "
            f"{fmt(row['mean_observable_pairs'])} | {fmt(row['mean_pairs'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Guardrail",
            "",
            "- This is a unification screen, not final Nature-level proof.",
            "- Rhone/Rhine/Indus use locally available LiCSAR coherence rasters from candidate exposure-observability runs; pair sampling should still be formalized before manuscript use.",
            "- Region-specific effects above 1 support heterogeneous observability censoring; mixed signs or intervals crossing 1 argue against a universal strong-subsidence main effect.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("radar_outputs") / "extended_region_binomial_with_candidates")
    parser.add_argument("--population-tif", type=Path, default=DEFAULT_POP_TIF)
    parser.add_argument("--builtup-tif", type=Path, default=DEFAULT_BUILT_TIF)
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--vlm-scale-to-mm", type=float, default=10.0)
    parser.add_argument("--block-size", type=int, default=10)
    parser.add_argument("--n-bootstrap", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260709)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--min-candidate-pairs", type=int, default=10)
    parser.add_argument("--strong-threshold-mm-yr", type=float, default=-5.0)
    parser.add_argument(
        "--central-valley-dwr",
        type=Path,
        default=Path("radar_outputs") / "public_timeseries_central_valley_north" / "Vertical_Displacement_TRE_ALTAMIRA_Annual_Rate_20220101_20230101.tif",
    )
    parser.add_argument(
        "--central-valley-need-arrays",
        type=Path,
        default=Path("radar_outputs") / "central_valley_independent_need_proxy" / "central_valley_independent_need_proxy_arrays.npz",
    )
    parser.add_argument(
        "--central-valley-pair-inventory",
        type=Path,
        default=Path("radar_outputs") / "licsar_frame_product_depth_sample250" / "licsar_frame_pair_product_inventory.csv",
    )
    parser.add_argument(
        "--central-valley-downloads",
        type=Path,
        default=Path("radar_outputs") / "central_valley_lisc_annual_observability" / "central_valley_lisc_annual_downloads.csv",
    )
    parser.add_argument("--central-valley-start-year", type=int, default=2016)
    parser.add_argument("--central-valley-end-year", type=int, default=2021)
    parser.add_argument("--central-valley-per-year", type=int, default=5)
    parser.add_argument("--central-valley-frame-id", default=FRAME_ID)
    parser.add_argument("--central-valley-block-size", type=int, default=20)
    parser.add_argument("--central-valley-strong-threshold-ft-yr", type=float, default=-0.25)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.min_pairs = args.min_candidate_pairs
    args.outdir.mkdir(parents=True, exist_ok=True)
    record = fetch_zenodo_record(args.outdir, args.timeout)
    grid_zip, zip_status = download_grid_zip(record, args.outdir, args.timeout)

    tables = []
    region_meta = []
    for config in CONFIGS:
        prepared = prepare_delta(config, args, grid_zip)
        tables.append(normalize_table(build_delta_rows(prepared, args.block_size)))
        region_meta.append(
            {
                "region": prepared["delta"],
                "frame_id": prepared["frame_id"],
                "n_pairs": prepared["n_pairs"],
                "shape": prepared["shape"],
                "bbox": prepared["bbox"],
                "source": "Nature 2026 delta VLM + controlled LiCSAR downloads_csv",
            }
        )
    for config in CANDIDATES:
        table, meta = prepare_candidate(config, args, grid_zip)
        tables.append(normalize_table(table))
        region_meta.append({**meta, "source": "Nature 2026 delta VLM + local candidate LiCSAR downloads"})
    central_table, central_meta = build_central_valley_table(args)
    tables.append(normalize_table(central_table))
    region_meta.append({**central_meta, "source": "California DWR/TRE displacement + LiCSAR annual observability"})

    table = concatenate_tables(tables)
    x, design_meta = design_matrix(table)
    failures = table["failure_count"].astype(float)
    trials = table["n_pairs"].astype(float)
    clusters = make_cluster_ids(table)
    fit = fit_binomial_logit(x, failures, trials)
    cov_result = clustered_covariance(x, failures, trials, fit["p"], fit["bread"], clusters)
    coef = coefficient_rows(fit["beta"], cov_result["cov"], design_meta["terms"])
    marginal = marginal_rows(fit["beta"], cov_result["cov"], design_meta)
    summary = count_summary(table)
    rng = np.random.default_rng(args.seed)
    boot, boot_failures = bootstrap_effects(x, failures, trials, table, design_meta, args.n_bootstrap, rng)

    coef_fields = ["term", "beta", "cluster_se", "z", "odds_ratio", "odds_ratio_ci_low", "odds_ratio_ci_high"]
    marginal_fields = ["effect", "beta", "cluster_se", "z", "p_value", "odds_ratio", "odds_ratio_ci_low", "odds_ratio_ci_high"]
    summary_fields = ["region", "n_cells", "n_blocks", "failure_rate", "strong_share", "strong_failure_rate", "nonstrong_failure_rate", "mean_observable_pairs", "mean_pairs"]
    boot_fields = ["effect", "n_success", "n_failed", "odds_ratio_boot_mean", "odds_ratio_boot_q025", "odds_ratio_boot_q50", "odds_ratio_boot_q975"]
    write_csv(args.outdir / "extended_region_binomial_coefficients.csv", coef, coef_fields)
    write_csv(args.outdir / "extended_region_binomial_marginal_strong_effects.csv", marginal, marginal_fields)
    write_csv(args.outdir / "extended_region_binomial_count_summary.csv", summary, summary_fields)
    write_csv(args.outdir / "extended_region_binomial_block_bootstrap.csv", boot, boot_fields)

    meta = {
        "zip": zip_status,
        "threshold": args.threshold,
        "block_size": args.block_size,
        "central_valley_block_size": args.central_valley_block_size,
        "n_bootstrap": args.n_bootstrap,
        "seed": args.seed,
        "n_observations": int(len(trials)),
        "n_clusters": int(cov_result["n_clusters"]),
        "n_bootstrap_failures": int(boot_failures),
        "converged": fit["converged"],
        "n_iter": fit["n_iter"],
        "log_likelihood_omits_binomial_constant": fit["log_likelihood"],
        "design": design_meta,
        "regions": region_meta,
    }
    (args.outdir / "extended_region_binomial_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(args.outdir / "extended_region_binomial_report.md", summary, coef, marginal, boot, meta)
    print(
        json.dumps(
            {
                "outdir": str(args.outdir),
                "n_observations": meta["n_observations"],
                "n_clusters": meta["n_clusters"],
                "converged": fit["converged"],
                "bootstrap_failures": boot_failures,
                "marginal_strong_effects": marginal,
                "bootstrap": boot,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
