"""Private window methods private impl helpers for reasoner_tools_shell.runner."""

from __future__ import annotations


def _bind_globals(namespace):
    """Bind runner.py globals for moved method bodies."""
    globals().update(namespace)

def _build_ui(self) -> None:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QRadioButton
    central = QWidget()
    self.setCentralWidget(central)
    main_layout = QVBoxLayout(central)

    self.tabs = QTabWidget()
    main_layout.addWidget(self.tabs)

    # ----- Collector tab (unchanged) -----
    collector_tab = QWidget()
    collector_layout = QVBoxLayout(collector_tab)

    root_row = QHBoxLayout()
    root_row.addWidget(QLabel("Project root:"))
    self.project_root_edit = QLineEdit(
        self._prefs.get("project_root", str(_DEFAULT_PROJECT_ROOT))
    )
    root_row.addWidget(self.project_root_edit)
    self.browse_project_button = QPushButton("Browse...")
    root_row.addWidget(self.browse_project_button)
    collector_layout.addLayout(root_row)

    out_row = QHBoxLayout()
    out_row.addWidget(QLabel("Output JSON:"))
    self.output_json_edit = QLineEdit(
        self._prefs.get("output_json", str(_DEFAULT_OUTPUT_JSON.resolve()))
    )
    out_row.addWidget(self.output_json_edit)
    self.browse_output_button = QPushButton("Browse...")
    out_row.addWidget(self.browse_output_button)
    collector_layout.addLayout(out_row)

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
    self.run_button = QPushButton("Run Collector")
    self.zip_json_files_button = QPushButton("Zip JSON files")
    self.zip_size_conservative_radio = QRadioButton("Conservative 25 MB")
    self.zip_size_default_radio = QRadioButton("Default 40 MB")
    self.zip_size_default_radio.setChecked(True)
    self.close_button = QPushButton("Close")
    button_row.addWidget(self.run_button)
    button_row.addWidget(self.zip_json_files_button)
    button_row.addWidget(QLabel("ZIP size:"))
    button_row.addWidget(self.zip_size_conservative_radio)
    button_row.addWidget(self.zip_size_default_radio)
    button_row.addWidget(self.close_button)
    button_row.addStretch()
    collector_layout.addLayout(button_row)

    try:
        from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_private_impl as _zip_json_impl
        self.zip_json_files_button.clicked.connect(
            lambda: _zip_json_impl.run_zip_json_files(self)
        )
    except Exception:
        pass

    self.status_label = QLabel("Idle")
    collector_layout.addWidget(self.status_label)

    self.log_box = QPlainTextEdit()
    self.log_box.setReadOnly(True)
    collector_layout.addWidget(self.log_box)

    self.tabs.addTab(collector_tab, "Collector")

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
