# project-path: kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py
"""Owner-enrichment presentation helpers for Engineering Diagnostics."""

from __future__ import annotations

import json

from .models import DiagnosticFindingView

__all__ = ["build_finding_detail_lines"]


def _joined(values: tuple[str, ...]) -> str:
    return ", ".join(values) or "(none)"


def _group_lines(view: DiagnosticFindingView) -> list[str]:
    if not view.groups:
        return ["Diagnostic groups: (none)"]
    lines = ["Diagnostic groups:"]
    for group in view.groups:
        lifecycle_head = next(
            (head for head in view.group_decision_heads if head.target_id == group.group_id),
            None,
        )
        lines.append(
            "- "
            + group.kind
            + " | "
            + group.confidence
            + " | "
            + group.label
            + " | members="
            + str(len(group.member_issue_fingerprints))
            + " | review="
            + group.review_state
            + " | lifecycle="
            + (lifecycle_head.current_state if lifecycle_head is not None else "OPEN")
        )
        lines.append("  Recipe: " + group.recipe_id)
        if group.evidence:
            lines.append(
                "  Evidence: "
                + json.dumps(dict(group.evidence), sort_keys=True)
            )
    return lines



def _remediation_lines(view: DiagnosticFindingView) -> list[str]:
    intent = view.remediation_intent
    if intent is None:
        return ["Remediation intent: (not evaluated)"]
    plan = intent.validation_plan
    lines = [
        "Remediation intent:",
        "- Action class: " + intent.action_class,
        "- Trust source: " + intent.primary_trust_source,
        "- Rule template: " + intent.rule_template_id,
        "- Likely correction: " + intent.likely_correction,
        "- Reason: " + intent.reason,
        "- Canonical owner: " + (intent.canonical_owner or "(not proven)"),
        "- Expected affected files: " + _joined(intent.expected_affected_files),
        "- Frozen-path impact: " + intent.frozen_path_impact,
        "- Required governed wave: "
        + (intent.required_governed_wave or "(none)"),
        "- Fix applicability: " + intent.fix_applicability,
        "- Mechanical safety: " + intent.mechanical_safety,
        "- Semantic review: " + intent.semantic_review_requirement,
        "- Uncertainty: " + intent.uncertainty,
        "- Executable patch: false",
        "- Source mutation allowed: false",
        "- Focused tests: " + _joined(plan.focused_tests),
        "- Validation commands: " + _joined(plan.validation_commands),
        "- Rollback expectation: " + plan.rollback_expectation,
        "- Required evidence: " + _joined(plan.evidence_required),
    ]
    if intent.ai_hypothesis is not None:
        lines.extend(
            (
                "- AI-assisted hypothesis:",
                "  Label: " + intent.ai_hypothesis.label,
                "  Text: " + intent.ai_hypothesis.text,
                "  Uncertainty: " + intent.ai_hypothesis.uncertainty,
                "  Deterministic references: "
                + _joined(intent.ai_hypothesis.deterministic_evidence_refs),
            )
        )
    return lines

def build_finding_detail_lines(
    view: DiagnosticFindingView,
    source_excerpt: str,
) -> list[str]:
    """Build deterministic detail text without importing Qt."""
    record = view.record
    owner = view.enrichment.owner
    return [
        "Baseline state: " + view.lifecycle_state,
        "Lifecycle decision state: " + view.decision_state,
        "Lifecycle generation: " + str(view.decision_generation),
        "Severity: " + record.severity,
        "Confidence: " + record.confidence,
        "Code: " + record.code,
        "Path: " + record.relative_path,
        "Line: " + str(record.line or ""),
        "Scope: " + view.scope_classification,
        "Scope confidence: " + view.scope_confidence,
        "Scope method: " + view.enrichment.scope.method,
        "Frozen status: " + view.frozen_status,
        "Governing Freeze IDs: " + (view.governing_freeze_ids or "(none)"),
        "Matched protected paths: "
        + _joined(view.enrichment.frozen_path.matched_protected_paths),
        "Owner status: " + view.owner_status,
        "Owner confidence: " + view.owner_confidence,
        "Canonical owner: " + (view.canonical_owner or "(none)"),
        "Active owner candidates: " + _joined(owner.active_candidates),
        "Historical owner candidates: "
        + _joined(owner.historical_candidates),
        "Owner selection method: " + (owner.selection_method or "(none)"),
        "Group kind: " + view.group_kind,
        "Group label: " + (view.group_label or "(none)"),
        "Group confidence: " + (view.group_confidence or "(none)"),
        "Group membership count: " + str(view.group_count),
        "",
        *_group_lines(view),
        "",
        *_remediation_lines(view),
        "",
        "Scope evidence:",
        "\n".join(view.enrichment.scope.evidence) or "(none)",
        "",
        "Freeze evidence:",
        "\n".join(view.enrichment.frozen_path.evidence) or "(none)",
        "",
        "Owner evidence:",
        "\n".join(owner.evidence) or "(none)",
        "",
        record.message,
        "",
        "Suggested action:",
        record.suggested_action or "(none)",
        "",
        "Evidence:",
        json.dumps(dict(record.evidence), indent=2, sort_keys=True),
        "",
        "Source excerpt:",
        source_excerpt,
    ]
