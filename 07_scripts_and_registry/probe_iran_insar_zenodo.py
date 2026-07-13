from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import requests
import tifffile


DEFAULT_RECORD_API = "https://zenodo.org/api/records/10815578"
DEFAULT_OUTDIR = Path(r"C:\Users\刘子轩\radar_outputs\iran_insar_zenodo_probe")


def download_json(url: str, path: Path, timeout: int) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "nature-radar-iran-insar-probe/0.1"})
    response.raise_for_status()
    path.write_text(response.text, encoding="utf-8")
    return response.json()


def download_file(url: str, out_path: Path, timeout: int) -> dict[str, Any]:
    if out_path.exists() and out_path.stat().st_size > 0:
        return {"status": "cached", "path": str(out_path), "bytes": out_path.stat().st_size}
    with requests.get(url, stream=True, timeout=timeout, headers={"User-Agent": "nature-radar-iran-insar-probe/0.1"}) as response:
        response.raise_for_status()
        with out_path.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)
    return {"status": "downloaded", "path": str(out_path), "bytes": out_path.stat().st_size}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def finite_stats(arr: np.ndarray, nodata: float | None = None) -> dict[str, Any]:
    values = arr.astype(float, copy=False)
    values = values[np.isfinite(values)]
    values = values[(values > -1.0e20) & (values < 1.0e20)]
    if nodata is not None and np.isfinite(nodata):
        values = values[values != nodata]
    if values.size == 0:
        return {"finite_count": 0}
    return {
        "finite_count": int(values.size),
        "min": float(np.nanmin(values)),
        "p05": float(np.nanpercentile(values, 5)),
        "p25": float(np.nanpercentile(values, 25)),
        "median": float(np.nanpercentile(values, 50)),
        "mean": float(np.nanmean(values)),
        "p75": float(np.nanpercentile(values, 75)),
        "p95": float(np.nanpercentile(values, 95)),
        "max": float(np.nanmax(values)),
        "fraction_lt_minus_5": float(np.mean(values < -5.0)),
        "fraction_lt_minus_10": float(np.mean(values < -10.0)),
    }


def inspect_tif(path: Path) -> dict[str, Any]:
    with tifffile.TiffFile(path) as tif:
        page = tif.pages[0]
        arr = page.asarray()
        tags = {tag.name: tag.value for tag in page.tags.values() if tag.name in {"ImageWidth", "ImageLength", "ModelPixelScaleTag", "ModelTiepointTag", "GeoKeyDirectoryTag", "GDAL_NODATA"}}
    nodata = None
    if "GDAL_NODATA" in tags:
        try:
            nodata = float(tags["GDAL_NODATA"])
        except Exception:
            nodata = None
    summary = {
        "path": str(path),
        "shape": list(arr.shape),
        "dtype": str(arr.dtype),
        "tags": tags,
        "stats": finite_stats(arr, nodata),
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and inspect the Iran nationwide InSAR Zenodo dataset.")
    parser.add_argument("--record-api", default=DEFAULT_RECORD_API)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--download-all", action="store_true", default=True)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    record = download_json(args.record_api, args.outdir / "zenodo_10815578.json", args.timeout)
    files = record.get("files", [])
    file_rows = []
    downloads = []
    inspections = []
    for item in files:
        key = item.get("key", "")
        size = int(item.get("size") or 0)
        url = item.get("links", {}).get("self") or item.get("links", {}).get("download")
        file_rows.append({"key": key, "size": size, "size_mb": f"{size / 1024 / 1024:.3f}", "url": url})
        if not key or not url:
            continue
        out_path = args.outdir / key
        downloads.append(download_file(url, out_path, args.timeout))
        if out_path.suffix.lower() in {".tif", ".tiff"}:
            try:
                inspections.append(inspect_tif(out_path))
            except Exception as exc:
                inspections.append(
                    {
                        "path": str(out_path),
                        "shape": [],
                        "dtype": "",
                        "tags": {},
                        "stats": {},
                        "read_error": f"{type(exc).__name__}: {exc}",
                    }
                )

    write_csv(args.outdir / "iran_zenodo_files.csv", file_rows, ["key", "size", "size_mb", "url"])
    (args.outdir / "download_results.json").write_text(json.dumps(downloads, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.outdir / "tif_inspection.json").write_text(json.dumps(inspections, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Iran nationwide InSAR Zenodo probe",
        "",
        f"Title: {record.get('title', '')}",
        f"DOI: {record.get('doi', '')}",
        f"Files: `{len(files)}`",
        "",
        "## Files",
        "",
        "| File | Size MB |",
        "|---|---:|",
    ]
    for row in file_rows:
        lines.append(f"| {row['key']} | {row['size_mb']} |")
    lines.extend(["", "## GeoTIFF inspections", ""])
    for item in inspections:
        stats = item.get("stats", {})
        if item.get("read_error"):
            lines.append(f"- `{Path(item['path']).name}`: read error `{item['read_error']}`")
        else:
            lines.append(
                f"- `{Path(item['path']).name}`: shape `{item['shape']}`, median `{stats.get('median', '')}`, "
                f"fraction < -5 `{stats.get('fraction_lt_minus_5', '')}`"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is a strict no-token, high-impact companion dataset. It can support a no-token arid-groundwater benchmark extension, but it is still a processed InSAR product rather than an independent truth layer.",
        ]
    )
    (args.outdir / "iran_insar_zenodo_probe_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote Iran InSAR probe to {args.outdir}")
    print(f"Files: {len(files)}")


if __name__ == "__main__":
    main()
