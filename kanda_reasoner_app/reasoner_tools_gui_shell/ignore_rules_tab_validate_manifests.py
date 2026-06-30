# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab_validate_manifests.py
"""Validate the helper manifest for the ignore-rules tab."""

from __future__ import annotations

__all__ = [
    "main",
    "validate_manifest",
]

import ast
import json
from pathlib import Path


MANIFEST_NAME = "ignore_rules_tab_help.json"


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


def _literal_all(path: Path) -> list[str]:
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
    
    tree = ast.parse(_read_text(path))

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

        if value is None:
            continue

        if isinstance(value, (ast.List, ast.Tuple)):
            result = []
            for item in value.elts:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    result.append(item.value)
            return result

    return []


def validate_manifest(manifest_path: Path) -> list[str]:
    """Return manifest validation errors."""
    errors: list[str] = []
    data = json.loads(_read_text(manifest_path))
    package_dir = manifest_path.parent
    project_root = package_dir.parents[1]

    origin_value = data.get("origin", "")
    help_folder_value = data.get("help_folder", "")
    if not isinstance(origin_value, str) or not origin_value:
        errors.append("manifest missing origin")
    if not isinstance(help_folder_value, str) or not help_folder_value:
        errors.append("manifest missing help_folder")

    if origin_value and not (project_root / origin_value).exists():
        errors.append("origin does not exist: " + origin_value)

    helper_folder = project_root / help_folder_value
    if help_folder_value and not helper_folder.exists():
        errors.append("help_folder does not exist: " + help_folder_value)
        return errors

    helpers = data.get("helpers", {})
    if not isinstance(helpers, dict):
        errors.append("manifest helpers must be an object")
        return errors

    for helper_name, helper_info in helpers.items():
        helper_path = helper_folder / helper_name
        if not helper_path.exists():
            errors.append(helper_name + " missing helper file")
            continue

        expected_exports = helper_info.get("exports", [])
        actual_exports = _literal_all(helper_path)
        if expected_exports != actual_exports:
            errors.append(helper_name + " exports do not match __all__")

    return errors


def main() -> int:
    """Validate the ignore-rules helper manifest."""
    manifest_path = Path(__file__).with_name(MANIFEST_NAME)
    errors = validate_manifest(manifest_path)

    if errors:
        print("FAIL - " + str(manifest_path))
        for error in errors:
            print("  - " + error)
        return 1

    print("PASS - " + str(manifest_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
