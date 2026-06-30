# project-path: kanda_reasoner_app/freeze_after_update/paths.py
"""Path helpers for the external Freeze Feature After Update state box."""

from __future__ import annotations


__all__ = [
    'build_paths',
    'FreezeAfterUpdatePaths',
    'legacy_box_root',
    'normalize_project_root',
    'relative_to_project',
]
from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_project_freeze_after_update_dir,
    legacy_project_freeze_after_update_dir,
)


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
    legacy_box_root: Path
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


def legacy_box_root(project_root: Path | str) -> Path:
    """Return the legacy in-source freeze box path."""
    return legacy_project_freeze_after_update_dir(project_root)


def build_paths(project_root: Path | str) -> FreezeAfterUpdatePaths:
    """Build all public box paths for a project root.

    New writes resolve to the external project-support root:
    ``<drive>/<project>_show_project_to_AI/project_freeze_after_update``.
    The legacy in-source path is kept only for migration and compatibility
    checks, not for new writes.
    """
    root = normalize_project_root(project_root)
    box_root = analysis_project_freeze_after_update_dir(root)
    memory_root = box_root / MEMORY_DIR_NAME
    entries_root = memory_root / ENTRIES_DIR_NAME
    send_root = box_root / SEND_DIR_NAME
    return FreezeAfterUpdatePaths(
        project_root=root,
        box_root=box_root,
        legacy_box_root=legacy_box_root(root),
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
    """Return a stable logical project-freeze relative path when possible."""
    resolved = path.resolve(strict=False)
    paths = build_paths(project_root)
    try:
        rel_to_box = resolved.relative_to(paths.box_root.resolve(strict=False))
        return Path(BOX_DIR_NAME) / rel_to_box
    except Exception:
        pass
    try:
        return resolved.relative_to(project_root.resolve(strict=False))
    except Exception:
        return path
