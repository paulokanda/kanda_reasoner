# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_3_private_impl.py
"""Private helper implementations for runtime runner GUI actions."""
from __future__ import annotations
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window
__all__ = []

def _bind_root_globals(root_globals):
    """Support bind root globals behavior.
    
    Parameters
    ----------
    root_globals : object
        The root globals value.
    """
    
    globals().update(root_globals)

def _rr_RuntimeCollectorWindow__browse_entry_script_impl(self) -> None:
    """Support rr runtime collector window browse entry script impl behavior.
    """
    
    file_path, _ = QFileDialog.getOpenFileName(self, 'Select entry script', self.project_root_edit.text().strip() or str(DEFAULT_PROJECT_ROOT), 'Python Files (*.py)')
    if file_path:
        self.entry_script_edit.setText(file_path)
        _save_prefs(self.project_root_edit.text().strip(), self.output_json_edit.text().strip(), file_path)

def _rr_RuntimeCollectorWindow__configure_trace_impl(self) -> None:
    """Support rr runtime collector window configure trace impl behavior.
    """
    
    project_root = self.project_root_edit.text().strip()
    output_json = self.output_json_edit.text().strip()
    entry_script = self.entry_script_edit.text().strip()
    if not output_json:
        QMessageBox.warning(self, 'Missing output path', 'Please specify an output JSON path.')
        return
    output_path = Path(output_json).expanduser()
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        show_error_copy_close_window(self, title='Cannot create output directory', message=traceback.format_exc())
        return
    try:
        configure_runtime_trace(project_root=project_root or str(DEFAULT_PROJECT_ROOT), output_path=str(output_path), entry_script=entry_script)
    except Exception:
        show_error_copy_close_window(self, title='Configure failed', message=traceback.format_exc())
        self._append_log('Configure failed:')
        self._append_log(traceback.format_exc())
        return
    self._trace_configured = True
    self.save_button.setEnabled(True)
    self.log_box.clear()
    self._append_log('Trace configured.')
    self._append_log('Project root:  ' + (project_root or '(not set)'))
    self._append_log('Output JSON:   ' + str(output_path))
    self._append_log('Entry script:  ' + (entry_script or '(not set)'))
    self._append_log('')
    self._append_log('Runtime trace writer is active.')
    self._append_log("Exercise the target code, then click 'Save Trace'.")
    _save_prefs(project_root, str(output_path), entry_script)

def _rr_RuntimeCollectorWindow__save_trace_impl(self) -> None:
    """Support rr runtime collector window save trace impl behavior.
    """
    
    if not self._trace_configured:
        QMessageBox.warning(self, 'Not configured', "Please click 'Configure Trace' before saving.")
        return
    output_json = self.output_json_edit.text().strip()
    if not output_json:
        QMessageBox.warning(self, 'Missing output path', 'Please specify an output JSON path.')
        return
    self.configure_button.setEnabled(False)
    self.save_button.setEnabled(False)
    self._start_spinner()
    self._worker = _SaveWorker(output_json, parent=self)
    self._worker.finished.connect(self._on_save_finished)
    self._worker.errored.connect(self._on_save_error)
    self._worker.start()

def _rr_RuntimeCollectorWindow__on_save_finished_impl(self, output_path: str) -> None:
    """Support rr runtime collector window on save finished impl behavior.
    
    Parameters
    ----------
    output_path : str
        The output path value.
    """
    
    self._stop_spinner()
    self.configure_button.setEnabled(True)
    self.save_button.setEnabled(True)
    self._append_log('')
    self._append_log('Trace saved: ' + output_path)
    _save_prefs(self.project_root_edit.text().strip(), output_path, self.entry_script_edit.text().strip())
    show_auto_close_action_window(self, title='Trace saved', message='Runtime trace written.', detail_text=output_path)

