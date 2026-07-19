from __future__ import annotations

import gzip
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUTROOT = ROOT / "egms_input_compatibility_selftest_v1"


def make_points() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Lon Deg": [-120.50, -120.49, -120.48, -120.47, -120.46],
            "Lat Deg": [36.50, 36.51, 36.52, 36.53, 36.54],
            "V_UP mm yr": [-6.0, -2.0, -0.1, 1.2, -10.5],
            "Temp Coh": [0.8, 0.7, 0.9, 0.6, 0.5],
            "Amp Dispersion": [0.2, 0.3, 0.1, 0.4, 0.5],
        }
    )


def run_closure(input_path: Path, label: str) -> dict:
    outdir = OUTROOT / f"closure_{label}"
    cmd = [
        sys.executable,
        str(ROOT / "build_egms_benchmark_closure_v1.py"),
        "--input",
        str(input_path),
        "--outdir",
        str(outdir),
        "--aoi-id",
        f"selftest_{label}",
        "--product-label",
        f"SELFTEST_{label}",
        "--thresholds",
        "1,2,5,10",
        "--max-point-output",
        "100",
    ]
    subprocess.run(cmd, check=True)
    meta = json.loads((outdir / "egms_benchmark_closure_meta_v1.json").read_text(encoding="utf-8"))
    thresholds = pd.read_csv(outdir / "egms_benchmark_closure_thresholds_v1.csv")
    return {
        "label": label,
        "input": str(input_path.relative_to(ROOT)),
        "detected_columns": {
            "longitude": meta["longitude_column"],
            "latitude": meta["latitude_column"],
            "velocity": meta["velocity_column"],
            "temporal_coherence": meta["temporal_coherence_column"],
            "amplitude_dispersion": meta["amplitude_dispersion_column"],
        },
        "n_valid_closure_rows": meta["n_valid_closure_rows"],
        "strong_points_at_5mm": int(thresholds.loc[thresholds["threshold_mm_per_year"] == 5.0, "n_strong_points"].iloc[0]),
    }


def main() -> None:
    if OUTROOT.exists():
        shutil.rmtree(OUTROOT)
    OUTROOT.mkdir(parents=True)
    inputs = OUTROOT / "inputs"
    inputs.mkdir()

    df = make_points()
    csv_path = inputs / "egms_variant_columns.csv"
    csv_gz_path = inputs / "egms_variant_columns.csv.gz"
    parquet_path = inputs / "egms_variant_columns.parquet"
    pq_path = inputs / "egms_variant_columns.pq"

    df.to_csv(csv_path, index=False)
    with gzip.open(csv_gz_path, "wt", encoding="utf-8", newline="") as handle:
        df.to_csv(handle, index=False)
    df.to_parquet(parquet_path, index=False)
    shutil.copy2(parquet_path, pq_path)

    results = [
        run_closure(csv_path, "csv"),
        run_closure(csv_gz_path, "csv_gz"),
        run_closure(parquet_path, "parquet"),
        run_closure(pq_path, "pq"),
    ]
    report = {
        "purpose": "Verify EGMS closure input compatibility for variant column names and csv/csv.gz/parquet/pq formats.",
        "expected_velocity_column": "V_UP mm yr",
        "results": results,
    }
    report_path = OUTROOT / "egms_input_compatibility_selftest_report_v1.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
