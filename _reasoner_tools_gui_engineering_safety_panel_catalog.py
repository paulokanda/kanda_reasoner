# project-path: _reasoner_tools_gui_engineering_safety_panel_catalog.py
"""Private catalog construction for the Engineering Safety panel."""

from __future__ import annotations

from typing import Any

__all__: list[str] = []

_TOOL_SPECS: tuple[tuple[str, str, str, str], ...] = (
    (
        "Source Hygiene",
        "Scan BOM",
        "bom-scan",
        "Dry-run scan for UTF-8 BOM and decoding issues.",
    ),
    (
        "Source Hygiene",
        "Ruff Quality",
        "ruff-quality",
        "Read-only project-wide Ruff lint and format check.",
    ),
    (
        "Source Hygiene",
        "Ruff Corrections",
        "ruff-correction-dialog",
        "Create, review, and explicitly apply a safe Ruff correction preview.",
    ),
    (
        "Source Hygiene",
        "Shadow Audit",
        "shadow-audit",
        "Read-only audit for public-symbol and facade conflicts.",
    ),
    (
        "Source Hygiene",
        "Plan Shadow Fix",
        "shadow-plan",
        "Build a read-only correction plan for shadow findings.",
    ),
    (
        "Source Hygiene",
        "Facade Fix Plan",
        "facade-fix-plan",
        "Plan safe mechanical facade cleanup without applying edits.",
    ),
    (
        "Engineering Safety",
        "Risk Change Radar",
        "risk-radar",
        "Estimate what can break before a patch.",
    ),
    (
        "Engineering Safety",
        "Crash Triage",
        "crash-triage",
        "Summarize a crash or traceback and first files to inspect.",
    ),
    (
        "Engineering Safety",
        "Refactor Playbook",
        "refactor-playbook",
        "Create a staged refactor plan with validation steps.",
    ),
    (
        "Governance Automation",
        "Release Notes",
        "release-notes",
        "Draft release notes from explicit bundle evidence.",
    ),
    (
        "Governance Automation",
        "Push Plan",
        "push-plan",
        "Show the default validation plan for every push.",
    ),
    (
        "Stack Compatibility",
        "Stack Brief",
        "stack-brief",
        "Draft dependency and runtime compatibility notes.",
    ),
    (
        "Draft Reliability",
        "API Contract",
        "api-contract",
        "Draft input/output guard recommendations.",
    ),
    (
        "Draft Reliability",
        "Property Test",
        "property-test",
        "Draft property-test guidance for a function.",
    ),
    (
        "Project Symbol Atlas",
        "Atlas Report",
        "atlas-report",
        "Build Project Symbol Atlas reports for the current project.",
    ),
    (
        "Project Symbol Atlas",
        "Evidence Freshness",
        "evidence-freshness",
        "Check whether Project Analysis Evidence still matches live source.",
    ),
    (
        "Project Symbol Atlas",
        "Find Symbol",
        "find-symbol",
        "Find an existing symbol before creating new code.",
    ),
    (
        "Project Symbol Atlas",
        "Find Owner",
        "find-owner",
        "Find the likely owner file for a symbol.",
    ),
    (
        "Project Symbol Atlas",
        "Facade Owner",
        "facade-owner",
        "Resolve whether a target file is a facade and identify the owner.",
    ),
    (
        "Project Symbol Atlas",
        "Main and Helpers",
        "main-helpers",
        "Map main file, helper files, and public API owner.",
    ),
    (
        "Project Symbol Atlas",
        "Related Files",
        "related-files",
        "Find tests, helpers, manifests, diagnostics, and related support files.",
    ),
    (
        "Project Symbol Atlas",
        "Pre-Patch Gate",
        "pre-patch-gate",
        "Run ownership checks before editing source files.",
    ),
    (
        "Utilities",
        "List Tools",
        "list-tools",
        "List available Safety Suite CLI commands.",
    ),
)


def _build_engineering_safety_panel_catalog(tool_type: type[Any]) -> tuple[Any, ...]:
    """Build the immutable panel catalog using the public panel tool type."""
    return tuple(
        tool_type(
            section=section,
            label=label,
            command_name=command_name,
            description=description,
        )
        for section, label, command_name, description in _TOOL_SPECS
    )
