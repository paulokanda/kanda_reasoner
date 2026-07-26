# project-path: kanda_reasoner_app/error_memory/store.py
"""Canonical project-specific Error Memory lesson store."""

from __future__ import annotations


__all__ = [
    'bootstrap_error_memory_store',
    'delete_lesson',
    'list_lessons',
    'load_lesson',
    'rebuild_index',
    'save_lesson',
]
import json
from pathlib import Path
from typing import Any

from .paths import (
    ensure_error_memory_dirs,
    resolve_error_memory_index_path,
    resolve_error_memory_lessons_dir,
)
from .schema import validate_lesson_shape, write_schema_if_missing


def bootstrap_error_memory_store(selected_project_root: str | Path) -> dict[str, Any]:
    """Create the Error Memory folders, schema, and index when needed."""
    paths = ensure_error_memory_dirs(selected_project_root)
    schema_path = write_schema_if_missing(selected_project_root)
    index_path = resolve_error_memory_index_path(selected_project_root)
    if not index_path.exists():
        index_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "project_slug": Path(selected_project_root).name,
                    "lessons": [],
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
    return {"paths": {key: str(value) for key, value in paths.items()}, "schema": str(schema_path), "index": str(index_path)}


def _lesson_path(selected_project_root: str | Path, lesson_id: str) -> Path:
    """Support lesson path behavior.
    
    Parameters
    ----------
    selected_project_root : str | Path
        The selected project root value.
    lesson_id : str
        The lesson id value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    safe_id = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in str(lesson_id))
    if not safe_id.startswith("lesson-"):
        safe_id = "lesson-" + safe_id
    return resolve_error_memory_lessons_dir(selected_project_root) / (safe_id + ".json")


def load_lesson(selected_project_root: str | Path, lesson_id: str) -> dict[str, Any]:
    """Load one lesson JSON object."""
    path = _lesson_path(selected_project_root, lesson_id)
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("Lesson file is not a JSON object: " + str(path))
    return payload


def _index_record(lesson: dict[str, Any]) -> dict[str, Any]:
    """Support index record behavior.
    
    Parameters
    ----------
    lesson : dict[str, Any]
        The lesson value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    fingerprint = lesson.get("fingerprint", {}) if isinstance(lesson.get("fingerprint"), dict) else {}
    return {
        "lesson_id": lesson.get("lesson_id", ""),
        "status": lesson.get("status", ""),
        "symptom": lesson.get("symptom", ""),
        "do_not_repeat_rule": lesson.get("do_not_repeat_rule", ""),
        "updated_at_utc": lesson.get("updated_at_utc", ""),
        "fingerprint_hash": fingerprint.get("fingerprint_hash", ""),
    }


def rebuild_index(selected_project_root: str | Path) -> dict[str, Any]:
    """Rebuild and write the lightweight index from lesson files."""
    bootstrap_error_memory_store(selected_project_root)
    lessons: list[dict[str, Any]] = []
    for path in sorted(resolve_error_memory_lessons_dir(selected_project_root).glob("lesson-*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
            if isinstance(payload, dict):
                ok, _failures = validate_lesson_shape(payload)
                if ok:
                    lessons.append(_index_record(payload))
        except Exception:
            continue
    index = {
        "schema_version": "1.0",
        "project_slug": Path(selected_project_root).name,
        "lessons": lessons,
    }
    resolve_error_memory_index_path(selected_project_root).write_text(
        json.dumps(index, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return index


def save_lesson(selected_project_root: str | Path, lesson: dict[str, Any]) -> Path:
    """Validate and save one canonical lesson JSON file."""
    bootstrap_error_memory_store(selected_project_root)
    ok, failures = validate_lesson_shape(lesson)
    if not ok:
        raise ValueError("Invalid Error Memory lesson: " + "; ".join(failures))
    path = _lesson_path(selected_project_root, str(lesson.get("lesson_id", "")))
    path.write_text(json.dumps(lesson, indent=2, sort_keys=True), encoding="utf-8")
    rebuild_index(selected_project_root)
    return path


def delete_lesson(selected_project_root: str | Path, lesson_id: str) -> dict[str, Any]:
    """Delete one canonical lesson file and rebuild the index.

    The deleted lesson object is returned so the GUI can offer a one-click undo
    without asking users to run manual PowerShell cleanup commands.
    """
    bootstrap_error_memory_store(selected_project_root)
    payload = load_lesson(selected_project_root, lesson_id)
    path = _lesson_path(selected_project_root, lesson_id)
    if path.exists():
        path.unlink()
    rebuild_index(selected_project_root)
    return payload


def list_lessons(selected_project_root: str | Path, *, include_inactive: bool = True) -> list[dict[str, Any]]:
    """Return full lesson objects from the canonical store."""
    bootstrap_error_memory_store(selected_project_root)
    result: list[dict[str, Any]] = []
    for path in sorted(resolve_error_memory_lessons_dir(selected_project_root).glob("lesson-*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        if not include_inactive and payload.get("status") != "active":
            continue
        result.append(payload)
    return result
