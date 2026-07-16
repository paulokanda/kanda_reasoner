# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_project_scan.py
"""Own source discovery, active-scope filtering, and project classification."""

from __future__ import annotations

import ast
import fnmatch
import importlib.util
import os
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .workflow_constants import (
    BACKUP_DIR_NAMES,
    DEFAULT_EXCLUDE_DIRS,
    DEPRECATED_DIR_NAMES,
    ENTRY_FILENAMES,
    GENERATED_DIR_NAMES,
    GUI_IMPORT_MARKERS,
    HARD_EXCLUDE_DIRS,
    SEMANTIC_EXCLUDE_DIR_PREFIXES,
    SEMANTIC_EXCLUDE_DIR_SUFFIXES,
    TEMPORARY_DIR_NAMES,
    VALIDATION_ONLY_FILE_PATTERNS,
    VALIDATION_ONLY_TOP_LEVEL_DIRS,
)
from .workflow_io import load_ignore_rules, read_text, utc_now_iso

__all__ = [
    "scan_project",
]

_CATEGORY_ACTIVE = "active_source"
_CATEGORY_TEST = "test_source"
_CATEGORY_VALIDATION = "validation_only"


def _matches_name(name: str, patterns: Iterable[str]) -> bool:
    """Return whether a case-insensitive filename matches any pattern."""
    folded = name.casefold()
    return any(
        fnmatch.fnmatchcase(folded, str(pattern).casefold())
        for pattern in patterns
    )


def _directory_exclusion_reason(
    dir_name: str,
    ignore_folders: list[str] | None = None,
) -> str | None:
    """Return the reason a directory must be pruned from discovery."""
    folded = dir_name.casefold()

    if folded in HARD_EXCLUDE_DIRS:
        return "infrastructure"

    if ignore_folders and _matches_name(dir_name, ignore_folders):
        return "user_ignored"

    if folded in DEPRECATED_DIR_NAMES:
        return "deprecated"
    if folded in BACKUP_DIR_NAMES:
        return "backup"
    if folded in TEMPORARY_DIR_NAMES:
        return "temporary"
    if folded in GENERATED_DIR_NAMES:
        return "generated"

    if any(folded.startswith(prefix) for prefix in SEMANTIC_EXCLUDE_DIR_PREFIXES):
        return "backup"
    if folded.endswith("_deprecated"):
        return "deprecated"
    if folded.endswith("_delete_after_daily_work"):
        return "temporary"
    if folded.endswith("_show_project_to_ai"):
        return "project_support"
    if any(folded.endswith(suffix) for suffix in SEMANTIC_EXCLUDE_DIR_SUFFIXES):
        return "generated"

    if folded in DEFAULT_EXCLUDE_DIRS:
        return "excluded"
    return None


def should_skip_dir(
    dir_name: str,
    ignore_folders: list[str] | None = None,
) -> bool:
    """Return whether a directory should be pruned during traversal."""
    return _directory_exclusion_reason(dir_name, ignore_folders) is not None


def iter_python_files(
    root: Path,
    ignore_folders: list[str],
    ignore_files: list[str],
    ignore_extensions: list[str],
    excluded_directory_counts: Counter[str] | None = None,
) -> Iterable[Path]:
    """Yield scanner-visible Python files while pruning excluded directories."""
    normalized_extensions = {str(value).casefold() for value in ignore_extensions}

    for dirpath, dirnames, filenames in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        kept_directories: list[str] = []
        for dir_name in dirnames:
            reason = _directory_exclusion_reason(dir_name, ignore_folders)
            if reason is None:
                kept_directories.append(dir_name)
            elif excluded_directory_counts is not None:
                excluded_directory_counts[reason] += 1
        dirnames[:] = kept_directories

        path_obj = Path(dirpath)
        for filename in filenames:
            if not filename.casefold().endswith(".py"):
                continue
            if _matches_name(filename, ignore_files):
                continue
            if Path(filename).suffix.casefold() in normalized_extensions:
                continue
            yield path_obj / filename


def _is_main_guard_test(node: ast.AST) -> bool:
    """Return whether an AST expression compares __name__ with __main__."""
    if not isinstance(node, ast.Compare) or len(node.ops) != 1:
        return False
    if not isinstance(node.ops[0], ast.Eq) or len(node.comparators) != 1:
        return False

    left = node.left
    right = node.comparators[0]
    pairs = ((left, right), (right, left))
    return any(
        isinstance(name_node, ast.Name)
        and name_node.id == "__name__"
        and isinstance(value_node, ast.Constant)
        and value_node.value == "__main__"
        for name_node, value_node in pairs
    )


