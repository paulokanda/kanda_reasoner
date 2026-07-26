"""Semantic contract and fixtures for Brick Wall Q22 facade drift tests."""

from __future__ import annotations

import ast
import importlib
import inspect
import sys
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Mapping

__all__: list[str] = []

RECORD_FIELDS = {
    "tests_required",
    "no_test_evidence",
    "primary_box",
    "contract_owner",
    "contract_facade",
    "cases",
    "unresolved_cases",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_q23",
    "may_begin_coding",
    "may_write_source",
}

CASE_FIELDS = {
    "case_id",
    "facade_path",
    "canonical_import_path",
    "package_root_path",
    "package_root_export_status",
    "public_symbols",
    "public_all_owner",
    "signature_policy",
    "fallback_policy",
    "fallback_evidence",
    "required_consumer_subset",
    "current_consumers",
    "private_helper_paths",
    "current_consumer_imports",
    "private_dependency_policy",
    "duplicate_public_owners",
    "canonical_validators",
    "expected_markers",
}

PACKAGE_ROOT_EXPORT_STATES = {"EXPLICIT", "NOT_EXPORTED"}
SIGNATURE_POLICIES = {"EXACT", "DECLARED_COMPATIBLE"}
FALLBACK_POLICIES = {"PRESERVE", "NOT_APPLICABLE"}
PRIVATE_POLICIES = {"FACADE_ONLY"}


def _fields(mapping: Mapping[str, object], required: set[str]) -> None:
    missing = required.difference(mapping)
    extra = set(mapping).difference(required)
    if missing or extra:
        raise AssertionError(
            "Q22 field mismatch; missing="
            + repr(sorted(missing))
            + " extra="
            + repr(sorted(extra))
        )


def _nonempty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def _validate_case(case: Mapping[str, object]) -> None:
    _fields(case, CASE_FIELDS)
    if not all(
        isinstance(case[name], str) and str(case[name]).strip()
        for name in (
            "case_id",
            "facade_path",
            "canonical_import_path",
            "package_root_path",
            "public_all_owner",
        )
    ):
        raise AssertionError("Q22 case identity fields are required")
    if case["package_root_export_status"] not in PACKAGE_ROOT_EXPORT_STATES:
        raise AssertionError("Q22 package-root export status is invalid")
    if case["signature_policy"] not in SIGNATURE_POLICIES:
        raise AssertionError("Q22 signature policy is invalid")
    if case["fallback_policy"] not in FALLBACK_POLICIES:
        raise AssertionError("Q22 fallback policy is invalid")
    if case["private_dependency_policy"] not in PRIVATE_POLICIES:
        raise AssertionError("Q22 private dependency policy is invalid")
    if not _nonempty_strings(case["public_symbols"]):
        raise AssertionError("Q22 public symbols are required")
    if len(case["public_symbols"]) != len(set(case["public_symbols"])):
        raise AssertionError("Q22 duplicate public symbol")
    if case["package_root_export_status"] == "NOT_EXPORTED":
        if str(case["canonical_import_path"]).startswith(
            str(case["package_root_path"]) + "."
        ) is False:
            raise AssertionError("Q22 canonical import is outside package root")
        symbol_owner = str(case["canonical_import_path"]).rsplit(".", 1)[0]
        if symbol_owner == str(case["package_root_path"]):
            raise AssertionError("Q22 assumes a non-exporting package root")
    if case["public_all_owner"] != case["facade_path"]:
        raise AssertionError("Q22 public __all__ owner must be the facade")
    if case["fallback_policy"] == "PRESERVE" and not case["fallback_evidence"]:
        raise AssertionError("Q22 preserved fallback requires evidence")
    required = set(case["required_consumer_subset"])
    current = set(case["current_consumers"])
    if not required.issubset(current):
        raise AssertionError("Q22 required consumer subset is missing")
    private_paths = tuple(str(path) for path in case["private_helper_paths"])
    for import_path in case["current_consumer_imports"]:
        if any(
            import_path == private
            or str(import_path).startswith(private + ".")
            for private in private_paths
        ):
            raise AssertionError("Q22 current consumer reaches private helper")
    if case["duplicate_public_owners"]:
        raise AssertionError("Q22 duplicate public ownership is forbidden")
    if not case["canonical_validators"] or not case["expected_markers"]:
        raise AssertionError("Q22 validators and markers are required")


