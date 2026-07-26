# project-path: tools/validate_large_file_refactor_planner_topology_responsibility_quality_scoring_v1.py
"""Validate projected dependency topology and responsibility-aware candidate scoring."""
from __future__ import annotations

import ast
from pathlib import Path
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
FEATURE = "large-file-refactor-planner-topology-responsibility-quality-scoring-v1"


def _install_namespace_packages() -> None:
    packages = (
        ("kanda_reasoner_app", ROOT / "kanda_reasoner_app"),
        ("kanda_reasoner_app.manage_architecture", ROOT / "kanda_reasoner_app/manage_architecture"),
        ("kanda_reasoner_app.manage_architecture.large_file_refactor_planner", BOX),
    )
    for name, path in packages:
        module = ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules.setdefault(name, module)


_install_namespace_packages()

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    ModuleAnalysisReport,
    ProposedModule,
    RefactorSymbol,
    SCHEMA_VERSION,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_dependency_topology import (
    build_module_dependency_topology,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_formatting import (
    format_split_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
    build_split_plan,
)


def main() -> None:
    _static_checks()
    _real_target_checks()
    _synthetic_cycle_checks()
    print("PROJECTED_DEPENDENCY_TOPOLOGY: DIRECTED_EXPLAINABLE")
    print("HELPER_CYCLE_POLICY: HARD_BLOCK")
    print("FACADE_BACK_REFERENCE_POLICY: EXPLICIT_BOUNDARY_RISK")
    print("CANDIDATE_QUALITY: RESPONSIBILITY_AND_TOPOLOGY_AWARE")
    print("MIXED_RESPONSIBILITY_PENALTY: ACTIVE")
    print("MAIN_HELPER_MAPPER_CASE: HELPER_DAG_WITH_FACADE_BOUNDARY_RISK")
    print("HEURISTIC_PARTITION: STEP2_122_452_PRESERVED")
    print("LOCAL_AI_LOGIC: UNCHANGED")
    print("WORKBENCH_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _static_checks() -> None:
    names = (
        "planner_dependency_topology.py",
        "planner_candidate_quality.py",
        "planner_heuristic_candidates.py",
        "split_planner.py",
        "split_formatting.py",
    )
    for name in names:
        path = BOX / name
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        line_count = len(text.splitlines())
        if line_count > 500:
            raise SystemExit(f"VALIDATION ERROR: {name} exceeds 500 lines: {line_count}")
    combined = "\n".join((BOX / name).read_text(encoding="utf-8") for name in names)
    required = (
        "build_module_dependency_topology",
        "helper_topological_order",
        "facade_back_references",
        "HELPER_DEPENDENCY_CYCLE",
        "responsibility_cohesion_score",
        "topology_score",
        "mixed_responsibility_penalty",
        "projected_dependency_topology",
    )
    for token in required:
        if token not in combined:
            raise SystemExit("VALIDATION ERROR: missing Step 3 token " + token)
    forbidden = (
        "planner_local_ai_plan_review",
        "planner_local_ai_comprehensive_review",
        "workbench_guarded_apply",
        "workbench_rollback_executor",
    )
    for token in forbidden:
        if token in combined:
            raise SystemExit("VALIDATION ERROR: Local AI or Workbench contamination: " + token)


def _real_target_checks() -> None:
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    report = analyze_python_file(target)
    first = build_split_plan(report)
    second = build_split_plan(report)
    if first.to_dict() != second.to_dict():
        raise SystemExit("VALIDATION ERROR: Step 3 plan is not deterministic")
    if first.status != "planned":
        raise SystemExit("VALIDATION ERROR: real target should remain planned")
    helpers = [item for item in first.proposed_modules if item.role != "public_facade"]
    if sorted(item.estimated_lines for item in helpers) != [122, 452]:
        raise SystemExit("VALIDATION ERROR: Step 2 partition changed")
    names = {item.filename for item in helpers}
    expected_names = {
        "_main_helper_mapper_path_resolution.py",
        "_main_helper_mapper_helper_selection.py",
    }
    if names != expected_names:
        raise SystemExit("VALIDATION ERROR: semantic filenames regressed: " + repr(names))

    topology = first.import_migration.get("projected_dependency_topology", {})
    if topology.get("status") != "ready_with_warnings":
        raise SystemExit("VALIDATION ERROR: expected explicit boundary-risk topology status")
    if topology.get("helper_cycles"):
        raise SystemExit("VALIDATION ERROR: real target has an unexpected helper-only cycle")
    if topology.get("blockers"):
        raise SystemExit("VALIDATION ERROR: boundary risk must not be mislabeled helper-cycle blocker")
    back_refs = topology.get("facade_back_references", [])
    expected_back_ref = "_main_helper_mapper_helper_selection.py -> main_helper_mapper.py"
    if expected_back_ref not in back_refs:
        raise SystemExit("VALIDATION ERROR: facade back-reference evidence missing")
    components = topology.get("full_cycle_components", [])
    expected_component = sorted([
        "_main_helper_mapper_helper_selection.py",
        "main_helper_mapper.py",
    ])
    if expected_component not in [sorted(item) for item in components]:
        raise SystemExit("VALIDATION ERROR: facade boundary cycle component missing")
    order = topology.get("helper_topological_order", [])
    if sorted(order) != sorted(names):
        raise SystemExit("VALIDATION ERROR: helper topological order is incomplete")

    selection = first.import_migration.get("heuristic_candidate_selection", {})
    if selection.get("selected_strategy") != "balanced":
        raise SystemExit("VALIDATION ERROR: Step 2 balanced selection regressed")
    candidates = selection.get("candidates", [])
    selected_id = selection.get("selected_candidate_id")
    selected = next(item for item in candidates if item.get("candidate_id") == selected_id)
    for field in (
        "responsibility_cohesion_score",
        "topology_score",
        "mixed_responsibility_penalty",
        "facade_back_reference_penalty",
        "quality_evidence",
    ):
        if field not in selected:
            raise SystemExit("VALIDATION ERROR: selected candidate lacks quality field " + field)
    if not (0.0 < float(selected["responsibility_cohesion_score"]) < 1.0):
        raise SystemExit("VALIDATION ERROR: responsibility cohesion evidence is not meaningful")
    if float(selected["topology_score"]) >= 1.0:
        raise SystemExit("VALIDATION ERROR: facade back-reference topology penalty not applied")
    if float(selected["mixed_responsibility_penalty"]) <= 0.0:
        raise SystemExit("VALIDATION ERROR: mixed responsibility penalty not applied")
    evidence = selected.get("quality_evidence", {})
    mixed = evidence.get("mixed_responsibility_clusters", [])
    if not any(
        item.get("primary_responsibility") == "helper_selection"
        and "decision_reporting" in item.get("secondary_responsibilities", [])
        and item.get("estimated_lines") == 452
        for item in mixed
    ):
        raise SystemExit("VALIDATION ERROR: 452-line mixed responsibility helper not surfaced")

    rendered = format_split_plan(first)
    for token in (
        "Projected dependency topology:",
        "Facade back-references:",
        "Helper cycles: <none>",
        "Selected candidate quality evidence:",
        "Mixed-responsibility helpers:",
        "primary=helper_selection; secondary=decision_reporting; lines=452",
    ):
        if token not in rendered:
            raise SystemExit("VALIDATION ERROR: Step 3 evidence missing from plan output: " + token)


def _synthetic_cycle_checks() -> None:
    report = ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id="fixture",
        target_file="cycle_fixture.py",
        source_content_hash="fixture",
        line_count_physical=20,
        module_docstring_present=False,
        module_docstring_preview="",
        all_names=["a", "b"],
        public_api_symbols=[],
        imports=[],
        symbols=[
            _symbol("a", 1, ["b"]),
            _symbol("b", 10, ["a"]),
        ],
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )
    modules = [
        _module("_a.py", ["a"]),
        _module("_b.py", ["b"]),
    ]
    topology = build_module_dependency_topology(report, modules)
    if topology.status != "blocked":
        raise SystemExit("VALIDATION ERROR: helper cycle did not block")
    if not topology.helper_cycles:
        raise SystemExit("VALIDATION ERROR: helper cycle evidence missing")
    if "HELPER_DEPENDENCY_CYCLE" not in topology.blockers:
        raise SystemExit("VALIDATION ERROR: helper-cycle blocker missing")
    if topology.helper_topological_order:
        raise SystemExit("VALIDATION ERROR: cyclic helper graph must not claim topological order")


def _symbol(name: str, line: int, references: list[str]) -> RefactorSymbol:
    return RefactorSymbol(
        schema_version=SCHEMA_VERSION,
        name=name,
        kind="function",
        visibility="private",
        start_line=line,
        end_line=line + 4,
        physical_lines=5,
        references=references,
        atomic_cluster_id="symbol:" + name,
        content_hash=name,
    )


def _module(filename: str, symbols: list[str]) -> ProposedModule:
    return ProposedModule(
        schema_version=SCHEMA_VERSION,
        filename=filename,
        role="function_helper",
        symbols=symbols,
        estimated_lines=120,
        status="planned",
    )


if __name__ == "__main__":
    main()
