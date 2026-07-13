from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import requests

from compute_central_valley_osm_exposure_censoring import (
    add_length,
    cell_index,
    exposure_category,
    init_stats,
    iter_segment_midpoints,
    length_km,
    summarize_osm,
)
from benchmark_delta_vlm_lisc_observability import (
    geotiff_tags as vlm_geotiff_tags,
    grid_centers as vlm_grid_centers,
    read_download_rows,
    valid_vlm_mask,
    write_csv,
)
from simulate_lisc_observability_censoring import coherence_array, geotiff_info, sample_to_target


CHAO_PHRAYA_FRAME_ID = "062D_07629_131313"
CHAO_PHRAYA_BBOX = {
    "south": 13.8,
    "west": 99.0,
    "north": 15.6,
    "east": 101.0,
}

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
]

DEFAULT_VLM_TIF = (
    Path.home() / "radar_outputs"
    / "delta_binomial_with_worldcover_main"
    / "chao_phraya"
    / "gridVLM"
    / "chaoPhraya_vlm.tif"
)
DEFAULT_CC_DOWNLOADS = Path.home() / "radar_outputs" / "chao_phraya_lisc_ghsl_exposure_observability" / "frame_ghsl_exposure_downloads.csv"


def build_overpass_query() -> str:
    south = CHAO_PHRAYA_BBOX["south"]
    west = CHAO_PHRAYA_BBOX["west"]
    north = CHAO_PHRAYA_BBOX["north"]
    east = CHAO_PHRAYA_BBOX["east"]
    return f"""
[out:json][timeout:180];
(
  way["highway"~"^(motorway|trunk|primary|secondary|tertiary)$"]({south},{west},{north},{east});
  way["railway"~"^(rail|light_rail)$"]({south},{west},{north},{east});
);
out tags geom;
""".strip()


def iter_segment_midpoints_screened(
    coords: list[tuple[float, float]],
    _pixel_size_x: float,
    _pixel_size_y: float,
    _sample_factor: float,
) -> Iterable[tuple[float, float, float]]:
    if len(coords) < 2:
        return []
    for (lon1, lat1), (lon2, lat2) in zip(coords[:-1], coords[1:]):
        seg_len = length_km([(lon1, lat1), (lon2, lat2)])
        yield (
            float((lon1 + lon2) / 2.0),
            float((lat1 + lat2) / 2.0),
            float(seg_len),
        )


def fetch_overpass(cache_path: Path, refresh: bool = False) -> dict[str, Any]:
    if cache_path.exists() and not refresh:
        return json.loads(cache_path.read_text(encoding="utf-8"))
    query = build_overpass_query()
    last_error = None
    headers = {"User-Agent": "nature-radar-noauth-scout/0.1"}
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            response = requests.post(endpoint, data={"data": query}, headers=headers, timeout=240)
            response.raise_for_status()
            payload = response.json()
            if payload.get("elements"):
                payload["_query_endpoint"] = endpoint
                payload["_query"] = query
                cache_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
                return payload
            last_error = RuntimeError(f"{endpoint} returned no elements")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise RuntimeError(f"all Overpass endpoints failed: {last_error}")


