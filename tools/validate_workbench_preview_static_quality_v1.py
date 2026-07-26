"""Validate Workbench preview static quality gates and facade normalization."""
from __future__ import annotations

import ast
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (  # noqa: E402
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_preview_rendering import (  # noqa: E402
    render_preview_facade,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_symbol_source_extractor import (  # noqa: E402
    extract_source_blocks,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (  # noqa: E402
    PlannerSettings,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_static_quality import (  # noqa: E402
    inspect_preview_static_quality,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (  # noqa: E402
    build_split_plan,
)

FEATURE_ID = "architecture-review-workbench-preview-static-quality-v1"


def main() -> None:
    """Run deterministic bad-fixture and real-target facade quality checks."""
    _validate_bad_fixture_is_blocked()
    print("BAD_PREVIEW_ARTIFACTS_DETECTED: PASS")

    facade_text = _render_real_target_facade()
    facade_path = Path("main_helper_mapper.py")
    quality = inspect_preview_static_quality(facade_path, facade_text)
    if quality.blockers:
        raise AssertionError("REAL_TARGET_FACADE_QUALITY_BLOCKED:" + "|".join(quality.blockers))
    print("REAL_TARGET_FACADE_STATIC_QUALITY: PASS")

    tree = ast.parse(facade_text)
    if ast.get_docstring(tree) != "Read-only main file and helper file mapper for Project Symbol Atlas.":
        raise AssertionError("ORIGINAL_MODULE_DOCSTRING_NOT_PRESERVED")
    print("ORIGINAL_MODULE_DOCSTRING_PRESERVED: PASS")

    all_lines = [
        node.lineno
        for node in tree.body
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and _assigns_all(node)
    ]
    if len(all_lines) != 1:
        raise AssertionError("PUBLIC_API_ALL_ASSIGNMENT_COUNT:" + str(len(all_lines)))
    print("SINGLE_PUBLIC_API_ALL_ASSIGNMENT: PASS")

    import_counts: dict[tuple[int, str], int] = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            key = (int(node.level or 0), str(node.module or ""))
            import_counts[key] = import_counts.get(key, 0) + 1
    fragmented = [key for key, count in import_counts.items() if count > 1]
    if fragmented:
        raise AssertionError("FRAGMENTED_IMPORTS_REMAIN:" + repr(fragmented))
    print("GROUPED_HELPER_IMPORTS: PASS")

    structural_source = (
        PROJECT_ROOT
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/real_preview_structural_validator.py"
    ).read_text(encoding="utf-8", errors="replace")
    for marker in (
        "inspect_preview_static_quality",
        "blockers.extend(quality.blockers)",
    ):
        if marker not in structural_source:
            raise AssertionError("STRUCTURAL_QUALITY_GATE_WIRING_MISSING:" + marker)
    print("STRUCTURAL_VALIDATOR_APPLIES_STATIC_QUALITY_GATE: PASS")

    touched_python = (
        PROJECT_ROOT
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_preview_rendering.py",
        PROJECT_ROOT
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_static_quality.py",
        PROJECT_ROOT
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/real_preview_structural_validator.py",
        PROJECT_ROOT / "tools/validate_large_file_refactor_workbench_real_widget_attemptability_v1.py",
    )
    oversized: list[str] = []
    for path in touched_python:
        line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if line_count > 500:
            oversized.append(f"{path.relative_to(PROJECT_ROOT)}:{line_count}")
    if oversized:
        raise AssertionError("TOUCHED_SOURCE_MODULE_TOO_LARGE:" + "|".join(oversized))
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("WORKBENCH_PREVIEW_STATIC_QUALITY: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def _validate_bad_fixture_is_blocked() -> None:
    bad = '''"""first"""\nfrom .helper import a\nfrom .helper import b\n__all__ = ["a"]\n"""second"""\n__all__ = ["b"]\n# project-path: one.py\n# project-path: two.py\n'''
    quality = inspect_preview_static_quality(Path("bad_preview.py"), bad)
    required_prefixes = (
        "DUPLICATE_PUBLIC_API_ALL_ASSIGNMENT:",
        "POINTLESS_TOP_LEVEL_STRING_EXPRESSION:",
        "FRAGMENTED_SAME_MODULE_IMPORTS:",
        "DUPLICATE_PROJECT_PATH_HEADER:",
    )
    for prefix in required_prefixes:
        if not any(item.startswith(prefix) for item in quality.blockers):
            raise AssertionError("BAD_FIXTURE_GATE_MISSING:" + prefix)


def _render_real_target_facade() -> str:
    target = PROJECT_ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    analysis = analyze_python_file(target)
    plan = build_split_plan(analysis, PlannerSettings(), source_path=None)
    if plan.status != "planned" or plan.validation_blockers:
        raise AssertionError("REAL_TARGET_PLAN_BLOCKED:" + "|".join(plan.validation_blockers))

    helper_for_symbol: dict[str, str] = {}
    facade_filename = target.name
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            facade_filename = module.filename
            continue
        for symbol in module.symbols:
            helper_for_symbol[symbol] = module.filename

    extraction = extract_source_blocks(target, set(helper_for_symbol))
    if extraction.blockers:
        raise AssertionError("REAL_TARGET_EXTRACTION_BLOCKED:" + "|".join(extraction.blockers))
    return render_preview_facade(
        plan,
        facade_filename,
        extraction.import_blocks,
        extraction.retained_facade_blocks,
        helper_for_symbol,
        extraction.extraction_backend,
    )


def _assigns_all(node: ast.Assign | ast.AnnAssign) -> bool:
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    return any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets)


if __name__ == "__main__":
    main()
