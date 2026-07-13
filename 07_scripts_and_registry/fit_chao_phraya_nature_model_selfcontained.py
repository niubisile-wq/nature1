from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
DEFAULT_CELL_CSV = ROOT / "03_exposure_closure" / "chao_phraya_area_weighted_exposure_censoring" / "chao_phraya_area_weighted_exposure_cells.csv"
DEFAULT_SUMMARY_CSV = ROOT / "03_exposure_closure" / "multi_delta_vlm_exposure_censoring_summary.csv"


def log1p_safe(values: np.ndarray) -> np.ndarray:
    return np.log1p(np.clip(values.astype(float), a_min=0.0, a_max=None))


def standardize(x: np.ndarray) -> tuple[np.ndarray, float, float]:
    mean = float(np.mean(x))
    std = float(np.std(x))
    if not np.isfinite(std) or std == 0.0:
        std = 1.0
    return (x - mean) / std, mean, std


def make_blocks(row: np.ndarray, col: np.ndarray, block_size: int) -> np.ndarray:
    return (row // block_size).astype(int) * 10000 + (col // block_size).astype(int)


def design_matrix(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    successes = df["observable_count"].astype(float).to_numpy()
    if "n_pairs" in df.columns:
        trials = df["n_pairs"].astype(float).to_numpy()
    else:
        observable_fraction = df["observable_fraction"].astype(float).to_numpy()
        with np.errstate(divide="ignore", invalid="ignore"):
            inferred = successes[observable_fraction > 0] / observable_fraction[observable_fraction > 0]
        if len(inferred) == 0:
            raise ValueError("cannot infer n_pairs because all observable_fraction values are zero")
        inferred_n_pairs = float(np.rint(np.median(inferred)))
        trials = np.full(len(df), inferred_n_pairs, dtype=float)
    keep = np.isfinite(trials) & (trials > 0)
    df = df.loc[keep].reset_index(drop=True)
    successes = successes[keep]
    trials = trials[keep]
    strong = df["strong_sub_5mm"].astype(float).to_numpy()
    pop = log1p_safe(df["population_weighted"].to_numpy())
    built = log1p_safe(df["builtup_m2_weighted"].to_numpy())
    row = df["row"].astype(float).to_numpy()
    col = df["col"].astype(float).to_numpy()
    row_z, row_mean, row_std = standardize(row)
    col_z, col_mean, col_std = standardize(col)
    pop_z, pop_mean, pop_std = standardize(pop)
    built_z, built_mean, built_std = standardize(built)

    x = np.column_stack(
        [
            np.ones(len(df), dtype=float),
            strong,
            pop_z,
            built_z,
            row_z,
            col_z,
            strong * pop_z,
            strong * built_z,
        ]
    )
    meta = {
        "terms": [
            "intercept",
            "strong_sub_5mm",
            "log1p_population_weighted_z",
            "log1p_builtup_m2_weighted_z",
            "row_z",
            "col_z",
            "strong_x_log1p_population_weighted_z",
            "strong_x_log1p_builtup_m2_weighted_z",
        ],
        "row_mean": row_mean,
        "row_std": row_std,
        "col_mean": col_mean,
        "col_std": col_std,
        "population_log1p_mean": pop_mean,
        "population_log1p_std": pop_std,
        "builtup_log1p_mean": built_mean,
        "builtup_log1p_std": built_std,
        "n_rows_dropped": int(np.sum(~keep)),
    }
    return x, successes, trials, meta


def fit_binomial_newton(
    x: np.ndarray,
    successes: np.ndarray,
    trials: np.ndarray,
    ridge: float = 1e-6,
    max_iter: int = 100,
    tol: float = 1e-9,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    beta = np.zeros(x.shape[1], dtype=float)
    eye = np.eye(x.shape[1], dtype=float)
    eye[0, 0] = 0.0
    converged = False
    n_iter = 0
    for n_iter in range(1, max_iter + 1):
        eta = x @ beta
        p = expit(eta)
        var = np.clip(trials * p * (1.0 - p), 1e-12, None)
        z = eta + (successes - trials * p) / var
        xtw = x.T * var
        h = xtw @ x + ridge * eye
        g = xtw @ z
        try:
            beta_new = np.linalg.solve(h, g)
        except np.linalg.LinAlgError:
            beta_new = np.linalg.lstsq(h, g, rcond=None)[0]
        delta = np.max(np.abs(beta_new - beta))
        beta = beta_new
        if delta < tol:
            converged = True
            break
    eta = x @ beta
    p = expit(eta)
    var = np.clip(trials * p * (1.0 - p), 1e-12, None)
    xtw = x.T * var
    h = xtw @ x + ridge * eye
    try:
        cov = np.linalg.inv(h)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(h)
    ll = np.sum(
        successes * np.log(np.clip(p, 1e-15, 1.0)) + (trials - successes) * np.log(np.clip(1.0 - p, 1e-15, 1.0))
    )
    meta = {"converged": converged, "n_iter": n_iter, "log_likelihood": float(ll)}
    return beta, cov, meta


def coef_rows(beta: np.ndarray, cov: np.ndarray, terms: list[str]) -> list[dict[str, Any]]:
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    rows = []
    for i, term in enumerate(terms):
        b = float(beta[i])
        s = float(se[i])
        z = b / s if s > 0 else float("nan")
        rows.append(
            {
                "term": term,
                "beta": b,
                "std_error": s,
                "z": z,
                "odds_ratio": float(math.exp(b)),
                "odds_ratio_ci_low": float(math.exp(b - 1.96 * s)) if s > 0 else float("nan"),
                "odds_ratio_ci_high": float(math.exp(b + 1.96 * s)) if s > 0 else float("nan"),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def block_bootstrap(
    df: pd.DataFrame,
    x: np.ndarray,
    successes: np.ndarray,
    trials: np.ndarray,
    meta: dict[str, Any],
    block_size: int,
    n_bootstrap: int,
    seed: int,
    ridge: float,
) -> tuple[list[dict[str, Any]], int]:
    blocks = make_blocks(df["row"].to_numpy(), df["col"].to_numpy(), block_size)
    unique_blocks = np.unique(blocks)
    rng = np.random.default_rng(seed)
    estimates: dict[str, list[float]] = {term: [] for term in meta["terms"][1:]}
    failures = 0
    for _ in range(n_bootstrap):
        sampled_blocks = rng.choice(unique_blocks, size=len(unique_blocks), replace=True)
        idx = np.concatenate([np.where(blocks == block)[0] for block in sampled_blocks])
        try:
            beta_b, cov_b, fit_meta = fit_binomial_newton(x[idx], successes[idx], trials[idx], ridge=ridge)
            if not fit_meta["converged"] or not np.all(np.isfinite(beta_b)):
                failures += 1
                continue
            for term in estimates:
                estimates[term].append(float(math.exp(beta_b[meta["terms"].index(term)])))
        except Exception:
            failures += 1
    rows = []
    for term, vals in estimates.items():
        arr = np.asarray(vals, dtype=float)
        if len(arr) == 0:
            rows.append(
                {
                    "term": term,
                    "n_success": 0,
                    "n_failed": failures,
                    "odds_ratio_boot_mean": float("nan"),
                    "odds_ratio_boot_q025": float("nan"),
                    "odds_ratio_boot_q50": float("nan"),
                    "odds_ratio_boot_q975": float("nan"),
                }
            )
            continue
        rows.append(
            {
                "term": term,
                "n_success": len(arr),
                "n_failed": failures,
                "odds_ratio_boot_mean": float(np.mean(arr)),
                "odds_ratio_boot_q025": float(np.quantile(arr, 0.025)),
                "odds_ratio_boot_q50": float(np.quantile(arr, 0.5)),
                "odds_ratio_boot_q975": float(np.quantile(arr, 0.975)),
            }
        )
    return rows, failures


def leave_one_block_out(
    df: pd.DataFrame,
    x: np.ndarray,
    successes: np.ndarray,
    trials: np.ndarray,
    meta: dict[str, Any],
    block_size: int,
    ridge: float,
) -> list[dict[str, Any]]:
    blocks = make_blocks(df["row"].to_numpy(), df["col"].to_numpy(), block_size)
    rows = []
    for block in np.unique(blocks):
        keep = blocks != block
        try:
            beta_b, cov_b, fit_meta = fit_binomial_newton(x[keep], successes[keep], trials[keep], ridge=ridge)
            idx = meta["terms"].index("strong_sub_5mm")
            rows.append(
                {
                    "left_out_block": int(block),
                    "n_cells_left_out": int(np.sum(~keep)),
                    "converged": fit_meta["converged"],
                    "strong_beta": float(beta_b[idx]),
                    "strong_odds_ratio": float(math.exp(beta_b[idx])),
                    "strong_ci_low": float(math.exp(beta_b[idx] - 1.96 * math.sqrt(max(cov_b[idx, idx], 0.0)))),
                    "strong_ci_high": float(math.exp(beta_b[idx] + 1.96 * math.sqrt(max(cov_b[idx, idx], 0.0)))),
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "left_out_block": int(block),
                    "n_cells_left_out": int(np.sum(~keep)),
                    "converged": False,
                    "strong_beta": "",
                    "strong_odds_ratio": "",
                    "strong_ci_low": "",
                    "strong_ci_high": "",
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Self-contained Chao Phraya Nature-standard lead-case model.")
    parser.add_argument("--cell-csv", type=Path, default=DEFAULT_CELL_CSV)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_SUMMARY_CSV)
    parser.add_argument("--outdir", type=Path, default=ROOT / "03_exposure_closure" / "chao_phraya_nature_model_v1")
    parser.add_argument("--block-size", type=int, default=5)
    parser.add_argument("--n-bootstrap", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260710)
    parser.add_argument("--ridge", type=float, default=1e-6)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.cell_csv)
    if "observable_count" not in df.columns or "observable_fraction" not in df.columns:
        raise ValueError("cell csv does not contain observable_count / observable_fraction")
    x, successes, trials, meta = design_matrix(df)
    beta, cov, fit_meta = fit_binomial_newton(x, successes, trials, ridge=args.ridge)
    coefs = coef_rows(beta, cov, meta["terms"])
    boot_rows, boot_failures = block_bootstrap(df, x, successes, trials, meta, args.block_size, args.n_bootstrap, args.seed, args.ridge)
    lobo_rows = leave_one_block_out(df, x, successes, trials, meta, args.block_size, args.ridge)

    # Supplementary binary model for not-majority observability.
    y_binary = df["not_majority_observable"].astype(float).to_numpy()
    row_z, _, _ = standardize(df["row"].astype(float).to_numpy())
    col_z, _, _ = standardize(df["col"].astype(float).to_numpy())
    xb = np.column_stack([np.ones(len(df), dtype=float), df["strong_sub_5mm"].astype(float).to_numpy(), row_z, col_z])
    binary_meta = {"terms": ["intercept", "strong_sub_5mm", "row_z", "col_z"]}
    beta_b, cov_b, fit_b = fit_binomial_newton(xb, y_binary, np.ones(len(df), dtype=float), ridge=args.ridge)
    coef_b = coef_rows(beta_b, cov_b, binary_meta["terms"])
    boot_b, boot_b_failures = block_bootstrap(
        df,
        xb,
        y_binary,
        np.ones(len(df), dtype=float),
        binary_meta,
        args.block_size,
        args.n_bootstrap,
        args.seed,
        args.ridge,
    )
    lobo_b = leave_one_block_out(
        df,
        xb,
        y_binary,
        np.ones(len(df), dtype=float),
        binary_meta,
        args.block_size,
        args.ridge,
    )

    summary = pd.read_csv(args.summary_csv)
    chao_summary = summary.loc[summary["delta"] == "Chao Phraya"].iloc[0].to_dict() if "delta" in summary.columns and any(summary["delta"] == "Chao Phraya") else {}
    po_summary = summary.loc[summary["delta"] == "Po"].iloc[0].to_dict() if "delta" in summary.columns and any(summary["delta"] == "Po") else {}

    coef_fields = ["term", "beta", "std_error", "z", "odds_ratio", "odds_ratio_ci_low", "odds_ratio_ci_high"]
    boot_fields = ["term", "n_success", "n_failed", "odds_ratio_boot_mean", "odds_ratio_boot_q025", "odds_ratio_boot_q50", "odds_ratio_boot_q975"]
    lobo_fields = ["left_out_block", "n_cells_left_out", "converged", "strong_beta", "strong_odds_ratio", "strong_ci_low", "strong_ci_high"]
    write_csv(args.outdir / "chao_phraya_nature_model_coefficients.csv", coefs, coef_fields)
    write_csv(args.outdir / "chao_phraya_nature_model_block_bootstrap.csv", boot_rows, boot_fields)
    write_csv(args.outdir / "chao_phraya_nature_model_leave_one_block_out.csv", lobo_rows, lobo_fields)
    write_csv(args.outdir / "chao_phraya_nature_model_binary_coefficients.csv", coef_b, coef_fields)
    write_csv(args.outdir / "chao_phraya_nature_model_binary_block_bootstrap.csv", boot_b, boot_fields)
    write_csv(args.outdir / "chao_phraya_nature_model_binary_leave_one_block_out.csv", lobo_b, lobo_fields)

    model_summary = {
        "cell_csv": str(args.cell_csv),
        "summary_csv": str(args.summary_csv),
        "n_cells": int(len(df)),
        "n_blocks": int(len(np.unique(make_blocks(df["row"].to_numpy(), df["col"].to_numpy(), args.block_size)))),
        "block_size": args.block_size,
        "n_bootstrap": args.n_bootstrap,
        "seed": args.seed,
        "ridge": args.ridge,
        "fit": fit_meta,
        "summary_rows": {
            "Chao Phraya": chao_summary,
            "Po": po_summary,
        },
        "bootstrap_failures": int(boot_failures),
        "binary_fit": fit_b,
        "binary_bootstrap_failures": int(boot_b_failures),
    }
    (args.outdir / "chao_phraya_nature_model_meta.json").write_text(json.dumps(model_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    strong_row = next(row for row in coefs if row["term"] == "strong_sub_5mm")
    pop_row = next(row for row in coefs if row["term"] == "log1p_population_weighted_z")
    built_row = next(row for row in coefs if row["term"] == "log1p_builtup_m2_weighted_z")
    boot_lookup = {row["term"]: row for row in boot_rows}

    report = [
        "# Chao Phraya Nature-Standard Lead-Case Model v1",
        "",
        "This is a self-contained binomial logistic model built directly from the lead-case cell table, without external helper modules.",
        "",
        "## Model",
        "",
        "`observable_count ~ Binomial(n_pairs, p)`",
        "",
        "`logit(p) ~ strong_sub_5mm + log1p(population_weighted) + log1p(builtup_m2_weighted) + row + col + strong:population + strong:builtup`",
        "",
        f"- Cells: `{len(df)}`",
        f"- Spatial block size: `{args.block_size}`",
        f"- Blocks: `{model_summary['n_blocks']}`",
        f"- Bootstrap replicates: `{args.n_bootstrap}`",
        f"- Converged: `{fit_meta['converged']}` in `{fit_meta['n_iter']}` iterations",
        "",
        "## Main Coefficients",
        "",
        "| term | OR | 95% CI | bootstrap median | bootstrap 95% interval |",
        "|---|---:|---:|---:|---:|",
        f"| strong_sub_5mm | {strong_row['odds_ratio']:.4f} | {strong_row['odds_ratio_ci_low']:.4f}-{strong_row['odds_ratio_ci_high']:.4f} | {boot_lookup['strong_sub_5mm']['odds_ratio_boot_q50']:.4f} | {boot_lookup['strong_sub_5mm']['odds_ratio_boot_q025']:.4f}-{boot_lookup['strong_sub_5mm']['odds_ratio_boot_q975']:.4f} |",
        f"| log1p_population_weighted_z | {pop_row['odds_ratio']:.4f} | {pop_row['odds_ratio_ci_low']:.4f}-{pop_row['odds_ratio_ci_high']:.4f} | {boot_lookup['log1p_population_weighted_z']['odds_ratio_boot_q50']:.4f} | {boot_lookup['log1p_population_weighted_z']['odds_ratio_boot_q025']:.4f}-{boot_lookup['log1p_population_weighted_z']['odds_ratio_boot_q975']:.4f} |",
        f"| log1p_builtup_m2_weighted_z | {built_row['odds_ratio']:.4f} | {built_row['odds_ratio_ci_low']:.4f}-{built_row['odds_ratio_ci_high']:.4f} | {boot_lookup['log1p_builtup_m2_weighted_z']['odds_ratio_boot_q50']:.4f} | {boot_lookup['log1p_builtup_m2_weighted_z']['odds_ratio_boot_q025']:.4f}-{boot_lookup['log1p_builtup_m2_weighted_z']['odds_ratio_boot_q975']:.4f} |",
        "",
        "## Leave-One-Block-Out",
        "",
        f"- Block leave-one-out rows: `{len(lobo_rows)}`",
        f"- Bootstrap failures: `{boot_failures}`",
        "",
        "## Region Context",
        "",
        f"- Chao Phraya summary OR: `{chao_summary.get('strong_vs_nonstrong_not_majority_odds_ratio', '')}`",
        f"- Po summary OR: `{po_summary.get('strong_vs_nonstrong_not_majority_odds_ratio', '')}`",
        "",
        "## Interpretation Guardrail",
        "",
        "- This model is a lead-case model, not the final multi-region hierarchical closure.",
        "- It is stronger than a hand-waved narrative because it is a real fit on cell-level data with block bootstrap.",
        "- The final Nature-level model still needs the missing helper-module stack or an equivalent multi-region self-contained rewrite.",
        "",
        "## Binary Sensitivity Model",
        "",
        "`not_majority_observable ~ Binomial(1, p)`",
        "",
        "`logit(p) ~ strong_sub_5mm + row + col`",
        "",
        f"- strong OR: `{coef_b[1]['odds_ratio']:.4f}`",
        f"- strong 95% CI: `{coef_b[1]['odds_ratio_ci_low']:.4f}-{coef_b[1]['odds_ratio_ci_high']:.4f}`",
        f"- bootstrap median: `{boot_b[0]['odds_ratio_boot_q50']:.4f}`",
        f"- bootstrap 95% interval: `{boot_b[0]['odds_ratio_boot_q025']:.4f}-{boot_b[0]['odds_ratio_boot_q975']:.4f}`",
    ]
    (args.outdir / "chao_phraya_nature_model_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "outdir": str(args.outdir),
                "n_cells": len(df),
                "n_blocks": model_summary["n_blocks"],
                "converged": fit_meta["converged"],
                "strong_or": strong_row["odds_ratio"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
