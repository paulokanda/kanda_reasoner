# project-path: tools/validate_project_intelligence_symbol_indexer_cohesive_split_v1.py
"""Validate the cohesive AST visitor split for Project Intelligence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

__all__ = ["main"]


FEATURE_ID = "project-intelligence-symbol-indexer-cohesive-ast-visitor-split-v1"

FACADE_REL = Path(
    "kanda_reasoner_app/project_intelligence/symbol_indexer.py"
)
HELPER_REL = Path(
    "kanda_reasoner_app/project_intelligence/_symbol_index_ast_visitor.py"
)
SELF_REL = Path(
    "tools/validate_project_intelligence_symbol_indexer_cohesive_split_v1.py"
)

EXPECTED_HASHES = {
    FACADE_REL.as_posix(): "ef1bd67f60cdb75916e39b49991cb91cb138c721065a9dca8e779b43922e69f0",
    HELPER_REL.as_posix(): "3eea7fe67269a88e92cfe06ce0b1656dbf999780a876d73ef1553bc4348031ca",
}

EXPECTED_FACADE_CLASSES = {
    "SymbolIndexResult": ("to_dict", "to_json_text"),
    "ProjectSymbolIndexer": (
        "run_scan",
        "to_markdown",
        "_iter_selected_files",
        "_normalize_context_filter",
        "_relative_path",
        "_file_summary",
        "_build_findings",
    ),
}

EXPECTED_VISITOR_METHODS = (
    "__init__",
    "visit_Import",
    "visit_ImportFrom",
    "visit_ClassDef",
    "visit_FunctionDef",
    "visit_AsyncFunctionDef",
    "_current_parent_name",
    "_function_type",
    "_visit_function",
)

DYNAMIC_CALL_NAMES = {
    "eval",
    "exec",
    "getattr",
    "setattr",
    "delattr",
    "globals",
    "locals",
    "__import__",
}


def fail(message: str) -> None:
    """Raise one deterministic validation failure."""
    raise AssertionError(message)


def read_text(root: Path, relative: Path) -> str:
    """Read one required project file as strict UTF-8 text."""
    path = root / relative
    if not path.is_file():
        fail("MISSING_REQUIRED_FILE: " + relative.as_posix())
    return path.read_text(encoding="utf-8-sig", errors="strict")


def sha256_file(path: Path) -> str:
    """Return one lowercase SHA-256 digest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def dotted_name(node: ast.AST) -> str:
    """Return a dotted name for a Name or Attribute AST node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return parent + "." + node.attr if parent else node.attr
    return ""


def class_methods(tree: ast.Module, class_name: str) -> tuple[str, ...]:
    """Return methods declared directly by one top-level class."""
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return tuple(
                child.name
                for child in node.body
                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                )
            )
    fail("MISSING_CLASS: " + class_name)
    return ()


def validate_source_identity(root: Path) -> None:
    """Require the exact reviewed candidate bytes."""
    for relative_text, expected in EXPECTED_HASHES.items():
        path = root / Path(relative_text)
        actual = sha256_file(path)
        if actual != expected:
            fail(
                "SOURCE_IDENTITY_DRIFT: "
                + relative_text
                + ":"
                + actual
            )
    print("SOURCE_IDENTITY_GUARD: PASS")


def validate_line_law(root: Path) -> None:
    """Require every touched permanent Python file to remain 101-499 lines."""
    counts: dict[str, int] = {}
    for relative in (FACADE_REL, HELPER_REL, SELF_REL):
        text = read_text(root, relative)
        count = len(text.splitlines())
        counts[relative.as_posix()] = count
        if not 101 <= count <= 499:
            fail(
                "LINE_LAW_101_499_VIOLATION: "
                + relative.as_posix()
                + ":"
                + str(count)
            )
        if any(ord(character) > 127 for character in text):
            fail("NON_ASCII_SOURCE: " + relative.as_posix())
        ast.parse(text, filename=str(root / relative))
    if counts[FACADE_REL.as_posix()] >= 500:
        fail("MODULE_TOO_LARGE_REMAINS: " + str(counts))
    print("LINE_LAW_101_499_FITNESS: PASS")
    print("MODULE_TOO_LARGE_SYMBOL_INDEXER_RESOLVED: PASS")


def validate_structure(root: Path) -> None:
    """Validate facade ownership and one-way helper dependency direction."""
    facade_text = read_text(root, FACADE_REL)
    helper_text = read_text(root, HELPER_REL)
    facade_tree = ast.parse(facade_text, filename=str(root / FACADE_REL))
    helper_tree = ast.parse(helper_text, filename=str(root / HELPER_REL))

    facade_defined = {
        node.name
        for node in facade_tree.body
        if isinstance(node, ast.ClassDef)
    }
    if "_SymbolVisitor" in facade_defined:
        fail("VISITOR_IMPLEMENTATION_STILL_IN_FACADE")

    imported_visitor = False
    for node in facade_tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module != "_symbol_index_ast_visitor":
            continue
        imported_visitor = any(
            alias.name == "_SymbolVisitor"
            for alias in node.names
        )
    if not imported_visitor:
        fail("FACADE_VISITOR_IMPORT_MISSING")

    helper_import_modules = {
        str(node.module or "")
        for node in helper_tree.body
        if isinstance(node, ast.ImportFrom)
    }
    if "symbol_indexer" in helper_import_modules:
        fail("HELPER_TO_FACADE_BACK_REFERENCE")

    dynamic_calls = {
        dotted_name(node.func)
        for node in ast.walk(helper_tree)
        if isinstance(node, ast.Call)
        and dotted_name(node.func) in DYNAMIC_CALL_NAMES
    }
    if dynamic_calls:
        fail("HELPER_DYNAMIC_CALLS: " + repr(sorted(dynamic_calls)))

    for class_name, expected_methods in EXPECTED_FACADE_CLASSES.items():
        actual_methods = class_methods(facade_tree, class_name)
        if actual_methods != expected_methods:
            fail(
                "PUBLIC_CLASS_METHOD_DRIFT: "
                + class_name
                + ":"
                + repr(actual_methods)
            )

    visitor_methods = class_methods(helper_tree, "_SymbolVisitor")
    if visitor_methods != EXPECTED_VISITOR_METHODS:
        fail("VISITOR_METHOD_DRIFT: " + repr(visitor_methods))

    print("PUBLIC_API_PRESERVATION: PASS")
    print("PRIVATE_VISITOR_COMPATIBILITY_IMPORT: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")


def fixture_source() -> str:
    """Return the behavior-equivalence fixture source."""
    return (
        "import os as operating_system\n"
        "from pkg.sub import thing as alias\n\n"
        "def documented():\n"
        "    \"\"\"Documented function.\"\"\"\n"
        "    def nested():\n"
        "        return 1\n"
        "    return nested()\n\n"
        "def undocumented():\n"
        "    return 2\n\n"
        "class Sample:\n"
        "    \"\"\"Sample class.\"\"\"\n"
        "    def method(self):\n"
        "        return 3\n\n"
        "    async def async_method(self):\n"
        "        return 4\n\n"
        "async def async_top():\n"
        "    return 5\n"
    )


def path_snapshot(root: Path) -> list[str]:
    """Return a deterministic relative path snapshot."""
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
    )


def validate_runtime_fixture(root: Path) -> None:
    """Run the preserved behavior contract against a disposable project."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from kanda_reasoner_app.project_intelligence import (
        ProjectSymbolIndexer,
        SymbolIndexResult,
    )
    from kanda_reasoner_app.project_intelligence.symbol_indexer import (
        _SymbolVisitor,
    )

    if _SymbolVisitor.__module__ != (
        "kanda_reasoner_app.project_intelligence._symbol_index_ast_visitor"
    ):
        fail("VISITOR_COMPATIBILITY_IMPORT_MODULE_DRIFT")

    with tempfile.TemporaryDirectory() as temp_text:
        fixture_root = Path(temp_text) / "fixture_project"
        fixture_root.mkdir()
        (fixture_root / "sample_module.py").write_text(
            fixture_source(),
            encoding="utf-8",
            newline="\n",
        )
        (fixture_root / "bad_syntax.py").write_text(
            "def broken(:\n    pass\n",
            encoding="utf-8",
            newline="\n",
        )
        excluded = fixture_root / "__pycache__"
        excluded.mkdir()
        (excluded / "ignored.py").write_text(
            "def must_not_appear():\n    return 0\n",
            encoding="utf-8",
            newline="\n",
        )
        hidden = fixture_root / ".venv"
        hidden.mkdir()
        (hidden / "ignored_too.py").write_text(
            "class MustNotAppear:\n    pass\n",
            encoding="utf-8",
            newline="\n",
        )

        before = path_snapshot(fixture_root)
        indexer = ProjectSymbolIndexer()
        result = indexer.run_scan(fixture_root)
        after = path_snapshot(fixture_root)

        if before != after:
            fail("TARGET_PROJECT_WAS_MUTATED")
        if not isinstance(result, SymbolIndexResult):
            fail("RESULT_TYPE_DRIFT")

        actual_symbols = {
            (
                item.name,
                item.symbol_type,
                item.parent_name,
                item.has_docstring,
                item.is_async,
            )
            for item in result.symbols
        }
        expected_symbols = {
            ("documented", "function", "", True, False),
            ("nested", "nested_function", "documented", False, False),
            ("undocumented", "function", "", False, False),
            ("Sample", "class", "", True, False),
            ("method", "method", "Sample", False, False),
            ("async_method", "async_method", "Sample", False, True),
            ("async_top", "async_function", "", False, True),
        }
        if actual_symbols != expected_symbols:
            fail("SYMBOL_BEHAVIOR_DRIFT: " + repr(sorted(actual_symbols)))

        actual_imports = {
            (
                item.module,
                item.imported_name,
                item.import_type,
            )
            for item in result.imports
        }
        expected_imports = {
            ("os", "operating_system", "import"),
            ("pkg.sub", "alias", "from_import"),
        }
        if actual_imports != expected_imports:
            fail("IMPORT_BEHAVIOR_DRIFT: " + repr(sorted(actual_imports)))

        if any("ignored" in item.file_path for item in result.symbols):
            fail("EXCLUDED_FOLDER_SYMBOL_LEAK")
        syntax_files = {
            item.file_path
            for item in result.files
            if item.syntax_error
        }
        if syntax_files != {"bad_syntax.py"}:
            fail("SYNTAX_ERROR_CONTRACT_DRIFT: " + repr(syntax_files))

        json.loads(result.to_json_text())
        markdown = indexer.to_markdown(result)
        required_markdown = (
            "Project Intelligence Symbol Indexer",
            "## Symbol summary",
            "This generated report is advisory evidence.",
        )
        for marker in required_markdown:
            if marker not in markdown:
                fail("MARKDOWN_CONTRACT_MISSING: " + marker)

    print("BEHAVIOR_EQUIVALENCE_FIXTURE: PASS")
    print("TARGET_READ_ONLY_BEHAVIOR: PASS")
    print("EXCLUSION_POLICY_REGRESSION: PASS")
    print("JSON_MARKDOWN_CONTRACT: PASS")


