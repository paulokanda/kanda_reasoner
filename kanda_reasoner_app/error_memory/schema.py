# project-path: kanda_reasoner_app/error_memory/schema.py
"""Lightweight schema helpers for owner-scoped Error Memory lessons."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .backend import ErrorMemoryBackend, OWNER_METADATA_FIELDS
from .models import active_ready_missing_reasons
from .paths import resolve_lesson_schema_path

LESSON_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "KANDA Error Memory Lesson",
    "type": "object",
    "required": [
        "schema_version",
        "lesson_id",
        "status",
        "project_slug",
        "operation_phase",
        "created_at_utc",
        "updated_at_utc",
        "raw_error_text",
        "raw_error_snapshot_scrubbed",
        "symptom",
        "root_cause",
        "wrong_assumption",
        "correct_fix",
        "long_term_prevention",
        "do_not_repeat_rule",
        "prevention_triggers",
        "exception",
        "fingerprint",
        "regression_check",
        "validation_evidence",
        "redaction",
    ],
    "properties": {
        "schema_version": {"const": "1.0"},
        "lesson_id": {"type": "string"},
        "status": {
            "enum": ["draft", "active", "deprecated", "superseded"]
        },
        "owner_scope": {"enum": ["TOOL", "PROJECT"]},
        "owner_id": {"type": "string"},
        "owner_slug": {"type": "string"},
        "owner_root_fingerprint": {"type": "string"},
        "affected_box": {"type": "string"},
    },
}


def write_schema_if_missing(
    target: ErrorMemoryBackend | str | Path,
) -> Path:
    """Write the local JSON schema file when missing."""
    path = resolve_lesson_schema_path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            json.dumps(LESSON_SCHEMA, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return path


def validate_owner_metadata_shape(
    lesson: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Validate owner metadata only when any canonical owner field is present."""
    present = [key for key in OWNER_METADATA_FIELDS if key in lesson]
    if not present:
        return True, []
    failures: list[str] = []
    missing = [key for key in OWNER_METADATA_FIELDS if not str(lesson.get(key) or "").strip()]
    failures.extend("owner metadata missing: " + key for key in missing)
    if str(lesson.get("owner_scope") or "") not in {"TOOL", "PROJECT"}:
        failures.append("owner_scope is invalid")
    return not failures, failures


def validate_lesson_shape(lesson: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return a simple dependency-free validation result."""
    failures: list[str] = []
    for key in LESSON_SCHEMA["required"]:
        if key not in lesson:
            failures.append("missing key: " + key)
    if str(lesson.get("schema_version", "")) != "1.0":
        failures.append("schema_version must be 1.0")
    if str(lesson.get("status", "")) not in {
        "draft",
        "active",
        "deprecated",
        "superseded",
    }:
        failures.append("status is invalid")
    if not isinstance(lesson.get("prevention_triggers", []), list):
        failures.append("prevention_triggers must be a list")
    if not isinstance(lesson.get("exception", {}), dict):
        failures.append("exception must be an object")
    if not isinstance(lesson.get("fingerprint", {}), dict):
        failures.append("fingerprint must be an object")
    if not isinstance(lesson.get("regression_check", {}), dict):
        failures.append("regression_check must be an object")
    if not isinstance(lesson.get("redaction", {}), dict):
        failures.append("redaction must be an object")
    owner_ok, owner_failures = validate_owner_metadata_shape(lesson)
    if not owner_ok:
        failures.extend(owner_failures)
    if str(lesson.get("status", "")).strip().lower() == "active":
        failures.extend(
            reason
            for reason in active_ready_missing_reasons(lesson)
            if reason not in failures
        )
    return not failures, failures
