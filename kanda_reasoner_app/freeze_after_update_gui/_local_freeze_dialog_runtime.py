# project-path: kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py
"""Human-authority runtime for one local Freeze Entry dialog."""

from __future__ import annotations

import json
from typing import Any, Mapping

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from kanda_reasoner_app.freeze_after_update.contract import (
    preview_freeze_entry,
    refresh_ai_compliance_context,
    validate_freeze_entry_preview,
    write_confirmed_freeze_entry,
)
from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import (
    parse_ai_formulary_response,
)
from kanda_reasoner_app.freeze_after_update_gui._freeze_formulary_ai_runtime import (
    FreezeFormularyAIController,
)
from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_widgets import (
    build_local_freeze_dialog_widgets,
)
from kanda_reasoner_app.freeze_after_update_gui.local_freeze_confirmation_binding import (
    FreezeActionStateController,
    apply_freeze_form_inputs,
    bind_freeze_confirmation_invalidation,
    build_freeze_confirmation_binding,
    collect_freeze_form_inputs,
    freeze_confirmation_binding_matches,
    render_freeze_findings,
)
from kanda_reasoner_app.freeze_after_update_gui.local_freeze_preview_log import (
    build_local_freeze_preview_log_text,
)
from kanda_reasoner_app.freeze_hint_intake import mark_latest_freeze_hint_used
from kanda_reasoner_app.templates.floating_windows import (
    show_auto_close_action_window,
    show_error_copy_close_window,
)

__all__ = ["FreezeLocalEntryRuntimeMixin"]

FREEZE_CONFIRM_ENABLED_STYLE = "color: #008000; font-weight: bold;"
FREEZE_IGNORE_ENABLED_STYLE = "color: #B00020; font-weight: bold;"
FREEZE_DISABLED_ACTION_STYLE = "color: #808080; font-weight: bold;"


