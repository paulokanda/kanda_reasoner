# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_process_private_impl.py
"""Qt process orchestration for Tab 4 JSON ZIP export."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import analysis_json_complete_dir
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_paths_private_impl import (
    _destination_inside_project_root,
    _start_folder_for_dialog,
    cleanup_show_project_to_ai_root_after_success,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_publish_private_impl import (
    publish_second_prompt_files_building_dir,
    write_second_prompt_status,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_state_private_impl import (
    _save_destination,
    _selected_part_size_mb,
    save_selected_part_size_mb,
    selected_part_size_mb,
)
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

__all__ = []


def _qt_widgets():
    """Support qt widgets behavior.
    """
    
    return importlib.import_module('PySide6' + '.QtWidgets')


def _process_helpers():
    """Support process helpers behavior.
    """
    
    from kanda_reasoner_app.reasoner_tools_shell.runner_help import window_process_private_impl as helpers
    return helpers


def _set_controls_enabled(window: Any, enabled: bool) -> None:
    """Support set controls enabled behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    enabled : bool
        The enabled value.
    """
    
    for attribute in ('run_button', 'browse_project_button', 'browse_output_button', 'zip_size_100_radio', 'zip_size_200_radio', 'zip_size_300_radio', 'zip_size_400_radio', 'zip_size_500_radio'):
        try:
            getattr(window, attribute).setEnabled(enabled)
        except Exception:
            pass


def _append_log(window: Any, text: str) -> None:
    """Support append log behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    text : str
        The text value.
    """
    
    try:
        window._append_log(text)
    except Exception:
        pass


def _start_zip_status(window: Any) -> None:
    """Support start zip status behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    """
    
    try:
        window._start_busy_animation('Zipping JSON files')
    except Exception:
        try:
            window.status_label.setText('Zipping JSON files...')
        except Exception:
            pass
    _set_controls_enabled(window, False)


def _finish_zip_status(window: Any, status_text: str) -> None:
    """Support finish zip status behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    status_text : str
        The status text value.
    """
    
    try:
        window._stop_busy_animation(status_text)
    except Exception:
        try:
            window.status_label.setText(status_text)
        except Exception:
            pass
    _set_controls_enabled(window, True)


def _decode_process_output(process: Any) -> tuple[str, str]:
    """Support decode process output behavior.
    
    Parameters
    ----------
    process : Any
        The process value.
    
    Returns
    -------
    tuple[str, str]
        The tuple of values.
    """
    
    stdout_text = bytes(process.readAllStandardOutput()).decode('utf-8', errors='replace').strip()
    stderr_text = bytes(process.readAllStandardError()).decode('utf-8', errors='replace').strip()
    return (stdout_text, stderr_text)


def _on_zip_process_finished(window: Any, exit_code: int, _exit_status: Any) -> None:
    """Support on zip process finished behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    exit_code : int
        The exit code value.
    _exit_status : Any
        The exit status value.
    """
    
    process = getattr(window, '_process', None)
    from kanda_reasoner_app.reasoner_tools_shell.runner_help import png_reuse_cancel_controls_private_impl as _png_controls
    if _png_controls.consume_cancel_on_finish(
        window, lambda status: _finish_zip_status(window, status)
    ):
        return
    stdout_text = ''
    stderr_text = ''
    if process is not None:
        stdout_text, stderr_text = _decode_process_output(process)
    if exit_code != 0:
        try:
            final_dir = getattr(window, '_pending_second_prompt_final_dir', '')
            if final_dir:
                write_second_prompt_status(final_dir, status='failed', step='ZIP export failed')
        except Exception:
            pass
        _finish_zip_status(window, 'Failed')
        _append_log(window, '[ERROR] JSON ZIP export failed:')
        _append_log(window, stderr_text or stdout_text or 'Unknown child-process error')
        QMessageBox = _qt_widgets().QMessageBox
        show_error_copy_close_window(window, title='JSON ZIP export error', message=stderr_text or stdout_text or 'Unknown child-process error')
        window._process = None
        return
    try:
        result = json.loads(stdout_text) if stdout_text else {}
    except Exception:
        result = {}
    zip_parts = result.get('zip_parts', [])
    zip_count = len(zip_parts) if isinstance(zip_parts, list) else 0
    warnings = result.get('warnings', [])
    png_assets_reused = bool(result.get('png_assets_reused', False))
    png_assets_reuse_method = str(
        result.get('png_assets_reuse_method', '') or ''
    ).strip()
    destination = str(result.get('destination_folder', '') or '').strip()
    published_after_zip: dict[str, object] | None = None
    try:
        pending_build = Path(str(getattr(window, '_pending_second_prompt_build_dir', '') or '')).expanduser().resolve(strict=False)
        pending_final = Path(str(getattr(window, '_pending_second_prompt_final_dir', '') or '')).expanduser().resolve(strict=False)
        destination_path = Path(destination).expanduser().resolve(strict=False) if destination else None
        if destination_path is not None and pending_build and (destination_path == pending_build) and str(pending_final):
            project_root_for_publish = getattr(window, '_pending_project_root', None)
            published_after_zip = publish_second_prompt_files_building_dir(pending_build, pending_final, project_root=project_root_for_publish)
            destination = str(pending_final)
            final_output_json = pending_final / Path(str(getattr(window, '_pending_output_json', '') or '')).name
            final_runtime_trace = pending_final / Path(str(getattr(window, '_pending_runtime_trace_json', '') or '')).name
            window._pending_output_json = str(final_output_json)
            window._pending_runtime_trace_json = str(final_runtime_trace)
            window._current_output_json = str(final_output_json)
            try:
                window.output_json_edit.setText(str(final_output_json))
                window.runtime_trace_json_edit.setText(str(final_runtime_trace))
            except Exception:
                pass
            _append_log(window, '[OK] Published second_prompt_files delivery folder after ZIP export.')
            _append_log(window, '  final folder: ' + str(pending_final))
            _append_log(window, '  moved_items: ' + str(published_after_zip.get('moved_items', '')))
    except Exception as exc:
        _finish_zip_status(window, 'Failed')
        _append_log(window, '[ERROR] Publishing second_prompt_files after ZIP export failed:')
        _append_log(window, str(exc))
        QMessageBox = _qt_widgets().QMessageBox
        show_error_copy_close_window(window, title='Collector publish error', message=str(exc))
        window._process = None
        return
    try:
        if destination:
            write_second_prompt_status(destination, status='complete', step='ZIP export complete', details=['ZIP parts created: ' + str(zip_count), 'Selected part size MB: ' + str(result.get('part_size_mb', '')), 'Published after ZIP: ' + str(published_after_zip is not None)])
            try:
                cleanup_root = getattr(window, '_pending_project_root', None)
                if cleanup_root:
                    cleanup_show_project_to_ai_root_after_success(cleanup_root, final_dir=destination)
            except Exception:
                pass
    except Exception:
        pass
    _finish_zip_status(window, 'Finished')
    _append_log(window, '[OK] JSON ZIP export completed.')
    _append_log(window, '  zip_count: ' + str(zip_count))
    _append_log(window, '  part_size_mb: ' + str(result.get('part_size_mb', '')))
    _append_log(window, '  png_assets_reused: ' + str(png_assets_reused))
    if png_assets_reuse_method:
        _append_log(
            window,
            '  png_assets_reuse_method: ' + png_assets_reuse_method,
        )
    if isinstance(zip_parts, list):
        for item in zip_parts:
            if isinstance(item, dict):
                _append_log(window, '  zip: ' + str(item.get('filename', '')) + ' (' + str(item.get('size_bytes', '')) + ' bytes)')
    if isinstance(warnings, list):
        for item in warnings:
            _append_log(window, '  warning: ' + str(item))
    window._process = None


def _on_zip_process_error(window: Any, _process_error: Any) -> None:
    """Support on zip process error behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    _process_error : Any
        The process error value.
    """
    
    _finish_zip_status(window, 'Failed')
    _append_log(window, '[ERROR] JSON ZIP export process could not start.')
    QMessageBox = _qt_widgets().QMessageBox
    show_error_copy_close_window(window, title='JSON ZIP export error', message='JSON ZIP export process could not start.')
    window._process = None


def _start_zip_process(window: Any, project_root: Path, destination_folder: Path, part_size_mb: int) -> None:
    """Support start zip process behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    project_root : Path
        The project root path.
    destination_folder : Path
        The destination folder value.
    part_size_mb : int
        The part size mb value.
    """
    
    helpers = _process_helpers()
    process = helpers.QProcess(window)
    window._process = process
    process.finished.connect(lambda exit_code, status: _on_zip_process_finished(window, exit_code, status))
    process.errorOccurred.connect(lambda error: _on_zip_process_error(window, error))
    env = helpers._tab4_build_child_env(project_root)
    try:
        helpers._tab4_apply_second_prompt_build_env(window, env)
    except Exception:
        pass
    helpers._tab4_apply_qprocess_env(process, env, helpers._tab4_tool_root())
    process_args = ['-m', 'kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter', '--root', str(project_root), '--destination', str(destination_folder), '--part-size-mb', str(part_size_mb), '--compact']
    _start_zip_status(window)
    process.start(sys.executable, process_args)


def auto_zip_json_complete(window: Any, project_root: str | Path | None=None) -> None:
    """Automatically export handoff ZIP parts into the dynamic second_prompt_files folder.

    This is the Create Second Prompt Files follow-up path. ZIP export is now
    integrated into generation: the selected project root owns the destination
    contract, and ZIPs are written next to the generated companion artifacts
    under ``<project_drive>:/<project_name>_show_project_to_AI/second_prompt_files``.
    """
    if getattr(window, '_process', None) is not None:
        _append_log(window, '[WARN] Automatic JSON ZIP export skipped because another process is active.')
        return
    raw_root = project_root
    if raw_root is None:
        raw_root = window.project_root_edit.text().strip()
    try:
        resolved_project_root = _process_helpers()._tab4_resolve_project_root(raw_root)
    except Exception as exc:
        _append_log(window, '[ERROR] Automatic JSON ZIP export could not resolve project root: ' + str(exc))
        return
    final_destination = analysis_json_complete_dir(resolved_project_root).expanduser().resolve()
    pending_build_raw = str(getattr(window, '_pending_second_prompt_build_dir', '') or '').strip()
    pending_final_raw = str(getattr(window, '_pending_second_prompt_final_dir', '') or '').strip()
    destination_path = final_destination
    if pending_build_raw and pending_final_raw:
        pending_build = Path(pending_build_raw).expanduser().resolve(strict=False)
        pending_final = Path(pending_final_raw).expanduser().resolve(strict=False)
        if pending_final == final_destination and pending_build.exists():
            destination_path = pending_build
    destination_path.mkdir(parents=True, exist_ok=True)
    part_size_mb = selected_part_size_mb(window)
    _append_log(window, 'Starting automatic JSON ZIP export from Create Second Prompt Files...')
    _append_log(window, '  manual ZIP button removed; ZIP export is part of Create Second Prompt Files')
    _append_log(window, '  root       : ' + str(resolved_project_root))
    _append_log(window, '  build/final: ' + ('build folder first' if destination_path != final_destination else 'final folder'))
    _append_log(window, '  destination: ' + str(destination_path))
    _append_log(window, '  final      : ' + str(final_destination))
    _append_log(window, '  part size  : ' + str(part_size_mb) + ' MB')
    _start_zip_process(window, resolved_project_root, destination_path, part_size_mb)


def run_zip_json_files(window: Any) -> None:
    """Prompt for an outside destination and export JSON handoff ZIP parts."""
    if getattr(window, '_process', None) is not None:
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, 'Busy', 'Wait for the current Tab 4 process to finish.')
        return
    project_root_raw = window.project_root_edit.text().strip()
    try:
        project_root = _process_helpers()._tab4_resolve_project_root(project_root_raw)
    except Exception as exc:
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, 'Invalid path', 'Project root must be a project folder, not a broad drive root.\n' + str(exc))
        return
    if not project_root.is_dir():
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, 'Invalid path', 'Project root does not exist:\n' + str(project_root))
        return
    QFileDialog = _qt_widgets().QFileDialog
    destination = QFileDialog.getExistingDirectory(window, 'Select ZIP destination outside the project folder', _start_folder_for_dialog(project_root))
    if not destination:
        return
    destination_path = Path(destination).expanduser()
    if not destination_path.exists() or not destination_path.is_dir():
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, 'Invalid ZIP destination', 'Selected ZIP destination folder does not exist:\n' + str(destination_path))
        return
    if _destination_inside_project_root(project_root, destination_path):
        QMessageBox = _qt_widgets().QMessageBox
        QMessageBox.warning(window, 'Invalid ZIP destination', 'ZIP files cannot be saved inside the active project folder.\n\nProject root:\n' + str(project_root) + '\n\nChoose a folder outside the project.')
        return
    _save_destination(str(destination_path))
    part_size_mb = _selected_part_size_mb(window)
    save_selected_part_size_mb(part_size_mb)
    _append_log(window, 'Starting JSON ZIP export...')
    _append_log(window, '  root       : ' + str(project_root))
    _append_log(window, '  destination: ' + str(destination_path))
    _append_log(window, '  part size  : ' + str(part_size_mb) + ' MB')
    _start_zip_process(window, project_root, destination_path, part_size_mb)

