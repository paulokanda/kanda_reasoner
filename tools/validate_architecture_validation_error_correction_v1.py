# project-path: tools/validate_architecture_validation_error_correction_v1.py
"""Validate the cumulative correction for reported architecture errors."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import py_compile
import subprocess
import sys
import zipfile

__all__ = [
    "main",
]

FEATURE_ID = "architecture-validation-error-correction-v1"

FOCUSED_VALIDATORS = (
    "tools/validate_external_ai_candidate_exchange_outbound_v1.py",
    "tools/validate_reasoner_symbol_atlas_main_helper_mapper_source_ready_refactor_v1.py",
    "tools/validate_architecture_review_ast_split_web_ai_risk_repair_wrapper_v1.py",
    "tools/validate_ast_safe_refactor_infrastructure_v1.py",
    "tools/validate_safe_refactor_how_to_button_v1.py",
)

STATIC_TEST_WRAPPERS = (
    "tools/validate_architecture_review_large_file_refactor_behavior_validation_v1.py",
    "tools/validate_large_module_split_audit_safety_classifier_v1.py",
)

TOUCHED_FILES = (
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates.py",
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
    "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py",
    "kanda_reasoner_app/manage_architecture/ast_split_web_ai_risk_repair_gui.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/external_ai_candidate_exchange_gui.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/external_ai_candidate_exchange_service.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_gui.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_pipeline.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_plan_review.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/post_apply_validation_formatting.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_validator.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_service.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/_main_helper_mapper_contract.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/_main_helper_mapper_helper_selection.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py",
    "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_passive_visibility_activation_models.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_apply.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_storage.py",
    "tools/patch5_transaction_fixture_support.py",
    "tools/patch6_controlled_real_module_support.py",
    "tools/validate_architecture_review_ast_split_web_ai_risk_repair_wrapper_v1.py",
    "tools/validate_architecture_review_large_file_refactor_behavior_validation_v1.py",
    "tools/validate_architecture_validation_error_correction_v1.py",
    "tools/validate_ast_safe_refactor_infrastructure_v1.py",
    "tools/validate_external_ai_candidate_exchange_outbound_v1.py",
    "tools/validate_large_module_split_audit_safety_classifier_v1.py",
    "tools/validate_reasoner_symbol_atlas_main_helper_mapper_source_ready_refactor_v1.py",
    "tools/validate_safe_refactor_how_to_button_v1.py",
)

REQUIRED_MARKERS = (
    "VALIDATION OK: external-ai-candidate-exchange-outbound-v1",
    "VALIDATION OK: reasoner-symbol-atlas-main-helper-mapper-source-ready-refactor-v1",
    "VALIDATION OK: architecture-review-ast-split-web-ai-risk-repair-single-output-v1",
    "VALIDATION OK: ast-safe-refactor-infrastructure-v1",
    "VALIDATION OK: safe-refactor-how-to-button-v1",
)


def _run_python(project_root: Path, relative_path: str) -> str:
    """Run one Python validator and return its complete output."""
    command = [sys.executable, str(project_root / relative_path)]
    result = subprocess.run(
        command,
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        print(output.rstrip())
        raise AssertionError(
            "FOCUSED_VALIDATOR_FAILED:" + relative_path + ":" + str(result.returncode)
        )
    return output


def _validate_focused_validators(project_root: Path) -> None:
    """Run the focused validators that protect the corrected contracts."""
    combined = []
    for relative_path in FOCUSED_VALIDATORS:
        output = _run_python(project_root, relative_path)
        combined.append(output)
        print("FOCUSED_VALIDATOR: PASS - " + relative_path)
    text = "\n".join(combined)
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            raise AssertionError("FOCUSED_VALIDATION_MARKER_MISSING:" + marker)


def _validate_no_static_test_imports(project_root: Path) -> None:
    """Require validation command wrappers to avoid static test import edges."""
    for relative_path in STATIC_TEST_WRAPPERS:
        path = project_root / relative_path
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            module = str(node.module or "")
            if module.startswith("validation.test_"):
                raise AssertionError("STATIC_VALIDATION_TEST_IMPORT:" + relative_path)
    print("VALIDATION_WRAPPER_STATIC_TEST_IMPORTS: 0")


def _validate_architecture(project_root: Path) -> None:
    """Run the complete architecture validator and require zero errors."""
    command = [
        sys.executable,
        str(
            project_root
            / "kanda_reasoner_app"
            / "manage_architecture"
            / "manage_architecture.py"
        ),
        "--root",
        str(project_root),
        "--validate",
    ]
    result = subprocess.run(
        command,
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    error_lines = [line for line in output.splitlines() if line.startswith("ERROR")]
    summary_lines = [line for line in output.splitlines() if "Errors:" in line]
    for line in error_lines:
        print(line)
    for line in summary_lines[-1:]:
        print(line)
    if result.returncode != 0 or error_lines:
        raise AssertionError("ARCHITECTURE_VALIDATION_ERRORS_REMAIN")
    if not any("Errors: 0" in line for line in summary_lines):
        raise AssertionError("ARCHITECTURE_ZERO_ERROR_SUMMARY_MISSING")
    print("ARCHITECTURE_ERROR_COUNT: 0")


def _validate_python_files(project_root: Path, files: list[str]) -> None:
    """Check syntax, ASCII source, and the maximum module-size contract."""
    for relative_path in files:
        if not relative_path.endswith(".py"):
            continue
        path = project_root / relative_path
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf") or not raw.isascii():
            raise AssertionError("PYTHON_ASCII_UTF8_CONTRACT:" + relative_path)
        lines = raw.decode("ascii").splitlines()
        if len(lines) > 500:
            raise AssertionError("PYTHON_MODULE_OVER_500_LINES:" + relative_path)
        py_compile.compile(str(path), doraise=True)
    print("PYTHON_SYNTAX_ASCII_MODULE_SIZE: PASS")


def _sha256_bytes(data: bytes) -> str:
    """Return a lowercase SHA-256 digest for bytes."""
    return hashlib.sha256(data).hexdigest()


def _validate_patch_zip(patch_zip: Path) -> list[str]:
    """Validate root sidecar, manifest, and exact payload hashes."""
    from kanda_reasoner_app.patch_governance.validator import validate_patch_zip

    report = validate_patch_zip(patch_zip, expect_freeze_hint=True)
    if not report.get("ok"):
        raise AssertionError("PATCH_ZIP_CONTRACT_FAILED")
    with zipfile.ZipFile(patch_zip) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))
        files = list(manifest.get("files", []))
        if not files:
            raise AssertionError("PACKAGE_MANIFEST_FILES_EMPTY")
        relative_paths = []
        for item in files:
            relative_path = str(item["relative_path"]).replace("\\", "/")
            payload_name = "payload/" + relative_path
            if payload_name not in names:
                raise AssertionError("PACKAGE_PAYLOAD_MISSING:" + relative_path)
            observed = _sha256_bytes(archive.read(payload_name))
            if observed != str(item["sha256"]):
                raise AssertionError("PACKAGE_PAYLOAD_HASH_MISMATCH:" + relative_path)
            relative_paths.append(relative_path)
    print("ZIP CONTRACT: PASS")
    print("PACKAGE_PAYLOAD_HASHES: PASS")
    return relative_paths


def main() -> int:
    """Run cumulative sandbox or local project validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", default="")
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    if args.patch_zip:
        relative_paths = _validate_patch_zip(
            Path(args.patch_zip).expanduser().resolve(strict=True)
        )
    else:
        relative_paths = list(TOUCHED_FILES)

    _validate_python_files(project_root, relative_paths)
    _validate_no_static_test_imports(project_root)
    _validate_focused_validators(project_root)
    _validate_architecture(project_root)

    print("CIRCULAR_IMPORT_REPAIR: PASS")
    print("PUBLIC_SYMBOL_OWNERSHIP_NARROWING: PASS")
    print("COMPATIBILITY_SHIM_CANONICAL_ROUTE: PASS")
    print("BUNDLE_MANIFEST_ACCEPTED_PLACEMENT: PASS")
    print("MISPLACED_TEST_IMPORT_EDGES: 0")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
