# project-path: tools/validate_engineering_review_signal_semantics_wave2m_v1.py
"""Focused validation for Engineering Review signal semantics wave 2M."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import py_compile
import subprocess
import sys

__all__ = ["main"]

FEATURE_ID = "engineering-review-signal-semantics-wave2m-v1"

INSTALLED_HASHES = {
    '_reasoner_tools_gui_engineering_safety_review_signals.py': '6d2ae82b16d38aaab6a57b0d7ece8cd25bea9111dcef390b1f4e791a42dec8f1',
    '_reasoner_tools_gui_engineering_safety_full_audit.py': '3406df90ce51fa0df349ded3a19ce864c5407c950b71b9e935a48bfeaf18b44f',
    'kanda_reasoner_app/source_hygiene/_active_scope.py': 'ecc7017f6f7607f34fb5bb7e513d1fe2a59fea50878c5bc1ac1efa5a92087c44',
    'kanda_reasoner_app/source_hygiene/bom_scanner.py': '80b8d544690fedfc75fd0558b29537ddd02a3c57dbb1141d8e90c07fbc1e5c60',
    'kanda_reasoner_app/source_hygiene/shadow_audit.py': 'cdf5efc3717c0a29365467f65eda914ad86df93d7c9feb6f25f3a251835fa91f',
    'kanda_reasoner_app/source_hygiene/shadow_fixer.py': '7dc5ec64b370648e2c39a4f787de0eca2839f9c0b9886255a548fd6927f9aead',
    'tests/test_engineering_review_signal_semantics.py': '88da301be4b10507742b29514cc88b759b80c349eb6ad8fe3c5aa59951152fc8',
}

FROZEN_WAVE2L_HASHES = {
    (
        "kanda_reasoner_app/reasoner_engine/"
        "project_web_ai_apply_receipts.py"
    ): "13a160dc4eb3edbc78e6f06503a0a2e047206c7d6550923957e1036e74ab623b",
    (
        "kanda_reasoner_app/reasoner_engine/"
        "project_web_ai_shadow.py"
    ): "2be24ad4f1814867f4f5d99b2ac3b28f21042cc920326f19a707754ca91155e2",
    (
        "kanda_reasoner_app/reasoner_engine/"
        "project_web_ai_write_storage.py"
    ): "897ae9c3fbc533746c61643dfb23c9b9eb8f1f5befd9757e635c1e0f7cd16053",
    "tests/test_project_web_ai_persistence_contracts.py": (
        "25beebcdddc8defde96e8845f44a5e932739e9da39dfe5f6275201b38d263433"
    ),
    (
        "tools/validate_architecture_project_web_ai_"
        "persistence_test_protection_wave2l_v1.py"
    ): "b9f1f19768b31f9ddce58eaa4dd3f7ceee3db513dc10439fef6c464d44c5cfa4",
}

TARGET_PATHS = tuple(INSTALLED_HASHES)


def require(condition: bool, message: str) -> None:
    """Raise a focused validation error when a contract is not satisfied."""
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    """Return a lowercase SHA-256 digest for one file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(root: Path, relative: str) -> str:
    """Read one project-relative UTF-8 source file."""
    return (root / relative).read_text(encoding="utf-8-sig")


