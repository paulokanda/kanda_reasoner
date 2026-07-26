"""Validate Error Memory tab pending row helper extraction."""
from __future__ import annotations

import ast
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-pending-rows-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_pending_rows.py"
TEST = ROOT / "tests/test_error_memory_tab_pending_rows_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._pending_rows import (",
    "draft_lesson_from_pending_raw_text,",
    "pending_lesson_rows_for_table,",
    "def _draft_lesson_from_pending_raw_text(self, pending_file: Path, raw_text: str) -> dict[str, Any]:",
    "return draft_lesson_from_pending_raw_text(",
    "project_slug=self._current_project_root().name",
    "def _pending_lesson_rows_for_table(self) -> list[dict[str, str]]:",
    "existing_lesson_ids = {",
    "return pending_lesson_rows_for_table(",
    "is_formatted_lesson_payload=self._text_is_formatted_error_lesson_payload",
    "lesson_from_formatted_text=self._lesson_from_formatted_text",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "def draft_lesson_from_pending_raw_text(",
    "def pending_lesson_rows_for_table(",
    "def _normalized_dismissed_markers",
    "pending_duplicate",
    "Pending malformed formatted lesson",
    "Raw pending evidence waiting for edition",
]


def _fail(message: str) -> None:
    raise SystemExit("VALIDATION FAIL: " + message)


def _read(path: Path) -> str:
    if not path.exists():
        _fail("missing file: " + str(path))
    return path.read_text(encoding="utf-8")


def _assert_no_upward_or_gui_imports(source: str) -> None:
    forbidden = ["PySide", "QtCore", "QtGui", "QtWidgets", "error_memory_tab", "ErrorMemoryTab"]
    for token in forbidden:
        if token in source:
            _fail("_pending_rows.py contains forbidden dependency token: " + token)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = ""
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
            for alias in getattr(node, "names", []):
                module = module + " " + alias.name
            if "PySide" in module or "error_memory_tab" in module:
                _fail("_pending_rows.py imports forbidden module: " + module)


def main() -> None:
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_pending_rows.py missing snippet: " + snippet)
    _assert_no_upward_or_gui_imports(helper_text)
    if "row = {\n                'kind': 'pending_edit'" in tab_text:
        _fail("error_memory_tab.py still owns old pending row assembly block")
    if "summary = self._summary_from_pending_raw_text(raw_text, pending_file)" in tab_text:
        _fail("error_memory_tab.py still owns old pending raw draft assembly")
    if len(tab_text.splitlines()) >= 1594:
        _fail("error_memory_tab.py did not shrink below cluster 6 line count")
    for path in [TAB, HELPER, TEST]:
        py_compile.compile(str(path), doraise=True)
    sys.path.insert(0, str(ROOT))
    import json
    import tempfile

    from kanda_reasoner_app.error_memory.intake import (
        ERROR_LESSON_JSON_BEGIN,
        ERROR_LESSON_JSON_END,
    )
    from kanda_reasoner_app.error_memory_gui import _pending_rows

    def is_formatted(value: str) -> bool:
        return ERROR_LESSON_JSON_BEGIN in value and ERROR_LESSON_JSON_END in value

    def lesson_from_formatted(value: str) -> dict[str, object]:
        inner = value.split(ERROR_LESSON_JSON_BEGIN, 1)[1].split(ERROR_LESSON_JSON_END, 1)[0]
        return json.loads(inner)

    def formatted(lesson_id: str) -> str:
        payload = {
            "lesson_id": lesson_id,
            "status": "active",
            "symptom": "Formatted pending symptom",
            "do_not_repeat_rule": "Keep formatted pending behavior.",
        }
        return ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps(payload) + "\n" + ERROR_LESSON_JSON_END

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        raw = temp / "raw.txt"
        new = temp / "formatted.json"
        dupe = temp / "duplicate.json"
        raw.write_text("plain raw evidence", encoding="utf-8")
        new.write_text(formatted("lesson-new"), encoding="utf-8")
        dupe.write_text(formatted("lesson-dupe"), encoding="utf-8")
        draft = _pending_rows.draft_lesson_from_pending_raw_text(
            raw,
            "plain raw evidence",
            project_slug="kanda_reasoner",
        )
        if draft.get("lesson_id") != "lesson-pending-raw" or draft.get("status") != "draft":
            _fail("draft pending row helper did not preserve draft identity/status")
        rows = _pending_rows.pending_lesson_rows_for_table(
            [raw, new, dupe],
            [],
            ["lesson-dupe"],
            is_formatted_lesson_payload=is_formatted,
            lesson_from_formatted_text=lesson_from_formatted,
        )
        by_id = {row["lesson_id"]: row for row in rows}
        if by_id.get("lesson-new", {}).get("kind") != "pending_review":
            _fail("formatted pending row was not classified as pending_review")
        if by_id.get("lesson-dupe", {}).get("kind") != "pending_duplicate":
            _fail("duplicate formatted pending row was not classified as pending_duplicate")
        if by_id.get("lesson-pending-raw", {}).get("kind") != "pending_edit":
            _fail("raw pending row was not classified as pending_edit")
        if _pending_rows.pending_lesson_rows_for_table(
            [raw],
            [str(raw.resolve(strict=False))],
            [],
            is_formatted_lesson_payload=is_formatted,
            lesson_from_formatted_text=lesson_from_formatted,
        ):
            _fail("dismissed pending source was not filtered out")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
