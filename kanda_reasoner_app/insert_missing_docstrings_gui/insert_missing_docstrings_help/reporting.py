# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/reporting.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : JSONL report construction and write verification output helpers
# EXPORTS       : build_report_row, function_report_kind_and_name, result_source, result_confidence, result_generation_source, result_failure_reason, result_issues, result_review_status, result_review_action_hint, result_review_severity, write_report_jsonl, mark_report_rows_for_write_result, print_post_write_verification
# DEPENDS ON    : project_exclusion_rules.py
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""JSONL report construction and write verification output helpers."""

from __future__ import annotations

import ast
import json
from pathlib import Path

from .project_exclusion_rules import normalize_rel_path

__all__ = [
    "build_report_row",
    "function_report_kind_and_name",
    "result_source",
    "result_confidence",
    "result_generation_source",
    "result_failure_reason",
    "result_issues",
    "result_review_status",
    "result_review_action_hint",
    "result_review_severity",
    "write_report_jsonl",
    "mark_report_rows_for_write_result",
    "print_post_write_verification",
]


def _function_report_kind_and_name(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    parent_map: dict[ast.AST, ast.AST],
) -> tuple[str, str]:
    """Return report kind and display name for a function or method node."""
    parent = parent_map.get(node)
    if isinstance(parent, ast.ClassDef):
        return "method", f"{parent.name}.{node.name}"
    return "function", node.name

def _report_row(
    root: Path,
    path: Path,
    *,
    target_kind: str,
    target_name: str,
    line: int | None,
    action: str,
    reason: str = "",
    source: str = "",
    confidence: str = "",
    generation_source: str = "",
    failure_reason: str = "",
    issues: list[str] | None = None,
    review_status: str = "",
    review_action_hint: str = "",
    review_severity: str = "",
    insert_line: int | None = None,
) -> dict[str, object]:
    """Build one JSONL-safe report row for a docstring target."""
    computed_review_status = review_status or _review_status_from_values(
        generation_source,
        failure_reason,
        issues,
        action,
    )
    computed_review_action_hint = (
        review_action_hint or _review_action_hint_from_status(computed_review_status)
    )
    computed_review_severity = (
        review_severity or _review_severity_from_status(computed_review_status)
    )

    return {
        "file": normalize_rel_path(root, path),
        "target_kind": target_kind,
        "target_name": target_name,
        "line": line,
        "insert_line": insert_line,
        "action": action,
        "reason": reason,
        "source": source,
        "confidence": confidence,
        "generation_source": generation_source,
        "failure_reason": failure_reason,
        "issues": list(issues or []),
        "review_status": computed_review_status,
        "review_action_hint": computed_review_action_hint,
        "review_severity": computed_review_severity,
    }

def _result_source(result: object) -> str:
    """Return a generation source label from a generation result."""
    return str(getattr(result, "source", "") or "ai")

def _result_confidence(result: object) -> str:
    """Return a confidence label from a generation result."""
    return str(getattr(result, "confidence", "") or "")


def _result_generation_source(result: object) -> str:
    """Return the detailed generation path for a generation result."""
    value = str(getattr(result, "generation_source", "") or "")
    return value or _result_source(result)


def _result_failure_reason(result: object) -> str:
    """Return why AI output was skipped, rejected, or downgraded."""
    return str(getattr(result, "failure_reason", "") or "none")


def _result_issues(result: object) -> list[str]:
    """Return generation or validation issues from a generation result."""
    issues = getattr(result, "issues", [])
    if not isinstance(issues, list):
        return [str(issues)] if issues else []
    return [str(item) for item in issues]



_REVIEW_FAILURE_REASONS = {
    "ai_call_failed",
    "model_invalid_json",
    "quality_rejected",
    "structured_render_error",
    "unsupported_ai_claim",
    "validation_rejected",
}


def _canonical_failure_reason(value: object) -> str:
    """Return a normalized failure reason label for review display."""
    text = str(value or "").strip().lower()
    if not text or text == "none":
        return "none"
    return text


def _review_status_from_values(
    generation_source: object,
    failure_reason: object,
    issues: object,
    action: object = "",
) -> str:
    """Return a compact review status from report-row evidence."""
    source = str(generation_source or "").strip().lower()
    failure = _canonical_failure_reason(failure_reason)
    has_issues = bool(issues)
    action_text = str(action or "").strip().lower()

    if failure == "private_symbol_skipped" or source == "skipped_private":
        return "skipped_private"
    if source in {"heuristic", "heuristic_fallback"}:
        return "fallback_review_required"
    if failure in _REVIEW_FAILURE_REASONS or has_issues:
        return "fallback_review_required"
    if failure != "none":
        return "blocked_or_rejected"
    if source in {"ai", "local_ai", "structured_ai"}:
        return "ready_for_review"
    if action_text in {"inserted", "would_insert", "would_update"}:
        return "ready_for_review"
    return "not_applicable"


def _review_action_hint_from_status(status: str) -> str:
    """Return a human-readable review action for a review status."""
    if status == "ready_for_review":
        return "Review AI-generated docstring against source evidence before insertion."
    if status == "fallback_review_required":
        return "Review fallback docstring carefully because AI output failed or was rejected."
    if status == "skipped_private":
        return "Private symbol was skipped by policy; review only if private docstrings are in scope."
    if status == "blocked_or_rejected":
        return "Do not insert until the reported generation failure is resolved."
    return "No generated docstring review action is required for this row."


def _review_severity_from_status(status: str) -> str:
    """Return a simple severity label for GUI and report review surfaces."""
    if status == "fallback_review_required":
        return "warning"
    if status == "blocked_or_rejected":
        return "error"
    return "info"


def _result_review_status(result: object) -> str:
    """Return a review status for a generated docstring result."""
    return _review_status_from_values(
        _result_generation_source(result),
        _result_failure_reason(result),
        _result_issues(result),
    )


def _result_review_action_hint(result: object) -> str:
    """Return the review action hint for a generated docstring result."""
    return _review_action_hint_from_status(_result_review_status(result))


def _result_review_severity(result: object) -> str:
    """Return the review severity for a generated docstring result."""
    return _review_severity_from_status(_result_review_status(result))

def write_report_jsonl(
    report_path: str | None,
    rows: list[dict[str, object]],
    *,
    root: Path,
    mode: str,
) -> None:
    """Write JSONL report rows for scan, diff, or write review."""
    if not report_path:
        return

    path = Path(report_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized_rows: list[dict[str, object]] = []
    for row in rows:
        item = dict(row)
        item["project_root"] = str(root)
        item["mode"] = mode
        normalized_rows.append(item)

    content = "\n".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True)
        for row in normalized_rows
    )
    if content:
        content += "\n"
    path.write_text(content, encoding="utf-8")

def _mark_report_rows_for_write_result(
    report_rows: list[dict[str, object]],
    written_paths: set[Path],
    *,
    root: Path,
) -> None:
    """Mark inserted report rows according to actual write completion."""
    written_rel_paths = {
        normalize_rel_path(root, path)
        for path in written_paths
    }

    for row in report_rows:
        if row.get("action") != "inserted":
            continue

        file_path = str(row.get("file", "") or "")
        if file_path in written_rel_paths:
            row["write_state"] = "written"
        else:
            row["write_state"] = "not_written"

def _print_post_write_verification(summary: dict[str, object]) -> None:
    """Print a compact post-write verification summary."""
    remaining_count = int(summary.get("files_with_missing_docstrings", 0) or 0)
    target_count = int(summary.get("remaining_insertable_targets", 0) or 0)

    if remaining_count == 0 and target_count == 0:
        print("Post-write verification: passed. No missing docstrings remain in scope.")
        return

    print(
        "Post-write verification: remaining missing docstrings found "
        f"({remaining_count} file(s), {target_count} target(s))."
    )

    remaining_files = summary.get("remaining_files", [])
    if isinstance(remaining_files, list):
        for file_path in remaining_files[:25]:
            print(f"REMAINING {file_path}")
        if len(remaining_files) > 25:
            print(f"REMAINING ... {len(remaining_files) - 25} more file(s)")

    skipped = summary.get("skipped", [])
    if isinstance(skipped, list):
        for message in skipped[:25]:
            print(f"VERIFY-SKIPPED {message}")
        if len(skipped) > 25:
            print(f"VERIFY-SKIPPED ... {len(skipped) - 25} more item(s)")


# Public aliases keep helper exports explicit while preserving the original implementation names.
function_report_kind_and_name = _function_report_kind_and_name
build_report_row = _report_row
result_source = _result_source
result_confidence = _result_confidence
result_generation_source = _result_generation_source
result_failure_reason = _result_failure_reason
result_issues = _result_issues
result_review_status = _result_review_status
result_review_action_hint = _result_review_action_hint
result_review_severity = _result_review_severity
mark_report_rows_for_write_result = _mark_report_rows_for_write_result
print_post_write_verification = _print_post_write_verification
