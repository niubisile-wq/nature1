from __future__ import annotations

import argparse
import csv
import json
import math
import tempfile
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import h5py
import requests


DEFAULT_METADATA = Path(r"C:\Users\刘子轩\radar_outputs\rescue_dataset_probe\zenodo.org_api_records_4243151")
DEFAULT_OUTDIR = Path(r"C:\Users\刘子轩\radar_outputs\japan_licsbas_selected_probe")


def read_metadata(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_files(files: list[dict[str, Any]], city: str, max_size_mb: float, limit: int) -> list[dict[str, Any]]:
    city_lower = city.lower()
    max_bytes = int(max_size_mb * 1024 * 1024)
    matches = []
    for item in files:
        key = item.get("key", "")
        size = int(item.get("size") or 0)
        if city_lower in key.lower() and size <= max_bytes:
            matches.append(item)
    matches.sort(key=lambda x: int(x.get("size") or 0))
    return matches[:limit]


def download_file(url: str, out_path: Path, timeout: int) -> dict[str, Any]:
    if out_path.exists() and out_path.stat().st_size > 0:
        return {"status": "cached", "path": str(out_path), "bytes": out_path.stat().st_size}
    headers = {"User-Agent": "nature-radar-japan-licsbas-probe/0.1"}
    with requests.get(url, stream=True, timeout=timeout, headers=headers) as response:
        response.raise_for_status()
        with out_path.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)
    return {"status": "downloaded", "path": str(out_path), "bytes": out_path.stat().st_size}


