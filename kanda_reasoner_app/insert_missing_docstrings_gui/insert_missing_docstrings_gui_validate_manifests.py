# kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_validate_manifests.py
"""Validate refactor manifests for insert_missing_docstrings_gui helpers."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_HEADER_FIELDS = (
    "MODULE ORIGIN",
    "MANIFEST",
    "HELP FOLDER",
    "PURPOSE",
    "EXPORTS",
    "DEPENDS ON",
    "REFACTOR DATE",
)


def _literal_all(path: Path) -> list[str] | None:
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
    
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return list(ast.literal_eval(node.value))
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                if node.value is None:
                    return []
                return list(ast.literal_eval(node.value))
    return None


def _path_tail(value: object, marker: str) -> str:
    """Support path tail behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    marker : str
        The marker value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = str(value or "").replace("\\", "/").strip("/")
    if marker in text:
        return text.split(marker, 1)[-1].strip("/")
    return text.rsplit("/", 1)[-1]


def _resolve_help_folder(base: Path, data: dict[str, Any]) -> Path | None:
    """Support resolve help folder behavior.
    
    Parameters
    ----------
    base : Path
        The base value.
    data : dict[str, Any]
        The input data.
    
    Returns
    -------
    Path | None
        The resolved path.
    """
    
    value = data.get("help_folder") or data.get("helper_folder")
    if not value:
        return None
    return base / _path_tail(value, "insert_missing_docstrings_gui/")


def _resolve_origin(base: Path, data: dict[str, Any]) -> Path | None:
    """Support resolve origin behavior.
    
    Parameters
    ----------
    base : Path
        The base value.
    data : dict[str, Any]
        The input data.
    
    Returns
    -------
    Path | None
        The resolved path.
    """
    
    value = data.get("origin")
    if not value:
        return None
    return base / Path(str(value).replace("\\", "/")).name


def _helper_entries(data: dict[str, Any], help_folder: Path) -> list[tuple[str, Path, dict[str, Any]]]:
    """Support helper entries behavior.
    
    Parameters
    ----------
    data : dict[str, Any]
        The input data.
    help_folder : Path
        The help folder value.
    
    Returns
    -------
    list[tuple[str, Path, dict[str, Any]]]
        The list of values.
    """
    
    helpers = data.get("helpers", {})
    entries: list[tuple[str, Path, dict[str, Any]]] = []
    if isinstance(helpers, dict):
        for name, meta in helpers.items():
            entries.append((str(name), help_folder / str(name), dict(meta or {})))
        return entries
    if isinstance(helpers, list):
        for item in helpers:
            meta = dict(item or {})
            rel_path = str(meta.get("path") or "")
            name = Path(rel_path.replace("\\", "/")).name
            entries.append((name, help_folder / name, meta))
    return entries


def _physical_helper_names(help_folder: Path) -> set[str]:
    """Support physical helper names behavior.
    
    Parameters
    ----------
    help_folder : Path
        The help folder value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {
        item.name
        for item in help_folder.glob("*.py")
        if item.name != "__pycache__"
    }


def _is_strict_manifest(data: dict[str, Any]) -> bool:
    """Support is strict manifest behavior.
    
    Parameters
    ----------
    data : dict[str, Any]
        The input data.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return bool(data.get("enforce_strict_headers"))


def validate_manifest(path: Path) -> list[str]:
    """Validate the manifest.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    base = path.parent
    help_folder = _resolve_help_folder(base, data)
    origin = _resolve_origin(base, data)
    strict_manifest = _is_strict_manifest(data)

    if help_folder is None:
        errors.append("manifest missing help_folder/helper_folder")
        return errors
    if origin is None:
        errors.append("manifest missing origin")
        return errors
    if not help_folder.exists():
        errors.append(f"help_folder missing: {help_folder}")
        return errors
    if not origin.exists():
        errors.append(f"origin missing: {origin}")

    entries = _helper_entries(data, help_folder)
    manifest_helpers = {name for name, _, _ in entries}
    physical_helpers = _physical_helper_names(help_folder)
    for item in sorted(manifest_helpers - physical_helpers):
        errors.append(f"helper listed but missing: {item}")
    for item in sorted(physical_helpers - manifest_helpers):
        errors.append(f"helper exists but not in manifest: {item}")

    for helper_name, helper_path, info in entries:
        if not helper_path.exists():
            continue
        text = helper_path.read_text(encoding="utf-8")
        if strict_manifest:
            for field in REQUIRED_HEADER_FIELDS:
                if field not in text[:1200]:
                    errors.append(f"{helper_name}: missing header field {field}")
        exported = list(info.get("exports", []))
        actual_all = _literal_all(helper_path)
        if actual_all is not None and sorted(actual_all) != sorted(exported):
            errors.append(
                f"{helper_name}: __all__ mismatch manifest exports "
                f"expected={exported!r} actual={actual_all!r}"
            )
        for dep in info.get("depends_on", []):
            if dep not in manifest_helpers:
                errors.append(f"{helper_name}: depends_on missing helper {dep}")
        graph_deps = data.get("dependency_graph", {}).get(helper_name, [])
        if strict_manifest and sorted(graph_deps) != sorted(info.get("depends_on", [])):
            errors.append(f"{helper_name}: dependency_graph mismatch")

    if origin.exists() and strict_manifest:
        origin_text = origin.read_text(encoding="utf-8")
        if "AI CONTEXT - REFACTORED MODULE" not in origin_text:
            errors.append(f"{origin.name}: missing AI CONTEXT docstring")
        if _literal_all(origin) is None:
            errors.append(f"{origin.name}: missing __all__")

    return errors


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    root = Path(__file__).resolve().parent
    manifests = sorted(root.rglob("*_help.json"))
    failed = False
    for manifest in manifests:
        errors = validate_manifest(manifest)
        if errors:
            failed = True
            print(f"FAIL - {manifest}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS - {manifest}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
