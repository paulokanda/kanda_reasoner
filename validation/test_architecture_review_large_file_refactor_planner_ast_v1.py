# project-path: validation/test_architecture_review_large_file_refactor_planner_ast_v1.py
"""Focused validation for Large File Refactor Planner AST train."""
from __future__ import annotations

import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-ast-v1"
REQUIRED_MARKERS = (
    "module_docstring_present",
    "public_api_symbols",
    "nested_symbol_count",
    "RELATIVE_IMPORT_RISK",
    "STAR_IMPORT",
    "GLOBAL_STATE",
    "NESTED_SYMBOL_CLUSTER",
)


def main() -> int:
    """Run focused validation against synthetic files and changed modules."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed = _changed_files(project_root)
    _assert_module_sizes(changed)
    _compile_files(changed)
    _validate_analyzer(project_root)
    _validate_gui_integration(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


def _changed_files(project_root: Path) -> list[Path]:
    """Return files changed by this train that must compile and stay small."""
    rels = [
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analysis_formatting.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ast_analysis.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py",
        "validation/test_architecture_review_large_file_refactor_planner_ast_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_ast_v1.py",
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
    """Compile every changed Python file."""
    for path in paths:
        py_compile.compile(str(path), doraise=True)


def _validate_analyzer(project_root: Path) -> None:
    """Validate read-only AST evidence extraction on a synthetic module."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
        analyze_python_file,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analysis_formatting import (
        format_analysis_report,
    )

    temp_dir = Path(tempfile.mkdtemp(prefix="large_file_planner_ast_"))
    try:
        sample = temp_dir / "sample_module.py"
        sample.write_text(_sample_source(), encoding="utf-8")
        before = sample.read_text(encoding="utf-8")
        report = analyze_python_file(sample)
        after = sample.read_text(encoding="utf-8")
        if before != after:
            raise AssertionError("Analyzer modified the source file.")
        text = format_analysis_report(report)
        _assert_report(report, text)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def _assert_report(report: object, text: str) -> None:
    """Assert important analysis evidence fields are present."""
    data = report.to_dict()
    for marker in REQUIRED_MARKERS:
        if marker not in text and marker not in str(data):
            raise AssertionError(f"Expected marker missing from report: {marker}")
    if not report.module_docstring_present:
        raise AssertionError("Module docstring should be detected.")
    if "Exported" not in report.public_api_symbols:
        raise AssertionError("__all__ public API symbol was not detected.")
    if report.missing_docstring_count < 1:
        raise AssertionError("Missing docstrings should be counted.")
    if not any(item.is_relative for item in report.imports):
        raise AssertionError("Relative import risk was not detected.")
    if not any(item.is_star for item in report.imports):
        raise AssertionError("Star import risk was not detected.")
    if not any(symbol.name == "Exported" for symbol in report.symbols):
        raise AssertionError("Class symbol was not detected.")
    if not any(symbol.name == "mutate" for symbol in report.symbols):
        raise AssertionError("Function symbol was not detected.")


def _validate_gui_integration(project_root: Path) -> None:
    """Confirm GUI shell calls analyzer and formatter without enabling patch creation."""
    gui = project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py"
    text = gui.read_text(encoding="utf-8", errors="replace")
    required = [
        "analyze_python_file(path)",
        "format_analysis_report(report)",
        "PlannerState.ANALYZING",
        "Patch: {patch}",
    ]
    for marker in required:
        if marker not in text:
            raise AssertionError(f"GUI integration marker missing: {marker}")
    if "safe_write_text(" in text:
        raise AssertionError("GUI train should not write preview files.")
    if "VALIDATION_PASSED.value" in text and "PATCH_ALLOWED" in text:
        raise AssertionError("Patch creation must remain blocked in AST train.")


def _sample_source() -> str:
    """Return a synthetic module with public API, imports, and risks."""
    return """\"\"\"Sample module for analyzer validation.\"\"\"
from .local import helper
from somewhere import *
import os as operating_system

__all__ = [\"Exported\", \"mutate\"]
GLOBAL_CACHE = {}
value = helper()

class Exported:
    def method(self, item):
        def nested():
            return item
        return nested()


def mutate(value):
    global GLOBAL_CACHE
    GLOBAL_CACHE[\"value\"] = value
    return operating_system.name

if __name__ == \"__main__\":
    print(mutate(1))
"""


if __name__ == "__main__":
    raise SystemExit(main())
