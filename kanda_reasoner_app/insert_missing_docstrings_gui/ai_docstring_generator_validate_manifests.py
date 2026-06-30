# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_validate_manifests.py
"""Validate the AI docstring generator helper manifest."""

from __future__ import annotations

__all__ = [
    "main",
    "validate_manifest",
]

import ast
import json
from pathlib import Path


MANIFEST_NAME = "ai_docstring_generator_help.json"
EXPECTED_ROOT_ALL = [
    "AIDocstringGenerator",
    "GenerationResult",
    "GenerationStats",
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


def literal_all(path: Path) -> list[str]:
    """Support literal all behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    list[str]
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
            output: list[str] = []
            for item in value.elts:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    output.append(item.value)
            return output
    return []


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


def validate_manifest(manifest_path: Path) -> list[str]:
    """Validate the manifest.
    
    Parameters
    ----------
    manifest_path : Path
        The manifest path value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    errors: list[str] = []
    package_dir = manifest_path.parent
    project_root = package_dir.parents[1]

    try:
        data = json.loads(read_text(manifest_path))
    except Exception as exc:
        return ["manifest is not valid JSON: " + str(exc)]

    origin_rel = data.get("origin", "")
    helper_rel = data.get("help_folder", "")
    if not isinstance(origin_rel, str) or not origin_rel:
        errors.append("manifest missing origin")
    if not isinstance(helper_rel, str) or not helper_rel:
        errors.append("manifest missing help_folder")

    origin = project_root / origin_rel
    helper_dir = project_root / helper_rel

    if not origin.exists():
        errors.append("origin does not exist: " + str(origin))
    else:
        if literal_all(origin) != EXPECTED_ROOT_ALL:
            errors.append("origin __all__ does not match expected public API")
        if has_star_import(origin):
            errors.append("origin has a star import")

    if not helper_dir.exists():
        errors.append("helper folder does not exist: " + str(helper_dir))
        return errors

    helpers = data.get("helpers", {})
    if not isinstance(helpers, dict):
        errors.append("manifest helpers must be an object")
        return errors

    for helper_name, helper_info in helpers.items():
        helper_path = helper_dir / helper_name
        if not helper_path.exists():
            errors.append("missing helper file: " + helper_name)
            continue
        if has_star_import(helper_path):
            errors.append("helper has a star import: " + helper_name)
        expected_exports = helper_info.get("exports", [])
        if not isinstance(expected_exports, list):
            errors.append("helper exports must be a list: " + helper_name)
            continue
        actual_exports = literal_all(helper_path)
        if actual_exports != expected_exports:
            errors.append("helper exports drift: " + helper_name)

    return errors


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    manifest_path = Path(__file__).with_name(MANIFEST_NAME)
    errors = validate_manifest(manifest_path)
    if errors:
        print("FAIL ai_docstring_generator helper manifest")
        for error in errors:
            print("  - " + error)
        return 1
    print("PASS ai_docstring_generator helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
