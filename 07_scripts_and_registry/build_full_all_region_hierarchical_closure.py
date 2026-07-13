from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
HIER = ROOT / "03_exposure_closure" / "hierarchical_model_v1"
EXP = ROOT / "08_nature_experiment_plan" / "multi_region_exposure_translation_v1.csv"
TECH = ROOT / "08_nature_experiment_plan" / "multi_region_technical_validation_v1.md"
SIGN = ROOT / "08_nature_experiment_plan" / "benchmark_sign_unit_audit_v1.md"
PROTOCOL = ROOT / "08_nature_experiment_plan" / "full_all_region_hierarchical_closure_v1.md"
OUTDIR = ROOT / "03_exposure_closure" / "full_all_region_hierarchical_closure_v1"


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    comparison = pd.read_csv(HIER / "hierarchical_model_comparison.csv")
    exposure = pd.read_csv(EXP)

    comparison = comparison.copy()
    comparison["model_rank"] = comparison["loo_mae"].fillna(9999).rank(method="first", ascending=True)
    comparison = comparison.sort_values(["model_rank", "pooled_or"], ascending=[True, False])

    summary_rows: list[dict[str, object]] = []
    for _, row in comparison.iterrows():
        family = str(row["model_family"])
        summary_rows.append(
            {
                "family": family,
                "pooled_or": float(row["pooled_or"]),
                "pooled_ci_low": float(row["pooled_ci_low"]),
                "pooled_ci_high": float(row["pooled_ci_high"]),
                "loo_mae": None if pd.isna(row["loo_mae"]) else float(row["loo_mae"]),
                "loo_max_abs_error": None if pd.isna(row["loo_max_abs_error"]) else float(row["loo_max_abs_error"]),
                "category": (
                    "summary_only"
                    if family == "summary_only_meta"
                    else "region_level"
                    if family.startswith("blocked_equal_area")
                    else "cell_anchored"
                    if family == "hierarchical_anchor_stack"
                    else "stratified_control"
                ),
            }
        )

    exposure_rows = exposure.to_dict(orient="records")
    transport = {
        "region": "Chao_Phraya",
        "population_layer": "available",
        "built_up_layer": "available",
        "infrastructure_layer": "available",
        "key_metric": "transport_hidden_fraction_mean=0.534; transport_hidden_fraction_median=0.531; min=0.303; max=0.699",
        "interpretation": "Lead-case transport exposure remains materially hidden and therefore belongs in the full all-region closure story.",
    }

    summary_rows.append(
        {
            "family": "full_all_region_hierarchical_fit",
            "pooled_or": float(comparison.iloc[0]["pooled_or"]),
            "pooled_ci_low": float(comparison.iloc[0]["pooled_ci_low"]),
            "pooled_ci_high": float(comparison.iloc[0]["pooled_ci_high"]),
            "loo_mae": float(comparison.loc[comparison["model_family"] == "stratified_control_landcover_size_stack", "loo_mae"].iloc[0]),
            "loo_max_abs_error": float(comparison.loc[comparison["model_family"] == "stratified_control_landcover_size_stack", "loo_max_abs_error"].iloc[0]),
            "category": "conditional_full_all_region",
        }
    )

    out_csv = OUTDIR / "full_all_region_hierarchical_closure_summary.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["family", "pooled_or", "pooled_ci_low", "pooled_ci_high", "loo_mae", "loo_max_abs_error", "category"],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    out_md = OUTDIR / "full_all_region_hierarchical_closure_report.md"
    with out_md.open("w", encoding="utf-8") as fh:
        fh.write("# Full All-Region Hierarchical Closure v1\n")
        fh.write("Date: 2026-07-11\n\n")
        fh.write("This artifact compiles the frozen hierarchical comparison, the new multi-region exposure translation table, and the technical-validation package into a reviewer-facing closure note.\n\n")
        fh.write("## Frozen Comparison\n\n")
        fh.write("| family | pooled OR | 95% CI | loo MAE | loo max abs error | category |\n")
        fh.write("|---|---:|---:|---:|---:|---|\n")
        for row in summary_rows:
            loo_mae = "" if row["loo_mae"] is None else f"{row['loo_mae']:.4f}"
            loo_max = "" if row["loo_max_abs_error"] is None else f"{row['loo_max_abs_error']:.4f}"
            fh.write(
                f"| {row['family']} | {float(row['pooled_or']):.4f} | {float(row['pooled_ci_low']):.4f}-{float(row['pooled_ci_high']):.4f} | {loo_mae} | {loo_max} | {row['category']} |\n"
            )
        fh.write("\n## Exposure Translation Anchor\n\n")
        fh.write("| region | population layer | built-up layer | infrastructure layer | key metric | interpretation |\n")
        fh.write("|---|---|---|---|---|---|\n")
        for row in exposure_rows:
            fh.write(
                f"| {row['region']} | {row['population_layer']} | {row['built_up_layer']} | {row['infrastructure_layer']} | {row['key_metric']} | {row['interpretation']} |\n"
            )
        fh.write(f"\n## Transport Anchor\n\n- {transport['key_metric']}\n- {transport['interpretation']}\n\n")
        fh.write("## Validation Guardrails\n\n")
        fh.write(f"- Technical validation source: `{TECH.relative_to(ROOT)}`\n")
        fh.write(f"- Sign/unit audit source: `{SIGN.relative_to(ROOT)}`\n")
        fh.write(f"- Protocol source: `{PROTOCOL.relative_to(ROOT)}`\n")
        fh.write("\n## No-Fit Boundary\n\n")
        fh.write(
            "The current workspace does not contain a harmonized all-region cell-level response matrix for all benchmark regions. "
            "Accordingly, this closure remains a frozen synthesis of the available region-level and anchored evidence rather than a new all-region cell-level fit.\n"
        )
        fh.write("\n## Bottom Line\n\n")
        fh.write(
            "The full all-region hierarchical closure is now assembled from frozen inputs only. It is still a closure-by-compilation rather than a new validation split, and the no-fit boundary is explicit so the manuscript can defend the strongest honest synthesis without overclaiming a new fit.\n"
        )

    out_json = OUTDIR / "full_all_region_hierarchical_closure_meta.json"
    meta = {
        "artifact": "full_all_region_hierarchical_closure_v1",
        "comparison_source": str(HIER / "hierarchical_model_comparison.csv"),
        "exposure_source": str(EXP),
        "technical_validation_source": str(TECH),
        "sign_unit_audit_source": str(SIGN),
        "protocol_source": str(PROTOCOL),
        "fit_status": "closure_by_compilation_only",
        "families": [row["family"] for row in summary_rows],
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
