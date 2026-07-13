from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from benchmark_delta_vlm_lisc_observability import (
    geotiff_tags,
    read_csv,
    sample_to_target as _sample_to_target,
    write_csv,
)


def geotiff_info(path: Path) -> dict[str, Any]:
    return geotiff_tags(path)


def sample_to_target(source: dict[str, Any], target: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    return _sample_to_target(source, target)


def coherence_array(sample: np.ndarray | dict[str, Any]) -> np.ndarray:
    if isinstance(sample, dict):
        return np.asarray(sample.get("array"), dtype=float)
    return np.asarray(sample, dtype=float)
