"""Validate helper manifest contract for this helper group."""

from __future__ import annotations

__all__ = [
    "main",
    "validate_manifest",
]

import ast
import json
from pathlib import Path


MANIFEST_NAME = "project_profile_help.json"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _literal_all(path: Path) -> list[str]:
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
    errors: list[str] = []

    data = json.loads(_read_text(manifest_path))
    root = manifest_path.parents[2]

    helper_folder_value = data.get("help_folder", "")
    if not isinstance(helper_folder_value, str) or not helper_folder_value:
        errors.append("manifest missing help_folder")
        return errors

    helper_folder = root / helper_folder_value
    if not helper_folder.exists():
        errors.append("help_folder does not exist: " + helper_folder_value)
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
