# project-path: tools/validate_error_memory_tab_draft_deletion_refactor_v1.py
"""Validate Error Memory tab draft deletion helper extraction."""
from __future__ import annotations

import ast
import py_compile
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "error-memory-tab-draft-deletion-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_draft_deletion.py"
TEST = ROOT / "tests/test_error_memory_tab_draft_deletion_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._draft_deletion import (",
    "delete_matching_canonical_draft_lessons,",
    "draft_delete_identity_from_sources,",
    "def _draft_delete_identity_from_windows(self) -> tuple[set[str], list[str], list[str]]:",
    "return draft_delete_identity_from_sources(",
    "current_lesson=self._lesson_from_current_windows_or_selection(),",
    "lesson_id_from_text=self._lesson_id_from_text_lenient,",
    "def _delete_matching_canonical_draft_lessons(self, lesson_ids: set[str]) -> tuple[int, list[str], list[str]]:",
    "return delete_matching_canonical_draft_lessons(self._current_project_root(), lesson_ids)",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "def draft_delete_identity_from_sources(",
    "def delete_matching_canonical_draft_lessons(",
    "active-ready saved lesson preserved",
    "rebuild_index(root)",
]

FORBIDDEN_OLD_TAB_SNIPPETS = [
    "def add_text(value: str) -> None:",
    "stored_status = str(stored.get('status', '')).strip().lower()",
    "can_delete = stored_status == 'draft' or not active_ready(dict(stored))",
    "failures.append('index rebuild -> ' + str(exc))",
]


def _fail(message: str) -> None:
    """Support fail behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    """
    
    raise SystemExit("VALIDATION FAIL: " + message)


def _read(path: Path) -> str:
    """Support read behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not path.exists():
        _fail("missing file: " + str(path))
    return path.read_text(encoding="utf-8")


def _assert_no_upward_or_gui_imports(source: str) -> None:
    """Support assert no upward or gui imports behavior.
    
    Parameters
    ----------
    source : str
        The source value.
    """
    
    forbidden = ["PySide", "QtCore", "QtGui", "QtWidgets", "error_memory_tab", "ErrorMemoryTab"]
    for token in forbidden:
        if token in source:
            _fail("_draft_deletion.py contains forbidden dependency token: " + token)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = ""
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
            for alias in getattr(node, "names", []):
                module = module + " " + alias.name
            if "PySide" in module or "error_memory_tab" in module:
                _fail("_draft_deletion.py imports forbidden module: " + module)


def main() -> None:
    """Support main behavior.
    """
    
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_draft_deletion.py missing snippet: " + snippet)
    for snippet in FORBIDDEN_OLD_TAB_SNIPPETS:
        if snippet in tab_text:
            _fail("error_memory_tab.py still owns old draft deletion block: " + snippet)
    _assert_no_upward_or_gui_imports(helper_text)
    if len(tab_text.splitlines()) >= 1544:
        _fail("error_memory_tab.py did not shrink below cluster 7 line count")
    for path in [TAB, HELPER, TEST]:
        py_compile.compile(str(path), doraise=True)
    sys.path.insert(0, str(ROOT))
    from kanda_reasoner_app.error_memory_gui import _draft_deletion

    lesson_ids, visible_texts, explicit_paths = _draft_deletion.draft_delete_identity_from_sources(
        raw_error_text='{"lesson_id": "raw-id"}',
        received_preview_text="plain visible draft",
        last_dismissed_pending_intake_text='{"lesson_id": "dismissed-id"}',
        loaded_pending_intake_lesson_id="loaded-id",
        last_dismissed_pending_intake_lesson_id="dismissed-marker-id",
        selected_lesson_id="selected-id",
        current_lesson={"lesson_id": "current-id"},
        loaded_pending_intake_file="/tmp/pending/raw.txt",
        last_dismissed_pending_intake_file="/tmp/pending/raw.txt",
        lesson_id_from_text=lambda text: "raw-id" if "raw-id" in text else ("dismissed-id" if "dismissed-id" in text else ""),
    )
    expected_ids = {"raw-id", "dismissed-id", "loaded-id", "dismissed-marker-id", "selected-id", "current-id"}
    if lesson_ids != expected_ids:
        _fail("draft identity helper did not collect expected lesson IDs")
    if visible_texts != ['{"lesson_id": "raw-id"}', "plain visible draft", '{"lesson_id": "dismissed-id"}']:
        _fail("draft identity helper did not preserve visible text ordering/deduplication")
    if explicit_paths != ["/tmp/pending/raw.txt"]:
        _fail("draft identity helper did not deduplicate explicit pending markers")

    calls: list[tuple[str, object]] = []
    lessons = {
        "draft-id": {"lesson_id": "draft-id", "status": "draft"},
        "active-id": {"lesson_id": "active-id", "status": "active"},
    }

    def fake_list_lessons(root, include_inactive=False):
        calls.append(("list", include_inactive))
        return list(lessons.values())

    def fake_active_ready(lesson):
        return lesson.get("lesson_id") == "active-id"

    def fake_delete_lesson(root, lesson_id):
        calls.append(("delete", lesson_id))
        return {"lesson_id": lesson_id}

    def fake_rebuild_index(root):
        calls.append(("rebuild", str(root)))

    _draft_deletion.list_lessons = fake_list_lessons
    _draft_deletion.active_ready = fake_active_ready
    _draft_deletion.delete_lesson = fake_delete_lesson
    _draft_deletion.rebuild_index = fake_rebuild_index
    with tempfile.TemporaryDirectory() as temp_dir:
        deleted_count, skipped, failures = _draft_deletion.delete_matching_canonical_draft_lessons(
            Path(temp_dir),
            {"draft-id", "active-id", ""},
        )
    if deleted_count != 1:
        _fail("draft deletion helper did not delete exactly one draft")
    if skipped != ["active-id (active-ready saved lesson preserved)"]:
        _fail("draft deletion helper did not preserve active-ready lesson")
    if failures:
        _fail("draft deletion helper returned unexpected failures: " + repr(failures))
    if ("delete", "draft-id") not in calls or ("delete", "active-id") in calls:
        _fail("draft deletion helper called delete_lesson incorrectly")
    if not any(item[0] == "rebuild" for item in calls):
        _fail("draft deletion helper did not rebuild the index")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
