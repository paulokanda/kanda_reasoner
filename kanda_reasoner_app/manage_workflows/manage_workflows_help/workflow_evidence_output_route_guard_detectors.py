"""Workflow detector for evidence output route regressions.

This detector keeps workflow validation aware of the storage-policy migration
that moved generated project evidence out of source. It is report-only through
workflow governance: it reads the route guard result and emits workflow issues
when the old in-source project_analysis_evidence route reappears or when the
active resolver points back inside the selected project source tree.
"""

from __future__ import annotations

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_evidence_output_route_guard_issues",
]


def _issue_from_finding(finding: object, index: int) -> WorkflowIssue:
    """Return a workflow issue for one route-guard finding."""
    risk = str(getattr(finding, "risk", "unknown_route_guard_risk"))
    path = str(getattr(finding, "path", ""))
    message = str(getattr(finding, "message", "Evidence output route guard finding."))

    return WorkflowIssue(
        issue_id="WORKFLOW_EVIDENCE_OUTPUT_ROUTE_GUARD_BLOCKED",
        category="workflow_evidence_output_route_guard",
        severity="error",
        workflow_step="storage_policy.evidence_output_route_guard",
        file_path=path,
        evidence=message,
        expected=(
            "Generated evidence must route to the external architecture audit "
            "folder, and the old in-source project_analysis_evidence folder "
            "must remain absent."
        ),
        actual=risk + ": " + path,
        owning_box="storage_policy",
        suggested_action=(
            "Run the storage-policy evidence output route guard and restore "
            "external routing before workflow validation can freeze."
        ),
        correction_allowed=False,
        details={
            "risk": risk,
            "path": path,
            "message": message,
            "finding_index": index,
        },
    )


def detect_evidence_output_route_guard_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Return workflow issues when evidence output routing regresses."""
    from kanda_reasoner_app.storage_policy.evidence_output_route_guard import (
        build_evidence_output_route_guard,
    )

    report = build_evidence_output_route_guard(
        context.resolved_root(),
        expected_min_audit_json_count=None,
        require_existing_audit_json_complete=False,
    )

    return [
        _issue_from_finding(finding, index)
        for index, finding in enumerate(report.findings, start=1)
    ]
