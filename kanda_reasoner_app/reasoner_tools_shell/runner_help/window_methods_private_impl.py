"""Private window methods private impl helpers for reasoner_tools_shell.runner."""

from __future__ import annotations


def _bind_globals(namespace):
    """Bind runner.py globals for moved method bodies."""
    globals().update(namespace)

def _build_ui(self) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import QGroupBox, QRadioButton, QSplitter

    central = QWidget()
    self.setCentralWidget(central)
    main_layout = QVBoxLayout(central)

    self.tabs = QTabWidget()
    main_layout.addWidget(self.tabs)

    # ----- Show Project to AI tab: shared project root + first/second prompt columns -----
    collector_tab = QWidget()
    collector_layout = QVBoxLayout(collector_tab)

    project_root_row = QHBoxLayout()
    self.create_first_and_second_prompt_files_button = QPushButton("Create First and Second Prompt Files")
    combined_button_font = QFont()
    combined_button_font.setBold(True)
    self.create_first_and_second_prompt_files_button.setFont(combined_button_font)
    self.create_first_and_second_prompt_files_button.setStyleSheet("color: green; font-weight: bold;")
    project_root_row.addWidget(self.create_first_and_second_prompt_files_button)
    project_root_row.addWidget(QLabel("Project root:"))
    self.project_root_edit = QLineEdit(
        self._prefs.get("project_root", str(_DEFAULT_PROJECT_ROOT))
    )
    project_root_row.addWidget(self.project_root_edit)
    self.browse_project_button = QPushButton("Browse...")
    project_root_row.addWidget(self.browse_project_button)
    project_root_row.addWidget(QLabel("AI answer Routine Blueprint:"))
    self.copy_patch_validate_freeze_routine_button = QPushButton(
        "Copy Patch Validate Freeze Recovery Routine"
    )
    project_root_row.addWidget(self.copy_patch_validate_freeze_routine_button)
    project_root_row.addWidget(QLabel("Bridge List:"))
    self.copy_complete_bridge_list_button = QPushButton("Complete Bridge List")
    project_root_row.addWidget(self.copy_complete_bridge_list_button)
    collector_layout.addLayout(project_root_row)

    def _copy_patch_validate_freeze_recovery_routine() -> None:
        try:
            from pathlib import Path
            from PySide6.QtWidgets import QApplication

            raw_root = self.project_root_edit.text().strip()
            project_root = Path(raw_root).expanduser().resolve()
            prompt_rel = Path(
                "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
                "05_patch_delivery_and_validation/"
                "patch_validate_freeze_error_memory_routine_blueprint.md"
            )
            prompt_path = project_root / prompt_rel
            if not prompt_path.is_file():
                app_root = Path(__file__).resolve().parents[3]
                prompt_path = app_root / prompt_rel
            if not prompt_path.is_file():
                raise FileNotFoundError("Prompt not found: " + str(prompt_rel))
            QApplication.clipboard().setText(prompt_path.read_text(encoding="utf-8"))
            message = "Copied Patch Validate Freeze Recovery Routine"
            try:
                self.first_prompt_status_label.setText(message)
            except Exception:
                pass
            try:
                self._append_log(message)
            except Exception:
                pass
        except Exception as exc:
            message = "[ERROR] Could not copy Patch Validate Freeze Recovery Routine: " + str(exc)
            try:
                self.first_prompt_status_label.setText(message)
            except Exception:
                pass
            try:
                self._append_log(message)
            except Exception:
                pass

    self.copy_patch_validate_freeze_routine_button.clicked.connect(
        _copy_patch_validate_freeze_recovery_routine
    )

    try:
        from kanda_reasoner_app.reasoner_tools_shell.runner_help import complete_bridge_list_private_impl as _bridge_list_impl
        self.copy_complete_bridge_list_button.clicked.connect(
            lambda: _bridge_list_impl.copy_complete_bridge_list_to_clipboard(self)
        )
    except Exception:
        pass

    left_group = QGroupBox("Show Project to AI First Prompt Files")
    left_layout = QVBoxLayout(left_group)
    left_layout.addWidget(QLabel("Create startup files for the first AI prompt."))
    left_layout.addWidget(QLabel("Output: <project_drive>:\\<project_name>_show_project_to_AI\\first_prompt_files\\"))
    left_layout.addWidget(QLabel("Uses the Project root field above as the source folder."))
    self.create_first_prompt_files_button = QPushButton("Create First Prompt Files")
    left_layout.addWidget(self.create_first_prompt_files_button)
    self.path_to_first_prompt_files_button = QPushButton("Path to First Prompt Files")
    self.path_to_first_prompt_files_button.setStyleSheet("color: blue;")
    left_layout.addWidget(self.path_to_first_prompt_files_button)
    self.first_prompt_status_label = QLabel("First prompt files idle")
    left_layout.addWidget(self.first_prompt_status_label)
    self.first_prompt_log_box = QPlainTextEdit()
    self.first_prompt_log_box.setReadOnly(True)
    left_layout.addWidget(self.first_prompt_log_box)

    try:
        from kanda_reasoner_app.reasoner_tools_shell.runner_help import first_prompt_files_private_impl as _first_prompt_impl
        self.create_first_prompt_files_button.clicked.connect(
            lambda: _first_prompt_impl.run_create_first_prompt_files(self)
        )
    except Exception:
        pass

    def _create_first_and_second_prompt_files() -> None:
        try:
            from kanda_reasoner_app.reasoner_tools_shell.runner_help import first_prompt_files_private_impl as _first_prompt_impl
            _first_prompt_impl.run_create_first_prompt_files(self)
            first_status = getattr(self, "first_prompt_status_label", None)
            first_status_text = first_status.text().lower() if first_status is not None else ""
            if any(marker in first_status_text for marker in ("failed", "invalid", "busy")):
                try:
                    self._append_log("[WARN] Create Second Prompt Files skipped because Create First Prompt Files did not finish cleanly.")
                except Exception:
                    pass
                return
            self._run_collector()
        except Exception as exc:
            try:
                self._append_log("[ERROR] Create First and Second Prompt Files failed: " + str(exc))
            except Exception:
                pass

    self.create_first_and_second_prompt_files_button.clicked.connect(_create_first_and_second_prompt_files)

    def _copy_show_project_to_ai_path(kind: str) -> None:
        try:
            from pathlib import Path
            from PySide6.QtWidgets import QApplication
            from kanda_reasoner_app.project_analysis_evidence_paths import (
                analysis_first_prompt_files_dir,
                analysis_json_complete_dir,
            )

            project_root = Path(self.project_root_edit.text()).expanduser()
            if kind == "first":
                target_path = analysis_first_prompt_files_dir(project_root)
                status_target = getattr(self, "first_prompt_status_label", None)
            else:
                target_path = analysis_json_complete_dir(project_root)
                status_target = getattr(self, "status_label", None)

            QApplication.clipboard().setText(str(target_path))
            message = "Copied path: " + str(target_path)
            if status_target is not None:
                status_target.setText(message)
            try:
                self._append_log(message)
            except Exception:
                pass
        except Exception as exc:
            message = "[ERROR] Could not copy Show Project to AI path: " + str(exc)
            try:
                self._append_log(message)
            except Exception:
                pass

    self.path_to_first_prompt_files_button.clicked.connect(
        lambda: _copy_show_project_to_ai_path("first")
    )

    right_group = QGroupBox("Show Project to AI Second Prompt Files")
    collector_right_layout = QVBoxLayout(right_group)

    out_row = QHBoxLayout()
    out_row.addWidget(QLabel("Output JSON:"))
    self.output_json_edit = QLineEdit(
        self._prefs.get("output_json", str(_DEFAULT_OUTPUT_JSON.resolve()))
    )
    out_row.addWidget(self.output_json_edit)
    self.browse_output_button = QPushButton("Browse...")
    out_row.addWidget(self.browse_output_button)
    collector_right_layout.addLayout(out_row)

    self.runtime_trace_json_edit = QLineEdit(
        self._prefs.get(
            "runtime_trace_json",
            str(_DEFAULT_RUNTIME_TRACE_JSON.resolve()),
        )
    )
    self.runtime_trace_json_edit.hide()

    self.browse_runtime_trace_button = QPushButton("Browse...")
    self.browse_runtime_trace_button.hide()

    button_row = QHBoxLayout()
    self.run_button = QPushButton("Create Second Prompt Files")
    self.path_to_second_prompt_files_button = QPushButton("Path to Second Prompt Files")
    self.path_to_second_prompt_files_button.setStyleSheet("color: blue;")
    self.zip_size_100_radio = QRadioButton("100 MB")
    self.zip_size_200_radio = QRadioButton("200 MB")
    self.zip_size_300_radio = QRadioButton("300 MB")
    self.zip_size_400_radio = QRadioButton("400 MB")
    self.zip_size_500_radio = QRadioButton("500 MB")
    self.close_button = QPushButton("Close")
    button_row.addWidget(self.run_button)
    button_row.addWidget(self.path_to_second_prompt_files_button)
    button_row.addWidget(QLabel("ZIP size limit:"))
    button_row.addWidget(self.zip_size_100_radio)
    button_row.addWidget(self.zip_size_200_radio)
    button_row.addWidget(self.zip_size_300_radio)
    button_row.addWidget(self.zip_size_400_radio)
    button_row.addWidget(self.zip_size_500_radio)
    button_row.addWidget(self.close_button)
    button_row.addStretch()
    collector_right_layout.addLayout(button_row)

    try:
        from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_private_impl as _zip_json_impl
        _saved_zip_size = _zip_json_impl.load_saved_part_size_mb()
        _zip_size_radios = {
            100: self.zip_size_100_radio,
            200: self.zip_size_200_radio,
            300: self.zip_size_300_radio,
            400: self.zip_size_400_radio,
            500: self.zip_size_500_radio,
        }
        _zip_size_radios.get(_saved_zip_size, self.zip_size_500_radio).setChecked(True)
        for _zip_size_mb, _radio in _zip_size_radios.items():
            _radio.toggled.connect(
                lambda checked, size=_zip_size_mb: (
                    _zip_json_impl.save_selected_part_size_mb(size) if checked else None
                )
            )
    except Exception:
        self.zip_size_500_radio.setChecked(True)

    self.path_to_second_prompt_files_button.clicked.connect(
        lambda: _copy_show_project_to_ai_path("second")
    )

    self.status_label = QLabel("Idle")
    collector_right_layout.addWidget(self.status_label)

    self.log_box = QPlainTextEdit()
    self.log_box.setReadOnly(True)
    collector_right_layout.addWidget(self.log_box)

    splitter = QSplitter(Qt.Horizontal)
    splitter.addWidget(left_group)
    splitter.addWidget(right_group)
    splitter.setStretchFactor(0, 1)
    splitter.setStretchFactor(1, 2)
    collector_layout.addWidget(splitter)

    self.tabs.addTab(collector_tab, "Show Project to AI")
    try:
        self.tabs.tabBar().setTabVisible(0, False)
    except Exception:
        self.tabs.setTabText(0, "")

    # ----- JSON Splitter tab (unchanged) -----
    self.splitter_panel = JsonSplitterPanel(self)
    self.tabs.addTab(self.splitter_panel, "JSON Splitter")

    # ----- Architecture Manager tab (embedded) -----
    arch_container = QWidget()
    arch_layout = QVBoxLayout(arch_container)
    arch_layout.setContentsMargins(0, 0, 0, 0)
    self.arch_window = ArchitectureManagerWindow()   # no parent argument
    self.arch_window.setParent(arch_container)
    self.arch_window.setWindowFlags(Qt.Widget)
    arch_layout.addWidget(self.arch_window)
    self.tabs.addTab(arch_container, "Architecture Manager")

    # ----- Workflow Manager tab (embedded) -----
    wf_container = QWidget()
    wf_layout = QVBoxLayout(wf_container)
    wf_layout.setContentsMargins(0, 0, 0, 0)
    self.wf_window = WorkflowManagerWindow()        # no parent argument
    self.wf_window.setParent(wf_container)
    self.wf_window.setWindowFlags(Qt.Widget)
    wf_layout.addWidget(self.wf_window)
    self.tabs.addTab(wf_container, "Workflow Manager")
