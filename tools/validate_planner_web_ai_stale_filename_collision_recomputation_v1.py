"""Validate stale filename collision recomputation in Web AI planning."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_bounded_refinement import (
    apply_bounded_architecture_refinement,
)


def _symbol(name: str, lines: int) -> RefactorSymbol:
    return RefactorSymbol(
        schema_version="1.0",
        name=name,
        kind="function",
        visibility="private",
        start_line=1,
        end_line=lines,
        physical_lines=lines,
        atomic_cluster_id="symbol:" + name,
    )


def _module(filename: str, symbols: list[str], lines: int) -> ProposedModule:
    return ProposedModule(
        schema_version="1.0",
        filename=filename,
        role="dependency_cluster_helper",
        symbols=symbols,
        estimated_lines=lines,
        status="planned",
    )


def _fixture() -> tuple[ModuleAnalysisReport, RefactorPlan]:
    symbols = [
        _symbol("_decision", 84),
        _symbol("_source_safe", 55),
        _symbol("_request", 60),
        _symbol("_policy_fields", 141),
    ]
    report = ModuleAnalysisReport(
        schema_version="1.0",
        feature_id="architecture-review-large-file-refactor-planner-v1",
        target_file="target.py",
        source_content_hash="fixture",
        line_count_physical=600,
        module_docstring_present=True,
        module_docstring_preview="fixture",
        all_names=[],
        public_api_symbols=["PublicFacade"],
        imports=[],
        symbols=symbols,
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )
    plan = RefactorPlan(
        schema_version="1.0",
        feature_id=report.feature_id,
        target_file=report.target_file,
        source_content_hash=report.source_content_hash,
        settings={
            "minimum_helper_physical_lines": 101,
            "maximum_physical_lines": 499,
        },
        public_api_before=["PublicFacade"],
        public_api_after_expected=["PublicFacade"],
        symbols=symbols,
        atomic_clusters=[item.atomic_cluster_id for item in symbols],
        proposed_modules=[
            ProposedModule(
                schema_version="1.0",
                filename="target.py",
                role="public_facade",
                symbols=["PublicFacade"],
                estimated_lines=180,
                status="planned",
            ),
            _module("_cohesive.py", ["_decision", "_source_safe"], 159),
            _module("_cohesive.py", ["_request"], 120),
            _module("_cohesive_2.py", ["_policy_fields"], 165),
        ],
        import_migration={},
        docstring_proposals=[],
        risks=["FILENAME_COLLISION"],
        validation_blockers=["Repeated proposed filename: _cohesive.py"],
        status="blocked",
    )
    return report, plan


def main() -> int:
    report, plan = _fixture()
    refined = apply_bounded_architecture_refinement(
        report,
        plan,
        reassignments=[
            {"symbol": "_decision", "target_module": "_cohesive_2.py"}
        ],
        module_merges=[],
        module_renames=[
            {
                "module": "_cohesive.py",
                "new_filename": "_input_safety.py",
            },
            {
                "module": "_cohesive_2.py",
                "new_filename": "_decision_policy.py",
            },
        ],
    )

    assert refined.status == "planned", refined.validation_blockers
    assert refined.validation_blockers == [], refined.validation_blockers
    assert "FILENAME_COLLISION" not in refined.risks, refined.risks
    helper_names = [
        module.filename
        for module in refined.proposed_modules
        if module.role != "public_facade"
    ]
    assert helper_names == ["_input_safety.py", "_decision_policy.py"], helper_names
    assert len(helper_names) == len(set(helper_names))
    print("STALE_REPEATED_FILENAME_BLOCKER_REMOVED_AFTER_BOUNDED_REBUILD: PASS")

    by_name = {module.filename: module for module in refined.proposed_modules}
    assert 101 <= by_name["_input_safety.py"].estimated_lines <= 499
    assert 101 <= by_name["_decision_policy.py"].estimated_lines <= 499
    print("REFINED_HELPER_SIZE_GATE_101_499: PASS")

    report2, plan2 = _fixture()
    plan2 = RefactorPlan(
        **{
            **plan2.__dict__,
            "validation_blockers": [
                "Repeated proposed filename: _cohesive.py",
                "Unrelated safety blocker must remain.",
            ],
        }
    )
    refined2 = apply_bounded_architecture_refinement(
        report2,
        plan2,
        reassignments=[],
        module_merges=[],
        module_renames=[],
    )
    assert "Unrelated safety blocker must remain." in refined2.validation_blockers
    assert refined2.status == "blocked"
    print("UNRELATED_BLOCKERS_REMAIN_FAIL_CLOSED: PASS")

    print("PLANNER_WEB_AI_STALE_FILENAME_COLLISION_RECOMPUTATION: PASS")
    print(
        "VALIDATION OK: "
        "large-file-refactor-planner-web-ai-stale-filename-collision-recomputation-v1"
    )
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
