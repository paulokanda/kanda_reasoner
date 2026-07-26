"""Validate Error Memory tab receive/import refactor."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = 'error-memory-tab-receive-import-refactor-v1'
ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / 'kanda_reasoner_app/error_memory_gui/error_memory_tab.py'
HELPER = ROOT / 'kanda_reasoner_app/error_memory_gui/_receive_import.py'
TEST = ROOT / 'tests/test_error_memory_tab_receive_import_public_contract.py'


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
    if len(tab_text.splitlines()) >= 895:
        fail('error_memory_tab.py did not shrink below cluster 14 baseline')
    if 'from kanda_reasoner_app.error_memory_gui._receive_import import (' not in tab_text:
        fail('receive/import helper import missing from facade')
    for name in [
        'receive_formulary_from_ai',
        'import_error_lesson_zip',
        'load_formatted_lesson_into_tab',
    ]:
        if name not in helper_text:
            fail('expected helper symbol missing: ' + name)
    for method in ['_receive_formulary_from_ai', '_import_error_lesson_zip']:
        if ('def ' + method) not in tab_text:
            fail('facade wrapper missing: ' + method)
    for module in top_level_import_modules(HELPER):
        if 'error_memory_tab' in module:
            fail('_receive_import imports the facade upward: ' + module)
    for module in top_level_import_modules(HELPER):
        if module.startswith('PySide6'):
            fail('_receive_import has top-level PySide/Qt import: ' + module)
    helper_tree = ast.parse(helper_text)
    all_assign = next((node for node in helper_tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '__all__' for t in node.targets)), None)
    if all_assign is None:
        fail('_receive_import missing __all__')

    print('VALIDATION OK: ' + FEATURE_ID)
    print('STATUS: IN_SYNC')


if __name__ == '__main__':
    main()
