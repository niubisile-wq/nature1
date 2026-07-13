from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch
from PIL import Image


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
FIG_DIR = ROOT / "09_figures_v1"
FIG_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
JAPAN = ROOT / "04_japan_licsbas_probe" / "h5_velocity_summary.json"
IRAN = ROOT / "05_iran_insar_probe" / "tif_inspection.json"
IRAN_JPG = Path(r"C:\Users\刘子轩\radar_outputs\iran_insar_zenodo_probe\Iran_subsidence_rate_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.jpg")


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
        fontsize=6.7,
        linespacing=1.15,
    )


def main() -> int:
    benchmark = pd.read_csv(BENCHMARK).copy()
    benchmark = benchmark.sort_values("dominant_landcover_fraction", ascending=False).copy()
    japan = json.loads(JAPAN.read_text(encoding="utf-8"))
    iran_stats = json.loads(IRAN.read_text(encoding="utf-8"))[0]["stats"]

    fig = plt.figure(figsize=(7.5, 5.9), constrained_layout=False)
    gs = fig.add_gridspec(2, 2, height_ratios=[0.98, 1.05], width_ratios=[1.0, 1.0], hspace=0.34, wspace=0.24)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    # Panel A: landcover control
    colors = benchmark["observability_bias_signal"].map(
        {"strong_positive": "#D08770", "positive": "#A3BE8C", "inconclusive": "#8FA3BF"}
    )
    y = np.arange(len(benchmark))
    ax_a.barh(y, benchmark["landcover_adjusted_or"], color=colors, height=0.66)
    ax_a.errorbar(
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
    ax_a.axvline(1.0, color="#444444", lw=0.9, ls="--")
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(benchmark["region"])
    ax_a.set_xlabel("Land-cover-adjusted OR")
    ax_a.set_title("A  Land-cover control", loc="left", fontweight="bold")
    ax_a.grid(axis="x", color="#E1E5EE", linewidth=0.7)
    ax_a.invert_yaxis()
    for yi, val, land in zip(y, benchmark["landcover_adjusted_or"], benchmark["dominant_landcover"]):
        ax_a.text(val + 0.08, yi, land, ha="left", va="center", fontsize=6.2)

    # Panel B: product lineage schematic
    ax_b.set_axis_off()
    ax_b.set_title("B  Product lineage controls the evidence boundary", loc="left", fontweight="bold")
    boxes = [
        ((0.05, 0.62), (0.25, 0.22), "Core\nanalysis\nVLM + GHSL\n+ WorldCover", "#EAF2FD"),
        ((0.37, 0.62), (0.25, 0.22), "Japan\nLiCSBAS\npublic\nextension", "#F6F7FB"),
        ((0.69, 0.62), (0.25, 0.22), "Iran\nnationwide\npublic\nextension", "#FDEFE7"),
    ]
    for xy, wh, text, fc in boxes:
        box(ax_b, xy, wh, text, fc)
    ax_b.annotate("", xy=(0.35, 0.73), xytext=(0.30, 0.73), xycoords=ax_b.transAxes, textcoords=ax_b.transAxes, arrowprops=dict(arrowstyle="->", lw=1.1, color="#3B4252"))
    ax_b.annotate("", xy=(0.67, 0.73), xytext=(0.62, 0.73), xycoords=ax_b.transAxes, textcoords=ax_b.transAxes, arrowprops=dict(arrowstyle="->", lw=1.1, color="#3B4252"))
    ax_b.text(0.50, 0.37, "Same censoring question,\nmultiple product families", transform=ax_b.transAxes, ha="center", va="center", fontsize=7.0, fontweight="bold")
    ax_b.text(0.50, 0.16, "The controls show the signal is not confined to one product line.", transform=ax_b.transAxes, ha="center", va="center", fontsize=6.3)

    # Panel C: Japan summary table
    ax_c.set_axis_off()
    ax_c.set_title("C  Japan Niigata extension confirms transferability", loc="left", fontweight="bold")
    rows = [
        ("cum.h5", japan[0]["velocity_stats"]["median"], japan[0]["velocity_stats"]["fraction_lt_minus_5"], japan[0]["n_time_steps"]),
        ("cum_filt.h5", japan[1]["velocity_stats"]["median"], japan[1]["velocity_stats"]["fraction_lt_minus_5"], japan[1]["n_time_steps"]),
    ]
    box(ax_c, (0.05, 0.22), (0.90, 0.58), "", "#F6F7FB")
    ax_c.text(0.09, 0.70, "File", transform=ax_c.transAxes, fontsize=7.0, fontweight="bold")
    ax_c.text(0.43, 0.70, "Median", transform=ax_c.transAxes, fontsize=7.0, fontweight="bold")
    ax_c.text(0.63, 0.70, "Frac < -5", transform=ax_c.transAxes, fontsize=7.0, fontweight="bold")
    ax_c.text(0.88, 0.70, "Steps", transform=ax_c.transAxes, fontsize=7.0, fontweight="bold", ha="center")
    for idx, (name, med, frac, nsteps) in enumerate(rows):
        y0 = 0.56 - idx * 0.20
        ax_c.text(0.09, y0, name, transform=ax_c.transAxes, fontsize=6.8)
        ax_c.text(0.43, y0, f"{med:.3f}", transform=ax_c.transAxes, fontsize=6.8)
        ax_c.text(0.64, y0, f"{frac:.3f}", transform=ax_c.transAxes, fontsize=6.8)
        ax_c.text(0.88, y0, str(nsteps), transform=ax_c.transAxes, fontsize=6.8, ha="center")
    ax_c.text(
        0.50,
        0.10,
        "Japan confirms the method can be extended to a non-Europe public InSAR product.",
        transform=ax_c.transAxes,
        ha="center",
        fontsize=6.3,
    )

    # Panel D: Iran image + stats
    ax_d.set_title("D  Iran nationwide product adds a second public extension", loc="left", fontweight="bold")
    ax_d.set_axis_off()
    img = Image.open(IRAN_JPG)
    ax_d.imshow(img)
    ax_d.text(
        0.03,
        0.94,
        f"Median rate: {iran_stats['median']:.1f}\nP95 rate: {iran_stats['p95']:.1f}\nValid pixels: {iran_stats['finite_count']:,}",
        transform=ax_d.transAxes,
        ha="left",
        va="top",
        fontsize=6.4,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#C9CEDA", alpha=0.88),
    )

    fig.suptitle("Mechanism controls and public-product transfer", y=0.995, fontsize=9.2, fontweight="bold")
    save_pub(fig, "fig5_controls_transfer")
    meta = {
        "benchmark": str(BENCHMARK),
        "japan": str(JAPAN),
        "iran": str(IRAN),
        "iran_image": str(IRAN_JPG),
        "output_dir": str(FIG_DIR),
    }
    (FIG_DIR / "fig5_controls_transfer_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    plt.close(fig)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
