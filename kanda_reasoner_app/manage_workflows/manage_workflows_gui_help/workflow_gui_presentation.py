# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_presentation.py
"""Presentation helpers for the Workflow Review window.

The helpers in this module own read-only dialogs and clipboard presentation.
Workflow execution, write confirmation, worker lifecycle, and source mutation stay
owned by ``workflow_gui_window.py``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QApplication, QMessageBox

from kanda_reasoner_app.refactor_report_evidence import (
    build_refactor_report_evidence_text,
)
from kanda_reasoner_app.templates.floating_windows import (
    show_error_copy_close_window,
)


def show_history(window: Any) -> None:
    """Show recent project roots and worker scripts for ``window``."""

    from .workflow_gui_history import get_recent_roots, get_recent_scripts

    roots = get_recent_roots()
    scripts = get_recent_scripts()
    lines: list[str] = []
    if roots:
        lines.append("Recent project roots:")
        for index, root in enumerate(roots, 1):
            lines.append(f"  {index}. {root}")
    else:
        lines.append("No recent project roots.")

    lines.append("")
    if scripts:
        lines.append("Recent worker scripts:")
        for index, script in enumerate(scripts, 1):
            lines.append(f"  {index}. {script}")
    else:
        lines.append("No recent worker scripts.")

    QMessageBox.information(window, "Session History", "\n".join(lines))


def show_mode_help(window: Any) -> None:
    """Show mode help for the worker script selected in ``window``."""

    script_name = window._current_script_path().name
    is_architecture_worker = "architecture" in script_name.lower()
    if is_architecture_worker:
        help_text = (
            "Validate\n"
            "  Checks docstrings, package declarations, EXPOSES/EXPORTS "
            "vs __all__,\n"
            "  module size, helper-group conventions, and duplicate public "
            "symbols.\n\n"
            "Diff\n"
            "  Previews changes to architecture_manifest.json, "
            "ARCHITECTURE.md,\n"
            "  and generated __init__.py facades - without writing anything.\n\n"
            "Scan\n"
            "  Prints the full architecture manifest as JSON (read-only).\n\n"
            "Write\n"
            "  Writes architecture_manifest.json, ARCHITECTURE.md, and "
            "minimal\n"
            "  __init__.py facades. Blocked if validation has errors."
        )
    else:
        help_text = (
            "Validate\n"
            "  Runs tests, runtime smoke commands, business checks, GUI "
            "flows,\n"
            "  integration commands, performance commands, and import "
            "probes.\n\n"
            "Diff\n"
            "  Previews changes to workflow_manifest.json and WORKFLOWS.md.\n\n"
            "Scan\n"
            "  Prints the generated workflow manifest template as JSON.\n\n"
            "Write\n"
            "  Writes workflow_manifest.json and WORKFLOWS.md.\n"
            "  Blocked if validation has failures."
        )

    QMessageBox.information(
        window,
        f"Mode Help - {script_name}",
        help_text,
    )


def copy_workflow_audit_to_clipboard(window: Any) -> None:
    """Copy Workflow Review output with optional refactor evidence."""

    audit_text = window._output.toPlainText()
    include_report = window._include_refactor_report_checkbox.isChecked()
    if include_report:
        root_path = window._current_root_path()
        window.statusBar().showMessage(
            "Running Refactor Report before copying Workflow Audit..."
        )
        QApplication.processEvents()
        try:
            audit_text += build_refactor_report_evidence_text(root_path)
        except Exception as exc:
            audit_text += (
                "\n\n---\n"
                "Refactor Report Evidence\n"
                f"Unable to auto-generate compact evidence for {root_path}:\n"
                f"{exc}\n"
            )
            show_error_copy_close_window(
                window,
                title="Refactor Report evidence failed",
                message=(
                    "Workflow Audit will still be copied, but Refactor "
                    f"Report evidence failed:\n{exc}"
                ),
            )

    QApplication.clipboard().setText(audit_text)
    if include_report:
        message = "Copied Workflow Audit with compact Refactor Report evidence"
    else:
        message = "Copied Workflow Audit to clipboard"
    window.statusBar().showMessage(message)


__all__ = [
    "copy_workflow_audit_to_clipboard",
    "show_history",
    "show_mode_help",
]
