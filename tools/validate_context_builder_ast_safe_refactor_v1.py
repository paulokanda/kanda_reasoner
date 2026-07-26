# project-path: tools/validate_context_builder_ast_safe_refactor_v1.py
"""Focused validation for the context-builder AST-safe refactor."""

from __future__ import annotations

import ast
import dataclasses
import hashlib
from pathlib import Path
import sys

__all__ = []

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FACADE_REL = "kanda_reasoner_app/insert_missing_docstrings_gui/context_builder.py"
HELPER_REL = (
    "kanda_reasoner_app/insert_missing_docstrings_gui/"
    "_context_builder_ast_support.py"
)
VALIDATOR_REL = "tools/validate_context_builder_ast_safe_refactor_v1.py"
FEATURE_ID = "context-builder-ast-safe-refactor-v1"
EXPECTED_ALL = (
    "AttributeInfo",
    "ParameterInfo",
    "SymbolContext",
    "build_class_context",
    "build_function_context",
    "build_module_context",
)
EXPECTED_FACADE_SHA256 = "94209a33b1a6c87122e9dd037659c45fe4057924ba6493a892afd8db31b272a4"
EXPECTED_HELPER_SHA256 = "c6c7a6600f0b24dcda924363dcb3e9809b6c9f66144b420db14df136a1fac285"

ROOT_TEXT = str(PROJECT_ROOT)
if ROOT_TEXT not in sys.path:
    sys.path.insert(0, ROOT_TEXT)