def validate_record(record: Mapping[str, object]) -> None:
    """Validate one complete Q22 record or evidence-backed N/A record."""
    _fields(record, RECORD_FIELDS)
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q22 cannot grant coding or source-write authority")
    required = bool(record["tests_required"])
    if required:
        if record["decision"] != "COMPLETE" or not record["may_proceed_to_q23"]:
            raise AssertionError("Q22 required tests must complete and proceed")
        if record["no_test_evidence"]:
            raise AssertionError("Q22 required record cannot carry N/A evidence")
        if not record["contract_owner"] or not record["contract_facade"]:
            raise AssertionError("Q22 contract owner and facade are required")
        if record["unresolved_cases"] or record["blockers"]:
            raise AssertionError("Q22 required record remains blocked")
        cases = record["cases"]
        if not isinstance(cases, list) or not cases:
            raise AssertionError("Q22 cases are required")
        ids: set[str] = set()
        facade_paths: set[str] = set()
        for case in cases:
            _validate_case(case)
            case_id = str(case["case_id"])
            facade_path = str(case["facade_path"])
            if case_id in ids:
                raise AssertionError("Q22 duplicate case id")
            if facade_path in facade_paths:
                raise AssertionError("Q22 duplicate facade case")
            ids.add(case_id)
            facade_paths.add(facade_path)
        if not record["tests"]:
            raise AssertionError("Q22 tests are required")
        return
    if record["decision"] != "NOT_APPLICABLE" or not record["may_proceed_to_q23"]:
        raise AssertionError("Q22 N/A record must be explicit and proceed")
    if record["cases"] or not record["no_test_evidence"]:
        raise AssertionError("Q22 N/A record must have evidence and no cases")


def _case(
    case_id: str,
    facade_path: str,
    canonical_import: str,
    package_root: str,
    public_symbols: list[str],
    *,
    fallback: str = "NOT_APPLICABLE",
    fallback_evidence: list[str] | None = None,
    required_consumers: list[str] | None = None,
    current_consumers: list[str] | None = None,
    private_helpers: list[str] | None = None,
    current_imports: list[str] | None = None,
) -> dict[str, object]:
    return {
        "case_id": case_id,
        "facade_path": facade_path,
        "canonical_import_path": canonical_import,
        "package_root_path": package_root,
        "package_root_export_status": "NOT_EXPORTED",
        "public_symbols": public_symbols,
        "public_all_owner": facade_path,
        "signature_policy": "EXACT",
        "fallback_policy": fallback,
        "fallback_evidence": fallback_evidence or [],
        "required_consumer_subset": required_consumers or [],
        "current_consumers": current_consumers or [],
        "private_helper_paths": private_helpers or [],
        "current_consumer_imports": current_imports or [],
        "private_dependency_policy": "FACADE_ONLY",
        "duplicate_public_owners": [],
        "canonical_validators": ["Q09", "Q22"],
        "expected_markers": ["PASS", "VALIDATION OK"],
    }


