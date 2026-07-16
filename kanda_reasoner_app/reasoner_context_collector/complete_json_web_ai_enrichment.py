# project-path: kanda_reasoner_app/reasoner_context_collector/complete_json_web_ai_enrichment.py
"""Web-AI enrichment for the canonical complete JSON artifact.

This module is intentionally deterministic and dependency-light. It is used by
Project Reasoner's official collection workflow to ensure the complete JSON
contains the web-AI sections required by architecture validation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    primary_evidence_json_path as build_primary_evidence_json_path,
)

from ._complete_json_web_ai_enrichment_analysis import (
    _file_responsibility_index,
    _iter_python_files,
    _read_text,
    _responsibility_from_path,
    _safe_parse,
    _stable_evidence_index,
    _symbol_kind,
    _symbol_records,
    _test_protection_index,
)

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


def _write_json(path: Path, payload: Any) -> None:
    """Write a JSON payload deterministically as UTF-8 text."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _read_json(path: Path) -> Any:
    """Read a JSON payload, returning an empty mapping for missing/invalid input."""
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
    """Return the project root that owns this package."""
    return Path(__file__).resolve().parents[2]


def complete_json_path_for_project(project_root: str | Path | None = None) -> Path:
    """Return the canonical complete JSON evidence path for a project."""
    root = Path(project_root).resolve() if project_root else _project_root_from_here()
    return build_primary_evidence_json_path(root)


def build_web_ai_sections(project_root: str | Path | None = None) -> dict[str, Any]:
    """Build deterministic Web-AI evidence sections for a project root."""
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
    """Add missing Web-AI evidence sections to the canonical JSON artifact."""
    root = Path(project_root).resolve() if project_root else _project_root_from_here()
    target = (
        Path(complete_json_path).resolve()
        if complete_json_path
        else complete_json_path_for_project(root)
    )
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
    """Enrich the canonical complete JSON artifact for one project root."""
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
