"""AI-formulary intake helpers for Error Memory lessons.

This module intentionally mirrors the Freeze Feature After Update workflow:
the GUI can copy a raw error or draft to an AI specialist, then paste or import
one formatted JSON object back into the Error Editor before Memorize Error saves it.
"""

from __future__ import annotations

from .intake_ai_form_prompt import build_error_lesson_ai_form_prompt as _build_error_lesson_ai_form_prompt
from .intake_form_builder import (
    build_lesson_from_ai_form as _build_lesson_from_ai_form,
    save_ai_form_as_lesson as _save_ai_form_as_lesson,
)
from .intake_json_parser import (
    _candidate_blocks,
    _escape_raw_control_chars_inside_strings,
    _extract_balanced_json_objects,
    _json_load_attempts,
    _normalize_ai_text,
    _payload_score,
    _remove_trailing_commas,
    _strip_markdown_fences,
    parse_error_lesson_ai_response as _parse_error_lesson_ai_response,
)
from .intake_normalization import (
    ALLOWED_ERROR_LESSON_FORM_KEYS,
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    _REQUIRED_ACTIVE_AI_KEYS,
    _UNCERTAIN_FIX_MARKERS,
    _VALIDATION_FAILURE_MARKERS,
    _VALIDATION_SUCCESS_MARKERS,
    _as_list,
    _as_text,
    _coerce_status_for_ai_form,
    _contains_any_marker,
    _downgrade_non_active_ready_lesson,
    _has_successful_validation_evidence,
    _normalize_redaction_for_error_memory_json,
    _normalize_regression_check_for_error_memory_json,
    _should_force_draft_status,
)
from .intake_plain_text import (
    _infer_phase_from_plain_text,
    _label_key,
    _plain_text_to_form,
    _plain_text_triggers,
    _strip_list_marker,
)

build_error_lesson_ai_form_prompt = _build_error_lesson_ai_form_prompt
build_lesson_from_ai_form = _build_lesson_from_ai_form
parse_error_lesson_ai_response = _parse_error_lesson_ai_response
save_ai_form_as_lesson = _save_ai_form_as_lesson

__all__ = [
    "build_error_lesson_ai_form_prompt",
    "build_lesson_from_ai_form",
    "parse_error_lesson_ai_response",
    "save_ai_form_as_lesson",
]
