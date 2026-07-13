from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import norm


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
EXPOSURE = ROOT / "08_nature_experiment_plan" / "multi_region_exposure_closure_v1.csv"
OUTDIR = ROOT / "03_exposure_closure" / "multi_region_summary_meta_closure_v1"


def derive_se(log_or: float, lo: float, hi: float) -> float:
    return (math.log(hi) - math.log(lo)) / (2.0 * 1.96)


def read_benchmark() -> pd.DataFrame:
    df = pd.read_csv(BENCHMARK)
    df["log_or"] = np.log(df["landcover_adjusted_or"].astype(float))
    df["se"] = [
        derive_se(orv, lo, hi)
        for orv, lo, hi in zip(
            df["landcover_adjusted_or"].astype(float),
            df["landcover_adjusted_boot_q025"].astype(float),
            df["landcover_adjusted_boot_q975"].astype(float),
        )
    ]
    df["var"] = df["se"] ** 2
    df["weight_fixed"] = 1.0 / df["var"]
    df["anchor_code"] = df["independent_anchor_status"].map(
        {
            "sparse_gnss_anchor": 0.0,
            "weak_or_missing_gnss_anchor": 1.0,
            "control_or_specification_case": -1.0,
        }
    ).astype(float)
    df["signal_code"] = df["observability_bias_signal"].map({"inconclusive": 0.0, "positive": 1.0, "strong_positive": 2.0}).astype(float)
    df["landcover_code"] = df["dominant_landcover"].map({"cropland": 0.0, "vegetation_non_crop": 1.0, "built_up": 2.0, "water_wetland_mangrove": 3.0}).astype(float)
    return df


def fixed_random_meta(y: np.ndarray, v: np.ndarray) -> dict[str, float]:
    w = 1.0 / v
    fe = float(np.sum(w * y) / np.sum(w))
    q = float(np.sum(w * (y - fe) ** 2))
    df = len(y) - 1
    c = float(np.sum(w) - np.sum(w**2) / np.sum(w))
    tau2 = max(0.0, (q - df) / c) if c > 0 else 0.0
    wr = 1.0 / (v + tau2)
    re = float(np.sum(wr * y) / np.sum(wr))
    se_fe = math.sqrt(1.0 / np.sum(w))
    se_re = math.sqrt(1.0 / np.sum(wr))
    i2 = max(0.0, (q - df) / q) if q > 0 else 0.0
    return {
        "k": float(len(y)),
        "fixed_log_or": fe,
        "fixed_se": se_fe,
        "fixed_or": float(math.exp(fe)),
        "fixed_ci_low": float(math.exp(fe - 1.96 * se_fe)),
        "fixed_ci_high": float(math.exp(fe + 1.96 * se_fe)),
        "random_log_or": re,
        "random_se": se_re,
        "random_or": float(math.exp(re)),
        "random_ci_low": float(math.exp(re - 1.96 * se_re)),
        "random_ci_high": float(math.exp(re + 1.96 * se_re)),
        "q": q,
        "tau2": tau2,
        "i2": i2,
        "df": float(df),
    }


def weighted_ridge_regression(x: np.ndarray, y: np.ndarray, w: np.ndarray, ridge: float = 1e-4) -> dict[str, Any]:
    sw = np.sqrt(w)[:, None]
    xw = x * sw
    yw = y * np.sqrt(w)
    xtx = xw.T @ xw
    eye = np.eye(x.shape[1], dtype=float)
    eye[0, 0] = 0.0
    beta = np.linalg.solve(xtx + ridge * eye, xw.T @ yw)
    cov = np.linalg.pinv(xtx + ridge * eye)
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    return {"beta": beta, "se": se, "cov": cov}


