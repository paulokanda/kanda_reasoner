# project-path: validation/test_architecture_review_large_file_refactor_behavior_validation_v1.py
"""Focused validation for Workbench optional behavior validation."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_behavior_validation import (
    run_workbench_behavior_validation,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_guarded_source_apply import (
    GuardedSourceApplyResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator import (
    PostApplyValidationResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder import (
    SourceApplyPayloadReadinessResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import SCHEMA_VERSION

FEATURE_MARKER = "architecture-review-large-file-refactor-behavior-validation-v1"


class BehaviorValidationTrainTests(unittest.TestCase):
    """Validate optional behavior/test validation gates."""

    def test_not_run_does_not_claim_behavior(self) -> None:
        """Empty command writes evidence but does not claim behavior equivalence."""
        with tempfile.TemporaryDirectory() as raw:
            project = _make_project(Path(raw))
            apply_result, post_apply, payload = _make_prerequisites(project)
            result = run_workbench_behavior_validation(
                apply_result=apply_result,
                post_apply_validation=post_apply,
                source_payload=payload,
                active_project_root=str(project),
                test_command="",
            )
            self.assertEqual(result.status, "behavior_validation_not_run")
            self.assertFalse(result.behavior_validation_claimed)
            self.assertTrue(Path(result.report_path).is_file())

    def test_blocks_non_allowlisted_command(self) -> None:
        """Behavior validation refuses shell-style arbitrary commands."""
        with tempfile.TemporaryDirectory() as raw:
            project = _make_project(Path(raw))
            apply_result, post_apply, payload = _make_prerequisites(project)
            result = run_workbench_behavior_validation(
                apply_result=apply_result,
                post_apply_validation=post_apply,
                source_payload=payload,
                active_project_root=str(project),
                test_command="cmd /c echo unsafe",
            )
            self.assertEqual(result.status, "blocked")
            self.assertIn("COMMAND_NOT_ALLOWLISTED_FOR_BEHAVIOR_VALIDATION", result.blockers)
            self.assertFalse(result.behavior_validation_claimed)

    def test_unittest_pass_claims_behavior_validation(self) -> None:
        """Passing allow-listed tests produce BEHAVIOR_VALIDATED_PASS evidence."""
        with tempfile.TemporaryDirectory() as raw:
            project = _make_project(Path(raw))
            tests = project / "tests"
            tests.mkdir()
            (tests / "test_ok.py").write_text(
                "import unittest\n\nclass Ok(unittest.TestCase):\n"
                "    def test_ok(self):\n        self.assertEqual(1 + 1, 2)\n",
                encoding="utf-8",
            )
            apply_result, post_apply, payload = _make_prerequisites(project)
            result = run_workbench_behavior_validation(
                apply_result=apply_result,
                post_apply_validation=post_apply,
                source_payload=payload,
                active_project_root=str(project),
                test_command=sys.executable + " -m unittest discover -s tests",
            )
            self.assertEqual(result.status, "behavior_validated_pass")
            self.assertEqual(result.behavior_status, "BEHAVIOR_VALIDATED_PASS")
            self.assertTrue(result.behavior_validation_claimed)


def _make_project(root: Path) -> Path:
    """Create a tiny temporary project root."""
    project = root / "demo_project"
    project.mkdir()
    (project / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    return project


def _make_prerequisites(project: Path):
    """Create prerequisite dataclass instances for behavior validation."""
    preview_root = project.parent / (project.name + "_delete_after_daily_work") / "large_file_refactor_preview"
    preview_root.mkdir(parents=True)
    target = project / "module.py"
    digest = hashlib.sha256(target.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    apply_result = GuardedSourceApplyResult(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-guarded-source-apply-v1",
        status="applied",
        target_file=str(target),
        source_content_hash_before=digest,
        source_content_hash_after=digest,
        preview_root=str(preview_root),
        payload_manifest_path=str(preview_root / "SOURCE_APPLY_PAYLOAD_MANIFEST.json"),
        rollback_manifest_path=str(preview_root / "SOURCE_APPLY_ROLLBACK_MANIFEST.json"),
        execution_manifest_path=str(preview_root / "SOURCE_APPLY_EXECUTION_MANIFEST.json"),
        expected_confirmation_token="TOKEN",
        confirmation_token_present=True,
        confirmation_token_valid=True,
        source_mutation_enabled=True,
        import_rewrite_enabled=False,
    )
    post_apply = PostApplyValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-post-apply-validation-v1",
        status="post_apply_validated",
        structural_status="STRUCTURAL_PASS_WITH_WARNINGS",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        target_file=str(target),
        preview_root=str(preview_root),
        report_path=str(preview_root / "SOURCE_APPLY_POST_APPLY_VALIDATION.json"),
        rollback_manifest_path=str(preview_root / "SOURCE_APPLY_ROLLBACK_MANIFEST.json"),
    )
    payload = SourceApplyPayloadReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-source-payload-readiness-v1",
        status="source_apply_payload_ready",
        target_file=str(target),
        source_content_hash=digest,
        preview_root=str(preview_root),
        payload_root=str(preview_root / "source_apply_payload"),
        payload_manifest_path=str(preview_root / "SOURCE_APPLY_PAYLOAD_MANIFEST.json"),
        structural_validation_status="passed_with_warnings",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        preflight_backup_status="preflight_backup_ready",
        source_hash_verified=True,
    )
    return apply_result, post_apply, payload


if __name__ == "__main__":
    unittest.main()
