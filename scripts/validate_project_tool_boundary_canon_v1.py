# project-path: scripts/validate_project_tool_boundary_canon_v1.py
"""Validate the KPR-12-001 boundary owner and compact startup bridge."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
import tempfile
from pathlib import Path

FEATURE_ID = "project-tool-boundary-canon-v2-0"
PLIB = Path("kanda_prompt_workspace/prompt_library")
FULL_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md"
BRIDGE_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_startup_bridge.md"
FULL_META_REL = PLIB / "METADATA/project_tool_boundary_canon.meta.json"
BRIDGE_META_REL = PLIB / "METADATA/project_tool_boundary_startup_bridge.meta.json"
SOURCE_MAP_REL = Path("kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json")
ROUTE_REL = PLIB / "ROUTING/prompt_navigation_index.json"


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def load_json(path: Path) -> dict[str, object]:
    loaded = json.loads(read(path))
    if not isinstance(loaded, dict):
        raise AssertionError("JSON root must be an object: " + str(path))
    return loaded


def version(value: object) -> tuple[int, ...]:
    parts = str(value).strip().split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise AssertionError("invalid version: " + str(value))
    return tuple(int(part) for part in parts)


def require(text: str, markers: tuple[str, ...], label: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(label + " missing marker: " + marker)


def gate(label: str, passed: bool) -> None:
    if not passed:
        raise AssertionError(label + ": FAIL")
    print(label + ": PASS")


def validate_sources(root: Path) -> None:
    full = read(root / FULL_REL)
    bridge = read(root / BRIDGE_REL)
    require(
        full,
        (
            "Prompt ID: project_tool_boundary_canon",
            "Prompt code: KPR-12-001",
            "Load type: routed",
            "Same canonical resolved Tool/Project root",
            "Project root fingerprint or immutable identity",
            "Cross-project access modes",
            "Generated evidence authority: NON_AUTHORITATIVE / CANON_ASSIGNED / UNRESOLVED",
            "May begin coding: NO",
            "Never duplicate MCard, Workbench, delivery, or durable-document owner contracts",
        ),
        "FULL_CANON",
    )
    require(
        bridge,
        (
            "prompt_code: KPR-12-006",
            "prompt_id: project_tool_boundary_startup_bridge",
            "This bridge is startup context only",
            "May mutate from this bridge alone: NO",
            "KPR-12-001 project_tool_boundary_canon",
        ),
        "STARTUP_BRIDGE",
    )
    gate("BOUNDARY_FULL_CANON_ROUTED", "Load type: always_startup" not in full)
    gate("BOUNDARY_STARTUP_BRIDGE_COMPACT", len(bridge.splitlines()) <= 60)
    gate("BOUNDARY_FULL_CANON_WITHIN_LIMIT", len(full.splitlines()) <= 500)


def validate_metadata(root: Path) -> None:
    full = load_json(root / FULL_META_REL)
    bridge = load_json(root / BRIDGE_META_REL)
    gate("BOUNDARY_FULL_METADATA_IDENTITY", full.get("prompt_code") == "KPR-12-001" and full.get("load_type") == "routed")
    gate("BOUNDARY_FULL_METADATA_VERSION", version(full.get("version")) >= (2, 0))
    gate("BOUNDARY_BRIDGE_METADATA_IDENTITY", bridge.get("prompt_code") == "KPR-12-006" and bridge.get("load_type") == "always_startup")
    gate("BOUNDARY_BRIDGE_METADATA_VERSION", version(bridge.get("version")) >= (1, 0))
    for label, item in (("full", full), ("bridge", bridge)):
        gate("BOUNDARY_METADATA_STAGE_" + label.upper(), bool(str(item.get("source_stage") or "").strip()) and item.get("source_stage") == item.get("updated_for"))


def validate_startup_and_routes(root: Path) -> None:
    source_map = load_json(root / SOURCE_MAP_REL)
    entries = source_map.get("startup_sources")
    if not isinstance(entries, list):
        raise AssertionError("startup_sources must be a list")
    matches = [
        item
        for item in entries
        if isinstance(item, dict)
        and item.get("prompt_id") == "project_tool_boundary_startup_bridge"
    ]
    gate("BOUNDARY_STARTUP_ENTRY_UNIQUE", len(matches) == 1)
    entry = matches[0]
    gate("BOUNDARY_STARTUP_BRIDGE_SOURCE", entry.get("prompt_id") == "project_tool_boundary_startup_bridge")
    gate("BOUNDARY_STARTUP_FILENAME_STABLE", entry.get("generated_filename") == "14_project_tool_boundary_canon.md")

    route = load_json(root / ROUTE_REL)
    route_entries = route.get("entries")
    if not isinstance(route_entries, list):
        raise AssertionError("route entries must be a list")
    ids = [item.get("prompt_id") for item in route_entries if isinstance(item, dict)]
    gate("BOUNDARY_ROUTE_FULL_UNIQUE", ids.count("project_tool_boundary_canon") == 1)
    gate("BOUNDARY_ROUTE_BRIDGE_UNIQUE", ids.count("project_tool_boundary_startup_bridge") == 1)


def validate_runtime_path_owner(root: Path) -> None:
    import sys

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from kanda_reasoner_app.project_analysis_evidence_paths import project_analysis_evidence_root

    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "sample_project"
        project.mkdir()
        support = project_analysis_evidence_root(project)
        gate("BOUNDARY_RUNTIME_SUPPORT_EXTERNAL", support != project and project not in support.parents)
        gate("BOUNDARY_RUNTIME_NOT_HARDCODED", support.name.startswith("sample_project"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    validate_sources(root)
    validate_metadata(root)
    validate_startup_and_routes(root)
    validate_runtime_path_owner(root)
    print("PROJECT_TOOL_BOUNDARY_CANON_REGRESSION_SET: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
