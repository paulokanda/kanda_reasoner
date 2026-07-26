# project-path: tools/validate_large_file_refactor_planner_imported_web_ai_semantics_v1.py
"""Validate native generation routes, imported Web AI semantics, and version rendering."""

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
FEATURE = "large-file-refactor-planner-imported-web-ai-semantics-v1"


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

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    DocstringProposal,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_ai_architecture_questions import (
    ARCHITECTURE_REVIEW_QUESTIONS,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_WEB_AI,
    get_planner_exchange_base_bundle,
    initialize_planner_version_state,
    select_planner_version,
    store_heuristic_version,
    store_local_ai_version,
    store_web_ai_version,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_versioned_generation import (
    planner_generation_route,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_web_ai_exchange import (
    WEB_AI_RESPONSE_BEGIN,
    WEB_AI_RESPONSE_END,
    build_comprehensive_web_ai_planning_prompt,
    parse_and_validate_web_ai_planning_response,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_web_ai_import_artifact import (
    build_web_ai_import_contract,
    read_installed_web_ai_response,
    web_ai_import_artifact_path,
)


def main() -> None:
    texts = _static_checks()
    _runtime_route_checks()
    _runtime_native_export_base_checks()
    _runtime_import_contract_checks()
    print("VERSION_LABEL: IMPORTED_WEB_AI_VERSION")
    print("HEURISTIC_ROUTE: AUTO_DOCSTRINGS")
    print("LOCAL_AI_ROUTE: AUTO_DOCSTRINGS_THEN_LOCAL_AI")
    print("IMPORTED_WEB_AI_ROUTE: NOT_LOCALLY_GENERATED")
    print("WEB_AI_EXPORT_BASE: LAST_GENERATED_NATIVE_PLAN")
    print("WEB_AI_IMPORT: INSTALLED_EXTERNAL_ARTIFACT_THEN_REVIEW")
    print("PROPOSED_PLAN_PANEL: SELECTED_VERSION_RENDERING")
    print("WORKBENCH_HANDOFF_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _static_checks() -> dict[str, str]:
    names = (
        "gui_shell.py",
        "planner_version_state.py",
        "planner_version_selector_gui.py",
        "planner_versioned_generation.py",
        "planner_web_ai_exchange.py",
        "planner_web_ai_exchange_gui.py",
        "planner_web_ai_import_artifact.py",
        "planner_local_ai_review_gui.py",
        "planner_preimplementation_summary.py",
    )
    texts: dict[str, str] = {}
    for name in names:
        path = BOX / name
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        lines = len(text.splitlines())
        if lines > 500:
            raise SystemExit(f"VALIDATION ERROR: {name} exceeds 500 lines: {lines}")
        texts[name] = text
    selector = texts["planner_version_selector_gui.py"]
    if '(PLANNER_VERSION_WEB_AI, "Imported Web AI Version")' not in selector:
        raise SystemExit("VALIDATION ERROR: imported Web AI label missing")
    if "render_selected_planner_version(window)" not in selector:
        raise SystemExit("VALIDATION ERROR: selected version does not rerender panel")
    gui = texts["gui_shell.py"]
    if "selected_version == PLANNER_VERSION_WEB_AI" not in gui:
        raise SystemExit("VALIDATION ERROR: imported Web AI local-generation block missing")
    web_gui = texts["planner_web_ai_exchange_gui.py"]
    for token in (
        "get_last_generated_native_bundle",
        "read_installed_web_ai_response",
        "Load as Imported Web AI Version",
        "Review Imported Web AI Version",
    ):
        if token not in web_gui:
            raise SystemExit("VALIDATION ERROR: imported Web AI GUI contract missing " + token)
    web_core = texts["planner_web_ai_exchange.py"]
    if "Create an installable ZIP containing INSTALL.ps1" not in web_core:
        raise SystemExit("VALIDATION ERROR: external installer ZIP contract missing")
    all_text = "\n".join(texts.values())
    for token in ("workbench_guarded_apply", "workbench_rollback_executor"):
        if token in all_text:
            raise SystemExit("VALIDATION ERROR: Workbench contamination: " + token)
    return texts


def _runtime_route_checks() -> None:
    heuristic = planner_generation_route(PLANNER_VERSION_HEURISTIC)
    local_ai = planner_generation_route(PLANNER_VERSION_LOCAL_AI)
    imported = planner_generation_route(PLANNER_VERSION_WEB_AI)
    if not heuristic.generate_docstrings_automatically or heuristic.start_local_ai_review:
        raise SystemExit("VALIDATION ERROR: heuristic auto-docstring route incorrect")
    if not local_ai.generate_docstrings_automatically or not local_ai.start_local_ai_review:
        raise SystemExit("VALIDATION ERROR: Local AI route incorrect")
    if imported.generate_docstrings_automatically or imported.start_local_ai_review or imported.prepare_web_ai_exchange:
        raise SystemExit("VALIDATION ERROR: imported Web AI is still treated as local generation route")


def _runtime_native_export_base_checks() -> None:
    report, heuristic_plan, local_plan, web_plan, proposals = _fixtures()
    window = SimpleNamespace()
    initialize_planner_version_state(window)
    store_heuristic_version(window, heuristic_plan, proposals)
    if get_planner_exchange_base_bundle(window).version_name != PLANNER_VERSION_HEURISTIC:
        raise SystemExit("VALIDATION ERROR: heuristic was not recorded as latest native base")
    store_local_ai_version(window, local_plan, proposals)
    select_planner_version(window, PLANNER_VERSION_WEB_AI)
    base = get_planner_exchange_base_bundle(window)
    if base is None or base.version_name != PLANNER_VERSION_LOCAL_AI:
        raise SystemExit("VALIDATION ERROR: selected display radio changed Web AI export base")
    store_web_ai_version(window, web_plan, proposals)
    base = get_planner_exchange_base_bundle(window)
    if base is None or base.version_name != PLANNER_VERSION_LOCAL_AI:
        raise SystemExit("VALIDATION ERROR: imported version contaminated latest native export base")


def _runtime_import_contract_checks() -> None:
    report, _heuristic_plan, local_plan, _web_plan, proposals = _fixtures()
    temp_project = Path(tempfile.mkdtemp(prefix="kanda_web_ai_import_")) / "demo_project"
    temp_project.mkdir(parents=True, exist_ok=True)
    contract = build_web_ai_import_contract(temp_project)
    prompt = build_comprehensive_web_ai_planning_prompt(
        report,
        local_plan,
        proposals,
        import_contract=contract,
        base_version_name=PLANNER_VERSION_LOCAL_AI,
    )
    if "installable ZIP" not in prompt or '"base_version_name": "local_ai"' not in prompt:
        raise SystemExit("VALIDATION ERROR: export prompt lacks installer/base-version semantics")
    package_text = prompt.split("KANDA_COMPREHENSIVE_PLANNING_PACKAGE_BEGIN\n", 1)[1].split(
        "\nKANDA_COMPREHENSIVE_PLANNING_PACKAGE_END", 1
    )[0]
    package = json.loads(package_text)
    answers = {
        question_id: "Reviewed from supplied deterministic evidence."
        for question_id, _question in ARCHITECTURE_REVIEW_QUESTIONS
    }
    payload = {
        "schema_version": "2.0",
        "exchange_feature_id": "large-file-refactor-planner-web-ai-exchange-v2",
        "source_content_hash": report.source_content_hash,
        "base_plan_hash": package["base_plan_hash"],
        "verdict": "valid",
        "module_merges": [],
        "reassignments": [],
        "module_renames": [],
        "docstring_updates": [],
        "architecture_answers": answers,
        "analysis_observations": [],
        "rationale": "Imported version preserves validated architecture.",
        "warnings": [],
    }
    raw = WEB_AI_RESPONSE_BEGIN + "\n" + json.dumps(payload) + "\n" + WEB_AI_RESPONSE_END
    artifact = web_ai_import_artifact_path(temp_project)
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(raw, encoding="utf-8")
    loaded = read_installed_web_ai_response(temp_project)
    proposal = parse_and_validate_web_ai_planning_response(
        loaded, report, local_plan, proposals
    )
    if proposal.proposed_plan.status != local_plan.status:
        raise SystemExit("VALIDATION ERROR: installed artifact did not validate into imported version")


def _fixtures() -> tuple[ModuleAnalysisReport, RefactorPlan, RefactorPlan, RefactorPlan, list[DocstringProposal]]:
    temp_root = Path(tempfile.gettempdir()) / "kanda_imported_web_ai_semantics_fixture"
    temp_root.mkdir(parents=True, exist_ok=True)
    target = temp_root / "fixture.py"
    target.write_text('"""fixture"""\n\ndef helper():\n    return 1\n', encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    report = ModuleAnalysisReport(
        schema_version="1.0",
        feature_id="architecture-review-large-file-refactor-planner-v1",
        target_file=str(target),
        source_content_hash=source_hash,
        line_count_physical=4,
        module_docstring_present=True,
        module_docstring_preview="fixture",
        all_names=["helper"],
        public_api_symbols=[],
        imports=[],
        symbols=[],
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )
    proposal = DocstringProposal(
        schema_version="1.0",
        feature_id=report.feature_id,
        target_file=str(target),
        target_kind="planned_module",
        target_name="fixture.py",
        proposed_docstring='"""Fixture plan."""',
        provenance="deterministic_template",
        confidence="medium",
    )
    module = ProposedModule(
        schema_version="1.0",
        filename="fixture.py",
        role="public_facade",
        symbols=[],
        estimated_lines=200,
        status="planned",
    )
    base = dict(
        schema_version="1.0",
        feature_id=report.feature_id,
        target_file=str(target),
        source_content_hash=source_hash,
        settings={"minimum_helper_physical_lines": 100, "maximum_physical_lines": 500},
        public_api_before=[],
        public_api_after_expected=[],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[module],
        import_migration={},
        docstring_proposals=[proposal],
        risks=[],
        validation_blockers=[],
        status="planned",
    )
    heuristic = RefactorPlan(**base)
    local_ai = RefactorPlan(**{**base, "risks": ["LOCAL_AI_REVIEWED"]})
    web_ai = RefactorPlan(**{**base, "risks": ["IMPORTED_WEB_AI_REVIEWED"]})
    return report, heuristic, local_ai, web_ai, [proposal]


if __name__ == "__main__":
    main()
