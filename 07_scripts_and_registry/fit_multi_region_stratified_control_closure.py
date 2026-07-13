from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
SUMMARY = ROOT / "03_exposure_closure" / "multi_region_summary_meta_closure_v1" / "multi_region_meta_closure_exposure_table.csv"
BLOCKED = ROOT / "03_exposure_closure" / "multi_region_blocked_equal_area_closure_v1" / "multi_region_blocked_equal_area_region_table.csv"
HYBRID = ROOT / "03_exposure_closure" / "hierarchical_anchor_closure_v1" / "hierarchical_anchor_region_table.csv"
OUTDIR = ROOT / "03_exposure_closure" / "multi_region_stratified_control_closure_v1"


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z]+", "_", text.strip().lower()).strip("_")
    return slug or "term"


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
    se_re = math.sqrt(1.0 / np.sum(wr))
    return {
        "k": float(len(log_or)),
        "random_log_or": re,
        "random_or": float(math.exp(re)),
        "random_ci_low": float(math.exp(re - 1.96 * se_re)),
        "random_ci_high": float(math.exp(re + 1.96 * se_re)),
        "q": q,
        "tau2": tau2,
        "i2": max(0.0, (q - df) / q) if q > 0 else 0.0,
    }


def derive_se_from_ci(lo: float, hi: float) -> float:
    return (math.log(hi) - math.log(lo)) / (2.0 * 1.96)


