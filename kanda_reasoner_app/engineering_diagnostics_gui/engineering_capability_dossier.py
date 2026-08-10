# project-path: kanda_reasoner_app/engineering_diagnostics_gui/engineering_capability_dossier.py
"""Architecture-grade correction dossiers for Engineering Safety capabilities."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
from typing import Iterable

from ._engineering_capability_models import EngineeringCapabilityResult

__all__ = [
    "CapabilityEvidenceProjection",
    "build_capability_dossier_lines",
    "project_capability_evidence",
]

_MAX_LIST_ITEMS = 80
_MAX_EVIDENCE_LINES = 180
_PATH_RE = re.compile(
    r"(?P<path>(?:[A-Za-z]:[\\/])?(?:[A-Za-z0-9_. -]+[\\/])+[A-Za-z0-9_. -]+\.py)"
)
_ATTRIBUTE_RE = re.compile(
    r"module ['\"](?P<module>[A-Za-z0-9_.]+)['\"] has no attribute "
    r"['\"](?P<symbol>[^'\"]+)['\"]"
)


@dataclass(frozen=True, slots=True)
class CapabilityEvidenceProjection:
    """Parsed read-only evidence projected from one public capability output."""

    report_id: str = ""
    report_type: str = ""
    reported_project_root: str = ""
    risk_level: str = ""
    confidence: str = ""
    owning_box: str = ""
    summary: str = ""
    root_cause: str = ""
    suggested_first_action: str = ""
    rollback_plan: str = ""
    affected_files: tuple[str, ...] = ()
    related_symbols: tuple[str, ...] = ()
    tests_to_run: tuple[str, ...] = ()
    input_sources: tuple[str, ...] = ()
    review_state: tuple[str, ...] = ()
    decision_details: tuple[str, ...] = ()
    failure_signature: str = ""
    failure_module: str = ""
    failure_symbol: str = ""
    evidence_sha256: str = ""
    evidence_line_count: int = 0


def _unique(values: Iterable[str], limit: int = _MAX_LIST_ITEMS) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in result:
            result.append(text)
        if len(result) >= limit:
            break
    return tuple(result)


def _sections(text: str) -> tuple[dict[str, list[str]], list[str]]:
    sections: dict[str, list[str]] = {}
    preamble: list[str] = []
    current: str | None = None
    for raw_line in str(text or "").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current = line[3:].strip().casefold()
            sections.setdefault(current, [])
            continue
        if current is None:
            preamble.append(line)
        else:
            sections[current].append(line)
    return sections, preamble


def _field(lines: Iterable[str], label: str) -> str:
    prefix = label.casefold() + ":"
    for line in lines:
        stripped = line.strip()
        if stripped.casefold().startswith(prefix):
            return stripped.split(":", 1)[1].strip()
    return ""


def _section_text(sections: dict[str, list[str]], name: str) -> str:
    lines = sections.get(name.casefold(), [])
    return "\n".join(line.strip() for line in lines if line.strip()).strip()


def _bullet_items(sections: dict[str, list[str]], name: str) -> tuple[str, ...]:
    values: list[str] = []
    for line in sections.get(name.casefold(), []):
        stripped = line.strip()
        if stripped.startswith("- "):
            values.append(stripped[2:].strip())
        elif stripped:
            values.append(stripped)
    return _unique(values)


def _decision_values(
    sections: dict[str, list[str]],
    key: str,
) -> tuple[str, ...]:
    values: list[str] = []
    target = key.casefold()
    for line in sections.get("decision details", []):
        stripped = line.strip().lstrip("-").strip()
        if "=" in stripped:
            candidate, value = stripped.split("=", 1)
            if candidate.strip().casefold() == target:
                values.append(value.strip())
        elif ":" in stripped:
            candidate, value = stripped.split(":", 1)
            if candidate.strip().casefold() == target:
                values.append(value.strip())
    return _unique(values)


def _paths_from_text(text: str) -> tuple[str, ...]:
    values: list[str] = []
    for match in _PATH_RE.finditer(text):
        path = match.group("path").strip().replace("/", "\\")
        if path.casefold().startswith("python\\"):
            continue
        values.append(path)
    return _unique(values)


def _module_to_relative_path(project_root: Path, module_name: str) -> str:
    candidate = project_root / (module_name.replace(".", "/") + ".py")
    try:
        resolved = candidate.resolve(strict=True)
        root = project_root.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return ""
    return resolved.relative_to(root).as_posix()


def project_capability_evidence(
    project_root: str | Path,
    item: EngineeringCapabilityResult,
) -> CapabilityEvidenceProjection:
    """Parse deterministic public capability evidence without changing truth."""
    root = Path(project_root).expanduser().resolve(strict=True)
    evidence = str(item.evidence or "")
    sections, preamble = _sections(evidence)
    preamble_lines = [line for line in preamble if line.strip()]
    attribute = _ATTRIBUTE_RE.search(evidence)
    failure_module = attribute.group("module") if attribute else ""
    failure_symbol = attribute.group("symbol") if attribute else ""

    affected = list(_bullet_items(sections, "affected files"))
    affected.extend(_decision_values(sections, "owner_path"))
    affected.extend(_decision_values(sections, "active_target_path"))
    affected.extend(_decision_values(sections, "main_path"))
    affected.extend(_decision_values(sections, "helper_path"))
    affected.extend(_paths_from_text(evidence))
    if failure_module:
        relative = _module_to_relative_path(root, failure_module)
        if relative:
            affected.append(relative)

    symbols: list[str] = []
    function_name = _field(preamble_lines, "Function")
    if function_name:
        symbols.append(function_name)
    symbols.extend(_decision_values(sections, "query"))
    if failure_symbol:
        symbols.append(failure_symbol)

    summary = _field(preamble_lines, "Summary")
    if not summary:
        summary = _section_text(sections, "summary")
    root_cause = _section_text(sections, "root cause or risk hypothesis")
    first_action = _section_text(sections, "suggested first action")
    rollback = _section_text(sections, "rollback plan")
    tests = _bullet_items(sections, "tests to run")
    if not tests:
        tests = _bullet_items(sections, "tests to add")

    failure_signature = ""
    if item.status_code not in {None, 0}:
        first_error = next(
            (line.strip() for line in evidence.splitlines() if line.strip()),
            "",
        )
        failure_signature = first_error or (
            "Public capability exit status " + str(item.status_code)
        )

    return CapabilityEvidenceProjection(
        report_id=_field(preamble_lines, "Report ID"),
        report_type=_field(preamble_lines, "Report type"),
        reported_project_root=_field(preamble_lines, "Project root"),
        risk_level=_field(preamble_lines, "Risk level"),
        confidence=_field(preamble_lines, "Confidence"),
        owning_box=_field(preamble_lines, "Owning box"),
        summary=summary,
        root_cause=root_cause,
        suggested_first_action=first_action,
        rollback_plan=rollback,
        affected_files=_unique(affected),
        related_symbols=_unique(symbols),
        tests_to_run=tests,
        input_sources=_bullet_items(sections, "input sources"),
        review_state=_bullet_items(sections, "review state"),
        decision_details=_bullet_items(sections, "decision details"),
        failure_signature=failure_signature,
        failure_module=failure_module,
        failure_symbol=failure_symbol,
        evidence_sha256=hashlib.sha256(
            evidence.encode("utf-8", errors="replace")
        ).hexdigest(),
        evidence_line_count=len(evidence.splitlines()),
    )


def _joined(values: Iterable[str]) -> str:
    items = tuple(str(value).strip() for value in values if str(value).strip())
    return ", ".join(items) if items else "(none established)"


def _specific_correction(
    item: EngineeringCapabilityResult,
    projection: CapabilityEvidenceProjection,
) -> str:
    if projection.failure_module and projection.failure_symbol:
        return (
            "Reconcile the exact owner for module "
            + projection.failure_module
            + " and missing symbol "
            + projection.failure_symbol
            + ". Determine whether the symbol was renamed, moved, removed, or "
            "incorrectly referenced. Restore the canonical public contract or "
            "update its public caller only after exact-source inspection; do not "
            "create a duplicate helper merely to satisfy the failing call."
        )
    if projection.suggested_first_action:
        return projection.suggested_first_action
    return item.correction_guidance


def _problem_id(item: EngineeringCapabilityResult, projection: CapabilityEvidenceProjection) -> str:
    identity = "\n".join(
        (
            item.surface,
            item.command_name,
            item.status,
            item.severity,
            projection.evidence_sha256,
        )
    ).encode("utf-8")
    return "CAP-" + hashlib.sha256(identity).hexdigest()[:16].upper()


def _evidence_excerpt(text: str) -> tuple[str, ...]:
    lines = [line.rstrip() for line in str(text or "").splitlines()]
    if len(lines) <= _MAX_EVIDENCE_LINES:
        return tuple(lines)
    head = lines[:120]
    tail = lines[-40:]
    return tuple(
        head
        + ["", "[... bounded capability evidence ...]", ""]
        + tail
    )


def build_capability_dossier_lines(
    project_root: str | Path,
    item: EngineeringCapabilityResult,
    index: int,
) -> list[str]:
    """Render one explicit Architecture-style capability assessment dossier."""
    projection = project_capability_evidence(project_root, item)
    problem = item.severity in {"ERROR", "WARNING"}
    lines = [
        "CAPABILITY " + str(index),
        "Surface: " + item.surface,
        "Section: " + item.section,
        "Capability: " + item.label,
        "Command: " + item.command_name,
        "Evaluation scope: " + item.scope_mode,
        "Execution contract: " + item.execution,
        "Status: " + item.status,
        "Severity: " + item.severity,
        "Assessment reason: " + item.assessment_reason,
        "Status code: " + (
            "(not executed)" if item.status_code is None else str(item.status_code)
        ),
        "Elapsed seconds: " + ("%.3f" % item.elapsed_seconds),
        "Finding count: " + (
            "(not applicable)"
            if item.finding_count is None
            else str(item.finding_count)
        ),
        "Report ID: " + (projection.report_id or "(not supplied)"),
        "Report type: " + (projection.report_type or "(not supplied)"),
        "Reported Project root: "
        + (projection.reported_project_root or "(not supplied)"),
        "Risk level: " + (projection.risk_level or "(not supplied)"),
        "Confidence: " + (projection.confidence or "(not supplied)"),
        "Owning Box from capability evidence: "
        + (projection.owning_box or "(not established)"),
        "Affected files: " + _joined(projection.affected_files),
        "Related symbols: " + _joined(projection.related_symbols),
        "Input/evidence sources: " + _joined(projection.input_sources),
        "Summary: " + (projection.summary or "(not supplied)"),
        "Root cause / risk hypothesis: "
        + (projection.root_cause or "(not established)"),
        "Suggested first action: "
        + (projection.suggested_first_action or "(not supplied)"),
        "Tests to run: " + _joined(projection.tests_to_run),
        "Rollback expectation: "
        + (projection.rollback_plan or "(not supplied by capability)"),
        "Review state: " + _joined(projection.review_state),
        "Decision details: " + _joined(projection.decision_details),
        "Failure signature: "
        + (projection.failure_signature or "(no execution failure signature)"),
        "Failure module: " + (projection.failure_module or "(none)"),
        "Failure symbol: " + (projection.failure_symbol or "(none)"),
        "Capability evidence SHA256: " + projection.evidence_sha256,
        "Capability evidence lines: " + str(projection.evidence_line_count),
        "Correction guidance: " + _specific_correction(item, projection),
        "Exact source inspection required before edit: YES",
        "Automatic correction authorized: NO",
        "Full Diagnostics source-apply lane: ABSENT",
    ]
    if problem:
        lines.extend(
            (
                "AI CORRECTION DOSSIER: REQUIRED",
                "Problem ID: " + _problem_id(item, projection),
                "Why this matters: The capability produced an explicit "
                + item.severity
                + " state that must remain visible to downstream AI review.",
                "Canonical-owner rule: Correct the public capability owner or "
                "its proven dependency; do not patch Full Diagnostics merely "
                "because it surfaced the problem.",
                "Protected-owner rule: Full Audit, Pontual Audit private state, "
                "EngineeringDiagnosticsStore, Symbol Atlas internals, Project "
                "Selection Registry, and Freeze Memory remain separate owners.",
            )
        )
    lines.append("Evidence:")
    evidence_lines = _evidence_excerpt(item.evidence)
    if evidence_lines:
        lines.extend("  " + line for line in evidence_lines)
    else:
        lines.append("  (no evidence payload supplied)")
    lines.extend(("-" * 88, ""))
    return lines
