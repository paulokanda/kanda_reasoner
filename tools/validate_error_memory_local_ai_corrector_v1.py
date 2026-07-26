# project-path: tools/validate_error_memory_local_ai_corrector_v1.py
"""Focused validation for the Error Memory local AI corrector patch."""

from __future__ import annotations

import ast
import importlib
import json
import py_compile
import sys
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

TOUCHED_FILES = [
    "kanda_reasoner_app/reasoner_engine/local_ai_chat_service.py",
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_ai_corrector_service.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_window_sync.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/error_memory_header_ai.py",
]


class FakeRegistry:
    """Small fake local model registry for resolver tests."""

    def list_models(self) -> list[str]:
        """Return deterministic fake models."""
        return ["qwen3-coder:30b", "qwen2.5-coder:7b"]


class FakeEdit:
    """Small text widget test double."""

    def __init__(self) -> None:
        """Create an empty fake text widget."""
        self.text = ""

    def setPlainText(self, value: str) -> None:
        """Store the text assigned by sync helpers."""
        self.text = str(value)

    def clear(self) -> None:
        """Clear the stored text."""
        self.text = ""


class FakeTab:
    """Minimal Error Memory tab test double."""

    def __init__(self) -> None:
        """Create fake tab state."""
        self.raw_error_edit = FakeEdit()
        self.received_preview_edit = FakeEdit()
        self._last_received_lesson: dict[str, Any] | None = None
        self._selected_lesson_id = ""
        self._loaded_pending_intake_file = "pending.json"
        self._loaded_pending_intake_lesson_id = "lesson-old-v1"
        self.refreshed = False

    def _refresh_heuristic_correction_button_state(self) -> None:
        """Record that refresh was requested."""
        self.refreshed = True


