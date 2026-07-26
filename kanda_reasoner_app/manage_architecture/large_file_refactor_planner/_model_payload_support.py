# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/_model_payload_support.py
"""Private payload and path support for planner data contracts.

This module owns serialization details and stable path normalization only. It
must not own public planner models or import the public ``models`` facade.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Protocol, TypeVar

__all__: list[str] = []

_CandidateT = TypeVar("_CandidateT")


class _DictReady(Protocol):
    """Structural contract for nested planner values."""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready mapping."""


class _ModuleAnalysisLike(Protocol):
    """Fields required to serialize an analysis report."""

    imports: list[_DictReady]
    symbols: list[_DictReady]


class _PreviewBundleLike(Protocol):
    """Fields required to serialize a preview bundle."""

    files: list[_DictReady]


class _ImportMigrationLike(Protocol):
    """Fields required to serialize an import-migration preview."""

    records: list[_DictReady]


class _RefactorPlanLike(Protocol):
    """Fields required to serialize a deterministic refactor plan."""

    symbols: list[_DictReady]
    proposed_modules: list[_DictReady]
    docstring_proposals: list[_DictReady]


def _plain_payload(value: object) -> dict[str, Any]:
    """Return the recursive dataclass representation of one model."""
    return asdict(value)


def _module_analysis_payload(
    report: _ModuleAnalysisLike,
) -> dict[str, Any]:
    """Build nested JSON data for one module-analysis report."""
    data = asdict(report)
    data["imports"] = [item.to_dict() for item in report.imports]
    data["symbols"] = [item.to_dict() for item in report.symbols]
    return data


def _preview_bundle_payload(
    bundle: _PreviewBundleLike,
) -> dict[str, Any]:
    """Build nested JSON data for one no-write preview bundle."""
    data = asdict(bundle)
    data["files"] = [item.to_dict() for item in bundle.files]
    return data


def _import_migration_payload(
    preview: _ImportMigrationLike,
) -> dict[str, Any]:
    """Build nested JSON data for one import-migration preview."""
    data = asdict(preview)
    data["records"] = [item.to_dict() for item in preview.records]
    return data


def _refactor_plan_payload(
    plan: _RefactorPlanLike,
) -> dict[str, Any]:
    """Build nested JSON data for one deterministic refactor plan."""
    data = asdict(plan)
    data["symbols"] = [item.to_dict() for item in plan.symbols]
    data["proposed_modules"] = [
        item.to_dict() for item in plan.proposed_modules
    ]
    data["docstring_proposals"] = [
        item.to_dict() for item in plan.docstring_proposals
    ]
    return data


def _blocked_candidate(
    candidate_type: type[_CandidateT],
    schema_version: str,
    path: Path,
    root: Path,
    line_count: int,
    reason: str,
    suggested_action: str,
) -> _CandidateT:
    """Build a blocked large-file candidate through its public class."""
    values: dict[str, Any] = {
        "schema_version": schema_version,
        "path": str(path),
        "relative_path": _stable_relative_path(path, root),
        "line_count_physical": line_count,
        "risk_flags": [reason],
        "is_eligible": False,
        "blocked_reason": reason,
        "suggested_action": suggested_action,
    }
    return candidate_type(**values)


def _stable_relative_path(path: Path, root: Path) -> str:
    """Return a project-relative path or a normalized absolute fallback."""
    resolved_path = path.resolve()
    resolved_root = root.resolve()
    try:
        selected = resolved_path.relative_to(resolved_root)
    except ValueError:
        selected = resolved_path
    return str(selected).replace("\\", "/")
