# project-path: kanda_reasoner_app/json_splitter/json_splitter_split_reassemble_validation_validate_manifests.py
"""Validate helper manifest for json_splitter_split_reassemble_validation."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT_PUBLIC_API = ['CHUNK_SCHEMA', 'stable_hash', 'validate_split_reassemble_output', 'main']


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


def module_all(path: Path) -> list[str] | None:
    """Support module all behavior.
    
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
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        return None
                    if isinstance(value, list):
                        return [str(item) for item in value]
    return None


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
    
    package_dir = Path(__file__).resolve().parent
    origin = package_dir / "json_splitter_split_reassemble_validation.py"
    helper_dir = package_dir / "json_splitter_split_reassemble_validation_help"
    core = helper_dir / "core.py"
    init_file = helper_dir / "__init__.py"
    manifest = package_dir / "json_splitter_split_reassemble_validation_help.json"
    required = [origin, helper_dir, core, init_file, manifest]
    for path in required:
        if not path.exists():
            print(f"FAIL missing: {path}")
            return 1
    try:
        data = json.loads(read_text(manifest))
    except Exception as exc:
        print(f"FAIL manifest JSON: {exc}")
        return 1
    if data.get("root_public_api") != ROOT_PUBLIC_API:
        print("FAIL manifest root_public_api mismatch")
        return 1
    root_all = module_all(origin)
    if root_all != ROOT_PUBLIC_API:
        print(f"FAIL root __all__ mismatch: {root_all}")
        return 1
    core_all = module_all(core)
    if core_all != ["CHUNK_SCHEMA", "stable_hash"]:
        print(f"FAIL core __all__ mismatch: {core_all}")
        return 1
    if len(read_text(origin).splitlines()) >= 500:
        print("FAIL root file has 500 or more lines")
        return 1
    for path in [origin, core, init_file]:
        if has_star_import(path):
            print(f"FAIL star import found: {path}")
            return 1
    print("PASS json_splitter_split_reassemble_validation helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
