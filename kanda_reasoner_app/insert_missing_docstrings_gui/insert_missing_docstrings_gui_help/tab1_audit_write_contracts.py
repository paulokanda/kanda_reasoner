
# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/tab1_audit_write_contracts.py
"""Shared contracts for Tab 1 audit write routing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


__all__ = [
    "TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY",
    "TAB1_AUDIT_WRITE_ROUTE_STATUS_READY",
    "TAB1_AUDIT_WRITE_ROUTE_STATUS_SKIPPED",
    "Tab1AuditWritePlan",
    "Tab1AuditWriteTarget",
]


TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY = "empty"
TAB1_AUDIT_WRITE_ROUTE_STATUS_READY = "ready"
TAB1_AUDIT_WRITE_ROUTE_STATUS_SKIPPED = "skipped"


@dataclass(frozen=True)
class Tab1AuditWriteTarget:
    """Represent one Python module target from the Tab 1 audit."""

    file_path: Path
    module_name: str
    finding_count: int


@dataclass(frozen=True)
class Tab1AuditWritePlan:
    """Represent the write plan derived from Tab 1 audit findings."""

    status: str
    project_root: Path
    targets: tuple[Tab1AuditWriteTarget, ...]
    ignored_findings: tuple[str, ...]
    message: str
