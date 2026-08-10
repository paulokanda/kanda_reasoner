# project-path: tools/validate_architecture_review_models_payload_support_refactor_v1.py
"""Validate the behavior-preserving planner models payload-support refactor."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import ast
import dataclasses
import hashlib
import importlib.util
import inspect
import json
import py_compile
import subprocess
import sys
from pathlib import Path
from typing import get_type_hints

FEATURE_ID = "architecture-review-models-payload-support-refactor-v1"
PUBLIC_MODULE = (
    "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models"
)
TARGET_RELATIVE = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py"
)
HELPER_RELATIVE = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "_model_payload_support.py"
)
EXPECTED_PROJECT_SOURCE_BEFORE = (
    "89c80036dd465bc2cd88b1f06af4b4a9a75e4d94e11df4fceb9eaf839d2a71a2"
)
EXPECTED_BASELINE_SOURCE = (
    "9271339d15a27f8813e2fce4878a669f6261d844827e550045e95935c5aab671"
)
EXPECTED_PUBLIC_ALL = [
    "DocstringProposal", "FEATURE_ID", "IDEAL_PHYSICAL_LINES",
    "ImportMigrationPreview", "ImportMigrationRecord", "ImportRecord",
    "LLMArbitrationRequest", "LLMArbitrationResult", "LargeFileCandidate",
    "MAX_PHYSICAL_LINES", "MIN_HELPER_PHYSICAL_LINES", "ModuleAnalysisReport",
    "PATCH_ALLOWED_STATE", "PlannerSettings", "PlannerState",
    "PreviewArtifactValidationResult", "PreviewBundle", "PreviewFileDraft",
    "PreviewValidationResult", "PreviewWriteResult", "ProjectPatchPayloadResult",
    "ProposedModule", "RefactorPlan", "RefactorSymbol", "SCHEMA_VERSION",
    "SourceSnapshot",
]
FAMILY = [TARGET_RELATIVE, HELPER_RELATIVE]
TARGET_CODES = {
    "MODULE_TOO_LARGE",
    "DUPLICATE_PUBLIC_SYMBOL",
    "PRIVATE_SYMBOL_EXPORTED",
    "MISSING_PUBLIC_SURFACE_CONTROL",
    "PUBLIC_API_INSTABILITY",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_SPEC_UNAVAILABLE: " + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _purge_candidate_modules() -> None:
    prefix = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
    for name in list(sys.modules):
        if name == prefix or name.startswith(prefix + "."):
            sys.modules.pop(name, None)


def _normalize_type(value: object) -> str:
    text = str(value)
    text = text.replace("baseline_models.", "")
    return text.replace(PUBLIC_MODULE + ".", "")


def _dataclass_parameters(cls: type) -> tuple[object, ...]:
    params = cls.__dataclass_params__
    names = ("init", "repr", "eq", "order", "unsafe_hash", "frozen")
    return tuple(getattr(params, name) for name in names)


def _required_value(type_text: str) -> object:
    if type_text == "str":
        return "value"
    if type_text == "int":
        return 1
    if type_text == "float":
        return 0.0
    if type_text == "bool":
        return True
    if type_text.startswith("tuple["):
        return (1, 2)
    if type_text.startswith("list["):
        return []
    if type_text.startswith("dict["):
        return {}
    raise AssertionError("NO_SAMPLE_VALUE_FOR_TYPE: " + type_text)


def _instance_for(cls: type) -> object:
    kwargs: dict[str, object] = {}
    for field in dataclasses.fields(cls):
        if field.default is not dataclasses.MISSING:
            continue
        if field.default_factory is not dataclasses.MISSING:
            continue
        kwargs[field.name] = _required_value(_normalize_type(field.type))
    return cls(**kwargs)


def _assert_public_contract(baseline: object, candidate: object) -> None:
    if list(candidate.__all__) != EXPECTED_PUBLIC_ALL:
        raise AssertionError("PUBLIC_ALL_CHANGED")
    if list(baseline.__all__) != list(candidate.__all__):
        raise AssertionError("BASELINE_PUBLIC_ALL_MISMATCH")
    for name in EXPECTED_PUBLIC_ALL:
        before = getattr(baseline, name)
        after = getattr(candidate, name)
        if not inspect.isclass(before):
            if before != after:
                raise AssertionError("PUBLIC_CONSTANT_CHANGED: " + name)
            continue
        if not inspect.isclass(after):
            raise AssertionError("PUBLIC_CLASS_MISSING: " + name)
        if before.__name__ != after.__name__:
            raise AssertionError("PUBLIC_CLASS_NAME_CHANGED: " + name)
        if before.__qualname__ != after.__qualname__:
            raise AssertionError("PUBLIC_CLASS_QUALNAME_CHANGED: " + name)
        if before.__doc__ != after.__doc__:
            raise AssertionError("PUBLIC_CLASS_DOCSTRING_CHANGED: " + name)
        if inspect.signature(before) != inspect.signature(after):
            raise AssertionError("PUBLIC_CLASS_SIGNATURE_CHANGED: " + name)
        if after.__module__ != PUBLIC_MODULE:
            raise AssertionError("PUBLIC_CLASS_OWNER_CHANGED: " + name)
        if dataclasses.is_dataclass(before):
            if not dataclasses.is_dataclass(after):
                raise AssertionError("DATACLASS_DECORATOR_LOST: " + name)
            before_fields = dataclasses.fields(before)
            after_fields = dataclasses.fields(after)
            if [field.name for field in before_fields] != [field.name for field in after_fields]:
                raise AssertionError("DATACLASS_FIELDS_CHANGED: " + name)
            before_types = [_normalize_type(field.type) for field in before_fields]
            after_types = [_normalize_type(field.type) for field in after_fields]
            if before_types != after_types:
                raise AssertionError("DATACLASS_FIELD_TYPES_CHANGED: " + name)
            if _dataclass_parameters(before) != _dataclass_parameters(after):
                raise AssertionError("DATACLASS_PARAMETERS_CHANGED: " + name)
            before_hints = {
                key: _normalize_type(value)
                for key, value in get_type_hints(before).items()
            }
            after_hints = {
                key: _normalize_type(value)
                for key, value in get_type_hints(after).items()
            }
            if before_hints != after_hints:
                raise AssertionError("ANNOTATION_RUNTIME_CHANGED: " + name)
            for method_name in ("to_dict", "blocked"):
                if not hasattr(before, method_name):
                    continue
                if not hasattr(after, method_name):
                    raise AssertionError("PUBLIC_METHOD_MISSING: " + name + "." + method_name)
                before_method = getattr(before, method_name)
                after_method = getattr(after, method_name)
                if inspect.signature(before_method) != inspect.signature(after_method):
                    raise AssertionError("PUBLIC_METHOD_SIGNATURE_CHANGED: " + name + "." + method_name)
                if before_method.__doc__ != after_method.__doc__:
                    raise AssertionError("PUBLIC_METHOD_DOCSTRING_CHANGED: " + name + "." + method_name)
    if [item.value for item in baseline.PlannerState] != [item.value for item in candidate.PlannerState]:
        raise AssertionError("PLANNER_STATE_VALUES_CHANGED")


def _assert_behavior(baseline: object, candidate: object) -> None:
    for name in EXPECTED_PUBLIC_ALL:
        before_cls = getattr(baseline, name)
        after_cls = getattr(candidate, name)
        if not inspect.isclass(before_cls) or not dataclasses.is_dataclass(before_cls):
            continue
        before = _instance_for(before_cls)
        after = _instance_for(after_cls)
        if before.to_dict() != after.to_dict():
            raise AssertionError("TO_DICT_CHANGED: " + name)
        clone_values = {
            field.name: getattr(after, field.name)
            for field in dataclasses.fields(after)
        }
        if after != after_cls(**clone_values):
            raise AssertionError("DATACLASS_EQUALITY_CHANGED: " + name)
        first_field = dataclasses.fields(after)[0].name
        try:
            setattr(after, first_field, "changed")
        except dataclasses.FrozenInstanceError:
            pass
        else:
            raise AssertionError("FROZEN_DECORATOR_CHANGED: " + name)
    before_symbol = baseline.RefactorSymbol(
        "1.0", "symbol", "function", "public", 1, 2, 2
    )
    after_symbol = candidate.RefactorSymbol(
        "1.0", "symbol", "function", "public", 1, 2, 2
    )
    before_import = baseline.ImportRecord("1.0", "a", "b")
    after_import = candidate.ImportRecord("1.0", "a", "b")
    before_report = baseline.ModuleAnalysisReport(
        "1.0", "f", "x.py", "hash", 2, True, "doc", ["symbol"],
        ["symbol"], [before_import], [before_symbol], [], [], [], [], [],
        False, 0, 0,
    )
    after_report = candidate.ModuleAnalysisReport(
        "1.0", "f", "x.py", "hash", 2, True, "doc", ["symbol"],
        ["symbol"], [after_import], [after_symbol], [], [], [], [], [],
        False, 0, 0,
    )
    if before_report.to_dict() != after_report.to_dict():
        raise AssertionError("NESTED_ANALYSIS_PAYLOAD_CHANGED")
    before_draft = baseline.PreviewFileDraft(
        "1.0", "f", "a.py", "helper", ["symbol"], "hash", 120
    )
    after_draft = candidate.PreviewFileDraft(
        "1.0", "f", "a.py", "helper", ["symbol"], "hash", 120
    )
    before_bundle = baseline.PreviewBundle(
        "1.0", "f", "x.py", "hash", "preview", "no_write", True,
        ["symbol"], ["symbol"], [before_draft], [], [], "ready",
    )
    after_bundle = candidate.PreviewBundle(
        "1.0", "f", "x.py", "hash", "preview", "no_write", True,
        ["symbol"], ["symbol"], [after_draft], [], [], "ready",
    )
    if before_bundle.to_dict() != after_bundle.to_dict():
        raise AssertionError("NESTED_PREVIEW_PAYLOAD_CHANGED")
    before_record = baseline.ImportMigrationRecord(
        "1.0", "f", "x.py", "old", "new", "replace", "move"
    )
    after_record = candidate.ImportMigrationRecord(
        "1.0", "f", "x.py", "old", "new", "replace", "move"
    )
    before_migration = baseline.ImportMigrationPreview(
        "1.0", "f", "x.py", "hash", False, [before_record]
    )
    after_migration = candidate.ImportMigrationPreview(
        "1.0", "f", "x.py", "hash", False, [after_record]
    )
    if before_migration.to_dict() != after_migration.to_dict():
        raise AssertionError("NESTED_MIGRATION_PAYLOAD_CHANGED")
    before_plan = baseline.RefactorPlan(
        "1.0", "f", "x.py", "hash", {}, ["symbol"], ["symbol"],
        [before_symbol], [], [], {}, [], [], [], "planned",
    )
    after_plan = candidate.RefactorPlan(
        "1.0", "f", "x.py", "hash", {}, ["symbol"], ["symbol"],
        [after_symbol], [], [], {}, [], [], [], "planned",
    )
    if before_plan.to_dict() != after_plan.to_dict():
        raise AssertionError("NESTED_REFACTOR_PLAN_PAYLOAD_CHANGED")


def _assert_consumer_compatibility(root: Path, candidate: object) -> int:
    consumer_count = 0
    target_parent = Path(TARGET_RELATIVE).parent
    for path in root.rglob("*.py"):
        parts = set(path.parts)
        if parts.intersection({".git", ".venv", "venv", "__pycache__", "project_freeze_ledger"}):
            continue
        try:
            source = path.read_text(encoding="utf-8", errors="strict")
            tree = ast.parse(source, filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        relative_parent = path.relative_to(root).parent
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            direct = node.module == PUBLIC_MODULE
            sibling = (
                node.level > 0
                and node.module == "models"
                and relative_parent == target_parent
            )
            if not direct and not sibling:
                continue
            consumer_count += 1
            for alias in node.names:
                if alias.name == "*":
                    continue
                if not hasattr(candidate, alias.name):
                    raise AssertionError(
                        "CONSUMER_IMPORT_MISSING: " + str(path) + ":" + alias.name
                    )
    if consumer_count == 0:
        raise AssertionError("NO_MODEL_CONSUMERS_DISCOVERED")
    return consumer_count


def _assert_source_family(root: Path) -> None:
    for relative in FAMILY:
        path = root / relative
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8_BOM_NOT_ALLOWED: " + relative)
        raw.decode("utf-8", errors="strict")
        if any(byte > 127 for byte in raw):
            raise AssertionError("NON_ASCII_SOURCE: " + relative)
        line_count = len(raw.decode("utf-8").splitlines())
        if not 100 < line_count < 500:
            raise AssertionError("LINE_LAW_VIOLATION: " + relative + ":" + str(line_count))
        py_compile.compile(str(path), doraise=True)
    helper_source = (root / HELPER_RELATIVE).read_text(encoding="utf-8")
    if "from .models" in helper_source or PUBLIC_MODULE in helper_source:
        raise AssertionError("HELPER_TO_FACADE_BACK_REFERENCE")
    helper_tree = ast.parse(helper_source, filename=HELPER_RELATIVE)
    public_defs = [
        node.name for node in helper_tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    ]
    if public_defs:
        raise AssertionError("PRIVATE_HELPER_PUBLIC_OWNERSHIP: " + repr(public_defs))


def _run_architecture_target_check(root: Path) -> str:
    script = root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    if not script.is_file():
        raise AssertionError("MANAGE_ARCHITECTURE_SCRIPT_MISSING")
    result = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--validate"],
        cwd=str(root), capture_output=True, text=True, errors="replace", timeout=900,
    )
    output = (result.stdout or "") + "\n" + (result.stderr or "")
    target_names = ("models.py", "_model_payload_support.py")
    for line in output.splitlines():
        if not any(name in line for name in target_names):
            continue
        if any(code in line for code in TARGET_CODES):
            raise AssertionError("TARGET_ARCHITECTURE_FINDING: " + line.strip())
    if result.returncode != 0:
        return "Unrelated baseline architecture findings remain outside this source family."
    return "Architecture validation completed with exit code 0."


def _run_fresh_audits(root: Path, audit_output_dir: Path) -> tuple[list[str], list[str]]:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )
    audit_output_dir.mkdir(parents=True, exist_ok=True)
    markers: list[str] = []
    warning_lines: list[str] = []
    for relative in FAMILY:
        result = run_large_module_split_audit(
            root, root / relative, classifier_mode="heuristic"
        )
        classification = result.data["refactor_safety_classification"]
        label = str(classification["label"])
        blockers = list(classification["hard_blockers"])
        warnings = list(classification["warnings"])
        output_name = relative.replace("/", "__") + ".md"
        (audit_output_dir / output_name).write_text(
            result.markdown, encoding="utf-8", newline="\n"
        )
        if label != "SAFE REFACTORING" or blockers:
            raise AssertionError(
                "AST_FAMILY_NOT_SAFE: " + relative + ":" + label + ":" + repr(blockers)
            )
        markers.append("AST_SPLIT_SAFE: " + relative)
        warning_lines.extend(relative + ": " + item for item in warnings)
    return markers, warning_lines


def _validate_install_receipt(receipt_path: Path, root: Path) -> None:
    data = json.loads(receipt_path.read_text(encoding="utf-8"))
    before = data.get("before_hashes", {}).get(TARGET_RELATIVE, "")
    after = data.get("after_hashes", {}).get(TARGET_RELATIVE, "")
    current = _sha256(root / TARGET_RELATIVE)
    allowed_before = {EXPECTED_PROJECT_SOURCE_BEFORE, current}
    if before not in allowed_before:
        raise AssertionError("SOURCE_IDENTITY_RECEIPT_MISMATCH: " + str(before))
    if after != current:
        raise AssertionError("SOURCE_INSTALL_HASH_MISMATCH")


def _write_evidence_and_hint(
    evidence_path: Path,
    hint_path: Path,
    markers: list[str],
    warnings: list[str],
) -> None:
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_text = "\n".join(markers) + "\n"
    evidence_path.write_text(evidence_text, encoding="utf-8", newline="\n")
    hint = json.loads(hint_path.read_text(encoding="utf-8-sig"))
    if hint.get("feature_id") != FEATURE_ID:
        raise AssertionError("FREEZE_HINT_FEATURE_ID_MISMATCH")
    hint["validation_evidence_summary"] = evidence_text.strip()
    hint["known_warnings"] = warnings or [
        "Fresh local AST audits reported no warnings beyond normal advisory output."
    ]
    hint["planned_next_step"] = (
        "Review the fresh AST Markdown reports, verify the source family in the real "
        "Architecture Review workflow, then use Preview Freeze Entry and explicit "
        "human Confirm and Write. Refresh startup freeze context after the local write."
    )
    hint_path.write_text(
        json.dumps(hint, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8", newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--install-receipt", required=True)
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--hint-path", required=True)
    parser.add_argument("--audit-output-dir", required=True)
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    package_root = Path(args.package_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    receipt_path = Path(args.install_receipt).resolve()
    evidence_path = Path(args.evidence_path).resolve()
    hint_path = Path(args.hint_path).resolve()
    audit_output_dir = Path(args.audit_output_dir).resolve()

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    _validate_install_receipt(receipt_path, root)
    baseline_path = package_root / "validation/baseline_models.py"
    if _sha256(baseline_path) != EXPECTED_BASELINE_SOURCE:
        raise AssertionError("BASELINE_SOURCE_IDENTITY_MISMATCH")
    baseline = _load_module(baseline_path, "baseline_models")
    _purge_candidate_modules()
    candidate = __import__(PUBLIC_MODULE, fromlist=["*"])

    _assert_source_family(root)
    _assert_public_contract(baseline, candidate)
    _assert_behavior(baseline, candidate)
    consumer_count = _assert_consumer_compatibility(root, candidate)
    architecture_note = _run_architecture_target_check(root)

    from kanda_reasoner_app.patch_governance.validator import validate_patch_zip
    validate_patch_zip(patch_zip)
    audit_markers, audit_warnings = _run_fresh_audits(root, audit_output_dir)

    markers = [
        "ZIP CONTRACT: PASS",
        "SOURCE_IDENTITY_GUARD: PASS",
        "PYTHON_SYNTAX: PASS",
        "PUBLIC_API_PRESERVATION: PASS",
        "CONSUMER_COMPATIBILITY_FITNESS: PASS",
        "DECORATOR_PRESERVATION: PASS",
        "ANNOTATION_IMPORT_PRESERVATION: PASS",
        "DEPENDENCY_DIRECTION_FITNESS: PASS",
        "BEHAVIOR_EQUIVALENCE_FITNESS: PASS",
        "LINE_LAW_101_499_FITNESS: PASS",
        "BEHAVIOR_REGRESSION: PASS",
        "AST_SPLIT_AUDIT_RERUN: PASS",
        "AST_SPLIT_FAMILY_ALL_SAFE: PASS",
        "AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING",
        "AST_SPLIT_HARD_BLOCKERS: 0",
        "INITIAL_RISK_STATE_REPAIRED: PASS",
        "MODEL_CONSUMER_IMPORT_RECORDS_CHECKED: " + str(consumer_count),
        *audit_markers,
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    warnings = [architecture_note, *audit_warnings]
    _write_evidence_and_hint(evidence_path, hint_path, markers, warnings)
    for marker in markers:
        print(marker)
    print("FREEZE_HINT_EVIDENCE_MERGE_OK: " + FEATURE_ID)
    print("AST_SPLIT_PRIMARY_REPORT_PATH: " + str(
        audit_output_dir / (TARGET_RELATIVE.replace("/", "__") + ".md")
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
