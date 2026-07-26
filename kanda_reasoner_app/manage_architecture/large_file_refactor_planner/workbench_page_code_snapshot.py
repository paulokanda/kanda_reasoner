"""Read-only text aggregation for the Workbench Page Code snapshot."""

from __future__ import annotations

from typing import Any


__all__ = ["build_workbench_page_code_text"]


_STAGE_SPECS = (
    (
        "1. Plan Intake from Large File Refactor Planner",
        "Public Planner handoff captured through workbench_snapshot_bridge and then owned as an immutable Workbench plan snapshot.",
        (("Plan Intake", "_large_file_refactor_workbench_intake_output"),),
    ),
    (
        "2. Dependency and Scope Readiness",
        "Workbench-owned Plan Intake evidence analyzed by workbench_dependency_readiness. This stage reads scope and dependency facts without mutating source.",
        (("Dependency Readiness", "_large_file_refactor_workbench_dependency_output"),),
    ),
    (
        "3. Real Moved-Code Preview Generation",
        "Workbench-owned plan, intake, and dependency readiness passed to the LibCST real preview writer. Output authority remains Project Support preview artifacts, not canonical source.",
        (("Real Preview", "_large_file_refactor_workbench_real_preview_output"),),
    ),
    (
        "4. Structural Validation",
        "Current Workbench plan and governed Real Preview passed to the structural validator and import-migration preview checks. Validation evidence does not write canonical source.",
        (("Structural Validation", "_large_file_refactor_workbench_validation_output"),),
    ),
    (
        "5. Advanced Quality Review",
        "Sealed baseline and Preview analysis views reviewed through the pinned five-analyzer environment, pure orchestration service, typed cross-check rules, and Project-owned immutable evidence store.",
        (
            ("AQR Progress", "_large_file_refactor_workbench_aqr_progress_output"),
            ("AQR Result", "_large_file_refactor_workbench_aqr_output"),
        ),
    ),
    (
        "6. Preflight Backup and Source Payload",
        "Structural and AQR-ready evidence feeds preflight backup readiness, then the exact source apply payload builder. These outputs prepare governed evidence and payloads without applying source changes.",
        (
            ("Preflight Backup Readiness", "_large_file_refactor_workbench_preflight_output"),
            ("Source Apply Payload", "_large_file_refactor_workbench_source_payload_output"),
        ),
    ),
    (
        "7. Completion Review and Refactor Authorization",
        "Completion evidence combines the Workbench snapshot, Preview, preflight, payload, review evidence, optional advisory review routes, external AI exchange state, transaction summary, and final authorization gate.",
        (
            ("Completion Status", "_large_file_refactor_workbench_completion_status_output"),
            ("Semantic Diff", "_large_file_refactor_workbench_semantic_diff_output"),
            ("Text Diff", "_large_file_refactor_workbench_text_diff_output"),
            ("Assisted Diff Review", "_large_file_refactor_workbench_diff_review_status_output"),
            ("External AI Candidate Exchange", "_large_file_refactor_workbench_ai_exchange_output"),
            ("Final Transaction Summary", "_large_file_refactor_workbench_transaction_summary_output"),
            ("Refactor Authorization Gate", "_large_file_refactor_workbench_refactor_gate_output"),
        ),
    ),
)


def build_workbench_page_code_text(window: object) -> str:
    """Return one read-only text snapshot of all current Workbench text outputs."""
    rows = [
        "Large File Refactor Workbench - Page Code",
        "",
        "Snapshot type: read-only aggregation of current Workbench text windows.",
        "Effect: does not execute stages, change gates, write source, or mutate Project Support evidence.",
        "Active project root: " + _active_project_root(window),
        "Workbench state: "
        + str(getattr(window, "_large_file_refactor_workbench_state", "UNKNOWN")),
    ]

    for title, origin, outputs in _STAGE_SPECS:
        rows.extend(("", "=" * 78, title, "Origin: " + origin))
        for output_label, attribute in outputs:
            rows.extend(
                (
                    "",
                    "Text window - " + output_label + ":",
                    _widget_text(window, attribute),
                )
            )

    return "\n".join(rows).rstrip() + "\n"


def _widget_text(window: object, attribute: str) -> str:
    """Read one text widget without assuming it exists during partial fixtures."""
    widget: Any = getattr(window, attribute, None)
    if widget is None:
        return "<text window not available in this page instance>"
    reader = getattr(widget, "toPlainText", None)
    if not callable(reader):
        return "<widget does not expose plain text>"
    text = str(reader()).strip()
    return text or "<empty text window>"


def _active_project_root(window: object) -> str:
    """Read the active project root without importing the Workbench shell."""
    edit: Any = getattr(window, "_root_path_edit", None)
    reader = getattr(edit, "text", None)
    if not callable(reader):
        return "<active project root unavailable>"
    text = str(reader()).strip()
    return text or "<active project root empty>"
