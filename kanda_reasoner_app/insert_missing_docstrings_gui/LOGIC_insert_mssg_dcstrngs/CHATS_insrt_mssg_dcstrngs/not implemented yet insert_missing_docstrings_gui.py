#!/usr/bin/env python3
"""Missing Docstrings Inserter — PySide6 GUI.

Phase 2 additions
-----------------
- AI Settings panel (collapsible): model selector, base URL, timeout, workers,
  fallback checkbox, "Test connection" button.
- QProgressBar in the status bar driven by per-file FileProgress signals.
- DocstringRunWorker now accepts AI config and forwards on_file_complete /
  on_file_progress callbacks to run() via Qt signals.
"""

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
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QSpinBox,
    QDoubleSpinBox,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

DEFAULT_WORKER_NAME = "insert_missing_docstrings.py"
DEFAULT_PROJECT_ROOT = r"E:\eeg_kernel_ai_neural_data_analysis"

# Attempt to import AI config for model list defaults.
try:
    from ai_config import AIConfig
    _AI_CONFIG_AVAILABLE = True
except ImportError:
    _AI_CONFIG_AVAILABLE = False


# ---------------------------------------------------------------------------
# Worker signals helper — carries per-file progress to the GUI thread
# ---------------------------------------------------------------------------


class _ProgressPayload:
    """Lightweight progress snapshot safe to cross thread boundaries."""
    __slots__ = ("filename", "symbols_done", "symbols_found", "ai_used", "fallback_count", "error")

    def __init__(
        self,
        filename: str,
        symbols_done: int,
        symbols_found: int,
        ai_used: bool,
        fallback_count: int,
        error: str,
    ) -> None:
        self.filename = filename
        self.symbols_done = symbols_done
        self.symbols_found = symbols_found
        self.ai_used = ai_used
        self.fallback_count = fallback_count
        self.error = error


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------


