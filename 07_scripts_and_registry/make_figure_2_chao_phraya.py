from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap, Normalize


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
FIG_DIR = ROOT / "09_figures_v1"
FIG_DIR.mkdir(parents=True, exist_ok=True)

AREA_SUMMARY = ROOT / "03_exposure_closure" / "chao_phraya_area_weighted_exposure_censoring" / "chao_phraya_area_weighted_exposure_summary.csv"
AREA_CELLS = ROOT / "03_exposure_closure" / "chao_phraya_area_weighted_exposure_censoring" / "chao_phraya_area_weighted_exposure_cells.csv"
OSM_SUMMARY = ROOT / "03_exposure_closure" / "chao_phraya_osm_exposure_censoring" / "chao_phraya_osm_exposure_censoring_summary.csv"


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


def reconstruct_grid(df: pd.DataFrame, value_col: str) -> np.ndarray:
    rows = int(df["row"].max()) + 1
    cols = int(df["col"].max()) + 1
    grid = np.full((rows, cols), np.nan, dtype=float)
    for _, r in df.iterrows():
        grid[int(r["row"]), int(r["col"])] = float(r[value_col])
    return grid


def add_panel_label(fig: mpl.figure.Figure, ax: mpl.Axes, label: str) -> None:
    pos = ax.get_position()
    fig.text(pos.x0 - 0.02, pos.y1 + 0.01, label, fontsize=9.5, fontweight="bold")


def main() -> int:
    area_summary = pd.read_csv(AREA_SUMMARY).iloc[0]
    cells = pd.read_csv(AREA_CELLS)
    osm = pd.read_csv(OSM_SUMMARY)

    vlm = reconstruct_grid(cells, "vlm_mm_yr")
    hidden = reconstruct_grid(cells, "not_majority_observable")
    strong = reconstruct_grid(cells, "strong_sub_5mm")

    transport = osm[osm["exposure_category"] == "transport_total"].copy()
    transport["pair_year"] = transport["pair"].str.slice(0, 4).astype(int)
    transport = transport.sort_values("pair_year")
    transport["visible_km"] = transport["transport_km_strong_subsidence"] - transport["transport_km_hidden_strong_subsidence"]

    fig = plt.figure(figsize=(7.4, 5.9), constrained_layout=False)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.98], width_ratios=[1.02, 1.0], hspace=0.34, wspace=0.26)

    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    # Panel A: VLM map
    vm = ax_a.imshow(np.ma.masked_invalid(vlm), cmap="RdBu_r", vmin=-16, vmax=4, origin="upper")
    ax_a.set_xticks([])
    ax_a.set_yticks([])
    ax_a.set_title("A  VLM field", loc="left", fontweight="bold")
    cb_a = fig.colorbar(vm, ax=ax_a, fraction=0.046, pad=0.02)
    cb_a.set_label("VLM (mm/yr)")

    # Panel B: hidden fraction map
    hm = ax_b.imshow(np.ma.masked_invalid(hidden), cmap=ListedColormap(["#F2F2F2", "#D95F02"]), vmin=0, vmax=1, origin="upper")
    ax_b.set_xticks([])
    ax_b.set_yticks([])
    ax_b.set_title("B  Hidden cells", loc="left", fontweight="bold")
    cb_b = fig.colorbar(hm, ax=ax_b, fraction=0.046, pad=0.02, ticks=[0, 1])
    cb_b.ax.set_yticklabels(["majority visible", "not majority visible"])

    # Panel C: population and built-up exposure bars
    labels = ["total", "strong", "hidden strong"]
    pop_vals = [
        float(area_summary["total_population_vlm_grid"]) / 1_000_000.0,
        float(area_summary["strong_sub_5mm_population"]) / 1_000_000.0,
        float(area_summary["strong_sub_5mm_population_not_majority"]) / 1_000_000.0,
    ]
    built_vals = [
        float(area_summary["total_builtup_km2_vlm_grid"]),
        float(area_summary["strong_sub_5mm_builtup_km2"]),
        float(area_summary["strong_sub_5mm_builtup_not_majority_km2"]),
    ]
    x = np.arange(len(labels))
    width = 0.35
    ax_c2 = ax_c.twinx()
    b1 = ax_c.bar(x - width / 2, pop_vals, width=width, color="#5E81AC", label="Population (M)", zorder=3)
    b2 = ax_c2.bar(x + width / 2, built_vals, width=width, color="#D08770", label="Built-up (km$^2$)", zorder=3)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(labels)
    ax_c.set_ylabel("Population (million)")
    ax_c2.set_ylabel("Built-up (km$^2$)", labelpad=10)
    ax_c2.yaxis.set_label_coords(1.08, 0.5)
    ax_c2.tick_params(axis="y", pad=3)
    ax_c.set_title("C  Population and built-up exposure", loc="left", fontweight="bold")
    ax_c.grid(axis="y", color="#E1E5EE", linewidth=0.7, zorder=0)
    handles = [b1, b2]
    labels_legend = ["Population", "Built-up"]
    ax_c.legend(handles, labels_legend, loc="upper left", fontsize=6.5)
    ax_c2.set_ylim(0, max(built_vals) * 1.18)
    ax_c.set_ylim(0, max(pop_vals) * 1.18)

    # Panel D: transport bars over time
    years = transport["pair_year"].to_numpy()
    visible = transport["visible_km"].to_numpy()
    hidden_km = transport["transport_km_hidden_strong_subsidence"].to_numpy()
    ax_d.bar(years, visible, color="#4C566A", width=0.6, label="Visible", zorder=3)
    ax_d.bar(years, hidden_km, bottom=visible, color="#A3BE8C", width=0.6, label="Hidden", zorder=3)
    ax_d.set_xlabel("Year")
    ax_d.set_ylabel("Transport length (km)")
    ax_d.set_title("D  Transport exposure by year", loc="left", fontweight="bold")
    ax_d.grid(axis="y", color="#E1E5EE", linewidth=0.7, zorder=0)
    ax_d.legend(loc="upper right", fontsize=6.5)

    # Supplemental note
    fig.text(
        0.52,
        0.01,
        f"Chao Phraya lead-case summary: hidden fraction of strong-subsidence population = {float(area_summary['strong_sub_5mm_population_not_majority_fraction']):.3f}; "
        f"hidden fraction of strong-subsidence built-up = {float(area_summary['strong_sub_5mm_builtup_not_majority_fraction']):.3f}.",
        ha="center",
        fontsize=6.2,
        color="#3B4252",
    )

    fig.suptitle(
        "Chao Phraya lead case: area-weighted exposure and transport censorship",
        y=0.995,
        fontsize=9.2,
        fontweight="bold",
    )

    save_pub(fig, "fig2_chao_phraya_lead_case")
    meta = {
        "area_summary": str(AREA_SUMMARY),
        "area_cells": str(AREA_CELLS),
        "osm_summary": str(OSM_SUMMARY),
        "output_dir": str(FIG_DIR),
    }
    (FIG_DIR / "fig2_chao_phraya_lead_case_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    plt.close(fig)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
