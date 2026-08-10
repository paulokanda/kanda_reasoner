"""Route live workspace paths before Tool archive classification.

Release 3 distinguishes the mutable developer workspace from the archive
candidate set.  Existing generated-output, cache, VCS, Portable-distribution,
and Project exclusion policies route paths out of the source archive before
the strict Tool-source classifier is consulted.  Every path receives one
routing decision, while only archive candidates require a canonical Tool
classification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from kanda_reasoner_app.source_hygiene.tool_archive_policy import (
    ToolArchiveDecision,
    ToolArchivePolicyError,
    ToolPathClassification,
    inspect_tool_archive_candidate,
)

from .generated_archive_policy import classify_generated_project_archive
from .schema_models import ExclusionRules, ProjectContext
from .source_tree_exporter_shared import (
    _ALWAYS_EXCLUDED_DIRS,
    _ALWAYS_EXCLUDED_EXTENSIONS,
    _ALWAYS_EXCLUDED_FILES,
    _excluded_by_project_rules,
    _exclusion_record,
    _is_generated_output_path,
)

__all__ = [
    "SourceArchiveRouteDecision",
    "SourceArchiveRouteKind",
    "route_builtin_source_archive_entry",
    "route_source_archive_entry",
]


class SourceArchiveRouteKind(str, Enum):
    """Final routing states for one live workspace path."""

    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class SourceArchiveRouteDecision:
    """Describe how one live path reaches or bypasses archive classification."""

    relative_path: str
    route: SourceArchiveRouteKind
    route_owner: str
    reason_code: str
    reason: str
    matched_rule: str
    tool_decision: ToolArchiveDecision | None = None
    exclusion_record: dict[str, Any] | None = None
    error: str = ""

    @property
    def archive_candidate(self) -> bool:
        """Return whether this path reached strict Tool classification."""
        return self.tool_decision is not None

    @property
    def include_in_archive(self) -> bool:
        """Return whether this path is an approved archive candidate."""
        return self.route is SourceArchiveRouteKind.INCLUDE


def _relative(entry: Path, context: ProjectContext) -> str:
    try:
        return entry.resolve(strict=False).relative_to(
            context.root.resolve(strict=False)
        ).as_posix()
    except ValueError:
        return str(entry).replace("\\", "/")


def _excluded(
    entry: Path,
    context: ProjectContext,
    *,
    route_owner: str,
    reason_code: str,
    reason: str,
    matched_rule: str,
    record: dict[str, Any] | None = None,
    tool_decision: ToolArchiveDecision | None = None,
) -> SourceArchiveRouteDecision:
    exclusion = record or _exclusion_record(
        entry,
        context,
        reason_code=reason_code,
        reason=reason,
        path_type="directory" if entry.is_dir() else "file",
        matched_rule=matched_rule,
    )
    return SourceArchiveRouteDecision(
        relative_path=_relative(entry, context),
        route=SourceArchiveRouteKind.EXCLUDE,
        route_owner=route_owner,
        reason_code=reason_code,
        reason=reason,
        matched_rule=matched_rule,
        tool_decision=tool_decision,
        exclusion_record=exclusion,
    )


def _route_builtin(
    entry: Path,
    context: ProjectContext,
    output_dir: Path,
) -> SourceArchiveRouteDecision | None:
    """Apply deterministic noncandidate routing shared by source export."""
    name = entry.name
    if entry.is_symlink():
        return _excluded(
            entry,
            context,
            route_owner="builtin_archive_policy",
            reason_code="symlink_unsupported",
            reason=(
                "Symbolic links are skipped to keep cross-platform "
                "reconstruction deterministic."
            ),
            matched_rule="symlink",
        )
    if _is_generated_output_path(entry, context, output_dir):
        return _excluded(
            entry,
            context,
            route_owner="generated_output_policy",
            reason_code="recursive_output_guard",
            reason=(
                "Generated Show Project to AI output folders are excluded "
                "before Tool archive classification."
            ),
            matched_rule="show_project_to_AI_output",
        )
    if entry.is_dir() and name in _ALWAYS_EXCLUDED_DIRS:
        return _excluded(
            entry,
            context,
            route_owner="builtin_archive_policy",
            reason_code="standard_noise_directory",
            reason=(
                "Standard VCS/cache/build/runtime directory excluded from "
                "the archive candidate set."
            ),
            matched_rule=name,
        )
    if entry.is_file() and name in _ALWAYS_EXCLUDED_FILES:
        return _excluded(
            entry,
            context,
            route_owner="builtin_archive_policy",
            reason_code="os_junk_file",
            reason="Operating-system metadata is outside the archive candidate set.",
            matched_rule=name,
        )
    if entry.is_file() and entry.suffix.lower() in _ALWAYS_EXCLUDED_EXTENSIONS:
        return _excluded(
            entry,
            context,
            route_owner="builtin_archive_policy",
            reason_code="compiled_runtime_artifact",
            reason="Compiled or runtime artifacts are outside the archive candidate set.",
            matched_rule=entry.suffix.lower(),
        )
    archive_record = classify_generated_project_archive(entry, context)
    if archive_record is not None:
        return _excluded(
            entry,
            context,
            route_owner="generated_archive_policy",
            reason_code=archive_record.reason_code,
            reason=archive_record.reason,
            matched_rule=archive_record.matched_rule,
        )
    return None


def route_builtin_source_archive_entry(
    entry: str | Path,
    context: ProjectContext,
    output_dir: str | Path,
) -> SourceArchiveRouteDecision | None:
    """Return the established built-in route for compatibility callers.

    Older source-export facades import ``_excluded_by_builtin_policy`` from
    the inventory module.  The inventory facade delegates here so built-in
    routing has one implementation owner after Release 3.
    """
    candidate = Path(entry)
    output_path = Path(output_dir).expanduser().resolve(strict=False)
    return _route_builtin(candidate, context, output_path)


def _route_project_exclusion(
    entry: Path,
    context: ProjectContext,
    rules: ExclusionRules,
) -> SourceArchiveRouteDecision | None:
    record = _excluded_by_project_rules(entry, context, rules)
    if record is None:
        return None
    return _excluded(
        entry,
        context,
        route_owner="project_exclusion_policy",
        reason_code=str(record.get("reason_code", "project_exclusion_rule")),
        reason=str(record.get("reason", "Matched Project exclusion policy.")),
        matched_rule=str(record.get("matched_rule", "")),
        record=record,
    )


def _tool_exclusion_code(classification: ToolPathClassification) -> str:
    return {
        ToolPathClassification.GENERATED_TOOL_EVIDENCE: "generated_tool_evidence",
        ToolPathClassification.PROJECT_CAPTURE_FORBIDDEN: "project_capture_forbidden",
        ToolPathClassification.CACHE: "tool_cache",
        ToolPathClassification.TRANSIENT: "tool_transient",
    }.get(classification, "tool_archive_classification_excluded")


def route_source_archive_entry(
    entry: str | Path,
    context: ProjectContext,
    output_dir: str | Path,
    rules: ExclusionRules,
    *,
    tool_hygiene_active: bool,
) -> SourceArchiveRouteDecision:
    """Route one path through exclusions, then strict Tool classification.

    Precedence is deliberate: recognized noncandidate paths are pruned before
    classification.  A path that remains eligible for a KANDA Tool archive
    must have an explicit Tool classification or the route is BLOCK.
    """
    candidate = Path(entry)
    output_path = Path(output_dir).expanduser().resolve(strict=False)
    builtin = _route_builtin(candidate, context, output_path)
    if builtin is not None:
        return builtin
    project = _route_project_exclusion(candidate, context, rules)
    if project is not None:
        return project
    if not tool_hygiene_active:
        return SourceArchiveRouteDecision(
            relative_path=_relative(candidate, context),
            route=SourceArchiveRouteKind.INCLUDE,
            route_owner="project_source_archive",
            reason_code="project_archive_candidate",
            reason="Project path remains after active exclusion policies.",
            matched_rule="project_archive_candidate",
        )
    try:
        decision = inspect_tool_archive_candidate(context.root, candidate)
    except ToolArchivePolicyError as exc:
        return SourceArchiveRouteDecision(
            relative_path=_relative(candidate, context),
            route=SourceArchiveRouteKind.BLOCK,
            route_owner="tool_archive_policy",
            reason_code="unclassified_tool_archive_candidate",
            reason="Archive candidate lacks safe Tool-source provenance.",
            matched_rule="tool_archive_fail_closed",
            error=str(exc),
        )
    if not decision.include_in_tool_archive:
        code = _tool_exclusion_code(decision.classification)
        return _excluded(
            candidate,
            context,
            route_owner="tool_archive_policy",
            reason_code=code,
            reason=decision.reason or "Tool classification excludes this path.",
            matched_rule=decision.matched_rule,
            tool_decision=decision,
        )
    return SourceArchiveRouteDecision(
        relative_path=decision.relative_path,
        route=SourceArchiveRouteKind.INCLUDE,
        route_owner="tool_archive_policy",
        reason_code="classified_tool_archive_candidate",
        reason=decision.reason,
        matched_rule=decision.matched_rule,
        tool_decision=decision,
    )
