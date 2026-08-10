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
    parse_error_lesson_ai_response as _parse_error_lesson_ai_response,
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
