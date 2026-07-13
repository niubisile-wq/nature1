from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch
from PIL import Image


ROOT = Path.home() / "Desktop" / "nature"
FIG_DIR = ROOT / "09_figures_v1"
FIG_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
JAPAN = ROOT / "04_japan_licsbas_probe" / "h5_velocity_summary.json"
IRAN = ROOT / "05_iran_insar_probe" / "tif_inspection.json"
EGMS = ROOT / "06_egms_query_pack" / "egms_api_rescue_plan.md"
IRAN_JPG = Path.home() / "radar_outputs" / "iran_insar_zenodo_probe" / "Iran_subsidence_rate_2014-2020_Sentinel-1_InSAR_desc_v1.0.0.jpg"


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
        fontsize=6.6,
        linespacing=1.12,
    )


def panel_label(fig: mpl.figure.Figure, ax: mpl.Axes, label: str) -> None:
    pos = ax.get_position()
    fig.text(pos.x0 - 0.02, pos.y1 + 0.01, label, fontsize=9.5, fontweight="bold")


def main() -> int:
    benchmark = pd.read_csv(BENCHMARK, usecols=["region", "ngl_station_count", "independent_anchor_status", "egms_status"])
    benchmark = benchmark.copy()
    benchmark["anchor_group"] = benchmark["independent_anchor_status"].map(
        {"sparse_gnss_anchor": "sparse", "weak_or_missing_gnss_anchor": "weak"}
    ).fillna("other")

    japan = json.loads(JAPAN.read_text(encoding="utf-8"))
    iran_stats = json.loads(IRAN.read_text(encoding="utf-8"))[0]["stats"]
    egms_text = EGMS.read_text(encoding="utf-8")

    fig = plt.figure(figsize=(7.6, 5.9), constrained_layout=False)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.02], width_ratios=[1.0, 1.0], hspace=0.36, wspace=0.28)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    # Panel A: Japan transfer summary
    ax_a.set_title("A  Japan transfer", loc="left", fontweight="bold")
    ax_a.set_axis_off()
    box(ax_a, (0.06, 0.50), (0.88, 0.20), "", "#F6F7FB")
    box(ax_a, (0.10, 0.56), (0.28, 0.08), "cum.h5\nmedian -1.016\nfrac < -5 0.188", "#FFFFFF")
    box(ax_a, (0.62, 0.56), (0.28, 0.08), "cum_filt.h5\nmedian -0.409\nfrac < -5 0.162", "#FFFFFF")
    ax_a.annotate("", xy=(0.58, 0.60), xytext=(0.38, 0.60), xycoords=ax_a.transAxes, textcoords=ax_a.transAxes, arrowprops=dict(arrowstyle="->", lw=1.0, color="#3B4252"))
    ax_a.text(0.50, 0.74, f"{japan[0]['date_start']} -> {japan[0]['date_end']}", transform=ax_a.transAxes, ha="center", fontsize=6.9, fontweight="bold")
    ax_a.text(0.50, 0.39, f"{japan[0]['n_time_steps']} steps, 163 x 335 pixels", transform=ax_a.transAxes, ha="center", fontsize=6.1, color="#3B4252")
    ax_a.text(
        0.50,
        0.12,
        "Japan shows the transfer is not Europe-specific.",
        transform=ax_a.transAxes,
        ha="center",
        fontsize=6.3,
    )

    # Panel B: Iran transfer summary
    ax_b.set_title("B  Iran extension", loc="left", fontweight="bold")
    ax_b.set_axis_off()
    if IRAN_JPG.exists():
        img = Image.open(IRAN_JPG)
        ax_b.imshow(img, extent=(0.10, 0.92, 0.20, 0.84), aspect="auto")
    ax_b.text(
        0.12,
        0.80,
        f"Median rate: {iran_stats['median']:.1f}\nP95 rate: {iran_stats['p95']:.1f}\nValid pixels: {iran_stats['finite_count']:,}",
        transform=ax_b.transAxes,
        ha="left",
        va="top",
        fontsize=6.0,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#C9CEDA", alpha=0.90),
    )
    ax_b.text(
        0.50,
        0.08,
        "Iran is a strict no-token companion product.",
        transform=ax_b.transAxes,
        ha="center",
        fontsize=6.0,
    )

    # Panel C: GNSS anchors
    bench_sorted = benchmark.sort_values(["ngl_station_count", "region"], ascending=[False, True]).copy()
    color_map = {"sparse": "#A3BE8C", "weak": "#8FA3BF", "other": "#D08770"}
    colors = bench_sorted["anchor_group"].map(color_map)
    y = np.arange(len(bench_sorted))
    ax_c.barh(y, bench_sorted["ngl_station_count"], color=colors, height=0.66)
    ax_c.set_yticks(y)
    ax_c.set_yticklabels(bench_sorted["region"])
    ax_c.set_xlabel("NGL station count")
    ax_c.grid(axis="x", color="#E1E5EE", linewidth=0.7)
    ax_c.set_title("C  GNSS support", loc="left", fontweight="bold")
    ax_c.invert_yaxis()
    ax_c.set_xlim(0, max(bench_sorted["ngl_station_count"]) * 1.15)
    ax_c.axvline(5, color="#444444", lw=0.8, ls="--")
    for yi, val, status in zip(y, bench_sorted["ngl_station_count"], bench_sorted["independent_anchor_status"]):
        ax_c.text(val + 0.6, yi, status.replace("_", " "), va="center", fontsize=6.0)
    # Panel D: EGMS upgrade path
    ax_d.set_axis_off()
    ax_d.set_title("D  EGMS upgrade path", loc="left", fontweight="bold")
    boxes = [
        ((0.05, 0.68), (0.21, 0.16), "Current\nno-token\nbenchmark", "#EAF2FD"),
        ((0.33, 0.68), (0.21, 0.16), "EGMS query\npack ready", "#F6F7FB"),
        ((0.61, 0.68), (0.16, 0.16), "Add\ntoken.jwt", "#FDEFE7"),
        ((0.81, 0.68), (0.14, 0.16), "Dense\nEurope\nupgrade", "#E8F3E8"),
    ]
    for xy, wh, text, fc in boxes:
        box(ax_d, xy, wh, text, fc)
    for x0, x1 in [(0.26, 0.33), (0.54, 0.61), (0.77, 0.81)]:
        ax_d.annotate("", xy=(x1, 0.76), xytext=(x0, 0.76), xycoords=ax_d.transAxes, textcoords=ax_d.transAxes, arrowprops=dict(arrowstyle="->", lw=1.1, color="#3B4252"))
    ax_d.text(0.50, 0.53, "Priority AOIs", transform=ax_d.transAxes, ha="center", fontsize=6.9, fontweight="bold")
    priority_lines = [
        "A: Po/Venice, Netherlands lowlands, Rhone",
        "B: Rhine specificity control",
        "C: Cyprus smoke test only",
    ]
    for i, line in enumerate(priority_lines):
        ax_d.text(0.50, 0.42 - 0.08 * i, line, transform=ax_d.transAxes, ha="center", fontsize=5.8)
    ax_d.text(
        0.50,
        0.03,
        "This panel limits scope: Europe is an upgrade route, not the current causal claim.",
        transform=ax_d.transAxes,
        ha="center",
        fontsize=6.0,
    )

    fig.suptitle("Transfer and scope limits", y=0.995, fontsize=9.2, fontweight="bold")
    save_pub(fig, "fig6_transfer_scope")
    meta = {
        "benchmark": str(BENCHMARK),
        "japan": str(JAPAN),
        "iran": str(IRAN),
        "egms": str(EGMS),
        "iran_image": str(IRAN_JPG),
        "output_dir": str(FIG_DIR),
    }
    (FIG_DIR / "fig6_transfer_scope_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    plt.close(fig)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
