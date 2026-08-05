# project-path: kanda_reasoner_app/error_memory/paths.py
"""Owner-aware paths for Tool and Project Error Memory stores."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    SECOND_PROMPT_FILES_DIR,
    show_project_to_ai_root_from_hint,
)

from .backend import (
    ErrorMemoryBackend,
    coerce_error_memory_backend,
    tool_error_memory_backend,
)

PROJECT_ERROR_MEMORY_DIR = "project_error_memory"
TOOL_ERROR_MEMORY_DIR = "tool_error_memory"
LESSONS_DIR = "lessons"
EXPORTS_DIR = "exports"
SCHEMAS_DIR = "schemas"
REFERENCES_DIR = "cross_owner_references"
LESSONS_INDEX_FILENAME = "lessons_index.json"
LESSON_SCHEMA_FILENAME = "lesson.schema.json"

__all__ = [
    "PROJECT_ERROR_MEMORY_DIR",
    "TOOL_ERROR_MEMORY_DIR",
    "ensure_error_memory_dirs",
    "resolve_error_memory_exports_dir",
    "resolve_error_memory_index_path",
    "resolve_error_memory_lessons_dir",
    "resolve_error_memory_references_dir",
    "resolve_error_memory_root",
    "resolve_error_memory_schemas_dir",
    "resolve_lesson_schema_path",
    "resolve_project_error_memory_root",
    "resolve_second_prompt_files_root",
    "resolve_show_project_to_ai_root",
    "resolve_tool_error_memory_root",
]


def resolve_show_project_to_ai_root(selected_project_root: str | Path) -> Path:
    """Return the canonical external Show Project to AI support root."""
    return show_project_to_ai_root_from_hint(selected_project_root)


def resolve_project_error_memory_root(selected_project_root: str | Path) -> Path:
    """Return the selected Project canonical Error Memory root."""
    return resolve_show_project_to_ai_root(selected_project_root) / PROJECT_ERROR_MEMORY_DIR


def resolve_tool_error_memory_root(
    tool_source_root: str | Path | None = None,
) -> Path:
    """Return the Tool canonical Error Memory root."""
    return tool_error_memory_backend(tool_source_root).root


def resolve_error_memory_root(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Return the explicit backend root or legacy Project backend root."""
    return coerce_error_memory_backend(target).root


def resolve_error_memory_lessons_dir(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Return the canonical lesson folder for one backend."""
    return coerce_error_memory_backend(target).lessons_dir


def resolve_error_memory_exports_dir(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Return the generated export folder for one backend."""
    return coerce_error_memory_backend(target).exports_dir


def resolve_error_memory_schemas_dir(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Return the local schema folder for one backend."""
    return coerce_error_memory_backend(target).schemas_dir


def resolve_error_memory_references_dir(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Return the cross-owner reference folder for one backend."""
    return coerce_error_memory_backend(target).references_dir


def resolve_error_memory_index_path(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Return the lightweight lesson index path for one backend."""
    return coerce_error_memory_backend(target).index_path


def resolve_lesson_schema_path(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Return the local lesson schema path for one backend."""
    return coerce_error_memory_backend(target).schema_path


def resolve_second_prompt_files_root(selected_project_root: str | Path) -> Path:
    """Return the selected Project generated second-prompt upload folder."""
    return resolve_show_project_to_ai_root(selected_project_root) / SECOND_PROMPT_FILES_DIR


def ensure_error_memory_dirs(
    target: ErrorMemoryBackend | str | Path,
) -> dict[str, Path]:
    """Create and return one explicit Error Memory backend directory set."""
    return coerce_error_memory_backend(target).ensure_dirs()
