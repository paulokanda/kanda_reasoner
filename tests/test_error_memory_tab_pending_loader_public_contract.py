"""Public-contract checks for ErrorMemoryTab pending-loader extraction."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
TAB_PATH = ROOT / 'kanda_reasoner_app/error_memory_gui/error_memory_tab.py'
HELPER_PATH = ROOT / 'kanda_reasoner_app/error_memory_gui/_pending_loader.py'


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding='utf-8'))


def test_pending_loader_helper_has_no_upward_facade_import() -> None:
    tree = _tree(HELPER_PATH)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = getattr(node, 'module', '') or ''
            names = [alias.name for alias in getattr(node, 'names', [])]
            assert 'error_memory_tab' not in module
            assert 'error_memory_tab' not in ' '.join(names)


def test_pending_loader_helper_keeps_qt_imports_local() -> None:
    tree = _tree(HELPER_PATH)
    top_level_imports = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    for node in top_level_imports:
        module = getattr(node, 'module', '') or ''
        names = [alias.name for alias in getattr(node, 'names', [])]
        assert not module.startswith('PySide6')
        assert all(not name.startswith('PySide6') for name in names)


def test_facade_preserves_pending_loader_methods_as_wrappers() -> None:
    text = TAB_PATH.read_text(encoding='utf-8')
    for method in [
        'load_pending_ai_assisted_error_lesson_intake_now',
        '_load_pending_ai_assisted_error_lesson_intake',
        '_show_duplicate_pending_intake_warning',
        '_lesson_id_exists_in_lessons',
        '_load_pending_intake_row_into_editor',
        '_delete_pending_file_quietly',
    ]:
        assert f'def {method}' in text
    assert 'from kanda_reasoner_app.error_memory_gui._pending_loader import (' in text


def test_delete_pending_file_quietly_is_safe_and_directly_testable(tmp_path: Path) -> None:
    from kanda_reasoner_app.error_memory_gui._pending_loader import delete_pending_file_quietly

    target = tmp_path / 'pending.json'
    target.write_text('{}', encoding='utf-8')
    assert delete_pending_file_quietly(target) is True
    assert not target.exists()
    assert delete_pending_file_quietly(target) is False


class _FakeRootEdit:
    def __init__(self, text: str = '') -> None:
        self._text = text
        self.changed_to: str | None = None

    def text(self) -> str:
        return self._text

    def setText(self, value: str) -> None:
        self.changed_to = value
        self._text = value


def test_public_loader_hook_updates_project_root_before_loading(tmp_path: Path) -> None:
    from kanda_reasoner_app.error_memory_gui._pending_loader import load_pending_ai_assisted_error_lesson_intake_now

    called = {'loaded': False}

    def load_now() -> bool:
        called['loaded'] = True
        return True

    tab = SimpleNamespace(
        _project_root=tmp_path,
        _syncing_project_root_field=False,
        project_root_value_label=_FakeRootEdit(''),
        _existing_directory_from_text=lambda text: Path(text),
        _load_pending_ai_assisted_error_lesson_intake=load_now,
    )
    assert load_pending_ai_assisted_error_lesson_intake_now(tab, tmp_path) is True
    assert called['loaded'] is True
    assert tab._project_root == tmp_path
    assert tab.project_root_value_label.text() == str(tmp_path)
