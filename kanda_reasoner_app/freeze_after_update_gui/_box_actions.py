# project-path: kanda_reasoner_app/freeze_after_update_gui/_box_actions.py
"""Box status, staged action, and log methods for the Freeze tab."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QMessageBox

from kanda_reasoner_app.freeze_after_update.contract import (
    ensure_freeze_after_update_box,
    generate_freeze_after_update_ai_files,
    inspect_freeze_after_update_box,
    refresh_freeze_exposure,
)
from kanda_reasoner_app.freeze_after_update.paths import build_paths
from kanda_reasoner_app.freeze_after_update.result import FreezeAfterUpdateResult
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

__all__ = ["FreezeBoxActionsMixin"]


class FreezeBoxActionsMixin:
    """Status, log, and staged freeze/AI-compliance action behavior."""

    def _append_log(self, message: str) -> None:
        """Support append log behavior.
        
        Parameters
        ----------
        message : str
            The message text.
        """
        
        self.output_log.append(message)

    def _append_log_block(self, text: str) -> None:
        """Append a plain-text block to the visible log without HTML rendering."""
        block = str(text or "").rstrip()
        if not block:
            return
        current = self.output_log.toPlainText().rstrip()
        combined = (current + "\n" if current else "") + block + "\n"
        self.output_log.setPlainText(combined)
        self.output_log.moveCursor(QTextCursor.MoveOperation.End)

    def _show_result(self, result: FreezeAfterUpdateResult) -> None:
        """Support show result behavior.
        
        Parameters
        ----------
        result : FreezeAfterUpdateResult
            The result value.
        """
        
        status_text = f"{result.status.value}: {result.message}"
        self.status_label.setText(status_text)
        self._append_log(status_text)
        if result.box_root is not None:
            self.box_folder_button.setToolTip("Open box folder: " + str(result.box_root))
            self.external_ai_review_folder_button.setToolTip(
                "Open external AI review folder: " + str(result.box_root / "files_to_send_ai")
            )
        if result.missing_paths:
            self._append_log("Missing paths:")
            for path in result.missing_paths:
                self._append_log(f"- {path}")
        if result.created_paths:
            self._append_log("Created paths:")
            for path in result.created_paths:
                self._append_log(f"- {path}")
        if result.output_zip is not None:
            self._last_output_folder = result.output_zip.parent
            self.external_ai_review_folder_button.setToolTip(
                "Open external AI review folder: " + str(result.output_zip.parent)
            )
            self._append_log(f"ZIP created: {result.output_zip}")
        if result.output_instruction is not None:
            self._last_output_folder = result.output_instruction.parent
            self.external_ai_review_folder_button.setToolTip(
                "Open external AI review folder: " + str(result.output_instruction.parent)
            )
            self._append_log(f"Instruction file created: {result.output_instruction}")
        if result.freeze_count:
            self._append_log(f"Freeze entries included: {result.freeze_count}")
        else:
            self._append_log("Freeze entries included: 0")

    def _check_box_status(self) -> None:
        """Support check box status behavior.
        """
        
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(inspect_freeze_after_update_box(project_root))

    def _create_or_repair_box(self) -> None:
        """Support create or repair box behavior.
        """
        
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(ensure_freeze_after_update_box(project_root))

    def _generate_files(self) -> None:
        """Support generate files behavior.
        """
        
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(generate_freeze_after_update_ai_files(project_root))

    def _set_pending_staged_action(self, project_root: Path | None, action: str | None) -> None:
        """Support set pending staged action behavior.
        
        Parameters
        ----------
        project_root : Path | None
            The project root path.
        action : str | None
            The action value.
        """
        
        self._pending_staged_project_root = project_root
        self._pending_staged_action = action
        has_pending = project_root is not None and action is not None
        self.do_staged_action_button.setEnabled(has_pending)
        self.undo_staged_action_button.setEnabled(has_pending)

    def _prepare_staged_freeze_action(self) -> None:
        """Support prepare staged freeze action behavior.
        """
        
        project_root = self._require_project_root()
        if project_root is None:
            return
        paths = build_paths(project_root)
        exposure = refresh_freeze_exposure(project_root)
        exposure_status = exposure.get("status") or "UNKNOWN"
        exposure_warnings = exposure.get("warnings") or []
        exposure_errors = exposure.get("errors") or []
        self.output_log.clear()
        self.status_label.setText(
            "Prepared staged freeze / AI compliance action. Review log, then choose Do it or Undo / Cancel."
        )
        self._append_log("STAGED ACTION PREVIEW")
        self._append_log("")
        self._append_log("Action: refresh Freeze Feature After Update AI compliance package")
        self._append_log(f"Active project: {paths.project_root}")
        self._append_log(f"Current freeze exposure status: {exposure_status}")
        if exposure_warnings:
            self._append_log("Warnings from current freeze exposure:")
            for warning in exposure_warnings:
                self._append_log(f"- {warning}")
        if exposure_errors:
            self._append_log("Current freeze exposure errors:")
            for error in exposure_errors:
                self._append_log(f"- {error}")
        self._append_log("")
        self._append_log("WILL READ:")
        self._append_log(f"- {paths.memory_root}")
        self._append_log(f"- {paths.freeze_index}")
        self._append_log(f"- {paths.frozen_steps}")
        self._append_log(f"- {paths.entries_root}")
        self._append_log("")
        self._append_log("WILL WRITE / REFRESH:")
        self._append_log(f"- {paths.send_root}")
        self._append_log("- fresh freeze_feature_ai_send_pack_*.zip")
        self._append_log(f"- {paths.what_to_say}")
        self._append_log("- AI startup-readable freeze/compliance instructions generated from active project memory")
        self._append_log("")
        self._append_log("WILL NOT WRITE:")
        self._append_log("- project_freeze_ledger as project-specific memory")
        self._append_log("- other project roots")
        self._append_log("- temporary files in the project root")
        self._append_log("- frozen_features_memory entries, freeze_index.json, or project_frozen_implemented_steps.md")
        self._append_log("")
        self._append_log("No files have been changed yet.")
        self._append_log("Choose Do it to perform this action once, or Undo / Cancel to discard it.")
        self._set_pending_staged_action(project_root, "refresh_ai_compliance_package")

    def _do_staged_freeze_action(self) -> None:
        """Support do staged freeze action behavior.
        """
        
        if self._pending_staged_project_root is None or self._pending_staged_action is None:
            QMessageBox.warning(self, "No staged action", "Prepare a staged action first.")
            return
        project_root = self._pending_staged_project_root
        action = self._pending_staged_action
        self._set_pending_staged_action(None, None)
        if action != "refresh_ai_compliance_package":
            show_error_copy_close_window(self, title="Unknown staged action", message=f"Unknown staged action: {action}")
            return
        self._append_log("")
        self._append_log("DO IT selected. Executing staged freeze / AI compliance action...")
        result = generate_freeze_after_update_ai_files(project_root)
        self._show_result(result)
        if result.ok:
            self._append_log("AI compliance package is ready for this project.")
            self._append_log(
                "Use it in the next AI interaction, or continue with local freeze writing when that workflow is available in the tab."
            )

    def _undo_staged_freeze_action(self) -> None:
        """Support undo staged freeze action behavior.
        """
        
        if self._pending_staged_project_root is None:
            self._append_log("No staged action to cancel.")
            self.do_staged_action_button.setEnabled(False)
            self.undo_staged_action_button.setEnabled(False)
            return
        cancelled_root = self._pending_staged_project_root
        self._set_pending_staged_action(None, None)
        self.status_label.setText("Staged action cancelled. No files were changed.")
        self._append_log("")
        self._append_log("UNDO / CANCEL selected.")
        self._append_log(f"Cancelled staged action for: {cancelled_root}")
        self._append_log("No files were changed.")
