from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from aggregate_licsar_frame_ghsl_exposure_observability import cropped_source
from benchmark_delta_vlm_lisc_observability import (
    download_grid_zip,
    extract_delta_tif,
    fetch_zenodo_record,
    geotiff_tags as vlm_geotiff_tags,
    grid_centers as vlm_grid_centers,
    observable_stack,
    slugify_delta,
    valid_vlm_mask,
)
from compute_central_valley_ghsl_population_censoring import (
    bbox_window,
    geotiff_tags as ghsl_geotiff_tags,
    read_population_crop,
    sample_array_at_centers,
)
from simulate_lisc_observability_censoring import read_csv, write_csv


CONFIGS = [
    {
        "delta": "po",
        "label": "Po",
        "frame_id": "117A_04454_131312",
        "downloads_csv": Path("radar_outputs") / "po_venice_lisc_ghsl_exposure_observability" / "frame_ghsl_exposure_downloads.csv",
    },
    {
        "delta": "chaoPhraya",
        "label": "Chao Phraya",
        "frame_id": "062D_07629_131313",
        "downloads_csv": Path("radar_outputs") / "chao_phraya_lisc_ghsl_exposure_observability" / "frame_ghsl_exposure_downloads.csv",
    },
    {
        "delta": "brantas",
        "label": "Brantas",
        "frame_id": "003D_09757_111111",
        "downloads_csv": Path("radar_outputs") / "brantas_lisc_ghsl_exposure_observability" / "frame_ghsl_exposure_downloads.csv",
    },
]


DEFAULT_POP_TIF = Path("radar_outputs") / "central_valley_ghsl_population_censoring" / "GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif"
DEFAULT_BUILT_TIF = Path("radar_outputs") / "central_valley_ghsl_builtup_censoring" / "GHS_BUILT_S_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif"


def bbox_from_info(info: dict[str, Any]) -> dict[str, float]:
    return {
        "lon_min": float(info["lon_min"]),
        "lon_max": float(info["lon_max"]),
        "lat_min": float(info["lat_min"]),
        "lat_max": float(info["lat_max"]),
    }


def read_ghsl_source(path: Path, bbox: dict[str, float]) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
    info = ghsl_geotiff_tags(path)
    window = bbox_window(info, bbox)
    arr = read_population_crop(path, window)
    source = cropped_source({**info, "window": list(window)}, arr)
    nodata = info.get("nodata", np.nan)
    valid = np.isfinite(arr) & (arr >= 0)
    if np.isfinite(nodata):
        valid &= arr != nodata
    return source, arr, valid


def read_download_rows(path: Path, frame_id: str) -> list[dict[str, str]]:
    rows = []
    for row in read_csv(path):
        if row.get("download_status") != "ok":
            continue
        if row.get("frame_id") and row["frame_id"] != frame_id:
            continue
        if Path(row["local_path"]).exists():
            rows.append(row)
    rows.sort(key=lambda row: row["pair"])
    return rows


def ratio(num: float, den: float) -> float:
    return float(num / den) if den else 0.0


def weighted_sum(weight: np.ndarray, mask: np.ndarray) -> float:
    return float(np.nansum(np.where(mask, weight, 0.0)))


def odds_ratio(a: int, b: int, c: int, d: int) -> float:
    # Haldane-Anscombe correction keeps the metric finite for sparse strata.
    return float(((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5)))


