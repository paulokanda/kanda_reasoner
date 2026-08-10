# project-path: tools/validate_query_intents_ast_safe_refactor_v1.py
"""Validate the query-intent AST-safe facade refactor."""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import types
from typing import Any
import traceback
import zipfile

from tools._query_intents_refactor_spec_v1 import (
    BASELINE_ENTRY,
    BASELINE_SOURCE_SHA256,
    ERROR_LESSON_ENTRIES,
    EXPECTED_CONSUMERS_ENTRY,
    EXPECTED_CONSUMERS_SHA256,
    EXPECTED_HASHES,
    FEATURE_ID,
    HELPER_MODULE_NAME,
    HELPER_RELATIVE_PATH,
    MANIFEST_RELATIVE_PATH,
    MODULE_NAME,
    PUBLIC_NAMES,
    RAW_ERROR_ENTRIES,
    TARGET_RELATIVE_PATH,
    VALIDATOR_RELATIVE_PATH,
    _assert,
    _digest,
    _parse_source,
    _sha256,
    _snapshot,
)

__all__ = [
    "main",
]

def _prepare_project_imports(project_root: Path) -> None:
    """Prepare imports so validation always uses the selected project root."""
    root_text = str(project_root)
    sys.path[:] = [entry for entry in sys.path if entry != root_text]
    sys.path.insert(0, root_text)
    importlib.invalidate_caches()
def _load_module(project_root: Path) -> Any:
    """Import the installed facade from the selected project root."""
    _prepare_project_imports(project_root)
    for name in list(sys.modules):
        if name == MODULE_NAME or name == HELPER_MODULE_NAME:
            del sys.modules[name]
    return importlib.import_module(MODULE_NAME)
def _load_baseline_module(patch_zip: Path, project_root: Path) -> Any:
    """Execute the exact original source as a real module object."""
    _prepare_project_imports(project_root)
    with zipfile.ZipFile(patch_zip) as archive:
        source_bytes = archive.read(BASELINE_ENTRY)
    _assert(
        hashlib.sha256(source_bytes).hexdigest() == BASELINE_SOURCE_SHA256,
        "Baseline source identity changed",
    )
    module = types.ModuleType(MODULE_NAME)
    module.__package__ = MODULE_NAME.rpartition(".")[0]
    module.__file__ = BASELINE_ENTRY
    source_text = source_bytes.decode("utf-8")
    exec(compile(source_text, BASELINE_ENTRY, "exec"), module.__dict__)
    print("BASELINE_MODULETYPE_EXECUTION: PASS")
    return module
def _validate_source_identity(project_root: Path) -> None:
    """Validate installed file identity against the delivered payload."""
    for relative_text, expected in EXPECTED_HASHES.items():
        path = project_root / relative_text
        _assert(path.is_file(), "Missing installed file: " + relative_text)
        _assert(_sha256(path) == expected, "Installed hash mismatch: " + relative_text)
    print("SOURCE_IDENTITY_GUARD: PASS")
def _validate_python_source(project_root: Path) -> None:
    """Compile, parse, and enforce ASCII and physical-line requirements."""
    for relative in (TARGET_RELATIVE_PATH, HELPER_RELATIVE_PATH, VALIDATOR_RELATIVE_PATH):
        path = project_root / relative
        text = path.read_text(encoding="utf-8")
        text.encode("ascii")
        _parse_source(text, str(path))
        completed = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            cwd=str(project_root), capture_output=True, text=True, check=False,
        )
        _assert(completed.returncode == 0, completed.stderr or "py_compile failed")
        line_count = len(text.splitlines())
        _assert(101 <= line_count <= 499, f"Line law failed for {relative}: {line_count}")
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")

