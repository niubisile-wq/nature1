from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
BENCHMARK = ROOT / "02_benchmark_v0_1" / "benchmark_region_evidence_v0_1.csv"
OBS_MASKS = ROOT / "08_nature_experiment_plan" / "observability_masks_v1.csv"
EXPOSURE_TRANSLATION = ROOT / "08_nature_experiment_plan" / "multi_region_exposure_translation_v1.csv"
OSM_SUMMARY = ROOT / "03_exposure_closure" / "chao_phraya_osm_exposure_censoring" / "chao_phraya_osm_exposure_censoring_summary.csv"

OUTDIR = ROOT / "03_exposure_closure" / "final_multi_region_equal_area_closure_v1"
PLAN_MD = ROOT / "08_nature_experiment_plan" / "final_multi_region_equal_area_closure_v1.md"
PLAN_CSV = ROOT / "08_nature_experiment_plan" / "final_multi_region_equal_area_closure_v1.csv"
NOFIT_MD = ROOT / "08_nature_experiment_plan" / "all_region_cell_level_no_fit_justification_v1.md"

SOURCE_ROOT = ROOT / "11_submission_ready_v1" / "source_data"
SOURCE_DIR = SOURCE_ROOT / "final_multi_region_equal_area_closure_v1"
SOURCE_PLAN_MD = SOURCE_ROOT / "final_multi_region_equal_area_closure_v1.md"
SOURCE_PLAN_CSV = SOURCE_ROOT / "final_multi_region_equal_area_closure_v1.csv"
SOURCE_NOFIT_MD = SOURCE_ROOT / "all_region_cell_level_no_fit_justification_v1.md"


REGION_META = {
    "Po": {
        "role": "supporting_case",
        "product_family": "open_delta_vlm_benchmark",
        "overlay_method": "equal_area_cell_overlap_proxy",
        "weighting_status": "area_weighted_proxy",
        "claim_status": "supporting_case",
    },
    "Chao Phraya": {
        "role": "lead_case",
        "product_family": "open_delta_vlm_benchmark",
        "overlay_method": "equal_area_cell_overlap",
        "weighting_status": "area_weighted_closed",
        "claim_status": "lead_case",
    },
    "Brantas": {
        "role": "supporting_case",
        "product_family": "open_delta_vlm_benchmark",
        "overlay_method": "equal_area_cell_overlap_proxy",
        "weighting_status": "area_weighted_proxy",
        "claim_status": "supporting_case",
    },
    "Indus": {
        "role": "transfer_case",
        "product_family": "open_delta_vlm_transfer",
        "overlay_method": "proxy_only",
        "weighting_status": "proxy_only",
        "claim_status": "transfer_case",
    },
    "Rhone": {
        "role": "transfer_case",
        "product_family": "open_delta_vlm_transfer",
        "overlay_method": "proxy_only",
        "weighting_status": "proxy_only",
        "claim_status": "transfer_case",
    },
    "Rhine": {
        "role": "control_case",
        "product_family": "open_delta_vlm_control",
        "overlay_method": "proxy_only",
        "weighting_status": "proxy_only",
        "claim_status": "control_case",
    },
}


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_if_needed(src: Path, dst: Path) -> None:
    ensure_parent(dst)
    shutil.copy2(src, dst)


def load_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    bench = pd.read_csv(BENCHMARK)
    masks = pd.read_csv(OBS_MASKS)
    exposure = pd.read_csv(EXPOSURE_TRANSLATION)
    osm = pd.read_csv(OSM_SUMMARY)
    return bench, masks, exposure, osm


def transport_summary(osm: pd.DataFrame) -> dict[str, float]:
    rows = osm.loc[osm["exposure_category"] == "transport_total"].copy()
    if rows.empty:
        return {"mean": float("nan"), "median": float("nan"), "min": float("nan"), "max": float("nan")}
    values = rows["hidden_strong_subsidence_transport_fraction"].astype(float).to_numpy()
    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
    }


