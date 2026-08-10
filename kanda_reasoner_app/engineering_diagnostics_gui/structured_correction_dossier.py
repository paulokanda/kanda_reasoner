# project-path: kanda_reasoner_app/engineering_diagnostics_gui/structured_correction_dossier.py
"""Architecture-grade details for grouped structured diagnostic findings."""

from __future__ import annotations

from collections import Counter
import hashlib
from pathlib import Path
from typing import Iterable

from .models import DiagnosticFindingView

__all__ = ["build_structured_correction_dossier_lines"]

_MAX_REPRESENTATIVES = 2
_EXCERPT_RADIUS = 4
_MAX_EXCERPT_CHARS = 8000


def _unique(values: Iterable[object]) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in result:
            result.append(text)
    return tuple(result)


def _joined(values: Iterable[object]) -> str:
    items = _unique(values)
    return ", ".join(items) if items else "(none)"


def _group_id(producer_id: str, findings: tuple[DiagnosticFindingView, ...]) -> str:
    raw = "\n".join(
        [producer_id]
        + sorted(view.record.issue_fingerprint for view in findings)
    ).encode("utf-8")
    return "EDG-" + hashlib.sha256(raw).hexdigest()[:16].upper()


def _safe_source_excerpt(
    project_root: Path,
    relative_path: str,
    line: int | None,
) -> tuple[str, ...]:
    if line is None or int(line) < 1:
        return ()
    root = project_root.resolve(strict=True)
    candidate = (root / str(relative_path)).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        return ()
    if not candidate.is_file() or candidate.stat().st_size > 2_000_000:
        return ()
    try:
        text = candidate.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ()
    lines = text.splitlines()
    target = int(line) - 1
    if target >= len(lines):
        return ()
    start = max(0, target - _EXCERPT_RADIUS)
    end = min(len(lines), target + _EXCERPT_RADIUS + 1)
    rendered = [
        (">> " if index == target else "   ")
        + str(index + 1)
        + ": "
        + lines[index]
        for index in range(start, end)
    ]
    payload = "\n".join(rendered)
    if len(payload) > _MAX_EXCERPT_CHARS:
        payload = payload[:_MAX_EXCERPT_CHARS] + "\n[excerpt truncated]"
    return tuple(payload.splitlines())


def _evidence_value(view: DiagnosticFindingView, key: str) -> str:
    evidence = dict(view.record.evidence)
    for candidate in (key, key.lower(), key.upper()):
        if candidate in evidence:
            value = evidence[candidate]
            if isinstance(value, (tuple, list, set)):
                return _joined(value)
            return str(value)
    return ""


def _representative_findings(
    findings: tuple[DiagnosticFindingView, ...],
) -> tuple[DiagnosticFindingView, ...]:
    severity_rank = {
        "critical": 0,
        "error": 1,
        "high": 2,
        "warning": 3,
        "medium": 4,
        "low": 5,
        "info": 6,
    }
    ordered = sorted(
        findings,
        key=lambda view: (
            severity_rank.get(view.record.severity.lower(), 7),
            view.record.relative_path,
            view.record.line or 0,
            view.record.issue_fingerprint,
        ),
    )
    return tuple(ordered[:_MAX_REPRESENTATIVES])


