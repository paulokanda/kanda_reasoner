# project-path: validation/test_architecture_review_large_file_refactor_preflight_backup_readiness_v1.py
"""Validate Workbench preflight backup readiness for Large File Refactor."""
from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ModuleAnalysisReport,
    PlannerSettings,
    ProposedModule,
    RefactorPlan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (
    validate_real_preview_structure,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (
    PREFLIGHT_BACKUP_READINESS_FEATURE_ID,
    build_and_write_preflight_backup_readiness,
)


def main() -> None:
    """Run focused validation checks."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "sample_project"
        root.mkdir()
        target = root / "large_target.py"
        target.write_text(_sample_source(), encoding="utf-8")
        source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        plan = _sample_plan(target, source_hash)
        analysis = _sample_analysis(target, source_hash)
        intake = build_workbench_plan_intake(
            plan=plan,
            analysis=analysis,
            active_project_root=str(root),
            planner_candidates=[SimpleNamespace(path=str(target))],
        )
        readiness = build_workbench_dependency_readiness(intake)
        preview = build_and_write_real_preview(
            plan=plan,
            intake=intake,
            dependency_readiness=readiness,
            active_project_root=str(root),
        )
        structural = validate_real_preview_structure(
            plan=plan,
            preview_result=preview,
            active_project_root=str(root),
        )
        result = build_and_write_preflight_backup_readiness(
            plan=plan,
            preview_result=preview,
            structural_validation=structural,
            active_project_root=str(root),
        )
        _expect(result.feature_id == PREFLIGHT_BACKUP_READINESS_FEATURE_ID, "unexpected feature id")
        _expect(result.status == "preflight_backup_ready", "preflight should be ready")
        _expect(result.source_hash_verified, "source hash should be verified")
        _expect(result.backup_snapshot_created, "backup snapshot should be created")
        _expect(result.backup_snapshot_verified, "backup snapshot should verify")
        _expect(result.ready_for_future_exact_token_apply, "future apply readiness should be marked")
        _expect(not result.source_mutation_enabled, "source mutation must remain disabled")
        _expect(not result.apply_enabled, "apply must remain disabled")
        _expect(not result.import_rewrite_enabled, "import rewrite must remain disabled")
        _expect(not result.blockers, "unexpected blockers: " + repr(result.blockers))
        manifest = Path(result.preflight_manifest_path)
        backup = Path(result.backup_snapshot_path)
        _expect(manifest.is_file(), "preflight manifest missing")
        _expect(backup.is_file(), "backup snapshot missing")
        _expect(hashlib.sha256(backup.read_bytes()).hexdigest() == source_hash, "backup hash mismatch")
        _expect(not str(manifest).startswith(str(root)), "manifest must stay outside source root")
    print("VALIDATION OK: architecture-review-large-file-refactor-preflight-backup-readiness-v1")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")


def _sample_source() -> str:
    """Return a sample target with one moved helper."""
    return '''"""Sample target module."""

import os

VALUE = 3


def run(value: int) -> int:
    """Public facade-owned function."""
    return helper(value) + VALUE


# important helper comment
def helper(value: int) -> int:
    return value + 1
'''


def _sample_plan(target: Path, source_hash: str) -> RefactorPlan:
    """Build a minimal valid split plan."""
    modules = [
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="large_target.py",
            role="public_facade",
            symbols=["run"],
            estimated_lines=30,
            exports=["run"],
            status="planned",
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_large_target_function.py",
            role="function_helper",
            symbols=["helper"],
            estimated_lines=20,
            status="planned",
            line_limit_justification="Small helper justified by dependency boundary.",
        ),
    ]
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        settings=PlannerSettings().to_dict(),
        public_api_before=["run"],
        public_api_after_expected=["run"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=modules,
        import_migration={"status": "preview_only"},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )


def _sample_analysis(target: Path, source_hash: str) -> ModuleAnalysisReport:
    """Build minimal analysis evidence with matching source hash."""
    return ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        line_count_physical=len(_sample_source().splitlines()),
        module_docstring_present=True,
        module_docstring_preview="Sample target module.",
        all_names=[],
        public_api_symbols=["run"],
        imports=[],
        symbols=[],
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )


def _expect(condition: bool, message: str) -> None:
    """Raise an assertion with a clear message."""
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    main()
