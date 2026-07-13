from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from benchmark_delta_vlm_lisc_observability import (
    geotiff_tags as vlm_geotiff_tags,
    grid_centers as vlm_grid_centers,
    observable_stack,
    read_download_rows,
    valid_vlm_mask,
    write_csv,
)
from compute_central_valley_ghsl_population_censoring import (
    bbox_window,
    geotiff_tags as ghsl_geotiff_tags,
    read_population_crop,
)


CHAO_PHRAYA_FRAME_ID = "062D_07629_131313"
CHAO_PHRAYA_DOWNLOADS_CSV = (
    Path.home() / "radar_outputs" / "chao_phraya_lisc_ghsl_exposure_observability" / "frame_ghsl_exposure_downloads.csv"
)
DEFAULT_VLM_TIF = (
    Path.home() / "radar_outputs"
    / "delta_binomial_with_worldcover_main"
    / "chao_phraya"
    / "gridVLM"
    / "chaoPhraya_vlm.tif"
)
DEFAULT_POP_TIF = (
    Path.home() / "radar_outputs"
    / "central_valley_ghsl_population_censoring"
    / "GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif"
)
DEFAULT_BUILT_TIF = (
    Path.home() / "radar_outputs"
    / "central_valley_ghsl_builtup_censoring"
    / "GHS_BUILT_S_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif"
)

EARTH_RADIUS_M = 6_371_000.0


def ratio(num: float, den: float) -> float:
    return float(num / den) if den else 0.0


def expand_bbox(bbox: dict[str, float], pad_deg: float) -> dict[str, float]:
    return {
        "lon_min": bbox["lon_min"] - pad_deg,
        "lon_max": bbox["lon_max"] + pad_deg,
        "lat_min": bbox["lat_min"] - pad_deg,
        "lat_max": bbox["lat_max"] + pad_deg,
    }


def crop_source(path: Path, bbox: dict[str, float]) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
    info = ghsl_geotiff_tags(path)
    window = bbox_window(info, bbox)
    arr = read_population_crop(path, window)
    cropped = {
        **info,
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "tie_lon": info["tie_lon"] + window[2] * info["pixel_size_x"],
        "tie_lat": info["tie_lat"] - window[0] * info["pixel_size_y"],
        "lon_min": info["tie_lon"] + window[2] * info["pixel_size_x"],
        "lon_max": info["tie_lon"] + window[3] * info["pixel_size_x"],
        "lat_max": info["tie_lat"] - window[0] * info["pixel_size_y"],
        "lat_min": info["tie_lat"] - window[1] * info["pixel_size_y"],
        "window": list(window),
    }
    nodata = cropped.get("nodata", np.nan)
    valid = np.isfinite(arr) & (arr >= 0)
    if np.isfinite(nodata):
        valid &= arr != nodata
    return cropped, arr.astype(float, copy=False), valid


def cell_bounds(info: dict[str, Any], row: int, col: int) -> tuple[float, float, float, float]:
    west = float(info["tie_lon"] + col * info["pixel_size_x"])
    east = west + float(info["pixel_size_x"])
    north = float(info["tie_lat"] - row * info["pixel_size_y"])
    south = north - float(info["pixel_size_y"])
    return west, east, south, north


def source_cell_area(info: dict[str, Any], row: int) -> float:
    north = math.radians(float(info["tie_lat"] - row * info["pixel_size_y"]))
    south = math.radians(float(info["tie_lat"] - (row + 1) * info["pixel_size_y"]))
    lon_width = math.radians(float(info["pixel_size_x"]))
    return EARTH_RADIUS_M**2 * lon_width * abs(math.sin(north) - math.sin(south))


def target_cell_area(info: dict[str, Any], row: int) -> float:
    return source_cell_area(info, row)


