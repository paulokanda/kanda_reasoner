"""Validate Error Memory GUI mixin import-surface repair behavior."""

from __future__ import annotations

import ast
from pathlib import Path

FEATURE_ID = "error-memory-gui-mixin-import-surface-repair-v1"
ROOT = Path(__file__).resolve().parents[1]

PROJECT_PATHS = ROOT / "kanda_reasoner_app/error_memory_gui/_project_paths_mixin.py"
TABLE_DRAFT = ROOT / "kanda_reasoner_app/error_memory_gui/_table_draft_mixin.py"
INTAKE_ACTIONS = ROOT / "kanda_reasoner_app/error_memory_gui/_intake_actions_mixin.py"
TABLE_VIEW = ROOT / "kanda_reasoner_app/error_memory_gui/_table_view.py"


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing expected file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def assert_contains(path: Path, snippet: str) -> None:
    text = read(path)
    if snippet not in text:
        raise AssertionError(f"Missing snippet in {path.relative_to(ROOT)}: {snippet}")


def exported_functions(path: Path) -> set[str]:
    tree = ast.parse(read(path))
    return {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}


def imported_names(path: Path) -> set[str]:
    tree = ast.parse(read(path))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".", 1)[0])
    return names


def main() -> None:
    # The previous frozen Error Memory GUI refactor moved methods out of
    # error_memory_tab.py. These imports/constants were available in the
    # original monolithic module and must be owned by the extracted mixins now.
    assert "bootstrap_error_memory_store" in imported_names(PROJECT_PATHS)
    assert_contains(PROJECT_PATHS, "ERROR_MEMORY_PENDING_PATH_ROLE = Qt.UserRole + 2")
    assert_contains(PROJECT_PATHS, "pending_path_role=ERROR_MEMORY_PENDING_PATH_ROLE")

    assert "list_lessons" in imported_names(TABLE_DRAFT)
    assert_contains(TABLE_DRAFT, "ERROR_MEMORY_ROW_KIND_ROLE = Qt.UserRole + 1")
    assert_contains(TABLE_DRAFT, "ERROR_MEMORY_PENDING_PATH_ROLE = Qt.UserRole + 2")
    assert_contains(TABLE_DRAFT, "row_kind_role=ERROR_MEMORY_ROW_KIND_ROLE")
    assert_contains(TABLE_DRAFT, "pending_path_role=ERROR_MEMORY_PENDING_PATH_ROLE")

    assert "resolve_project_error_memory_root" in imported_names(INTAKE_ACTIONS)
    assert_contains(INTAKE_ACTIONS, "resolve_project_error_memory_root(self._current_project_root())")

    # Preserve the prior import-surface repair: _table_draft_mixin imports this
    # helper from _table_view, so _table_view must continue to expose it.
    assert "lesson_from_current_windows_or_selection" in exported_functions(TABLE_VIEW)
    assert_contains(TABLE_DRAFT, "lesson_from_current_windows_or_selection")

    # Guard against accidental behavior changes while repairing imports.
    assert_contains(PROJECT_PATHS, "bootstrap_error_memory_store(root)")
    assert_contains(TABLE_DRAFT, "list_lessons(self._current_project_root(), include_inactive=True)")
    assert_contains(INTAKE_ACTIONS, "PENDING_AI_ASSISTED_INTAKE_DIR_NAME")

    print(f"VALIDATION OK: {FEATURE_ID}")


if __name__ == "__main__":
    main()
