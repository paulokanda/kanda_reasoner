"""Read-only group catalog for Prompt Library dashboard cards."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .library_catalog import PromptLibraryItem, load_prompt_library_items
from .library_paths import prompt_library_root

__all__ = [
    "PromptGroup",
    "build_group_stack_text",
    "filter_items_for_group",
    "load_prompt_groups",
    "prompt_groups_path",
]


@dataclass(frozen=True)
class PromptGroup:
    """Describe one read-only prompt group shown on the Tab 9 dashboard.

    Attributes:
        group_id: Stable group identifier.
        display_name: User-facing group title.
        color_role: Symbolic color role used by the GUI layer.
        description: Plain-language explanation of the group.
        prompt_ids: Ordered prompt identifiers included in the group.
        copy_stack_enabled: Whether a full-stack copy action is useful.
        open_as_floating_window: Whether the group should open in a window.
    """

    group_id: str
    display_name: str
    color_role: str
    description: str
    prompt_ids: tuple[str, ...]
    copy_stack_enabled: bool = True
    open_as_floating_window: bool = True


def prompt_groups_path(root: Path | None = None) -> Path:
    """Return the package-owned prompt group catalog path."""
    library_root = root or prompt_library_root()
    return library_root / "groups" / "PROMPT_GROUPS.json"


def _as_string_list(value: object) -> tuple[str, ...]:
    """Return a tuple of non-empty strings from a JSON value."""
    if not isinstance(value, list):
        return ()
    result: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return tuple(result)


def _load_json_object(path: Path) -> dict[str, object]:
    """Read a JSON object from a file, returning an empty object on failure."""
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    if isinstance(data, dict):
        return data
    return {}


def load_prompt_groups(root: Path | None = None) -> list[PromptGroup]:
    """Load prompt groups from the package-owned group catalog.

    Args:
        root: Optional prompt_library root override for tests.

    Returns:
        Ordered prompt groups. Missing or invalid catalogs return an empty list.
    """
    path = prompt_groups_path(root)
    data = _load_json_object(path)
    groups_value = data.get("groups")
    if not isinstance(groups_value, list):
        return []

    groups: list[PromptGroup] = []
    seen: set[str] = set()
    for raw_group in groups_value:
        if not isinstance(raw_group, dict):
            continue
        group_id = str(raw_group.get("group_id", "")).strip()
        display_name = str(raw_group.get("display_name", "")).strip()
        color_role = str(raw_group.get("color_role", "neutral")).strip() or "neutral"
        description = str(raw_group.get("description", "")).strip()
        prompt_ids = _as_string_list(raw_group.get("prompt_ids"))
        if not group_id or not display_name or group_id in seen:
            continue
        seen.add(group_id)
        groups.append(
            PromptGroup(
                group_id=group_id,
                display_name=display_name,
                color_role=color_role,
                description=description,
                prompt_ids=prompt_ids,
                copy_stack_enabled=bool(raw_group.get("copy_stack_enabled", True)),
                open_as_floating_window=bool(raw_group.get("open_as_floating_window", True)),
            )
        )
    return groups


def _item_identifier_values(item: PromptLibraryItem) -> set[str]:
    """Return normalized identifier values for an item."""
    values = {item.relative_path, item.path.stem}
    for key in ("prompt_id", "display_name"):
        value = item.metadata.get(key)
        if isinstance(value, str) and value.strip():
            values.add(value.strip())
    return {_normalize_identifier(value) for value in values if value}


def _normalize_identifier(value: str) -> str:
    """Normalize user-facing or metadata identifiers for matching."""
    chars: list[str] = []
    last_was_sep = False
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
            last_was_sep = False
        elif not last_was_sep:
            chars.append("_")
            last_was_sep = True
    return "".join(chars).strip("_")


def filter_items_for_group(
    group: PromptGroup,
    items: list[PromptLibraryItem] | None = None,
    root: Path | None = None,
) -> list[PromptLibraryItem]:
    """Return prompt-library items for one group in catalog order.

    Args:
        group: Group descriptor.
        items: Optional preloaded items.
        root: Optional prompt_library root override if items are not supplied.

    Returns:
        Items whose identifiers match the group's prompt_ids, ordered by prompt_ids.
    """
    available_items = items if items is not None else load_prompt_library_items(root)
    index: dict[str, PromptLibraryItem] = {}
    for item in available_items:
        for identifier in _item_identifier_values(item):
            index.setdefault(identifier, item)

    result: list[PromptLibraryItem] = []
    added: set[str] = set()
    for prompt_id in group.prompt_ids:
        normalized_id = _normalize_identifier(prompt_id)
        item = index.get(normalized_id)
        if item is None:
            continue
        if item.relative_path in added:
            continue
        result.append(item)
        added.add(item.relative_path)
    return result


def build_group_stack_text(group: PromptGroup, items: list[PromptLibraryItem]) -> str:
    """Build copyable text containing all prompts in a group.

    Args:
        group: Group descriptor.
        items: Items to include in the stack.

    Returns:
        Plain text with deterministic separators and prompt contents.
    """
    sections = [
        "PROMPT GROUP: " + group.display_name,
        "GROUP ID: " + group.group_id,
        "DESCRIPTION: " + group.description,
        "",
    ]
    for index, item in enumerate(items, start=1):
        sections.extend(
            [
                "=" * 78,
                "PROMPT " + str(index) + ": " + item.title,
                "PATH: " + item.relative_path,
                "=" * 78,
                item.path.read_text(encoding="utf-8", errors="replace").rstrip(),
                "",
            ]
        )
    return "\n".join(sections).rstrip() + "\n"
