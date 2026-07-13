from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from benchmark_delta_vlm_lisc_observability import (
    download_grid_zip,
    fetch_zenodo_record,
    geotiff_tags as vlm_geotiff_tags,
    grid_centers as vlm_grid_centers,
)
from bootstrap_multi_delta_vlm_exposure_censoring import prepare_delta
from compute_multi_delta_vlm_exposure_censoring import CONFIGS, DEFAULT_BUILT_TIF, DEFAULT_POP_TIF
from fit_multi_delta_vlm_binomial_observability import clustered_covariance, fit_binomial_logit
from fit_multi_delta_vlm_spatial_logit import build_delta_rows, concatenate_tables, fmt, make_cluster_ids, quantile_summary, write_csv, z_standardize
from probe_candidate_worldcover_landcover import sample_worldcover
from screen_candidate_delta_vlm_binomial import CANDIDATES, prepare_candidate


REGION_BASELINE = "Po"
LANDCOVER_GROUPS = [
    "cropland",
    "built_up",
    "water_wetland_mangrove",
    "vegetation_non_crop",
    "bare_sparse",
]
LANDCOVER_CODES = {
    "cropland": {40},
    "built_up": {50},
    "water_wetland_mangrove": {80, 90, 95},
    "vegetation_non_crop": {10, 20, 30, 100},
    "bare_sparse": {60},
}


def worldcover_group(classes: np.ndarray) -> np.ndarray:
    out = np.asarray(["other"] * len(classes), dtype=object)
    for group, codes in LANDCOVER_CODES.items():
        out[np.isin(classes, list(codes))] = group
    return out


