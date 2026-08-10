# project-path: kanda_reasoner_app/reasoner_context_collector/collector_web_ai_complete_json_audit.py
"""Audit the complete Step 4 JSON for web-AI awareness sections.

This module validates that the canonical complete JSON produced by the GUI
workflow "4. Fourth step: collect project structure" contains the additive
web-AI sections added during the collector JSON-awareness phase.

It does not run the collector and does not modify JSON files.
"""

from __future__ import annotations

import logging

import argparse
import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import primary_evidence_json_path

__all__ = [
    "CANONICAL_COMPLETE_JSON_RELATIVE_PATH",
    "REQUIRED_WEB_AI_KEYS",
    "audit_complete_json_payload",
    "audit_complete_json_file",
    "main",
]

CANONICAL_COMPLETE_JSON_RELATIVE_PATH = Path("project_analysis_evidence/json_complete/project__complete.json")

REQUIRED_WEB_AI_KEYS = (
    "web_ai_symbol_index",
    "web_ai_symbol_summary",
    "primary_definition_index",
    "primary_definition_summary",
    "stable_evidence_id_index",
    "stable_evidence_id_summary",
    "entry_points_detail",
    "entry_points_detail_summary",
    "web_ai_file_responsibility_index",
    "web_ai_file_responsibility_summary",
    "web_ai_test_protection_index",
    "web_ai_test_protection_summary",
    "web_ai_readme",
    "web_ai_readme_summary",
)


def _safe_len(value: Any) -> int:
    """Return len(value) for common containers, otherwise zero."""
    if isinstance(value, (dict, list, tuple, set)):
        return len(value)
    return 0


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from path."""
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("Complete JSON top level must be an object.")

    return data


def _key_status(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Return status for one required web-AI key."""
    value = data.get(key)
    return {
        "key": key,
        "present": key in data,
        "value_type": type(value).__name__ if key in data else "",
        "item_count": _safe_len(value),
        "non_empty": bool(value),
    }


def _readme_route_types(web_ai_readme: Any) -> list[str]:
    """Return question route types found in web_ai_readme."""
    if not isinstance(web_ai_readme, dict):
        return []

    routes = web_ai_readme.get("question_routes", [])
    if not isinstance(routes, list):
        return []

    out: list[str] = []
    for item in routes:
        if isinstance(item, dict):
            value = str(item.get("question_type", "")).strip()
            if value:
                out.append(value)
    return sorted(out)


def audit_complete_json_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Audit an already-loaded complete JSON payload."""
    key_rows = [_key_status(data, key) for key in REQUIRED_WEB_AI_KEYS]
    missing = [row["key"] for row in key_rows if not row["present"]]

    readme_routes = _readme_route_types(data.get("web_ai_readme"))
    required_routes = {
        "symbol_responsibility",
        "symbol_definition_location",
        "file_or_box_responsibility",
        "test_protection",
        "entry_point_or_startup_flow",
        "citation_or_cross_chunk_evidence",
        "local_ai_answer_flow",
    }
    missing_routes = sorted(required_routes - set(readme_routes))

    project_summary = data.get("project_summary", {})
    if not isinstance(project_summary, dict):
        project_summary = {}

    project_summary_counts = {
        "web_ai_symbol_count": project_summary.get("web_ai_symbol_count", 0),
        "web_ai_symbol_docstring_count": project_summary.get(
            "web_ai_symbol_docstring_count",
            0,
        ),
        "primary_definition_symbol_group_count": project_summary.get(
            "primary_definition_symbol_group_count",
            0,
        ),
        "stable_evidence_record_count": project_summary.get(
            "stable_evidence_record_count",
            0,
        ),
        "entry_points_detail_count": project_summary.get(
            "entry_points_detail_count",
            0,
        ),
        "web_ai_file_responsibility_count": project_summary.get(
            "web_ai_file_responsibility_count",
            0,
        ),
        "web_ai_test_protected_source_count": project_summary.get(
            "web_ai_test_protected_source_count",
            0,
        ),
        "web_ai_test_unprotected_source_count": project_summary.get(
            "web_ai_test_unprotected_source_count",
            0,
        ),
        "web_ai_readme_question_route_count": project_summary.get(
            "web_ai_readme_question_route_count",
            0,
        ),
    }

    ok = not missing and not missing_routes

    return {
        "ok": ok,
        "missing_required_keys": missing,
        "required_key_status": key_rows,
        "web_ai_readme_route_types": readme_routes,
        "missing_web_ai_readme_routes": missing_routes,
        "project_summary_web_ai_counts": project_summary_counts,
        "top_level_key_count": len(data),
        "message": (
            "Complete JSON contains all required web-AI sections."
            if ok
            else "Complete JSON is missing required web-AI sections or routes."
        ),
    }


def audit_complete_json_file(path: Path) -> dict[str, Any]:
    """Audit a complete JSON file by path."""
    data = _load_json(path)
    result = audit_complete_json_payload(data)
    result["json_path"] = str(path)
    return result


def _resolve_json_path(project_root: str | None, json_path: str | None) -> Path:
    """Resolve the complete JSON path from arguments."""
    if json_path:
        return Path(json_path).resolve()

    root = Path(project_root or ".").resolve()
    return primary_evidence_json_path(root).resolve()


def _print_result(result: dict[str, Any]) -> None:
    """Print a readable audit result."""
    print("WEB-AI COMPLETE JSON AUDIT")
    print("status:", "PASS" if result.get("ok") else "FAIL")
    print("message:", result.get("message", ""))
    print("json_path:", result.get("json_path", ""))
    print("top_level_key_count:", result.get("top_level_key_count", 0))

    print("")
    print("required keys:")
    for row in result.get("required_key_status", []):
        print(
            "- {key}: present={present} type={value_type} count={item_count} non_empty={non_empty}".format(
                **row
            )
        )

    print("")
    print("web_ai_readme routes:")
    for route in result.get("web_ai_readme_route_types", []):
        print("- " + route)

    missing_keys = result.get("missing_required_keys", [])
    missing_routes = result.get("missing_web_ai_readme_routes", [])

    if missing_keys:
        print("")
        print("missing required keys:")
        for key in missing_keys:
            print("- " + key)

    if missing_routes:
        print("")
        print("missing web_ai_readme routes:")
        for route in missing_routes:
            print("- " + route)

    print("")
    print("project_summary web-AI counts:")
    counts = result.get("project_summary_web_ai_counts", {})
    if isinstance(counts, dict):
        for key in sorted(counts):
            print("- " + key + ": " + str(counts[key]))


def main(argv: list[str] | None = None) -> int:
    """Run the complete JSON audit CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        default=None,
        help="Project root containing project-analysis evidence.",
    )
    parser.add_argument(
        "--json-path",
        default=None,
        help="Explicit path to the complete generated JSON.",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Print machine-readable JSON instead of text.",
    )
    args = parser.parse_args(argv)

    path = _resolve_json_path(args.project_root, args.json_path)

    try:
        result = audit_complete_json_file(path)
    except Exception as exc:
        logging.exception("Boundary failure in main")
        result = {
            "ok": False,
            "json_path": str(path),
            "message": type(exc).__name__ + ": " + str(exc),
            "missing_required_keys": list(REQUIRED_WEB_AI_KEYS),
            "required_key_status": [],
            "web_ai_readme_route_types": [],
            "missing_web_ai_readme_routes": [],
            "project_summary_web_ai_counts": {},
            "top_level_key_count": 0,
        }

    if args.json_output:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        _print_result(result)

    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
