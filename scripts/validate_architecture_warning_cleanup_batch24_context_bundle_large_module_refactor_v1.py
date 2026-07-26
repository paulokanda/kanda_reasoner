"""Validate Batch 24 context-bundle large-module refactor."""

from __future__ import annotations

import ast
import importlib.util
import py_compile
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
    if result.returncode != 0:
        raise AssertionError("Architecture validator failed:\n" + output)
    if "Errors: 0" not in output:
        raise AssertionError("Architecture validation did not report Errors: 0:\n" + output)
    target_fragments = (
        "MODULE_TOO_LARGE             kanda_reasoner_app/reasoner_context_bundle/file_manifest_builder.py",
        "MODULE_TOO_LARGE             kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py",
    )
    for fragment in target_fragments:
        if fragment in output:
            raise AssertionError("Target large-module warning is still present: " + fragment)
    if "CIRCULAR_IMPORT" in output:
        raise AssertionError("Circular import finding introduced by refactor:\n" + output)
    return output


def main() -> int:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    _compile_targets(TARGET_FILES)
    _assert_line_counts()
    _assert_private_helper_public_surface()
    _assert_public_facades_keep_public_all()
    _run_characterization_test()
    _run_architecture_validation()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
