# project-path: kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py
"""Canonical Engineering Diagnostics table-column contract."""

from __future__ import annotations

__all__ = ["ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS"]

ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS = (
    ("lifecycle_state", "Baseline State"),
    ("decision_state", "Decision State"),
    ("remediation_action_class", "Remediation"),
    ("severity", "Severity"),
    ("code", "Code"),
    ("scope_classification", "Scope"),
    ("frozen_status", "Frozen"),
    ("owner_status", "Owner Status"),
    ("owner_confidence", "Owner Confidence"),
    ("canonical_owner", "Canonical Owner"),
    ("group_kind", "Group Kind"),
    ("group_label", "Diagnostic Group"),
    ("relative_path", "Path"),
    ("line", "Line"),
    ("message", "Message"),
    ("confidence", "Confidence"),
)
