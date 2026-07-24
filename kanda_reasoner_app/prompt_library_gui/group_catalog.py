# project-path: kanda_reasoner_app/prompt_library_gui/group_catalog.py
"""Read-only group catalog for the Prompt Library dashboard."""

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

_COLOR_ROLES = (
    "blue",
    "green",
    "gold",
    "orange",
    "purple",
    "red",
    "teal",
    "gray",
    "indigo",
    "cyan",
    "pink",
    "lime",
)


@dataclass(frozen=True)
class PromptGroup:
    """Describe one read-only prompt group shown on the dashboard."""

    group_id: str
    display_name: str
    color_role: str
    description: str
    prompt_ids: tuple[str, ...]
    copy_stack_enabled: bool = True
    open_as_floating_window: bool = True


def prompt_groups_path(root: Path | None = None) -> Path:
    """Return the canonical group catalog, with a legacy fallback."""
    library_root = root or prompt_library_root()
    canonical_path = library_root / "GROUPS" / "PROMPT_GROUPS_DRAFT.json"
    if canonical_path.is_file():
        return canonical_path
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


def _item_prompt_id(item: PromptLibraryItem) -> str:
    """Return the stable prompt identifier for one current catalog item."""
    prompt_id = item.metadata.get("prompt_id")
    if isinstance(prompt_id, str) and prompt_id.strip():
        return prompt_id.strip()
    return item.path.stem


def _items_by_category(
    items: list[PromptLibraryItem],
) -> dict[str, list[PromptLibraryItem]]:
    """Return current prompt items grouped by canonical category."""
    grouped: dict[str, list[PromptLibraryItem]] = {}
    for item in items:
        grouped.setdefault(item.category, []).append(item)
    return grouped


def _ordered_current_prompt_ids(
    raw_prompt_ids: tuple[str, ...],
    current_items: list[PromptLibraryItem],
) -> tuple[str, ...]:
    """Prune stale IDs and append current prompts missing from the registry."""
    current_by_id = {
        _normalize_identifier(_item_prompt_id(item)): _item_prompt_id(item)
        for item in current_items
    }
    result: list[str] = []
    seen: set[str] = set()

    for prompt_id in raw_prompt_ids:
        normalized = _normalize_identifier(prompt_id)
        current_id = current_by_id.get(normalized)
        if current_id is None or normalized in seen:
            continue
        result.append(current_id)
        seen.add(normalized)

    for item in current_items:
        prompt_id = _item_prompt_id(item)
        normalized = _normalize_identifier(prompt_id)
        if normalized in seen:
            continue
        result.append(prompt_id)
        seen.add(normalized)

    return tuple(result)


def _friendly_group_name(group_id: str) -> str:
    """Return a readable fallback title for a canonical folder identifier."""
    value = group_id
    if len(value) > 3 and value[:2].isdigit() and value[2] == "_":
        value = value[3:]
    return value.replace("_", " ").title()


def _load_canonical_groups(
    path: Path,
    data: dict[str, object],
    items: list[PromptLibraryItem],
) -> list[PromptGroup]:
    """Load canonical groups and reconcile them with current prompt files."""
    groups_value = data.get("groups")
    if not isinstance(groups_value, list):
        return []

    current_by_category = _items_by_category(items)
    groups: list[PromptGroup] = []
    seen: set[str] = set()

    for index, raw_group in enumerate(groups_value):
        if not isinstance(raw_group, dict):
            continue
        group_id = str(raw_group.get("group_id", "")).strip()
        display_name = str(raw_group.get("display_name", "")).strip()
        description = str(raw_group.get("description", "")).strip()
        if not group_id or group_id in seen:
            continue
        seen.add(group_id)
        current_items = current_by_category.get(group_id, [])
        prompt_ids = _ordered_current_prompt_ids(
            _as_string_list(raw_group.get("prompt_ids")),
            current_items,
        )
        color_role = str(raw_group.get("color_role", "")).strip()
        if not color_role:
            color_role = _COLOR_ROLES[index % len(_COLOR_ROLES)]
        groups.append(
            PromptGroup(
                group_id=group_id,
                display_name=display_name or _friendly_group_name(group_id),
                color_role=color_role,
                description=description or "Current prompts in " + group_id + ".",
                prompt_ids=prompt_ids,
                copy_stack_enabled=bool(raw_group.get("copy_stack_enabled", True)),
                open_as_floating_window=bool(
                    raw_group.get("open_as_floating_window", True)
                ),
            )
        )

    for group_id in sorted(current_by_category):
        if group_id in seen or group_id == "root":
            continue
        index = len(groups)
        current_items = current_by_category[group_id]
        groups.append(
            PromptGroup(
                group_id=group_id,
                display_name=_friendly_group_name(group_id),
                color_role=_COLOR_ROLES[index % len(_COLOR_ROLES)],
                description="Current prompts discovered in " + group_id + ".",
                prompt_ids=tuple(_item_prompt_id(item) for item in current_items),
            )
        )

    return groups


def _load_legacy_groups(data: dict[str, object]) -> list[PromptGroup]:
    """Load the package compatibility group catalog without reinterpretation."""
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
        color_role = str(raw_group.get("color_role", "neutral")).strip()
        description = str(raw_group.get("description", "")).strip()
        prompt_ids = _as_string_list(raw_group.get("prompt_ids"))
        if not group_id or not display_name or group_id in seen:
            continue
        seen.add(group_id)
        groups.append(
            PromptGroup(
                group_id=group_id,
                display_name=display_name,
                color_role=color_role or "neutral",
                description=description,
                prompt_ids=prompt_ids,
                copy_stack_enabled=bool(raw_group.get("copy_stack_enabled", True)),
                open_as_floating_window=bool(
                    raw_group.get("open_as_floating_window", True)
                ),
            )
        )
    return groups


def load_prompt_groups(root: Path | None = None) -> list[PromptGroup]:
    """Load current prompt groups from canonical source or legacy fallback."""
    library_root = root or prompt_library_root()
    path = prompt_groups_path(library_root)
    data = _load_json_object(path)
    if path.parent.name == "GROUPS":
        items = load_prompt_library_items(library_root)
        return _load_canonical_groups(path, data, items)
    return _load_legacy_groups(data)


def _item_identifier_values(item: PromptLibraryItem) -> set[str]:
    """Return normalized identifier values for an item."""
    values = {item.relative_path, item.path.stem}
    for key in ("prompt_id", "display_name"):
        value = item.metadata.get(key)
        if isinstance(value, str) and value.strip():
            values.add(value.strip())
    return {_normalize_identifier(value) for value in values if value}


def filter_items_for_group(
    group: PromptGroup,
    items: list[PromptLibraryItem] | None = None,
    root: Path | None = None,
) -> list[PromptLibraryItem]:
    """Return prompt-library items for one group in catalog order."""
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
    """Build copyable text containing all prompts in a group."""
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
                item.path.read_text(
                    encoding="utf-8",
                    errors="replace",
                ).rstrip(),
                "",
            ]
        )
    return "\n".join(sections).rstrip() + "\n"
