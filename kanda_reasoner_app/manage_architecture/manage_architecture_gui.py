# project-path: kanda_reasoner_app/manage_architecture/manage_architecture_gui.py
"""Qt GUI for running architecture scan, validate, diff, and write modes."""
from __future__ import annotations

from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
from kanda_reasoner_app.manage_architecture.architecture_audit_actions_gui import ArchitectureAuditActionsMixin
from kanda_reasoner_app.manage_architecture.architecture_review_subtabs import build_architecture_review_ui
from kanda_reasoner_app.manage_architecture.large_module_split_audit_gui import LargeModuleSplitAuditGuiMixin
from kanda_reasoner_app.manage_architecture.large_module_target_queue import LargeModuleTarget
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
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton
import importlib as _architecture_gui_importlib
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
    """Represent architecture run worker."""
    
    output_ready = Signal(str)
    finished_ok = Signal(str)
    finished_error = Signal(str, str)

    def __init__(self, manager_script_path: str, project_root: str, mode: str) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        manager_script_path : str
            The manager script path value.
        project_root : str
            The project root path.
        mode : str
            The selected mode.
        """
        
        super().__init__()
        self._manager_script_path = Path(manager_script_path)
        self._project_root = Path(project_root)
        self._mode = mode

    def run(self) -> None:
        """Support run behavior.
        """
        
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
        """Support load manager module behavior.
        
        Parameters
        ----------
        script_path : Path
            The script path value.
        """
        
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

class ArchitectureManagerWindow(
    ArchitectureAuditActionsMixin,
    LargeModuleSplitAuditGuiMixin,
    QMainWindow,
):

    """Represent architecture manager window."""
    
    def __init__(self) -> None:
        """Support init behavior.
        """
        
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
        self._ai_review_controls_moved_to_host = False
        self._python_path_edit = QLineEdit(sys.executable)
        self._python_path_edit.setEnabled(False)
        self._large_module_targets: list[LargeModuleTarget] = []
        self._large_module_target_index = -1
        self._large_module_target_source = 'none'
        self._last_large_module_split_handoff = ''
        self._build_ui()

    def _manager_script_path(self) -> Path:
        """Support manager script path behavior.
        
        Returns
        -------
        Path
            The resolved path.
        """
        
        default_path = Path(__file__).resolve().parent / DEFAULT_MANAGER_NAME
        script_edit = getattr(self, '_script_path_edit', None)
        if script_edit is not None:
            text = script_edit.text().strip()
            if text:
                return Path(text)
        return default_path

    def _build_ui(self) -> None:
        """Build the Architecture Review UI."""
        build_architecture_review_ui(self, install_tab1_ai_review_controls)

    def move_project_root_controls_to_layout(self, destination_layout, insert_index: int | None=None) -> None:
        """Move the Tab 1 project-root controls into a host layout."""
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

    def move_ai_review_controls_to_layout(self, destination_layout, insert_index: int | None=None) -> None:
        """Move the Tab 1 AI review controls into the host Architecture header."""
        if self._ai_review_controls_moved_to_host:
            return

        widgets = [
            getattr(self, '_ai_review_model_label', None),
            getattr(self, '_ai_review_model_combo', None),
            getattr(self, '_ai_review_refresh_models_button', None),
            getattr(self, '_ai_review_button', None),
        ]
        target_index = destination_layout.count() if insert_index is None else insert_index
        offset = 0
        for widget in widgets:
            if widget is None:
                continue
            parent = widget.parentWidget()
            parent_layout = parent.layout() if parent is not None else None
            if parent_layout is not None:
                parent_layout.removeWidget(widget)
            destination_layout.insertWidget(target_index + offset, widget, 0)
            offset += 1
        self._ai_review_controls_moved_to_host = True

    def browse_script(self) -> None:
        """Support browse script behavior.
        """
        
        start = str(self._manager_script_path().parent)
        path, _ = QFileDialog.getOpenFileName(self, 'Select worker script', start, 'Python files (*.py)')
        if path:
            self._script_path_edit.setText(path)

    def browse_root(self) -> None:
        """Support browse root behavior.
        """
        
        path = QFileDialog.getExistingDirectory(self, 'Select project root', self._root_path_edit.text().strip() or str(Path.cwd()))
        if path:
            self._root_path_edit.setText(path)

    def run_selected_mode(self) -> None:
        """Run the selected mode.
        """
        
        self.run_mode(self._mode_combo.currentText())

    def run_mode(self, mode: str) -> None:
        """Run the mode.
        
        Parameters
        ----------
        mode : str
            The selected mode.
        """
        
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
        """Support confirm write behavior.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle('Confirm write')
        box.setText('Write mode can update __init__.py files, ARCHITECTURE.md, and architecture_manifest.json.')
        box.setInformativeText('Continue?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        return box.exec() == QMessageBox.Yes

    def _append_text(self, text: str) -> None:
        """Support append text behavior.
        
        Parameters
        ----------
        text : str
            The text value.
        """
        
        if not text:
            return
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)
        self._output.insertPlainText(text)
        self._output.moveCursor(self._output.textCursor().MoveOperation.End)

    def _handle_worker_success(self, mode: str) -> None:
        """Support handle worker success behavior.
        
        Parameters
        ----------
        mode : str
            The selected mode.
        """
        
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
        """Support handle worker error behavior.
        
        Parameters
        ----------
        mode : str
            The selected mode.
        details : str
            The details value.
        """
        
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
        """Support cleanup worker behavior.
        """
        
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
        """Support force cancel worker thread behavior.
        """
        
        thread = self._worker_thread
        if thread is not None and thread.isRunning():
            self._output.appendPlainText('[cancel] terminating Architecture worker thread.\n')
            thread.terminate()
            thread.wait(1000)

    def _force_cancel_ai_review_thread(self) -> None:
        """Support force cancel ai review thread behavior.
        """
        
        thread = self._ai_review_thread
        if thread is not None and thread.isRunning():
            self._output.appendPlainText('[cancel] terminating Architecture AI review thread.\n')
            thread.terminate()
            thread.wait(1000)

    def show_mode_help(self) -> None:
        """Show the mode help.
        """
        
        help_text = 'Validate\n- checks the project tree for duplicate public symbols, helper-folder rule violations, docstring mismatches, and oversized modules.\n\nDiff\n- previews the changes that would be written to __init__.py files, ARCHITECTURE.md, and architecture_manifest.json.\n\nScan\n- prints the full manifest JSON describing the project structure.\n\nWrite\n- writes architecture_manifest.json, minimal __init__.py facades, and ARCHITECTURE.md, but only when validation has no errors.'
        QMessageBox.information(self, 'Mode Help', help_text)

    def save_output(self) -> None:
        """Save the output.
        """
        
        path, _ = QFileDialog.getSaveFileName(self, 'Save audit', str(Path.cwd() / 'architecture_manager_audit.txt'), 'Text Files (*.txt)')
        if not path:
            return
        Path(path).write_text(self._output.toPlainText(), encoding='utf-8')
        self.statusBar().showMessage(f'Saved audit to {path}')

def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    app = QApplication(sys.argv)
    window = ArchitectureManagerWindow()
    window.show()
    return app.exec()
if __name__ == '__main__':
    raise SystemExit(main())
