# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_project_scan.py
"""Own source discovery and project classification."""

from __future__ import annotations

import argparse
import contextlib
import difflib
import fnmatch
import importlib.util
import io
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .workflow_constants import (
    DEFAULT_EXCLUDE_DIRS,
    ENTRY_FILENAMES,
    GUI_IMPORT_MARKERS,
)
from .workflow_io import (
    load_ignore_rules,
    read_text,
    utc_now_iso,
)

__all__ = [
    "scan_project",
]

def should_skip_dir(dir_name: str, ignore_folders: list[str] | None = None) -> bool:
    """Support should skip dir behavior.
    
    Parameters
    ----------
    dir_name : str
        The dir name value.
    ignore_folders : list[str] | None, optional
        The optional ignore folders value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if dir_name in DEFAULT_EXCLUDE_DIRS:
        return True
    if ignore_folders and dir_name in ignore_folders:
        return True
    return False

def iter_python_files(root: Path, ignore_folders: list[str], ignore_files: list[str], ignore_extensions: list[str]) -> Iterable[Path]:
    """Support iter python files behavior.
    
    Parameters
    ----------
    root : Path
        The root path.
    ignore_folders : list[str]
        The ignore folders value.
    ignore_files : list[str]
        The ignore files value.
    ignore_extensions : list[str]
        The ignore extensions value.
    
    Returns
    -------
    Iterable[Path]
        The sequence of values.
    """
    
    for dirpath, dirnames, filenames in os.walk(root):
        path_obj = Path(dirpath)
        dirnames[:] = [
            d for d in dirnames
            if not should_skip_dir(d, ignore_folders)
        ]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            # Check user ignore files (exact match or wildcard)
            if any(fnmatch.fnmatch(filename, pattern) for pattern in ignore_files):
                continue
            ext = Path(filename).suffix
            if ext and ext in ignore_extensions:
                continue
            rel_path = path_obj.relative_to(root)
            if any(part in ignore_folders for part in rel_path.parts):
                continue
            yield path_obj / filename

def has_main_guard(text: str) -> bool:
    """Return whether main guard.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return 'if __name__ == "__main__":' in text or "if __name__ == '__main__':" in text

def has_gui_marker(text: str) -> bool:
    """Return whether gui marker.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for marker in GUI_IMPORT_MARKERS:
        if f"import {marker}" in text or f"from {marker}" in text:
            return True
    return False

def is_test_path(path: Path) -> bool:
    """Return whether test path.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    return "tests" in parts or "test" in parts or name.startswith("test_") or name.endswith("_test.py")

def module_id_for_path(root: Path, path: Path) -> str | None:
    """Support module id for path behavior.
    
    Parameters
    ----------
    root : Path
        The root path.
    path : Path
        The file or folder path.
    
    Returns
    -------
    str | None
        The string result.
    """
    
    rel = path.relative_to(root)
    if path.parent == root:
        return path.stem if path.name != "__init__.py" else None

    parents = list(rel.parts[:-1])
    current = root
    for part in parents:
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
    """Scan the project.
    
    Parameters
    ----------
    root : Path
        The root path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    ignore_folders, ignore_files, ignore_extensions = load_ignore_rules()
    python_files: list[str] = []
    gui_files: list[str] = []
    entry_files: list[str] = []
    test_files: list[str] = []
    test_dirs: set[str] = set()
    package_roots: set[str] = set()
    importable_modules: list[str] = []

    for path in iter_python_files(root, ignore_folders, ignore_files, ignore_extensions):
        rel = str(path.relative_to(root)).replace("\\", "/")
        python_files.append(rel)

        try:
            text = read_text(path)
        except Exception:
            text = ""

        if has_gui_marker(text):
            gui_files.append(rel)

        if path.name in ENTRY_FILENAMES or has_main_guard(text):
            entry_files.append(rel)

        if is_test_path(path):
            test_files.append(rel)
            if path.parent != root:
                test_dirs.add(str(path.parent.relative_to(root)).replace("\\", "/"))

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

    discovered = {
        "project_root": str(root),
        "generated_at_utc": utc_now_iso(),
        "python_file_count": len(python_files),
        "python_files": sorted(python_files),
        "package_roots": sorted(package_roots),
        "entry_files": sorted(dict.fromkeys(entry_files)),
        "gui_files": sorted(dict.fromkeys(gui_files)),
        "test_files": sorted(test_files),
        "test_dirs": sorted(test_dirs),
        "pytest_files": pytest_files,
        "importable_modules": sorted(dict.fromkeys(importable_modules)),
    }
    return discovered

def pytest_available() -> bool:
    """Support pytest available behavior.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return importlib.util.find_spec("pytest") is not None
