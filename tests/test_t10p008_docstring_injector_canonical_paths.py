"""Validate canonical paths in the module docstring injector script."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class DocstringInjectorCanonicalPathTests(unittest.TestCase):
    """Check that the root docstring injector no longer hardcodes legacy paths."""

    def test_source_does_not_hardcode_legacy_project_paths(self) -> None:
        source = Path("_inject_missing_module_docstrings.py").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("developer_tools", source)
        self.assertNotIn("_project_reference", source)
        self.assertNotIn('ask_' 'ai_project_reasoner', source)

    def test_validation_command_uses_canonical_package_cli(self) -> None:
        module = importlib.import_module("_inject_missing_module_docstrings")
        command_path = module.MANAGE_ARCHITECTURE.as_posix()

        self.assertIn("kanda_reasoner_app/manage_architecture/manage_architecture.py", command_path)
        self.assertNotIn('ask_' 'ai_project_reasoner' '/manage_architecture', command_path)

    def test_backup_root_uses_hidden_project_reference_folder(self) -> None:
        module = importlib.import_module("_inject_missing_module_docstrings")
        backup_path = module.BACKUP_ROOT.as_posix()

        self.assertIn("workbench/docstring_injection_backups", backup_path)
        self.assertNotIn("_project_reference/docstring_injection_backups", backup_path)

    def test_role_prefixes_support_canonical_and_legacy_package_names(self) -> None:
        module = importlib.import_module("_inject_missing_module_docstrings")
        prefixes = {prefix for prefix, _sentence in module.ROLE_PREFIXES}

        self.assertIn(
            "kanda_reasoner_app/reasoner_context_collector/",
            prefixes,
        )
        self.assertIn(
            module.LEGACY_PACKAGE_NAME + "/reasoner_context_collector/",
            prefixes,
        )


if __name__ == "__main__":
    unittest.main()
