# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/window_state.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Initialize the main window state and persist preference payloads.
# EXPORTS       : initialize_window, current_prefs_payload
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Window initialization and preference payload helpers."""

from __future__ import annotations

import tempfile
from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLineEdit,
    QLabel,
    QListWidget,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSpinBox,
)

from .constants import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_PROJECT_ROOT,
    DEFAULT_WORKER_NAME,
)
from .preferences import safe_bool, safe_int, safe_text

__all__ = ["initialize_window", "current_prefs_payload"]


def _canonical_worker_script_path() -> str:
    """Return the canonical Tab 3 missing-docstrings worker path."""
    current_file = Path(__file__).resolve()

    for parent in current_file.parents:
        candidate = (
            parent
            / "kanda_reasoner_app"
            / "insert_missing_docstrings_gui"
            / DEFAULT_WORKER_NAME
        )
        if candidate.exists():
            return str(candidate)

    return str(current_file.parent.parent / DEFAULT_WORKER_NAME)


def initialize_window(self) -> None:
    """Initialize widgets and state for the main GUI window."""
    self.setWindowTitle("Missing Docstrings Inserter")
    self.resize(1360, 860)
    self._worker_thread: QThread | None = None
    self._worker: DocstringRunWorker | None = None
    self._docstring_ai_thread: QThread | None = None
    self._docstring_ai_worker = None
    self._docstring_ai_receiver = None
    self._docstring_ai_active_identity = None
    self._docstring_ai_session_id = ""
    self._runtime_dir = Path(tempfile.mkdtemp(prefix="docstring_gui_"))
    self._current_report_path: Path | None = None
    self._report_rows: list[dict] = []
    self._prefs = self._load_prefs()
    self._root_path_label = QLabel("Project Root:")
    self._root_path_label.setStyleSheet("color: #0B3D91; font-weight: bold;")
    self._root_path_edit = QLineEdit(
        safe_text(self._prefs.get("project_root"), DEFAULT_PROJECT_ROOT)
    )
    self._root_path_edit.setPlaceholderText("Project root")
    self._browse_root_button = QPushButton("Browser")
    self._project_root_controls_moved_to_host = False
    self._worker_path_edit = QLineEdit(_canonical_worker_script_path())
    self._worker_path_edit.setEnabled(False)
    self._mode_combo = QComboBox()
    self._mode_combo.addItems(["scan", "diff", "write"])
    self._mode_combo.setCurrentText(
        safe_text(self._prefs.get("mode"), "scan")
    )
    self._tab1_audit_docstring_radio = QRadioButton(
        "get missing docstring from Tab 1 audit"
    )
    self._tab1_audit_docstring_radio.setChecked(
        safe_bool(self._prefs.get("use_tab1_audit_docstring_source"), False)
    )
    font = self._tab1_audit_docstring_radio.font()
    font.setBold(True)
    self._tab1_audit_docstring_radio.setFont(font)
    self._tab1_audit_docstring_radio.setStyleSheet("color: green; font-weight: bold;")
    self._tab1_audit_docstring_radio.setToolTip(
        "Read MISSING_DOCSTRING targets from the Tab 1 architecture audit."
    )
    self._module_checkbox = QCheckBox("Module header docstring")
    self._module_checkbox.setChecked(
        safe_bool(self._prefs.get("include_module"), True)
    )
    self._class_checkbox = QCheckBox("Classes")
    self._class_checkbox.setChecked(
        safe_bool(self._prefs.get("include_classes"), True)
    )
    self._function_checkbox = QCheckBox("Function/method")
    self._function_checkbox.setChecked(
        safe_bool(self._prefs.get("include_functions"), True)
    )
    self._file_address_checkbox = QCheckBox("Insert file address at top if missing")
    self._file_address_checkbox.setChecked(
        safe_bool(self._prefs.get("insert_file_address_at_top"), False)
    )
    self._file_address_checkbox.setToolTip(
        "When enabled, scan/diff/write audits each selected Python file and inserts "
        "a top file-address comment when it is missing."
    )
    self._confirm_write_checkbox = QCheckBox("Require confirm before write")
    self._confirm_write_checkbox.setChecked(
        safe_bool(self._prefs.get("confirm_write"), True)
    )
    ai_controls = __import__(
        "kanda_reasoner_app.tab3_manual_review_runtime.ai_web_controls_runtime",
        fromlist=["initialize_controls"],
    )
    ai_controls.initialize_controls(self, self._prefs)
    self._config_path_edit = QLineEdit(
        safe_text(self._prefs.get("config_path"), "")
    )
    self._load_config_button = QPushButton("Load config...")
    self._save_config_button = QPushButton("Save config...")
    self._include_private_checkbox = QCheckBox("Document private symbols with AI")
    self._include_private_checkbox.setChecked(
        safe_bool(self._prefs.get("include_private"), True)
    )
    self._min_confidence_combo = QComboBox()
    self._min_confidence_combo.addItems(["low", "medium", "high"])
    self._min_confidence_combo.setCurrentText(
        safe_text(self._prefs.get("min_confidence"), "low")
    )
    self._no_uncertain_checkbox = QCheckBox("Suppress # AI-UNCERTAIN comments")
    self._workers_spin = QSpinBox()
    self._workers_spin.setRange(1, 64)
    self._workers_spin.setValue(
        safe_int(self._prefs.get("workers"), 4, 1, 64)
    )
    self._scope_combo = QComboBox()
    self._scope_combo.addItems(["Full project", "Package/folder", "Module/file"])
    self._scope_combo.setCurrentText(
        safe_text(self._prefs.get("scope"), "Full project")
    )
    self._target_path_edit = QLineEdit(
        safe_text(self._prefs.get("target_path"), "")
    )
    self._browse_target_button = QPushButton("Browse...")
    self._clear_target_button = QPushButton("Clear")
    self._report_path_edit = QLineEdit(
        safe_text(self._prefs.get("report_path"), "")
    )
    self._browse_report_button = QPushButton("Browse...")
    self._output = QPlainTextEdit()
    self._output.setReadOnly(True)
    self._output.setLineWrapMode(QPlainTextEdit.NoWrap)
    self._output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self._review_summary = QLabel("No run report loaded.")
    self._review_summary.setWordWrap(True)
    self._review_filter_combo = QComboBox()
    self._review_filter_combo.addItems(
        [
            "Needs review",
            "All",
            "Ready for review",
            "Fallback review",
            "Blocked/rejected",
            "Warnings/errors",
            "AI only",
            "Fallback only",
            "Low confidence",
        ]
    )
    self._review_list = QListWidget()
    self._review_details = QPlainTextEdit()
    self._review_details.setReadOnly(True)
    self._progress = QProgressBar()
    self._progress.setRange(0, 1)
    self._progress.setValue(0)
    self._progress.setFormat("Idle")
    self._build_ui()
    self._wire_events()
    self._set_ai_controls_enabled(False)
    self._update_scope_controls()


def current_prefs_payload(self) -> dict[str, object]:
    """Build the current standalone GUI preferences payload."""
    payload = {
        "project_root": self._root_path_edit.text().strip(),
        "mode": self._mode_combo.currentText(),
        "include_module": self._module_checkbox.isChecked(),
        "include_classes": self._class_checkbox.isChecked(),
        "include_functions": self._function_checkbox.isChecked(),
        "insert_file_address_at_top": self._file_address_checkbox.isChecked(),
        "confirm_write": self._confirm_write_checkbox.isChecked(),
        "ai_enabled": False,
        "base_url": self._base_url_edit.text().strip(),
        "model": self._model_combo.currentText().strip(),
        "config_path": self._config_path_edit.text().strip(),
        "include_private": self._include_private_checkbox.isChecked(),
        "min_confidence": self._min_confidence_combo.currentText(),
        "no_uncertain": self._no_uncertain_checkbox.isChecked(),
        "workers": self._workers_spin.value(),
        "scope": self._scope_combo.currentText(),
        "target_path": self._target_path_edit.text().strip(),
        "report_path": self._report_path_edit.text().strip(),
        "use_tab1_audit_docstring_source": self._tab1_audit_docstring_radio.isChecked(),
    }
    ai_controls = __import__(
        "kanda_reasoner_app.tab3_manual_review_runtime.ai_web_controls_runtime",
        fromlist=["preferences_payload"],
    )
    payload.update(ai_controls.preferences_payload(self))
    return payload
