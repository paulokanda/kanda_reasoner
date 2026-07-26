# project-path: validation/test_architecture_review_large_file_refactor_planner_docstring_contracts_v1.py
"""Focused validation for Large File Refactor Planner docstring contracts."""
from __future__ import annotations

import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-docstring-contracts-v1"
SPLIT_FEATURE_ID = "architecture-review-large-file-refactor-planner-split-contracts-v1"
AST_FEATURE_ID = "architecture-review-large-file-refactor-planner-ast-v1"


def main() -> int:
    """Run focused docstring-contract validation."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed = _changed_files(project_root)
    _assert_module_sizes(changed)
    _compile_files(changed)
    _run_split_baseline(project_root)
    _validate_docstring_planner()
    _validate_gui_contract(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"VALIDATION OK: {SPLIT_FEATURE_ID}")
    print(f"VALIDATION OK: {AST_FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


def _changed_files(project_root: Path) -> list[Path]:
    """Return files touched by the docstring train."""
    rels = [
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/docstring_planner.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/docstring_formatting.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
        "validation/test_architecture_review_large_file_refactor_planner_docstring_contracts_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_docstring_contracts_v1.py",
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


def _run_split_baseline(project_root: Path) -> None:
    """Run the frozen split-contract validator when available."""
    validator = project_root / "validation/test_architecture_review_large_file_refactor_planner_split_contracts_v1.py"
    if not validator.exists():
        raise AssertionError("Split contracts v1 validator is required before docstring contracts.")
    namespace = {"__name__": "split_v1_embedded", "__file__": str(validator)}
    code = compile(validator.read_text(encoding="utf-8"), str(validator), "exec")
    exec(code, namespace)
    result = namespace["main"]()
    if result != 0:
        raise AssertionError("Split contracts v1 baseline validation returned nonzero.")


def _validate_docstring_planner() -> None:
    """Validate deterministic docstring proposal behavior."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
        analyze_python_file,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.docstring_formatting import (
        format_docstring_proposals,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.docstring_planner import (
        build_docstring_proposals,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
        DocstringProposal,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
        build_split_plan,
    )

    temp_dir = Path(tempfile.mkdtemp(prefix="large_file_docstring_contracts_"))
    try:
        sample = temp_dir / "sample_docstrings.py"
        sample.write_text(_sample_source(), encoding="utf-8")
        before = sample.read_text(encoding="utf-8")
        report = analyze_python_file(sample)
        plan = build_split_plan(report)
        proposals = build_docstring_proposals(report, plan)
        after = sample.read_text(encoding="utf-8")
        if before != after:
            raise AssertionError("Docstring planner must not modify source files.")
        if not proposals or not all(isinstance(item, DocstringProposal) for item in proposals):
            raise AssertionError("Docstring planner must return proposal records.")
        names = {item.target_name for item in proposals}
        for expected in {"sample_docstrings", "MissingClass", "missing_function", "MissingClass.run"}:
            if expected not in names:
                raise AssertionError(f"Missing expected docstring proposal: {expected}")
        if "Documented" in names:
            raise AssertionError("Existing docstrings must not be overwritten.")
        provenance = {item.provenance for item in proposals}
        if "deterministic_template" not in provenance:
            raise AssertionError("Deterministic provenance is required.")
        if not any(item.provenance in {"manual_required", "low_confidence_needs_review"} for item in proposals):
            raise AssertionError("Low-confidence/manual provenance is required for unclear symbols.")
        if not all(item.proposed_docstring.startswith('\"\"\"') for item in proposals):
            raise AssertionError("Proposals must use triple double quote docstrings.")
        text = format_docstring_proposals(proposals)
        for marker in ("does not insert docstrings", "Existing docstrings are not overwritten", "Provenance"):
            if marker not in text:
                raise AssertionError(f"Docstring text missing marker: {marker}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def _validate_gui_contract(project_root: Path) -> None:
    """Confirm GUI exposes docstring proposal generation but keeps preview blocked."""
    gui = project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py"
    text = gui.read_text(encoding="utf-8", errors="replace")
    required = [
        "Generate Docstring Plan",
        "build_docstring_proposals(report, plan)",
        "format_docstring_proposals(proposals)",
        "PlannerState.DOCSTRING_READY",
        "Generate Preview",
        "Create Patch ZIP",
    ]
    for marker in required:
        if marker not in text:
            raise AssertionError(f"GUI docstring contract marker missing: {marker}")
    if "safe_write_text(" in text or "safe_write_bytes(" in text:
        raise AssertionError("Docstring-contract GUI must not write preview files.")


def _sample_source() -> str:
    """Return a synthetic module with missing and existing docstrings."""
    private_body = "\n".join(
        f"    total += value + {index}" for index in range(45)
    )
    return (
        "class MissingClass:\n"
        "    def run(self, value: int) -> int:\n"
        "        return value + 1\n\n"
        "class Documented:\n"
        "    \"\"\"Existing class docstring.\"\"\"\n"
        "    def run(self):\n"
        "        \"\"\"Existing method docstring.\"\"\"\n"
        "        return 1\n\n"
        "def missing_function(value: int) -> int:\n"
        "    return value + 1\n\n"
        "def _complex_private(value):\n"
        "    total = 0\n"
        + private_body
        + "\n    return total\n"
    )

if __name__ == "__main__":
    raise SystemExit(main())
