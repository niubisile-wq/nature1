import csv
import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})


COLORS = {
    "lead": "#2f78bd",
    "support": "#5a9367",
    "boundary": "#7a8793",
    "control": "#c84d42",
    "neutral": "#566573",
    "light": "#eef3f6",
    "line": "#2d3436",
    "built": "#c47f2c",
    "pop": "#2f78bd",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def as_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def save_pub(fig, stem):
    fig.savefig(ROOT / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(ROOT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(ROOT / f"{stem}.tiff", dpi=600, bbox_inches="tight")
    fig.savefig(ROOT / f"{stem}.png", dpi=220, bbox_inches="tight")


def write_source(stem, rows, fields):
    with open(ROOT / f"{stem}_source_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def figure_10():
    rows = read_csv(ROOT / "regional_non_egms_strengthening_v1.csv")
    order = ["Chao Phraya", "Po", "Brantas", "Rhone", "Rhine"]
    rows = sorted(rows, key=lambda r: order.index(r["region"]))

    y = np.arange(len(rows))[::-1]
    labels = [r["region"] for r in rows]
    ors = np.array([float(r["odds_ratio"]) for r in rows])
    lo = np.array([float(r["ci_low"]) if r["ci_low"] else np.nan for r in rows])
    hi = np.array([float(r["ci_high"]) if r["ci_high"] else np.nan for r in rows])
    pop_hidden = np.array([as_float(r["strong_population_not_majority_fraction"]) for r in rows])
    built_hidden = np.array([as_float(r["strong_builtup_not_majority_fraction"]) for r in rows])

    role_color = {
        "lead_case": COLORS["lead"],
        "supporting_case": COLORS["support"],
        "conditional_upgrade_case": COLORS["boundary"],
        "control_or_specification_case": COLORS["control"],
    }
    point_colors = [role_color.get(r["evidence_role"], COLORS["neutral"]) for r in rows]

    fig = plt.figure(figsize=(7.2, 3.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.25], wspace=0.38)

    ax = fig.add_subplot(gs[0, 0])
    ax.axvline(1, color="#9aa6af", lw=0.9, ls="--", zorder=0)
    for i, r in enumerate(rows):
        yi = y[i]
        if not math.isnan(lo[i]):
            ax.plot([lo[i], hi[i]], [yi, yi], color=point_colors[i], lw=1.5, solid_capstyle="round")
        ax.scatter(ors[i], yi, s=34, color=point_colors[i], edgecolor="white", linewidth=0.6, zorder=3)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Odds ratio for strong deformation in hidden support")
    ax.set_xlim(0.55, 9.0)
    ax.set_title("Regional transfer and control behavior", loc="left", fontweight="bold", pad=8)
    ax.grid(axis="x", color="#e3e8ec", lw=0.6)

    ax2 = fig.add_subplot(gs[0, 1])
    h = 0.32
    ax2.barh(y + h / 2, pop_hidden, height=h, color=COLORS["pop"], alpha=0.86, label="Population")
    ax2.barh(y - h / 2, built_hidden, height=h, color=COLORS["built"], alpha=0.86, label="Built-up")
    ax2.set_yticks(y)
    ax2.set_yticklabels([])
    ax2.set_xlim(0, 0.52)
    ax2.set_xlabel("Hidden-support share within strong-exposure layer")
    ax2.set_title("Exposure retained by the audit", loc="left", fontweight="bold", pad=8)
    ax2.grid(axis="x", color="#e3e8ec", lw=0.6)
    ax2.legend(loc="lower right", ncol=2, handlelength=1.2, columnspacing=0.9)
    for i, val in enumerate(pop_hidden):
        if not math.isnan(val):
            ax2.text(val + 0.01, y[i] + h / 2, f"{val:.2f}", va="center", fontsize=6, color=COLORS["pop"])
    for i, val in enumerate(built_hidden):
        if not math.isnan(val):
            ax2.text(val + 0.01, y[i] - h / 2, f"{val:.2f}", va="center", fontsize=6, color=COLORS["built"])
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    save_pub(fig, "ESIN_Figure_10")
    write_source(
        "ESIN_Figure_10",
        rows,
        [
            "region",
            "evidence_role",
            "odds_ratio",
            "ci_low",
            "ci_high",
            "strong_population_not_majority_fraction",
            "strong_builtup_not_majority_fraction",
            "interpretation",
        ],
    )


def figure_11():
    dwr = read_csv(
        ROOT.parent / "03_exposure_closure" / "dwr_ghsl_exposure_closure_v1" / "dwr_ghsl_exposure_closure_thresholds_v1.csv"
    )
    cyprus = read_csv(ROOT / "egms_benchmark_closure_thresholds_v1.csv")

    dwr5 = [r for r in dwr if float(r["threshold_mm_per_year"]) == 5.0]
    names = ["Tulare/Corcoran", "Fresno"]
    pop = np.array([float(dwr5[0]["strong_population"]), float(dwr5[1]["strong_population"])]) / 1000.0
    built = np.array([float(dwr5[0]["strong_builtup_km2"]), float(dwr5[1]["strong_builtup_km2"])])

    thr = np.array([float(r["threshold_mm_per_year"]) for r in cyprus])
    point_share = np.array([float(r["strong_point_fraction"]) for r in cyprus]) * 100
    pop_share = np.array([float(r["strong_population_share"]) for r in cyprus]) * 100
    built_share = np.array([float(r["strong_builtup_share"]) for r in cyprus]) * 100

    fig = plt.figure(figsize=(7.2, 3.55))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.15], wspace=0.34)

    ax = fig.add_subplot(gs[0, 0])
    x = np.arange(len(names))
    w = 0.34
    ax.bar(x - w / 2, pop, width=w, color=COLORS["pop"], label="Population, thousand")
    ax.bar(x + w / 2, built, width=w, color=COLORS["built"], label="Built-up, km$^2$")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("Strong-zone exposure at 5 mm yr$^{-1}$")
    ax.set_title("DWR/TRE positive-control exposure", loc="left", fontweight="bold", pad=8)
    ax.set_ylim(0, max(pop) * 1.22)
    ax.grid(axis="y", color="#e3e8ec", lw=0.6)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.98), ncol=1, handlelength=1.4)
    for xi, value in zip(x - w / 2, pop):
        ax.text(xi, value + max(pop) * 0.025, f"{value:.0f}", ha="center", va="bottom", fontsize=6)
    for xi, value in zip(x + w / 2, built):
        ax.text(xi, value + max(pop) * 0.025, f"{value:.1f}", ha="center", va="bottom", fontsize=6)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(thr, point_share, marker="o", lw=1.6, color=COLORS["line"], label="EGMS points")
    ax2.plot(thr, pop_share, marker="o", lw=1.4, color=COLORS["pop"], label="Population")
    ax2.plot(thr, built_share, marker="o", lw=1.4, color=COLORS["built"], label="Built-up")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xticks(thr)
    ax2.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax2.set_xlabel("Cyprus EGMS threshold (mm yr$^{-1}$)")
    ax2.set_ylabel("Strong class share (%)")
    ax2.set_title("Near-zero EGMS boundary control", loc="left", fontweight="bold", pad=8)
    ax2.grid(which="both", color="#e3e8ec", lw=0.6)
    ax2.legend(loc="upper right")
    ax2.annotate(
        "0.31% population\nat 5 mm yr$^{-1}$",
        xy=(5.0, pop_share[thr.tolist().index(5.0)]),
        xytext=(6.55, 1.15),
        textcoords="data",
        ha="left",
        va="center",
        color=COLORS["pop"],
        fontsize=6,
        bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.88),
        arrowprops=dict(arrowstyle="-", color=COLORS["pop"], lw=0.7, shrinkA=2, shrinkB=5),
    )

    fig.text(
        0.01,
        0.015,
        "External controls bound behavior; they do not directly validate the Chao Phraya estimate.",
        color="#637381",
        fontsize=6,
    )
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    save_pub(fig, "ESIN_Figure_11")

    rows = []
    for r in dwr5:
        rows.append({
            "panel": "DWR_TRE_positive_control",
            "case": r["box"],
            "threshold_mm_per_year": r["threshold_mm_per_year"],
            "strong_population": r["strong_population"],
            "strong_builtup_km2": r["strong_builtup_km2"],
            "share_metric": "",
            "share_percent": "",
        })
    for r in cyprus:
        rows.extend([
            {
                "panel": "Cyprus_EGMS_boundary_control",
                "case": "cyprus_sourcecoop_smoke",
                "threshold_mm_per_year": r["threshold_mm_per_year"],
                "strong_population": r["strong_population"],
                "strong_builtup_km2": r["strong_builtup"],
                "share_metric": "strong_point_fraction",
                "share_percent": float(r["strong_point_fraction"]) * 100,
            },
            {
                "panel": "Cyprus_EGMS_boundary_control",
                "case": "cyprus_sourcecoop_smoke",
                "threshold_mm_per_year": r["threshold_mm_per_year"],
                "strong_population": r["strong_population"],
                "strong_builtup_km2": r["strong_builtup"],
                "share_metric": "strong_population_share",
                "share_percent": float(r["strong_population_share"]) * 100,
            },
            {
                "panel": "Cyprus_EGMS_boundary_control",
                "case": "cyprus_sourcecoop_smoke",
                "threshold_mm_per_year": r["threshold_mm_per_year"],
                "strong_population": r["strong_population"],
                "strong_builtup_km2": r["strong_builtup"],
                "share_metric": "strong_builtup_share",
                "share_percent": float(r["strong_builtup_share"]) * 100,
            },
        ])
    write_source(
        "ESIN_Figure_11",
        rows,
        ["panel", "case", "threshold_mm_per_year", "strong_population", "strong_builtup_km2", "share_metric", "share_percent"],
    )


if __name__ == "__main__":
    figure_10()
    figure_11()
