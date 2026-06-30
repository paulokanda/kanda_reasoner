# project-path: kanda_reasoner_app/reasoner_context_collector/complete_json_web_ai_enrichment.py
"""Web-AI enrichment for the canonical complete JSON artifact.

This module is intentionally deterministic and dependency-light. It is used by
Project Reasoner's official collection workflow to ensure the complete JSON
contains the web-AI sections required by architecture validation.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import primary_evidence_json_path as build_primary_evidence_json_path
from typing import Any

REQUIRED_WEB_AI_SECTIONS = [
    "web_ai_readme",
    "web_ai_readme_summary",
    "web_ai_symbol_index",
    "primary_definition_index",
    "stable_evidence_id_index",
    "entry_points_detail",
    "web_ai_file_responsibility_index",
    "web_ai_test_protection_index",
]

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "_patch_backups",
    ".project_reference",
    "_project_reference",
    "project_freeze_ledger",
    "build",
    "dist",
    "node_modules",
    "venv",
}


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
    
    return path.read_text(encoding="utf-8", errors="replace")


def _write_json(path: Path, payload: Any) -> None:
    """Support write json behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    payload : Any
        The payload value.
    """
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _read_json(path: Path) -> Any:
    """Support read json behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    Any
        The any result.
    """
    
    if not path.exists():
        return {}
    text = _read_text(path).strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def _project_root_from_here() -> Path:
    """Support project root from here behavior.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    return Path(__file__).resolve().parents[2]


def complete_json_path_for_project(project_root: str | Path | None = None) -> Path:
    """Support complete json path for project behavior.
    
    Parameters
    ----------
    project_root : str | Path | None, optional
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    root = Path(project_root).resolve() if project_root else _project_root_from_here()
    return build_primary_evidence_json_path(root)


def _iter_python_files(project_root: Path) -> list[Path]:
    """Support iter python files behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    list[Path]
        The list of values.
    """
    
    result = []
    for path in project_root.rglob("*.py"):
        rel_parts = path.relative_to(project_root).parts
        if any(part in SKIP_DIR_NAMES for part in rel_parts):
            continue
        if path.name.endswith(".pyc"):
            continue
        result.append(path)
    return sorted(result, key=lambda item: str(item).lower())


def _safe_parse(path: Path) -> ast.AST | None:
    """Support safe parse behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    ast.AST | None
        The ast result.
    """
    
    try:
        return ast.parse(_read_text(path), filename=str(path))
    except SyntaxError:
        return None


def _symbol_kind(node: ast.AST) -> str:
    """Support symbol kind behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(node, ast.ClassDef):
        return "class"
    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"
    if isinstance(node, ast.FunctionDef):
        return "function"
    return "symbol"


def _responsibility_from_path(rel_path: str) -> str:
    """Support responsibility from path behavior.
    
    Parameters
    ----------
    rel_path : str
        The rel path value.
    
    Returns
    -------
    str
        The string result.
    """
    
    lowered = rel_path.lower()
    if "runtime" in lowered:
        return "runtime evidence collection"
    if "collector" in lowered:
        return "static evidence collection"
    if "reasoner_retriever" in lowered or "retrieval" in lowered:
        return "retrieval and evidence selection"
    if "json_splitter" in lowered:
        return "json splitting and reassembly"
    if "manage_architecture" in lowered:
        return "architecture governance"
    if "manage_workflows" in lowered:
        return "workflow governance"
    if "gui" in lowered or "window" in lowered:
        return "gui behavior"
    if "test" in lowered:
        return "test support"
    return "project support"


