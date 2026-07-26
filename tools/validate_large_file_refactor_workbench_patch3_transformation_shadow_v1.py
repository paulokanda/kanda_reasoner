# project-path: tools/validate_large_file_refactor_workbench_patch3_transformation_shadow_v1.py
"""Focused validator for Patch 3 transformation truth and shadow runtime."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    ProposedModule,
    RefactorPlan,
    SCHEMA_VERSION,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (
    export_latest_planner_workbench_handoff,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (
    validate_real_preview_structure,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import (
    resolve_preview_root,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dynamic_python_risks import (
    analyze_dynamic_python_risks,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_basis import (
    build_workbench_execution_basis_set,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_contract import (
    build_workbench_execution_contract,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_feasibility import (
    evaluate_workbench_execution_feasibility,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (
    build_workbench_plan_snapshot,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (
    build_and_write_preflight_backup_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_baseline import (
    BehaviorBaselineEvidence,
    build_refactor_baseline,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_sealed_payload import (
    build_and_write_sealed_payload,
    verify_sealed_payload,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_shadow_backend import (
    ControlledMirrorBackend,
    GitWorktreeBackend,
    choose_shadow_backend,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_shadow_provenance import (
    prove_shadow_runtime_provenance,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_shadow_validation import (
    validate_shadow_refactor,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder import (
    build_and_write_source_apply_payload,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transformation_recipe import (
    build_transformation_recipe,
)

FEATURE_MARKER = (
    "architecture-review-large-file-refactor-workbench-patch3-"
    "transformation-truth-shadow-runtime-v1"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _large_function(name: str, steps: int = 112) -> str:
    lines = [f"def {name}():", f'    \"\"\"Return deterministic value for {name}.\"\"\"', "    value = 0"]
    for index in range(1, steps + 1):
        lines.append(f"    value += {index}")
    lines.append("    return value")
    return "\n".join(lines)


def _source_text() -> str:
    parts = [
        '"""Large fixture module for Patch 3 transformation validation."""',
        "",
        "__all__ = ['alpha', 'beta', 'facade_support']",
        "",
        _large_function("facade_support"),
        "",
        _large_function("alpha"),
        "",
        _large_function("beta"),
        "",
    ]
    return "\n".join(parts)


def _test_text() -> str:
    expected = sum(range(1, 113))
    return (
        "from fixture_pkg.large_module import alpha, beta, facade_support\n\n"
        "def test_public_behavior():\n"
        f"    assert alpha() == {expected}\n"
        f"    assert beta() == {expected}\n"
        f"    assert facade_support() == {expected}\n"
    )


def _baseline_behavior(project_root: Path, test_file: Path) -> BehaviorBaselineEvidence:
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(test_file)],
        cwd=str(project_root),
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    digest = hashlib.sha256((completed.stdout + "\n" + completed.stderr).encode("utf-8")).hexdigest()
    return BehaviorBaselineEvidence(
        status="BEHAVIOR_BASELINE_PASS",
        collected_tests=(str(test_file.resolve()),),
        exit_code=completed.returncode,
        output_hash=digest,
    )


def _build_snapshot(target: Path):
    analysis = analyze_python_file(target)
    assert not analysis.analysis_errors, analysis.analysis_errors
    symbol_names = {symbol.name for symbol in analysis.symbols}
    assert {"alpha", "beta", "facade_support"}.issubset(symbol_names)
    source_hash = _sha(target)
    modules = [
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename=target.name,
            role="public_facade",
            symbols=["facade_support"],
            estimated_lines=130,
            exports=["alpha", "beta", "facade_support"],
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_alpha.py",
            role="alpha_responsibility",
            symbols=["alpha"],
            estimated_lines=120,
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_beta.py",
            role="beta_responsibility",
            symbols=["beta"],
            estimated_lines=120,
        ),
    ]
    plan = RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target.resolve()),
        source_content_hash=source_hash,
        settings={},
        public_api_before=["alpha", "beta", "facade_support"],
        public_api_after_expected=["alpha", "beta", "facade_support"],
        symbols=list(analysis.symbols),
        atomic_clusters=[],
        proposed_modules=modules,
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )
    window = SimpleNamespace(
        _large_file_refactor_last_plan=plan,
        _large_file_refactor_last_analysis=analysis,
        _large_file_refactor_planner_candidates=[SimpleNamespace(path=str(target.resolve()))],
    )
    return build_workbench_plan_snapshot(export_latest_planner_workbench_handoff(window))


def _build_contract(project_root: Path, target: Path, test_file: Path):
    snapshot = _build_snapshot(target)
    plan = snapshot.materialize_plan()
    basis = build_workbench_execution_basis_set(
        plan=plan,
        active_project_root=str(project_root),
        api_basis_paths=[target],
        dependency_basis_paths=[target],
        validation_basis_paths=[test_file],
    )
    assert basis.status == "execution_basis_ready", basis.blockers
    feasibility = evaluate_workbench_execution_feasibility(plan=plan, execution_basis=basis)
    assert feasibility.verdict == "EXECUTABLE", feasibility.blockers
    baseline = build_refactor_baseline(
        snapshot=snapshot,
        execution_basis=basis,
        behavior_baseline=_baseline_behavior(project_root, test_file),
    )
    assert baseline.integrity_valid()
    contract = build_workbench_execution_contract(
        snapshot=snapshot,
        baseline=baseline,
        execution_basis=basis,
        feasibility=feasibility,
    )
    assert contract.integrity_valid()
    assert contract.feasibility_verdict == "EXECUTABLE", contract.blocking_reasons
    return snapshot, baseline, contract


def _build_payload_chain(
    project_root: Path,
    snapshot,
    contract,
):
    plan = snapshot.materialize_plan()
    intake = build_workbench_plan_intake(snapshot=snapshot, active_project_root=str(project_root))
    assert intake.status == "plan_intake_ready", intake.blockers
    dependency = build_workbench_dependency_readiness(intake)
    assert dependency.ready_for_real_preview_writer, dependency.blockers
    preview_root = Path(resolve_preview_root(str(project_root))).resolve() / "patch3_fixture"
    preview = build_and_write_real_preview(
        plan=plan,
        intake=intake,
        dependency_readiness=dependency,
        active_project_root=str(project_root),
        preview_root=str(preview_root),
    )
    assert preview.status == "real_preview_written", preview.blockers
    assert preview.extraction_backend == "libcst_position_provider", preview.extraction_backend
    assert preview.cst_transform_fidelity.get("transform_backend") == "libcst_transform_partition"
    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=str(project_root),
    )
    assert structural.status.startswith("passed"), structural.blockers
    preflight = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=str(project_root),
    )
    assert preflight.status == "preflight_backup_ready", preflight.blockers
    for item in preview.files:
        preview_path = preview_root / item.relative_path
        assert _sha(preview_path) == item.content_hash, item.relative_path
    source_payload = build_and_write_source_apply_payload(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        preflight_backup=preflight,
        active_project_root=str(project_root),
    )
    assert source_payload.status == "source_apply_payload_ready", source_payload.blockers
    for item in source_payload.files:
        assert _sha(Path(item.payload_path)) == item.content_hash, item.relative_path
    risks = analyze_dynamic_python_risks(plan.target_file)
    assert risks.status == "dynamic_risk_clear", risks.to_dict()
    recipe = build_transformation_recipe(
        snapshot=snapshot,
        contract=contract,
        dynamic_risks=risks,
    )
    assert recipe.integrity_valid()
    assert not recipe.blockers, recipe.blockers
    sealed = build_and_write_sealed_payload(
        contract=contract,
        recipe=recipe,
        preview=preview,
        source_payload=source_payload,
    )
    valid, blockers = verify_sealed_payload(sealed)
    assert valid, blockers
    assert not sealed.source_mutation_enabled
    return risks, recipe, sealed


def _validate_dynamic_risks(sandbox: Path) -> None:
    risky = sandbox / "dynamic_risk_fixture.py"
    risky.write_text(
        "import sys\n"
        "names = ['x']\n"
        "__all__ = names\n"
        "sys.modules['alias'] = sys.modules[__name__]\n"
        "def __getattr__(name):\n"
        "    return name\n",
        encoding="utf-8",
    )
    report = analyze_dynamic_python_risks(risky)
    assert report.status == "dynamic_risk_blocked"
    assert "DYNAMIC_ALL_UNRESOLVED" in report.blockers
    assert "SYS_MODULES_MUTATION" in report.blockers
    assert any(item.code == "MODULE_GETATTR_PRESENT" for item in report.evidence)


def _validate_seal_tamper(sealed) -> None:
    victim = Path(sealed.files[0].payload_path)
    original = victim.read_bytes()
    victim.write_bytes(original + b"# tamper\n")
    valid, blockers = verify_sealed_payload(sealed)
    assert not valid
    assert any(item.startswith("SEALED_PAYLOAD_FILE_HASH_CHANGED:") for item in blockers)
    victim.write_bytes(original)
    valid, blockers = verify_sealed_payload(sealed)
    assert valid, blockers


def _validate_shadow(
    project_root: Path,
    baseline,
    contract,
    sealed,
    risks,
    shadow_parent: Path,
) -> None:
    source_before = _sha(Path(contract.target_file))
    mirror = ControlledMirrorBackend()
    mirror_result = mirror.materialize(
        project_root=project_root,
        shadow_root=shadow_parent / "mirror_shadow",
        sealed_payload=sealed,
    )
    assert mirror_result.status == "shadow_materialized", mirror_result.blockers
    provenance = prove_shadow_runtime_provenance(
        materialization=mirror_result,
        module_names=["fixture_pkg.large_module", "fixture_pkg._alpha", "fixture_pkg._beta"],
    )
    assert provenance.status == "shadow_provenance_pass", provenance.to_dict()
    wrong_origin = prove_shadow_runtime_provenance(
        materialization=mirror_result,
        module_names=["json"],
    )
    assert wrong_origin.status == "shadow_provenance_failed"
    assert "SHADOW_IMPORT_ORIGIN_OUTSIDE_SHADOW:json" in wrong_origin.blockers
    result = validate_shadow_refactor(
        contract=contract,
        baseline=baseline,
        sealed_payload=sealed,
        materialization=mirror_result,
        provenance=provenance,
        dynamic_risks=risks,
    )
    assert result.status == "shadow_validation_pass", result.to_dict()
    assert result.structural_status == "STRUCTURAL_PASS"
    assert result.api_status == "API_EQUIVALENT"
    assert result.topology_status == "TOPOLOGY_PASS"
    assert result.provenance_status == "shadow_provenance_pass"
    assert result.behavior.execution_status == "BEHAVIOR_PASS"
    assert result.behavior.baseline_comparison == "BASELINE_PASS_SHADOW_PASS"
    assert _sha(Path(contract.target_file)) == source_before

    backend, eligibility = choose_shadow_backend(project_root)
    assert eligibility.eligible, eligibility.to_dict()
    if shutil.which("git"):
        assert backend.name in {"git_worktree", "controlled_mirror"}


def _initialize_git(project_root: Path) -> None:
    if not shutil.which("git"):
        return
    commands = [
        ["git", "init"],
        ["git", "config", "user.email", "patch3-validator@example.invalid"],
        ["git", "config", "user.name", "Patch3 Validator"],
        ["git", "add", "."],
        ["git", "commit", "-m", "fixture baseline"],
    ]
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=str(project_root),
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr


def run_validation() -> None:
    try:
        import libcst  # noqa: F401
    except Exception as exc:
        raise AssertionError(f"LIBCST_REQUIRED_FOR_PATCH3_VALIDATION:{exc}") from exc

    with TemporaryDirectory(prefix="kanda_patch3_shadow_") as raw:
        sandbox = Path(raw).resolve()
        project_root = Path(sandbox.anchor) / f"kanda_patch3_fixture_{sandbox.name}"
        package = project_root / "fixture_pkg"
        tests = project_root / "tests"
        package.mkdir(parents=True)
        tests.mkdir(parents=True)
        (package / "__init__.py").write_text("\n", encoding="utf-8")
        target = package / "large_module.py"
        test_file = tests / "test_large_module.py"
        target.write_text(_source_text(), encoding="utf-8", newline="\n")
        test_file.write_text(_test_text(), encoding="utf-8", newline="\n")
        source_hash_before = _sha(target)

        snapshot, baseline, contract = _build_contract(project_root, target, test_file)
        risks, recipe, sealed = _build_payload_chain(project_root, snapshot, contract)
        assert recipe.transform_backend_required.startswith("libcst_")
        assert sealed.transform_backend.startswith("libcst_")
        _validate_dynamic_risks(sandbox)
        _validate_seal_tamper(sealed)
        _initialize_git(project_root)
        _validate_shadow(
            project_root,
            baseline,
            contract,
            sealed,
            risks,
            sandbox / "shadow_roots",
        )
        assert _sha(target) == source_hash_before

        if shutil.which("git"):
            git_backend = GitWorktreeBackend()
            eligibility = git_backend.eligibility(project_root)
            assert eligibility.eligible, eligibility.to_dict()
            worktree_result = git_backend.materialize(
                project_root=project_root,
                shadow_root=sandbox / "git_shadow",
                sealed_payload=sealed,
            )
            assert worktree_result.status == "shadow_materialized", worktree_result.blockers
            for path in worktree_result.applied_files:
                assert Path(path).is_file()
            assert _sha(target) == source_hash_before

        daily_root = project_root.parent / f"{project_root.name}_delete_after_daily_work"
        support_root = project_root.parent / f"{project_root.name}_show_project_to_AI"
        shutil.rmtree(project_root, ignore_errors=True)
        shutil.rmtree(daily_root, ignore_errors=True)
        shutil.rmtree(support_root, ignore_errors=True)

    print("TRANSFORMATION_RECIPE: PASS")
    print("DYNAMIC_PYTHON_RISK_CLASSIFICATION: PASS")
    print("LIBCST_EXACT_PAYLOAD: PASS")
    print("PREVIEW_PAYLOAD_BYTE_IDENTITY: PASS")
    print("SEALED_PAYLOAD_IDENTITY: PASS")
    print("CONTROLLED_MIRROR_SHADOW: PASS")
    print("GIT_WORKTREE_BACKEND: PASS" if shutil.which("git") else "GIT_WORKTREE_BACKEND: SKIPPED_GIT_UNAVAILABLE")
    print("SHADOW_PROVENANCE: PASS")
    print("SHADOW_API_TOPOLOGY_RUNTIME: PASS")
    print("SHADOW_BEHAVIOR_BASELINE_COMPARISON: PASS")
    print("NO_SOURCE_MUTATION: PASS")
    print(f"VALIDATION OK: {FEATURE_MARKER}")


if __name__ == "__main__":
    run_validation()
