"""Public-contract checks for ErrorMemoryTab receive/import extraction."""
from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
TAB_PATH = ROOT / 'kanda_reasoner_app/error_memory_gui/error_memory_tab.py'
HELPER_PATH = ROOT / 'kanda_reasoner_app/error_memory_gui/_receive_import.py'


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding='utf-8'))


def test_receive_import_helper_has_no_upward_facade_import() -> None:
    tree = _tree(HELPER_PATH)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = getattr(node, 'module', '') or ''
            names = [alias.name for alias in getattr(node, 'names', [])]
            assert 'error_memory_tab' not in module
            assert 'error_memory_tab' not in ' '.join(names)


def test_receive_import_helper_keeps_qt_imports_local() -> None:
    tree = _tree(HELPER_PATH)
    top_level_imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    for node in top_level_imports:
        module = getattr(node, 'module', '') or ''
        names = [alias.name for alias in getattr(node, 'names', [])]
        assert not module.startswith('PySide6')
        assert all(not name.startswith('PySide6') for name in names)


def test_facade_preserves_receive_import_methods_as_wrappers() -> None:
    text = TAB_PATH.read_text(encoding='utf-8')
    assert 'from kanda_reasoner_app.error_memory_gui._receive_import import (' in text
    assert 'def _receive_formulary_from_ai' in text
    assert 'receive_formulary_from_ai(self)' in text
    assert 'def _import_error_lesson_zip' in text
    assert 'import_error_lesson_zip(self)' in text


class _FakeEdit:
    def __init__(self) -> None:
        self.value = ''

    def setPlainText(self, value: str) -> None:
        self.value = value


def test_load_formatted_lesson_into_tab_sets_editor_state() -> None:
    from kanda_reasoner_app.error_memory_gui._receive_import import load_formatted_lesson_into_tab

    lesson = {'lesson_id': 'lesson-demo', 'status': 'draft'}
    tab = SimpleNamespace(
        _selected_lesson_id='',
        _last_received_lesson=None,
        _loaded_pending_intake_file='old-file',
        _loaded_pending_intake_lesson_id='old-id',
        raw_error_edit=_FakeEdit(),
        received_preview_edit=_FakeEdit(),
    )
    load_formatted_lesson_into_tab(tab, 'FORMATTED', lesson)
    assert tab._selected_lesson_id == 'lesson-demo'
    assert tab._last_received_lesson == lesson
    assert tab._loaded_pending_intake_file == ''
    assert tab._loaded_pending_intake_lesson_id == ''
    assert tab.raw_error_edit.value == 'FORMATTED'
    parsed = json.loads(tab.received_preview_edit.value)
    assert parsed['lesson_id'] == 'lesson-demo'
