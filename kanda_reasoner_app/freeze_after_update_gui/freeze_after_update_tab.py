# project-path: kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py
"""GUI tab for local freeze after update and auto-filled local freezing."""
from __future__ import annotations

__all__ = ['FreezeAfterUpdateTab']
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
import json
import queue
import threading
from pathlib import Path
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
from kanda_reasoner_app.freeze_after_update.contract import preview_freeze_entry, refresh_ai_compliance_context, validate_freeze_entry_preview, write_confirmed_freeze_entry
from kanda_reasoner_app.freeze_hint_intake import mark_latest_freeze_hint_used
from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import parse_ai_formulary_response as parse_ai_formulary_response_payload
from kanda_reasoner_app.freeze_after_update_gui._box_actions import FreezeBoxActionsMixin
from kanda_reasoner_app.freeze_after_update_gui._freeze_memory_exports import FreezeMemoryExportMixin
from kanda_reasoner_app.freeze_after_update_gui._local_ai_formulary import (
    AUTO_LOCAL_AI_MODEL_LABEL,
    LocalFreezeAIFormularyRunner,
    _list_local_ai_models,
    _local_ai_response_looks_like_prompt_echo,
    _model_name_from_local_ai_combo_text,
    _validate_local_ai_form_against_heuristic,
)
from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_widgets import (
    FreezeLocalFreezeDialogSupportMixin,
    build_local_freeze_dialog_widgets,
)
from kanda_reasoner_app.freeze_after_update_gui._path_controls import FreezePathControlsMixin
from kanda_reasoner_app.freeze_after_update_gui._ui_builder import FreezeUiBuilderMixin
from kanda_reasoner_app.freeze_after_update_gui.local_freeze_preview_log import build_local_freeze_preview_log_text
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window
FREEZE_CONFIRM_ENABLED_STYLE = 'color: #008000; font-weight: bold;'
FREEZE_IGNORE_ENABLED_STYLE = 'color: #B00020; font-weight: bold;'
FREEZE_DISABLED_ACTION_STYLE = 'color: #808080; font-weight: bold;'

