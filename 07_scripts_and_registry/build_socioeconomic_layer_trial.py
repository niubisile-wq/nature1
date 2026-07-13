from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
PLAN_DIR = ROOT / "08_nature_experiment_plan"
OUTDIR = ROOT / "03_exposure_closure" / "socioeconomic_layer_trial_v1"


REGION_MAP = {
    "Po": {"preferred_source": "GVI", "secondary_source": "SHDI", "country_or_area": "Italy", "trial_mode": "region_level_context"},
    "Chao Phraya": {"preferred_source": "GVI", "secondary_source": "SHDI", "country_or_area": "Thailand", "trial_mode": "region_level_context"},
    "Brantas": {"preferred_source": "GVI", "secondary_source": "SHDI", "country_or_area": "Indonesia", "trial_mode": "region_level_context"},
    "Indus": {"preferred_source": "GVI", "secondary_source": "SHDI", "country_or_area": "Pakistan_or_India_basin_context", "trial_mode": "multi_country_context"},
    "Rhone": {"preferred_source": "GVI", "secondary_source": "SHDI", "country_or_area": "France", "trial_mode": "region_level_context"},
    "Rhine": {"preferred_source": "GVI", "secondary_source": "SHDI", "country_or_area": "Multi_country_basin_context", "trial_mode": "multi_country_context"},
}


COUNTRY_ISO_MAP = {
    "Italy": "ITA",
    "Thailand": "THA",
    "Indonesia": "IDN",
    "France": "FRA",
    "Pakistan_or_India_basin_context": "IND",
    "Multi_country_basin_context": None,
}


def normalize_region(label: str) -> str:
    return label.replace("_", " ").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_region_evidence() -> pd.DataFrame:
    return pd.read_csv(PLAN_DIR / "decision_facing_exposure_matrix_v1.csv")


def fetch_public_table_series(base_url: str, iso: str) -> dict[str, Any]:
    """Fetch the national row from a public Global Data Lab table page."""
    url = f"{base_url}{iso}/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    row = re.search(
        r'<tr>\s*<td class="region"><span title="([^"]+)">([^<]+)</span>(.*?)</tr>',
        html,
        flags=re.S,
    )
    if not row:
        raise RuntimeError(f"Could not find SHDI national row for {iso}")

    values = re.findall(r'<td class="proper">([^<]+)</td>', row.group(3))
    if not values:
        raise RuntimeError(f"Could not parse SHDI values for {iso}")

    years = list(range(1990, 1990 + len(values)))
    return {
        "iso": iso,
        "label": row.group(2).strip(),
        "title": row.group(1).strip(),
        "source_url": url,
        "years": years,
        "values": values,
        "latest_year": years[-1],
        "latest_value": values[-1],
    }


def parse_public_table_rows(base_url: str, iso: str) -> list[dict[str, Any]]:
    """Return all country/subnational rows from a public Global Data Lab table page."""
    url = f"{base_url}{iso}/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    rows: list[dict[str, Any]] = []
    for match in re.finditer(
        r'<tr>\s*<td class="region"><span title="([^"]+)">([^<]+)</span>(.*?)</tr>',
        html,
        flags=re.S,
    ):
        title, label, body = match.groups()
        values = re.findall(r'<td class="proper">([^<]+)</td>', body)
        if not values:
            continue
        years = list(range(1990, 1990 + len(values)))
        rows.append(
            {
                "title": title.strip(),
                "label": label.strip(),
                "source_url": url,
                "years": years,
                "values": values,
                "latest_year": years[-1],
                "latest_value": values[-1],
            }
        )
    return rows


def fetch_gvi_country_series(iso: str) -> dict[str, Any]:
    return fetch_public_table_series("https://globaldatalab.org/gvi/table/gvi/", iso)


def fetch_shdi_country_series(iso: str) -> dict[str, Any]:
    return fetch_public_table_series("https://globaldatalab.org/shdi/table/shdi/", iso)


def build_access_rows() -> list[dict[str, Any]]:
    rows = []
    for region, meta in REGION_MAP.items():
        iso = COUNTRY_ISO_MAP.get(meta["country_or_area"])
        rows.append(
            {
                "region": region,
                "preferred_source": meta["preferred_source"],
                "secondary_source": meta["secondary_source"],
                "country_or_area": meta["country_or_area"],
                "trial_mode": meta["trial_mode"],
                "country_iso": iso or "",
                "access_status": "ready_for_gvi_trial" if meta["preferred_source"] == "GVI" else "access_gated",
                "notes": (
                    "GVI is a public vulnerability index and is the preferred socioeconomic context layer for the current trial."
                    if meta["preferred_source"] == "GVI"
                    else "Raster upgrade path remains reserved for GRDI."
                ),
            }
        )
    return rows


