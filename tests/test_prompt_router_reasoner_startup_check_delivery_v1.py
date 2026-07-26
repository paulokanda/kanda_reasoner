"""Regression tests for Prompt Router Reasoner startup check delivery."""

from __future__ import annotations

import json
from pathlib import Path
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT / "kanda_prompt_workspace"
PROMPT_ROOT = WORKSPACE_ROOT / "prompt_library"
SOURCE_MAP = WORKSPACE_ROOT / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
GENERATOR = WORKSPACE_ROOT / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
DELIVERY_ZIP = WORKSPACE_ROOT / "first_AI_deliver" / "first_prompts_to_ai.zip"
PASTE_FILE = WORKSPACE_ROOT / "first_AI_deliver" / "paste_after_first_prompts_to_ai.md"
PROMPT_FILE = (
    PROMPT_ROOT
    / "ACTIVE_PROMPTS"
    / "01_session_start_and_navigation"
    / "prompt_router_reasoner_startup_check.md"
)
METADATA_FILE = PROMPT_ROOT / "METADATA" / "prompt_router_reasoner_startup_check.meta.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_canonical_prompt_and_metadata_exist() -> None:
    text = _read(PROMPT_FILE)
    metadata = json.loads(_read(METADATA_FILE))

    assert "Prompt Router Reasoner Startup Check" in text
    assert "PROMPT ROUTER REASONER CHECK" in text
    assert "PROMPT ROUTER REASONER IS FIT TO RUN" in text
    assert metadata["prompt_id"] == "prompt_router_reasoner_startup_check"
    assert metadata["category"] == "01_session_start_and_navigation"


def test_source_map_loads_startup_check_at_beginning_of_day() -> None:
    data = json.loads(_read(SOURCE_MAP))
    matches = [
        item
        for item in data["startup_sources"]
        if item.get("prompt_id") == "prompt_router_reasoner_startup_check"
    ]

    assert len(matches) == 1
    entry = matches[0]
    assert entry["load_order"] == 10
    assert entry["load_mode"] == "always_startup"
    assert entry["generated_filename"] == "10_prompt_router_reasoner_startup_check.md"
    assert entry["canonical_source"].endswith("prompt_router_reasoner_startup_check.md")


def test_generator_emits_prompt_router_reasoner_check_shape() -> None:
    text = _read(GENERATOR)

    assert "def prompt_router_reasoner_startup_check_block" in text
    assert "PROMPT ROUTER REASONER CHECK" in text
    assert "PROMPT ROUTER REASONER IS FIT TO RUN" in text
    assert "prompt_router_reasoner_check" in text
    assert "10_prompt_router_reasoner_startup_check.md" in text


def test_delivery_zip_and_paste_include_startup_check() -> None:
    paste_text = _read(PASTE_FILE)
    assert "10_prompt_router_reasoner_startup_check.md" in paste_text
    assert "PROMPT ROUTER REASONER CHECK" in paste_text
    assert "PROMPT ROUTER REASONER IS FIT TO RUN" in paste_text

    with zipfile.ZipFile(DELIVERY_ZIP, "r") as archive:
        names = set(archive.namelist())
        assert "00_START_HERE_FOR_AI.md" in names
        assert "10_prompt_router_reasoner_startup_check.md" in names
        start_here = archive.read("00_START_HERE_FOR_AI.md").decode("utf-8")
        prompt_text = archive.read("10_prompt_router_reasoner_startup_check.md").decode("utf-8")
        manifest = json.loads(archive.read("STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json").decode("utf-8"))

    assert "PROMPT ROUTER REASONER CHECK" in start_here
    assert "PROMPT ROUTER REASONER IS FIT TO RUN" in start_here
    assert "PROMPT ROUTER REASONER CHECK" in prompt_text
    assert any(
        item.get("prompt_id") == "prompt_router_reasoner_startup_check"
        for item in manifest["files"]
    )


if __name__ == "__main__":
    test_canonical_prompt_and_metadata_exist()
    test_source_map_loads_startup_check_at_beginning_of_day()
    test_generator_emits_prompt_router_reasoner_check_shape()
    test_delivery_zip_and_paste_include_startup_check()
    print("VALIDATION OK: prompt router reasoner startup check delivery")
