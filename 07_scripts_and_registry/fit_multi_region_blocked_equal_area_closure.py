from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
AREA = ROOT / "08_nature_experiment_plan" / "area_weighted_exposure_v1.csv"
EXPOSURE = ROOT / "08_nature_experiment_plan" / "multi_region_exposure_closure_v1.csv"
OUTDIR = ROOT / "03_exposure_closure" / "multi_region_blocked_equal_area_closure_v1"


def derive_se_from_ci(lo: float, hi: float) -> float:
    return (math.log(hi) - math.log(lo)) / (2.0 * 1.96)


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not np.any(mask):
        return float("nan")
    values = values[mask]
    weights = weights[mask]
    denom = float(np.sum(weights))
    if denom <= 0:
        return float("nan")
    return float(np.sum(values * weights) / denom)


def fixed_random_meta(log_or: np.ndarray, var: np.ndarray) -> dict[str, float]:
    w = 1.0 / var
    fe = weighted_mean(log_or, w)
    q = float(np.sum(w * (log_or - fe) ** 2))
    df = max(len(log_or) - 1, 1)
    c = float(np.sum(w) - np.sum(w**2) / np.sum(w))
    tau2 = max(0.0, (q - df) / c) if c > 0 else 0.0
    wr = 1.0 / (var + tau2)
    re = weighted_mean(log_or, wr)
    se_fe = math.sqrt(1.0 / np.sum(w))
    se_re = math.sqrt(1.0 / np.sum(wr))
    i2 = max(0.0, (q - df) / q) if q > 0 else 0.0
    return {
        "k": float(len(log_or)),
        "fixed_log_or": fe,
        "fixed_or": float(math.exp(fe)),
        "fixed_ci_low": float(math.exp(fe - 1.96 * se_fe)),
        "fixed_ci_high": float(math.exp(fe + 1.96 * se_fe)),
        "random_log_or": re,
        "random_or": float(math.exp(re)),
        "random_ci_low": float(math.exp(re - 1.96 * se_re)),
        "random_ci_high": float(math.exp(re + 1.96 * se_re)),
        "q": q,
        "tau2": tau2,
        "i2": i2,
    }


def ridge_wls(x: np.ndarray, y: np.ndarray, w: np.ndarray, ridge: float = 1e-3) -> dict[str, np.ndarray]:
    sw = np.sqrt(w)[:, None]
    xw = x * sw
    yw = y * np.sqrt(w)
    xtx = xw.T @ xw
    eye = np.eye(x.shape[1], dtype=float)
    eye[0, 0] = 0.0
    beta = np.linalg.solve(xtx + ridge * eye, xw.T @ yw)
    cov = np.linalg.pinv(xtx + ridge * eye)
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    return {"beta": beta, "cov": cov, "se": se}


