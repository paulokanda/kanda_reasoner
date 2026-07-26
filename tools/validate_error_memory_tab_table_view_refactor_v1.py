"""Validate Error Memory tab table view refactor."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = 'error-memory-tab-table-view-refactor-v1'
ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / 'kanda_reasoner_app/error_memory_gui/error_memory_tab.py'
HELPER = ROOT / 'kanda_reasoner_app/error_memory_gui/_table_view.py'
TEST = ROOT / 'tests/test_error_memory_tab_table_view_public_contract.py'


def fail(message: str) -> None:
    print('VALIDATION ERROR: ' + message)
    raise SystemExit(1)


def top_level_import_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    modules: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            modules.append(node.module or '')
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return modules


def main() -> None:
    for path in [TAB, HELPER, TEST]:
        if not path.exists():
            fail('missing file: ' + str(path.relative_to(ROOT)))

    subprocess.run([sys.executable, '-m', 'py_compile', str(TAB), str(HELPER), str(TEST)], check=True)

    tab_text = TAB.read_text(encoding='utf-8')
    helper_text = HELPER.read_text(encoding='utf-8')
    if len(tab_text.splitlines()) >= 1055:
        fail('error_memory_tab.py did not shrink below cluster 12 baseline')
    if 'from kanda_reasoner_app.error_memory_gui._table_view import (' not in tab_text:
        fail('table view helper import missing from facade')
    if 'QTableWidgetItem' in tab_text:
        fail('QTableWidgetItem should be local to _table_view after extraction')
    for name in [
        'reload_table',
        'load_selected_lesson_into_preview',
        'formatted_lesson_block',
        'selected_lesson_id_from_table',
    ]:
        if name not in helper_text:
            fail('expected helper symbol missing: ' + name)
    for module in top_level_import_modules(HELPER):
        if 'error_memory_tab' in module:
            fail('_table_view imports the facade upward: ' + module)
    for module in top_level_import_modules(HELPER):
        if module.startswith('PySide6'):
            fail('_table_view has top-level PySide/Qt import: ' + module)
    helper_tree = ast.parse(helper_text)
    all_assign = next((node for node in helper_tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '__all__' for t in node.targets)), None)
    if all_assign is None:
        fail('_table_view missing __all__')

    print('VALIDATION OK: ' + FEATURE_ID)
    print('STATUS: IN_SYNC')


if __name__ == '__main__':
    main()
