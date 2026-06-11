"""Tests for the read-only Prompt Library catalog."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.prompt_library_gui.library_catalog import (
    load_prompt_library_items,
)
from kanda_reasoner_app.prompt_library_gui.library_paths import prompt_library_root


def test_prompt_library_root_exists() -> None:
    """Verify the package-owned prompt_library folder is present."""
    assert prompt_library_root().exists()


def test_prompt_library_catalog_loads_active_prompts() -> None:
    """Verify the catalog finds active prompt text files."""
    items = load_prompt_library_items()
    relative_paths = {item.relative_path for item in items}
    assert "active/0000 0.1 PYARCHITECT GENERAL PROMPT STACK LOAD ORDER v1.0.md" in relative_paths
    assert "stacks/GENERAL_PROJECT_DAILY_PROMPT_STACK.md" in relative_paths


def test_prompt_library_catalog_attaches_metadata() -> None:
    """Verify at least one active prompt has parsed metadata."""
    items = load_prompt_library_items()
    matching = [
        item
        for item in items
        if item.relative_path.endswith("GENERAL PROMPT STACK LOAD ORDER v1.0.md")
    ]
    assert matching
    assert matching[0].metadata
    assert matching[0].metadata.get("project_agnostic") is True


def test_prompt_library_catalog_can_use_override_root(tmp_path: Path) -> None:
    """Verify the catalog works with a temporary root for isolated tests."""
    active = tmp_path / "active"
    metadata = tmp_path / "metadata"
    active.mkdir()
    metadata.mkdir()
    prompt = active / "sample.md"
    prompt.write_text("# Sample\n", encoding="utf-8")
    meta = metadata / "sample.meta.json"
    meta.write_text(
        '{"display_name": "Sample Prompt", "project_agnostic": true}',
        encoding="utf-8",
    )

    items = load_prompt_library_items(tmp_path)

    assert len(items) == 1
    assert items[0].title == "Sample Prompt"
    assert items[0].read_text() == "# Sample\n"
