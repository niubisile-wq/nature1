from pathlib import Path
import csv

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon


OUT = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

NAVY = "#23313d"
BLUE = "#2f74b5"
BLUE_LIGHT = "#e7f0f6"
RED = "#c94b45"
RED_LIGHT = "#faebe6"
GREEN = "#5b8f66"
GREEN_LIGHT = "#e8f2e8"
GOLD = "#b77a2b"
GOLD_LIGHT = "#f6eedf"
GREY = "#66788a"
LINE = "#9aa9b5"


def save_all(fig, base):
    fig.savefig(OUT / f"{base}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{base}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{base}.png", dpi=400, bbox_inches="tight")
    fig.savefig(OUT / f"{base}.tiff", dpi=400, bbox_inches="tight")
    plt.close(fig)


def make_figure_3():
    rows = []
    with (OUT / "ESIN_Figure_2_source_data.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)

    pop = next(r for r in rows if r["metric"] == "Population")
    built = next(r for r in rows if r["metric"] == "Built-up area")
    pop_vals = [float(pop["area_weighted"]), float(pop["native_pixel"])]
    built_vals = [float(built["area_weighted"]), float(built["native_pixel"])]

    fig = plt.figure(figsize=(6.4, 3.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.34)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    fig.text(
        0.02,
        0.98,
        "Lead-case exposure retained by the observability audit",
        ha="left",
        va="top",
        fontsize=10.5,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.02,
        0.91,
        "Hidden exposure is reported only inside strong-screen cells that are not majority observable.",
        ha="left",
        va="top",
        fontsize=7.2,
        color=GREY,
    )

    methods = ["Area-\nweighted", "Native\npixel"]
    colors = [RED, BLUE]
    ax1.bar([0, 1], pop_vals, color=colors, width=0.58)
    ax1.set_xticks([0, 1], methods)
    ax1.set_ylabel("Hidden population (million)")
    ax1.set_ylim(0, 4.25)
    ax1.set_title("a  Population", loc="left", fontsize=8.2, fontweight="bold", color=NAVY, pad=8)
    ax1.grid(axis="y", color="#e5ebef", linewidth=0.8)
    ax1.set_axisbelow(True)
    for i, v in enumerate(pop_vals):
        ax1.text(i, v + 0.1, f"{v:.2f}", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color=NAVY)

    ax2.bar([0, 1], built_vals, color=colors, width=0.58)
    ax2.set_xticks([0, 1], methods)
    ax2.set_ylabel("Hidden built-up area (km$^2$)")
    ax2.set_ylim(0, 455)
    ax2.set_title("b  Built-up surface", loc="left", fontsize=8.2, fontweight="bold", color=NAVY, pad=8)
    ax2.grid(axis="y", color="#e5ebef", linewidth=0.8)
    ax2.set_axisbelow(True)
    for i, v in enumerate(built_vals):
        ax2.text(i, v + 10, f"{v:.2f}", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color=NAVY)

    for ax in (ax1, ax2):
        ax.tick_params(axis="both", labelsize=6.8)
        ax.spines["left"].set_color(LINE)
        ax.spines["bottom"].set_color(LINE)

    fig.subplots_adjust(top=0.72, bottom=0.22, left=0.11, right=0.98)

    save_all(fig, "ESIN_Figure_2")


def ladder_box(ax, x, y, w, h, title, body, face, edge, status):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=face, edgecolor=edge, linewidth=1.2))
    ax.text(x + 0.16, y + h - 0.18, title, ha="left", va="top", fontsize=7.4, fontweight="bold", color=NAVY)
    ax.text(x + 0.16, y + h - 0.52, body, ha="left", va="top", fontsize=5.85, color=GREY, linespacing=1.02)
    ax.text(x + w - 0.16, y + 0.17, status, ha="right", va="bottom", fontsize=6.1, color=edge, fontweight="bold")