def _source_signals(text: str) -> tuple[bool, bool]:
    """Return real AST-backed main-guard and GUI-import signals."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False, False

    has_main = any(
        isinstance(node, ast.If) and _is_main_guard_test(node.test)
        for node in ast.walk(tree)
    )

    gui_roots = {marker.casefold() for marker in GUI_IMPORT_MARKERS}
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(
                alias.name.split(".", 1)[0].casefold()
                for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0].casefold())
    return has_main, bool(gui_roots & imported_roots)


def has_main_guard(text: str) -> bool:
    """Return whether source text contains a real AST main guard."""
    return _source_signals(text)[0]


def has_gui_marker(text: str) -> bool:
    """Return whether source text contains a real supported GUI import."""
    return _source_signals(text)[1]


def is_test_path(path: Path) -> bool:
    """Return whether a path is conventional Python test source."""
    parts = {part.casefold() for part in path.parts}
    name = path.name.casefold()
    return (
        "tests" in parts
        or "test" in parts
        or name.startswith("test_")
        or name.endswith("_test.py")
    )


def _is_validation_only_file(root: Path, path: Path) -> bool:
    """Return whether a file is maintained validation tooling, not app source."""
    relative = path.relative_to(root)
    folded_parts = tuple(part.casefold() for part in relative.parts)
    filename = path.name.casefold()

    if fnmatch.fnmatchcase(filename, "*_validate_manifests.py"):
        return True

    tooling_path = any(
        part in VALIDATION_ONLY_TOP_LEVEL_DIRS
        for part in folded_parts[:-1]
    )
    if not tooling_path:
        return False
    return any(
        fnmatch.fnmatchcase(filename, pattern.casefold())
        for pattern in VALIDATION_ONLY_FILE_PATTERNS
    )


def _classify_python_path(root: Path, path: Path) -> str:
    """Classify a scanner-visible Python file by operational disposition."""
    if _is_validation_only_file(root, path):
        return _CATEGORY_VALIDATION
    if is_test_path(path.relative_to(root)):
        return _CATEGORY_TEST
    return _CATEGORY_ACTIVE


def module_id_for_path(root: Path, path: Path) -> str | None:
    """Return the importable module identifier for a package-backed path."""
    rel = path.relative_to(root)
    if path.parent == root:
        return path.stem if path.name != "__init__.py" else None

    current = root
    for part in rel.parts[:-1]:
        current = current / part
        if not (current / "__init__.py").exists():
            return None

    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
        if not parts:
            return None
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def scan_project(root: Path) -> dict[str, Any]:
    """Scan active project source while retaining concise exclusion evidence."""
    ignore_folders, ignore_files, ignore_extensions = load_ignore_rules()
    excluded_directory_counts: Counter[str] = Counter()

    python_files: list[str] = []
    active_python_files: list[str] = []
    validation_files: list[str] = []
    gui_files: list[str] = []
    entry_files: list[str] = []
    test_files: list[str] = []
    test_dirs: set[str] = set()
    package_roots: set[str] = set()
    importable_modules: list[str] = []

    for path in iter_python_files(
        root,
        ignore_folders,
        ignore_files,
        ignore_extensions,
        excluded_directory_counts,
    ):
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        python_files.append(rel)
        category = _classify_python_path(root, path)

        if category == _CATEGORY_VALIDATION:
            validation_files.append(rel)
            continue

        if category == _CATEGORY_TEST:
            test_files.append(rel)
            if path.parent != root:
                test_dirs.add(path.parent.relative_to(root).as_posix())
            continue

        active_python_files.append(rel)
        try:
            text = read_text(path)
        except (OSError, UnicodeError):
            text = ""

        has_main, has_gui = _source_signals(text)
        if has_gui:
            gui_files.append(rel)
        if path.name in ENTRY_FILENAMES or has_main:
            entry_files.append(rel)

        if path.name == "__init__.py":
            package_dir = path.parent.relative_to(root)
            if package_dir.parts:
                package_roots.add(".".join(package_dir.parts))

        module_id = module_id_for_path(root, path)
        if module_id:
            importable_modules.append(module_id)

    pytest_files = [
        name
        for name in ("pytest.ini", "conftest.py", "tox.ini", "pyproject.toml")
        if (root / name).exists()
    ]

    return {
        "project_root": str(root),
        "generated_at_utc": utc_now_iso(),
        "python_file_count": len(python_files),
        "active_python_file_count": len(active_python_files),
        "validation_only_file_count": len(validation_files),
        "test_python_file_count": len(test_files),
        "excluded_directory_counts": dict(sorted(excluded_directory_counts.items())),
        "python_files": sorted(python_files),
        "active_python_files": sorted(active_python_files),
        "validation_files": sorted(validation_files),
        "package_roots": sorted(package_roots),
        "entry_files": sorted(dict.fromkeys(entry_files)),
        "gui_files": sorted(dict.fromkeys(gui_files)),
        "test_files": sorted(test_files),
        "test_dirs": sorted(test_dirs),
        "pytest_files": pytest_files,
        "importable_modules": sorted(dict.fromkeys(importable_modules)),
    }


def pytest_available() -> bool:
    """Return whether pytest is importable in the current interpreter."""
    return importlib.util.find_spec("pytest") is not None
