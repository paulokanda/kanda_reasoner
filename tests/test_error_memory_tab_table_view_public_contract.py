"""Public-contract checks for ErrorMemoryTab table-view extraction."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAB_PATH = ROOT / 'kanda_reasoner_app/error_memory_gui/error_memory_tab.py'
HELPER_PATH = ROOT / 'kanda_reasoner_app/error_memory_gui/_table_view.py'


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding='utf-8'))


def test_table_view_helper_has_no_upward_facade_import() -> None:
    text = HELPER_PATH.read_text(encoding='utf-8')
    tree = _tree(HELPER_PATH)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = getattr(node, 'module', '') or ''
            names = [alias.name for alias in getattr(node, 'names', [])]
            assert 'error_memory_tab' not in module
            assert 'error_memory_tab' not in ' '.join(names)


def test_table_view_helper_keeps_qt_imports_local() -> None:
    tree = _tree(HELPER_PATH)
    top_level_imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    for node in top_level_imports:
        module = getattr(node, 'module', '') or ''
        names = [alias.name for alias in getattr(node, 'names', [])]
        assert not module.startswith('PySide6')
        assert all(not name.startswith('PySide6') for name in names)


def test_facade_preserves_table_view_methods_as_wrappers() -> None:
    text = TAB_PATH.read_text(encoding='utf-8')
    for method in [
        '_reload_table',
        '_row_kind_for_row',
        '_pending_path_for_row',
        '_lesson_id_for_row',
        '_selected_lesson_id_from_table',
        '_formatted_lesson_block',
        '_lesson_json_text_for_windows',
        '_set_ai_assisted_intake_and_error_editor_from_pending_text',
        '_load_selected_lesson_into_preview',
    ]:
        assert f'def {method}' in text
    assert 'from kanda_reasoner_app.error_memory_gui._table_view import (' in text
    assert 'QTableWidgetItem' not in text


def test_formatted_lesson_block_uses_error_lesson_markers() -> None:
    from kanda_reasoner_app.error_memory_gui._table_view import formatted_lesson_block

    text = formatted_lesson_block({'lesson_id': 'demo', 'status': 'active'})
    assert text.startswith('KANDA_ERROR_LESSON_JSON_BEGIN')
    assert text.rstrip().endswith('KANDA_ERROR_LESSON_JSON_END')
    assert '"lesson_id": "demo"' in text


class _FakeItem:
    def __init__(self, text: str, data_by_role: dict[int, str]) -> None:
        self._text = text
        self._data_by_role = data_by_role

    def data(self, role: int) -> str:
        return self._data_by_role.get(role, '')

    def text(self) -> str:
        return self._text


class _FakeTable:
    def __init__(self, item: _FakeItem | None) -> None:
        self._item = item

    def item(self, row: int, col: int):
        return self._item if row == 0 and col == 4 else None


def test_row_metadata_helpers_are_directly_testable_without_qt() -> None:
    from kanda_reasoner_app.error_memory_gui._table_view import pending_path_for_row, row_kind_for_row

    item = _FakeItem('lesson-1', {101: 'pending_review', 102: 'E:/demo/pending.json'})
    table = _FakeTable(item)
    assert row_kind_for_row(table, 0, row_kind_role=101) == 'pending_review'
    assert pending_path_for_row(table, 0, pending_path_role=102) == 'E:/demo/pending.json'
    assert row_kind_for_row(table, -1, row_kind_role=101) == ''
    assert pending_path_for_row(_FakeTable(None), 0, pending_path_role=102) == ''
