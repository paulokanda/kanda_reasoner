# project-path: validation/test_architecture_review_large_file_refactor_planner_governed_preview_generation_v1.py
"""Focused validation for governed preview generation."""
from __future__ import annotations

import hashlib
import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-governed-preview-generation-v1"
DEP_PREVIEW = "architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1"
DEP_LLM = "architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1"
DEP_DOC = "architecture-review-large-file-refactor-planner-docstring-contracts-v1"
DEP_SPLIT = "architecture-review-large-file-refactor-planner-split-contracts-v1"
DEP_AST = "architecture-review-large-file-refactor-planner-ast-v1"


def main() -> int:
    """Run focused governed preview generation validation."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed = _changed_files(project_root)
    _assert_module_sizes(changed)
    _compile_files(changed)
    _run_preview_skeleton_baseline(project_root)
    _validate_governed_preview_generation()
    _validate_gui_contract(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
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
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_writer.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_formatting.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
        "validation/test_architecture_review_large_file_refactor_planner_governed_preview_generation_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_governed_preview_generation_v1.py",
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


def _run_preview_skeleton_baseline(project_root: Path) -> None:
    """Run the previous frozen preview-skeleton validation baseline."""
    script = project_root / "validation/test_architecture_review_large_file_refactor_planner_preview_writer_skeleton_v1.py"
    if not script.exists():
        raise AssertionError("Preview skeleton baseline validation script missing")
    namespace = {"__name__": "__baseline__", "__file__": str(script)}
    code = compile(script.read_text(encoding="utf-8"), str(script), "exec")
    exec(code, namespace)
    if int(namespace["main"]()) != 0:
        raise AssertionError("Preview skeleton baseline validation did not return 0")


def _validate_governed_preview_generation() -> None:
    """Validate preview writes remain daily-work only and source-safe."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import PlannerSettings, PreviewWriteResult
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import (
        build_preview_bundle,
        resolve_preview_root,
        validate_preview_bundle,
        write_preview_files,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan

    tmp = Path(tempfile.mkdtemp(prefix="kanda_governed_preview_test_"))
    try:
        project_root = tmp / "sample_project"
        project_root.mkdir()
        source = project_root / "large_module.py"
        source.write_text(_sample_source(), encoding="utf-8")
        before = _hash_file(source)
        report = analyze_python_file(str(source))
        plan = build_split_plan(report, PlannerSettings(ideal_physical_lines=120, minimum_helper_physical_lines=20))
        preview_root = resolve_preview_root(str(project_root))
        bundle = build_preview_bundle(plan, preview_root=preview_root, governed_write=True)
        validation = validate_preview_bundle(bundle)
        if validation.status != "passed":
            raise AssertionError("Governed preview bundle should validate")
        result = write_preview_files(bundle, str(project_root))
        if not isinstance(result, PreviewWriteResult):
            raise AssertionError("write_preview_files must return PreviewWriteResult")
        if result.status != "written":
            raise AssertionError("Governed preview result was not written: " + repr(result.blockers))
        if _hash_file(source) != before:
            raise AssertionError("Selected project source was modified")
        preview_path = Path(result.preview_root).resolve()
        if _is_relative_to(preview_path, project_root.resolve()):
            raise AssertionError("Preview root is inside project source")
        if not any(Path(item).name == "PREVIEW_MANIFEST.json" for item in result.written_files):
            raise AssertionError("Preview manifest was not written")
        if not any(Path(item).name == "NO_SOURCE_WRITE_PROOF.txt" for item in result.written_files):
            raise AssertionError("No-source-write proof was not written")
        bad_bundle = build_preview_bundle(plan, preview_root=str(project_root / "bad"), governed_write=True)
        bad_result = write_preview_files(bad_bundle, str(project_root))
        if bad_result.status != "blocked" or "PREVIEW_ROOT_INSIDE_PROJECT_SOURCE" not in bad_result.blockers:
            raise AssertionError("Unsafe preview root was not blocked")
        skeleton = build_preview_bundle(plan, preview_root=preview_root, governed_write=False)
        skeleton_result = write_preview_files(skeleton, str(project_root))
        if skeleton_result.status != "blocked" or "WRITE_MODE_NOT_GOVERNED" not in skeleton_result.blockers:
            raise AssertionError("Skeleton write mode was not blocked")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _validate_gui_contract(project_root: Path) -> None:
    """Validate GUI wiring text without importing PySide6."""
    gui = (project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py").read_text(encoding="utf-8")
    required = [
        "write_preview_files",
        "governed_write=True",
        "_large_file_refactor_preview_write_result",
        "format_preview_write_result",
    ]
    missing = [item for item in required if item not in gui]
    if missing:
        raise AssertionError("GUI governed preview contract missing: " + ", ".join(missing))


def _sample_source() -> str:
    """Return a simple source module with public and private symbols."""
    return '"""Sample large module."""\n\nVALUE = 1\n\ndef public_one():\n    return VALUE\n\ndef public_two():\n    return public_one() + 1\n\ndef _private_helper():\n    return public_two()\n'


def _hash_file(path: Path) -> str:
    """Return a stable file hash."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
