"""Regression tests for T10P062 GUI shell canonical Python references."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest

if False:
    pass


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell"
LEGACY_TOKEN = 'ask_' 'ai_project_reasoner'
CANONICAL_TOKEN = "kanda_reasoner_app"


class ReasonerToolsGuiShellCanonicalPythonRefsTests(unittest.TestCase):
    """Protect the staged GUI shell package migration."""

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        """The active owner-box Python surface should not pin the legacy package token."""
        offenders: list[str] = []
        for path in sorted(OWNER_ROOT.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if LEGACY_TOKEN in text:
                offenders.append(str(path.relative_to(PROJECT_ROOT)))

        self.assertEqual([], offenders)

    def test_tool_specs_use_canonical_module_candidates_and_source_hints(self) -> None:
        """Tool registry entries should point callers at canonical package names."""
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        legacy_values: list[str] = []
        for spec in TOOLS:
            legacy_values.extend(
                value for value in spec.module_candidates if LEGACY_TOKEN in value
            )
            if LEGACY_TOKEN in spec.source_hint:
                legacy_values.append(spec.source_hint)

        self.assertEqual([], legacy_values)
        self.assertTrue(
            any(
                any(value.startswith(CANONICAL_TOKEN + ".") for value in spec.module_candidates)
                for spec in TOOLS
            )
        )

    def test_prompt_library_tab_public_contract_is_declared(self) -> None:
        """The prompt-library tab remains an explicit public plugin contract."""
        path = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "prompt_library_gui" / "prompt_library_tab.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        exported = []
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                continue
            if isinstance(node.value, ast.List):
                exported = [
                    item.value
                    for item in node.value.elts
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)
                ]
        self.assertIn("PromptLibraryTab", exported)

    def test_main_window_manifest_validator_uses_dynamic_staged_paths(self) -> None:
        """The manifest validator should preserve staged physical paths dynamically."""
        path = OWNER_ROOT / "main_window_validate_manifests.py"
        text = path.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_TOKEN, text)
        self.assertIn("LEGACY_PACKAGE_NAME", text)
        ast.parse(text)

    def test_gui_support_uses_dynamic_staged_package_dir(self) -> None:
        """Worker-script paths should stay physical without hard-coding the legacy token."""
        path = OWNER_ROOT / "gui_support.py"
        text = path.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_TOKEN, text)
        self.assertIn("LEGACY_PACKAGE_NAME", text)
        ast.parse(text)


if __name__ == "__main__":
    unittest.main()