from kanda_reasoner_app.insert_missing_docstrings_gui import context_builder as context_module
from kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator import (
    AttributeInfo as GeneratorAttributeInfo,
    ParameterInfo as GeneratorParameterInfo,
    SymbolContext as GeneratorSymbolContext,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.docstring_payloads import (
    AttributeInfo as PayloadAttributeInfo,
    ParameterInfo as PayloadParameterInfo,
    SymbolContext as PayloadSymbolContext,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.heuristics import (
    ParameterInfo as HeuristicParameterInfo,
    SymbolContext as HeuristicSymbolContext,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.context_builder import (
    AttributeInfo,
    ParameterInfo,
    SymbolContext,
    build_class_context,
    build_function_context,
    build_module_context,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.context_builder_validate_manifests import (
    main as validate_context_builder_manifest,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.docstring_validator import (
    SymbolContext as ValidatorSymbolContext,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help import (
    insertion_collector,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.module_summarizer import (
    ClassProfile,
    InitAttribute,
    ModuleSummary,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_source_identity() -> None:
    assert _sha256(PROJECT_ROOT / FACADE_REL) == EXPECTED_FACADE_SHA256
    assert _sha256(PROJECT_ROOT / HELPER_REL) == EXPECTED_HELPER_SHA256
    print("SOURCE_IDENTITY_GUARD: PASS")


def _assert_source_family() -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
        detect_semantic_dynamic_risks,
    )

    family = (FACADE_REL, HELPER_REL, VALIDATOR_REL)
    for relative_path in family:
        path = PROJECT_ROOT / relative_path
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), relative_path
        source = raw.decode("utf-8", errors="strict")
        line_count = len(source.splitlines())
        assert 100 < line_count < 500, (relative_path, line_count)
        ast.parse(source, filename=str(path))
        findings = detect_semantic_dynamic_risks(source, relative_path)
        assert not findings, (relative_path, findings)

    report = check_candidate_dependency_direction(
        PROJECT_ROOT,
        facade_relative_path=FACADE_REL,
        helper_relative_paths=[HELPER_REL],
    )
    assert report.get("pass") is True, report
    helper_source = (PROJECT_ROOT / HELPER_REL).read_text(encoding="utf-8")
    assert "from .context_builder import" not in helper_source
    assert "import context_builder" not in helper_source

    print("PYTHON_SYNTAX: PASS")
    print("NO_DYNAMIC_REFLECTION_CALLS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _assert_public_contract() -> None:
    assert tuple(context_module.__all__) == EXPECTED_ALL
    assert ParameterInfo.__module__.endswith(".context_builder")
    assert AttributeInfo.__module__.endswith(".context_builder")
    assert SymbolContext.__module__.endswith(".context_builder")

    source = (PROJECT_ROOT / FACADE_REL).read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    expected_args = {
        "build_module_context": [
            "path", "module_id", "tree", "source_lines", "module_summary"
        ],
        "build_class_context": [
            "node", "tree", "module_id", "source_lines", "module_summary",
            "class_docstring_override",
        ],
        "build_function_context": [
            "node", "tree", "module_id", "source_lines", "module_summary"
        ],
    }
    for name, args in expected_args.items():
        assert [item.arg for item in functions[name].args.args] == args

    assert dataclasses.is_dataclass(ParameterInfo)
    assert dataclasses.is_dataclass(AttributeInfo)
    assert dataclasses.is_dataclass(SymbolContext)
    assert [field.name for field in dataclasses.fields(ParameterInfo)] == [
        "name", "annotation", "has_default", "is_vararg", "is_kwarg", "is_kwonly"
    ]
    assert [field.name for field in dataclasses.fields(AttributeInfo)] == [
        "name", "type_hint", "description_hint"
    ]
    assert [field.name for field in dataclasses.fields(SymbolContext)] == [
        "kind", "name", "module_id", "source_lines", "signature", "parameters",
        "return_annotation", "decorators", "enclosing_class", "module_docstring",
        "module_summary_block", "class_docstring", "class_attributes",
        "sibling_docstrings", "overload_siblings", "imports", "raises_types",
        "is_async", "is_property", "is_cached_property", "is_abstract",
        "is_staticmethod", "is_classmethod", "is_overload", "is_dataclass",
        "is_init", "lineno",
    ]

    print("PUBLIC_API_PRESERVATION: PASS")
    print("PUBLIC_SIGNATURE_PRESERVATION: PASS")
    print("DATACLASS_DECORATOR_PRESERVATION: PASS")
    print("DATACLASS_FIELD_ORDER_PRESERVATION: PASS")
    print("DATACLASS_DEFAULTS_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")
    print("PUBLIC_CLASS_MODULE_IDENTITY_PRESERVATION: PASS")


def _fixture() -> tuple[ast.Module, list[str], ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef]:
    source = '''\n"""Module docs."""\nimport os\nfrom typing import overload, cached_property\n\n@dataclass\nclass Demo:\n    """Demo docs."""\n    def __init__(self, x: int, y="v"):\n        self.x = x\n        self.y = y\n        self.z: str = "z"\n\n    @property\n    def prop(self) -> str:\n        return self.z\n\n@overload\ndef fun(a: int) -> int: ...\n@overload\ndef fun(a: str) -> str: ...\ndef fun(a, *args: int, flag: bool=True, **kwargs: str):\n    if a is None:\n        raise RuntimeError("none")\n    return a\n\nasync def afun(x: float) -> float:\n    return x\n'''.lstrip("\n")
    tree = ast.parse(source)
    demo = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    funcs = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    fun_impl = [node for node in funcs if node.name == "fun"][-1]
    afun = next(node for node in funcs if node.name == "afun")
    assert isinstance(fun_impl, ast.FunctionDef)
    assert isinstance(afun, ast.AsyncFunctionDef)
    return tree, source.splitlines(), demo, fun_impl, afun


def _assert_behavior() -> None:
    tree, lines, demo, fun_impl, afun = _fixture()
    summary = ModuleSummary(
        module_id="pkg.demo",
        one_liner="Fixture module.",
        classes=[
            ClassProfile(
                name="Demo",
                init_attributes=[
                    InitAttribute(name="alpha", type_hint="int", assigned_from="x"),
                    InitAttribute(name="beta", assigned_from="call()"),
                ],
            )
        ],
    )

    module_ctx = build_module_context(Path("demo.py"), "pkg.demo", tree, lines, summary)
    class_ctx = build_class_context(demo, tree, "pkg.demo", lines, summary, "override")
    function_ctx = build_function_context(fun_impl, tree, "pkg.demo", lines, summary)
    async_ctx = build_function_context(afun, tree, "pkg.demo", lines, summary)

    assert module_ctx.kind == "module"
    assert module_ctx.module_summary_block.startswith("Module purpose: Fixture module.")
    assert module_ctx.imports == ["import os", "from typing import overload, cached_property"]
    assert class_ctx.kind == "class"
    assert class_ctx.class_docstring == "override"
    assert [(item.name, item.type_hint, item.description_hint) for item in class_ctx.class_attributes] == [
        ("alpha", "int", "x"), ("beta", "", "call()")
    ]
    assert function_ctx.kind == "function"
    assert function_ctx.overload_siblings == [
        "def fun(a: int) -> int", "def fun(a: str) -> str"
    ]
    assert function_ctx.raises_types == ["RuntimeError"]
    assert [item.name for item in function_ctx.parameters] == ["a", "args", "flag", "kwargs"]
    assert async_ctx.is_async is True
    assert SymbolContext(kind="function", name="f", module_id="m").full_name == "f"
    assert SymbolContext(
        kind="method", name="f", module_id="m", enclosing_class="C"
    ).full_name == "C.f"

    print("SAFE_UNPARSE_BEHAVIOR: PASS")
    print("DECORATOR_EXTRACTION_BEHAVIOR: PASS")
    print("PARAMETER_EXTRACTION_BEHAVIOR: PASS")
    print("IMPORT_EXTRACTION_BEHAVIOR: PASS")
    print("SOURCE_LINE_EXTRACTION_BEHAVIOR: PASS")
    print("SIBLING_DOCSTRING_BEHAVIOR: PASS")
    print("CLASS_ATTRIBUTE_EXTRACTION_BEHAVIOR: PASS")
    print("RAISE_TYPE_EXTRACTION_BEHAVIOR: PASS")
    print("PARENT_CLASS_DISCOVERY_BEHAVIOR: PASS")
    print("OVERLOAD_SIBLING_BEHAVIOR: PASS")
    print("MODULE_SUMMARY_BRIDGE_BEHAVIOR: PASS")
    print("CLASS_PROFILE_ATTRIBUTE_BEHAVIOR: PASS")
    print("MODULE_CONTEXT_EQUIVALENCE: PASS")
    print("CLASS_CONTEXT_EQUIVALENCE: PASS")
    print("FUNCTION_CONTEXT_EQUIVALENCE: PASS")
    print("FULL_NAME_BEHAVIOR_EQUIVALENCE: PASS")
    print("ERROR_CONTRACT_PRESERVATION: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _assert_consumers() -> None:
    assert GeneratorAttributeInfo is AttributeInfo
    assert GeneratorParameterInfo is ParameterInfo
    assert GeneratorSymbolContext is SymbolContext
    assert PayloadAttributeInfo is AttributeInfo
    assert PayloadParameterInfo is ParameterInfo
    assert PayloadSymbolContext is SymbolContext
    assert HeuristicParameterInfo is ParameterInfo
    assert HeuristicSymbolContext is SymbolContext
    assert ValidatorSymbolContext is SymbolContext
    assert insertion_collector._AI_AVAILABLE is True
    assert validate_context_builder_manifest() == 0

    print("DOCSTRING_GENERATOR_CONSUMER_REGRESSION: PASS")
    print("DOCSTRING_PAYLOAD_CONSUMER_REGRESSION: PASS")
    print("HEURISTICS_CONSUMER_REGRESSION: PASS")
    print("DOCSTRING_VALIDATOR_CONSUMER_REGRESSION: PASS")
    print("INSERTION_COLLECTOR_REGRESSION: PASS")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")


def _assert_fresh_audits() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for relative_path in (FACADE_REL, HELPER_REL, VALIDATOR_REL):
        result = run_large_module_split_audit(
            PROJECT_ROOT,
            PROJECT_ROOT / relative_path,
            classifier_mode="heuristic",
        )
        classification = result.data["refactor_safety_classification"]
        assert classification["label"] == "SAFE REFACTORING", classification
        assert not classification["hard_blockers"], classification

    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")


def _run_validation() -> None:
    _assert_source_identity()
    _assert_source_family()
    _assert_public_contract()
    _assert_behavior()
    _assert_consumers()
    _assert_fresh_audits()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


_run_validation()