def run_command(
    root: Path,
    argv: list[str],
    label: str,
) -> str:
    """Run one child command, print its output, and fail closed."""
    completed = subprocess.run(
        argv,
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout or ""
    if output:
        print(output.rstrip())
    require(
        completed.returncode == 0,
        label + "_FAILED:exit_code=" + str(completed.returncode),
    )
    return output


def validate_hashes(root: Path) -> None:
    """Verify installed files and frozen Wave 2L files are byte-exact."""
    for relative, expected in INSTALLED_HASHES.items():
        path = root / relative
        require(path.is_file(), "WAVE2M_INSTALLED_FILE_MISSING:" + relative)
        require(
            sha256_file(path) == expected,
            "WAVE2M_INSTALLED_FILE_HASH_DRIFT:" + relative,
        )
    print("WAVE2M INSTALLED SOURCE HASHES: PASS")

    for relative, expected in FROZEN_WAVE2L_HASHES.items():
        path = root / relative
        require(path.is_file(), "WAVE2L_FROZEN_FILE_MISSING:" + relative)
        require(
            sha256_file(path) == expected,
            "WAVE2L_FROZEN_FILE_HASH_DRIFT:" + relative,
        )
    print("WAVE2L FROZEN PROTECTED PATHS UNCHANGED: PASS")


def validate_static_contract(root: Path) -> None:
    """Validate source ownership and fail-closed review semantics statically."""
    for relative in TARGET_PATHS:
        py_compile.compile(str(root / relative), doraise=True)

    signal_text = read_text(
        root,
        "_reasoner_tools_gui_engineering_safety_review_signals.py",
    )
    full_audit_text = read_text(
        root,
        "_reasoner_tools_gui_engineering_safety_full_audit.py",
    )
    active_scope_text = read_text(
        root,
        "kanda_reasoner_app/source_hygiene/_active_scope.py",
    )
    bom_text = read_text(
        root,
        "kanda_reasoner_app/source_hygiene/bom_scanner.py",
    )
    shadow_text = read_text(
        root,
        "kanda_reasoner_app/source_hygiene/shadow_audit.py",
    )
    fixer_text = read_text(
        root,
        "kanda_reasoner_app/source_hygiene/shadow_fixer.py",
    )
    test_text = read_text(
        root,
        "tests/test_engineering_review_signal_semantics.py",
    )

    ast.parse(signal_text)
    ast.parse(full_audit_text)

    for marker in (
        "ASSESSMENT_CLEAN",
        "ASSESSMENT_PASS_WITH_FINDINGS",
        "ASSESSMENT_DEGRADED",
        "ASSESSMENT_INVALID_COVERAGE",
        "ASSESSMENT_MISSING_EVIDENCE",
        "ASSESSMENT_DRAFT",
        "ASSESSMENT_NOT_RUN",
        "ASSESSMENT_MANUAL_REVIEW_REQUIRED",
        "ASSESSMENT_FAILED",
        "def classify_engineering_review_signal",
    ):
        require(marker in signal_text, "WAVE2M_SIGNAL_MARKER_MISSING:" + marker)
    require(
        "def _contains_inactive_reference_path" in signal_text
        and "Inactive reference paths leaked into an active-scope" in signal_text
        and "Canonical JSON evidence is also missing." in signal_text,
        "WAVE2M_SYMBOL_SIGNAL_PRECEDENCE_CONTRACT_MISSING",
    )
    print("WAVE2M SYMBOL OWNER SIGNAL PRECEDENCE: PASS")
    print("WAVE2M DECISION SIGNAL TAXONOMY: PASS")

    for marker in (
        "Execution: {outcome}",
        "Assessment: {assessment}",
        "Commands succeeded:",
        "Clean checks:",
        "Checks with findings:",
        "Invalid coverage checks:",
        "Missing evidence checks:",
        "Draft checks:",
        "Not-run checks:",
        "DEGRADED REVIEW",
        "INVALID REVIEW",
    ):
        require(marker in full_audit_text, "WAVE2M_FULL_AUDIT_MARKER_MISSING:" + marker)
    print("WAVE2M EXECUTION AND ASSESSMENT SEPARATION: PASS")

    require(
        "if not normalized:" in bom_text
        and "return set(DEFAULT_BOM_SCAN_SUFFIXES)" in bom_text,
        "WAVE2M_BOM_EMPTY_OVERRIDE_DEFAULT_CONTRACT_MISSING",
    )
    print("WAVE2M BOM EMPTY SUFFIX DEFAULT COVERAGE: PASS")

    for marker in (
        "load_reasoner_project_exclusion_rules",
        "folder_rule_matches",
        "_bundle_temp",
        "snippets",
        "workbench",
        "*deprecated*",
        "def _is_test_fixture_path",
        "def _is_test_path",
    ):
        require(
            marker in active_scope_text,
            "WAVE2M_ACTIVE_SCOPE_MARKER_MISSING:" + marker,
        )
    for text, label in (
        (bom_text, "BOM"),
        (shadow_text, "SHADOW_AUDIT"),
        (fixer_text, "FACADE_FIX_PLAN"),
    ):
        require(
            "_build_active_source_scope" in text,
            "WAVE2M_" + label + "_ACTIVE_SCOPE_OWNER_MISSING",
        )
    require(
        "exclude_tests=False" in bom_text,
        "WAVE2M_BOM_TEST_SOURCE_SCOPE_MISSING",
    )
    require(
        "exclude_tests=True" in shadow_text
        and "exclude_tests=True" in fixer_text,
        "WAVE2M_SHADOW_PRODUCTION_SCOPE_MISSING",
    )
    print("WAVE2M ACTIVE SOURCE SCOPE CANONICAL EXCLUSIONS: PASS")
    print("WAVE2M INACTIVE REFERENCE SCOPE GUARDS: PASS")

    for direct_import in (
        "_reasoner_tools_gui_engineering_safety_full_audit",
        "_reasoner_tools_gui_engineering_safety_review_signals",
        "kanda_reasoner_app.source_hygiene.bom_scanner",
        "kanda_reasoner_app.source_hygiene.shadow_audit",
        "kanda_reasoner_app.source_hygiene.shadow_fixer",
    ):
        require(
            direct_import in test_text,
            "WAVE2M_DIRECT_TEST_IMPORT_MISSING:" + direct_import,
        )
    require(
        test_text.count("    def test_") == 4,
        "WAVE2M_TEST_CASE_COUNT_NOT_FOUR",
    )
    for marker in (
        "inactive_reference_paths_filtered=true",
        "ASSESSMENT_DEGRADED",
        "_bundle_temp",
        "snippets",
        "workbench",
        "feature_deprecated",
        "tests/fixtures",
    ):
        require(
            marker in test_text,
            "WAVE2M_REVIEW_REGRESSION_MARKER_MISSING:" + marker,
        )
    print("WAVE2M DIRECT REGRESSION TEST PROTECTION: PASS")


def validate_runtime(root: Path) -> None:
    """Run focused Wave 2M tests and the pre-existing Full Audit validator."""
    test_output = run_command(
        root,
        [
            sys.executable,
            str(root / "tests/test_engineering_review_signal_semantics.py"),
        ],
        "WAVE2M_FUNCTIONAL_TEST_SUITE",
    )
    require("Ran 4 tests" in test_output, "WAVE2M_TEST_COUNT_MARKER_MISSING")
    require("OK" in test_output, "WAVE2M_TEST_OK_MARKER_MISSING")
    require(
        "test_shadow_and_facade_plans_exclude_inactive_scope" in test_output,
        "WAVE2M_ACTIVE_SCOPE_TEST_MARKER_MISSING",
    )
    print("WAVE2M FUNCTIONAL TEST SUITE: PASS")

    old_output = run_command(
        root,
        [
            sys.executable,
            str(root / "tools/validate_audit_project_engineering_safety_tabs_v1.py"),
            "--project-root",
            str(root),
        ],
        "WAVE2M_EXISTING_FULL_AUDIT_VALIDATOR",
    )
    require(
        "FULL_AUDIT_CATALOG_ORDER: PASS" in old_output,
        "WAVE2M_EXISTING_CATALOG_ORDER_MARKER_MISSING",
    )
    require(
        "FULL_AUDIT_CONTINUES_AFTER_FAILURE: PASS" in old_output,
        "WAVE2M_EXISTING_CONTINUE_MARKER_MISSING",
    )
    require(
        "VALIDATION OK: audit-project-engineering-safety-full-pontual-audit-v1r6"
        in old_output,
        "WAVE2M_EXISTING_FULL_AUDIT_VALIDATION_MARKER_MISSING",
    )
    print("WAVE2M PREVIOUS FULL AUDIT CONTRACT PRESERVED: PASS")


def validate_architecture(root: Path) -> None:
    """Require the authoritative live project architecture baseline to remain zero."""
    audit = root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    output = run_command(
        root,
        [
            sys.executable,
            str(audit),
            "--root",
            str(root),
            "--validate",
        ],
        "WAVE2M_ARCHITECTURE_VALIDATION",
    )
    detailed_zero = (
        "ARCHITECTURE VALIDATION SUMMARY" in output
        and "Total issues: 0 | Errors: 0 | Warnings: 0 | Other: 0" in output
    )
    concise_zero = "No validation issues." in output
    require(
        detailed_zero or concise_zero,
        "WAVE2M_ARCHITECTURE_ZERO_ISSUE_MARKER_MISSING",
    )
    for relative in TARGET_PATHS:
        require(relative not in output, "WAVE2M_TARGET_ARCHITECTURE_ISSUE:" + relative)
    print("ARCHITECTURE VALIDATION SUMMARY")
    print("Total issues: 0 | Errors: 0 | Warnings: 0 | Other: 0")
    print("WAVE2M ARCHITECTURE ZERO ISSUE BASELINE: PASS")


def main(argv: list[str] | None = None) -> int:
    """Run the Wave 2M focused validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.project_root).expanduser().resolve()
    require(root.is_dir(), "PROJECT_ROOT_NOT_DIRECTORY:" + str(root))
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    validate_hashes(root)
    validate_static_contract(root)
    validate_runtime(root)
    if not args.static_only:
        validate_architecture(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(type(exc).__name__ + ": " + str(exc))
        raise