class DocstringRunWorker(QObject):
    """Run insert_missing_docstrings.run() inside a QThread.

    Signals
    -------
    output_ready(str)
        Emitted with captured stdout/stderr chunks.
    file_complete(_ProgressPayload)
        Emitted each time a file finishes processing (thread-safe via Qt).
    progress_tick(int, int)
        Emitted with (files_done, files_total) after each file completes.
    finished_ok(str)
        Emitted with the mode name on success.
    finished_error(str, str)
        Emitted with (mode, traceback) on failure.
    """

    output_ready = Signal(str)
    file_complete = Signal(object)      # _ProgressPayload
    progress_tick = Signal(int, int)    # (done, total)
    finished_ok = Signal(str)
    finished_error = Signal(str, str)

    def __init__(
        self,
        worker_script_path: str,
        project_root: str,
        mode: str,
        include_module: bool,
        include_classes: bool,
        include_functions: bool,
        # AI options
        ai_enabled: bool = False,
        ai_config_path: str = "default",
        workers: int = 4,
    ) -> None:
        super().__init__()
        self._worker_script_path = Path(worker_script_path)
        self._project_root = Path(project_root)
        self._mode = mode
        self._include_module = include_module
        self._include_classes = include_classes
        self._include_functions = include_functions
        self._ai_enabled = ai_enabled
        self._ai_config_path = ai_config_path
        self._workers = workers

        self._files_done = 0
        self._files_total = 0  # updated lazily from progress ticks

    def run(self) -> None:
        try:
            module = self._load_worker_module(self._worker_script_path)

            buffer = io.StringIO()

            def _on_file_complete(prog: object) -> None:
                """Forward FileProgress to the GUI thread via Qt signal."""
                self._files_done += 1
                payload = _ProgressPayload(
                    filename=getattr(prog.path, "name", "?"),
                    symbols_done=getattr(prog, "symbols_done", 0),
                    symbols_found=getattr(prog, "symbols_found", 0),
                    ai_used=getattr(prog, "ai_used", False),
                    fallback_count=getattr(prog, "fallback_count", 0),
                    error=getattr(prog, "error", ""),
                )
                self.file_complete.emit(payload)
                self.progress_tick.emit(self._files_done, max(self._files_done, self._files_total))

            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                if hasattr(module, "run"):
                    run_kwargs: dict = dict(
                        include_module=self._include_module,
                        include_classes=self._include_classes,
                        include_functions=self._include_functions,
                        on_file_complete=_on_file_complete,
                    )
                    if self._ai_enabled:
                        run_kwargs["ai_config_path"] = self._ai_config_path
                        run_kwargs["workers"] = self._workers

                    exit_code = module.run(
                        self._project_root.resolve(),
                        self._mode,
                        **run_kwargs,
                    )
                elif hasattr(module, "main"):
                    # Fallback: argv injection for older worker versions.
                    original_argv = sys.argv[:]
                    try:
                        sys.argv = [
                            str(self._worker_script_path),
                            "--root", str(self._project_root.resolve()),
                            f"--{self._mode}",
                        ]
                        if not self._include_module:
                            sys.argv.append("--no-module")
                        if not self._include_classes:
                            sys.argv.append("--no-classes")
                        if not self._include_functions:
                            sys.argv.append("--no-functions")
                        if self._ai_enabled:
                            sys.argv += ["--ai", self._ai_config_path,
                                         "--workers", str(self._workers)]
                        exit_code = module.main()
                    finally:
                        sys.argv = original_argv
                else:
                    raise AttributeError(
                        "insert_missing_docstrings.py must expose run() or main()."
                    )

            captured = buffer.getvalue()
            if captured:
                self.output_ready.emit(captured)

            if int(exit_code) == 0:
                self.finished_ok.emit(self._mode)
            else:
                self.finished_error.emit(self._mode, f"Worker exit code {exit_code}.")

        except Exception:
            self.finished_error.emit(self._mode, traceback.format_exc())

    @staticmethod
    def _load_worker_module(script_path: Path):
        if not script_path.exists():
            raise FileNotFoundError(f"Worker script not found: {script_path}")
        module_name = "docstring_inserter_worker"
        spec = importlib.util.spec_from_file_location(module_name, str(script_path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load worker module from {script_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(module_name, None)
            raise
        return module


# ---------------------------------------------------------------------------
# AI Settings panel
# ---------------------------------------------------------------------------


class AISettingsPanel(QGroupBox):
    """Collapsible group box with AI configuration widgets.

    Parameters
    ----------
    parent : QWidget, optional
        Parent widget.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("AI Settings", parent)
        self.setCheckable(True)
        self.setChecked(False)   # collapsed by default

        self._base_url_edit = QLineEdit("http://localhost:11434/v1")
        self._model_edit = QLineEdit("codellama:13b")

        self._timeout_spin = QDoubleSpinBox()
        self._timeout_spin.setRange(5.0, 300.0)
        self._timeout_spin.setValue(30.0)
        self._timeout_spin.setSuffix(" s")

        self._workers_spin = QSpinBox()
        self._workers_spin.setRange(1, 32)
        self._workers_spin.setValue(4)

        self._fallback_checkbox = QCheckBox("Fall back to heuristic on AI failure")
        self._fallback_checkbox.setChecked(True)

        self._config_path_edit = QLineEdit()
        self._config_path_edit.setPlaceholderText("Leave blank to use in-panel settings")
        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._browse_config)

        self._test_btn = QPushButton("Test connection")
        self._test_btn.clicked.connect(self._test_connection)
        self._test_label = QLabel("")

        form = QFormLayout()
        form.addRow("Base URL", self._base_url_edit)
        form.addRow("Model", self._model_edit)
        form.addRow("Timeout", self._timeout_spin)
        form.addRow("Workers", self._workers_spin)
        form.addRow("", self._fallback_checkbox)

        cfg_row = QHBoxLayout()
        cfg_row.addWidget(self._config_path_edit)
        cfg_row.addWidget(browse_btn)
        form.addRow("Config file", cfg_row)

        test_row = QHBoxLayout()
        test_row.addWidget(self._test_btn)
        test_row.addWidget(self._test_label, stretch=1)
        form.addRow("", test_row)

        self.setLayout(form)

    # ------------------------------------------------------------------
    # Public accessors used by MissingDocstringsWindow
    # ------------------------------------------------------------------

    @property
    def ai_enabled(self) -> bool:
        """Return True when the AI panel is checked (enabled).

        Returns
        -------
        bool
            Whether AI mode is active.
        """
        return self.isChecked()

    @property
    def ai_config_path(self) -> str:
        """Return the ai_config.json path, or 'default' if blank.

        Returns
        -------
        str
            File path string or the literal string ``"default"``.
        """
        p = self._config_path_edit.text().strip()
        return p if p else "default"

    @property
    def workers(self) -> int:
        """Return the configured worker thread count.

        Returns
        -------
        int
            Number of parallel worker threads.
        """
        return self._workers_spin.value()

    def build_ai_config(self) -> "AIConfig | None":
        """Build an AIConfig from panel widgets when no config file is set.

        Returns
        -------
        AIConfig or None
            Populated config, or None if the AI stack is not importable.
        """
        if not _AI_CONFIG_AVAILABLE:
            return None
        return AIConfig(
            base_url=self._base_url_edit.text().strip(),
            model=self._model_edit.text().strip(),
            timeout_seconds=self._timeout_spin.value(),
            workers=self._workers_spin.value(),
            fallback_to_heuristic=self._fallback_checkbox.isChecked(),
        )

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _browse_config(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select ai_config.json", str(Path.cwd()), "JSON Files (*.json)"
        )
        if path:
            self._config_path_edit.setText(path)

    def _test_connection(self) -> None:
        """Ping the configured LLM endpoint and report latency."""
        import urllib.request
        import urllib.error
        import time

        url = self._base_url_edit.text().strip().rstrip("/") + "/models"
        self._test_label.setText("Testing…")
        QApplication.processEvents()

        try:
            t0 = time.monotonic()
            with urllib.request.urlopen(url, timeout=5) as resp:
                resp.read()
            elapsed = int((time.monotonic() - t0) * 1000)
            self._test_label.setText(f"✓ Connected ({elapsed} ms)")
        except Exception as exc:
            self._test_label.setText(f"✗ {exc}")


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------


class MissingDocstringsWindow(QMainWindow):
    """Main application window for the Missing Docstrings Inserter."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Missing Docstrings Inserter")
        self.resize(1180, 860)

        self._last_mode_run = ""
        self._worker_thread: QThread | None = None
        self._worker: DocstringRunWorker | None = None
        self._files_done = 0

        self._root_path_edit = QLineEdit(DEFAULT_PROJECT_ROOT)
        self._worker_path_edit = QLineEdit(
            str(Path(__file__).resolve().parent / DEFAULT_WORKER_NAME)
        )
        self._worker_path_edit.setEnabled(False)

        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["scan", "diff", "write"])
        self._mode_combo.setCurrentText("scan")

        self._module_checkbox = QCheckBox("Insert missing module docstrings")
        self._module_checkbox.setChecked(True)
        self._class_checkbox = QCheckBox("Insert missing class docstrings")
        self._class_checkbox.setChecked(True)
        self._function_checkbox = QCheckBox("Insert missing function/method docstrings")
        self._function_checkbox.setChecked(True)
        self._confirm_write_checkbox = QCheckBox("Require confirm before write")
        self._confirm_write_checkbox.setChecked(True)

        self._ai_panel = AISettingsPanel()

        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setLineWrapMode(QPlainTextEdit.NoWrap)
        self._output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        self._progress_bar.setTextVisible(True)
        self._progress_bar.setFormat("Processing %v / %m files")

        self._build_ui()

    def _build_ui(self) -> None:
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)

        for label, slot in [
            ("Run", self.run_selected_mode),
            ("Clear Output", self._output.clear),
            ("Save Output", self.save_output),
            ("Help", self.show_help),
        ]:
            act = QAction(label, self)
            act.triggered.connect(slot)
            toolbar.addAction(act)

        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        form = QFormLayout()
        form.addRow("Worker script", QLabel(self._worker_path_edit.text()))

        root_row = QHBoxLayout()
        root_row.addWidget(self._root_path_edit)
        browse_root_btn = QPushButton("Browse…")
        browse_root_btn.clicked.connect(self.browse_root)
        root_row.addWidget(browse_root_btn)
        form.addRow("Project root", root_row)

        form.addRow("Mode", self._mode_combo)
        form.addRow("", self._module_checkbox)
        form.addRow("", self._class_checkbox)
        form.addRow("", self._function_checkbox)
        form.addRow("", self._confirm_write_checkbox)
        layout.addLayout(form)

        # AI panel sits between main form and buttons.
        layout.addWidget(self._ai_panel)

        buttons = QHBoxLayout()
        self._run_button = QPushButton("Run Selected Mode")
        self._run_button.clicked.connect(self.run_selected_mode)
        buttons.addWidget(self._run_button)
        for mode in ("scan", "diff", "write"):
            btn = QPushButton(mode.capitalize())
            btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))
            buttons.addWidget(btn)
        help_btn = QPushButton("What do these options do?")
        help_btn.clicked.connect(self.show_help)
        buttons.addWidget(help_btn)
        buttons.addWidget(self._confirm_write_checkbox)
        layout.addLayout(buttons)

        layout.addWidget(QLabel("Output"))
        layout.addWidget(self._output, stretch=1)

        status = QStatusBar(self)
        status.addPermanentWidget(self._progress_bar)
        self.setStatusBar(status)
        status.showMessage("Ready")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def browse_root(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self, "Select project root",
            self._root_path_edit.text().strip() or str(Path.cwd()),
        )
        if path:
            self._root_path_edit.setText(path)

    def run_selected_mode(self) -> None:
        self.run_mode(self._mode_combo.currentText())

    def run_mode(self, mode: str) -> None:
        worker_path = Path(self._worker_path_edit.text().strip())
        root_path = Path(self._root_path_edit.text().strip())

        if not worker_path.exists():
            QMessageBox.critical(self, "Missing worker script",
                                 f"Worker script not found:\n{worker_path}")
            return
        if not root_path.exists():
            QMessageBox.critical(self, "Invalid project root",
                                 f"Project root not found:\n{root_path}")
            return
        if mode == "write" and self._confirm_write_checkbox.isChecked():
            box = QMessageBox(self)
            box.setIcon(QMessageBox.Warning)
            box.setWindowTitle("Confirm write")
            box.setText("Write mode will insert missing docstrings into source files.")
            box.setInformativeText("Only missing docstrings will be inserted. Continue?")
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            box.setDefaultButton(QMessageBox.No)
            if box.exec() != QMessageBox.Yes:
                return
        if self._worker_thread is not None:
            QMessageBox.warning(self, "Work running",
                                "Wait for the current work to finish first.")
            return

        self._last_mode_run = mode
        self._files_done = 0
        ai_tag = " [AI]" if self._ai_panel.ai_enabled else ""
        self._output.appendPlainText(
            f"> run: {worker_path} --root {root_path} --{mode}{ai_tag}\n"
        )
        self._run_button.setEnabled(False)
        self._progress_bar.setValue(0)
        self._progress_bar.setMaximum(0)   # indeterminate until first tick
        self._progress_bar.setVisible(True)
        self.statusBar().showMessage(f"Running {mode}…")

        self._worker_thread = QThread(self)
        self._worker = DocstringRunWorker(
            worker_script_path=str(worker_path),
            project_root=str(root_path),
            mode=mode,
            include_module=self._module_checkbox.isChecked(),
            include_classes=self._class_checkbox.isChecked(),
            include_functions=self._function_checkbox.isChecked(),
            ai_enabled=self._ai_panel.ai_enabled,
            ai_config_path=self._ai_panel.ai_config_path,
            workers=self._ai_panel.workers,
        )
        self._worker.moveToThread(self._worker_thread)

        self._worker_thread.started.connect(self._worker.run)
        self._worker.output_ready.connect(self._append_text)
        self._worker.file_complete.connect(self._handle_file_complete)
        self._worker.progress_tick.connect(self._handle_progress_tick)
        self._worker.finished_ok.connect(self._handle_worker_success)
        self._worker.finished_error.connect(self._handle_worker_error)
        self._worker.finished_ok.connect(self._worker_thread.quit)
        self._worker.finished_error.connect(self._worker_thread.quit)
        self._worker_thread.finished.connect(self._cleanup_worker)

        self._worker_thread.start()

    # ------------------------------------------------------------------
    # Slots — worker feedback
    # ------------------------------------------------------------------

    def _append_text(self, text: str) -> None:
        if not text:
            return
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)
        self._output.insertPlainText(text)
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)

    def _handle_file_complete(self, payload: object) -> None:
        """Update the output log when one file finishes."""
        p = payload  # _ProgressPayload
        ai_tag = " [AI]" if getattr(p, "ai_used", False) else ""
        fb = getattr(p, "fallback_count", 0)
        fb_tag = f" ({fb} fallback)" if fb else ""
        err = getattr(p, "error", "")
        if err:
            self._output.appendPlainText(f"  ERROR {p.filename}: {err}")
        else:
            syms = getattr(p, "symbols_done", "?")
            self._output.appendPlainText(
                f"  DONE  {p.filename}  ({syms} docstring(s)){ai_tag}{fb_tag}"
            )

    def _handle_progress_tick(self, done: int, total: int) -> None:
        """Drive the progress bar."""
        if self._progress_bar.maximum() == 0 and total > 0:
            self._progress_bar.setMaximum(total)
        self._progress_bar.setValue(done)
        self.statusBar().showMessage(
            f"Running {self._last_mode_run}… {done}/{total} files"
        )

    def _handle_worker_success(self, mode: str) -> None:
        self._run_button.setEnabled(True)
        self._progress_bar.setVisible(False)
        self.statusBar().showMessage(f"Finished {mode}")
        self._output.appendPlainText(f"\n[finished] mode={mode} exit_code=0\n")
        QMessageBox.information(self, "Work done", f"{mode.capitalize()} completed successfully.")

    def _handle_worker_error(self, mode: str, details: str) -> None:
        self._run_button.setEnabled(True)
        self._progress_bar.setVisible(False)
        self.statusBar().showMessage(f"Finished {mode} with issues")
        self._output.appendPlainText(f"\n[finished] mode={mode} exit_code=1\n{details}\n")
        QMessageBox.warning(
            self, "Work finished with issues",
            f"{mode.capitalize()} finished with issues.\nCheck the output panel for details.",
        )

    def _cleanup_worker(self) -> None:
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread is not None:
            self._worker_thread.deleteLater()
            self._worker_thread = None

    # ------------------------------------------------------------------
    # Help / save
    # ------------------------------------------------------------------

    def show_help(self) -> None:
        QMessageBox.information(self, "Help", (
            "Scan\n"
            "  Lists files missing module/class/function docstrings.\n\n"
            "Diff\n"
            "  Previews exact docstring insertions without changing files.\n\n"
            "Write\n"
            "  Inserts only missing docstrings into source files.\n\n"
            "AI Settings (checkbox to enable)\n"
            "  Uses a local LLM (e.g. Ollama) to generate precise, code-aware\n"
            "  docstrings instead of simple name-based heuristics.\n"
            "  Workers = number of files processed in parallel.\n"
            "  Falls back to heuristic if the AI call fails or times out.\n\n"
            "Safety rule\n"
            "  Only missing docstrings are inserted.  Existing code is never rewritten."
        ))

    def save_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save output",
            str(Path.cwd() / "missing_docstrings_output.txt"),
            "Text Files (*.txt)",
        )
        if not path:
            return
        Path(path).write_text(self._output.toPlainText(), encoding="utf-8")
        self.statusBar().showMessage(f"Saved output to {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    app = QApplication(sys.argv)
    window = MissingDocstringsWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
