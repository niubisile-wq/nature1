from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import tifffile

def geotiff_tags(path: Path) -> dict[str, Any]:
    with tifffile.TiffFile(path) as tf:
        page = tf.pages[0]
        tags = page.tags
        tiepoint = tags.get("ModelTiepointTag")
        scale = tags.get("ModelPixelScaleTag")
        nodata_tag = tags.get("GDAL_NODATA")
        tiepoint_value = tiepoint.value if tiepoint is not None else (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        scale_value = scale.value if scale is not None else (1.0, 1.0, 0.0)
        nodata_raw = nodata_tag.value if nodata_tag is not None else None
        nodata = float(nodata_raw) if nodata_raw not in (None, "", b"") else np.nan
        width = int(page.imagewidth)
        height = int(page.imagelength)
        return {
            "path": str(path),
            "width": width,
            "height": height,
            "tie_lon": float(tiepoint_value[3]),
            "tie_lat": float(tiepoint_value[4]),
            "pixel_size_x": float(scale_value[0]),
            "pixel_size_y": float(scale_value[1]),
            "lon_min": float(tiepoint_value[3]),
            "lon_max": float(tiepoint_value[3] + width * scale_value[0]),
            "lat_max": float(tiepoint_value[4]),
            "lat_min": float(tiepoint_value[4] - height * scale_value[1]),
            "nodata": nodata,
            "tilewidth": int(getattr(page, "tilewidth", width)),
            "tilelength": int(getattr(page, "tilelength", height)),
        }


def _decode_window_from_tiled_tiff(path: Path, window: tuple[int, int, int, int]) -> np.ndarray:
    row0, row1, col0, col1 = window
    with tifffile.TiffFile(path) as tf:
        page = tf.pages[0]
        height = int(page.imagelength)
        width = int(page.imagewidth)
        tile_w = int(getattr(page, "tilewidth", width))
        tile_h = int(getattr(page, "tilelength", height))
        tiles_x = math.ceil(width / tile_w)
        out = np.full((row1 - row0, col1 - col0), np.nan, dtype=float)
        fh = tf.filehandle
        for tile_row in range(row0 // tile_h, (row1 - 1) // tile_h + 1):
            for tile_col in range(col0 // tile_w, (col1 - 1) // tile_w + 1):
                tile_index = tile_row * tiles_x + tile_col
                if tile_index >= len(page.dataoffsets):
                    continue
                offset = int(page.dataoffsets[tile_index])
                bytecount = int(page.databytecounts[tile_index])
                fh.seek(offset)
                raw = fh.read(bytecount)
                decoded = page.decode(raw, tile_index)
                tile = np.squeeze(decoded[0]).astype(float, copy=False)
                tile_r0 = tile_row * tile_h
                tile_c0 = tile_col * tile_w
                tile_r1 = min(tile_r0 + tile.shape[0], height)
                tile_c1 = min(tile_c0 + tile.shape[1], width)
                inter_r0 = max(row0, tile_r0)
                inter_r1 = min(row1, tile_r1)
                inter_c0 = max(col0, tile_c0)
                inter_c1 = min(col1, tile_c1)
                if inter_r1 <= inter_r0 or inter_c1 <= inter_c0:
                    continue
                src_r0 = inter_r0 - tile_r0
                src_r1 = src_r0 + (inter_r1 - inter_r0)
                src_c0 = inter_c0 - tile_c0
                src_c1 = src_c0 + (inter_c1 - inter_c0)
                dst_r0 = inter_r0 - row0
                dst_r1 = dst_r0 + (inter_r1 - inter_r0)
                dst_c0 = inter_c0 - col0
                dst_c1 = dst_c0 + (inter_c1 - inter_c0)
                out[dst_r0:dst_r1, dst_c0:dst_c1] = tile[src_r0:src_r1, src_c0:src_c1]
        return out


def bbox_window(info: dict[str, Any], bbox: dict[str, float]) -> tuple[int, int, int, int]:
    x0 = float(info["tie_lon"])
    y0 = float(info["tie_lat"])
    sx = float(info["pixel_size_x"])
    sy = float(info["pixel_size_y"])
    width = int(info["width"])
    height = int(info["height"])
    col0 = max(0, int(math.floor((bbox["lon_min"] - x0) / sx)))
    col1 = min(width, int(math.ceil((bbox["lon_max"] - x0) / sx)))
    row0 = max(0, int(math.floor((y0 - bbox["lat_max"]) / sy)))
    row1 = min(height, int(math.ceil((y0 - bbox["lat_min"]) / sy)))
    return row0, row1, col0, col1


def read_population_crop(path: Path, window: tuple[int, int, int, int]) -> np.ndarray:
    return _decode_window_from_tiled_tiff(path, window)


def sample_array_at_centers(source: dict[str, Any], lon: np.ndarray, lat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
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
