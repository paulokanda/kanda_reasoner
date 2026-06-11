"""Direct import protection for project_symbol_atlas_integration."""

from __future__ import annotations

import unittest

import kanda_reasoner_app.engineering_safety.project_symbol_atlas_integration as module


class ProjectSymbolAtlasIntegrationDirectImportTests(unittest.TestCase):
    """Protect the engineering safety symbol atlas integration public contract."""

    def test_module_imports_through_public_contract(self) -> None:
        self.assertIsNotNone(module)

    def test_public_all_is_present(self) -> None:
        exported_names = getattr(module, "__all__", None)

        self.assertIsInstance(exported_names, (list, tuple))
        self.assertGreater(len(exported_names), 0)

    def test_exported_names_are_defined(self) -> None:
        missing_names = [
            name
            for name in getattr(module, "__all__", ())
            if not hasattr(module, name)
        ]

        self.assertEqual([], missing_names)


if __name__ == "__main__":
    unittest.main()
