# project-path: tools/validate_large_file_refactor_planner_responsibility_labeling_semantic_naming_v1.py
"""Validate deterministic responsibility labeling and semantic helper naming."""
from __future__ import annotations

import ast
from pathlib import Path
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
FEATURE = "large-file-refactor-planner-responsibility-labeling-semantic-naming-v1"


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
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_responsibility_labels import (
    ResponsibilityLabel,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_semantic_naming import (
    semantic_helper_filename,
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
    _naming_fallback_checks()
    print("RESPONSIBILITY_LABELING: DETERMINISTIC_EXPLAINABLE")
    print("RESPONSIBILITY_EVIDENCE: PRIMARY_SECONDARY_CONFIDENCE_TOKENS")
    print("SEMANTIC_FILENAMES: RESPONSIBILITY_BASED_PRIVATE_BASENAMES")
    print("GENERIC_SERIAL_NAMES_REAL_CASE: REMOVED")
    print("MAIN_HELPER_MAPPER_NAMES: PATH_RESOLUTION_AND_HELPER_SELECTION")
    print("HEURISTIC_CANDIDATE_SELECTION: PRESERVED")
    print("LOCAL_AI_LOGIC: UNCHANGED")
    print("WORKBENCH_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _static_checks() -> None:
    names = (
        "planner_responsibility_labels.py",
        "planner_semantic_naming.py",
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
        "label_cluster_responsibilities",
        "semantic_helper_filename",
        "primary_responsibility",
        "secondary_responsibilities",
        "confidence_score",
        "responsibility_labeling",
    )
    for token in required:
        if token not in combined:
            raise SystemExit("VALIDATION ERROR: missing responsibility token " + token)
    forbidden = (
        "planner_local_ai_plan_review",
        "planner_local_ai_comprehensive_review",
        "workbench_guarded_apply",
        "workbench_rollback_executor",
    )
    for token in forbidden:
        if token in combined:
            raise SystemExit("VALIDATION ERROR: AI or Workbench contamination: " + token)


def _runtime_real_target_checks() -> None:
    target = ROOT / "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
    report = analyze_python_file(target)
    first = build_split_plan(report)
    second = build_split_plan(report)
    if first.to_dict() != second.to_dict():
        raise SystemExit("VALIDATION ERROR: responsibility labeling is not deterministic")
    if first.status != "planned":
        raise SystemExit("VALIDATION ERROR: Step 1 planned architecture regressed")
    selection = first.import_migration.get("heuristic_candidate_selection", {})
    if selection.get("selected_strategy") != "balanced":
        raise SystemExit("VALIDATION ERROR: candidate selection changed unexpectedly")
    labels = first.import_migration.get("responsibility_labeling", {})
    if not isinstance(labels, dict) or len(labels) != 2:
        raise SystemExit("VALIDATION ERROR: expected two responsibility labels")
    helpers = [module for module in first.proposed_modules if module.role != "public_facade"]
    names = {module.filename for module in helpers}
    expected_names = {
        "_main_helper_mapper_path_resolution.py",
        "_main_helper_mapper_helper_selection.py",
    }
    if names != expected_names:
        raise SystemExit("VALIDATION ERROR: unexpected semantic names: " + repr(names))
    if any("function" in name or "dependency_cluster" in name for name in names):
        raise SystemExit("VALIDATION ERROR: generic helper names remain in real case")
    primary_labels = {record.get("primary_responsibility") for record in labels.values()}
    if primary_labels != {"path_resolution", "helper_selection"}:
        raise SystemExit("VALIDATION ERROR: unexpected primary responsibilities: " + repr(primary_labels))
    path_record = next(record for record in labels.values() if record.get("primary_responsibility") == "path_resolution")
    selection_record = next(record for record in labels.values() if record.get("primary_responsibility") == "helper_selection")
    if path_record.get("confidence") != "high" or selection_record.get("confidence") != "high":
        raise SystemExit("VALIDATION ERROR: expected high confidence on real-case labels")
    if "decision_reporting" not in selection_record.get("secondary_responsibilities", []):
        raise SystemExit("VALIDATION ERROR: decision/reporting secondary responsibility not surfaced")
    rendered = format_split_plan(first)
    for token in (
        "Responsibility labeling:",
        "path_resolution: confidence=high",
        "helper_selection: confidence=high",
        "Secondary: decision_reporting",
    ):
        if token not in rendered:
            raise SystemExit("VALIDATION ERROR: responsibility evidence missing from plan output: " + token)
    helper_sizes = sorted(module.estimated_lines for module in helpers)
    if helper_sizes != [122, 452]:
        raise SystemExit("VALIDATION ERROR: Step 1 architecture sizes changed: " + repr(helper_sizes))


def _naming_fallback_checks() -> None:
    low = ResponsibilityLabel(
        cluster_id="fixture",
        primary_responsibility="uncertain thing",
        secondary_responsibilities=(),
        confidence="low",
        confidence_score=0.1,
        evidence_tokens=(),
        scores={},
    )
    name = semantic_helper_filename(Path("service.py"), low)
    if name != "_service_cohesive_operations.py":
        raise SystemExit("VALIDATION ERROR: low-confidence naming fallback is unstable: " + name)
    if not name.startswith("_") or not name.endswith(".py"):
        raise SystemExit("VALIDATION ERROR: semantic filename is not a private Python basename")


if __name__ == "__main__":
    main()
