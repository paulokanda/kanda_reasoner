# project-path: kanda_reasoner_app/freeze_after_update_gui/_ui_builder.py
"""Widget construction and signal wiring for the Freeze tab."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

__all__ = ["FreezeUiBuilderMixin"]


class FreezeUiBuilderMixin:
    """Build and connect the top-level Freeze Feature After Update UI."""

    def _build_ui(self) -> None:
        """Support build ui behavior.
        """
        
        self.setMinimumSize(0, 0)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.freeze_screen_scroll = QScrollArea(self)
        self.freeze_screen_scroll.setObjectName("freeze_after_update_screen_scroll")
        self.freeze_screen_scroll.setWidgetResizable(True)
        self.freeze_screen_scroll.setMinimumSize(0, 0)

        scroll_body = QWidget(self.freeze_screen_scroll)
        scroll_body.setObjectName("freeze_after_update_screen_scroll_body")
        content_layout = QVBoxLayout(scroll_body)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(10)
        self.freeze_screen_scroll.setWidget(scroll_body)
        root_layout.addWidget(self.freeze_screen_scroll, 1)
        self.help_button = QPushButton("Help")
        self.help_button.setToolTip("Open practical help for the Freeze Feature After Update tab")
        self.get_last_freeze_button = QPushButton("Get Last Freeze")
        self.get_last_freeze_button.setToolTip("Copy the latest frozen feature entry snippet for pasting to AI")
        self.get_last_freeze_button.setStyleSheet("color: #008000; font-weight: bold;")
        self.get_all_frozen_button = QPushButton("Get All Frozen")
        self.get_all_frozen_button.setToolTip("Copy all frozen feature entry snippets for pasting to AI")
        self.get_all_frozen_button.setStyleSheet("color: #003366; font-weight: bold;")
        self.get_blueprint_freeze_button = QPushButton("Get Blueprint Freeze")
        self.get_blueprint_freeze_button.setToolTip(
            "Copy the audited generic receive-ready KANDA freeze blueprint for AI"
        )
        self.get_blueprint_freeze_button.setStyleSheet("color: #FF8C00; font-weight: bold;")
        self.list_frozen_button = QPushButton("List Frozen")
        self.list_frozen_button.setObjectName("freeze_after_update_list_frozen_button")
        self.list_frozen_button.setToolTip("Open the floating frozen-entry status and management window")
        self.list_frozen_button.setStyleSheet("color: #0057B8; font-weight: bold;")
        self.send_zip_freeze_button = QPushButton("Send zip freeze")
        self.send_zip_freeze_button.setObjectName("freeze_after_update_send_zip_freeze_button")
        self.send_zip_freeze_button.setToolTip(
            "Copy the canonical self-contained freeze-entry intake ZIP prompt"
        )
        self.send_zip_freeze_button.setStyleSheet("color: #FF8C00; font-weight: bold;")
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(12)
        content_layout.addLayout(columns_layout, 1)
        left_column_widget = QWidget()
        left_column_widget.setMinimumSize(0, 0)
        left_column_widget.setSizePolicy(
            QSizePolicy.Ignored,
            QSizePolicy.Expanding,
        )
        left_column = QVBoxLayout(left_column_widget)
        left_column.setContentsMargins(0, 0, 0, 0)
        left_column.setSpacing(10)
        right_column_widget = QWidget()
        right_column_widget.setMinimumSize(0, 0)
        right_column_widget.setSizePolicy(
            QSizePolicy.Ignored,
            QSizePolicy.Expanding,
        )
        right_column = QVBoxLayout(right_column_widget)
        right_column.setContentsMargins(0, 0, 0, 0)
        right_column.setSpacing(10)
        columns_layout.addWidget(left_column_widget, 1)
        columns_layout.addWidget(right_column_widget, 1)
        intro = QLabel(
            "Prepare or execute the project-local freeze / AI-compliance flow after a validated update. "
            "Normal freezing happens locally through preview and human confirmation. External AI review export "
            "remains available as an advanced fallback. Frozen memory stays inside the actual project."
        )
        intro.setWordWrap(True)
        left_column.addWidget(intro)
        freeze_copy_grid = QGridLayout()
        freeze_copy_grid.setContentsMargins(0, 0, 0, 0)
        freeze_copy_grid.setHorizontalSpacing(8)
        freeze_copy_grid.setVerticalSpacing(6)
        freeze_copy_grid.addWidget(self.get_last_freeze_button, 0, 0)
        freeze_copy_grid.addWidget(self.get_all_frozen_button, 0, 1)
        freeze_copy_grid.addWidget(self.get_blueprint_freeze_button, 0, 2)
        self.list_frozen_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.send_zip_freeze_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        freeze_copy_grid.addWidget(self.list_frozen_button, 0, 3)
        freeze_copy_grid.addWidget(self.send_zip_freeze_button, 0, 4)
        freeze_copy_grid.setColumnStretch(0, 1)
        freeze_copy_grid.setColumnStretch(1, 1)
        freeze_copy_grid.setColumnStretch(2, 1)
        left_column.addLayout(freeze_copy_grid)
        self.project_root_header_label = QLabel("Project Root:")
        self.project_root_header_label.setStyleSheet("color: #0B3D91; font-weight: bold; padding-left: 4px;")
        self.project_root_edit = QLineEdit()
        self.project_root_edit.setObjectName("freeze_after_update_project_root_edit")
        self.project_root_edit.setPlaceholderText("Project root")
        self.project_root_edit.setMinimumWidth(180)
        self.project_root_edit.setMaximumWidth(320)
        self.search_project_button = QPushButton("Browse...")
        self.search_project_button.setToolTip("Select the active project root")
        self.choose_project_button = self.search_project_button
        self.box_folder_button = QPushButton("Box Folder")
        self.box_folder_button.setObjectName("freeze_after_update_box_folder_button")
        self.box_folder_button.setToolTip("Open the project_freeze_after_update box folder for the selected project root")
        self.box_folder_header_label = self.box_folder_button
        self.external_ai_review_folder_button = QPushButton("External AI Review Folder")
        self.external_ai_review_folder_button.setObjectName("freeze_after_update_external_ai_review_folder_button")
        self.external_ai_review_folder_button.setToolTip("Open the external AI review folder for the selected project root")
        self.external_ai_review_header_label = self.external_ai_review_folder_button
        path_buttons_row = QHBoxLayout()
        path_buttons_row.setContentsMargins(0, 0, 0, 0)
        path_buttons_row.setSpacing(8)
        path_buttons_row.addWidget(self.box_folder_button, 0)
        path_buttons_row.addWidget(self.external_ai_review_folder_button, 0)
        path_buttons_row.addStretch(1)
        left_column.addLayout(path_buttons_row)
        status_group = QGroupBox("Box status and repair")
        status_layout = QGridLayout(status_group)
        status_layout.setColumnStretch(1, 1)
        status_help = QLabel(
            "Check Box Status inspects the project-local freeze box and reports whether it is valid, missing, "
            "or incomplete. Create / Repair Box creates missing safe folder structure without writing frozen memory."
        )
        status_help.setWordWrap(True)
        status_layout.addWidget(status_help, 0, 0, 1, 3)
        status_layout.addWidget(QLabel("Status:"), 1, 0)
        self.status_label = QLabel("Not checked yet")
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label, 1, 1, 1, 2)
        self.check_button = QPushButton("Check Box Status")
        self.check_button.setToolTip("Inspect the selected project's freeze-after-update box and report missing/valid structure")
        self.create_button = QPushButton("Create / Repair Box")
        self.create_button.setToolTip("Create or repair missing project-local freeze-after-update folders without writing frozen memory")
        self.open_box_button = QPushButton("Open project_freeze_after_update")
        self.open_box_button.setToolTip("Open the selected project's freeze-after-update box folder")
        status_layout.addWidget(self.check_button, 2, 0)
        status_layout.addWidget(self.create_button, 2, 1)
        status_layout.addWidget(self.open_box_button, 2, 2)
        left_column.addWidget(status_group)
        staged_group = QGroupBox("Staged freeze / AI compliance action")
        staged_layout = QGridLayout(staged_group)
        staged_layout.setColumnStretch(1, 1)
        self.prepare_staged_action_button = QPushButton("Prepare Freeze / AI Compliance Update")
        self.do_staged_action_button = QPushButton("Do it")
        self.undo_staged_action_button = QPushButton("Undo / Cancel")
        self.do_staged_action_button.setEnabled(False)
        self.undo_staged_action_button.setEnabled(False)
        staged_help = QLabel(
            "Click Prepare first. The log will show exactly what will be read, written, refreshed, and not touched. "
            "Nothing changes until Do it."
        )
        staged_help.setWordWrap(True)
        staged_layout.addWidget(staged_help, 0, 0, 1, 3)
        staged_layout.addWidget(self.prepare_staged_action_button, 1, 0)
        staged_layout.addWidget(self.do_staged_action_button, 1, 1)
        staged_layout.addWidget(self.undo_staged_action_button, 1, 2)
        left_column.addWidget(staged_group)
        local_freeze_group = QGroupBox("Local freeze entry")
        local_freeze_layout = QGridLayout(local_freeze_group)
        local_freeze_layout.setColumnStretch(1, 1)
        local_freeze_help = QLabel(
            "Create a local freeze entry from this tab. Choose Heuristic, Local AI, or Web AI; Web settings come "
            "only from Config Web AI. Every mode produces a draft only. Preview remains read-only and Confirm and "
            "Write remains the explicit human authority."
        )
        local_freeze_help.setWordWrap(True)
        self.new_local_freeze_entry_button = QPushButton("Local Freeze Entry")
        self.new_local_freeze_entry_button.setToolTip("Open an auto-filled local freeze draft; review, preview, then confirm/write")
        self.new_local_freeze_entry_button.setStyleSheet("color: #008000; font-weight: bold;")
        local_freeze_layout.addWidget(local_freeze_help, 0, 0, 1, 2)
        local_freeze_layout.addWidget(self.new_local_freeze_entry_button, 1, 0)
        left_column.addWidget(local_freeze_group)
        left_column.addStretch(1)
        log_group = QGroupBox("Log window")
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(8, 8, 8, 8)
        log_layout.setSpacing(6)
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setPlaceholderText("Output log")
        log_layout.addWidget(self.output_log, 1)
        right_column.addWidget(log_group, 1)
        self._refresh_derived_paths()

    def _connect_signals(self) -> None:
        """Support connect signals behavior.
        """
        
        self.project_root_edit.textChanged.connect(self._refresh_derived_paths)
        self.choose_project_button.clicked.connect(self._choose_project_folder)
        self.check_button.clicked.connect(self._check_box_status)
        self.create_button.clicked.connect(self._create_or_repair_box)
        self.prepare_staged_action_button.clicked.connect(self._prepare_staged_freeze_action)
        self.do_staged_action_button.clicked.connect(self._do_staged_freeze_action)
        self.undo_staged_action_button.clicked.connect(self._undo_staged_freeze_action)
        self.new_local_freeze_entry_button.clicked.connect(self._open_local_freeze_entry_dialog)
        self.box_folder_button.clicked.connect(self._open_box_folder)
        self.external_ai_review_folder_button.clicked.connect(self._open_output_folder)
        self.open_box_button.clicked.connect(self._open_box_folder)
        self.help_button.clicked.connect(self._show_help_window)
        self.get_last_freeze_button.clicked.connect(self._copy_last_freeze_snippet)
        self.get_all_frozen_button.clicked.connect(self._copy_all_frozen_snippets)
        self.get_blueprint_freeze_button.clicked.connect(self._copy_freeze_form_blueprint)
        self.list_frozen_button.clicked.connect(self._show_frozen_list_window)
        self.send_zip_freeze_button.clicked.connect(self._copy_send_zip_freeze_prompt)
