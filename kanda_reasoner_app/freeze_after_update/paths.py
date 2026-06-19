"""Path helpers for the project-local Freeze Feature After Update box."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BOX_DIR_NAME = "project_freeze_after_update"
MEMORY_DIR_NAME = "frozen_features_memory"
ENTRIES_DIR_NAME = "entries"
SEND_DIR_NAME = "files_to_send_ai"
FREEZE_INDEX_NAME = "freeze_index.json"
FROZEN_STEPS_NAME = "project_frozen_implemented_steps.md"
ROOT_README_NAME = "README.md"
ENTRIES_README_NAME = "README.md"
SEND_README_NAME = "README.md"
WHAT_TO_SAY_NAME = "what_to_say_to_ai_freeze_feature.md"
PACK_PREFIX = "freeze_feature_ai_send_pack_"
PACK_GLOB = "freeze_feature_ai_send_pack_*.zip"


@dataclass(frozen=True)
class FreezeAfterUpdatePaths:
    """Resolved paths for one project's freeze-after-update box."""

    project_root: Path
    box_root: Path
    memory_root: Path
    entries_root: Path
    send_root: Path
    root_readme: Path
    freeze_index: Path
    frozen_steps: Path
    entries_readme: Path
    send_readme: Path
    what_to_say: Path


def normalize_project_root(project_root: Path | str) -> Path:
    """Return a resolved project root path without creating it."""
    return Path(project_root).expanduser().resolve()


def build_paths(project_root: Path | str) -> FreezeAfterUpdatePaths:
    """Build all public box paths for a project root."""
    root = normalize_project_root(project_root)
    box_root = root / BOX_DIR_NAME
    memory_root = box_root / MEMORY_DIR_NAME
    entries_root = memory_root / ENTRIES_DIR_NAME
    send_root = box_root / SEND_DIR_NAME
    return FreezeAfterUpdatePaths(
        project_root=root,
        box_root=box_root,
        memory_root=memory_root,
        entries_root=entries_root,
        send_root=send_root,
        root_readme=box_root / ROOT_README_NAME,
        freeze_index=memory_root / FREEZE_INDEX_NAME,
        frozen_steps=memory_root / FROZEN_STEPS_NAME,
        entries_readme=entries_root / ENTRIES_README_NAME,
        send_readme=send_root / SEND_README_NAME,
        what_to_say=send_root / WHAT_TO_SAY_NAME,
    )


def relative_to_project(path: Path, project_root: Path) -> Path:
    """Return project-relative path when possible."""
    try:
        return path.resolve().relative_to(project_root.resolve())
    except Exception:
        return path
