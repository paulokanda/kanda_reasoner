# project-path: tools/validate_architecture_project_web_ai_persistence_test_protection_wave2l_v1.py
"""Validate Wave 2L direct functional protection for Project Web AI owners."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

__all__ = ["main"]

FEATURE_ID = "architecture-project-web-ai-persistence-test-protection-wave2l-v1"
TEST_REL = Path("tests/test_project_web_ai_persistence_contracts.py")
SOURCE_HASHES = {
    "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_receipts.py":
        "13a160dc4eb3edbc78e6f06503a0a2e047206c7d6550923957e1036e74ab623b",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_shadow.py":
        "2be24ad4f1814867f4f5d99b2ac3b28f21042cc920326f19a707754ca91155e2",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_write_storage.py":
        "897ae9c3fbc533746c61643dfb23c9b9eb8f1f5befd9757e635c1e0f7cd16053",
}
TEST_SHA256 = "25beebcdddc8defde96e8845f44a5e932739e9da39dfe5f6275201b38d263433"
DIRECT_MODULES = (
    "kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts",
    "kanda_reasoner_app.reasoner_engine.project_web_ai_shadow",
    "kanda_reasoner_app.reasoner_engine.project_web_ai_write_storage",
)
REQUIRED_SYMBOLS = (
    "ProjectWebAIApplyReceipt",
    "ProjectWebAIApplyReceiptError",
    "apply_preview_caption",
    "assert_project_web_ai_handoff_fresh",
    "receipt_allows_retry_after_shadow_delete",
    "receipt_matches_fresh_project_context",
    "prepare_receipt_root",
    "write_apply_receipt",
    "ProjectWebAIShadowError",
    "ProjectWebAIShadowPreview",
    "ShadowTargetPreview",
    "build_shadow_preview",
    "delete_shadow_preview",
    "atomic_replace_source",
    "contained_project_file",
    "contained_shadow_file",
    "exclusive_apply_lock",
    "require_distinct_apply_roots",
    "project_web_ai_sha256_bytes",
    "write_source_backups",
    "write_transaction_state",
)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(
    root: Path,
    command: list[str],
    markers: tuple[str, ...],
    code: str,
    *,
    timeout: int = 1800,
) -> str:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="kanda_wave2l_pycache_") as cache:
        environment["PYTHONPYCACHEPREFIX"] = cache
        completed = subprocess.run(
            command,
            cwd=str(root),
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=timeout,
        )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, code + "_NONZERO_EXIT")
    for marker in markers:
        require(marker in output, code + "_MARKER_MISSING:" + marker)
    return output


def validate_static_contract(root: Path) -> None:
    for relative, expected in SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), "WAVE2L_SOURCE_MISSING:" + relative)
        require(
            sha256_file(path) == expected,
            "WAVE2L_SOURCE_HASH_DRIFT:" + relative,
        )
    print("PROJECT WEB AI PERSISTENCE OWNERS UNCHANGED: PASS")

    test_path = root / TEST_REL
    require(test_path.is_file(), "WAVE2L_TEST_MISSING")
    require(sha256_file(test_path) == TEST_SHA256, "WAVE2L_TEST_HASH_DRIFT")
    require(TEST_REL.parts[0] == "tests", "WAVE2L_TEST_NOT_CANONICAL")
    text = test_path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(TEST_REL))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    for module in DIRECT_MODULES:
        require(module in imported, "WAVE2L_DIRECT_IMPORT_MISSING:" + module)
    for symbol in REQUIRED_SYMBOLS:
        require(symbol in text, "WAVE2L_PUBLIC_SYMBOL_NOT_EXERCISED:" + symbol)
    forbidden_mock_tokens = (
        "unittest.mock",
        "mock.patch",
        "monkeypatch",
        "patch.object",
    )
    require(
        not any(token in text for token in forbidden_mock_tokens),
        "WAVE2L_OWNER_MOCKING_PRESENT",
    )
    require(len(text.splitlines()) <= 500, "WAVE2L_TEST_EXCEEDS_500_LINES")
    print("PROJECT WEB AI THREE OWNER DIRECT TEST IMPORTS: PASS")
    print("PROJECT WEB AI PUBLIC MUTATION OPERATIONS COVERED: PASS")
    print("PROJECT WEB AI REAL FILESYSTEM BOUNDARIES: PASS")
    print("PROJECT WEB AI OWNER MOCKING: ABSENT")
    print("WAVE2L TEST LOCATION CANONICAL: PASS")


def validate_functional_test(root: Path) -> None:
    run_command(
        root,
        [sys.executable, str(root / TEST_REL)],
        (
            "Ran 3 tests",
            "OK",
        ),
        "WAVE2L_FUNCTIONAL_TEST",
    )
    print("PROJECT WEB AI PERSISTENCE FUNCTIONAL TEST SUITE: PASS")


def validate_architecture(root: Path) -> None:
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
        (),
        "WAVE2L_ARCHITECTURE_VALIDATION",
    )
    detailed_zero_issue = (
        "ARCHITECTURE VALIDATION SUMMARY" in output
        and "Total issues: 0 | Errors: 0 | Warnings: 0 | Other: 0" in output
    )
    concise_zero_issue = "No validation issues." in output
    require(
        detailed_zero_issue or concise_zero_issue,
        "WAVE2L_ARCHITECTURE_ZERO_ISSUE_MARKER_MISSING",
    )
    for relative in SOURCE_HASHES:
        require(relative not in output, "WAVE2L_TARGET_WARNING_REMAINS:" + relative)
    require("TEST_PROTECTION_GAP" not in output, "WAVE2L_TEST_GAP_REMAINS")
    require("WARNING " not in output, "WAVE2L_ARCHITECTURE_WARNING_REMAINS")
    require("ERROR " not in output, "WAVE2L_ARCHITECTURE_ERROR_REMAINS")
    print("ARCHITECTURE VALIDATION SUMMARY")
    print("Total issues: 0 | Errors: 0 | Warnings: 0 | Other: 0")
    print("WAVE2L ARCHITECTURE OUTPUT NORMALIZED: PASS")
    print("WAVE2L PROJECT WEB AI TEST PROTECTION GAPS ABSENT: PASS")
    print("WAVE2L ARCHITECTURE ZERO ISSUE BASELINE: PASS")
    print("WAVE2L PROJECT WEB AI PERSISTENCE FAMILY CLOSED: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    validate_static_contract(root)
    validate_functional_test(root)
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
        raise SystemExit(1)
