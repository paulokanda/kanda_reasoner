"""Validate retirement of the compiled architecture companion."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import csv
import json
import zipfile
from pathlib import Path

FEATURE_ID = "governed-architecture-companion-startup-and-routing-v1"
PROMPT_ID = "governed_architecture_companion_handoff"
PROMPT_CODE = "KPR-04-007"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(f"{marker}: FAIL")
    print(f"{marker}: PASS")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def validate_source(project_root: Path) -> None:
    library = project_root / "kanda_prompt_workspace" / "prompt_library"
    prompt = read_text(
        library / "ACTIVE_PROMPTS" / "04_box_architecture_and_boundaries"
        / f"{PROMPT_ID}.md"
    )
    meta = load_json(library / "METADATA" / f"{PROMPT_ID}.meta.json")
    require(
        all(token in prompt for token in (
            f"prompt_code: {PROMPT_CODE}",
            "status: deprecated",
            "load_type: never",
            "historical_redirect_only",
            "The former compiled architecture companion is retired",
            "May begin coding: NO",
            "May write source: NO",
        )),
        "ARCH_COMPANION_DEPRECATED_REDIRECT_CONTRACT",
    )
    require(
        meta.get("prompt_code") == PROMPT_CODE
        and meta.get("status") == "deprecated"
        and meta.get("load_type") == "never"
        and meta.get("active_route") is False,
        "ARCH_COMPANION_DEPRECATED_METADATA",
    )
    nav = load_json(library / "ROUTING" / "prompt_navigation_index.json")
    require(
        not any(e.get("prompt_id") == PROMPT_ID for e in nav.get("entries", [])),
        "ARCH_COMPANION_MACHINE_ROUTE_RETIRED",
    )
    groups = load_json(library / "ROUTING" / "group_assimilation_index.json")
    require(
        not any(
            route.get("task_intent") == "GOVERNED_ARCHITECTURE_COMPANION"
            for route in groups.get("task_routes", [])
        ),
        "ARCH_COMPANION_GROUP_ROUTE_RETIRED",
    )
    with (library / "ROUTING" / "prompt_route_coverage_table.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    require(
        not any(row.get("prompt_id") == PROMPT_ID for row in rows),
        "ARCH_COMPANION_CSV_ROUTE_RETIRED",
    )
    startup = read_text(
        library / "ACTIVE_PROMPTS" / "01_session_start_and_navigation"
        / "start_of_day_master_stack.md"
    )
    require(
        "Class 04 Architecture Owner Dispatch Bridge" in startup
        and "Do not load the retired compiled architecture companion" in startup
        and "Load `governed_architecture_companion_handoff`" not in startup,
        "ARCH_COMPANION_STARTUP_DISPATCH_MIGRATED",
    )
    start_here = read_text(
        project_root / "kanda_prompt_workspace" / "prompt_tools"
        / "startup_kernel" / "start_here_lists.py"
    )
    require(
        "4. Class 04 Architecture Owner Dispatch" in start_here
        and "full governed_architecture_companion_handoff" not in start_here,
        "ARCH_COMPANION_START_HERE_MIGRATED",
    )
    bridge = read_text(
        library / "ACTIVE_PROMPTS" / "05_patch_delivery_and_validation"
        / "router_bridge_governed_implementation.md"
    )
    require(
        "the retired architecture companion is never loaded" in bridge
        and len(bridge.splitlines()) <= 500,
        "ARCH_COMPANION_ROUTER_BRIDGE_MIGRATED",
    )
    substitution = read_text(
        library / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing"
        / "prompt_substitution_map.md"
    )
    require(
        PROMPT_ID in substitution and "current canonical owner dispatch" in substitution,
        "ARCH_COMPANION_SUBSTITUTION_ROUTE",
    )


def validate_generated(delivery_dir: Path) -> None:
    startup_zip = delivery_dir / "first_prompts_to_ai.zip"
    prompt_zip = delivery_dir / "prompt_library.zip"
    with zipfile.ZipFile(startup_zip) as archive:
        stack = archive.read("05_start_of_day_master_stack.md").decode("utf-8")
        start_here = archive.read("00_START_HERE_FOR_AI.md").decode("utf-8")
    require(
        "Class 04 Architecture Owner Dispatch Bridge" in stack
        and "4. Class 04 Architecture Owner Dispatch" in start_here,
        "ARCH_COMPANION_GENERATED_STARTUP_MIGRATED",
    )
    with zipfile.ZipFile(prompt_zip) as archive:
        member = (
            "ACTIVE_PROMPTS/04_box_architecture_and_boundaries/"
            f"{PROMPT_ID}.md"
        )
        text = archive.read(member).decode("utf-8")
    require(
        "status: deprecated" in text and "historical_redirect_only" in text,
        "ARCH_COMPANION_PROMPT_LIBRARY_REDIRECT",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--delivery-dir")
    args = parser.parse_args()
    validate_source(Path(args.project_root).resolve())
    if args.delivery_dir:
        validate_generated(Path(args.delivery_dir).resolve())
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ARCH_COMPANION_VALIDATION_ERROR: {type(exc).__name__}: {exc}")
        raise