def leave_one_out_meta(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for idx in range(len(df)):
        keep = np.ones(len(df), dtype=bool)
        keep[idx] = False
        stats = fixed_random_meta(df.loc[keep, "log_or"].to_numpy(), df.loc[keep, "var"].to_numpy())
        rows.append(
            {
                "left_out_region": df.loc[idx, "region"],
                "pooled_random_or": stats["random_or"],
                "pooled_random_ci_low": stats["random_ci_low"],
                "pooled_random_ci_high": stats["random_ci_high"],
                "tau2": stats["tau2"],
                "i2": stats["i2"],
            }
        )
    return rows


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    bench = read_benchmark()

    overall = fixed_random_meta(bench["log_or"].to_numpy(), bench["var"].to_numpy())
    lead_mask = bench["observability_bias_signal"].isin(["positive", "strong_positive"])
    control_mask = bench["observability_bias_signal"].eq("inconclusive")
    sparse_anchor_mask = bench["independent_anchor_status"].eq("sparse_gnss_anchor")
    weak_anchor_mask = bench["independent_anchor_status"].eq("weak_or_missing_gnss_anchor")

    lead = fixed_random_meta(bench.loc[lead_mask, "log_or"].to_numpy(), bench.loc[lead_mask, "var"].to_numpy())
    control = fixed_random_meta(bench.loc[control_mask, "log_or"].to_numpy(), bench.loc[control_mask, "var"].to_numpy()) if control_mask.any() else None
    sparse = fixed_random_meta(bench.loc[sparse_anchor_mask, "log_or"].to_numpy(), bench.loc[sparse_anchor_mask, "var"].to_numpy())
    weak = fixed_random_meta(bench.loc[weak_anchor_mask, "log_or"].to_numpy(), bench.loc[weak_anchor_mask, "var"].to_numpy())

    # Exploratory meta-regression with a small ridge penalty.
    x = np.column_stack(
        [
            np.ones(len(bench), dtype=float),
            bench["anchor_code"].to_numpy(),
            bench["signal_code"].to_numpy(),
            bench["cropland_fraction"].astype(float).to_numpy(),
            bench["built_up_fraction"].astype(float).to_numpy(),
            np.log1p(bench["ngl_station_count"].astype(float).to_numpy()),
        ]
    )
    reg = weighted_ridge_regression(x, bench["log_or"].to_numpy(), 1.0 / bench["var"].to_numpy(), ridge=1e-3)
    reg_terms = [
        "intercept",
        "anchor_code",
        "signal_code",
        "cropland_fraction",
        "built_up_fraction",
        "log1p_ngl_station_count",
    ]
    reg_rows = []
    for i, term in enumerate(reg_terms):
        b = float(reg["beta"][i])
        s = float(reg["se"][i])
        reg_rows.append(
            {
                "term": term,
                "beta": b,
                "se": s,
                "z": b / s if s > 0 else float("nan"),
                "or": float(math.exp(b)),
                "or_ci_low": float(math.exp(b - 1.96 * s)) if s > 0 else float("nan"),
                "or_ci_high": float(math.exp(b + 1.96 * s)) if s > 0 else float("nan"),
            }
        )

    loo = leave_one_out_meta(bench)

    bench_fields = [
        "region",
        "observability_bias_signal",
        "independent_anchor_status",
        "dominant_landcover",
        "landcover_adjusted_or",
        "landcover_adjusted_boot_q025",
        "landcover_adjusted_boot_q975",
        "log_or",
        "se",
        "weight_fixed",
        "n_lisc_pairs",
        "n_cells",
        "cropland_fraction",
        "built_up_fraction",
        "water_wetland_mangrove_fraction",
    ]
    exposure = pd.read_csv(EXPOSURE)
    exposure_join = exposure[["region", "signal", "anchor", "landcover", "odds_ratio", "strong_cells", "strong_pop_fraction", "strong_pop_not_majority_fraction", "strong_built_not_majority_fraction", "risk_proxy", "readiness"]].copy()

    with (OUTDIR / "multi_region_meta_closure_region_table.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=bench_fields)
        writer.writeheader()
        writer.writerows(bench[bench_fields].to_dict(orient="records"))

    with (OUTDIR / "multi_region_meta_closure_exposure_table.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(exposure_join.columns))
        writer.writeheader()
        writer.writerows(exposure_join.to_dict(orient="records"))

    with (OUTDIR / "multi_region_meta_closure_meta_regression.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["term", "beta", "se", "z", "or", "or_ci_low", "or_ci_high"])
        writer.writeheader()
        writer.writerows(reg_rows)

    with (OUTDIR / "multi_region_meta_closure_leave_one_out.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["left_out_region", "pooled_random_or", "pooled_random_ci_low", "pooled_random_ci_high", "tau2", "i2"])
        writer.writeheader()
        writer.writerows(loo)

    summary = [
        "# Multi-Region Summary Meta-Closure v1",
        "",
        "This artifact is a self-contained summary-level closure over the regional benchmark evidence.",
        "It is not a replacement for the full cell-level hierarchical model, but it closes the current region-level evidence layer without missing helper modules.",
        "",
        "## Region-Level Evidence",
        "",
        "| region | signal | anchor | OR | 95% CI | weight |",
        "|---|---|---|---:|---:|---:|",
    ]
    for _, row in bench.iterrows():
        summary.append(
            f"| {row['region']} | {row['observability_bias_signal']} | {row['independent_anchor_status']} | {row['landcover_adjusted_or']:.4f} | {row['landcover_adjusted_boot_q025']:.4f}-{row['landcover_adjusted_boot_q975']:.4f} | {row['weight_fixed']:.2f} |"
        )

    summary.extend(
        [
            "",
            "## Meta-Analysis",
            "",
            f"- Regions: `{int(overall['k'])}`",
            f"- Fixed-effect pooled OR: `{overall['fixed_or']:.4f}`",
            f"- Fixed-effect 95% CI: `{overall['fixed_ci_low']:.4f}-{overall['fixed_ci_high']:.4f}`",
            f"- Random-effect pooled OR: `{overall['random_or']:.4f}`",
            f"- Random-effect 95% CI: `{overall['random_ci_low']:.4f}-{overall['random_ci_high']:.4f}`",
            f"- Heterogeneity Q: `{overall['q']:.4f}`",
            f"- Tau^2: `{overall['tau2']:.6f}`",
            f"- I^2: `{overall['i2']:.3f}`",
            "",
            "## Subgroups",
            "",
            f"- Lead/positive subgroup pooled OR: `{lead['random_or']:.4f}`",
            f"- Sparse-anchor subgroup pooled OR: `{sparse['random_or']:.4f}`",
            f"- Weak-anchor subgroup pooled OR: `{weak['random_or']:.4f}`",
        ]
    )
    if control is not None:
        summary.append(f"- Control/specification subgroup pooled OR: `{control['random_or']:.4f}`")
    summary.extend(
        [
            "",
            "## Meta-Regression",
            "",
            "| term | beta | se | z | OR | 95% CI |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in reg_rows:
        summary.append(
            f"| {row['term']} | {row['beta']:.4f} | {row['se']:.4f} | {row['z']:.4f} | {row['or']:.4f} | {row['or_ci_low']:.4f}-{row['or_ci_high']:.4f} |"
        )
    summary.extend(
        [
            "",
            "## Leave-One-Out",
            "",
            "The leave-one-out table is written to CSV and lets the reader see whether any single region dominates the pooled result.",
            "",
            "## Interpretation Guardrail",
            "",
            "- This is a summary-level closure over the current regional evidence set.",
            "- It does not replace the cell-level lead-case model already recovered for Chao Phraya.",
            "- It does close the region-level inference layer that was previously only documented narratively.",
        ]
    )
    (OUTDIR / "multi_region_meta_closure_report.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    meta = {
        "overall": overall,
        "lead": lead,
        "sparse": sparse,
        "weak": weak,
        "control": control,
        "n_regions": int(len(bench)),
        "n_exposure_rows": int(len(exposure_join)),
    }
    (OUTDIR / "multi_region_meta_closure_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "outdir": str(OUTDIR),
                "random_or": overall["random_or"],
                "i2": overall["i2"],
                "lead_or": lead["random_or"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
