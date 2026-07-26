"""Formatting helpers for the Advanced Quality Review Workbench section."""
from __future__ import annotations

from typing import Any

__all__ = [
    "format_advanced_quality_review_failure",
    "format_advanced_quality_review_outcome",
    "format_advanced_quality_review_progress",
]


def format_advanced_quality_review_progress(
    stage_states: dict[str, str],
    stage_order: tuple[str, ...],
) -> str:
    """Render all canonical stages without hiding not-yet-run dimensions."""
    lines = ["ADVANCED QUALITY REVIEW PROGRESS", ""]
    for stage in stage_order:
        state = str(stage_states.get(stage, "WAITING") or "WAITING")
        lines.append(f"{stage}: {state}")
    return "\n".join(lines)


def format_advanced_quality_review_outcome(outcome: Any) -> str:
    """Render multidimensional cross-check evidence and durable receipt."""
    report = getattr(outcome, "cross_check_report", None)
    run_record = getattr(outcome, "run_record", None)
    receipt = getattr(outcome, "persistence_receipt", None)
    decision = _enum_text(getattr(report, "quality_decision", ""))
    execution = _enum_text(getattr(run_record, "execution_status", ""))
    lines = [
        "ADVANCED QUALITY REVIEW COMPLETE",
        "",
        "Execution status: " + (execution or "<missing>"),
        "Quality decision: " + (decision or "<missing>"),
        "Analysis identity: "
        + str(getattr(outcome, "analysis_identity_hash", "") or "<missing>"),
        "Run ID: " + str(getattr(run_record, "run_id", "") or "<missing>"),
        "Evidence root: "
        + str(getattr(receipt, "run_root", "") or getattr(receipt, "run_path", "") or "<missing>"),
        "",
        "TYPED CROSS-CHECK RESULTS",
    ]
    for item in tuple(getattr(report, "rule_results", ()) or ()):
        lines.append(
            "- "
            + str(getattr(item, "rule_id", "<unknown>"))
            + ": "
            + _enum_text(getattr(item, "decision", ""))
        )
        rationale = str(getattr(item, "rationale", "") or "").strip()
        if rationale:
            lines.append("  " + rationale)
        evidence = tuple(getattr(item, "evidence_keys", ()) or ())
        for key in evidence:
            lines.append("  evidence: " + str(key))
    lines.extend(
        [
            "",
            "Authorization note:",
            "Only PASS or PASS_WITH_WARNINGS may open Preflight Backup Readiness.",
            "REVIEW_REQUIRED, BLOCKED, INDETERMINATE, cancellation, and failure stay fail-closed.",
        ]
    )
    return "\n".join(lines)


def format_advanced_quality_review_failure(diagnostic: str) -> str:
    """Render a fail-closed review failure without synthetic quality PASS."""
    return "\n".join(
        [
            "ADVANCED QUALITY REVIEW FAILED",
            "",
            str(diagnostic or "AQR_UNKNOWN_FAILURE"),
            "",
            "No quality PASS was synthesized.",
            "Preflight remains closed until a fresh review generation succeeds.",
        ]
    )


def _enum_text(value: Any) -> str:
    return str(getattr(value, "value", value) or "")
