# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_paths_private_impl.py
"""Path resolution and Show Project to AI root cleanup helpers."""
from __future__ import annotations

import shutil
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    LIFECYCLE_MANIFEST_NAME,
    PROJECT_FREEZE_AFTER_UPDATE_DIR,
    ensure_show_project_lifecycle_manifest,
    is_show_project_persistent_child,
    project_analysis_evidence_root,
    project_name_from_root,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help.zip_json_files_state_private_impl import (
    STATUS_FILE_NAME,
    _load_destination,
)

__all__ = []


_ALLOWED_SHOW_PROJECT_CHILD_DIRS = {
    'first_prompt_files',
    'second_prompt_files',
    'project_error_memory',
    PROJECT_FREEZE_AFTER_UPDATE_DIR,
}
_STALE_SHOW_PROJECT_DIR_NAMES = {'second_prompt_files_building', 'json_splitted'}
_STALE_SHOW_PROJECT_DIR_PREFIXES = (
    'json_handoff_zip_export_',
    '.json_handoff_zip_export_',
    '.json_handoff_zip_stage_',
    '.json_handoff_zip_work_',
    '.second_prompt_files_publish_',
    '.second_prompt_files_previous_',
)
_TRANSIENT_DAILY_REFACTOR_DIR_NAMES = {
    'daily_refactor',
    'daily_refactor_report',
    'daily_refactor_engine',
}

def _require_show_project_child_dir(output_dir: str | Path, expected_name: str) -> Path:
    """Support require show project child dir behavior.
    
    Parameters
    ----------
    output_dir : str | Path
        The output dir value.
    expected_name : str
        The expected name value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    resolved_dir = Path(output_dir).expanduser().resolve(strict=False)
    if resolved_dir.name != expected_name:
        raise ValueError('Refusing output-folder operation because folder is not ' + expected_name + ': ' + str(resolved_dir))
    parent = resolved_dir.parent
    if not parent.name.endswith('_show_project_to_AI'):
        raise ValueError('Refusing output-folder operation because parent is not *_show_project_to_AI: ' + str(resolved_dir))
    return resolved_dir


def _is_known_show_project_root_file(path: Path, project_root: str | Path | None=None) -> bool:
    """Return True only for known generated files that leaked to the parent root."""
    if not path.is_file():
        return False
    name = path.name
    if name == STATUS_FILE_NAME:
        return True
    slug = ''
    if project_root is not None:
        try:
            slug = project_name_from_root(project_root)
        except Exception:
            slug = ''
    generated_suffixes = {'.json', '.zip', '.txt', '.md'}
    if path.suffix.lower() not in generated_suffixes:
        return False
    if slug and (name.startswith(slug + '__') or name.startswith(slug + '_split_') or name.startswith(slug + '__complete')):
        return True
    return '__source_archive_' in name or '__ai_handoff' in name or '__complete' in name or name.endswith('_split_manifest.json') or name.endswith('_split_index.json') or name.endswith('__complete__web_ai_route_manifest.json')


def cleanup_show_project_to_ai_root_after_success(project_root: str | Path, *, final_dir: str | Path | None=None) -> dict[str, object]:
    """Remove stale generated siblings while preserving persistent state.

    This cleanup is deliberately limited to known Show Project to AI generated
    folders/files. It preserves canonical child folders and persistent project
    state declared by the lifecycle manifest. Unknown folders are skipped.
    """
    root = project_analysis_evidence_root(project_root).expanduser().resolve(strict=False)
    removed: list[str] = []
    skipped: list[str] = []
    if not root.exists():
        return {'root': str(root), 'removed': removed, 'skipped': skipped}
    ensure_show_project_lifecycle_manifest(project_root)
    final_path = Path(final_dir).expanduser().resolve(strict=False) if final_dir is not None else None
    for child in list(root.iterdir()):
        name = child.name
        if name == LIFECYCLE_MANIFEST_NAME:
            skipped.append(str(child))
            continue
        if name in _ALLOWED_SHOW_PROJECT_CHILD_DIRS or is_show_project_persistent_child(project_root, name):
            skipped.append(str(child))
            continue
        if final_path is not None:
            try:
                if child.resolve(strict=False) == final_path:
                    skipped.append(str(child))
                    continue
            except Exception:
                pass
        remove_child = False
        if child.is_dir():
            remove_child = name in _STALE_SHOW_PROJECT_DIR_NAMES or name.startswith(_STALE_SHOW_PROJECT_DIR_PREFIXES)
        elif child.is_file():
            remove_child = _is_known_show_project_root_file(child, project_root)
        if not remove_child:
            skipped.append(str(child))
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
        removed.append(str(child))
    return {'root': str(root), 'removed': removed, 'skipped': skipped}


def _is_transient_daily_refactor_folder(path: Path) -> bool:
    """Return True for generated daily-refactor folders safe to remove."""
    name = path.name.lower()
    return name in _TRANSIENT_DAILY_REFACTOR_DIR_NAMES or name.endswith('_daily_refactor_engine') or name.endswith('_daily_refactor_report')


def _destination_inside_project_root(project_root: Path, destination: Path) -> bool:
    """Support destination inside project root behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    destination : Path
        The destination path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    try:
        resolved_root = project_root.expanduser().resolve()
        resolved_destination = destination.expanduser().resolve()
        resolved_destination.relative_to(resolved_root)
        return True
    except ValueError:
        return False
    except Exception:
        return False


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


def resolve_zip_dialog_start_folder(project_root: str | Path, last_destination: str | Path | None=None) -> str:
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
    """Support start folder for dialog behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return resolve_zip_dialog_start_folder(project_root)