def _rr_RuntimeCollectorWindow__on_save_error_impl(self, tb_str: str) -> None:
    """Support rr runtime collector window on save error impl behavior.
    
    Parameters
    ----------
    tb_str : str
        The tb str value.
    """
    
    self._stop_spinner()
    self.configure_button.setEnabled(True)
    self.save_button.setEnabled(True)
    show_error_copy_close_window(self, title='Save failed', message=tb_str)
    self._append_log('Save failed:')
    self._append_log(tb_str)

def _rr_RuntimeCollectorWindow_closeEvent_impl(self, event) -> None:
    """Support rr runtime collector window close event impl behavior.
    
    Parameters
    ----------
    event : object
        The event object.
    """
    
    _save_prefs(self.project_root_edit.text().strip(), self.output_json_edit.text().strip(), self.entry_script_edit.text().strip())
    super().closeEvent(event)
import importlib as _pass_065f_importlib
import sys as _pass_065f_sys
import traceback as traceback
from pathlib import Path as Path

def _pass_073b_noop(*args, **kwargs):
    """Support pass 073b noop behavior.
    
    Parameters
    ----------
    *args : object
        The positional arguments.
    **kwargs : object
        The kwargs value.
    """
    
    return None

def _pass_073b_import_module(module_name):
    """Support pass 073b import module behavior.
    
    Parameters
    ----------
    module_name : object
        The module name value.
    """
    
    try:
        return _pass_065f_importlib.import_module(module_name)
    except Exception:
        return None

def _pass_073b_import_attr(module_name, attr_name):
    """Support pass 073b import attr behavior.
    
    Parameters
    ----------
    module_name : object
        The module name value.
    attr_name : object
        The attr name value.
    """
    
    module = _pass_073b_import_module(module_name)
    if module is None:
        return None
    return getattr(module, attr_name, None)

def _pass_073b_import_first_attr(module_names, attr_name):
    """Support pass 073b import first attr behavior.
    
    Parameters
    ----------
    module_names : object
        The module names value.
    attr_name : object
        The attr name value.
    """
    
    for module_name in module_names:
        value = _pass_073b_import_attr(module_name, attr_name)
        if value is not None:
            return value
    return None

def _pass_073b_import_runtime_trace_attr(attr_name):
    """Support pass 073b import runtime trace attr behavior.
    
    Parameters
    ----------
    attr_name : object
        The attr name value.
    """
    
    value = _pass_073b_import_attr('kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api', attr_name)
    if callable(value):
        return value
    return _pass_073b_noop
QFileDialog = _pass_073b_import_first_attr(('PySide6.QtWidgets', 'PyQt6.QtWidgets'), 'QFileDialog')
QMessageBox = _pass_073b_import_first_attr(('PySide6.QtWidgets', 'PyQt6.QtWidgets'), 'QMessageBox')
configure_runtime_trace = _pass_073b_import_runtime_trace_attr('configure_runtime_trace')
save_runtime_trace = _pass_073b_import_runtime_trace_attr('save_runtime_trace')
trace_event = _pass_073b_import_runtime_trace_attr('trace_event')
trace_signal_connection = _pass_073b_import_runtime_trace_attr('trace_signal_connection')
trace_state_snapshot = _pass_073b_import_runtime_trace_attr('trace_state_snapshot')
DEFAULT_PROJECT_ROOT = _pass_073b_import_attr('kanda_reasoner_app.reasoner_runtime_collector.runtime_runner', 'DEFAULT_PROJECT_ROOT') or Path.cwd()

def _save_prefs(*args, **kwargs):
    """Support save prefs behavior.
    
    Parameters
    ----------
    *args : object
        The positional arguments.
    **kwargs : object
        The kwargs value.
    """
    
    return None

def _SaveWorker(*args, **kwargs):
    """Support save worker behavior.
    
    Parameters
    ----------
    *args : object
        The positional arguments.
    **kwargs : object
        The kwargs value.
    """
    
    raise NameError('_SaveWorker is not bound in runtime_runner part 3')
