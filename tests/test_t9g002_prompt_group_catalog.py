"""Tests for the read-only Prompt Library group catalog."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.prompt_library_gui.group_catalog import (
    build_group_stack_text,
    filter_items_for_group,
    load_prompt_groups,
)
from kanda_reasoner_app.prompt_library_gui.library_catalog import (
    load_prompt_library_items,
)
from kanda_reasoner_app.prompt_library_gui.library_paths import prompt_library_root


def test_prompt_groups_load_from_package_catalog() -> None:
    """Verify the package-owned group catalog loads expected groups."""
    groups = load_prompt_groups()
    group_ids = {group.group_id for group in groups}
    assert "daily_start" in group_ids
    assert "end_of_day_handoff" in group_ids
    assert "architecture_hardening" in group_ids
    assert "prompt_library_tools" in group_ids


def test_daily_start_group_filters_prompts_in_order() -> None:
    """Verify Daily Start returns only its configured prompts in order."""
    groups = load_prompt_groups()
    daily_group = next(group for group in groups if group.group_id == "daily_start")
    items = filter_items_for_group(daily_group, load_prompt_library_items())
    prompt_ids = [str(item.metadata.get("prompt_id")) for item in items]
    assert prompt_ids == list(daily_group.prompt_ids)


def test_group_stack_text_contains_only_group_prompts() -> None:
    """Verify full group copy text contains deterministic group sections."""
    groups = load_prompt_groups()
    refactor_group = next(group for group in groups if group.group_id == "large_module_refactor")
    items = filter_items_for_group(refactor_group, load_prompt_library_items())
    stack_text = build_group_stack_text(refactor_group, items)
    assert "PROMPT GROUP: Large Module Refactor" in stack_text
    assert "Large Module Refactor Protocol" in stack_text
    assert "Daily Startup Loader" not in stack_text


def test_prompt_groups_can_use_override_root(tmp_path: Path) -> None:
    """Verify groups can load from an isolated prompt_library root."""
    groups_dir = tmp_path / "groups"
    active_dir = tmp_path / "active"
    metadata_dir = tmp_path / "metadata"
    groups_dir.mkdir()
    active_dir.mkdir()
    metadata_dir.mkdir()

    (groups_dir / "PROMPT_GROUPS.json").write_text(
        '{"groups":[{"group_id":"sample","display_name":"Sample",'
        '"color_role":"blue","description":"Sample group",'
        '"prompt_ids":["sample_prompt"]}]}',
        encoding="utf-8",
    )
    (active_dir / "sample.md").write_text("# Sample\n", encoding="utf-8")
    (metadata_dir / "sample.meta.json").write_text(
        '{"prompt_id":"sample_prompt","display_name":"Sample Prompt"}',
        encoding="utf-8",
    )

    groups = load_prompt_groups(tmp_path)
    items = filter_items_for_group(groups[0], root=tmp_path)

    assert len(groups) == 1
    assert len(items) == 1
    assert items[0].title == "Sample Prompt"


def test_prompt_groups_catalog_path_exists() -> None:
    """Verify the installed group catalog exists in the package library."""
    assert (prompt_library_root() / "groups" / "PROMPT_GROUPS.json").exists()
