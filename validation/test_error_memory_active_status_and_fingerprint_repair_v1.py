"""Validation for Error Memory active-status and fingerprint repair v1."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.error_memory.intake import (  # noqa: E402
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    build_lesson_from_ai_form,
    parse_error_lesson_ai_response,
)
from kanda_reasoner_app.error_memory.fingerprint import extract_exception_info  # noqa: E402


def _wrapped(payload: dict[str, object]) -> str:
    return (
        ERROR_LESSON_JSON_BEGIN
        + "\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n"
        + ERROR_LESSON_JSON_END
    )


def test_failed_pre_correction_json_is_saved_as_draft() -> None:
    payload = {
        "status": "active",
        "raw_error_text": "Validation failed with KeyError for missing ml_pilot_activation_state.",
        "operation_phase": "validation",
        "symptom": "Validation failed with KeyError for missing ml_pilot_activation_state.",
        "root_cause": "A validation-visible GUI state key was expected, but the producer did not return it.",
        "correct_fix": "Update the GUI state producer and rerun validation to confirm the key is present.",
        "do_not_repeat_rule": "Do not add a validation-visible GUI key only to tests.",
        "prevention_triggers": ["KeyError", "ml_pilot_activation_state", "GUI state key"],
        "validation_evidence": ["Validation failed before correction with KeyError for missing ml_pilot_activation_state."],
        "notes": "This should be reviewed after the correction patch passes validation.",
    }
    form = parse_error_lesson_ai_response(_wrapped(payload))
    assert form["status"] == "draft", form
    with tempfile.TemporaryDirectory() as tmp:
        lesson = build_lesson_from_ai_form(selected_project_root=tmp, form_inputs=form)
    assert lesson["status"] == "draft"
    assert lesson["exception"]["type"] == "KeyError"
    assert lesson["exception"]["message_normalized"]
    assert "ml_pilot_activation_state" in lesson["exception"]["message_normalized"]
    assert lesson["fingerprint"]["components"][4]


def test_validated_correction_can_remain_active() -> None:
    payload = {
        "status": "active",
        "raw_error_text": "Validation failed with KeyError: ml_pilot_activation_state",
        "operation_phase": "validation",
        "symptom": "Validation failed with KeyError for missing ml_pilot_activation_state.",
        "root_cause": "The producer method did not expose the validation-visible key.",
        "correct_fix": "Updated the producer method to include ml_pilot_activation_state and added validation.",
        "do_not_repeat_rule": "Update producer, consumer, and validation together for GUI state keys.",
        "prevention_triggers": ["ml_pilot_activation_state", "GUI state key"],
        "validation_evidence": ["VALIDATION OK: error-memory-gui-state-key-repair", "STATUS: IN_SYNC"],
    }
    form = parse_error_lesson_ai_response(_wrapped(payload))
    assert form["status"] == "active", form
    with tempfile.TemporaryDirectory() as tmp:
        lesson = build_lesson_from_ai_form(selected_project_root=tmp, form_inputs=form)
    assert lesson["status"] == "active"


def test_plain_text_keyerror_has_useful_normalized_message() -> None:
    info = extract_exception_info(
        "Validation failed with KeyError for missing ml_pilot_activation_state.",
        operation_phase="validation",
    )
    assert info["type"] == "KeyError"
    assert info["message_normalized"]
    assert "ml_pilot_activation_state" in info["message_normalized"]


if __name__ == "__main__":
    test_failed_pre_correction_json_is_saved_as_draft()
    test_validated_correction_can_remain_active()
    test_plain_text_keyerror_has_useful_normalized_message()
    print("VALIDATION OK: error-memory-active-status-and-fingerprint-repair-v1")
    print("STATUS: IN_SYNC")
