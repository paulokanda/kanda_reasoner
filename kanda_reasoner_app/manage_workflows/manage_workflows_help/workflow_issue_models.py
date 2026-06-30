# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_issue_models.py
"""Workflow detector issue models.

This module owns the small report object used by Tab 2 workflow detectors.
It stays independent from the workflow runner so detector infrastructure can
be imported without triggering command execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


__all__ = [
    "WorkflowIssue",
    "workflow_issue_to_check_result",
]


@dataclass(frozen=True)
class WorkflowIssue:
    """Structured issue returned by workflow detector gates."""

    issue_id: str
    category: str
    severity: str
    workflow_step: str = ""
    file_path: str = ""
    evidence: str = ""
    expected: str = ""
    actual: str = ""
    owning_box: str = "workflow_governance"
    suggested_action: str = ""
    correction_allowed: bool = False
    details: dict[str, Any] = field(default_factory=dict)

    def normalized_severity(self) -> str:
        """Return severity normalized to the workflow result vocabulary."""
        value = self.severity.strip().lower()
        if value in {"pass", "fail", "warn", "skip"}:
            return value
        if value in {"error", "fatal"}:
            return "fail"
        if value in {"warning"}:
            return "warn"
        return "warn"

    def as_dict(self) -> dict[str, Any]:
        """Return a plain dictionary representation."""
        return {
            "issue_id": self.issue_id,
            "category": self.category,
            "severity": self.severity,
            "workflow_step": self.workflow_step,
            "file_path": self.file_path,
            "evidence": self.evidence,
            "expected": self.expected,
            "actual": self.actual,
            "owning_box": self.owning_box,
            "suggested_action": self.suggested_action,
            "correction_allowed": self.correction_allowed,
            "details": dict(self.details),
        }


def workflow_issue_to_check_result(issue: WorkflowIssue) -> dict[str, Any]:
    """Convert a workflow issue into a runner-compatible result mapping."""
    return {
        "category": "workflow_detectors",
        "name": issue.issue_id,
        "status": issue.normalized_severity(),
        "message": issue.evidence or issue.suggested_action or issue.category,
        "duration_seconds": None,
        "command": None,
        "details": issue.as_dict(),
    }