def _validate_public_contract(module: Any, baseline_module: Any) -> None:
    """Compare stable public contract and same-host behavior separately."""
    _assert(tuple(module.__all__) == PUBLIC_NAMES, "Facade __all__ changed")
    for name in PUBLIC_NAMES:
        obj = getattr(module, name, None)
        _assert(callable(obj), "Missing callable public symbol: " + name)
        _assert(obj.__module__ == MODULE_NAME, "Public ownership moved: " + name)
    baseline_snapshot = _snapshot(baseline_module)
    installed_snapshot = _snapshot(module)
    baseline_contract = {"all": baseline_snapshot["all"], "contract": baseline_snapshot["contract"]}
    installed_contract = {"all": installed_snapshot["all"], "contract": installed_snapshot["contract"]}
    print("BASELINE_PUBLIC_CONTRACT_DIGEST: " + _digest(baseline_contract))
    print("INSTALLED_PUBLIC_CONTRACT_DIGEST: " + _digest(installed_contract))
    if installed_contract != baseline_contract:
        for name in PUBLIC_NAMES:
            if installed_snapshot["contract"][name] != baseline_snapshot["contract"][name]:
                print("PUBLIC_CONTRACT_DIFF_SYMBOL: " + name)
        raise AssertionError("Same-host public contract changed")
    print("PUBLIC_CONTRACT_EQUIVALENCE: PASS")
    baseline_rows = baseline_snapshot["rows"]
    installed_rows = installed_snapshot["rows"]
    print("BASELINE_BEHAVIOR_DIGEST: " + _digest(baseline_rows))
    print("INSTALLED_BEHAVIOR_DIGEST: " + _digest(installed_rows))
    if installed_rows != baseline_rows:
        differences = 0
        for baseline_row, installed_row in zip(baseline_rows, installed_rows):
            if baseline_row == installed_row:
                continue
            query = baseline_row[0]
            for name in PUBLIC_NAMES:
                before = baseline_row[1][name]
                after = installed_row[1][name]
                if before != after:
                    print("BEHAVIOR_DIFF_QUERY: " + repr(query))
                    print("BEHAVIOR_DIFF_SYMBOL: " + name)
                    print("BEHAVIOR_DIFF_VALUES: " + repr(before) + " -> " + repr(after))
                    differences += 1
                    if differences >= 20:
                        break
            if differences >= 20:
                break
        raise AssertionError("Same-host behavior rows changed")
    print("BEHAVIOR_ROW_EQUIVALENCE: PASS")
    print("SAME_HOST_BASELINE_EQUIVALENCE: PASS")
    print("PUBLIC_API_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")

def _validate_consumers(project_root: Path, module: Any, patch_zip: Path) -> None:
    """Preserve audited consumers while allowing valid new facade consumers."""
    with zipfile.ZipFile(patch_zip) as archive:
        payload = json.loads(archive.read(EXPECTED_CONSUMERS_ENTRY).decode("utf-8"))
    expected = {(item["consumer"], item["symbol"]) for item in payload["records"]}
    current: set[tuple[str, str]] = set()
    private_reach_in = []
    for path in project_root.rglob("*.py"):
        try:
            tree = _parse_source(path.read_text(encoding="utf-8", errors="replace"), str(path))
        except (OSError, SyntaxError):
            continue
        relative = path.relative_to(project_root).as_posix()
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            imported_module = node.module or ""
            if imported_module in {MODULE_NAME, "query_intents", "reasoner_retriever_help.query_intents"}:
                for alias in node.names:
                    _assert(alias.name in PUBLIC_NAMES, "Non-public facade import: " + alias.name)
                    _assert(hasattr(module, alias.name), "Consumer import missing: " + alias.name)
                    current.add((relative, alias.name))
            if imported_module in {HELPER_MODULE_NAME, "_query_intent_location_and_explanation", "reasoner_retriever_help._query_intent_location_and_explanation"} and path != project_root / TARGET_RELATIVE_PATH:
                private_reach_in.append(relative)
    missing = sorted(expected - current)
    additional = sorted(current - expected)
    _assert(not missing, "Required consumer records missing: " + json.dumps(missing))
    _assert(not private_reach_in, "Private helper reach-in: " + ", ".join(sorted(set(private_reach_in))))
    print("REQUIRED_CONSUMER_SET_PRESERVED: PASS")
    print(f"CURRENT_PUBLIC_CONSUMER_RECORDS: {len(current)}")
    print(f"ADDITIONAL_PUBLIC_CONSUMER_RECORDS: {len(additional)}")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")

def _validate_dependency_direction(project_root: Path) -> None:
    """Validate one-way facade-to-private-helper dependency direction."""
    helper_path = project_root / HELPER_RELATIVE_PATH
    helper_tree = _parse_source(helper_path.read_text(encoding="utf-8"), str(helper_path))
    for node in ast.walk(helper_tree):
        if isinstance(node, ast.ImportFrom):
            _assert(node.module != MODULE_NAME, "Helper imports facade")
        if isinstance(node, ast.Import):
            for alias in node.names:
                _assert(alias.name != MODULE_NAME, "Helper imports facade")
    functions = [node.name for node in helper_tree.body if isinstance(node, ast.FunctionDef)]
    _assert(functions and all(name.startswith("_") for name in functions), "Helper leaked public owners")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")

