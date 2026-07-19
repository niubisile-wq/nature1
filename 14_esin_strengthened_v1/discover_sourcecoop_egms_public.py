from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode

import requests


BASE_URL = "https://data.source.coop/youssef-harby/egms-copernicus/"
PREFIX = "L2a/parquet/"
NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}


def list_keys(prefix: str = PREFIX, max_keys: int = 1000) -> list[str]:
    keys: list[str] = []
    token: str | None = None
    while True:
        params = {"list-type": "2", "prefix": prefix, "max-keys": str(max_keys)}
        if token:
            params["continuation-token"] = token
        response = requests.get(BASE_URL + "?" + urlencode(params), timeout=60)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        keys.extend(
            key.text or ""
            for key in root.findall("s3:Contents/s3:Key", NS)
            if key.text
        )
        truncated = root.findtext("s3:IsTruncated", namespaces=NS)
        token = root.findtext("s3:NextContinuationToken", namespaces=NS)
        if truncated != "true" or not token:
            break
    return keys


def country_from_key(key: str) -> str:
    parts = key.split("/")
    if len(parts) >= 4 and len(parts[3]) == 2:
        return parts[3]
    return "ROOT_OR_AGGREGATE"


def main() -> None:
    outdir = Path("sourcecoop_public_discovery_20260719")
    outdir.mkdir(parents=True, exist_ok=True)
    keys = list_keys()
    rows = [
        {
            "key": key,
            "country_or_group": country_from_key(key),
            "url": f"https://data.source.coop/youssef-harby/{key}",
        }
        for key in keys
    ]
    with (outdir / "sourcecoop_egms_l2a_public_keys.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["country_or_group", "key", "url"])
        writer.writeheader()
        writer.writerows(rows)

    countries = sorted({row["country_or_group"] for row in rows})
    report = [
        "# Source Cooperative EGMS public discovery",
        "",
        f"- Base URL: `{BASE_URL}`",
        f"- Listed prefix: `{PREFIX}`",
        f"- Object count: `{len(rows)}`",
        f"- Country/group directories found: `{', '.join(countries)}`",
        "",
        "## Interpretation",
        "",
        "The public Source Cooperative mirror is useful for reproducing the Cyprus EGMS boundary-control run, "
        "but this discovery pass did not find Italy or France EGMS parquet products under the public L2a parquet prefix. "
        "Therefore Po delta, Po-Venice and Rhone/Camargue still require CLMS/EGMS authenticated download or a manually supplied EGMS product file.",
        "",
        "## Source notes",
        "",
        "- Source Cooperative product page states that the repository contains Copernicus EGMS data converted from zipped CSV files into cloud-native geospatial formats.",
        "- Copernicus/EEA metadata states that EGMS Ortho Vertical 2019-2023 is a vector product distributed in CSV format and that download requires authentication.",
    ]
    (outdir / "sourcecoop_egms_public_discovery_20260719.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
