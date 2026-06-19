"""GUI tab for preparing AI freeze files after a project update."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.freeze_after_update.contract import (
    ensure_freeze_after_update_box,
    generate_freeze_after_update_ai_files,
    inspect_freeze_after_update_box,
)
from kanda_reasoner_app.freeze_after_update.paths import build_paths
from kanda_reasoner_app.freeze_after_update.result import FreezeAfterUpdateResult


class FreezeAfterUpdateTab(QWidget):
    """Human-facing controller for the project-local freeze-after-update box."""

    def __init__(self) -> None:
        super().__init__()
        self._last_output_folder: Path | None = None
        self._what_to_say_dialog: QDialog | None = None
        self._what_to_say_text_edit: QTextEdit | None = None
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        title = QLabel("Freeze Feature After Update")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title.setFont(title_font)
        root_layout.addWidget(title)

        intro = QLabel(
            "Create or refresh the project-local files that you upload to AI "
            "after updating the selected project. The frozen memory stays inside "
            "the actual project, not inside KANDA Reasoner."
        )
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(12)
        root_layout.addLayout(columns_layout, 1)

        left_column_widget = QWidget()
        left_column = QVBoxLayout(left_column_widget)
        left_column.setContentsMargins(0, 0, 0, 0)
        left_column.setSpacing(10)

        right_column_widget = QWidget()
        right_column = QVBoxLayout(right_column_widget)
        right_column.setContentsMargins(0, 0, 0, 0)
        right_column.setSpacing(10)

        columns_layout.addWidget(left_column_widget, 1)
        columns_layout.addWidget(right_column_widget, 1)

        project_group = QGroupBox("Active project")
        project_layout = QGridLayout(project_group)
        project_layout.setColumnStretch(1, 1)

        project_layout.addWidget(QLabel("Project root:"), 0, 0)
        self.project_root_edit = QLineEdit()
        self.project_root_edit.setPlaceholderText("Select or receive the current project root")
        project_layout.addWidget(self.project_root_edit, 0, 1)

        self.choose_project_button = QPushButton("Choose Project Folder")
        project_layout.addWidget(self.choose_project_button, 0, 2)

        project_layout.addWidget(QLabel("Box folder:"), 1, 0)
        self.box_folder_edit = QLineEdit()
        self.box_folder_edit.setReadOnly(True)
        project_layout.addWidget(self.box_folder_edit, 1, 1, 1, 2)

        project_layout.addWidget(QLabel("files_to_send_ai:"), 2, 0)
        self.files_to_send_path_edit = QLineEdit()
        self.files_to_send_path_edit.setReadOnly(True)
        project_layout.addWidget(self.files_to_send_path_edit, 2, 1, 1, 2)

        left_column.addWidget(project_group)

        status_group = QGroupBox("Status and actions")
        status_layout = QGridLayout(status_group)
        status_layout.setColumnStretch(1, 1)

        status_layout.addWidget(QLabel("Status:"), 0, 0)
        self.status_label = QLabel("Not checked yet")
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label, 0, 1, 1, 3)

        self.check_button = QPushButton("Check Box Status")
        self.create_button = QPushButton("Create / Repair Box")
        self.generate_button = QPushButton("Generate Files To Send AI")
        self.open_box_button = QPushButton("Open project_freeze_after_update")
        self.open_output_button = QPushButton("Open files_to_send_ai")
        self.copy_output_path_button = QPushButton("Copy files_to_send_ai Path")
        self.show_instruction_button = QPushButton("Show what_to_say_to_ai")

        status_layout.addWidget(self.check_button, 1, 0)
        status_layout.addWidget(self.create_button, 1, 1)
        status_layout.addWidget(self.generate_button, 1, 2)
        status_layout.addWidget(self.open_box_button, 2, 0)
        status_layout.addWidget(self.open_output_button, 2, 1)
        status_layout.addWidget(self.copy_output_path_button, 2, 2)
        status_layout.addWidget(self.show_instruction_button, 3, 0, 1, 3)

        left_column.addWidget(status_group)

        outputs_group = QGroupBox("Generated output")
        outputs_layout = QGridLayout(outputs_group)
        outputs_layout.setColumnStretch(1, 1)

        outputs_layout.addWidget(QLabel("ZIP:"), 0, 0)
        self.zip_edit = QLineEdit()
        self.zip_edit.setReadOnly(True)
        outputs_layout.addWidget(self.zip_edit, 0, 1)

        outputs_layout.addWidget(QLabel("Instruction MD:"), 1, 0)
        self.instruction_edit = QLineEdit()
        self.instruction_edit.setReadOnly(True)
        outputs_layout.addWidget(self.instruction_edit, 1, 1)

        left_column.addWidget(outputs_group)
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
        self.project_root_edit.textChanged.connect(self._refresh_derived_paths)
        self.choose_project_button.clicked.connect(self._choose_project_folder)
        self.check_button.clicked.connect(self._check_box_status)
        self.create_button.clicked.connect(self._create_or_repair_box)
        self.generate_button.clicked.connect(self._generate_files)
        self.open_box_button.clicked.connect(self._open_box_folder)
        self.open_output_button.clicked.connect(self._open_output_folder)
        self.copy_output_path_button.clicked.connect(self._copy_output_folder_path)
        self.show_instruction_button.clicked.connect(self._show_what_to_say_window)

    def _project_root(self) -> Path | None:
        text = self.project_root_edit.text().strip()
        if not text:
            return None
        return Path(text).expanduser()

    def _paths(self):
        project_root = self._project_root()
        if project_root is None:
            return None
        return build_paths(project_root)

    def _refresh_derived_paths(self) -> None:
        paths = self._paths()
        if paths is None:
            self.box_folder_edit.clear()
            self.files_to_send_path_edit.clear()
            return
        self.box_folder_edit.setText(str(paths.box_root))
        self.files_to_send_path_edit.setText(str(paths.send_root))

    def _choose_project_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose Project Folder")
        if folder:
            self.project_root_edit.setText(folder)

    def _append_log(self, message: str) -> None:
        self.output_log.append(message)

    def _show_result(self, result: FreezeAfterUpdateResult) -> None:
        status_text = f"{result.status.value}: {result.message}"
        self.status_label.setText(status_text)
        self._append_log(status_text)

        if result.box_root is not None:
            self.box_folder_edit.setText(str(result.box_root))
            self.files_to_send_path_edit.setText(str(result.box_root / "files_to_send_ai"))

        if result.missing_paths:
            self._append_log("Missing paths:")
            for path in result.missing_paths:
                self._append_log(f"- {path}")

        if result.created_paths:
            self._append_log("Created paths:")
            for path in result.created_paths:
                self._append_log(f"- {path}")

        if result.output_zip is not None:
            self.zip_edit.setText(str(result.output_zip))
            self._last_output_folder = result.output_zip.parent
            self.files_to_send_path_edit.setText(str(result.output_zip.parent))
            self._append_log(f"ZIP created: {result.output_zip}")

        if result.output_instruction is not None:
            self.instruction_edit.setText(str(result.output_instruction))
            self._last_output_folder = result.output_instruction.parent
            self.files_to_send_path_edit.setText(str(result.output_instruction.parent))
            self._append_log(f"Instruction file created: {result.output_instruction}")

        if result.freeze_count:
            self._append_log(f"Freeze entries included: {result.freeze_count}")
        else:
            self._append_log("Freeze entries included: 0")

    def _require_project_root(self) -> Path | None:
        project_root = self._project_root()
        if project_root is None:
            QMessageBox.warning(self, "Project missing", "Select a project folder first.")
            return None
        return project_root

    def _check_box_status(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(inspect_freeze_after_update_box(project_root))

    def _create_or_repair_box(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(ensure_freeze_after_update_box(project_root))

    def _generate_files(self) -> None:
        project_root = self._require_project_root()
        if project_root is None:
            return
        self._show_result(generate_freeze_after_update_ai_files(project_root))

    def _open_path(self, path: Path | None, label: str) -> None:
        if path is None:
            QMessageBox.warning(self, "Path missing", f"No {label} path is available yet.")
            return
        if not path.exists():
            QMessageBox.warning(self, "Path missing", f"The {label} path does not exist:\n{path}")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def _open_box_folder(self) -> None:
        paths = self._paths()
        self._open_path(paths.box_root if paths is not None else None, "box folder")

    def _send_root_path(self) -> Path | None:
        paths = self._paths()
        output_path = self._last_output_folder
        if output_path is None and paths is not None:
            output_path = paths.send_root
        return output_path

    def _what_to_say_path(self) -> Path | None:
        paths = self._paths()
        if paths is None:
            return None
        return paths.what_to_say

    def _open_output_folder(self) -> None:
        self._open_path(self._send_root_path(), "files_to_send_ai folder")

    def _copy_output_folder_path(self) -> None:
        output_path = self._send_root_path()
        if output_path is None:
            QMessageBox.warning(self, "Path missing", "No files_to_send_ai path is available yet.")
            return
        QApplication.clipboard().setText(str(output_path))
        self.files_to_send_path_edit.setText(str(output_path))
        self._append_log(f"Copied files_to_send_ai path: {output_path}")

    def _show_what_to_say_window(self) -> None:
        what_to_say_path = self._what_to_say_path()
        if what_to_say_path is None:
            QMessageBox.warning(self, "Project missing", "Select a project folder first.")
            return
        if not what_to_say_path.exists():
            QMessageBox.warning(
                self,
                "Instruction file missing",
                "The instruction file does not exist yet.\n\n"
                "Generate Files To Send AI first, then open this window.\n\n"
                f"Expected path:\n{what_to_say_path}",
            )
            return

        try:
            text = what_to_say_path.read_text(encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(self, "Could not read instruction file", str(exc))
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("what_to_say_to_ai_freeze_feature.md")
        dialog.resize(900, 700)

        layout = QVBoxLayout(dialog)

        warning = QLabel(
            'Warning: file "what_to_say_to_ai_freeze_feature.md" should not be edited manually here or anywhere else.'
        )
        warning.setWordWrap(True)
        warning_font = QFont()
        warning_font.setBold(True)
        warning.setFont(warning_font)
        layout.addWidget(warning)

        path_label = QLabel(str(what_to_say_path))
        path_label.setWordWrap(True)
        layout.addWidget(path_label)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text)
        layout.addWidget(text_edit, 1)

        button_row = QHBoxLayout()
        copy_button = QPushButton("Copy Complete Text")
        close_button = QPushButton("Close")
        button_row.addStretch(1)
        button_row.addWidget(copy_button)
        button_row.addWidget(close_button)
        layout.addLayout(button_row)

        def copy_complete_text() -> None:
            QApplication.clipboard().setText(text_edit.toPlainText())
            self._append_log("Copied complete what_to_say_to_ai_freeze_feature.md text.")

        copy_button.clicked.connect(copy_complete_text)
        close_button.clicked.connect(dialog.close)

        self._what_to_say_dialog = dialog
        self._what_to_say_text_edit = text_edit
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
