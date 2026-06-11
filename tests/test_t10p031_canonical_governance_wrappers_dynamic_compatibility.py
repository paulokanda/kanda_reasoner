"""Regression tests for canonical governance wrapper compatibility imports."""

from __future__ import annotations

import ast
import importlib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
COMPATIBILITY_PACKAGE = "_".join(("ask", "ai", "project", "reasoner"))

CHANGED_FILES = (
    Path("kanda_reasoner_app/manage_workflows/__init__.py"),
    Path("kanda_reasoner_app/manage_workflows/manage_workflows.py"),
    Path("kanda_reasoner_app/manage_architecture/__init__.py"),
    Path("kanda_reasoner_app/manage_architecture/manage_architecture.py"),
)


class CanonicalGovernanceWrapperDynamicCompatibilityTests(unittest.TestCase):
    """Verify canonical governance wrappers avoid fixed compatibility names."""

    def _read(self, relative_path: Path) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_changed_files_remain_ast_parseable(self) -> None:
        """Changed wrapper files should remain syntactically valid Python."""
        for relative_path in CHANGED_FILES:
            with self.subTest(relative_path=str(relative_path)):
                ast.parse(self._read(relative_path), filename=str(relative_path))

    def test_changed_files_do_not_hardcode_compatibility_package_token(self) -> None:
        """Changed wrappers should not contain the fixed compatibility token."""
        for relative_path in CHANGED_FILES:
            with self.subTest(relative_path=str(relative_path)):
                self.assertNotIn(COMPATIBILITY_PACKAGE, self._read(relative_path))

    def test_wrappers_use_dynamic_compatibility_constant(self) -> None:
        """Changed wrappers should derive module names from LEGACY_PACKAGE_NAME."""
        for relative_path in CHANGED_FILES:
            text = self._read(relative_path)
            with self.subTest(relative_path=str(relative_path)):
                self.assertIn("LEGACY_PACKAGE_NAME", text)
                self.assertIn("importlib.import_module", text)

    def test_workflow_wrapper_loads_dynamic_compatibility_module(self) -> None:
        """Workflow wrapper should load the implementation through importlib."""
        workflow_wrapper = importlib.import_module(
            "kanda_reasoner_app.manage_workflows.manage_workflows"
        )
        loaded = []
        fake_module = SimpleNamespace(main=lambda: 0, validate_project=lambda root: root)

        with mock.patch.object(
            workflow_wrapper.importlib,
            "import_module",
            side_effect=lambda name: loaded.append(name) or fake_module,
        ):
            self.assertEqual(workflow_wrapper.main(["--help"]), 0)
            self.assertEqual(workflow_wrapper.validate_project("E:/demo"), "E:/demo")

        expected = ".".join(
            (COMPATIBILITY_PACKAGE, "manage_workflows", "manage_workflows")
        )
        self.assertEqual(loaded, [expected, expected])

    def test_architecture_wrapper_loads_dynamic_compatibility_module(self) -> None:
        """Architecture wrapper should load the implementation through importlib."""
        architecture_wrapper = importlib.import_module(
            "kanda_reasoner_app.manage_architecture.manage_architecture"
        )
        loaded = []
        fake_module = SimpleNamespace(main=lambda: 0)

        with mock.patch.object(
            architecture_wrapper.importlib,
            "import_module",
            side_effect=lambda name: loaded.append(name) or fake_module,
        ):
            self.assertEqual(architecture_wrapper.main(["--help"]), 0)

        expected = ".".join(
            (COMPATIBILITY_PACKAGE, "manage_architecture", "manage_architecture")
        )
        self.assertEqual(loaded, [expected])


if __name__ == "__main__":
    unittest.main()
