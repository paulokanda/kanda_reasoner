"""Validate the AST-safe comparison engine refactor and package contract."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import inspect
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

FEATURE_ID = "comparison-engine-ast-safe-refactor-v1"
TARGET_RELATIVE_PATH = (
    "kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/"
    "comparison_engine.py"
)
FAMILY_RELATIVE_PATHS = (
    TARGET_RELATIVE_PATH,
    "kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/"
    "_comparison_engine_analysis.py",
    "kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/"
    "_comparison_engine_support.py",
    "kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness/"
    "_comparison_engine_result_model.py",
)
EXPECTED_ORIGINAL_SHA256 = (
    "8a4647941ba640907bb5baaf2459a1f926319b2b3ae78ace0eadf523fb867e10"
)
EXPECTED_BEHAVIOR_SHA256 = (
    "03f95c3d46c22e72207ac1bac1006a28707f4253e1ca38fc46e688a38fa4c330"
)
EXPECTED_PUBLIC_ALL = [
    "AdviserComparisonResult",
    "compare_many",
    "compare_teacher_and_candidate",
]
FORBIDDEN_DYNAMIC_CALLS = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "getattr",
    "globals",
    "locals",
    "setattr",
    "vars",
    "importlib.import_module",
}


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return parent + "." + node.attr if parent else node.attr
    return ""


def _dynamic_findings(path: Path) -> list[tuple[str, int]]:
    source = path.read_text(encoding="utf-8", errors="strict")
    tree = ast.parse(source, filename=str(path))
    findings: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node.func)
        if name in FORBIDDEN_DYNAMIC_CALLS:
            findings.append((name, int(node.lineno)))
    return sorted(findings)


def _local_imports(path: Path) -> set[str]:
    source = path.read_text(encoding="utf-8", errors="strict")
    tree = ast.parse(source, filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _package_manifest(patch_zip: Path) -> dict[str, Any]:
    with zipfile.ZipFile(patch_zip, "r") as archive:
        return json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))


def _verify_package_hashes(patch_zip: Path) -> None:
    manifest = _package_manifest(patch_zip)
    with zipfile.ZipFile(patch_zip, "r") as archive:
        for item in manifest["files"]:
            relative = str(item["relative_path"])
            raw = archive.read("payload/" + relative)
            actual = _sha256_bytes(raw)
            expected = str(item["sha256"]).lower()
            if actual != expected:
                raise AssertionError("PACKAGE PAYLOAD HASH MISMATCH: " + relative)
    print("PACKAGE_PAYLOAD_HASHES: PASS")


def _verify_zip_contract(root: Path, patch_zip: Path) -> None:
    script = root / "scripts" / "validate_patch_zip.py"
    result = subprocess.run(
        [sys.executable, str(script), str(patch_zip)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout)
    print("ZIP CONTRACT: PASS")


def _verify_source_identity(root: Path, patch_zip: Path) -> None:
    manifest = _package_manifest(patch_zip)
    target_item = next(
        item for item in manifest["files"]
        if item["relative_path"] == TARGET_RELATIVE_PATH
    )
    accepted = {str(value).lower() for value in target_item["accepted_existing_sha256"]}
    if EXPECTED_ORIGINAL_SHA256 not in accepted:
        raise AssertionError("ORIGINAL SOURCE IDENTITY MISSING FROM MANIFEST")
    installed = _sha256_path(root / TARGET_RELATIVE_PATH)
    if installed != str(target_item["sha256"]).lower():
        raise AssertionError("INSTALLED TARGET HASH DOES NOT MATCH MANIFEST")
    print("SOURCE_IDENTITY_GUARD: PASS")


def _verify_line_law_and_syntax(root: Path) -> None:
    for relative in FAMILY_RELATIVE_PATHS:
        path = root / relative
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8 BOM: " + relative)
        source = raw.decode("utf-8", errors="strict")
        count = len(source.splitlines())
        if not 100 < count < 500:
            raise AssertionError(f"LINE LAW FAILED: {relative}: {count}")
        ast.parse(source, filename=str(path))
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _verify_dynamic_safety(root: Path) -> None:
    findings: dict[str, list[tuple[str, int]]] = {}
    for relative in FAMILY_RELATIVE_PATHS:
        current = _dynamic_findings(root / relative)
        if current:
            findings[relative] = current
    if findings:
        raise AssertionError("SEMANTIC DYNAMIC FINDINGS: " + repr(findings))
    print("SEMANTIC_DYNAMIC_SAFETY: PASS")


def _verify_dependency_direction(root: Path) -> None:
    base = root / "kanda_reasoner_app/routing_signal_scorer/adviser_offline/harness"
    facade = _local_imports(base / "comparison_engine.py")
    analysis = _local_imports(base / "_comparison_engine_analysis.py")
    support = _local_imports(base / "_comparison_engine_support.py")
    model = _local_imports(base / "_comparison_engine_result_model.py")
    if "_comparison_engine_analysis" not in facade:
        raise AssertionError("FACADE DOES NOT IMPORT ANALYSIS OWNER")
    if "_comparison_engine_result_model" not in facade:
        raise AssertionError("FACADE DOES NOT IMPORT RESULT MODEL OWNER")
    if "_comparison_engine_support" not in facade:
        raise AssertionError("FACADE DOES NOT IMPORT SUPPORT OWNER")
    if "_comparison_engine_support" not in analysis:
        raise AssertionError("ANALYSIS DOES NOT DEPEND ON SUPPORT")
    if "_comparison_engine_support" not in model:
        raise AssertionError("RESULT MODEL DOES NOT DEPEND ON SUPPORT")
    for modules in (analysis, support, model):
        if "comparison_engine" in modules:
            raise AssertionError("HELPER TO FACADE BACK REFERENCE")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")


def _base_candidate() -> dict[str, Any]:
    return {
        "schema_version": "3.41-adviser-schema-family-design",
        "case_id": "case-001",
        "candidate_id": "cand-001",
        "candidate_version": "v1",
        "run_id": "run-001",
        "input_hash": "abc",
        "governance_domain": "coding",
        "path_recommendation": "fast_path",
        "required_prompt_groups": ["python_refactoring", "architecture_review"],
        "required_specialist_prompts": ["python_specialist"],
        "recommended_prompt_groups": ["testing"],
        "recommended_specialist_prompts": [],
        "context_requirements": {
            "required": ["source", "tests"],
            "recommended": ["docs"],
            "optional": [],
            "missing_required": [],
            "missing_recommended": [],
        },
        "risk_assessment": {"severity": "low", "flags": [], "critical_risks": []},
        "governance_flags": {
            "freeze": [], "box": [], "startup": [], "prompt_library": [],
            "patch_delivery": [], "authority": [], "adversarial": [],
        },
        "advisory_proceed_recommendation": "CONDITIONAL",
        "requires_human_confirmation": "false",
        "authority_statement": "advisory_only",
        "rationale": {"short": "bounded rationale", "evidence": []},
    }


def _clone(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _teacher(answer: dict[str, Any], status: str = "approved_as_gold") -> dict[str, Any]:
    return {
        "case_id": answer["case_id"],
        "teacher_id": "teach-001",
        "review_status": status,
        "answer": _clone(answer),
    }


def _behavior_payload(module: Any) -> dict[str, Any]:
    exact = _base_candidate()
    mismatch = _clone(exact)
    mismatch["governance_domain"] = "freeze"
    mismatch["path_recommendation"] = "routed_work"
    mismatch["requires_human_confirmation"] = "true"
    mismatch["required_prompt_groups"].append("freeze_protocol")
    mismatch["required_specialist_prompts"].append("freeze_specialist")
    mismatch["context_requirements"]["required"].append("frozen_memory")
    mismatch["risk_assessment"]["severity"] = "critical"
    candidate_less = _clone(exact)
    unsafe = _clone(exact)
    unsafe["governance_domain"] = "freeze"
    unsafe["advisory_proceed_recommendation"] = "YES"
    unsafe["requires_human_confirmation"] = "false"
    unsafe["authority_statement"] = "router_authority"
    cases = {
        "exact_reviewed": (_teacher(exact), exact, "ordinary input"),
        "draft_teacher": (_teacher(exact, "draft"), exact, "ordinary input"),
        "candidate_not_mapping": (_teacher(exact), ["bad"], "ordinary input"),
        "structured_mismatch": (_teacher(mismatch), candidate_less, "ordinary input"),
        "unsafe_guard": (_teacher(mismatch), unsafe, "freeze automatically without confirmation"),
        "invalid_teacher_payload": (
            {"case_id": "case-bad", "review_status": "approved_as_gold", "answer": "not-a-mapping"},
            exact,
            "ordinary input",
        ),
    }
    comparisons = {
        name: module.compare_teacher_and_candidate(
            teacher_answer=teacher_answer,
            candidate_answer=candidate_answer,
            input_text=input_text,
            run_id="probe-run",
        )
        for name, (teacher_answer, candidate_answer, input_text) in cases.items()
    }
    private = {
        "core_fields": module._compare_core_fields(mismatch, candidate_less),
        "missing_list": module._missing_list_items(
            "required_prompt_groups", mismatch, candidate_less, severity="high"
        ),
        "missing_context": module._missing_context_items(mismatch, candidate_less),
        "risk_severity": module._risk_severity_disagreement(mismatch, candidate_less),
        "field_severity_authority": module._field_severity(
            "authority_statement", "advisory_only", "router_authority", mismatch, candidate_less
        ),
        "field_severity_proceed": module._field_severity(
            "advisory_proceed_recommendation", "NO", "YES", mismatch, candidate_less
        ),
        "field_impact_unknown": module._field_impact("unknown_field"),
        "field_recommendation_authority": module._field_recommendation("authority_statement"),
        "teacher_payload_mapping": module._teacher_payload(_teacher(exact)),
        "teacher_payload_nonmapping": module._teacher_payload("bad"),
        "teacher_review_status": module._teacher_review_status(_teacher(exact)),
        "teacher_review_status_nonmapping": module._teacher_review_status("bad"),
        "extract_case_teacher": module._extract_case_id({"case_id": "tcase"}, {"case_id": "ccase"}),
        "extract_case_candidate": module._extract_case_id({}, {"case_id": "ccase"}),
        "answer_ref_id": module._answer_ref({"answer_id": "a1"}, "teacher"),
        "answer_ref_case": module._answer_ref({"case_id": "c1"}, "candidate"),
        "answer_ref_nonmapping": module._answer_ref([], "candidate"),
        "candidate_domain": module._candidate_domain({"governance_domain": "freeze"}),
        "severity_guard_known": module._severity_from_guard({"severity": "P0_CRITICAL"}),
        "severity_guard_unknown": module._severity_from_guard({"severity": "UNKNOWN"}),
        "aggregate_empty": module._aggregate_severity([]),
        "aggregate_mixed": module._aggregate_severity(
            [{"severity": "low"}, {"severity": "critical"}, {"severity": "medium"}]
        ),
        "disagreement_no_missing": module._disagreement(
            field="x", teacher_value=1, candidate_value=2,
            severity="low", impact="i", recommendation="r"
        ),
        "disagreement_missing": module._disagreement(
            field="x", teacher_value=1, candidate_value=2,
            severity="high", impact="i", recommendation="r", missing_items=("a", "b")
        ),
        "string_sequence_list": module._as_string_sequence([1, "x"]),
        "string_sequence_text": module._as_string_sequence("abc"),
        "string_sequence_mapping": module._as_string_sequence({"a": 1}),
    }
    instance = module.AdviserComparisonResult(
        ok=True, report_id="r", run_id="run", case_id="case",
        teacher_answer_ref="t", candidate_answer_ref="c",
        disagreements=({"field": "x"},), aggregate_severity="low",
        promotion_blocker=False, review_status="reviewed",
        teacher_review_status="approved_as_gold", candidate_guard_ok=True,
        resource_limits_ok=True,
    )
    return {
        "public_all": list(module.__all__),
        "public_class_module": module.AdviserComparisonResult.__module__,
        "constants": {
            name: getattr(module, name)
            for name in ("FEATURE_ID", "SCHEMA_VERSION", "AUTHORITY_STATEMENT")
        },
        "constant_collections": {
            "TEACHER_REVIEWED_STATUSES": sorted(module.TEACHER_REVIEWED_STATUSES),
            "UNSAFE_PROCEED_VALUES": sorted(module.UNSAFE_PROCEED_VALUES),
            "GOVERNED_DOMAINS": sorted(module.GOVERNED_DOMAINS),
            "SEVERITY_ORDER": dict(module.SEVERITY_ORDER),
            "P_SEVERITY_TO_DISAGREEMENT": dict(module.P_SEVERITY_TO_DISAGREEMENT),
        },
        "comparisons": comparisons,
        "compare_many": module.compare_many(
            [
                {"teacher_answer": _teacher(exact), "candidate_answer": exact, "input_text": "ordinary input", "run_id": "case-run"},
                "invalid-case",
                {"teacher_answer": _teacher(mismatch), "candidate_answer": candidate_less, "input_text": "ordinary input"},
            ],
            run_id="many-run",
        ),
        "private": private,
        "dataclass_to_dict": instance.to_dict(),
    }


def _verify_public_contract(module: Any) -> None:
    if list(module.__all__) != EXPECTED_PUBLIC_ALL:
        raise AssertionError("PUBLIC __all__ CHANGED")
    if module.AdviserComparisonResult.__module__ != (
        "kanda_reasoner_app.routing_signal_scorer.adviser_offline.harness.comparison_engine"
    ):
        raise AssertionError("PUBLIC CLASS MODULE IDENTITY CHANGED")
    expected_signatures = {
        "compare_teacher_and_candidate": "(*, teacher_answer: 'Mapping[str, Any] | object', candidate_answer: 'Mapping[str, Any] | object', input_text: 'object' = '', run_id: 'str' = 'run-not-recorded-pure-harness') -> 'dict[str, object]'",
        "compare_many": "(cases: 'Sequence[Mapping[str, Any]]', *, run_id: 'str' = 'run-not-recorded-pure-harness') -> 'list[dict[str, object]]'",
    }
    for name, expected in expected_signatures.items():
        if str(inspect.signature(getattr(module, name))) != expected:
            raise AssertionError("PUBLIC SIGNATURE CHANGED: " + name)
    params = module.AdviserComparisonResult.__dataclass_params__
    if params is None or params.frozen is not True:
        raise AssertionError("DATACLASS FROZEN CONTRACT CHANGED")
    print("PUBLIC_API_PRESERVATION: PASS")
    print("DECORATOR_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")


def _verify_behavior(module: Any) -> None:
    payload = _behavior_payload(module)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    actual = _sha256_bytes(raw)
    if actual != EXPECTED_BEHAVIOR_SHA256:
        raise AssertionError("BEHAVIOR DIGEST CHANGED: " + actual)
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _verify_fresh_audits(root: Path) -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    results = []
    for relative in FAMILY_RELATIVE_PATHS:
        result = run_large_module_split_audit(
            root,
            root / relative,
            classifier_mode="heuristic",
        )
        classification = result.data["refactor_safety_classification"]
        results.append((relative, classification))
        if classification["label"] != "SAFE REFACTORING":
            raise AssertionError("FRESH AST NOT SAFE: " + relative)
        if classification["hard_blockers"]:
            raise AssertionError("FRESH AST HARD BLOCKERS: " + relative)
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("FRESH_FAMILY_AST_FITNESS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()
    root = _project_root()
    patch_zip = Path(args.patch_zip).resolve()
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    _verify_zip_contract(root, patch_zip)
    _verify_package_hashes(patch_zip)
    _verify_source_identity(root, patch_zip)
    _verify_line_law_and_syntax(root)
    _verify_dynamic_safety(root)
    _verify_dependency_direction(root)

    module = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.adviser_offline.harness.comparison_engine"
    )
    _verify_public_contract(module)
    _verify_behavior(module)
    _verify_fresh_audits(root)
    print("INSTALLABILITY_FITNESS: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
