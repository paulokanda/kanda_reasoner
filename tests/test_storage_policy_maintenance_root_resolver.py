"""Tests for storage policy maintenance root resolution."""

from __future__ import annotations

import inspect
from pathlib import Path
import unittest

import kanda_reasoner_app.storage_policy.maintenance_root_resolver as resolver
from kanda_reasoner_app.storage_policy.path_resolver import get_app_root


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class StoragePolicyMaintenanceRootResolverTests(unittest.TestCase):
    """Validate side-effect-free maintenance root resolver behavior."""

    def test_default_maintenance_root_name_is_canonical(self) -> None:
        root = resolver.get_default_maintenance_root(PROJECT_ROOT)

        self.assertEqual(root.name, resolver.MAINTENANCE_ROOT_FOLDER_NAME)

    def test_default_maintenance_root_is_outside_app_root(self) -> None:
        root = resolver.get_default_maintenance_root(PROJECT_ROOT)

        self.assertFalse(resolver.is_maintenance_root_inside_app(root, PROJECT_ROOT))

    def test_get_maintenance_root_uses_default_without_environment(self) -> None:
        root = resolver.get_maintenance_root(PROJECT_ROOT, environment={})

        self.assertEqual(root, resolver.get_default_maintenance_root(PROJECT_ROOT))

    def test_get_maintenance_root_uses_lowercase_environment_override(self) -> None:
        override = PROJECT_ROOT.parent / "custom_maintenance_root"
        root = resolver.get_maintenance_root(
            PROJECT_ROOT,
            environment={"kanda_reasoner_maintenance_root": str(override)},
        )

        self.assertEqual(root, override.resolve())

    def test_get_maintenance_root_uses_uppercase_environment_override(self) -> None:
        override = PROJECT_ROOT.parent / "custom_maintenance_root_upper"
        root = resolver.get_maintenance_root(
            PROJECT_ROOT,
            environment={"KANDA_REASONER_MAINTENANCE_ROOT": str(override)},
        )

        self.assertEqual(root, override.resolve())

    def test_lowercase_environment_override_has_priority(self) -> None:
        lower = PROJECT_ROOT.parent / "lower_priority_root"
        upper = PROJECT_ROOT.parent / "upper_priority_root"
        root = resolver.get_maintenance_root(
            PROJECT_ROOT,
            environment={
                "kanda_reasoner_maintenance_root": str(lower),
                "KANDA_REASONER_MAINTENANCE_ROOT": str(upper),
            },
        )

        self.assertEqual(root, lower.resolve())

    def test_build_maintenance_root_from_windows_drive_string(self) -> None:
        root = resolver.build_maintenance_root_from_drive_or_anchor("X:")

        self.assertEqual(str(root), "X:\\_kanda_reasoner_temp")

    def test_build_maintenance_root_from_posix_anchor(self) -> None:
        root = resolver.build_maintenance_root_from_drive_or_anchor("/")

        self.assertEqual(root, Path("/") / resolver.MAINTENANCE_ROOT_FOLDER_NAME)

    def test_empty_drive_or_anchor_raises(self) -> None:
        with self.assertRaises(ValueError):
            resolver.build_maintenance_root_from_drive_or_anchor("")

    def test_assert_maintenance_root_outside_app_accepts_safe_root(self) -> None:
        root = resolver.get_default_maintenance_root(PROJECT_ROOT)

        self.assertEqual(
            resolver.assert_maintenance_root_outside_app(root, PROJECT_ROOT),
            root.resolve(),
        )

    def test_assert_maintenance_root_outside_app_rejects_inside_root(self) -> None:
        inside = PROJECT_ROOT / "_kanda_reasoner_temp"

        with self.assertRaises(ValueError):
            resolver.assert_maintenance_root_outside_app(inside, PROJECT_ROOT)

    def test_actual_app_root_still_resolves(self) -> None:
        self.assertEqual(get_app_root(), PROJECT_ROOT)

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "MAINTENANCE_ROOT_ENV_VARS",
            "MAINTENANCE_ROOT_FOLDER_NAME",
            "assert_maintenance_root_outside_app",
            "build_maintenance_root_from_drive_or_anchor",
            "get_default_maintenance_root",
            "get_maintenance_root",
            "is_maintenance_root_inside_app",
        }

        self.assertEqual(set(resolver.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(resolver, name))

    def test_resolver_source_has_no_hardcoded_project_paths(self) -> None:
        source = inspect.getsource(resolver)
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "C:\\",
            "D:\\",
            "developer_tools",
            "project_analysis_evidence",
            "kanda_reasoner_architecture_audit",
        ]

        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, source)


if __name__ == "__main__":
    unittest.main()
