"""Qt window for the Workflow Review GUI.

This is the canonical readable source for Workflow Review. The older
encoded backend payload is deprecated and must not be used as the main
editable source for this tab.
"""
from __future__ import annotations
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
import sys
from importlib import import_module
from pathlib import Path
from PySide6.QtCore import QThread
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QPlainTextEdit, QSizePolicy, QStatusBar, QToolBar, QVBoxLayout, QWidget
from .workflow_gui_constants import _WORKFLOW_GUI_DEFAULT_MANAGER_NAME, _WORKFLOW_GUI_DEFAULT_PROJECT_ROOT
from .workflow_gui_history import get_recent_roots, get_recent_scripts, record_root, record_script
from .workflow_gui_worker import WorkflowRunWorker
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window
__all__ = ['WorkflowManagerWindow', 'main']

class WorkflowManagerWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Workflow & Architecture Manager')
        self.resize(1200, 820)
        self._worker_thread: QThread | None = None
        self._worker: WorkflowRunWorker | None = None
        self._script_row_label: QLabel | None = None
        self._script_row_widget: QWidget | None = None
        self._browse_script_btn: QPushButton | None = None
        self._script_selector_moved_to_host = False
        self._project_root_controls_moved_to_host = False
        recent_scripts = get_recent_scripts()
        default_script = recent_scripts[0] if recent_scripts else str(Path(__file__).resolve().parent / _WORKFLOW_GUI_DEFAULT_MANAGER_NAME)
        self._script_combo = QComboBox()
        self._script_combo.setEditable(True)
        self._script_combo.setMinimumWidth(500)
        self._script_combo.addItem(default_script)
        seen_scripts: set[str] = {default_script}
        for s in recent_scripts:
            if s not in seen_scripts:
                self._script_combo.addItem(s)
                seen_scripts.add(s)
        arch_sibling = str(Path(__file__).resolve().parent / 'manage_architecture.py')
        if arch_sibling not in seen_scripts:
            self._script_combo.addItem(arch_sibling)
        recent_roots = get_recent_roots()
        default_root = recent_roots[0] if recent_roots else _WORKFLOW_GUI_DEFAULT_PROJECT_ROOT
        self._root_path_label = QLabel('Project Root:')
        self._root_path_label.setStyleSheet('color: #0B3D91; font-weight: bold; padding-left: 4px;')
        self._root_combo = QComboBox()
        self._root_combo.setEditable(True)
        self._root_combo.setMinimumWidth(180)
        self._root_combo.setMaximumWidth(360)
        self._root_combo.addItem(default_root)
        seen_roots: set[str] = {default_root}
        for r in recent_roots:
            if r not in seen_roots:
                self._root_combo.addItem(r)
                seen_roots.add(r)
        self._browse_root_btn = QPushButton('Browse...')
        self._browse_root_btn.clicked.connect(self.browse_root)
        self._python_path_label = QLabel(sys.executable)
        self._python_path_label.setFont(QFont('Courier New', 9))
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
        self._output.setFont(QFont('Courier New', 9))
        self._output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._build_ui()

    def _current_script_path(self) -> Path:
        return Path(self._script_combo.currentText().strip())

    def _current_root_path(self) -> Path:
        return Path(self._root_combo.currentText().strip())

    def _build_ui(self) -> None:
        toolbar = QToolBar('Main')
        self.addToolBar(toolbar)
        self._mode_action_toolbar_widget = QWidget(self)
        self._mode_action_toolbar_widget.setObjectName('workflow_review_mode_action_toolbar_widget')
        mode_action_toolbar_layout = QHBoxLayout(self._mode_action_toolbar_widget)
        mode_action_toolbar_layout.setContentsMargins(0, 0, 8, 0)
        mode_action_toolbar_layout.setSpacing(6)
        self._run_button = QPushButton('Run Selected Mode')
        self._run_button.setDefault(True)
        self._run_button.setToolTip('Run the mode currently selected in the Mode list')
        self._run_button.clicked.connect(self.run_selected_mode)
        mode_action_toolbar_layout.addWidget(self._run_button)
        self._mode_quick_buttons: dict[str, QPushButton] = {}
        for mode in ('validate', 'diff', 'scan', 'write'):
            btn = QPushButton(mode.capitalize())
            btn.setToolTip(f'Run {mode} immediately')
            btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))
            self._mode_quick_buttons[mode] = btn
            mode_action_toolbar_layout.addWidget(btn)
        toolbar.addWidget(self._mode_action_toolbar_widget)
        toolbar.addSeparator()
        self._run_options_toolbar_widget = QWidget(self)
        self._run_options_toolbar_widget.setObjectName('workflow_review_run_options_toolbar_widget')
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
        self._mode_help_toolbar_button = QPushButton('What do these modes do?')
        self._mode_help_toolbar_button.setObjectName('workflow_review_mode_help_toolbar_button')
        self._mode_help_toolbar_button.clicked.connect(self.show_mode_help)
        toolbar.addWidget(self._mode_help_toolbar_button)
        toolbar.addSeparator()
        clear_action = QAction('Clear Output', self)
        clear_action.triggered.connect(self._output.clear)
        toolbar.addAction(clear_action)
        save_action = QAction('Save Output...', self)
        save_action.triggered.connect(self.save_output)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        history_action = QAction('Show History', self)
        history_action.triggered.connect(self.show_history)
        toolbar.addAction(history_action)
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.addWidget(QLabel('Output'))
        layout.addWidget(self._output, stretch=1)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage('Ready')

    def move_script_selector_to_layout(self, destination_layout, insert_index: int | None=None) -> None:
        """Deprecated host move hook; Workflow Review no longer shows script controls."""
        return

    def move_project_root_controls_to_layout(self, destination_layout, insert_index: int | None=None) -> None:
        """Move Workflow Review Project Root controls into the host source row."""
        if self._project_root_controls_moved_to_host:
            return
        self._root_path_label.setParent(None)
        self._root_combo.setParent(None)
        self._browse_root_btn.setParent(None)
        if insert_index is None:
            destination_layout.addSpacing(12)
            destination_layout.addWidget(self._root_path_label, 0)
            destination_layout.addWidget(self._root_combo, 0)
            destination_layout.addWidget(self._browse_root_btn, 0)
        else:
            destination_layout.insertSpacing(insert_index, 12)
            destination_layout.insertWidget(insert_index + 1, self._root_path_label, 0)
            destination_layout.insertWidget(insert_index + 2, self._root_combo, 0)
            destination_layout.insertWidget(insert_index + 3, self._browse_root_btn, 0)
        self._project_root_controls_moved_to_host = True

    def browse_script(self) -> None:
        start = str(self._current_script_path().parent)
        path, _ = QFileDialog.getOpenFileName(self, 'Select worker script', start, 'Python files (*.py)')
        if path:
            if self._script_combo.findText(path) == -1:
                self._script_combo.insertItem(0, path)
            self._script_combo.setCurrentText(path)

    def browse_root(self) -> None:
        path = QFileDialog.getExistingDirectory(self, 'Select project root', self._root_combo.currentText().strip() or str(Path.cwd()))
        if path:
            if self._root_combo.findText(path) == -1:
                self._root_combo.insertItem(0, path)
            self._root_combo.setCurrentText(path)

    def run_selected_mode(self) -> None:
        self.run_mode(self._mode_combo.currentText())

    def run_mode(self, mode: str) -> None:
        script_path = self._current_script_path()
        root_path = self._current_root_path()
        if not script_path.exists():
            show_error_copy_close_window(self, title='Missing worker script', message=f'Worker script not found:\n{script_path}\n\nUse the Browse button or type the correct path.')
            return
        if not root_path.exists():
            show_error_copy_close_window(self, title='Invalid project root', message=f'Project root not found:\n{root_path}')
            return
        if mode == 'write' and self._strict_write_checkbox.isChecked():
            if not self._confirm_write(script_path.name):
                return
        if self._worker_thread is not None:
            QMessageBox.warning(self, 'Work running', 'Wait for the current work to finish first.')
            return
        record_root(str(root_path.resolve()))
        record_script(str(script_path.resolve()))
        self._output.clear()
        self._output.appendPlainText(f'> {script_path.name} --root {root_path} --{mode}\n')
        self._run_button.setEnabled(False)
        self.statusBar().showMessage(f'Running {mode}...')
        self._worker_thread = QThread(self)
        self._worker = WorkflowRunWorker(manager_script_path=str(script_path), project_root=str(root_path), mode=mode)
        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.started.connect(self._worker.run)
        self._worker.output_ready.connect(self._append_text)
        self._worker.finished_ok.connect(self._handle_worker_success)
        self._worker.finished_error.connect(self._handle_worker_error)
        self._worker.finished_ok.connect(self._worker_thread.quit)
        self._worker.finished_error.connect(self._worker_thread.quit)
        self._worker_thread.finished.connect(self._cleanup_worker)
        self._worker_thread.start()

    def _confirm_write(self, script_name: str) -> bool:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle('Confirm write')
        box.setText(f'Write mode will update files on disk via {script_name}.')
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
        self.statusBar().showMessage(f'OK Finished {mode}')
        self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=0\n')
        show_auto_close_action_window(self, title='Done', message=f'{mode.capitalize()} completed successfully.')

    def _handle_worker_error(self, mode: str, details: str) -> None:
        self._run_button.setEnabled(True)
        self.statusBar().showMessage(f'ERROR Finished {mode} with issues')
        self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=1\n{details}\n')
        QMessageBox.warning(self, 'Finished with issues', f'{mode.capitalize()} finished with issues.\nCheck the output panel for details.')

    def _cleanup_worker(self) -> None:
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread is not None:
            self._worker_thread.deleteLater()
            self._worker_thread = None

    def show_history(self) -> None:
        roots = get_recent_roots()
        scripts = get_recent_scripts()
        lines: list[str] = []
        if roots:
            lines.append('Recent project roots:')
            for i, r in enumerate(roots, 1):
                lines.append(f'  {i}. {r}')
        else:
            lines.append('No recent project roots.')
        lines.append('')
        if scripts:
            lines.append('Recent worker scripts:')
            for i, s in enumerate(scripts, 1):
                lines.append(f'  {i}. {s}')
        else:
            lines.append('No recent worker scripts.')
        QMessageBox.information(self, 'Session History', '\n'.join(lines))

    def show_mode_help(self) -> None:
        script_name = self._current_script_path().name
        is_arch = 'architecture' in script_name.lower()
        if is_arch:
            help_text = 'Validate\n  Checks docstrings, package declarations, EXPOSES/EXPORTS vs __all__,\n  module size, helper-group conventions, and duplicate public symbols.\n\nDiff\n  Previews changes to architecture_manifest.json, ARCHITECTURE.md,\n  and generated __init__.py facades - without writing anything.\n\nScan\n  Prints the full architecture manifest as JSON (read-only).\n\nWrite\n  Writes architecture_manifest.json, ARCHITECTURE.md, and minimal\n  __init__.py facades. Blocked if validation has errors.'
        else:
            help_text = 'Validate\n  Runs tests, runtime smoke commands, business checks, GUI flows,\n  integration commands, performance commands, and import probes.\n\nDiff\n  Previews changes to workflow_manifest.json and WORKFLOWS.md.\n\nScan\n  Prints the generated workflow manifest template as JSON.\n\nWrite\n  Writes workflow_manifest.json and WORKFLOWS.md.\n  Blocked if validation has failures.'
        QMessageBox.information(self, f'Mode Help - {script_name}', help_text)

    def save_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, 'Save output', str(Path.cwd() / 'manager_output.txt'), 'Text Files (*.txt)')
        if not path:
            return
        Path(path).write_text(self._output.toPlainText(), encoding='utf-8')
        self.statusBar().showMessage(f'Saved output to {path}')

def main() -> int:
    app = QApplication(sys.argv)
    window = WorkflowManagerWindow()
    window.show()
    return app.exec()
_BaseWorkflowManagerWindow = WorkflowManagerWindow

def _load_tab2_ai_review_window_factory():
    """Return the optional Tab 2 AI review window enhancer."""
    module_name = 'kanda_reasoner_app.' + 'manage_' + 'workflows.ai_review.gui_integration'
    return import_module(module_name).create_tab2_ai_review_window_class
try:
    _create_tab2_ai_review_window_class = _load_tab2_ai_review_window_factory()
except Exception:
    pass
else:
    WorkflowManagerWindow = _create_tab2_ai_review_window_class(_BaseWorkflowManagerWindow)
    globals()['WorkflowManagerWindow'] = WorkflowManagerWindow
__all__ = ['WorkflowManagerWindow', 'main']
