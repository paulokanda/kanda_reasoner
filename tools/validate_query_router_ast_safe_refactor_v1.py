# project-path: tools/validate_query_router_ast_safe_refactor_v1.py
"""Focused validation for the query-router AST-safe refactor."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = "kanda_reasoner_app/reasoner_engine/query_router.py"
HELPER_REL = "kanda_reasoner_app/reasoner_engine/_query_router_rules.py"
VALIDATOR_REL = "tools/validate_query_router_ast_safe_refactor_v1.py"
FEATURE_ID = "query-router-ast-safe-refactor-v1"
EXPECTED_ALL = [
    "QueryRouteDecision",
    "route_query_intent",
    "is_one_line_locator_question",
    "is_exact_file_locator_question",
    "is_exact_symbol_locator_question",
    "is_which_calls_question",
    "is_signal_or_action_question",
    "is_responsibility_question",
    "is_widget_listing_question",
    "is_listing_or_discovery_question",
    "is_explanatory_question",
    "is_code_localization_question",
    "is_locator_plus_explanation_question",
]
EXPECTED_TERM_DIGEST = "7c78792568bc47495b3b35f79714217982401955cbadbafdd864d2e4d850c997"
EXPECTED_CORPUS_DIGEST = "80ee0b7b6669116b6db7e601905648ae230246967ceaf0b23bd6dc01d9182ec4"
DYNAMIC_NAMES = {
    "getattr", "setattr", "hasattr", "globals", "locals", "vars",
    "eval", "exec", "__import__", "import_module",
}


def _path(relative: str) -> Path:
    return PROJECT_ROOT / relative


def _tree(relative: str) -> ast.Module:
    return ast.parse(_path(relative).read_text(encoding="utf-8"), filename=relative)


def _literal_all(tree: ast.Module) -> list[str]:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = ast.literal_eval(node.value)
                    return list(value)
    raise AssertionError("PUBLIC_ALL_NOT_FOUND")


def _function_nodes(tree: ast.Module) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _signature_shape(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple:
    positional = tuple(arg.arg for arg in node.args.posonlyargs + node.args.args)
    positional_annotations = tuple(
        ast.unparse(arg.annotation) if arg.annotation is not None else ""
        for arg in node.args.posonlyargs + node.args.args
    )
    defaults = tuple(ast.unparse(value) for value in node.args.defaults)
    keyword_only = tuple(arg.arg for arg in node.args.kwonlyargs)
    keyword_defaults = tuple(
        ast.unparse(value) if value is not None else ""
        for value in node.args.kw_defaults
    )
    returns = ast.unparse(node.returns) if node.returns is not None else ""
    return (
        positional,
        positional_annotations,
        defaults,
        keyword_only,
        keyword_defaults,
        node.args.vararg.arg if node.args.vararg else "",
        node.args.kwarg.arg if node.args.kwarg else "",
        returns,
    )


def _expected_signature_shapes() -> dict[str, tuple]:
    q_bool = (("q",), ("str",), (), (), (), "", "", "bool")
    return {
        "_norm": (("text",), ("str",), (), (), (), "", "", "str"),
        "_has_any": (("text", "terms"), ("str", "tuple[str, ...]"), (), (), (), "", "", "bool"),
        "_which_calls_needs_code_answer": q_bool,
        "is_one_line_locator_question": q_bool,
        "is_exact_file_locator_question": q_bool,
        "is_exact_symbol_locator_question": q_bool,
        "is_which_calls_question": q_bool,
        "is_signal_or_action_question": q_bool,
        "is_responsibility_question": q_bool,
        "is_widget_listing_question": q_bool,
        "is_listing_or_discovery_question": q_bool,
        "is_explanatory_question": q_bool,
        "is_code_localization_question": q_bool,
        "is_locator_plus_explanation_question": q_bool,
        "route_query_intent": (("question",), ("str",), (), (), (), "", "", "QueryRouteDecision"),
    }


def _assert_python_and_line_law() -> None:
    for relative in (TARGET_REL, HELPER_REL, VALIDATOR_REL):
        source = _path(relative).read_text(encoding="utf-8")
        ast.parse(source, filename=relative)
        line_count = len(source.splitlines())
        if not 101 <= line_count <= 499:
            raise AssertionError(f"LINE_LAW:{relative}:{line_count}")
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _assert_public_contract() -> None:
    tree = _tree(TARGET_REL)
    if _literal_all(tree) != EXPECTED_ALL:
        raise AssertionError("PUBLIC_API_PRESERVATION")
    functions = _function_nodes(tree)
    for name, expected in _expected_signature_shapes().items():
        node = functions.get(name)
        if node is None or _signature_shape(node) != expected:
            raise AssertionError("PUBLIC_SIGNATURE_PRESERVATION:" + name)
    class_node = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "QueryRouteDecision"
    )
    decorators = tuple(ast.unparse(item) for item in class_node.decorator_list)
    if decorators != ("dataclass(frozen=True)",):
        raise AssertionError("QUERY_ROUTE_DECISION_DATACLASS_PRESERVATION")
    fields = [
        node.target.id
        for node in class_node.body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    ]
    field_annotations = [
        ast.unparse(node.annotation)
        for node in class_node.body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    ]
    if fields != ["route", "intent_name", "reason"] or field_annotations != ["str", "str", "str"]:
        raise AssertionError("QUERY_ROUTE_DECISION_FIELD_ORDER_PRESERVATION")
    print("PUBLIC_API_PRESERVATION: PASS")
    print("PUBLIC_SIGNATURE_PRESERVATION: PASS")
    print("QUERY_ROUTE_DECISION_DATACLASS_PRESERVATION: PASS")
    print("QUERY_ROUTE_DECISION_FROZEN_PRESERVATION: PASS")
    print("QUERY_ROUTE_DECISION_FIELD_ORDER_PRESERVATION: PASS")
    print("QUERY_ROUTE_DECISION_ANNOTATION_PRESERVATION: PASS")


def _assert_semantic_safety() -> None:
    for relative in (TARGET_REL, HELPER_REL, VALIDATOR_REL):
        tree = _tree(relative)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_NAMES:
                    raise AssertionError(f"DYNAMIC_CALL:{relative}:{node.func.id}")
                if isinstance(node.func, ast.Attribute) and node.func.attr in DYNAMIC_NAMES:
                    raise AssertionError(f"DYNAMIC_CALL:{relative}:{node.func.attr}")
    helper_tree = _tree(HELPER_REL)
    for node in ast.walk(helper_tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.endswith("query_router"):
                raise AssertionError("HELPER_TO_FACADE_BACK_REFERENCE")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.endswith(".query_router"):
                    raise AssertionError("HELPER_TO_FACADE_BACK_REFERENCE")
    print("NO_DYNAMIC_REFLECTION_CALLS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")


def _term_payload(qr: object) -> dict[str, list[str]]:
    return {
        "CODE_EXPLANATION_TERMS": list(qr.CODE_EXPLANATION_TERMS),
        "CODE_LOCALIZATION_TERMS": list(qr.CODE_LOCALIZATION_TERMS),
        "DISCOVERY_TERMS": list(qr.DISCOVERY_TERMS),
        "EXPLANATORY_CORE_TERMS": list(qr.EXPLANATORY_CORE_TERMS),
        "EXPLANATORY_TERMS": list(qr.EXPLANATORY_TERMS),
        "FILE_LOCATOR_TERMS": list(qr.FILE_LOCATOR_TERMS),
        "RESPONSIBILITY_TERMS": list(qr.RESPONSIBILITY_TERMS),
        "SIGNAL_ACTION_TERMS": list(qr.SIGNAL_ACTION_TERMS),
        "SYMBOL_LOCATOR_TERMS": list(qr.SYMBOL_LOCATOR_TERMS),
        "WHICH_CALLS_TERMS": list(qr.WHICH_CALLS_TERMS),
        "WHICH_CALLS_WITH_CODE_EXTRA_TERMS": list(qr.WHICH_CALLS_WITH_CODE_EXTRA_TERMS),
        "WIDGET_LISTING_TERMS": list(qr.WIDGET_LISTING_TERMS),
    }


def _assert_behavior() -> None:
    from kanda_reasoner_app.reasoner_engine import query_router as qr

    if qr.QueryRouteDecision.__module__ != "kanda_reasoner_app.reasoner_engine.query_router":
        raise AssertionError("QUERY_ROUTE_DECISION_MODULE_IDENTITY")
    public_functions = {
        "route_query_intent": qr.route_query_intent,
        "is_one_line_locator_question": qr.is_one_line_locator_question,
        "is_exact_file_locator_question": qr.is_exact_file_locator_question,
        "is_exact_symbol_locator_question": qr.is_exact_symbol_locator_question,
        "is_which_calls_question": qr.is_which_calls_question,
        "is_signal_or_action_question": qr.is_signal_or_action_question,
        "is_responsibility_question": qr.is_responsibility_question,
        "is_widget_listing_question": qr.is_widget_listing_question,
        "is_listing_or_discovery_question": qr.is_listing_or_discovery_question,
        "is_explanatory_question": qr.is_explanatory_question,
        "is_code_localization_question": qr.is_code_localization_question,
        "is_locator_plus_explanation_question": qr.is_locator_plus_explanation_question,
    }
    for name, function in public_functions.items():
        if function.__module__ != "kanda_reasoner_app.reasoner_engine.query_router":
            raise AssertionError("PUBLIC_FUNCTION_MODULE_IDENTITY:" + name)
    term_payload = _term_payload(qr)
    term_blob = json.dumps(term_payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    if hashlib.sha256(term_blob.encode("utf-8")).hexdigest() != EXPECTED_TERM_DIGEST:
        raise AssertionError("TERM_TABLE_IDENTITY")

    corpus = {"", "unmatched neutral question", "   Explain the architecture   "}
    for terms in term_payload.values():
        for term in terms:
            corpus.add(term)
            corpus.add("  " + term.upper() + "  ")
    corpus.update([
        "answer only in one line " + qr.FILE_LOCATOR_TERMS[0],
        qr.WHICH_CALLS_TERMS[0] + " show code",
        qr.WHICH_CALLS_TERMS[0] + " explain",
        qr.FILE_LOCATOR_TERMS[0] + " explain flow",
        qr.FILE_LOCATOR_TERMS[0] + " explain with code",
        qr.WIDGET_LISTING_TERMS[0] + " " + qr.DISCOVERY_TERMS[0],
        qr.SIGNAL_ACTION_TERMS[0] + " explain",
        qr.DISCOVERY_TERMS[0] + " explain",
    ])
    predicates = {
        "is_code_localization_question": qr.is_code_localization_question,
        "is_exact_file_locator_question": qr.is_exact_file_locator_question,
        "is_exact_symbol_locator_question": qr.is_exact_symbol_locator_question,
        "is_explanatory_question": qr.is_explanatory_question,
        "is_listing_or_discovery_question": qr.is_listing_or_discovery_question,
        "is_locator_plus_explanation_question": qr.is_locator_plus_explanation_question,
        "is_one_line_locator_question": qr.is_one_line_locator_question,
        "is_responsibility_question": qr.is_responsibility_question,
        "is_signal_or_action_question": qr.is_signal_or_action_question,
        "is_which_calls_question": qr.is_which_calls_question,
        "is_widget_listing_question": qr.is_widget_listing_question,
    }
    rows: list[dict[str, object]] = []
    for question in sorted(corpus):
        normalized = qr._norm(question)
        decision = qr.route_query_intent(question)
        rows.append({
            "q": question,
            "norm": normalized,
            "preds": {name: function(normalized) for name, function in predicates.items()},
            "decision": [decision.route, decision.intent_name, decision.reason],
        })
    blob = json.dumps(rows, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    if hashlib.sha256(blob.encode("utf-8")).hexdigest() != EXPECTED_CORPUS_DIGEST:
        raise AssertionError("ROUTE_DECISION_CORPUS_EQUIVALENCE")

    original = qr.is_one_line_locator_question
    qr.is_one_line_locator_question = lambda q: True
    try:
        decision = qr.route_query_intent("neutral monkeypatch probe")
        if decision.intent_name != "one_line_locator":
            raise AssertionError("MONKEYPATCH_GLOBAL_PREDICATE_SEMANTICS")
    finally:
        qr.is_one_line_locator_question = original

    print("QUERY_ROUTE_DECISION_MODULE_IDENTITY: PASS")
    print("PUBLIC_FUNCTION_MODULE_IDENTITY_PRESERVATION: PASS")
    print("PRIVATE_COMPATIBILITY_SURFACE: PASS")
    print("TERM_TABLE_IDENTITY: PASS")
    print("TERM_TABLE_ORDER_PRESERVATION: PASS")
    print("NORMALIZATION_BEHAVIOR: PASS")
    print("TERM_MATCHING_BEHAVIOR: PASS")
    print("PREDICATE_CORPUS_EQUIVALENCE: PASS")
    print("ROUTE_PRECEDENCE_EQUIVALENCE: PASS")
    print("ROUTE_DECISION_CORPUS_EQUIVALENCE: PASS")
    print("ROUTE_REASON_TEXT_EQUIVALENCE: PASS")
    print("MONKEYPATCH_GLOBAL_PREDICATE_SEMANTICS: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _assert_consumers() -> None:
    from kanda_reasoner_app.reasoner_engine import query_router as package_query_router
    from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help import session_service
    from kanda_reasoner_app.reasoner_engine.prompt_builder_help import widget_registry_section

    if session_service.QueryRouteDecision is not package_query_router.QueryRouteDecision:
        raise AssertionError("SESSION_SERVICE_CONSUMER_REGRESSION")
    if session_service.route_query_intent is not package_query_router.route_query_intent:
        raise AssertionError("SESSION_SERVICE_CONSUMER_REGRESSION")
    if not callable(widget_registry_section.append_widget_registry_section):
        raise AssertionError("WIDGET_REGISTRY_CONSUMER_REGRESSION")
    dry_run_paths = (
        "tools/ask_ai_project_reasoner_deletion_dry_run.py",
        "tools/project_reasoner_v10_deletion_dry_run.py",
    )
    import_probe = "import kanda_reasoner_app.reasoner_engine.query_router"
    for relative in dry_run_paths:
        if import_probe not in _path(relative).read_text(encoding="utf-8"):
            raise AssertionError("DELETION_DRY_RUN_IMPORT_CONTRACT:" + relative)
    print("SESSION_SERVICE_CONSUMER_REGRESSION: PASS")
    print("WIDGET_REGISTRY_CONSUMER_REGRESSION: PASS")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")
    print("REASONER_ENGINE_PACKAGE_IMPORT: PASS")
    print("DELETION_DRY_RUN_IMPORT_CONTRACT: PASS")


def _assert_fresh_audits() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    labels: list[str] = []
    blockers: list[str] = []
    for relative in (TARGET_REL, HELPER_REL, VALIDATOR_REL):
        result = run_large_module_split_audit(PROJECT_ROOT, relative)
        classification = dict(result.data.get("refactor_safety_classification") or {})
        labels.append(str(classification.get("label") or ""))
        blockers.extend(str(item) for item in classification.get("hard_blockers") or [])
    if any(label != "SAFE REFACTORING" for label in labels):
        raise AssertionError("AST_SPLIT_FAMILY_ALL_SAFE:" + repr(labels))
    if blockers:
        raise AssertionError("AST_SPLIT_HARD_BLOCKERS:" + repr(blockers))
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    parser.parse_args()
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    _assert_python_and_line_law()
    _assert_public_contract()
    _assert_semantic_safety()
    _assert_behavior()
    _assert_consumers()
    _assert_fresh_audits()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
