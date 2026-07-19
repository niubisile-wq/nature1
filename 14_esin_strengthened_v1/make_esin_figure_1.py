import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch


OUT = Path(__file__).resolve().parent

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
        "axes.linewidth": 0.8,
    }
)


def add_cell(
    ax,
    x,
    y,
    w,
    h,
    face,
    edge,
    title,
    subtitle,
    title_color,
    alpha=1.0,
    title_size=8.4,
    subtitle_size=6.4,
):
    ax.add_patch(
        Rectangle(
            (x, y),
            w,
            h,
            facecolor=face,
            edgecolor=edge,
            linewidth=1.1,
            alpha=alpha,
        )
    )
    ax.text(
        x + w / 2,
        y + h * 0.57,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color=title_color,
        linespacing=1.05,
    )
    ax.text(
        x + w / 2,
        y + h * 0.31,
        subtitle,
        ha="center",
        va="center",
        fontsize=subtitle_size,
        color="#607384",
        linespacing=1.05,
    )


def main():
    fig, ax = plt.subplots(figsize=(6.2, 3.65))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    navy = "#1f2d3a"
    blue = "#2f74b5"
    blue_bg = "#eaf3f7"
    red = "#c74b43"
    red_bg = "#faeee5"
    grey = "#6f7f8d"
    grey_bg = "#f2f5f7"
    line = "#8fa0ad"

    ax.text(
        5,
        5.52,
        "Cell classification: deformation relevance × public-product observability",
        ha="center",
        va="center",
        fontsize=10.2,
        fontweight="bold",
        color=navy,
    )

    x0, y0 = 2.0, 1.4
    cw, ch = 2.75, 1.5
    gap = 0.55
    rh = 0.55

    ax.text(x0 + cw / 2, y0 + 2 * ch + 0.35, "Majority observable", ha="center", va="bottom", fontsize=7.4, fontweight="bold", color=navy)
    ax.text(x0 + cw + gap + cw / 2, y0 + 2 * ch + 0.35, "Not majority observable", ha="center", va="bottom", fontsize=7.4, fontweight="bold", color=navy)

    ax.text(x0 - 0.48, y0 + ch + ch / 2, "Passes frozen\nstrong-deformation\nscreen", ha="right", va="center", fontsize=6.8, fontweight="bold", color="#b35a1f", linespacing=0.98)
    ax.text(x0 - 0.48, y0 + ch / 2, "Does not pass\nscreen", ha="right", va="center", fontsize=6.8, color=grey, linespacing=0.98)

    add_cell(
        ax,
        x0,
        y0 + ch,
        cw,
        ch,
        blue_bg,
        line,
        "Visible exposure",
        r"$D = 1$, $O \geq \tau_O$" + "\ncounted as product-supported",
        blue,
    )
    add_cell(
        ax,
        x0 + cw + gap,
        y0 + ch,
        cw,
        ch,
        red_bg,
        red,
        "Hidden exposure\nretained",
        r"$D = 1$, $O < \tau_O$" + "\nenters audit account",
        red,
    )
    add_cell(
        ax,
        x0,
        y0,
        cw,
        ch,
        grey_bg,
        line,
        "Observable background",
        r"$O \geq \tau_O$ but $D = 0$" + "\nnot in deformation screen",
        grey,
        alpha=0.82,
        title_size=7.6,
        subtitle_size=5.9,
    )
    add_cell(
        ax,
        x0 + cw + gap,
        y0,
        cw,
        ch,
        "#f7f3eb",
        line,
        "Low-support background",
        r"$O < \tau_O$ but $D = 0$" + "\nnot counted as hidden exposure",
        grey,
        alpha=0.82,
        title_size=7.6,
        subtitle_size=5.9,
    )

    # Highlight the only quadrant used by the hidden-exposure estimator.
    ax.add_patch(
        Rectangle(
            (x0 + cw + gap - 0.08, y0 + ch - 0.08),
            cw + 0.16,
            ch + 0.16,
            facecolor="none",
            edgecolor=red,
            linewidth=2.0,
        )
    )
    arrow_x = x0 + cw + gap + cw + 0.32
    ax.add_patch(
        FancyArrowPatch(
            (arrow_x, y0 + ch + 0.18),
            (arrow_x, 0.92),
            arrowstyle="-|>",
            mutation_scale=9,
            linewidth=1.2,
            color=red,
            connectionstyle="arc3,rad=0",
        )
    )
    ax.text(
        x0 + cw + gap + cw / 2,
        0.53,
        "Only this intersection is reported as hidden exposure.",
        ha="center",
        va="center",
        fontsize=7.0,
        fontweight="bold",
        color=red,
    )

    ax.text(5, 0.18, r"$D$: frozen deformation-screen indicator; $O$: public-product observability fraction; $\tau_O$: majority-observable threshold.", ha="center", va="center", fontsize=6.2, color="#607384")

    base = OUT / "ESIN_Figure_1"
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(base.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    with (OUT / "ESIN_Figure_1_source_data.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class", "deformation_screen", "observability_class", "accounting_role"])
        writer.writerow(["visible_exposure", "D=1", "O>=tau_O", "product-supported exposure"])
        writer.writerow(["hidden_exposure_retained", "D=1", "O<tau_O", "hidden-exposure audit account"])
        writer.writerow(["observable_background", "D=0", "O>=tau_O", "not in deformation screen"])
        writer.writerow(["low_support_background", "D=0", "O<tau_O", "not counted as hidden exposure"])


if __name__ == "__main__":
    main()
