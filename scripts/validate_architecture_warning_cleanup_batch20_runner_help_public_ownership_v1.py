# project-path: scripts/validate_architecture_warning_cleanup_batch20_runner_help_public_ownership_v1.py
"""Focused validator for Batch 20 runner-help public ownership repair."""

from __future__ import annotations

import ast
import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch20-runner-help-public-ownership-repair-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPAIR_SCRIPT = PROJECT_ROOT / "scripts/repair_architecture_warning_cleanup_batch20_runner_help_public_ownership_v1.py"
TEST_FILE = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch20_runner_help_public_ownership.py"
ARCHITECTURE_VALIDATOR = PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture.py"

IMPLEMENTATION_ONLY_MODULES = (
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_state_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_process_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_paths_private_impl.py",
)
DUPLICATE_SYMBOLS = (
    "ALLOWED_ZIP_SIZE_MB_OPTIONS",
    "auto_zip_json_complete",
    "cleanup_loose_json_files_after_success",
    "cleanup_show_project_to_ai_root_after_success",
    "cleanup_transient_daily_refactor_folders",
    "clear_second_prompt_files_building_dir",
    "clear_second_prompt_files_dir",
    "DEFAULT_ZIP_SIZE_MB",
    "EXTENDED_ZIP_SIZE_MB_OPTIONS",
    "load_saved_part_size_mb",
    "publish_second_prompt_files_building_dir",
    "resolve_zip_dialog_start_folder",
    "run_zip_json_files",
    "save_selected_part_size_mb",
    "second_prompt_files_building_dir",
    "selected_part_size_mb",
    "write_second_prompt_status",
)

__all__ = ["main"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _literal_dunder_all(path: Path) -> list[str] | None:
    tree = ast.parse(_read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = ast.literal_eval(node.value)
                    require(isinstance(value, (list, tuple)), f"{path}: __all__ is not a literal sequence")
                    require(all(isinstance(item, str) for item in value), f"{path}: __all__ contains non-string entries")
                    return list(value)
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__":
                value = ast.literal_eval(node.value)
                require(isinstance(value, (list, tuple)), f"{path}: __all__ is not a literal sequence")
                require(all(isinstance(item, str) for item in value), f"{path}: __all__ contains non-string entries")
                return list(value)
    return None


def validate_py_compile() -> None:
    for path in (Path(__file__), REPAIR_SCRIPT, TEST_FILE):
        require(path.is_file(), f"Missing validation target: {path}")
        py_compile.compile(str(path), doraise=True)


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


def validate_helper_ownership_contracts() -> None:
    for relative in IMPLEMENTATION_ONLY_MODULES:
        path = PROJECT_ROOT / relative
        if not path.is_file():
            continue
        exported = _literal_dunder_all(path)
        require(exported == [], f"{relative} must be implementation-only with __all__ = [], found {exported!r}")
        py_compile.compile(str(path), doraise=True)


def validate_static_test_mentions_targets() -> None:
    text = _read_text(TEST_FILE)
    for relative in IMPLEMENTATION_ONLY_MODULES:
        require(relative in text, f"Static Batch 20 test missing helper target: {relative}")
    for symbol in DUPLICATE_SYMBOLS:
        require(symbol in text, f"Static Batch 20 test missing duplicate-symbol evidence: {symbol}")


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
    require("zip_json_files_private_impl" not in output or "DUPLICATE_PUBLIC_SYMBOL" not in output, output)


def main() -> int:
    validate_py_compile()
    validate_repair_script_idempotent()
    validate_helper_ownership_contracts()
    validate_static_test_mentions_targets()
    validate_architecture_no_duplicate_public_symbols()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
