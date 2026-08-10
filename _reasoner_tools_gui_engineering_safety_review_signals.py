# project-path: _reasoner_tools_gui_engineering_safety_review_signals.py
"""Private result classification for Complete Engineering Review signals."""

from __future__ import annotations

from dataclasses import dataclass
import re

__all__ = [
    "ASSESSMENT_CLEAN",
    "ASSESSMENT_DEGRADED",
    "ASSESSMENT_DRAFT",
    "ASSESSMENT_FAILED",
    "ASSESSMENT_INVALID_COVERAGE",
    "ASSESSMENT_MANUAL_REVIEW_REQUIRED",
    "ASSESSMENT_MISSING_EVIDENCE",
    "ASSESSMENT_NOT_RUN",
    "ASSESSMENT_PASS_WITH_FINDINGS",
    "EngineeringReviewSignal",
    "classify_engineering_review_signal",
]

ASSESSMENT_CLEAN = "CLEAN"
ASSESSMENT_PASS_WITH_FINDINGS = "PASS_WITH_FINDINGS"
ASSESSMENT_DEGRADED = "DEGRADED"
ASSESSMENT_INVALID_COVERAGE = "INVALID_COVERAGE"
ASSESSMENT_MISSING_EVIDENCE = "MISSING_EVIDENCE"
ASSESSMENT_DRAFT = "DRAFT"
ASSESSMENT_NOT_RUN = "NOT_RUN"
ASSESSMENT_MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
ASSESSMENT_FAILED = "FAILED"

_SOURCE_HYGIENE_COMMANDS = frozenset(
    {
        "bom-scan",
        "ruff-quality",
        "shadow-audit",
        "shadow-plan",
        "facade-fix-plan",
    }
)
_DRAFT_COMMANDS = frozenset(
    {
        "risk-radar",
        "crash-triage",
        "refactor-playbook",
        "release-notes",
        "api-contract",
        "property-test",
    }
)
_SYMBOL_QUERY_COMMANDS = frozenset(
    {
        "find-symbol",
        "find-owner",
        "facade-owner",
        "main-helpers",
        "related-files",
        "pre-patch-gate",
    }
)


@dataclass(frozen=True)
class EngineeringReviewSignal:
    """Decision-quality assessment independent from command execution status."""

    assessment: str
    reason: str
    finding_count: int | None = None
    files_scanned: int | None = None