def _looks_like_entry_point(tree: ast.AST) -> bool:
    """Support looks like entry point behavior.
    
    Parameters
    ----------
    tree : ast.AST
        The parsed syntax tree.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        try:
            test_text = ast.unparse(node.test)
        except Exception:
            test_text = ""
        if "__name__" in test_text and "__main__" in test_text:
            return True
    return False


def _symbol_records(project_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    """Support symbol records behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]
        The tuple of values.
    """
    
    symbol_index = []
    primary_definitions = {}
    entry_points = []

    for path in _iter_python_files(project_root):
        rel_path = path.relative_to(project_root).as_posix()
        tree = _safe_parse(path)
        if tree is None:
            continue
        module_symbols = []
        for node in getattr(tree, "body", []):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                record = {
                    "name": node.name,
                    "kind": _symbol_kind(node),
                    "file": rel_path,
                    "line": int(getattr(node, "lineno", 0) or 0),
                }
                module_symbols.append(record)
                primary_definitions.setdefault(node.name, []).append(record)
        if module_symbols:
            symbol_index.append(
                {
                    "file": rel_path,
                    "responsibility": _responsibility_from_path(rel_path),
                    "symbols": module_symbols,
                }
            )
        if _looks_like_entry_point(tree) or any(item["name"] == "main" for item in module_symbols):
            entry_points.append(
                {
                    "file": rel_path,
                    "has_main_function": any(item["name"] == "main" for item in module_symbols),
                    "has_main_guard": _looks_like_entry_point(tree),
                }
            )
    return symbol_index, primary_definitions, entry_points


def _file_responsibility_index(project_root: Path, symbol_index: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Support file responsibility index behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    symbol_index : list[dict[str, Any]]
        The symbol index value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    by_file = {entry["file"]: entry for entry in symbol_index}
    records = []
    for path in _iter_python_files(project_root):
        rel_path = path.relative_to(project_root).as_posix()
        entry = by_file.get(rel_path, {})
        records.append(
            {
                "file": rel_path,
                "responsibility": _responsibility_from_path(rel_path),
                "public_symbols": [
                    item["name"] for item in entry.get("symbols", []) if not item["name"].startswith("_")
                ],
            }
        )
    return records


def _test_protection_index(project_root: Path, responsibility_index: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Support test protection index behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    responsibility_index : list[dict[str, Any]]
        The responsibility index value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    test_files = {
        path.relative_to(project_root).as_posix().lower()
        for path in _iter_python_files(project_root)
        if "test" in path.name.lower() or "tests" in [part.lower() for part in path.relative_to(project_root).parts]
    }
    records = []
    for item in responsibility_index:
        rel_path = item["file"]
        stem = Path(rel_path).stem.lower()
        related_tests = [test for test in sorted(test_files) if stem in test]
        records.append(
            {
                "file": rel_path,
                "has_related_test": bool(related_tests),
                "related_tests": related_tests[:10],
            }
        )
    return records


def _stable_evidence_index(sections: dict[str, Any]) -> dict[str, Any]:
    """Support stable evidence index behavior.
    
    Parameters
    ----------
    sections : dict[str, Any]
        The sections value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    evidence = {}
    for section_name, section_value in sorted(sections.items()):
        encoded = json.dumps(section_value, sort_keys=True, default=str)
        evidence_id = hashlib.sha256((section_name + "\n" + encoded).encode("utf-8")).hexdigest()[:16]
        evidence[evidence_id] = {
            "section": section_name,
            "sha256_16": evidence_id,
        }
    return evidence


