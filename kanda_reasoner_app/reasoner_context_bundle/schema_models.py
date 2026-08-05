# project-path: kanda_reasoner_app/reasoner_context_bundle/schema_models.py
"""Data models for the reasoner context bundle box.

The models in this module are intentionally small contracts shared by the
bundle builders. They do not generate files and do not modify other boxes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "BundleArtifactPaths",
    "ExclusionDecision",
    "ExclusionRules",
    "ProjectContext",
]


@dataclass(frozen=True)
class ProjectContext:
    """Resolved dynamic context for one active project."""

    root: Path
    project_slug: str
    evidence_root: Path
    json_complete_dir: Path
    active_project_id: str
    active_project_root_fingerprint: str
    tool_project_slug: str = "kanda_reasoner"
    tool_source_root: Path = Path(".")
    active_project_support_root: Path = Path(".")
    active_project_daily_work_root: Path = Path(".")
    selection_mode: str = "EXPLICIT_EXTERNAL_PROJECT"
    same_canonical_resolved_root: bool = False
    self_hosting_mode: bool = False

    def as_dict(self) -> dict[str, str]:
        """Return a JSON-friendly representation of the project context."""
        return {
            "root": str(self.root),
            "project_slug": self.project_slug,
            "evidence_root": str(self.evidence_root),
            "json_complete_dir": str(self.json_complete_dir),
            "active_project_id": self.active_project_id,
            "active_project_root_fingerprint": self.active_project_root_fingerprint,
            "tool_project_slug": self.tool_project_slug,
            "tool_source_root": str(self.tool_source_root),
            "active_project_support_root": str(
                self.active_project_support_root
            ),
            "active_project_daily_work_root": str(
                self.active_project_daily_work_root
            ),
            "selection_mode": self.selection_mode,
            "same_canonical_resolved_root": (
                self.same_canonical_resolved_root
            ),
            "self_hosting_mode": self.self_hosting_mode,
        }


@dataclass(frozen=True)
class ExclusionRules:
    """Normalized active project exclusion rules."""

    folders: tuple[str, ...]
    files: tuple[str, ...]
    extensions: tuple[str, ...]
    source: str

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation of the rules."""
        return {
            "folders": list(self.folders),
            "files": list(self.files),
            "extensions": list(self.extensions),
            "source": self.source,
        }


@dataclass(frozen=True)
class ExclusionDecision:
    """Include/exclude decision for one project-relative path."""

    path: str
    included: bool
    excluded: bool
    matched_rule: str
    rule_type: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly decision record."""
        return {
            "path": self.path,
            "included": self.included,
            "excluded": self.excluded,
            "matched_rule": self.matched_rule,
            "rule_type": self.rule_type,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class BundleArtifactPaths:
    """Resolved artifact paths for the additive AI context bundle."""

    complete_json: Path
    ai_briefing_json: Path
    routing_manifest_json: Path
    patch_safety_routes_json: Path
    active_snapshot_json: Path
    file_manifest_json: Path
    exclusion_rules_json: Path
    validation_state_json: Path
    reconstruction_payload_json: Path
    bundle_manifest_json: Path

    def as_dict(self) -> dict[str, str]:
        """Return artifact paths keyed by stable artifact name."""
        return {
            "complete_json": str(self.complete_json),
            "ai_briefing_json": str(self.ai_briefing_json),
            "routing_manifest_json": str(self.routing_manifest_json),
            "patch_safety_routes_json": str(self.patch_safety_routes_json),
            "active_snapshot_json": str(self.active_snapshot_json),
            "file_manifest_json": str(self.file_manifest_json),
            "exclusion_rules_json": str(self.exclusion_rules_json),
            "validation_state_json": str(self.validation_state_json),
            "reconstruction_payload_json": str(self.reconstruction_payload_json),
            "bundle_manifest_json": str(self.bundle_manifest_json),
        }

    def required_paths(self) -> list[Path]:
        """Return the required JSON artifact paths in generation order."""
        return [
            self.ai_briefing_json,
            self.routing_manifest_json,
            self.patch_safety_routes_json,
            self.file_manifest_json,
            self.exclusion_rules_json,
            self.validation_state_json,
            self.bundle_manifest_json,
        ]
