# project-path: validation/test_architecture_review_large_file_refactor_helper_import_synthesis_v1.py
"""Focused validation for helper dependency/import synthesis depth."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.helper_import_synthesizer import (
    synthesize_helper_imports,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    ProposedModule,
    RefactorPlan,
    SCHEMA_VERSION,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import resolve_preview_root
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.symbol_dependency_builder import (
    build_symbol_dependency_report,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    WorkbenchDependencyReadinessResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    WorkbenchPlanIntakeResult,
)


class HelperImportSynthesisTests(unittest.TestCase):
    """Validate helper imports are synthesized from dependency evidence."""

    def test_synthesizer_selects_only_required_import_blocks(self) -> None:
        """A helper should receive imports used by its moved symbols only."""
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "big_module.py"
            target.write_text(_source_text(), encoding="utf-8")
            source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            plan = _plan(target, source_hash)
            dependency_report = build_symbol_dependency_report(target)
            readiness = _readiness(target, source_hash, dependency_report)
            imports = [
                "from __future__ import annotations",
                "import os",
                "import json as js",
                "from pathlib import Path",
            ]
            result = synthesize_helper_imports(plan=plan, readiness=readiness, import_blocks=imports)
            self.assertEqual(result.status, "helper_import_synthesis_ready")
            self.assertFalse(result.source_mutation_enabled)
            helper_imports = result.imports_for_module("big_module_core.py")
            self.assertIn("from __future__ import annotations", helper_imports)
            self.assertIn("import os", helper_imports)
            self.assertIn("from pathlib import Path", helper_imports)
            self.assertNotIn("import json as js", helper_imports)

    def test_real_preview_manifest_records_helper_import_synthesis(self) -> None:
        """Real preview manifest should include helper import synthesis metadata."""
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            package = project_root / "pkg"
            package.mkdir(parents=True)
            target = package / "big_module.py"
            target.write_text(_source_text(), encoding="utf-8")
            source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            plan = _plan(target, source_hash)
            preview_root = Path(resolve_preview_root(str(project_root)))
            dependency_report = build_symbol_dependency_report(target)
            result = build_and_write_real_preview(
                plan=plan,
                intake=_intake(project_root, target, source_hash),
                dependency_readiness=_readiness(target, source_hash, dependency_report),
                active_project_root=str(project_root),
                preview_root=str(preview_root),
            )
            self.assertEqual(result.status, "real_preview_written")
            helper_text = (preview_root / "big_module_core.py").read_text(encoding="utf-8")
            self.assertIn("import os", helper_text)
            self.assertIn("from pathlib import Path", helper_text)
            self.assertNotIn("import json as js", helper_text)
            manifest = json.loads((preview_root / "REAL_PREVIEW_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["helper_import_synthesis_enabled"])
            self.assertEqual(manifest["helper_import_synthesis"]["status"], "helper_import_synthesis_ready")
            self.assertIn("HELPER_IMPORT_SYNTHESIS_METADATA_ENABLED", manifest["warnings"])


def _source_text() -> str:
    """Return source with multiple import dependencies."""
    return (
        "from __future__ import annotations\n"
        "import os\n"
        "import json as js\n"
        "from pathlib import Path\n"
        "\n"
        "def alpha(value: str) -> Path:\n"
        "    return Path(os.path.join(value, 'x'))\n"
        "\n"
        "def beta(value: object) -> str:\n"
        "    return js.dumps(value)\n"
    )


def _plan(target: Path, source_hash: str) -> RefactorPlan:
    """Build a minimal plan that moves alpha only."""
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-planner-v1",
        target_file=str(target),
        source_content_hash=source_hash,
        settings={},
        public_api_before=["alpha", "beta"],
        public_api_after_expected=["alpha", "beta"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[
            ProposedModule(SCHEMA_VERSION, "big_module.py", "public_facade", ["alpha"], 60),
            ProposedModule(SCHEMA_VERSION, "big_module_core.py", "helper", ["alpha"], 120),
        ],
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )


def _intake(project_root: Path, target: Path, source_hash: str) -> WorkbenchPlanIntakeResult:
    """Return a ready intake result."""
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


def _readiness(target: Path, source_hash: str, report: object) -> WorkbenchDependencyReadinessResult:
    """Return dependency readiness with dependency report evidence."""
    return WorkbenchDependencyReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id="architecture-review-large-file-refactor-workbench-intake-v1",
        status="dependency_readiness_ready",
        target_file=str(target),
        source_content_hash=source_hash,
        dependency_report=report,
        ready_for_real_preview_writer=True,
    )


if __name__ == "__main__":
    unittest.main()
