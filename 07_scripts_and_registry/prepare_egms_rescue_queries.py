from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from typing import Any

import requests


API_ENDPOINT = "https://egms.land.copernicus.eu/insar-api/archive"


AOIS: list[dict[str, Any]] = [
    {
        "aoi_id": "po_venice_broad",
        "name": "Po Basin and Venice",
        "bbox": [10.0, 44.0, 13.0, 46.0],
        "priority": "A",
        "role": "EGMS benchmark for Po/Venice LiCSAR observability bias",
        "reason": "European high-quality benchmark overlapping the Po delta and Venice subsidence literature.",
    },
    {
        "aoi_id": "po_delta_core",
        "name": "Po delta core",
        "bbox": [11.7, 44.35, 12.9, 45.55],
        "priority": "A",
        "role": "Core positive-control delta benchmark",
        "reason": "Small AOI around the current Po-delta VLM/LiCSAR prototype for fast EGMS closure.",
    },
    {
        "aoi_id": "netherlands_lowlands",
        "name": "Netherlands lowlands",
        "bbox": [3.2, 50.7, 7.2, 53.8],
        "priority": "A",
        "role": "Independent EGMS lowland benchmark",
        "reason": "Dense European product coverage; separates open-observability bias from purely groundwater framing.",
    },
    {
        "aoi_id": "rhine_core",
        "name": "Rhine-Meuse delta core",
        "bbox": [3.2, 51.0, 5.2, 52.35],
        "priority": "B",
        "role": "Specificity control",
        "reason": "Current WorldCover-adjusted model weakens Rhine; EGMS can test whether this is product/land-cover confounding.",
    },
    {
        "aoi_id": "rhone_delta_core",
        "name": "Rhone delta / Camargue core",
        "bbox": [4.0, 43.2, 5.15, 44.05],
        "priority": "A",
        "role": "Land-cover mediated delta benchmark",
        "reason": "Strong signal survives WorldCover controls; EGMS tests whether it is a real public-product observability gap.",
    },
    {
        "aoi_id": "cyprus_sourcecoop_smoke",
        "name": "Cyprus Source Cooperative smoke test",
        "bbox": [32.0, 34.4, 34.8, 35.8],
        "priority": "C",
        "role": "Cloud-native EGMS format smoke test",
        "reason": "Matches the public Source Cooperative sample region; useful for parser development, not a Nature benchmark.",
    },
]


QUERY_SPECS: list[dict[str, Any]] = [
    {
        "query_kind": "l3_ortho_up",
        "levels": ["L3"],
        "releases": ["2019-2023"],
        "productType": "ORTHO-UP",
        "purpose": "Primary vertical-motion benchmark for exposure and observability closure.",
    },
    {
        "query_kind": "l3_ortho_east",
        "levels": ["L3"],
        "releases": ["2019-2023"],
        "productType": "ORTHO-EAST",
        "purpose": "Optional horizontal component sanity check for coastal/delta deformation interpretation.",
    },
    {
        "query_kind": "l2b_calibrated",
        "levels": ["L2B"],
        "releases": ["2019-2023"],
        "purpose": "Optional calibrated-track product for product-bias transfer-function tests.",
    },
]


def ensure_bbox_size(aoi: dict[str, Any]) -> None:
    min_lon, min_lat, max_lon, max_lat = aoi["bbox"]
    lon_width = max_lon - min_lon
    lat_width = max_lat - min_lat
    if lon_width <= 0 or lat_width <= 0:
        raise ValueError(f"{aoi['aoi_id']} has an invalid bbox: {aoi['bbox']}")
    if lon_width > 5 or lat_width > 5:
        raise ValueError(
            f"{aoi['aoi_id']} bbox exceeds the EGMS API 5-degree limit: "
            f"{lon_width:.2f} x {lat_width:.2f}"
        )


def bbox_payload(bbox: list[float]) -> list[list[float]]:
    min_lon, min_lat, max_lon, max_lat = bbox
    return [[min_lon, min_lat], [max_lon, max_lat]]


