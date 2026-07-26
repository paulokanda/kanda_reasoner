# project-path: kanda_reasoner_app/error_memory/paths.py
"""Dynamic paths for project-specific Error Memory.

Error Memory data is owned by the selected project, but it is intentionally
stored outside the selected source tree under the selected project's external
``*_show_project_to_AI`` folder.  This keeps project source folders clean while
preserving one Error Memory bucket per project.
"""

from __future__ import annotations


__all__ = [
    'ensure_error_memory_dirs',
    'resolve_error_memory_exports_dir',
    'resolve_error_memory_index_path',
    'resolve_error_memory_lessons_dir',
    'resolve_error_memory_schemas_dir',
    'resolve_lesson_schema_path',
    'resolve_project_error_memory_root',
    'resolve_second_prompt_files_root',
    'resolve_show_project_to_ai_root',
]
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SECOND_PROMPT_FILES_DIR,
    show_project_to_ai_root_from_hint,
)

PROJECT_ERROR_MEMORY_DIR = "project_error_memory"
LESSONS_DIR = "lessons"
EXPORTS_DIR = "exports"
SCHEMAS_DIR = "schemas"
LESSONS_INDEX_FILENAME = "lessons_index.json"
LESSON_SCHEMA_FILENAME = "lesson.schema.json"


def resolve_show_project_to_ai_root(selected_project_root: str | Path) -> Path:
    """Return ``<drive_where_project_is>/<project>_show_project_to_AI``.

    The input may be the real project root, an existing ``*_show_project_to_AI``
    folder, one of its generated child folders, or the daily-work maintenance
    folder.  Generated-output hints are canonicalized so Error Memory never
    creates sibling typo folders such as
    ``project_error_memory_show_project_to_AI`` or
    ``<project>_delete_after_daily_work_show_project_to_AI``.
    """
    return show_project_to_ai_root_from_hint(selected_project_root)


def resolve_project_error_memory_root(selected_project_root: str | Path) -> Path:
    """Return ``<drive>/<project>_show_project_to_AI/project_error_memory``."""
    return resolve_show_project_to_ai_root(selected_project_root) / PROJECT_ERROR_MEMORY_DIR


def resolve_error_memory_lessons_dir(selected_project_root: str | Path) -> Path:
    """Return the canonical JSON lesson folder for the selected project."""
    return resolve_project_error_memory_root(selected_project_root) / LESSONS_DIR


def resolve_error_memory_exports_dir(selected_project_root: str | Path) -> Path:
    """Return the generated/disposable Error Memory export folder."""
    return resolve_project_error_memory_root(selected_project_root) / EXPORTS_DIR


def resolve_error_memory_schemas_dir(selected_project_root: str | Path) -> Path:
    """Return the local schema folder for Error Memory records."""
    return resolve_project_error_memory_root(selected_project_root) / SCHEMAS_DIR


def resolve_error_memory_index_path(selected_project_root: str | Path) -> Path:
    """Return the lightweight lesson index path for the selected project."""
    return resolve_project_error_memory_root(selected_project_root) / LESSONS_INDEX_FILENAME


def resolve_lesson_schema_path(selected_project_root: str | Path) -> Path:
    """Return the local lesson schema path for Error Memory records."""
    return resolve_error_memory_schemas_dir(selected_project_root) / LESSON_SCHEMA_FILENAME


def resolve_second_prompt_files_root(selected_project_root: str | Path) -> Path:
    """Return the generated second-prompt upload folder for the selected project."""
    return resolve_show_project_to_ai_root(selected_project_root) / SECOND_PROMPT_FILES_DIR


def ensure_error_memory_dirs(selected_project_root: str | Path) -> dict[str, Path]:
    """Create and return canonical Error Memory directories."""
    root = resolve_project_error_memory_root(selected_project_root)
    lessons = resolve_error_memory_lessons_dir(selected_project_root)
    exports = resolve_error_memory_exports_dir(selected_project_root)
    schemas = resolve_error_memory_schemas_dir(selected_project_root)
    for path in (root, lessons, exports, schemas):
        path.mkdir(parents=True, exist_ok=True)
    return {
        "root": root,
        "lessons": lessons,
        "exports": exports,
        "schemas": schemas,
    }
