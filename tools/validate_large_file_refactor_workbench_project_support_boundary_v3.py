"""Validate Workbench Tool/Project/Support/Daily-Work path ownership."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import types

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_PACKAGE_PATHS = {
    "kanda_reasoner_app": _PROJECT_ROOT / "kanda_reasoner_app",
    "kanda_reasoner_app.manage_architecture": (
        _PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture"
    ),
    "kanda_reasoner_app.manage_architecture.large_file_refactor_planner": (
        _PROJECT_ROOT
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
    ),
}
for _package_name, _package_path in _PACKAGE_PATHS.items():
    if _package_name not in sys.modules:
        _package = types.ModuleType(_package_name)
        _package.__path__ = [str(_package_path)]
        sys.modules[_package_name] = _package

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    REAL_PREVIEW_FEATURE_ID,
    RealPreviewFile,
    RealPreviewWriteResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (
    validate_real_preview_structure,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ProposedModule,
    RefactorPlan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_artifact_validation import (
    validate_preview_artifacts,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import (
    build_preview_bundle,
    resolve_preview_root,
    write_preview_files,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    daily_work_root,
    preview_root_blockers,
    preview_runs_root,
    project_support_root,
    workbench_path_class,
    workbench_support_root,
)
from kanda_reasoner_app.project_support_boundary import (
    canonical_project_support_root,
    canonical_transient_garbage_root,
)
from tools.workbench_support_boundary_validation_fixture import (
    expected_external_root,
    isolated_workbench_paths,
)

FEATURE_MARKER = "architecture-review-large-file-refactor-workbench-project-support-boundary-v3"


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return whether path is contained by root."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _build_plan(target: Path) -> RefactorPlan:
    """Build a minimal deterministic Preview plan for path validation."""
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    module = ProposedModule(
        schema_version=SCHEMA_VERSION,
        filename=target.name,
        role="public_facade",
        symbols=["alpha"],
        estimated_lines=120,
        exports=["alpha"],
    )
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target.resolve()),
        source_content_hash=source_hash,
        settings={},
        public_api_before=["alpha"],
        public_api_after_expected=["alpha"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[module],
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )


def _validate_distinct_tool_and_project(
    sandbox: Path,
) -> tuple[Path, bool, Path, bool]:
    """Prove another project uses canonical drive-root ownership."""
    tool_root = sandbox / "kanda_reasoner"
    project_root = sandbox / "other_project"
    tool_root.mkdir()
    project_root.mkdir()

    support_root = project_support_root(project_root)
    daily_root = daily_work_root(project_root)
    expected_support = expected_external_root(
        project_root,
        "_show_project_to_AI",
    )
    expected_daily = expected_external_root(
        project_root,
        "_delete_after_daily_work",
    )
    assert support_root == expected_support
    assert support_root == canonical_project_support_root(project_root)
    assert daily_root == expected_daily
    assert daily_root == canonical_transient_garbage_root(project_root)
    assert support_root != project_root / "other_project_show_project_to_AI"
    assert daily_root != project_root / "other_project_delete_after_daily_work"
    print("TOOL_PROJECT_IDENTITY_SEPARATION: PASS")
    print("WORKBENCH_SUPPORT_ROOT_CANONICAL_EXTERNAL: PASS")
    print("WORKBENCH_DAILY_ROOT_CANONICAL_EXTERNAL: PASS")
    return support_root, support_root.exists(), daily_root, daily_root.exists()


def _validate_self_hosting(sandbox: Path) -> None:
    """Prove self-hosting keeps logical ownership classes separate."""
    project_root = sandbox / "kanda_reasoner_self_host"
    project_root.mkdir()
    support = project_support_root(project_root)
    preview = Path(resolve_preview_root(str(project_root))).resolve()
    daily = daily_work_root(project_root)

    assert _is_relative_to(preview, support)
    assert not _is_relative_to(preview, project_root)
    assert not _is_relative_to(preview, daily)
    assert workbench_path_class(project_root, preview) == "active_project_preview_support"
    assert workbench_path_class(project_root, daily / "trash.zip") == "daily_work_garbage"
    print("SELF_HOSTING_BOUNDARY_SEPARATION: PASS")


def _validate_preview_write_and_artifact_validation(sandbox: Path) -> None:
    """Write and validate real Preview support artifacts outside daily-work."""
    project_root = sandbox / "clinical_project"
    project_root.mkdir()
    target = project_root / "target.py"
    target.write_text("def alpha():\n    return 1\n", encoding="utf-8")
    plan = _build_plan(target)
    preview_root = Path(resolve_preview_root(str(project_root))).resolve()
    bundle = build_preview_bundle(
        plan,
        preview_root=str(preview_root),
        governed_write=True,
    )
    write_result = write_preview_files(bundle, active_project_root=str(project_root))
    assert write_result.status == "written", write_result.blockers
    validation = validate_preview_artifacts(
        bundle,
        write_result,
        active_project_root=str(project_root),
    )
    assert validation.status == "passed", validation.blockers

    support = workbench_support_root(project_root)
    daily = daily_work_root(project_root)
    for raw in write_result.written_files:
        path = Path(raw).resolve()
        assert _is_relative_to(path, support), path
        assert not _is_relative_to(path, daily), path
        assert not _is_relative_to(path, project_root), path
    print("PREVIEW_WRITES_PROJECT_SUPPORT_ONLY: PASS")
    print("PREVIEW_ARTIFACT_VALIDATION_PROJECT_SUPPORT: PASS")


def _large_function(name: str, steps: int = 112) -> str:
    """Return one deterministic function large enough for Workbench policy."""
    lines = [
        f"def {name}():",
        f'    """Return deterministic value for {name}."""',
        "    value = 0",
    ]
    for index in range(1, steps + 1):
        lines.append(f"    value += {index}")
    lines.append("    return value")
    return "\n".join(lines)


def _real_preview_plan(target: Path) -> RefactorPlan:
    """Build a three-module plan for real Preview and structural validation."""
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
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
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target.resolve()),
        source_content_hash=source_hash,
        settings={},
        public_api_before=["alpha", "beta", "facade_support"],
        public_api_after_expected=["alpha", "beta", "facade_support"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=modules,
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )


def _preview_source_text() -> str:
    """Return source text used by structural validation fixtures."""
    return (
        "\n\n".join(
            [
                '\"\"\"Real Preview path-boundary fixture.\"\"\"',
                "__all__ = ['alpha', 'beta', 'facade_support']",
                _large_function("facade_support"),
                _large_function("alpha"),
                _large_function("beta"),
            ]
        )
        + "\n"
    )


def _write_manual_preview_bundle(project_root: Path, plan: RefactorPlan) -> RealPreviewWriteResult:
    """Write deterministic Preview files under dynamic project support."""
    preview_root = Path(resolve_preview_root(str(project_root))).resolve()
    preview_root.mkdir(parents=True, exist_ok=True)
    header = "# KANDA PREVIEW ARTIFACT - NOT SOURCE TRUTH\n"
    facade_text = (
        header
        + "from ._alpha import alpha\n"
        + "from ._beta import beta\n\n"
        + "__all__ = ['alpha', 'beta', 'facade_support']\n\n"
        + _large_function("facade_support")
        + "\n"
    )
    alpha_text = header + _large_function("alpha") + "\n"
    beta_text = header + _large_function("beta") + "\n"
    payloads = {
        "large_module.py": ("public_facade", ["facade_support"], facade_text),
        "_alpha.py": ("alpha_responsibility", ["alpha"], alpha_text),
        "_beta.py": ("beta_responsibility", ["beta"], beta_text),
    }
    files: list[RealPreviewFile] = []
    written_files: list[str] = []
    for relative_path, (role, symbols, content) in payloads.items():
        target = preview_root / relative_path
        target.write_bytes(content.encode("utf-8"))
        files.append(
            RealPreviewFile(
                relative_path=relative_path,
                role=role,
                symbols=symbols,
                content_hash=hashlib.sha256(target.read_bytes()).hexdigest(),
                physical_lines=len(content.splitlines()),
            )
        )
        written_files.append(str(target))
    return RealPreviewWriteResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_FEATURE_ID,
        status="real_preview_written",
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        preview_root=str(preview_root),
        libcst_available=False,
        files=files,
        written_files=written_files,
        source_mutation_enabled=False,
        blockers=[],
        warnings=[],
    )


def _validate_real_preview_structural_chain(sandbox: Path) -> None:
    """Validate Preview and reports remain in selected-project support state."""
    project_root = sandbox / "real_preview_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text(_preview_source_text(), encoding="utf-8")
    plan = _real_preview_plan(target)
    preview = _write_manual_preview_bundle(project_root, plan)
    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=str(project_root),
    )
    assert structural.status.startswith("passed"), structural.blockers
    support = workbench_support_root(project_root)
    daily = daily_work_root(project_root)
    for raw in [*preview.written_files, *structural.report_files]:
        path = Path(raw).resolve()
        assert _is_relative_to(path, support), path
        assert not _is_relative_to(path, daily), path
    assert Path(preview.preview_root).is_dir()
    print("REAL_PREVIEW_PROJECT_SUPPORT_PATH: PASS")
    print("STRUCTURAL_VALIDATION_REPORTS_PROJECT_SUPPORT: PASS")


def _validate_missing_preview_root_fails_closed(sandbox: Path) -> None:
    """Prove missing Preview support state blocks without Path.write_text crash."""
    project_root = sandbox / "missing_preview_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text(_preview_source_text(), encoding="utf-8")
    plan = _real_preview_plan(target)
    preview_root = Path(resolve_preview_root(str(project_root))).resolve()
    missing_file = RealPreviewFile(
        relative_path="large_module.py",
        role="public_facade",
        symbols=["facade_support"],
        content_hash="0" * 64,
        physical_lines=120,
    )
    preview = RealPreviewWriteResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_FEATURE_ID,
        status="real_preview_written",
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        preview_root=str(preview_root),
        libcst_available=False,
        files=[missing_file],
        written_files=[str(preview_root / missing_file.relative_path)],
        source_mutation_enabled=False,
        blockers=[],
        warnings=[],
    )
    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=str(project_root),
    )
    assert structural.status.startswith("blocked"), structural.status
    assert "PREVIEW_FILE_MISSING" in structural.blockers, structural.blockers
    for raw in structural.report_files:
        path = Path(raw).resolve()
        assert _is_relative_to(path, workbench_support_root(project_root)), path
        assert not _is_relative_to(path, daily_work_root(project_root)), path
        assert path.is_file(), path
    print("MISSING_PREVIEW_ROOT_FAILS_CLOSED_WITH_REPORTS: PASS")

def _validate_fail_closed_wrong_roots(sandbox: Path) -> None:
    """Prove project source and daily-work cannot masquerade as Preview support."""
    project_root = sandbox / "boundary_project"
    project_root.mkdir()
    daily_preview = daily_work_root(project_root) / "large_file_refactor_preview" / "wrong"
    source_preview = project_root / "preview" / "wrong"
    support_preview = preview_runs_root(project_root) / "correct"

    assert "PREVIEW_ROOT_OUTSIDE_PROJECT_SUPPORT" in preview_root_blockers(
        project_root,
        daily_preview,
    )
    source_blockers = preview_root_blockers(project_root, source_preview)
    assert "PREVIEW_ROOT_INSIDE_PROJECT_SOURCE" in source_blockers
    assert "PREVIEW_ROOT_OUTSIDE_PROJECT_SUPPORT" in source_blockers
    assert preview_root_blockers(project_root, support_preview) == []
    print("DAILY_WORK_PREVIEW_ROOT_REJECTED: PASS")
    print("PROJECT_SOURCE_PREVIEW_ROOT_REJECTED: PASS")


def _validate_static_no_regression(project_root: Path) -> None:
    """Reject old daily-work Preview ownership assertions in Workbench source."""
    planner_root = (
        project_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
    )
    forbidden = (
        "PREVIEW_ROOT_OUTSIDE_DAILY_WORK",
        '"large_file_refactor_preview"',
    )
    allowed_literal_files = {
        "candidate_discovery.py",
        "import_migration_preview.py",
        "workbench_execution_basis.py",
        "workbench_plan_intake.py",
    }
    for path in planner_root.glob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert forbidden[0] not in text, path
        if path.name not in allowed_literal_files:
            assert forbidden[1] not in text, path

    preflight_path = planner_root / "source_apply_preflight_backup_contract.py"
    assert preflight_path.is_file(), preflight_path
    preflight_text = preflight_path.read_text(encoding="utf-8", errors="ignore")
    assert "preview_root_must_remain_under_daily_work" not in preflight_text, preflight_path
    assert "_daily_root_for" not in preflight_text, preflight_path
    assert "preview_root_blockers" in preflight_text, preflight_path
    assert "preview_root_inside_project_support_only" in preflight_text, preflight_path

    readiness_path = planner_root / "workbench_preflight_backup_readiness.py"
    assert readiness_path.is_file(), readiness_path
    readiness_text = readiness_path.read_text(encoding="utf-8", errors="ignore")
    assert "PREVIEW_ROOT_OUTSIDE_DAILY_WORK" not in readiness_text, readiness_path
    assert "preview_root_blockers" in readiness_text, readiness_path

    formatting_path = planner_root / "workbench_preflight_backup_formatting.py"
    assert formatting_path.is_file(), formatting_path
    formatting_text = formatting_path.read_text(encoding="utf-8", errors="ignore")
    assert "PREVIEW_ROOT_OUTSIDE_DAILY_WORK" not in formatting_text, formatting_path
    assert "PREVIEW_ROOT_OUTSIDE_PROJECT_SUPPORT" in formatting_text, formatting_path
    assert "project support root" in formatting_text.lower(), formatting_path

    print("PREFLIGHT_BACKUP_CONTRACT_PROJECT_SUPPORT_POLICY: PASS")
    print("PREFLIGHT_BACKUP_READINESS_PROJECT_SUPPORT_POLICY: PASS")
    print("PREFLIGHT_BACKUP_FORMATTING_PROJECT_SUPPORT_POLICY: PASS")
    print("NO_DAILY_WORK_PREVIEW_POLICY_REGRESSION: PASS")


def run_validation() -> None:
    """Run all focused boundary checks."""
    project_root = Path(__file__).resolve().parents[1]
    with TemporaryDirectory(prefix="kanda_support_boundary_") as raw:
        sandbox = Path(raw).resolve()
        support_path, support_before, daily_path, daily_before = (
            _validate_distinct_tool_and_project(sandbox)
        )
        with isolated_workbench_paths(
            sandbox,
            sys.modules[__name__],
        ) as fixture_roots:
            _validate_self_hosting(sandbox)
            _validate_preview_write_and_artifact_validation(sandbox)
            _validate_real_preview_structural_chain(sandbox)
            _validate_missing_preview_root_fails_closed(sandbox)
            _validate_fail_closed_wrong_roots(sandbox)
        support_base, daily_base = fixture_roots
        assert _is_relative_to(support_base, sandbox)
        assert _is_relative_to(daily_base, sandbox)
        assert support_path.exists() == support_before
        assert daily_path.exists() == daily_before
        print("WORKBENCH_VALIDATION_SUPPORT_ISOLATED: PASS")
        print("WORKBENCH_VALIDATION_DAILY_WORK_ISOLATED: PASS")
        print("WORKBENCH_DRIVE_ROOT_FIXTURE_STATE_UNCHANGED: PASS")
    _validate_static_no_regression(project_root)
    print("VALIDATION OK: project-tool-boundary-canon-v1")
    print("STATUS: IN_SYNC")
    print(f"VALIDATION OK: {FEATURE_MARKER}")



if __name__ == "__main__":
    run_validation()