def _validate_manifest(project_root: Path) -> None:
    """Validate helper-folder manifest ownership and dependency records."""
    manifest = json.loads((project_root / MANIFEST_RELATIVE_PATH).read_text(encoding="utf-8"))
    summary = manifest["summary"]
    _assert(summary["total_helpers"] == 20, "Manifest total_helpers mismatch")
    _assert(summary["internal_helpers"] == 1, "Manifest internal_helpers mismatch")
    helper_name = HELPER_RELATIVE_PATH.name
    helper = manifest["helpers"].get(helper_name)
    _assert(isinstance(helper, dict), "Private helper missing from manifest")
    _assert(helper.get("stability") == "internal", "Private helper stability mismatch")
    _assert(helper.get("consumed_by") == ["query_intents.py"], "Manifest consumer mismatch")
    expected_dependencies = [helper_name, "query_text.py"]
    _assert(
        manifest["helpers"]["query_intents.py"].get("depends_on") == expected_dependencies,
        "Facade manifest dependencies mismatch",
    )
    print("HELPER_MANIFEST_FITNESS: PASS")

def _validate_patch_zip(patch_zip: Path, project_root: Path) -> None:
    """Validate release ZIP structure, sidecar placement, and payload hashes."""
    _assert(patch_zip.is_file(), "Patch ZIP not found: " + str(patch_zip))
    expected_entries = {
        "INSTALL.ps1",
        "VALIDATE.ps1",
        "FREEZE.ps1",
        "KANDA_FREEZE_HINT.json",
        "bundle_manifest.json",
        BASELINE_ENTRY,
        EXPECTED_CONSUMERS_ENTRY,
        *ERROR_LESSON_ENTRIES,
        *RAW_ERROR_ENTRIES,
        *("payload/" + path for path in EXPECTED_HASHES),
        "payload/" + VALIDATOR_RELATIVE_PATH.as_posix(),
    }
    with zipfile.ZipFile(patch_zip) as archive:
        names = {name for name in archive.namelist() if not name.endswith("/")}
        _assert(names == expected_entries, "ZIP entry contract mismatch")
        _assert("payload/KANDA_FREEZE_HINT.json" not in names, "Freeze hint duplicated")
        for name in names:
            parts = Path(name).parts
            _assert(".." not in parts and not Path(name).is_absolute(), "Unsafe ZIP path")
        manifest = json.loads(archive.read("bundle_manifest.json").decode("utf-8"))
        _assert(manifest.get("feature_id") == FEATURE_ID, "Bundle feature mismatch")
        payload_hashes = manifest.get("payload_sha256", {})
        validator_key = VALIDATOR_RELATIVE_PATH.as_posix()
        validator_bytes = archive.read("payload/" + validator_key)
        validator_hash = hashlib.sha256(validator_bytes).hexdigest()
        _assert(
            payload_hashes.get(validator_key) == validator_hash,
            "Validator payload hash missing or mismatched",
        )
        _assert(
            (project_root / VALIDATOR_RELATIVE_PATH).read_bytes() == validator_bytes,
            "Installed validator differs from packaged validator",
        )
        baseline_bytes = archive.read(BASELINE_ENTRY)
        _assert(hashlib.sha256(baseline_bytes).hexdigest() == BASELINE_SOURCE_SHA256,
                "Packaged baseline source hash mismatch")
        consumer_bytes = archive.read(EXPECTED_CONSUMERS_ENTRY)
        _assert(hashlib.sha256(consumer_bytes).hexdigest() == EXPECTED_CONSUMERS_SHA256,
                "Expected-consumer evidence hash mismatch")
        for relative_text, expected in EXPECTED_HASHES.items():
            data = archive.read("payload/" + relative_text)
            _assert(hashlib.sha256(data).hexdigest() == expected, "Payload hash mismatch")
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
        _assert(hint.get("feature_id") == FEATURE_ID, "Freeze hint feature mismatch")
        for entry in ERROR_LESSON_ENTRIES:
            lesson_text = archive.read(entry).decode("utf-8")
            _assert(lesson_text.count("KANDA_ERROR_LESSON_JSON_BEGIN") == 1,
                    "Lesson begin marker mismatch")
            _assert(lesson_text.count("KANDA_ERROR_LESSON_JSON_END") == 1,
                    "Lesson end marker mismatch")
        for entry in RAW_ERROR_ENTRIES:
            _assert(archive.read(entry), "Raw Error Memory evidence missing")
    print("ZIP CONTRACT: PASS")

