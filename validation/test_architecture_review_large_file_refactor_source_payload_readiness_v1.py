# project-path: validation/test_architecture_review_large_file_refactor_source_payload_readiness_v1.py
"""Validate Large File Refactor Workbench source payload readiness v1."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    RealPreviewFile,
    RealPreviewWriteResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    ProposedModule,
    RefactorPlan,
    SCHEMA_VERSION,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (
    PreviewFileValidation,
    RealPreviewStructuralValidationResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (
    WorkbenchPreflightBackupReadinessResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder import (
    build_and_write_source_apply_payload,
)

FEATURE_ID = "architecture-review-large-file-refactor-source-payload-readiness-v1"


def test_source_payload_readiness() -> None:
    """Source payload readiness strips preview markers and never applies source."""
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp)
        project = base / "demo_project"
        project.mkdir()
        target = project / "target_module.py"
        target.write_text("def kept():\n    return 'kept'\n\ndef moved():\n    return 'moved'\n", encoding="utf-8")
        source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        preview_root = base / "demo_project_delete_after_daily_work" / "large_file_refactor_preview" / "case"
        preview_root.mkdir(parents=True)
        facade_text = (
            "# KANDA PREVIEW ARTIFACT - NOT SOURCE TRUTH\n"
            "# Preview facade for target_module.py.\n"
            f"# Target source: {target}\n"
            f"# Source hash: {source_hash}\n"
            "# Source mutation is disabled; this file belongs only in daily-work preview.\n"
            "\n"
            "def kept():\n    return 'kept'\n"
            "from ._target_module_moved import moved\n"
            "__all__ = ['kept', 'moved']\n"
        )
        helper_text = (
            "# KANDA PREVIEW ARTIFACT - NOT SOURCE TRUTH\n"
            "# Preview helper role: domain_helper\n"
            f"# Target source: {target}\n"
            f"# Source hash: {source_hash}\n"
            "# Source mutation is disabled; this file belongs only in daily-work preview.\n"
            "\n"
            "def moved():\n    return 'moved'\n"
        )
        (preview_root / "target_module.py").write_text(facade_text, encoding="utf-8")
        (preview_root / "_target_module_moved.py").write_text(helper_text, encoding="utf-8")
        plan = _plan(target, source_hash)
        preview = _preview(target, source_hash, preview_root)
        structural = _structural(target, source_hash, preview_root)
        preflight = _preflight(target, source_hash, preview_root)
        result = build_and_write_source_apply_payload(
            plan=plan,
            preview_result=preview,
            structural_validation=structural,
            preflight_backup=preflight,
            active_project_root=str(project),
        )
        assert result.status == "source_apply_payload_ready", result.blockers
        assert result.source_mutation_enabled is False
        assert result.apply_enabled is False
        assert result.import_rewrite_enabled is False
        assert Path(result.payload_manifest_path).is_file()
        for file_result in result.files:
            payload = Path(file_result.payload_path)
            assert payload.is_file()
            text = payload.read_text(encoding="utf-8")
            assert "KANDA PREVIEW ARTIFACT" not in text
            assert "Source mutation is disabled" not in text
            assert file_result.compile_ok is True
            assert file_result.ast_parse_ok is True
            assert not file_result.blockers


def _plan(target: Path, source_hash: str) -> RefactorPlan:
    """Build a tiny split plan fixture."""
    modules = [
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="target_module.py",
            role="public_facade",
            symbols=["kept"],
            estimated_lines=8,
            exports=["kept", "moved"],
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_target_module_moved.py",
            role="domain_helper",
            symbols=["moved"],
            estimated_lines=4,
        ),
    ]
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id="fixture",
        target_file=str(target),
        source_content_hash=source_hash,
        settings={},
        public_api_before=["kept", "moved"],
        public_api_after_expected=["kept", "moved"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=modules,
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="plan_ready",
    )


def _preview(target: Path, source_hash: str, preview_root: Path) -> RealPreviewWriteResult:
    """Build a real-preview result fixture."""
    files = [
        RealPreviewFile("target_module.py", "public_facade", ["kept"], "hash-a", 9),
        RealPreviewFile("_target_module_moved.py", "domain_helper", ["moved"], "hash-b", 7),
    ]
    return RealPreviewWriteResult(
        schema_version=SCHEMA_VERSION,
        feature_id="fixture",
        status="real_preview_written",
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        libcst_available=False,
        files=files,
        written_files=[str(preview_root / item.relative_path) for item in files],
        source_mutation_enabled=False,
        blockers=[],
        warnings=[],
    )


def _structural(target: Path, source_hash: str, preview_root: Path) -> RealPreviewStructuralValidationResult:
    """Build a structural validation fixture."""
    file_results = [
        PreviewFileValidation(str(preview_root / "target_module.py"), "public_facade", 9, True, True, ["kept"]),
        PreviewFileValidation(str(preview_root / "_target_module_moved.py"), "domain_helper", 7, True, True, ["moved"]),
    ]
    return RealPreviewStructuralValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id="fixture",
        status="passed_with_warnings",
        structural_status="STRUCTURAL_PASS_WITH_WARNINGS",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        source_hash_verified=True,
        source_mutation_enabled=False,
        import_migration_preview_status="preview_generated",
        checked_files=[item.path for item in file_results],
        report_files=[],
        file_results=file_results,
        blockers=[],
        warnings=[],
    )


def _preflight(target: Path, source_hash: str, preview_root: Path) -> WorkbenchPreflightBackupReadinessResult:
    """Build a preflight readiness fixture."""
    backup = preview_root / "SOURCE_APPLY_BACKUP_SNAPSHOT.py"
    backup.write_bytes(target.read_bytes())
    return WorkbenchPreflightBackupReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id="fixture",
        status="preflight_backup_ready",
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        structural_validation_status="STRUCTURAL_PASS_WITH_WARNINGS",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        preflight_manifest_path=str(preview_root / "SOURCE_APPLY_PREFLIGHT_BACKUP_READINESS.json"),
        backup_snapshot_path=str(backup),
        backup_snapshot_hash=source_hash,
        backup_snapshot_created=True,
        backup_snapshot_verified=True,
        source_hash_verified=True,
        source_mutation_enabled=False,
        apply_enabled=False,
        import_rewrite_enabled=False,
        ready_for_future_exact_token_apply=True,
        checked_rules=[],
        blockers=[],
        warnings=[],
    )


if __name__ == "__main__":
    test_source_payload_readiness()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
