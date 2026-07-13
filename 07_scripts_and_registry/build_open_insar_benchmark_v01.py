from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_ROOT = Path(r"C:\Users\刘子轩\radar_outputs")
OUTDIR = OUTPUT_ROOT / "open_insar_observability_benchmark_v0_1"

DELTA_WORLDCOVER = OUTPUT_ROOT / "delta_binomial_with_worldcover_main"
EXTENDED_MODEL = OUTPUT_ROOT / "extended_region_binomial_with_candidates"
RESCUE_PROBE = OUTPUT_ROOT / "rescue_dataset_probe"
EGMS_QUERY_PACK = OUTPUT_ROOT / "egms_api_rescue_queries"
JAPAN_SELECTED_PROBE = OUTPUT_ROOT / "japan_licsbas_selected_probe"


REGION_TO_NGL = {
    "Po": "Po_delta_core",
    "Rhone": "Rhone_core",
    "Rhine": "Rhine_core",
    "Chao Phraya": "Chao_Phraya_core",
    "Brantas": "Brantas_core",
    "Indus": "Indus_core",
    "Central Valley": "Central_Valley_large",
}

EUROPE_EGMS_STATUS = {
    "Po": "query_pack_ready_token_required",
    "Rhone": "query_pack_ready_token_required",
    "Rhine": "query_pack_ready_token_required",
}

