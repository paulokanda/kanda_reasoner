"""Regression tests for canonical reasoner_engine project_profile migration."""

from __future__ import annotations

import importlib
from pathlib import Path
import unittest

import kanda_reasoner_app.reasoner_engine.project_profile as canonical_project_profile
import kanda_reasoner_app.reasoner_engine.project_profile_help.built_in_profiles as canonical_built_in_profiles
import kanda_reasoner_app.reasoner_engine.project_profile_help.inference as canonical_inference
import kanda_reasoner_app.reasoner_engine.project_profile_help.profile_types as canonical_profile_types
import kanda_reasoner_app.reasoner_engine.project_profile_help.registry as canonical_registry

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"


class ReasonerEngineProjectProfileCanonicalMigrationTests(unittest.TestCase):
    """Protect the canonical project_profile owner box during staged migration."""

    def test_canonical_project_profile_implementation_files_exist(self) -> None:
        self.assertTrue((CANONICAL_DIR / "project_profile.py").is_file())
        self.assertTrue((CANONICAL_DIR / "project_profile_help.json").is_file())
        self.assertTrue((CANONICAL_DIR / "project_profile_validate_manifests.py").is_file())
        self.assertTrue((CANONICAL_DIR / "project_profile_help" / "__init__.py").is_file())
        self.assertTrue((CANONICAL_DIR / "project_profile_help" / "built_in_profiles.py").is_file())
        self.assertTrue((CANONICAL_DIR / "project_profile_help" / "inference.py").is_file())
        self.assertTrue((CANONICAL_DIR / "project_profile_help" / "profile_types.py").is_file())
        self.assertTrue((CANONICAL_DIR / "project_profile_help" / "registry.py").is_file())

    def test_legacy_project_profile_remains_available_during_migration(self) -> None:
        self.assertTrue((LEGACY_DIR / "project_profile.py").is_file())
        self.assertTrue((LEGACY_DIR / "project_profile_help" / "built_in_profiles.py").is_file())
        self.assertTrue((LEGACY_DIR / "ai_bridge.py").is_file())

    def test_canonical_and_legacy_project_profile_imports_resolve_same_payload(self) -> None:
        canonical = importlib.import_module("kanda_reasoner_app.reasoner_engine.project_profile")
        legacy = importlib.import_module("kanda_reasoner_app.project_reasoner_v10.project_profile")
        self.assertEqual(canonical.__name__, "kanda_reasoner_app.reasoner_engine.project_profile")
        self.assertEqual(legacy.__name__, "kanda_reasoner_app.project_reasoner_v10.project_profile")
        self.assertEqual(
            canonical.GENERIC_PROJECT_PROFILE.to_dict(),
            legacy.GENERIC_PROJECT_PROFILE.to_dict(),
        )
        self.assertEqual(set(canonical.PROJECT_PROFILES), set(legacy.PROJECT_PROFILES))
        for profile_name in canonical.PROJECT_PROFILES:
            self.assertEqual(
                canonical.PROJECT_PROFILES[profile_name].to_dict(),
                legacy.PROJECT_PROFILES[profile_name].to_dict(),
            )
        self.assertEqual(
            canonical.infer_project_profile_name_from_metadata(),
            legacy.infer_project_profile_name_from_metadata(),
        )

    def test_canonical_project_profile_uses_reasoner_engine_manifest_paths(self) -> None:
        manifest = (CANONICAL_DIR / "project_profile_help.json").read_text(encoding="utf-8")
        self.assertIn("kanda_reasoner_app/reasoner_engine/project_profile.py", manifest)
        self.assertIn("kanda_reasoner_app/reasoner_engine/project_profile_help", manifest)
        self.assertNotIn("kanda_reasoner_app/project_reasoner_v10/project_profile.py", manifest)

    def test_canonical_project_profile_helpers_import_through_public_contracts(self) -> None:
        module_names = [
            "built_in_profiles",
            "inference",
            "profile_types",
            "registry",
        ]
        for module_name in module_names:
            with self.subTest(module_name=module_name):
                imported = importlib.import_module(
                    "kanda_reasoner_app.reasoner_engine.project_profile_help." + module_name
                )
                self.assertTrue(hasattr(imported, "__all__"))

    def test_canonical_project_profile_public_contracts_are_directly_importable(self) -> None:
        self.assertTrue(hasattr(canonical_project_profile, "ProjectProfile"))
        self.assertTrue(hasattr(canonical_built_in_profiles, "GENERIC_PROJECT_PROFILE"))
        self.assertTrue(hasattr(canonical_inference, "infer_project_profile"))
        self.assertTrue(hasattr(canonical_profile_types, "ProjectProfile"))
        self.assertTrue(hasattr(canonical_registry, "get_project_profile"))

    def test_project_profile_inference_and_registry_are_callable(self) -> None:
        self.assertTrue(callable(canonical_inference.infer_project_profile))
        self.assertTrue(callable(canonical_inference.infer_project_profile_name_from_metadata))
        self.assertTrue(callable(canonical_registry.get_project_profile))
        self.assertTrue(callable(canonical_registry.iter_project_profiles))
        self.assertEqual(canonical_registry.get_project_profile(None).name, "generic")


if __name__ == "__main__":
    unittest.main()
