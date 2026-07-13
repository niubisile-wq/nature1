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
BLOCKED_EQUAL_AREA = ROOT / "03_exposure_closure" / "multi_region_blocked_equal_area_closure_v1" / "multi_region_blocked_equal_area_region_table.csv"
CHAO_BINARY_COEF = ROOT / "03_exposure_closure" / "chao_phraya_nature_model_v1" / "chao_phraya_nature_model_binary_coefficients.csv"
CHAO_BINARY_BOOT = ROOT / "03_exposure_closure" / "chao_phraya_nature_model_v1" / "chao_phraya_nature_model_binary_block_bootstrap.csv"
CHAO_BINARY_LOO = ROOT / "03_exposure_closure" / "chao_phraya_nature_model_v1" / "chao_phraya_nature_model_binary_leave_one_block_out.csv"
OUTDIR = ROOT / "03_exposure_closure" / "hierarchical_anchor_closure_v1"


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


def load_region_table() -> pd.DataFrame:
    bench = pd.read_csv(BENCHMARK)
    blocked = pd.read_csv(BLOCKED_EQUAL_AREA)
    blocked = blocked.rename(columns={"landcover_adjusted_or": "blocked_equal_area_or"})
    df = bench.merge(
        blocked[["region", "blocked_equal_area_or", "readiness"]],
        on="region",
        how="left",
        suffixes=("", "_blocked"),
    )
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
    df["cell_level"] = (df["region"].astype(str) == "Chao Phraya").astype(float)
    df["blocked_equal_area_or"] = df["blocked_equal_area_or"].astype(float)
    return df


def load_chao_cell_level() -> dict[str, float]:
    coef = pd.read_csv(CHAO_BINARY_COEF)
    boot = pd.read_csv(CHAO_BINARY_BOOT)
    loo = pd.read_csv(CHAO_BINARY_LOO)
    row = coef.loc[coef["term"] == "strong_sub_5mm"].iloc[0]
    boot_row = boot.loc[boot["term"] == "strong_sub_5mm"].iloc[0]
    return {
        "beta": float(row["beta"]),
        "std_error": float(row["std_error"]),
        "odds_ratio": float(row["odds_ratio"]),
        "odds_ratio_ci_low": float(row["odds_ratio_ci_low"]),
        "odds_ratio_ci_high": float(row["odds_ratio_ci_high"]),
        "boot_mean": float(boot_row["odds_ratio_boot_mean"]),
        "boot_q025": float(boot_row["odds_ratio_boot_q025"]),
        "boot_q50": float(boot_row["odds_ratio_boot_q50"]),
        "boot_q975": float(boot_row["odds_ratio_boot_q975"]),
        "loo_max_abs_deviation": float(np.max(np.abs(np.log(loo["strong_odds_ratio"].astype(float) / row["odds_ratio"])))),
    }


