# project-path: kanda_reasoner_app/project_analysis_evidence_paths.py
"""Path helpers for generated project-analysis evidence artifacts.

Generated evidence resolves outside the selected project source tree.
The active output root is the external ``show project to AI`` folder for the
selected/analyzed project. Complete Project Structure Map files are generated
inside its ``second_prompt_files`` child folder:
``<project_drive>:/<project_name>_show_project_to_AI/second_prompt_files``.
During a Run Collector rebuild, child processes may temporarily write to
``second_prompt_files_building`` via a guarded environment override before the
finished files are published to ``second_prompt_files``.

The historical names ``project_analysis_evidence`` and ``json_complete`` are
retained in helper/function names for compatibility with existing callers, but
complete Project Structure Map artifacts now resolve to the dynamic
``*_show_project_to_AI/second_prompt_files`` folder rather than to an
architecture-audit ``current/json_complete`` subfolder.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from kanda_reasoner_app._project_analysis_evidence_path_resolution import (
    PROJECT_REFERENCE_DIR,
    PROJECT_ANALYSIS_EVIDENCE_DIR,
    SHOW_PROJECT_TO_AI_SUFFIX,
    DELETE_AFTER_DAILY_WORK_SUFFIX,
    SECOND_PROMPT_FILES_DIR,
    SECOND_PROMPT_FILES_BUILDING_DIR,
    FIRST_PROMPT_FILES_DIR,
    PROJECT_ERROR_MEMORY_DIR,
    PROJECT_FREEZE_AFTER_UPDATE_DIR,
    LIFECYCLE_MANIFEST_NAME,
    SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV,
    SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV,
    JSON_COMPLETE_DIR,
    JSON_PARTS_DIR,
    _SAFE_NAME_RE,
    _SAFE_SLUG_RE,
    _REPEATED_UNDERSCORE_RE,
    normalize_path,
    make_safe_slug,
    project_name_from_root,
    _folder_name_for_slug,
    _base_slug_from_suffixed_name,
    show_project_to_ai_root_from_hint,
    _show_project_to_ai_root,
    project_analysis_evidence_root,
    _normalize_project_analysis_evidence_dir_casing,
    _paths_refer_to_same_location,
    analysis_json_building_dir,
    _show_project_to_ai_override_project_root,
    _active_artifact_project_root,
    _analysis_json_complete_dir_override,
    analysis_json_complete_dir,
    analysis_project_error_memory_dir,
    analysis_project_freeze_after_update_dir,
    legacy_project_freeze_after_update_dir,
    show_project_lifecycle_manifest_path,
    analysis_first_prompt_files_dir,
    analysis_json_parts_dir,
    _project_name,
    primary_evidence_json_path,
    secondary_evidence_json_path,
    working_copy_json_path,
    working_copy_metadata_path,
    parts_manifest_file_path,
    parts_index_file_path,
    route_manifest_file_path,
    normalize_evidence_artifact_path,
)

__all__ = [
    "PROJECT_REFERENCE_DIR",
    "PROJECT_ANALYSIS_EVIDENCE_DIR",
    "JSON_COMPLETE_DIR",
    "SECOND_PROMPT_FILES_DIR",
    "SECOND_PROMPT_FILES_BUILDING_DIR",
    "FIRST_PROMPT_FILES_DIR",
    "PROJECT_ERROR_MEMORY_DIR",
    "PROJECT_FREEZE_AFTER_UPDATE_DIR",
    "LIFECYCLE_MANIFEST_NAME",
    "SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV",
    "SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV",
    "SHOW_PROJECT_TO_AI_SUFFIX",
    "DELETE_AFTER_DAILY_WORK_SUFFIX",
    "JSON_PARTS_DIR",
    "project_name_from_root",
    "show_project_to_ai_root_from_hint",
    "project_analysis_evidence_root",
    "analysis_json_complete_dir",
    "analysis_json_building_dir",
    "analysis_first_prompt_files_dir",
    "analysis_project_error_memory_dir",
    "analysis_project_freeze_after_update_dir",
    "legacy_project_freeze_after_update_dir",
    "show_project_lifecycle_manifest_path",
    "ensure_show_project_lifecycle_manifest",
    "load_show_project_lifecycle_manifest",
    "is_show_project_disposable_child",
    "is_show_project_persistent_child",
    "analysis_json_parts_dir",
    "ensure_project_analysis_evidence_dirs",
    "primary_evidence_json_path",
    "secondary_evidence_json_path",
    "parts_manifest_file_path",
    "parts_index_file_path",
    "route_manifest_file_path",
    "working_copy_json_path",
    "working_copy_metadata_path",
    "relative_evidence_path",
    "relative_primary_evidence_json_path",
    "relative_secondary_evidence_json_path",
    "relative_parts_manifest_file_path",
    "relative_parts_index_file_path",
    "relative_route_manifest_file_path",
    "relative_working_copy_json_path",
    "relative_working_copy_metadata_path",
    "normalize_evidence_artifact_path",
]

def _default_show_project_lifecycle_manifest() -> dict[str, Any]:
    """Return the default persistent/disposable child-folder policy."""
    return {
        "schema_version": "1.0",
        "persistent": [
            PROJECT_ERROR_MEMORY_DIR,
            PROJECT_FREEZE_AFTER_UPDATE_DIR,
        ],
        "disposable": [
            FIRST_PROMPT_FILES_DIR,
            SECOND_PROMPT_FILES_DIR,
            SECOND_PROMPT_FILES_BUILDING_DIR,
            "install_and_patch",
            JSON_PARTS_DIR,
        ],
    }


def _atomic_write_text(path: Path, text: str) -> None:
    """Write a UTF-8 text file atomically in its target directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
        dir=str(path.parent),
        prefix="." + path.name + ".",
        suffix=".tmp",
    )
    tmp_name = handle.name
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        tmp_path = Path(tmp_name)
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    """Return stripped unique string values in first-seen order."""
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value).strip()
        if not item or item in seen:
            continue
        result.append(item)
        seen.add(item)
    return result


