# project-path: tools/validate_architecture_review_large_file_refactor_preflight_backup_readiness_v1.py
"""Focused validation for Workbench preflight restoration and size-policy gates."""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (  # noqa: E402
    REAL_PREVIEW_FEATURE_ID,
    RealPreviewFile,
    RealPreviewWriteResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (  # noqa: E402
    ProposedModule,
    RefactorPlan,
    SCHEMA_VERSION,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.module_size_policy import (  # noqa: E402
    check_resulting_module_size,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import (  # noqa: E402
    resolve_preview_root,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (  # noqa: E402
    REAL_PREVIEW_VALIDATION_FEATURE_ID,
    RealPreviewStructuralValidationResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_dry_run_validator import (  # noqa: E402
    SourceApplyDryRunValidationResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_preflight_backup_contract import (  # noqa: E402
    build_source_apply_preflight_backup_contract,
    write_source_apply_preflight_backup_contract_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_basis import (  # noqa: E402
    build_workbench_execution_basis_set,
    execution_basis_is_fresh,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_feasibility import (  # noqa: E402
    evaluate_workbench_execution_feasibility,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_formatting import (  # noqa: E402
    format_preflight_gate_reason,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (  # noqa: E402
    build_and_write_preflight_backup_readiness,
)

FEATURE_ID = "architecture-review-large-file-refactor-preflight-backup-readiness-v1"


def main() -> int:
    """Run package import, boundary, readiness, drift, and collision checks."""
    _validate_package_import()
    _validate_strict_size_boundaries()
    with TemporaryDirectory(prefix="kanda_lfr_preflight_") as tmp:
        root = Path(tmp).resolve()
        project_root = root / "fixture_project"
        target_dir = project_root / "pkg"
        target_dir.mkdir(parents=True)
        target = target_dir / "large_module.py"
        source_text = _python_text("ORIGINAL", 130)
        target.write_text(source_text, encoding="utf-8")
        source_hash = _sha256(target)
        preview_root = Path(resolve_preview_root(str(project_root))).resolve()
        preview_root.mkdir(parents=True, exist_ok=True)
        facade_text = _python_text("FACADE", 130)
        helper_text = _python_text("HELPER", 140)
        facade = preview_root / target.name
        helper = preview_root / "_large_module_core.py"
        facade.write_text(facade_text, encoding="utf-8")
        helper.write_text(helper_text, encoding="utf-8")
        plan = _plan(target, source_hash)
        preview = _preview_result(target, source_hash, preview_root, facade, helper)
        structural = _structural_result(target, source_hash, preview_root)

        ready = build_and_write_preflight_backup_readiness(
            plan=plan,
            preview_result=preview,
            structural_validation=structural,
            active_project_root=str(project_root),
        )
        _assert_ready_result(ready, target, source_hash)
        _validate_source_drift(project_root, plan, preview, structural, target, source_text)
        _validate_preview_drift(project_root, plan, preview, structural, helper, helper_text)
        _validate_destination_collision(project_root, plan, preview, structural, target_dir)
        _validate_legacy_preflight_contract(project_root, target, source_hash)
        _validate_gate_reason_text()
        _validate_execution_basis_and_feasibility(project_root, plan, target)

    print("ZIP CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _validate_package_import() -> None:
    """Prove the package and both restored preflight owners import together."""
    package = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    )
    required = (
        "build_source_apply_preflight_backup_contract",
        "build_and_write_preflight_backup_readiness",
        "build_and_write_source_apply_payload",
    )
    missing = [name for name in required if not hasattr(package, name)]
    assert not missing, "PACKAGE_EXPORTS_MISSING:" + ",".join(missing)


def _validate_strict_size_boundaries() -> None:
    """Prove the canonical 101-499 contract at all four edge values."""
    expected = {
        100: False,
        101: True,
        499: True,
        500: False,
    }
    for count, valid in expected.items():
        text = _python_text("SIZE", count)
        result = check_resulting_module_size(
            text,
            relative_path=f"size_{count}.py",
        )
        assert result.physical_lines == count
        assert result.valid is valid, (count, result.to_dict())


def _plan(target: Path, source_hash: str) -> RefactorPlan:
    """Build a minimal immutable plan fixture for preflight validation."""
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id="fixture-plan",
        target_file=str(target.resolve()),
        source_content_hash=source_hash,
        settings={},
        public_api_before=[],
        public_api_after_expected=[],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[
            ProposedModule(
                schema_version=SCHEMA_VERSION,
                filename=target.name,
                role="public_facade",
                symbols=[],
                estimated_lines=130,
            ),
            ProposedModule(
                schema_version=SCHEMA_VERSION,
                filename="_large_module_core.py",
                role="core",
                symbols=[],
                estimated_lines=140,
            ),
        ],
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="ready",
    )


def _preview_result(
    target: Path,
    source_hash: str,
    preview_root: Path,
    facade: Path,
    helper: Path,
) -> RealPreviewWriteResult:
    """Build preview evidence whose hashes exactly match the fixture files."""
    files = [
        RealPreviewFile(
            relative_path=facade.name,
            role="public_facade",
            symbols=[],
            content_hash=_sha256(facade),
            physical_lines=len(facade.read_text(encoding="utf-8").splitlines()),
        ),
        RealPreviewFile(
            relative_path=helper.name,
            role="core",
            symbols=[],
            content_hash=_sha256(helper),
            physical_lines=len(helper.read_text(encoding="utf-8").splitlines()),
        ),
    ]
    return RealPreviewWriteResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_FEATURE_ID,
        status="real_preview_written",
        target_file=str(target.resolve()),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        libcst_available=False,
        files=files,
        written_files=[str(facade), str(helper)],
        source_mutation_enabled=False,
    )


def _structural_result(
    target: Path,
    source_hash: str,
    preview_root: Path,
) -> RealPreviewStructuralValidationResult:
    """Build accepted structural evidence for focused preflight testing."""
    return RealPreviewStructuralValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_VALIDATION_FEATURE_ID,
        status="passed_with_warnings",
        structural_status="STRUCTURAL_PASS_WITH_WARNINGS",
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        target_file=str(target.resolve()),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        source_hash_verified=True,
        source_mutation_enabled=False,
        import_migration_preview_status="ready",
        checked_files=[],
        report_files=[],
        file_results=[],
        blockers=[],
        warnings=["STRUCTURAL_VALIDATION_ONLY"],
    )


def _assert_ready_result(result: object, target: Path, source_hash: str) -> None:
    """Assert the ready path created verified recovery evidence only."""
    assert result.status == "preflight_backup_ready", result.blockers
    assert result.source_hash_verified
    assert result.preview_hashes_verified
    assert result.destination_collision_free
    assert result.backup_destination_writable
    assert result.backup_snapshot_verified
    assert result.rollback_manifest_prepared
    assert not result.source_mutation_enabled
    assert _sha256(target) == source_hash
    assert Path(result.backup_snapshot_path).is_file()
    assert _sha256(Path(result.backup_snapshot_path)) == source_hash
    assert Path(result.preflight_manifest_path).is_file()
    assert Path(result.rollback_manifest_path).is_file()


def _validate_source_drift(
    project_root: Path,
    plan: RefactorPlan,
    preview: RealPreviewWriteResult,
    structural: RealPreviewStructuralValidationResult,
    target: Path,
    source_text: str,
) -> None:
    """Prove external source drift blocks preflight readiness."""
    target.write_text(source_text + "# external drift\n", encoding="utf-8")
    result = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=str(project_root),
    )
    assert result.status == "blocked"
    assert "SOURCE_DRIFT_DETECTED" in result.blockers
    target.write_text(source_text, encoding="utf-8")


def _validate_preview_drift(
    project_root: Path,
    plan: RefactorPlan,
    preview: RealPreviewWriteResult,
    structural: RealPreviewStructuralValidationResult,
    helper: Path,
    helper_text: str,
) -> None:
    """Prove changed preview bytes invalidate readiness."""
    helper.write_text(helper_text + "# preview drift\n", encoding="utf-8")
    result = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=str(project_root),
    )
    assert result.status == "blocked"
    assert any(item.startswith("PREVIEW_HASH_CHANGED:") for item in result.blockers)
    helper.write_text(helper_text, encoding="utf-8")


def _validate_destination_collision(
    project_root: Path,
    plan: RefactorPlan,
    preview: RealPreviewWriteResult,
    structural: RealPreviewStructuralValidationResult,
    target_dir: Path,
) -> None:
    """Prove an existing helper destination blocks readiness."""
    collision = target_dir / "_large_module_core.py"
    collision.write_text("# existing helper\n", encoding="utf-8")
    result = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=str(project_root),
    )
    assert result.status == "blocked"
    assert "DESTINATION_HELPER_COLLISION:_large_module_core.py" in result.blockers
    collision.unlink()


def _validate_legacy_preflight_contract(
    project_root: Path,
    target: Path,
    source_hash: str,
) -> None:
    """Prove the legacy owner accepts canonical Project Support preview evidence."""
    preview_root = (
        project_root.parent
        / (project_root.name + "_show_project_to_AI")
        / "large_file_refactor_workbench"
        / "preview"
        / "legacy_fixture"
    )
    preview_root.mkdir(parents=True, exist_ok=True)
    dry_run_manifest = preview_root / "SOURCE_APPLY_DRY_RUN_VALIDATION.json"
    dry_run_manifest.write_text(json.dumps({"status": "validated"}) + "\n", encoding="utf-8")
    dry_run = SourceApplyDryRunValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id="legacy-fixture",
        status="source_apply_dry_run_validated",
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_zip_path=str(preview_root / "payload.zip"),
        final_plan_manifest_path=str(preview_root / "final-plan.json"),
        dry_run_manifest_path=str(dry_run_manifest),
        confirmation_token_required="fixture",
        dry_run_confirmation_present=True,
        dry_run_confirmation_valid=True,
        blockers=[],
    )
    result = build_source_apply_preflight_backup_contract(
        dry_run,
        active_project_root=str(project_root),
    )
    assert result.status == "source_apply_preflight_backup_ready", result.blockers
    manifest = write_source_apply_preflight_backup_contract_manifest(result)
    assert manifest.is_file()
    assert result.backup_snapshot_verified


def _validate_gate_reason_text() -> None:
    """Prove explicit Preflight gate diagnostics remain machine-readable."""
    blocked = format_preflight_gate_reason("blocked")
    assert "REAL_PREVIEW_STRUCTURAL_VALIDATION_NOT_ACCEPTED" in blocked
    ready = format_preflight_gate_reason("passed_with_warnings")
    assert "AQR_REQUIRED" in ready
    assert "PREFLIGHT_AVAILABLE" not in ready



def _validate_execution_basis_and_feasibility(
    project_root: Path,
    plan: RefactorPlan,
    target: Path,
) -> None:
    """Prove basis hashing, drift detection, fitness gates, and Compliance Veto."""
    basis = build_workbench_execution_basis_set(
        plan=plan,
        active_project_root=str(project_root),
    )
    assert basis.status == "execution_basis_ready", basis.blockers
    fresh, blockers = execution_basis_is_fresh(basis)
    assert fresh, blockers
    feasible = evaluate_workbench_execution_feasibility(
        plan=plan,
        execution_basis=basis,
    )
    assert feasible.verdict == "EXECUTABLE", feasible.blockers
    assert feasible.compliance_veto is None
    target.write_text(target.read_text(encoding="utf-8") + "# basis drift\n", encoding="utf-8")
    fresh, blockers = execution_basis_is_fresh(basis)
    assert not fresh
    assert any(item.startswith("BASIS_HASH_CHANGED:") for item in blockers)
    target.write_text(_python_text("ORIGINAL", 130), encoding="utf-8")
    invalid_plan = RefactorPlan(
        schema_version=plan.schema_version,
        feature_id=plan.feature_id,
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        settings=dict(plan.settings),
        public_api_before=list(plan.public_api_before),
        public_api_after_expected=list(plan.public_api_after_expected),
        symbols=list(plan.symbols),
        atomic_clusters=list(plan.atomic_clusters),
        proposed_modules=[
            ProposedModule(
                schema_version=SCHEMA_VERSION,
                filename="too_small.py",
                role="core",
                symbols=[],
                estimated_lines=100,
            )
        ],
        import_migration=dict(plan.import_migration),
        docstring_proposals=list(plan.docstring_proposals),
        risks=list(plan.risks),
        validation_blockers=list(plan.validation_blockers),
        status=plan.status,
    )
    invalid_basis = build_workbench_execution_basis_set(
        plan=invalid_plan,
        active_project_root=str(project_root),
    )
    blocked = evaluate_workbench_execution_feasibility(
        plan=invalid_plan,
        execution_basis=invalid_basis,
    )
    assert blocked.verdict == "PLAN_CORRECTION_REQUIRED"
    assert blocked.compliance_veto is not None
    assert blocked.compliance_veto.workbench_architecture_mutation_allowed is False
    assert "too_small.py" in blocked.compliance_veto.affected_modules

def _python_text(label: str, physical_lines: int) -> str:
    """Return valid Python text with exactly the requested splitlines count."""
    if physical_lines < 1:
        return ""
    lines = [f'"""{label} fixture."""']
    for index in range(1, physical_lines):
        lines.append(f"VALUE_{index} = {index}")
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    """Return SHA-256 for one fixture file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
