"""Validate Batch 24 context-bundle large-module refactor."""

from __future__ import annotations

import ast
import importlib.util
import py_compile
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

FEATURE_ID = "architecture-warning-cleanup-batch24-context-bundle-large-module-refactor-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_FILES = (
    Path("kanda_reasoner_app/reasoner_context_bundle/file_manifest_builder.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/file_manifest_records_private.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_validation_private.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_paths_private.py"),
    Path("tests/test_architecture_warning_cleanup_batch24_context_bundle_large_module_refactor.py"),
    Path("scripts/validate_architecture_warning_cleanup_batch24_context_bundle_large_module_refactor_v1.py"),
)
LINE_COUNT_TARGETS = (
    Path("kanda_reasoner_app/reasoner_context_bundle/file_manifest_builder.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/file_manifest_records_private.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_validation_private.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_paths_private.py"),
)
PRIVATE_HELPER_TARGETS = (
    Path("kanda_reasoner_app/reasoner_context_bundle/file_manifest_records_private.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_validation_private.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_paths_private.py"),
)
PUBLIC_FACADE_TARGETS = (
    Path("kanda_reasoner_app/reasoner_context_bundle/file_manifest_builder.py"),
    Path("kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py"),
)
TEST_FILE = Path("tests/test_architecture_warning_cleanup_batch24_context_bundle_large_module_refactor.py")
ARCHITECTURE_VALIDATOR = Path("kanda_reasoner_app/manage_architecture/manage_architecture.py")

__all__: list[str] = []


def _project_path(relative_path: Path) -> Path:
    return PROJECT_ROOT / relative_path


def _read_text(relative_path: Path) -> str:
    return _project_path(relative_path).read_text(encoding="utf-8")


def _line_count(relative_path: Path) -> int:
    return len(_read_text(relative_path).splitlines())


def _compile_targets(paths: Iterable[Path]) -> None:
    for relative_path in paths:
        py_compile.compile(str(_project_path(relative_path)), doraise=True)


def _find_all_assignment(tree: ast.Module) -> ast.AST | None:
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "__all__":
                return node.value
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return node.value
    return None


def _assert_line_counts() -> None:
    too_large = []
    for relative_path in LINE_COUNT_TARGETS:
        count = _line_count(relative_path)
        if count > 500:
            too_large.append(str(relative_path) + " has " + str(count) + " lines")
    if too_large:
        raise AssertionError("Touched file line-count limit exceeded: " + "; ".join(too_large))


def _assert_private_helper_public_surface() -> None:
    for relative_path in PRIVATE_HELPER_TARGETS:
        tree = ast.parse(_read_text(relative_path))
        value = _find_all_assignment(tree)
        if value is None:
            raise AssertionError(str(relative_path) + " does not declare __all__")
        if not isinstance(value, ast.List) or value.elts:
            raise AssertionError(str(relative_path) + " must keep an empty __all__")


def _assert_public_facades_keep_public_all() -> None:
    for relative_path in PUBLIC_FACADE_TARGETS:
        tree = ast.parse(_read_text(relative_path))
        value = _find_all_assignment(tree)
        if value is None:
            raise AssertionError(str(relative_path) + " does not declare __all__")
        if not isinstance(value, ast.List) or not value.elts:
            raise AssertionError(str(relative_path) + " must keep a non-empty public __all__")