def valid_required_record() -> dict[str, object]:
    """Return a complete representative Q22 record."""
    cases = [
        _case(
            "workflow_gui_public_entrypoint",
            "kanda_reasoner_app/manage_workflows/manage_workflows_gui.py",
            "kanda_reasoner_app.manage_workflows.manage_workflows_gui.WorkflowManagerWindow",
            "kanda_reasoner_app.manage_workflows",
            ["WorkflowManagerWindow"],
            fallback="PRESERVE",
            fallback_evidence=["legacy import aliases remain facade-owned"],
            private_helpers=[
                "kanda_reasoner_app.manage_workflows.manage_workflows_gui_help"
            ],
            current_imports=[
                "kanda_reasoner_app.manage_workflows.manage_workflows_gui"
            ],
        ),
        _case(
            "facade_consumer_compatibility",
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/facade_consumer_compatibility.py",
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.facade_consumer_compatibility.build_facade_consumer_compatibility_report",
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner",
            ["build_facade_consumer_compatibility_report"],
            required_consumers=["routing_signal_scorer.contract"],
            current_consumers=[
                "routing_signal_scorer.contract",
                "focused_q22_validator",
            ],
            private_helpers=[
                "kanda_reasoner_app.manage_architecture.large_file_refactor_planner._private_facade_consumer"
            ],
            current_imports=[
                "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.facade_consumer_compatibility"
            ],
        ),
        _case(
            "synthetic_signature_and_fallback",
            "validation_fixture/pkg/facade.py",
            "pkg.facade.resolve",
            "pkg",
            ["resolve"],
            fallback="PRESERVE",
            fallback_evidence=["resolve(None) returns private default through facade"],
            required_consumers=["consumer_good.py"],
            current_consumers=["consumer_good.py"],
            private_helpers=["pkg._impl"],
            current_imports=["pkg.facade"],
        ),
    ]
    return {
        "tests_required": True,
        "no_test_evidence": [],
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "contract_owner": "Brick Wall Q22 validation-only contract",
        "contract_facade": "tools/brick_wall_q22_public_facade_contract.py",
        "cases": cases,
        "unresolved_cases": [],
        "blockers": [],
        "tests": ["focused semantic matrix", "isolated import and drift fixture"],
        "decision": "COMPLETE",
        "may_proceed_to_q23": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    """Return explicit N/A evidence for work with no public contract surface."""
    record = valid_required_record()
    record.update(
        tests_required=False,
        no_test_evidence=["No importable public facade or consumer contract is affected."],
        cases=[],
        tests=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    """Return a deep copy for focused negative tests."""
    return deepcopy(valid_required_record())


def snapshot_public_contract(source: str, function_name: str) -> dict[str, object]:
    """Return stable AST contract fields for one public function."""
    tree = ast.parse(source)
    exports: list[str] = []
    target: ast.FunctionDef | ast.AsyncFunctionDef | None = None
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(item, ast.Name) and item.id == "__all__" for item in targets):
                value = node.value
                if isinstance(value, (ast.List, ast.Tuple)):
                    exports = [
                        item.value
                        for item in value.elts
                        if isinstance(item, ast.Constant)
                        and isinstance(item.value, str)
                    ]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            target = node
    if target is None:
        raise AssertionError("Q22 public function missing")
    positional = [arg.arg for arg in (*target.args.posonlyargs, *target.args.args)]
    defaults = [ast.dump(item, include_attributes=False) for item in target.args.defaults]
    arg_annotations = {
        arg.arg: ast.unparse(arg.annotation) if arg.annotation is not None else None
        for arg in (*target.args.posonlyargs, *target.args.args, *target.args.kwonlyargs)
    }
    return {
        "name": target.name,
        "positional": positional,
        "defaults": defaults,
        "kwonly": [arg.arg for arg in target.args.kwonlyargs],
        "annotations": arg_annotations,
        "returns": ast.unparse(target.returns) if target.returns is not None else None,
        "docstring": ast.get_docstring(target, clean=False),
        "exports": exports,
    }


def detect_private_imports(source: str, private_modules: set[str]) -> set[str]:
    """Return private modules imported by one consumer source."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [str(node.module or "")]
        else:
            continue
        for module in modules:
            if any(module == private or module.startswith(private + ".") for private in private_modules):
                found.add(module)
    return found


def run_isolated_facade_fixture() -> None:
    """Exercise import, signature, fallback, consumer, and ownership guards."""
    baseline = '''\nfrom ._impl import _resolve as _public_resolve\n__all__ = ["resolve"]\ndef resolve(value: str | None = None) -> str:\n    """Resolve a value through the stable public facade."""\n    return _public_resolve(value)\n'''.lstrip()
    signature_drift = baseline.replace("= None", "= 'changed'", 1)
    docstring_drift = baseline.replace("stable public facade", "changed facade")
    assert snapshot_public_contract(baseline, "resolve") != snapshot_public_contract(signature_drift, "resolve")
    assert snapshot_public_contract(baseline, "resolve") != snapshot_public_contract(docstring_drift, "resolve")
    with TemporaryDirectory(prefix="kanda_q22_facade_") as temp:
        root = Path(temp)
        package = root / "pkg"
        package.mkdir()
        (package / "__init__.py").write_text("__all__ = []\n", encoding="utf-8")
        (package / "_impl.py").write_text(
            '__all__ = []\ndef _resolve(value=None):\n    return "default" if value is None else value\n',
            encoding="utf-8",
        )
        (package / "facade.py").write_text(baseline, encoding="utf-8")
        good = "from pkg.facade import resolve\n"
        bad = "from pkg._impl import _resolve\n"
        (root / "consumer_good.py").write_text(good, encoding="utf-8")
        (root / "consumer_bad.py").write_text(bad, encoding="utf-8")
        sys.path.insert(0, str(root))
        try:
            pkg = importlib.import_module("pkg")
            facade = importlib.import_module("pkg.facade")
            if hasattr(pkg, "resolve"):
                raise AssertionError("Q22 non-exporting package root exposed resolve")
            signature_text = str(inspect.signature(facade.resolve))
            if signature_text not in {
                "(value: str | None = None) -> str",
                "(value: 'str | None' = None) -> 'str'",
            }:
                raise AssertionError("Q22 runtime signature drift")
            if facade.resolve(None) != "default" or facade.resolve("x") != "x":
                raise AssertionError("Q22 fallback drift")
            if detect_private_imports(good, {"pkg._impl"}):
                raise AssertionError("Q22 good consumer flagged private")
            if detect_private_imports(bad, {"pkg._impl"}) != {"pkg._impl"}:
                raise AssertionError("Q22 private consumer not detected")
            duplicate_private = '__all__ = ["resolve"]\ndef resolve(value=None): return value\n'
            duplicate_exports = {"resolve"} if '__all__ = ["resolve"]' in duplicate_private else set()
            facade_exports = set(snapshot_public_contract(baseline, "resolve")["exports"])
            if facade_exports.isdisjoint(duplicate_exports):
                raise AssertionError("Q22 duplicate public owner was not detected")
        finally:
            sys.path.remove(str(root))
            for name in ["pkg.facade", "pkg._impl", "pkg"]:
                sys.modules.pop(name, None)
