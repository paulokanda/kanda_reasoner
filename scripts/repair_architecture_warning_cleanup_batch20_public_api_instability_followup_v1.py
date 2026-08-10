# project-path: scripts/repair_architecture_warning_cleanup_batch20_public_api_instability_followup_v1.py
"""Repair Batch 20 runner-help public API instability follow-up.

The prior Batch 20 repair made the zip-json split helpers implementation-only by
setting ``__all__ = []``. That removed duplicate public-symbol ownership but made
``zip_json_files_private_impl.py`` re-export symbols from sources that explicitly
declared those symbols non-public, which the architecture validator reports as
PUBLIC_API_INSTABILITY errors.

This follow-up removes the local split-helper ``__all__`` declarations instead of
emptying them. The compatibility facade remains the public owner, while the split
private helpers no longer assert an explicit contradictory public API contract.

The script uses AST parsing and py_compile only. It must not execute target module
source.
"""

from __future__ import annotations

import ast
import py_compile
import warnings
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch20-public-api-instability-followup-v1"

TARGET_HELPERS = (
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
    target_modules = {_module_name_for_relative(relative) for relative in TARGET_HELPERS}
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


def _find_top_level_dunder_all_assignment(tree: ast.Module) -> ast.Assign | ast.AnnAssign | None:
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


def _literal_dunder_all(path: Path) -> list[str] | None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(_read_text(path), filename=str(path))
    node = _find_top_level_dunder_all_assignment(tree)
    if node is None:
        return None
    value_node = node.value if isinstance(node, (ast.Assign, ast.AnnAssign)) else None
    value = ast.literal_eval(value_node)
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{path}: __all__ must be a literal list/tuple of strings before repair")
    return list(value)


def _remove_empty_dunder_all(path: Path) -> bool:
    text = _read_text(path)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(text, filename=str(path))
    node = _find_top_level_dunder_all_assignment(tree)
    if node is None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            py_compile.compile(str(path), doraise=True)
        return False

    current = _literal_dunder_all(path)
    if current != []:
        raise ValueError(
            f"{path}: refusing to remove non-empty __all__={current!r}; expected the prior Batch 20 empty helper contract"
        )

    lines = text.splitlines(keepends=True)
    start = int(node.lineno) - 1
    end = int(getattr(node, "end_lineno", node.lineno))
    del lines[start:end]
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
        print("REFUSING REPAIR: star imports from Batch 20 helper targets were found.")
        for hit in star_imports:
            print(f" - {hit}")
        return 2

    checked: list[str] = []
    changed: list[str] = []

    for relative in TARGET_HELPERS:
        path = project_root / relative
        if not path.is_file():
            print(f"SKIP missing local split helper: {relative}")
            continue
        checked.append(relative)
        if _remove_empty_dunder_all(path):
            changed.append(relative)

    facade_path = project_root / FACADE_OWNER_MODULE
    if facade_path.is_file():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            py_compile.compile(str(facade_path), doraise=True)

    print(f"REPAIR OK: {FEATURE_ID}")
    if checked:
        print("Batch 20 helper modules checked:")
        for relative in checked:
            print(f" - {relative}")
    else:
        print("No local Batch 20 helper modules were present in this source snapshot.")
    if changed:
        print("Removed empty helper __all__ declarations from:")
        for relative in changed:
            print(f" - {relative}")
    else:
        print("No changes needed; helper __all__ declarations were already absent or helpers were absent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
