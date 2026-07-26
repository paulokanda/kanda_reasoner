# project-path: scripts/validate_architecture_warning_cleanup_batch20_public_api_instability_followup_v1.py
"""Focused validator for Batch 20 public API instability follow-up repair."""

from __future__ import annotations

import ast
import py_compile
import subprocess
import sys
import warnings
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch20-public-api-instability-followup-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPAIR_SCRIPT = PROJECT_ROOT / "scripts/repair_architecture_warning_cleanup_batch20_public_api_instability_followup_v1.py"
TEST_FILE = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch20_public_api_instability_followup.py"
ARCHITECTURE_VALIDATOR = PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
TARGET_HELPERS = (
    PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_state_private_impl.py",
    PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_process_private_impl.py",
    PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py",
    PROJECT_ROOT / "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_paths_private_impl.py",
)

__all__ = ["main"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _has_top_level_dunder_all(path: Path) -> bool:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(_read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                return True
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                return True
    return False


def validate_py_compile() -> None:
    for path in (Path(__file__), REPAIR_SCRIPT, TEST_FILE):
        require(path.is_file(), f"Missing validation target: {path}")
        py_compile.compile(str(path), doraise=True)


def validate_repair_script_static_contract() -> None:
    text = _read_text(REPAIR_SCRIPT)
    require("exec(compile" not in text, "repair script must not execute target module source")
    require("_remove_empty_dunder_all" in text, "repair script must remove the prior empty helper __all__ declaration")
    require("refusing to remove non-empty __all__" in text, "repair script must refuse non-empty helper __all__ values")
    require('"snippets"' in text, "repair script star-import scan must continue skipping snippets")
    require("warnings.simplefilter(\"ignore\", SyntaxWarning)" in text, "repair script must suppress unrelated SyntaxWarning noise")


def validate_repair_script_idempotent() -> None:
    result = subprocess.run(
        [sys.executable, str(REPAIR_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require(result.returncode == 0, output)
    require(f"REPAIR OK: {FEATURE_ID}" in result.stdout, output)
    require("invalid escape sequence" not in output, output)
    require("SyntaxWarning" not in output, output)


def validate_helper_all_removed_when_present() -> None:
    for path in TARGET_HELPERS:
        if path.is_file():
            require(not _has_top_level_dunder_all(path), f"Unexpected helper __all__ remains in {path}")
            py_compile.compile(str(path), doraise=True)


def validate_architecture_no_errors() -> None:
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
    require("ERROR   PUBLIC_API_INSTABILITY" not in output, output)


def main() -> int:
    validate_py_compile()
    validate_repair_script_static_contract()
    validate_repair_script_idempotent()
    validate_helper_all_removed_when_present()
    validate_architecture_no_errors()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
