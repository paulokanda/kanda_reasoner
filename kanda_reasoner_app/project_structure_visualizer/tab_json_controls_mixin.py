"""Responsive complete-JSON controls for the Project Structure 3D tab."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import QProcess, QProcessEnvironment, Slot
from PySide6.QtWidgets import QMessageBox

from kanda_reasoner_app.templates.green_sonar_monitor import (
    GreenSonarActivityMonitor,
)

from .complete_json_artifacts import inspect_complete_json_artifacts
from .complete_json_zip_cache import resolve_complete_json_evidence

__all__: list[str] = []


class ProjectStructureJsonControlsMixin:
    """Own Project Structure 3D JSON creation without blocking the GUI."""

    def _initialize_complete_json_controls(self) -> None:
        self._complete_json_process: QProcess | None = None
        self._complete_json_stdout_buffer = ""
        self._complete_json_stderr: list[str] = []
        self._complete_json_mode = ""
        self._complete_json_sonar: GreenSonarActivityMonitor | None = None

    def _json_sonar(self) -> GreenSonarActivityMonitor:
        monitor = self._complete_json_sonar
        if monitor is None:
            monitor = GreenSonarActivityMonitor(
                self,
                title="Project Structure 3D JSON",
                host=self,
            )
            self._complete_json_sonar = monitor
        return monitor

    def _refresh_complete_json_status(self) -> None:
        if self._project_root is None:
            self.create_project_json_button.setStyleSheet(
                "color: #d84a4a; font-weight: 700;"
            )
            self.update_project_json_button.setEnabled(False)
            self.json_artifact_status_label.setText("JSON: project not selected")
            return
        status = inspect_complete_json_artifacts(self._project_root)
        running = self._complete_json_process is not None
        legacy_path = None
        legacy_source = ""
        if not status.get("valid"):
            try:
                legacy_path, legacy_source, _cache_status = resolve_complete_json_evidence(
                    self._project_root
                )
            except (OSError, ValueError, TypeError):
                legacy_path = None
        if status.get("valid"):
            self.create_project_json_button.setStyleSheet(
                "color: #2fbf71; font-weight: 700;"
            )
            part_count = int(status.get("part_count") or 0)
            self.json_artifact_status_label.setText(
                f"JSON ready ({part_count} ZIP part{'s' if part_count != 1 else ''})"
            )
        elif legacy_path is not None:
            self.create_project_json_button.setStyleSheet(
                "color: #2fbf71; font-weight: 700;"
            )
            self.json_artifact_status_label.setText(
                "JSON ready from Show Project to AI: "
                + str(legacy_path)
                + (" [" + legacy_source + "]" if legacy_source else "")
            )
        else:
            self.create_project_json_button.setStyleSheet(
                "color: #d84a4a; font-weight: 700;"
            )
            reason = str(status.get("reason") or "missing")
            self.json_artifact_status_label.setText(
                "JSON missing: " + reason + ". Run Show Project to AI or click Create Project JSON."
            )
        self.create_project_json_button.setEnabled(not running)
        self.update_project_json_button.setEnabled(
            not running
            and bool(status.get("valid"))
            and bool(status.get("incremental_ready"))
        )

    @Slot()
    def _create_project_json(self) -> None:
        if self._project_root is None:
            QMessageBox.warning(self, "Project JSON", "Select a Project first.")
            return
        answer = QMessageBox.question(
            self,
            "Create Project JSON",
            "Erase the previous Project Structure 3D JSON family and create "
            "a new one from the current project source?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        self._start_complete_json_job("create")

    @Slot()
    def _update_project_json_incrementally(self) -> None:
        if self._project_root is None:
            QMessageBox.warning(self, "Project JSON", "Select a Project first.")
            return
        status = inspect_complete_json_artifacts(self._project_root)
        if not status.get("valid") or not status.get("incremental_ready"):
            QMessageBox.warning(
                self,
                "Incremental Project JSON",
                "A valid disk-indexed Project JSON baseline is required. "
                "Run Create Project JSON once.",
            )
            return
        self._start_complete_json_job("incremental")

    def _start_complete_json_job(self, mode: str) -> None:
        if self._complete_json_process is not None or self._project_root is None:
            return
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.SeparateChannels)
        environment = QProcessEnvironment.systemEnvironment()
        existing_pythonpath = environment.value("PYTHONPATH")
        project_text = str(self._project_root)
        environment.insert(
            "PYTHONPATH",
            project_text
            + (os.pathsep + existing_pythonpath if existing_pythonpath else ""),
        )
        process.setProcessEnvironment(environment)
        process.setWorkingDirectory(project_text)
        process.readyReadStandardOutput.connect(self._read_complete_json_stdout)
        process.readyReadStandardError.connect(self._read_complete_json_stderr)
        process.finished.connect(self._complete_json_process_finished)
        process.errorOccurred.connect(self._complete_json_process_error)
        self._complete_json_process = process
        self._complete_json_mode = mode
        self._complete_json_stdout_buffer = ""
        self._complete_json_stderr = []
        self.create_project_json_button.setEnabled(False)
        self.update_project_json_button.setEnabled(False)
        action = "Creating" if mode == "create" else "Updating"
        self.json_artifact_status_label.setText(action + " Project JSON...")
        self._json_sonar().start(
            action + " Project JSON",
            (
                "Scanning source through a disk-backed index",
                "Streaming JSON bytes directly into bounded ZIP members",
                "Published ZIP parts remain limited to 450 MB",
            ),
        )
        process.start(
            sys.executable,
            [
                "-m",
                "kanda_reasoner_app.project_structure_visualizer.complete_json_cli",
                "--root",
                project_text,
                "--mode",
                mode,
            ],
        )

    @Slot()
    def _read_complete_json_stdout(self) -> None:
        process = self._complete_json_process
        if process is None:
            return
        chunk = bytes(process.readAllStandardOutput()).decode("utf-8", errors="replace")
        self._complete_json_stdout_buffer += chunk
        lines = self._complete_json_stdout_buffer.split("\n")
        self._complete_json_stdout_buffer = lines.pop()
        for line in lines:
            text = line.strip()
            if text.startswith("PROGRESS: "):
                message = text[len("PROGRESS: ") :]
                self.json_artifact_status_label.setText(message)
                self._json_sonar().start(
                    "Project JSON is running",
                    (
                        message,
                        "The Project Structure 3D tab remains responsive",
                        "Old published evidence remains available until success",
                    ),
                )

    @Slot()
    def _read_complete_json_stderr(self) -> None:
        process = self._complete_json_process
        if process is None:
            return
        text = bytes(process.readAllStandardError()).decode("utf-8", errors="replace")
        if text:
            self._complete_json_stderr.append(text)

    @Slot(int, QProcess.ExitStatus)
    def _complete_json_process_finished(
        self,
        exit_code: int,
        exit_status: QProcess.ExitStatus,
    ) -> None:
        process = self._complete_json_process
        if process is not None:
            self._read_complete_json_stdout()
            self._read_complete_json_stderr()
            process.deleteLater()
        self._complete_json_process = None
        succeeded = exit_status == QProcess.NormalExit and exit_code == 0
        if succeeded:
            self._json_sonar().finish_success(
                "Project JSON published",
                (
                    "ZIP family passed the 450 MB part gate",
                    "Incremental state is ready for later updates",
                    "Reloading the Project Structure 3D visualization",
                ),
            )
            self._refresh_complete_json_status()
            self._reload_project_evidence()
            return
        message = "".join(self._complete_json_stderr).strip()
        if not message:
            message = f"Project JSON process failed with exit code {exit_code}."
        self._json_sonar().finish_error(
            "Project JSON failed",
            (
                "The previous published JSON family was preserved",
                "Review the copied diagnostic message",
                "No project source file was modified",
            ),
        )
        self._refresh_complete_json_status()
        QMessageBox.critical(self, "Project JSON failed", message)

    @Slot(QProcess.ProcessError)
    def _complete_json_process_error(self, _error: QProcess.ProcessError) -> None:
        process = self._complete_json_process
        if process is None:
            return
        self._complete_json_stderr.append(process.errorString())
