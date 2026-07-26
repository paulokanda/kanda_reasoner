"""Validate Error Memory tab text payload extraction refactor v1."""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-text-payloads-refactor-v1"
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_text_payloads.py"
TEST = ROOT / "tests/test_error_memory_tab_text_payloads_public_contract.py"


def fail(message: str) -> None:
    raise SystemExit("VALIDATION FAIL: " + message)


def read_text(path: Path) -> str:
    if not path.exists():
        fail("Missing required file: " + path.as_posix())
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(label + " missing: " + needle)


def assert_not_contains(text: str, needle: str, label: str) -> None:
    if needle in text:
        fail(label + " must not contain: " + needle)


def assert_compiles() -> None:
    for path in (TARGET, HELPER, TEST):
        py_compile.compile(str(path), doraise=True)


def assert_helper_contract() -> None:
    text = read_text(HELPER)
    assert_contains(text, '"""Pure text and archive payload helpers for the Error Memory GUI tab."""', "helper docstring")
    assert_contains(text, "__all__ = [", "helper public surface")
    for name in [
        "archive_entry_text",
        "json_payload_from_text",
        "lesson_id_from_text_lenient",
        "operation_phase_from_editor_texts",
        "pending_file_updated_text",
        "summary_from_pending_raw_text",
        "text_has_formatted_lesson_payload",
        "validation_evidence_is_passing",
    ]:
        assert_contains(text, '"' + name + '"', "helper __all__")
        assert_contains(text, "def " + name + "(", "helper function")
    assert_not_contains(text, "from PySide6", "non-GUI helper")
    assert_not_contains(text, "import PySide6", "non-GUI helper")
    assert_not_contains(text, "error_memory_tab import", "dependency direction")


def assert_tab_contract() -> None:
    text = read_text(TARGET)
    assert_contains(text, "from kanda_reasoner_app.error_memory_gui._text_payloads import (", "target helper import")
    assert_contains(text, "return operation_phase_from_editor_texts(", "operation-phase delegation")
    assert_contains(text, "return pending_file_updated_text(pending_file)", "pending updated delegation")
    assert_contains(text, "return summary_from_pending_raw_text(text, pending_file)", "summary delegation")
    assert_contains(text, "return lesson_id_from_text_lenient(text)", "lesson-id delegation")
    assert_contains(text, "return text_has_formatted_lesson_payload(text)", "formatted payload delegation")
    assert_contains(text, "return json_payload_from_text(text)", "json payload delegation")
    assert_contains(text, "return archive_entry_text(archive, member_name)", "archive entry delegation")
    assert_contains(text, "return validation_evidence_is_passing(lesson)", "validation evidence delegation")
    assert_not_contains(text, "from datetime import datetime, timezone", "target datetime import")
    line_count = len(text.splitlines())
    if line_count >= 1873:
        fail("error_memory_tab.py line count did not decrease; found " + str(line_count))


def assert_test_contract() -> None:
    text = read_text(TEST)
    assert_contains(text, "from kanda_reasoner_app.error_memory_gui._text_payloads import (", "direct static helper import")
    assert_contains(text, "test_json_payload_from_wrapped_text_and_lesson_id", "wrapped payload characterization test")
    assert_contains(text, "test_archive_entry_text_rejects_unsafe_member", "archive safety characterization test")
    result = subprocess.run([sys.executable, str(TEST)], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        fail("helper characterization test failed:\n" + result.stdout + result.stderr)


def assert_helper_import_smoke() -> None:
    code = """
from kanda_reasoner_app.error_memory_gui._text_payloads import json_payload_from_text
assert json_payload_from_text('{\\"lesson_id\\": \\"x\\"}')['lesson_id'] == 'x'
"""
    result = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        fail("helper import smoke failed:\n" + result.stdout + result.stderr)


def main() -> int:
    assert_compiles()
    assert_helper_contract()
    assert_tab_contract()
    assert_test_contract()
    assert_helper_import_smoke()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
