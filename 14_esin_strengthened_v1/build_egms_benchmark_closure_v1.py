from __future__ import annotations

import argparse
import csv
import gzip
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import rasterio


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "03_exposure_closure" / "egms_benchmark_closure_v1"
POP_TIF = ROOT / "radar_outputs" / "central_valley_ghsl_population_censoring" / "GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif"
BUILT_TIF = ROOT / "radar_outputs" / "central_valley_ghsl_builtup_censoring" / "GHS_BUILT_S_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif"


LON_CANDIDATES = ["longitude", "lon", "x", "long"]
LAT_CANDIDATES = ["latitude", "lat", "y"]
VEL_CANDIDATES = [
    "mean_velocity",
    "velocity",
    "vel",
    "up_velocity",
    "vertical_velocity",
    "vertical_velocity_mm_year",
    "vertical_velocity_mm_per_year",
    "mean_velocity_mm_year",
    "mean_velocity_mm_per_year",
    "mean_velocity_mm_yr",
    "mean_vel",
    "v_mean",
    "v_up",
    "vu",
    "ortho_up",
    "up",
]
COH_CANDIDATES = ["temporal_coherence", "coherence", "temp_coh"]
AMP_CANDIDATES = ["amplitude_dispersion", "amp_dispersion", "ad"]


def normalize_column_name(name: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in str(name)).strip("_")


def find_column(columns: list[str], candidates: list[str], label: str) -> str:
    lower = {normalize_column_name(c): c for c in columns}
    for candidate in candidates:
        key = normalize_column_name(candidate)
        if key in lower:
            return lower[key]
    for candidate in candidates:
        key = normalize_column_name(candidate)
        for normalized, original in lower.items():
            if key and key in normalized:
                return original
    preview = ", ".join(map(str, columns[:80]))
    raise ValueError(
        f"Could not find {label} column using candidates {candidates}. "
        f"Available columns preview: {preview}"
    )


def optional_column(columns: list[str], candidates: list[str]) -> str | None:
    lower = {normalize_column_name(c): c for c in columns}
    for candidate in candidates:
        key = normalize_column_name(candidate)
        if key in lower:
            return lower[key]
    for candidate in candidates:
        key = normalize_column_name(candidate)
        for normalized, original in lower.items():
            if key and key in normalized:
                return original
    return None


