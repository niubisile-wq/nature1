from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "03_exposure_closure"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
})


def save_pub(fig, stem):
    for ext, kwargs in {
        "pdf": {},
        "svg": {},
        "png": {"dpi": 300},
        "tiff": {"dpi": 600},
    }.items():
        fig.savefig(ROOT / f"{stem}.{ext}", bbox_inches="tight", **kwargs)


def main():
    region = pd.read_csv(
        DATA / "multi_region_summary_meta_closure_v1" / "multi_region_meta_closure_region_table.csv"
    )
    loo = pd.read_csv(
        DATA / "multi_region_summary_meta_closure_v1" / "multi_region_meta_closure_leave_one_out.csv"
    )
    dwr = pd.read_csv(
        DATA / "dwr_ngl_external_validation_v1" / "dwr_ngl_station_validation_stats_v1.csv"
    )

    region = region.sort_values("landcover_adjusted_or")
    loo = loo.sort_values("pooled_random_or")

    source_rows = []
    for _, r in region.iterrows():
        source_rows.append({
            "panel": "A",
            "region": r["region"],
            "estimate": r["landcover_adjusted_or"],
            "low": r["landcover_adjusted_boot_q025"],
            "high": r["landcover_adjusted_boot_q975"],
            "n_cells": r["n_cells"],
            "anchor": r["independent_anchor_status"],
        })
    for _, r in loo.iterrows():
        source_rows.append({
            "panel": "B",
            "region": f"without {r['left_out_region']}",
            "estimate": r["pooled_random_or"],
            "low": r["pooled_random_ci_low"],
            "high": r["pooled_random_ci_high"],
            "n_cells": np.nan,
            "anchor": "leave-one-out",
        })
    for _, r in dwr.iterrows():
        source_rows.append({
            "panel": "C",
            "region": f"{r['site']} {r['service_key']}",
            "estimate": r["same_sign_negative_fraction"],
            "low": np.nan,
            "high": np.nan,
            "n_cells": r["n_valid_dwr_ngl_pairs"],
            "anchor": "DWR/NGL sign concordance",
        })
    pd.DataFrame(source_rows).to_csv(ROOT / "ESIN_Supplementary_Figure_S3_source_data.csv", index=False)

    fig = plt.figure(figsize=(7.2, 5.8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 0.9], width_ratios=[1.25, 1.0], hspace=0.45, wspace=0.36)
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])

    y = np.arange(len(region))
    colors = ["#7a8793" if x == "inconclusive" else "#2f78bd" for x in region["observability_bias_signal"]]
    ax1.errorbar(
        region["landcover_adjusted_or"],
        y,
        xerr=[
            region["landcover_adjusted_or"] - region["landcover_adjusted_boot_q025"],
            region["landcover_adjusted_boot_q975"] - region["landcover_adjusted_or"],
        ],
        fmt="none",
        ecolor="#6d7c88",
        elinewidth=1.1,
        capsize=2.5,
        zorder=1,
    )
    ax1.scatter(region["landcover_adjusted_or"], y, s=34, c=colors, edgecolor="white", linewidth=0.6, zorder=3)
    ax1.axvline(1, color="#222222", lw=0.9, ls=":")
    ax1.set_yticks(y)
    ax1.set_yticklabels(region["region"])
    ax1.set_xscale("log")
    ax1.set_xlabel("Land-cover-adjusted odds ratio")
    ax1.set_title("A  Transfer signal across regions", loc="left", fontweight="bold")
    ax1.grid(axis="x", color="#e1e7ec", lw=0.7)
    for yi, (_, r) in enumerate(region.iterrows()):
        ax1.text(r["landcover_adjusted_boot_q975"] * 1.05, yi, f"n={int(r['n_cells'])}", va="center", fontsize=6, color="#5d6f7f")

    y2 = np.arange(len(loo))
    ax2.errorbar(
        loo["pooled_random_or"],
        y2,
        xerr=[
            loo["pooled_random_or"] - loo["pooled_random_ci_low"],
            loo["pooled_random_ci_high"] - loo["pooled_random_or"],
        ],
        fmt="o",
        color="#c77c24",
        ecolor="#9f6722",
        markersize=4,
        capsize=2.3,
        lw=1.1,
    )
    ax2.axvline(1, color="#222222", lw=0.9, ls=":")
    ax2.set_yticks(y2)
    ax2.set_yticklabels(loo["left_out_region"].map(lambda x: f"without {x}"), fontsize=6)
    ax2.set_xscale("log")
    ax2.set_xlabel("Pooled random-effects OR")
    ax2.set_title("B  No single-region dependence", loc="left", fontweight="bold")
    ax2.grid(axis="x", color="#e1e7ec", lw=0.7)

    dwr_plot = dwr.copy()
    dwr_plot["label"] = [
        "Fresno\nannual",
        "Fresno\ntotal",
        "Tulare\nannual",
        "Tulare\ntotal",
    ]
    x = np.arange(len(dwr_plot))
    ax3.bar(x, dwr_plot["same_sign_negative_fraction"], color="#3f8f5f", width=0.62)
    ax3.set_ylim(0, 1.08)
    ax3.set_ylabel("Negative-sign concordance")
    ax3.set_xticks(x)
    ax3.set_xticklabels(dwr_plot["label"], fontsize=6)
    ax3.set_title("C  Official raster and station anchor agree in sign", loc="left", fontweight="bold")
    ax3.grid(axis="y", color="#e1e7ec", lw=0.7)
    for xi, (_, r) in enumerate(dwr_plot.iterrows()):
        ax3.text(xi, r["same_sign_negative_fraction"] + 0.035, f"{int(r['n_valid_dwr_ngl_pairs'])} pairs", ha="center", fontsize=6)

    fig.text(
        0.01,
        0.005,
        "Evidence role: panels A-B test transfer and single-region dependence; panel C is an external sign-control probe, not dense validation of the lead case.",
        fontsize=6.6,
        color="#5d6f7f",
    )
    fig.subplots_adjust(bottom=0.14)
    save_pub(fig, "ESIN_Supplementary_Figure_S3")
    plt.close(fig)


if __name__ == "__main__":
    main()
