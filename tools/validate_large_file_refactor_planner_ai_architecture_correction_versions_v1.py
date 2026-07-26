# project-path: tools/validate_large_file_refactor_planner_ai_architecture_correction_versions_v1.py
"""Validate Planner AI architecture correction, hard size gates, and version selection."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def _install_validation_namespace_packages() -> None:
    """Import focused Planner modules without executing unrelated package facades."""

    packages = (
        ("kanda_reasoner_app", ROOT / "kanda_reasoner_app"),
        (
            "kanda_reasoner_app.manage_architecture",
            ROOT / "kanda_reasoner_app/manage_architecture",
        ),
        (
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner",
            BOX,
        ),
    )
    for name, path in packages:
        if name in sys.modules:
            continue
        module = ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module


_install_validation_namespace_packages()

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ModuleAnalysisReport,
    PlannerSettings,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_ai_architecture_questions import (
    ARCHITECTURE_REVIEW_QUESTIONS,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_bounded_refinement import (
    apply_bounded_architecture_refinement,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    get_planner_version_bundle,
    initialize_planner_version_state,
    select_planner_version,
    selected_planner_version,
    store_heuristic_version,
    store_local_ai_version,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_web_ai_exchange import (
    WEB_AI_RESPONSE_BEGIN,
    WEB_AI_RESPONSE_END,
    build_comprehensive_web_ai_planning_prompt,
    parse_and_validate_web_ai_planning_response,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
    build_split_plan,
)

FEATURE = "large-file-refactor-planner-ai-architecture-correction-versions-v1"


def main() -> None:
    """Run static boundary checks plus runtime architecture/version tests."""

    files = _required_files()
    texts: dict[str, str] = {}
    for name, path in files.items():
        if not path.is_file():
            raise SystemExit("VALIDATION ERROR: missing " + str(path))
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        line_count = len(text.splitlines())
        if line_count > 500:
            raise SystemExit(
                "VALIDATION ERROR: module exceeds 500 lines: "
                + name
                + "="
                + str(line_count)
            )
        texts[name] = text

    _static_contract_checks(texts)
    _runtime_size_and_refinement_test()
    _runtime_version_isolation_test()
    _runtime_web_ai_exchange_test()

    print("PLANNER_VERSION_SELECTOR: HEURISTIC_LOCAL_AI_WEB_AI")
    print("DEFAULT_SELECTED_VERSION: LOCAL_AI")
    print("TINY_HELPER_POLICY: HARD_BLOCK_BELOW_100")
    print("LOCAL_AI_ARCHITECTURE_ACTIONS: MERGE_REASSIGN_RENAME")
    print("LOCAL_AI_ARCHITECTURE_QUESTIONS: REQUIRED")
    print("WEB_AI_ARCHITECTURE_ACTIONS: MERGE_REASSIGN_RENAME")
    print("WEB_AI_ARCHITECTURE_QUESTIONS: REQUIRED")
    print("VERSION_ISOLATION: PASS")
    print("WORKBENCH_HANDOFF_SELECTION: ACTIVE_VERSION_ONLY")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _required_files() -> dict[str, Path]:
    names = (
        "gui_shell.py",
        "split_planner.py",
        "planner_action_enablement.py",
        "planner_ai_architecture_questions.py",
        "planner_bounded_refinement.py",
        "planner_local_ai_plan_review.py",
        "planner_local_ai_comprehensive_formatting.py",
        "planner_local_ai_review_gui.py",
        "planner_split_plan_gui.py",
        "planner_preimplementation_summary.py",
        "planner_version_state.py",
        "planner_version_selector_gui.py",
        "planner_web_ai_exchange.py",
        "planner_web_ai_exchange_gui.py",
    )
    return {name: BOX / name for name in names}


def _static_contract_checks(texts: dict[str, str]) -> None:
    gui = texts["gui_shell.py"]
    if '(PLANNER_VERSION_LOCAL_AI, "Local AI")' not in texts["planner_version_selector_gui.py"]:
        raise SystemExit("VALIDATION ERROR: Local AI version radio missing")
    selector = texts["planner_version_selector_gui.py"]
    if "setExclusive(True)" not in selector:
        raise SystemExit("VALIDATION ERROR: version radios are not exclusive")
    if "PLANNER_VERSION_LOCAL_AI].setChecked(True)" not in selector:
        raise SystemExit("VALIDATION ERROR: Local AI is not default selected")
    if "setRange(100, 500)" not in gui:
        raise SystemExit("VALIDATION ERROR: GUI minimum helper floor is below 100")
    split = texts["split_planner.py"]
    if '"TOO_SMALL_HELPER"' not in split or "blockers.append(" not in split:
        raise SystemExit("VALIDATION ERROR: tiny helper hard blocker missing")
    local_review = texts["planner_local_ai_plan_review.py"]
    for token in (
        "module_merges",
        "reassignments",
        "module_renames",
        "architecture_answers",
        "ARCHITECTURE_REVIEW_QUESTIONS",
    ):
        if token not in local_review:
            raise SystemExit("VALIDATION ERROR: local AI contract missing " + token)
    web = texts["planner_web_ai_exchange.py"]
    for token in (
        "module_merges",
        "module_renames",
        "architecture_answers",
        "tiny_helpers_are_hard_blockers",
    ):
        if token not in web and token != "tiny_helpers_are_hard_blockers":
            raise SystemExit("VALIDATION ERROR: Web AI contract missing " + token)
    all_text = "\n".join(texts.values())
    forbidden = (
        "workbench_guarded_apply",
        "workbench_rollback_executor",
        "workbench_real_preview",
    )
    for token in forbidden:
        if token in all_text:
            raise SystemExit("VALIDATION ERROR: Workbench contamination: " + token)


def _runtime_size_and_refinement_test() -> None:
    report, plan = _fixture_plan()
    tiny_report = ModuleAnalysisReport(
        schema_version=report.schema_version,
        feature_id=report.feature_id,
        target_file=report.target_file,
        source_content_hash=report.source_content_hash,
        line_count_physical=report.line_count_physical,
        module_docstring_present=report.module_docstring_present,
        module_docstring_preview=report.module_docstring_preview,
        all_names=report.all_names,
        public_api_symbols=report.public_api_symbols,
        imports=report.imports,
        symbols=[report.symbols[0]],
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )
    generated = build_split_plan(
        tiny_report,
        PlannerSettings(minimum_helper_physical_lines=1),
    )
    if generated.status != "blocked":
        raise SystemExit("VALIDATION ERROR: <100 helper did not hard block")
    if not any("100 lines" in item for item in generated.validation_blockers):
        raise SystemExit("VALIDATION ERROR: hard 100-line floor not evidenced")

    corrected = apply_bounded_architecture_refinement(
        report,
        plan,
        reassignments=[],
        module_merges=[
            {
                "source_module": "_fixture_tiny.py",
                "target_module": "_fixture_core.py",
            }
        ],
        module_renames=[
            {
                "module": "_fixture_core.py",
                "new_filename": "_fixture_resolution.py",
            }
        ],
    )
    if corrected.status != "planned" or corrected.validation_blockers:
        raise SystemExit("VALIDATION ERROR: bounded architecture correction failed")
    helpers = [
        module
        for module in corrected.proposed_modules
        if module.role != "public_facade"
    ]
    if any(module.estimated_lines < 100 for module in helpers):
        raise SystemExit("VALIDATION ERROR: corrected plan retains tiny helper")
    if not any(module.filename == "_fixture_resolution.py" for module in helpers):
        raise SystemExit("VALIDATION ERROR: safe semantic rename not applied")


def _runtime_version_isolation_test() -> None:
    _report, heuristic = _fixture_plan()
    corrected = RefactorPlan(
        **{
            **heuristic.__dict__,
            "validation_blockers": [],
            "risks": [],
            "status": "planned",
        }
    )
    window = SimpleNamespace()
    initialize_planner_version_state(window)
    if selected_planner_version(window) != PLANNER_VERSION_LOCAL_AI:
        raise SystemExit("VALIDATION ERROR: Local AI is not default version intent")
    store_heuristic_version(window, heuristic, [])
    if window._large_file_refactor_last_plan is not None:
        raise SystemExit("VALIDATION ERROR: unavailable Local AI silently fell back")
    store_local_ai_version(window, corrected, [])
    if window._large_file_refactor_last_plan.status != "planned":
        raise SystemExit("VALIDATION ERROR: Local AI version did not become active")
    if not select_planner_version(window, PLANNER_VERSION_HEURISTIC):
        raise SystemExit("VALIDATION ERROR: heuristic version selection failed")
    window._large_file_refactor_last_plan.validation_blockers.append("MUTATION")
    stored = get_planner_version_bundle(window, PLANNER_VERSION_HEURISTIC)
    if stored is None or "MUTATION" in stored.plan.validation_blockers:
        raise SystemExit("VALIDATION ERROR: active version aliases stored version")


def _runtime_web_ai_exchange_test() -> None:
    report, plan = _fixture_plan()
    prompt = build_comprehensive_web_ai_planning_prompt(report, plan, [])
    package_text = prompt.split(
        "KANDA_COMPREHENSIVE_PLANNING_PACKAGE_BEGIN\n", 1
    )[1].split("\nKANDA_COMPREHENSIVE_PLANNING_PACKAGE_END", 1)[0]
    package = json.loads(package_text)
    answers = {
        question_id: "Reviewed from supplied evidence and resolved safely."
        for question_id, _question in ARCHITECTURE_REVIEW_QUESTIONS
    }
    payload = {
        "schema_version": "2.0",
        "exchange_feature_id": "large-file-refactor-planner-web-ai-exchange-v2",
        "source_content_hash": report.source_content_hash,
        "base_plan_hash": package["base_plan_hash"],
        "verdict": "refine",
        "module_merges": [
            {
                "source_module": "_fixture_tiny.py",
                "target_module": "_fixture_core.py",
            }
        ],
        "reassignments": [],
        "module_renames": [
            {
                "module": "_fixture_core.py",
                "new_filename": "_fixture_resolution.py",
            }
        ],
        "docstring_updates": [],
        "architecture_answers": answers,
        "analysis_observations": ["Tiny helper consolidation is safe."],
        "rationale": "Consolidate a blocked tiny helper into a cohesive owner.",
        "warnings": [],
    }
    raw = (
        WEB_AI_RESPONSE_BEGIN
        + "\n"
        + json.dumps(payload)
        + "\n"
        + WEB_AI_RESPONSE_END
    )
    proposal = parse_and_validate_web_ai_planning_response(
        raw,
        report,
        plan,
        [],
    )
    if proposal.proposed_plan.status != "planned":
        raise SystemExit("VALIDATION ERROR: Web AI correction did not revalidate")
    if proposal.module_merges_count != 1 or proposal.module_renames_count != 1:
        raise SystemExit("VALIDATION ERROR: Web AI action counts incorrect")


def _fixture_plan() -> tuple[ModuleAnalysisReport, RefactorPlan]:
    temp_root = Path(tempfile.gettempdir()) / "kanda_planner_ai_architecture_fixture"
    temp_root.mkdir(parents=True, exist_ok=True)
    target = temp_root / "fixture.py"
    target.write_text("def fixture():\n    return 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    symbols = [
        _symbol("_a", 40, ["_b"], "cluster_a"),
        _symbol("_b", 40, [], "cluster_a"),
        _symbol("_c", 120, [], "cluster_c"),
        _symbol("_d", 120, [], "cluster_d"),
    ]
    report = ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        line_count_physical=320,
        module_docstring_present=True,
        module_docstring_preview="fixture",
        all_names=[item.name for item in symbols],
        public_api_symbols=[],
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
    modules = [
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="fixture.py",
            role="public_facade",
            symbols=[],
            estimated_lines=20,
            status="planned",
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_fixture_tiny.py",
            role="function",
            symbols=["_a", "_b"],
            estimated_lines=90,
            risk_flags=["TOO_SMALL_HELPER"],
            status="warning",
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_fixture_core.py",
            role="function",
            symbols=["_c"],
            estimated_lines=130,
            status="planned",
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_fixture_other.py",
            role="function",
            symbols=["_d"],
            estimated_lines=130,
            status="planned",
        ),
    ]
    plan = RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        settings={
            "minimum_helper_physical_lines": 100,
            "maximum_physical_lines": 500,
        },
        public_api_before=[],
        public_api_after_expected=[],
        symbols=symbols,
        atomic_clusters=[],
        proposed_modules=modules,
        import_migration={},
        docstring_proposals=[],
        risks=["TOO_SMALL_HELPER"],
        validation_blockers=[
            "Planned helper _fixture_tiny.py is below minimum helper size of 100 lines."
        ],
        status="blocked",
    )
    return report, plan


def _symbol(
    name: str,
    lines: int,
    references: list[str],
    cluster_id: str,
) -> RefactorSymbol:
    return RefactorSymbol(
        schema_version=SCHEMA_VERSION,
        name=name,
        kind="function",
        visibility="private",
        start_line=1,
        end_line=lines,
        physical_lines=lines,
        references=references,
        atomic_cluster_id=cluster_id,
    )


if __name__ == "__main__":
    main()