def build_structured_correction_dossier_lines(
    project_root: str | Path,
    producer_id: str,
    findings: tuple[DiagnosticFindingView, ...],
) -> list[str]:
    """Render one bounded Architecture-style dossier for one correction group."""
    root = Path(project_root).expanduser().resolve(strict=True)
    owner = tuple(view.enrichment.owner for view in findings)
    scope = tuple(view.enrichment.scope for view in findings)
    frozen = tuple(view.enrichment.frozen_path for view in findings)
    records = tuple(view.record for view in findings)
    intents = tuple(
        view.remediation_intent
        for view in findings
        if view.remediation_intent is not None
    )
    severity_counts = Counter(record.severity for record in records)
    affected_files = _unique(record.relative_path for record in records)
    symbols = _unique(record.symbol_id for record in records)
    semantic_keys = _unique(record.semantic_key for record in records)
    location_keys = _unique(record.location_key for record in records)
    suggested_actions = _unique(record.suggested_action for record in records)
    validation_sources = _unique(
        value
        for view in findings
        for value in (
            _evidence_value(view, "validation_source"),
            _evidence_value(view, "validation_sources"),
            _evidence_value(view, "source"),
        )
        if value
    )
    expected_files = _unique(
        path
        for intent in intents
        for path in intent.expected_affected_files
    )
    focused_tests = _unique(
        test
        for intent in intents
        for test in intent.validation_plan.focused_tests
    )
    validation_commands = _unique(
        command
        for intent in intents
        for command in intent.validation_plan.validation_commands
    )
    rollback = _unique(
        intent.validation_plan.rollback_expectation for intent in intents
    )
    evidence_required = _unique(
        item
        for intent in intents
        for item in intent.validation_plan.evidence_required
    )
    governance = _unique(
        rule
        for intent in intents
        for rule in intent.project_governance_rules
    )

    lines = [
        "ARCHITECTURE-GRADE CORRECTION DOSSIER",
        "Problem group ID: " + _group_id(producer_id, findings),
        "Producer: " + producer_id,
        "Issue count: " + str(len(findings)),
        "Severity counts: " + str(dict(sorted(severity_counts.items()))),
        "Affected files: " + _joined(affected_files),
        "Related symbols: " + _joined(symbols),
        "Semantic keys: " + _joined(semantic_keys),
        "Location keys: " + _joined(location_keys),
        "Suggested actions from producers: " + _joined(suggested_actions),
        "Canonical owners: " + _joined(
            getattr(view, "canonical_owner", "") for view in findings
        ),
        "Owner statuses: " + _joined(
            getattr(view, "owner_status", "") for view in findings
        ),
        "Owner confidences: " + _joined(
            getattr(view, "owner_confidence", "") for view in findings
        ),
        "Active owner candidates: " + _joined(
            candidate
            for item in owner
            for candidate in getattr(item, "active_candidates", ())
        ),
        "Historical owner candidates: " + _joined(
            candidate
            for item in owner
            for candidate in getattr(item, "historical_candidates", ())
        ),
        "Owner selection methods: " + _joined(
            getattr(item, "selection_method", "") for item in owner
        ),
        "Owner evidence: " + _joined(
            evidence
            for item in owner
            for evidence in getattr(item, "evidence", ())
        ),
        "Scope classifications: " + _joined(
            getattr(view, "scope_classification", "") for view in findings
        ),
        "Scope confidence: " + _joined(
            getattr(view, "scope_confidence", "") for view in findings
        ),
        "Scope methods: " + _joined(
            getattr(item, "method", "") for item in scope
        ),
        "Scope evidence: " + _joined(
            evidence for item in scope for evidence in item.evidence
        ),
        "Freeze statuses: " + _joined(
            getattr(view, "frozen_status", "") for view in findings
        ),
        "Governing Freeze IDs: " + _joined(
            freeze_id for item in frozen for freeze_id in item.governing_freeze_ids
        ),
        "Matched protected paths: " + _joined(
            path for item in frozen for path in item.matched_protected_paths
        ),
        "Freeze evidence: " + _joined(
            evidence for item in frozen for evidence in item.evidence
        ),
        "Validation sources: " + _joined(validation_sources),
        "Expected files to change: " + _joined(expected_files),
        "Focused tests: " + _joined(focused_tests),
        "Validation commands: " + _joined(validation_commands),
        "Required validation evidence: " + _joined(evidence_required),
        "Rollback expectation: " + _joined(rollback),
        "Project governance rules: " + _joined(governance),
        "Exact current source inspection before edit: REQUIRED",
        "Automatic source apply: NO",
        "Competing owner creation authorized: NO",
    ]

    for index, view in enumerate(_representative_findings(findings), start=1):
        record = view.record
        lines.extend(
            (
                "Representative problem " + str(index) + ":",
                "  Issue fingerprint: " + record.issue_fingerprint,
                "  Evidence digest: " + record.evidence_digest,
                "  Rule/code: " + record.code,
                "  Category: " + record.category,
                "  Severity: " + record.severity,
                "  Confidence: " + record.confidence,
                "  Path: " + record.relative_path,
                "  Line: " + str(record.line or "(not supplied)"),
                "  Symbol: " + (record.symbol_id or "(not supplied)"),
                "  Message: " + record.message,
            )
        )
        excerpt = _safe_source_excerpt(root, record.relative_path, record.line)
        lines.append("  Exact source excerpt:")
        if excerpt:
            lines.extend("    " + line for line in excerpt)
        else:
            lines.append(
                "    (not embedded; inspect the exact current source path before edit)"
            )
    lines.extend(("END ARCHITECTURE-GRADE DOSSIER", ""))
    return lines
