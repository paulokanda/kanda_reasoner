# project-path: validation/test_architecture_review_large_file_refactor_planner_ast_baseline_recovery_v1.py
"""Recovery validation for Large File Refactor Planner AST baseline files."""
from __future__ import annotations

import py_compile
import runpy
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-ast-baseline-recovery-v1"
AST_FEATURE_ID = "architecture-review-large-file-refactor-planner-ast-v1"


def main() -> int:
    """Validate shell baseline plus AST train files are installed together."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed_files = _changed_files(project_root)
    _assert_files_exist(changed_files)
    _assert_module_sizes(changed_files)
    _compile_files(changed_files)
    _assert_baseline_imports()
    _run_ast_validation(project_root)
    _assert_gui_registration(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"VALIDATION OK: {AST_FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


def _changed_files(project_root: Path) -> list[Path]:
    """Return source and validation files required by the recovery patch."""
    rels = [
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analysis_formatting.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ast_analysis.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/candidate_discovery.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/guards.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py",
        "validation/test_architecture_review_large_file_refactor_planner_ast_v1.py",
        "validation/test_architecture_review_large_file_refactor_planner_ast_baseline_recovery_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_ast_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_ast_baseline_recovery_v1.py",
    ]
    return [project_root / rel for rel in rels]


def _assert_files_exist(paths: list[Path]) -> None:
    """Confirm every expected file is present before validation continues."""
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise AssertionError("Missing required recovery files: " + "; ".join(missing))


def _assert_module_sizes(paths: list[Path]) -> None:
    """Enforce the hard 500-line size gate for touched Python files."""
    for path in paths:
        if path.suffix != ".py":
            continue
        line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if line_count > 500:
            raise AssertionError(f"Module exceeds 500 physical lines: {path} ({line_count})")


def _compile_files(paths: list[Path]) -> None:
    """Compile every changed Python file."""
    for path in paths:
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)


def _assert_baseline_imports() -> None:
    """Validate AST train imports its shell baseline dependencies."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
        analyze_python_file,
        discover_candidates,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.guards import (
        compute_content_hash,
        make_source_snapshot,
    )
    if not callable(analyze_python_file):
        raise AssertionError("analyze_python_file is not callable.")
    if not callable(discover_candidates):
        raise AssertionError("discover_candidates is not callable.")
    if not callable(compute_content_hash):
        raise AssertionError("compute_content_hash is not callable.")
    if not callable(make_source_snapshot):
        raise AssertionError("make_source_snapshot is not callable.")


def _run_ast_validation(project_root: Path) -> None:
    """Run the original AST validation as a nested required check."""
    script = project_root / "validation" / "test_architecture_review_large_file_refactor_planner_ast_v1.py"
    try:
        runpy.run_path(str(script), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise AssertionError(f"Nested AST validation failed with exit code {exc.code}") from exc


def _assert_gui_registration(project_root: Path) -> None:
    """Confirm the Architecture Review registration includes the planner tab."""
    subtabs = project_root / "kanda_reasoner_app" / "manage_architecture" / "architecture_review_subtabs.py"
    text = subtabs.read_text(encoding="utf-8", errors="replace")
    if "Large File Refactor Planner" not in text:
        raise AssertionError("Large File Refactor Planner tab registration is missing.")
    if "build_large_file_refactor_planner_page" not in text:
        raise AssertionError("Large File Refactor Planner page builder is missing.")


if __name__ == "__main__":
    raise SystemExit(main())
