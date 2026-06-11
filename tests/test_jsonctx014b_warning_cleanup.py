"""JSONCTX014B warning cleanup focused checks."""

from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAZY_TABS_PATH = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "lazy_tabs.py"
OUTPUT_POLICY_PATH = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_symbol_atlas" / "output_policy.py"


def _is_broad_exception(handler: ast.ExceptHandler) -> bool:
    if handler.type is None:
        return True
    if isinstance(handler.type, ast.Name):
        return handler.type.id in {"Exception", "BaseException"}
    if isinstance(handler.type, ast.Tuple):
        for item in handler.type.elts:
            if isinstance(item, ast.Name) and item.id in {"Exception", "BaseException"}:
                return True
    return False


def _constant_value(node: ast.AST) -> object:
    if isinstance(node, ast.Constant):
        return node.value
    return None


def test_lazy_tab_load_tool_returns_false_on_isolated_failure() -> None:
    source = LAZY_TABS_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    load_tool = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "load_tool":
            load_tool = node
            break

    assert load_tool is not None
    assert isinstance(load_tool.returns, ast.Name)
    assert load_tool.returns.id == "bool"

    broad_handlers = [
        node
        for node in ast.walk(load_tool)
        if isinstance(node, ast.ExceptHandler) and _is_broad_exception(node)
    ]
    assert not broad_handlers

    specific_handlers = [
        node
        for node in ast.walk(load_tool)
        if isinstance(node, ast.ExceptHandler) and not _is_broad_exception(node)
    ]
    assert specific_handlers
    assert any(
        False in [
            _constant_value(child.value)
            for child in ast.walk(handler)
            if isinstance(child, ast.Return)
        ]
        for handler in specific_handlers
    )

    assert 'self.status_label.setText("FAILED TO LOAD")' in source
    assert "ToolLoadErrorPanel(" in source


def test_output_policy_declares_public_surface() -> None:
    source = OUTPUT_POLICY_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    all_assignments = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
    ]
    assert all_assignments

    value = all_assignments[0].value
    assert isinstance(value, ast.List)
    public_names = [_constant_value(item) for item in value.elts]

    required = {
        "IMPORTANT_TEST_TERMS",
        "INACTIVE_PATH_MARKERS",
        "LOW_VALUE_TEST_MARKERS",
        "MAX_RELATED_FILES",
        "MAX_TESTS_TO_RUN",
        "is_active_atlas_path",
        "is_active_test_command",
        "normalize_atlas_path",
        "sanitize_atlas_markdown_text",
    }
    assert required.issubset(set(public_names))


def main() -> int:
    test_lazy_tab_load_tool_returns_false_on_isolated_failure()
    test_output_policy_declares_public_surface()
    print("JSONCTX014B warning cleanup tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
