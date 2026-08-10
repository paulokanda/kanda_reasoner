# project-path: scripts/repair_architecture_warning_cleanup_batch20_runner_help_public_ownership_v1.py
"""Repair Batch 19 runner-help duplicate public ownership.

Batch 19 exposed duplicate public-symbol ownership in the
reasoner_tools_shell.runner_help zip-json split helper family. This repair keeps
zip_json_files_private_impl.py as the compatibility/public owner and makes the
split private implementation modules implementation-only by setting
``__all__ = []``.

The script is AST-only and py_compile-based. It must not execute target module
source.
"""

from __future__ import annotations

import ast
import py_compile
import warnings
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch20-runner-help-public-ownership-repair-v1"

RUNNER_HELP_PREFIX = "kanda_reasoner_app.reasoner_tools_shell.runner_help"
IMPLEMENTATION_ONLY_MODULES = (
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_state_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_process_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_publish_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_paths_private_impl.py",
)
FACADE_OWNER_MODULE = "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py"

__all__ = ["main"]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _module_name_for_relative(relative: str) -> str:
    return relative.removesuffix(".py").replace("/", ".")


def _iter_python_files(project_root: Path) -> list[Path]:
    ignored_parts = {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "project_freeze_after_update",
        "project_error_memory",
        "snippets",
        ".project_reference",
        "project_reference",
        "legacy_physical_package_archive",
    }
    files: list[Path] = []
    for path in project_root.rglob("*.py"):
        try:
            relative_parts = set(path.relative_to(project_root).parts)
        except ValueError:
            continue
        if relative_parts & ignored_parts:
            continue
        files.append(path)
    return files


def _has_star_import_from_targets(project_root: Path) -> list[str]:
    target_modules = {_module_name_for_relative(relative) for relative in IMPLEMENTATION_ONLY_MODULES}
    short_names = {module.rsplit(".", 1)[-1] for module in target_modules}
    hits: list[str] = []

    for path in _iter_python_files(project_root):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                tree = ast.parse(_read_text(path), filename=str(path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if not any(alias.name == "*" for alias in node.names):
                continue
            module = node.module or ""
            if module in target_modules or module in short_names:
                hits.append(f"{path.relative_to(project_root).as_posix()}:{node.lineno}: from {module} import *")
    return hits


def _empty_dunder_all_assignment() -> str:
    return "__all__ = []\n"


def _find_dunder_all_assignment(tree: ast.Module) -> ast.Assign | ast.AnnAssign | None:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return node
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__":
                return node
    return None


def _insertion_line_for_dunder_all(tree: ast.Module) -> int:
    insert_after = 0
    body = list(tree.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant):
        if isinstance(body[0].value.value, str):
            insert_after = int(getattr(body[0], "end_lineno", body[0].lineno))
    for node in body:
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            insert_after = max(insert_after, int(getattr(node, "end_lineno", node.lineno)))
    return insert_after


def _literal_dunder_all(path: Path) -> list[str] | None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(_read_text(path), filename=str(path))
    node = _find_dunder_all_assignment(tree)
    if node is None:
        return None
    value_node = node.value if isinstance(node, (ast.Assign, ast.AnnAssign)) else None
    value = ast.literal_eval(value_node)
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{path}: __all__ must be a literal list/tuple of strings")
    return list(value)


def _force_empty_dunder_all(path: Path) -> bool:
    text = _read_text(path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(text, filename=str(path))
    current = _literal_dunder_all(path)
    if current == []:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            py_compile.compile(str(path), doraise=True)
        return False

    lines = text.splitlines(keepends=True)
    node = _find_dunder_all_assignment(tree)
    assignment = _empty_dunder_all_assignment()

    if node is None:
        insertion_line = _insertion_line_for_dunder_all(tree)
        lines.insert(insertion_line, assignment)
    else:
        start = int(node.lineno) - 1
        end = int(getattr(node, "end_lineno", node.lineno))
        lines[start:end] = [assignment]

    new_text = "".join(lines)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        ast.parse(new_text, filename=str(path))
    _write_text(path, new_text)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        py_compile.compile(str(path), doraise=True)
    return True


def main() -> int:
    project_root = _project_root()

    star_imports = _has_star_import_from_targets(project_root)
    if star_imports:
        print("REFUSING REPAIR: star imports from implementation-only targets were found.")
        for hit in star_imports:
            print(f" - {hit}")
        return 2

    changed: list[str] = []
    checked: list[str] = []

    for relative in IMPLEMENTATION_ONLY_MODULES:
        path = project_root / relative
        if not path.is_file():
            print(f"SKIP missing local split helper: {relative}")
            continue
        checked.append(relative)
        if _force_empty_dunder_all(path):
            changed.append(relative)

    facade_path = project_root / FACADE_OWNER_MODULE
    if facade_path.is_file():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            py_compile.compile(str(facade_path), doraise=True)

    print(f"REPAIR OK: {FEATURE_ID}")
    if checked:
        print("Implementation-only helper modules checked:")
        for relative in checked:
            print(f" - {relative}")
    else:
        print("No local split helper modules were present in this source snapshot.")
    if changed:
        print("Changed files:")
        for relative in changed:
            print(f" - {relative}")
    else:
        print("No changes needed; helper __all__ contracts already implementation-only or absent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
