"""Tests for Prompt Library group filtering behavior."""

from __future__ import annotations

from kanda_reasoner_app.prompt_library_gui.group_catalog import (
    filter_items_for_group,
    load_prompt_groups,
)
from kanda_reasoner_app.prompt_library_gui.library_catalog import load_prompt_library_items


def test_every_group_resolves_at_least_one_prompt() -> None:
    """Verify every installed prompt group resolves at least one prompt."""
    items = load_prompt_library_items()
    for group in load_prompt_groups():
        assert filter_items_for_group(group, items), group.group_id


def test_group_filtering_avoids_duplicate_items() -> None:
    """Verify repeated prompt IDs do not duplicate displayed items."""
    items = load_prompt_library_items()
    group = next(item for item in load_prompt_groups() if item.group_id == "domain_special_overlays")
    filtered = filter_items_for_group(group, items)
    relative_paths = [item.relative_path for item in filtered]
    assert len(relative_paths) == len(set(relative_paths))


def test_prompt_library_tools_group_includes_template_blueprint() -> None:
    """Verify prompt-library tools group includes the template blueprint."""
    items = load_prompt_library_items()
    group = next(item for item in load_prompt_groups() if item.group_id == "prompt_library_tools")
    filtered = filter_items_for_group(group, items)
    titles = {item.title for item in filtered}
    assert "Prompt Template Blueprint" in titles


def test_governance_freeze_group_stays_read_only_text_assets() -> None:
    """Verify governance group points to prompt text, not governance files."""
    items = load_prompt_library_items()
    group = next(item for item in load_prompt_groups() if item.group_id == "governance_freeze")
    filtered = filter_items_for_group(group, items)
    assert filtered
    for item in filtered:
        assert "ACTIVE_PROJECT_ GOVERNANCE" not in item.relative_path
        assert item.path.suffix.lower() in {".md", ".txt"}
