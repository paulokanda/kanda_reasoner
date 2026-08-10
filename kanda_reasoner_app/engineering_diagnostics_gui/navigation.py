# project-path: kanda_reasoner_app/engineering_diagnostics_gui/navigation.py
"""Public read-only navigation helpers for Engineering Diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from .navigation_models import (
    EngineeringDiagnosticsNavigationRequest,
    EngineeringDiagnosticsNavigationSummary,
)
from .source_identity import project_source_fingerprint

__all__ = [
    "build_engineering_diagnostics_navigation_summary",
    "request_engineering_diagnostics_navigation",
]


def _raw_count(provenance: Mapping[str, object], fallback: int) -> int:
    for key in ("raw_finding_count", "raw_issue_count"):
        value = provenance.get(key)
        if isinstance(value, int) and value >= 0:
            return value
    metadata = provenance.get("metadata")
    if isinstance(metadata, Mapping):
        for key in ("raw_finding_count", "raw_issue_count"):
            value = metadata.get(key)
            if isinstance(value, int) and value >= 0:
                return value
    return max(0, int(fallback))


def build_engineering_diagnostics_navigation_summary(
    controller: object,
    project_root: str | Path,
    producer_id: str,
) -> EngineeringDiagnosticsNavigationSummary:
    """Return counts for the newest run matching the current Project source."""
    root = Path(project_root).expanduser().resolve(strict=True)
    current_source = project_source_fingerprint(root)
    runs = controller.list_runs(root, producer_id=producer_id, limit=200)
    compatible = next(
        (
            run
            for run in runs
            if run.completion_status == "COMPLETED"
            and run.source_fingerprint == current_source
        ),
        None,
    )
    if compatible is None:
        return EngineeringDiagnosticsNavigationSummary(
            producer_id=str(producer_id),
            compatible_run_id="",
            raw_finding_count=0,
            canonical_issue_count=0,
            diagnostic_group_count=0,
            new_high_priority_count=0,
            comparison_status="NO_COMPATIBLE_RUN",
            source_fingerprint=current_source,
        )
    view = controller.load_run_view(root, compatible.run_id)
    new_ids = set(view.comparison.new_issue_fingerprints)
    high_priority = sum(
        1
        for finding in view.findings
        if finding.record.severity == "error"
        and finding.record.issue_fingerprint in new_ids
    )
    group_count = len({group.group_id for group in view.groups})
    return EngineeringDiagnosticsNavigationSummary(
        producer_id=compatible.producer_id,
        compatible_run_id=compatible.run_id,
        raw_finding_count=_raw_count(compatible.provenance, compatible.finding_count),
        canonical_issue_count=compatible.finding_count,
        diagnostic_group_count=group_count,
        new_high_priority_count=high_priority,
        comparison_status=view.comparison.status,
        source_fingerprint=current_source,
    )


def request_engineering_diagnostics_navigation(
    panel: object,
    request: EngineeringDiagnosticsNavigationRequest,
) -> bool:
    """Apply one request through the panel's narrow public navigation contract."""
    if not isinstance(request, EngineeringDiagnosticsNavigationRequest):
        raise TypeError("EngineeringDiagnosticsNavigationRequest is required.")
    handler = getattr(panel, "apply_engineering_diagnostics_navigation", None)
    if not callable(handler):
        raise RuntimeError("ENGINEERING_DIAGNOSTICS_NAVIGATION_CONTRACT_MISSING")
    return bool(handler(request))
