# project-path: validation/test_architecture_review_large_file_refactor_planner_split_contracts_v1.py
"""Focused validation for Large File Refactor Planner split contracts."""
from __future__ import annotations

import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-split-contracts-v1"
AST_FEATURE_ID = "architecture-review-large-file-refactor-planner-ast-v1"


def main() -> int:
    """Run focused split-contract validation."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed = _changed_files(project_root)
    _assert_module_sizes(changed)
    _compile_files(changed)
    _run_ast_baseline(project_root)
    _validate_split_planner()
    _validate_gui_contract(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"VALIDATION OK: {AST_FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


def _changed_files(project_root: Path) -> list[Path]:
    """Return files touched by the split-contract train."""
    rels = [
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/split_planner.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/split_formatting.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
        "validation/test_architecture_review_large_file_refactor_planner_split_contracts_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_split_contracts_v1.py",
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


def _run_ast_baseline(project_root: Path) -> None:
    """Run the frozen AST train validator when available."""
    validator = project_root / "validation/test_architecture_review_large_file_refactor_planner_ast_v1.py"
    if not validator.exists():
        raise AssertionError("AST v1 validator is required before split contracts.")
    namespace = {"__name__": "ast_v1_embedded", "__file__": str(validator)}
    code = compile(validator.read_text(encoding="utf-8"), str(validator), "exec")
    exec(code, namespace)
    result = namespace["main"]()
    if result != 0:
        raise AssertionError("AST v1 baseline validation returned nonzero.")


def _validate_split_planner() -> None:
    """Validate deterministic plan contracts on synthetic modules."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
        analyze_python_file,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
        MAX_PHYSICAL_LINES,
        PlannerSettings,
        RefactorPlan,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_formatting import (
        format_split_plan,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
        build_split_plan,
    )

    temp_dir = Path(tempfile.mkdtemp(prefix="large_file_split_contracts_"))
    try:
        sample = temp_dir / "sample_module.py"
        sample.write_text(_sample_source(), encoding="utf-8")
        before = sample.read_text(encoding="utf-8")
        report = analyze_python_file(sample)
        plan = build_split_plan(report, PlannerSettings())
        after = sample.read_text(encoding="utf-8")
        if before != after:
            raise AssertionError("Split planner must not modify the source file.")
        if not isinstance(plan, RefactorPlan):
            raise AssertionError("build_split_plan must return RefactorPlan.")
        if plan.public_api_before != plan.public_api_after_expected:
            raise AssertionError("Public API preservation contract changed.")
        if not plan.proposed_modules or plan.proposed_modules[0].role != "public_facade":
            raise AssertionError("Original module must remain the first public facade.")
        if any(module.estimated_lines > MAX_PHYSICAL_LINES for module in plan.proposed_modules):
            raise AssertionError("Planned module exceeds max line contract.")
        text = format_split_plan(plan)
        for marker in ("public_facade", "preview files", "Patch creation remains blocked"):
            if marker not in text:
                raise AssertionError(f"Plan text missing marker: {marker}")
        _validate_blocking_rules(temp_dir, build_split_plan, analyze_python_file)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def _validate_blocking_rules(temp_dir: Path, build_split_plan: object, analyze_python_file: object) -> None:
    """Validate oversized class and filename collision blockers."""
    large_class = temp_dir / "large_class_module.py"
    large_class.write_text(_large_class_source(), encoding="utf-8")
    class_plan = build_split_plan(analyze_python_file(large_class))
    if "TOO_LARGE_CLASS" not in class_plan.risks:
        raise AssertionError("Oversized class must be blocked.")
    if class_plan.status != "blocked":
        raise AssertionError("Oversized class plan must be blocked.")

    collision = temp_dir / "collision_module.py"
    collision.write_text(_collision_source(), encoding="utf-8")
    (temp_dir / "_collision_module_function.py").write_text("# exists\n", encoding="utf-8")
    collision_plan = build_split_plan(analyze_python_file(collision))
    if "FILENAME_COLLISION" not in collision_plan.risks:
        raise AssertionError("Filename collision must be detected.")
    if collision_plan.status != "blocked":
        raise AssertionError("Filename collision must block the plan.")


def _validate_gui_contract(project_root: Path) -> None:
    """Confirm GUI exposes plan generation but keeps preview/patch blocked."""
    gui = project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py"
    text = gui.read_text(encoding="utf-8", errors="replace")
    required = [
        "build_split_plan(report, settings)",
        "format_split_plan(plan)",
        "_large_file_refactor_plan_button",
        "Generate Preview",
        "Create Patch ZIP",
    ]
    for marker in required:
        if marker not in text:
            raise AssertionError(f"GUI split contract marker missing: {marker}")
    if "safe_write_text(" in text or "safe_write_bytes(" in text:
        raise AssertionError("Split-contract GUI must not write preview files.")


def _sample_source() -> str:
    """Return a synthetic source that produces facade plus helper contracts."""
    helpers = "\n\n".join(
        f"def helper_{index}(value):\n    return value + {index}\n" for index in range(20)
    )
    return (
        "\"\"\"Sample module.\"\"\"\n"
        "__all__ = [\"PublicApi\"]\n\n"
        "class PublicApi:\n"
        "    \"\"\"Public facade class.\"\"\"\n"
        "    def run(self):\n"
        "        return helper_1(1)\n\n"
        + helpers
        + "\n"
    )


def _large_class_source() -> str:
    """Return source with one class above the hard module limit."""
    methods = "\n".join(
        f"    def method_{index}(self):\n        return {index}\n" for index in range(260)
    )
    return "\"\"\"Large class sample.\"\"\"\n\nclass Giant:\n" + methods + "\n"


def _collision_source() -> str:
    """Return source whose helper filename already exists."""
    helpers = "\n\n".join(
        f"def _helper_{index}(value):\n    return value + {index}\n" for index in range(20)
    )
    return "\"\"\"Collision sample.\"\"\"\n\n" + helpers + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
