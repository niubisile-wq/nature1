from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests


ROOT = Path(__file__).resolve().parent
DEFAULT_PAYLOADS = ROOT / "egms_query_payloads.json"
DEFAULT_DOWNLOAD_DIR = ROOT / "egms_priority_downloads_v1"
DEFAULT_OUTDIR = ROOT / "egms_priority_benchmark_closure_v1"
DEFAULT_CLMS_BASE_URL = "https://land.copernicus.eu/"
DEFAULT_EGMS_API_ENDPOINT = "https://egms.land.copernicus.eu/insar-api/archive"
JWT_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)


def require_pyjwt() -> Any:
    try:
        import jwt  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "PyJWT is required for service-key authentication. Install with: py -3 -m pip install pyjwt"
        ) from exc
    return jwt


def access_token_from_service_key(service_key_path: Path) -> str:
    jwt = require_pyjwt()
    service_key = load_json(service_key_path)
    token_uri = service_key.get("token_uri") or urljoin(DEFAULT_CLMS_BASE_URL, "@@oauth2-token")
    private_key = service_key["private_key"].encode("utf-8")
    now = int(time.time())
    claim_set = {
        "iss": service_key["client_id"],
        "sub": service_key["user_id"],
        "aud": token_uri,
        "iat": now,
        "exp": now + 3600,
    }
    assertion = jwt.encode(claim_set, private_key, algorithm="RS256")
    response = requests.post(
        token_uri,
        headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": JWT_GRANT_TYPE, "assertion": assertion},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"No access_token in CLMS token response. Keys: {sorted(data.keys())}")
    return token


def resolve_access_token(args: argparse.Namespace) -> str:
    if args.access_token:
        return args.access_token
    env_access = os.environ.get("EGMS_ACCESS_TOKEN") or os.environ.get("CLMS_ACCESS_TOKEN")
    if env_access:
        return env_access
    service_key_value = args.service_key_json or os.environ.get("EGMS_SERVICE_KEY_JSON") or os.environ.get("CLMS_SERVICE_KEY_JSON")
    if service_key_value:
        return access_token_from_service_key(Path(service_key_value))
    token_jwt = args.token_jwt or os.environ.get("EGMS_TOKEN_JWT") or os.environ.get("CLMS_TOKEN_JWT")
    if token_jwt:
        return access_token_from_service_key(Path(token_jwt))
    local_token = ROOT / "token.jwt"
    if local_token.exists():
        return access_token_from_service_key(local_token)
    raise SystemExit(
        "No EGMS/CLMS credential found. Provide one of: --access-token, --service-key-json, --token-jwt, "
        "$env:EGMS_ACCESS_TOKEN, $env:EGMS_SERVICE_KEY_JSON, $env:EGMS_TOKEN_JWT, or local token.jwt."
    )


def auth_headers(token: str) -> dict[str, str]:
    return {"Accept": "application/json", "Authorization": f"Bearer {token}"}


def search_payload(api_endpoint: str, token: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{api_endpoint.rstrip('/')}/search"
    response = requests.post(url, headers={**auth_headers(token), "Content-Type": "application/json"}, json=payload, timeout=120)
    response.raise_for_status()
    return {"request_payload": payload, "search_endpoint": url, "response": response.json()}


def extract_urls(obj: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = str(key).lower()
            if isinstance(value, str) and value.startswith("http") and any(x in key_lower for x in ["download", "href", "url"]):
                urls.append(value)
            else:
                urls.extend(extract_urls(value))
    elif isinstance(obj, list):
        for item in obj:
            urls.extend(extract_urls(item))
    return list(dict.fromkeys(urls))


def download_url(url: str, token: str, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    filename = url.split("?")[0].rstrip("/").split("/")[-1] or "egms_download.bin"
    target = outdir / filename
    with requests.get(url, headers=auth_headers(token), stream=True, timeout=120) as response:
        response.raise_for_status()
        with target.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)
    return target


def egms_download_links(api_endpoint: str, search_response: dict[str, Any]) -> list[str]:
    response = search_response.get("response", {})
    query_id = response.get("id")
    hits = response.get("hits", [])
    if not query_id or not isinstance(hits, list):
        return []
    links = []
    for hit in hits:
        filename = hit.get("filename") if isinstance(hit, dict) else None
        if filename:
            links.append(f"{api_endpoint.rstrip('/')}/download/{filename}?id={query_id}")
    return links


def run_closure(input_path: Path, outdir: Path, aoi_id: str, product_label: str, dry_run: bool) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "build_egms_benchmark_closure_v1.py"),
        "--input",
        str(input_path),
        "--outdir",
        str(outdir / aoi_id),
        "--aoi-id",
        aoi_id,
        "--product-label",
        product_label,
    ]
    if dry_run:
        print("DRY-RUN closure command:", " ".join(cmd))
        return
    subprocess.run(cmd, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search/download A-priority EGMS products through CLMS credentials and run the local EGMS/GHSL closure."
    )
    parser.add_argument("--payloads", type=Path, default=DEFAULT_PAYLOADS)
    parser.add_argument("--api-endpoint", default=DEFAULT_EGMS_API_ENDPOINT)
    parser.add_argument("--token-jwt", type=Path)
    parser.add_argument("--service-key-json", type=Path)
    parser.add_argument("--access-token")
    parser.add_argument("--download-dir", type=Path, default=DEFAULT_DOWNLOAD_DIR)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--aoi-id", default="po_delta_core")
    parser.add_argument("--query-kind", default="l3_ortho_up")
    parser.add_argument("--max-downloads", type=int, default=1)
    parser.add_argument("--local-egms-file", type=Path, help="Skip search/download and run closure on an already downloaded EGMS csv/parquet file.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    if args.local_egms_file:
        run_closure(args.local_egms_file, args.outdir, args.aoi_id, "EGMS_LOCAL_PRODUCT", args.dry_run)
        return

    token = resolve_access_token(args)
    payload_rows = load_json(args.payloads)
    selected = [
        row
        for row in payload_rows
        if row.get("aoi_id") == args.aoi_id and row.get("query_kind") == args.query_kind
    ]
    if not selected:
        raise SystemExit(f"No payload found for aoi_id={args.aoi_id!r}, query_kind={args.query_kind!r}")

    search_records: list[dict[str, Any]] = []
    downloaded: list[str] = []
    for row in selected:
        record = search_payload(args.api_endpoint, token, row["payload"])
        record["aoi_id"] = row["aoi_id"]
        record["query_kind"] = row["query_kind"]
        search_records.append(record)
        urls = egms_download_links(args.api_endpoint, record) or extract_urls(record["response"])
        for url in urls[: args.max_downloads]:
            path = download_url(url, token, args.download_dir / row["aoi_id"] / row["query_kind"])
            downloaded.append(str(path))
            if path.suffix.lower() in {".csv", ".parquet", ".pq"} or "".join(path.suffixes[-2:]).lower() == ".csv.gz":
                run_closure(path, args.outdir, row["aoi_id"], f"EGMS_{row['query_kind']}", args.dry_run)

    write_json(args.outdir / "egms_clms_priority_search_response_v1.json", search_records)
    write_json(
        args.outdir / "egms_clms_priority_download_manifest_v1.json",
        {
            "aoi_id": args.aoi_id,
            "query_kind": args.query_kind,
            "downloaded_files": downloaded,
            "closure_note": "Closure is run automatically only for direct csv/parquet/pq/csv.gz downloads. If EGMS returns zip/gpkg, extract/convert to csv or parquet and rerun with --local-egms-file.",
        },
    )
    print(f"Wrote search response to {args.outdir / 'egms_clms_priority_search_response_v1.json'}")
    print(f"Wrote download manifest to {args.outdir / 'egms_clms_priority_download_manifest_v1.json'}")


if __name__ == "__main__":
    main()
