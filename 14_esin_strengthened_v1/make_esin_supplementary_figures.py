import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.parent / "03_exposure_closure"
MAUP = DATA_ROOT / "chao_phraya_maup_sensitivity_v1" / "chao_phraya_maup_sensitivity_v1.csv"
PLACEBO_SUMMARY = DATA_ROOT / "chao_phraya_placebo_randomization_v1" / "chao_phraya_placebo_randomization_summary_v1.csv"
PLACEBO_DRAWS = DATA_ROOT / "chao_phraya_placebo_randomization_v1" / "chao_phraya_placebo_randomization_draws_v1.csv"

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

COL = {
    "pop": "#2f78bd",
    "built": "#c9822b",
    "gray": "#6f7d8a",
    "dark": "#263238",
    "red": "#c84d42",
    "green": "#5a9367",
    "grid": "#e1e7eb",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def f(v):
    try:
        return float(v)
    except Exception:
        return np.nan


def save(fig, stem):
    fig.savefig(ROOT / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(ROOT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(ROOT / f"{stem}.tiff", dpi=600, bbox_inches="tight")
    fig.savefig(ROOT / f"{stem}.png", dpi=220, bbox_inches="tight")


def make_s1_maup():
    rows = read_csv(MAUP)
    block_sizes = sorted({int(r["block_size"]) for r in rows})
    pop_by_block = []
    built_by_block = []
    nblocks_by_block = []
    for bs in block_sizes:
        sub = [r for r in rows if int(r["block_size"]) == bs]
        pop_by_block.append([f(r["strong_hidden_population_fraction"]) for r in sub])
        built_by_block.append([f(r["strong_hidden_builtup_fraction"]) for r in sub])
        nblocks_by_block.append([f(r["n_blocks"]) for r in sub])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.05), gridspec_kw={"wspace": 0.35})
    pos = np.arange(len(block_sizes))
    width = 0.34
    bp1 = ax1.boxplot(pop_by_block, positions=pos - width / 2, widths=0.25, patch_artist=True, showfliers=False)
    bp2 = ax1.boxplot(built_by_block, positions=pos + width / 2, widths=0.25, patch_artist=True, showfliers=False)
    for patch in bp1["boxes"]:
        patch.set(facecolor=COL["pop"], alpha=0.72, edgecolor=COL["pop"])
    for patch in bp2["boxes"]:
        patch.set(facecolor=COL["built"], alpha=0.72, edgecolor=COL["built"])
    for key in ["whiskers", "caps", "medians"]:
        for line in bp1[key]:
            line.set(color=COL["pop"], lw=1.0)
        for line in bp2[key]:
            line.set(color=COL["built"], lw=1.0)
    for i, vals in enumerate(pop_by_block):
        ax1.scatter(np.full(len(vals), pos[i] - width / 2), vals, s=12, color=COL["pop"], edgecolor="white", linewidth=0.4, zorder=3)
    for i, vals in enumerate(built_by_block):
        ax1.scatter(np.full(len(vals), pos[i] + width / 2), vals, s=12, color=COL["built"], edgecolor="white", linewidth=0.4, zorder=3)
    ax1.set_xticks(pos)
    ax1.set_xticklabels([str(b) for b in block_sizes])
    ax1.set_xlabel("Block size, cells")
    ax1.set_ylabel("Hidden share within strong exposure")
    ax1.set_title("Exposure fractions were stable", loc="left", fontweight="bold", pad=7)
    ax1.set_ylim(0.17, 0.355)
    ax1.grid(axis="y", color=COL["grid"], lw=0.6)
    ax1.legend(
        handles=[
            mpl.patches.Patch(color=COL["pop"], alpha=0.72, label="Population"),
            mpl.patches.Patch(color=COL["built"], alpha=0.72, label="Built-up"),
        ],
        loc="lower center",
        bbox_to_anchor=(0.68, 0.04),
        ncol=2,
        handlelength=1.3,
        columnspacing=0.9,
    )

    med_n = [np.median(v) for v in nblocks_by_block]
    ax2.plot(block_sizes, med_n, marker="o", color=COL["dark"], lw=1.6)
    ax2.set_xscale("log")
    ax2.set_xticks(block_sizes)
    ax2.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax2.set_xlabel("Block size, cells")
    ax2.set_ylabel("Median reporting blocks")
    ax2.set_title("Aggregation changed reporting units", loc="left", fontweight="bold", pad=7)
    ax2.grid(axis="both", color=COL["grid"], lw=0.6)
    for x, y in zip(block_sizes, med_n):
        ax2.text(x, y * 1.04, f"{y:.0f}", ha="center", va="bottom", fontsize=6)

    fig.tight_layout()
    save(fig, "ESIN_Supplementary_Figure_S1")


def make_s2_placebo():
    draws = read_csv(PLACEBO_DRAWS)
    summary = read_csv(PLACEBO_SUMMARY)

    def draw_values(model, metric):
        return np.array([f(r[metric]) for r in draws if r["null_model"] == model])

    def observed(model, metric):
        for r in summary:
            if r["null_model"] == model and r["metric"] == metric:
                return f(r["observed"]), f(r["null_q025"]), f(r["null_q975"]), f(r["two_sided_empirical_p"])
        return np.nan, np.nan, np.nan, np.nan

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw={"wspace": 0.34})

    model1 = "strong_label_spatial_8x8_cells"
    vals1 = draw_values(model1, "strong_notmajority_or")
    obs1, q1lo, q1hi, p1 = observed(model1, "strong_notmajority_or")
    ax1.hist(vals1, bins=36, color="#c9d6df", edgecolor="white")
    ax1.axvspan(q1lo, q1hi, color="#9eb4c3", alpha=0.28, label="95% null interval")
    ax1.axvline(obs1, color=COL["red"], lw=1.8, label="Observed")
    ax1.set_xlabel("Strong-not-majority odds ratio")
    ax1.set_ylabel("Placebo iterations")
    ax1.set_title("Strong labels exceeded spatial null", loc="left", fontweight="bold", pad=7)
    ax1.grid(axis="y", color=COL["grid"], lw=0.6)
    ax1.text(
        obs1 * 0.88,
        ax1.get_ylim()[1] * 0.78,
        f"Observed {obs1:.2f}\nnull mean 3.38\np={p1:.4f}",
        ha="right",
        va="top",
        fontsize=6,
        color=COL["red"],
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=2),
    )
    ax1.legend(loc="upper right")

    models = [
        "hidden_mask_global_strong_cells",
        "hidden_mask_spatial_8x8_strong_cells",
        "hidden_mask_deformation_decile_strong_cells",
        "hidden_mask_spatial4_deformation5_strong_cells",
    ]
    labels = ["Global", "Spatial", "Deformation", "Spatial +\ndeformation"]
    obs_pop = []
    null_mean = []
    qlo = []
    qhi = []
    for m in models:
        row = next(r for r in summary if r["null_model"] == m and r["metric"] == "hidden_population_in_strong_people")
        obs_pop.append(f(row["observed"]) / 1e6)
        null_mean.append(f(row["null_mean"]) / 1e6)
        qlo.append(f(row["null_q025"]) / 1e6)
        qhi.append(f(row["null_q975"]) / 1e6)
    x = np.arange(len(models))
    yerr = [np.array(null_mean) - np.array(qlo), np.array(qhi) - np.array(null_mean)]
    ax2.errorbar(x, null_mean, yerr=yerr, fmt="o", color=COL["dark"], capsize=3, lw=1.2, label="Null mean and 95% interval")
    ax2.scatter(x, obs_pop, s=36, color=COL["red"], edgecolor="white", linewidth=0.5, zorder=3, label="Observed")
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.set_ylabel("Hidden population in strong cells, million")
    ax2.set_title("Hidden mask was not an upper-tail artefact", loc="left", fontweight="bold", pad=7)
    ax2.grid(axis="y", color=COL["grid"], lw=0.6)
    ax2.legend(loc="upper right", fontsize=6)
    ax2.text(x[0] - 0.1, obs_pop[0] + 0.4, "Observed\n3.77 M", color=COL["red"], fontsize=6, ha="left")

    fig.tight_layout()
    save(fig, "ESIN_Supplementary_Figure_S2")


if __name__ == "__main__":
    make_s1_maup()
    make_s2_placebo()