def inspect_zip(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as zf:
        infos = zf.infolist()
        suffixes = Counter(Path(info.filename).suffix.lower() or "[no_suffix]" for info in infos if not info.is_dir())
        top_dirs = Counter(info.filename.split("/", 1)[0] for info in infos if info.filename)
        largest = sorted(
            [
                {
                    "filename": info.filename,
                    "size": info.file_size,
                    "compressed_size": info.compress_size,
                }
                for info in infos
                if not info.is_dir()
            ],
            key=lambda x: int(x["size"]),
            reverse=True,
        )[:20]
    return {
        "zip": str(path),
        "n_members": len(infos),
        "n_files": sum(1 for info in infos if not info.is_dir()),
        "suffix_counts": dict(suffixes),
        "top_dirs": dict(top_dirs),
        "largest_files": largest,
        "has_geotiff": any(suf in suffixes for suf in [".tif", ".tiff"]),
        "has_text_metadata": any(suf in suffixes for suf in [".txt", ".csv", ".json", ".xml", ".rsc", ".par"]),
    }


def numeric_stats(values: Any) -> dict[str, Any]:
    flat = []
    for value in values.ravel():
        number = float(value)
        if math.isfinite(number):
            flat.append(number)
    if not flat:
        return {"finite_count": 0}
    flat.sort()
    n = len(flat)

    def q(frac: float) -> float:
        idx = min(n - 1, max(0, int(round(frac * (n - 1)))))
        return flat[idx]

    return {
        "finite_count": n,
        "min": flat[0],
        "p05": q(0.05),
        "p25": q(0.25),
        "median": q(0.50),
        "mean": sum(flat) / n,
        "p75": q(0.75),
        "p95": q(0.95),
        "max": flat[-1],
        "fraction_lt_minus_5": sum(1 for x in flat if x < -5.0) / n,
        "fraction_lt_minus_10": sum(1 for x in flat if x < -10.0) / n,
    }


def inspect_h5_payloads(zip_path: Path) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    with zipfile.ZipFile(zip_path) as zf:
        h5_names = [name for name in zf.namelist() if name.endswith(".h5")]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            for name in h5_names:
                h5_path = tmp / Path(name).name
                h5_path.write_bytes(zf.read(name))
                with h5py.File(h5_path, "r") as h5:
                    vel = h5["vel"][()]
                    height, width = vel.shape
                    corner_lon = float(h5["corner_lon"][()])
                    corner_lat = float(h5["corner_lat"][()])
                    post_lon = float(h5["post_lon"][()])
                    post_lat = float(h5["post_lat"][()])
                    lon2 = corner_lon + post_lon * (width - 1)
                    lat2 = corner_lat + post_lat * (height - 1)
                    imdates = h5["imdates"][()]
                    summary = {
                        "zip": str(zip_path),
                        "h5_member": name,
                        "shape_yx": [int(height), int(width)],
                        "n_time_steps": int(len(imdates)),
                        "date_start": str(int(imdates.min())) if len(imdates) else "",
                        "date_end": str(int(imdates.max())) if len(imdates) else "",
                        "bbox_wgs84": {
                            "lon_min": min(corner_lon, lon2),
                            "lon_max": max(corner_lon, lon2),
                            "lat_min": min(corner_lat, lat2),
                            "lat_max": max(corner_lat, lat2),
                        },
                        "post_lon": post_lon,
                        "post_lat": post_lat,
                        "velocity_stats": numeric_stats(vel),
                        "velocity_unit_note": "LiCSBAS velocity convention; verify unit in source paper before manuscript claims.",
                    }
                    summaries.append(summary)
    return summaries


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, metadata: dict[str, Any], selected: list[dict[str, Any]], downloads: list[dict[str, Any]], inspections: list[dict[str, Any]]) -> None:
    lines = [
        "# Japan LiCSBAS selective probe",
        "",
        f"Record: {metadata.get('title', '')}",
        f"DOI: {metadata.get('doi', '')}",
        f"Files in record: `{len(metadata.get('files', []))}`",
        "",
        "## Selected files",
        "",
        "| File | Size MB | Status | Has GeoTIFF | Files |",
        "|---|---:|---|---|---:|",
    ]
    by_path = {Path(item["path"]).name: item for item in downloads}
    by_zip = {Path(item["zip"]).name: item for item in inspections}
    for item in selected:
        key = item.get("key", "")
        download = by_path.get(key, {})
        inspect = by_zip.get(key, {})
        size_mb = int(item.get("size") or 0) / 1024 / 1024
        lines.append(
            f"| {key} | {size_mb:.1f} | {download.get('status', '')} | "
            f"{inspect.get('has_geotiff', '')} | {inspect.get('n_files', '')} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This probe checks whether the Japan LiCSBAS Zenodo record can be selectively ingested without downloading the full 28.7 GB archive.",
            "A successful small-city download gives the benchmark pipeline a non-US/non-Europe public deformation-product extension, but it is still LiCSAR/LiCSBAS-derived and therefore not an independent truth layer.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Selectively download and inspect small Japan LiCSBAS Zenodo zip files.")
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--city", default="Niigata")
    parser.add_argument("--max-size-mb", type=float, default=180.0)
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--no-download", action="store_true")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    metadata = read_metadata(args.metadata)
    selected = select_files(metadata.get("files", []), args.city, args.max_size_mb, args.limit)
    selected_rows = [
        {
            "key": item.get("key", ""),
            "size": item.get("size", ""),
            "size_mb": f"{int(item.get('size') or 0) / 1024 / 1024:.3f}",
            "download_url": item.get("links", {}).get("self") or item.get("links", {}).get("download") or "",
        }
        for item in selected
    ]
    write_csv(args.outdir / "selected_files.csv", selected_rows, ["key", "size", "size_mb", "download_url"])

    downloads: list[dict[str, Any]] = []
    inspections: list[dict[str, Any]] = []
    h5_summaries: list[dict[str, Any]] = []
    for item in selected:
        key = item.get("key", "")
        url = item.get("links", {}).get("self") or item.get("links", {}).get("download")
        if not key or not url:
            continue
        out_path = args.outdir / key
        if args.no_download:
            downloads.append({"status": "not_downloaded", "path": str(out_path), "bytes": ""})
            continue
        downloads.append(download_file(url, out_path, args.timeout))
        inspections.append(inspect_zip(out_path))
        h5_summaries.extend(inspect_h5_payloads(out_path))

    (args.outdir / "download_results.json").write_text(json.dumps(downloads, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.outdir / "zip_inspection.json").write_text(json.dumps(inspections, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.outdir / "h5_velocity_summary.json").write_text(json.dumps(h5_summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(args.outdir / "japan_licsbas_selected_probe_report.md", metadata, selected, downloads, inspections)
    print(f"Selected files: {len(selected)}")
    print(f"Wrote Japan LiCSBAS probe to {args.outdir}")


if __name__ == "__main__":
    main()