def read_points(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    suffixes = [s.lower() for s in path.suffixes]
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if suffix in {".csv", ".txt"} or suffixes[-2:] == [".csv", ".gz"]:
        return pd.read_csv(path)
    if suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            return pd.read_csv(fh)
    raise ValueError(f"Unsupported input format: {path}. Use parquet, pq, csv or csv.gz.")


def sample_raster(path: Path, lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    with rasterio.open(path) as src:
        samples = np.array([v[0] for v in src.sample(zip(lon, lat))], dtype=float)
        if src.nodata is not None:
            samples[samples == src.nodata] = np.nan
        return samples


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def finite_sum(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    return float(np.nansum(values))


def finite_median(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    return float(np.nanmedian(values)) if np.isfinite(values).any() else float("nan")


def quantile(series: pd.Series, q: float) -> float:
    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    return float(np.nanquantile(values, q)) if np.isfinite(values).any() else float("nan")


def build_closure(
    input_path: Path,
    outdir: Path,
    aoi_id: str,
    product_label: str,
    thresholds: list[float],
    max_point_output: int,
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    df = read_points(input_path)
    columns = list(df.columns)
    lon_col = find_column(columns, LON_CANDIDATES, "longitude")
    lat_col = find_column(columns, LAT_CANDIDATES, "latitude")
    vel_col = find_column(columns, VEL_CANDIDATES, "velocity")
    coh_col = optional_column(columns, COH_CANDIDATES)
    amp_col = optional_column(columns, AMP_CANDIDATES)

    work = pd.DataFrame(
        {
            "longitude": pd.to_numeric(df[lon_col], errors="coerce"),
            "latitude": pd.to_numeric(df[lat_col], errors="coerce"),
            "velocity_mm_per_year": pd.to_numeric(df[vel_col], errors="coerce"),
        }
    )
    if coh_col:
        work["temporal_coherence"] = pd.to_numeric(df[coh_col], errors="coerce")
    if amp_col:
        work["amplitude_dispersion"] = pd.to_numeric(df[amp_col], errors="coerce")

    valid_xy = np.isfinite(work["longitude"]) & np.isfinite(work["latitude"])
    work = work.loc[valid_xy].copy()
    work["ghsl_population"] = sample_raster(POP_TIF, work["longitude"].to_numpy(), work["latitude"].to_numpy())
    work["ghsl_builtup"] = sample_raster(BUILT_TIF, work["longitude"].to_numpy(), work["latitude"].to_numpy())
    valid = np.isfinite(work["velocity_mm_per_year"]) & np.isfinite(work["ghsl_population"]) & np.isfinite(work["ghsl_builtup"])
    base = work.loc[valid].copy()

    total_pop = finite_sum(base["ghsl_population"])
    total_built = finite_sum(base["ghsl_builtup"])
    rows: list[dict[str, Any]] = []
    for threshold in thresholds:
        strong = base["velocity_mm_per_year"] <= -abs(threshold)
        control = (base["velocity_mm_per_year"] > -0.5) & (base["velocity_mm_per_year"] < 0.5)
        strong_pop = finite_sum(base.loc[strong, "ghsl_population"])
        strong_built = finite_sum(base.loc[strong, "ghsl_builtup"])
        rows.append(
            {
                "aoi_id": aoi_id,
                "product_label": product_label,
                "threshold_mm_per_year": abs(threshold),
                "n_valid_points": int(len(base)),
                "n_strong_points": int(strong.sum()),
                "n_control_points": int(control.sum()),
                "strong_point_fraction": float(strong.mean()) if len(base) else float("nan"),
                "strong_population": strong_pop,
                "strong_builtup": strong_built,
                "strong_population_share": strong_pop / total_pop if total_pop else float("nan"),
                "strong_builtup_share": strong_built / total_built if total_built else float("nan"),
                "strong_velocity_median": finite_median(base.loc[strong, "velocity_mm_per_year"]),
                "control_velocity_median": finite_median(base.loc[control, "velocity_mm_per_year"]),
                "strong_population_median": finite_median(base.loc[strong, "ghsl_population"]),
                "control_population_median": finite_median(base.loc[control, "ghsl_population"]),
                "strong_builtup_median": finite_median(base.loc[strong, "ghsl_builtup"]),
                "control_builtup_median": finite_median(base.loc[control, "ghsl_builtup"]),
            }
        )

    summary = {
        "aoi_id": aoi_id,
        "product_label": product_label,
        "input_path": str(input_path),
        "n_input_rows": int(len(df)),
        "n_valid_xy_rows": int(len(work)),
        "n_valid_closure_rows": int(len(base)),
        "longitude_column": lon_col,
        "latitude_column": lat_col,
        "velocity_column": vel_col,
        "temporal_coherence_column": coh_col,
        "amplitude_dispersion_column": amp_col,
        "velocity_median": finite_median(base["velocity_mm_per_year"]),
        "velocity_q05": quantile(base["velocity_mm_per_year"], 0.05),
        "velocity_q95": quantile(base["velocity_mm_per_year"], 0.95),
        "total_population_on_valid_egms_points": total_pop,
        "total_builtup_on_valid_egms_points": total_built,
        "bbox": {
            "lon_min": float(np.nanmin(work["longitude"])) if len(work) else float("nan"),
            "lon_max": float(np.nanmax(work["longitude"])) if len(work) else float("nan"),
            "lat_min": float(np.nanmin(work["latitude"])) if len(work) else float("nan"),
            "lat_max": float(np.nanmax(work["latitude"])) if len(work) else float("nan"),
        },
        "thresholds_mm_per_year": thresholds,
        "claim_boundary": (
            "This is an independent EGMS point-support exposure closure. "
            "It validates alternative-product deformation/exposure alignment, but it is not an areal missing-pixel inventory unless a gridded valid-support layer is also supplied."
        ),
    }

    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(outdir / "egms_benchmark_closure_thresholds_v1.csv", rows, fieldnames)
    with (outdir / "egms_benchmark_closure_meta_v1.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)

    point_cols = ["longitude", "latitude", "velocity_mm_per_year", "ghsl_population", "ghsl_builtup"]
    for optional in ["temporal_coherence", "amplitude_dispersion"]:
        if optional in work.columns:
            point_cols.append(optional)
    point_out = work.loc[:, point_cols].head(max_point_output)
    point_out.to_csv(outdir / "egms_benchmark_point_overlay_sample_v1.csv", index=False)

    lines = [
        "# EGMS benchmark closure v1",
        "",
        f"- AOI: `{aoi_id}`",
        f"- Product: `{product_label}`",
        f"- Input rows: `{summary['n_input_rows']}`",
        f"- Valid closure rows: `{summary['n_valid_closure_rows']}`",
        f"- Velocity median: `{summary['velocity_median']:.4f}` mm/yr",
        f"- Velocity q05/q95: `{summary['velocity_q05']:.4f}` / `{summary['velocity_q95']:.4f}` mm/yr",
        "",
        "## Threshold closure",
        "",
        "| threshold mm/yr | strong points | strong population share | strong built-up share | strong velocity median |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {threshold_mm_per_year:.1f} | {n_strong_points} | {strong_population_share:.6f} | {strong_builtup_share:.6f} | {strong_velocity_median:.4f} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            summary["claim_boundary"],
        ]
    )
    (outdir / "egms_benchmark_closure_v1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an EGMS/GHSL independent benchmark closure from a local EGMS point file.")
    parser.add_argument("--input", required=True, type=Path, help="Local EGMS csv or parquet file with lon/lat and velocity columns.")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--aoi-id", default="egms_benchmark")
    parser.add_argument("--product-label", default="EGMS")
    parser.add_argument("--thresholds", default="1,2,5,10", help="Comma-separated positive thresholds in mm/yr.")
    parser.add_argument("--max-point-output", type=int, default=200000, help="Maximum rows to write to the point-overlay sample CSV.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    thresholds = [float(x.strip()) for x in args.thresholds.split(",") if x.strip()]
    build_closure(
        input_path=args.input,
        outdir=args.outdir,
        aoi_id=args.aoi_id,
        product_label=args.product_label,
        thresholds=thresholds,
        max_point_output=args.max_point_output,
    )


if __name__ == "__main__":
    main()
