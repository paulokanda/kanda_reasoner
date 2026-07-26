# project-path: scripts/validate_architecture_warning_cleanup_batch26_symbol_atlas_large_module_refactor_v1.py
"""Validate Batch 26 symbol-atlas large-module refactor."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "architecture-warning-cleanup-batch26-symbol-atlas-large-module-refactor-v1"
TARGET_FILES = (
    "kanda_reasoner_app/reasoner_symbol_atlas/_related_file_finder_support.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/import_analyzer.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/complete_json_adapter.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py",
)
HELPER_FILES = (
    "kanda_reasoner_app/reasoner_symbol_atlas/_related_file_finder_path_helpers_private.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/import_analyzer_ast_private.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/complete_json_adapter_helpers_private.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder_matching_private.py",
)
TEST_FILE = "tests/test_architecture_warning_cleanup_batch26_symbol_atlas_large_module_refactor.py"
MAX_LINES = 500


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run(command: list[str], root: Path) -> str:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        command,
        cwd=str(root),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    if completed.returncode != 0:
        raise RuntimeError(
            "Command failed: " + " ".join(command) + "\n" + output
        )
    return output


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _assert_empty_all(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "__all__":
                if not isinstance(node.value, ast.List) or node.value.elts:
                    raise AssertionError(str(path) + " must keep empty __all__")
                return
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if not isinstance(node.value, ast.List) or node.value.elts:
                        raise AssertionError(str(path) + " must keep empty __all__")
                    return
    raise AssertionError(str(path) + " is missing explicit empty __all__")


def main() -> int:
    root = _project_root()
    files = TARGET_FILES + HELPER_FILES + (TEST_FILE, __file__)
    for relative in files:
        path = root / relative if isinstance(relative, str) else Path(relative)
        if not path.exists():
            raise FileNotFoundError(str(path))
        if _line_count(path) > MAX_LINES:
            raise AssertionError(str(path) + " exceeds 500 lines")

    for relative in HELPER_FILES:
        _assert_empty_all(root / relative)

    _run([sys.executable, "-m", "py_compile", *files], root)
    _run([sys.executable, TEST_FILE], root)
    architecture_output = _run(
        [
            sys.executable,
            "kanda_reasoner_app/manage_architecture/manage_architecture.py",
            "--root",
            str(root),
            "--validate",
        ],
        root,
    )
    if "Errors: 0" not in architecture_output:
        raise AssertionError("Architecture validation did not report Errors: 0")
    for relative in TARGET_FILES:
        needle = "MODULE_TOO_LARGE             " + relative
        if needle in architecture_output:
            raise AssertionError("Target module still too large: " + relative)
    if "CIRCULAR_IMPORT" in architecture_output:
        raise AssertionError("CIRCULAR_IMPORT finding introduced")

    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