def classify_engineering_review_signal(
    command_name: str,
    status_code: int,
    stdout: str,
    stderr: str = "",
) -> EngineeringReviewSignal:
    """Classify one command result without redefining its process exit code."""
    command = str(command_name or "").strip().casefold()
    output = "\n".join((str(stdout or ""), str(stderr or ""))).strip()
    lowered = output.casefold()

    if int(status_code) != 0:
        return EngineeringReviewSignal(
            ASSESSMENT_FAILED,
            "Command execution returned a non-zero status.",
        )

    if "project_context_unavailable:" in lowered:
        return EngineeringReviewSignal(
            ASSESSMENT_NOT_RUN,
            "No safe Project-owned target was available; Tool fallback was blocked.",
        )

    finding_count = _first_int(
        output,
        (
            r"(?im)^finding count:\s*(\d+)\s*$",
            r"(?i)(?:^|[;\s])findings=(\d+)(?:[.;\s]|$)",
        ),
    )
    files_scanned = _first_int(
        output,
        (r"(?i)(?:^|[;\s])files_scanned=(\d+)(?:[.;\s]|$)",),
    )

    if command == "bom-scan":
        if files_scanned is None or files_scanned <= 0:
            return EngineeringReviewSignal(
                ASSESSMENT_INVALID_COVERAGE,
                "BOM scan did not examine any files.",
                finding_count=finding_count,
                files_scanned=files_scanned,
            )
        return _finding_signal(
            finding_count,
            files_scanned,
            clean_reason="BOM scan covered active text files with no findings.",
            finding_reason="BOM scan completed with source-hygiene findings.",
        )

    if command == "ruff-quality":
        if _contains_any(
            lowered,
            (
                "ruff quality check was blocked",
                "ruff_quality_blocked",
                "ruff_lint_execution_failed",
                "ruff_format_execution_failed",
            ),
        ):
            return EngineeringReviewSignal(
                ASSESSMENT_DEGRADED,
                "Ruff execution evidence was blocked or incomplete.",
                finding_count=finding_count,
            )
        format_status = _first_int(
            output,
            (r"(?i)(?:^|[;\s])format_status=(-?\d+)(?:[.;\s]|$)",),
        )
        lint_status = _first_int(
            output,
            (r"(?i)(?:^|[;\s])lint_status=(-?\d+)(?:[.;\s]|$)",),
        )
        if lint_status not in (None, 0) or format_status not in (None, 0, 1):
            return EngineeringReviewSignal(
                ASSESSMENT_DEGRADED,
                "Ruff process status invalidated complete quality evidence.",
                finding_count=finding_count,
            )
        if (finding_count or 0) > 0 or format_status == 1:
            return EngineeringReviewSignal(
                ASSESSMENT_PASS_WITH_FINDINGS,
                "Read-only Ruff checks completed and reported quality debt.",
                finding_count=finding_count,
            )
        return EngineeringReviewSignal(
            ASSESSMENT_CLEAN,
            "Read-only Ruff lint and format checks completed cleanly.",
            finding_count=finding_count,
        )

    if command in {"shadow-audit", "shadow-plan"}:
        if files_scanned is not None and files_scanned <= 0:
            return EngineeringReviewSignal(
                ASSESSMENT_INVALID_COVERAGE,
                "Shadow analysis did not examine active Python files.",
                finding_count=finding_count,
                files_scanned=files_scanned,
            )
        return _finding_signal(
            finding_count,
            files_scanned,
            clean_reason="Shadow analysis completed with no active-scope findings.",
            finding_reason="Shadow analysis completed with active-scope findings.",
        )

    if command == "facade-fix-plan":
        return _finding_signal(
            finding_count,
            files_scanned,
            clean_reason="No safe active-scope facade fix candidates were found.",
            finding_reason="Safe active-scope facade fix candidates require review.",
        )

    if command in _DRAFT_COMMANDS:
        if command == "release-notes" and "status: draft" in lowered:
            return EngineeringReviewSignal(
                ASSESSMENT_DRAFT,
                "Release notes are explicitly marked as draft.",
            )
        if command in {"api-contract", "property-test"}:
            return EngineeringReviewSignal(
                ASSESSMENT_DRAFT,
                "The command produces draft guidance, not a completed validation.",
            )
        if _contains_any(
            lowered,
            (
                "human decision: pending",
                "validation status: not_run",
                "validation status: not run",
            ),
        ):
            return EngineeringReviewSignal(
                ASSESSMENT_DRAFT,
                "Advisory report still requires human decision or validation.",
            )

    if command == "push-plan":
        if _contains_any(
            lowered,
            (
                "overall status: unknown",
                "no check results were supplied",
            ),
        ):
            return EngineeringReviewSignal(
                ASSESSMENT_NOT_RUN,
                "Push validation commands were listed but no check results ran.",
            )
        if "overall status: failed" in lowered:
            return EngineeringReviewSignal(
                ASSESSMENT_FAILED,
                "One or more supplied push validation results failed.",
            )
        return EngineeringReviewSignal(
            ASSESSMENT_CLEAN,
            "Supplied push validation results completed without failure markers.",
        )

    if command == "evidence-freshness":
        freshness_status = _status_value(
            output,
            "evidence freshness status",
        )
        if freshness_status == "missing_evidence":
            return EngineeringReviewSignal(
                ASSESSMENT_MISSING_EVIDENCE,
                "Canonical Project Analysis Evidence is missing.",
            )
        if freshness_status in {
            "invalid_evidence",
            "wrong_project",
            "stale",
            "probably_stale",
        }:
            return EngineeringReviewSignal(
                ASSESSMENT_DEGRADED,
                "Project Analysis Evidence is not current and canonical.",
            )
        if freshness_status:
            return EngineeringReviewSignal(
                ASSESSMENT_CLEAN,
                "Project Analysis Evidence freshness is acceptable.",
            )
        return EngineeringReviewSignal(
            ASSESSMENT_DEGRADED,
            "Evidence freshness status could not be determined.",
        )

    if command in _SYMBOL_QUERY_COMMANDS:
        if _contains_inactive_reference_path(lowered):
            return EngineeringReviewSignal(
                ASSESSMENT_DEGRADED,
                (
                    "Inactive reference paths leaked into an active-scope "
                    "Symbol Atlas result."
                ),
            )
        if _contains_any(
            lowered,
            (
                "status=needs_owner_review",
                "pre_patch_status=facade_patch_risk",
            ),
        ):
            reason = "Symbol ownership or facade risk requires a human decision."
            if "missing_evidence" in lowered:
                reason += " Canonical JSON evidence is also missing."
            return EngineeringReviewSignal(
                ASSESSMENT_MANUAL_REVIEW_REQUIRED,
                reason,
            )
        if "missing_evidence" in lowered:
            return EngineeringReviewSignal(
                ASSESSMENT_MISSING_EVIDENCE,
                "Symbol query ran without canonical JSON evidence.",
            )
        if _contains_any(
            lowered,
            (
                "status=no_matches",
                "confidence=low",
                "merge status: live_only",
                "merge_status: live_only",
            ),
        ):
            return EngineeringReviewSignal(
                ASSESSMENT_DEGRADED,
                "Symbol query result is low-confidence or live-only.",
            )
        return EngineeringReviewSignal(
            ASSESSMENT_CLEAN,
            "Symbol query returned a resolved result without degradation markers.",
        )

    if command == "atlas-report":
        report_count = _line_int(output, "Report count")
        written_count = _line_int(output, "Written report count")
        if (
            "status: written" in lowered
            and report_count is not None
            and report_count > 0
            and report_count == written_count
        ):
            return EngineeringReviewSignal(
                ASSESSMENT_CLEAN,
                "All requested Project Symbol Atlas reports were written.",
            )
        return EngineeringReviewSignal(
            ASSESSMENT_DEGRADED,
            "Project Symbol Atlas report generation was incomplete or ambiguous.",
        )

    if command in _SOURCE_HYGIENE_COMMANDS:
        return _finding_signal(
            finding_count,
            files_scanned,
            clean_reason="Source-hygiene command completed with no findings.",
            finding_reason="Source-hygiene command completed with findings.",
        )

    if not output:
        return EngineeringReviewSignal(
            ASSESSMENT_DEGRADED,
            "Command completed without decision evidence.",
        )
    if "draft only" in lowered or lowered.startswith("# ") and " draft" in lowered:
        return EngineeringReviewSignal(
            ASSESSMENT_DRAFT,
            "Output is explicitly a draft artifact.",
        )
    if "missing_evidence" in lowered:
        return EngineeringReviewSignal(
            ASSESSMENT_MISSING_EVIDENCE,
            "Output reports missing canonical evidence.",
        )
    if "not_run" in lowered or "not run" in lowered:
        return EngineeringReviewSignal(
            ASSESSMENT_NOT_RUN,
            "Output reports that validation was not run.",
        )
    if (finding_count or 0) > 0:
        return EngineeringReviewSignal(
            ASSESSMENT_PASS_WITH_FINDINGS,
            "Command completed with findings requiring review.",
            finding_count=finding_count,
            files_scanned=files_scanned,
        )
    return EngineeringReviewSignal(
        ASSESSMENT_CLEAN,
        "Command completed with sufficient clean decision evidence.",
        finding_count=finding_count,
        files_scanned=files_scanned,
    )


