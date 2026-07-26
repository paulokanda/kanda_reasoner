# project-path: kanda_reasoner_app/error_memory_gui/error_memory_tab.py
"""Error Memory GUI tab with AI-assisted intake and editable lessons."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from kanda_reasoner_app.error_memory_gui._intake_actions_mixin import (
    ErrorMemoryIntakeActionsMixin,
    PENDING_AI_ASSISTED_INTAKE_DIR_NAME,
    PENDING_AI_ASSISTED_INTAKE_SUFFIXES,
)
from kanda_reasoner_app.error_memory_gui._project_paths_mixin import ErrorMemoryProjectPathsMixin
from kanda_reasoner_app.error_memory_gui._table_draft_mixin import ErrorMemoryTableDraftMixin
from kanda_reasoner_app.error_memory_gui._text_payloads import (
    json_payload_from_text,
    lesson_id_from_text_lenient,
    operation_phase_from_editor_texts,
    pending_file_updated_text,
    summary_from_pending_raw_text,
    text_has_formatted_lesson_payload,
    validation_evidence_is_passing,
)
from kanda_reasoner_app.error_memory_gui._pending_sources import (
    candidate_pending_ai_assisted_intake_dirs,
    delete_matching_pending_intake_files,
    pending_file_matches_draft_identity,
    pending_intake_dirs_for_root_hint,
    pending_intake_files_for_candidate_dirs,
    safe_pending_lesson_id_from_file,
)
from kanda_reasoner_app.error_memory_gui._lesson_payloads import (
    canonical_draft_lesson_from_partial,
    lesson_from_formatted_text,
    text_is_formatted_error_lesson_payload,
)
from kanda_reasoner_app.error_memory_gui._lesson_imports import (
    formatted_import_text_for_window,
    formatted_text_from_manifested_lesson_zip,
)
from kanda_reasoner_app.error_memory_gui._intake_blueprint import (
    error_lesson_intake_blueprint_clipboard_text,
    error_memory_prompt_template_dir,
    read_error_memory_intake_template_file,
)
from kanda_reasoner_app.error_memory_gui._project_roots import (
    existing_directory_from_text,
    source_root_from_directory_hint,
    source_root_peer_from_generated_output,
)
from kanda_reasoner_app.error_memory_gui._pending_rows import (
    draft_lesson_from_pending_raw_text,
    pending_lesson_rows_for_table,
)
from kanda_reasoner_app.error_memory_gui._draft_deletion import (
    delete_matching_canonical_draft_lessons,
    draft_delete_identity_from_sources,
)
from kanda_reasoner_app.error_memory_gui._lesson_actions import (
    delete_selected_lesson,
    lesson_from_preview_or_selection,
    save_draft_lesson_from_partial,
    save_preview_lesson,
    set_selected_lesson_status,
    supersede_selected_lesson,
    undo_lesson_action,
)
from kanda_reasoner_app.error_memory_gui._memorize_flow import (
    candidate_text_for_memorize,
    clear_ai_assisted_intake_after_memorize,
    consume_loaded_pending_intake_file_if_matches,
    memorize_error_from_text_window,
    save_active_ready_lesson,
    select_saved_active_lesson_row,
)
from kanda_reasoner_app.error_memory_gui._clipboard_export import (
    copy_ai_assisted_intake_error_draft_to_clipboard,
    copy_complete_error_memory_json_to_clipboard,
    copy_correct_error_delivery_canon_to_clipboard,
    copy_error_draft_to_clipboard,
    copy_error_lesson_intake_blueprint_to_clipboard,
    copy_path_to_clipboard,
    export_for_ai,
    show_action_done,
    show_active_ready_failure_copy_window,
)
from kanda_reasoner_app.error_memory_gui._correction_guard import (
    active_ready_missing_text,
    apply_heuristic_correction_to_error_editor,
    check_against_lessons,
    heuristic_correction_result_for_editor,
    operation_phase_for_guard,
    refresh_heuristic_correction_button_state,
    show_repeat_guard_report,
)
from kanda_reasoner_app.error_memory_gui._table_view import (
    formatted_lesson_block,
    lesson_id_for_row,
    lesson_json_text_for_windows,
    load_selected_lesson_into_preview,
    pending_path_for_row,
    reload_table,
    row_kind_for_row,
    selected_lesson_id_from_table,
    set_ai_assisted_intake_and_error_editor_from_pending_text,
)
from kanda_reasoner_app.error_memory_gui._pending_loader import (
    delete_pending_file_quietly,
    lesson_id_exists_in_lessons,
    load_pending_ai_assisted_error_lesson_intake,
    load_pending_ai_assisted_error_lesson_intake_now,
    load_pending_intake_row_into_editor,
    show_duplicate_pending_intake_warning,
)
from kanda_reasoner_app.error_memory_gui._receive_import import (
    import_error_lesson_zip,
    receive_formulary_from_ai,
)
from kanda_reasoner_app.error_memory_gui._portable_transfer import (
    export_errors_from_tab,
    import_errors_into_tab,
)
from kanda_reasoner_app.error_memory_gui._pending_live_refresh import (
    initialize_pending_intake_live_refresh,
    refresh_pending_intake_live,
)
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog, QGroupBox, QLineEdit, QHBoxLayout, QLabel, QMessageBox, QPushButton, QPlainTextEdit, QSplitter, QTableWidget, QVBoxLayout, QWidget
from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root, resolve_second_prompt_files_root
from kanda_reasoner_app.error_memory.store import bootstrap_error_memory_store, delete_lesson, list_lessons, rebuild_index, save_lesson
from kanda_reasoner_app.templates.floating_windows import show_copy_message_window
ERROR_MEMORY_ROW_KIND_ROLE = Qt.UserRole + 1
ERROR_MEMORY_PENDING_PATH_ROLE = Qt.UserRole + 2

__all__ = [
    'ERROR_MEMORY_PENDING_PATH_ROLE',
    'ERROR_MEMORY_ROW_KIND_ROLE',
    'ErrorMemoryTab',
]

class ErrorMemoryTab(ErrorMemoryProjectPathsMixin, ErrorMemoryTableDraftMixin, ErrorMemoryIntakeActionsMixin, QWidget):
    """GUI for project-specific Error Memory lessons and AI formulary intake."""

    def __init__(self) -> None:
        """Support init behavior.
        """
        
        super().__init__()
        self._project_root = Path.cwd()
        self._last_received_lesson: dict[str, Any] | None = None
        self._selected_lesson_id = ''
        self._undo_deleted_lesson: dict[str, Any] | None = None
        self._loaded_pending_intake_file = ''
        self._loaded_pending_intake_lesson_id = ''
        self._dismissed_pending_intake_files: set[str] = set()
        self._dismissed_pending_intake_lesson_ids: set[str] = set()
        self._warned_duplicate_pending_intake_lesson_ids: set[str] = set()
        self._last_dismissed_pending_intake_file = ''
        self._last_dismissed_pending_intake_lesson_id = ''
        self._last_dismissed_pending_intake_text = ''
        self._syncing_project_root_field = False
        self._error_memory_ai_correction_generation = 0
        self._build_ui()
        self._refresh_paths()
        QTimer.singleShot(0, self.load_pending_ai_assisted_error_lesson_intake_now)
        QTimer.singleShot(250, self.load_pending_ai_assisted_error_lesson_intake_now)
        initialize_pending_intake_live_refresh(self)
        self._pending_intake_live_refresh_timer = QTimer(self)
        self._pending_intake_live_refresh_timer.setInterval(500)
        self._pending_intake_live_refresh_timer.timeout.connect(self._refresh_pending_intake_live)
        self._pending_intake_live_refresh_timer.start()

    def _build_ui(self) -> None:
        """Support build ui behavior.
        """
        
        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(10)
        self._project_root_controls_moved = False
        self.project_root_header_label = QLabel('Project Root:')
        self.project_root_header_label.setStyleSheet('color: #0B3D91; font-weight: bold;')
        self.project_root_value_label = QLineEdit(str(self._project_root))
        self.project_root_value_label.setObjectName('error_memory_project_root_edit')
        self.project_root_value_label.setReadOnly(True)
        self.project_root_value_label.setPlaceholderText('Project root')
        self.project_root_value_label.setMinimumWidth(180)
        self.project_root_value_label.setMaximumWidth(320)
        self.project_root_edit = self.project_root_value_label
        self.project_root_value_label.textChanged.connect(self._on_project_root_field_changed)
        self.search_project_button = QPushButton('browse project folder')
        self.open_memory_button = QPushButton('Open EM Folder')
        self.open_second_prompt_button = QPushButton('Open Second Prompt Files')
        self.copy_memory_path_button = QPushButton('Get path to EM Folder')
        self.copy_second_prompt_path_button = QPushButton('Get path to Second Prompt Files')
        self.copy_correct_error_delivery_button = QPushButton('Get correct way to send me errors')
        self.copy_correct_error_delivery_button.setStyleSheet('color: #FF8C00; font-weight: bold;')
        path_action_row = QHBoxLayout()
        path_action_row.addWidget(self.open_memory_button)
        path_action_row.addWidget(self.open_second_prompt_button)
        path_action_row.addWidget(self.copy_memory_path_button)
        path_action_row.addWidget(self.copy_second_prompt_path_button)
        path_action_row.addWidget(self.copy_correct_error_delivery_button)
        path_action_row.addStretch(1)
        outer.addLayout(path_action_row)
        splitter = QSplitter(Qt.Horizontal)
        outer.addWidget(splitter, 1)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        splitter.addWidget(left)
        right = QWidget()
        right_layout = QVBoxLayout(right)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        intake_box = QGroupBox('AI-assisted error lesson intake')
        intake_layout = QVBoxLayout(intake_box)
        help_label = QLabel('Paste raw error/context, import an AI-created formatted Error Lesson ZIP, or paste AI formatted JSON. Operation phase is metadata stored inside the formatted lesson JSON, not a manual chooser.')
        help_label.setWordWrap(True)
        intake_layout.addWidget(help_label)
        self.raw_error_edit = QPlainTextEdit()
        self.raw_error_edit.setPlaceholderText('Raw error, draft text, or formatted AI lesson appears here. Import Error Lesson ZIP and Paste error formatted from AI may fill this automatically. Memorize Error saves active-ready lessons as active. Draft lessons must use Mark Draft or AI correction before active promotion.')
        intake_layout.addWidget(self.raw_error_edit, 1)
        intake_buttons_1 = QHBoxLayout()
        self.receive_formulary_button = QPushButton('Paste error formatted from AI')
        self.copy_ai_assisted_intake_error_draft_button = QPushButton('Copy error/draft')
        self.clean_intake_button = QPushButton('Clean')
        self.delete_draft_button = QPushButton('Del Draft')
        intake_buttons_1.addWidget(self.receive_formulary_button)
        intake_buttons_1.addWidget(self.copy_ai_assisted_intake_error_draft_button)
        intake_buttons_1.addWidget(self.clean_intake_button)
        intake_buttons_1.addWidget(self.delete_draft_button)
        intake_buttons_1.addStretch(1)
        intake_layout.addLayout(intake_buttons_1)
        intake_buttons_2 = QHBoxLayout()
        self.memorize_error_button = QPushButton('Memorize Error')
        self.import_zip_button = QPushButton('Import Error Lesson ZIP')
        intake_buttons_2.addWidget(self.memorize_error_button)
        intake_buttons_2.addWidget(self.import_zip_button)
        intake_layout.addLayout(intake_buttons_2)
        intake_buttons_3 = QHBoxLayout()
        self.check_against_lessons_button = QPushButton('Check Against Lessons')
        self.copy_error_lesson_intake_blueprint_button = QPushButton('Copy Error Lesson Intake blueprint')
        intake_buttons_3.addWidget(self.check_against_lessons_button)
        intake_buttons_3.addWidget(self.copy_error_lesson_intake_blueprint_button)
        intake_buttons_3.addStretch(1)
        intake_layout.addLayout(intake_buttons_3)
        self.receive_formulary_button.setToolTip("Paste AI's formatted Error Memory JSON block; KANDA loads it into the intake window and Error Editor without saving until Memorize Error.")
        self.copy_ai_assisted_intake_error_draft_button.setToolTip('Copy the current AI-assisted intake text plus the active-ready Error Memory templates so AI can correct or create valid intake JSON.')
        self.clean_intake_button.setToolTip('Clear both AI-assisted intake and Error Editor. It remembers the dismissed pending source for this session, but it does not delete disk-backed drafts.')
        self.delete_draft_button.setToolTip('Delete the current Error Memory draft completely: AI-assisted intake, Error Editor, pending source files, matching draft Lessons row, and stale index entry.')
        self.memorize_error_button.setToolTip('Save the formatted lesson currently shown in Error Editor/intake only when it is active-ready. Draft lessons use Mark Draft, or AI correction before Mark Active.')
        self.import_zip_button.setToolTip('Load an AI-created formatted Error Lesson ZIP/JSON/text file into the intake window and Error Editor. It is not saved until Memorize Error.')
        self.check_against_lessons_button.setToolTip('Check whether the current error/draft already exists in the Error Memory lesson library. Advisory only; no hard block.')
        self.copy_error_lesson_intake_blueprint_button.setToolTip('Copy the active-ready Error Memory AI intake instructions and model template. Paste this to AI when asking it to create text for the AI-assisted error lesson intake window.')
        left_layout.addWidget(intake_box, 2)
        preview_box = QGroupBox('Error Editor')
        preview_layout = QVBoxLayout(preview_box)
        from kanda_reasoner_app.error_memory_gui import _ai_mode_runtime

        _ai_mode_runtime.initialize_mode_controls(self)
        preview_layout.addWidget(_ai_mode_runtime.build_mode_group(self))
        self.received_preview_edit = QPlainTextEdit()
        self.received_preview_edit.setReadOnly(False)
        self.received_preview_edit.setPlaceholderText('After Paste error formatted from AI, Import Error Lesson ZIP, or clicking a lesson, the canonical lesson JSON appears here. Edit here if needed, then click Memorize Error for active-ready lessons, Mark Draft for draft preservation, or Save for direct JSON save.')
        preview_layout.addWidget(self.received_preview_edit, 1)
        preview_buttons = QHBoxLayout()
        self.save_preview_button = QPushButton('Save')
        self.copy_error_draft_button = QPushButton('Copy error/draft')
        self.clean_editor_button = QPushButton('Clean')
        self.undo_button = QPushButton('Undo')
        self.delete_button = QPushButton('Delete')
        self.export_errors_button = QPushButton('Export Errors')
        self.import_errors_button = QPushButton('Import Errors')
        self.export_button = QPushButton('Lessons to Clipboard')
        self.export_errors_button.setObjectName('error_memory_export_errors_button')
        self.import_errors_button.setObjectName('error_memory_import_errors_button')
        self.save_preview_button.setToolTip('Save the JSON currently shown in Error Editor into the canonical lesson store.')
        self.copy_error_draft_button.setToolTip('Copy the current Error Editor text plus the active-ready Error Memory templates so AI can correct or create valid intake JSON.')
        self.clean_editor_button.setToolTip('Clear both Error Editor and AI-assisted intake.')
        self.undo_button.setToolTip('Restore the most recently deleted lesson, or reload the selected lesson if nothing was deleted.')
        self.delete_button.setToolTip('Delete the selected lesson from the canonical Error Memory store. Undo is available until another delete.')
        self.export_errors_button.setToolTip('Choose a folder and save a portable copy of every valid lesson from the current project, including inactive lessons.')
        self.import_errors_button.setToolTip('Choose a KANDA Error Memory export folder and merge only unique validated lessons into the current project. Current lessons are never deleted or replaced.')
        self.export_button.setToolTip('Copy the complete Error Memory JSON payload to the clipboard. This button does not copy the second_prompt_files path.')
        preview_buttons.addWidget(self.save_preview_button)
        preview_buttons.addWidget(self.copy_error_draft_button)
        preview_buttons.addWidget(self.clean_editor_button)
        preview_buttons.addWidget(self.undo_button)
        preview_buttons.addWidget(self.delete_button)
        preview_buttons.addWidget(self.export_errors_button)
        preview_buttons.addWidget(self.import_errors_button)
        preview_buttons.addWidget(self.export_button)
        preview_buttons.addStretch(1)
        preview_layout.addLayout(preview_buttons)
        status_buttons = QHBoxLayout()
        self.mark_draft_button = QPushButton('Mark Draft')
        self.mark_active_button = QPushButton('Mark Active')
        self.deprecate_button = QPushButton('Deprecate')
        self.supersede_button = QPushButton('Supersede')
        self.heuristic_correction_button = QPushButton('Need AI to Correct')
        self.heuristic_correction_button.setVisible(False)
        self.correct_with_ai_button = QPushButton('Correct with AI')
        self.correct_with_ai_button.setStyleSheet('QPushButton { color: #187a2f; font-weight: 700; }')
        self.mark_draft_button.setToolTip('Set selected lesson status to draft and save it.')
        self.mark_active_button.setToolTip('Promote selected lesson to active only when required fields and validation evidence are present.')
        self.deprecate_button.setToolTip('Set selected lesson status to deprecated so it is kept but excluded from active exports.')
        self.supersede_button.setToolTip('Set selected lesson status to superseded and record the replacement lesson ID.')
        self.heuristic_correction_button.setToolTip('Locked unless deterministic Level 1 structural normalization is possible for the current Error Editor JSON. It never invents root cause, correction, prevention rules, or validation evidence.')
        self.correct_with_ai_button.setToolTip('Run the selected correction engine in a background worker and load the result as preview only. This action does not save, delete, activate, supersede, or memorize lessons.')
        status_buttons.addWidget(self.mark_draft_button)
        status_buttons.addWidget(self.mark_active_button)
        status_buttons.addWidget(self.deprecate_button)
        status_buttons.addWidget(self.supersede_button)
        status_buttons.addWidget(self.heuristic_correction_button)
        status_buttons.addWidget(self.correct_with_ai_button)
        status_buttons.addStretch(1)
        preview_layout.addLayout(status_buttons)
        right_layout.addWidget(preview_box, 2)
        list_box = QGroupBox('Lessons')
        list_layout = QVBoxLayout(list_box)
        self.lesson_status_summary_layout = QHBoxLayout()
        self.lesson_status_summary_layout.setSpacing(6)
        list_layout.addLayout(self.lesson_status_summary_layout)
        self.lessons_table = QTableWidget(0, 5)
        self.lessons_table.setHorizontalHeaderLabels(['Status', 'Symptom', 'Do-not-repeat rule', 'Updated', 'Lesson ID'])
        self.lessons_table.setToolTip('Saved lessons and pending intake files waiting for edition. Pending rows are virtual until the user saves them with Memorize Error, Mark Draft, or another explicit action.')
        self.lessons_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.lessons_table.setSelectionMode(QTableWidget.SingleSelection)
        self.lessons_table.setEditTriggers(QTableWidget.NoEditTriggers)
        list_layout.addWidget(self.lessons_table, 1)
        right_layout.addWidget(list_box, 2)
        self.search_project_button.clicked.connect(self._search_project_root)
        self.open_memory_button.clicked.connect(lambda: self._open_folder(resolve_project_error_memory_root(self._project_root)))
        self.open_second_prompt_button.clicked.connect(lambda: self._open_folder(resolve_second_prompt_files_root(self._project_root)))
        self.copy_memory_path_button.clicked.connect(lambda: self._copy_path_to_clipboard(resolve_project_error_memory_root(self._project_root), 'Error Memory folder'))
        self.copy_second_prompt_path_button.clicked.connect(lambda: self._copy_path_to_clipboard(resolve_second_prompt_files_root(self._project_root), 'Second Prompt Files'))
        self.copy_correct_error_delivery_button.clicked.connect(lambda: copy_correct_error_delivery_canon_to_clipboard(self))
        self.copy_error_draft_button.clicked.connect(self._copy_error_draft_to_clipboard)
        self.copy_ai_assisted_intake_error_draft_button.clicked.connect(self._copy_ai_assisted_intake_error_draft_to_clipboard)
        self.heuristic_correction_button.clicked.connect(self._apply_heuristic_correction_to_error_editor)
        self.correct_with_ai_button.clicked.connect(self._correct_with_ai_from_error_memory_tab)
        _ai_mode_runtime.wire_mode_controls(self)
        self.receive_formulary_button.clicked.connect(self._receive_formulary_from_ai)
        self.clean_intake_button.clicked.connect(self._clean_intake_window)
        self.delete_draft_button.clicked.connect(self._delete_current_draft_completely)
        self.memorize_error_button.clicked.connect(self._memorize_error_from_text_window)
        self.import_zip_button.clicked.connect(self._import_error_lesson_zip)
        self.check_against_lessons_button.clicked.connect(self._check_against_lessons)
        self.copy_error_lesson_intake_blueprint_button.clicked.connect(self._copy_error_lesson_intake_blueprint_to_clipboard)
        self.export_errors_button.clicked.connect(lambda: export_errors_from_tab(self))
        self.import_errors_button.clicked.connect(lambda: import_errors_into_tab(self))
        self.export_button.clicked.connect(self._export_for_ai)
        self.save_preview_button.clicked.connect(self._save_preview_lesson)
        self.clean_editor_button.clicked.connect(self._clean_error_editor)
        self.undo_button.clicked.connect(self._undo_lesson_action)
        self.delete_button.clicked.connect(self._delete_selected_lesson)
        self.mark_draft_button.clicked.connect(lambda: self._set_selected_lesson_status('draft'))
        self.mark_active_button.clicked.connect(lambda: self._set_selected_lesson_status('active'))
        self.deprecate_button.clicked.connect(lambda: self._set_selected_lesson_status('deprecated'))
        self.supersede_button.clicked.connect(self._supersede_selected_lesson)
        self.received_preview_edit.textChanged.connect(self._refresh_heuristic_correction_button_state)
        self.raw_error_edit.textChanged.connect(self._refresh_heuristic_correction_button_state)
        self.lessons_table.itemSelectionChanged.connect(self._load_selected_lesson_into_preview)
        self._refresh_heuristic_correction_button_state()

    def _correct_with_ai_from_error_memory_tab(self) -> None:
        """Run the local AI correction workflow from the in-tab action row."""
        from kanda_reasoner_app.error_memory_gui._ai_correction_action import (
            run_error_memory_ai_correction_from_tab,
        )

        run_error_memory_ai_correction_from_tab(self)


    def showEvent(self, event) -> None:
        """Refresh pending AI-assisted intake when the tab becomes visible."""
        super().showEvent(event)
        self._refresh_paths()
        QTimer.singleShot(0, self.load_pending_ai_assisted_error_lesson_intake_now)
        QTimer.singleShot(250, self.load_pending_ai_assisted_error_lesson_intake_now)

    def _refresh_pending_intake_live(self) -> bool:
        """Load newly staged Error Memory intake without restarting the app."""
        return refresh_pending_intake_live(self)


    def run_ai_review_first_check(self) -> None:
        """Copy the Error Memory AI intake blueprint from the header action."""
        self._copy_error_lesson_intake_blueprint_to_clipboard()


    def move_project_root_controls_to_layout(self, target_layout: QHBoxLayout, insert_index: int | None=None) -> None:
        """Move only Project Root controls into the tab header template."""
        if self._project_root_controls_moved:
            return
        controls = [
            self.project_root_header_label,
            self.project_root_value_label,
            self.search_project_button,
        ]
        if insert_index is None:
            target_layout.addSpacing(24)
            for control in controls:
                target_layout.addWidget(control, 0)
        else:
            current_index = insert_index
            target_layout.insertSpacing(current_index, 24)
            current_index += 1
            for control in controls:
                target_layout.insertWidget(current_index, control, 0)
                current_index += 1
        self._project_root_controls_moved = True

























    def _operation_phase_from_editor_or_unknown(self) -> str:
        """Return operation_phase from Error Editor JSON when available."""
        return operation_phase_from_editor_texts(
            self.received_preview_edit.toPlainText(),
            self.raw_error_edit.toPlainText(),
        )












    def _refresh_heuristic_correction_button_state(self) -> None:
        """Support refresh heuristic correction button state behavior.
        """
        
        refresh_heuristic_correction_button_state(self)
        from kanda_reasoner_app.error_memory_gui import _ai_mode_runtime

        _ai_mode_runtime.sync_mode_controls(self)
