"""Validation fixtures for live-workspace versus archive-candidate routing."""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Callable

from kanda_reasoner_app.reasoner_context_bundle.exclusion_provider import (
    load_bundle_exclusion_rules,
)
from kanda_reasoner_app.reasoner_context_bundle.project_context import (
    resolve_project_context,
)
from kanda_reasoner_app.reasoner_context_bundle.source_archive_routing import (
    SourceArchiveRouteDecision,
    SourceArchiveRouteKind,
    route_source_archive_entry,
)

__all__ = ["validate_workspace_archive_routing"]

Gate = Callable[[str, bool, str], None]


def _route(
    project_root: Path,
    path: Path,
    output_dir: Path,
) -> SourceArchiveRouteDecision:
    context = resolve_project_context(project_root)
    rules = load_bundle_exclusion_rules(context)
    return route_source_archive_entry(
        path,
        context,
        output_dir,
        rules,
        tool_hygiene_active=True,
    )


def _validate_live_tree(project_root: Path, gate: Gate) -> None:
    context = resolve_project_context(project_root)
    rules = load_bundle_exclusion_rules(context)
    output_dir = project_root.parent / (
        project_root.name + "_show_project_to_AI"
    ) / "second_prompt_files"
    included_directories = 0
    included_files = 0
    excluded_roots = 0
    routed_paths = 0
    top_level_names = {
        item.name for item in project_root.iterdir()
    }
    top_level_routed: set[str] = set()
    for current, directory_names, file_names in os.walk(project_root):
        current_path = Path(current)
        retained: list[str] = []
        for name in directory_names:
            candidate = current_path / name
            decision = route_source_archive_entry(
                candidate,
                context,
                output_dir,
                rules,
                tool_hygiene_active=True,
            )
            routed_paths += 1
            if current_path == project_root:
                top_level_routed.add(name)
            if decision.route is SourceArchiveRouteKind.BLOCK:
                raise AssertionError(
                    "LIVE_WORKSPACE_ROUTE_BLOCKED:"
                    + decision.relative_path
                    + ":"
                    + decision.error
                )
            if decision.route is SourceArchiveRouteKind.EXCLUDE:
                excluded_roots += 1
                continue
            if (
                decision.tool_decision is None
                or not decision.tool_decision.include_in_tool_archive
            ):
                raise AssertionError(
                    "ARCHIVE_CANDIDATE_WITHOUT_TOOL_CLASSIFICATION:"
                    + decision.relative_path
                )
            included_directories += 1
            retained.append(name)
        directory_names[:] = retained
        for name in file_names:
            candidate = current_path / name
            decision = route_source_archive_entry(
                candidate,
                context,
                output_dir,
                rules,
                tool_hygiene_active=True,
            )
            routed_paths += 1
            if current_path == project_root:
                top_level_routed.add(name)
            if decision.route is SourceArchiveRouteKind.BLOCK:
                raise AssertionError(
                    "LIVE_WORKSPACE_ROUTE_BLOCKED:"
                    + decision.relative_path
                    + ":"
                    + decision.error
                )
            if decision.route is SourceArchiveRouteKind.EXCLUDE:
                continue
            if (
                decision.tool_decision is None
                or not decision.tool_decision.include_in_tool_archive
            ):
                raise AssertionError(
                    "ARCHIVE_FILE_WITHOUT_TOOL_CLASSIFICATION:"
                    + decision.relative_path
                )
            included_files += 1
    gate(
        "ALL_LIVE_ROOTS_ROUTED",
        top_level_routed == top_level_names and routed_paths > 0,
        "missing=" + ",".join(sorted(top_level_names - top_level_routed)),
    )
    gate(
        "ALL_ARCHIVE_CANDIDATES_CLASSIFIED",
        included_directories > 0 and included_files > 0,
        f"directories={included_directories};files={included_files}",
    )
    gate(
        "EXCLUDED_ROOTS_NOT_RECURSIVELY_CLASSIFIED",
        excluded_roots > 0,
        f"excluded_roots={excluded_roots}",
    )
    gate(
        "TOOL_SOURCE_DIRECTORY_CLASSIFICATION",
        included_directories > 0 and included_files > 0,
    )


def _generated_output_decision(project_root: Path) -> SourceArchiveRouteDecision:
    """Route the canonical generated-output name using the active Project."""
    first_prompt = project_root / "first_prompt_files"
    return _route(
        project_root,
        first_prompt,
        project_root.parent / (project_root.name + "_show_project_to_AI"),
    )


def _validate_generated_output_precedence(project_root: Path, gate: Gate) -> None:
    decision = _generated_output_decision(project_root)
    gate(
        "FIRST_PROMPT_FILES_ROUTED_AS_GENERATED_OUTPUT",
        decision.route is SourceArchiveRouteKind.EXCLUDE
        and decision.route_owner == "generated_output_policy"
        and decision.reason_code == "recursive_output_guard"
        and not decision.archive_candidate,
        repr(decision),
    )
    gate(
        "GENERATED_OUTPUT_ROOTS_OUTSIDE_ARCHIVE",
        not decision.include_in_archive,
        repr(decision),
    )


