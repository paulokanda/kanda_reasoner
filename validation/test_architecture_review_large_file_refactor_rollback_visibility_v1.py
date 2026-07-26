# project-path: validation/test_architecture_review_large_file_refactor_rollback_visibility_v1.py
"""Validate rollback visibility and exact-token recovery for Workbench source apply."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import SCHEMA_VERSION
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_guarded_source_apply import (
    execute_guarded_source_apply,
    expected_guarded_apply_token,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator import (
    validate_and_write_post_apply,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (
    WorkbenchPreflightBackupReadinessResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_rollback_executor import (
    execute_workbench_rollback,
    expected_workbench_rollback_token,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder import (
    SourceApplyPayloadFile,
    SourceApplyPayloadReadinessResult,
)

FEATURE_ID = "architecture-review-large-file-refactor-rollback-visibility-v1"


def main() -> None:
    """Run exact-token rollback checks."""
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp)
        project = base / "demo_project"
        project.mkdir()
        target = project / "target_module.py"
        original = "def kept():\n    return 'old'\n"
        target.write_text(original, encoding="utf-8")
        source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        preview_root = base / "demo_project_delete_after_daily_work" / "large_file_refactor_preview" / "case"
        payload_root = preview_root / "source_apply_payload"
        payload_root.mkdir(parents=True)
        facade_text = "def kept():\n    return 'new'\nfrom ._target_module_moved import moved\n"
        helper_text = "def moved():\n    return 'moved'\n"
        facade = payload_root / "target_module.py"
        helper = payload_root / "_target_module_moved.py"
        facade.write_text(facade_text, encoding="utf-8")
        helper.write_text(helper_text, encoding="utf-8")
        payload = _payload(target, source_hash, preview_root, facade, helper)
        preflight = _preflight(target, source_hash, preview_root)
        apply_result = execute_guarded_source_apply(
            source_payload=payload,
            preflight_backup=preflight,
            active_project_root=str(project),
            confirmation_token=expected_guarded_apply_token(payload),
        )
        _expect(apply_result.status == "applied", "apply failed: " + repr(apply_result.blockers))
        post = validate_and_write_post_apply(
            apply_result=apply_result,
            source_payload=payload,
            active_project_root=str(project),
        )
        _expect(post.status == "post_apply_validated", "post apply failed: " + repr(post.blockers))
        wrong = execute_workbench_rollback(
            apply_result=apply_result,
            source_payload=payload,
            active_project_root=str(project),
            confirmation_token="wrong-token",
        )
        _expect(wrong.status == "blocked", "wrong rollback token should block")
        _expect(target.read_text(encoding="utf-8") == facade_text, "wrong token restored source")
        rollback = execute_workbench_rollback(
            apply_result=apply_result,
            source_payload=payload,
            active_project_root=str(project),
            confirmation_token=expected_workbench_rollback_token(apply_result),
        )
        _expect(rollback.status == "rollback_completed", "rollback failed: " + repr(rollback.blockers))
        _expect(target.read_text(encoding="utf-8") == original, "target source not restored")
        _expect(not (project / "_target_module_moved.py").exists(), "generated helper not removed")
        _expect(rollback.selected_source_restored, "rollback did not prove source restoration")
        _expect(rollback.backup_snapshot_verified, "backup snapshot not verified")
        _expect(not rollback.import_rewrite_enabled, "import rewrite rollback must remain disabled")
        _expect(Path(rollback.rollback_report_path).is_file(), "rollback report missing")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")


def _payload(
    target: Path,
    source_hash: str,
    preview_root: Path,
    facade: Path,
    helper: Path,
) -> SourceApplyPayloadReadinessResult:
    """Build a source-payload fixture."""
    files = [
        SourceApplyPayloadFile(
            payload_path=str(facade),
            destination_path=str(target),
            relative_path="target_module.py",
            content_hash=_hash_text(facade.read_text(encoding="utf-8")),
            physical_lines=3,
            compile_ok=True,
            ast_parse_ok=True,
            role="public_facade",
            symbols=["kept"],
        ),
        SourceApplyPayloadFile(
            payload_path=str(helper),
            destination_path=str(target.parent / "_target_module_moved.py"),
            relative_path="_target_module_moved.py",
            content_hash=_hash_text(helper.read_text(encoding="utf-8")),
            physical_lines=2,
            compile_ok=True,
            ast_parse_ok=True,
            role="domain_helper",
            symbols=["moved"],
        ),
    ]
    return SourceApplyPayloadReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id="fixture",
        status="source_apply_payload_ready",
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_root=str(preview_root / "source_apply_payload"),
        payload_manifest_path=str(preview_root / "SOURCE_APPLY_PAYLOAD_MANIFEST.json"),
        structural_validation_status="STRUCTURAL_PASS_WITH_WARNINGS",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        preflight_backup_status="preflight_backup_ready",
        source_hash_verified=True,
        files=files,
        blockers=[],
        warnings=[],
    )


def _preflight(target: Path, source_hash: str, preview_root: Path) -> WorkbenchPreflightBackupReadinessResult:
    """Build a preflight fixture with source backup."""
    backup = preview_root / "SOURCE_APPLY_BACKUP_SNAPSHOT.py"
    backup.parent.mkdir(parents=True, exist_ok=True)
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


def _hash_text(text: str) -> str:
    """Return SHA-256 over UTF-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _expect(condition: bool, message: str) -> None:
    """Raise AssertionError when condition is false."""
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    main()
