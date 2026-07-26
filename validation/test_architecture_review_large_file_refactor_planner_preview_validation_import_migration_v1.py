# project-path: validation/test_architecture_review_large_file_refactor_planner_preview_validation_import_migration_v1.py
"""Focused validation for preview artifact validation and import migration preview."""
from __future__ import annotations

import dataclasses
import hashlib
import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-preview-validation-import-migration-v1"
DEP_GOVERNED = "architecture-review-large-file-refactor-planner-governed-preview-generation-v1"
DEP_PREVIEW = "architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1"
DEP_LLM = "architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1"
DEP_DOC = "architecture-review-large-file-refactor-planner-docstring-contracts-v1"
DEP_SPLIT = "architecture-review-large-file-refactor-planner-split-contracts-v1"
DEP_AST = "architecture-review-large-file-refactor-planner-ast-v1"


def main() -> int:
    """Run focused preview artifact and import migration validation."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed = _changed_files(project_root)
    _assert_module_sizes(changed)
    _compile_files(changed)
    _run_governed_preview_baseline(project_root)
    _validate_preview_artifacts_and_import_migration()
    _validate_gui_contract(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"VALIDATION OK: {DEP_GOVERNED}")
    print(f"VALIDATION OK: {DEP_PREVIEW}")
    print(f"VALIDATION OK: {DEP_LLM}")
    print(f"VALIDATION OK: {DEP_DOC}")
    print(f"VALIDATION OK: {DEP_SPLIT}")
    print(f"VALIDATION OK: {DEP_AST}")
    print("STATUS: IN_SYNC")
    return 0


def _changed_files(project_root: Path) -> list[Path]:
    """Return files touched by this train."""
    rels = [
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/import_migration_preview.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_artifact_validation.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_formatting.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
        "validation/test_architecture_review_large_file_refactor_planner_preview_validation_import_migration_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_preview_validation_import_migration_v1.py",
    ]
    return [project_root / rel for rel in rels]


def _assert_module_sizes(paths: list[Path]) -> None:
    """Assert every touched Python file remains under the hard limit."""
    for path in paths:
        if not path.exists():
            raise AssertionError(f"Missing changed file: {path}")
        line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if line_count > 500:
            raise AssertionError(f"Module exceeds 500 physical lines: {path} ({line_count})")


def _compile_files(paths: list[Path]) -> None:
    """Compile changed Python files."""
    for path in paths:
        py_compile.compile(str(path), doraise=True)


def _run_governed_preview_baseline(project_root: Path) -> None:
    """Run the previous frozen governed-preview validation baseline."""
    script = project_root / "validation/test_architecture_review_large_file_refactor_planner_governed_preview_generation_v1.py"
    if not script.exists():
        raise AssertionError("Governed preview baseline validation script missing")
    namespace = {"__name__": "__baseline__", "__file__": str(script)}
    code = compile(script.read_text(encoding="utf-8"), str(script), "exec")
    exec(code, namespace)
    if int(namespace["main"]()) != 0:
        raise AssertionError("Governed preview baseline validation did not return 0")


def _validate_preview_artifacts_and_import_migration() -> None:
    """Validate artifact checks and read-only import migration preview."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.import_migration_preview import build_import_migration_preview
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import PlannerSettings
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_artifact_validation import validate_preview_artifacts
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import (
        build_preview_bundle,
        resolve_preview_root,
        write_preview_files,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan

    tmp = Path(tempfile.mkdtemp(prefix="kanda_preview_artifact_validation_test_"))
    try:
        sample_root = tmp / "sample_project"
        sample_root.mkdir()
        source = sample_root / "large_module.py"
        source.write_text(_sample_source(), encoding="utf-8")
        consumer = sample_root / "consumer.py"
        consumer.write_text("from large_module import public_one\nprint(public_one())\n", encoding="utf-8")
        before_hash = _hash_file(source)
        report = analyze_python_file(str(source))
        plan = build_split_plan(report, PlannerSettings(ideal_physical_lines=120, minimum_helper_physical_lines=20))
        preview_root = resolve_preview_root(str(sample_root))
        bundle = build_preview_bundle(plan, preview_root=preview_root, governed_write=True)
        write_result = write_preview_files(bundle, str(sample_root))
        import_preview = build_import_migration_preview(plan, active_project_root=str(sample_root))
        artifact_result = validate_preview_artifacts(
            bundle,
            write_result,
            active_project_root=str(sample_root),
            import_preview=import_preview,
        )
        if artifact_result.status != "passed":
            raise AssertionError("Preview artifact validation should pass: " + repr(artifact_result.blockers))
        if not import_preview.records:
            raise AssertionError("Import migration preview should discover consumer.py")
        if import_preview.rewrite_enabled:
            raise AssertionError("Import migration preview must not enable rewrites")
        if _hash_file(source) != before_hash:
            raise AssertionError("Selected source changed during preview artifact validation")
        unsafe_plan = dataclasses.replace(plan, import_migration={"rewrite_project_imports": True})
        unsafe_preview = build_import_migration_preview(unsafe_plan, importer_paths=[str(consumer)])
        unsafe_result = validate_preview_artifacts(
            bundle,
            write_result,
            active_project_root=str(sample_root),
            import_preview=unsafe_preview,
        )
        if unsafe_result.status != "blocked" or "IMPORT_REWRITE_ENABLED_NOT_ALLOWED_IN_PREVIEW" not in unsafe_result.blockers:
            raise AssertionError("Import rewrite enablement was not blocked")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _validate_gui_contract(project_root: Path) -> None:
    """Validate GUI wiring text without importing PySide6."""
    gui = (project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py").read_text(encoding="utf-8")
    required = [
        "build_import_migration_preview",
        "validate_preview_artifacts",
        "format_import_migration_preview",
        "format_preview_artifact_validation",
        "_large_file_refactor_import_migration_preview",
    ]
    missing = [item for item in required if item not in gui]
    if missing:
        raise AssertionError("GUI preview validation/import migration contract missing: " + ", ".join(missing))


def _sample_source() -> str:
    """Return a simple source module with public and private symbols."""
    return '"""Sample large module."""\n\nVALUE = 1\n\ndef public_one():\n    return VALUE\n\ndef public_two():\n    return public_one() + 1\n\ndef _private_helper():\n    return public_two()\n'


def _hash_file(path: Path) -> str:
    """Return a stable file hash."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
