# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_validate_manifests.py
"""Validate reasoner_tools_shell.runner helper manifest artifacts."""

from __future__ import annotations

import ast
import json
import py_compile
from pathlib import Path

__all__ = ["main"]

MAX_LINES = 499
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
ORIGIN = BASE / "runner.py"
HELP_DIR = BASE / "runner_help"
MANIFEST = BASE / "runner_help.json"


def _read_text(path: Path) -> str:
    """Support read text behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _line_count(path: Path) -> int:
    """Support line count behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    text = _read_text(path)
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    errors: list[str] = []
    for path, label in ((ORIGIN, "origin"), (HELP_DIR, "helper dir"), (MANIFEST, "manifest")):
        if not path.exists():
            errors.append("missing " + label + ": " + str(path))
    if errors:
        for error in errors:
            print("FAIL " + error)
        return 1
    try:
        data = json.loads(_read_text(MANIFEST))
    except json.JSONDecodeError as exc:
        print("FAIL invalid manifest JSON: " + str(exc))
        return 1
    helpers = data.get("helpers", {})
    if not isinstance(helpers, dict):
        print("FAIL manifest helpers must be an object")
        return 1
    for rel_name in sorted(helpers):
        helper_path = HELP_DIR / rel_name
        if not helper_path.exists():
            errors.append("missing helper file: " + str(helper_path))
            continue
        if helper_path.suffix == ".py":
            if _line_count(helper_path) > MAX_LINES:
                errors.append("helper file has 500 or more lines: " + str(helper_path))
            try:
                ast.parse(_read_text(helper_path), filename=str(helper_path))
                py_compile.compile(str(helper_path), doraise=True)
            except (SyntaxError, py_compile.PyCompileError) as exc:
                errors.append("helper compile/parse failed: " + str(helper_path) + " :: " + str(exc))
    if _line_count(ORIGIN) > MAX_LINES:
        errors.append("origin file has 500 or more lines: " + str(ORIGIN))
    try:
        py_compile.compile(str(ORIGIN), doraise=True)
    except py_compile.PyCompileError as exc:
        errors.append("origin compile failed: " + str(exc))
    if errors:
        for error in errors:
            print("FAIL " + error)
        return 1
    print("PASS runner helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
