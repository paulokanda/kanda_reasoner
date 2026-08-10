# project-path: kanda_reasoner_app/_project_fire_shield_types.py
"""Internal value types for the public Fire Shield facade."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from kanda_reasoner_app.project_operation_authority import ProjectOperationAuthority
from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

__all__: tuple[str, ...] = ()


class FireShieldError(RuntimeError):
    """Raised when a Fire Shield invariant is not provably safe."""


class FireShieldMode(str, Enum):
    """Resolved Fire Shield operating modes."""

    EXTERNAL_PROJECT = "EXTERNAL_PROJECT"
    KANDA_SELF_HOSTING = "KANDA_SELF_HOSTING"


class FireShieldPhase(str, Enum):
    """Lifecycle phases with distinct write ownership."""

    PROJECT_SOURCE_MUTATION = "PROJECT_SOURCE_MUTATION"
    PROJECT_TRANSIENT_WRITE = "PROJECT_TRANSIENT_WRITE"
    FREEZE_WRITE = "FREEZE_WRITE"
    ERROR_MEMORY_WRITE = "ERROR_MEMORY_WRITE"
    VALIDATE_READ_ONLY = "VALIDATE_READ_ONLY"


@dataclass(frozen=True)
class ToolFileState:
    """Stable content and physical identity for one protected Tool file."""

    relative_path: str
    size: int
    sha256: str
    device: int
    inode: int


@dataclass(frozen=True)
class ToolSnapshot:
    """Immutable protected Tool source snapshot."""

    tool_root: Path
    entries: tuple[ToolFileState, ...]
    digest_sha256: str


@dataclass(frozen=True)
class FireShieldContext:
    """One immutable Fire Shield authority for a governed operation."""

    boundary: ProjectToolBoundaryIdentity
    authority: ProjectOperationAuthority
    mode: FireShieldMode
    phase: FireShieldPhase
    operation_id: str
    allowed_write_root: Path
    writes_allowed: bool
    tool_snapshot: ToolSnapshot | None
    registry_path: Path | None

    def markers(self) -> tuple[str, ...]:
        """Return stable evidence markers for this resolved context."""
        if self.tool_snapshot is not None:
            pre_state = "FIRE_SHIELD_TOOL_PRE_STATE_CAPTURED: PASS"
        elif self.mode == FireShieldMode.KANDA_SELF_HOSTING:
            pre_state = "FIRE_SHIELD_TOOL_PRE_STATE_CAPTURED: N/A_SELF_HOSTING"
        else:
            pre_state = "FIRE_SHIELD_TOOL_PRE_STATE_CAPTURED: N/A_READ_ONLY"
        return (
            "FIRE_SHIELD_MODE: " + self.mode.value,
            "FIRE_SHIELD_PROJECT_IDENTITY_VERIFIED: PASS",
            "FIRE_SHIELD_TOOL_IDENTITY_VERIFIED: PASS",
            "FIRE_SHIELD_TOOL_ROOT_PROTECTED: PASS",
            "FIRE_SHIELD_PROJECT_WRITE_ZONES_VERIFIED: PASS",
            pre_state,
        )


@dataclass(frozen=True)
class FireShieldArchiveReport:
    """Deterministic package preflight evidence."""

    archive_path: Path
    member_count: int
    project_payload_count: int
    delivery_control_count: int
    freeze_hint_count: int
    transient_evidence_count: int
    tool_source_transfer_count: int
    private_tool_import_count: int
