"""Validate Batch 22 static context parser large-module refactor."""

from __future__ import annotations

import ast
import importlib.util
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "architecture-warning-cleanup-batch22-static-context-parser-large-module-refactor-v1"
VALIDATION_OK = "VALIDATION OK: " + FEATURE_ID
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

TOUCHED_FILES = [
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/documentation_intent_parser.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_documentation_intent_result_helpers.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_documentation_intent_extractors.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_documentation_intent_scan_helpers.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/packaging_metadata_parser.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_packaging_metadata_result_helpers.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_packaging_metadata_file_helpers.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_packaging_metadata_file_parsers.py",
    "tests/test_architecture_warning_cleanup_batch22_static_context_parser_large_module_refactor.py",
    "scripts/validate_architecture_warning_cleanup_batch22_static_context_parser_large_module_refactor_v1.py",
]

MAX_MODULE_LINES = 500
TARGET_MODULES = [
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/documentation_intent_parser.py",
    "kanda_reasoner_app/reasoner_context_collector/parsers/static_context/packaging_metadata_parser.py",
]
PUBLIC_MODULES = [
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser",
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser",
]
HELPER_MODULES = [
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context._documentation_intent_result_helpers",
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context._documentation_intent_extractors",
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context._documentation_intent_scan_helpers",
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context._packaging_metadata_result_helpers",
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context._packaging_metadata_file_helpers",
    "kanda_reasoner_app.reasoner_context_collector.parsers.static_context._packaging_metadata_file_parsers",
]


def _project_file(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path


def _read_text(relative_path: str) -> str:
    return _project_file(relative_path).read_text(encoding="utf-8")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _compile_touched_files() -> None:
    for relative_path in TOUCHED_FILES:
        py_compile.compile(str(_project_file(relative_path)), doraise=True)


def _validate_line_counts() -> None:
    for relative_path in TOUCHED_FILES:
        if not relative_path.endswith(".py"):
            continue
        line_count = len(_read_text(relative_path).splitlines())
        _assert(
            line_count <= MAX_MODULE_LINES,
            f"{relative_path} has {line_count} lines; expected <= {MAX_MODULE_LINES}",
        )


def _literal_all_from_tree(tree: ast.Module) -> object:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return ast.literal_eval(node.value)
    return None


def _validate_public_surface() -> None:
    expected_all = {
        "documentation_intent_parser.py": [
            "DEFAULT_DOCUMENTATION_GLOB_PATTERNS",
            "parse_documentation_intent",
        ],
        "packaging_metadata_parser.py": [
            "DEFAULT_PACKAGING_FILE_PATTERNS",
            "parse_packaging_metadata",
        ],
    }
    for relative_path in TARGET_MODULES:
        tree = ast.parse(_read_text(relative_path))
        all_value = _literal_all_from_tree(tree)
        _assert(all_value == expected_all[Path(relative_path).name], f"Unexpected __all__ in {relative_path}")

    for module_name in HELPER_MODULES:
        module_path = PROJECT_ROOT / (module_name.replace(".", "/") + ".py")
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        found_empty_all = False
        for node in tree.body:
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if node.target.id == "__all__" and isinstance(node.value, ast.List) and len(node.value.elts) == 0:
                    found_empty_all = True
        _assert(found_empty_all, f"Helper module must declare empty __all__: {module_name}")


def _import_public_paths() -> None:
    import importlib

    for module_name in PUBLIC_MODULES + HELPER_MODULES:
        importlib.import_module(module_name)

    doc_module = importlib.import_module(PUBLIC_MODULES[0])
    pkg_module = importlib.import_module(PUBLIC_MODULES[1])
    _assert(hasattr(doc_module, "parse_documentation_intent"), "Documentation parser facade lost public parser")
    _assert(hasattr(pkg_module, "parse_packaging_metadata"), "Packaging parser facade lost public parser")


def _run_characterization_test() -> None:
    test_path = _project_file("tests/test_architecture_warning_cleanup_batch22_static_context_parser_large_module_refactor.py")
    spec = importlib.util.spec_from_file_location("batch22_static_context_parser_test", test_path)
    _assert(spec is not None and spec.loader is not None, "Could not load characterization test")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as temp_dir:
        module.test_static_context_parser_facades_keep_public_behavior(Path(temp_dir))


def _validate_architecture_targets() -> None:
    command = [
        sys.executable,
        str(PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
        "--root",
        str(PROJECT_ROOT),
        "--validate",
    ]
    completed = subprocess.run(command, cwd=str(PROJECT_ROOT), text=True, capture_output=True, check=False)
    output = completed.stdout + completed.stderr
    _assert(completed.returncode == 0, "Architecture validation command failed")
    _assert("Errors: 0" in output, "Architecture validation did not report Errors: 0")
    for target in TARGET_MODULES:
        _assert(
            f"MODULE_TOO_LARGE             {target}" not in output,
            f"Target module still reports MODULE_TOO_LARGE: {target}",
        )
    forbidden_target_markers = [
        "MISSING_PUBLIC_SURFACE_CONTROL",
        "PRIVATE_SYMBOL_EXPORTED",
        "PUBLIC_API_INSTABILITY",
        "DUPLICATE_PUBLIC_SYMBOL",
        "CROSS_BOX_PUBLIC_SYMBOL_COLLISION",
    ]
    touched_target_names = [Path(item).name for item in TOUCHED_FILES]
    for line in output.splitlines():
        if not line.startswith("WARNING") and not line.startswith("ERROR"):
            continue
        if not any(name in line for name in touched_target_names):
            continue
        for marker in forbidden_target_markers:
            _assert(marker not in line, f"Unexpected target architecture finding: {line}")


def main() -> int:
    _compile_touched_files()
    _validate_line_counts()
    _validate_public_surface()
    _import_public_paths()
    _run_characterization_test()
    _validate_architecture_targets()
    print(VALIDATION_OK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