class FreezeAfterUpdateTab(
    FreezeUiBuilderMixin, FreezePathControlsMixin, FreezeBoxActionsMixin,
    FreezeMemoryExportMixin, FreezeLocalFreezeDialogSupportMixin, QWidget,
):
    """Human-facing controller for the project-local freeze-after-update box."""

    def __init__(self) -> None:
        """Support init behavior.
        """
        
        super().__init__()
        self._last_output_folder: Path | None = None
        self._pending_staged_project_root: Path | None = None
        self._pending_staged_action: str | None = None
        self._local_freeze_preview: dict | None = None
        self._local_freeze_dialog: QDialog | None = None
        self._what_to_say_dialog: QDialog | None = None
        self._what_to_say_text_edit: QTextEdit | None = None
        self._project_root_controls_moved = False
        self._local_freeze_ai_thread: threading.Thread | None = None
        self._local_freeze_ai_result_queue: queue.Queue | None = None
        self._local_freeze_ai_request_id: object | None = None
        self._local_freeze_ai_poll_timer: QTimer | None = None
        self._build_ui()
        self._connect_signals()

    def _open_local_freeze_entry_dialog(self) -> None:
        """Support open local freeze entry dialog behavior.
        """
        
        if self._raise_existing_local_freeze_dialog():
            return
        project_root = self._require_project_root()
        if project_root is None:
            return
        widgets = build_local_freeze_dialog_widgets(self, disabled_action_style=FREEZE_DISABLED_ACTION_STYLE)
        dialog = widgets.dialog
        local_ai_radio = widgets.local_ai_radio
        heuristic_radio = widgets.heuristic_radio
        local_ai_model_combo = widgets.local_ai_model_combo
        refresh_local_ai_models_button = widgets.refresh_local_ai_models_button
        mode_status_label = widgets.mode_status_label
        feature_title_edit = widgets.feature_title_edit
        primary_box_edit = widgets.primary_box_edit
        box_type_edit = widgets.box_type_edit
        validated_files_edit = widgets.validated_files_edit
        generated_files_edit = widgets.generated_files_edit
        protected_paths_edit = widgets.protected_paths_edit
        do_not_regress_edit = widgets.do_not_regress_edit
        validation_evidence_edit = widgets.validation_evidence_edit
        known_warnings_edit = widgets.known_warnings_edit
        planned_next_step_edit = widgets.planned_next_step_edit
        notes_edit = widgets.notes_edit
        preview_text_edit = widgets.preview_text_edit
        autofill_button = widgets.autofill_button
        copy_to_ai_button = widgets.copy_to_ai_button
        receive_from_ai_button = widgets.receive_from_ai_button
        preview_button = widgets.preview_button
        confirm_write_button = widgets.confirm_write_button
        ignore_freeze_button = widgets.ignore_freeze_button
        cancel_button = widgets.cancel_button
        self._local_freeze_preview = None

        def set_freeze_action_buttons_state(can_confirm: bool, can_ignore: bool, reason: str='') -> None:
            """Enable freeze action buttons only after a clean writable preview."""
            confirm_write_button.setEnabled(can_confirm)
            ignore_freeze_button.setEnabled(can_ignore)
            if can_confirm:
                confirm_write_button.setStyleSheet(FREEZE_CONFIRM_ENABLED_STYLE)
                confirm_write_button.setToolTip('Write this validated local freeze entry after explicit human confirmation.')
            else:
                confirm_write_button.setStyleSheet(FREEZE_DISABLED_ACTION_STYLE)
                confirm_reason = reason or 'Preview and validate a writable freeze entry before confirming.'
                confirm_write_button.setToolTip(confirm_reason)
            if can_ignore:
                ignore_freeze_button.setStyleSheet(FREEZE_IGNORE_ENABLED_STYLE)
                ignore_freeze_button.setToolTip('Discard this current writable freeze draft and mark the current freeze hint as ignored/used. No freeze entry is written.')
            else:
                ignore_freeze_button.setStyleSheet(FREEZE_DISABLED_ACTION_STYLE)
                ignore_reason = reason or 'No current writable freeze draft is available to ignore.'
                ignore_freeze_button.setToolTip(ignore_reason)

        def disable_freeze_action_buttons(reason: str='') -> None:
            """Disable both destructive/local-freeze action buttons with one reason."""
            set_freeze_action_buttons_state(False, False, reason)
        disable_freeze_action_buttons('No writable freeze preview has been generated yet.')

        def collect_inputs() -> dict:
            return {'feature_title': feature_title_edit.text().strip(), 'primary_box': primary_box_edit.text().strip(), 'box_type': box_type_edit.text().strip() or 'Module Box', 'validated_files': validated_files_edit.toPlainText(), 'generated_files': generated_files_edit.toPlainText(), 'protected_paths': protected_paths_edit.toPlainText(), 'do_not_regress_rules': do_not_regress_edit.toPlainText(), 'validation_evidence_summary': validation_evidence_edit.toPlainText(), 'known_warnings': known_warnings_edit.toPlainText().strip(), 'planned_next_step': planned_next_step_edit.toPlainText().strip(), 'notes': notes_edit.toPlainText().strip()}

        def apply_inputs(inputs: dict) -> None:
            feature_title_edit.setText(str(inputs.get('feature_title', '')))
            primary_box_edit.setText(str(inputs.get('primary_box', '')))
            box_type_edit.setText(str(inputs.get('box_type', 'Module Box') or 'Module Box'))
            validated_files_edit.setPlainText(str(inputs.get('validated_files', '')))
            generated_files_edit.setPlainText(str(inputs.get('generated_files', '')))
            protected_paths_edit.setPlainText(str(inputs.get('protected_paths', '')))
            do_not_regress_edit.setPlainText(str(inputs.get('do_not_regress_rules', '')))
            validation_evidence_edit.setPlainText(str(inputs.get('validation_evidence_summary', '')))
            known_warnings_edit.setPlainText(str(inputs.get('known_warnings', '')))
            planned_next_step_edit.setPlainText(str(inputs.get('planned_next_step', '')))
            notes_edit.setPlainText(str(inputs.get('notes', '')))

        def selected_local_ai_model_name() -> str:
            return _model_name_from_local_ai_combo_text(str(local_ai_model_combo.currentText() or ''))

        def set_ai_fill_busy(is_busy: bool) -> None:
            autofill_button.setEnabled(not is_busy)
            preview_button.setEnabled(not is_busy)
            copy_to_ai_button.setEnabled(not is_busy)
            receive_from_ai_button.setEnabled(not is_busy)
            refresh_local_ai_models_button.setEnabled(not is_busy)
            local_ai_radio.setEnabled(not is_busy)
            heuristic_radio.setEnabled(not is_busy)
            local_ai_model_combo.setEnabled(not is_busy)
            if is_busy:
                disable_freeze_action_buttons('Local AI fill is still running.')

        def populate_local_ai_model_combo() -> list[str]:
            previous = selected_local_ai_model_name()
            local_ai_model_combo.blockSignals(True)
            try:
                local_ai_model_combo.clear()
                local_ai_model_combo.addItem(AUTO_LOCAL_AI_MODEL_LABEL)
                try:
                    models = _list_local_ai_models()
                except Exception as exc:
                    models = []
                    mode_status_label.setText('Local AI model refresh failed; Heuristics remains available. Error: ' + str(exc))
                for model_name in models:
                    local_ai_model_combo.addItem(model_name)
                if previous:
                    index = local_ai_model_combo.findText(previous)
                    if index >= 0:
                        local_ai_model_combo.setCurrentIndex(index)
                if models:
                    mode_status_label.setText('Local AI ready: ' + str(len(models)) + ' model(s) found. Default fill mode is Local AI.')
                else:
                    mode_status_label.setText('No local AI model found yet. Local AI mode will fall back to Heuristics.')
                return models
            finally:
                local_ai_model_combo.blockSignals(False)

        def fill_with_heuristics_only(reason: str='') -> None:
            disable_freeze_action_buttons('No writable freeze preview has been generated yet.')
            self._local_freeze_preview = None
            apply_inputs(self._build_heuristic_local_freeze_inputs(project_root))
            if reason:
                self._append_log(reason)
            self._append_log('Local freeze entry fields filled from project-local freeze hint intake when available; otherwise a safe starter was used. No files were written.')
            preview_local_freeze()

        def handle_local_ai_fill_result(response_text: str, model_name: str) -> None:
            set_ai_fill_busy(False)
            heuristic_inputs = self._build_heuristic_local_freeze_inputs(project_root)
            if _local_ai_response_looks_like_prompt_echo(response_text):
                self._append_log('Local AI output rejected by quality gates: prompt echo detected. Heuristic draft kept.')
                mode_status_label.setText('Local AI echoed the prompt; heuristic draft kept.')
                QMessageBox.warning(dialog, 'Local AI fill rejected', 'Local AI echoed the prompt/instructions instead of returning a clean form. The heuristic draft was kept and previewed.')
                preview_local_freeze()
                return
            try:
                updated_inputs = parse_ai_formulary_response(response_text)
            except Exception as exc:
                self._append_log('Local AI returned an answer that could not be parsed. Keeping heuristic draft.')
                self._append_log('Local AI parse error: ' + str(exc))
                mode_status_label.setText('Local AI answer could not be parsed; heuristic draft kept.')
                QMessageBox.warning(dialog, 'Local AI fill fallback', 'Local AI ran, but its answer could not be parsed. The heuristic draft was kept and previewed.')
                preview_local_freeze()
                return
            ok_to_apply, quality_reasons = _validate_local_ai_form_against_heuristic(updated_inputs, heuristic_inputs)
            if not ok_to_apply:
                self._append_log('Local AI output rejected by quality gates. Heuristic draft kept.')
                for reason in quality_reasons:
                    self._append_log('- ' + reason)
                mode_status_label.setText('Local AI degraded the heuristic baseline; heuristic draft kept.')
                QMessageBox.warning(dialog, 'Local AI fill rejected', 'Local AI returned a parseable form, but it weakened the heuristic baseline. The heuristic draft was kept.\n\n' + '\n'.join(('- ' + reason for reason in quality_reasons[:8])))
                preview_local_freeze()
                return
            disable_freeze_action_buttons('Local AI changed the form. Preview and validation must run again.')
            self._local_freeze_preview = None
            apply_inputs(updated_inputs)
            self._append_log('Local AI filled the freeze formulary using model: ' + str(model_name) + '. Quality gates passed. No files were written.')
            mode_status_label.setText('Local AI fill applied with model: ' + str(model_name) + ' after quality gates.')
            preview_local_freeze()

        def handle_local_ai_fill_error(error_message: str) -> None:
            set_ai_fill_busy(False)
            mode_status_label.setText('Local AI unavailable; heuristic draft was kept.')
            self._append_log('Local AI fill unavailable. Falling back to heuristics. Error: ' + str(error_message))
            preview_local_freeze()

        def stop_local_ai_polling() -> None:
            self._local_freeze_ai_request_id = None
            if self._local_freeze_ai_poll_timer is not None:
                self._local_freeze_ai_poll_timer.stop()
                self._local_freeze_ai_poll_timer.deleteLater()
                self._local_freeze_ai_poll_timer = None
            self._local_freeze_ai_result_queue = None

        def poll_local_ai_fill_queue() -> None:
            request_id = self._local_freeze_ai_request_id
            result_queue = self._local_freeze_ai_result_queue
            if request_id is None or result_queue is None:
                return
            try:
                returned_request_id, ok, payload, model_name = result_queue.get_nowait()
            except queue.Empty:
                return
            stop_local_ai_polling()
            self._local_freeze_ai_thread = None
            if returned_request_id is not request_id:
                return
            if not dialog.isVisible():
                return
            if ok:
                handle_local_ai_fill_result(str(payload), str(model_name))
            else:
                handle_local_ai_fill_error(str(payload))

        def fill_with_local_ai() -> None:
            fill_with_heuristics_only('Local AI mode starts from the deterministic heuristic draft, then asks the selected local model to improve it.')
            selected_model = selected_local_ai_model_name()
            if local_ai_model_combo.count() <= 1 and (not selected_model):
                mode_status_label.setText('No local AI model found; heuristic draft kept.')
                self._append_log('Local AI mode selected, but no model was found. Heuristic draft kept.')
                return
            stop_local_ai_polling()
            set_ai_fill_busy(True)
            request_id = object()
            result_queue: queue.Queue = queue.Queue(maxsize=1)
            self._local_freeze_ai_request_id = request_id
            self._local_freeze_ai_result_queue = result_queue
            mode_status_label.setText('Local AI is filling the freeze form. The form remains usable after the result returns.')
            self._append_log('Local AI formulary fill requested through a shutdown-safe Python daemon thread. No files will be written.')
            runner = LocalFreezeAIFormularyRunner(inputs=collect_inputs(), project_root=project_root, model_name=selected_model)

            def run_local_ai_request() -> None:
                ok, payload, model_name = runner.run()
                try:
                    result_queue.put_nowait((request_id, ok, payload, model_name))
                except Exception:
                    pass
            self._local_freeze_ai_thread = threading.Thread(target=run_local_ai_request, name='kanda-local-freeze-ai-fill', daemon=True)
            self._local_freeze_ai_thread.start()
            self._local_freeze_ai_poll_timer = QTimer(dialog)
            self._local_freeze_ai_poll_timer.setInterval(200)
            self._local_freeze_ai_poll_timer.timeout.connect(poll_local_ai_fill_queue)
            dialog.destroyed.connect(stop_local_ai_polling)
            self._local_freeze_ai_poll_timer.start()

        def auto_fill_local_freeze() -> None:
            if local_ai_radio.isChecked():
                fill_with_local_ai()
            else:
                fill_with_heuristics_only()

        def render_findings(result: dict) -> str:
            lines = []
            errors = result.get('errors') or []
            warnings = result.get('warnings') or []
            if errors:
                lines.append('ERRORS:')
                lines.extend((f'- {item}' for item in errors))
                lines.append('')
            if warnings:
                lines.append('WARNINGS:')
                lines.extend((f'- {item}' for item in warnings))
                lines.append('')
            return '\n'.join(lines)

        def preview_local_freeze() -> None:
            self._local_freeze_preview = None
            disable_freeze_action_buttons('Preview is being rebuilt.')
            inputs = collect_inputs()
            result = preview_freeze_entry(project_root, inputs)
            self._local_freeze_preview = result if result.get('ok') else None
            markdown = result.get('markdown') or ''
            preview_text_edit.setPlainText(render_findings(result) + markdown)
            validation_result = None
            if result.get('ok') and result.get('is_writable'):
                validation_result = validate_freeze_entry_preview(project_root, result)
                if validation_result.get('ok'):
                    self._local_freeze_preview = result
                    set_freeze_action_buttons_state(True, True)
                    self.status_label.setText('Local freeze preview ready. Review it, then confirm if correct.')
                    self._append_log('Local freeze entry preview is ready and writable. No files were written.')
                else:
                    reason = 'Freeze preview validation blocked writing. Fix the errors before confirming or ignoring this freeze.'
                    disable_freeze_action_buttons(reason)
                    preview_text_edit.setPlainText(render_findings(validation_result) + markdown)
                    self._append_log('Local freeze preview was generated but validation blocked writing.')
            else:
                reason = 'No writable freeze entry is available. Fix missing fields or validation evidence first.'
                disable_freeze_action_buttons(reason)
                self._append_log('Local freeze preview is not writable. Fix the required fields or validation evidence.')
            self._append_log_block(build_local_freeze_preview_log_text(result, validation_result))

        def build_ai_review_prompt() -> str:
            current_inputs = collect_inputs()
            current_json = json.dumps(current_inputs, ensure_ascii=False, indent=2)
            return f'You are a specialist in KANDA Reasoner, Box Architecture, local-first freeze memory, AI-assisted programming workflows, human-confirmed freeze entries, and safe project-memory governance.\n\nContext:\nI just implemented and validated a feature. I am about to freeze it using the KANDA Reasoner Freeze Feature After Update tab. The form below was auto-filled heuristically by KANDA Reasoner.\n\nTask:\nReview and correct the freeze form for the current validated feature only. Improve clarity, protected paths, do-not-regress rules, validation summary, warnings, and notes. If the current form contains placeholders or stale legacy data from another feature, replace it using only evidence already present in this chat. Do not invent validation that is not present. Do not ask me to upload files. Do not write a patch. Do not include explanations outside the required return format.\n\nCritical rules:\n- Keep project-specific frozen memory under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.\n- Do not store project-specific frozen memory inside project_freeze_ledger.\n- Preserve the local freeze workflow: preview is read-only; Confirm and Write requires human confirmation.\n- Preserve AI startup compliance: after local freeze write, the startup freeze context must be refreshed.\n- External AI review remains advanced/fallback, not the normal freeze path.\n\nReturn format - strict copy/paste contract for KANDA Reasoner:\nYour entire answer must be exactly the receive-ready block.\nThe first visible characters of your answer must be KANDA_FREEZE_FORM_JSON_BEGIN.\nThe last visible characters of your answer must be KANDA_FREEZE_FORM_JSON_END.\nDo not use markdown. Do not use code fences. Do not use bullets. Do not add comments.\nDo not write explanations before or after the block.\nBetween the markers, return one valid JSON object only.\nUse double quotes for every key and string value.\nDo not use trailing commas.\nFor multiline text fields, keep each field as one JSON string and escape line breaks as \\n.\nDo not place real unescaped line breaks inside string values.\nDo not change the marker names.\n\nCopy/paste-ready answer shape:\nKANDA_FREEZE_FORM_JSON_BEGIN\n{{\n  "feature_title": "...",\n  "primary_box": "...",\n  "box_type": "...",\n  "validated_files": "one project-relative path per line, encoded with \\\\n between lines",\n  "generated_files": "one project-relative path per line, encoded with \\\\n between lines",\n  "protected_paths": "one project-relative path per line, encoded with \\\\n between lines",\n  "do_not_regress_rules": "one rule per line, encoded with \\\\n between lines",\n  "validation_evidence_summary": "validation evidence only; do not invent validation; encode line breaks with \\\\n",\n  "known_warnings": "...",\n  "planned_next_step": "...",\n  "notes": "..."\n}}\nKANDA_FREEZE_FORM_JSON_END\n\nCurrent form JSON to review and correct for the current feature only:\nIf a field is a placeholder or belongs to an older unrelated freeze workflow, replace it from the current chat evidence.\n{current_json}\n'

        def copy_formulary_to_ai() -> None:
            QApplication.clipboard().setText(build_ai_review_prompt())
            self._append_log('Copied AI specialist review prompt for the current local freeze formulary. No files were written.')
            show_auto_close_action_window(dialog, title='Copied formulary prompt', message='The strict AI review prompt was copied to the clipboard.', detail_text='Paste it into AI. Its answer should start with KANDA_FREEZE_FORM_JSON_BEGIN and end with KANDA_FREEZE_FORM_JSON_END, with no markdown or explanation. Then paste that exact answer into Receive Formulary from AI.')

        def parse_ai_formulary_response(text: str) -> dict:
            parsed = parse_ai_formulary_response_payload(text, collect_inputs())
            if parsed.ignored_fields:
                self._append_log('Ignored unknown AI formulary field(s): ' + ', '.join(parsed.ignored_fields))
            return parsed.inputs

        def receive_formulary_from_ai() -> None:
            receive_dialog = QDialog(dialog)
            receive_dialog.setWindowTitle('Receive Formulary from AI')
            receive_dialog.resize(820, 620)
            receive_layout = QVBoxLayout(receive_dialog)
            receive_help = QLabel('Paste the AI answer here. It must contain JSON between KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END. Applying it updates this form and regenerates a read-only preview; it does not write files.')
            receive_help.setWordWrap(True)
            receive_layout.addWidget(receive_help)
            response_edit = QTextEdit()
            response_edit.setPlaceholderText('Paste AI response here, including KANDA_FREEZE_FORM_JSON_BEGIN / END markers.')
            receive_layout.addWidget(response_edit, 1)
            receive_button_row = QHBoxLayout()
            apply_button = QPushButton('Apply AI Formulary to Form')
            close_receive_button = QPushButton('Cancel')
            receive_button_row.addStretch(1)
            receive_button_row.addWidget(apply_button)
            receive_button_row.addWidget(close_receive_button)
            receive_layout.addLayout(receive_button_row)

            def apply_ai_formulary() -> None:
                try:
                    updated_inputs = parse_ai_formulary_response(response_edit.toPlainText())
                except Exception as exc:
                    show_error_copy_close_window(receive_dialog, title='Could not parse AI formulary', message=f'The AI answer could not be parsed even after the tolerant extractor tried to select and repair the JSON block. Ask AI to do it again. Tell AI to return exactly one valid JSON object between KANDA_FREEZE_FORM_JSON_BEGIN and KANDA_FREEZE_FORM_JSON_END, with no markdown, no prose, and no extra text. You can also paste the JSON object only.\n\nError: {exc}')
                    return
                disable_freeze_action_buttons('AI formulary changed the form. Preview and validation must run again.')
                self._local_freeze_preview = None
                apply_inputs(updated_inputs)
                self._append_log('Received AI formulary and applied it to the local freeze form. No files were written.')
                preview_local_freeze()
                receive_dialog.close()
            apply_button.clicked.connect(apply_ai_formulary)
            close_receive_button.clicked.connect(receive_dialog.close)
            receive_dialog.show()
            receive_dialog.raise_()
            receive_dialog.activateWindow()

        def ignore_this_freeze() -> None:
            reply = QMessageBox.question(self, 'Ignore this freeze', 'This will discard the current local freeze draft and will not write any frozen memory entry.\n\nIf a KANDA_FREEZE_HINT intake record filled this form, it will be marked as ignored/used so it does not keep refilling this same draft.\n\nContinue?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply != QMessageBox.Yes:
                self._append_log('Ignore this Freeze cancelled by human.')
                return
            self._local_freeze_preview = None
            preview_text_edit.clear()
            disable_freeze_action_buttons('Freeze draft was ignored by the human.')
            intake_used = mark_latest_freeze_hint_used(project_root, freeze_id='ignored-by-human')
            self.status_label.setText('Local freeze draft ignored. No freeze entry was written.')
            self._append_log('IGNORE THIS FREEZE selected. No frozen memory entry was written.')
            if intake_used.get('ok'):
                self._append_log('Freeze hint intake record marked ignored/used so it will not refill this draft.')
            elif intake_used.get('warnings'):
                self._append_log('Freeze hint intake ignore warning:')
                for warning in intake_used.get('warnings') or []:
                    self._append_log('- ' + str(warning))
            elif intake_used.get('errors'):
                self._append_log('Freeze hint intake ignore warning:')
                for error in intake_used.get('errors') or []:
                    self._append_log('- ' + str(error))
            else:
                self._append_log('No current freeze hint intake record was found to mark ignored.')
            dialog.close()

        def confirm_and_write_local_freeze() -> None:
            preview = self._local_freeze_preview
            if not preview:
                QMessageBox.warning(self, 'Preview missing', 'Generate a valid preview first.')
                return
            targets = preview.get('write_targets') or []
            target_text = '\n'.join((f'- {path}' for path in targets))
            reply = QMessageBox.question(self, 'Confirm local freeze write', f'You are about to write a local freeze entry for this active project.\n\nWILL WRITE:\n{target_text}\n\nWILL NOT WRITE:\n- project_freeze_ledger as project-specific memory\n- other project roots\n- temporary files in the project root\n\nContinue?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply != QMessageBox.Yes:
                self._append_log('Local freeze write cancelled by human confirmation gate.')
                return
            result = write_confirmed_freeze_entry(project_root, preview, confirmation=True)
            if not result.get('ok'):
                errors = '\n'.join(result.get('errors') or ['Unknown error'])
                show_error_copy_close_window(self, title='Local freeze write failed', message=errors)
                self._append_log('LOCAL FREEZE WRITE FAILED')
                self._append_log(errors)
                return
            self.status_label.setText('Local freeze entry written successfully.')
            self._append_log('LOCAL FREEZE WRITE OK')
            self._append_log(f"Freeze ID: {result.get('freeze_id')}")
            self._append_log('Written paths:')
            for path in result.get('written_paths') or []:
                self._append_log(f'- {path}')
            intake_used = mark_latest_freeze_hint_used(project_root, freeze_id=str(result.get('freeze_id') or ''))
            if intake_used.get('ok'):
                self._append_log('Freeze hint intake record marked as used for this freeze.')
            elif intake_used.get('warnings'):
                self._append_log('Freeze hint intake was not marked used:')
                for warning in intake_used.get('warnings') or []:
                    self._append_log(f'- {warning}')
            elif intake_used.get('errors'):
                self._append_log('Freeze hint intake mark-used warning:')
                for error in intake_used.get('errors') or []:
                    self._append_log(f'- {error}')
            compliance = refresh_ai_compliance_context(project_root)
            self._append_log('')
            self._append_log('AI COMPLIANCE REFRESH AFTER LOCAL WRITE')
            if compliance.get('project_local_ai_send_generation_deprecated'):
                self._append_log('Project-local files_to_send_ai ZIP generation is deprecated; using Show Project to AI startup/source-archive exposure instead.')
            elif compliance.get('ai_send_refreshed'):
                self._append_log('AI-send exposure refreshed for current freeze memory.')
                if compliance.get('ai_send_zip'):
                    self._append_log(f"- AI-send ZIP: {compliance.get('ai_send_zip')}")
                if compliance.get('ai_send_instruction'):
                    self._append_log(f"- AI-send instruction: {compliance.get('ai_send_instruction')}")
            else:
                self._append_log('AI-send exposure refresh failed or was unavailable.')
            if compliance.get('startup_context_refreshed'):
                self._append_log('Startup freeze context refreshed for next AI programming session.')
                self._append_log(f"- Startup ZIP: {compliance.get('startup_zip')}")
                read_before_all = compliance.get('read_before_all_instruction') or compliance.get('paste_after_uploading')
                self._append_log(f'- Read-before-all file: {read_before_all}')
                if compliance.get('prompt_library_zip'):
                    self._append_log(f"- Prompt library ZIP: {compliance.get('prompt_library_zip')}")
                self._append_log(f"- Context file inside startup ZIP: {compliance.get('generated_context_filename')}")
            else:
                self._append_log('Startup freeze context refresh failed or was unavailable.')
            if compliance.get('errors'):
                self._append_log('AI compliance refresh errors:')
                for error in compliance.get('errors') or []:
                    self._append_log(f'- {error}')
            if compliance.get('report'):
                self._append_log('')
                self._append_log('Current freeze exposure after write:')
                self._append_log(str(compliance.get('report')))
            if not compliance.get('ok'):
                QMessageBox.warning(self, 'Local freeze written; AI compliance refresh warning', 'The local freeze entry was written, but the AI-visible startup context refresh reported a warning or error. Check the log.')
                dialog.close()
            else:
                show_auto_close_action_window(self, title='Local freeze written', message='Freeze entry written successfully and AI startup freeze context was refreshed.', on_close=dialog.close)
        refresh_local_ai_models_button.clicked.connect(populate_local_ai_model_combo)
        local_ai_radio.toggled.connect(lambda checked: mode_status_label.setText('Local AI selected. The form will use the selected local model only if it passes quality gates; otherwise heuristic draft is kept.' if checked else 'Heuristics selected. The form will use deterministic local rules only.'))
        autofill_button.clicked.connect(auto_fill_local_freeze)
        copy_to_ai_button.clicked.connect(copy_formulary_to_ai)
        receive_from_ai_button.clicked.connect(receive_formulary_from_ai)
        preview_button.clicked.connect(preview_local_freeze)
        confirm_write_button.clicked.connect(confirm_and_write_local_freeze)
        ignore_freeze_button.clicked.connect(ignore_this_freeze)
        cancel_button.clicked.connect(dialog.close)

        def on_local_freeze_dialog_finished(_result: int=0) -> None:
            stop_local_ai_polling()
            self._clear_local_freeze_dialog_reference(dialog)
        dialog.finished.connect(on_local_freeze_dialog_finished)
        self._local_freeze_dialog = dialog
        populate_local_ai_model_combo()
        auto_fill_local_freeze()
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