def build_web_ai_sections(project_root: str | Path | None = None) -> dict[str, Any]:
    """Build a web ai sections.
    
    Parameters
    ----------
    project_root : str | Path | None, optional
        The project root path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    root = Path(project_root).resolve() if project_root else _project_root_from_here()
    symbol_index, primary_definitions, entry_points = _symbol_records(root)
    responsibility_index = _file_responsibility_index(root, symbol_index)
    test_index = _test_protection_index(root, responsibility_index)

    summary = {
        "project_root": str(root),
        "python_file_count": len(responsibility_index),
        "symbol_file_count": len(symbol_index),
        "entry_point_count": len(entry_points),
        "test_index_count": len(test_index),
        "source": "pass_064d_ast_fallback",
    }
    readme = {
        "title": "Project Reasoner complete JSON web-AI sections",
        "purpose": "Provide stable symbol, responsibility, entry-point, and test-protection evidence for local/web AI routing.",
        "summary": summary,
    }

    sections = {
        "web_ai_readme": readme,
        "web_ai_readme_summary": summary,
        "web_ai_symbol_index": symbol_index,
        "primary_definition_index": primary_definitions,
        "entry_points_detail": entry_points,
        "web_ai_file_responsibility_index": responsibility_index,
        "web_ai_test_protection_index": test_index,
    }
    sections["stable_evidence_id_index"] = _stable_evidence_index(sections)
    return sections


def enrich_complete_json_for_web_ai(
    complete_json_path: str | Path | None = None,
    project_root: str | Path | None = None,
) -> dict[str, Any]:
    """Support enrich complete json for web ai behavior.
    
    Parameters
    ----------
    complete_json_path : str | Path | None, optional
        The optional complete json path value.
    project_root : str | Path | None, optional
        The project root path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    root = Path(project_root).resolve() if project_root else _project_root_from_here()
    target = Path(complete_json_path).resolve() if complete_json_path else complete_json_path_for_project(root)
    payload = _read_json(target)
    if not isinstance(payload, dict):
        payload = {}

    before_missing = [name for name in REQUIRED_WEB_AI_SECTIONS if name not in payload]
    sections = build_web_ai_sections(root)
    changed = False
    for name in REQUIRED_WEB_AI_SECTIONS:
        if name not in payload:
            payload[name] = sections[name]
            changed = True

    if changed:
        _write_json(target, payload)

    after_missing = [name for name in REQUIRED_WEB_AI_SECTIONS if name not in payload]
    return {
        "target": str(target),
        "changed": changed,
        "missing_before": before_missing,
        "missing_after": after_missing,
    }


def enrich_project_complete_json(project_root: str | Path | None = None) -> dict[str, Any]:
    """Support enrich project complete json behavior.
    
    Parameters
    ----------
    project_root : str | Path | None, optional
        The project root path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    root = Path(project_root).resolve() if project_root else _project_root_from_here()
    return enrich_complete_json_for_web_ai(complete_json_path_for_project(root), root)


__all__ = [
    "REQUIRED_WEB_AI_SECTIONS",
    "build_web_ai_sections",
    "complete_json_path_for_project",
    "enrich_complete_json_for_web_ai",
    "enrich_project_complete_json",
    "main",
]


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for deterministic complete JSON enrichment."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Deterministically add AI-readable evidence sections to complete JSON."
    )
    parser.add_argument("--root", default=None, help="Project root path.")
    parser.add_argument(
        "--complete-json",
        default=None,
        help="Path to the complete JSON file to enrich. Defaults to the project evidence path.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Emit compact JSON status output.",
    )
    args = parser.parse_args(argv)

    result = enrich_complete_json_for_web_ai(args.complete_json, args.root)
    print(
        json.dumps(
            result,
            sort_keys=True,
            indent=None if args.compact else 2,
            ensure_ascii=True,
        ),
        flush=True,
    )
    return 0 if not result.get("missing_after") else 1


if __name__ == "__main__":
    raise SystemExit(main())


# PASS_069C_STATIC_CONTEXT_SCOPE_OVERRIDE_START
def _iter_python_files(project_root, *args, **kwargs):
    """Support iter python files behavior.
    
    Parameters
    ----------
    project_root : object
        The project root path.
    *args : object
        The positional arguments.
    **kwargs : object
        The kwargs value.
    """
    
    from kanda_reasoner_app.reasoner_context_collector.collector_scope import iter_project_python_files
    return list(iter_project_python_files(project_root))
# PASS_069C_STATIC_CONTEXT_SCOPE_OVERRIDE_END
