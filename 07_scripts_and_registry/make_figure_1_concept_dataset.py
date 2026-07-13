from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
FIG_DIR = ROOT / "09_figures_v1"
FIG_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
DATASET = ROOT / "02_benchmark_v0_1" / "benchmark_dataset_inventory_v0_1.csv"


mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
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


def box(ax: mpl.Axes, xy: tuple[float, float], wh: tuple[float, float], text: str, fc: str, ec: str = "#3B4252") -> None:
    patch = FancyBboxPatch(
        xy,
        wh[0],
        wh[1],
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=0.8,
        edgecolor=ec,
        facecolor=fc,
        transform=ax.transAxes,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + wh[0] / 2,
        xy[1] + wh[1] / 2,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=7,
        linespacing=1.15,
    )


def main() -> int:
    benchmark = pd.read_csv(BENCHMARK).copy()
    dataset = pd.read_csv(DATASET).copy()

    fig = plt.figure(figsize=(7.2, 5.6), constrained_layout=False)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.95], width_ratios=[1.05, 0.95], hspace=0.36, wspace=0.3)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])

    # Panel A: concept chain
    ax_a.set_axis_off()
    ax_a.set_title("A  Concept: open observability bias censors exposure", loc="left", fontweight="bold")
    box(ax_a, (0.05, 0.60), (0.27, 0.22), "Observability\nfailure\n(public gaps)", "#EAF2FD")
    box(ax_a, (0.365, 0.60), (0.27, 0.22), "Monitoring\ndebt\n(unserved risk)", "#F6F7FB")
    box(ax_a, (0.68, 0.60), (0.27, 0.22), "Risk\nunderestimation\nfactor", "#FDEFE7")
    ax_a.annotate("", xy=(0.355, 0.71), xytext=(0.32, 0.71), xycoords=ax_a.transAxes, textcoords=ax_a.transAxes, arrowprops=dict(arrowstyle="->", lw=1.1, color="#3B4252"))
    ax_a.annotate("", xy=(0.67, 0.71), xytext=(0.635, 0.71), xycoords=ax_a.transAxes, textcoords=ax_a.transAxes, arrowprops=dict(arrowstyle="->", lw=1.1, color="#3B4252"))
    ax_a.text(0.17, 0.43, "What is\nmissing?", transform=ax_a.transAxes, ha="center", va="center", fontsize=6.8, fontweight="bold", linespacing=1.05)
    ax_a.text(0.50, 0.43, "Why does\nit matter?", transform=ax_a.transAxes, ha="center", va="center", fontsize=6.8, fontweight="bold", linespacing=1.05)
    ax_a.text(0.84, 0.43, "How much\nchanges?", transform=ax_a.transAxes, ha="center", va="center", fontsize=6.8, fontweight="bold", linespacing=1.05)
    ax_a.text(
        0.5,
        0.11,
        "Core claim: open InSAR products do not fail at random; they fail where exposure is hardest to monitor.",
        transform=ax_a.transAxes,
        ha="center",
        va="center",
        fontsize=5.95,
    )

    # Panel B: regional evidence
    benchmark = benchmark.sort_values("landcover_adjusted_or", ascending=False).copy()
    y = np.arange(len(benchmark))
    colors = benchmark["observability_bias_signal"].map(
        {"strong_positive": "#D08770", "positive": "#A3BE8C", "inconclusive": "#8FA3BF"}
    )
    ax_b.barh(y, benchmark["landcover_adjusted_or"], color=colors, height=0.68)
    ax_b.errorbar(
        benchmark["landcover_adjusted_or"],
        y,
        xerr=[
            benchmark["landcover_adjusted_or"] - benchmark["landcover_adjusted_boot_q025"],
            benchmark["landcover_adjusted_boot_q975"] - benchmark["landcover_adjusted_or"],
        ],
        fmt="none",
        ecolor="#3B4252",
        elinewidth=0.8,
        capsize=2.5,
    )
    ax_b.axvline(1.0, color="#444444", lw=0.9, ls="--")
    ax_b.set_yticks(y)
    ax_b.set_yticklabels(benchmark["region"])
    ax_b.set_xlabel("Land-cover-adjusted OR")
    ax_b.set_title("B  Benchmark regions carry distinct bias signals", loc="left", fontweight="bold")
    ax_b.set_xlim(0, max(benchmark["landcover_adjusted_boot_q975"]) * 1.1)
    ax_b.grid(axis="x", color="#E1E5EE", linewidth=0.7)
    ax_b.invert_yaxis()

    # Panel C: dataset boundary / tiers
    ax_c.set_axis_off()
    ax_c.set_title("C  Dataset boundary: primary benchmark, secondary extension, and upgrade path", loc="left", fontweight="bold")
    tiers = [
        ("Primary benchmark", "#EAF2FD", [
            "Open InSAR bias model",
            "Chao Phraya closure",
            "Multi-delta table",
        ]),
        ("Secondary extension", "#F6F7FB", [
            "Japan Niigata probe",
            "Iran nationwide probe",
            "GNSS sparse anchors",
        ]),
        ("Upgrade path", "#FDEFE7", [
            "EGMS query pack",
            "CLMS token for Europe benchmark",
            "Source-data ready outputs",
        ]),
    ]
    x_positions = [0.03, 0.35, 0.67]
    widths = [0.28, 0.28, 0.28]
    for (title, fc, items), x0, w in zip(tiers, x_positions, widths):
        box(ax_c, (x0, 0.23), (w, 0.55), "", fc)
        ax_c.text(x0 + 0.02, 0.71, title, transform=ax_c.transAxes, ha="left", va="center", fontsize=7.5, fontweight="bold")
        for idx, item in enumerate(items):
            ax_c.text(x0 + 0.02, 0.61 - idx * 0.14, f"• {item}", transform=ax_c.transAxes, ha="left", va="center", fontsize=6.15)
    ax_c.text(
        0.5,
        0.06,
        f"Inventory includes {len(dataset)} entries; the manuscript uses the primary benchmark and the two extension layers as evidence boundaries.",
        transform=ax_c.transAxes,
        ha="center",
        va="center",
        fontsize=6.0,
        color="#3B4252",
    )

    fig.suptitle("Open InSAR observability bias and exposure benchmark", y=0.995, fontsize=9.3, fontweight="bold")
    save_pub(fig, "fig1_concept_dataset_map")
    meta = {
        "benchmark": str(BENCHMARK),
        "dataset": str(DATASET),
        "output_dir": str(FIG_DIR),
        "regions": int(len(benchmark)),
        "datasets": int(len(dataset)),
    }
    (FIG_DIR / "fig1_concept_dataset_map_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    plt.close(fig)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