def validate_existing_test(root: Path) -> None:
    """Run the historical direct test when it is present in the project."""
    test_path = root / "tests" / "test_project_intelligence_symbol_indexer.py"
    if not test_path.is_file():
        print("LEGACY_SYMBOL_INDEXER_TEST: NOT_PRESENT")
        return
    result = subprocess.run(
        [sys.executable, str(test_path)],
        cwd=str(root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if output:
        print(output.rstrip())
    if result.returncode != 0:
        fail("LEGACY_SYMBOL_INDEXER_TEST_EXIT: " + str(result.returncode))
    for marker in (
        "VALIDATION OK: project-intelligence-symbol-indexer-v1",
        "STATUS: IN_SYNC",
    ):
        if marker not in output:
            fail("LEGACY_TEST_MARKER_MISSING: " + marker)
    print("LEGACY_SYMBOL_INDEXER_TEST: PASS")


def validate_ast_family(root: Path) -> None:
    """Require a fresh SAFE AST audit for both touched source modules."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    for relative in (FACADE_REL, HELPER_REL):
        result = run_large_module_split_audit(
            root,
            root / relative,
            classifier_mode="heuristic",
        )
        classification: dict[str, Any] = result.data[
            "refactor_safety_classification"
        ]
        if classification.get("label") != "SAFE REFACTORING":
            fail(
                "AST_SPLIT_NOT_SAFE: "
                + relative.as_posix()
                + ":"
                + repr(classification)
            )
        if classification.get("hard_blockers"):
            fail(
                "AST_SPLIT_HARD_BLOCKERS: "
                + relative.as_posix()
                + ":"
                + repr(classification.get("hard_blockers"))
            )
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_HARD_BLOCKERS: 0")


def main() -> int:
    """Run all focused split validations."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()

    validate_source_identity(root)
    validate_line_law(root)
    validate_structure(root)
    validate_runtime_fixture(root)
    validate_existing_test(root)
    validate_ast_family(root)

    print("SYMBOL_INDEXER_COHESIVE_AST_VISITOR_SPLIT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
