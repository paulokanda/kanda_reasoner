# project-path: kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py
"""Human-authority runtime for one local Freeze Entry dialog."""

from __future__ import annotations

from typing import Any, Mapping

from PySide6.QtWidgets import (
    QApplication, QDialog,
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
from kanda_reasoner_app.freeze_after_update_gui._external_ai_formulary_handoff import (
    copy_freeze_formulary_to_clipboard,
)
from kanda_reasoner_app.freeze_after_update_gui._freeze_formulary_ai_runtime import (
    FreezeFormularyAIController,
)
from kanda_reasoner_app.freeze_after_update_gui._local_freeze_bootstrap_worker import (
    LocalFreezeBootstrapRequest,
    create_local_freeze_bootstrap_job,
)
from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_widgets import (
    build_local_freeze_dialog_widgets,
    build_local_freeze_fallback_inputs,
)
from kanda_reasoner_app.freeze_after_update_gui.local_freeze_confirmation_binding import (
    FreezeActionStateController,
    apply_freeze_form_inputs,
    bind_freeze_confirmation_invalidation,
    build_freeze_confirmation_binding,
    collect_freeze_form_inputs,
    freeze_confirmation_binding_matches,
)
from kanda_reasoner_app.freeze_after_update_gui.local_freeze_preview_log import (
    build_local_freeze_preview_log_text,
)
from kanda_reasoner_app.freeze_after_update_gui._local_freeze_preview_presentation import (
    render_local_freeze_preview,
)
from kanda_reasoner_app.freeze_hint_intake import (
    discard_latest_freeze_hint_candidate,
    mark_latest_freeze_hint_used,
)
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

        starter_inputs = build_local_freeze_fallback_inputs()

        def displayed_candidate_present() -> bool:
            title = widgets.feature_title_edit.text().strip()
            return bool(title) and title != starter_inputs["feature_title"]

        def apply_inputs(inputs: Mapping[str, Any]) -> None:
            nonlocal applying_inputs
            applying_inputs = True
            try:
                apply_freeze_form_inputs(widgets, inputs)
            finally:
                applying_inputs = False

        def apply_preview_result(
            inputs: Mapping[str, Any],
            result: Mapping[str, Any],
            validation_result: Mapping[str, Any] | None,
        ) -> None:
            nonlocal confirmation_binding
            preview = dict(result or {})
            validation = dict(validation_result or {})
            self._local_freeze_preview = preview if preview.get("ok") else None
            confirmation_binding = None
            rendered = render_local_freeze_preview(preview, validation)
            if preview.get("ok") and preview.get("is_writable"):
                if validation.get("ok"):
                    try:
                        confirmation_binding = build_freeze_confirmation_binding(
                            project_root, inputs
                        )
                    except Exception as exc:
                        self._local_freeze_preview = None
                        action_state.set_state(
                            False,
                            displayed_candidate_present(),
                            "Active Project authority is unavailable. Select the "
                            "Project again, then rebuild Preview. The displayed "
                            "candidate may still be ignored."
                        )
                        rendered = (
                            "ERRORS:\n- Active Project authority is unavailable: "
                            + str(exc)
                            + "\n\n"
                            + "The frozen-style entry is withheld until authority is restored.\n"
                        )
                        self.status_label.setText(
                            "Local freeze Preview could not bind the Active Project."
                        )
                        self._append_log(
                            "LOCAL FREEZE CONFIRMATION BINDING BLOCKED: "
                            + str(exc)
                        )
                    else:
                        action_state.set_state(True, True)
                        self.status_label.setText(
                            "Local freeze preview ready. Review it, then confirm if correct."
                        )
                        self._append_log(
                            "Local freeze entry preview is ready and writable. No files were written."
                        )
                else:
                    self._local_freeze_preview = None
                    action_state.set_state(
                        False,
                        True,
                        "Freeze preview validation blocked writing. You may still delete this candidate.",
                    )
                    rendered = render_local_freeze_preview(preview, validation)
                    self._append_log(
                        "Local freeze preview was generated but validation blocked writing."
                    )
            else:
                action_state.set_state(
                    False,
                    displayed_candidate_present(),
                    "No writable freeze entry is available. You may delete the displayed candidate or fix it.",
                )
                self._append_log("Local freeze preview is not writable.")
            widgets.preview_text_edit.setPlainText(rendered)
            self._append_log_block(
                build_local_freeze_preview_log_text(
                    preview,
                    validation if validation else None,
                )
            )

        def preview_local_freeze(*, copy_candidate_to_clipboard: bool = False) -> None:
            self._local_freeze_preview = None
            action_state.disable("Preview is being rebuilt.")
            inputs = collect_inputs()
            result = preview_freeze_entry(project_root, inputs)
            validation_result = None
            if result.get("ok") and result.get("is_writable"):
                validation_result = validate_freeze_entry_preview(project_root, result)
            apply_preview_result(inputs, result, validation_result)
            if copy_candidate_to_clipboard: QApplication.clipboard().setText(widgets.preview_text_edit.toPlainText())

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
                action_state.set_state(
                    False,
                    displayed_candidate_present(),
                    "The form or selected project changed after Preview. Preview "
                    "again to confirm, or Ignore this Freeze to discard the "
                    "displayed candidate."
                )
            ai_runtime.invalidate(
                "The Project or form changed; pending AI result discarded."
            )

        bind_freeze_confirmation_invalidation(
            widgets, self.project_root_edit, invalidate_current_confirmation
        )

        def copy_formulary_to_ai() -> None:
            try:
                copy_freeze_formulary_to_clipboard(collect_inputs())
            except Exception as exc:
                show_error_copy_close_window(
                    dialog,
                    title="Copy Entry to AI failed",
                    message=(
                        "The Freeze formulary draft was not copied.\n\nError: "
                        + str(exc)
                    ),
                )
                return
            self._append_log(
                "Copied Freeze formulary entry to the clipboard. No files were "
                "written and no external site was opened."
            )
            show_auto_close_action_window(
                dialog,
                title="Freeze entry copied",
                message=(
                    "The strict Freeze draft prompt was copied to the clipboard. "
                    "Paste it into the AI of your choice, review the answer, then use "
                    "Receive Formulary from AI. No external site was opened."
                ),
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
            nonlocal confirmation_binding
            displayed_title = widgets.feature_title_edit.text().strip()
            discarded = discard_latest_freeze_hint_candidate(
                project_root, expected_feature_title=displayed_title
            )
            if not discarded.get("ok"):
                self.status_label.setText(
                    "Freeze candidate changed; nothing was deleted. Review the log."
                )
                for error in discarded.get("errors") or []:
                    self._append_log("IGNORE THIS FREEZE BLOCKED: " + str(error))
                return
            ai_runtime.invalidate("Current Freeze candidate was deleted by the human.")
            self._local_freeze_preview = None
            confirmation_binding = None
            apply_inputs(starter_inputs)
            preview_local_freeze()
            action_state.disable("The safe starter placeholder is not a Freeze candidate.")
            self.status_label.setText(
                "Current Freeze candidate deleted. Safe starter placeholder restored."
            )
            self._append_log(
                "IGNORE THIS FREEZE: CURRENT CANDIDATE DELETED AND FORGOTTEN. "
                "Safe starter placeholder restored; no frozen memory entry was written."
            )
            if discarded.get("candidate_found"):
                authority = "PASS" if discarded.get(
                    "explicit_human_ignore_recorded"
                ) else "NOT RECORDED"
                self._append_log(
                    "EXPLICIT HUMAN IGNORE AUTHORITY: " + authority
                )
            else:
                self._append_log(
                    "IGNORE THIS FREEZE: no persisted intake candidate was "
                    "present; the displayed draft was cleared only."
                )
            for path in discarded.get("deleted_paths") or []:
                self._append_log("- DELETED: " + str(path))
            for warning in discarded.get("warnings") or []:
                self._append_log("- WARNING: " + str(warning))

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
        widgets.preview_button.clicked.connect(lambda _checked=False: preview_local_freeze(copy_candidate_to_clipboard=True))
        widgets.confirm_write_button.clicked.connect(confirm_and_write_local_freeze)
        widgets.ignore_freeze_button.clicked.connect(ignore_this_freeze)
        widgets.cancel_button.clicked.connect(dialog.close)

        def on_finished(_result: int = 0) -> None:
            current_job = self._local_freeze_bootstrap_job
            if current_job is not None and current_job.running():
                current_job.request_cancel()
                self._local_freeze_bootstrap_retired_jobs.append(current_job)
                self._local_freeze_bootstrap_job = None
                self._local_freeze_bootstrap_generation += 1
            ai_runtime.close()
            self._clear_local_freeze_dialog_reference(dialog)

        def settle_bootstrap(generation: int) -> None:
            job = self._local_freeze_bootstrap_job
            is_current = (
                job is not None
                and job.request.generation == generation
                and job.request.project_root == str(project_root)
            )
            if not is_current:
                self._local_freeze_bootstrap_retired_jobs = [
                    item
                    for item in self._local_freeze_bootstrap_retired_jobs
                    if item.request.generation != generation
                ]
                return
            self._local_freeze_bootstrap_job = None
            try:
                dialog_visible = dialog.isVisible()
            except RuntimeError:
                dialog_visible = False
            current_root = self._project_root()
            if (
                not dialog_visible
                or current_root is None
                or str(current_root.resolve(strict=False)) != str(project_root)
            ):
                self._append_log(
                    "Stale Local Freeze bootstrap result discarded after dialog or Project change."
                )
                return
            ai_runtime._set_busy(False)
            if job.was_cancelled:
                widgets.mode_status_label.setText(
                    "Local Freeze intake was cancelled before settlement."
                )
                return
            if job.failure_text:
                widgets.mode_status_label.setText(
                    "Local Freeze intake failed. Use Fill with Heuristic to retry."
                )
                self._append_log(
                    "LOCAL FREEZE BOOTSTRAP FAILED: " + job.failure_text
                )
                return
            payload = dict(job.result or {})
            inputs = dict(payload.get("inputs") or {})
            apply_inputs(inputs)
            apply_preview_result(
                inputs,
                dict(payload.get("preview") or {}),
                dict(payload.get("validation") or {}),
            )
            widgets.mode_status_label.setText(
                "Heuristic intake loaded without blocking the interface."
            )
            self._append_log(
                "Local Freeze intake and initial Preview completed off the GUI thread."
            )

        dialog.finished.connect(on_finished)
        self._local_freeze_dialog = dialog
        ai_runtime.wire()
        action_state.disable("Local Freeze intake is loading in the background.")
        ai_runtime._set_busy(True)
        widgets.mode_status_label.setText(
            "Loading project-local Freeze intake in the background..."
        )
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

        self._local_freeze_bootstrap_generation += 1
        request = LocalFreezeBootstrapRequest(
            generation=self._local_freeze_bootstrap_generation,
            project_root=str(project_root),
            fallback_inputs=build_local_freeze_fallback_inputs(),
        )
        job = create_local_freeze_bootstrap_job(
            request,
            settled_callback=settle_bootstrap,
        )
        self._local_freeze_bootstrap_job = job
        job.start()
