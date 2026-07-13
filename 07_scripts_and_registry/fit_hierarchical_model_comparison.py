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
SUMMARY_DIR = ROOT / "03_exposure_closure" / "multi_region_summary_meta_closure_v1"
BLOCKED_DIR = ROOT / "03_exposure_closure" / "multi_region_blocked_equal_area_closure_v1"
HYBRID_DIR = ROOT / "03_exposure_closure" / "hierarchical_anchor_closure_v1"
STRATIFIED_DIR = ROOT / "03_exposure_closure" / "multi_region_stratified_control_closure_v1"
CHAO = ROOT / "03_exposure_closure" / "chao_phraya_nature_model_v1"
OUTDIR = ROOT / "03_exposure_closure" / "hierarchical_model_v1"


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


def load_base() -> pd.DataFrame:
    bench = pd.read_csv(BENCHMARK)
    summary_exposure = pd.read_csv(SUMMARY_DIR / "multi_region_meta_closure_exposure_table.csv")
    blocked = pd.read_csv(BLOCKED_DIR / "multi_region_blocked_equal_area_region_table.csv")
    hybrid = pd.read_csv(HYBRID_DIR / "hierarchical_anchor_region_table.csv")
    stratified = pd.read_csv(STRATIFIED_DIR / "multi_region_stratified_control_comparison.csv")

    df = bench.merge(
        summary_exposure[
            [
                "region",
                "strong_cells",
                "strong_pop_not_majority_fraction",
                "strong_built_not_majority_fraction",
                "risk_proxy",
            ]
        ],
        on="region",
        how="left",
    ).merge(
        blocked[["region", "landcover_adjusted_or"]].rename(columns={"landcover_adjusted_or": "blocked_equal_area_or"}),
        on="region",
        how="left",
    ).merge(
        hybrid[["region", "cell_level"]],
        on="region",
        how="left",
    )

    df["log_or"] = np.log(df["landcover_adjusted_or"].astype(float))
    df["se"] = [
        derive_se_from_ci(float(lo), float(hi))
        for lo, hi in zip(df["landcover_adjusted_boot_q025"].astype(float), df["landcover_adjusted_boot_q975"].astype(float))
    ]
    df["var"] = df["se"] ** 2
    df["anchor_code"] = df["independent_anchor_status"].map(
        {
            "sparse_gnss_anchor": 0.0,
            "weak_or_missing_gnss_anchor": 1.0,
            "control_or_specification_case": -1.0,
        }
    ).astype(float)
    df["signal_code"] = df["observability_bias_signal"].map({"inconclusive": 0.0, "positive": 1.0, "strong_positive": 2.0}).astype(float)
    df["landcover_code"] = df["dominant_landcover"].astype("category").cat.codes.astype(float)
    df["n_cells_log"] = np.log1p(df["n_cells"].astype(float))
    df["strong_cells_log"] = np.log1p(df["strong_cells"].astype(float))
    df["hidden_share"] = pd.to_numeric(df["strong_pop_not_majority_fraction"], errors="coerce")
    df["built_hidden_share"] = pd.to_numeric(df["strong_built_not_majority_fraction"], errors="coerce")
    df.attrs["stratified_comparison"] = stratified.to_dict(orient="records")
    return df