class FreezeLocalEntryRuntimeMixin:
    """Keep Preview, Confirm, Write, ignore, and external review human-owned."""

    def _open_local_freeze_entry_dialog(self) -> None:
        """Open one single-instance Freeze Entry formulary."""
        if self._raise_existing_local_freeze_dialog():
            return
        project_root = self._require_project_root()
        if project_root is None:
            return
        widgets = build_local_freeze_dialog_widgets(
            self, disabled_action_style=FREEZE_DISABLED_ACTION_STYLE
        )
        dialog = widgets.dialog
        self._local_freeze_preview = None
        confirmation_binding: dict[str, str] | None = None
        applying_inputs = False

        action_state = FreezeActionStateController(
            confirm_button=widgets.confirm_write_button,
            ignore_button=widgets.ignore_freeze_button,
            confirm_enabled_style=FREEZE_CONFIRM_ENABLED_STYLE,
            ignore_enabled_style=FREEZE_IGNORE_ENABLED_STYLE,
            disabled_style=FREEZE_DISABLED_ACTION_STYLE,
        )
        action_state.disable("No writable freeze preview has been generated yet.")

        def collect_inputs() -> dict[str, str]:
            return collect_freeze_form_inputs(widgets)

        def apply_inputs(inputs: Mapping[str, Any]) -> None:
            nonlocal applying_inputs
            applying_inputs = True
            try:
                apply_freeze_form_inputs(widgets, inputs)
            finally:
                applying_inputs = False

        def preview_local_freeze() -> None:
            nonlocal confirmation_binding
            self._local_freeze_preview = None
            confirmation_binding = None
            action_state.disable("Preview is being rebuilt.")
            inputs = collect_inputs()
            result = preview_freeze_entry(project_root, inputs)
            self._local_freeze_preview = result if result.get("ok") else None
            markdown = result.get("markdown") or ""
            widgets.preview_text_edit.setPlainText(
                render_freeze_findings(result) + markdown
            )
            validation_result = None
            if result.get("ok") and result.get("is_writable"):
                validation_result = validate_freeze_entry_preview(project_root, result)
                if validation_result.get("ok"):
                    confirmation_binding = build_freeze_confirmation_binding(
                        project_root, inputs
                    )
                    action_state.set_state(True, True)
                    self.status_label.setText(
                        "Local freeze preview ready. Review it, then confirm if correct."
                    )
                    self._append_log(
                        "Local freeze entry preview is ready and writable. No files were written."
                    )
                else:
                    self._local_freeze_preview = None
                    action_state.disable(
                        "Freeze preview validation blocked writing. Fix errors before confirming."
                    )
                    widgets.preview_text_edit.setPlainText(
                        render_freeze_findings(validation_result) + markdown
                    )
                    self._append_log(
                        "Local freeze preview was generated but validation blocked writing."
                    )
            else:
                action_state.disable(
                    "No writable freeze entry is available. Fix required fields or validation evidence."
                )
                self._append_log("Local freeze preview is not writable.")
            self._append_log_block(
                build_local_freeze_preview_log_text(result, validation_result)
            )

        ai_runtime = FreezeFormularyAIController(
            owner=self,
            dialog=dialog,
            widgets=widgets,
            project_root=project_root,
            action_state=action_state,
            collect_inputs=collect_inputs,
            apply_inputs=apply_inputs,
            preview_callback=preview_local_freeze,
        )

        def invalidate_current_confirmation(*_args: object) -> None:
            nonlocal confirmation_binding
            if applying_inputs:
                return
            if self._local_freeze_preview is not None or confirmation_binding is not None:
                self._local_freeze_preview = None
                confirmation_binding = None
                widgets.preview_text_edit.clear()
                action_state.disable(
                    "The form or selected project changed after Preview. Preview again."
                )
            ai_runtime.invalidate(
                "The Project or form changed; pending AI result discarded."
            )

        bind_freeze_confirmation_invalidation(
            widgets, self.project_root_edit, invalidate_current_confirmation
        )

        def copy_formulary_to_ai() -> None:
            current_json = json.dumps(collect_inputs(), ensure_ascii=False, indent=2)
            prompt = (
                "Review this KANDA Freeze formulary for the current validated feature only. "
                "Return one JSON object between KANDA_FREEZE_FORM_JSON_BEGIN and "
                "KANDA_FREEZE_FORM_JSON_END. Do not invent evidence. Preserve every "
                "validated file, protected path, rule, and validation line. Preview is "
                "read-only and Confirm and Write remains human. Project memory stays under "
                "<project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.\n\n"
                + current_json
            )
            QApplication.clipboard().setText(prompt)
            self._append_log(
                "Copied advanced external AI review prompt. No files were written."
            )
            show_auto_close_action_window(
                dialog,
                title="Copied formulary prompt",
                message="The external AI review prompt was copied.",
            )

        def receive_formulary_from_ai() -> None:
            receive_dialog = QDialog(dialog)
            receive_dialog.setWindowTitle("Receive Formulary from AI")
            receive_dialog.resize(820, 620)
            layout = QVBoxLayout(receive_dialog)
            help_label = QLabel(
                "Paste one AI JSON answer. Applying it updates the form and rebuilds a read-only preview; it does not write files."
            )
            help_label.setWordWrap(True)
            layout.addWidget(help_label)
            response_edit = QTextEdit()
            layout.addWidget(response_edit, 1)
            row = QHBoxLayout()
            apply_button = QPushButton("Apply AI Formulary to Form")
            close_button = QPushButton("Cancel")
            row.addStretch(1)
            row.addWidget(apply_button)
            row.addWidget(close_button)
            layout.addLayout(row)

            def apply_external_form() -> None:
                try:
                    parsed = parse_ai_formulary_response(
                        response_edit.toPlainText(), collect_inputs()
                    )
                except Exception as exc:
                    show_error_copy_close_window(
                        receive_dialog,
                        title="Could not parse AI formulary",
                        message="The AI answer could not be parsed.\n\nError: " + str(exc),
                    )
                    return
                action_state.disable(
                    "AI formulary changed the form. Preview and validation must run again."
                )
                self._local_freeze_preview = None
                apply_inputs(parsed.inputs)
                self._append_log(
                    "Received external AI formulary and applied it. No files were written."
                )
                preview_local_freeze()
                receive_dialog.close()

            apply_button.clicked.connect(apply_external_form)
            close_button.clicked.connect(receive_dialog.close)
            receive_dialog.show()

        def ignore_this_freeze() -> None:
            self._local_freeze_preview = None
            widgets.preview_text_edit.clear()
            action_state.disable("Freeze draft was ignored by the human.")
            intake_used = mark_latest_freeze_hint_used(
                project_root, freeze_id="ignored-by-human"
            )
            self.status_label.setText(
                "Local freeze draft ignored. No freeze entry was written."
            )
            self._append_log(
                "IGNORE THIS FREEZE selected. No frozen memory entry was written."
            )
            for warning in intake_used.get("warnings") or intake_used.get("errors") or []:
                self._append_log("- " + str(warning))
            dialog.close()

        def confirm_and_write_local_freeze() -> None:
            preview = self._local_freeze_preview
            if not preview:
                self.status_label.setText(
                    "No valid local freeze preview was available. The form was closed."
                )
                self._append_log(
                    "Local freeze write skipped: no valid preview was available."
                )
                dialog.close()
                return
            current_project_root = self._project_root()
            binding_ok, binding_error = freeze_confirmation_binding_matches(
                confirmation_binding, current_project_root or "", collect_inputs()
            )
            if not binding_ok:
                invalidate_current_confirmation()
                self.status_label.setText(
                    "Freeze confirmation became stale. Preview again before writing."
                )
                self._append_log("LOCAL FREEZE WRITE BLOCKED: " + binding_error)
                return
            result = write_confirmed_freeze_entry(
                project_root, preview, confirmation=True
            )
            if not result.get("ok"):
                self.status_label.setText("Local freeze write failed. Check the log.")
                self._append_log("LOCAL FREEZE WRITE FAILED")
                self._append_log("\n".join(result.get("errors") or ["Unknown error"]))
                dialog.close()
                return
            self.status_label.setText("Local freeze entry written successfully.")
            self._append_log("LOCAL FREEZE WRITE OK")
            self._append_log("Freeze ID: " + str(result.get("freeze_id") or ""))
            for path in result.get("written_paths") or []:
                self._append_log("- " + str(path))
            mark_latest_freeze_hint_used(
                project_root, freeze_id=str(result.get("freeze_id") or "")
            )
            compliance = refresh_ai_compliance_context(project_root)
            self._append_log("AI COMPLIANCE REFRESH AFTER LOCAL WRITE")
            if compliance.get("startup_context_refreshed"):
                self._append_log(
                    "Startup freeze context refreshed for next AI programming session."
                )
            for error in compliance.get("errors") or []:
                self._append_log("- " + str(error))
            if not compliance.get("ok"):
                self.status_label.setText(
                    "Local freeze written. AI compliance refresh warning logged."
                )
            dialog.close()

        widgets.copy_to_ai_button.clicked.connect(copy_formulary_to_ai)
        widgets.receive_from_ai_button.clicked.connect(receive_formulary_from_ai)
        widgets.preview_button.clicked.connect(preview_local_freeze)
        widgets.confirm_write_button.clicked.connect(confirm_and_write_local_freeze)
        widgets.ignore_freeze_button.clicked.connect(ignore_this_freeze)
        widgets.cancel_button.clicked.connect(dialog.close)

        def on_finished(_result: int = 0) -> None:
            ai_runtime.close()
            self._clear_local_freeze_dialog_reference(dialog)

        dialog.finished.connect(on_finished)
        self._local_freeze_dialog = dialog
        ai_runtime.wire()
        ai_runtime.fill_selected()
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
