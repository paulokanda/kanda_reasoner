"""Validate Stage 5 analyzer transport, Preview evidence, and cumulative correction repair."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import inspect
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import advanced_quality_cross_check_rules as rules
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import griffe_api_fitness_adapter
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import mypy_fitness_adapter
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import ruff_fitness_adapter
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import AnalysisExecutionStatus
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_environment_contract import AnalyzerCapabilityMode
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_specific_delta_strategies import GraphTopologyDeltaState
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.aqr_expected_topology import derive_expected_preview_import_edges
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_preview_rendering import _filtered_import_blocks as filter_facade_imports
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.helper_import_synthesizer import _filtered_import_blocks as filter_helper_imports
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.helper_import_synthesizer import _type_checking_import_blocks

FEATURE_ID = "advanced-quality-review-stage5-runtime-cumulative-correction-repair-v1"


def check(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def main() -> int:
    ruff_source = inspect.getsource(ruff_fitness_adapter)
    griffe_source = inspect.getsource(griffe_api_fitness_adapter)
    mypy_source = inspect.getsource(mypy_fitness_adapter)
    check('"--output-file"' in ruff_source and 'load_machine_output_as_stdout' in ruff_source,
          "RUFF_MACHINE_OUTPUT_FILE_AVOIDS_STDOUT_TRUNCATION")
    check('"--output"' in griffe_source and 'load_machine_output_as_stdout' in griffe_source,
          "GRIFFE_MACHINE_OUTPUT_FILE_AVOIDS_STDOUT_TRUNCATION")
    check('"--explicit-package-bases"' in mypy_source,
          "MYPY_SEALED_VIEW_EXPLICIT_PACKAGE_BASES")

    helper_blocks = filter_helper_imports(
        ["from .schemas import ProjectModuleRecord, ProjectSymbol, normalize_project_atlas_text"],
        {"ProjectModuleRecord", "normalize_project_atlas_text"},
    )
    check(helper_blocks == ["from .schemas import ProjectModuleRecord, normalize_project_atlas_text"],
          "HELPER_IMPORT_BLOCKS_NARROW_TO_REQUIRED_NAMES")
    facade_blocks = filter_facade_imports(
        ["from .output_policy import is_active_atlas_path, is_active_test_command"],
        {"is_active_atlas_path"},
    )
    check(facade_blocks == ["from .output_policy import is_active_atlas_path"],
          "FACADE_IMPORTS_NARROW_TO_RETAINED_USAGE")
    type_blocks = _type_checking_import_blocks("main_helper_mapper", ["ProjectSymbolAtlasMainHelperDecision"])
    check("TYPE_CHECKING" in "\n".join(type_blocks) and "ProjectSymbolAtlasMainHelperDecision" in "\n".join(type_blocks),
          "FACADE_ANNOTATION_DEPENDENCY_USES_TYPE_CHECKING_IMPORT")

    preview = SimpleNamespace(
        files=(
            SimpleNamespace(role="public_facade", relative_path="main_helper_mapper.py"),
            SimpleNamespace(role="dependency_cluster_helper", relative_path="_selection.py"),
        ),
        helper_import_synthesis={
            "records": [
                {
                    "helper_filename": "_selection.py",
                    "synthesized_import_blocks": [
                        "from .schemas import ProjectModuleRecord",
                    ],
                }
            ]
        },
        facade_global_import_insertion={
            "insertions": [
                {"helper_filename": "_selection.py"},
            ]
        },
    )
    expected = derive_expected_preview_import_edges(
        target_relative_path="pkg/box/main_helper_mapper.py",
        preview_result=preview,
    )
    expected_set = set(expected)
    check("pkg.box.main_helper_mapper->pkg.box._selection" in expected_set,
          "EXPECTED_TOPOLOGY_INCLUDES_FACADE_TO_HELPER_EDGE")
    check("pkg.box._selection->pkg.box.schemas" in expected_set,
          "EXPECTED_TOPOLOGY_INCLUDES_SYNTHESIZED_HELPER_DEPENDENCY")
    check("pkg.box._selection->pkg.box.main_helper_mapper" in expected_set,
          "EXPECTED_TOPOLOGY_INCLUDES_GOVERNED_DEFERRED_FACADE_DEPENDENCY")

    bundle = SimpleNamespace(execution_status=AnalysisExecutionStatus.SUCCEEDED)
    deltas = tuple(
        SimpleNamespace(
            state=GraphTopologyDeltaState.NEW_EDGE,
            importer=edge.split("->", 1)[0],
            imported=edge.split("->", 1)[1],
        )
        for edge in expected
    )
    topology = SimpleNamespace(bundle=bundle, topology_deltas=deltas)
    result = rules._grimp_topology_rule(topology, expected_new_import_edges=expected)
    check(result.decision is rules.CrossCheckRuleDecision.PASS,
          "GRIMP_EXPECTED_PREVIEW_EDGES_PASS_WITHOUT_BLIND_ALLOWLIST")

    unexpected = SimpleNamespace(
        bundle=bundle,
        topology_deltas=deltas + (
            SimpleNamespace(
                state=GraphTopologyDeltaState.NEW_EDGE,
                importer="pkg.box._selection",
                imported="pkg.other_box.private_owner",
            ),
        ),
    )
    result = rules._grimp_topology_rule(unexpected, expected_new_import_edges=expected)
    check(result.decision is rules.CrossCheckRuleDecision.REVIEW_REQUIRED,
          "GRIMP_UNEXPECTED_EDGE_REMAINS_REVIEW_REQUIRED")

    failed_bundle = SimpleNamespace(
        execution_status=AnalysisExecutionStatus.FAILED,
        deltas=(),
        preview_findings=(),
    )
    check(rules._ruff_regression_rule(failed_bundle).decision is rules.CrossCheckRuleDecision.INDETERMINATE,
          "RUFF_FAILED_EXECUTION_CANNOT_REPORT_PASS")
    check(rules._griffe_contract_rule(failed_bundle).decision is rules.CrossCheckRuleDecision.INDETERMINATE,
          "GRIFFE_FAILED_EXECUTION_CANNOT_REPORT_PASS")
    mypy_result = SimpleNamespace(
        capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE,
        bundle=failed_bundle,
        relocation_deltas=(),
    )
    check(rules._mypy_type_contract_rule(mypy_result).decision is rules.CrossCheckRuleDecision.WARNING,
          "NONAUTHORITATIVE_MYPY_FAILURE_CANNOT_REPORT_PASS")

    service_source = (ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_service.py").read_text(encoding="utf-8")
    receive_source = (ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_exchange_gui.py").read_text(encoding="utf-8")
    gui_source = (ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_gui.py").read_text(encoding="utf-8")
    check("blocked_plan," in service_source and "base_plan: object | None = None" in receive_source,
          "WEB_AI_CORRECTION_EXPORT_BINDS_CURRENT_WORKBENCH_PLAN")
    check("base_plan=current_plan" in gui_source,
          "WEB_AI_CORRECTION_RECEIVE_VALIDATES_AGAINST_CURRENT_WORKBENCH_PLAN")

    touched = [
        "analyzer_machine_output.py",
        "aqr_expected_topology.py",
        "advanced_quality_review_orchestration.py",
        "advanced_quality_cross_check_rules.py",
        "advanced_quality_review_gui_context.py",
        "ruff_fitness_adapter.py",
        "griffe_api_fitness_adapter.py",
        "mypy_fitness_adapter.py",
        "helper_import_synthesizer.py",
        "cst_preview_rendering.py",
        "cst_facade_global_import_inserter.py",
        "planner_web_ai_exchange_gui.py",
        "workbench_stage_correction_service.py",
        "workbench_stage_correction_gui.py",
    ]
    base = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
    for name in touched:
        count = len((base / name).read_text(encoding="utf-8").splitlines())
        if count > 500:
            raise AssertionError("MODULE_OVER_500:" + name + ":" + str(count))
    print("TOUCHED_MODULES_MAX_500_LINES: PASS")
    print("AQR_STAGE5_RUNTIME_CUMULATIVE_CORRECTION_REPAIR: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