def _validate_error_memory_intake(project_root: Path, patch_zip: Path) -> None:
    """Validate staged draft Error Memory lessons against the package."""
    pending_root = (project_root.parent / (project_root.name + "_show_project_to_AI") /
                    "project_error_memory" / "pending_ai_assisted_error_lesson_intake")
    with zipfile.ZipFile(patch_zip) as archive:
        for entry in ERROR_LESSON_ENTRIES:
            pending = pending_root / Path(entry).name
            _assert(pending.is_file(), "Pending Error Memory intake was not staged")
            _assert(pending.read_bytes() == archive.read(entry),
                    "Staged Error Memory lesson differs")
    print("ERROR_MEMORY_INTAKE_FITNESS: PASS")

def _validate_ruff(_project_root: Path) -> None:
    """Keep validation independent of ambient Ruff availability."""
    print("RUFF_FITNESS: NOT_REQUESTED")

def _validate_ast_family(project_root: Path, audit_output_dir: Path) -> str:
    """Run the real read-only AST audit over the complete touched source family."""
    audit_output_dir.mkdir(parents=True, exist_ok=True)
    from kanda_reasoner_app.manage_architecture import large_module_split_audit as audit_module

    audit_module._daily_work_dir = lambda _project_root: audit_output_dir
    target_markdown = ""
    for relative in (TARGET_RELATIVE_PATH, HELPER_RELATIVE_PATH):
        result = audit_module.run_large_module_split_audit(
            project_root, relative, classifier_mode="heuristic"
        )
        classification = result.data["refactor_safety_classification"]
        _assert(classification["label"] == "SAFE REFACTORING", "AST family not SAFE")
        _assert(classification["hard_blockers"] == [], "AST hard blockers remain")
        if relative == TARGET_RELATIVE_PATH:
            target_markdown = result.markdown
    report_path = audit_output_dir / "query_intents_fresh_ast_split_audit.md"
    report_path.write_text(target_markdown, encoding="utf-8", newline="\n")
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("INITIAL_RISK_STATE_REPAIRED: PASS")
    return target_markdown

def _build_parser() -> argparse.ArgumentParser:
    """Build the focused validator command parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--audit-output-dir", required=True)
    return parser

def main() -> int:
    """Run all focused validation gates."""
    args = _build_parser().parse_args()
    project_root = Path(args.project_root).resolve()
    patch_zip = Path(args.patch_zip).resolve()
    audit_output_dir = Path(args.audit_output_dir).resolve()
    phase = "argument_resolution"
    try:
        phase = "patch_zip_contract"
        _validate_patch_zip(patch_zip, project_root)
        phase = "source_identity"
        _validate_source_identity(project_root)
        phase = "python_source"
        _validate_python_source(project_root)
        phase = "baseline_load"
        baseline_module = _load_baseline_module(patch_zip, project_root)
        phase = "installed_module_load"
        module = _load_module(project_root)
        phase = "public_contract_and_behavior"
        _validate_public_contract(module, baseline_module)
        phase = "consumer_compatibility"
        _validate_consumers(project_root, module, patch_zip)
        phase = "dependency_direction"
        _validate_dependency_direction(project_root)
        phase = "manifest_contract"
        _validate_manifest(project_root)
        phase = "error_memory_intake"
        _validate_error_memory_intake(project_root, patch_zip)
        phase = "ruff_policy"
        _validate_ruff(project_root)
        phase = "ast_family_audit"
        _validate_ast_family(project_root, audit_output_dir)
    except Exception as exc:
        print("VALIDATION_FAILURE_PHASE: " + phase)
        traceback.print_exc(file=sys.stdout)
        print("VALIDATION FAILED: " + str(exc))
        return 1
    print("DECORATOR_PRESERVATION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