def overlap_area_m2(
    target: dict[str, Any],
    source: dict[str, Any],
    t_row: int,
    t_col: int,
    s_row: int,
    s_col: int,
) -> float:
    twest, teast, tsouth, tnorth = cell_bounds(target, t_row, t_col)
    swest, seast, ssouth, snorth = cell_bounds(source, s_row, s_col)
    west = max(twest, swest)
    east = min(teast, seast)
    south = max(tsouth, ssouth)
    north = min(tnorth, snorth)
    if east <= west or north <= south:
        return 0.0
    lon = math.radians(east - west)
    lat = abs(math.sin(math.radians(north)) - math.sin(math.radians(south)))
    return EARTH_RADIUS_M**2 * lon * lat


def candidate_range(
    target_min: float,
    target_max: float,
    source_origin: float,
    source_step: float,
    limit: int,
    is_lon: bool,
) -> tuple[int, int]:
    if is_lon:
        start = int(math.floor((target_min - source_origin) / source_step)) - 1
        stop = int(math.ceil((target_max - source_origin) / source_step)) + 1
    else:
        start = int(math.floor((source_origin - target_max) / source_step)) - 1
        stop = int(math.ceil((source_origin - target_min) / source_step)) + 1
    return max(0, start), min(limit - 1, stop)


