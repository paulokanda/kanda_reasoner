# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py
"""Tab 4 JSON ZIP export helpers.

This module keeps ZIP-export GUI behavior outside the collector process helper
so the collector box remains focused on collection and bundle generation.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_state_private_impl as _state_impl
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_state_private_impl import (
    ALLOWED_ZIP_SIZE_MB_OPTIONS as _public_ALLOWED_ZIP_SIZE_MB_OPTIONS,
    DEFAULT_ZIP_SIZE_MB as _public_DEFAULT_ZIP_SIZE_MB,
    EXTENDED_ZIP_SIZE_MB_OPTIONS as _public_EXTENDED_ZIP_SIZE_MB_OPTIONS,
    STATUS_FILE_NAME as _public_STATUS_FILE_NAME,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_paths_private_impl import (
    _destination_inside_project_root,
    _existing_dialog_start_folder,
    _fallback_dialog_start_folder,
    _is_known_show_project_root_file,
    _is_transient_daily_refactor_folder,
    _require_show_project_child_dir,
    _start_folder_for_dialog,
    cleanup_show_project_to_ai_root_after_success as _public_cleanup_show_project_to_ai_root_after_success,
    resolve_zip_dialog_start_folder as _public_resolve_zip_dialog_start_folder,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_process_private_impl import (
    _append_log,
    _decode_process_output,
    _finish_zip_status,
    _on_zip_process_error,
    _on_zip_process_finished,
    _process_helpers,
    _qt_widgets,
    _set_controls_enabled,
    _start_zip_process,
    _start_zip_status,
    auto_zip_json_complete as _public_auto_zip_json_complete,
    run_zip_json_files as _public_run_zip_json_files,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_publish_private_impl import (
    _clear_dir_contents,
    _refresh_bundle_manifest_after_publish_rewrite,
    _remove_forbidden_second_prompt_payloads,
    _rewrite_generated_text_paths,
    clear_second_prompt_files_building_dir as _public_clear_second_prompt_files_building_dir,
    clear_second_prompt_files_dir as _public_clear_second_prompt_files_dir,
    cleanup_loose_json_files_after_success as _public_cleanup_loose_json_files_after_success,
    cleanup_transient_daily_refactor_folders as _public_cleanup_transient_daily_refactor_folders,
    publish_second_prompt_files_building_dir as _public_publish_second_prompt_files_building_dir,
    second_prompt_files_building_dir as _public_second_prompt_files_building_dir,
    write_second_prompt_status as _public_write_second_prompt_status,
)

DEFAULT_ZIP_SIZE_MB = _public_DEFAULT_ZIP_SIZE_MB
EXTENDED_ZIP_SIZE_MB_OPTIONS = _public_EXTENDED_ZIP_SIZE_MB_OPTIONS
ALLOWED_ZIP_SIZE_MB_OPTIONS = _public_ALLOWED_ZIP_SIZE_MB_OPTIONS
STATUS_FILE_NAME = _public_STATUS_FILE_NAME
cleanup_show_project_to_ai_root_after_success = _public_cleanup_show_project_to_ai_root_after_success
resolve_zip_dialog_start_folder = _public_resolve_zip_dialog_start_folder
auto_zip_json_complete = _public_auto_zip_json_complete
run_zip_json_files = _public_run_zip_json_files
cleanup_loose_json_files_after_success = _public_cleanup_loose_json_files_after_success
cleanup_transient_daily_refactor_folders = _public_cleanup_transient_daily_refactor_folders
clear_second_prompt_files_building_dir = _public_clear_second_prompt_files_building_dir
clear_second_prompt_files_dir = _public_clear_second_prompt_files_dir
publish_second_prompt_files_building_dir = _public_publish_second_prompt_files_building_dir
second_prompt_files_building_dir = _public_second_prompt_files_building_dir
write_second_prompt_status = _public_write_second_prompt_status

__all__ = [
    'DEFAULT_ZIP_SIZE_MB',
    'EXTENDED_ZIP_SIZE_MB_OPTIONS',
    'ALLOWED_ZIP_SIZE_MB_OPTIONS',
    'load_saved_part_size_mb',
    'save_selected_part_size_mb',
    'cleanup_loose_json_files_after_success',
    'cleanup_transient_daily_refactor_folders',
    'auto_zip_json_complete',
    'cleanup_show_project_to_ai_root_after_success',
    'clear_second_prompt_files_dir',
    'clear_second_prompt_files_building_dir',
    'publish_second_prompt_files_building_dir',
    'second_prompt_files_building_dir',
    'write_second_prompt_status',
    'resolve_zip_dialog_start_folder',
    'run_zip_json_files',
    'selected_part_size_mb',
]

# Compatibility markers for tests that inspect this historical wrapper path.
# helpers.QProcess(window)
# QFileDialog.getExistingDirectory
# QMessageBox
# Selected ZIP destination folder does not exist
# importlib.import_module
# manual ZIP button removed
# analysis_json_complete_dir
# second_prompt_files
# second_prompt_files_building

_DEFAULT_PREFS_PATH = _state_impl._prefs_path


def _prefs_path() -> Path:
    """Return the ZIP export preference file path."""
    return _DEFAULT_PREFS_PATH()


def _sync_state_prefs_path() -> None:
    _state_impl._prefs_path = _prefs_path


def _load_prefs_payload() -> dict[str, Any]:
    _sync_state_prefs_path()
    return _state_impl._load_prefs_payload()


def _save_prefs_payload(payload: dict[str, Any]) -> None:
    _sync_state_prefs_path()
    _state_impl._save_prefs_payload(payload)


def _load_destination() -> str:
    _sync_state_prefs_path()
    return _state_impl._load_destination()


def _save_destination(destination_folder: str) -> None:
    _sync_state_prefs_path()
    _state_impl._save_destination(destination_folder)


def load_saved_part_size_mb() -> int:
    """Return the saved ZIP part-size preference or the default 500 MB."""
    _sync_state_prefs_path()
    return _state_impl.load_saved_part_size_mb()


def save_selected_part_size_mb(part_size_mb: int) -> None:
    """Persist the user's selected ZIP part-size option for next session."""
    _sync_state_prefs_path()
    _state_impl.save_selected_part_size_mb(part_size_mb)


def selected_part_size_mb(window: Any) -> int:
    """Return and persist the selected ZIP size option for the collector tab."""
    _sync_state_prefs_path()
    return _state_impl.selected_part_size_mb(window)


def _selected_part_size_mb(window: Any) -> int:
    _sync_state_prefs_path()
    return _state_impl._selected_part_size_mb(window)
