# project-path: kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py
"""Pure summary text for one Engineering Diagnostics run view."""

from __future__ import annotations

from .models import DiagnosticRunView

__all__ = ["build_diagnostic_run_summary"]


def build_diagnostic_run_summary(view: DiagnosticRunView) -> str:
    """Return compact deterministic run and governance counts."""
    comparison = view.comparison
    frozen_count = sum(
        1
        for finding in view.findings
        if finding.frozen_status in ("FROZEN", "TOUCHES_FROZEN")
    )
    unknown_scope = sum(
        1 for finding in view.findings if finding.scope_classification == "UNKNOWN"
    )
    needs_owner_review = sum(
        1 for finding in view.findings if finding.owner_status == "NEEDS_REVIEW"
    )
    governed_count = sum(
        1 for finding in view.findings if finding.decision_state != "OPEN"
    )
    safe_mechanical = sum(
        1
        for finding in view.findings
        if finding.remediation_action_class == "SAFE_MECHANICAL_FIX_AVAILABLE"
    )
    governed_wave = sum(
        1
        for finding in view.findings
        if finding.remediation_action_class == "PLAN_GOVERNED_WAVE"
    )
    return (
        "Findings: "
        + str(view.run.finding_count)
        + " | comparison: "
        + comparison.status
        + " | new: "
        + str(len(comparison.new_issue_fingerprints))
        + " | persistent: "
        + str(len(comparison.persistent_issue_fingerprints))
        + " | resolved: "
        + str(len(comparison.resolved_issue_fingerprints))
        + " | frozen impact: "
        + str(frozen_count)
        + " | unknown scope: "
        + str(unknown_scope)
        + " | owner review: "
        + str(needs_owner_review)
        + " | governed decisions: "
        + str(governed_count)
        + " | safe remediation candidates: "
        + str(safe_mechanical)
        + " | governed-wave remediation: "
        + str(governed_wave)
    )