def model_fit(df: pd.DataFrame, xcols: list[str]) -> dict[str, Any]:
    x = np.column_stack([np.ones(len(df), dtype=float)] + [df[c].astype(float).to_numpy() for c in xcols])
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    fit = ridge_wls(x, df["log_or"].to_numpy(), 1.0 / df["var"].to_numpy(), ridge=1e-3)
    rows = []
    names = ["intercept"] + xcols
    for i, name in enumerate(names):
        b = float(fit["beta"][i])
        s = float(fit["se"][i])
        rows.append(
            {
                "term": name,
                "beta": b,
                "se": s,
                "z": b / s if s > 0 else float("nan"),
                "or": float(math.exp(b)),
                "or_ci_low": float(math.exp(b - 1.96 * s)) if s > 0 else float("nan"),
                "or_ci_high": float(math.exp(b + 1.96 * s)) if s > 0 else float("nan"),
            }
        )

    loo = []
    for idx in range(len(df)):
        keep = np.ones(len(df), dtype=bool)
        keep[idx] = False
        sub = df.loc[keep]
        sub_fit = ridge_wls(
            np.nan_to_num(
                np.column_stack([np.ones(len(sub), dtype=float)] + [sub[c].astype(float).to_numpy() for c in xcols]),
                nan=0.0,
                posinf=0.0,
                neginf=0.0,
            ),
            sub["log_or"].to_numpy(),
            1.0 / sub["var"].to_numpy(),
            ridge=1e-3,
        )
        x0 = np.array([1.0] + [float(df.iloc[idx][c]) if pd.notna(df.iloc[idx][c]) else 0.0 for c in xcols], dtype=float)
        pred_log = float(x0 @ sub_fit["beta"])
        loo.append(
            {
                "left_out_region": df.iloc[idx]["region"],
                "observed_log_or": float(df.iloc[idx]["log_or"]),
                "predicted_log_or": pred_log,
                "abs_log_error": float(abs(pred_log - df.iloc[idx]["log_or"])),
                "observed_or": float(df.iloc[idx]["landcover_adjusted_or"]),
                "predicted_or": float(math.exp(pred_log)),
            }
        )

    loo_df = pd.DataFrame(loo)
    return {
        "coef": rows,
        "loo": loo_df,
        "mae": float(loo_df["abs_log_error"].mean()),
        "max_abs_error": float(loo_df["abs_log_error"].max()),
        "pred_min_or": float(loo_df["predicted_or"].min()),
        "pred_max_or": float(loo_df["predicted_or"].max()),
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = load_base()
    stratified_comparison = pd.DataFrame(df.attrs["stratified_comparison"])
    stratified_best = stratified_comparison.sort_values(["loo_mae", "reference_or"], ascending=[True, False]).iloc[0].to_dict()

    xcols = [
        "signal_code",
        "anchor_code",
        "n_cells_log",
        "cell_level",
    ]
    fit = model_fit(df, xcols)
    pooled = fixed_random_meta(df["log_or"].to_numpy(), df["var"].to_numpy())

    write_csv(OUTDIR / "hierarchical_model_coefficients.csv", fit["coef"], ["term", "beta", "se", "z", "or", "or_ci_low", "or_ci_high"])
    write_csv(
        OUTDIR / "hierarchical_model_leave_one_out.csv",
        fit["loo"].to_dict(orient="records"),
        ["left_out_region", "observed_log_or", "predicted_log_or", "abs_log_error", "observed_or", "predicted_or"],
    )

    comparison = [
        {
            "model_family": "summary_only_meta",
            "pooled_or": pooled["random_or"],
            "pooled_ci_low": pooled["random_ci_low"],
            "pooled_ci_high": pooled["random_ci_high"],
            "loo_mae": float("nan"),
            "loo_max_abs_error": float("nan"),
            "notes": "Frozen region-level random-effects benchmark.",
        },
        {
            "model_family": "hierarchical_anchor_stack",
            "pooled_or": 1.9646318688752513,
            "pooled_ci_low": 1.120580669991814,
            "pooled_ci_high": 3.4443837920321856,
            "loo_mae": fit["mae"],
            "loo_max_abs_error": fit["max_abs_error"],
            "notes": "Cell-anchored hybrid synthesis with region-level covariates.",
        },
        {
            "model_family": f"stratified_control_{stratified_best['family']}",
            "pooled_or": float(stratified_best["reference_or"]),
            "pooled_ci_low": float(stratified_best["reference_ci_low"]),
            "pooled_ci_high": float(stratified_best["reference_ci_high"]),
            "loo_mae": float(stratified_best["loo_mae"]),
            "loo_max_abs_error": float(stratified_best["loo_max_abs_error"]),
            "notes": "Frozen multi-stratum control ladder promoted from the gap-to-upgrade matrix.",
        },
    ]
    write_csv(
        OUTDIR / "hierarchical_model_comparison.csv",
        comparison,
        ["model_family", "pooled_or", "pooled_ci_low", "pooled_ci_high", "loo_mae", "loo_max_abs_error", "notes"],
    )

    report_lines = [
        "# Hierarchical Model Comparison v1",
        "",
        "This artifact compares the current region-level meta-analysis against a frozen cell-anchored hierarchical stack.",
        "",
        "## Model Family Comparison",
        "",
        "| model | pooled OR | 95% CI | loo MAE (log OR) | loo max abs error |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in comparison:
        mae = row["loo_mae"]
        max_err = row["loo_max_abs_error"]
        report_lines.append(
            f"| {row['model_family']} | {float(row['pooled_or']):.4f} | {float(row['pooled_ci_low']):.4f}-{float(row['pooled_ci_high']):.4f} | "
            f"{mae:.4f} | {max_err:.4f} |"
        )
    report_lines.extend(
        [
            "",
            "## Hierarchical Coefficients",
            "",
            "| term | beta | se | z | OR | 95% CI |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in fit["coef"]:
        report_lines.append(
            f"| {row['term']} | {float(row['beta']):.4f} | {float(row['se']):.4f} | {float(row['z']):.4f} | "
            f"{float(row['or']):.4f} | {float(row['or_ci_low']):.4f}-{float(row['or_ci_high']):.4f} |"
        )
    report_lines.extend(
        [
            "",
            "## Interpretation Guardrail",
            "",
            "- This is a frozen comparison, not a search over arbitrarily many model families.",
            "- The model uses the existing cell-level Chao Phraya anchor plus the regional benchmark covariates.",
            "- It improves the E5 layer by making the model-family decision auditable rather than purely narrative.",
        ]
    )
    (OUTDIR / "hierarchical_model_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    meta = {
        "artifact": "hierarchical_model_v1",
        "files": [
            "hierarchical_model_coefficients.csv",
            "hierarchical_model_leave_one_out.csv",
            "hierarchical_model_comparison.csv",
            "hierarchical_model_report.md",
        ],
        "pooled_or": pooled["random_or"],
        "pooled_ci_low": pooled["random_ci_low"],
        "pooled_ci_high": pooled["random_ci_high"],
        "hierarchical_stack_loo_mae": fit["mae"],
        "hierarchical_stack_loo_max_abs_error": fit["max_abs_error"],
    }
    (OUTDIR / "hierarchical_model_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