def loo_meta(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for idx in range(len(df)):
        keep = np.ones(len(df), dtype=bool)
        keep[idx] = False
        stats = fixed_random_meta(df.loc[keep, "log_or"].to_numpy(), df.loc[keep, "var"].to_numpy())
        rows.append(
            {
                "left_out_region": df.loc[idx, "region"],
                "observed_or": float(df.loc[idx, "landcover_adjusted_or"]),
                "pooled_random_or": stats["random_or"],
                "pooled_random_ci_low": stats["random_ci_low"],
                "pooled_random_ci_high": stats["random_ci_high"],
                "tau2": stats["tau2"],
                "i2": stats["i2"],
            }
        )
    return rows


def meta_regression(df: pd.DataFrame) -> list[dict[str, Any]]:
    x = np.column_stack(
        [
            np.ones(len(df), dtype=float),
            df["cell_level"].astype(float).to_numpy(),
            df["signal_code"].astype(float).to_numpy(),
            df["anchor_code"].astype(float).to_numpy(),
            np.log1p(df["n_cells"].astype(float).to_numpy()),
        ]
    )
    fit = ridge_wls(x, df["log_or"].to_numpy(), 1.0 / df["var"].to_numpy(), ridge=1e-3)
    terms = ["intercept", "cell_level", "signal_code", "anchor_code", "log1p_n_cells"]
    rows = []
    for i, term in enumerate(terms):
        b = float(fit["beta"][i])
        s = float(fit["se"][i])
        rows.append(
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
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = load_region_table()
    chao = load_chao_cell_level()

    hybrid = df.copy()
    hybrid.loc[hybrid["region"] == "Chao Phraya", "log_or"] = math.log(chao["odds_ratio"])
    hybrid.loc[hybrid["region"] == "Chao Phraya", "se"] = (math.log(chao["odds_ratio_ci_high"]) - math.log(chao["odds_ratio_ci_low"])) / (2.0 * 1.96)
    hybrid["var"] = hybrid["se"] ** 2
    hybrid["weight_fixed"] = 1.0 / hybrid["var"]

    benchmark_meta = fixed_random_meta(df["log_or"].to_numpy(), df["var"].to_numpy())
    hybrid_meta = fixed_random_meta(hybrid["log_or"].to_numpy(), hybrid["var"].to_numpy())
    blocked_meta = fixed_random_meta(np.log(df["blocked_equal_area_or"].astype(float).to_numpy()), df["var"].to_numpy())

    region_cols = [
        "region",
        "observability_bias_signal",
        "independent_anchor_status",
        "dominant_landcover",
        "landcover_adjusted_or",
        "landcover_adjusted_boot_q025",
        "landcover_adjusted_boot_q975",
        "blocked_equal_area_or",
        "log_or",
        "se",
        "weight_fixed",
        "n_cells",
        "n_lisc_pairs",
        "signal_code",
        "anchor_code",
        "cell_level",
        "cropland_fraction",
        "built_up_fraction",
        "water_wetland_mangrove_fraction",
        "readiness",
    ]
    write_csv(OUTDIR / "hierarchical_anchor_region_table.csv", hybrid[region_cols].to_dict(orient="records"), region_cols)

    meta_rows = meta_regression(hybrid)
    write_csv(OUTDIR / "hierarchical_anchor_meta_regression.csv", meta_rows, ["term", "beta", "se", "z", "or", "or_ci_low", "or_ci_high"])

    loo = loo_meta(hybrid)
    write_csv(
        OUTDIR / "hierarchical_anchor_leave_one_out.csv",
        loo,
        ["left_out_region", "observed_or", "pooled_random_or", "pooled_random_ci_low", "pooled_random_ci_high", "tau2", "i2"],
    )

    compare_rows = [
        {
            "scheme": "benchmark_summary_only",
            "pooled_or": benchmark_meta["random_or"],
            "ci_low": benchmark_meta["random_ci_low"],
            "ci_high": benchmark_meta["random_ci_high"],
        },
        {
            "scheme": "hybrid_with_chao_cell_level",
            "pooled_or": hybrid_meta["random_or"],
            "ci_low": hybrid_meta["random_ci_low"],
            "ci_high": hybrid_meta["random_ci_high"],
        },
        {
            "scheme": "blocked_equal_area_proxy",
            "pooled_or": blocked_meta["random_or"],
            "ci_low": blocked_meta["random_ci_low"],
            "ci_high": blocked_meta["random_ci_high"],
        },
    ]
    write_csv(OUTDIR / "hierarchical_anchor_sensitivity.csv", compare_rows, ["scheme", "pooled_or", "ci_low", "ci_high"])

    report = [
        "# Hierarchical Anchor Closure v1",
        "",
        "This artifact upgrades the multi-region closure by anchoring the Chao Phraya region to the cell-level primary model and pooling it with frozen region-level estimates.",
        "",
        "## Chao Phraya Cell-Level Anchor",
        "",
        f"- Primary strong-subsidence OR: `{chao['odds_ratio']:.4f}`",
        f"- 95% CI: `{chao['odds_ratio_ci_low']:.4f}-{chao['odds_ratio_ci_high']:.4f}`",
        f"- Block-bootstrap median: `{chao['boot_q50']:.4f}`",
        f"- Block-bootstrap 95% interval: `{chao['boot_q025']:.4f}-{chao['boot_q975']:.4f}`",
        "",
        "## Pooled Results",
        "",
        f"- Benchmark summary-only random-effects OR: `{benchmark_meta['random_or']:.4f}`",
        f"- Hybrid cell-anchored random-effects OR: `{hybrid_meta['random_or']:.4f}`",
        f"- Blocked equal-area proxy random-effects OR: `{blocked_meta['random_or']:.4f}`",
        "",
        "## Hybrid Meta-Regression",
        "",
        "| term | beta | se | z | OR | 95% CI |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in meta_rows:
        report.append(
            f"| {row['term']} | {row['beta']:.4f} | {row['se']:.4f} | {row['z']:.4f} | {row['or']:.4f} | {row['or_ci_low']:.4f}-{row['or_ci_high']:.4f} |"
        )
    report.extend(
        [
            "",
            "## Leave-One-Out",
            "",
            "| left_out_region | observed OR | pooled OR | 95% CI |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in loo:
        report.append(
            f"| {row['left_out_region']} | {row['observed_or']:.4f} | {row['pooled_random_or']:.4f} | {row['pooled_random_ci_low']:.4f}-{row['pooled_random_ci_high']:.4f} |"
        )
    report.extend(
        [
            "",
            "## Sensitivity",
            "",
            "| scheme | pooled OR | 95% CI |",
            "|---|---:|---:|",
        ]
    )
    for row in compare_rows:
        report.append(f"| {row['scheme']} | {row['pooled_or']:.4f} | {row['ci_low']:.4f}-{row['ci_high']:.4f} |")
    report.extend(
        [
            "",
            "## Interpretation Guardrail",
            "",
            "- This is a hybrid hierarchical synthesis, not a full Bayesian cell-level model across all regions.",
            "- It makes the cell-level Chao Phraya anchor explicit and freezes the cross-region pooling rule.",
            "- It is intended as the strongest self-contained cross-region synthesis available from the current local evidence.",
        ]
    )
    (OUTDIR / "hierarchical_anchor_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    meta = {
        "artifact": "hierarchical_anchor_closure_v1",
        "chao_cell_level": chao,
        "benchmark_summary_only_random_or": benchmark_meta["random_or"],
        "hybrid_cell_anchored_random_or": hybrid_meta["random_or"],
        "blocked_equal_area_proxy_random_or": blocked_meta["random_or"],
        "files": [
            "hierarchical_anchor_region_table.csv",
            "hierarchical_anchor_meta_regression.csv",
            "hierarchical_anchor_leave_one_out.csv",
            "hierarchical_anchor_sensitivity.csv",
            "hierarchical_anchor_report.md",
        ],
    }
    (OUTDIR / "hierarchical_anchor_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