def build_country_context_rows(access_rows: list[dict[str, Any]], source: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in access_rows:
        iso = row.get("country_iso") or COUNTRY_ISO_MAP.get(row["country_or_area"])
        if not iso:
            rows.append(
                {
                    "region": row["region"],
                    "country_or_area": row["country_or_area"],
                    "country_iso": "",
                    "series_label": "",
                    "latest_year": "",
                    "latest_value": "",
                    "status": "multi_country_context_unresolved",
                    "source_url": "",
                    "notes": "No single-country context mapping was frozen for this multi-country basin context.",
                }
            )
            continue

        series = fetch_gvi_country_series(iso) if source == "GVI" else fetch_shdi_country_series(iso)
        rows.append(
            {
                "region": row["region"],
                "country_or_area": row["country_or_area"],
                "country_iso": iso,
                "series_label": series["label"],
                "latest_year": series["latest_year"],
                "latest_value": series["latest_value"],
                "status": "retrieved_from_public_table",
                "source_url": series["source_url"],
                "notes": f"National {source} row fetched from the public Global Data Lab table page ({series['title']}).",
            }
        )
    return rows


def build_spread_rows(access_rows: list[dict[str, Any]], source: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in access_rows:
        iso = row.get("country_iso") or COUNTRY_ISO_MAP.get(row["country_or_area"])
        if not iso:
            rows.append(
                {
                    "region": row["region"],
                    "country_or_area": row["country_or_area"],
                    "country_iso": "",
                    "source": source,
                    "year": "",
                    "national_value": "",
                    "subnational_count": "",
                    "subnational_min": "",
                    "subnational_median": "",
                    "subnational_max": "",
                    "spread_note": "multi_country_context_unresolved",
                }
            )
            continue

        base_url = "https://globaldatalab.org/gvi/table/gvi/" if source == "GVI" else "https://globaldatalab.org/shdi/table/shdi/"
        all_rows = parse_public_table_rows(base_url, iso)
        if not all_rows:
            continue
        national = all_rows[0]
        subnational = all_rows[1:]
        sub_latest = [float(r["latest_value"]) for r in subnational if r["latest_value"] not in ("", None)]
        if sub_latest:
            subnational_min = min(sub_latest)
            subnational_max = max(sub_latest)
            subnational_median = float(pd.Series(sub_latest).median())
        else:
            subnational_min = subnational_max = subnational_median = float(national["latest_value"])
        rows.append(
            {
                "region": row["region"],
                "country_or_area": row["country_or_area"],
                "country_iso": iso,
                "source": source,
                "year": national["latest_year"],
                "national_value": national["latest_value"],
                "subnational_count": len(subnational),
                "subnational_min": f"{subnational_min:.1f}",
                "subnational_median": f"{subnational_median:.1f}",
                "subnational_max": f"{subnational_max:.1f}",
                "spread_note": "retrieved_from_public_table",
            }
        )
    return rows


def build_report(
    region_df: pd.DataFrame,
    access_rows: list[dict[str, Any]],
    country_rows: list[dict[str, Any]] | None = None,
    gvi_spread_rows: list[dict[str, Any]] | None = None,
    shdi_spread_rows: list[dict[str, Any]] | None = None,
) -> list[str]:
    access_map = {normalize_region(row["region"]): row for row in access_rows}
    lines = [
        "# Socioeconomic Layer Trial Report v1",
        "",
        "This report is a frozen scaffold for the socioeconomic trial. It records which regions can be matched immediately to GVI / SHDI-style contextual data and which regions remain access-gated for GRDI raster upgrades.",
        "",
        "## Region Access Matrix",
        "",
        "| region | preferred source | secondary source | country / area | trial mode | country ISO | access status | notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for raw_region in region_df["region"].tolist():
        region = normalize_region(raw_region)
        row = access_map.get(region)
        if row is None:
            row = {
                "preferred_source": "GVI",
                "secondary_source": "SHDI",
                "country_or_area": "unknown",
                "trial_mode": "region_level_context",
                "country_iso": "",
                "access_status": "needs_manual_mapping",
                "notes": "Region name did not match the frozen socioeconomic access matrix.",
            }
        lines.append(
            f"| {raw_region} | {row['preferred_source']} | {row['secondary_source']} | {row['country_or_area']} | {row['trial_mode']} | {row['country_iso']} | {row['access_status']} | {row['notes']} |"
        )

    lines.extend(
        [
            "",
            "## GVI Country Context Layer",
            "",
            "This layer is built from public Global Data Lab GVI table pages. It is intentionally country-level context rather than pixel-level truth, because the current trial is a conservative fallback.",
            "",
            "| region | country / area | country ISO | GVI label | latest year | latest GVI | status | notes |",
            "|---|---|---|---|---:|---:|---|---|",
        ]
    )
    if country_rows:
        for row in country_rows:
            lines.append(
                f"| {row['region']} | {row['country_or_area']} | {row['country_iso']} | {row['series_label']} | {row['latest_year']} | {row['latest_value']} | {row['status']} | {row['notes']} |"
            )
    else:
        lines.append("| _not computed_ | _not computed_ | _ | _ | _ | _ | scaffold_only | No GVI web fetch was requested. |")

    lines.extend(
        [
            "",
            "## GVI Subnational Spread Summary",
            "",
            "This summary shows the within-country spread of the public GVI table pages. It is useful because it makes the vulnerability gradient visible rather than collapsing the layer to a single number.",
            "",
            "| region | country / area | country ISO | year | national GVI | subnational count | subnational min | subnational median | subnational max | note |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    if gvi_spread_rows:
        for row in gvi_spread_rows:
            lines.append(
                f"| {row['region']} | {row['country_or_area']} | {row['country_iso']} | {row['year']} | {row['national_value']} | {row['subnational_count']} | {row['subnational_min']} | {row['subnational_median']} | {row['subnational_max']} | {row['spread_note']} |"
            )
    else:
        lines.append("| _not computed_ | _not computed_ | _ | _ | _ | _ | _ | _ | _ | No GVI spread summary was requested. |")

    lines.extend(
        [
            "",
            "## SHDI Backup Layer",
            "",
            "The SHDI fallback remains available as a country-context backup for the single-country cases and may be used if the GVI route ever proves unsuitable.",
            "",
            "| region | country / area | country ISO | SHDI label | latest year | latest SHDI | status | notes |",
            "|---|---|---|---|---:|---:|---|---|",
        ]
    )
    if country_rows:
        for row in build_country_context_rows(access_rows, "SHDI"):
            lines.append(
                f"| {row['region']} | {row['country_or_area']} | {row['country_iso']} | {row['series_label']} | {row['latest_year']} | {row['latest_value']} | {row['status']} | {row['notes']} |"
            )
    else:
        lines.append("| _not computed_ | _not computed_ | _ | _ | _ | _ | scaffold_only | No SHDI web fetch was requested. |")

    lines.extend(
        [
            "",
            "## SHDI Subnational Spread Summary",
            "",
            "This summary shows the within-country spread of the public SHDI table pages. It is kept as a backup comparator against the GVI layer.",
            "",
            "| region | country / area | country ISO | year | national SHDI | subnational count | subnational min | subnational median | subnational max | note |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    if shdi_spread_rows:
        for row in shdi_spread_rows:
            lines.append(
                f"| {row['region']} | {row['country_or_area']} | {row['country_iso']} | {row['year']} | {row['national_value']} | {row['subnational_count']} | {row['subnational_min']} | {row['subnational_median']} | {row['subnational_max']} | {row['spread_note']} |"
            )
    else:
        lines.append("| _not computed_ | _not computed_ | _ | _ | _ | _ | _ | _ | _ | No SHDI spread summary was requested. |")

    lines.extend(
        [
            "",
            "## Trial Logic",
            "",
            "1. GVI is the first executable socioeconomic vulnerability layer because it is public and more directly aligned with the climate-vulnerability question.",
            "2. SHDI remains the secondary fallback because it is a public contextual layer but is less directly vulnerability-specific than GVI.",
            "3. GRDI remains the preferred raster upgrade, but it is access-gated and should be attempted only after the contextual route is frozen.",
            "4. Nightlights remains a last-resort proxy only.",
            "",
            "## Current Status",
            "",
            "- GVI country-level vulnerability values are now computed directly from public Global Data Lab table pages for the single-country regions.",
            "- GVI subnational spreads are now computed from the same public table pages, so the vulnerability layer has visible internal gradients instead of a single collapsed number.",
            "- SHDI country-level context values are also computed as a backup from the same source family, and SHDI subnational spreads are available for comparison.",
            "- Multi-country basin contexts remain unresolved until a basin aggregation policy is frozen.",
            "- The access matrix and region mapping are explicit, so a raster upgrade or finer-grained SHDI/GVI ingestion can be added without redesigning the workflow.",
        ]
    )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a socioeconomic layer trial scaffold.")
    parser.add_argument("--shdi", type=Path, default=None, help="Path to a downloaded SHDI CSV")
    parser.add_argument("--grdi", type=Path, default=None, help="Path to a downloaded GRDI raster or extracted table")
    parser.add_argument("--gvi-web", action="store_true", help="Fetch GVI country context directly from public table pages")
    parser.add_argument("--shdi-web", action="store_true", help="Fetch SHDI country context directly from public table pages")
    parser.add_argument("--outdir", type=Path, default=OUTDIR, help="Output directory")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    region_df = load_region_evidence()
    access_rows = build_access_rows()
    write_csv(
        args.outdir / "socioeconomic_layer_access_matrix.csv",
        access_rows,
        ["region", "preferred_source", "secondary_source", "country_or_area", "trial_mode", "country_iso", "access_status", "notes"],
    )
    write_csv(
        args.outdir / "socioeconomic_layer_region_map.csv",
        access_rows,
        ["region", "preferred_source", "secondary_source", "country_or_area", "trial_mode", "country_iso", "access_status", "notes"],
    )

    country_rows: list[dict[str, Any]] = []
    gvi_spread_rows: list[dict[str, Any]] = []
    shdi_spread_rows: list[dict[str, Any]] = []
    if args.gvi_web:
        country_rows = build_country_context_rows(access_rows, "GVI")
        gvi_spread_rows = build_spread_rows(access_rows, "GVI")
        write_csv(
            args.outdir / "socioeconomic_layer_gvi_country_context.csv",
            country_rows,
            ["region", "country_or_area", "country_iso", "series_label", "latest_year", "latest_value", "status", "source_url", "notes"],
        )
        write_csv(
            args.outdir / "socioeconomic_layer_gvi_subnational_spread.csv",
            gvi_spread_rows,
            ["region", "country_or_area", "country_iso", "source", "year", "national_value", "subnational_count", "subnational_min", "subnational_median", "subnational_max", "spread_note"],
        )
    if args.shdi_web:
        shdi_rows = build_country_context_rows(access_rows, "SHDI")
        shdi_spread_rows = build_spread_rows(access_rows, "SHDI")
        write_csv(
            args.outdir / "socioeconomic_layer_shdi_country_context.csv",
            shdi_rows,
            ["region", "country_or_area", "country_iso", "series_label", "latest_year", "latest_value", "status", "source_url", "notes"],
        )
        write_csv(
            args.outdir / "socioeconomic_layer_shdi_subnational_spread.csv",
            shdi_spread_rows,
            ["region", "country_or_area", "country_iso", "source", "year", "national_value", "subnational_count", "subnational_min", "subnational_median", "subnational_max", "spread_note"],
        )
        if not country_rows:
            country_rows = shdi_rows

    report = build_report(
        region_df,
        access_rows,
        country_rows if (args.gvi_web or args.shdi_web) else None,
        gvi_spread_rows if args.gvi_web else None,
        shdi_spread_rows if args.shdi_web else None,
    )
    (args.outdir / "socioeconomic_layer_trial_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    meta = {
        "has_shdi_input": args.shdi is not None and args.shdi.exists(),
        "has_grdi_input": args.grdi is not None and args.grdi.exists(),
        "has_gvi_web": bool(args.gvi_web),
        "has_shdi_web": bool(args.shdi_web),
        "country_context_rows": len(country_rows),
        "gvi_spread_rows": len(gvi_spread_rows),
        "shdi_spread_rows": len(shdi_spread_rows),
        "status": "gvi_country_context_retrieved" if args.gvi_web and country_rows else ("shdi_country_context_retrieved" if args.shdi_web and country_rows else ("scaffold_only" if not (args.shdi and args.shdi.exists()) and not (args.grdi and args.grdi.exists()) else "ready_to_compute")),
    }
    (args.outdir / "socioeconomic_layer_trial_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