def _finding_signal(
    finding_count: int | None,
    files_scanned: int | None,
    *,
    clean_reason: str,
    finding_reason: str,
) -> EngineeringReviewSignal:
    if (finding_count or 0) > 0:
        return EngineeringReviewSignal(
            ASSESSMENT_PASS_WITH_FINDINGS,
            finding_reason,
            finding_count=finding_count,
            files_scanned=files_scanned,
        )
    return EngineeringReviewSignal(
        ASSESSMENT_CLEAN,
        clean_reason,
        finding_count=finding_count,
        files_scanned=files_scanned,
    )


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def _contains_inactive_reference_path(text: str) -> bool:
    normalized = str(text or "").replace("\\\\", "/").replace("\\", "/")
    markers = (
        ".project_reference/",
        "_project_reference/",
        "project_freeze_ledger/",
    )
    return any(marker in normalized for marker in markers)


def _first_int(text: str, patterns: tuple[str, ...]) -> int | None:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match is not None:
            try:
                return int(match.group(1))
            except (TypeError, ValueError):
                continue
    return None


def _line_int(text: str, label: str) -> int | None:
    return _first_int(
        text,
        (rf"(?im)^{re.escape(label)}:\s*(\d+)\s*$",),
    )


def _status_value(text: str, label: str) -> str:
    match = re.search(
        rf"(?i){re.escape(label)}=([a-z0-9_\-]+)",
        text,
    )
    if match is None:
        return ""
    return match.group(1).casefold()
