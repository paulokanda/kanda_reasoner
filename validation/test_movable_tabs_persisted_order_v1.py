"""Validate movable persisted tabs v1 patch."""

from __future__ import annotations

import ast
import py_compile
from pathlib import Path

FEATURE_ID = "movable-tabs-persisted-order-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_WINDOW = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "main_window.py"
WINDOW_STATE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "main_window_help"
    / "window_state.py"
)
WINDOW_TOOL_PATCHES = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "main_window_help"
    / "window_tool_patches.py"
)

TOUCHED_FILES = (MAIN_WINDOW, WINDOW_STATE, WINDOW_TOOL_PATCHES)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _function_names(path: Path) -> set[str]:
    tree = ast.parse(_read(path), filename=str(path))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def test_source_compiles() -> None:
    for path in TOUCHED_FILES:
        py_compile.compile(str(path), doraise=True)


def test_main_window_enables_movable_tabs() -> None:
    text = _read(MAIN_WINDOW)
    _assert("self.tabs.setMovable(True)" in text, "QTabWidget must be movable")
    _assert("self.tabs.setMovable(False)" not in text, "tabs must not remain locked")
    _assert(
        "self.tabs.tabBar().tabMoved.connect(self._on_tab_moved)" in text,
        "tabMoved signal must be connected",
    )


def test_main_window_persists_and_restores_order() -> None:
    text = _read(MAIN_WINDOW)
    names = _function_names(MAIN_WINDOW)
    for name in (
        "_ordered_tool_specs",
        "_refresh_tab_indexes_from_widgets",
        "_current_tab_order",
        "_remember_tab_order",
        "_on_tab_moved",
    ):
        _assert(name in names, f"missing method: {name}")

    _assert(
        "for spec in self._ordered_tool_specs(TOOLS):" in text,
        "startup must use persisted tab order",
    )
    _assert(
        "self._prefs[\"tab_order\"] = self._current_tab_order()" in text,
        "tab moves must update prefs tab_order",
    )
    _assert(
        "self._tab_navigation_controller.refresh_tab_index_map" in text,
        "navigation map must refresh after reordering",
    )
    _assert(
        "self.tabs.tabBar().setTabData(index, spec.tab_id)" in text,
        "tabs must carry stable tab IDs",
    )


def test_prefs_saves_tab_order_without_overwriting_other_prefs() -> None:
    text = _read(WINDOW_STATE)
    _assert("payload[\"tab_order\"]" in text, "_save_prefs must write tab_order")
    _assert("existing.update(payload)" in text, "_save_prefs must merge with existing prefs")
    _assert("last_project_root" in text, "existing project-root prefs must be preserved")


def test_lazy_loading_survives_reordered_indexes() -> None:
    text = _read(WINDOW_TOOL_PATCHES)
    names = _function_names(WINDOW_TOOL_PATCHES)
    _assert("_lazy_page_for_tab_index" in names, "lazy lookup helper is missing")
    _assert(
        "self.tabs.widget(index)" in text,
        "lazy page lookup must fall back to the actual tab widget",
    )
    _assert(
        "widget.__class__.__name__ == \"LazyToolTab\"" in text,
        "lazy lookup must recognize LazyToolTab after tab moves",
    )
    _assert(
        "page = self._lazy_page_for_tab_index(index)" in text,
        "tab change handler must use reorder-safe lookup",
    )


def main() -> int:
    tests = (
        test_source_compiles,
        test_main_window_enables_movable_tabs,
        test_main_window_persists_and_restores_order,
        test_prefs_saves_tab_order_without_overwriting_other_prefs,
        test_lazy_loading_survives_reordered_indexes,
    )
    for test in tests:
        print("RUN " + test.__name__)
        test()
        print("PASS " + test.__name__)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
