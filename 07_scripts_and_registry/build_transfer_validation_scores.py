from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
PLAN = ROOT / "08_nature_experiment_plan"
OUTDIR = PLAN / "transfer_validation_scores_v1"
OUTDIR.mkdir(parents=True, exist_ok=True)

BENCH = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
JAPAN = ROOT / "04_japan_licsbas_probe" / "h5_velocity_summary.json"
IRAN = ROOT / "05_iran_insar_probe" / "tif_inspection.json"
TRANSFER_NOTE = PLAN / "transfer_validation_v1.md"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    bench = pd.read_csv(BENCH)
    japan = load_json(JAPAN)
    iran = load_json(IRAN)

    benchmark_rows = []
    for _, row in bench.iterrows():
        signal = str(row["observability_bias_signal"])
        anchor = str(row["independent_anchor_status"])
        egms_status = str(row["egms_status"])
        transfer_supported = 1 if signal in {"positive", "strong_positive"} and "query_pack_ready_token_required" in egms_status else 0
        control_flag = 1 if signal == "inconclusive" else 0
        benchmark_rows.append(
            {
                "scope": "regional_benchmark",
                "target": str(row["region"]),
                "signal": signal,
                "anchor": anchor,
                "evidence_type": "regional_lineage_extension",
                "status": "supported" if transfer_supported else ("control" if control_flag else "partial"),
                "readable": 1,
                "directional_support": transfer_supported,
                "independent_truth": 0,
                "token_required": 1 if "query_pack_ready_token_required" in egms_status else 0,
                "notes": str(row["nature_readiness"]),
            }
        )

    japan_row = japan[0]
    japan_score = 1 if japan_row["velocity_stats"]["fraction_lt_minus_5"] >= 0.15 and japan_row["velocity_stats"]["finite_count"] > 10000 else 0
    benchmark_rows.append(
        {
            "scope": "external_transfer",
            "target": "Japan Niigata",
            "signal": "subsidence_lineage_extension",
            "anchor": "public_licsbas_product",
            "evidence_type": "public_selective_download",
            "status": "supported" if japan_score else "partial",
            "readable": 1,
            "directional_support": japan_score,
            "independent_truth": 0,
            "token_required": 0,
            "notes": f"n_time_steps={japan_row['n_time_steps']}; fraction_lt_minus_5={japan_row['velocity_stats']['fraction_lt_minus_5']:.3f}",
        }
    )

    iran_rate = iran[0]
    iran_mask = iran[2]
    iran_score = 1 if iran_rate["stats"]["finite_count"] > 1000000 and iran_mask["stats"]["median"] == 0.0 else 0
    benchmark_rows.append(
        {
            "scope": "external_transfer",
            "target": "Iran nationwide InSAR",
            "signal": "no_token_processed_insar_extension",
            "anchor": "public_zenodo_product",
            "evidence_type": "no_token_processed_raster",
            "status": "supported" if iran_score else "partial",
            "readable": 1,
            "directional_support": iran_score,
            "independent_truth": 0,
            "token_required": 0,
            "notes": f"rate_median={iran_rate['stats']['median']:.3f}; mask_median={iran_mask['stats']['median']:.1f}",
        }
    )

    # A frozen scalar summary that does not pretend to be an external truth benchmark.
    support_score = (
        sum(r["directional_support"] for r in benchmark_rows) / len(benchmark_rows)
        if benchmark_rows
        else 0.0
    )

    fieldnames = [
        "scope",
        "target",
        "signal",
        "anchor",
        "evidence_type",
        "status",
        "readable",
        "directional_support",
        "independent_truth",
        "token_required",
        "notes",
    ]
    write_csv(OUTDIR / "transfer_validation_scores_v1.csv", benchmark_rows, fieldnames)

    report_lines = [
        "# Transfer Validation Scores v1",
        "",
        "This artifact freezes the current transfer evidence without opening any new validation split.",
        "",
        "## Frozen Decision Rule",
        "",
        "A transfer target is marked supported only when the evidence shows a readable, reproducible lineage extension and does not claim independent truth.",
        "",
        "## Score Table",
        "",
        "| scope | target | status | readable | directional support | independent truth | token required | notes |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for row in benchmark_rows:
        report_lines.append(
            f"| {row['scope']} | {row['target']} | {row['status']} | {row['readable']} | "
            f"{row['directional_support']} | {row['independent_truth']} | {row['token_required']} | {row['notes']} |"
        )
    report_lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Frozen transfer support score: `{support_score:.3f}`",
            "- Japan is scored as a public product-lineage extension after selective ingest, not independent truth.",
            "- Iran is scored as a no-token processed InSAR extension, not independent truth.",
            "- EGMS remains token-blocked, so no new external truth benchmark is claimed.",
            "",
            "## Guardrail",
            "",
            "- This is a frozen validation summary, not a fresh hyperparameter search.",
            "- It supports the manuscript's scope-extension language while keeping the Nature-grade boundary explicit.",
        ]
    )
    (OUTDIR / "transfer_validation_scores_v1.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    note_lines = TRANSFER_NOTE.read_text(encoding="utf-8").splitlines()
    if "transfer_validation_scores_v1" not in "\n".join(note_lines):
        note_lines.extend(
            [
                "",
                "## Frozen Scores",
                "- `08_nature_experiment_plan/transfer_validation_scores_v1/transfer_validation_scores_v1.csv`",
                "- `08_nature_experiment_plan/transfer_validation_scores_v1/transfer_validation_scores_v1.md`",
            ]
        )
        TRANSFER_NOTE.write_text("\n".join(note_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