def load_frame() -> pd.DataFrame:
    bench = pd.read_csv(BENCHMARK)
    summary = pd.read_csv(SUMMARY)
    blocked = pd.read_csv(BLOCKED)
    hybrid = pd.read_csv(HYBRID)

    df = bench.merge(
        summary[
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
        blocked[["region", "landcover_adjusted_or", "equal_area_weight", "strong_area_weight"]].rename(
            columns={"landcover_adjusted_or": "blocked_equal_area_or"}
        ),
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

    df["signal_code"] = df["observability_bias_signal"].map({"inconclusive": 0.0, "positive": 1.0, "strong_positive": 2.0}).astype(float)
    df["anchor_code"] = df["independent_anchor_status"].map(
        {"sparse_gnss_anchor": 0.0, "weak_or_missing_gnss_anchor": 1.0, "control_or_specification_case": -1.0}
    ).astype(float)

    df["n_cells_log"] = np.log1p(df["n_cells"].astype(float))
    df["strong_cells_log"] = np.log1p(pd.to_numeric(df["strong_cells"], errors="coerce"))
    df["cell_level"] = pd.to_numeric(df["cell_level"], errors="coerce")
    df["cropland_fraction"] = pd.to_numeric(df["cropland_fraction"], errors="coerce")
    df["built_up_fraction"] = pd.to_numeric(df["built_up_fraction"], errors="coerce")
    df["water_wetland_mangrove_fraction"] = pd.to_numeric(df["water_wetland_mangrove_fraction"], errors="coerce")
    df["hidden_share"] = pd.to_numeric(df["strong_pop_not_majority_fraction"], errors="coerce")
    df["built_hidden_share"] = pd.to_numeric(df["strong_built_not_majority_fraction"], errors="coerce")

    # One-hot landcover controls. Cropland is the baseline.
    baseline = "cropland"
    categories = sorted({str(item) for item in df["dominant_landcover"].dropna().astype(str)})
    for category in categories:
        if category == baseline:
            continue
        slug = slugify(category)
        df[f"landcover_{slug}"] = (df["dominant_landcover"].astype(str) == category).astype(float)

    return df


def zscore_train_test(train: pd.DataFrame, test: pd.DataFrame, cols: list[str]) -> tuple[np.ndarray, np.ndarray, dict[str, tuple[float, float]]]:
    train_cols = []
    test_cols = []
    meta: dict[str, tuple[float, float]] = {}
    for col in cols:
        train_values = pd.to_numeric(train[col], errors="coerce").astype(float).to_numpy()
        test_values = pd.to_numeric(test[col], errors="coerce").astype(float).to_numpy()
        mean = float(np.nanmean(train_values))
        std = float(np.nanstd(train_values))
        if not np.isfinite(std) or std == 0.0:
            std = 1.0
        train_values = np.where(np.isfinite(train_values), train_values, mean)
        test_values = np.where(np.isfinite(test_values), test_values, mean)
        train_cols.append((train_values - mean) / std)
        test_cols.append((test_values - mean) / std)
        meta[col] = (mean, std)
    return np.column_stack(train_cols), np.column_stack(test_cols), meta


def ridge_wls(x: np.ndarray, y: np.ndarray, var: np.ndarray, ridge: float = 1e-3) -> dict[str, np.ndarray]:
    w = 1.0 / var
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


def fit_family(df: pd.DataFrame, xcols: list[str]) -> dict[str, Any]:
    if not xcols:
        pooled = fixed_random_meta(df["log_or"].to_numpy(), df["var"].to_numpy())
        return {
            "family": "summary_only_meta",
            "reference_or": pooled["random_or"],
            "reference_ci_low": pooled["random_ci_low"],
            "reference_ci_high": pooled["random_ci_high"],
            "loo_mae": float("nan"),
            "loo_max_abs_error": float("nan"),
            "coef_rows": [],
            "loo_rows": [],
            "notes": "Frozen random-effects benchmark with no additional covariates.",
        }

    x_train, _, meta = zscore_train_test(df, df, xcols)
    x = np.column_stack([np.ones(len(df), dtype=float), x_train])
    fit = ridge_wls(x, df["log_or"].to_numpy(), df["var"].to_numpy())

    coef_rows = []
    names = ["intercept"] + xcols
    for i, name in enumerate(names):
        beta = float(fit["beta"][i])
        se = float(fit["se"][i])
        coef_rows.append(
            {
                "term": name,
                "beta": beta,
                "se": se,
                "z": beta / se if se > 0 else float("nan"),
                "or": float(math.exp(beta)),
                "or_ci_low": float(math.exp(beta - 1.96 * se)) if se > 0 else float("nan"),
                "or_ci_high": float(math.exp(beta + 1.96 * se)) if se > 0 else float("nan"),
            }
        )

    loo_rows = []
    for idx in range(len(df)):
        train = df.drop(index=idx)
        test = df.iloc[[idx]]
        x_train, x_test, _ = zscore_train_test(train, test, xcols)
        xfit = np.column_stack([np.ones(len(train), dtype=float), x_train])
        x0 = np.column_stack([np.ones(len(test), dtype=float), x_test])
        subfit = ridge_wls(xfit, train["log_or"].to_numpy(), train["var"].to_numpy())
        pred_log = float((x0 @ subfit["beta"]).ravel()[0])
        loo_rows.append(
            {
                "left_out_region": str(test.iloc[0]["region"]),
                "observed_log_or": float(test.iloc[0]["log_or"]),
                "predicted_log_or": pred_log,
                "abs_log_error": float(abs(pred_log - test.iloc[0]["log_or"])),
                "observed_or": float(test.iloc[0]["landcover_adjusted_or"]),
                "predicted_or": float(math.exp(pred_log)),
            }
        )

    loo_df = pd.DataFrame(loo_rows)
    reference_or = float(math.exp(fit["beta"][0]))
    reference_ci_low = float(math.exp(fit["beta"][0] - 1.96 * fit["se"][0]))
    reference_ci_high = float(math.exp(fit["beta"][0] + 1.96 * fit["se"][0]))

    return {
        "family": "stratified_" + "_".join(slugify(col) for col in xcols[:3]) if len(xcols) <= 3 else "stratified_control_stack",
        "reference_or": reference_or,
        "reference_ci_low": reference_ci_low,
        "reference_ci_high": reference_ci_high,
        "loo_mae": float(loo_df["abs_log_error"].mean()),
        "loo_max_abs_error": float(loo_df["abs_log_error"].max()),
        "coef_rows": coef_rows,
        "loo_rows": loo_df.to_dict(orient="records"),
        "notes": "Frozen control-family comparison with standardized predictors and leave-one-out refits.",
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = load_frame()

    landcover_cols = [col for col in df.columns if col.startswith("landcover_")]
    family_specs = [
        ("summary_only_meta", []),
        ("landcover_size_stack", ["signal_code", "anchor_code", "n_cells_log", *landcover_cols]),
        ("exposure_composition_stack", ["signal_code", "anchor_code", "n_cells_log", "strong_cells_log", "cropland_fraction", "built_up_fraction", "water_wetland_mangrove_fraction"]),
        ("hidden_stratified_stack", ["signal_code", "anchor_code", "n_cells_log", "strong_cells_log", "hidden_share", "built_hidden_share", "cell_level"]),
        (
            "full_stratified_control_stack",
            [
                "signal_code",
                "anchor_code",
                "n_cells_log",
                "strong_cells_log",
                "hidden_share",
                "built_hidden_share",
                "cell_level",
                "cropland_fraction",
                "built_up_fraction",
                "water_wetland_mangrove_fraction",
                *landcover_cols,
            ],
        ),
    ]

    results: list[dict[str, Any]] = []
    all_coef_rows: list[dict[str, Any]] = []
    all_loo_rows: list[dict[str, Any]] = []
    for family, xcols in family_specs:
        fit = fit_family(df, xcols)
        results.append(
            {
                "family": family,
                "reference_or": fit["reference_or"],
                "reference_ci_low": fit["reference_ci_low"],
                "reference_ci_high": fit["reference_ci_high"],
                "loo_mae": fit["loo_mae"],
                "loo_max_abs_error": fit["loo_max_abs_error"],
                "n_terms": len(xcols),
                "notes": fit["notes"],
            }
        )
        for row in fit["coef_rows"]:
            row_out = dict(row)
            row_out["family"] = family
            all_coef_rows.append(row_out)
        for row in fit["loo_rows"]:
            row_out = dict(row)
            row_out["family"] = family
            all_loo_rows.append(row_out)

    results = sorted(results, key=lambda row: (math.inf if not np.isfinite(row["loo_mae"]) else row["loo_mae"], row["family"]))
    write_csv(
        OUTDIR / "multi_region_stratified_control_comparison.csv",
        results,
        ["family", "reference_or", "reference_ci_low", "reference_ci_high", "loo_mae", "loo_max_abs_error", "n_terms", "notes"],
    )
    write_csv(
        OUTDIR / "multi_region_stratified_control_coefficients.csv",
        all_coef_rows,
        ["family", "term", "beta", "se", "z", "or", "or_ci_low", "or_ci_high"],
    )
    write_csv(
        OUTDIR / "multi_region_stratified_control_leave_one_out.csv",
        all_loo_rows,
        ["family", "left_out_region", "observed_log_or", "predicted_log_or", "abs_log_error", "observed_or", "predicted_or"],
    )

    report = [
        "# Multi-Region Stratified Control Closure v1",
        "",
        "This artifact freezes a compact family of region-level control models and checks whether the pooled signal remains > 1 under progressively richer controls.",
        "",
        "## Model Family Comparison",
        "",
        "| family | reference OR | 95% CI | loo MAE (log OR) | loo max abs error | terms |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        report.append(
            f"| {row['family']} | {float(row['reference_or']):.4f} | {float(row['reference_ci_low']):.4f}-{float(row['reference_ci_high']):.4f} | "
            f"{row['loo_mae']:.4f} | {row['loo_max_abs_error']:.4f} | {int(row['n_terms'])} |"
        )

    report.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The comparison is frozen: the candidate families were defined up front from the available region tables.",
            "- The richer control stacks add landcover composition, exposure composition, hidden-share summaries, and the cell-level anchor code.",
            "- If the reference OR stays above 1 across the control stacks, the core lowballing signal is not an artifact of one narrow specification.",
            "",
            "## Guardrail",
            "",
            "- This is not a search over unlimited model variants.",
            "- It is a constrained robustness ladder intended to strengthen the current Nature-level evidence package.",
        ]
    )
    (OUTDIR / "multi_region_stratified_control_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    meta = {
        "artifact": "multi_region_stratified_control_closure_v1",
        "source": str(BENCHMARK.relative_to(ROOT)),
        "files": [
            "multi_region_stratified_control_comparison.csv",
            "multi_region_stratified_control_coefficients.csv",
            "multi_region_stratified_control_leave_one_out.csv",
            "multi_region_stratified_control_report.md",
        ],
        "families": [name for name, _ in family_specs],
        "n_regions": int(len(df)),
        "best_family": results[0]["family"] if results else None,
    }
    (OUTDIR / "multi_region_stratified_control_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
