"""Tab 4 JSON ZIP export helpers.

This module keeps ZIP-export GUI behavior outside the collector process helper
so the collector box remains focused on collection and bundle generation.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any

__all__ = [
    "CONSERVATIVE_ZIP_SIZE_MB",
    "DEFAULT_ZIP_SIZE_MB",
    "resolve_zip_dialog_start_folder",
    "run_zip_json_files",
]

CONSERVATIVE_ZIP_SIZE_MB = 25
DEFAULT_ZIP_SIZE_MB = 40


def _qt_widgets():
    return importlib.import_module("PySide6" + ".QtWidgets")


def _process_helpers():
    from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
        window_process_private_impl as helpers,
    )
    return helpers


def _prefs_path() -> Path:
    return Path(__file__).resolve().parent / ".zip_json_export_prefs.json"


def _load_destination() -> str:
    try:
        prefs_path = _prefs_path()
        if prefs_path.exists():
            payload = json.loads(prefs_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                destination = str(payload.get("destination_folder", "")).strip()
                if destination:
                    return destination
    except Exception:
        pass
    return ""


def _save_destination(destination_folder: str) -> None:
    try:
        _prefs_path().write_text(
            json.dumps({"destination_folder": destination_folder}, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def _destination_inside_project_root(project_root: Path, destination: Path) -> bool:
    try:
        resolved_root = project_root.expanduser().resolve()
        resolved_destination = destination.expanduser().resolve()
        resolved_destination.relative_to(resolved_root)
        return True
    except ValueError:
        return False
    except Exception:
        return False


def _selected_part_size_mb(window: Any) -> int:
    try:
        if bool(window.zip_size_conservative_radio.isChecked()):
            return CONSERVATIVE_ZIP_SIZE_MB
    except Exception:
        pass
    return DEFAULT_ZIP_SIZE_MB


def _set_controls_enabled(window: Any, enabled: bool) -> None:
    for attribute in (
        "run_button",
        "browse_project_button",
        "browse_output_button",
        "zip_json_files_button",
        "zip_size_conservative_radio",
        "zip_size_default_radio",
    ):
        try:
            getattr(window, attribute).setEnabled(enabled)
        except Exception:
            pass


def _append_log(window: Any, text: str) -> None:
    try:
        window._append_log(text)
    except Exception:
        pass


def _start_zip_status(window: Any) -> None:
    try:
        window._start_busy_animation("Zipping JSON files")
    except Exception:
        try:
            window.status_label.setText("Zipping JSON files...")
        except Exception:
            pass
    _set_controls_enabled(window, False)


def _finish_zip_status(window: Any, status_text: str) -> None:
    try:
        window._stop_busy_animation(status_text)
    except Exception:
        try:
            window.status_label.setText(status_text)
        except Exception:
            pass
    _set_controls_enabled(window, True)


def _decode_process_output(process: Any) -> tuple[str, str]:
    stdout_text = bytes(process.readAllStandardOutput()).decode("utf-8", errors="replace").strip()
    stderr_text = bytes(process.readAllStandardError()).decode("utf-8", errors="replace").strip()
    return stdout_text, stderr_text


def _on_zip_process_finished(window: Any, exit_code: int, _exit_status: Any) -> None:
    process = getattr(window, "_process", None)
    stdout_text = ""
    stderr_text = ""
    if process is not None:
        stdout_text, stderr_text = _decode_process_output(process)

    if exit_code != 0:
        _finish_zip_status(window, "Failed")
        _append_log(window, "[ERROR] JSON ZIP export failed:")
        _append_log(window, stderr_text or stdout_text or "Unknown child-process error")
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.critical(
            window,
            "JSON ZIP export error",
            stderr_text or stdout_text or "Unknown child-process error",
        )
        window._process = None
        return

    try:
        result = json.loads(stdout_text) if stdout_text else {}
    except Exception:
        result = {}

    zip_parts = result.get("zip_parts", [])
    zip_count = len(zip_parts) if isinstance(zip_parts, list) else 0
    warnings = result.get("warnings", [])

    _finish_zip_status(window, "Finished")
    _append_log(window, "[OK] JSON ZIP export completed.")
    _append_log(window, "  zip_count: " + str(zip_count))
    _append_log(window, "  part_size_mb: " + str(result.get("part_size_mb", "")))
    if isinstance(zip_parts, list):
        for item in zip_parts:
            if isinstance(item, dict):
                _append_log(
                    window,
                    "  zip: "
                    + str(item.get("filename", ""))
                    + " ("
                    + str(item.get("size_bytes", ""))
                    + " bytes)",
                )
    if isinstance(warnings, list):
        for item in warnings:
            _append_log(window, "  warning: " + str(item))

    window._process = None


def _on_zip_process_error(window: Any, _process_error: Any) -> None:
    _finish_zip_status(window, "Failed")
    _append_log(window, "[ERROR] JSON ZIP export process could not start.")
    QMessageBox = _qt_widgets().QMessageBox
    QMessageBox.critical(window, "JSON ZIP export error", "JSON ZIP export process could not start.")
    window._process = None


def _start_zip_process(
    window: Any,
    project_root: Path,
    destination_folder: Path,
    part_size_mb: int,
) -> None:
    helpers = _process_helpers()
    process = helpers.QProcess(window)
    window._process = process
    process.finished.connect(lambda exit_code, status: _on_zip_process_finished(window, exit_code, status))
    process.errorOccurred.connect(lambda error: _on_zip_process_error(window, error))

    env = helpers._tab4_build_child_env(project_root)
    helpers._tab4_apply_qprocess_env(process, env, helpers._tab4_tool_root())

    process_args = [
        "-m",
        "kanda_reasoner_app.project_context_bundle.handoff_zip_exporter",
        "--root",
        str(project_root),
        "--destination",
        str(destination_folder),
        "--part-size-mb",
        str(part_size_mb),
        "--compact",
    ]

    _start_zip_status(window)
    process.start(sys.executable, process_args)


def _existing_dialog_start_folder(path_text: str) -> Path | None:
    """Return an existing folder suitable for QFileDialog, if available."""
    try:
        candidate = Path(path_text).expanduser()
        if candidate.exists():
            if candidate.is_dir():
                return candidate.resolve()
            parent = candidate.parent
            if parent.exists() and parent.is_dir():
                return parent.resolve()
        parent = candidate.parent
        if parent != candidate and parent.exists() and parent.is_dir():
            return parent.resolve()
    except Exception:
        return None
    return None


def _fallback_dialog_start_folder(project_root: Path) -> str:
    """Return a stable existing start folder for the ZIP destination dialog."""
    anchor = project_root.anchor
    if anchor:
        try:
            anchor_path = Path(anchor).resolve()
            if anchor_path.exists() and anchor_path.is_dir():
                return str(anchor_path)
        except Exception:
            pass
    parent = project_root.parent
    try:
        if parent.exists() and parent.is_dir():
            return str(parent.resolve())
    except Exception:
        pass
    return str(project_root)


def resolve_zip_dialog_start_folder(
    project_root: str | Path,
    last_destination: str | Path | None = None,
) -> str:
    """Return an existing start folder for the ZIP destination dialog."""
    root_path = Path(project_root).expanduser()
    if last_destination is None:
        destination_text = _load_destination()
    else:
        destination_text = str(last_destination).strip()
    if destination_text:
        existing_start = _existing_dialog_start_folder(destination_text)
        if existing_start is not None:
            return str(existing_start)
    return _fallback_dialog_start_folder(root_path)


def _start_folder_for_dialog(project_root: Path) -> str:
    return resolve_zip_dialog_start_folder(project_root)


def run_zip_json_files(window: Any) -> None:
    """Prompt for an outside destination and export JSON handoff ZIP parts."""
    if getattr(window, "_process", None) is not None:
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, "Busy", "Wait for the current Tab 4 process to finish.")
        return

    project_root_raw = window.project_root_edit.text().strip()
    try:
        project_root = _process_helpers()._tab4_resolve_project_root(project_root_raw)
    except Exception as exc:
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(
            window,
            "Invalid path",
            "Project root must be a project folder, not a broad drive root.\n" + str(exc),
        )
        return

    if not project_root.is_dir():
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, "Invalid path", "Project root does not exist:\n" + str(project_root))
        return

    QFileDialog = _qt_widgets().QFileDialog
    destination = QFileDialog.getExistingDirectory(
        window,
        "Select ZIP destination outside the project folder",
        _start_folder_for_dialog(project_root),
    )
    if not destination:
        return

    destination_path = Path(destination).expanduser()
    if not destination_path.exists() or not destination_path.is_dir():
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(
            window,
            "Invalid ZIP destination",
            "Selected ZIP destination folder does not exist:\n" + str(destination_path),
        )
        return

    if _destination_inside_project_root(project_root, destination_path):
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(
            window,
            "Invalid ZIP destination",
            "ZIP files cannot be saved inside the active project folder.\n\n"
            "Project root:\n" + str(project_root) + "\n\n"
            "Choose a folder outside the project.",
        )
        return

    _save_destination(str(destination_path))
    part_size_mb = _selected_part_size_mb(window)
    _append_log(window, "Starting JSON ZIP export...")
    _append_log(window, "  root       : " + str(project_root))
    _append_log(window, "  destination: " + str(destination_path))
    _append_log(window, "  part size  : " + str(part_size_mb) + " MB")
    _start_zip_process(window, project_root, destination_path, part_size_mb)
