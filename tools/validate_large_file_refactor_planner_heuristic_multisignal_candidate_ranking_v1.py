# project-path: tools/validate_large_file_refactor_planner_heuristic_multisignal_candidate_ranking_v1.py
"""Validate deterministic multi-signal heuristic candidates and ranking."""
from __future__ import annotations

import ast
from pathlib import Path
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
FEATURE = "large-file-refactor-planner-heuristic-multisignal-candidate-ranking-v1"


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
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_formatting import (
    format_split_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
    build_split_plan,
)


def main() -> None:
    _static_checks()
    _runtime_real_target_checks()
    print("HEURISTIC_ENGINE: MULTI_SIGNAL_CONSTRAINED_CANDIDATE_SEARCH")
    print("CANDIDATE_SET: DEPENDENCY_BALANCED_RESPONSIBILITY")
    print("AFFINITY_SIGNALS: STRUCTURAL_SEMANTIC_SOURCE_PROXIMITY_ROLE")
    print("TINY_HELPER_REPAIR: BOUNDED_MERGE_SEARCH")
    print("SIZE_POLICY: HARD_100_TO_500")
    print("ATOMIC_CLUSTER_PRESERVATION: PASS")
    print("DETERMINISTIC_RANKING: PASS")
    print("MAIN_HELPER_MAPPER_CASE: BLOCKED_TO_PLANNED")
    print("LOCAL_AI_LOGIC: UNCHANGED")
    print("WORKBENCH_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _static_checks() -> None:
    names = (
        "planner_symbol_affinity.py",
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
        "build_ranked_heuristic_candidates",
        "cluster_affinity",
        "heuristic_candidate_selection",
        "dependency_dominant",
        "balanced",
        "responsibility_dominant",
    )
    for token in required:
        if token not in combined:
            raise SystemExit("VALIDATION ERROR: missing heuristic token " + token)
    forbidden = (
        "planner_local_ai_plan_review",
        "planner_local_ai_comprehensive_review",
        "workbench_guarded_apply",
        "workbench_rollback_executor",
    )
    for token in forbidden:
        if token in combined:
            raise SystemExit("VALIDATION ERROR: cross-box or AI contamination: " + token)


def _runtime_real_target_checks() -> None:
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    if not target.exists():
        raise SystemExit("VALIDATION ERROR: real target fixture missing: " + str(target))
    report = analyze_python_file(target)
    first = build_split_plan(report)
    second = build_split_plan(report)
    if first.to_dict() != second.to_dict():
        raise SystemExit("VALIDATION ERROR: heuristic candidate selection is not deterministic")
    if first.status != "planned":
        raise SystemExit("VALIDATION ERROR: real target did not improve from blocked to planned")
    selection = first.import_migration.get("heuristic_candidate_selection")
    if not isinstance(selection, dict):
        raise SystemExit("VALIDATION ERROR: candidate selection evidence missing")
    if selection.get("selected_strategy") != "balanced":
        raise SystemExit("VALIDATION ERROR: balanced candidate was not selected")
    candidates = selection.get("candidates", [])
    if len(candidates) != 3:
        raise SystemExit("VALIDATION ERROR: expected three deterministic candidates")
    statuses = {item.get("strategy"): item.get("status") for item in candidates}
    expected = {
        "dependency_dominant": "blocked",
        "balanced": "valid",
        "responsibility_dominant": "valid",
    }
    if statuses != expected:
        raise SystemExit("VALIDATION ERROR: unexpected candidate status matrix: " + repr(statuses))
    helpers = [module for module in first.proposed_modules if module.role != "public_facade"]
    if len(helpers) != 2:
        raise SystemExit("VALIDATION ERROR: selected plan should have two helpers")
    helper_sizes = sorted(module.estimated_lines for module in helpers)
    if helper_sizes != [122, 452]:
        raise SystemExit("VALIDATION ERROR: unexpected selected helper sizes: " + repr(helper_sizes))
    if any(module.estimated_lines < 100 or module.estimated_lines > 500 for module in helpers):
        raise SystemExit("VALIDATION ERROR: selected helper violates hard 100-500 size gate")
    assignments = {
        symbol_name: module.filename
        for module in helpers
        for symbol_name in module.symbols
    }
    path_cluster = {
        "_find_target_record",
        "_normalize_path_for_compare",
        "_normalize_record_path",
    }
    if len({assignments[name] for name in path_cluster}) != 1:
        raise SystemExit("VALIDATION ERROR: path atomic dependency cluster was split")
    large_cluster = {
        "_record_is_active",
        "_active_records",
        "_target_is_helper_like",
        "_record_is_low_signal_support_file",
        "_target_role",
        "_select_main_record",
        "_main_candidates_for_helper",
        "_select_helper_records",
        "_helper_score",
        "_module_imports",
        "_module_stem",
        "_strip_helper_suffix",
        "_has_helper_suffix",
        "_record_is_private_helper",
        "_public_helper_warnings",
    }
    if len({assignments[name] for name in large_cluster}) != 1:
        raise SystemExit("VALIDATION ERROR: large atomic dependency cluster was split")
    selected_candidate = next(
        item for item in candidates if item.get("candidate_id") == selection.get("selected_candidate_id")
    )
    merge_evidence = selected_candidate.get("merge_evidence", [])
    if not merge_evidence:
        raise SystemExit("VALIDATION ERROR: selected candidate lacks explainable merge evidence")
    if not any(item.get("shared_callers") for item in merge_evidence):
        raise SystemExit("VALIDATION ERROR: structural shared-caller evidence was not recorded")
    if not any(item.get("shared_semantic_tokens") for item in merge_evidence):
        raise SystemExit("VALIDATION ERROR: semantic affinity evidence was not recorded")
    rendered = format_split_plan(first)
    for token in (
        "Heuristic candidate selection:",
        "Selected: heuristic:balanced",
        "Strategy: balanced",
    ):
        if token not in rendered:
            raise SystemExit("VALIDATION ERROR: candidate selection not visible in plan output: " + token)


if __name__ == "__main__":
    main()
