"""Validate Error Memory pending-intake duplicate user-control behavior."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
FEATURE_ID = "error-memory-pending-duplicate-user-control-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def source_text() -> str:
    return TARGET.read_text(encoding="utf-8")


def test_source_compiles() -> None:
    compile(source_text(), str(TARGET), "exec")


def test_duplicate_warning_state_exists() -> None:
    text = source_text()
    require(
        "self._warned_duplicate_pending_intake_lesson_ids: set[str] = set()" in text,
        "duplicate warning session set is missing",
    )
    require(
        "def _show_duplicate_pending_intake_warning" in text,
        "duplicate pending-intake warning helper is missing",
    )
    require(
        "already exists in Lessons" in text,
        "warning does not explain that the lesson already exists in Lessons",
    )
    require(
        "Pending source kept for user control" in text,
        "warning does not tell the user that the pending source is kept",
    )


def test_duplicate_branch_warns_and_does_not_delete() -> None:
    text = source_text()
    duplicate_start = text.index("if lesson_id and self._lesson_id_exists_in_lessons(lesson_id):")
    branch_end = text.index("self._loaded_pending_intake_file = marker", duplicate_start)
    branch = text[duplicate_start:branch_end]
    require(
        "self._show_duplicate_pending_intake_warning(lesson_id, candidate)" in branch,
        "duplicate lesson branch does not show the user-facing warning",
    )
    require(
        "self._delete_pending_file_quietly(candidate)" not in branch,
        "duplicate lesson branch still deletes the pending source silently",
    )
    require(
        "self._dismissed_pending_intake_files.add(marker)" in branch,
        "duplicate lesson branch does not suppress repeat warning for this file in-session",
    )
    require(
        "self._dismissed_pending_intake_lesson_ids.add(lesson_id)" in branch,
        "duplicate lesson branch does not suppress repeat warning for this lesson id in-session",
    )


def test_loader_contract_mentions_user_control() -> None:
    text = source_text()
    require(
        "the loader must warn the user instead of silently" in text,
        "loader docstring does not document the duplicate user-control contract",
    )
    require(
        "Memorize Error remains" in text,
        "pending-intake loader no-save contract was removed",
    )


def test_no_new_payload_or_freeze_bypass() -> None:
    text = source_text()
    require("project_freeze_ledger" not in text, "Error Memory tab must not write project_freeze_ledger")
    require("Confirm and Write" not in text, "Error Memory tab patch must not change freeze Confirm and Write")
    require("save_lesson(self._current_project_root(), lesson)" in text, "Memorize Error save route was unexpectedly removed")


def main() -> int:
    test_source_compiles()
    test_duplicate_warning_state_exists()
    test_duplicate_branch_warns_and_does_not_delete()
    test_loader_contract_mentions_user_control()
    test_no_new_payload_or_freeze_bypass()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
