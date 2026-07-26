"""Dynamic Project Support workspaces for external AI candidate exchange."""
from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
import shutil

from .workbench_project_support_paths import (
    ai_refactoring_card_exchange_root,
    ai_refactoring_exchange_root,
    exchange_root_blockers,
)

__all__ = [
    "clean_external_ai_exchange_workspace",
    "external_ai_exchange_workspace_root",
]


def external_ai_exchange_workspace_root(
    active_project_root: str | Path,
    project_card_identity: str,
    target_relative_path: str,
) -> Path:
    """Return a short, target-readable workspace path under Project Support."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    target = PurePosixPath(str(target_relative_path).replace("\\", "/"))
    target_stem = _safe_component(target.stem or "target", 48)
    card_token = _short_identity_token(project_card_identity)
    return ai_refactoring_exchange_root(project_root) / f"{target_stem}__{card_token}"


def clean_external_ai_exchange_workspace(
    *,
    active_project_root: str | Path,
    project_card_identity: str,
    target_relative_path: str,
) -> tuple[str, ...]:
    """Remove every generated exchange artifact for one card/target workspace."""
    project_root = Path(active_project_root).expanduser().resolve(strict=True)
    exchange_base = ai_refactoring_exchange_root(project_root).resolve(strict=False)
    current = external_ai_exchange_workspace_root(
        project_root,
        project_card_identity,
        target_relative_path,
    ).resolve(strict=False)
    legacy = ai_refactoring_card_exchange_root(
        project_root,
        project_card_identity,
    ).resolve(strict=False)
    removed: list[str] = []
    seen: set[str] = set()
    for root in (current, legacy):
        key = str(root).casefold()
        if key in seen:
            continue
        seen.add(key)
        blockers = exchange_root_blockers(project_root, root)
        if blockers:
            raise ValueError("AI_EXCHANGE_CLEAN_OWNERSHIP_BLOCKED:" + "|".join(blockers))
        try:
            root.relative_to(exchange_base)
        except ValueError as error:
            raise ValueError("AI_EXCHANGE_CLEAN_OUTSIDE_EXCHANGE_ROOT") from error
        if root == exchange_base:
            raise ValueError("AI_EXCHANGE_CLEAN_BASE_ROOT_FORBIDDEN")
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir(), key=lambda item: item.name.lower()):
            _require_child(child, root)
            removed.append(root.name + "/" + child.name)
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()
    return tuple(removed)


def _short_identity_token(value: str) -> str:
    text = "".join(character for character in str(value or "") if character.isalnum())
    if len(text) >= 12:
        return text[:12].lower()
    return hashlib.sha256(str(value or "").encode("utf-8")).hexdigest()[:12]


def _safe_component(value: str, limit: int) -> str:
    cleaned = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in str(value or "")
    ).strip("_-. ")
    if not cleaned:
        return "target"
    return cleaned[:limit]


def _require_child(path: Path, root: Path) -> None:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError as error:
        raise ValueError("AI_EXCHANGE_CLEAN_CHILD_ESCAPES_ROOT") from error