def build_rows(bench: pd.DataFrame, masks: pd.DataFrame, exposure: pd.DataFrame, osm: pd.DataFrame) -> list[dict[str, object]]:
    mask_lookup = masks.set_index("region").to_dict(orient="index")
    exp_lookup = exposure.set_index("region").to_dict(orient="index")
    transport = transport_summary(osm)

    rows: list[dict[str, object]] = []
    for _, row in bench.iterrows():
        region = str(row["region"])
        meta = REGION_META[region]
        mask = mask_lookup.get(region, {})
        exp = exp_lookup.get(region, {})

        strong_cells = mask.get("strong_cells")
        strong_pop = mask.get("strong_sub_5mm_population")
        strong_pop_hidden_frac = mask.get("strong_sub_5mm_population_not_majority_fraction")
        strong_built = mask.get("strong_sub_5mm_builtup_km2")
        strong_built_hidden_frac = mask.get("strong_sub_5mm_builtup_not_majority_fraction")

        observable_fraction = ""
        hidden_population = ""
        hidden_built_up_area = ""
        hidden_transport = ""

        if pd.notna(strong_pop_hidden_frac):
            observable_fraction = float(1.0 - float(mask["strong_sub_5mm_not_majority_fraction"]))
            hidden_population = float(float(strong_pop) * float(strong_pop_hidden_frac))
            hidden_built_up_area = float(float(strong_built) * float(strong_built_hidden_frac))

        if region == "Chao Phraya":
            hidden_transport = (
                f"mean={transport['mean']:.3f}; median={transport['median']:.3f}; "
                f"min={transport['min']:.3f}; max={transport['max']:.3f}"
            )

        exposure_metric = exp.get("key_metric", "")
        role_note = exp.get("interpretation", "")

        rows.append(
            {
                "region": region,
                "role": meta["role"],
                "product_family": meta["product_family"],
                "overlay_method": meta["overlay_method"],
                "cell_count": int(row["n_cells"]),
                "strong_cell_count": "" if pd.isna(strong_cells) else int(strong_cells),
                "observable_fraction": observable_fraction,
                "hidden_population": hidden_population,
                "hidden_built_up_area": hidden_built_up_area,
                "hidden_transport_or_infrastructure": hidden_transport,
                "weighting_status": meta["weighting_status"],
                "claim_status": meta["claim_status"],
                "supporting_metric": exposure_metric,
                "supporting_note": role_note,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, rows: list[dict[str, object]], transport: dict[str, float]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("# Final Multi-Region Equal-Area Closure v1\n")
        fh.write("Date: 2026-07-13\n\n")
        fh.write(
            "This package tightens the benchmark by making the multi-region weighting status explicit. "
            "It is the final equal-area / polygon-facing closure layer for the current manuscript evidence stack.\n\n"
        )
        fh.write("## Region Table\n\n")
        fh.write(
            "| region | role | product_family | overlay_method | cell_count | strong_cell_count | observable_fraction | hidden_population | hidden_built_up_area | hidden_transport_or_infrastructure | weighting_status | claim_status |\n"
        )
        fh.write("|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|\n")
        for row in rows:
            obs = "" if row["observable_fraction"] == "" else f"{float(row['observable_fraction']):.6f}"
            hidden_pop = "" if row["hidden_population"] == "" else f"{float(row['hidden_population']):.3f}"
            hidden_built = "" if row["hidden_built_up_area"] == "" else f"{float(row['hidden_built_up_area']):.3f}"
            fh.write(
                f"| {row['region']} | {row['role']} | {row['product_family']} | {row['overlay_method']} | "
                f"{row['cell_count']} | {row['strong_cell_count']} | {obs} | {hidden_pop} | {hidden_built} | "
                f"{row['hidden_transport_or_infrastructure']} | {row['weighting_status']} | {row['claim_status']} |\n"
            )
        fh.write("\n## Transport Anchor\n\n")
        fh.write(
            f"- Chao Phraya transport hidden fraction mean: {transport['mean']:.3f}\n"
            f"- median: {transport['median']:.3f}\n"
            f"- min: {transport['min']:.3f}\n"
            f"- max: {transport['max']:.3f}\n\n"
        )
        fh.write("## Bottom Line\n\n")
        fh.write(
            "Chao Phraya is the only lead case with a closed equal-area / polygon-facing exposure package. "
            "Po and Brantas remain supporting area-weighted proxies. Indus, Rhone, and Rhine stay explicit proxy or control cases and are not silently promoted to lead status.\n"
        )


def write_nofit_note(path: Path) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("# All-Region Cell-Level No-Fit Justification v1\n")
        fh.write("Date: 2026-07-13\n\n")
        fh.write("## Decision\n\n")
        fh.write(
            "A new all-region cell-level hierarchical fit is not being claimed because the current workspace does not contain a harmonized region-wide cell-level response matrix for all benchmark regions.\n\n"
        )
        fh.write("## Why This Is The Correct Boundary\n\n")
        fh.write(
            "- Chao Phraya has a frozen cell-level anchor and can support a lead-case hierarchical closure.\n"
            "- The other benchmark regions are available as region-level summaries, area-weighted proxies, or transfer cases.\n"
            "- Converting those summaries into a new cell-level all-region fit would require fabricating cell-level rows or mixing incompatible resolutions, which would not survive a reviewer audit.\n"
            "- The closure-by-compilation package is therefore the honest substitute until a true harmonized all-region cell table exists.\n\n"
        )
        fh.write("## What The Paper Can Say Instead\n\n")
        fh.write(
            "- The manuscript can defend a frozen hierarchical comparison.\n"
            "- The manuscript can defend a closure-by-compilation all-region package.\n"
            "- The manuscript should explicitly state that the all-region cell-level fit remains unavailable rather than overclaiming it.\n\n"
        )
        fh.write("## Practical Implication\n\n")
        fh.write(
            "This note closes the reviewer-facing gap by making the non-fit explicit. It strengthens the paper because it removes the impression that a missing model was simply omitted after the fact.\n"
        )


def main() -> None:
    bench, masks, exposure, osm = load_tables()
    rows = build_rows(bench, masks, exposure, osm)
    transport = transport_summary(osm)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "region",
        "role",
        "product_family",
        "overlay_method",
        "cell_count",
        "strong_cell_count",
        "observable_fraction",
        "hidden_population",
        "hidden_built_up_area",
        "hidden_transport_or_infrastructure",
        "weighting_status",
        "claim_status",
        "supporting_metric",
        "supporting_note",
    ]

    out_csv = OUTDIR / "final_multi_region_equal_area_closure_summary.csv"
    out_md = OUTDIR / "final_multi_region_equal_area_closure_report.md"
    out_meta = OUTDIR / "final_multi_region_equal_area_closure_meta.json"

    write_csv(out_csv, rows, fieldnames)
    write_report(out_md, rows, transport)
    out_meta.write_text(
        json.dumps(
            {
                "artifact": "final_multi_region_equal_area_closure_v1",
                "sources": {
                    "benchmark": str(BENCHMARK),
                    "observability_masks": str(OBS_MASKS),
                    "exposure_translation": str(EXPOSURE_TRANSLATION),
                    "osm_summary": str(OSM_SUMMARY),
                },
                "regions": [row["region"] for row in rows],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    write_csv(PLAN_CSV, rows, fieldnames)
    write_report(PLAN_MD, rows, transport)
    write_nofit_note(NOFIT_MD)

    copy_if_needed(out_csv, SOURCE_DIR / "final_multi_region_equal_area_closure_summary.csv")
    copy_if_needed(out_md, SOURCE_DIR / "final_multi_region_equal_area_closure_report.md")
    copy_if_needed(out_meta, SOURCE_DIR / "final_multi_region_equal_area_closure_meta.json")

    copy_if_needed(PLAN_CSV, SOURCE_PLAN_CSV)
    copy_if_needed(PLAN_MD, SOURCE_PLAN_MD)
    copy_if_needed(NOFIT_MD, SOURCE_NOFIT_MD)


if __name__ == "__main__":
    main()
