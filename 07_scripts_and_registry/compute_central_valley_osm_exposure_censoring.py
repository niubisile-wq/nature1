from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from benchmark_delta_vlm_lisc_observability import grid_centers as vlm_grid_centers


def add_length(item: dict[str, float], key: str, value: float) -> None:
    item[key] = float(item.get(key, 0.0) + float(value))


def cell_index(vlm: dict[str, Any], lon: float, lat: float) -> tuple[int, int] | None:
    x0 = float(vlm["tie_lon"])
    y0 = float(vlm["tie_lat"])
    sx = float(vlm["pixel_size_x"])
    sy = float(vlm["pixel_size_y"])
    col = int(math.floor((float(lon) - x0) / sx))
    row = int(math.floor((y0 - float(lat)) / sy))
    if 0 <= row < int(vlm["height"]) and 0 <= col < int(vlm["width"]):
        return row, col
    return None


def exposure_category(tags: dict[str, Any]) -> str | None:
    if "railway" in tags:
        return "railway"
    highway = str(tags.get("highway", "")).lower()
    if highway:
        return "major_road"
    return None


def init_stats() -> dict[str, float]:
    return defaultdict(float)


def length_km(coords: Iterable[tuple[float, float]]) -> float:
    pts = list(coords)
    if len(pts) < 2:
        return 0.0
    total = 0.0
    for (lon1, lat1), (lon2, lat2) in zip(pts[:-1], pts[1:]):
        dx = math.radians(float(lon2) - float(lon1))
        dy = math.radians(float(lat2) - float(lat1))
        a = math.sin(dy / 2) ** 2 + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(dx / 2) ** 2
        total += 2.0 * 6371.0 * math.asin(min(1.0, math.sqrt(a)))
    return float(total)


def iter_segment_midpoints(coords: list[tuple[float, float]], pixel_size_x: float, pixel_size_y: float) -> Iterable[tuple[float, float, float]]:
    if len(coords) < 2:
        return []
    step = max(float(pixel_size_x), float(pixel_size_y), 1e-9)
    for (lon1, lat1), (lon2, lat2) in zip(coords[:-1], coords[1:]):
        seg_len = length_km([(lon1, lat1), (lon2, lat2)])
        n = max(1, int(math.ceil((seg_len * 1000.0) / step)))
        for i in range(n):
            t = (i + 0.5) / n
            yield (
                float(lon1 + (lon2 - lon1) * t),
                float(lat1 + (lat2 - lat1) * t),
                float(seg_len / n),
            )


def summarize_osm(payload: dict[str, Any], vlm: dict[str, Any], masks_by_pair: dict[str, dict[str, np.ndarray]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    stats: dict[tuple[str, str], dict[str, float]] = defaultdict(init_stats)
    way_counts: dict[str, int] = defaultdict(int)
    highway_values: dict[str, int] = defaultdict(int)
    railway_values: dict[str, int] = defaultdict(int)
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
        for seg_lon, seg_lat, km in iter_segment_midpoints(coords, vlm["pixel_size_x"], vlm["pixel_size_y"]):
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
        for seg_lon, seg_lat, km in iter_segment_midpoints(coords, vlm["pixel_size_x"], vlm["pixel_size_y"]):
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