PRIMARY_REGIONS = ["Po", "Chao Phraya", "Indus", "Rhone", "Brantas", "Rhine"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value in ("", None, "nan"):
            return default
        return float(value)
    except Exception:
        return default


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def region_meta(meta: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in meta.get("regions", []):
        name = row.get("region") or row.get("delta")
        if name:
            out[str(name)] = row
    return out


def effect_by_region(path: Path, effect_prefix: str = "avg_strong_effect:") -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        effect = row.get("effect", "")
        region = effect.removeprefix(effect_prefix)
        out[region] = row
    return out


def bootstrap_by_region(path: Path) -> dict[str, dict[str, str]]:
    return {row["effect"]: row for row in read_csv(path)}


def ngl_screen_by_region(path: Path) -> dict[str, dict[str, str]]:
    return {row["region"]: row for row in read_csv(path)}


def landcover_summary(path: Path) -> dict[str, dict[str, float | str]]:
    rows = read_csv(path)
    out: dict[str, dict[str, float | str]] = {}
    for row in rows:
        region = row["region"]
        rec = out.setdefault(
            region,
            {
                "dominant_landcover": "",
                "dominant_landcover_fraction": 0.0,
                "max_failure_landcover": "",
                "max_failure_rate": -1.0,
                "cropland_fraction": 0.0,
                "built_up_fraction": 0.0,
                "water_wetland_mangrove_fraction": 0.0,
            },
        )
        lc = row["landcover_group"]
        frac = as_float(row.get("cell_fraction_in_region"), 0.0) or 0.0
        fail = as_float(row.get("failure_rate"), -1.0) or -1.0
        if frac > float(rec["dominant_landcover_fraction"]):
            rec["dominant_landcover"] = lc
            rec["dominant_landcover_fraction"] = frac
        if fail > float(rec["max_failure_rate"]):
            rec["max_failure_landcover"] = lc
            rec["max_failure_rate"] = fail
        if lc in {"cropland", "built_up", "water_wetland_mangrove"}:
            rec[f"{lc}_fraction"] = frac
    return out


def classify_signal(or_value: float | None, boot_low: float | None, boot_high: float | None) -> str:
    if or_value is None or boot_low is None or boot_high is None:
        return "missing"
    if boot_low > 1.0:
        if or_value >= 3.0:
            return "strong_positive"
        return "positive"
    if boot_high < 1.0:
        return "negative"
    return "inconclusive"


def classify_nature_readiness(signal: str, n_gnss: int, egms_status: str) -> str:
    has_sparse_anchor = n_gnss >= 5
    if signal in {"strong_positive", "positive"} and has_sparse_anchor and egms_status == "query_pack_ready_token_required":
        return "conditional_nature_go_after_egms"
    if signal in {"strong_positive", "positive"} and has_sparse_anchor:
        return "benchmark_v0_landed_needs_dense_truth"
    if signal in {"strong_positive", "positive"}:
        return "statistical_signal_needs_independent_anchor"
    if signal == "inconclusive":
        return "control_or_specification_case"
    return "do_not_lead"


def build_region_evidence() -> list[dict[str, Any]]:
    meta = load_json(DELTA_WORLDCOVER / "delta_worldcover_meta.json")
    meta_by_region = region_meta(meta)
    effects = effect_by_region(DELTA_WORLDCOVER / "delta_worldcover_avg_strong_effects.csv")
    boot = bootstrap_by_region(DELTA_WORLDCOVER / "delta_worldcover_avg_strong_bootstrap.csv")
    lc = landcover_summary(DELTA_WORLDCOVER / "delta_worldcover_landcover_summary.csv")
    ngl = ngl_screen_by_region(RESCUE_PROBE / "ngl_region_station_screen.csv")

    rows: list[dict[str, Any]] = []
    for region in PRIMARY_REGIONS:
        m = meta_by_region.get(region, {})
        eff = effects.get(region) or effects.get(f"avg_strong_effect:{region}", {})
        b = boot.get(region, {})
        lcr = lc.get(region, {})
        ngl_name = REGION_TO_NGL.get(region, "")
        nglr = ngl.get(ngl_name, {})
        or_value = as_float(eff.get("odds_ratio"))
        boot_low = as_float(b.get("odds_ratio_boot_q025"))
        boot_high = as_float(b.get("odds_ratio_boot_q975"))
        signal = classify_signal(or_value, boot_low, boot_high)
        n_gnss = int(float(nglr.get("n_stations", 0) or 0))
        egms_status = EUROPE_EGMS_STATUS.get(region, "not_applicable")
        rows.append(
            {
                "region": region,
                "frame_id": m.get("frame_id", ""),
                "bbox_wgs84": bbox_to_text(m.get("bbox", {})),
                "n_lisc_pairs": m.get("n_pairs", ""),
                "n_cells": m.get("n_cells", ""),
                "landcover_adjusted_or": fmt(or_value),
                "landcover_adjusted_boot_q025": fmt(boot_low),
                "landcover_adjusted_boot_q975": fmt(boot_high),
                "observability_bias_signal": signal,
                "bias_or_minus_one_proxy": fmt((or_value - 1.0) if or_value is not None else None),
                "dominant_landcover": lcr.get("dominant_landcover", ""),
                "dominant_landcover_fraction": fmt(lcr.get("dominant_landcover_fraction")),
                "cropland_fraction": fmt(lcr.get("cropland_fraction")),
                "built_up_fraction": fmt(lcr.get("built_up_fraction")),
                "water_wetland_mangrove_fraction": fmt(lcr.get("water_wetland_mangrove_fraction")),
                "max_failure_landcover": lcr.get("max_failure_landcover", ""),
                "max_failure_rate": fmt(lcr.get("max_failure_rate")),
                "ngl_region": ngl_name,
                "ngl_station_count": n_gnss,
                "ngl_median_up_mmyr": nglr.get("median_up_mmyr", ""),
                "independent_anchor_status": "sparse_gnss_anchor" if n_gnss >= 5 else "weak_or_missing_gnss_anchor",
                "egms_status": egms_status,
                "nature_readiness": classify_nature_readiness(signal, n_gnss, egms_status),
            }
        )
    return rows


def bbox_to_text(bbox: dict[str, Any]) -> str:
    if not bbox:
        return ""
    keys = ["lon_min", "lat_min", "lon_max", "lat_max"]
    return ",".join(str(bbox.get(k, "")) for k in keys)


def fmt(value: Any) -> str:
    number = as_float(value)
    if number is None:
        return ""
    return f"{number:.6g}"


def build_external_candidates() -> list[dict[str, Any]]:
    ngl_rows = read_csv(RESCUE_PROBE / "ngl_region_station_screen.csv")
    japan_probe = load_japan_probe_summary()
    candidate_notes = {
        "Central_Valley_large": "DWR/TRE local InSAR and dense GNSS make this the best no-auth US validation control, but existing model signal is not positive.",
        "Japan_Kanto": "High GNSS station density plus Japan LiCSBAS Zenodo can support a non-US data-product extension; GNSS median uplift means not a simple subsidence lead.",
        "Japan_Niigata": "Dense GNSS plus Japan LiCSBAS candidate; useful for deformation diversity rather than primary subsidence claim.",
        "Mexico_City": "Extreme GNSS subsidence anchors exist; needs open InSAR product ingestion and exposure overlay to become a lead case.",
        "Jakarta": "High policy relevance but sparse NGL anchors; needs separate independent benchmark.",
    }
    rows: list[dict[str, Any]] = []
    for row in ngl_rows:
        region = row["region"]
        if region in REGION_TO_NGL.values():
            continue
        n = int(float(row.get("n_stations", 0) or 0))
        median = as_float(row.get("median_up_mmyr"))
        if n >= 20:
            priority = "A"
        elif n >= 5:
            priority = "B"
        else:
            priority = "C"
        rows.append(
            {
                "candidate": region,
                "priority": priority,
                "ngl_station_count": n,
                "ngl_median_up_mmyr": fmt(median),
                "role": candidate_role(region, n, median),
                "next_data_needed": next_data_needed(region),
                "selected_probe_status": selected_probe_status(region, japan_probe),
                "selected_probe_velocity_median": selected_probe_value(region, japan_probe, "median"),
                "selected_probe_fraction_lt_minus_5": selected_probe_value(region, japan_probe, "fraction_lt_minus_5"),
                "selected_probe_time_steps": selected_probe_time_steps(region, japan_probe),
                "note": candidate_notes.get(region, ""),
            }
        )
    return rows


def load_japan_probe_summary() -> list[dict[str, Any]]:
    path = JAPAN_SELECTED_PROBE / "h5_velocity_summary.json"
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []


def selected_probe_status(region: str, japan_probe: list[dict[str, Any]]) -> str:
    if region != "Japan_Niigata":
        return ""
    if not japan_probe:
        return "not_run"
    if any("cum_filt.h5" in row.get("h5_member", "") for row in japan_probe):
        return "niigata_h5_velocity_ingested"
    return "niigata_zip_downloaded"


def selected_probe_value(region: str, japan_probe: list[dict[str, Any]], key: str) -> str:
    if region != "Japan_Niigata":
        return ""
    selected = None
    for row in japan_probe:
        if "cum_filt.h5" in row.get("h5_member", ""):
            selected = row
            break
    if selected is None and japan_probe:
        selected = japan_probe[0]
    if selected is None:
        return ""
    return fmt(selected.get("velocity_stats", {}).get(key))


def selected_probe_time_steps(region: str, japan_probe: list[dict[str, Any]]) -> str:
    if region != "Japan_Niigata" or not japan_probe:
        return ""
    return str(japan_probe[0].get("n_time_steps", ""))


def candidate_role(region: str, n: int, median: float | None) -> str:
    if region == "Mexico_City":
        return "extreme_subsidence_anchor_case"
    if region.startswith("Japan"):
        return "japan_licsbas_extension_case"
    if region == "Central_Valley_large":
        return "dense_us_control_and_methods_validation"
    if n >= 20 and median is not None and median < -1:
        return "strong_gnss_subsidence_candidate"
    if n >= 20:
        return "dense_gnss_deformation_candidate"
    return "secondary_candidate"


def next_data_needed(region: str) -> str:
    if region.startswith("Japan"):
        return "selective Zenodo LiCSBAS city zip download plus GEONET/GSI or NGL station overlay"
    if region == "Mexico_City":
        return "open InSAR deformation product plus GHSL/Google buildings exposure overlay"
    if region == "Central_Valley_large":
        return "area-weighted exposure overlay and source-data packaging"
    return "independent dense deformation benchmark and exposure overlay"


def build_dataset_inventory() -> list[dict[str, Any]]:
    registry_path = PROJECT_DIR / "dataset_registry_noauth_v2.csv"
    registry = read_csv(registry_path)
    allowed = {
        "ngl_midas_gnss",
        "japan_licsbas_zenodo",
        "ghsl_built_s_r2023a",
        "ms_global_buildings",
        "google_open_buildings_temporal",
    }
    rows = []
    for row in registry:
        if row.get("dataset_id") in allowed:
            rows.append(row)
    rows.extend(
        [
            {
                "dataset_id": "egms_api_query_pack_local",
                "category": "benchmark_scaffold",
                "dataset_name": "Local EGMS API query payload pack for Nature rescue AOIs",
                "provider": "Generated locally from official EGMS API specification",
                "probe_url": str(EGMS_QUERY_PACK / "egms_query_payloads.json"),
                "probe_method": "LOCAL_FILE",
                "role_in_project": "Credential-ready high-density European benchmark scaffold",
                "risk_or_limitation": "Requires CLMS token before actual EGMS product search and download",
                "decision": "primary_benchmark_pending",
            },
            {
                "dataset_id": "delta_worldcover_model_local",
                "category": "analysis_output",
                "dataset_name": "Land-cover-adjusted multi-delta observability-bias model outputs",
                "provider": "Generated locally from public VLM, LiCSAR observability, GHSL and WorldCover inputs",
                "probe_url": str(DELTA_WORLDCOVER),
                "probe_method": "LOCAL_FILE",
                "role_in_project": "Current core evidence table for benchmark v0.1",
                "risk_or_limitation": "Still needs dense independent benchmark closure and area-weighted exposure overlay",
                "decision": "primary_analysis_output",
            },
            {
                "dataset_id": "japan_licsbas_niigata_selected_local",
                "category": "radar_insar_probe",
                "dataset_name": "Selected Niigata LiCSBAS HDF5/GeoTIFF zip from Japan Zenodo record",
                "provider": "Zenodo record 4243151, downloaded and inspected locally",
                "probe_url": str(JAPAN_SELECTED_PROBE),
                "probe_method": "LOCAL_FILE",
                "role_in_project": "Non-US/non-Europe public deformation-product extension smoke test",
                "risk_or_limitation": "LiCSAR/LiCSBAS-derived product, not independent truth; unit convention must be verified before manuscript claims",
                "decision": "secondary_benchmark_ingested",
            },
        ]
    )
    return rows


def write_readme(path: Path, region_rows: list[dict[str, Any]], candidate_rows: list[dict[str, Any]]) -> None:
    positive = [r for r in region_rows if r["observability_bias_signal"] in {"positive", "strong_positive"}]
    conditional = [r for r in region_rows if r["nature_readiness"] == "conditional_nature_go_after_egms"]
    lines = [
        "# Open InSAR Observability Bias and Exposure Benchmark v0.1",
        "",
        "## Scope",
        "",
        "This is a local, reproducible benchmark scaffold for testing whether open InSAR observability gaps censor land-subsidence exposure estimates.",
        "It is not yet a final Nature-grade dataset because dense independent EGMS benchmark closure is still pending.",
        "",
        "## Core metrics",
        "",
        "- `observability_bias_signal`: land-cover-adjusted strong-subsidence effect on public-product failure probability.",
        "- `bias_or_minus_one_proxy`: first-pass proxy for extra observability failure associated with strong subsidence.",
        "- `independent_anchor_status`: whether sparse NGL GNSS anchors exist in the AOI.",
        "- `egms_status`: whether a high-density European EGMS benchmark query is ready.",
        "- `nature_readiness`: current publication-readiness classification.",
        "",
        "## Current result",
        "",
        f"- Primary regions assessed: `{len(region_rows)}`",
        f"- Positive or strong-positive observability-bias signals: `{len(positive)}`",
        f"- Conditional Nature leads after EGMS closure: `{len(conditional)}`",
        f"- External expansion candidates: `{len(candidate_rows)}`",
        "",
        "## Files",
        "",
        "- `benchmark_region_evidence_v0_1.csv`: one row per primary delta/case.",
        "- `benchmark_external_candidates_v0_1.csv`: NGL-screened expansion cases plus selected Japan probe status.",
        "- `benchmark_dataset_inventory_v0_1.csv`: source and derived dataset inventory.",
        "- `benchmark_manifest_v0_1.json`: machine-readable provenance and gate status.",
        "- `benchmark_v0_1_report.md`: human-readable decision report.",
        "",
        "## Immediate blocker",
        "",
        "Nature-level closure requires executing the prepared EGMS API queries with a CLMS token and adding the resulting EGMS L3 ORTHO-UP product manifests and derived validation layers.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(path: Path, region_rows: list[dict[str, Any]], candidate_rows: list[dict[str, Any]]) -> None:
    lead_rows = [r for r in region_rows if r["nature_readiness"] == "conditional_nature_go_after_egms"]
    landed_rows = [r for r in region_rows if r["nature_readiness"] == "benchmark_v0_landed_needs_dense_truth"]
    lines = [
        "# 创新点落地状态：Open InSAR Observability Benchmark v0.1",
        "日期：2026-07-09",
        "",
        "## 现在做的方向",
        "方向已经从普通沉降制图转为：公开 InSAR 产品的可观测性删失是否会系统性低估沉降暴露。",
        "",
        "核心数据产品名：",
        "**Open InSAR Observability Bias and Exposure Benchmark**",
        "",
        "## v0.1 已落地内容",
        "- 多 delta LiCSAR 可观测性与强沉降关系已经统一进一张证据表。",
        "- WorldCover 地表覆盖控制已经纳入主模型。",
        "- NGL GNSS 独立锚点已经接入，用于判断每个区域是否有外部垂向运动约束。",
        "- EGMS API 查询包已经生成，等待 CLMS token 后即可跑欧洲高密度 benchmark。",
        "- 数据源 inventory 已经按 Nature 数据可用性要求分清复用数据、派生数据和本地分析输出。",
        "",
        "## 主结果判定",
        "",
        "| Region | Signal | OR | Boot 95% CI | NGL stations | EGMS | Readiness |",
        "|---|---|---:|---|---:|---|---|",
    ]
    for r in region_rows:
        ci = f"{r['landcover_adjusted_boot_q025']}–{r['landcover_adjusted_boot_q975']}"
        lines.append(
            f"| {r['region']} | {r['observability_bias_signal']} | {r['landcover_adjusted_or']} | "
            f"{ci} | {r['ngl_station_count']} | {r['egms_status']} | {r['nature_readiness']} |"
        )
    lines.extend(
        [
            "",
            "## 现在能不能说创新点落地",
            "**可以说 v0.1 落地，但不能说 Nature 正刊证据最终落地。**",
            "",
            "已经落地的是机制框架和可复现实证骨架：强沉降、公开产品失败概率、地表覆盖、GNSS 锚点和 EGMS 查询路径已经进入同一数据产品。",
            "还没落地的是 Nature 级的高密度独立 benchmark 闭环，也就是 EGMS 下载和对齐。",
            "",
            "## 当前 lead cases",
        ]
    )
    if lead_rows:
        for r in lead_rows:
            lines.append(f"- `{r['region']}`：统计信号 + NGL 锚点 + EGMS 查询包齐备，等 EGMS token 后优先闭环。")
    else:
        lines.append("- 暂无完全满足 Nature lead 条件的区域。")
    if landed_rows:
        lines.append("")
        lines.append("## 无 EGMS 也能继续推进的 v0 cases")
        for r in landed_rows:
            lines.append(f"- `{r['region']}`：已有统计信号和 GNSS 锚点，但仍缺高密度独立 benchmark。")
    lines.extend(
        [
            "",
            "## 外部扩展候选",
            "",
            "| Candidate | Priority | NGL stations | Median up mm/yr | Role |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for r in candidate_rows:
        probe = r.get("selected_probe_status") or "-"
        lines.append(
            f"| {r['candidate']} | {r['priority']} | {r['ngl_station_count']} | "
            f"{r['ngl_median_up_mmyr']} | {r['role']} / {probe} |"
        )
    lines.extend(
        [
            "",
            "## 下一步",
            "1. 拿到 CLMS `token.jwt` 后执行 EGMS 查询包。",
            "2. 对 Po、Rhone、Rhine/Netherlands 下载 L3 ORTHO-UP，并转成统一网格 benchmark。",
            "3. 用 GHSL built-up、GHSL population、OSM/建筑物层做 area-weighted exposure overlay。",
            "4. 输出 figure source data 和仓储 README，准备 Zenodo/Dryad/PANGAEA 记录。",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    region_rows = build_region_evidence()
    candidate_rows = build_external_candidates()
    inventory_rows = build_dataset_inventory()

    region_fields = [
        "region",
        "frame_id",
        "bbox_wgs84",
        "n_lisc_pairs",
        "n_cells",
        "landcover_adjusted_or",
        "landcover_adjusted_boot_q025",
        "landcover_adjusted_boot_q975",
        "observability_bias_signal",
        "bias_or_minus_one_proxy",
        "dominant_landcover",
        "dominant_landcover_fraction",
        "cropland_fraction",
        "built_up_fraction",
        "water_wetland_mangrove_fraction",
        "max_failure_landcover",
        "max_failure_rate",
        "ngl_region",
        "ngl_station_count",
        "ngl_median_up_mmyr",
        "independent_anchor_status",
        "egms_status",
        "nature_readiness",
    ]
    write_csv(OUTDIR / "benchmark_region_evidence_v0_1.csv", region_rows, region_fields)
    write_csv(
        OUTDIR / "benchmark_external_candidates_v0_1.csv",
        candidate_rows,
        [
            "candidate",
            "priority",
            "ngl_station_count",
            "ngl_median_up_mmyr",
            "role",
            "next_data_needed",
            "selected_probe_status",
            "selected_probe_velocity_median",
            "selected_probe_fraction_lt_minus_5",
            "selected_probe_time_steps",
            "note",
        ],
    )
    write_csv(
        OUTDIR / "benchmark_dataset_inventory_v0_1.csv",
        inventory_rows,
        [
            "dataset_id",
            "category",
            "dataset_name",
            "provider",
            "probe_url",
            "probe_method",
            "role_in_project",
            "risk_or_limitation",
            "decision",
        ],
    )

    manifest = {
        "name": "Open InSAR Observability Bias and Exposure Benchmark",
        "version": "v0.1",
        "date": "2026-07-09",
        "status": "landed_scaffold_pending_egms_dense_benchmark",
        "primary_claim": "Open InSAR observability gaps can censor land-subsidence exposure estimates.",
        "nature_gate": {
            "innovation_framework": "pass",
            "multi_region_signal": "partial_pass",
            "landcover_adjustment": "pass",
            "sparse_independent_gnss_anchors": "partial_pass",
            "non_us_public_deformation_product_extension": "pass_niigata_selected_probe",
            "dense_independent_egms_benchmark": "pending_token",
            "area_weighted_exposure_overlay": "pending",
            "nature_readiness": "conditional_go_after_egms",
        },
        "input_outputs": {
            "delta_worldcover_model": str(DELTA_WORLDCOVER),
            "extended_model": str(EXTENDED_MODEL),
            "ngl_probe": str(RESCUE_PROBE),
            "egms_query_pack": str(EGMS_QUERY_PACK),
            "japan_selected_probe": str(JAPAN_SELECTED_PROBE),
        },
        "files": {
            "region_evidence": "benchmark_region_evidence_v0_1.csv",
            "external_candidates": "benchmark_external_candidates_v0_1.csv",
            "dataset_inventory": "benchmark_dataset_inventory_v0_1.csv",
            "report": "benchmark_v0_1_report.md",
            "readme": "README.md",
        },
    }
    (OUTDIR / "benchmark_manifest_v0_1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_readme(OUTDIR / "README.md", region_rows, candidate_rows)
    write_report(OUTDIR / "benchmark_v0_1_report.md", region_rows, candidate_rows)
    print(f"Wrote benchmark v0.1 to {OUTDIR}")
    print(f"Primary regions: {len(region_rows)}")
    print(f"External candidates: {len(candidate_rows)}")


if __name__ == "__main__":
    main()
