"""Support the run real project static context smoke module for Project Reasoner."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PACKAGE_PARENT = CURRENT_FILE.parent.parent

if __name__ == "__main__":
    if str(PACKAGE_PARENT) not in sys.path:
        sys.path.insert(0, str(PACKAGE_PARENT))

from kanda_reasoner_app.reasoner_engine_data_collector.collector_main import (
    run_collector,
)
from kanda_reasoner_app.project_root_resolver import (
    default_smoke_output_json_path,
    resolve_active_project_root,
)

DEFAULT_PROJECT_ROOT = resolve_active_project_root()
DEFAULT_OUTPUT_JSON = default_smoke_output_json_path(DEFAULT_PROJECT_ROOT)


def main() -> int:
    project_root = DEFAULT_PROJECT_ROOT
    output_json = DEFAULT_OUTPUT_JSON

    if not project_root.is_dir():
        print(f"ERROR: project root not found: {project_root}")
        return 1

    output_json.parent.mkdir(parents=True, exist_ok=True)

    result = run_collector(
        project_root=str(project_root),
        output_json=str(output_json),
        runtime_trace_json=None,
    )

    packaging = result.get("packaging_metadata", {})
    docs = result.get("documentation_intent", {})

    print("REAL PROJECT STATIC CONTEXT SMOKE")
    print(f"Project root: {project_root}")
    print(f"Output JSON : {output_json}")
    print("")

    print("PACKAGING METADATA")
    print(f"  project_name          : {packaging.get('project_name', '')}")
    print(f"  declared_version      : {packaging.get('declared_version', '')}")
    print(f"  build_backend         : {packaging.get('build_backend', '')}")
    print(
        f"  packaging_files_found : {len(packaging.get('packaging_files_found', []))}"
    )
    print(
        f"  declared_dependencies : {len(packaging.get('declared_dependencies', []))}"
    )
    print("")

    print("DOCUMENTATION INTENT")
    print(
        f"  project_purpose_summary : {docs.get('project_purpose_summary', '')[:160]}"
    )
    print(
        f"  documentation_files_found: {len(docs.get('documentation_files_found', []))}"
    )
    print(f"  declared_workflows      : {len(docs.get('declared_workflows', []))}")
    print(f"  run_instructions        : {len(docs.get('run_instructions', []))}")
    print(f"  named_features          : {len(docs.get('named_features', []))}")
    print(f"  external_integrations   : {len(docs.get('external_integrations', []))}")
    print("")

    with open(output_json, "r", encoding="utf-8", errors="replace") as handle:
        payload = json.load(handle)

    if "packaging_metadata" not in payload:
        print("ERROR: packaging_metadata missing from written JSON.")
        return 1

    if "documentation_intent" not in payload:
        print("ERROR: documentation_intent missing from written JSON.")
        return 1

    print("Smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
