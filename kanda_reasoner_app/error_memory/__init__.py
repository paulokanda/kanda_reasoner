# project-path: kanda_reasoner_app/error_memory/__init__.py
"""Project-specific Error Memory helpers for KANDA Reasoner."""

from __future__ import annotations

from .paths import (
    PROJECT_ERROR_MEMORY_DIR,
    resolve_project_error_memory_root,
    resolve_error_memory_lessons_dir,
    resolve_error_memory_exports_dir,
    resolve_error_memory_schemas_dir,
    resolve_second_prompt_files_root,
)
from .store import bootstrap_error_memory_store, save_lesson, list_lessons, load_lesson
from .exporter import build_complete_error_memory_ai_clipboard_json, write_complete_error_memory_ai_clipboard_export, write_error_memory_ai_send_files
from .importer import import_error_memory_file, import_error_memory_zip
from .guard import analyze_error_against_lessons
from .intake import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    build_error_lesson_ai_form_prompt,
    parse_error_lesson_ai_response,
    save_ai_form_as_lesson,
)

__all__ = [
    "PROJECT_ERROR_MEMORY_DIR",
    "resolve_project_error_memory_root",
    "resolve_error_memory_lessons_dir",
    "resolve_error_memory_exports_dir",
    "resolve_error_memory_schemas_dir",
    "resolve_second_prompt_files_root",
    "bootstrap_error_memory_store",
    "save_lesson",
    "list_lessons",
    "load_lesson",
    "build_complete_error_memory_ai_clipboard_json",
    "write_complete_error_memory_ai_clipboard_export",
    "write_error_memory_ai_send_files",
    "ERROR_LESSON_JSON_BEGIN",
    "ERROR_LESSON_JSON_END",
    "build_error_lesson_ai_form_prompt",
    "parse_error_lesson_ai_response",
    "save_ai_form_as_lesson",
    "import_error_memory_file",
    "import_error_memory_zip",
    "analyze_error_against_lessons",
]