def build_payloads() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for aoi in AOIS:
        ensure_bbox_size(aoi)
        for spec in QUERY_SPECS:
            payload = {
                "id": None,
                "bbox": bbox_payload(aoi["bbox"]),
                "levels": spec["levels"],
                "releases": spec["releases"],
            }
            if "productType" in spec:
                payload["productType"] = spec["productType"]
            rows.append(
                {
                    "aoi_id": aoi["aoi_id"],
                    "aoi_name": aoi["name"],
                    "priority": aoi["priority"],
                    "role": aoi["role"],
                    "reason": aoi["reason"],
                    "query_kind": spec["query_kind"],
                    "purpose": spec["purpose"],
                    "payload": payload,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def get_access_token(token_jwt: Path) -> str:
    try:
        import jwt  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install PyJWT before using --token-jwt: py -m pip install pyjwt") from exc
    service_key = json.loads(token_jwt.read_text(encoding="utf-8"))
    private_key = service_key["private_key"].encode("utf-8")
    now = int(time.time())
    claim_set = {
        "iss": service_key["client_id"],
        "sub": service_key["user_id"],
        "aud": service_key["token_uri"],
        "iat": now,
        "exp": now + 60 * 60,
    }
    grant = jwt.encode(claim_set, private_key, algorithm="RS256")
    response = requests.post(
        service_key["token_uri"],
        headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": grant},
        timeout=60,
    )
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        raise RuntimeError(f"No access_token returned from token endpoint: {response.text[:500]}")
    return str(token)


def query_egms(rows: list[dict[str, Any]], access_token: str, timeout: int) -> list[dict[str, Any]]:
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    results: list[dict[str, Any]] = []
    for row in rows:
        payload = row["payload"]
        try:
            response = requests.post(f"{API_ENDPOINT}/search", headers=headers, json=payload, timeout=timeout)
            content_type = response.headers.get("content-type", "")
            result: Any
            if "json" in content_type:
                result = response.json()
            else:
                result = {"raw_text": response.text[:1000]}
            hits = result.get("hits", []) if isinstance(result, dict) else []
            query_id = result.get("id", "") if isinstance(result, dict) else ""
            results.append(
                {
                    **{k: v for k, v in row.items() if k != "payload"},
                    "status_code": response.status_code,
                    "ok": response.ok,
                    "query_id": query_id,
                    "hit_count": len(hits),
                    "result": result,
                }
            )
        except Exception as exc:
            results.append(
                {
                    **{k: v for k, v in row.items() if k != "payload"},
                    "status_code": "",
                    "ok": False,
                    "query_id": "",
                    "hit_count": "",
                    "result": {"error": f"{type(exc).__name__}: {exc}"},
                }
            )
    return results


def flatten_hits(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hits_rows: list[dict[str, Any]] = []
    for result in results:
        raw = result.get("result", {})
        if not isinstance(raw, dict):
            continue
        hits = raw.get("hits", [])
        if not isinstance(hits, list):
            continue
        for hit in hits:
            if not isinstance(hit, dict):
                continue
            filename = hit.get("filename", "")
            query_id = result.get("query_id", "")
            download_url = f"{API_ENDPOINT}/download/{filename}?id={query_id}" if filename and query_id else ""
            hits_rows.append(
                {
                    "aoi_id": result.get("aoi_id", ""),
                    "aoi_name": result.get("aoi_name", ""),
                    "query_kind": result.get("query_kind", ""),
                    "filename": filename,
                    "filesize": hit.get("filesize", ""),
                    "productLevel": hit.get("productLevel", ""),
                    "productType": hit.get("productType", ""),
                    "release": hit.get("release", ""),
                    "version": hit.get("version", ""),
                    "tileId": hit.get("tileId", ""),
                    "direction": hit.get("direction", ""),
                    "relativeOrbit": hit.get("relativeOrbit", ""),
                    "burstCycle": hit.get("burstCycle", ""),
                    "swath": hit.get("swath", ""),
                    "download_url": download_url,
                }
            )
    return hits_rows


def write_report(path: Path, rows: list[dict[str, Any]], queried: bool, results: list[dict[str, Any]] | None) -> None:
    lines = [
        "# EGMS rescue query pack",
        "",
        "This pack turns the Nature rescue route into reproducible EGMS API queries.",
        "The default run is credential-free and only writes query payloads; pass an access token to execute searches.",
        "",
        "## Decision use",
        "",
        "- Primary goal: close the independent benchmark gap for the open-InSAR observability-bias claim.",
        "- Fastest Nature rescue: EGMS L3 ORTHO-UP over Po/Venice, Netherlands lowlands, Rhone, and Rhine controls.",
        "- Parser-only smoke test: Cyprus, because a Source Cooperative EGMS sample exists there.",
        "",
        "## AOIs",
        "",
        "| AOI | Priority | Role | BBox |",
        "|---|---:|---|---|",
    ]
    for aoi in AOIS:
        lines.append(
            f"| {aoi['aoi_id']} | {aoi['priority']} | {aoi['role']} | "
            f"{', '.join(str(x) for x in aoi['bbox'])} |"
        )
    lines.extend(
        [
            "",
            "## Query kinds",
            "",
            "| Query kind | Levels | Product type | Purpose |",
            "|---|---|---|---|",
        ]
    )
    for spec in QUERY_SPECS:
        lines.append(
            f"| {spec['query_kind']} | {','.join(spec['levels'])} | "
            f"{spec.get('productType', '')} | {spec['purpose']} |"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `egms_rescue_aoi_registry.csv`: AOI table.",
            "- `egms_query_payloads.json`: machine-readable payloads.",
            "- `egms_query_payloads.csv`: compact payload table.",
        ]
    )
    if queried:
        total_hits = sum(int(r.get("hit_count") or 0) for r in results or [])
        lines.extend(
            [
                "- `egms_search_results.json`: full API responses.",
                "- `egms_hits.csv`: flattened product/download manifest.",
                "",
                "## API search summary",
                "",
                f"- Queries executed: `{len(results or [])}`",
                f"- Total hits: `{total_hits}`",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Next command with credentials",
                "",
                "```powershell",
                "py prepare_egms_rescue_queries.py --token-jwt C:\\path\\to\\token.jwt",
                "```",
                "",
                "Or, if a short-lived bearer token is already available:",
                "",
                "```powershell",
                "py prepare_egms_rescue_queries.py --access-token $env:EGMS_ACCESS_TOKEN",
                "```",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or execute EGMS API queries for the Nature rescue benchmark.")
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path(r"C:\Users\刘子轩\radar_outputs\egms_api_rescue_queries"),
        help="Output directory.",
    )
    parser.add_argument("--access-token", default="", help="Short-lived EGMS/CLMS bearer access token.")
    parser.add_argument("--token-jwt", type=Path, help="CLMS service-key JSON file, usually named token.jwt.")
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    rows = build_payloads()

    aoi_rows = [
        {
            "aoi_id": aoi["aoi_id"],
            "name": aoi["name"],
            "bbox_wgs84": ",".join(str(x) for x in aoi["bbox"]),
            "priority": aoi["priority"],
            "role": aoi["role"],
            "reason": aoi["reason"],
        }
        for aoi in AOIS
    ]
    write_csv(
        args.outdir / "egms_rescue_aoi_registry.csv",
        aoi_rows,
        ["aoi_id", "name", "bbox_wgs84", "priority", "role", "reason"],
    )

    (args.outdir / "egms_query_payloads.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_csv(
        args.outdir / "egms_query_payloads.csv",
        [
            {
                **{k: v for k, v in row.items() if k != "payload"},
                "payload_json": json.dumps(row["payload"], ensure_ascii=False, separators=(",", ":")),
            }
            for row in rows
        ],
        ["aoi_id", "aoi_name", "priority", "role", "reason", "query_kind", "purpose", "payload_json"],
    )

    access_token = args.access_token
    if args.token_jwt:
        access_token = get_access_token(args.token_jwt)

    results: list[dict[str, Any]] | None = None
    if access_token:
        results = query_egms(rows, access_token, args.timeout)
        (args.outdir / "egms_search_results.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        hits_rows = flatten_hits(results)
        write_csv(
            args.outdir / "egms_hits.csv",
            hits_rows,
            [
                "aoi_id",
                "aoi_name",
                "query_kind",
                "filename",
                "filesize",
                "productLevel",
                "productType",
                "release",
                "version",
                "tileId",
                "direction",
                "relativeOrbit",
                "burstCycle",
                "swath",
                "download_url",
            ],
        )

    write_report(args.outdir / "egms_api_rescue_plan.md", rows, bool(access_token), results)
    print(f"Wrote EGMS rescue query pack to {args.outdir}")
    print(f"Queries prepared: {len(rows)}")
    if results is not None:
        print(f"Queries executed: {len(results)}")
        print(f"Total hits: {sum(int(r.get('hit_count') or 0) for r in results)}")


if __name__ == "__main__":
    main()
