from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TARGETS = [
    ("po_delta_core", "l3_ortho_up", [11.7, 44.35, 12.9, 45.55]),
    ("po_venice_broad", "l3_ortho_up", [10.0, 44.0, 13.0, 46.0]),
    ("rhone_delta_core", "l3_ortho_up", [4.0, 43.2, 5.15, 44.05]),
]

READABLE_SUFFIXES = {".csv", ".parquet", ".pq", ".gz"}
ARCHIVE_SUFFIXES = {".zip", ".gpkg", ".geojson", ".json"}
COORD_HINTS = {"lon", "longitude", "x", "lat", "latitude", "y", "easting", "northing", "geometry"}
VEL_HINTS = {"velocity", "mean_velocity", "vel", "v", "up", "vu", "mean_vel", "deformation"}
PLACEHOLDER_NAMES = {"DOWNLOAD_HERE.txt"}


def sniff_csv_header(path: Path) -> list[str]:
    opener = path.open
    if path.suffix.lower() == ".gz":
        import gzip

        opener = gzip.open
    with opener(path, "rt", encoding="utf-8", errors="replace", newline="") as handle:
        sample = handle.read(8192)
    dialect = csv.Sniffer().sniff(sample)
    reader = csv.reader(sample.splitlines(), dialect)
    return next(reader, [])


def inspect_file(path: Path) -> dict:
    suffix = path.suffix.lower()
    info = {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "suffix": suffix,
        "status": "needs_conversion" if suffix in ARCHIVE_SUFFIXES else "candidate",
        "header": [],
        "coord_hint_columns": [],
        "velocity_hint_columns": [],
        "note": "",
    }
    if path.name in PLACEHOLDER_NAMES:
        info["status"] = "placeholder"
        info["note"] = "Instruction file only; replace by adding a downloaded EGMS point product in the same folder."
        return info
    if suffix in {".csv", ".gz"}:
        try:
            header = sniff_csv_header(path)
        except Exception as exc:
            info["status"] = "unreadable"
            info["note"] = f"CSV header read failed: {exc}"
            return info
        lower_map = {col: col.strip().lower() for col in header}
        info["header"] = header[:80]
        info["coord_hint_columns"] = [col for col, low in lower_map.items() if any(h in low for h in COORD_HINTS)]
        info["velocity_hint_columns"] = [col for col, low in lower_map.items() if any(h in low for h in VEL_HINTS)]
        if not info["coord_hint_columns"] or not info["velocity_hint_columns"]:
            info["status"] = "inspect_columns"
            info["note"] = "Header is readable, but coordinate or velocity columns need manual confirmation."
    elif suffix in {".parquet", ".pq"}:
        try:
            try:
                import pyarrow.parquet as pq

                columns = list(pq.ParquetFile(path).schema.names)
            except ImportError:
                import pandas as pd

                columns = list(pd.read_parquet(path, columns=[]).columns)
        except Exception as exc:
            info["status"] = "unreadable"
            info["note"] = f"Parquet schema read failed: {exc}"
            return info
        lower_map = {col: col.strip().lower() for col in columns}
        info["header"] = columns[:80]
        info["coord_hint_columns"] = [col for col, low in lower_map.items() if any(h in low for h in COORD_HINTS)]
        info["velocity_hint_columns"] = [col for col, low in lower_map.items() if any(h in low for h in VEL_HINTS)]
        if not info["coord_hint_columns"] or not info["velocity_hint_columns"]:
            info["status"] = "inspect_columns"
            info["note"] = "Schema is readable, but coordinate or velocity columns need manual confirmation."
    elif suffix not in ARCHIVE_SUFFIXES:
        info["status"] = "unsupported_suffix"
        info["note"] = "Convert or extract this file before running the closure."
    return info


def main() -> None:
    report = {
        "package_root": ".",
        "report_note": "Paths are relative to the strengthened package root.",
        "targets": [],
    }
    for aoi_id, query_kind, bbox in TARGETS:
        folder = ROOT / "egms_priority_downloads_v1" / aoi_id / query_kind
        folder.mkdir(parents=True, exist_ok=True)
        files = [p for p in folder.iterdir() if p.is_file()]
        inspected = [inspect_file(p) for p in sorted(files)]
        report["targets"].append(
            {
                "aoi_id": aoi_id,
                "query_kind": query_kind,
                "bbox_lonlat": bbox,
                "folder": str(folder.relative_to(ROOT)),
                "file_count": len(files),
                "files": inspected,
                "ready_candidates": [
                    item["path"]
                    for item in inspected
                    if item["status"] in {"candidate", "inspect_columns"} and item["suffix"] in READABLE_SUFFIXES
                ],
            }
        )
    out = ROOT / "egms_manual_download_preflight_report_v1.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