def load_tables() -> pd.DataFrame:
    bench = pd.read_csv(BENCHMARK)
    area = pd.read_csv(AREA)
    exposure = pd.read_csv(EXPOSURE)
    df = bench.merge(area, on="region", how="left", suffixes=("", "_area")).merge(exposure, on="region", how="left", suffixes=("", "_exp"))
    df["log_or"] = np.log(df["landcover_adjusted_or"].astype(float))
    df["se"] = [
        derive_se_from_ci(float(lo), float(hi))
        for lo, hi in zip(df["landcover_adjusted_boot_q025"].astype(float), df["landcover_adjusted_boot_q975"].astype(float))
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
    df["landcover_code"] = df["dominant_landcover"].map(
        {
            "cropland": 0.0,
            "vegetation_non_crop": 1.0,
            "built_up": 2.0,
            "water_wetland_mangrove": 3.0,
        }
    ).astype(float)
    df["equal_area_weight"] = df["n_cells"].astype(float)
    df["strong_area_weight"] = df["strong_cells"].astype(float)
    df["naturalness_group"] = np.where(
        df["observability_bias_signal"].isin(["positive", "strong_positive"]),
        "signal_positive",
        np.where(df["observability_bias_signal"].eq("inconclusive"), "control_spec", "other"),
    )
    return df


def loo_blocked(df: pd.DataFrame, xcols: list[str], ridge: float = 1e-3) -> list[dict[str, Any]]:
    rows = []
    for idx in range(len(df)):
        keep = np.ones(len(df), dtype=bool)
        keep[idx] = False
        train = df.loc[keep].copy()
        test = df.loc[~keep].iloc[0]
        x_train = np.column_stack([np.ones(len(train), dtype=float)] + [train[col].astype(float).to_numpy() for col in xcols])
        fit = ridge_wls(x_train, train["log_or"].to_numpy(), 1.0 / train["var"].to_numpy(), ridge=ridge)
        x_test = np.array([1.0] + [float(test[col]) for col in xcols], dtype=float)
        pred = float(x_test @ fit["beta"])
        pred_se = float(math.sqrt(max(x_test @ fit["cov"] @ x_test, 0.0)))
        rows.append(
            {
                "left_out_region": test["region"],
                "observed_log_or": float(test["log_or"]),
                "observed_or": float(test["landcover_adjusted_or"]),
                "predicted_log_or": pred,
                "predicted_or": float(math.exp(pred)),
                "predicted_or_ci_low": float(math.exp(pred - 1.96 * pred_se)),
                "predicted_or_ci_high": float(math.exp(pred + 1.96 * pred_se)),
                "residual_log_or": float(test["log_or"] - pred),
            }
        )
    return rows


def as_rows(df: pd.DataFrame, cols: list[str]) -> list[dict[str, Any]]:
    return df[cols].to_dict(orient="records")


def meta_or(values: np.ndarray, weights: np.ndarray) -> float:
    return float(math.exp(weighted_mean(np.log(values), weights)))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = load_tables()

    overall = fixed_random_meta(df["log_or"].to_numpy(), df["var"].to_numpy())
    equal_area_or = meta_or(df["landcover_adjusted_or"].astype(float).to_numpy(), df["equal_area_weight"].to_numpy())
    strong_area_or = meta_or(df["landcover_adjusted_or"].astype(float).to_numpy(), np.nan_to_num(df["strong_area_weight"].astype(float).to_numpy(), nan=0.0))
    pop_weight_or = meta_or(
        df["landcover_adjusted_or"].astype(float).to_numpy(),
        np.nan_to_num(df["strong_pop_fraction"].astype(float).to_numpy(), nan=0.0),
    )

    xcols = [
        "signal_code_z",
        "anchor_code_z",
        "log1p_cells_z",
    ]
    df["log1p_cells"] = np.log1p(df["n_cells"].astype(float))
    df["signal_code_z"] = (df["signal_code"] - df["signal_code"].mean()) / (df["signal_code"].std(ddof=0) or 1.0)
    df["anchor_code_z"] = (df["anchor_code"] - df["anchor_code"].mean()) / (df["anchor_code"].std(ddof=0) or 1.0)
    df["log1p_cells_z"] = (df["log1p_cells"] - df["log1p_cells"].mean()) / (df["log1p_cells"].std(ddof=0) or 1.0)
    x = np.column_stack([np.ones(len(df), dtype=float)] + [df[col].astype(float).to_numpy() for col in xcols])
    fit = ridge_wls(x, df["log_or"].to_numpy(), 1.0 / df["var"].to_numpy(), ridge=5.0)
    terms = ["intercept"] + xcols
    coef_rows = []
    for i, term in enumerate(terms):
        b = float(fit["beta"][i])
        s = float(fit["se"][i])
        coef_rows.append(
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

    loo = loo_blocked(df, xcols)

    region_cols = [
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
        "n_cells",
        "n_lisc_pairs",
        "equal_area_weight",
        "strong_area_weight",
        "strong_cells",
        "strong_sub_5mm_population_fraction",
        "strong_sub_5mm_population_not_majority_fraction",
        "strong_sub_5mm_builtup_fraction",
        "strong_sub_5mm_builtup_not_majority_fraction",
        "signal_code",
        "anchor_code",
        "cropland_fraction",
        "built_up_fraction",
        "water_wetland_mangrove_fraction",
        "readiness",
    ]
    write_csv(OUTDIR / "multi_region_blocked_equal_area_region_table.csv", as_rows(df, region_cols), region_cols)
    write_csv(OUTDIR / "multi_region_blocked_equal_area_meta_regression.csv", coef_rows, ["term", "beta", "se", "z", "or", "or_ci_low", "or_ci_high"])
    write_csv(
        OUTDIR / "multi_region_blocked_equal_area_leave_one_out.csv",
        loo,
        [
            "left_out_region",
            "observed_log_or",
            "observed_or",
            "predicted_log_or",
            "predicted_or",
            "predicted_or_ci_low",
            "predicted_or_ci_high",
            "residual_log_or",
        ],
    )

    weighted_summary = [
        {
            "scheme": "inverse_variance",
            "pooled_or": overall["random_or"],
            "ci_low": overall["random_ci_low"],
            "ci_high": overall["random_ci_high"],
            "notes": "Random-effects pooled OR from regional summary evidence.",
        },
        {
            "scheme": "equal_area_by_cell_count",
            "pooled_or": equal_area_or,
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "notes": "Equal-area proxy weighted by region cell count; summary-level approximation.",
        },
        {
            "scheme": "equal_area_by_strong_cell_count",
            "pooled_or": strong_area_or,
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "notes": "Stronger area-weighted proxy weighted by strong-cell count.",
        },
        {
            "scheme": "population_weighted_signal_proxy",
            "pooled_or": pop_weight_or,
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "notes": "Population-weighted proxy using strong-subsidence population fraction.",
        },
    ]
    write_csv(
        OUTDIR / "multi_region_blocked_equal_area_weighted_summary.csv",
        weighted_summary,
        ["scheme", "pooled_or", "ci_low", "ci_high", "notes"],
    )

    blocked_split = pd.DataFrame(
        [
            {
                "split": "signal_positive",
                "n_regions": int((df["observability_bias_signal"] != "inconclusive").sum()),
                "pooled_or": fixed_random_meta(
                    df.loc[df["observability_bias_signal"] != "inconclusive", "log_or"].to_numpy(),
                    df.loc[df["observability_bias_signal"] != "inconclusive", "var"].to_numpy(),
                )["random_or"],
            },
            {
                "split": "control_specification",
                "n_regions": int((df["observability_bias_signal"] == "inconclusive").sum()),
                "pooled_or": fixed_random_meta(
                    df.loc[df["observability_bias_signal"] == "inconclusive", "log_or"].to_numpy(),
                    df.loc[df["observability_bias_signal"] == "inconclusive", "var"].to_numpy(),
                )["random_or"],
            },
            {
                "split": "sparse_anchor",
                "n_regions": int((df["independent_anchor_status"] == "sparse_gnss_anchor").sum()),
                "pooled_or": fixed_random_meta(
                    df.loc[df["independent_anchor_status"] == "sparse_gnss_anchor", "log_or"].to_numpy(),
                    df.loc[df["independent_anchor_status"] == "sparse_gnss_anchor", "var"].to_numpy(),
                )["random_or"],
            },
            {
                "split": "weak_anchor",
                "n_regions": int((df["independent_anchor_status"] == "weak_or_missing_gnss_anchor").sum()),
                "pooled_or": fixed_random_meta(
                    df.loc[df["independent_anchor_status"] == "weak_or_missing_gnss_anchor", "log_or"].to_numpy(),
                    df.loc[df["independent_anchor_status"] == "weak_or_missing_gnss_anchor", "var"].to_numpy(),
                )["random_or"],
            },
        ]
    )
    write_csv(OUTDIR / "multi_region_blocked_equal_area_split_summary.csv", blocked_split.to_dict(orient="records"), ["split", "n_regions", "pooled_or"])

    report_lines = [
        "# Multi-Region Blocked Equal-Area Closure v1",
        "",
        "This artifact is a self-contained region-level blocked synthesis that upgrades the current multi-region evidence layer.",
        "It combines regional benchmark ORs, area-weighted exposure summaries, and frozen leave-one-region-out validation.",
        "",
        "## Region-Level Inputs",
        "",
        "| region | signal | anchor | OR | 95% CI | n_cells | strong_cells | readiness |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for _, row in df.iterrows():
        report_lines.append(
            f"| {row['region']} | {row['observability_bias_signal']} | {row['independent_anchor_status']} | "
            f"{row['landcover_adjusted_or']:.4f} | {row['landcover_adjusted_boot_q025']:.4f}-{row['landcover_adjusted_boot_q975']:.4f} | "
            f"{int(row['n_cells'])} | {int(row['strong_cells']) if pd.notna(row['strong_cells']) else ''} | {row['readiness']} |"
        )

    report_lines.extend(
        [
            "",
            "## Core Synthesis",
            "",
            f"- Random-effects pooled OR: `{overall['random_or']:.4f}`",
            f"- Random-effects 95% CI: `{overall['random_ci_low']:.4f}-{overall['random_ci_high']:.4f}`",
            f"- Heterogeneity I^2: `{overall['i2']:.3f}`",
            f"- Equal-area proxy OR by cell count: `{equal_area_or:.4f}`",
            f"- Equal-area proxy OR by strong-cell count: `{strong_area_or:.4f}`",
            f"- Population-weighted signal proxy OR: `{pop_weight_or:.4f}`",
            "",
            "## Blocked Meta-Regression",
            "",
            "| term | beta | se | z | OR | 95% CI |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in coef_rows:
        report_lines.append(
            f"| {row['term']} | {row['beta']:.4f} | {row['se']:.4f} | {row['z']:.4f} | {row['or']:.4f} | {row['or_ci_low']:.4f}-{row['or_ci_high']:.4f} |"
        )

    report_lines.extend(
        [
            "",
            "## Leave-One-Out Blocked Validation",
            "",
            "| left_out_region | observed OR | predicted OR | predicted 95% CI | residual log OR |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in loo:
        report_lines.append(
            f"| {row['left_out_region']} | {row['observed_or']:.4f} | {row['predicted_or']:.4f} | {row['predicted_or_ci_low']:.4f}-{row['predicted_or_ci_high']:.4f} | {row['residual_log_or']:.4f} |"
        )

    report_lines.extend(
        [
            "",
            "## Blocked Split View",
            "",
            "| split | n_regions | pooled OR |",
            "|---|---:|---:|",
        ]
    )
    for row in blocked_split.to_dict(orient="records"):
        report_lines.append(f"| {row['split']} | {int(row['n_regions'])} | {float(row['pooled_or']):.4f} |")

    report_lines.extend(
        [
            "",
            "## Interpretation Guardrail",
            "",
            "- This is a summary-level blocked/equal-area closure, not a replacement for a full cell-level hierarchical model.",
            "- It does tighten the current multi-region package by making the region-size and validation structure explicit.",
            "- The remaining Nature-grade gap is the cell-level equal-area benchmark and external EGMS closure.",
        ]
    )

    (OUTDIR / "multi_region_blocked_equal_area_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    meta = {
        "artifact": "multi_region_blocked_equal_area_closure_v1",
        "n_regions": int(len(df)),
        "random_effects_or": overall["random_or"],
        "equal_area_or_by_cell_count": equal_area_or,
        "equal_area_or_by_strong_cell_count": strong_area_or,
        "population_weighted_signal_proxy_or": pop_weight_or,
        "files": [
            "multi_region_blocked_equal_area_region_table.csv",
            "multi_region_blocked_equal_area_meta_regression.csv",
            "multi_region_blocked_equal_area_leave_one_out.csv",
            "multi_region_blocked_equal_area_weighted_summary.csv",
            "multi_region_blocked_equal_area_split_summary.csv",
            "multi_region_blocked_equal_area_report.md",
        ],
    }
    (OUTDIR / "multi_region_blocked_equal_area_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
