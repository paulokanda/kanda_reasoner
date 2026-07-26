# project-path: scripts/validate_architecture_warning_cleanup_batch20_install_warning_invalid_escape_repair_v1.py
"""Focused validator for Batch 20 invalid-escape install warning repair.

This validator verifies that the Batch 20 runner-help repair no longer lets
SyntaxWarning output from unrelated project files, such as snippets with
invalid escape sequences, break the PowerShell installer.
"""

from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch20-install-warning-invalid-escape-repair-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPAIR_SCRIPT = PROJECT_ROOT / "scripts/repair_architecture_warning_cleanup_batch20_runner_help_public_ownership_v1.py"
TEST_FILE = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch20_install_warning_invalid_escape_repair.py"
ARCHITECTURE_VALIDATOR = PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture.py"

__all__ = ["main"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def validate_py_compile() -> None:
    for path in (Path(__file__), REPAIR_SCRIPT, TEST_FILE):
        require(path.is_file(), f"Missing validation target: {path}")
        py_compile.compile(str(path), doraise=True)


def validate_repair_script_suppresses_unrelated_syntax_warnings() -> None:
    text = _read_text(REPAIR_SCRIPT)
    require("import warnings" in text, "repair script must import warnings")
    require("warnings.simplefilter(\"ignore\", SyntaxWarning)" in text, "repair script must suppress SyntaxWarning during AST/compile checks")
    require('"snippets"' in text, "repair script star-import scan must skip snippets")
    require('".project_reference"' in text, "repair script star-import scan must skip project reference folders")
    require("ast.parse(_read_text(path)" in text, "repair script must remain AST-based for project scans")
    require("exec(compile" not in text, "repair script must not execute target module source")


def validate_repair_script_idempotent_and_stdout_clean_enough() -> None:
    result = subprocess.run(
        [sys.executable, str(REPAIR_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require(result.returncode == 0, output)
    require("REPAIR OK: architecture-warning-cleanup-batch20-runner-help-public-ownership-repair-v1" in result.stdout, output)
    require("invalid escape sequence" not in output, output)
    require("SyntaxWarning" not in output, output)


def validate_architecture_no_duplicate_public_symbols() -> None:
    result = subprocess.run(
        [sys.executable, str(ARCHITECTURE_VALIDATOR), "--root", str(PROJECT_ROOT), "--validate"],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require(result.returncode == 0, output)
    require("Errors: 0" in output, output)
    require("DUPLICATE_PUBLIC_SYMBOL" not in output, output)


def main() -> int:
    validate_py_compile()
    validate_repair_script_suppresses_unrelated_syntax_warnings()
    validate_repair_script_idempotent_and_stdout_clean_enough()
    validate_architecture_no_duplicate_public_symbols()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