def summarize_delta(
    label: str,
    frame_id: str,
    vlm_info: dict[str, Any],
    valid: np.ndarray,
    n_pairs: int,
    count: np.ndarray,
    inside_any: np.ndarray,
    pop: np.ndarray,
    pop_valid: np.ndarray,
    built: np.ndarray,
    built_valid: np.ndarray,
    threshold: float,
) -> dict[str, Any]:
    vlm = vlm_info["array"].astype(float, copy=False)
    obs_fraction = count.astype(float) / float(n_pairs)
    majority = count >= math.ceil(n_pairs / 2)
    stable75 = count >= math.ceil(n_pairs * 0.75)
    any_obs = count >= 1
    low25 = obs_fraction < 0.25

    base_valid = valid & inside_any
    strong5 = base_valid & (vlm <= -5.0)
    nonstrong5 = base_valid & (vlm > -5.0)
    not_majority = base_valid & ~majority
    not_stable75 = base_valid & ~stable75
    never = base_valid & ~any_obs

    pop_w = np.where(base_valid & pop_valid, pop, 0.0)
    built_w = np.where(base_valid & built_valid, built, 0.0)

    strong_not_majority = strong5 & ~majority
    strong_not_stable75 = strong5 & ~stable75
    strong_never = strong5 & ~any_obs
    strong_low25 = strong5 & low25

    nonstrong_not_majority = nonstrong5 & ~majority

    a = int(strong_not_majority.sum())
    b = int((strong5 & majority).sum())
    c = int(nonstrong_not_majority.sum())
    d = int((nonstrong5 & majority).sum())

    total_pop = weighted_sum(pop_w, base_valid)
    strong_pop = weighted_sum(pop_w, strong5)
    strong_pop_not_majority = weighted_sum(pop_w, strong_not_majority)
    strong_pop_not_stable75 = weighted_sum(pop_w, strong_not_stable75)
    strong_pop_never = weighted_sum(pop_w, strong_never)

    total_built_m2 = weighted_sum(built_w, base_valid)
    strong_built_m2 = weighted_sum(built_w, strong5)
    strong_built_not_majority_m2 = weighted_sum(built_w, strong_not_majority)
    strong_built_not_stable75_m2 = weighted_sum(built_w, strong_not_stable75)
    strong_built_never_m2 = weighted_sum(built_w, strong_never)

    return {
        "delta": label,
        "frame_id": frame_id,
        "threshold": threshold,
        "n_pairs": n_pairs,
        "valid_vlm_cells": int(valid.sum()),
        "covered_vlm_cells": int(base_valid.sum()),
        "strong_sub_5mm_cells": int(strong5.sum()),
        "strong_sub_5mm_fraction": ratio(int(strong5.sum()), int(base_valid.sum())),
        "strong_sub_5mm_mean_vlm_mm_yr": float(np.nanmean(vlm[strong5])) if strong5.any() else float("nan"),
        "strong_sub_5mm_mean_observability": float(np.nanmean(obs_fraction[strong5])) if strong5.any() else float("nan"),
        "strong_sub_5mm_never_observable_fraction": ratio(int(strong_never.sum()), int(strong5.sum())),
        "strong_sub_5mm_not_majority_fraction": ratio(int(strong_not_majority.sum()), int(strong5.sum())),
        "strong_sub_5mm_not_stable75_fraction": ratio(int(strong_not_stable75.sum()), int(strong5.sum())),
        "strong_sub_5mm_obs_lt_0p25_fraction": ratio(int(strong_low25.sum()), int(strong5.sum())),
        "nonstrong_not_majority_fraction": ratio(int(nonstrong_not_majority.sum()), int(nonstrong5.sum())),
        "strong_vs_nonstrong_not_majority_odds_ratio": odds_ratio(a, b, c, d),
        "total_population_vlm_grid": total_pop,
        "strong_sub_5mm_population": strong_pop,
        "strong_sub_5mm_population_fraction": ratio(strong_pop, total_pop),
        "strong_sub_5mm_population_never_observable": strong_pop_never,
        "strong_sub_5mm_population_not_majority": strong_pop_not_majority,
        "strong_sub_5mm_population_not_stable75": strong_pop_not_stable75,
        "strong_sub_5mm_population_never_observable_fraction": ratio(strong_pop_never, strong_pop),
        "strong_sub_5mm_population_not_majority_fraction": ratio(strong_pop_not_majority, strong_pop),
        "strong_sub_5mm_population_not_stable75_fraction": ratio(strong_pop_not_stable75, strong_pop),
        "total_builtup_km2_vlm_grid": total_built_m2 / 1_000_000.0,
        "strong_sub_5mm_builtup_km2": strong_built_m2 / 1_000_000.0,
        "strong_sub_5mm_builtup_fraction": ratio(strong_built_m2, total_built_m2),
        "strong_sub_5mm_builtup_never_observable_km2": strong_built_never_m2 / 1_000_000.0,
        "strong_sub_5mm_builtup_not_majority_km2": strong_built_not_majority_m2 / 1_000_000.0,
        "strong_sub_5mm_builtup_not_stable75_km2": strong_built_not_stable75_m2 / 1_000_000.0,
        "strong_sub_5mm_builtup_never_observable_fraction": ratio(strong_built_never_m2, strong_built_m2),
        "strong_sub_5mm_builtup_not_majority_fraction": ratio(strong_built_not_majority_m2, strong_built_m2),
        "strong_sub_5mm_builtup_not_stable75_fraction": ratio(strong_built_not_stable75_m2, strong_built_m2),
    }


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Multi-delta VLM-grid exposure censoring",
        "",
        "This report places Nature 2026 VLM, LiCSAR observability, GHSL population, and GHSL built-up on the VLM grid.",
        "",
        "## Strong-Subsidence Exposure Closure",
        "",
        "| delta | strong cells | strong pop | pop not majority | pop not stable-75 | strong built-up km2 | built-up not majority | built-up not stable-75 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['delta']} | {row['strong_sub_5mm_cells']} | "
            f"{row['strong_sub_5mm_population']:.0f} | {row['strong_sub_5mm_population_not_majority_fraction']:.3f} | "
            f"{row['strong_sub_5mm_population_not_stable75_fraction']:.3f} | "
            f"{row['strong_sub_5mm_builtup_km2']:.3f} | {row['strong_sub_5mm_builtup_not_majority_fraction']:.3f} | "
            f"{row['strong_sub_5mm_builtup_not_stable75_fraction']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Strong-vs-Nonstrong Cell Test",
            "",
            "| delta | strong not majority | nonstrong not majority | odds ratio |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['delta']} | {row['strong_sub_5mm_not_majority_fraction']:.3f} | "
            f"{row['nonstrong_not_majority_fraction']:.3f} | {row['strong_vs_nonstrong_not_majority_odds_ratio']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a same-grid exposure closure, not just a frame-level exposure observability summary.",
            "- Population and built-up weights are sampled from GHSL at VLM grid-cell centers; this is stronger than separate frame-level summaries but still not a polygon area-weighted overlay.",
            "- The odds ratio is a screening statistic, not a spatially autocorrelation-corrected inferential model.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("radar_outputs") / "multi_delta_vlm_exposure_censoring")
    parser.add_argument("--population-tif", type=Path, default=DEFAULT_POP_TIF)
    parser.add_argument("--builtup-tif", type=Path, default=DEFAULT_BUILT_TIF)
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--vlm-scale-to-mm", type=float, default=10.0)
    parser.add_argument("--timeout", type=int, default=300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    record = fetch_zenodo_record(args.outdir, args.timeout)
    grid_zip, zip_status = download_grid_zip(record, args.outdir, args.timeout)

    rows: list[dict[str, Any]] = []
    meta: dict[str, Any] = {"zip": zip_status, "threshold": args.threshold, "deltas": []}
    for config in CONFIGS:
        delta_slug = slugify_delta(config["delta"])
        delta_dir = args.outdir / delta_slug
        delta_dir.mkdir(parents=True, exist_ok=True)
        vlm_path, _members = extract_delta_tif(grid_zip, config["delta"], delta_dir)
        vlm_info = vlm_geotiff_tags(vlm_path)
        vlm_info["array"] = vlm_info["array"].astype(float, copy=True) * float(args.vlm_scale_to_mm)
        valid = valid_vlm_mask(vlm_info)
        lon, lat = vlm_grid_centers(vlm_info)
        bbox = bbox_from_info(vlm_info)

        pop_source, _pop_crop, _pop_valid_crop = read_ghsl_source(args.population_tif, bbox)
        built_source, _built_crop, _built_valid_crop = read_ghsl_source(args.builtup_tif, bbox)
        pop_sample, inside_pop = sample_array_at_centers(pop_source, lon, lat)
        built_sample, inside_built = sample_array_at_centers(built_source, lon, lat)
        pop_valid = inside_pop & np.isfinite(pop_sample) & (pop_sample >= 0)
        built_valid = inside_built & np.isfinite(built_sample) & (built_sample >= 0)

        download_rows = read_download_rows(config["downloads_csv"], config["frame_id"])
        count, inside_any, _pair_rows = observable_stack(download_rows, lon, lat, args.threshold)
        row = summarize_delta(
            config["label"],
            config["frame_id"],
            vlm_info,
            valid,
            len(download_rows),
            count,
            inside_any,
            pop_sample,
            pop_valid,
            built_sample,
            built_valid,
            args.threshold,
        )
        rows.append(row)
        meta["deltas"].append(
            {
                "delta": config["label"],
                "frame_id": config["frame_id"],
                "vlm_path": str(vlm_path),
                "downloads_csv": str(config["downloads_csv"]),
                "n_pairs": len(download_rows),
                "bbox": bbox,
            }
        )

    fieldnames = list(rows[0].keys())
    write_csv(args.outdir / "multi_delta_vlm_exposure_censoring_summary.csv", rows, fieldnames)
    (args.outdir / "multi_delta_vlm_exposure_censoring_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(args.outdir / "multi_delta_vlm_exposure_censoring_report.md", rows)
    print(json.dumps({"outdir": str(args.outdir), "deltas": len(rows), "rows": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