def make_figure_7():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(
        0.2,
        5.65,
        "External evidence hierarchy for bounded workflow claims",
        ha="left",
        va="top",
        fontsize=10.5,
        fontweight="bold",
        color=NAVY,
    )
    ax.text(
        0.2,
        5.16,
        "Completed checks support workflow behavior; unavailable strong-subsidence EGMS closure remains a future benchmark.",
        ha="left",
        va="top",
        fontsize=7.0,
        color=GREY,
    )

    def block(x, y, w, h, dx, dy, face, side, top, edge, title, body, status):
        ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w + dx, y + h + dy), (x + dx, y + h + dy)], facecolor=top, edgecolor=edge, linewidth=0.9, zorder=2))
        ax.add_patch(Polygon([(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + h + dy), (x + w, y + h)], facecolor=side, edgecolor=edge, linewidth=0.9, zorder=2))
        ax.add_patch(Rectangle((x, y), w, h, facecolor=face, edgecolor=edge, linewidth=1.25, zorder=3))
        ax.text(x + 0.16, y + h - 0.17, title, ha="left", va="top", fontsize=7.0, fontweight="bold", color=NAVY, zorder=4)
        ax.text(x + 0.16, y + h - 0.48, body, ha="left", va="top", fontsize=5.0, color=GREY, linespacing=0.98, zorder=4)
        ax.text(x + w - 0.16, y + 0.12, status, ha="right", va="bottom", fontsize=5.45, color=edge, fontweight="bold", zorder=4)

    dx, dy = 0.38, 0.30
    steps = [
        (0.75, 1.22, GREEN_LIGHT, "#d5e8d7", "#f0f7f0", GREEN, "DWR/TRE-GHSL", "positive-control check", "complete"),
        (2.82, 1.88, BLUE_LIGHT, "#d4e5f3", "#f1f7fb", BLUE, "Cyprus EGMS", "near-zero boundary", "pipeline proven"),
        (4.92, 2.54, GOLD_LIGHT, "#ead8b9", "#fbf5ea", GOLD, "Po non-EGMS", "exposure closure", "bounded support"),
        (7.02, 3.20, RED_LIGHT, "#efd2cd", "#fff3ef", RED, "Po/Rhone EGMS", "closure absent", "future benchmark"),
    ]
    for x, y, face, side, top, edge, title, body, status in steps:
        block(x, y, 1.82, 0.96, dx, dy, face, side, top, edge, title, body, status)

    arrow_y = 4.64
    ax.add_patch(
        FancyArrowPatch(
            (1.08, arrow_y),
            (8.45, arrow_y),
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=1.2,
            color="#111111",
            zorder=2,
        )
    )
    ax.text(1.08, 4.88, "bounded workflow evidence", ha="left", va="center", fontsize=6.2, color="#111111")
    ax.text(8.45, 4.88, "dense independent validation target", ha="right", va="center", fontsize=6.2, color="#111111")

    for (x1, y1), (x2, y2) in [((2.54, 2.05), (2.76, 2.15)), ((4.62, 2.72), (4.86, 2.82)), ((6.72, 3.38), (6.96, 3.48))]:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7, linewidth=1.0, color=LINE, zorder=1))

    ax.text(
        5,
        0.08,
        "Interpretation boundary: no completed check is treated as dense site-level validation of every hidden cell.",
        ha="center",
        va="bottom",
        fontsize=6.4,
        color=GREY,
    )

    save_all(fig, "ESIN_Figure_9")

    with (OUT / "ESIN_Figure_9_source_data.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", "status", "role"])
        writer.writerow(["DWR/TRE-GHSL", "complete", "positive-control deformation-exposure logic"])
        writer.writerow(["Cyprus EGMS", "pipeline proven", "real EGMS/GHSL overlay and near-zero boundary control"])
        writer.writerow(["Po non-EGMS", "bounded support", "transfer case with exposure closure and sparse geodetic context"])
        writer.writerow(["Po/Rhone EGMS", "future hook", "high-value strong-subsidence benchmark not claimed as complete"])


if __name__ == "__main__":
    make_figure_3()
    make_figure_7()