def _assert(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear message when condition is false."""
    if not condition:
        raise AssertionError(message)


def _line_count(path: Path) -> int:
    """Return physical line count for a source file."""
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def _sample_lesson(status: str = "draft") -> dict[str, Any]:
    """Return a valid-enough lesson for parser and sync tests."""
    return {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": "lesson-local-ai-corrector-test-v1",
        "status": status,
        "superseded_by": "",
        "operation_phase": "validation",
        "created_at_utc": "2026-07-01T00:00:00Z",
        "updated_at_utc": "2026-07-01T00:00:00Z",
        "source_patch_zip": "kanda_test_patch.zip",
        "raw_error_text": "INSTALL ERROR: sample",
        "raw_error_snapshot_scrubbed": "Sample scrubbed snapshot.",
        "symptom": "Sample symptom.",
        "root_cause": "Sample root cause.",
        "wrong_assumption": "Sample wrong assumption.",
        "correct_fix": "Sample correct fix.",
        "do_not_repeat_rule": "Sample do not repeat rule.",
        "long_term_prevention": "Sample prevention.",
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets included."],
        },
        "exception": {
            "type": "SampleError",
            "phase": "validation",
            "relative_file_path": "tools/sample.py",
            "function_or_test_name": "sample_test",
            "message_normalized": "sample",
            "stacktrace_scrubbed": "No traceback.",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["SampleError", "sample"],
            "fingerprint_hash": "local_ai_corrector_test_v1",
        },
        "prevention_triggers": ["sample trigger"],
        "regression_check": {
            "type": "validation_command",
            "command": "python tools/validate_sample.py",
            "expected_marker": "VALIDATION OK: sample",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run focused validation.",
        "validation_evidence": ["Observed sample validation evidence."],
        "install_command_summary": "Install sample patch.",
        "notes": "Sample notes.",
    }


def _validate_module_hygiene() -> None:
    """Validate touched files compile and remain within the line-count gate."""
    for relative in TOUCHED_FILES:
        path = PROJECT_ROOT / relative
        _assert(path.exists(), "missing touched file: " + relative)
        count = _line_count(path)
        _assert(count <= 500, relative + " exceeds 500 lines")
        py_compile.compile(str(path), doraise=True)
        ast.parse(path.read_text(encoding="utf-8", errors="replace"))


def _validate_model_resolution() -> None:
    """Validate model selection resolves through the shared registry path."""
    service = importlib.import_module("kanda_reasoner_app.reasoner_engine.local_ai_chat_service")
    auto = service.resolve_local_ai_model(service.AUTO_LOCAL_AI_MODEL_LABEL, FakeRegistry())
    explicit = service.resolve_local_ai_model("qwen2.5-coder:7b", FakeRegistry())
    fallback = service.resolve_local_ai_model("missing-model", FakeRegistry())
    _assert(auto == "qwen3-coder:30b", "auto model did not resolve to first model")
    _assert(explicit == "qwen2.5-coder:7b", "explicit model did not resolve")
    _assert(fallback == "qwen3-coder:30b", "missing model did not fall back safely")


def _validate_prompt_builder() -> None:
    """Validate prompt construction contains the Error Memory contract."""
    builder = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_prompt_builder")
    messages = builder.build_error_memory_correction_messages(
        intake_text="INSTALL ERROR: Traceback",
        editor_text="{}",
        project_root="E:/kanda_reasoner",
    )
    text = "\n".join(message["content"] for message in messages)
    for marker in [
        "KANDA_ERROR_LESSON_JSON_BEGIN",
        "KANDA_ERROR_LESSON_JSON_END",
        "Do not invent validation evidence",
        "Set status to draft unless successful validation evidence is explicit",
        "INSTALL ERROR: Traceback",
    ]:
        _assert(marker in text, "prompt missing marker: " + marker)


def _validate_response_parser() -> None:
    """Validate strict marker parsing and baseline lesson checks."""
    validator = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_response_validator")
    lesson = _sample_lesson()
    block = validator.format_lesson_block(lesson)
    parsed = validator.parse_one_lesson_block(block)
    _assert(parsed.lesson["lesson_id"] == lesson["lesson_id"], "valid lesson did not parse")
    for bad in [
        json.dumps(lesson),
        "prefix\n" + block,
        block + "\n" + block,
    ]:
        try:
            validator.parse_one_lesson_block(bad)
        except validator.AIResponseValidationError:
            pass
        else:
            raise AssertionError("invalid response was accepted")
    missing = dict(lesson)
    missing.pop("lesson_id")
    try:
        validator.parse_one_lesson_block(validator.format_lesson_block(missing))
    except validator.AIResponseValidationError as exc:
        _assert("lesson_id" in str(exc), "missing field error was not specific")
    else:
        raise AssertionError("missing lesson_id was accepted")


def _validate_window_sync() -> None:
    """Validate corrected lessons populate both work windows without consuming pending."""
    validator = importlib.import_module("kanda_reasoner_app.error_memory_gui._ai_response_validator")
    sync = importlib.import_module("kanda_reasoner_app.error_memory_gui._window_sync")
    tab = FakeTab()
    lesson = _sample_lesson()
    block = validator.parse_one_lesson_block(validator.format_lesson_block(lesson))
    sync.apply_corrected_lesson_to_work_windows(tab, block)
    _assert(tab.raw_error_edit.text == block.formatted_text, "intake window not updated")
    _assert(json.loads(tab.received_preview_edit.text)["lesson_id"] == lesson["lesson_id"], "editor not updated")
    _assert(tab._loaded_pending_intake_file == "pending.json", "pending file was consumed")
    _assert(tab._loaded_pending_intake_lesson_id == "lesson-old-v1", "pending id was changed")
    _assert(tab._selected_lesson_id == lesson["lesson_id"], "selected lesson id not updated")
    _assert(tab.refreshed, "heuristic refresh was not called")


def _validate_header_delegates_to_corrector() -> None:
    """Validate the header helper delegates to the correction action module."""
    path = PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_gui_shell/error_memory_header_ai.py"
    text = path.read_text(encoding="utf-8", errors="replace")
    _assert("run_error_memory_ai_correction_from_header" in text, "header does not delegate")
    _assert("_copy_error_lesson_intake_blueprint_to_clipboard" not in text, "header still copies blueprint")


def main() -> int:
    """Run focused validation."""
    _validate_module_hygiene()
    _validate_model_resolution()
    _validate_prompt_builder()
    _validate_response_parser()
    _validate_window_sync()
    _validate_header_delegates_to_corrector()
    print("VALIDATION OK: error-memory-local-ai-corrector-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
