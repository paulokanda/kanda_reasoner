"""Validate Real Preview imports for facade-owned module assignments."""

from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (
    export_latest_planner_workbench_handoff,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (
    validate_real_preview_structure,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
    build_split_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (
    build_workbench_plan_snapshot,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import (
    resolve_workbench_preview_root,
)
from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
    run_large_module_split_audit,
)

FEATURE_ID = (
    "large-file-refactor-real-preview-facade-assignment-dependency-repair-v1"
)
TARGET_RELATIVE = Path(
    "kanda_reasoner_app/reasoner_symbol_atlas/json_active_scope_quality.py"
)
TARGET_HASH = (
    "db5380f8815685efd4fe8dc8fd1d3b4adb3b31ad828e0a22f991d6c0ad6ded8c"
)
ENGINE_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "cst_facade_global_import_inserter.py"
)
EXPECTED_HELPER = "_json_active_scope_quality_path_resolution.py"
EXPECTED_IMPORT_USERS = {
    "_inactive_marker_in_text",
    "_is_path_like_text",
}
EXPECTED_GLOBAL = "INACTIVE_TEXT_MARKERS"


def _sha256(path: Path) -> str:
    """Return the lowercase SHA-256 for one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_plan_shape(plan: object) -> None:
    """Require the exact approved responsibility-dominant plan shape."""
    proposed_modules = getattr(plan, "proposed_modules")
    helper_modules = [
        module for module in proposed_modules if module.role != "public_facade"
    ]
    if len(helper_modules) != 1:
        raise AssertionError("EXPECTED_ONE_HELPER_MODULE")
    helper = helper_modules[0]
    if helper.filename != EXPECTED_HELPER:
        raise AssertionError("HELPER_FILENAME_MISMATCH:" + helper.filename)
    missing = EXPECTED_IMPORT_USERS - set(helper.symbols)
    if missing:
        raise AssertionError("EXPECTED_HELPER_SYMBOLS_MISSING:" + ",".join(sorted(missing)))


def _assert_facade_global_insertions(preview: object, preview_root: Path) -> None:
    """Require local facade imports for both module-assignment consumers."""
    report = getattr(preview, "facade_global_import_insertion")
    if report.get("status") != "facade_global_import_insertion_ready":
        raise AssertionError("FACADE_GLOBAL_IMPORT_INSERTION_NOT_READY")
    found: set[str] = set()
    for item in report.get("insertions", []):
        if tuple(item.get("imported_names", ())) == (EXPECTED_GLOBAL,):
            found.add(str(item.get("symbol_name", "")))
    if found != EXPECTED_IMPORT_USERS:
        raise AssertionError("FACADE_GLOBAL_INSERTION_SET_MISMATCH:" + repr(sorted(found)))

    helper_path = preview_root / EXPECTED_HELPER
    source = helper_path.read_text(encoding="utf-8")
    import_line = (
        "from .json_active_scope_quality import " + EXPECTED_GLOBAL
    )
    if source.count(import_line) != 2:
        raise AssertionError("EXPECTED_TWO_FUNCTION_LOCAL_IMPORTS")
    compile(source, str(helper_path), "exec")


def main() -> None:
    """Run focused end-to-end Workbench Preview validation."""
    project_root = Path(__file__).resolve().parents[1]
    target = (project_root / TARGET_RELATIVE).resolve()
    engine = (project_root / ENGINE_RELATIVE).resolve()

    if _sha256(target) != TARGET_HASH:
        raise AssertionError("EXACT_TARGET_HASH_MISMATCH")

    analysis = analyze_python_file(target)
    plan = build_split_plan(
        analysis,
        source_path=target,
        preferred_strategy="responsibility_dominant",
    )
    if plan.status != "planned" or plan.validation_blockers:
        raise AssertionError("PLANNER_PLAN_NOT_READY:" + "|".join(plan.validation_blockers))
    _assert_plan_shape(plan)

    window = SimpleNamespace(
        _large_file_refactor_last_plan=plan,
        _large_file_refactor_last_analysis=analysis,
        _large_file_refactor_planner_candidates=[SimpleNamespace(path=str(target))],
    )
    handoff = export_latest_planner_workbench_handoff(window)
    snapshot = build_workbench_plan_snapshot(handoff)
    intake = build_workbench_plan_intake(
        snapshot=snapshot,
        active_project_root=str(project_root),
    )
    if intake.status != "plan_intake_ready" or intake.blockers:
        raise AssertionError("PLAN_INTAKE_BLOCKED:" + "|".join(intake.blockers))

    readiness = build_workbench_dependency_readiness(intake)
    if readiness.status != "dependency_readiness_ready" or readiness.blockers:
        raise AssertionError(
            "DEPENDENCY_READINESS_BLOCKED:" + "|".join(readiness.blockers)
        )
    assignments = set(readiness.dependency_report.module_assignments)
    if EXPECTED_GLOBAL not in assignments:
        raise AssertionError("EXPECTED_MODULE_ASSIGNMENT_MISSING")

    preview_root = resolve_workbench_preview_root(
        project_root,
        "validation_facade_assignment_dependency_repair_v1",
    )
    preview = build_and_write_real_preview(
        plan=plan,
        intake=intake,
        dependency_readiness=readiness,
        active_project_root=str(project_root),
        preview_root=str(preview_root),
    )
    if preview.status != "real_preview_written" or preview.blockers:
        raise AssertionError("REAL_PREVIEW_BLOCKED:" + "|".join(preview.blockers))
    _assert_facade_global_insertions(preview, preview_root)

    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=str(project_root),
    )
    if structural.status not in {"passed", "passed_with_warnings"}:
        raise AssertionError(
            "STRUCTURAL_VALIDATION_NOT_READY:" + "|".join(structural.blockers)
        )
    if structural.blockers:
        raise AssertionError(
            "STRUCTURAL_VALIDATION_BLOCKED:" + "|".join(structural.blockers)
        )

    if _sha256(target) != TARGET_HASH:
        raise AssertionError("TARGET_SOURCE_MUTATED_DURING_PREVIEW")

    line_count = len(engine.read_text(encoding="utf-8").splitlines())
    if not 100 < line_count < 500:
        raise AssertionError("TOUCHED_ENGINE_LINE_LAW:" + str(line_count))

    audit = run_large_module_split_audit(
        project_root,
        engine,
        classifier_mode="heuristic",
    )
    classification = audit.data.get("refactor_safety_classification", {})
    if classification.get("label") != "SAFE REFACTORING":
        raise AssertionError("TOUCHED_ENGINE_AST_NOT_SAFE")
    if classification.get("hard_blockers"):
        raise AssertionError("TOUCHED_ENGINE_AST_HARD_BLOCKERS")

    print("EXACT_TARGET_HASH_MATCH: PASS")
    print("RESPONSIBILITY_DOMINANT_PLAN_SHAPE: PASS")
    print("PLAN_INTAKE_AND_DEPENDENCY_READINESS: PASS")
    print("MODULE_ASSIGNMENT_FACADE_OWNERSHIP: PASS")
    print("INACTIVE_TEXT_MARKERS_LOCAL_IMPORT_SYNTHESIS: PASS")
    print("REAL_PREVIEW_ORIGINAL_BLOCKERS_REMOVED: PASS")
    print("REAL_PREVIEW_WRITTEN: PASS")
    print("STRUCTURAL_VALIDATION: PASS")
    print("TARGET_SOURCE_MUTATION_DISABLED: PASS")
    print("TOUCHED_ENGINE_LINE_LAW_101_499: PASS")
    print("FRESH_TOUCHED_ENGINE_AST_SAFE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
