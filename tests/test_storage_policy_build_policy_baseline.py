"""Tests for the storage policy build and ignore baseline."""

from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.storage_policy.build_policy_baseline import (
    BuildPolicyBaseline,
    DEVELOPMENT_ONLY_WARN_PATTERNS,
    FAIL_BEFORE_COMPILATION_PATTERNS,
    GENERATED_INTENTIONAL_SOURCE_ALLOWLIST,
    PACKAGING_EXCLUDE_PATTERNS,
    POLICY_MODE_COMPILATION,
    POLICY_MODE_DEV,
    SECRET_EXCLUDE_HINT_PATTERNS,
    describe_build_policy_baseline,
    get_build_policy_baseline,
    render_buildignore_baseline,
    render_gitignore_baseline,
)
import kanda_reasoner_app.storage_policy.build_policy_baseline as policy_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "build_policy_baseline.py"
)


class StoragePolicyBuildPolicyBaselineTests(unittest.TestCase):
    """Validate build and ignore policy baseline data."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "BuildPolicyBaseline",
            "DEVELOPMENT_ONLY_WARN_PATTERNS",
            "FAIL_BEFORE_COMPILATION_PATTERNS",
            "GENERATED_INTENTIONAL_SOURCE_ALLOWLIST",
            "PACKAGING_EXCLUDE_PATTERNS",
            "POLICY_MODE_COMPILATION",
            "POLICY_MODE_DEV",
            "SECRET_EXCLUDE_HINT_PATTERNS",
            "describe_build_policy_baseline",
            "get_build_policy_baseline",
            "render_buildignore_baseline",
            "render_gitignore_baseline",
        }

        self.assertEqual(set(policy_module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(policy_module, name))

    def test_policy_modes_are_stable(self) -> None:
        self.assertEqual(POLICY_MODE_DEV, "dev")
        self.assertEqual(POLICY_MODE_COMPILATION, "compilation")

    def test_policy_constants_are_tuples(self) -> None:
        self.assertIsInstance(FAIL_BEFORE_COMPILATION_PATTERNS, tuple)
        self.assertIsInstance(DEVELOPMENT_ONLY_WARN_PATTERNS, tuple)
        self.assertIsInstance(PACKAGING_EXCLUDE_PATTERNS, tuple)
        self.assertIsInstance(GENERATED_INTENTIONAL_SOURCE_ALLOWLIST, tuple)
        self.assertIsInstance(SECRET_EXCLUDE_HINT_PATTERNS, tuple)

    def test_policy_contains_kanda_compilation_failures(self) -> None:
        policy = get_build_policy_baseline()

        self.assertIsInstance(policy, BuildPolicyBaseline)
        self.assertIn("*.bak", policy.fail_before_compilation)
        self.assertIn("*.backup", policy.fail_before_compilation)
        self.assertIn("*_old.*", policy.fail_before_compilation)
        self.assertIn("*_deprecated.*", policy.fail_before_compilation)
        self.assertIn("__pycache__/", policy.fail_before_compilation)
        self.assertIn(".pytest_cache/", policy.fail_before_compilation)
        self.assertIn("project_analysis_evidence/", policy.fail_before_compilation)
        self.assertIn("*_architecture_audit/", policy.fail_before_compilation)

    def test_workbench_is_warning_not_failure(self) -> None:
        policy = get_build_policy_baseline()

        self.assertIn("workbench/", policy.development_only_warnings)
        self.assertIn("workbench/bundle_manifest/", policy.development_only_warnings)
        self.assertNotIn("workbench/", policy.fail_before_compilation)
        self.assertNotIn(
            "workbench/bundle_manifest/",
            policy.fail_before_compilation,
        )

    def test_packaging_excludes_development_and_evidence_outputs(self) -> None:
        policy = get_build_policy_baseline()

        self.assertIn("workbench/", policy.packaging_excludes)
        self.assertIn("project_analysis_evidence/", policy.packaging_excludes)
        self.assertIn("*_architecture_audit/", policy.packaging_excludes)
        self.assertIn("*__complete.json", policy.packaging_excludes)

    def test_generated_intentional_source_allowlist_is_small(self) -> None:
        policy = get_build_policy_baseline()

        self.assertIn(
            "architecture_manifest.json",
            policy.generated_intentional_source_allowlist,
        )
        self.assertIn(
            "workflow_manifest.json",
            policy.generated_intentional_source_allowlist,
        )

    def test_rendered_baselines_are_suggestions_only(self) -> None:
        gitignore_text = render_gitignore_baseline()
        buildignore_text = render_buildignore_baseline()

        self.assertIn("Generated suggestion only", gitignore_text)
        self.assertIn("Generated suggestion only", buildignore_text)
        self.assertIn("project_analysis_evidence/", gitignore_text)
        self.assertIn("project_analysis_evidence/", buildignore_text)

    def test_describe_policy_returns_copy(self) -> None:
        first = describe_build_policy_baseline()
        second = describe_build_policy_baseline()

        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertIsInstance(first["packaging_excludes"], tuple)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = POLICY_SOURCE.read_text(encoding="utf-8")
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "C:\\",
            "C:/",
            "D:\\",
            "D:/",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
