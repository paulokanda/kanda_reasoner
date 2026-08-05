# project-path: kanda_reasoner_app/error_memory/__init__.py
"""Owner-scoped Error Memory helpers for KANDA Reasoner."""

from __future__ import annotations

from .backend import (
    ErrorMemoryBackend,
    ErrorMemoryBackendError,
    OwnerMetadataPolicy,
    project_error_memory_backend,
    tool_error_memory_backend,
)
from .cross_owner_reference import (
    CrossOwnerLessonReference,
    create_cross_owner_reference,
    list_cross_owner_references,
    resolve_cross_owner_reference,
)
from .exporter import (
    build_complete_error_memory_ai_clipboard_json,
    write_complete_error_memory_ai_clipboard_export,
    write_error_memory_ai_send_files,
)
from .guard import analyze_error_against_lessons
from .importer import import_error_memory_file, import_error_memory_zip
from .intake import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    build_error_lesson_ai_form_prompt,
    parse_error_lesson_ai_response,
    save_ai_form_as_lesson,
)
from .paths import (
    PROJECT_ERROR_MEMORY_DIR,
    TOOL_ERROR_MEMORY_DIR,
    resolve_error_memory_exports_dir,
    resolve_error_memory_lessons_dir,
    resolve_error_memory_schemas_dir,
    resolve_project_error_memory_root,
    resolve_second_prompt_files_root,
    resolve_tool_error_memory_root,
)
from .store import (
    bootstrap_error_memory_store,
    list_lessons,
    load_lesson,
    save_lesson,
)

__all__ = [
    "CrossOwnerLessonReference",
    "ERROR_LESSON_JSON_BEGIN",
    "ERROR_LESSON_JSON_END",
    "ErrorMemoryBackend",
    "ErrorMemoryBackendError",
    "OwnerMetadataPolicy",
    "PROJECT_ERROR_MEMORY_DIR",
    "TOOL_ERROR_MEMORY_DIR",
    "analyze_error_against_lessons",
    "bootstrap_error_memory_store",
    "build_complete_error_memory_ai_clipboard_json",
    "build_error_lesson_ai_form_prompt",
    "create_cross_owner_reference",
    "import_error_memory_file",
    "import_error_memory_zip",
    "list_cross_owner_references",
    "list_lessons",
    "load_lesson",
    "parse_error_lesson_ai_response",
    "project_error_memory_backend",
    "resolve_cross_owner_reference",
    "resolve_error_memory_exports_dir",
    "resolve_error_memory_lessons_dir",
    "resolve_error_memory_schemas_dir",
    "resolve_project_error_memory_root",
    "resolve_second_prompt_files_root",
    "resolve_tool_error_memory_root",
    "save_ai_form_as_lesson",
    "save_lesson",
    "tool_error_memory_backend",
    "write_complete_error_memory_ai_clipboard_export",
    "write_error_memory_ai_send_files",
]
