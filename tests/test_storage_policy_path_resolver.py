"""Tests for storage policy path resolver helpers."""

from __future__ import annotations

import inspect
from pathlib import Path
import unittest

import kanda_reasoner_app.storage_policy.path_resolver as path_resolver


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "storage_policy" / "path_resolver.py"


class StoragePolicyPathResolverTests(unittest.TestCase):
    """Validate side-effect-free path resolver behavior."""

    def test_app_root_resolves_to_project_root(self) -> None:
        self.assertEqual(path_resolver.get_app_root(), PROJECT_ROOT)

    def test_app_package_root_resolves_to_canonical_package(self) -> None:
        package_root = path_resolver.get_app_package_root()

        self.assertEqual(package_root.name, "kanda_reasoner_app")
        self.assertEqual(package_root.parent, PROJECT_ROOT)

    def test_storage_policy_package_root_resolves_to_owner_box(self) -> None:
        package_root = path_resolver.get_storage_policy_package_root()

        self.assertEqual(package_root.name, "storage_policy")
        self.assertEqual(package_root.parent.name, "kanda_reasoner_app")

    def test_app_slug_is_dynamic_from_app_root_name(self) -> None:
        self.assertEqual(
            path_resolver.get_app_slug(PROJECT_ROOT),
            path_resolver.make_safe_slug(PROJECT_ROOT.name),
        )

    def test_make_safe_slug_normalizes_common_project_names(self) -> None:
        cases = {
            "Kanda Reasoner": "kanda_reasoner",
            "app-v2.0": "app_v2_0",
            "  My Project Name  ": "my_project_name",
            "": "project",
            "___": "project",
        }

        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(path_resolver.make_safe_slug(source), expected)

    def test_drive_or_anchor_has_stable_value(self) -> None:
        value = path_resolver.get_app_drive_or_anchor(PROJECT_ROOT)

        self.assertIsInstance(value, str)
        self.assertTrue(value)

    def test_path_inside_helpers(self) -> None:
        child = PROJECT_ROOT / "kanda_reasoner_app" / "storage_policy"

        self.assertTrue(path_resolver.is_path_inside(child, PROJECT_ROOT))
        self.assertTrue(path_resolver.is_path_same_or_inside(child, PROJECT_ROOT))
        self.assertTrue(path_resolver.is_path_same_or_inside(PROJECT_ROOT, PROJECT_ROOT))
        self.assertFalse(path_resolver.is_path_inside(PROJECT_ROOT, PROJECT_ROOT))

    def test_find_parent_named_raises_for_missing_parent(self) -> None:
        with self.assertRaises(ValueError):
            path_resolver.find_parent_named(MODULE_PATH, "missing_parent_name_xyz")

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "APP_PACKAGE_NAME",
            "DEFAULT_SLUG_FALLBACK",
            "find_parent_named",
            "get_app_drive_or_anchor",
            "get_app_package_root",
            "get_app_root",
            "get_app_slug",
            "get_storage_policy_package_root",
            "is_path_inside",
            "is_path_same_or_inside",
            "make_safe_slug",
            "normalize_path",
        }

        self.assertEqual(set(path_resolver.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(path_resolver, name))

    def test_resolver_source_has_no_hardcoded_project_paths(self) -> None:
        source = inspect.getsource(path_resolver)
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "C:\\",
            "D:\\",
            "developer_tools",
            "_kanda_reasoner_temp",
            "kanda_reasoner_architecture_audit",
            "project_analysis_evidence",
        ]

        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, source)


if __name__ == "__main__":
    unittest.main()
