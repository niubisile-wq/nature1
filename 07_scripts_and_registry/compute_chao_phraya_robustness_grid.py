from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from benchmark_delta_vlm_lisc_observability import (
    observable_stack,
    read_download_rows,
    valid_vlm_mask,
    write_csv,
    geotiff_tags as vlm_geotiff_tags,
    grid_centers as vlm_grid_centers,
)
from compute_chao_phraya_area_weighted_exposure import (
    CHAO_PHRAYA_DOWNLOADS_CSV,
    CHAO_PHRAYA_FRAME_ID,
    DEFAULT_BUILT_TIF,
    DEFAULT_POP_TIF,
    DEFAULT_VLM_TIF,
    area_weighted_transfer,
    crop_source,
    expand_bbox,
)
from simulate_lisc_observability_censoring import coherence_array, geotiff_info, sample_to_target


THRESHOLDS = [0.2, 0.3, 0.4]
STRONG_THRESHOLDS = [3.0, 5.0, 10.0]
BLOCK_SIZES = [5, 10, 20]


def ratio(num: float, den: float) -> float:
    return float(num / den) if den else 0.0


def odds_ratio(a: float, b: float, c: float, d: float) -> float:
    return float(((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5)))


def build_blocks(shape: tuple[int, int], block_size: int) -> list[tuple[slice, slice]]:
    rows, cols = shape
    blocks = []
    for row0 in range(0, rows, block_size):
        for col0 in range(0, cols, block_size):
            blocks.append((slice(row0, min(row0 + block_size, rows)), slice(col0, min(col0 + block_size, cols))))
    return blocks


def block_stats(
    base_valid: np.ndarray,
    strong: np.ndarray,
    majority: np.ndarray,
    not_majority: np.ndarray,
    pop_w: np.ndarray,
    built_w: np.ndarray,
    block: tuple[slice, slice],
) -> dict[str, float]:
    sl_r, sl_c = block
    base = base_valid[sl_r, sl_c]
    strong_b = strong[sl_r, sl_c] & base
    nonstrong_b = (~strong[sl_r, sl_c]) & base
    majority_b = majority[sl_r, sl_c]
    not_majority_b = not_majority[sl_r, sl_c]
    pop_b = pop_w[sl_r, sl_c]
    built_b = built_w[sl_r, sl_c]

    strong_nm = strong_b & not_majority_b
    strong_m = strong_b & majority_b
    nonstrong_nm = nonstrong_b & not_majority_b
    nonstrong_m = nonstrong_b & majority_b

    return {
        "strong_cells": float(strong_b.sum()),
        "strong_not_majority": float(strong_nm.sum()),
        "strong_majority": float(strong_m.sum()),
        "nonstrong_cells": float(nonstrong_b.sum()),
        "nonstrong_not_majority": float(nonstrong_nm.sum()),
        "nonstrong_majority": float(nonstrong_m.sum()),
        "strong_pop": float(np.nansum(np.where(strong_b, pop_b, 0.0))),
        "strong_pop_not_majority": float(np.nansum(np.where(strong_nm, pop_b, 0.0))),
        "strong_built": float(np.nansum(np.where(strong_b, built_b, 0.0))),
        "strong_built_not_majority": float(np.nansum(np.where(strong_nm, built_b, 0.0))),
    }


def combine_stats(block_rows: list[dict[str, float]], indices: np.ndarray) -> dict[str, float]:
    totals: dict[str, float] = {}
    keys = block_rows[0].keys()
    for key in keys:
        totals[key] = float(sum(block_rows[int(idx)][key] for idx in indices))
    return {
        "strong_not_majority_fraction": ratio(totals["strong_not_majority"], totals["strong_cells"]),
        "strong_population_not_majority_fraction": ratio(totals["strong_pop_not_majority"], totals["strong_pop"]),
        "strong_builtup_not_majority_fraction": ratio(totals["strong_built_not_majority"], totals["strong_built"]),
        "strong_vs_nonstrong_not_majority_odds_ratio": odds_ratio(
            totals["strong_not_majority"],
            totals["strong_majority"],
            totals["nonstrong_not_majority"],
            totals["nonstrong_majority"],
        ),
    }


