# project-path: kanda_reasoner_app/manage_architecture/architecture_audit_external_ai.py
"""Manual external-AI handoff for read-only Audit Project evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QApplication, QMessageBox

from kanda_reasoner_app.manage_architecture.architecture_finding_dispositions import (
    active_audit_text,
)
from kanda_reasoner_app.external_ai_workflow import (
    ExternalAIWorkflowResult,
    handoff_to_selected_external_ai,
)
from kanda_reasoner_app.refactor_report_evidence import (
    build_refactor_report_evidence_text,
)
from kanda_reasoner_app.templates.floating_windows import (
    show_auto_close_action_window,
    show_error_copy_close_window,
)

__all__ = [
    "build_audit_results_text",
    "copy_audit_results",
    "handoff_audit_results_to_external_ai",
]


def build_audit_results_text(window: Any) -> str:
    """Build the exact read-only audit evidence selected by the user."""
    audit_text = active_audit_text(window)
    include_refactor = bool(window._include_refactor_report_checkbox.isChecked())
    if not include_refactor:
        return audit_text
    root_path = Path(window._root_path_edit.text().strip())
    window.statusBar().showMessage(
        "Running Refactor Report before preparing Project Audit Results..."
    )
    QApplication.processEvents()
    try:
        return audit_text + build_refactor_report_evidence_text(root_path)
    except Exception as exc:
        show_error_copy_close_window(
            window,
            title="Refactor Report evidence failed",
            message=(
                "Project Audit Results will still be prepared, but Refactor "
                "Report evidence failed:\n" + str(exc)
            ),
        )
        return (
            audit_text
            + "\n\n---\nRefactor Report Evidence\n"
            + "Unable to auto-generate compact evidence for "
            + str(root_path)
            + ":\n"
            + str(exc)
            + "\n"
        )


def copy_audit_results(window: Any) -> None:
    """Copy the selected Audit Project evidence without opening a service."""
    audit_text = build_audit_results_text(window)
    QApplication.clipboard().setText(audit_text)
    if window._include_refactor_report_checkbox.isChecked():
        window.statusBar().showMessage(
            "Copied Project Audit Results with compact Refactor Report evidence"
        )
    else:
        window.statusBar().showMessage("Copied Project Audit Results to clipboard")


def _audit_external_prompt(audit_text: str) -> str:
    """Build a strict read-only advisory request around current audit evidence."""
    return (
        "Review the following KANDA Audit Project evidence as a read-only advisory "
        "draft. Do not modify files, claim approval, change audit pass/fail, authorize "
        "a patch, write Freeze memory, or create Error Memory. Distinguish evidence "
        "from inference and identify any missing source needed before implementation.\n\n"
        "Return exactly between these markers:\n"
        "KANDA_AUDIT_EXTERNAL_REVIEW_BEGIN\n"
        "Summary:\n"
        "Highest-risk findings:\n"
        "Likely false positives:\n"
        "Missing evidence:\n"
        "Smallest safe next action:\n"
        "KANDA_AUDIT_EXTERNAL_REVIEW_END\n\n"
        "AUDIT_EVIDENCE_BEGIN\n"
        + audit_text
        + "\nAUDIT_EVIDENCE_END\n"
    )


def handoff_audit_results_to_external_ai(window: Any) -> ExternalAIWorkflowResult:
    """Copy Audit Project evidence and open the selected external assistant."""
    audit_text = build_audit_results_text(window).strip()
    if not audit_text:
        QMessageBox.information(
            window,
            "Run Project Audit first",
            "Run deterministic Project Audit before opening an external review.",
        )
        return ExternalAIWorkflowResult(
            ok=False,
            assistant_id="",
            display_name="",
            copied_characters=0,
            browser_open_requested=False,
            official_url="",
            error="AUDIT_PROJECT_RESULTS_EMPTY",
        )
    result = handoff_to_selected_external_ai(_audit_external_prompt(audit_text))
    if not result.ok:
        show_error_copy_close_window(
            window,
            title="Audit Project external handoff failed",
            message=result.error,
        )
        return result
    window.statusBar().showMessage(
        "Copied read-only Audit Project review and opened " + result.display_name
    )
    show_auto_close_action_window(
        window,
        title="External Audit review ready",
        message=(
            "The current audit evidence was copied and the official "
            + result.display_name
            + " site was opened. Paste manually. The answer remains advisory and "
            "cannot modify Project source or approval state."
        ),
    )
    return result
