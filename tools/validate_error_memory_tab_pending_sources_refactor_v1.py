"""Validate Error Memory tab pending sources refactor v1."""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-pending-sources-refactor-v1"
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
TEXT_HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_text_payloads.py"
PENDING_HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_pending_sources.py"
TEST = ROOT / "tests/test_error_memory_tab_pending_sources_public_contract.py"


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
    for path in (TARGET, TEXT_HELPER, PENDING_HELPER, TEST):
        py_compile.compile(str(path), doraise=True)


def assert_helper_contract() -> None:
    text = read_text(PENDING_HELPER)
    assert_contains(text, '"""Pending source path and deletion helpers for the Error Memory GUI tab."""', "helper docstring")
    assert_contains(text, "__all__ = [", "helper public surface")
    for name in [
        "candidate_pending_ai_assisted_intake_dirs",
        "delete_matching_pending_intake_files",
        "pending_file_matches_draft_identity",
        "pending_intake_dirs_for_root_hint",
        "pending_intake_files_for_candidate_dirs",
        "safe_pending_lesson_id_from_file",
    ]:
        assert_contains(text, '"' + name + '"', "helper __all__")
        assert_contains(text, "def " + name + "(", "helper function")
    assert_not_contains(text, "from PySide6", "non-GUI helper")
    assert_not_contains(text, "import PySide6", "non-GUI helper")
    assert_not_contains(text, "error_memory_tab import", "dependency direction")


def assert_tab_contract() -> None:
    text = read_text(TARGET)
    assert_contains(text, "from kanda_reasoner_app.error_memory_gui._pending_sources import (", "target helper import")
    assert_contains(text, "return pending_intake_dirs_for_root_hint(", "pending dir delegation")
    assert_contains(text, "return candidate_pending_ai_assisted_intake_dirs(", "candidate dir delegation")
    assert_contains(text, "return safe_pending_lesson_id_from_file(pending_file)", "safe id delegation")
    assert_contains(text, "return pending_intake_files_for_candidate_dirs(", "file listing delegation")
    assert_contains(text, "return pending_file_matches_draft_identity(path, lesson_ids, visible_texts, explicit_paths)", "identity delegation")
    assert_contains(text, "deleted_count, failures, dismissed_markers = delete_matching_pending_intake_files(", "delete delegation")
    assert_contains(text, "self._dismissed_pending_intake_files.update(dismissed_markers)", "dismissed marker update")
    assert_contains(text, "class ErrorMemoryTab(QWidget):", "ErrorMemoryTab facade preserved")
    assert_contains(text, "'ErrorMemoryTab',", "public __all__ preserved")
    if len(text.splitlines()) >= 1846:
        fail("error_memory_tab.py line count did not decrease from cluster 1; found " + str(len(text.splitlines())))


def assert_test_contract() -> None:
    text = read_text(TEST)
    assert_contains(text, "from kanda_reasoner_app.error_memory_gui._pending_sources import (", "direct helper import")
    assert_contains(text, "test_delete_matching_pending_files_returns_dismissed_markers", "delete behavior test")
    result = subprocess.run([sys.executable, str(TEST)], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        fail("pending source helper test failed:\n" + result.stdout + result.stderr)


def assert_import_smoke() -> None:
    code = """
from kanda_reasoner_app.error_memory_gui._pending_sources import safe_pending_lesson_id_from_file
from pathlib import Path
assert safe_pending_lesson_id_from_file(Path('RAW_ERROR_EVIDENCE_X.txt')) == 'lesson-pending-x'
"""
    result = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        fail("helper import smoke failed:\n" + result.stdout + result.stderr)


def main() -> int:
    assert_compiles()
    assert_helper_contract()
    assert_tab_contract()
    assert_test_contract()
    assert_import_smoke()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
