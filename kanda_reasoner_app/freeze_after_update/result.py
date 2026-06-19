"""Result objects for the Freeze Feature After Update box."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class FreezeAfterUpdateStatus(Enum):
    """Public status values returned by the freeze-after-update contract."""

    VALID = "valid"
    CREATED = "created"
    UPDATED = "updated"
    PACK_CREATED = "pack_created"
    INCOMPLETE = "incomplete"
    INVALID_PROJECT_ROOT = "invalid_project_root"
    INVALID_BOX_PATH = "invalid_box_path"
    ERROR = "error"


@dataclass(frozen=True)
class FreezeAfterUpdateResult:
    """Public result returned by Freeze Feature After Update operations."""

    status: FreezeAfterUpdateStatus
    project_root: Path | None = None
    box_root: Path | None = None
    message: str = ""
    missing_paths: tuple[Path, ...] = field(default_factory=tuple)
    created_paths: tuple[Path, ...] = field(default_factory=tuple)
    output_zip: Path | None = None
    output_instruction: Path | None = None
    freeze_count: int = 0

    @property
    def ok(self) -> bool:
        """Return True when the operation completed successfully."""
        return self.status in {
            FreezeAfterUpdateStatus.VALID,
            FreezeAfterUpdateStatus.CREATED,
            FreezeAfterUpdateStatus.UPDATED,
            FreezeAfterUpdateStatus.PACK_CREATED,
        }