def summarize_osm(
    payload: dict[str, Any],
    vlm: dict[str, Any],
    masks_by_pair: dict[str, dict[str, np.ndarray]],
    sample_factor: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    stats: dict[tuple[str, str], dict[str, float]] = defaultdict(init_stats)
    way_counts: Counter[str] = Counter()
    highway_values: Counter[str] = Counter()
    railway_values: Counter[str] = Counter()
    segment_count = 0
    used_segment_count = 0
    valid_mask = next(iter(masks_by_pair.values()))["valid"]
    lon, lat = vlm_grid_centers(vlm)
    for element in payload.get("elements", []):
        if element.get("type") != "way" or "geometry" not in element:
            continue
        tags = element.get("tags", {})
        category = exposure_category(tags)
        if category is None:
            continue
        way_counts[category] += 1
        if "highway" in tags:
            highway_values[str(tags["highway"])] += 1
        if "railway" in tags:
            railway_values[str(tags["railway"])] += 1
        coords = [(float(point["lon"]), float(point["lat"])) for point in element["geometry"]]
        categories = [category, "transport_total"]
        for seg_lon, seg_lat, km in iter_segment_midpoints_screened(
            coords,
            vlm["pixel_size_x"],
            vlm["pixel_size_y"],
            sample_factor,
        ):
            segment_count += 1
            idx = cell_index(vlm, seg_lon, seg_lat)
            if idx is None:
                continue
            row, col = idx
            if not bool(valid_mask[row, col]):
                continue
            used_segment_count += 1
            for pair, masks in masks_by_pair.items():
                observable = bool(masks["observable"][row, col])
                for cat in categories:
                    item = stats[(pair, cat)]
                    add_length(item, "transport_km_valid", km)
                    if not observable:
                        add_length(item, "transport_km_hidden_strong_subsidence", 0.0)
                    if cat in {"major_road", "railway", "transport_total"}:
                        pass
    # Re-run with actual displacement thresholds in a second pass to keep code explicit.
    dwr_arr = vlm["array"].astype(float, copy=False)
    strong = valid_mask & (dwr_arr <= -5.0)
    for element in payload.get("elements", []):
        if element.get("type") != "way" or "geometry" not in element:
            continue
        tags = element.get("tags", {})
        category = exposure_category(tags)
        if category is None:
            continue
        coords = [(float(point["lon"]), float(point["lat"])) for point in element["geometry"]]
        categories = [category, "transport_total"]
        for seg_lon, seg_lat, km in iter_segment_midpoints_screened(
            coords,
            vlm["pixel_size_x"],
            vlm["pixel_size_y"],
            sample_factor,
        ):
            idx = cell_index(vlm, seg_lon, seg_lat)
            if idx is None:
                continue
            row, col = idx
            if not bool(valid_mask[row, col]):
                continue
            for pair, masks in masks_by_pair.items():
                observable = bool(masks["observable"][row, col])
                for cat in categories:
                    item = stats[(pair, cat)]
                    if strong[row, col]:
                        add_length(item, "transport_km_strong_subsidence", km)
                        if not observable:
                            add_length(item, "transport_km_hidden_strong_subsidence", km)
    rows: list[dict[str, Any]] = []
    for (pair, category), item in sorted(stats.items()):
        strong_km = item["transport_km_strong_subsidence"]
        hidden_strong = item["transport_km_hidden_strong_subsidence"]
        rows.append(
            {
                "pair": pair,
                "exposure_category": category,
                "transport_km_valid": item["transport_km_valid"],
                "transport_km_strong_subsidence": strong_km,
                "transport_km_hidden_strong_subsidence": hidden_strong,
                "hidden_strong_subsidence_transport_fraction": hidden_strong / strong_km if strong_km else 0.0,
            }
        )
    meta = {
        "overpass_endpoint": payload.get("_query_endpoint", ""),
        "osm_way_count_by_category": dict(way_counts),
        "osm_highway_values": dict(highway_values),
        "osm_railway_values": dict(railway_values),
        "segment_count": segment_count,
        "used_segment_count": used_segment_count,
    }
    return rows, meta


def write_markdown(path: Path, rows: list[dict[str, Any]], meta: dict[str, Any], threshold: float) -> None:
    total_rows = [row for row in rows if row["exposure_category"] == "transport_total"]
    lines = [
        "# Chao Phraya OSM transport exposure censoring",
        "",
        "This prototype uses no-auth OpenStreetMap Overpass data for major roads and railways.",
        "It estimates transport-infrastructure exposure that falls on Chao Phraya strong-subsidence pixels but is hidden by LiCSAR coherence censoring.",
        "",
        f"- Coherence observability threshold: `{threshold}`",
        f"- Overpass endpoint: `{meta.get('overpass_endpoint', '')}`",
        f"- OSM way counts: `{json.dumps(meta.get('osm_way_count_by_category', {}), ensure_ascii=False)}`",
        f"- Segments tested / used: `{meta.get('segment_count', 0)}` / `{meta.get('used_segment_count', 0)}`",
        "",
        "| pair | exposed transport on strong subsidence (km) | hidden strong-subsidence transport (km) | hidden fraction |",
        "|---|---:|---:|---:|",
    ]
    for row in total_rows:
        lines.append(
            f"| {row['pair']} | {row['transport_km_strong_subsidence']:.2f} | "
            f"{row['transport_km_hidden_strong_subsidence']:.2f} | "
            f"{row['hidden_strong_subsidence_transport_fraction']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is an exposure-censoring estimate, not an asset-level engineering risk model.",
            "- Road and railway lengths are assigned to the VLM grid by one midpoint per original OSM way segment.",
            "- The result is a minimum infrastructure-exposure layer for testing whether LiCSAR observability censoring affects risk estimates, not just area estimates.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vlm-tif", type=Path, default=DEFAULT_VLM_TIF)
    parser.add_argument("--cc-downloads", type=Path, default=DEFAULT_CC_DOWNLOADS)
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--sample-factor", type=float, default=1.0)
    parser.add_argument("--refresh-osm", action="store_true")
    parser.add_argument("--outdir", type=Path, default=Path("radar_outputs") / "chao_phraya_osm_exposure_censoring")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    payload = fetch_overpass(args.outdir / "osm_major_transport_overpass.json", refresh=args.refresh_osm)
    vlm = vlm_geotiff_tags(args.vlm_tif)
    vlm["array"] = vlm["array"].astype(float, copy=True) * 10.0
    valid = valid_vlm_mask(vlm)
    samples = read_download_rows(args.cc_downloads, CHAO_PHRAYA_FRAME_ID)
    masks_by_pair = {}
    for sample in samples:
        cc_info = geotiff_info(Path(sample["local_path"]))
        cc_sample, inside = sample_to_target(cc_info, vlm)
        cc = coherence_array(cc_sample)
        observable = valid & inside & np.isfinite(cc) & (cc >= args.threshold)
        masks_by_pair[sample["pair"]] = {"valid": valid, "observable": observable}
    rows, meta = summarize_osm(payload, vlm, masks_by_pair, args.sample_factor)
    meta["coherence_threshold"] = args.threshold
    meta["sample_factor"] = args.sample_factor
    write_csv(
        args.outdir / "chao_phraya_osm_exposure_censoring_summary.csv",
        rows,
        [
            "pair",
            "exposure_category",
            "transport_km_valid",
            "transport_km_strong_subsidence",
            "transport_km_hidden_strong_subsidence",
            "hidden_strong_subsidence_transport_fraction",
        ],
    )
    (args.outdir / "chao_phraya_osm_exposure_censoring_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(args.outdir / "chao_phraya_osm_exposure_censoring_report.md", rows, meta, args.threshold)
    print(json.dumps({"rows": len(rows), "meta": meta, "outdir": str(args.outdir)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
