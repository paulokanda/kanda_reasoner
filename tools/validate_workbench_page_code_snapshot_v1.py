"""Validate the read-only Workbench Page Code aggregation contract."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

__all__ = [
    "main",
]


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_page_code_snapshot import (
    build_workbench_page_code_text,
)


FEATURE_ID = "large-file-refactor-workbench-page-code-snapshot-v1"
WORKBENCH_GUI = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner" / "workbench_gui.py"
PAGE_GUI = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner" / "workbench_page_code_gui.py"
PAGE_SNAPSHOT = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner" / "workbench_page_code_snapshot.py"
TUTORIAL = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner" / "LARGE_FILE_REFACTOR_WORKBENCH_TUTORIAL.md"


class _FakeText:
    def __init__(self, text: str) -> None:
        self._text = text

    def toPlainText(self) -> str:
        return self._text


class _FakeRoot:
    def text(self) -> str:
        return r"E:\kanda_reasoner"


class _FakeWindow:
    pass


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _build_fixture() -> tuple[_FakeWindow, list[str]]:
    window = _FakeWindow()
    window._root_path_edit = _FakeRoot()
    window._large_file_refactor_workbench_state = "DEPENDENCY_READY"
    attributes = (
        "_large_file_refactor_workbench_intake_output",
        "_large_file_refactor_workbench_dependency_output",
        "_large_file_refactor_workbench_real_preview_output",
        "_large_file_refactor_workbench_validation_output",
        "_large_file_refactor_workbench_aqr_progress_output",
        "_large_file_refactor_workbench_aqr_output",
        "_large_file_refactor_workbench_preflight_output",
        "_large_file_refactor_workbench_source_payload_output",
        "_large_file_refactor_workbench_completion_status_output",
        "_large_file_refactor_workbench_semantic_diff_output",
        "_large_file_refactor_workbench_text_diff_output",
        "_large_file_refactor_workbench_diff_review_status_output",
        "_large_file_refactor_workbench_ai_exchange_output",
        "_large_file_refactor_workbench_transaction_summary_output",
        "_large_file_refactor_workbench_refactor_gate_output",
    )
    tokens = []
    for index, attribute in enumerate(attributes, start=1):
        token = "PAGE_CODE_TEXT_WINDOW_TOKEN_%02d" % index
        setattr(window, attribute, _FakeText(token))
        tokens.append(token)
    return window, tokens


def main() -> None:
    workbench_source = WORKBENCH_GUI.read_text(encoding="utf-8")
    page_gui_source = PAGE_GUI.read_text(encoding="utf-8")
    page_snapshot_source = PAGE_SNAPSHOT.read_text(encoding="utf-8")
    tutorial_source = TUTORIAL.read_text(encoding="utf-8")

    for path in (WORKBENCH_GUI, PAGE_GUI, PAGE_SNAPSHOT):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    _assert('QPushButton("Get Page Code")' in page_gui_source, "Get Page Code button missing")
    _assert("build_workbench_page_code_button(window)" in workbench_source, "Top-level button wiring missing")
    button_pos = workbench_source.index("layout.addWidget(build_workbench_page_code_button(window))")
    scroll_pos = workbench_source.index("scroll_area, content, content_layout = build_scrollable_workbench_content()")
    intake_pos = workbench_source.index("content_layout.addWidget(_build_intake_section(window))")
    _assert(button_pos < scroll_pos < intake_pos, "Get Page Code must be outside and above the numbered stage containers")
    print("WORKBENCH_PAGE_CODE_BUTTON_OUTSIDE_ABOVE_STAGE_ONE: PASS")

    window, tokens = _build_fixture()
    snapshot = build_workbench_page_code_text(window)
    for stage in range(1, 8):
        _assert((str(stage) + ". ") in snapshot, "Missing stage heading: %d" % stage)
    _assert(snapshot.count("Origin: ") == 7, "Every numbered stage must explain its origin")
    for token in tokens:
        _assert(token in snapshot, "Missing text window content: " + token)
    print("WORKBENCH_PAGE_CODE_ALL_SEVEN_STAGES_WITH_ORIGINS: PASS")
    print("WORKBENCH_PAGE_CODE_ALL_CURRENT_TEXT_WINDOWS_INCLUDED: PASS")

    _assert("read-only aggregation" in snapshot, "Read-only snapshot declaration missing")
    _assert("does not execute stages" in snapshot, "No-side-effect declaration missing")
    _assert("E:\\kanda_reasoner" in snapshot, "Active project root missing")
    _assert("DEPENDENCY_READY" in snapshot, "Workbench state missing")
    print("WORKBENCH_PAGE_CODE_READ_ONLY_NO_GATE_MUTATION_CONTRACT: PASS")

    _assert("QDialog(window)" in page_gui_source, "Page Code dialog must be window-owned")
    _assert("output.setReadOnly(True)" in page_gui_source, "Page Code output must be read-only")
    _assert("build_workbench_page_code_text(window)" in page_gui_source, "Dialog must snapshot current page state at open time")
    print("WORKBENCH_PAGE_CODE_READ_ONLY_DIALOG_CONTRACT: PASS")

    _assert("Get Page Code" in tutorial_source, "Tutorial must document Get Page Code")
    _assert("Origin:" in tutorial_source, "Tutorial must explain origin annotations")
    print("WORKBENCH_PAGE_CODE_TUTORIAL_SYNC: PASS")

    for path in (WORKBENCH_GUI, PAGE_GUI, PAGE_SNAPSHOT):
        count = _line_count(path)
        _assert(101 <= count <= 499 or path == PAGE_GUI, "Touched source module size outside policy: %s=%d" % (path.name, count))
    _assert(_line_count(PAGE_GUI) <= 500, "Page Code GUI module exceeds maximum")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")

    for path in (WORKBENCH_GUI, PAGE_GUI, PAGE_SNAPSHOT):
        data = path.read_bytes()
        _assert(not data.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM not allowed: " + path.name)
        data.decode("ascii")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")

    print("WORKBENCH_PAGE_CODE_SNAPSHOT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
