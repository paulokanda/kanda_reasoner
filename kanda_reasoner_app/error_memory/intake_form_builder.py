"""Build and save canonical Error Memory lessons from AI intake forms."""

from __future__ import annotations

__all__: list[str] = []


from pathlib import Path
from typing import Any, Mapping

from .intake_normalization import (
    _as_list,
    _as_text,
    _coerce_status_for_ai_form,
    _downgrade_non_active_ready_lesson,
    _normalize_redaction_for_error_memory_json,
    _normalize_regression_check_for_error_memory_json,
)
from .models import active_ready, build_lesson
from .store import save_lesson


def build_lesson_from_ai_form(
    *,
    selected_project_root: str | Path,
    form_inputs: Mapping[str, Any],
    fallback_raw_error_text: str = "",
    fallback_operation_phase: str = "unknown",
) -> dict[str, Any]:
    """Convert parsed AI form inputs into a canonical Error Memory lesson."""
    raw_error_text = _as_text(form_inputs.get("raw_error_text")) or fallback_raw_error_text
    operation_phase = _as_text(form_inputs.get("operation_phase")) or fallback_operation_phase
    existing_metadata = {
        "created_at_utc": _as_text(form_inputs.get("created_at_utc")),
        "source_patch_zip": _as_text(form_inputs.get("source_patch_zip")),
        "install_command_summary": _as_text(form_inputs.get("install_command_summary")),
        "validation_command_summary": _as_text(form_inputs.get("validation_command_summary")),
        "notes": _as_text(form_inputs.get("notes")),
    }
    lesson = build_lesson(
        selected_project_root=selected_project_root,
        raw_error_text=raw_error_text,
        operation_phase=operation_phase,
        symptom=_as_text(form_inputs.get("symptom")),
        root_cause=_as_text(form_inputs.get("root_cause")),
        wrong_assumption=_as_text(form_inputs.get("wrong_assumption")),
        correct_fix=_as_text(form_inputs.get("correct_fix")),
        long_term_prevention=_as_text(form_inputs.get("long_term_prevention")),
        do_not_repeat_rule=_as_text(form_inputs.get("do_not_repeat_rule")),
        prevention_triggers=_as_list(form_inputs.get("prevention_triggers")),
        validation_evidence=_as_list(form_inputs.get("validation_evidence")),
        regression_check=_normalize_regression_check_for_error_memory_json(form_inputs.get("regression_check")),
        status=_coerce_status_for_ai_form(form_inputs, _as_text(form_inputs.get("status")) or "active"),
        lesson_id=_as_text(form_inputs.get("lesson_id")) or None,
        existing={key: value for key, value in existing_metadata.items() if value},
    )
    for key in (
        "source_patch_zip",
        "install_command_summary",
        "validation_command_summary",
        "notes",
        "raw_error_snapshot_scrubbed",
    ):
        value = _as_text(form_inputs.get(key))
        if value:
            lesson[key] = value
    for key in ("exception", "fingerprint"):
        value = form_inputs.get(key)
        if isinstance(value, dict) and value:
            lesson[key] = dict(value)
    normalized_redaction = _normalize_redaction_for_error_memory_json(form_inputs.get("redaction"))
    if normalized_redaction:
        lesson["redaction"] = normalized_redaction
    if _as_text(form_inputs.get("updated_at_utc")):
        lesson["updated_at_utc"] = _as_text(form_inputs.get("updated_at_utc"))
    if _as_text(form_inputs.get("project_slug")):
        lesson["project_slug"] = _as_text(form_inputs.get("project_slug"))
    if _coerce_status_for_ai_form(form_inputs, _as_text(form_inputs.get("status")) or "active") == "active" and active_ready(lesson):
        lesson["status"] = "active"
    _downgrade_non_active_ready_lesson(lesson)
    return lesson


def save_ai_form_as_lesson(
    *,
    selected_project_root: str | Path,
    form_inputs: Mapping[str, Any],
    fallback_raw_error_text: str = "",
    fallback_operation_phase: str = "unknown",
) -> tuple[Path, dict[str, Any]]:
    """Build and save an AI-provided Error Memory lesson form."""
    lesson = build_lesson_from_ai_form(
        selected_project_root=selected_project_root,
        form_inputs=form_inputs,
        fallback_raw_error_text=fallback_raw_error_text,
        fallback_operation_phase=fallback_operation_phase,
    )
    path = save_lesson(selected_project_root, lesson)
    return path, lesson
