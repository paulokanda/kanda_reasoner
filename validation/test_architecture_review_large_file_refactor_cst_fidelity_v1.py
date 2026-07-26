# project-path: validation/test_architecture_review_large_file_refactor_cst_fidelity_v1.py
"""Focused validation for Workbench real-preview CST fidelity train."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_symbol_source_extractor import (
    extract_source_blocks,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    ProposedModule,
    RefactorPlan,
    SCHEMA_VERSION,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import resolve_preview_root
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    WorkbenchDependencyReadinessResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    WorkbenchPlanIntakeResult,
)


class CstFidelityPreviewTests(unittest.TestCase):
    """Validate stronger extraction fidelity without source mutation."""

    def test_extractor_preserves_decorator_comments_and_class_body(self) -> None:
        """Moved symbols should keep decorators, attached comments, and body text."""
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "big_module.py"
            target.write_text(_source_text(), encoding="utf-8")
            result = extract_source_blocks(target, {"alpha", "Beta"})
            self.assertFalse(result.blockers)
            self.assertIn(result.extraction_backend, {"ast_source_span_fallback", "libcst_position_provider"})
            alpha = result.symbol_blocks["alpha"]
            beta = result.symbol_blocks["Beta"]
            self.assertIn("# attached alpha comment", alpha)
            self.assertIn("@decorator", alpha)
            self.assertIn("def alpha", alpha)
            self.assertIn("class Beta", beta)
            self.assertIn("def value", beta)
            self.assertTrue(any("import os" in item for item in result.import_blocks))

    def test_real_preview_manifest_records_extraction_backend(self) -> None:
        """Real preview output should contain real bodies and fidelity metadata."""
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            package = project_root / "pkg"
            package.mkdir(parents=True)
            target = package / "big_module.py"
            target.write_text(_source_text(), encoding="utf-8")
            source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            plan = _plan(target, source_hash)
            preview_root = Path(resolve_preview_root(str(project_root)))
            intake = _intake(project_root, target, source_hash)
            readiness = _readiness(target, source_hash)
            result = build_and_write_real_preview(
                plan=plan,
                intake=intake,
                dependency_readiness=readiness,
                active_project_root=str(project_root),
                preview_root=str(preview_root),
            )
            self.assertEqual(result.status, "real_preview_written")
            self.assertFalse(result.source_mutation_enabled)
            self.assertIn(result.extraction_backend, {"ast_source_span_fallback", "libcst_position_provider"})
            helper_text = (preview_root / "big_module_core.py").read_text(encoding="utf-8")
            facade_text = (preview_root / "big_module.py").read_text(encoding="utf-8")
            self.assertIn("# Extraction backend:", helper_text)
            self.assertIn("# attached alpha comment", helper_text)
            self.assertIn("@decorator", helper_text)
            self.assertIn("class Beta", helper_text)
            self.assertIn("from .big_module_core import alpha", facade_text)
            self.assertIn("CST_FIDELITY_METADATA_ENABLED", result.warnings)


def _source_text() -> str:
    """Return a compact target source with fidelity-sensitive syntax."""
    return (
        "from __future__ import annotations\n"
        "import os\n"
        "\n"
        "CONSTANT = os.name\n"
        "\n"
        "def decorator(func):\n"
        "    return func\n"
        "\n"
        "# attached alpha comment\n"
        "@decorator\n"
        "def alpha(value: int) -> int:\n"
        "    # keep this body comment\n"
        "    return value + 1\n"
        "\n"
        "class Beta:\n"
        "    @property\n"
        "    def value(self) -> int:\n"
        "        return alpha(1)\n"
    )


def _plan(target: Path, source_hash: str) -> RefactorPlan:
    """Build a minimal plan that moves two symbols into a helper."""
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-planner-v1",
        target_file=str(target),
        source_content_hash=source_hash,
        settings={},
        public_api_before=["alpha", "Beta"],
        public_api_after_expected=["alpha", "Beta"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[
            ProposedModule(SCHEMA_VERSION, "big_module.py", "public_facade", ["alpha", "Beta"], 80),
            ProposedModule(SCHEMA_VERSION, "big_module_core.py", "helper", ["alpha", "Beta"], 140),
        ],
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )


def _intake(project_root: Path, target: Path, source_hash: str) -> WorkbenchPlanIntakeResult:
    """Return a ready intake result for preview generation tests."""
    return WorkbenchPlanIntakeResult(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-workbench-intake-v1",
        status="plan_intake_ready",
        active_project_root=str(project_root),
        target_file=str(target),
        source_content_hash=source_hash,
        current_source_content_hash=source_hash,
        source_hash_fresh=True,
        planner_status="planned",
        planner_candidate_verified=True,
        ready_for_real_preview=True,
    )


def _readiness(target: Path, source_hash: str) -> WorkbenchDependencyReadinessResult:
    """Return a ready dependency-readiness result for preview generation tests."""
    return WorkbenchDependencyReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-workbench-intake-v1",
        status="dependency_readiness_ready",
        target_file=str(target),
        source_content_hash=source_hash,
        ready_for_real_preview_writer=True,
    )


if __name__ == "__main__":
    unittest.main()
