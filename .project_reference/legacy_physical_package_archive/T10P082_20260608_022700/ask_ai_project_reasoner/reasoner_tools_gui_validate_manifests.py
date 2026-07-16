"""Validate the root Reasoner tools GUI shell helper manifest contract."""

from __future__ import annotations

import ast
import json
from pathlib import Path

__all__ = [
    "main",
    "validate_manifest",
]

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_PACKAGE = Path(__file__).resolve().parent.name
ORIGIN = Path("reasoner_tools_gui.py")
MANIFEST = Path(PRODUCT_PACKAGE) / "reasoner_tools_gui_shell.json"
HELP_FOLDER = Path(PRODUCT_PACKAGE) / "reasoner_tools_gui_shell"


def _extract_all(path: Path) -> list[str]:
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
    expected_origin = sorted(data.get("origin_all", []))

    actual: list[str] = []
    for helper_name in sorted(data.get("helpers", {})):
        helper_path = help_path / helper_name
        if not helper_path.exists():
            errors.append("Missing helper: " + helper_name)
            continue
        actual.extend(_extract_all(helper_path))

    if sorted(actual) != expected:
        errors.append("Helper exports do not match manifest exports")

    if origin_path.exists() and sorted(_extract_all(origin_path)) != expected_origin:
        errors.append("Origin exports do not match manifest origin_all")

    return errors


def main() -> int:
    errors = validate_manifest()
    if errors:
        for error in errors:
            print(error)
        return 1
    print("reasoner tools GUI shell helper manifest ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
