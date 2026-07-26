# project-path: kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py
"""Local-freeze dialog shell and support methods for the Freeze tab."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
)

from kanda_reasoner_app.freeze_hint_intake import build_freeze_form_inputs_from_latest_hint
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window

__all__ = [
    "FreezeLocalFreezeDialogSupportMixin",
    "LocalFreezeDialogWidgets",
    "build_local_freeze_dialog_widgets",
]


@dataclass(frozen=True)
class LocalFreezeDialogWidgets:
    """Widget references used by the local-freeze dialog callbacks."""

    dialog: QDialog
    heuristic_radio: QRadioButton
    local_ai_radio: QRadioButton
    web_ai_radio: QRadioButton
    mode_status_label: QLabel
    web_config_summary_label: QLabel
    open_config_web_ai_button: QPushButton
    feature_title_edit: QLineEdit
    primary_box_edit: QLineEdit
    box_type_edit: QLineEdit
    validated_files_edit: QTextEdit
    generated_files_edit: QTextEdit
    protected_paths_edit: QTextEdit
    do_not_regress_edit: QTextEdit
    validation_evidence_edit: QTextEdit
    known_warnings_edit: QTextEdit
    planned_next_step_edit: QTextEdit
    notes_edit: QTextEdit
    preview_text_edit: QTextEdit
    autofill_button: QPushButton
    copy_to_ai_button: QPushButton
    receive_from_ai_button: QPushButton
    preview_button: QPushButton
    confirm_write_button: QPushButton
    ignore_freeze_button: QPushButton
    cancel_button: QPushButton


class FreezeLocalFreezeDialogSupportMixin:
    """Single-window guard and heuristic form-input support for the local-freeze dialog."""

    def _raise_existing_local_freeze_dialog(self) -> bool:
        """Raise the active local-freeze form and block duplicate form windows."""
        dialog = self._local_freeze_dialog
        if dialog is None:
            return False
        try:
            if dialog.isVisible():
                dialog.raise_()
                dialog.activateWindow()
                self._append_log(
                    "Local Freeze Entry form is already open. Reusing the existing floating formulary window."
                )
                show_auto_close_action_window(
                    self,
                    title="Local Freeze Entry already open",
                    message=(
                        "A Local Freeze Entry formulary window is already open. "
                        "Close it before opening another one."
                    ),
                )
                return True
        except RuntimeError:
            self._local_freeze_dialog = None
            return False
        self._local_freeze_dialog = None
        return False

    def _clear_local_freeze_dialog_reference(self, dialog: QDialog) -> None:
        """Release the single-window guard after the local-freeze form closes."""
        if self._local_freeze_dialog is dialog:
            self._local_freeze_dialog = None
        self._local_freeze_preview = None

    def _build_heuristic_local_freeze_inputs(self, project_root: Path) -> dict:
        """Build the local freeze form from project-local intake, then fallback.

        The normal local-freeze path is: patch ZIP carries root-level
        KANDA_FREEZE_HINT.json, the intake box saves that sidecar under the
        selected project's <project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake, and
        the Freeze Feature After Update tab fills this form from that saved
        project-local JSON.

        If no current hint exists, return a safe starter draft. The starter is
        intentionally not writable until the human/AI supplies current feature
        validation evidence.
        """
        fallback_inputs = {
            "feature_title": "Current validated feature - replace with exact feature title",
            "primary_box": "Replace with the primary box for the current feature",
            "box_type": "Replace with the current box type",
            "validated_files": "",
            "generated_files": "",
            "protected_paths": "project_freeze_after_update/frozen_features_memory/",
            "do_not_regress_rules": "\n".join(
                [
                    "Do not freeze without current feature validation evidence.",
                    "Preserve the current feature behavior validated by the user.",
                    "Keep project-specific frozen memory under <project>_show_project_to_AI/project_freeze_after_update/frozen_features_memory.",
                    "Do not store project-specific frozen memory inside project_freeze_ledger.",
                    "Do not replace current feature data with stale legacy workflow data.",
                ]
            ),
            "validation_evidence_summary": "",
            "known_warnings": (
                "Starter draft only. Replace placeholders with the current validated feature data. "
                "No validation evidence has been inferred or invented."
            ),
            "planned_next_step": (
                "Replace placeholders with current feature evidence, then Preview Freeze Entry before Confirm and Write."
            ),
            "notes": (
                "Auto-filled by the Freeze Feature After Update tab as a safe current-feature starter. "
                "This draft intentionally avoids stale legacy freeze-workflow titles, paths, and validation markers."
            ),
        }
        try:
            return build_freeze_form_inputs_from_latest_hint(project_root, fallback_inputs)
        except Exception as exc:
            recovered = dict(fallback_inputs)
            recovered["known_warnings"] = (
                str(recovered.get("known_warnings", "")).strip()
                + " Freeze hint intake was unavailable, so the safe starter draft was kept. Error: "
                + str(exc)
            ).strip()
            return recovered


def build_local_freeze_dialog_widgets(parent: object, *, disabled_action_style: str) -> LocalFreezeDialogWidgets:
    """Create the local-freeze dialog shell and return callback widget references."""
    dialog = QDialog(parent)
    dialog.setWindowTitle("New Local Freeze Entry")
    dialog.resize(980, 820)
    layout = QVBoxLayout(dialog)
    intro = QLabel(
        "Local freeze entry workflow: choose Heuristic, Local AI, or Web AI. Heuristic is the deterministic "
        "default. Local and Web AI may improve only the draft and must pass quality gates. Preview is read-only; "
        "Confirm and Write uses the button click as confirmation and closes immediately."
    )
    intro.setWordWrap(True)
    layout.addWidget(intro)
    mode_group = QGroupBox("Auto-fill mode")
    mode_group.setObjectName("freeze_formulary_mode_group")
    mode_layout = QGridLayout(mode_group)
    mode_layout.setColumnStretch(3, 1)
    heuristic_radio = QRadioButton("Heuristic")
    local_ai_radio = QRadioButton("Local AI")
    web_ai_radio = QRadioButton("Web AI")
    heuristic_radio.setObjectName("freeze_formulary_mode_heuristic")
    local_ai_radio.setObjectName("freeze_formulary_mode_local_ai")
    web_ai_radio.setObjectName("freeze_formulary_mode_web_ai")
    heuristic_radio.setChecked(True)
    mode_status_label = QLabel(
        "Heuristic selected. Deterministic intake and validation remain authoritative."
    )
    mode_status_label.setWordWrap(True)
    web_config_summary_label = QLabel("AI configuration is managed in Config AI.")
    web_config_summary_label.setObjectName("freeze_formulary_web_config_summary")
    web_config_summary_label.setWordWrap(True)
    open_config_web_ai_button = QPushButton("Open Config AI")
    open_config_web_ai_button.setObjectName("freeze_formulary_open_config_web_ai")
    mode_layout.addWidget(heuristic_radio, 0, 0)
    mode_layout.addWidget(local_ai_radio, 0, 1)
    mode_layout.addWidget(web_ai_radio, 0, 2)
    mode_layout.addWidget(open_config_web_ai_button, 0, 3)
    mode_layout.addWidget(mode_status_label, 1, 0, 1, 4)
    mode_layout.addWidget(web_config_summary_label, 2, 0, 1, 4)
    layout.addWidget(mode_group, 0)
    form_group = QGroupBox("Freeze entry fields")
    form_layout = QGridLayout(form_group)
    form_layout.setColumnStretch(1, 1)
    feature_title_edit = QLineEdit()
    feature_title_edit.setPlaceholderText("Example: Local Freeze Writer Contract v1.1")
    primary_box_edit = QLineEdit()
    primary_box_edit.setPlaceholderText("Example: kanda_reasoner_app/freeze_after_update/contract.py")
    box_type_edit = QLineEdit("Module Box")
    validated_files_edit = QTextEdit()
    validated_files_edit.setPlaceholderText("One project-relative validated file per line")
    generated_files_edit = QTextEdit()
    generated_files_edit.setPlaceholderText("Optional: one generated file per line")
    protected_paths_edit = QTextEdit()
    protected_paths_edit.setPlaceholderText("One protected project-relative path per line")
    do_not_regress_edit = QTextEdit()
    do_not_regress_edit.setPlaceholderText("One do-not-regress rule per line")
    validation_evidence_edit = QTextEdit()
    validation_evidence_edit.setPlaceholderText(
        "Paste validation output. Must include a marker such as VALIDATION OK, INSTALL OK, "
        "py_compile passed, validator passed, or STATUS: IN_SYNC."
    )
    known_warnings_edit = QTextEdit()
    known_warnings_edit.setPlaceholderText("Optional warnings")
    planned_next_step_edit = QTextEdit()
    planned_next_step_edit.setPlaceholderText("Optional planned next step")
    notes_edit = QTextEdit()
    notes_edit.setPlaceholderText("Optional summary/notes")
    for editor in [
        validated_files_edit,
        generated_files_edit,
        protected_paths_edit,
        do_not_regress_edit,
        validation_evidence_edit,
        known_warnings_edit,
        planned_next_step_edit,
        notes_edit,
    ]:
        editor.setMaximumHeight(86)
    row = 0
    form_layout.addWidget(QLabel("Feature title:"), row, 0)
    form_layout.addWidget(feature_title_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Primary box:"), row, 0)
    form_layout.addWidget(primary_box_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Box type:"), row, 0)
    form_layout.addWidget(box_type_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Validated files:"), row, 0)
    form_layout.addWidget(validated_files_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Generated files:"), row, 0)
    form_layout.addWidget(generated_files_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Protected paths:"), row, 0)
    form_layout.addWidget(protected_paths_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Do-not-regress rules:"), row, 0)
    form_layout.addWidget(do_not_regress_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Validation evidence:"), row, 0)
    form_layout.addWidget(validation_evidence_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Known warnings:"), row, 0)
    form_layout.addWidget(known_warnings_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Planned next step:"), row, 0)
    form_layout.addWidget(planned_next_step_edit, row, 1)
    row += 1
    form_layout.addWidget(QLabel("Notes:"), row, 0)
    form_layout.addWidget(notes_edit, row, 1)
    layout.addWidget(form_group, 0)
    preview_group = QGroupBox("Preview and validation")
    preview_layout = QVBoxLayout(preview_group)
    preview_text_edit = QTextEdit()
    preview_text_edit.setReadOnly(True)
    preview_text_edit.setPlaceholderText("Click Preview Freeze Entry to generate a read-only local freeze preview.")
    preview_layout.addWidget(preview_text_edit, 1)
    layout.addWidget(preview_group, 1)
    button_row = QHBoxLayout()
    autofill_button = QPushButton("Fill Form Now")
    copy_to_ai_button = QPushButton("Copy Formulary to AI")
    receive_from_ai_button = QPushButton("Receive Formulary from AI")
    preview_button = QPushButton("Preview Freeze Entry")
    confirm_write_button = QPushButton("Confirm and Write Freeze Entry")
    ignore_freeze_button = QPushButton("Ignore this Freeze")
    cancel_button = QPushButton("Cancel")
    confirm_write_button.setStyleSheet(disabled_action_style)
    ignore_freeze_button.setStyleSheet(disabled_action_style)
    confirm_write_button.setEnabled(False)
    ignore_freeze_button.setEnabled(False)
    confirm_write_button.setToolTip("Preview and validate a writable freeze entry before confirming.")
    ignore_freeze_button.setToolTip("No current writable freeze draft is available to ignore.")
    copy_to_ai_button.setToolTip("Copy a strict review prompt with the current auto-filled freeze form for an AI specialist")
    receive_from_ai_button.setToolTip("Paste the strict AI JSON answer and apply it back into this form")
    autofill_button.setToolTip("Fill using Heuristic, Local AI, or the central Config Web AI selection.")
    button_row.addWidget(autofill_button)
    button_row.addWidget(copy_to_ai_button)
    button_row.addWidget(receive_from_ai_button)
    button_row.addWidget(preview_button)
    button_row.addWidget(confirm_write_button)
    button_row.addWidget(ignore_freeze_button)
    button_row.addStretch(1)
    button_row.addWidget(cancel_button)
    layout.addLayout(button_row)
    return LocalFreezeDialogWidgets(
        dialog=dialog,
        heuristic_radio=heuristic_radio,
        local_ai_radio=local_ai_radio,
        web_ai_radio=web_ai_radio,
        mode_status_label=mode_status_label,
        web_config_summary_label=web_config_summary_label,
        open_config_web_ai_button=open_config_web_ai_button,
        feature_title_edit=feature_title_edit,
        primary_box_edit=primary_box_edit,
        box_type_edit=box_type_edit,
        validated_files_edit=validated_files_edit,
        generated_files_edit=generated_files_edit,
        protected_paths_edit=protected_paths_edit,
        do_not_regress_edit=do_not_regress_edit,
        validation_evidence_edit=validation_evidence_edit,
        known_warnings_edit=known_warnings_edit,
        planned_next_step_edit=planned_next_step_edit,
        notes_edit=notes_edit,
        preview_text_edit=preview_text_edit,
        autofill_button=autofill_button,
        copy_to_ai_button=copy_to_ai_button,
        receive_from_ai_button=receive_from_ai_button,
        preview_button=preview_button,
        confirm_write_button=confirm_write_button,
        ignore_freeze_button=ignore_freeze_button,
        cancel_button=cancel_button,
    )
