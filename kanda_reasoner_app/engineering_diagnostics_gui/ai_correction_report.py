# project-path: kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_report.py
"""Grouped correction-ready AI handoff rendering for Engineering Diagnostics."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.project_selection_registry import ProjectSelectionRecord

from ._ai_correction_grouping import (
    build_console_summary,
    build_correction_group_lines,
    build_run_correction_groups,
    readiness,
    safe_json,
)
from ._engineering_capability_models import EngineeringCapabilityCoverage
from .engineering_capability_render import (
    build_capability_console_summary,
    build_capability_report_lines,
)
from .models import DiagnosticRunView
from .run_summary import build_diagnostic_run_summary
from .structured_correction_dossier import (
    build_structured_correction_dossier_lines,
)

__all__ = [
    "AiCorrectionCollectorResult",
    "AiCorrectionReport",
    "build_full_ai_correction_report",
]


@dataclass(frozen=True, slots=True)
class AiCorrectionCollectorResult:
    """One Full Engineering Diagnostics collector result for report assembly."""

    label: str
    status: str
    run_id: str = ""
    finding_count: int = 0
    error_text: str = ""


@dataclass(frozen=True, slots=True)
class AiCorrectionReport:
    """Immutable grouped correction report plus a compact GUI summary."""

    text: str
    console_summary: str
    finding_count: int
    correction_group_count: int
    correction_ready_count: int
    blocked_count: int
    review_required_count: int
    capability_surface_count: int
    capability_error_count: int
    capability_warning_count: int


def _run_header_lines(
    view: DiagnosticRunView,
    correction_group_count: int,
) -> list[str]:
    run = view.run
    readiness_counts = Counter(readiness(finding) for finding in view.findings)
    return [
        "RUN",
        "Producer: " + run.producer_id,
        "Producer version: " + run.producer_version,
        "Run ID: " + run.run_id,
        "Attempt ID: " + run.attempt_id,
        "Project ID: " + run.project_id,
        "Project root fingerprint: " + run.project_root_fingerprint,
        "Source fingerprint: " + run.source_fingerprint,
        "Scope fingerprint: " + run.scope_fingerprint,
        "Configuration fingerprint: " + run.configuration_fingerprint,
        "Operation generation: " + str(run.operation_generation),
        "Completion status: " + run.completion_status,
        "Finding count: " + str(run.finding_count),
        "Correction group count: " + str(correction_group_count),
        "Content digest: " + run.content_digest,
        "Started at UTC: " + run.started_at_utc,
        "Completed at UTC: " + run.completed_at_utc,
        "Comparison status: " + view.comparison.status,
        "Run summary: " + build_diagnostic_run_summary(view),
        "Correction context ready: "
        + str(readiness_counts["CORRECTION_CONTEXT_READY"]),
        "Blocked by Freeze: " + str(readiness_counts["BLOCKED_BY_FREEZE"]),
        "Owner review required: "
        + str(readiness_counts["OWNER_REVIEW_REQUIRED"]),
        "Evidence required: " + str(readiness_counts["EVIDENCE_REQUIRED"]),
        "Human decision required: "
        + str(readiness_counts["HUMAN_DECISION_REQUIRED"]),
        "Do not touch: " + str(readiness_counts["DO_NOT_TOUCH"]),
        "Run provenance: " + safe_json(dict(run.provenance)),
        "=" * 88,
    ]


def build_full_ai_correction_report(
    project_root: str,
    collector_results: tuple[AiCorrectionCollectorResult, ...],
    run_views: tuple[DiagnosticRunView, ...],
    capability_coverage: EngineeringCapabilityCoverage | None = None,
    *,
    project_card: ProjectSelectionRecord | None = None,
    tool_root: str | None = None,
    complete_review_sha256: str = "",
    complete_review_item_count: int = 0,
) -> AiCorrectionReport:
    """Build a grouped deterministic handoff without duplicating raw findings."""
    all_findings = tuple(
        finding for view in run_views for finding in view.findings
    )
    if capability_coverage is None:
        capability_coverage = EngineeringCapabilityCoverage(
            results=(),
            gui_catalog_count=0,
            cli_catalog_count=0,
            unique_safety_surface_count=0,
            architecture_surface_count=0,
        )
    readiness_counts = Counter(readiness(finding) for finding in all_findings)
    correction_ready = readiness_counts["CORRECTION_CONTEXT_READY"]
    blocked = (
        readiness_counts["BLOCKED_BY_FREEZE"]
        + readiness_counts["DO_NOT_TOUCH"]
    )
    review_required = (
        readiness_counts["OWNER_REVIEW_REQUIRED"]
        + readiness_counts["EVIDENCE_REQUIRED"]
        + readiness_counts["HUMAN_DECISION_REQUIRED"]
    )
    run_groups = tuple(
        (view.run.producer_id, build_run_correction_groups(view))
        for view in run_views
    )
    correction_group_count = sum(len(groups) for _producer, groups in run_groups)
    correction_summary = build_console_summary(run_groups, len(all_findings))
    capability_summary = build_capability_console_summary(capability_coverage)
    console_summary = capability_summary + "\n\n" + correction_summary

    root_path = Path(project_root).expanduser().resolve(strict=False)
    tool_path = (
        Path(tool_root).expanduser().resolve(strict=False)
        if str(tool_root or "").strip()
        else None
    )
    same_physical_root = bool(tool_path is not None and tool_path == root_path)
    project_identity_lines = [
        "AUDIT TARGET ROLE: ACTIVE PROJECT",
        "Audit target derived from Tool root: NO",
        "KANDA Tool role: AUDIT EXECUTION PROVIDER ONLY",
        "KANDA Tool root: "
        + (str(tool_path) if tool_path is not None else "(not supplied)"),
        "Tool and Project same physical root: "
        + ("YES" if same_physical_root else "NO"),
    ]
    if project_card is not None:
        project_identity_lines.extend(
            (
                "Active Project stable ID: " + project_card.stable_project_id,
                "Active Project slug: " + project_card.project_slug,
                "Active Project root: " + project_card.project_root,
                "Active Project root fingerprint: "
                + project_card.project_root_fingerprint,
                "Active Project support root: " + project_card.project_support_root,
                "Project selection mode: " + project_card.selection_mode.value,
                "Project selection snapshot UTC: " + project_card.updated_at_utc,
                "Project is the M-card for this audit: YES",
            )
        )
    if complete_review_sha256:
        project_identity_lines.extend(
            (
                "Complete Engineering Review SHA256: " + complete_review_sha256,
                "Complete Engineering Review catalog items: "
                + str(complete_review_item_count),
                "Complete Review evidence consumed without rerunning "
                "its 23 GUI actions: YES",
            )
        )

    lines = [
        "FULL ENGINEERING DIAGNOSTICS AI CORRECTION HANDOFF",
        "Project root: " + str(project_root),
        "Purpose: expose grouped deterministic correction context for AI review.",
        "Authority: diagnostic evidence only; exact source remains source truth.",
        "Automatic source correction: NO",
        "Executable patch included: NO",
        "EngineeringDiagnosticsStore owner changed: NO",
        "Project Symbol Atlas owner changed: NO",
        "Project Selection Registry changed: NO",
        "Freeze Memory changed: NO",
        "Tool and selected Project logical roles merged: NO",
        "Raw finding count: " + str(len(all_findings)),
        "Correction group count: " + str(correction_group_count),
        "Correction context ready: " + str(correction_ready),
        "Blocked findings: " + str(blocked),
        "Review/evidence required: " + str(review_required),
        "Raw finding duplication into this handoff: NO",
        "Report standard: Architecture Review-grade correction evidence",
        "Every capability ERROR/WARNING has a correction dossier: YES",
        "Structured correction groups include owner/scope/Freeze/source context: YES",
        "",
        *project_identity_lines,
        "",
        "COLLECTOR EXECUTION",
    ]
    for result in collector_results:
        lines.append(
            result.label
            + " | status="
            + result.status
            + " | findings="
            + str(result.finding_count)
            + " | run_id="
            + (result.run_id or "(none)")
        )
        if result.error_text:
            lines.extend(("Collector error evidence:", result.error_text.rstrip()))
    lines.extend(("",))
    lines.extend(build_capability_report_lines(project_root, capability_coverage))
    lines.extend(
        (
            "",
            "AI CORRECTION CONTRACT",
            "1. Inspect exact current source before proposing an edit.",
            "2. Respect canonical owner and Box boundaries in every correction.",
            "3. Treat frozen-path impact as a hard governance constraint.",
            "4. Use remediation guidance as advice, not executable authority.",
            "5. Run listed focused tests and validation commands after edits.",
            "6. Preserve rollback expectations and Project-specific ownership.",
            "7. Do not create another store, Symbol Atlas, or diagnostics engine.",
            "8. Do not mutate source from this report or Diagnostics itself.",
            "9. Raw findings remain available by run ID in Diagnostics history.",
            "",
            console_summary,
            "",
        )
    )
    for view, (_producer_id, groups) in zip(run_views, run_groups):
        lines.extend(_run_header_lines(view, len(groups)))
        for index, (key, findings) in enumerate(groups, start=1):
            lines.extend(
                build_correction_group_lines(
                    index,
                    view.run.producer_id,
                    key,
                    findings,
                )
            )
            lines.extend(
                build_structured_correction_dossier_lines(
                    project_root,
                    view.run.producer_id,
                    findings,
                )
            )
        lines.append("")
    return AiCorrectionReport(
        text="\n".join(lines).rstrip() + "\n",
        console_summary=console_summary,
        finding_count=len(all_findings),
        correction_group_count=correction_group_count,
        correction_ready_count=correction_ready,
        blocked_count=blocked,
        review_required_count=review_required,
        capability_surface_count=capability_coverage.total_surface_count,
        capability_error_count=capability_coverage.error_count,
        capability_warning_count=capability_coverage.warning_count,
    )
