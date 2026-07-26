# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_boundary_context.py
"""Immutable Tool-versus-Project boundary context for Project Web AI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from kanda_reasoner_app.project_support_boundary import (
    ProjectSupportBoundaryError,
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.web_ai_provider_contracts import ProjectWebAIRequestIdentity

__all__ = [
    "ProjectAgentBoundaryContext",
    "ProjectAgentBoundaryError",
]

SECOND_PROMPT_FILES_DIR = "second_prompt_files"
PROJECT_ROOT_MARKER = "<PROJECT_ROOT>"
PROJECT_SUPPORT_ROOT_MARKER = "<PROJECT_SUPPORT_ROOT>"
TOOL_SOURCE_ROOT_MARKER = "<TOOL_SOURCE_ROOT>"


class ProjectAgentBoundaryError(RuntimeError):
    """Raised when a Project Web AI request has stale or mixed ownership."""


@dataclass(frozen=True)
class ProjectAgentBoundaryContext:
    """Bind one read-only agent request to current Tool and Project identity."""

    tool_project_slug: str
    tool_source_root: str
    active_project_slug: str
    active_project_root: str
    active_project_support_root: str
    active_project_daily_work_root: str
    active_project_id: str
    active_project_root_fingerprint: str
    same_canonical_resolved_root: bool
    self_hosting_mode: bool
    project_epoch: int
    snapshot_id: str
    context_hash: str

    @classmethod
    def from_request(
        cls,
        project_root: str | Path,
        request: ProjectWebAIRequestIdentity,
    ) -> "ProjectAgentBoundaryContext":
        """Resolve current identity and require an exact request-bound match."""
        try:
            identity = resolve_project_tool_boundary_identity(project_root)
        except ProjectSupportBoundaryError as exc:
            raise ProjectAgentBoundaryError(str(exc)) from exc
        checks = (
            (request.project_id, identity.active_project_id, "PROJECT_ID"),
            (
                request.project_slug,
                identity.active_project_slug,
                "PROJECT_SLUG",
            ),
            (
                request.project_root_fingerprint,
                identity.active_project_root_fingerprint,
                "PROJECT_ROOT_FINGERPRINT",
            ),
            (
                _path_key(request.support_root),
                _path_key(identity.active_project_support_root),
                "PROJECT_SUPPORT_ROOT",
            ),
        )
        for expected, actual, label in checks:
            if str(expected) != str(actual):
                raise ProjectAgentBoundaryError(
                    "PROJECT_AGENT_BOUNDARY_IDENTITY_MISMATCH:" + label
                )
        if request.project_epoch < 0 or not request.snapshot_id or not request.context_hash:
            raise ProjectAgentBoundaryError(
                "PROJECT_AGENT_REQUEST_IDENTITY_INCOMPLETE"
            )
        return cls(
            tool_project_slug=identity.tool_project_slug,
            tool_source_root=str(identity.tool_source_root),
            active_project_slug=identity.active_project_slug,
            active_project_root=str(identity.active_project_root),
            active_project_support_root=str(identity.active_project_support_root),
            active_project_daily_work_root=str(
                identity.active_project_daily_work_root
            ),
            active_project_id=identity.active_project_id,
            active_project_root_fingerprint=(
                identity.active_project_root_fingerprint
            ),
            same_canonical_resolved_root=(
                identity.same_canonical_resolved_root
            ),
            self_hosting_mode=identity.self_hosting_mode,
            project_epoch=request.project_epoch,
            snapshot_id=request.snapshot_id,
            context_hash=request.context_hash,
        )

    def prompt_contract(self) -> str:
        """Return authoritative dynamic path semantics without local path leakage."""
        support_name = self.active_project_slug + "_show_project_to_AI"
        return (
            "KANDA TOOL VERSUS PROJECT BOUNDARY\n"
            "The active Project source and Project Support are two separate "
            "folders. Never join Project Support beneath the Project source.\n"
            "Active Project marker: " + PROJECT_ROOT_MARKER + "\n"
            "Active Project folder name: " + self.active_project_slug + "\n"
            "Project Support marker: " + PROJECT_SUPPORT_ROOT_MARKER + "\n"
            "Project Support folder name: " + support_name + "\n"
            "Dynamic Project Support contract: "
            "<project_drive>:\\<project_name>_show_project_to_AI\n"
            "Second-prompt folder: " + PROJECT_SUPPORT_ROOT_MARKER
            + "\\" + SECOND_PROMPT_FILES_DIR + "\n"
            "Tool source marker: " + TOOL_SOURCE_ROOT_MARKER + "\n"
            "Tool project slug: " + self.tool_project_slug + "\n"
            "Self-hosting mode: "
            + ("YES" if self.self_hosting_mode else "NO")
            + "\n"
            "If self-hosting is YES, Tool and Project may share a physical "
            "root, but their logical ownership remains separate.\n"
            "Manifest paths beginning with show_project_to_AI/ are stable "
            "logical evidence prefixes. They do not mean that a physical "
            "show_project_to_AI folder exists inside " + PROJECT_ROOT_MARKER
            + ".\nForbidden physical forms include " + PROJECT_ROOT_MARKER
            + "\\show_project_to_AI and " + PROJECT_ROOT_MARKER + "\\"
            + support_name + ".\n"
            "Project epoch: " + str(self.project_epoch) + "\n"
            "Snapshot identity: " + self.snapshot_id[:16] + "\n"
            "This identity is immutable for the current request. A Project "
            "switch invalidates it before another tool call may be accepted."
        )

    def tool_payload(self) -> Mapping[str, object]:
        """Return bounded non-secret identity facts for the remote model."""
        support_name = self.active_project_slug + "_show_project_to_AI"
        return {
            "tool_project_slug": self.tool_project_slug,
            "tool_source_root_marker": TOOL_SOURCE_ROOT_MARKER,
            "active_project_slug": self.active_project_slug,
            "active_project_root_marker": PROJECT_ROOT_MARKER,
            "active_project_folder_name": self.active_project_slug,
            "project_support_root_marker": PROJECT_SUPPORT_ROOT_MARKER,
            "project_support_folder_name": support_name,
            "project_support_relationship": "SEPARATE_EXTERNAL_FOLDER",
            "dynamic_support_contract": (
                "<project_drive>:\\<project_name>_show_project_to_AI"
            ),
            "second_prompt_files": (
                PROJECT_SUPPORT_ROOT_MARKER + "\\" + SECOND_PROMPT_FILES_DIR
            ),
            "logical_manifest_prefix": "show_project_to_AI/",
            "logical_prefix_is_physical_child": False,
            "forbidden_nested_forms": [
                PROJECT_ROOT_MARKER + "\\show_project_to_AI",
                PROJECT_ROOT_MARKER + "\\" + support_name,
            ],
            "same_canonical_resolved_tool_project_root": (
                self.same_canonical_resolved_root
            ),
            "self_hosting_mode": self.self_hosting_mode,
            "logical_ownership_collapsed": False,
            "project_epoch": self.project_epoch,
            "snapshot_id_prefix": self.snapshot_id[:16],
            "project_support_read_authority": False,
            "project_source_read_authority": True,
        }


def _path_key(path: str | Path) -> str:
    """Return one platform-aware canonical path comparison key."""
    return os.path.normcase(str(Path(path).expanduser().resolve(strict=False)))
