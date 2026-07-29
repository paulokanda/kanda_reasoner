#!/usr/bin/env python3
"""Validate handoff package ownership and routed artifact visibility."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter_paths_private import (
    _remove_obsolete_all_in_one_outputs,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter_support import (
    external_readme_text,
    package_specs,
)
from kanda_reasoner_app.reasoner_context_bundle.routing_manifest_builder import (
    build_routing_manifest_payload,
)
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ProjectContext
from kanda_reasoner_app.reasoner_engine.project_web_ai_handoff_reader import (
    OPTIONAL_SUFFIXES,
    _matching_suffix,
)


def _context(base: Path) -> ProjectContext:
    """Create one isolated self-hosting project context."""
    root = base / "kanda_reasoner"
    evidence_root = base / "kanda_reasoner_show_project_to_AI"
    return ProjectContext(
        root=root,
        project_slug="kanda_reasoner",
        evidence_root=evidence_root,
        json_complete_dir=evidence_root / "second_prompt_files",
        active_project_id="validation-project-id",
        active_project_root_fingerprint="validation-root-fingerprint",
    )


def _require(condition: bool, message: str) -> None:
    """Raise a clear validation failure when condition is false."""
    if not condition:
        raise AssertionError(message)


def _validate_single_package(context: ProjectContext, base: Path) -> None:
    """Require one canonical AI-readable upload package."""
    specs = package_specs(context, [base / "artifact.json"])
    _require(len(specs) == 1, "Expected exactly one handoff package spec.")
    _require(specs[0]["name"] == "upload", "Upload must be the canonical package.")
    _require(
        "all_in_one" not in external_readme_text(context, 500),
        "External README still advertises the deprecated all-in-one package.",
    )
    print("HANDOFF PACKAGE SINGLE OWNER: PASS")


def _validate_stale_cleanup(context: ProjectContext, base: Path) -> None:
    """Require stale all-in-one ZIP cleanup without upload ZIP deletion."""
    destination = base / "second_prompt_files"
    destination.mkdir(parents=True, exist_ok=True)
    stale = destination / "kanda_reasoner__ai_handoff_all_in_one.zip"
    upload = destination / "kanda_reasoner__ai_handoff_upload.zip"
    stale.write_bytes(b"stale")
    upload.write_bytes(b"current")

    removed = _remove_obsolete_all_in_one_outputs(
        destination,
        context.project_slug,
    )
    _require(removed == [stale], "Unexpected obsolete-package cleanup result.")
    _require(not stale.exists(), "Deprecated all-in-one ZIP was not removed.")
    _require(upload.exists(), "Canonical upload ZIP was removed incorrectly.")
    print("HANDOFF STALE ALL_IN_ONE CLEANUP: PASS")


def _validate_routing(context: ProjectContext) -> None:
    """Require explicit paths and conditional exclusion-audit routing."""
    payload = build_routing_manifest_payload(context)
    artifact_paths = payload["artifact_paths"]
    required_paths = {
        "exclusion_rules_json",
        "source_archive_manifest_json",
        "validation_state_json",
    }
    _require(
        required_paths.issubset(artifact_paths),
        "Routing manifest is missing required artifact paths.",
    )

    routes = payload["task_routes"]
    _require("exclusion_policy_audit" in routes, "Exclusion audit route is missing.")
    exclusion_route = set(routes["exclusion_policy_audit"]["route_read_artifacts"])
    _require(
        required_paths.issubset(exclusion_route),
        "Exclusion audit route is missing required artifacts.",
    )

    structure_route = set(
        routes["project_structure_map_update"]["route_read_artifacts"]
    )
    _require(
        required_paths.issubset(structure_route),
        "Project Structure Map route is missing required artifacts.",
    )
    print("EXCLUSION RULES ROUTING: PASS")
    print("HANDOFF ROUTING ARTIFACT PATHS: PASS")


def _validate_reader_contract() -> None:
    """Require the integrated handoff reader to expose exclusion rules."""
    suffix = "__exclusion_rules.json"
    _require(suffix in OPTIONAL_SUFFIXES, "Reader optional suffix is missing.")
    _require(
        _matching_suffix("folder/project" + suffix) == suffix,
        "Reader does not recognize exclusion-rules members.",
    )
    print("HANDOFF READER EXCLUSION RULES: PASS")


def main() -> int:
    """Run focused deterministic validation and return an exit code."""
    try:
        with TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            context = _context(base)
            _validate_single_package(context, base)
            _validate_stale_cleanup(context, base)
            _validate_routing(context)
            _validate_reader_contract()
        print("SHOW PROJECT HANDOFF PACKAGE ROUTING CLEANUP: PASS")
        return 0
    except Exception as exc:
        print("SHOW PROJECT HANDOFF PACKAGE ROUTING CLEANUP: FAIL")
        print(type(exc).__name__ + ": " + str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
