from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parent

COL = {
    "ink": "#1f2933",
    "muted": "#5b6773",
    "line": "#7b8794",
    "input": "#eef2f6",
    "support": "#d9e8f5",
    "screen": "#f2e6d7",
    "exposure": "#dcebdc",
    "bad": "#f4d8d4",
    "good": "#dce6f5",
    "bad_edge": "#b65a50",
    "good_edge": "#426aa1",
}


def set_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.5,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0.8,
        }
    )


def add_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    face: str,
    edge: str | None = None,
    lw: float = 0.9,
    fs: float = 7.4,
    weight: str = "normal",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=face,
        edgecolor=edge or COL["line"],
        linewidth=lw,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        color=COL["ink"],
        fontsize=fs,
        fontweight=weight,
        linespacing=1.15,
    )


def add_arrow(ax, xy1, xy2, color=None, rad=0.0, lw=1.0) -> None:
    arrow = FancyArrowPatch(
        xy1,
        xy2,
        arrowstyle="-|>",
        mutation_scale=10,
        color=color or COL["line"],
        linewidth=lw,
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=3,
        shrinkB=3,
    )
    ax.add_patch(arrow)


def add_label(ax, x, y, text, color=None, fs=7.2, weight="normal", ha="center") -> None:
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va="center",
        color=color or COL["muted"],
        fontsize=fs,
        fontweight=weight,
        linespacing=1.15,
    )


def main() -> None:
    set_style()
    fig, ax = plt.subplots(figsize=(7.1, 3.85))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Title and premise.
    ax.text(
        0.03,
        0.955,
        "Observability-driven exposure bias",
        ha="left",
        va="top",
        fontsize=8.8,
        fontweight="bold",
        color=COL["ink"],
    )
    ax.text(
        0.03,
        0.915,
        "Applying a support mask before exposure accounting changes the denominator.",
        ha="left",
        va="top",
        fontsize=7.2,
        color=COL["muted"],
    )

    # Inputs.
    add_label(ax, 0.08, 0.805, "Inputs", fs=7.2, weight="bold", ha="left")
    add_box(ax, 0.05, 0.685, 0.22, 0.085, "Public InSAR\nvalid support", COL["support"])
    add_box(ax, 0.39, 0.685, 0.22, 0.085, "Frozen strong-\ndeformation screen", COL["screen"])
    add_box(ax, 0.73, 0.685, 0.22, 0.085, "Population and\nbuilt-up exposure", COL["exposure"])

    # Central accounting gate.
    add_box(
        ax,
        0.34,
        0.545,
        0.32,
        0.08,
        "Exposure accounting step",
        COL["input"],
        edge="#687789",
        weight="bold",
    )
    add_arrow(ax, (0.16, 0.685), (0.39, 0.625))
    add_arrow(ax, (0.50, 0.685), (0.50, 0.625))
    add_arrow(ax, (0.84, 0.685), (0.61, 0.625))

    # Two workflows.
    add_box(
        ax,
        0.075,
        0.35,
        0.34,
        0.10,
        "Clip deformation-relevant cells\nto valid radar support",
        COL["bad"],
        edge=COL["bad_edge"],
    )
    add_box(
        ax,
        0.585,
        0.35,
        0.34,
        0.10,
        "Keep weakly observed support\nas an explicit audit class",
        COL["good"],
        edge=COL["good_edge"],
    )
    add_arrow(ax, (0.43, 0.545), (0.25, 0.435), color=COL["bad_edge"], rad=0.04, lw=1.1)
    add_arrow(ax, (0.57, 0.545), (0.755, 0.435), color=COL["good_edge"], rad=-0.04, lw=1.1)

    add_box(
        ax,
        0.075,
        0.17,
        0.34,
        0.105,
        "Support-conditioned denominator\nweakly observed exposure is omitted",
        "#faebe8",
        edge=COL["bad_edge"],
    )
    add_box(
        ax,
        0.585,
        0.17,
        0.34,
        0.105,
        "Visible exposure + hidden exposure\nproduct support remains traceable",
        "#eaf0fa",
        edge=COL["good_edge"],
    )
    add_arrow(ax, (0.245, 0.35), (0.245, 0.275), color=COL["bad_edge"], lw=1.1)
    add_arrow(ax, (0.755, 0.35), (0.755, 0.275), color=COL["good_edge"], lw=1.1)

    # Bottom message.
    ax.plot([0.46, 0.54], [0.225, 0.225], color=COL["line"], lw=0.9)
    add_label(
        ax,
        0.50,
        0.095,
        "Audit target: quantify exposure that remains in the deformation-relevant domain\nbut is weakly supported by the public radar product.",
        fs=7.7,
        color=COL["ink"],
    )

    # Minimal panel letters for manuscript readability.
    ax.text(0.05, 0.79, "a", fontsize=8.2, fontweight="bold", color=COL["ink"])
    ax.text(0.075, 0.465, "b", fontsize=8.2, fontweight="bold", color=COL["bad_edge"])
    ax.text(0.585, 0.465, "c", fontsize=8.2, fontweight="bold", color=COL["good_edge"])

    stem = ROOT / "ESIN_Figure_mechanism"
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    (ROOT / "ESIN_Figure_mechanism_source_data.csv").write_text(
        "element,role,interpretation\n"
        "public_insar_valid_support,input,radar product support layer\n"
        "frozen_strong_deformation_screen,input,deformation-relevant domain\n"
        "population_and_built_up_exposure,input,exposure layer\n"
        "visible_only_workflow,comparison_path,clips support before counting exposure\n"
        "observability_aware_workflow,proposed_path,retains weak support as hidden exposure\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