def area_weighted_transfer(
    source_arr: np.ndarray,
    source_valid: np.ndarray,
    source_info: dict[str, Any],
    target_info: dict[str, Any],
    target_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    out = np.full((target_info["height"], target_info["width"]), np.nan, dtype=float)
    cover = np.zeros_like(out, dtype=float)
    for t_row in range(target_info["height"]):
        tnorth = float(target_info["tie_lat"] - t_row * target_info["pixel_size_y"])
        tsouth = tnorth - float(target_info["pixel_size_y"])
        s_row0, s_row1 = candidate_range(tsouth, tnorth, source_info["tie_lat"], source_info["pixel_size_y"], source_info["height"], False)
        for t_col in range(target_info["width"]):
            if target_mask is not None and not target_mask[t_row, t_col]:
                continue
            twest = float(target_info["tie_lon"] + t_col * target_info["pixel_size_x"])
            teast = twest + float(target_info["pixel_size_x"])
            s_col0, s_col1 = candidate_range(twest, teast, source_info["tie_lon"], source_info["pixel_size_x"], source_info["width"], True)
            total = 0.0
            covered = 0.0
            for s_row in range(s_row0, s_row1 + 1):
                snorth = float(source_info["tie_lat"] - s_row * source_info["pixel_size_y"])
                ssouth = snorth - float(source_info["pixel_size_y"])
                lat_overlap = min(tnorth, snorth) - max(tsouth, ssouth)
                if lat_overlap <= 0:
                    continue
                src_row_area = source_cell_area(source_info, s_row)
                for s_col in range(s_col0, s_col1 + 1):
                    swest = float(source_info["tie_lon"] + s_col * source_info["pixel_size_x"])
                    seast = swest + float(source_info["pixel_size_x"])
                    lon_overlap = min(teast, seast) - max(twest, swest)
                    if lon_overlap <= 0:
                        continue
                    overlap = EARTH_RADIUS_M**2 * math.radians(lon_overlap) * abs(
                        math.sin(math.radians(min(tnorth, snorth)))
                        - math.sin(math.radians(max(tsouth, ssouth)))
                    )
                    covered += overlap
                    if source_valid[s_row, s_col]:
                        frac = overlap / src_row_area if src_row_area else 0.0
                        total += float(source_arr[s_row, s_col]) * frac
            if covered > 0:
                out[t_row, t_col] = total
                cover[t_row, t_col] = covered / target_cell_area(target_info, t_row)
    return out, cover


def summarize(
    vlm_info: dict[str, Any],
    valid_vlm: np.ndarray,
    count: np.ndarray,
    inside_any: np.ndarray,
    pop: np.ndarray,
    pop_cover: np.ndarray,
    pop_valid: np.ndarray,
    built: np.ndarray,
    built_cover: np.ndarray,
    built_valid: np.ndarray,
    n_pairs: int,
    threshold: float,
) -> dict[str, Any]:
    vlm = vlm_info["array"].astype(float, copy=False)
    obs_fraction = count.astype(float) / float(max(1, n_pairs))
    base_valid = valid_vlm & inside_any & pop_valid & built_valid
    strong5 = base_valid & (vlm <= -5.0)
    nonstrong5 = base_valid & ~strong5
    any_obs = count >= 1
    majority = count >= math.ceil(n_pairs / 2)
    stable75 = count >= math.ceil(n_pairs * 0.75)
    low25 = count < math.ceil(n_pairs * 0.25)
    not_majority = ~majority

    pop_w = np.where(base_valid, pop, 0.0)
    built_w = np.where(base_valid, built, 0.0)

    def wsum(weight: np.ndarray, mask: np.ndarray) -> float:
        return float(np.nansum(np.where(mask & base_valid, weight, 0.0)))

    strong_not_majority = strong5 & not_majority
    strong_not_stable75 = strong5 & ~stable75
    strong_never = strong5 & ~any_obs
    strong_low25 = strong5 & low25
    nonstrong_not_majority = nonstrong5 & not_majority

    a = int(strong_not_majority.sum())
    b = int((strong5 & majority).sum())
    c = int(nonstrong_not_majority.sum())
    d = int((nonstrong5 & majority).sum())

    total_pop = float(np.nansum(pop_w))
    total_built_m2 = float(np.nansum(built_w))
    strong_pop = wsum(pop_w, strong5)
    strong_built_m2 = wsum(built_w, strong5)

    return {
        "frame_id": CHAO_PHRAYA_FRAME_ID,
        "coherence_threshold": threshold,
        "n_pairs": n_pairs,
        "valid_vlm_cells": int(valid_vlm.sum()),
        "covered_vlm_cells": int(base_valid.sum()),
        "strong_sub_5mm_cells": int(strong5.sum()),
        "strong_sub_5mm_fraction": ratio(int(strong5.sum()), int(base_valid.sum())),
        "strong_sub_5mm_mean_vlm_mm_yr": float(np.nanmean(vlm[strong5])) if strong5.any() else float("nan"),
        "strong_sub_5mm_mean_observability": float(np.nanmean(obs_fraction[strong5])) if strong5.any() else float("nan"),
        "strong_sub_5mm_never_observable_fraction": ratio(int(strong_never.sum()), int(strong5.sum())),
        "strong_sub_5mm_not_majority_fraction": ratio(int(strong_not_majority.sum()), int(strong5.sum())),
        "strong_sub_5mm_not_stable75_fraction": ratio(int(strong_not_stable75.sum()), int(strong5.sum())),
        "strong_sub_5mm_obs_lt_0p25_fraction": ratio(int(strong_low25.sum()), int(strong5.sum())),
        "strong_vs_nonstrong_not_majority_odds_ratio": ratio((a + 0.5) * (d + 0.5), (b + 0.5) * (c + 0.5)),
        "total_population_vlm_grid": total_pop,
        "strong_sub_5mm_population": strong_pop,
        "strong_sub_5mm_population_fraction": ratio(strong_pop, total_pop),
        "strong_sub_5mm_population_never_observable": wsum(pop_w, strong_never),
        "strong_sub_5mm_population_not_majority": wsum(pop_w, strong_not_majority),
        "strong_sub_5mm_population_not_stable75": wsum(pop_w, strong_not_stable75),
        "strong_sub_5mm_population_never_observable_fraction": ratio(wsum(pop_w, strong_never), strong_pop),
        "strong_sub_5mm_population_not_majority_fraction": ratio(wsum(pop_w, strong_not_majority), strong_pop),
        "strong_sub_5mm_population_not_stable75_fraction": ratio(wsum(pop_w, strong_not_stable75), strong_pop),
        "total_builtup_km2_vlm_grid": total_built_m2 / 1_000_000.0,
        "strong_sub_5mm_builtup_km2": strong_built_m2 / 1_000_000.0,
        "strong_sub_5mm_builtup_fraction": ratio(strong_built_m2, total_built_m2),
        "strong_sub_5mm_builtup_never_observable_km2": wsum(built_w, strong_never) / 1_000_000.0,
        "strong_sub_5mm_builtup_not_majority_km2": wsum(built_w, strong_not_majority) / 1_000_000.0,
        "strong_sub_5mm_builtup_not_stable75_km2": wsum(built_w, strong_not_stable75) / 1_000_000.0,
        "strong_sub_5mm_builtup_never_observable_fraction": ratio(wsum(built_w, strong_never), strong_built_m2),
        "strong_sub_5mm_builtup_not_majority_fraction": ratio(wsum(built_w, strong_not_majority), strong_built_m2),
        "strong_sub_5mm_builtup_not_stable75_fraction": ratio(wsum(built_w, strong_not_stable75), strong_built_m2),
        "population_any_observable": wsum(pop_w, any_obs),
        "population_majority_observable": wsum(pop_w, majority),
        "population_not_majority_observable": wsum(pop_w, not_majority),
        "population_never_observable": wsum(pop_w, ~any_obs),
        "population_obs_lt_0p25": wsum(pop_w, low25),
        "population_any_observable_fraction": ratio(wsum(pop_w, any_obs), total_pop),
        "population_majority_observable_fraction": ratio(wsum(pop_w, majority), total_pop),
        "population_not_majority_observable_fraction": ratio(wsum(pop_w, not_majority), total_pop),
        "population_never_observable_fraction": ratio(wsum(pop_w, ~any_obs), total_pop),
        "population_obs_lt_0p25_fraction": ratio(wsum(pop_w, low25), total_pop),
        "builtup_any_observable_km2": wsum(built_w, any_obs) / 1_000_000.0,
        "builtup_majority_observable_km2": wsum(built_w, majority) / 1_000_000.0,
        "builtup_not_majority_observable_km2": wsum(built_w, not_majority) / 1_000_000.0,
        "builtup_never_observable_km2": wsum(built_w, ~any_obs) / 1_000_000.0,
        "builtup_obs_lt_0p25_km2": wsum(built_w, low25) / 1_000_000.0,
        "builtup_any_observable_fraction": ratio(wsum(built_w, any_obs), total_built_m2),
        "builtup_majority_observable_fraction": ratio(wsum(built_w, majority), total_built_m2),
        "builtup_not_majority_observable_fraction": ratio(wsum(built_w, not_majority), total_built_m2),
        "builtup_never_observable_fraction": ratio(wsum(built_w, ~any_obs), total_built_m2),
        "builtup_obs_lt_0p25_fraction": ratio(wsum(built_w, low25), total_built_m2),
        "population_weighted_mean_observability": ratio(float(np.nansum(pop_w * obs_fraction)), total_pop),
        "builtup_weighted_mean_observability": ratio(float(np.nansum(built_w * obs_fraction)), total_built_m2),
        "mean_pop_cover_fraction": float(np.nanmean(pop_cover[base_valid])) if base_valid.any() else float("nan"),
        "mean_built_cover_fraction": float(np.nanmean(built_cover[base_valid])) if base_valid.any() else float("nan"),
    }


def write_markdown(path: Path, row: dict[str, Any]) -> None:
    lines = [
        "# Chao Phraya area-weighted GHSL exposure censoring",
        "",
        "This report transfers GHSL population and built-up totals onto the Chao Phraya VLM grid using exact cell-overlap area weights, then applies LiCSAR coherence observability on the same VLM cells.",
        "",
        "## Core Summary",
        "",
        f"- Frame ID: `{row['frame_id']}`",
        f"- Coherence threshold: `{row['coherence_threshold']}`",
        f"- LiCSAR pairs: `{row['n_pairs']}`",
        f"- Valid VLM cells: `{row['valid_vlm_cells']}`",
        f"- Covered VLM cells: `{row['covered_vlm_cells']}`",
        "",
        "## Exposure Closure",
        "",
        "| metric | population | built-up km2 |",
        "|---|---:|---:|",
        f"| total | {row['total_population_vlm_grid']:.1f} | {row['total_builtup_km2_vlm_grid']:.3f} |",
        f"| strong subsidence | {row['strong_sub_5mm_population']:.1f} | {row['strong_sub_5mm_builtup_km2']:.3f} |",
        f"| strong and not majority observable | {row['strong_sub_5mm_population_not_majority']:.1f} | {row['strong_sub_5mm_builtup_not_majority_km2']:.3f} |",
        f"| strong and never observable | {row['strong_sub_5mm_population_never_observable']:.1f} | {row['strong_sub_5mm_builtup_never_observable_km2']:.3f} |",
        "",
        "## Visibility Share",
        "",
        f"- Population weighted mean observability: `{row['population_weighted_mean_observability']:.3f}`",
        f"- Built-up weighted mean observability: `{row['builtup_weighted_mean_observability']:.3f}`",
        f"- Population not majority observable fraction: `{row['population_not_majority_observable_fraction']:.3f}`",
        f"- Built-up not majority observable fraction: `{row['builtup_not_majority_observable_fraction']:.3f}`",
        "",
        "## Interpretation",
        "",
        "- This version is area-weighted at the GHSL-to-VLM transfer step, so it is stronger than the earlier center-sampled closure.",
        "- Observability is still evaluated at VLM-cell centers from the LiCSAR coherence stack.",
        "- The result is intended to support the paper's core claim that exposure underestimation is a product of observability censoring, not just a sampling artifact.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_cell_table(
    path: Path,
    vlm_info: dict[str, Any],
    count: np.ndarray,
    pop: np.ndarray,
    pop_cover: np.ndarray,
    built: np.ndarray,
    built_cover: np.ndarray,
    base_valid: np.ndarray,
    n_pairs: int,
) -> None:
    rows: list[dict[str, Any]] = []
    for row in range(vlm_info["height"]):
        for col in range(vlm_info["width"]):
            if not base_valid[row, col]:
                continue
            west, east, south, north = cell_bounds(vlm_info, row, col)
            rows.append(
                {
                    "row": row,
                    "col": col,
                    "lon_center": west + 0.5 * vlm_info["pixel_size_x"],
                    "lat_center": south + 0.5 * vlm_info["pixel_size_y"],
                    "vlm_mm_yr": float(vlm_info["array"][row, col]),
                    "observable_count": int(count[row, col]),
                    "observable_fraction": float(count[row, col] / float(max(1, n_pairs))),
                    "any_observable": int(count[row, col] >= 1),
                    "majority_observable": int(count[row, col] >= math.ceil(n_pairs / 2)),
                    "not_majority_observable": int(count[row, col] < math.ceil(n_pairs / 2)),
                    "strong_sub_5mm": int(vlm_info["array"][row, col] <= -5.0),
                    "population_weighted": float(pop[row, col]),
                    "population_cover_fraction": float(pop_cover[row, col]),
                    "builtup_m2_weighted": float(built[row, col]),
                    "builtup_cover_fraction": float(built_cover[row, col]),
                }
            )
    write_csv(
        path,
        rows,
        [
            "row",
            "col",
            "lon_center",
            "lat_center",
            "vlm_mm_yr",
            "observable_count",
            "observable_fraction",
            "any_observable",
            "majority_observable",
            "not_majority_observable",
            "strong_sub_5mm",
            "population_weighted",
            "population_cover_fraction",
            "builtup_m2_weighted",
            "builtup_cover_fraction",
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vlm-tif", type=Path, default=DEFAULT_VLM_TIF)
    parser.add_argument("--population-tif", type=Path, default=DEFAULT_POP_TIF)
    parser.add_argument("--builtup-tif", type=Path, default=DEFAULT_BUILT_TIF)
    parser.add_argument("--downloads-csv", type=Path, default=CHAO_PHRAYA_DOWNLOADS_CSV)
    parser.add_argument("--frame-id", default=CHAO_PHRAYA_FRAME_ID)
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--vlm-scale-to-mm", type=float, default=10.0)
    parser.add_argument("--outdir", type=Path, default=Path("radar_outputs") / "chao_phraya_area_weighted_exposure_censoring")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    vlm_info = vlm_geotiff_tags(args.vlm_tif)
    vlm_info["array"] = vlm_info["array"].astype(float, copy=True) * float(args.vlm_scale_to_mm)
    valid_vlm = valid_vlm_mask(vlm_info)
    lon, lat = vlm_grid_centers(vlm_info)
    bbox = {
        "lon_min": float(vlm_info["lon_min"]),
        "lon_max": float(vlm_info["lon_max"]),
        "lat_min": float(vlm_info["lat_min"]),
        "lat_max": float(vlm_info["lat_max"]),
    }

    pad_deg = 2.0 * max(float(vlm_info["pixel_size_x"]), float(vlm_info["pixel_size_y"]))
    pop_source, pop_arr, pop_src_valid = crop_source(args.population_tif, expand_bbox(bbox, pad_deg))
    built_source, built_arr, built_src_valid = crop_source(args.builtup_tif, expand_bbox(bbox, pad_deg))

    pop_weighted, pop_cover = area_weighted_transfer(pop_arr, pop_src_valid, pop_source, vlm_info)
    built_weighted, built_cover = area_weighted_transfer(built_arr, built_src_valid, built_source, vlm_info)

    pop_valid = np.isfinite(pop_weighted) & (pop_weighted >= 0) & (pop_cover > 0)
    built_valid = np.isfinite(built_weighted) & (built_weighted >= 0) & (built_cover > 0)

    download_rows = read_download_rows(args.downloads_csv, args.frame_id)
    count, inside_any, pair_rows = observable_stack(download_rows, lon, lat, args.threshold)

    row = summarize(
        vlm_info,
        valid_vlm,
        count,
        inside_any,
        pop_weighted,
        pop_cover,
        pop_valid,
        built_weighted,
        built_cover,
        built_valid,
        len(download_rows),
        args.threshold,
    )

    base_valid = valid_vlm & inside_any & pop_valid & built_valid

    write_csv(
        args.outdir / "chao_phraya_area_weighted_exposure_summary.csv",
        [row],
        list(row.keys()),
    )
    write_cell_table(
        args.outdir / "chao_phraya_area_weighted_exposure_cells.csv",
        vlm_info,
        count,
        pop_weighted,
        pop_cover,
        built_weighted,
        built_cover,
        base_valid,
        len(download_rows),
    )
    meta = {
        "vlm_tif": str(args.vlm_tif),
        "population_tif": str(args.population_tif),
        "builtup_tif": str(args.builtup_tif),
        "downloads_csv": str(args.downloads_csv),
        "download_rows": len(download_rows),
        "threshold": args.threshold,
        "vlm_scale_to_mm": args.vlm_scale_to_mm,
        "bbox": bbox,
        "pad_deg": pad_deg,
        "vlm_info": {k: v for k, v in vlm_info.items() if k != "array"},
        "pair_rows": pair_rows,
        "summary": row,
    }
    (args.outdir / "chao_phraya_area_weighted_exposure_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(args.outdir / "chao_phraya_area_weighted_exposure_report.md", row)
    print(json.dumps({"outdir": str(args.outdir), "summary": row}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
