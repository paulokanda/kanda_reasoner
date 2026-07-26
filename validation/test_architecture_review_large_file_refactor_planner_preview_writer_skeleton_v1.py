# project-path: validation/test_architecture_review_large_file_refactor_planner_preview_writer_skeleton_v1.py
"""Focused validation for Large File Refactor Planner preview writer skeleton."""
from __future__ import annotations

import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1"
LLM_FEATURE_ID = "architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1"
DOC_FEATURE_ID = "architecture-review-large-file-refactor-planner-docstring-contracts-v1"
SPLIT_FEATURE_ID = "architecture-review-large-file-refactor-planner-split-contracts-v1"
AST_FEATURE_ID = "architecture-review-large-file-refactor-planner-ast-v1"


def main() -> int:
    """Run focused preview writer skeleton validation."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed = _changed_files(project_root)
    _assert_module_sizes(changed)
    _compile_files(changed)
    _run_llm_baseline(project_root)
    _validate_preview_contracts()
    _validate_gui_contract(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"VALIDATION OK: {LLM_FEATURE_ID}")
    print(f"VALIDATION OK: {DOC_FEATURE_ID}")
    print(f"VALIDATION OK: {SPLIT_FEATURE_ID}")
    print(f"VALIDATION OK: {AST_FEATURE_ID}")
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
        "validation/test_architecture_review_large_file_refactor_planner_preview_writer_skeleton_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_preview_writer_skeleton_v1.py",
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


def _run_llm_baseline(project_root: Path) -> None:
    """Run the previous frozen LLM validation baseline."""
    script = project_root / "validation/test_architecture_review_large_file_refactor_planner_llm_arbitration_contracts_v1.py"
    if not script.exists():
        raise AssertionError("LLM baseline validation script missing")
    namespace = {"__name__": "__baseline__", "__file__": str(script)}
    code = compile(script.read_text(encoding="utf-8"), str(script), "exec")
    exec(code, namespace)
    result = int(namespace["main"]())
    if result != 0:
        raise AssertionError("LLM baseline validation did not return 0")


def _validate_preview_contracts() -> None:
    """Validate no-write preview bundle behavior."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
        SCHEMA_VERSION,
        PlannerSettings,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import (
        build_preview_bundle,
        resolve_preview_root,
        validate_preview_bundle,
        write_preview_files,
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "large_module.py"
        target.write_text(_sample_source(), encoding="utf-8")
        report = analyze_python_file(str(target))
        plan = build_split_plan(report, PlannerSettings())
        preview_root = resolve_preview_root(str(root))
        if Path(preview_root).exists():
            raise AssertionError("resolve_preview_root must not create directories")
        bundle = build_preview_bundle(plan, preview_root=preview_root)
        if bundle.schema_version != SCHEMA_VERSION:
            raise AssertionError("Preview bundle schema mismatch")
        if bundle.write_mode != "preview_only_no_write_skeleton":
            raise AssertionError("Unsafe preview write mode")
        if any(file.write_enabled for file in bundle.files):
            raise AssertionError("Preview file draft has writes enabled")
        validation = validate_preview_bundle(bundle)
        if validation.status not in {"passed", "blocked"}:
            raise AssertionError("Unexpected preview validation status")
        try:
            write_preview_files(bundle)
        except RuntimeError as exc:
            if "disabled" not in str(exc):
                raise
        else:
            raise AssertionError("write_preview_files must refuse writes in skeleton v1")
        if list(root.iterdir()) != [target]:
            raise AssertionError("Preview skeleton must not write extra files")


def _validate_gui_contract(project_root: Path) -> None:
    """Validate GUI wiring text without requiring Qt import."""
    gui = (project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py").read_text(encoding="utf-8")
    required = [
        "Generate Preview",
        "Validate Preview",
        "_generate_preview_skeleton",
        "_validate_preview_skeleton",
        "_large_file_refactor_preview_button",
        "_large_file_refactor_validate_preview_button",
    ]
    for needle in required:
        if needle not in gui:
            raise AssertionError("Missing GUI preview contract text: " + needle)


def _sample_source() -> str:
    """Return a sample source module for preview contract validation."""
    return '\nVALUE = 1\n\n\ndef alpha(value: int) -> int:\n    return value + VALUE\n\n\ndef beta(value: int) -> int:\n    return alpha(value) * 2\n\n\nclass Gamma:\n    def method(self, item: int) -> int:\n        return beta(item)\n'


if __name__ == "__main__":
    raise SystemExit(main())
