"""Focused validation for the live reusable Freeze blueprint box."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .tool_archive_policy import ToolPathClassification, classify_tool_source_path

__all__ = [
    "seed_freeze_blueprint_fixture",
    "validate_freeze_blueprint_policy",
    "validate_freeze_blueprint_show_project_exclusion",
]


def _gate(marker: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def seed_freeze_blueprint_fixture(fixture_root: Path) -> Path:
    """Create the minimum exact ownership shape used by archive fixtures."""
    ledger = fixture_root / "project_freeze_ledger"
    tools = ledger / "freeze_tools"
    backups = ledger / "_patch_backups" / "historical_patch"
    tools.mkdir(parents=True)
    backups.mkdir(parents=True)
    (tools / "local_freeze_writer.py").write_text(
        "VALUE = 1\n", encoding="utf-8"
    )
    (ledger / "README.md").write_text(
        "# Freeze blueprint\n", encoding="utf-8"
    )
    (ledger / "manual_docstring_review_state.json").write_text(
        "{}", encoding="utf-8"
    )
    (backups / "old.py.bak").write_text(
        "historical", encoding="utf-8"
    )
    return ledger


def _required_live_files(blueprint: Path) -> tuple[Path, ...]:
    return (
        blueprint / "freeze_tools" / "local_freeze_writer.py",
        blueprint / "README.md",
        blueprint / "manual_docstring_review_state.json",
        blueprint / "_patch_backups",
    )


def validate_freeze_blueprint_policy(project_root: Path) -> None:
    """Validate exact source, evidence, cache, and root classifications."""
    blueprint = project_root / "project_freeze_ledger"
    required = _required_live_files(blueprint)
    _gate(
        "FREEZE_BLUEPRINT_LIVE_OWNER_PRESENT",
        blueprint.is_dir() and all(path.exists() for path in required),
    )
    root_decision = classify_tool_source_path(project_root, blueprint)
    source_decision = classify_tool_source_path(project_root, required[0])
    readme_decision = classify_tool_source_path(project_root, required[1])
    state_decision = classify_tool_source_path(project_root, required[2])
    backup_decision = classify_tool_source_path(project_root, required[3])
    _gate(
        "FREEZE_BLUEPRINT_TOOL_SOURCE_CLASSIFIED",
        root_decision.classification
        is ToolPathClassification.CANONICAL_TOOL_SOURCE
        and source_decision.classification
        is ToolPathClassification.CANONICAL_TOOL_SOURCE
        and readme_decision.classification
        is ToolPathClassification.PACKAGED_TOOL_RESOURCE
        and state_decision.classification
        is ToolPathClassification.GENERATED_TOOL_EVIDENCE
        and backup_decision.classification is ToolPathClassification.CACHE
        and root_decision.include_in_tool_archive
        and source_decision.include_in_tool_archive
        and readme_decision.include_in_tool_archive
        and not state_decision.include_in_tool_archive
        and not backup_decision.include_in_tool_archive,
    )


def validate_freeze_blueprint_show_project_exclusion(
    included_paths: Iterable[str],
    excluded_paths: Iterable[str],
) -> None:
    """Require the separate blueprint box to remain outside Project handoffs."""
    included = set(included_paths)
    excluded = set(excluded_paths)
    _gate(
        "FREEZE_BLUEPRINT_SHOW_PROJECT_EXCLUSION_PRESERVED",
        "project_freeze_ledger" in excluded
        and not any(
            path == "project_freeze_ledger"
            or path.startswith("project_freeze_ledger/")
            for path in included
        ),
    )


def _contract_examples() -> tuple[tuple[str, str], ...]:
    """Document the narrow ownership matrix used by policy and tests."""
    return (
        ("project_freeze_ledger", "CANONICAL_TOOL_SOURCE"),
        (
            "project_freeze_ledger/freeze_tools/local_freeze_writer.py",
            "CANONICAL_TOOL_SOURCE",
        ),
        ("project_freeze_ledger/README.md", "PACKAGED_TOOL_RESOURCE"),
        (
            "project_freeze_ledger/manual_docstring_review_state.json",
            "GENERATED_TOOL_EVIDENCE",
        ),
        ("project_freeze_ledger/_patch_backups", "CACHE"),
    )


def _validate_documented_contract_shape() -> None:
    examples = _contract_examples()
    if len(examples) != len({path for path, _ in examples}):
        raise AssertionError("FREEZE_BLUEPRINT_CONTRACT_DUPLICATE_PATH")
    if {classification for _, classification in examples} != {
        "CANONICAL_TOOL_SOURCE",
        "PACKAGED_TOOL_RESOURCE",
        "GENERATED_TOOL_EVIDENCE",
        "CACHE",
    }:
        raise AssertionError("FREEZE_BLUEPRINT_CONTRACT_CLASSIFICATION_SET")


_validate_documented_contract_shape()
