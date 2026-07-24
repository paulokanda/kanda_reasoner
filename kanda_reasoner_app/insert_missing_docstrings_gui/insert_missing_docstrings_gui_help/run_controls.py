# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py
"""Run-control helpers for the missing-docstrings GUI."""
from __future__ import annotations
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
from pathlib import Path
from importlib import import_module as _qtcore_import_module

def _qt_core_attr(name: str):
    """Return a PySide6.QtCore attribute without a static QtCore import."""
    return getattr(_qtcore_import_module('PySide6.QtCore'), name)
from PySide6.QtWidgets import QMessageBox
from kanda_reasoner_app.templates.floating_windows import show_auto_close_action_window
from .constants import DEFAULT_MODEL
from kanda_reasoner_app.templates.green_sonar_monitor import GreenSonarActivityMonitor
from .worker_thread import DocstringRunWorker
from kanda_reasoner_app.project_support_boundary import resolve_project_tool_boundary_identity
from kanda_reasoner_app.tab3_manual_review_runtime.project_paths_runtime import (
    run_report_path,
)
__all__ = [
    'run_selected_mode',
    'stop_running_selected_mode',
    'effective_report_path',
    'run_mode',
    'append_text',
    'handle_worker_progress',
    'handle_worker_success',
    'handle_worker_error',
    'cleanup_worker',
]


def _tab3_sonar_monitor(self):
    """Return the Docstring Assistant floating sonar monitor."""
    monitor = getattr(self, '_tab3_sonar_monitor', None)
    if monitor is None:
        monitor = GreenSonarActivityMonitor(self, title='Docstring Assistant')
        self._tab3_sonar_monitor = monitor
    return monitor

def _start_tab3_sonar(self, mode: str, target_label: str) -> None:
    """Start contextual Docstring Assistant processing feedback."""
    monitor = _tab3_sonar_monitor(self)
    normalized = str(mode or 'audit').strip().lower()
    monitor.start(
        'Running ' + normalized + ' mode',
        (
            'Scanning Python symbols and docstring gaps',
            'Target: ' + str(target_label or '*'),
            'Progress and final output stay in this tab',
        ),
    )

def _finish_tab3_sonar_success(self, mode: str) -> None:
    """Show successful Docstring Assistant completion feedback."""
    monitor = getattr(self, '_tab3_sonar_monitor', None)
    if monitor is not None:
        monitor.finish_success(
            'Complete: ' + str(mode or 'run') + ' finished',
            (
                'Docstring run finished successfully',
                'Review generated report rows if needed',
                'Ready for another selected-mode run',
            ),
        )

def _finish_tab3_sonar_error(self, mode: str, *, stopped: bool = False) -> None:
    """Show stopped/error Docstring Assistant completion feedback."""
    monitor = getattr(self, '_tab3_sonar_monitor', None)
    if monitor is not None:
        monitor.finish_error(
            ('Stopped: ' if stopped else 'Needs review: ') + str(mode or 'run'),
            (
                'Docstring run did not finish cleanly',
                'Check the output panel for details',
                'No hidden write is performed by this monitor',
            ),
        )

def run_selected_mode(self) -> None:
    """Run  selected mode.
    """
    self.run_mode(self._mode_combo.currentText())

def effective_report_path(self) -> str:
    """Handle effective report path.

    Returns
    -------
    str
        TODO: describe the return value.
    """
    explicit = self._report_path_edit.text().strip()
    if explicit:
        return explicit
    return str(run_report_path(self))

def _set_stop_button_enabled(self, enabled: bool) -> None:
    """Enable or disable the optional Tab 3 stop button."""
    button = getattr(self, '_stop_button', None)
    setter = getattr(button, 'setEnabled', None)
    if callable(setter):
        setter(bool(enabled))

def stop_running_selected_mode(self) -> None:
    """Request cooperative cancellation of the active selected-mode run."""
    worker = getattr(self, '_worker', None)
    thread = getattr(self, '_worker_thread', None)
    if worker is None or thread is None:
        self._append_text('\n[stop requested] no active selected-mode run.\n')
        _set_stop_button_enabled(self, False)
        return
    stop = getattr(worker, 'stop', None)
    if callable(stop):
        stop()
    request_interruption = getattr(thread, 'requestInterruption', None)
    if callable(request_interruption):
        request_interruption()
    _set_stop_button_enabled(self, False)
    self.statusBar().showMessage('Stopping selected mode...')
    self._progress.setRange(0, 1)
    self._progress.setValue(0)
    self._progress.setFormat('Stopping...')
    self._append_text('\n[stop requested] waiting for the current safe checkpoint.\n')

