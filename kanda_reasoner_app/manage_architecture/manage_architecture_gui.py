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
from PySide6.QtCore import QObject, QThread, Signal, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QPlainTextEdit, QSizePolicy, QStatusBar, QToolBar, QVBoxLayout, QWidget
import importlib as _architecture_gui_importlib
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window
from kanda_reasoner_app.manage_architecture.large_module_split_audit import run_large_module_split_audit
from kanda_reasoner_app.manage_architecture.large_module_target_queue import LargeModuleTarget, count_python_lines, format_target_counter, normalize_target_text, parse_module_too_large_findings
_STAGED_PACKAGE_NAME = 'ask' + '_ai' + '_project' + '_reasoner'
_AI_REVIEW_GUI_MODULE = _architecture_gui_importlib.import_module(_STAGED_PACKAGE_NAME + '.manage_architecture.ai_review.gui_integration')
install_tab1_ai_review_controls = _AI_REVIEW_GUI_MODULE.install_tab1_ai_review_controls
del _AI_REVIEW_GUI_MODULE
del _STAGED_PACKAGE_NAME
del _architecture_gui_importlib
DEFAULT_MANAGER_NAME = 'manage_architecture.py'
DEFAULT_PROJECT_ROOT = '.'
LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH = 'kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md'
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
        self._operation_cancel_requested = False
        self._cancel_operation_button: QPushButton | None = None
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
        self._large_module_target_edit = QLineEdit('')
        self._large_module_target_edit.setPlaceholderText('Run Validate to populate oversized module targets')
        self._large_module_target_edit.setMinimumWidth(360)
        self._large_module_target_edit.setMaximumWidth(720)
        self._large_module_targets: list[LargeModuleTarget] = []
        self._large_module_target_index = -1
        self._large_module_target_source = 'none'
        self._last_large_module_split_handoff = ''
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
        clear_action = QAction('Clear Audit Results', self)
        clear_action.triggered.connect(self._output.clear)
        toolbar.addAction(clear_action)
        save_action = QAction('Save Audit Results', self)
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
        self._mode_quick_buttons: dict[str, QPushButton] = {}
        for mode in ('validate', 'diff', 'scan', 'write'):
            btn = QPushButton(mode.capitalize())
            btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))
            self._mode_quick_buttons[mode] = btn
            buttons.addWidget(btn)
        self._cancel_operation_button = QPushButton('Cancel')
        self._cancel_operation_button.setObjectName('architecture_review_cancel_operation_button')
        self._cancel_operation_button.setToolTip('Cancel the currently running Architecture operation. Hard cancellation may stop a worker thread mid-run.')
        self._cancel_operation_button.setStyleSheet(
            'QPushButton { color: #C2185B; font-weight: bold; } '
            'QPushButton:disabled { color: #9A9A9A; }'
        )
        self._cancel_operation_button.setEnabled(False)
        self._cancel_operation_button.clicked.connect(self.cancel_running_operation)
        buttons.addWidget(self._cancel_operation_button)
        install_tab1_ai_review_controls(self, buttons)
        help_btn = QPushButton('What do these modes do?')
        help_btn.clicked.connect(self.show_mode_help)
        buttons.addWidget(help_btn)
        layout.addLayout(buttons)
        audit_header = QHBoxLayout()
        self._audit_results_label = QLabel('Project Audit Results')
        self._audit_results_label.setStyleSheet(
            'color: #2E7D32; '
            'font-weight: bold; '
            'border: 1px solid #2E7D32; '
            'border-radius: 4px; '
            'padding: 4px 8px;'
        )
        audit_header.addWidget(self._audit_results_label)
        self._copy_audit_btn = QPushButton('Copy Audit Results')
        self._copy_audit_btn.clicked.connect(self.copy_audit_to_clipboard)
        audit_header.addWidget(self._copy_audit_btn)
        self._copy_large_module_protocol_btn = QPushButton('Large Module Creation/Refactor Protocol')
        self._copy_large_module_protocol_btn.clicked.connect(self.copy_large_module_protocol_to_clipboard)
        audit_header.addWidget(self._copy_large_module_protocol_btn)
        audit_header.addStretch(1)
        layout.addLayout(audit_header)
        split_header = QHBoxLayout()
        self._large_module_split_label = QLabel('Large Module AST Split Audit')
        self._large_module_split_label.setStyleSheet('color: #6A1B9A; font-weight: bold; padding: 4px 8px;')
        split_header.addWidget(self._large_module_split_label)
        split_header.addWidget(QLabel('Target .py:'))
        split_header.addWidget(self._large_module_target_edit, stretch=1)
        self._large_module_target_count_label = QLabel('0 large modules')
        self._large_module_target_count_label.setMinimumWidth(120)
        split_header.addWidget(self._large_module_target_count_label)
        self._copy_large_module_target_path_btn = QPushButton('Copy Path')
        self._copy_large_module_target_path_btn.setObjectName('architecture_review_copy_large_module_target_path_button')
        self._copy_large_module_target_path_btn.setToolTip('Copy the selected Large Module AST Audit target .py path to clipboard')
        self._copy_large_module_target_path_btn.clicked.connect(self.copy_large_module_target_path_to_clipboard)
        split_header.addWidget(self._copy_large_module_target_path_btn)
        self._prev_large_module_target_btn = QPushButton('<-')
        self._prev_large_module_target_btn.setToolTip('Previous oversized module from latest Project Audit Results')
        self._prev_large_module_target_btn.clicked.connect(lambda: self._move_large_module_target(-1))
        split_header.addWidget(self._prev_large_module_target_btn)
        self._next_large_module_target_btn = QPushButton('->')
        self._next_large_module_target_btn.setToolTip('Next oversized module from latest Project Audit Results')
        self._next_large_module_target_btn.clicked.connect(lambda: self._move_large_module_target(1))
        split_header.addWidget(self._next_large_module_target_btn)
        self._browse_large_module_target_btn = QPushButton('Browse Target...')
        self._browse_large_module_target_btn.clicked.connect(self.browse_large_module_target)
        split_header.addWidget(self._browse_large_module_target_btn)
        self._run_large_module_split_btn = QPushButton('Run AST Split Audit')
        self._run_large_module_split_btn.clicked.connect(self.run_large_module_split_audit_from_gui)
        split_header.addWidget(self._run_large_module_split_btn)
        self._copy_large_module_split_btn = QPushButton('Copy Split Handoff for AI')
        self._copy_large_module_split_btn.clicked.connect(self.copy_large_module_split_handoff)
        split_header.addWidget(self._copy_large_module_split_btn)
        self._large_module_target_edit.textChanged.connect(lambda _text='': self._sync_large_module_target_controls())
        layout.addLayout(split_header)
        self._sync_large_module_target_controls()
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
            QMessageBox.warning(self, 'Work running', 'Cancel or wait for the current work to finish first.')
            return
        self._operation_cancel_requested = False
        self._set_operation_buttons_running(True)
        self._last_mode_run = mode
        self._reset_large_module_target_state_for_new_project_audit_run(mode)
        self._output.clear()
        indicator = getattr(self, '_tab1_activity_indicator', None)
        if indicator is not None:
            indicator.start_heuristic(mode)
        self._output.appendPlainText(f'> in-process audit run: {script_path} --root {root_path} --{mode}\n')
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
        if self._operation_cancel_requested:
            self.statusBar().showMessage(f'Canceled {mode}')
            self._output.appendPlainText(f'\n[canceled] mode={mode} late success ignored\n')
            return
        self._set_operation_buttons_running(False)
        indicator = getattr(self, '_tab1_activity_indicator', None)
        if indicator is not None:
            indicator.finish_success(f'{mode} finished')
        self.statusBar().showMessage(f'Finished {mode}')
        self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=0\n')
        if mode == 'validate':
            self._refresh_large_module_targets_from_audit_results()
        show_auto_close_action_window(self, title='Work done', message=f'{mode.capitalize()} completed successfully.')

    def _handle_worker_error(self, mode: str, details: str) -> None:
        if self._operation_cancel_requested:
            self.statusBar().showMessage(f'Canceled {mode}')
            self._output.appendPlainText(f'\n[canceled] mode={mode} late error ignored\n')
            return
        self._set_operation_buttons_running(False)
        indicator = getattr(self, '_tab1_activity_indicator', None)
        if indicator is not None:
            indicator.finish_error(f'{mode} finished with issues')
        self.statusBar().showMessage(f'Finished {mode} with issues')
        self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=1\n{details}\n')
        if mode == 'validate':
            self._refresh_large_module_targets_from_audit_results()
            if self._large_module_targets:
                self.statusBar().showMessage(f'Finished validate with issues; loaded {len(self._large_module_targets)} oversized module target(s)')
        QMessageBox.warning(self, 'Work finished with issues', f'{mode.capitalize()} finished with issues.\nCheck the audit panel for details.')

    def _cleanup_worker(self) -> None:
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread is not None:
            self._worker_thread.deleteLater()
            self._worker_thread = None
        self._set_operation_buttons_running(False)

    def _set_operation_buttons_running(self, running: bool) -> None:
        """Synchronize deterministic Architecture run/cancel controls."""
        for widget in (getattr(self, '_run_button', None),):
            if widget is not None:
                widget.setEnabled(not running)
        for button in getattr(self, '_mode_quick_buttons', {}).values():
            button.setEnabled(not running)
        cancel_button = getattr(self, '_cancel_operation_button', None)
        if cancel_button is not None:
            cancel_button.setEnabled(running)

    def cancel_running_operation(self) -> None:
        """Cancel the active Architecture worker or advisory review thread."""
        if self._worker_thread is not None:
            self._operation_cancel_requested = True
            self._set_operation_buttons_running(True)
            cancel_button = getattr(self, '_cancel_operation_button', None)
            if cancel_button is not None:
                cancel_button.setEnabled(False)
            mode = self._last_mode_run or self._mode_combo.currentText()
            self.statusBar().showMessage(f'Cancel requested for {mode}...')
            self._output.appendPlainText(f'\n[cancel requested] mode={mode}\n')
            indicator = getattr(self, '_tab1_activity_indicator', None)
            if indicator is not None:
                indicator.finish_error(f'{mode} canceled')
            self._worker_thread.requestInterruption()
            self._worker_thread.quit()
            QTimer.singleShot(300, self._force_cancel_worker_thread)
            return
        if self._ai_review_thread is not None:
            self._operation_cancel_requested = True
            self.statusBar().showMessage('Cancel requested for AI review...')
            self._output.appendPlainText('\n[cancel requested] advisory AI review\n')
            indicator = getattr(self, '_tab1_activity_indicator', None)
            if indicator is not None:
                indicator.finish_error('AI review canceled')
            self._ai_review_thread.requestInterruption()
            self._ai_review_thread.quit()
            QTimer.singleShot(300, self._force_cancel_ai_review_thread)
            return
        self.statusBar().showMessage('No running Architecture operation to cancel')

    def _force_cancel_worker_thread(self) -> None:
        thread = self._worker_thread
        if thread is not None and thread.isRunning():
            self._output.appendPlainText('[cancel] terminating Architecture worker thread.\n')
            thread.terminate()
            thread.wait(1000)

    def _force_cancel_ai_review_thread(self) -> None:
        thread = self._ai_review_thread
        if thread is not None and thread.isRunning():
            self._output.appendPlainText('[cancel] terminating Architecture AI review thread.\n')
            thread.terminate()
            thread.wait(1000)

    def copy_audit_to_clipboard(self) -> None:
        audit_text = self._output.toPlainText()
        QApplication.clipboard().setText(audit_text)
        self.statusBar().showMessage('Copied Project Audit Results to clipboard')

    def copy_large_module_protocol_to_clipboard(self) -> None:
        prompt_path = self._large_module_protocol_path()
        if prompt_path is None or not prompt_path.exists():
            show_error_copy_close_window(
                self,
                title='Large Module Creation/Refactor Protocol not found',
                message=(
                    'Could not find the canonical Large Module Creation/Refactor Protocol at:\n'
                    + LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH
                    + '\n\nSelect the active KANDA project root and try again.'
                ),
            )
            return
        QApplication.clipboard().setText(prompt_path.read_text(encoding='utf-8'))
        self.statusBar().showMessage('Copied Large Module Creation/Refactor Protocol to clipboard')

    def _large_module_protocol_path(self) -> Path | None:
        candidates: list[Path] = []
        root_text = self._root_path_edit.text().strip()
        if root_text:
            candidates.append(Path(root_text) / LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH)
        candidates.append(Path(__file__).resolve().parents[2] / LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH)
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0] if candidates else None

    def _reset_large_module_target_state_for_new_project_audit_run(self, mode: str) -> None:
        """Clear stale AST target data before replacing Project Audit Results."""
        self._large_module_targets = []
        self._large_module_target_index = -1
        self._large_module_target_source = 'pending' if mode == 'validate' else 'none'
        self._last_large_module_split_handoff = ''
        if hasattr(self, '_large_module_target_edit'):
            self._large_module_target_edit.clear()
            if mode == 'validate':
                self._large_module_target_edit.setPlaceholderText('Validate running - AST target queue will refresh from new results')
            else:
                self._large_module_target_edit.setPlaceholderText('Run Validate to populate oversized module targets')
        self._sync_large_module_target_controls()

    def _refresh_large_module_targets_from_audit_results(self) -> None:
        """Populate the AST target selector from MODULE_TOO_LARGE findings."""
        targets = parse_module_too_large_findings(self._output.toPlainText())
        self._large_module_targets = targets
        self._large_module_target_source = 'audit' if targets else 'none'
        self._large_module_target_index = 0 if targets else -1
        self._last_large_module_split_handoff = ''
        if targets:
            self._large_module_target_edit.setText(targets[0].path)
            self.statusBar().showMessage(f'Loaded {len(targets)} oversized module target(s) from Project Audit Results')
        else:
            self._large_module_target_edit.clear()
            self._large_module_target_edit.setPlaceholderText('No MODULE_TOO_LARGE findings in latest Validate output')
            self.statusBar().showMessage('No oversized modules found in latest Project Audit Results')
        self._sync_large_module_target_controls()

    def _sync_large_module_target_controls(self) -> None:
        """Enable AST controls only when an oversized module target is selected."""
        has_targets = bool(self._large_module_targets) and 0 <= self._large_module_target_index < len(self._large_module_targets)
        if hasattr(self, '_large_module_target_count_label'):
            self._large_module_target_count_label.setText(format_target_counter(self._large_module_targets, self._large_module_target_index))
        if hasattr(self, '_prev_large_module_target_btn'):
            navigation_enabled = len(self._large_module_targets) > 1
            self._prev_large_module_target_btn.setEnabled(navigation_enabled)
            self._next_large_module_target_btn.setEnabled(navigation_enabled)
        if hasattr(self, '_run_large_module_split_btn'):
            self._run_large_module_split_btn.setEnabled(has_targets)
        if hasattr(self, '_copy_large_module_split_btn'):
            self._copy_large_module_split_btn.setEnabled(bool(self._last_large_module_split_handoff))
        if hasattr(self, '_copy_large_module_target_path_btn'):
            target_text = self._large_module_target_edit.text().strip() if hasattr(self, '_large_module_target_edit') else ''
            self._copy_large_module_target_path_btn.setEnabled(bool(target_text))
        if hasattr(self, '_large_module_split_label'):
            if has_targets:
                self._large_module_split_label.setText('Large Module AST Split Audit')
                self._large_module_split_label.setToolTip('Active: oversized module target selected from audit findings or manual browse.')
            else:
                self._large_module_split_label.setText('Large Module AST Split Audit - inactive')
                self._large_module_split_label.setToolTip('Run Validate to populate MODULE_TOO_LARGE targets before running AST split audit.')

    def _select_large_module_target(self, index: int) -> None:
        """Select an oversized module target by index and refresh line information."""
        if not self._large_module_targets:
            self._large_module_target_index = -1
            self._large_module_target_edit.clear()
            self._sync_large_module_target_controls()
            return
        self._large_module_target_index = max(0, min(index, len(self._large_module_targets) - 1))
        current = self._large_module_targets[self._large_module_target_index]
        self._large_module_target_edit.setText(current.path)
        self._sync_large_module_target_controls()

    def _move_large_module_target(self, step: int) -> None:
        """Move through the audit-derived oversized-module queue."""
        self._prune_current_large_module_target_if_resolved()
        if not self._large_module_targets:
            return
        next_index = (self._large_module_target_index + step) % len(self._large_module_targets)
        self._select_large_module_target(next_index)

    def _prune_current_large_module_target_if_resolved(self) -> None:
        """Remove the current target when it has already dropped to 500 lines or below."""
        if not self._large_module_targets or not (0 <= self._large_module_target_index < len(self._large_module_targets)):
            self._sync_large_module_target_controls()
            return
        root_text = self._root_path_edit.text().strip() or str(Path.cwd())
        current = self._large_module_targets[self._large_module_target_index]
        current_lines = count_python_lines(root_text, current.path)
        if current_lines <= 0:
            self._sync_large_module_target_controls()
            return
        if current_lines <= 500:
            removed_path = current.path
            del self._large_module_targets[self._large_module_target_index]
            if self._large_module_targets:
                self._large_module_target_index = min(self._large_module_target_index, len(self._large_module_targets) - 1)
                self._select_large_module_target(self._large_module_target_index)
            else:
                self._large_module_target_index = -1
                self._large_module_target_edit.clear()
                self._large_module_target_edit.setPlaceholderText('No oversized module targets remain')
                self._sync_large_module_target_controls()
            self.statusBar().showMessage(f'Removed resolved module from AST queue: {removed_path}')
            return
        if current_lines != current.line_count:
            self._large_module_targets[self._large_module_target_index] = LargeModuleTarget(current.path, current_lines)
            self._large_module_targets.sort(key=lambda item: (-item.line_count, item.path.lower()))
            self._large_module_target_index = next(
                (idx for idx, target in enumerate(self._large_module_targets) if target.path == current.path),
                0,
            )
            self._sync_large_module_target_controls()

    def browse_large_module_target(self) -> None:
        root_text = self._root_path_edit.text().strip() or str(Path.cwd())
        start = str(Path(root_text)) if Path(root_text).exists() else str(Path.cwd())
        path, _ = QFileDialog.getOpenFileName(self, 'Select large module target', start, 'Python files (*.py)')
        if path:
            target_text = normalize_target_text(root_text, path)
            line_count = count_python_lines(root_text, target_text)
            self._last_large_module_split_handoff = ''
            if line_count <= 500:
                self._large_module_targets = []
                self._large_module_target_index = -1
                self._large_module_target_source = 'manual'
                self._large_module_target_edit.setText(target_text)
                self._large_module_target_edit.setPlaceholderText('Selected module is not above 500 lines')
                self._sync_large_module_target_controls()
                QMessageBox.information(self, 'AST target inactive', f'Selected module has {line_count} lines. AST Split Audit activates only for modules above 500 lines.')
                return
            self._large_module_targets = [LargeModuleTarget(target_text, line_count)]
            self._large_module_target_index = 0
            self._large_module_target_source = 'manual'
            self._large_module_target_edit.setText(target_text)
            self._sync_large_module_target_controls()
            self.statusBar().showMessage(f'Manual oversized AST target selected: {line_count} lines')

    def run_large_module_split_audit_from_gui(self) -> None:
        root_path = Path(self._root_path_edit.text().strip())
        self._prune_current_large_module_target_if_resolved()
        target_text = self._large_module_target_edit.text().strip()
        if not root_path.exists():
            show_error_copy_close_window(self, title='Invalid project root', message=f'Project root not found:\n{root_path}')
            return
        if not self._large_module_targets or not target_text:
            show_error_copy_close_window(self, title='AST Split Audit inactive', message='Run Validate first and select a MODULE_TOO_LARGE target, or Browse Target to choose a .py file above 500 lines.')
            return
        if self._worker_thread is not None or self._ai_review_thread is not None:
            QMessageBox.warning(self, 'Work running', 'Wait for the current work to finish first.')
            return
        try:
            result = run_large_module_split_audit(root_path, target_text)
        except Exception as exc:
            show_error_copy_close_window(self, title='AST Split Audit failed', message=str(exc))
            return
        self._last_large_module_split_handoff = result.markdown
        self._output.clear()
        self._output.appendPlainText(result.markdown)
        self._output.appendPlainText(f'\n[report] markdown={result.markdown_path}\n[report] json={result.json_path}\n')
        self._sync_large_module_target_controls()
        self.statusBar().showMessage('Large Module AST Split Audit completed')
        show_auto_close_action_window(self, title='AST Split Audit done', message='Read-only split audit completed. Use Copy Split Handoff for AI to paste the report into chat.')

    def copy_large_module_target_path_to_clipboard(self) -> None:
        """Copy the currently selected Large Module AST Audit target path."""
        target_text = self._large_module_target_edit.text().strip()
        if not target_text:
            self.statusBar().showMessage('No Large Module AST Audit target path to copy')
            return
        target_path = Path(target_text)
        if not target_path.is_absolute():
            root_text = self._root_path_edit.text().strip() or str(Path.cwd())
            target_path = Path(root_text) / target_path
        QApplication.clipboard().setText(str(target_path))
        self.statusBar().showMessage('Copied Large Module AST Audit target .py path to clipboard')

    def copy_large_module_split_handoff(self) -> None:
        handoff = self._last_large_module_split_handoff or self._output.toPlainText()
        QApplication.clipboard().setText(handoff)
        self.statusBar().showMessage('Copied Large Module Split Handoff for AI to clipboard')

    def show_mode_help(self) -> None:
        help_text = 'Validate\n- checks the project tree for duplicate public symbols, helper-folder rule violations, docstring mismatches, and oversized modules.\n\nDiff\n- previews the changes that would be written to __init__.py files, ARCHITECTURE.md, and architecture_manifest.json.\n\nScan\n- prints the full manifest JSON describing the project structure.\n\nWrite\n- writes architecture_manifest.json, minimal __init__.py facades, and ARCHITECTURE.md, but only when validation has no errors.'
        QMessageBox.information(self, 'Mode Help', help_text)

    def save_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, 'Save audit', str(Path.cwd() / 'architecture_manager_audit.txt'), 'Text Files (*.txt)')
        if not path:
            return
        Path(path).write_text(self._output.toPlainText(), encoding='utf-8')
        self.statusBar().showMessage(f'Saved audit to {path}')

def main() -> int:
    app = QApplication(sys.argv)
    window = ArchitectureManagerWindow()
    window.show()
    return app.exec()
if __name__ == '__main__':
    raise SystemExit(main())
