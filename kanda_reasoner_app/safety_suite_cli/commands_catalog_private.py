# project-path: kanda_reasoner_app/safety_suite_cli/commands_catalog_private.py
"""Private command catalog for the safety-suite CLI."""

from __future__ import annotations

__all__: list[str] = []


def _available_cli_commands() -> tuple[str, ...]:
    """Return stable command names exposed by the safety-suite CLI."""
    return (
        "api-contract",
        "bom-scan",
        "crash-triage",
        "atlas-report",
        "evidence-freshness",
        "facade-fix-plan",
        "facade-owner",
        "find-owner",
        "find-symbol",
        "list-tools",
        "logic-placement",
        "main-helpers",
        "pre-patch-gate",
        "property-test",
        "push-plan",
        "refactor-playbook",
        "release-notes",
        "risk-radar",
        "ruff-quality",
        "shadow-audit",
        "related-files",
        "shadow-plan",
        "stack-brief",
        "symbol-atlas",
    )
