"""Validate startup Project Ready Check after second_prompt_files upload."""

from __future__ import annotations

import py_compile
from pathlib import Path

SOURCE_PATH = Path("kanda_prompt_workspace") / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
PROJECT_WAIT_ACTION = "Waiting for all files (Project Files) from second_prompt_files folder"
READY_ACTION = "WAIT_FOR_TASK"
PROJECT_READY = "PROJECT READY CHECK"


def _read_source() -> str:
    if not SOURCE_PATH.is_file():
        raise AssertionError("Missing source file: " + str(SOURCE_PATH))
    return SOURCE_PATH.read_text(encoding="utf-8", errors="replace")


def _assert_contains(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError("Expected source to contain: " + needle)


def _assert_not_contains(text: str, needle: str) -> None:
    if needle in text:
        raise AssertionError("Unexpected stale source text: " + needle)


def main() -> int:
    py_compile.compile(str(SOURCE_PATH), doraise=True)
    text = _read_source()

    _assert_contains(text, 'FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION = "' + PROJECT_WAIT_ACTION + '"')
    _assert_contains(text, 'SECOND_UPLOAD_READY_ACTION = "' + READY_ACTION + '"')
    _assert_contains(text, 'PROJECT_READY_CHECK_TITLE = "' + PROJECT_READY + '"')
    _assert_contains(text, "Next action:\n{FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION} or REQUEST_MISSING_FILES")
    _assert_contains(text, "Next action:\n" + PROJECT_WAIT_ACTION + "\n```")
    _assert_contains(text, "return `{PROJECT_READY_CHECK_TITLE}`")
    _assert_contains(text, "Project slug:")
    _assert_contains(text, "Active project root:")
    _assert_contains(text, "KANDA tool root:")
    _assert_contains(text, "Same physical root: YES / NO")
    _assert_contains(text, "Compact Error Memory loaded:")
    _assert_contains(text, "Second-upload handoff loaded:")
    _assert_contains(text, "Tier-1 gates active:")
    _assert_contains(text, "Only after `{PROJECT_READY_CHECK_TITLE}` ends")
    _assert_contains(text, "kanda_reasoner` can be both the active project and the KANDA tool")
    _assert_contains(text, "Compact Error Memory files when present")
    _assert_contains(text, "<project_slug>__png_assets_partXX_of_YY.zip")

    _assert_not_contains(text, "PROJECT FILES LOAD CHECK")
    _assert_not_contains(text, "project-files load check")
    _assert_not_contains(text, "After STARTUP PACK LOAD CHECK is COMPLETE and Next action is WAIT_FOR_TASK")
    _assert_not_contains(text, "Only after `COMPLETE / WAIT_FOR_TASK`, send the real task")

    print("VALIDATION OK: kanda-startup-project-ready-check-v1")
    print("PROJECT READY CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
