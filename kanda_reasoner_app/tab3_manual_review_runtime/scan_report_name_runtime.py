# project-path: kanda_reasoner_app/tab3_manual_review_runtime/scan_report_name_runtime.py
"""Report-name helpers for the Tab 3 scan-only workflow."""

from __future__ import annotations

import re
from pathlib import Path

__all__ = [
    "REPORT_DATE_FORMAT",
    "build_project_missing_docstrings_report_name",
]

REPORT_DATE_FORMAT = "%Y%m%d_%H%M%S"


def build_project_missing_docstrings_report_name(project_root: Path, timestamp: str) -> str:
    """Return a project-specific timestamped missing-docstrings report name."""
    project_name = _safe_project_name(project_root.name or "project")
    return project_name + "_missing_docstrings_" + timestamp + ".jsonl"


def _safe_project_name(name: str) -> str:
    """Return a filesystem-safe project slug for report filenames."""
    safe = re.sub(r"[^A-Za-z0-9]+", "_", name.strip()).strip("_").lower()
    return safe or "project"
