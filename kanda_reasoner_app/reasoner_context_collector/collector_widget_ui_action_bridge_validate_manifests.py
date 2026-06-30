# project-path: kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_validate_manifests.py
"""Validate collector widget UI action bridge helper extraction."""

from __future__ import annotations

import ast
import json
from pathlib import Path


EXPECTED_ROOT_ALL = [
    "build_widget_ui_action_bridge",
    "build_widget_ui_action_hotspots",
]

HELPER_FILES = [
    "normalization.py",
    "matching.py",
    "indexing.py",
]


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


def literal_all(path: Path) -> list[str] | None:
    """Support literal all behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    list[str] | None
        The list of values.
    """
    
    tree = ast.parse(read_text(path))
    for node in tree.body:
        value = None
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = node.value
                    break
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__":
                value = node.value
        if isinstance(value, (ast.List, ast.Tuple)):
            result: list[str] = []
            for item in value.elts:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    result.append(item.value)
            return result
    return None


def has_module_docstring(path: Path) -> bool:
    """Return whether module docstring.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    tree = ast.parse(read_text(path))
    return bool(ast.get_docstring(tree))


def has_star_import(path: Path) -> bool:
    """Return whether star import.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    tree = ast.parse(read_text(path))
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
    origin = base / "collector_widget_ui_action_bridge.py"
    helper_dir = base / "collector_widget_ui_action_bridge_help"
    manifest = base / "collector_widget_ui_action_bridge_help.json"
    errors: list[str] = []

    if not origin.exists():
        errors.append("Missing origin file: " + str(origin))
    else:
        if literal_all(origin) != EXPECTED_ROOT_ALL:
            errors.append("Unexpected root __all__ in origin")
        if has_star_import(origin):
            errors.append("Origin contains a star import")
        root_lines = len(read_text(origin).splitlines())
        if root_lines >= 500:
            errors.append("Origin still has 500 or more lines: " + str(root_lines))

    if not helper_dir.exists():
        errors.append("Missing helper directory: " + str(helper_dir))
    else:
        for filename in HELPER_FILES:
            path = helper_dir / filename
            if not path.exists():
                errors.append("Missing helper file: " + filename)
                continue
            if not has_module_docstring(path):
                errors.append("Missing module docstring: " + filename)
            if literal_all(path) != []:
                errors.append("Helper __all__ should be empty: " + filename)
            if has_star_import(path):
                errors.append("Helper contains a star import: " + filename)

    if manifest.exists():
        try:
            json.loads(read_text(manifest))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append("Manifest JSON parse failed: " + str(exc))

    if errors:
        print("FAIL collector_widget_ui_action_bridge helper manifest")
        for error in errors:
            print("  - " + error)
        return 1

    print("PASS collector_widget_ui_action_bridge helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
