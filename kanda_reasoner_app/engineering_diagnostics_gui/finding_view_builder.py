# project-path: kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py
"""Pure finding-view construction for Engineering Diagnostics GUI."""

from __future__ import annotations

from kanda_reasoner_app.engineering_diagnostics import (
    DiagnosticComparison,
    DiagnosticFindingRecord,
    DiagnosticRunRecord,
    EngineeringDiagnosticsEnricher,
    build_diagnostic_remediation_intents,
)

from .models import DiagnosticFindingView

__all__ = ["build_diagnostic_finding_views"]


def build_diagnostic_finding_views(
    run: DiagnosticRunRecord,
    findings: tuple[DiagnosticFindingRecord, ...],
    comparison: DiagnosticComparison,
    enricher: EngineeringDiagnosticsEnricher,
    group_index,
    lifecycle_index,
) -> tuple[DiagnosticFindingView, ...]:
    """Project baseline, enrichment, governance, and advice into immutable rows."""
    new = set(comparison.new_issue_fingerprints)
    persistent = set(comparison.persistent_issue_fingerprints)
    enrichments = enricher.enrich_many(findings)
    remediation_intents = build_diagnostic_remediation_intents(
        run,
        findings,
        enrichments,
        group_index,
        lifecycle_index,
    )
    rows: list[DiagnosticFindingView] = []
    for finding, enrichment, remediation in zip(
        findings,
        enrichments,
        remediation_intents,
    ):
        baseline_state = "current"
        if finding.issue_fingerprint in new:
            baseline_state = "new"
        elif finding.issue_fingerprint in persistent:
            baseline_state = "persistent"
        groups = tuple(group_index.get(finding.issue_fingerprint, ()))
        issue_head = lifecycle_index.get(("ISSUE", finding.issue_fingerprint))
        group_heads = tuple(
            head
            for group in groups
            for head in (lifecycle_index.get(("GROUP", group.group_id)),)
            if head is not None
        )
        rows.append(
            DiagnosticFindingView(
                finding,
                baseline_state,
                enrichment,
                groups,
                decision_state=(
                    issue_head.current_state if issue_head is not None else "OPEN"
                ),
                decision_generation=(
                    issue_head.generation if issue_head is not None else 0
                ),
                decision_head=issue_head,
                group_decision_heads=group_heads,
                remediation_intent=remediation,
            )
        )
    return tuple(rows)
