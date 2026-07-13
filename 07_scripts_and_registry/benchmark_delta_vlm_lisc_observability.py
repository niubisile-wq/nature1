from __future__ import annotations

import csv
import json
import math
import re
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import requests
import tifffile


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _tag_value(tags: dict[str, Any], name: str, default: Any = None) -> Any:
    tag = tags.get(name)
    return default if tag is None else tag.value


def geotiff_tags(path: Path) -> dict[str, Any]:
    with tifffile.TiffFile(path) as tif:
        page = tif.pages[0]
        array = page.asarray().astype(float, copy=False)
        tags = page.tags
        tiepoint = _tag_value(tags, "ModelTiepointTag", (0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        scale = _tag_value(tags, "ModelPixelScaleTag", (1.0, 1.0, 0.0))
        nodata_raw = _tag_value(tags, "GDAL_NODATA", None)
        nodata = float(nodata_raw) if nodata_raw not in (None, "", b"") else np.nan
        tie_lon = float(tiepoint[3])
        tie_lat = float(tiepoint[4])
        pixel_size_x = float(scale[0])
        pixel_size_y = float(scale[1])
        height, width = array.shape[:2]
        return {
            "array": array,
            "width": int(width),
            "height": int(height),
            "tie_lon": tie_lon,
            "tie_lat": tie_lat,
            "pixel_size_x": pixel_size_x,
            "pixel_size_y": pixel_size_y,
            "lon_min": tie_lon,
            "lon_max": tie_lon + width * pixel_size_x,
            "lat_max": tie_lat,
            "lat_min": tie_lat - height * pixel_size_y,
            "nodata": nodata,
            "path": str(path),
        }


def grid_centers(info: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    lon = info["tie_lon"] + (np.arange(info["width"], dtype=float) + 0.5) * info["pixel_size_x"]
    lat = info["tie_lat"] - (np.arange(info["height"], dtype=float) + 0.5) * info["pixel_size_y"]
    return lon, lat


def valid_vlm_mask(info: dict[str, Any]) -> np.ndarray:
    arr = np.asarray(info["array"], dtype=float)
    mask = np.isfinite(arr)
    nodata = info.get("nodata", np.nan)
    if np.isfinite(nodata):
        mask &= arr != nodata
    return mask


def read_download_rows(path: Path, frame_id: str) -> list[dict[str, str]]:
    rows = []
    for row in read_csv(path):
        if row.get("download_status") != "ok":
            continue
        if row.get("frame_id") and row["frame_id"] != frame_id:
            continue
        if "local_path" in row and row["local_path"] and Path(row["local_path"]).exists():
            rows.append(row)
    rows.sort(key=lambda row: row.get("pair", ""))
    return rows


def _sample_nearest(source: dict[str, Any], lon: np.ndarray, lat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    arr = np.asarray(source["array"], dtype=float)
    width = int(source["width"])
    height = int(source["height"])
    x0 = float(source["tie_lon"])
    y0 = float(source["tie_lat"])
    sx = float(source["pixel_size_x"])
    sy = float(source["pixel_size_y"])

    out = np.full((len(lat), len(lon)), np.nan, dtype=float)
    inside = np.zeros_like(out, dtype=bool)
    for r, y in enumerate(lat):
        rr = int(math.floor((y0 - float(y)) / sy))
        for c, x in enumerate(lon):
            cc = int(math.floor((float(x) - x0) / sx))
            if 0 <= rr < height and 0 <= cc < width:
                out[r, c] = float(arr[rr, cc])
                inside[r, c] = True
    return out, inside


def sample_to_target(source: dict[str, Any], target: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    lon, lat = grid_centers(target)
    return _sample_nearest(source, lon, lat)


def observable_stack(
    download_rows: list[dict[str, str]],
    lon: np.ndarray,
    lat: np.ndarray,
    threshold: float,
) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]]]:
    count = np.zeros((len(lat), len(lon)), dtype=int)
    inside_any = np.zeros_like(count, dtype=bool)
    pair_rows: list[dict[str, Any]] = []
    for row in download_rows:
        local_path = Path(row["local_path"])
        source = geotiff_tags(local_path)
        sample, inside = _sample_nearest(source, lon, lat)
        obs = inside & np.isfinite(sample) & (sample >= threshold)
        count += obs.astype(int)
        inside_any |= inside
        pair_rows.append(
            {
                "pair": row.get("pair", ""),
                "local_path": str(local_path),
                "observable_cells": int(obs.sum()),
                "inside_cells": int(inside.sum()),
            }
        )
    return count, inside_any, pair_rows


def slugify_delta(delta: str) -> str:
    value = delta.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def fetch_zenodo_record(record_id: str | int) -> dict[str, Any]:
    url = f"https://zenodo.org/api/records/{record_id}"
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    return response.json()


def download_grid_zip(url: str, out_path: Path) -> Path:
    response = requests.get(url, timeout=240, stream=True)
    response.raise_for_status()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as fh:
        for chunk in response.iter_content(chunk_size=1 << 20):
            if chunk:
                fh.write(chunk)
    return out_path


def extract_delta_tif(grid_zip: Path, delta: str, outdir: Path) -> tuple[Path, list[str]]:
    outdir.mkdir(parents=True, exist_ok=True)
    wanted = slugify_delta(delta)
    with zipfile.ZipFile(grid_zip, "r") as zf:
        members = [name for name in zf.namelist() if wanted in Path(name).stem.lower() and Path(name).suffix.lower() in {".tif", ".tiff"}]
        if not members:
            raise FileNotFoundError(f"no tif member matched delta {delta} in {grid_zip}")
        member = members[0]
        zf.extract(member, path=outdir)
        extracted = outdir / member
        return extracted, members
