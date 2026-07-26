# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_semantic_naming.py
"""Deterministic semantic helper filenames from responsibility evidence."""
from __future__ import annotations

import re
from pathlib import Path

from .planner_responsibility_labels import ResponsibilityLabel

__all__ = ["semantic_helper_filename"]

_SAFE_PART = re.compile(r"[^a-z0-9_]+")


def semantic_helper_filename(
    target_path: Path,
    label: ResponsibilityLabel,
    ordinal: int = 1,
) -> str:
    """Return a stable private helper basename from responsibility evidence."""
    target_stem = _safe_part(target_path.stem)
    responsibility = _safe_part(label.primary_responsibility)
    if label.confidence == "low":
        responsibility = "cohesive_operations"
    serial = "" if ordinal == 1 else f"_{ordinal}"
    return f"_{target_stem}_{responsibility}{serial}.py"


def _safe_part(value: str) -> str:
    cleaned = _SAFE_PART.sub("_", str(value).strip().lower()).strip("_")
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned or "operations"