def _run_characterization_test() -> None:
    test_path = _project_path(TEST_FILE)
    spec = importlib.util.spec_from_file_location("batch24_context_bundle_test", test_path)
    if spec is None or spec.loader is None:
        raise AssertionError("Unable to load characterization test module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.test_batch24_context_bundle_public_facades_still_run()


ARCHITECTURE_TARGET_FRAGMENTS = tuple(
    str(path).replace("\\", "/")
    for path in LINE_COUNT_TARGETS
)
ARCHITECTURE_SUMMARY_PATTERN = re.compile(r"Errors:\s*(\d+)")


def _architecture_detail_lines(output: str, level: str) -> list[str]:
    prefix = level.upper()
    return [
        line
        for line in output.splitlines()
        if line.lstrip().startswith(prefix)
    ]


def _line_touches_target(line: str) -> bool:
    normalized = line.replace("\\", "/")
    return any(fragment in normalized for fragment in ARCHITECTURE_TARGET_FRAGMENTS)


def _assert_scoped_architecture_result(
    output: str,
    return_code: int,
) -> int:
    if "ARCHITECTURE VALIDATION SUMMARY" not in output:
        raise AssertionError(
            "Architecture validator did not produce a recognizable summary:\n"
            + output
        )

    match = ARCHITECTURE_SUMMARY_PATTERN.search(output)
    if match is None:
        raise AssertionError(
            "Architecture validator summary does not expose an error count:\n"
            + output
        )

    global_error_count = int(match.group(1))
    if return_code not in (0, 1):
        raise AssertionError(
            "Architecture validator terminated unexpectedly with exit code "
            + str(return_code)
            + ":\n"
            + output
        )

    target_errors = [
        line
        for line in _architecture_detail_lines(output, "ERROR")
        if _line_touches_target(line)
    ]
    if target_errors:
        raise AssertionError(
            "Architecture errors affect the Batch 24 context-bundle target scope:\n"
            + "\n".join(target_errors)
        )

    target_warning_codes = ("MODULE_TOO_LARGE", "CIRCULAR_IMPORT")
    target_warnings = [
        line
        for line in _architecture_detail_lines(output, "WARNING")
        if _line_touches_target(line)
        and any(code in line for code in target_warning_codes)
    ]
    if target_warnings:
        raise AssertionError(
            "Architecture regression remains in the Batch 24 target scope:\n"
            + "\n".join(target_warnings)
        )

    return global_error_count


def _assert_scope_policy_characterization() -> None:
    unrelated_output = """ARCHITECTURE VALIDATION SUMMARY
Total issues: 3 | Errors: 3 | Warnings: 0 | Other: 0
DETAILS
ERROR   BUNDLE_SAFETY KandaReasoner-Windows-Portable.zip :: unrelated
ERROR   CROSS_BOX_PUBLIC_SYMBOL_COLLISION sha256_bytes :: unrelated
ERROR   BUNDLE_SAFETY another_bundle.zip :: unrelated
"""
    count = _assert_scoped_architecture_result(unrelated_output, 1)
    if count != 3:
        raise AssertionError("Scoped architecture policy lost the global error count.")

    target_output = """ARCHITECTURE VALIDATION SUMMARY
Total issues: 1 | Errors: 1 | Warnings: 0 | Other: 0
DETAILS
ERROR   CROSS_BOX_PUBLIC_SYMBOL_COLLISION symbol :: owner=kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py
"""
    try:
        _assert_scoped_architecture_result(target_output, 1)
    except AssertionError:
        return
    raise AssertionError(
        "Scoped architecture policy did not reject a target-related error."
    )


def _run_architecture_validation() -> str:
    command = [
        sys.executable,
        str(_project_path(ARCHITECTURE_VALIDATOR)),
        "--root",
        str(PROJECT_ROOT),
        "--validate",
    ]
    result = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout
    global_error_count = _assert_scoped_architecture_result(
        output,
        result.returncode,
    )
    print(
        "ARCHITECTURE GLOBAL ERRORS OUTSIDE TARGET: "
        + str(global_error_count)
    )
    for line in _architecture_detail_lines(output, "ERROR"):
        if not _line_touches_target(line):
            print("ARCHITECTURE GLOBAL ERROR OUTSIDE TARGET: " + line.strip())
    print("ARCHITECTURE CONTEXT BUNDLE TARGET SCOPE: PASS")
    return output


def main() -> int:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    _compile_targets(TARGET_FILES)
    _assert_line_counts()
    _assert_private_helper_public_surface()
    _assert_public_facades_keep_public_all()
    _run_characterization_test()
    _assert_scope_policy_characterization()
    _run_architecture_validation()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
