"""Support the assert real project static context smoke module for Project Reasoner."""

from __future__ import annotations

import json

from kanda_reasoner_app.project_root_resolver import default_smoke_output_json_path


DEFAULT_JSON_PATH = default_smoke_output_json_path()


def main() -> int:
    json_path = DEFAULT_JSON_PATH

    if not json_path.is_file():
        print(f"ERROR: smoke JSON not found: {json_path}")
        return 1

    with open(json_path, "r", encoding="utf-8", errors="replace") as handle:
        payload = json.load(handle)

    packaging = payload.get("packaging_metadata", {})
    docs = payload.get("documentation_intent", {})

    if not isinstance(packaging, dict):
        print("ERROR: packaging_metadata is missing or is not a dictionary.")
        return 1

    if not isinstance(docs, dict):
        print("ERROR: documentation_intent is missing or is not a dictionary.")
        return 1

    packaging_files_found = packaging.get("packaging_files_found", [])
    documentation_files_found = docs.get("documentation_files_found", [])

    if not isinstance(packaging_files_found, list):
        print("ERROR: packaging_files_found is not a list.")
        return 1

    if not isinstance(documentation_files_found, list):
        print("ERROR: documentation_files_found is not a list.")
        return 1

    if len(documentation_files_found) == 0:
        print("ERROR: documentation_intent found zero documentation files.")
        return 1

    print("REAL PROJECT STATIC CONTEXT ASSERTION")
    print(f"JSON path                  : {json_path}")
    print(f"packaging files found      : {len(packaging_files_found)}")
    print(f"documentation files found  : {len(documentation_files_found)}")
    print(f"project_name               : {packaging.get('project_name', '')}")
    print(f"declared_version           : {packaging.get('declared_version', '')}")
    print(f"build_backend              : {packaging.get('build_backend', '')}")
    print(f"project_purpose_summary    : {str(docs.get('project_purpose_summary', ''))[:160]}")
    print("Assertion passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