def _create_progress_receiver(window):
    """Create a GUI-thread receiver for worker progress payloads."""
    qobject_type = _qt_core_attr('QObject')
    slot_type = _qt_core_attr('Slot')

    class Tab3ProgressReceiver(qobject_type):
        """Receive progress payloads on the GUI thread."""

        @slot_type(object)
        def receive(self, payload):
            """Support receive behavior.
            
            Parameters
            ----------
            payload : object
                The payload value.
            """
            
            handle_worker_progress(window, payload)
    return Tab3ProgressReceiver(window)

def _connect_progress_signal(worker, receiver) -> None:
    """Connect progress through a queued Qt receiver when available."""
    try:
        queued = _qt_core_attr('Qt').ConnectionType.QueuedConnection
        worker.progress_ready.connect(receiver.receive, queued)
    except (AttributeError, TypeError):
        worker.progress_ready.connect(receiver.receive)

def run_mode(self, mode: str) -> None:
    """Run  mode.

    Parameters
    ----------
    mode : str
        TODO: describe mode.
    """
    worker_path = Path(self._worker_path_edit.text().strip())
    root_path = Path(self._root_path_edit.text().strip())
    if not worker_path.exists():
        show_error_copy_close_window(self, title='Missing worker script', message=f'Worker script not found:\n{worker_path}')
        return
    if not root_path.exists():
        show_error_copy_close_window(self, title='Invalid project root', message=f'Project root not found:\n{root_path}')
        return
    if mode == 'write' and self._confirm_write_checkbox.isChecked():
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle('Confirm write')
        box.setText('Write mode will insert missing docstrings into source files.')
        box.setInformativeText('Only missing docstrings will be inserted. Continue?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        if box.exec() != QMessageBox.Yes:
            return
    if self._worker_thread is not None:
        QMessageBox.warning(self, 'Work running', 'Wait for the current work to finish first, or click Stop Running Selected Mode.')
        return
    ai_api_key = ''
    self._docstring_run_project_identity = None
    if self._ai_enabled_checkbox.isChecked():
        controls = _qtcore_import_module(
            'kanda_reasoner_app.tab3_manual_review_runtime.ai_web_controls_runtime'
        )
        self._docstring_run_project_identity = resolve_project_tool_boundary_identity(
            root_path
        )
        if controls.provider_mode_from_owner(self) == 'web':
            descriptor = controls.selected_model_descriptor(self)
            if (
                descriptor is None
                or 'response_format' not in set(descriptor.supported_parameters)
            ):
                QMessageBox.warning(
                    self,
                    'Structured model required',
                    'Refresh models and select one that advertises '
                    'response_format support.',
                )
                return
            fingerprint = (
                str(root_path.resolve())
                + '|'
                + str(mode)
                + '|'
                + self._scope_combo.currentText()
                + '|'
                + controls.gateway_id_from_owner(self)
                + '|'
                + controls.selected_model_id(self)
            )
            approval = controls.request_cloud_approval(
                self,
                operation='Docstring Assistant ' + str(mode) + ' run',
                item_count=1,
                payload_bytes=0,
                input_fingerprint=fingerprint,
            )
            if not approval:
                return
            ai_api_key = controls.api_key_from_owner(self)
    self._output.clear()
    self._tab3_live_progress_active = False
    self._tab3_run_final_output_started = False
    if mode == 'write':
        if _run_tab1_audit_write_route_from_run_controls(self, mode):
            return
    report_path = self._effective_report_path()
    config_path = 'default'
    if self._ai_enabled_checkbox.isChecked():
        config_path = str(self._persist_runtime_config())
    target_module = self._effective_target_module()
    target_package = self._effective_target_package()
    target_label = target_module or target_package or '*'
    self._current_report_path = Path(report_path)
    self._report_rows = []
    self._review_list.clear()
    self._review_details.clear()
    self._review_summary.setText('Run in progress...')
    self._progress.setRange(0, 1)
    self._progress.setValue(0)
    self._progress.setFormat('Running...')
    _start_tab3_sonar(self, mode, target_label)
    self._save_prefs()
    self._output.appendPlainText(f'> in-process run: {worker_path} --root {root_path} --{mode} [module={self._module_checkbox.isChecked()} class={self._class_checkbox.isChecked()} function={self._function_checkbox.isChecked()} file_address={self._file_address_checkbox.isChecked()} ai={self._ai_enabled_checkbox.isChecked()} model={self._model_combo.currentText().strip() or DEFAULT_MODEL} private={self._include_private_checkbox.isChecked()} min_conf={self._min_confidence_combo.currentText()} workers={self._workers_spin.value()} scope={self._scope_combo.currentText()} target={target_label} report={report_path}]\n')
    self._run_button.setEnabled(False)
    _set_stop_button_enabled(self, True)
    self.statusBar().showMessage(f'Running {mode}...')
    self._worker_thread = _qt_core_attr('QThread')(self)
    self._worker = DocstringRunWorker(worker_script_path=str(worker_path), project_root=str(root_path), mode=mode, include_module=self._module_checkbox.isChecked(), include_classes=self._class_checkbox.isChecked(), include_functions=self._function_checkbox.isChecked(), insert_file_address_at_top=self._file_address_checkbox.isChecked(), ai_enabled=self._ai_enabled_checkbox.isChecked(), ai_config_path=config_path, ai_api_key=ai_api_key, include_private=self._include_private_checkbox.isChecked(), min_confidence=self._min_confidence_combo.currentText(), no_uncertain=self._no_uncertain_checkbox.isChecked(), workers=self._workers_spin.value(), report_path=report_path, target_module=target_module, target_package=target_package)
    self._worker.moveToThread(self._worker_thread)
    self._tab3_progress_receiver = _create_progress_receiver(self)
    self._worker_thread.started.connect(self._worker.run)
    self._worker.output_ready.connect(self._append_text)
    _connect_progress_signal(self._worker, self._tab3_progress_receiver)
    self._worker.finished_ok.connect(self._handle_worker_success)
    self._worker.finished_error.connect(self._handle_worker_error)
    self._worker.finished_ok.connect(self._worker_thread.quit)
    self._worker.finished_error.connect(self._worker_thread.quit)
    self._worker_thread.finished.connect(self._cleanup_worker)
    self._worker_thread.start()

def append_text(self, text: str) -> None:
    """Append final worker output, replacing transient progress text."""
    if not text:
        return
    if getattr(self, '_tab3_live_progress_active', False):
        self._output.clear()
        self._tab3_live_progress_active = False
        self._tab3_run_final_output_started = True
    self._output.moveCursor(self._output.textCursor().MoveOperation.End)
    self._output.insertPlainText(text)
    self._output.moveCursor(self._output.textCursor().MoveOperation.End)

def _safe_progress_int(payload: dict[str, object], key: str) -> int:
    """Return a non-negative integer from a progress payload."""
    try:
        return max(0, int(payload.get(key, 0)))
    except (TypeError, ValueError):
        return 0

def _format_live_audit_progress(payload: dict[str, object]) -> str:
    """Return the transient Tab 3 audit-progress output text."""
    total = _safe_progress_int(payload, 'total_files_to_audit')
    audited = _safe_progress_int(payload, 'files_audited')
    remaining = _safe_progress_int(payload, 'files_to_go')
    return 'Tab 3 audit is running.\nTotal files to audit: ' + str(total) + '\nFiles audited: ' + str(audited) + '\nFiles to go: ' + str(remaining) + '\n\nThis progress text is temporary. It will be replaced by the final real output when the run finishes.\n'

def handle_worker_progress(self, payload: dict[str, object]) -> None:
    """Show transient file-audit progress in the output panel."""
    if not isinstance(payload, dict):
        return
    total = _safe_progress_int(payload, 'total_files_to_audit')
    audited = _safe_progress_int(payload, 'files_audited')
    self._tab3_live_progress_active = True
    self._output.setPlainText(_format_live_audit_progress(payload))
    self._output.moveCursor(self._output.textCursor().MoveOperation.End)
    if total > 0:
        self._progress.setRange(0, total)
        self._progress.setValue(min(audited, total))
        self._progress.setFormat(str(audited) + '/' + str(total) + ' files audited')
    else:
        self._progress.setRange(0, 1)
        self._progress.setValue(0)
        self._progress.setFormat('Auditing files...')

def handle_worker_success(self, mode: str) -> None:
    """Handle handle worker success.

    Parameters
    ----------
    mode : str
        TODO: describe mode.
    """
    self._run_button.setEnabled(True)
    _set_stop_button_enabled(self, False)
    if not _run_result_is_current(self):
        self._output.appendPlainText(
            '\n[stale result rejected] active Project changed during the run.\n'
        )
        self.statusBar().showMessage('Stale Docstring run result rejected')
        return
    self.statusBar().showMessage(f'Finished {mode}')
    if getattr(self, '_tab3_live_progress_active', False):
        self._output.clear()
        self._tab3_live_progress_active = False
    self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=0\n')
    self._progress.setRange(0, 1)
    self._progress.setValue(1)
    self._progress.setFormat('Finished')
    self._load_report_rows()
    _finish_tab3_sonar_success(self, mode)
    show_auto_close_action_window(self, title='Work done', message=f'{mode.capitalize()} completed successfully.')

def handle_worker_error(self, mode: str, details: str) -> None:
    """Handle handle worker error.

    Parameters
    ----------
    mode : str
        TODO: describe mode.
    details : str
        TODO: describe details.
    """
    self._run_button.setEnabled(True)
    _set_stop_button_enabled(self, False)
    if not _run_result_is_current(self):
        self._output.appendPlainText(
            '\n[stale result rejected] active Project changed during the run.\n'
        )
        self.statusBar().showMessage('Stale Docstring run result rejected')
        return
    was_stopped = 'stopped by user' in (details or '').lower()
    if was_stopped:
        self.statusBar().showMessage(f'Stopped {mode}')
        if getattr(self, '_tab3_live_progress_active', False):
            self._output.clear()
            self._tab3_live_progress_active = False
        self._output.appendPlainText(f'\n[stopped] mode={mode}\n{details}\n')
        self._progress.setRange(0, 1)
        self._progress.setValue(1)
        self._progress.setFormat('Stopped')
        self._load_report_rows()
        _finish_tab3_sonar_error(self, mode, stopped=True)
        return
    self.statusBar().showMessage(f'Finished {mode} with issues')
    if getattr(self, '_tab3_live_progress_active', False):
        self._output.clear()
        self._tab3_live_progress_active = False
    self._output.appendPlainText(f'\n[finished] mode={mode} exit_code=1\n{details}\n')
    self._progress.setRange(0, 1)
    self._progress.setValue(1)
    self._progress.setFormat('Finished with issues')
    self._load_report_rows()
    _finish_tab3_sonar_error(self, mode)
    QMessageBox.warning(self, 'Work finished with issues', f'{mode.capitalize()} finished with issues.\nCheck the output panel for details.')


def _run_result_is_current(self) -> bool:
    """Return whether the completed run still belongs to the selected Project."""
    expected = getattr(self, '_docstring_run_project_identity', None)
    if expected is None:
        return True
    try:
        current = resolve_project_tool_boundary_identity(
            Path(self._root_path_edit.text().strip())
        )
    except Exception:
        return False
    return (
        current.active_project_id == expected.active_project_id
        and current.active_project_root_fingerprint
        == expected.active_project_root_fingerprint
    )

def cleanup_worker(self) -> None:
    """Handle cleanup worker.
    """
    progress_receiver = getattr(self, '_tab3_progress_receiver', None)
    if progress_receiver is not None:
        progress_receiver.deleteLater()
        self._tab3_progress_receiver = None
    if self._worker is not None:
        self._worker.deleteLater()
        self._worker = None
    if self._worker_thread is not None:
        self._worker_thread.deleteLater()
        self._worker_thread = None
    self._docstring_run_project_identity = None

def _run_tab1_audit_write_route_from_run_controls(self, mode: str) -> bool:
    """Run Write using Tab 1 audit targets from the existing controls boundary."""
    from pathlib import Path
    from .tab1_audit_docstring_source import refresh_tab1_audit_docstring_source
    from .tab1_audit_write_contracts import TAB1_AUDIT_WRITE_ROUTE_STATUS_READY
    from kanda_reasoner_app.tab1_audit_write_support.planning import build_tab1_audit_write_plan, tab1_audit_write_route_should_handle
    from kanda_reasoner_app.tab1_audit_write_support.worker import start_tab1_audit_write_worker
    if not tab1_audit_write_route_should_handle(self, mode):
        return False
    root_path = Path(self._root_path_edit.text().strip() or Path.cwd())
    refresh_result = refresh_tab1_audit_docstring_source(self, checked=True)
    findings = tuple(getattr(refresh_result, 'findings', tuple()) if refresh_result else tuple())
    plan = build_tab1_audit_write_plan(root_path, findings)
    setattr(self, '_tab1_audit_write_plan', plan)
    self._append_text('[tab1 audit write] findings=' + str(len(findings)) + ' target_files=' + str(len(plan.targets)) + '\n')
    if plan.ignored_findings:
        self._append_text('[tab1 audit write] ignored findings=' + str(len(plan.ignored_findings)) + '\n')
    if plan.status != TAB1_AUDIT_WRITE_ROUTE_STATUS_READY:
        self._append_text('[tab1 audit write] ' + plan.message + '\n')
        return True
    start_tab1_audit_write_worker(self, mode, plan)
    return True
