# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_gui_validate_manifests.py
"""Validate the workflow GUI helper manifest contract."""

from __future__ import annotations

import ast
import json
from pathlib import Path

__all__ = [
    "main",
    "validate_manifest",
]

ROOT = Path(__file__).resolve().parents[2]
_STAGED_PACKAGE_DIR = "_".join(("ask", "ai", "project", "reasoner"))
ORIGIN = Path(_STAGED_PACKAGE_DIR) / "manage_workflows" / "manage_workflows_gui.py"
MANIFEST = Path(_STAGED_PACKAGE_DIR) / "manage_workflows" / "manage_workflows_gui_help.json"
HELP_FOLDER = Path(_STAGED_PACKAGE_DIR) / "manage_workflows" / "manage_workflows_gui_help"


def _extract_all(path: Path) -> list[str]:
    """Support extract all behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        if not isinstance(node.value, ast.List):
            return []
        result: list[str] = []
        for item in node.value.elts:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                result.append(item.value)
        return result
    return []


def validate_manifest(root: Path = ROOT) -> list[str]:
    """Validate the manifest.
    
    Parameters
    ----------
    root : Path, optional
        The root path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    errors: list[str] = []
    manifest_path = root / MANIFEST
    help_path = root / HELP_FOLDER
    origin_path = root / ORIGIN

    if not origin_path.exists():
        errors.append("Missing origin: " + str(ORIGIN))
    if not help_path.exists():
        errors.append("Missing helper folder: " + str(HELP_FOLDER))
    if not manifest_path.exists():
        errors.append("Missing manifest: " + str(MANIFEST))
        return errors

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = sorted(data.get("exports", []))

    actual: list[str] = []
    for helper_name in sorted(data.get("helpers", {})):
        helper_path = help_path / helper_name
        if not helper_path.exists():
            errors.append("Missing helper: " + helper_name)
            continue
        actual.extend(_extract_all(helper_path))

    if sorted(actual) != expected:
        errors.append("Helper exports do not match manifest exports")

    return errors


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    errors = validate_manifest()
    if errors:
        for error in errors:
            print(error)
        return 1
    print("workflow GUI helper manifest ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
