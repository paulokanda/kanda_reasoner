"""Support V10 project reasoning and evidence handling."""
from __future__ import annotations
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
import os
import sys
from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QFileDialog, QMessageBox
from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.ui_components import shorten_path
__all__ = ['AnalysisController']

class AnalysisController:

    def expected_generated_json_path(self, project_root: str) -> str:
        return os.path.join(project_root, 'project_structure_index.json')

    def pick_project_root(self, window) -> None:
        start_dir = window.project_root_edit.text().strip() or os.getcwd()
        path = QFileDialog.getExistingDirectory(window, 'Select project root', start_dir)
        if not path:
            return
        window.project_root_edit.setText(path)
        window._append_log('Project root selected: ' + path)
        window._refresh_workflow_controls()
        window._save_last_config()

    def build_analysis_command(self, project_root: str) -> tuple[str, list[str]]:
        python_exe = sys.executable
        module_name = 'kanda_reasoner_app.reasoner_engine_data_collector.collector_main'
        args = ['-m', module_name, '--project-root', project_root]
        return (python_exe, args)

    def run_analysis(self, window) -> None:
        if window._analysis_running:
            QMessageBox.information(window, 'Analysis running', 'Analysis is already running.')
            return
        project_root = window.project_root_edit.text().strip()
        if not project_root:
            QMessageBox.warning(window, 'No project root', 'Please select a project root first.')
            return
        if not os.path.isdir(project_root):
            QMessageBox.warning(window, 'Invalid project root', 'Selected project root does not exist.')
            return
        program, args = self.build_analysis_command(project_root)
        process = QProcess(window)
        process.setProgram(program)
        process.setArguments(args)
        process.setWorkingDirectory(project_root)
        process.readyReadStandardOutput.connect(window._on_analysis_stdout_ready)
        process.readyReadStandardError.connect(window._on_analysis_stderr_ready)
        process.errorOccurred.connect(window._on_analysis_error_occurred)
        process.finished.connect(window._on_analysis_finished)
        expected_json = self.expected_generated_json_path(project_root)
        window._analysis_process = process
        window._analysis_running = True
        window.analysis_status_value_label.setText('Running')
        window.analysis_output_json_value_label.setText(shorten_path(expected_json))
        window._last_generated_json_path = expected_json
        window._append_log('Starting analysis for project root: ' + project_root)
        window._append_log('Analysis command: ' + ' '.join([program] + args))
        window._refresh_workflow_controls()
        process.start()
        if not process.waitForStarted(3000):
            window._analysis_process = None
            window._analysis_running = False
            window.analysis_status_value_label.setText('Failed to start')
            window._refresh_workflow_controls()
            show_error_copy_close_window(window, title='Analysis error', message='Failed to start collector process.')

    def on_analysis_stdout_ready(self, window) -> None:
        process = window._analysis_process
        if process is None:
            return
        data = bytes(process.readAllStandardOutput()).decode('utf-8', errors='replace')
        if data.strip():
            window._append_log(data.rstrip())

    def on_analysis_stderr_ready(self, window) -> None:
        process = window._analysis_process
        if process is None:
            return
        data = bytes(process.readAllStandardError()).decode('utf-8', errors='replace')
        if data.strip():
            window._append_log('[stderr] ' + data.rstrip())

    def on_analysis_error_occurred(self, window, process_error: QProcess.ProcessError) -> None:
        window.analysis_status_value_label.setText('Error')
        window._analysis_running = False
        window._append_log('Analysis process error: ' + str(process_error))
        window._refresh_workflow_controls()

    def on_analysis_finished(self, window, exit_code: int, exit_status: object) -> None:
        _ = exit_status
        process = window._analysis_process
        window._analysis_process = None
        window._analysis_running = False
        if exit_code == 0:
            window.analysis_status_value_label.setText('Finished')
            json_path = window._last_generated_json_path
            if json_path and os.path.exists(json_path):
                window.analysis_output_json_value_label.setText(shorten_path(json_path))
                window._append_log('Analysis completed: ' + json_path)
                if window.analysis_auto_load_checkbox.isChecked():
                    try:
                        window._load_json_from_path(json_path)
                    except Exception as exc:
                        QMessageBox.warning(window, 'Auto-load failed', 'Analysis finished but JSON auto-load failed:\n' + str(exc))
            else:
                window._append_log('Analysis finished, but no generated JSON was found.')
        else:
            window.analysis_status_value_label.setText('Failed')
            window._append_log('Analysis finished with exit code: ' + str(exit_code))
            if process is not None:
                data = bytes(process.readAllStandardError()).decode('utf-8', errors='replace')
                if data.strip():
                    window._append_log('[stderr] ' + data.rstrip())
        window._refresh_workflow_controls()
        window._save_last_config()
