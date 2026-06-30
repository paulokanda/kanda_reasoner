# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/snippet_retrieval_validate_manifests.py
"""Validate snippet_retrieval helper manifest artifacts."""

from __future__ import annotations

__all__ = []

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_STAGED_PACKAGE_NAME = "_".join(("ask", "ai", "project", "reasoner"))
BASE = ROOT / _STAGED_PACKAGE_NAME / "project_reasoner_v10" / "reasoner_retriever_help"
HELP_DIR = BASE / "snippet_retrieval_help"
MANIFEST = BASE / "snippet_retrieval_help.json"


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


def _extract_public_names(path: Path) -> list[str]:
    """Support extract public names behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    tree = ast.parse(_read_text(path), filename=str(path))
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
    return names


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    if not MANIFEST.exists():
        print(f"FAIL missing manifest: {MANIFEST}")
        return 1
    data = json.loads(_read_text(MANIFEST))
    errors: list[str] = []
    helper_dir_name = data.get("helper_directory", "snippet_retrieval_help")
    helper_base = BASE / helper_dir_name
    for rel_name in data.get("helper_files", []):
        path = helper_base / rel_name
        if not path.exists():
            errors.append(f"missing helper file: {path}")
            continue
        public_names = _extract_public_names(path)
        if public_names:
            errors.append(f"helper exposes public names: {rel_name}: {public_names}")
    if errors:
        for error in errors:
            print("FAIL " + error)
        return 1
    print("PASS snippet_retrieval helper manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
