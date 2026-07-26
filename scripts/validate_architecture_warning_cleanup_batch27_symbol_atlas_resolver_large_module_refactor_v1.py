# project-path: scripts/validate_architecture_warning_cleanup_batch27_symbol_atlas_resolver_large_module_refactor_v1.py
"""Validate Batch 27 symbol-atlas resolver large-module refactor."""

from __future__ import annotations

import ast
import os
import py_compile
import subprocess
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "architecture-warning-cleanup-batch27-symbol-atlas-resolver-large-module-refactor-v1"
TARGET_FILES = (
    "kanda_reasoner_app/reasoner_symbol_atlas/evidence_freshness.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/evidence_merger.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/implementation_responsibility_resolver.py",
)
HELPER_FILES = (
    "kanda_reasoner_app/reasoner_symbol_atlas/evidence_freshness_helpers_private.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/evidence_merger_helpers_private.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver_helpers_private.py",
    "kanda_reasoner_app/reasoner_symbol_atlas/implementation_responsibility_helpers_private.py",
)
TEST_FILE = "tests/test_architecture_warning_cleanup_batch27_symbol_atlas_resolver_large_module_refactor.py"
MAX_LINES = 500


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _run(command: list[str], root: Path) -> str:
    env = dict(os.environ)
    old_path = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(root) if not old_path else str(root) + os.pathsep + old_path
    completed = subprocess.run(
        command,
        cwd=str(root),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=240,
    )
    output = completed.stdout
    if completed.returncode != 0:
        raise RuntimeError("Command failed: " + " ".join(command) + "\n" + output)
    return output


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


def _run_characterization_shell(root: Path) -> None:
    if os.name == "nt":
        command = (
            'set "PYTHONPATH=' + str(root) + ';%PYTHONPATH%" && '
            + '"' + sys.executable + '" "' + TEST_FILE + '"'
        )
    else:
        command = (
            'PYTHONPATH="' + str(root) + os.pathsep + '$PYTHONPATH" '
            + '"' + sys.executable + '" "' + TEST_FILE + '"'
        )
    completed = subprocess.run(
        command,
        cwd=str(root),
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=240,
    )
    if completed.returncode != 0:
        raise RuntimeError("Characterization command failed\n" + completed.stdout)


def main() -> int:
    root = _project_root()
    files = TARGET_FILES + HELPER_FILES + (TEST_FILE, "scripts/validate_architecture_warning_cleanup_batch27_symbol_atlas_resolver_large_module_refactor_v1.py")
    for relative in files:
        path = root / relative
        if not path.exists():
            raise FileNotFoundError(str(path))
        if _line_count(path) > MAX_LINES:
            raise AssertionError(str(path) + " exceeds 500 lines")
    for relative in HELPER_FILES:
        _assert_empty_all(root / relative)

    for relative in files:
        py_compile.compile(str(root / relative), doraise=True)
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
    _run_characterization_shell(root)
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
