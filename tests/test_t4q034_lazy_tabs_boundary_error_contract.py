
from __future__ import annotations

import ast
from pathlib import Path
import unittest


TARGET = 'ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/lazy_tabs.py'


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


class T4Q034LazyTabsBoundaryErrorContractTests(unittest.TestCase):
    """Protect explicit error propagation in LazyToolTab.load_tool."""

    def test_load_tool_broad_handlers_reraise_or_return(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
        tree = ast.parse(source)

        load_tool = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "load_tool":
                load_tool = node
                break

        self.assertIsNotNone(load_tool, "load_tool not found")

        broad_handlers = [
            node
            for node in ast.walk(load_tool)
            if isinstance(node, ast.ExceptHandler) and _is_broad_exception(node)
        ]
        self.assertTrue(broad_handlers, "no broad exception handlers found in load_tool")

        for handler in broad_handlers:
            has_raise = any(isinstance(child, ast.Raise) for child in ast.walk(handler))
            has_return = any(isinstance(child, ast.Return) for child in ast.walk(handler))
            self.assertTrue(
                has_raise or has_return,
                "broad exception handler must explicitly raise or return",
            )

    def test_lazy_tabs_import_smoke(self) -> None:
        import kanda_reasoner_app.reasoner_tools_gui_shell.lazy_tabs as lazy_tabs

        self.assertTrue(hasattr(lazy_tabs, "LazyToolTab"))


if __name__ == "__main__":
    unittest.main()
