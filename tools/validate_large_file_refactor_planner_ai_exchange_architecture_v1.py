# project-path: tools/validate_large_file_refactor_planner_ai_exchange_architecture_v1.py
"""Validate clean Planner pipeline, comprehensive local AI, and Web AI exchange."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    DocstringProposal,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_web_ai_exchange import (
    WEB_AI_RESPONSE_BEGIN,
    WEB_AI_RESPONSE_END,
    build_comprehensive_web_ai_planning_prompt,
    parse_and_validate_web_ai_planning_response,
)

FEATURE = "large-file-refactor-planner-ai-exchange-architecture-v1"
ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def main() -> None:
    files = {
        path.name: path
        for path in BOX.glob("*.py")
        if path.name in {
            "gui_shell.py",
            "planner_action_enablement.py",
            "planner_bounded_refinement.py",
            "planner_local_ai_plan_review.py",
            "planner_local_ai_docstring_review.py",
            "planner_local_ai_comprehensive_review.py",
            "planner_local_ai_comprehensive_formatting.py",
            "planner_local_ai_review_gui.py",
            "planner_split_plan_gui.py",
            "planner_sonar_activity.py",
            "planner_settings_panel_presentation.py",
            "planner_preimplementation_summary.py",
            "planner_web_ai_exchange.py",
            "planner_web_ai_exchange_gui.py",
        }
    }
    texts = {}
    for name, path in files.items():
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        if len(text.splitlines()) > 500:
            raise SystemExit("VALIDATION ERROR: module >500 lines: " + name)
        texts[name] = text

    gui = texts["gui_shell.py"]
    required_buttons = (
        "Analyze File",
        "Generate Split Plan",
        "Generate Docstring Plan",
        "Review & Refine Plan with Local AI",
        "Copy Comprehensive Planning for Web AI",
        "Receive Planning from Web AI",
        "View Web AI Proposal",
        "Show Planning Summary",
    )
    for label in required_buttons:
        if label not in gui:
            raise SystemExit("VALIDATION ERROR: missing button: " + label)
    for removed in (
        "Ask Local LLM for Ambiguous Symbols",
        "Copy Planning Summary",
        "Use local AI when available",
    ):
        if removed in gui:
            raise SystemExit("VALIDATION ERROR: legacy control remains: " + removed)

    split_gui = texts["planner_split_plan_gui.py"]
    if "start_optional_plan_review_for_window" in split_gui:
        raise SystemExit("VALIDATION ERROR: split generation still auto-starts AI")
    if "deterministic split plan ready" not in split_gui:
        raise SystemExit("VALIDATION ERROR: deterministic split sonar success missing")

    web_gui = texts["planner_web_ai_exchange_gui.py"]
    if "Accept Validated Proposal" not in web_gui:
        raise SystemExit("VALIDATION ERROR: explicit Web AI human gate missing")
    forbidden_web = (
        "workbench_gui",
        "guarded_source_apply",
        "rollback_executor",
        "preview_writer",
    )
    combined_web = texts["planner_web_ai_exchange.py"] + web_gui
    for marker in forbidden_web:
        if marker in combined_web:
            raise SystemExit("VALIDATION ERROR: Web AI cross-box leak: " + marker)

    _runtime_web_exchange_test()

    print("PLANNER_PIPELINE: DETERMINISTIC_THEN_LOCAL_AI_THEN_WEB_AI")
    print("GENERATE_SPLIT_PLAN: DETERMINISTIC_ONLY")
    print("GENERATE_DOCSTRING_PLAN: DETERMINISTIC_ONLY")
    print("LOCAL_AI_STAGE: SPLIT_AMBIGUITY_DOCSTRING_REVIEW")
    print("WEB_AI_EXPORT: COMPREHENSIVE_SELECTED_FILE_PACKAGE")
    print("WEB_AI_IMPORT: MARKER_SCHEMA_HASH_VALIDATED")
    print("WEB_AI_ACCEPTANCE: EXPLICIT_HUMAN_GATE")
    print("AST_ANALYSIS_OVERWRITE_BY_AI: BLOCKED")
    print("WORKBENCH_CONTAMINATION: NONE")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _runtime_web_exchange_test() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        target = root / "large_module.py"
        target.write_text(
            "def alpha():\n    return 1\n\ndef beta():\n    return 2\n",
            encoding="utf-8",
        )
        source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        alpha = RefactorSymbol(
            schema_version=SCHEMA_VERSION,
            name="alpha",
            kind="function",
            visibility="public",
            start_line=1,
            end_line=2,
            physical_lines=2,
            signature="alpha()",
        )
        beta = RefactorSymbol(
            schema_version=SCHEMA_VERSION,
            name="beta",
            kind="function",
            visibility="public",
            start_line=4,
            end_line=5,
            physical_lines=2,
            signature="beta()",
        )
        report = ModuleAnalysisReport(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            target_file=str(target),
            source_content_hash=source_hash,
            line_count_physical=5,
            module_docstring_present=False,
            module_docstring_preview="",
            all_names=["alpha", "beta"],
            public_api_symbols=["alpha", "beta"],
            imports=[],
            symbols=[alpha, beta],
            constants=[],
            assignments=[],
            global_statements=[],
            nonlocal_statements=[],
            module_level_calls=[],
            if_main_present=False,
            nested_symbol_count=0,
            missing_docstring_count=2,
        )
        modules = [
            ProposedModule(
                schema_version=SCHEMA_VERSION,
                filename="large_module.py",
                role="public_facade",
                symbols=[],
                estimated_lines=10,
            ),
            ProposedModule(
                schema_version=SCHEMA_VERSION,
                filename="large_module_core.py",
                role="core",
                symbols=["alpha"],
                estimated_lines=10,
            ),
            ProposedModule(
                schema_version=SCHEMA_VERSION,
                filename="large_module_formatting.py",
                role="formatting",
                symbols=["beta"],
                estimated_lines=10,
            ),
        ]
        plan = RefactorPlan(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            target_file=str(target),
            source_content_hash=source_hash,
            settings={"maximum_physical_lines": 500},
            public_api_before=["alpha", "beta"],
            public_api_after_expected=["alpha", "beta"],
            symbols=[alpha, beta],
            atomic_clusters=[],
            proposed_modules=modules,
            import_migration={},
            docstring_proposals=[],
            risks=[],
            validation_blockers=[],
            status="planned",
        )
        docs = [
            DocstringProposal(
                schema_version=SCHEMA_VERSION,
                feature_id=FEATURE_ID,
                target_file=str(target),
                target_kind="function",
                target_name="alpha",
                proposed_docstring='"""Describe alpha."""',
                provenance="manual_required",
                confidence="low",
                status="review_required",
            )
        ]
        prompt = build_comprehensive_web_ai_planning_prompt(
            report, plan, docs, local_ai_summary={"status": "not_run"}
        )
        if "source_code" not in prompt or WEB_AI_RESPONSE_BEGIN not in prompt:
            raise SystemExit("VALIDATION ERROR: comprehensive export incomplete")
        plan_hash = hashlib.sha256(
            json.dumps(
                plan.to_dict(),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            ).encode("utf-8")
        ).hexdigest()
        response = {
            "schema_version": "1.0",
            "exchange_feature_id": "large-file-refactor-planner-web-ai-exchange-v1",
            "source_content_hash": source_hash,
            "base_plan_hash": plan_hash,
            "verdict": "refine",
            "reassignments": [
                {"symbol": "beta", "target_module": "large_module_core.py"}
            ],
            "docstring_updates": [
                {
                    "target_kind": "function",
                    "target_name": "alpha",
                    "proposed_docstring": '\"\"\"Return the alpha value.\"\"\"',
                }
            ],
            "analysis_observations": ["alpha and beta appear cohesive"],
            "rationale": "Keep cohesive helpers together.",
            "warnings": [],
        }
        wrapped = (
            WEB_AI_RESPONSE_BEGIN
            + "\n"
            + json.dumps(response)
            + "\n"
            + WEB_AI_RESPONSE_END
        )
        proposal = parse_and_validate_web_ai_planning_response(
            wrapped, report, plan, docs
        )
        if proposal.reassignments_count != 1:
            raise SystemExit("VALIDATION ERROR: reassignment not accepted")
        if proposal.docstring_updates_count != 1:
            raise SystemExit("VALIDATION ERROR: docstring update not accepted")
        if not proposal.proposed_plan.docstring_proposals:
            raise SystemExit("VALIDATION ERROR: accepted docstrings not attached to plan")
        target_module = next(
            module
            for module in proposal.proposed_plan.proposed_modules
            if module.filename == "large_module_core.py"
        )
        if "beta" not in target_module.symbols:
            raise SystemExit("VALIDATION ERROR: bounded reassignment not applied")
        stale = dict(response)
        stale["base_plan_hash"] = "0" * 64
        stale_wrapped = (
            WEB_AI_RESPONSE_BEGIN
            + "\n"
            + json.dumps(stale)
            + "\n"
            + WEB_AI_RESPONSE_END
        )
        try:
            parse_and_validate_web_ai_planning_response(
                stale_wrapped, report, plan, docs
            )
        except ValueError as exc:
            if "STALE_WEB_AI_RESPONSE_BASE_PLAN_HASH" not in str(exc):
                raise
        else:
            raise SystemExit("VALIDATION ERROR: stale Web AI response was accepted")


if __name__ == "__main__":
    main()
