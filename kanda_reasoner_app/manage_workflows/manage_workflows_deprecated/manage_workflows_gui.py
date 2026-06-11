#!/usr/bin/env python3
"""Qt GUI for running workflow scan, validate, diff, and write modes."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import traceback
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

DEFAULT_MANAGER_NAME = "manage_workflows.py"
DEFAULT_PROJECT_ROOT = r"E:\eeg_kernel_ai_neural_data_analysis"


class WorkflowRunWorker(QObject):
    output_ready = Signal(str)
    finished_ok = Signal(str)
    finished_error = Signal(str, str)

    def __init__(self, manager_script_path: str, project_root: str, mode: str) -> None:
        super().__init__()
        self._manager_script_path = Path(manager_script_path)
        self._project_root = Path(project_root)
        self._mode = mode

    def run(self) -> None:
        try:
            module = self._load_manager_module(self._manager_script_path)

            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                if hasattr(module, "run"):
                    exit_code = module.run(self._project_root.resolve(), self._mode)
                elif hasattr(module, "main"):
                    original_argv = sys.argv[:]
                    try:
                        sys.argv = [
                            str(self._manager_script_path),
                            "--root",
                            str(self._project_root.resolve()),
                            f"--{self._mode}",
                        ]
                        exit_code = module.main()
                    finally:
                        sys.argv = original_argv
                else:
                    raise AttributeError(
                        "manage_workflows.py must expose either run(root, mode) or main()."
                    )

            captured = buffer.getvalue()
            if captured:
                self.output_ready.emit(captured)

            if int(exit_code) == 0:
                self.finished_ok.emit(self._mode)
            else:
                self.finished_error.emit(
                    self._mode,
                    f"Worker finished with exit code {exit_code}.",
                )
        except Exception:
            tb = traceback.format_exc()
            self.finished_error.emit(self._mode, tb)

    def _load_manager_module(self, script_path: Path):
        if not script_path.exists():
            raise FileNotFoundError(f"Worker script not found: {script_path}")

        module_name = "workflow_manager_worker"

        spec = importlib.util.spec_from_file_location(
            module_name,
            str(script_path),
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load worker module from {script_path}")

        module = importlib.util.module_from_spec(spec)

        # Required for Python 3.12 dataclass(slots=True) and similar decorators
        # that look up the defining module in sys.modules during execution.
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(module_name, None)
            raise

        return module


class WorkflowManagerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Workflow Manager")
        self.resize(1100, 760)

        self._worker_thread: QThread | None = None
        self._worker: WorkflowRunWorker | None = None

        self._root_path_edit = QLineEdit(DEFAULT_PROJECT_ROOT)
        self._python_path_edit = QLineEdit(sys.executable)
        self._python_path_edit.setEnabled(False)

        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["validate", "diff", "scan", "write"])
        self._mode_combo.setCurrentText("validate")

        self._strict_write_checkbox = QCheckBox("Require confirm before write")
        self._strict_write_checkbox.setChecked(True)

        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setLineWrapMode(QPlainTextEdit.NoWrap)
        self._output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._build_ui()

    def _manager_script_path(self) -> Path:
        return Path(__file__).resolve().parent / DEFAULT_MANAGER_NAME

    def _build_ui(self) -> None:
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)

        run_action = QAction("Run", self)
        run_action.triggered.connect(self.run_selected_mode)
        toolbar.addAction(run_action)

        clear_action = QAction("Clear Output", self)
        clear_action.triggered.connect(self._output.clear)
        toolbar.addAction(clear_action)

        save_action = QAction("Save Output", self)
        save_action.triggered.connect(self.save_output)
        toolbar.addAction(save_action)

        help_action = QAction("Mode Help", self)
        help_action.triggered.connect(self.show_mode_help)
        toolbar.addAction(help_action)

        central = QWidget(self)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        form = QFormLayout()

        script_label = QLabel(str(self._manager_script_path()))
        form.addRow("Worker script", script_label)

        root_row = QHBoxLayout()
        root_row.addWidget(self._root_path_edit)
        browse_root_btn = QPushButton("Browse…")
        browse_root_btn.clicked.connect(self.browse_root)
        root_row.addWidget(browse_root_btn)
        form.addRow("Project root", root_row)

        python_row = QHBoxLayout()
        python_row.addWidget(self._python_path_edit)
        form.addRow("Python executable", python_row)

        form.addRow("Mode", self._mode_combo)
        form.addRow("", self._strict_write_checkbox)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        self._run_button = QPushButton("Run Selected Mode")
        self._run_button.clicked.connect(self.run_selected_mode)
        buttons.addWidget(self._run_button)

        for mode in ("validate", "diff", "scan", "write"):
            btn = QPushButton(mode.capitalize())
            btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))
            buttons.addWidget(btn)

        help_btn = QPushButton("What do these modes do?")
        help_btn.clicked.connect(self.show_mode_help)
        buttons.addWidget(help_btn)
        buttons.addWidget(self._strict_write_checkbox)

        layout.addLayout(buttons)
        layout.addWidget(QLabel("Output"))
        layout.addWidget(self._output, stretch=1)

        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

    def browse_root(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self,
            "Select project root",
            self._root_path_edit.text().strip() or str(Path.cwd()),
        )
        if path:
            self._root_path_edit.setText(path)

    def run_selected_mode(self) -> None:
        self.run_mode(self._mode_combo.currentText())

    def run_mode(self, mode: str) -> None:
        script_path = self._manager_script_path()
        root_path = Path(self._root_path_edit.text().strip())

        if not script_path.exists():
            QMessageBox.critical(
                self,
                "Missing worker script",
                "The GUI could not find the sibling worker script:\n"
                f"{script_path}\n\n"
                "Place manage_workflows.py in the same folder as this GUI file.",
            )
            return

        if not root_path.exists():
            QMessageBox.critical(
                self,
                "Invalid project root",
                f"Project root not found:\n{root_path}",
            )
            return

        if mode == "write" and self._strict_write_checkbox.isChecked():
            if not self._confirm_write():
                return

        if self._worker_thread is not None:
            QMessageBox.warning(
                self,
                "Work running",
                "Wait for the current work to finish first.",
            )
            return

        self._output.appendPlainText(
            f"> in-process run: {script_path} --root {root_path} --{mode}\n"
        )
        self._run_button.setEnabled(False)
        self.statusBar().showMessage(f"Running {mode}…")

        self._worker_thread = QThread(self)
        self._worker = WorkflowRunWorker(
            manager_script_path=str(script_path),
            project_root=str(root_path),
            mode=mode,
        )
        self._worker.moveToThread(self._worker_thread)

        self._worker_thread.started.connect(self._worker.run)
        self._worker.output_ready.connect(self._append_text)
        self._worker.finished_ok.connect(self._handle_worker_success)
        self._worker.finished_error.connect(self._handle_worker_error)

        self._worker.finished_ok.connect(self._worker_thread.quit)
        self._worker.finished_error.connect(self._worker_thread.quit)
        self._worker_thread.finished.connect(self._cleanup_worker)

        self._worker_thread.start()

    def _confirm_write(self) -> bool:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle("Confirm write")
        box.setText(
            "Write mode can update workflow_manifest.json and WORKFLOWS.md."
        )
        box.setInformativeText("Continue?")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        return box.exec() == QMessageBox.Yes

    def _append_text(self, text: str) -> None:
        if not text:
            return
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)
        self._output.insertPlainText(text)
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)

    def _handle_worker_success(self, mode: str) -> None:
        self._run_button.setEnabled(True)
        self.statusBar().showMessage(f"Finished {mode}")
        self._output.appendPlainText(f"\n[finished] mode={mode} exit_code=0\n")
        QMessageBox.information(
            self,
            "Work done",
            f"{mode.capitalize()} completed successfully.",
        )

    def _handle_worker_error(self, mode: str, details: str) -> None:
        self._run_button.setEnabled(True)
        self.statusBar().showMessage(f"Finished {mode} with issues")
        self._output.appendPlainText(
            f"\n[finished] mode={mode} exit_code=1\n{details}\n"
        )
        QMessageBox.warning(
            self,
            "Work finished with issues",
            f"{mode.capitalize()} finished with issues.\n"
            "Check the output panel for details.",
        )

    def _cleanup_worker(self) -> None:
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread is not None:
            self._worker_thread.deleteLater()
            self._worker_thread = None

    def show_mode_help(self) -> None:
        help_text = (
            "Validate\n"
            "- runs dynamic workflow checks from workflow_manifest.json, "
            "including tests, runtime smoke commands, business checks, GUI flows, "
            "integration commands, performance commands, and import-side-effect probes.\n\n"
            "Diff\n"
            "- previews the changes that would be written to workflow_manifest.json "
            "and WORKFLOWS.md.\n\n"
            "Scan\n"
            "- prints the generated workflow manifest template as JSON.\n\n"
            "Write\n"
            "- writes workflow_manifest.json and WORKFLOWS.md."
        )
        QMessageBox.information(self, "Mode Help", help_text)

    def save_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save output",
            str(Path.cwd() / "workflow_manager_output.txt"),
            "Text Files (*.txt)",
        )
        if not path:
            return
        Path(path).write_text(self._output.toPlainText(), encoding="utf-8")
        self.statusBar().showMessage(f"Saved output to {path}")


def main() -> int:
    app = QApplication(sys.argv)
    window = WorkflowManagerWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
