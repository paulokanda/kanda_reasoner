"""Focused tests for the Tab Navigation Controller Box."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "tab_navigation_controller.py"
)

FORBIDDEN_IMPORT_ROOTS = (
    "PySide6",
    "main_window",
    "brain_navigator",
    "remember_box",
    "engineering_safety",
    "prompt_library",
)


class TabNavigationControllerContractTests(unittest.TestCase):
    """Verify stable tab-id navigation without GUI coupling."""

    def test_public_contract_imports_module_directly(self) -> None:
        """The focused test should import the public contract module directly."""

        import kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller as controller_module

        self.assertEqual(
            "tab_navigation_controller",
            controller_module.TAB_NAVIGATION_CONTROLLER_BOX_ID,
        )
        self.assertEqual(
            "0.1",
            controller_module.TAB_NAVIGATION_CONTROLLER_CONTRACT_VERSION,
        )
        self.assertIn("TabNavigationController", controller_module.__all__)

    def test_summary_declares_pure_controller_boundary(self) -> None:
        """The summary should describe a pure controller box boundary."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            get_tab_navigation_controller_summary,
        )

        summary = get_tab_navigation_controller_summary()

        self.assertEqual("tab_navigation_controller", summary.box_id)
        self.assertEqual("0.1", summary.contract_version)
        self.assertEqual("pure_controller_box", summary.implementation_state)
        self.assertIn(
            "kanda_reasoner_app/reasoner_tools_gui_shell/tab_navigation_controller.py",
            summary.owner_paths,
        )
        self.assertIn("PySide6", summary.forbidden_dependencies)
        self.assertIn("brain_navigator", summary.forbidden_dependencies)

    def test_builds_tab_id_index_map_from_dynamic_registry(self) -> None:
        """The controller should use stable tab IDs from the registry."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            build_tab_id_index_map,
        )
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        mapping = build_tab_id_index_map(TOOLS)

        self.assertEqual(0, mapping["brain_navigator"])
        self.assertEqual(1, mapping["architecture_review"])
        self.assertEqual(2, mapping["workflow_review"])
        self.assertEqual(3, mapping["engineering_safety"])
        self.assertIn("prompt_library", mapping)
        self.assertEqual(len(TOOLS), len(mapping))

    def test_first_index_allows_offset_when_embedding_tabs(self) -> None:
        """The map builder should support nonzero first visible indexes."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            build_tab_id_index_map,
        )
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        mapping = build_tab_id_index_map(TOOLS, first_index=1)

        self.assertEqual(1, mapping["brain_navigator"])
        self.assertEqual(2, mapping["architecture_review"])
        self.assertEqual(4, mapping["engineering_safety"])

    def test_open_known_tab_uses_bound_adapter(self) -> None:
        """Known tabs should open through the injected adapter callback."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            create_tab_navigation_controller,
        )

        opened_indexes: list[int] = []
        controller = create_tab_navigation_controller(
            {"brain_navigator": 0, "engineering_safety": 3},
            set_current_index=opened_indexes.append,
        )

        result = controller.open_tab_by_id("engineering_safety")

        self.assertTrue(result.success)
        self.assertEqual("opened", result.reason)
        self.assertEqual(3, result.tab_index)
        self.assertEqual([3], opened_indexes)

    def test_unknown_tab_returns_safe_failure(self) -> None:
        """Unknown tabs should fail safely without calling the adapter."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            create_tab_navigation_controller,
        )

        opened_indexes: list[int] = []
        controller = create_tab_navigation_controller(
            {"architecture_review": 0},
            set_current_index=opened_indexes.append,
        )

        result = controller.open_tab_by_id("not_registered")

        self.assertFalse(result.success)
        self.assertEqual("unknown_tab_id", result.reason)
        self.assertIsNone(result.tab_index)
        self.assertEqual([], opened_indexes)

    def test_known_tab_without_adapter_returns_navigation_not_bound(self) -> None:
        """A known tab without GUI binding should not crash."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            create_tab_navigation_controller,
        )

        controller = create_tab_navigation_controller({"prompt_library": 10})

        result = controller.open_tab_by_id("prompt_library")

        self.assertFalse(result.success)
        self.assertEqual("navigation_not_bound", result.reason)
        self.assertEqual(10, result.tab_index)

    def test_refresh_rejects_empty_tab_id_and_negative_index(self) -> None:
        """Invalid mappings should fail during boundary setup."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            create_tab_navigation_controller,
        )

        controller = create_tab_navigation_controller()

        with self.assertRaises(ValueError):
            controller.refresh_tab_index_map({"": 0})
        with self.assertRaises(ValueError):
            controller.refresh_tab_index_map({"architecture_review": -1})

    def test_controller_has_no_forbidden_imports_or_hardcoded_tab_switches(self) -> None:
        """The controller should not import GUI boxes or use numeric tab switching."""

        text = CONTROLLER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

        for token in FORBIDDEN_IMPORT_ROOTS:
            self.assertNotIn(token, imported_roots)
        self.assertNotIn("setCurrentIndex(", text)
        self.assertNotIn("self.tabs", text)

    def test_current_index_reader_is_optional(self) -> None:
        """The optional current-index reader should be adapter based."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tab_navigation_controller import (
            create_tab_navigation_controller,
        )

        controller = create_tab_navigation_controller(
            {"architecture_review": 0},
            get_current_index=lambda: 7,
        )

        self.assertEqual(7, controller.get_current_index())
        self.assertEqual(("architecture_review",), controller.list_registered_tab_ids())


if __name__ == "__main__":
    unittest.main()