def quantiles(values: list[float]) -> dict[str, float]:
    arr = np.asarray([value for value in values if np.isfinite(value)], dtype=float)
    if arr.size == 0:
        return {"mean": float("nan"), "q025": float("nan"), "q50": float("nan"), "q975": float("nan")}
    return {
        "mean": float(np.mean(arr)),
        "q025": float(np.quantile(arr, 0.025)),
        "q50": float(np.quantile(arr, 0.5)),
        "q975": float(np.quantile(arr, 0.975)),
    }


def bootstrap_metrics(
    base_valid: np.ndarray,
    strong: np.ndarray,
    majority: np.ndarray,
    pop_w: np.ndarray,
    built_w: np.ndarray,
    block_size: int,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> tuple[dict[str, float], dict[str, dict[str, float]], int]:
    blocks = build_blocks(base_valid.shape, block_size)
    block_rows = [block_stats(base_valid, strong, majority, ~majority, pop_w, built_w, block) for block in blocks]
    block_rows = [row for row in block_rows if row["strong_cells"] > 0 or row["nonstrong_cells"] > 0]
    observed = combine_stats(block_rows, np.arange(len(block_rows)))
    samples: dict[str, list[float]] = {key: [] for key in observed}
    for _ in range(n_bootstrap):
        sampled = rng.integers(0, len(block_rows), size=len(block_rows))
        row = combine_stats(block_rows, sampled)
        for key, value in row.items():
            samples[key].append(value)
    return observed, {key: quantiles(values) for key, values in samples.items()}, len(block_rows)


def load_chao_phraya_inputs(
    vlm_tif: Path,
    population_tif: Path,
    builtup_tif: Path,
    downloads_csv: Path,
    threshold: float,
) -> dict[str, Any]:
    vlm = vlm_geotiff_tags(vlm_tif)
    vlm["array"] = vlm["array"].astype(float, copy=True) * 10.0
    valid = valid_vlm_mask(vlm)
    lon, lat = vlm_grid_centers(vlm)
    bbox = {
        "lon_min": float(vlm["lon_min"]),
        "lon_max": float(vlm["lon_max"]),
        "lat_min": float(vlm["lat_min"]),
        "lat_max": float(vlm["lat_max"]),
    }
    pad_deg = 2.0 * max(float(vlm["pixel_size_x"]), float(vlm["pixel_size_y"]))
    pop_source, pop_arr, pop_valid = crop_source(population_tif, expand_bbox(bbox, pad_deg))
    built_source, built_arr, built_valid = crop_source(builtup_tif, expand_bbox(bbox, pad_deg))
    pop_weighted, _pop_cover = area_weighted_transfer(pop_arr, pop_valid, pop_source, vlm)
    built_weighted, _built_cover = area_weighted_transfer(built_arr, built_valid, built_source, vlm)

    download_rows = read_download_rows(downloads_csv, CHAO_PHRAYA_FRAME_ID)
    counts_by_threshold: dict[float, np.ndarray] = {}
    for thr in THRESHOLDS:
        if abs(thr - threshold) < 1e-12:
            count, _inside_any, _ = observable_stack(download_rows, lon, lat, thr)
            counts_by_threshold[thr] = count
        else:
            count, _inside_any, _ = observable_stack(download_rows, lon, lat, thr)
            counts_by_threshold[thr] = count

    return {
        "vlm": vlm,
        "valid": valid,
        "pop_weighted": pop_weighted,
        "built_weighted": built_weighted,
        "counts_by_threshold": counts_by_threshold,
        "download_rows": download_rows,
        "bbox": bbox,
    }


def write_report(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Chao Phraya robustness grid",
        "",
        "This grid sweeps LiCSAR observability thresholds 0.2/0.3/0.4 and strong-subsidence thresholds 3/5/10 mm/yr.",
        "Block bootstrap is used as a screening check for spatial dependence at 5x5, 10x10, and 20x20 VLM-grid blocks.",
        "",
        "## Summary",
        "",
        "| threshold | strong threshold | block | OR | strong not-majority | strong population not-majority | strong built-up not-majority |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['threshold']} | {row['strong_threshold']} | {row['block_size']} | "
            f"{row['strong_vs_nonstrong_not_majority_odds_ratio']:.3f} "
            f"[{row['strong_vs_nonstrong_not_majority_odds_ratio_q025']:.3f}, {row['strong_vs_nonstrong_not_majority_odds_ratio_q975']:.3f}] | "
            f"{row['strong_not_majority_fraction']:.3f} [{row['strong_not_majority_fraction_q025']:.3f}, {row['strong_not_majority_fraction_q975']:.3f}] | "
            f"{row['strong_population_not_majority_fraction']:.3f} [{row['strong_population_not_majority_fraction_q025']:.3f}, {row['strong_population_not_majority_fraction_q975']:.3f}] | "
            f"{row['strong_builtup_not_majority_fraction']:.3f} [{row['strong_builtup_not_majority_fraction_q025']:.3f}, {row['strong_builtup_not_majority_fraction_q975']:.3f}] |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The sensitivity grid is intended to check whether the core censoring signal survives reasonable threshold changes.",
            "- Strong thresholds of 3, 5, and 10 mm/yr bracket a moderate-to-strong deformation regime.",
            "- Block resampling is a screening-level uncertainty check; it does not replace a full spatial model.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vlm-tif", type=Path, default=DEFAULT_VLM_TIF)
    parser.add_argument("--population-tif", type=Path, default=DEFAULT_POP_TIF)
    parser.add_argument("--builtup-tif", type=Path, default=DEFAULT_BUILT_TIF)
    parser.add_argument("--downloads-csv", type=Path, default=CHAO_PHRAYA_DOWNLOADS_CSV)
    parser.add_argument("--outdir", type=Path, default=Path("radar_outputs") / "chao_phraya_robustness_grid")
    parser.add_argument("--n-bootstrap", type=int, default=400)
    parser.add_argument("--seed", type=int, default=20260709)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    inputs = load_chao_phraya_inputs(
        args.vlm_tif,
        args.population_tif,
        args.builtup_tif,
        args.downloads_csv,
        0.3,
    )
    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, Any]] = []
    meta: dict[str, Any] = {
        "thresholds": THRESHOLDS,
        "strong_thresholds": STRONG_THRESHOLDS,
        "block_sizes": BLOCK_SIZES,
        "n_bootstrap": args.n_bootstrap,
        "seed": args.seed,
        "bbox": inputs["bbox"],
        "n_pairs": len(inputs["download_rows"]),
    }
    vlm = inputs["vlm"]
    valid = inputs["valid"]
    pop_w = inputs["pop_weighted"]
    built_w = inputs["built_weighted"]
    counts_by_threshold = inputs["counts_by_threshold"]

    for threshold in THRESHOLDS:
        count = counts_by_threshold[threshold]
        majority = count >= math.ceil(len(inputs["download_rows"]) / 2)
        base_valid = valid & np.isfinite(pop_w) & np.isfinite(built_w)
        for strong_threshold in STRONG_THRESHOLDS:
            strong = base_valid & (vlm["array"] <= -strong_threshold)
            for block_size in BLOCK_SIZES:
                observed, intervals, n_blocks = bootstrap_metrics(
                    base_valid,
                    strong,
                    majority,
                    pop_w,
                    built_w,
                    block_size,
                    args.n_bootstrap,
                    rng,
                )
                row: dict[str, Any] = {
                    "threshold": threshold,
                    "strong_threshold": strong_threshold,
                    "block_size": block_size,
                    "n_blocks": n_blocks,
                    "n_bootstrap": args.n_bootstrap,
                    "n_pairs": len(inputs["download_rows"]),
                }
                for key, value in observed.items():
                    row[key] = value
                    row[f"{key}_q025"] = intervals[key]["q025"]
                    row[f"{key}_q50"] = intervals[key]["q50"]
                    row[f"{key}_q975"] = intervals[key]["q975"]
                    row[f"{key}_boot_mean"] = intervals[key]["mean"]
                rows.append(row)

    fieldnames = list(rows[0].keys())
    write_csv(args.outdir / "chao_phraya_robustness_grid.csv", rows, fieldnames)
    (args.outdir / "chao_phraya_robustness_grid_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_report(args.outdir / "chao_phraya_robustness_grid.md", rows)
    print(json.dumps({"outdir": str(args.outdir), "rows": len(rows)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
