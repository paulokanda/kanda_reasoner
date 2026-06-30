#!/usr/bin/env python3
# project-path: kanda_reasoner_app/reasoner_context_collector/collector_runtime_scenarios_validate_manifests.py
"""Validate collector_runtime_scenarios helper split."""

from __future__ import annotations

import ast
import json
import py_compile
from pathlib import Path

PUBLIC_ALL = ['build_runtime_scenario_hotspots', 'build_runtime_scenario_index', 'build_runtime_scenario_summary']


def read_text(path: Path) -> str:
    """Return the text.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return path.read_text(encoding="utf-8", errors="replace")


def fail(message: str) -> int:
    """Support fail behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    
    Returns
    -------
    int
        The integer result.
    """
    
    print(f"FAIL {message}")
    return 1


def literal_all(source: str) -> list[str]:
    """Support literal all behavior.
    
    Parameters
    ----------
    source : str
        The source value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = [getattr(target, "id", None) for target in node.targets]
            if "__all__" in targets:
                value = ast.literal_eval(node.value)
                if isinstance(value, list):
                    return [str(item) for item in value]
    return []


def has_star_import(source: str) -> bool:
    """Return whether star import.
    
    Parameters
    ----------
    source : str
        The source value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    return True
    return False


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    base = Path(__file__).resolve().parent
    root = base / "collector_runtime_scenarios.py"
    helper_dir = base / "collector_runtime_scenarios_help"
    manifest = base / "collector_runtime_scenarios_help.json"
    required = [
        root,
        helper_dir / "__init__.py",
        helper_dir / "normalization.py",
        helper_dir / "event_classification.py",
        helper_dir / "hotspots.py",
        manifest,
    ]
    for path in required:
        if not path.exists():
            return fail(f"missing required file: {path}")
    for path in required:
        if path.suffix == ".py":
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                return fail(f"py_compile failed for {path}: {exc}")
            source = read_text(path)
            if has_star_import(source):
                return fail(f"star import found in {path}")
    root_source = read_text(root)
    if len(root_source.splitlines()) >= 500:
        return fail("root file has 500 or more lines")
    if literal_all(root_source) != PUBLIC_ALL:
        return fail(f"root __all__ mismatch: {literal_all(root_source)}")
    helper_init_all = literal_all(read_text(helper_dir / "__init__.py"))
    if helper_init_all != []:
        return fail(f"helper package __all__ should be empty: {helper_init_all}")
    data = json.loads(read_text(manifest))
    if data.get("public_origin_exports") != PUBLIC_ALL:
        return fail("manifest public_origin_exports mismatch")
    print("PASS collector_runtime_scenarios helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
