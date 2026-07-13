from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(r"C:\Users\刘子轩\Desktop\nature")
CHECKSUMS = ROOT / "11_submission_ready_v1" / "submission_checksums_v1.md"
CHECKSUMS_MIRROR = ROOT / "11_submission_ready_v1" / "source_data" / "submission_checksums_v1.md"

EXTRA_PATHS = [
    "08_nature_experiment_plan/transfer_validation_scores_v1/transfer_validation_scores_v1.csv",
    "08_nature_experiment_plan/transfer_validation_scores_v1/transfer_validation_scores_v1.md",
    "11_submission_ready_v1/source_data/transfer_validation_scores_v1/transfer_validation_scores_v1.csv",
    "11_submission_ready_v1/source_data/transfer_validation_scores_v1/transfer_validation_scores_v1.md",
    "03_exposure_closure/hierarchical_model_v1/hierarchical_model_coefficients.csv",
    "03_exposure_closure/hierarchical_model_v1/hierarchical_model_comparison.csv",
    "03_exposure_closure/hierarchical_model_v1/hierarchical_model_leave_one_out.csv",
    "03_exposure_closure/hierarchical_model_v1/hierarchical_model_meta.json",
    "03_exposure_closure/hierarchical_model_v1/hierarchical_model_report.md",
    "11_submission_ready_v1/source_data/hierarchical_model_v1/hierarchical_model_coefficients.csv",
    "11_submission_ready_v1/source_data/hierarchical_model_v1/hierarchical_model_comparison.csv",
    "11_submission_ready_v1/source_data/hierarchical_model_v1/hierarchical_model_leave_one_out.csv",
    "11_submission_ready_v1/source_data/hierarchical_model_v1/hierarchical_model_meta.json",
    "11_submission_ready_v1/source_data/hierarchical_model_v1/hierarchical_model_report.md",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> None:
    raw = CHECKSUMS.read_text(encoding="utf-8").splitlines()
    paths: list[str] = []
    for line in raw:
        if not line.startswith("| `"):
            continue
        parts = line.split("`")
        if len(parts) < 3:
            continue
        rel = parts[1]
        if rel in {
            "11_submission_ready_v1/submission_checksums_v1.md",
            "11_submission_ready_v1/source_data/submission_checksums_v1.md",
        }:
            continue
        if rel not in paths:
            paths.append(rel)
    for rel in EXTRA_PATHS:
        if rel not in paths:
            paths.append(rel)

    rows: list[str] = []
    for rel in paths:
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(path)
        rows.append(f"| `{rel}` | `{sha256(path)}` |")

    lines = [
        "# Submission Checksums v1",
        "Date: 2026-07-10",
        "",
        "## Canonical Files",
        "",
        "| Path | SHA256 |",
        "|---|---|",
        *rows,
        "",
        "## Notes",
        "- These hashes lock the current local handoff state.",
        "- Any change to the manuscript, references, or package contents should update this file.",
        "- The checksum list is local only; it is not a public release artifact.",
        "- The archive hash is recorded separately in `08_nature_experiment_plan/submission_archive_hash_v1.md` to avoid self-referential hashing.",
        "",
    ]
    text = "\n".join(lines)
    CHECKSUMS.write_text(text, encoding="utf-8")
    CHECKSUMS_MIRROR.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