def load_show_project_lifecycle_manifest(project_root: str | Path) -> dict[str, Any]:
    """Load the external project-support lifecycle manifest, or defaults."""
    manifest_path = show_project_lifecycle_manifest_path(project_root)
    if not manifest_path.is_file():
        return _default_show_project_lifecycle_manifest()
    try:
        loaded = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return _default_show_project_lifecycle_manifest()
    if not isinstance(loaded, dict):
        return _default_show_project_lifecycle_manifest()
    default = _default_show_project_lifecycle_manifest()
    persistent = loaded.get("persistent") if isinstance(loaded.get("persistent"), list) else []
    disposable = loaded.get("disposable") if isinstance(loaded.get("disposable"), list) else []
    return {
        "schema_version": str(loaded.get("schema_version") or default["schema_version"]),
        "persistent": _dedupe_preserve_order([*default["persistent"], *[str(item) for item in persistent]]),
        "disposable": _dedupe_preserve_order([*default["disposable"], *[str(item) for item in disposable]]),
    }


def ensure_show_project_lifecycle_manifest(project_root: str | Path) -> Path:
    """Create or repair the lifecycle manifest for persistent-state safety."""
    manifest_path = show_project_lifecycle_manifest_path(project_root)
    manifest = load_show_project_lifecycle_manifest(project_root)
    _atomic_write_text(
        manifest_path,
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    )
    return manifest_path


def is_show_project_persistent_child(project_root: str | Path, child_name: str) -> bool:
    """Return True if child_name is explicitly persistent."""
    manifest = load_show_project_lifecycle_manifest(project_root)
    return str(child_name) in set(str(item) for item in manifest.get("persistent", []))


def is_show_project_disposable_child(project_root: str | Path, child_name: str) -> bool:
    """Return True if child_name is explicitly disposable."""
    manifest = load_show_project_lifecycle_manifest(project_root)
    return str(child_name) in set(str(item) for item in manifest.get("disposable", []))


def ensure_project_analysis_evidence_dirs(project_root: str | Path) -> Path:
    """Create and return the external evidence root and child folders."""
    evidence_root = project_analysis_evidence_root(project_root)
    analysis_first_prompt_files_dir(project_root).mkdir(parents=True, exist_ok=True)
    analysis_project_error_memory_dir(project_root).mkdir(parents=True, exist_ok=True)
    analysis_project_freeze_after_update_dir(project_root).mkdir(parents=True, exist_ok=True)
    analysis_json_complete_dir(project_root).mkdir(parents=True, exist_ok=True)
    ensure_show_project_lifecycle_manifest(project_root)
    # Normal Show Project to AI root must only contain first_prompt_files and
    # second_prompt_files after a successful run. The temporary building folder
    # is created only by the runner while work is active, and legacy
    # json_splitted is not created by normal directory preparation.
    return evidence_root


def relative_evidence_path(*parts: str) -> str:
    """Return a portable POSIX relative path for generated evidence.

    ``analysis_json_complete_dir`` now points at
    ``*_show_project_to_AI/second_prompt_files``. Avoid duplicating the logical
    folder name when callers pass retained compatibility constants.
    """
    cleaned = [str(part).strip("/\\") for part in parts if str(part).strip("/\\")]
    if cleaned and cleaned[0] == PROJECT_ANALYSIS_EVIDENCE_DIR:
        cleaned = cleaned[1:]
    return str(
        Path(PROJECT_ANALYSIS_EVIDENCE_DIR) / Path(*cleaned)
    ).replace("\\", "/")


def relative_primary_evidence_json_path(project_name: str = "project") -> str:
    """Return the primary generated JSON relative path for a project name."""
    return relative_evidence_path(JSON_COMPLETE_DIR, f"{project_name}__complete.json")


def relative_secondary_evidence_json_path(project_name: str = "project") -> str:
    """Return the runtime-trace JSON relative path for a project name."""
    return relative_evidence_path(
        JSON_COMPLETE_DIR,
        f"{project_name}__complete_runtime_trace.json",
    )


def relative_working_copy_json_path(project_name: str = "project") -> str:
    """Return the generated working-copy JSON relative path."""
    return relative_evidence_path(
        JSON_COMPLETE_DIR,
        f"{project_name}__complete_local_AI.json",
    )


def relative_working_copy_metadata_path(project_name: str = "project") -> str:
    """Return the generated working-copy metadata relative path."""
    return relative_evidence_path(
        JSON_COMPLETE_DIR,
        f"{project_name}__complete_local_AI.meta.json",
    )


def relative_parts_manifest_file_path(project_name: str = "project") -> str:
    """Return the split manifest relative path for a project name."""
    return relative_evidence_path(JSON_PARTS_DIR, f"{project_name}_split_manifest.json")


def relative_parts_index_file_path(project_name: str = "project") -> str:
    """Return the split index relative path for a project name."""
    return relative_evidence_path(JSON_PARTS_DIR, f"{project_name}_split_index.json")


def relative_route_manifest_file_path(project_name: str = "project") -> str:
    """Return the route manifest relative path for a project name."""
    return relative_evidence_path(
        JSON_PARTS_DIR,
        f"{project_name}__complete__web_ai_route_manifest.json",
    )
