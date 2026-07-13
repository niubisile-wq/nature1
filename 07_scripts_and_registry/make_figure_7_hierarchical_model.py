from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
FIG_DIR = ROOT / "09_figures_v1"
FIG_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DIR = ROOT / "03_exposure_closure" / "hierarchical_model_v1"
ANCHOR_DIR = ROOT / "03_exposure_closure" / "hierarchical_anchor_closure_v1"
LEAD_DIR = ROOT / "03_exposure_closure" / "chao_phraya_nature_model_v1"


mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7.1,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": 0.8,
        "legend.frameon": False,
    }
)


def save_pub(fig: mpl.figure.Figure, stem: str) -> None:
    fig.savefig(FIG_DIR / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.tiff", dpi=600, bbox_inches="tight")


def forest(ax: plt.Axes, labels, mids, lows, highs, colors, xlim, title: str) -> None:
    y = np.arange(len(labels))
    for yi, mid, lo, hi, c in zip(y, mids, lows, highs, colors):
        ax.errorbar(
            mid,
            yi,
            xerr=[[mid - lo], [hi - mid]],
            fmt="o",
            color=c,
            ecolor=c,
            elinewidth=1.2,
            capsize=2.6,
            markersize=4.6,
        )
    ax.axvline(1.0, color="#4A4A4A", lw=0.9, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xscale("log")
    ax.set_xlim(*xlim)
    ax.grid(axis="x", color="#E4E8F0", linewidth=0.7)
    ax.set_title(title, loc="left", fontweight="bold")
    ax.invert_yaxis()


def main() -> int:
    model = pd.read_csv(MODEL_DIR / "hierarchical_model_comparison.csv")
    loo = pd.read_csv(MODEL_DIR / "hierarchical_model_leave_one_out.csv")
    coef = pd.read_csv(MODEL_DIR / "hierarchical_model_coefficients.csv")
    anchor = json.loads((ANCHOR_DIR / "hierarchical_anchor_meta.json").read_text(encoding="utf-8"))
    lead = json.loads((LEAD_DIR / "chao_phraya_nature_model_meta.json").read_text(encoding="utf-8"))

    fig = plt.figure(figsize=(7.6, 5.7), constrained_layout=False)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.08], width_ratios=[1.05, 0.95], hspace=0.36, wspace=0.28)
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    # Panel A: model-family comparison
    colors = ["#8FA3BF", "#A3BE8C"]
    mids = model["pooled_or"].tolist()
    lows = model["pooled_ci_low"].tolist()
    highs = model["pooled_ci_high"].tolist()
    labels = ["summary-only\nmeta-analysis", "cell-anchored\nhierarchical stack"]
    forest(ax_a, labels, mids, lows, highs, colors, (1.05, 3.9), "A  Frozen model-family comparison")
    ax_a.text(
        0.03,
        0.06,
        "Hybrid stack preserves a positive pooled signal and is the preferred frozen synthesis.",
        transform=ax_a.transAxes,
        fontsize=6.5,
        ha="left",
        va="bottom",
        color="#3B4252",
    )
    ax_a.text(
        0.98,
        0.84,
        f"Delta pooled OR = {mids[1] - mids[0]:.3f}\nLOO MAE = {model.loc[1, 'loo_mae']:.3f}",
        transform=ax_a.transAxes,
        fontsize=6.2,
        ha="right",
        va="top",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#C9CEDA"),
    )

    # Panel B: leave-one-out absolute error by region
    loo = loo.sort_values("abs_log_error", ascending=True).copy()
    y = np.arange(len(loo))
    ax_b.barh(y, loo["abs_log_error"], color="#8FA3BF", height=0.66)
    ax_b.axvline(loo["abs_log_error"].mean(), color="#4A4A4A", lw=0.9, ls="--")
    ax_b.set_yticks(y)
    ax_b.set_yticklabels(loo["left_out_region"])
    ax_b.set_xlabel("Absolute log-OR error")
    ax_b.set_title("B  Leave-one-out stability", loc="left", fontweight="bold")
    ax_b.grid(axis="x", color="#E4E8F0", linewidth=0.7)
    ax_b.invert_yaxis()
    ax_b.set_xlim(0, max(loo["abs_log_error"]) * 1.18)
    for yi, err in zip(y, loo["abs_log_error"]):
        ax_b.text(err + 0.02, yi, f"{err:.3f}", va="center", fontsize=6.2)
    ax_b.text(
        0.02,
        -0.14,
        f"mean={loo['abs_log_error'].mean():.3f}; max={loo['abs_log_error'].max():.3f}",
        transform=ax_b.transAxes,
        fontsize=6.2,
        ha="left",
    )

    # Panel C: hierarchical coefficients
    coef = coef.loc[coef["term"] != "intercept"].copy()
    term_map = {
        "signal_code": "signal code",
        "anchor_code": "anchor code",
        "n_cells_log": "log1p n cells",
        "cell_level": "cell-level anchor",
    }
    coef["display"] = coef["term"].map(term_map).fillna(coef["term"])
    coef = coef.sort_values("or").reset_index(drop=True)
    forest(
        ax_c,
        coef["display"].tolist(),
        coef["or"].tolist(),
        coef["or_ci_low"].tolist(),
        coef["or_ci_high"].tolist(),
        ["#A3BE8C"] * len(coef),
        (0.45, 3.2),
        "C  Hierarchical coefficients",
    )
    ax_c.text(
        0.03,
        -0.14,
        f"Chao anchor OR={anchor['chao_cell_level']['odds_ratio']:.2f}; pooled OR={anchor['hybrid_cell_anchored_random_or']:.2f}",
        transform=ax_c.transAxes,
        fontsize=6.2,
        ha="left",
    )

    fig.suptitle("Frozen hierarchical model comparison", y=0.995, fontsize=9.2, fontweight="bold")
    save_pub(fig, "fig7_hierarchical_model_comparison")
    meta = {
        "model_dir": str(MODEL_DIR),
        "anchor_dir": str(ANCHOR_DIR),
        "lead_dir": str(LEAD_DIR),
        "output_dir": str(FIG_DIR),
        "core_conclusion": "The frozen cell-anchored hierarchical stack is the preferred E5 synthesis over the summary-only meta-analysis.",
    }
    (FIG_DIR / "fig7_hierarchical_model_comparison_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    plt.close(fig)
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

