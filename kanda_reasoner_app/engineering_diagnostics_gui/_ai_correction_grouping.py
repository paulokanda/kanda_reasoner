# project-path: kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_grouping.py
"""Deterministic correction-group projections for AI diagnostic handoff."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from typing import Iterable

from .models import DiagnosticFindingView, DiagnosticRunView

__all__ = [
    "build_console_summary",
    "build_correction_group_lines",
    "build_run_correction_groups",
    "readiness",
    "safe_json",
]

_MAX_CONSOLE_GROUPS = 20
_MAX_REPRESENTATIVE_FINDINGS = 3
_MAX_REMEDIATION_VARIANTS = 12


def joined(values: Iterable[object]) -> str:
    normalized = [str(value).strip() for value in values if str(value).strip()]
    return ", ".join(normalized) or "(none)"


def safe_json(value: object) -> str:
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=True)
    except TypeError:
        return json.dumps(str(value), ensure_ascii=True)


def readiness(view: DiagnosticFindingView) -> str:
    intent = view.remediation_intent
    if view.frozen_status in {"FROZEN", "TOUCHES_FROZEN"}:
        return "BLOCKED_BY_FREEZE"
    if view.owner_status != "READY" or view.owner_confidence in {"low", "none"}:
        return "OWNER_REVIEW_REQUIRED"
    if intent is None:
        return "EVIDENCE_REQUIRED"
    if intent.action_class in {
        "EVIDENCE_REQUIRED",
        "HUMAN_DECISION_REQUIRED",
        "DO_NOT_TOUCH",
    }:
        return intent.action_class
    return "CORRECTION_CONTEXT_READY"


def severity_rank(value: str) -> int:
    text = str(value or "").strip().lower()
    return {
        "critical": 0,
        "error": 1,
        "high": 2,
        "warning": 3,
        "medium": 4,
        "low": 5,
        "info": 6,
    }.get(text, 7)


def selected_group(view: DiagnosticFindingView):
    manual = next((group for group in view.groups if group.kind == "MANUAL"), None)
    if manual is not None:
        return manual
    return view.groups[0] if view.groups else None


def _group_key(producer_id: str, view: DiagnosticFindingView) -> tuple[str, ...]:
    group = selected_group(view)
    intent = view.remediation_intent
    if group is not None:
        return (
            producer_id,
            "GROUP",
            group.group_id,
            readiness(view),
            intent.action_class if intent is not None else "EVIDENCE_REQUIRED",
        )
    record = view.record
    return (
        producer_id,
        "SIGNATURE",
        record.code,
        record.category,
        view.canonical_owner,
        view.frozen_status,
        readiness(view),
        intent.rule_template_id if intent is not None else "",
        intent.action_class if intent is not None else "EVIDENCE_REQUIRED",
        intent.likely_correction if intent is not None else "",
    )


def _group_identity(key: tuple[str, ...]) -> str:
    raw = "\n".join(key).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def unique(values: Iterable[object]) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in result:
            result.append(text)
    return tuple(result)


def _remediation_signature(view: DiagnosticFindingView) -> tuple[str, ...]:
    intent = view.remediation_intent
    if intent is None:
        return ("EVIDENCE_REQUIRED", "", "", "", "", "")
    return (
        intent.action_class,
        intent.primary_trust_source,
        intent.rule_template_id,
        intent.likely_correction,
        intent.reason,
        intent.semantic_review_requirement,
    )


def _remediation_variant_lines(findings: tuple[DiagnosticFindingView, ...]) -> list[str]:
    variants: dict[tuple[str, ...], list[DiagnosticFindingView]] = {}
    for view in findings:
        variants.setdefault(_remediation_signature(view), []).append(view)
    ordered = sorted(variants.items(), key=lambda item: (-len(item[1]), item[0]))
    lines = ["Remediation variant count: " + str(len(ordered))]
    for index, (_signature, members) in enumerate(
        ordered[:_MAX_REMEDIATION_VARIANTS],
        start=1,
    ):
        representative = members[0]
        intent = representative.remediation_intent
        lines.append("Remediation variant " + str(index) + ":")
        lines.append("  Member findings: " + str(len(members)))
        if intent is None:
            lines.extend(
                (
                    "  Action class: EVIDENCE_REQUIRED",
                    "  Likely correction: (not established)",
                    "  Source mutation authority: NO",
                )
            )
            continue
        plan = intent.validation_plan
        expected_files = unique(
            path
            for member in members
            if member.remediation_intent is not None
            for path in member.remediation_intent.expected_affected_files
        )
        focused_tests = unique(
            item
            for member in members
            if member.remediation_intent is not None
            for item in member.remediation_intent.validation_plan.focused_tests
        )
        validation_commands = unique(
            item
            for member in members
            if member.remediation_intent is not None
            for item in member.remediation_intent.validation_plan.validation_commands
        )
        deterministic_evidence = unique(
            item
            for member in members
            if member.remediation_intent is not None
            for item in member.remediation_intent.deterministic_evidence
        )
        governance_rules = unique(
            item
            for member in members
            if member.remediation_intent is not None
            for item in member.remediation_intent.project_governance_rules
        )
        lines.extend(
            (
                "  Action class: " + intent.action_class,
                "  Trust source: " + intent.primary_trust_source,
                "  Rule template: " + intent.rule_template_id,
                "  Likely correction: " + intent.likely_correction,
                "  Correction reason: " + intent.reason,
                "  Expected affected files: " + joined(expected_files),
                "  Frozen-path impact: " + intent.frozen_path_impact,
                "  Required governed wave: "
                + (intent.required_governed_wave or "(none)"),
                "  Fix applicability: " + intent.fix_applicability,
                "  Mechanical safety: " + intent.mechanical_safety,
                "  Semantic review requirement: "
                + intent.semantic_review_requirement,
                "  Uncertainty: " + intent.uncertainty,
                "  Focused tests: " + joined(focused_tests),
                "  Validation commands: " + joined(validation_commands),
                "  Rollback expectation: " + plan.rollback_expectation,
                "  Required validation evidence: " + joined(plan.evidence_required),
                "  Deterministic remediation evidence: "
                + joined(deterministic_evidence),
                "  Project governance rules: " + joined(governance_rules),
                "  Executable patch included: NO",
                "  Source mutation authority: NO",
            )
        )
    omitted = len(ordered) - _MAX_REMEDIATION_VARIANTS
    if omitted > 0:
        lines.append("Additional remediation variants summarized only: " + str(omitted))
    return lines


def _representative_lines(findings: tuple[DiagnosticFindingView, ...]) -> list[str]:
    ordered = sorted(
        findings,
        key=lambda view: (
            severity_rank(view.record.severity),
            view.record.relative_path,
            view.record.line or 0,
            view.record.issue_fingerprint,
        ),
    )
    lines = [
        "Representative evidence count: "
        + str(min(len(ordered), _MAX_REPRESENTATIVE_FINDINGS))
    ]
    for index, view in enumerate(
        ordered[:_MAX_REPRESENTATIVE_FINDINGS],
        start=1,
    ):
        record = view.record
        lines.extend(
            (
                "Representative finding " + str(index) + ":",
                "  Issue fingerprint: " + record.issue_fingerprint,
                "  Evidence digest: " + record.evidence_digest,
                "  Path: " + record.relative_path,
                "  Line: " + str(record.line or ""),
                "  Symbol ID: " + (record.symbol_id or "(none)"),
                "  Message: " + record.message,
                "  Raw deterministic evidence: " + safe_json(dict(record.evidence)),
            )
        )
    return lines


def build_correction_group_lines(
    index: int,
    producer_id: str,
    key: tuple[str, ...],
    findings: tuple[DiagnosticFindingView, ...],
) -> list[str]:
    first = findings[0]
    selected = selected_group(first)
    paths = tuple(sorted(unique(view.record.relative_path for view in findings)))
    severity_counts = Counter(view.record.severity for view in findings)
    readiness_counts = Counter(readiness(view) for view in findings)
    owners = unique(view.canonical_owner for view in findings)
    owner_statuses = unique(view.owner_status for view in findings)
    owner_confidences = unique(view.owner_confidence for view in findings)
    scopes = unique(view.scope_classification for view in findings)
    frozen_statuses = unique(view.frozen_status for view in findings)
    freeze_ids = unique(
        freeze_id
        for view in findings
        for freeze_id in view.enrichment.frozen_path.governing_freeze_ids
    )
    codes = unique(view.record.code for view in findings)
    categories = unique(view.record.category for view in findings)
    lifecycle_states = unique(view.decision_state for view in findings)
    group_label = selected.label if selected is not None else (
        (first.record.code or "UNSPECIFIED")
        + " / "
        + (first.record.category or "UNSPECIFIED")
    )
    lines = [
        "CORRECTION GROUP " + str(index),
        "Correction group identity: " + _group_identity(key),
        "Producer: " + producer_id,
        "Group label: " + group_label,
        "Group kind: " + (selected.kind if selected is not None else "SIGNATURE"),
        "Group confidence: "
        + (selected.confidence if selected is not None else "derived"),
        "Issue count: " + str(len(findings)),
        "Severity counts: " + safe_json(dict(sorted(severity_counts.items()))),
        "AI correction readiness counts: "
        + safe_json(dict(sorted(readiness_counts.items()))),
        "Codes: " + joined(codes),
        "Categories: " + joined(categories),
        "Lifecycle states: " + joined(lifecycle_states),
        "Canonical owners: " + joined(owners),
        "Owner statuses: " + joined(owner_statuses),
        "Owner confidences: " + joined(owner_confidences),
        "Scope classifications: " + joined(scopes),
        "Frozen statuses: " + joined(frozen_statuses),
        "Governing Freeze IDs: " + joined(freeze_ids),
        "Affected path count: " + str(len(paths)),
        "Affected paths:",
    ]
    lines.extend("  - " + path for path in paths)
    lines.extend(_remediation_variant_lines(findings))
    lines.extend(_representative_lines(findings))
    lines.extend(
        (
            "Exact source inspection required before edit: YES",
            "Raw findings remain authoritative in EngineeringDiagnosticsStore: YES",
            "Automatic correction from this handoff: NO",
            "-" * 88,
        )
    )
    return lines


def build_run_correction_groups(view: DiagnosticRunView):
    groups: dict[tuple[str, ...], list[DiagnosticFindingView]] = {}
    producer_id = view.run.producer_id
    for finding in view.findings:
        groups.setdefault(_group_key(producer_id, finding), []).append(finding)
    ordered = sorted(
        groups.items(),
        key=lambda item: (
            min(severity_rank(member.record.severity) for member in item[1]),
            -len(item[1]),
            item[0],
        ),
    )
    return tuple((key, tuple(members)) for key, members in ordered)


def build_console_summary(run_groups, finding_count: int) -> str:
    flattened = [
        (producer_id, key, findings)
        for producer_id, groups in run_groups
        for key, findings in groups
    ]
    readiness_counts = Counter(
        readiness(finding)
        for _producer, _key, findings in flattened
        for finding in findings
    )
    lines = [
        "AI CORRECTION SUMMARY",
        "Raw findings: " + str(finding_count),
        "Correction groups: " + str(len(flattened)),
        "Correction-context-ready findings: "
        + str(readiness_counts["CORRECTION_CONTEXT_READY"]),
        "Blocked-by-Freeze findings: "
        + str(readiness_counts["BLOCKED_BY_FREEZE"]),
        "Owner/evidence/human-review findings: "
        + str(
            readiness_counts["OWNER_REVIEW_REQUIRED"]
            + readiness_counts["EVIDENCE_REQUIRED"]
            + readiness_counts["HUMAN_DECISION_REQUIRED"]
        ),
        "Top correction groups:",
    ]
    ordered = sorted(
        flattened,
        key=lambda item: (
            min(severity_rank(member.record.severity) for member in item[2]),
            -len(item[2]),
            item[0],
            item[1],
        ),
    )
    for index, (producer_id, _key, findings) in enumerate(
        ordered[:_MAX_CONSOLE_GROUPS],
        start=1,
    ):
        first = findings[0]
        selected = selected_group(first)
        intent = first.remediation_intent
        label = selected.label if selected is not None else (
            (first.record.code or "UNSPECIFIED")
            + " / "
            + (first.record.category or "UNSPECIFIED")
        )
        path_count = len(unique(member.record.relative_path for member in findings))
        lines.append(
            str(index)
            + ". ["
            + producer_id
            + "] "
            + label
            + " | issues="
            + str(len(findings))
            + " | paths="
            + str(path_count)
            + " | owner="
            + (first.canonical_owner or first.owner_status)
            + " | readiness="
            + readiness(first)
        )
        if intent is not None and intent.likely_correction:
            lines.append("   Correction: " + intent.likely_correction)
    omitted = len(ordered) - _MAX_CONSOLE_GROUPS
    if omitted > 0:
        lines.append("Additional correction groups in full handoff: " + str(omitted))
    return "\n".join(lines)
