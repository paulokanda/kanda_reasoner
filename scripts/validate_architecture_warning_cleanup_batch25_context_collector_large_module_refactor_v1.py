"""Validate Batch 25 context collector large-module refactor."""

from __future__ import annotations

import importlib.util
import py_compile
import subprocess
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "architecture-warning-cleanup-batch25-context-collector-large-module-refactor-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_VALIDATOR = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture.py"
TEST_FILE = PROJECT_ROOT / "tests" / "test_architecture_warning_cleanup_batch25_context_collector_large_module_refactor.py"

TOUCHED_FILES = [
    "kanda_reasoner_app/reasoner_context_collector/collector_ast.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_ast_helpers_private.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_canonical_conflicts.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_canonical_conflicts_helpers_private.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_canonical_conflicts_scoring_private.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_implementation_chronology.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_implementation_chronology_helpers_private.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap_helpers_private.py",
    "tests/test_architecture_warning_cleanup_batch25_context_collector_large_module_refactor.py",
    "scripts/validate_architecture_warning_cleanup_batch25_context_collector_large_module_refactor_v1.py",
]

TARGET_LARGE_MODULE_PATHS = [
    "kanda_reasoner_app/reasoner_context_collector/collector_ast.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_canonical_conflicts.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_implementation_chronology.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap.py",
]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _compile_touched_files() -> None:
    for relative_path in TOUCHED_FILES:
        path = PROJECT_ROOT / relative_path
        _assert(path.exists(), f"Missing touched file: {relative_path}")
        py_compile.compile(str(path), doraise=True)


def _assert_touched_files_under_limit() -> None:
    for relative_path in TOUCHED_FILES:
        line_count = len((PROJECT_ROOT / relative_path).read_text(encoding="utf-8").splitlines())
        _assert(line_count <= 500, f"Touched file above 500 lines: {relative_path} ({line_count})")


def _run_characterization_tests() -> None:
    module_name = "batch25_context_collector_characterization"
    spec = importlib.util.spec_from_file_location(module_name, TEST_FILE)
    _assert(spec is not None and spec.loader is not None, "Could not load characterization test module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    temp_root = PROJECT_ROOT / "_tmp_batch25_context_collector_test"
    if temp_root.exists():
        for child in sorted(temp_root.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        temp_root.rmdir()
    temp_root.mkdir(parents=True, exist_ok=True)
    try:
        module.test_context_collector_public_facades_keep_expected_outputs()
        module.test_parse_python_file_public_facade_keeps_core_shape(temp_root)
    finally:
        for child in sorted(temp_root.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        if temp_root.exists():
            temp_root.rmdir()


def _run_architecture_validation() -> str:
    completed = subprocess.run(
        [sys.executable, str(ARCHITECTURE_VALIDATOR), "--root", str(PROJECT_ROOT), "--validate"],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = completed.stdout + completed.stderr
    _assert(completed.returncode == 0, "Architecture validator returned a non-zero exit code")
    _assert("Errors: 0" in output, "Architecture validation did not report Errors: 0")
    _assert("CIRCULAR_IMPORT" not in output, "Architecture validation reported CIRCULAR_IMPORT")
    for target in TARGET_LARGE_MODULE_PATHS:
        needle = f"WARNING MODULE_TOO_LARGE             {target}"
        _assert(needle not in output, f"Target module still reports MODULE_TOO_LARGE: {target}")
    return output


def main() -> int:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    _compile_touched_files()
    _assert_touched_files_under_limit()
    _run_characterization_tests()
    _run_architecture_validation()

    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
