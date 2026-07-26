# project-path: tools/validate_large_file_refactor_planner_local_ai_json_adapter_repair_v1.py
"""Validate tolerant transport extraction with strict Planner AI schema gates."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
FEATURE = "large-file-refactor-planner-local-ai-json-adapter-repair-v1"


def _install_namespace_packages() -> None:
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


_install_namespace_packages()

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_ai_architecture_questions import (
    ARCHITECTURE_REVIEW_QUESTIONS,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_local_ai_json_response import (
    LocalAIJSONResponseError,
    parse_local_ai_json_object,
)
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_local_ai_plan_review as plan_review


def main() -> None:
    files = _required_files()
    texts: dict[str, str] = {}
    for name, path in files.items():
        if not path.is_file():
            raise SystemExit("VALIDATION ERROR: missing " + str(path))
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        if len(text.splitlines()) > 500:
            raise SystemExit("VALIDATION ERROR: module exceeds 500 lines: " + name)
        texts[name] = text

    _static_checks(texts)
    _parser_transport_tests()
    _strict_failure_tests()
    _runtime_architecture_correction_test()

    print("LOCAL_AI_JSON_TRANSPORT: DIRECT_FENCED_PREFIXED_THINK_MARKER_SUPPORTED")
    print("EMPTY_OR_MALFORMED_RESPONSE: FAIL_CLOSED")
    print("LOCAL_AI_SCHEMA_VALIDATION: PRESERVED")
    print("LOCAL_AI_ARCHITECTURE_CORRECTION: BLOCKED_TO_PLANNED")
    print("DETERMINISTIC_REVALIDATION: PASS")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _required_files() -> dict[str, Path]:
    names = (
        "planner_local_ai_json_response.py",
        "planner_local_ai_plan_review.py",
        "planner_local_ai_docstring_review.py",
    )
    return {name: BOX / name for name in names}


def _static_checks(texts: dict[str, str]) -> None:
    helper = texts["planner_local_ai_json_response.py"]
    for token in (
        "_balanced_json_object_candidates",
        "_FENCE_PATTERN",
        "response_length=",
        "LocalAIJSONResponseError",
    ):
        if token not in helper:
            raise SystemExit("VALIDATION ERROR: JSON adapter missing " + token)
    for module_name in (
        "planner_local_ai_plan_review.py",
        "planner_local_ai_docstring_review.py",
    ):
        if "parse_local_ai_json_object" not in texts[module_name]:
            raise SystemExit("VALIDATION ERROR: shared adapter not used by " + module_name)
    all_text = "\n".join(texts.values())
    for forbidden in (
        "workbench_guarded_apply",
        "workbench_rollback_executor",
        "workbench_real_preview",
    ):
        if forbidden in all_text:
            raise SystemExit("VALIDATION ERROR: Workbench contamination: " + forbidden)


def _parser_transport_tests() -> None:
    payload = {"verdict": "valid", "nested": {"text": "brace } inside string"}}
    raw = json.dumps(payload)
    samples = (
        raw,
        "```json\n" + raw + "\n```",
        "<think>reviewed constraints</think>\n" + raw,
        "Architecture review complete.\n" + raw + "\nDone.",
        "KANDA_BEGIN\n" + raw + "\nKANDA_END",
        json.dumps(raw),
    )
    for index, sample in enumerate(samples, start=1):
        parsed = parse_local_ai_json_object(sample, context="fixture")
        if parsed != payload:
            raise SystemExit("VALIDATION ERROR: transport sample failed: " + str(index))


def _strict_failure_tests() -> None:
    invalid = ("", "   ", "```json\n{broken\n```", "no json here")
    for sample in invalid:
        try:
            parse_local_ai_json_object(sample, context="fixture")
        except LocalAIJSONResponseError:
            continue
        raise SystemExit("VALIDATION ERROR: invalid response did not fail closed")


def _runtime_architecture_correction_test() -> None:
    report, plan = _fixture_plan()
    answers = {
        question_id: "Reviewed from deterministic evidence and resolved safely."
        for question_id, _question in ARCHITECTURE_REVIEW_QUESTIONS
    }
    response = {
        "verdict": "needs_correction",
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
        "architecture_answers": answers,
        "rationale": "Merge the tiny helper into its cohesive owner and use a semantic name.",
        "warnings": [],
    }
    fenced = "```json\n" + json.dumps(response) + "\n```"
    valid_after = {
        "verdict": "valid",
        "module_merges": [],
        "reassignments": [],
        "module_renames": [],
        "architecture_answers": answers,
        "rationale": "All surviving helpers satisfy deterministic architecture gates.",
        "warnings": [],
    }
    responses = iter((fenced, "<think>checked</think>\n" + json.dumps(valid_after)))

    original_candidates = plan_review.get_local_ai_model_candidates
    original_chat = plan_review._chat_first_available
    plan_review.get_local_ai_model_candidates = lambda _selection: ["fixture-model"]
    plan_review._chat_first_available = lambda _candidates, _messages: (
        next(responses),
        "fixture-model",
    )
    try:
        result = plan_review.review_and_correct_plan_with_local_ai(
            report,
            plan,
            enabled=True,
            max_rounds=2,
        )
    finally:
        plan_review.get_local_ai_model_candidates = original_candidates
        plan_review._chat_first_available = original_chat

    if result.status != "corrected":
        raise SystemExit("VALIDATION ERROR: local AI correction status=" + result.status)
    if result.plan.status != "planned" or result.plan.validation_blockers:
        raise SystemExit("VALIDATION ERROR: corrected plan did not revalidate")
    helpers = [
        module
        for module in result.plan.proposed_modules
        if module.role != "public_facade"
    ]
    if any(module.estimated_lines < 100 for module in helpers):
        raise SystemExit("VALIDATION ERROR: corrected plan retains tiny helper")
    if not any(module.filename == "_fixture_resolution.py" for module in helpers):
        raise SystemExit("VALIDATION ERROR: semantic helper rename missing")
    if result.corrections_applied != 2:
        raise SystemExit("VALIDATION ERROR: expected two architecture actions")


def _fixture_plan() -> tuple[ModuleAnalysisReport, RefactorPlan]:
    temp_root = Path(tempfile.gettempdir()) / "kanda_local_ai_json_adapter_fixture"
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


def _symbol(name: str, lines: int, references: list[str], cluster_id: str) -> RefactorSymbol:
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
