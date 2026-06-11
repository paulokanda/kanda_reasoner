"""Tests for the Teach AI prompt authoring dashboard group."""

from __future__ import annotations

from kanda_reasoner_app.prompt_library_gui.group_catalog import (
    build_group_stack_text,
    filter_items_for_group,
    load_prompt_groups,
)
from kanda_reasoner_app.prompt_library_gui.library_catalog import load_prompt_library_items


def test_teach_ai_prompt_authoring_group_exists() -> None:
    """Verify the Teach AI prompt authoring group is registered."""
    group_ids = {group.group_id for group in load_prompt_groups()}
    assert "teach_ai_prompt_authoring" in group_ids


def test_teach_ai_prompt_authoring_group_resolves_items() -> None:
    """Verify the Teach AI group resolves its prompt-library text assets."""
    items = load_prompt_library_items()
    group = next(item for item in load_prompt_groups() if item.group_id == "teach_ai_prompt_authoring")
    filtered = filter_items_for_group(group, items)
    prompt_ids = {str(item.metadata.get("prompt_id")) for item in filtered}
    assert "teach_ai_tab9_prompt_authoring_guide" in prompt_ids
    assert "teach_ai_create_or_update_prompt_request" in prompt_ids
    assert "tab9_prompt_asset_placement_rules" in prompt_ids


def test_teach_ai_prompt_authoring_stack_explains_tab9_logic() -> None:
    """Verify the copy stack includes the Tab 9 authoring guide."""
    items = load_prompt_library_items()
    group = next(item for item in load_prompt_groups() if item.group_id == "teach_ai_prompt_authoring")
    filtered = filter_items_for_group(group, items)
    stack_text = build_group_stack_text(group, filtered)
    assert "PROMPT GROUP: Teach AI Prompt Authoring" in stack_text
    assert "Tab 9 is an isolated prompt library box" in stack_text
    assert 'ask_' 'ai_project_reasoner' '\\prompt_library' in stack_text
