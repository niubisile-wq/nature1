from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
EXPOSURE = ROOT / "03_exposure_closure" / "multi_delta_vlm_exposure_censoring_summary.csv"
OUT_CSV = ROOT / "08_nature_experiment_plan" / "multi_region_exposure_closure_v1.csv"
OUT_MD = ROOT / "08_nature_experiment_plan" / "multi_region_exposure_closure_v1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    benchmark_rows = {row["region"]: row for row in read_csv(BENCHMARK)}
    exposure_rows = {row["delta"]: row for row in read_csv(EXPOSURE)}

    regions = ["Po", "Chao Phraya", "Indus", "Rhone", "Brantas", "Rhine"]
    out_rows: list[dict[str, str]] = []
    for region in regions:
        bench = benchmark_rows.get(region, {})
        exp = exposure_rows.get(region, {})
        out_rows.append(
            {
                "region": region,
                "signal": bench.get("observability_bias_signal", bench.get("signal", "")),
                "anchor": bench.get("independent_anchor_status", bench.get("gnss_anchor_status", "")),
                "landcover": bench.get("dominant_landcover", ""),
                "odds_ratio": bench.get("landcover_adjusted_or", ""),
                "strong_cells": exp.get("strong_sub_5mm_cells", ""),
                "strong_pop_fraction": exp.get("strong_sub_5mm_population_fraction", ""),
                "strong_pop_not_majority_fraction": exp.get("strong_sub_5mm_population_not_majority_fraction", ""),
                "strong_built_not_majority_fraction": exp.get("strong_sub_5mm_builtup_not_majority_fraction", ""),
                "risk_proxy": bench.get("bias_or_minus_one_proxy", ""),
                "readiness": bench.get("nature_readiness", ""),
                "source_note": "Derived from benchmark and exposure summaries",
            }
        )

    fieldnames = [
        "region",
        "signal",
        "anchor",
        "landcover",
        "odds_ratio",
        "strong_cells",
        "strong_pop_fraction",
        "strong_pop_not_majority_fraction",
        "strong_built_not_majority_fraction",
        "risk_proxy",
        "readiness",
        "source_note",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    lines = [
        "# Multi-Region Exposure Closure v1",
        "",
        "This file is generated from `benchmark_region_evidence_v0_1.csv` and `multi_delta_vlm_exposure_censoring_summary.csv`.",
        "",
        "| region | signal | anchor | landcover | OR | strong cells | strong pop fraction | pop not-majority | built not-majority | risk proxy | readiness |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in out_rows:
        lines.append(
            f"| {row['region']} | {row['signal']} | {row['anchor']} | {row['landcover']} | {row['odds_ratio']} | "
            f"{row['strong_cells']} | {row['strong_pop_fraction']} | {row['strong_pop_not_majority_fraction']} | "
            f"{row['strong_built_not_majority_fraction']} | {row['risk_proxy']} | {row['readiness']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