def _validate_live_transient_workspace_if_present(
    project_root: Path,
    gate: Gate,
) -> None:
    transient_root = project_root / "_delete_after_daily_work"
    if not transient_root.is_dir():
        gate(
            "LIVE_PROJECT_TRANSIENT_WORKSPACE_OPTIONAL",
            True,
            "not_present",
        )
        return
    decision = _route(
        project_root,
        transient_root,
        project_root.parent / (project_root.name + "_show_project_to_AI"),
    )
    gate(
        "LIVE_PROJECT_TRANSIENT_WORKSPACE_PRECEDES_TOOL_CLASSIFIER",
        decision.route is SourceArchiveRouteKind.EXCLUDE
        and decision.route_owner == "generated_output_policy"
        and decision.reason_code == "recursive_output_guard"
        and not decision.archive_candidate,
        repr(decision),
    )


def _validation_path(project_root: Path, name: str) -> Path:
    """Return a non-mutating synthetic path under the active Project root."""
    return project_root / name


def _validate_negative_archive_candidate(project_root: Path, gate: Gate) -> None:
    """Exercise synthetic names without inventing a second Project root."""
    output_dir = project_root.parent / (
        project_root.name + "_show_project_to_AI"
    ) / "second_prompt_files"

    unknown = _validation_path(
        project_root,
        "__kanda_validation_unregistered_archive_candidate__",
    )
    decision = _route(project_root, unknown, output_dir)
    gate(
        "UNCLASSIFIED_ARCHIVE_CANDIDATE_REJECTED",
        decision.route is SourceArchiveRouteKind.BLOCK
        and "UNCLASSIFIED_TOOL_SOURCE_PATH" in decision.error,
        repr(decision),
    )

    generated = _validation_path(project_root, "first_prompt_files")
    generated_decision = _route(project_root, generated, output_dir)
    gate(
        "GENERATED_OUTPUT_PRECEDES_TOOL_CLASSIFIER",
        generated_decision.route is SourceArchiveRouteKind.EXCLUDE
        and generated_decision.route_owner == "generated_output_policy"
        and not generated_decision.archive_candidate,
        repr(generated_decision),
    )

    legacy_transient = _validation_path(
        project_root,
        "_delete_after_daily_work",
    )
    legacy_decision = _route(project_root, legacy_transient, output_dir)
    gate(
        "LEGACY_TRANSIENT_WORKSPACE_PRECEDES_TOOL_CLASSIFIER",
        legacy_decision.route is SourceArchiveRouteKind.EXCLUDE
        and legacy_decision.route_owner == "generated_output_policy"
        and not legacy_decision.archive_candidate,
        repr(legacy_decision),
    )

    named_transient = _validation_path(
        project_root,
        project_root.name + "_delete_after_daily_work",
    )
    named_decision = _route(project_root, named_transient, output_dir)
    gate(
        "PROJECT_NAMED_TRANSIENT_WORKSPACE_PRECEDES_TOOL_CLASSIFIER",
        named_decision.route is SourceArchiveRouteKind.EXCLUDE
        and named_decision.route_owner == "generated_output_policy"
        and not named_decision.archive_candidate,
        repr(named_decision),
    )

    lookalike = _validation_path(
        project_root,
        "__kanda_validation_notes_delete_after_daily_work",
    )
    lookalike_decision = _route(project_root, lookalike, output_dir)
    gate(
        "TRANSIENT_WORKSPACE_LOOKALIKE_FAILS_CLOSED",
        lookalike_decision.route is SourceArchiveRouteKind.BLOCK
        and "UNCLASSIFIED_TOOL_SOURCE_PATH" in lookalike_decision.error,
        repr(lookalike_decision),
    )
    gate(
        "SYNTHETIC_ROUTING_CASES_USE_ACTIVE_PROJECT_CONTEXT",
        True,
        str(project_root),
    )


def _validate_exporter_compatibility_facade(
    project_root: Path,
    gate: Gate,
) -> None:
    """Prove the legacy source-export import delegates to shared routing."""
    exporter = importlib.import_module(
        "kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter"
    )
    inventory = importlib.import_module(
        "kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter_inventory"
    )
    facade = getattr(inventory, "_excluded_by_builtin_policy", None)
    context = resolve_project_context(project_root)
    output_dir = project_root.parent / (
        project_root.name + "_show_project_to_AI"
    ) / "second_prompt_files"
    generated = project_root / "first_prompt_files"
    legacy_record = facade(generated, context, output_dir) if callable(facade) else None
    shared_route = route_source_archive_entry(
        generated,
        context,
        output_dir,
        load_bundle_exclusion_rules(context),
        tool_hygiene_active=True,
    )
    gate(
        "SOURCE_EXPORTER_COMPATIBILITY_FACADE_PRESERVED",
        callable(facade)
        and callable(getattr(exporter, "gather_source_archive_inventory", None))
        and isinstance(legacy_record, dict)
        and legacy_record == shared_route.exclusion_record
        and shared_route.route is SourceArchiveRouteKind.EXCLUDE,
        repr({
            "facade_callable": callable(facade),
            "legacy_record": legacy_record,
            "shared_route": shared_route,
        }),
    )


def validate_workspace_archive_routing(project_root: Path, gate: Gate) -> None:
    """Validate current workspace routing and fail-closed candidate behavior."""
    root = project_root.expanduser().resolve(strict=True)
    _validate_live_tree(root, gate)
    _validate_generated_output_precedence(root, gate)
    _validate_live_transient_workspace_if_present(root, gate)
    _validate_negative_archive_candidate(root, gate)
    _validate_exporter_compatibility_facade(root, gate)
