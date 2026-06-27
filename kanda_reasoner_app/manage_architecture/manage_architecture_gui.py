"""Qt GUI for running architecture scan, validate, diff, and write modes."""
from __future__ import annotations

from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
def _install_deleted_legacy_root_importlib_aliases():
    """Install in-process aliases for deleted legacy payload imports."""
    import importlib
    import sys
    legacy_root_name = 'ask_ai' + '_project_reasoner'
    legacy_engine_name = legacy_root_name + '.project_reasoner_v10'
    canonical_root = importlib.import_module('kanda_reasoner_app')
    sys.modules.setdefault(legacy_root_name, canonical_root)
    try:
        canonical_engine = importlib.import_module('kanda_reasoner_app.reasoner_engine')
    except ModuleNotFoundError:
        return
    sys.modules.setdefault(legacy_engine_name, canonical_engine)
    setattr(canonical_root, 'project_reasoner_v10', canonical_engine)
_install_deleted_legacy_root_importlib_aliases()
import logging
import contextlib
import importlib.util
import io
import sys
import traceback
from pathlib import Path
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QPlainTextEdit, QSizePolicy, QStatusBar, QToolBar, QVBoxLayout, QWidget
import importlib as _architecture_gui_importlib
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window
_STAGED_PACKAGE_NAME = 'ask' + '_ai' + '_project' + '_reasoner'
_AI_REVIEW_GUI_MODULE = _architecture_gui_importlib.import_module(_STAGED_PACKAGE_NAME + '.manage_architecture.ai_review.gui_integration')
install_tab1_ai_review_controls = _AI_REVIEW_GUI_MODULE.install_tab1_ai_review_controls
del _AI_REVIEW_GUI_MODULE
del _STAGED_PACKAGE_NAME
del _architecture_gui_importlib
DEFAULT_MANAGER_NAME = 'manage_architecture.py'
DEFAULT_PROJECT_ROOT = '.'
__all__ = ['ArchitectureManagerWindow', 'ArchitectureRunWorker', 'main']

class ArchitectureRunWorker(QObject):
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
                if hasattr(module, 'run'):
                    exit_code = module.run(self._project_root.resolve(), self._mode)
                elif hasattr(module, 'main'):
                    original_argv = sys.argv[:]
                    try:
                        sys.argv = [str(self._manager_script_path), '--root', str(self._project_root.resolve()), f'--{self._mode}']
                        exit_code = module.main()
                    finally:
                        sys.argv = original_argv
                else:
                    raise AttributeError('manage_architecture.py must expose either run(root, mode) or main().')
            captured = buffer.getvalue()
            if captured:
                self.output_ready.emit(captured)
            if int(exit_code) == 0:
                self.finished_ok.emit(self._mode)
            else:
                self.finished_error.emit(self._mode, f'Worker finished with exit code {exit_code}.')
        except Exception:
            logging.exception('Boundary failure in run')
            tb = traceback.format_exc()
            self.finished_error.emit(self._mode, tb)

    def _load_manager_module(self, script_path: Path):
        if not script_path.exists():
            raise FileNotFoundError(f'Worker script not found: {script_path}')
        module_name = 'architecture_manager_worker'
        spec = importlib.util.spec_from_file_location(module_name, str(script_path))
        if spec is None or spec.loader is None:
            raise ImportError(f'Could not load worker module from {script_path}')
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(module_name, None)
            raise
        return module

class ArchitectureManagerWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Architecture Manager')
        self.resize(1100, 760)
        self._last_mode_run = ''
        self._worker_thread: QThread | None = None
        self._worker: ArchitectureRunWorker | None = None
        self._ai_review_thread: QThread | None = None
        self._ai_review_worker: object | None = None
        self._script_path_edit = QLineEdit(str(self._manager_script_path()))
        self._script_path_edit.setMinimumWidth(360)
        self._script_path_edit.setMaximumWidth(720)
        self._browse_script_btn = QPushButton('Browse...')
        self._browse_script_btn.clicked.connect(self.browse_script)
        self._root_path_label = QLabel('Project Root:')
        self._root_path_label.setStyleSheet('color: #0B3D91; font-weight: bold; padding-left: 4px;')
        self._root_path_edit = QLineEdit(DEFAULT_PROJECT_ROOT)
        self._root_path_edit.setMinimumWidth(180)
        self._root_path_edit.setMaximumWidth(360)
        self._browse_root_btn = QPushButton('Browse...')
        self._browse_root_btn.clicked.connect(self.browse_root)
        self._project_root_controls_moved_to_host = False
        self._python_path_edit = QLineEdit(sys.executable)
        self._python_path_edit.setEnabled(False)
        self._mode_combo = QComboBox()
        self._mode_combo.setMinimumWidth(105)
        self._mode_combo.setMaximumWidth(130)
        self._mode_combo.addItems(['validate', 'diff', 'scan', 'write'])
        self._mode_combo.setCurrentText('validate')
        self._strict_write_checkbox = QCheckBox('Require confirm before write')
        self._strict_write_checkbox.setChecked(True)
        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setLineWrapMode(QPlainTextEdit.NoWrap)
        self._output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._build_ui()

    def _manager_script_path(self) -> Path:
        default_path = Path(__file__).resolve().parent / DEFAULT_MANAGER_NAME
        script_edit = getattr(self, '_script_path_edit', None)
        if script_edit is not None:
            text = script_edit.text().strip()
            if text:
                return Path(text)
        return default_path

    def _build_ui(self) -> None:
        toolbar = QToolBar('Main')
        self.addToolBar(toolbar)
        self._run_options_toolbar_widget = QWidget(self)
        self._run_options_toolbar_widget.setObjectName('architecture_review_run_options_toolbar_widget')
        run_options_toolbar_layout = QHBoxLayout(self._run_options_toolbar_widget)
        run_options_toolbar_layout.setContentsMargins(0, 0, 8, 0)
        run_options_toolbar_layout.setSpacing(6)
        self._run_options_toolbar_label = QLabel('Run options')
        self._mode_toolbar_label = QLabel('Mode')
        run_options_toolbar_layout.addWidget(self._run_options_toolbar_label)
        run_options_toolbar_layout.addWidget(self._mode_toolbar_label)
        run_options_toolbar_layout.addWidget(self._mode_combo)
        run_options_toolbar_layout.addWidget(self._strict_write_checkbox)
        toolbar.addWidget(self._run_options_toolbar_widget)
        toolbar.addSeparator()
        run_action = QAction('Run', self)
        run_action.triggered.connect(self.run_selected_mode)
        toolbar.addAction(run_action)
        clear_action = QAction('Clear Output', self)
        clear_action.triggered.connect(self._output.clear)
        toolbar.addAction(clear_action)
        save_action = QAction('Save Output', self)
        save_action.triggered.connect(self.save_output)
        toolbar.addAction(save_action)
        help_action = QAction('Mode Help', self)
        help_action.triggered.connect(self.show_mode_help)
        toolbar.addAction(help_action)
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        buttons = QHBoxLayout()
        self._run_button = QPushButton('Run Selected Mode')
        self._run_button.clicked.connect(self.run_selected_mode)
        buttons.addWidget(self._run_button)
        for mode in ('validate', 'diff', 'scan', 'write'):
            btn = QPushButton(mode.capitalize())
            btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))
            buttons.addWidget(btn)
        install_tab1_ai_review_controls(self, buttons)
        help_btn = QPushButton('What do these modes do?')
        help_btn.clicked.connect(self.show_mode_help)
        buttons.addWidget(help_btn)
        layout.addLayout(buttons)
        layout.addWidget(QLabel('Output'))
        layout.addWidget(self._output, stretch=1)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage('Ready')

    def move_project_root_controls_to_layout(self, destination_layout, insert_index: int | None=None) -> None:
        """Move the Tab 1 project-root controls into the host source row."""
        if self._project_root_controls_moved_to_host:
            return
        self._root_path_label.setParent(None)
        self._root_path_edit.setParent(None)
        self._browse_root_btn.setParent(None)
        if insert_index is None:
            destination_layout.addSpacing(12)
            destination_layout.addWidget(self._root_path_label, 0)
            destination_layout.addWidget(self._root_path_edit, 0)
            destination_layout.addWidget(self._browse_root_btn, 0)
        else:
            destination_layout.insertSpacing(insert_index, 12)
            destination_layout.insertWidget(insert_index + 1, self._root_path_label, 0)
            destination_layout.insertWidget(insert_index + 2, self._root_path_edit, 0)
            destination_layout.insertWidget(insert_index + 3, self._browse_root_btn, 0)
        self._project_root_controls_moved_to_host = True

    def browse_script(self) -> None:
        start = str(self._manager_script_path().parent)
        path, _ = QFileDialog.getOpenFileName(self, 'Select worker script', start, 'Python files (*.py)')
        if path:
            self._script_path_edit.setText(path)

    def browse_root(self) -> None:
        path = QFileDialog.getExistingDirectory(self, 'Select project root', self._root_path_edit.text().strip() or str(Path.cwd()))
        if path:
            self._root_path_edit.setText(path)

    def run_selected_mode(self) -> None:
        self.run_mode(self._mode_combo.currentText())

    def run_mode(self, mode: str) -> None:
        script_path = self._manager_script_path()
        root_path = Path(self._root_path_edit.text().strip())
        if not script_path.exists():
            show_error_copy_close_window(self, title='Missing worker script', message=f'The GUI could not find the sibling worker script:\n{script_path}\n\nPlace manage_architecture.py in the same folder as this GUI file.')
            return
        if not root_path.exists():
            show_error_copy_close_window(self, title='Invalid project root', message=f'Project root not found:\n{root_path}')
            return
        if mode == 'write' and self._strict_write_checkbox.isChecked():
            if not self._confirm_write():
                return
        if self._worker_thread is not None or self._ai_review_thread is not None:
            QMessageBox.warning(self, 'Work running', 'Wait for the current work to finish first.')
            return
        self._last_mode_run = mode
        self._output.clear()
        indicator = getattr(self, '_tab1_activity_indicator', None)
        if indicator is not None:
            indicator.start_heuristic(mode)
        self._output.appendPlainText(f'> in-process run: {script_path} --root {root_path} --{mode}\n')
        self._run_button.setEnabled(False)
        self.statusBar().showMessage(f'Running {mode}...')
        self._worker_thread = QThread(self)
        self._worker = ArchitectureRunWorker(manager_script_path=str(script_path), project_root=str(root_path), mode=mode)
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
        box.setWindowTitle('Confirm write')
        box.setText('Write mode can update __init__.py files, ARCHITECTURE.md, and architecture_manifest.json.')
        box.setInformativeText('Continue?')
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
        indicator = getattr(self, '_tab1_activity_indicator', None)
        if indicator is not None:
            indicator.finish_success(f'{mode} finished')
        self.statusBar().showMessage(f'Finished {mode}')
        self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=0\n')
        show_auto_close_action_window(self, title='Work done', message=f'{mode.capitalize()} completed successfully.')

    def _handle_worker_error(self, mode: str, details: str) -> None:
        self._run_button.setEnabled(True)
        indicator = getattr(self, '_tab1_activity_indicator', None)
        if indicator is not None:
            indicator.finish_error(f'{mode} finished with issues')
        self.statusBar().showMessage(f'Finished {mode} with issues')
        self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=1\n{details}\n')
        QMessageBox.warning(self, 'Work finished with issues', f'{mode.capitalize()} finished with issues.\nCheck the output panel for details.')

    def _cleanup_worker(self) -> None:
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread is not None:
            self._worker_thread.deleteLater()
            self._worker_thread = None

    def show_mode_help(self) -> None:
        help_text = 'Validate\n- checks the project tree for duplicate public symbols, helper-folder rule violations, docstring mismatches, and oversized modules.\n\nDiff\n- previews the changes that would be written to __init__.py files, ARCHITECTURE.md, and architecture_manifest.json.\n\nScan\n- prints the full manifest JSON describing the project structure.\n\nWrite\n- writes architecture_manifest.json, minimal __init__.py facades, and ARCHITECTURE.md, but only when validation has no errors.'
        QMessageBox.information(self, 'Mode Help', help_text)

    def save_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, 'Save output', str(Path.cwd() / 'architecture_manager_output.txt'), 'Text Files (*.txt)')
        if not path:
            return
        Path(path).write_text(self._output.toPlainText(), encoding='utf-8')
        self.statusBar().showMessage(f'Saved output to {path}')

def main() -> int:
    app = QApplication(sys.argv)
    window = ArchitectureManagerWindow()
    window.show()
    return app.exec()
if __name__ == '__main__':
    raise SystemExit(main())