def table_points(table: dict[str, np.ndarray], vlm_path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    info = vlm_geotiff_tags(Path(vlm_path))
    lon, lat = vlm_grid_centers(info)
    if lon.ndim == 1 and lat.ndim == 1:
        return lon[table["col"]], lat[table["row"]]
    return lon[table["row"], table["col"]], lat[table["row"], table["col"]]


def add_worldcover(
    table: dict[str, np.ndarray],
    bbox: dict[str, float],
    vlm_path: str | Path,
    args: argparse.Namespace,
) -> tuple[dict[str, np.ndarray], list[dict[str, Any]]]:
    lon, lat = table_points(table, vlm_path)
    classes, tiles = sample_worldcover(lon, lat, bbox, args.tile_dir, args.overview_level, args.timeout)
    out = dict(table)
    out["landcover_code"] = classes.astype(float)
    out["landcover_group"] = worldcover_group(classes)
    return out, tiles


def build_all_delta_tables(args: argparse.Namespace, grid_zip: Path) -> tuple[dict[str, np.ndarray], list[dict[str, Any]], list[dict[str, Any]]]:
    tables: list[dict[str, np.ndarray]] = []
    region_meta: list[dict[str, Any]] = []
    tile_meta: list[dict[str, Any]] = []

    for config in CONFIGS:
        prepared = prepare_delta(config, args, grid_zip)
        table = build_delta_rows(prepared, args.block_size)
        table, tiles = add_worldcover(table, prepared["bbox"], prepared["vlm_path"], args)
        tables.append(table)
        tile_meta.extend([{**tile, "region": prepared["delta"]} for tile in tiles])
        region_meta.append(
            {
                "region": prepared["delta"],
                "frame_id": prepared["frame_id"],
                "n_pairs": prepared["n_pairs"],
                "n_cells": int(len(table["strong"])),
                "bbox": prepared["bbox"],
                "vlm_path": prepared["vlm_path"],
                "source": "controlled delta LiCSAR downloads_csv",
            }
        )

    args.min_pairs = args.min_candidate_pairs
    for config in CANDIDATES:
        table, meta = prepare_candidate(config, args, grid_zip)
        if "y" not in table:
            table["y"] = (table["observable_count"].astype(float) < np.ceil(table["n_pairs"].astype(float) / 2.0)).astype(float)
        table, tiles = add_worldcover(table, meta["bbox"], meta["vlm_path"], args)
        tables.append(table)
        tile_meta.extend([{**tile, "region": meta["delta"]} for tile in tiles])
        region_meta.append(
            {
                "region": meta["delta"],
                "frame_id": meta["frame_id"],
                "n_pairs": meta["n_pairs"],
                "n_cells": int(len(table["strong"])),
                "bbox": meta["bbox"],
                "vlm_path": meta["vlm_path"],
                "source": "local candidate LiCSAR downloads",
            }
        )

    return concatenate_tables(tables), region_meta, tile_meta


def design_matrix(table: dict[str, np.ndarray], include_strong_landcover: bool) -> tuple[np.ndarray, dict[str, Any]]:
    region = table["delta"].astype(str)
    regions = sorted(set(region))
    if REGION_BASELINE not in regions:
        raise ValueError(f"baseline region {REGION_BASELINE!r} is absent")
    regions = [REGION_BASELINE] + [item for item in regions if item != REGION_BASELINE]

    strong = table["strong"].astype(float)
    pop_z, pop_mean, pop_std = z_standardize(np.log1p(table["population"].astype(float)))
    built_z, built_mean, built_std = z_standardize(np.log1p(table["builtup"].astype(float)))
    lc = table["landcover_group"].astype(str)

    terms = ["intercept", "strong_subsidence", "log1p_population_z", "log1p_builtup_z"]
    cols = [np.ones(len(region), dtype=float), strong, pop_z, built_z]
    region_interactions: dict[str, str] = {}
    for label in regions[1:]:
        dummy = (region == label).astype(float)
        rterm = f"region_{label.lower().replace(' ', '_')}"
        iterm = f"strong_x_{label.lower().replace(' ', '_')}"
        terms.extend([rterm, iterm])
        cols.extend([dummy, strong * dummy])
        region_interactions[label] = iterm

    landcover_interactions: dict[str, str] = {}
    for group in LANDCOVER_GROUPS:
        dummy = (lc == group).astype(float)
        lterm = f"lc_{group}"
        iterm = f"strong_x_lc_{group}"
        terms.append(lterm)
        cols.append(dummy)
        if include_strong_landcover:
            terms.append(iterm)
            cols.append(strong * dummy)
            landcover_interactions[group] = iterm

    terms.extend(["strong_x_population_z", "strong_x_builtup_z"])
    cols.extend([strong * pop_z, strong * built_z])
    return np.column_stack(cols), {
        "terms": terms,
        "regions": regions,
        "region_interactions": region_interactions,
        "landcover_groups": LANDCOVER_GROUPS,
        "landcover_interactions": landcover_interactions,
        "include_strong_landcover": include_strong_landcover,
        "population_log1p_mean": pop_mean,
        "population_log1p_std": pop_std,
        "builtup_log1p_mean": built_mean,
        "builtup_log1p_std": built_std,
    }


def coefficient_rows(beta: np.ndarray, cov: np.ndarray, terms: list[str]) -> list[dict[str, Any]]:
    diag = np.diag(cov)
    se = np.sqrt(np.where(diag >= 0.0, diag, np.nan))
    rows = []
    for idx, term in enumerate(terms):
        z = float(beta[idx] / se[idx]) if np.isfinite(se[idx]) and se[idx] > 0 else float("nan")
        rows.append(
            {
                "term": term,
                "beta": float(beta[idx]),
                "cluster_se": float(se[idx]),
                "z": z,
                "odds_ratio": float(np.exp(beta[idx])),
                "odds_ratio_ci_low": float(np.exp(beta[idx] - 1.96 * se[idx])) if np.isfinite(se[idx]) else float("nan"),
                "odds_ratio_ci_high": float(np.exp(beta[idx] + 1.96 * se[idx])) if np.isfinite(se[idx]) else float("nan"),
            }
        )
    return rows


def row_effect_weights(table: dict[str, np.ndarray], design_meta: dict[str, Any]) -> np.ndarray:
    terms = design_meta["terms"]
    weights = np.zeros((len(table["strong"]), len(terms)), dtype=float)
    weights[:, terms.index("strong_subsidence")] = 1.0
    region = table["delta"].astype(str)
    lc = table["landcover_group"].astype(str)
    pop_z, _m, _s = z_standardize(np.log1p(table["population"].astype(float)))
    built_z, _m2, _s2 = z_standardize(np.log1p(table["builtup"].astype(float)))
    for label, term in design_meta["region_interactions"].items():
        weights[region == label, terms.index(term)] = 1.0
    for group, term in design_meta["landcover_interactions"].items():
        weights[lc == group, terms.index(term)] = 1.0
    weights[:, terms.index("strong_x_population_z")] = pop_z
    weights[:, terms.index("strong_x_builtup_z")] = built_z
    return weights


def averaged_effect_row(effect: str, weights: np.ndarray, beta: np.ndarray, cov: np.ndarray) -> dict[str, Any]:
    w = np.mean(weights, axis=0)
    log_or = float(w @ beta)
    se = float(np.sqrt(max(float(w @ cov @ w), 0.0)))
    z = log_or / se if se > 0 else float("nan")
    return {
        "effect": effect,
        "log_odds_ratio": log_or,
        "cluster_se": se,
        "z": z,
        "odds_ratio": float(np.exp(log_or)),
        "odds_ratio_ci_low": float(np.exp(log_or - 1.96 * se)) if se > 0 else float("nan"),
        "odds_ratio_ci_high": float(np.exp(log_or + 1.96 * se)) if se > 0 else float("nan"),
    }


def averaged_region_effects(table: dict[str, np.ndarray], beta: np.ndarray, cov: np.ndarray, design_meta: dict[str, Any]) -> list[dict[str, Any]]:
    weights = row_effect_weights(table, design_meta)
    rows = []
    for region in design_meta["regions"]:
        mask = table["delta"].astype(str) == region
        rows.append(averaged_effect_row(f"avg_strong_effect:{region}", weights[mask], beta, cov))
    rows.append(averaged_effect_row("avg_strong_effect:ALL", weights, beta, cov))
    return rows


def bootstrap_region_effects(
    x: np.ndarray,
    failures: np.ndarray,
    trials: np.ndarray,
    table: dict[str, np.ndarray],
    design_meta: dict[str, Any],
    n_bootstrap: int,
    rng: np.random.Generator,
    max_iter: int,
    ridge: float,
) -> tuple[list[dict[str, Any]], int]:
    base_weights = row_effect_weights(table, design_meta)
    regions = table["delta"].astype(str)
    clusters = make_cluster_ids(table)
    block_rows: dict[str, list[np.ndarray]] = {}
    for region in sorted(set(regions)):
        region_mask = regions == region
        region_clusters = sorted(set(clusters[region_mask].astype(str)))
        block_rows[region] = [np.where(clusters == cluster)[0] for cluster in region_clusters]
    effects = list(design_meta["regions"]) + ["ALL"]
    values: dict[str, list[float]] = {effect: [] for effect in effects}
    failures_count = 0
    for _ in range(n_bootstrap):
        sampled_indices = []
        for region, blocks in block_rows.items():
            sampled = rng.integers(0, len(blocks), size=len(blocks))
            sampled_indices.extend(blocks[int(idx)] for idx in sampled)
        idx = np.concatenate(sampled_indices)
        try:
            fit = fit_binomial_logit(x[idx], failures[idx], trials[idx], max_iter=max_iter, ridge=ridge)
            beta = fit["beta"]
            if not np.all(np.isfinite(beta)):
                failures_count += 1
                continue
            for region in design_meta["regions"]:
                region_idx = idx[regions[idx] == region]
                if len(region_idx):
                    values[region].append(float(np.exp(np.mean(base_weights[region_idx], axis=0) @ beta)))
            values["ALL"].append(float(np.exp(np.mean(base_weights[idx], axis=0) @ beta)))
        except (FloatingPointError, ValueError, np.linalg.LinAlgError):
            failures_count += 1

    rows = []
    for effect, vals in values.items():
        q = quantile_summary(vals)
        rows.append(
            {
                "effect": effect,
                "n_success": len(vals),
                "n_failed": failures_count,
                "odds_ratio_boot_mean": q["mean"],
                "odds_ratio_boot_q025": q["q025"],
                "odds_ratio_boot_q50": q["q50"],
                "odds_ratio_boot_q975": q["q975"],
            }
        )
    return rows, failures_count


def landcover_summary(table: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows = []
    regions = list(sorted(set(table["delta"].astype(str)))) + ["ALL"]
    groups = ["other"] + LANDCOVER_GROUPS
    for region in regions:
        region_mask = np.ones(len(table["strong"]), dtype=bool) if region == "ALL" else table["delta"].astype(str) == region
        for group in groups:
            mask = region_mask & (table["landcover_group"].astype(str) == group)
            if not np.any(mask):
                continue
            strong = table["strong"][mask] == 1.0
            failures = table["failure_count"][mask].astype(float)
            trials = table["n_pairs"][mask].astype(float)
            rows.append(
                {
                    "region": region,
                    "landcover_group": group,
                    "cells": int(mask.sum()),
                    "cell_fraction_in_region": float(mask.sum() / region_mask.sum()),
                    "strong_share": float(np.mean(strong)),
                    "failure_rate": float(np.sum(failures) / np.sum(trials)),
                    "strong_failure_rate": float(np.sum(failures[strong]) / np.sum(trials[strong])) if np.any(strong) else float("nan"),
                    "nonstrong_failure_rate": float(np.sum(failures[~strong]) / np.sum(trials[~strong])) if np.any(~strong) else float("nan"),
                }
            )
    return rows


def write_markdown(path: Path, region_rows: list[dict[str, Any]], boot_rows: list[dict[str, Any]], coef_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]], meta: dict[str, Any]) -> None:
    boot = {row["effect"]: row for row in boot_rows}
    lines = [
        "# Delta binomial model with WorldCover land-cover controls",
        "",
        "This model tests whether the positive strong-subsidence observability-censoring signal remains after adding ESA WorldCover 2021 v200 land-cover groups.",
        "",
        "`failure_count_i ~ Binomial(n_pairs_i, p_i)`",
        "",
        "`logit(p_i) ~ strong_subsidence + exposure_z + region + landcover + strong:region + strong:landcover + strong:exposure_z`",
        "",
        f"Bootstrap replicates: `{meta['n_bootstrap']}`, seed `{meta['seed']}`.",
        "",
        "## Land-Cover-Adjusted Average Strong Effect",
        "",
        "| region | clustered OR | clustered 95% CI | bootstrap median | bootstrap 95% interval |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in region_rows:
        key = row["effect"].split(":", 1)[1]
        b = boot.get(key)
        if not b:
            continue
        lines.append(
            f"| {key} | {fmt(row['odds_ratio'])} | {fmt(row['odds_ratio_ci_low'])}-{fmt(row['odds_ratio_ci_high'])} | "
            f"{fmt(b['odds_ratio_boot_q50'])} | {fmt(b['odds_ratio_boot_q025'])}-{fmt(b['odds_ratio_boot_q975'])} |"
        )
    if any(row["term"].startswith("strong_x_lc_") for row in coef_rows):
        lines.extend(["", "## Strong x Land-Cover Terms", "", "| term | OR | 95% CI |", "|---|---:|---:|"])
        for row in coef_rows:
            if row["term"].startswith("strong_x_lc_"):
                lines.append(f"| {row['term']} | {fmt(row['odds_ratio'])} | {fmt(row['odds_ratio_ci_low'])}-{fmt(row['odds_ratio_ci_high'])} |")
    lines.extend(["", "## Land-Cover Summary", "", "| region | group | cells | cell fraction | strong share | failure rate | strong failure | nonstrong failure |", "|---|---|---:|---:|---:|---:|---:|---:|"])
    for row in summary_rows:
        if row["region"] == "ALL" or row["landcover_group"] in {"cropland", "built_up", "water_wetland_mangrove"}:
            lines.append(
                f"| {row['region']} | {row['landcover_group']} | {row['cells']} | {fmt(row['cell_fraction_in_region'])} | "
                f"{fmt(row['strong_share'])} | {fmt(row['failure_rate'])} | {fmt(row['strong_failure_rate'])} | {fmt(row['nonstrong_failure_rate'])} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation Guardrail",
            "",
            "- These effects are averaged over each region's observed WorldCover and exposure distribution on the log-odds scale.",
            "- If region effects collapse after land-cover adjustment, the innovation should become a land-cover-mediated observability-censoring framework rather than a strong-subsidence effect.",
            "- Candidate regions still need controlled annual pair sampling before manuscript-level claims.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("radar_outputs") / "delta_binomial_with_worldcover")
    parser.add_argument("--tile-dir", type=Path, default=Path("radar_outputs") / "worldcover_tiles")
    parser.add_argument("--population-tif", type=Path, default=DEFAULT_POP_TIF)
    parser.add_argument("--builtup-tif", type=Path, default=DEFAULT_BUILT_TIF)
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--vlm-scale-to-mm", type=float, default=10.0)
    parser.add_argument("--strong-threshold-mm-yr", type=float, default=-5.0)
    parser.add_argument("--block-size", type=int, default=10)
    parser.add_argument("--n-bootstrap", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260709)
    parser.add_argument("--max-iter", type=int, default=500)
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--min-candidate-pairs", type=int, default=10)
    parser.add_argument("--overview-level", type=int, default=4)
    parser.add_argument("--include-strong-landcover", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    record = fetch_zenodo_record(args.outdir, args.timeout)
    grid_zip, zip_status = download_grid_zip(record, args.outdir, args.timeout)
    table, region_meta, tile_meta = build_all_delta_tables(args, grid_zip)
    x, design_meta = design_matrix(table, args.include_strong_landcover)
    failures = table["failure_count"].astype(float)
    trials = table["n_pairs"].astype(float)
    clusters = make_cluster_ids(table)
    fit = fit_binomial_logit(x, failures, trials, max_iter=args.max_iter, ridge=args.ridge)
    cov_result = clustered_covariance(x, failures, trials, fit["p"], fit["bread"], clusters)
    coef_rows = coefficient_rows(fit["beta"], cov_result["cov"], design_meta["terms"])
    region_rows = averaged_region_effects(table, fit["beta"], cov_result["cov"], design_meta)
    summary_rows = landcover_summary(table)
    rng = np.random.default_rng(args.seed)
    boot_rows, boot_failures = bootstrap_region_effects(
        x,
        failures,
        trials,
        table,
        design_meta,
        args.n_bootstrap,
        rng,
        args.max_iter,
        args.ridge,
    )

    write_csv(args.outdir / "delta_worldcover_coefficients.csv", coef_rows, ["term", "beta", "cluster_se", "z", "odds_ratio", "odds_ratio_ci_low", "odds_ratio_ci_high"])
    write_csv(args.outdir / "delta_worldcover_avg_strong_effects.csv", region_rows, ["effect", "log_odds_ratio", "cluster_se", "z", "odds_ratio", "odds_ratio_ci_low", "odds_ratio_ci_high"])
    write_csv(args.outdir / "delta_worldcover_avg_strong_bootstrap.csv", boot_rows, ["effect", "n_success", "n_failed", "odds_ratio_boot_mean", "odds_ratio_boot_q025", "odds_ratio_boot_q50", "odds_ratio_boot_q975"])
    write_csv(args.outdir / "delta_worldcover_landcover_summary.csv", summary_rows, ["region", "landcover_group", "cells", "cell_fraction_in_region", "strong_share", "failure_rate", "strong_failure_rate", "nonstrong_failure_rate"])
    write_csv(args.outdir / "delta_worldcover_tile_access.csv", tile_meta, ["region", "tile", "url", "status", "bytes", "lon_min", "lon_max", "lat_min", "lat_max", "overview_shape", "overview_level"])
    meta = {
        "zip": zip_status,
        "threshold": args.threshold,
        "n_bootstrap": args.n_bootstrap,
        "seed": args.seed,
        "max_iter": args.max_iter,
        "ridge": args.ridge,
        "overview_level": args.overview_level,
        "include_strong_landcover": args.include_strong_landcover,
        "n_observations": int(len(trials)),
        "n_clusters": int(cov_result["n_clusters"]),
        "n_bootstrap_failures": int(boot_failures),
        "converged": fit["converged"],
        "n_iter": fit["n_iter"],
        "log_likelihood_omits_binomial_constant": fit["log_likelihood"],
        "design": design_meta,
        "regions": region_meta,
        "worldcover_tiles": tile_meta,
    }
    (args.outdir / "delta_worldcover_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(args.outdir / "delta_worldcover_report.md", region_rows, boot_rows, coef_rows, summary_rows, meta)
    print(
        json.dumps(
            {
                "outdir": str(args.outdir),
                "n_observations": meta["n_observations"],
                "n_clusters": meta["n_clusters"],
                "converged": fit["converged"],
                "bootstrap_failures": boot_failures,
                "avg_strong_effects": region_rows,
                "bootstrap": boot_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
