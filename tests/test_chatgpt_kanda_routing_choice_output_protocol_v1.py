from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT / "kanda_prompt_workspace"
PROMPT_ROOT = WORKSPACE_ROOT / "prompt_library"
PROMPT_FILE = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "chatgpt_kanda_routing_choice_output_protocol.md"
META_FILE = PROMPT_ROOT / "METADATA" / "chatgpt_kanda_routing_choice_output_protocol.meta.json"
SOURCE_MAP = WORKSPACE_ROOT / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
STARTUP_ZIP = WORKSPACE_ROOT / "first_AI_deliver" / "first_prompts_to_ai.zip"
PASTE_FILE = WORKSPACE_ROOT / "first_AI_deliver" / "paste_after_first_prompts_to_ai.md"


def test_protocol_prompt_and_metadata_are_coded_and_startup_loaded() -> None:
    assert PROMPT_FILE.is_file()
    text = PROMPT_FILE.read_text(encoding="utf-8-sig")
    assert "Prompt code: KPR-02-001" in text
    assert "KANDA_ROUTING_CHOICE_START" in text
    assert "KANDA_ROUTING_CHOICE_END" in text
    assert "\"advisory_only\": true" in text
    assert "Do not invent `prompt_code` values for legacy prompts." in text

    meta = json.loads(META_FILE.read_text(encoding="utf-8-sig"))
    assert meta["prompt_code"] == "KPR-02-001"
    assert meta["prompt_id"] == "chatgpt_kanda_routing_choice_output_protocol"
    assert meta["folder"] == "ACTIVE_PROMPTS/02_prompt_routing_and_indexing"
    assert meta["load_type"] == "always_startup"
    assert meta["canonical_path"].endswith("chatgpt_kanda_routing_choice_output_protocol.md")


def test_source_map_includes_protocol_as_always_startup_entry() -> None:
    data = json.loads(SOURCE_MAP.read_text(encoding="utf-8-sig"))
    matches = [entry for entry in data["startup_sources"] if entry["prompt_id"] == "chatgpt_kanda_routing_choice_output_protocol"]
    assert len(matches) == 1
    entry = matches[0]
    assert entry["load_mode"] == "always_startup"
    assert entry["generated_filename"] == "11_chatgpt_kanda_routing_choice_output_protocol.md"
    assert entry["canonical_source"].endswith("chatgpt_kanda_routing_choice_output_protocol.md")


def test_startup_delivery_after_sync_contains_protocol_and_boot_lists_it() -> None:
    # This test intentionally validates the generated startup artifacts after
    # local startup sync has been run by the validation block.
    assert STARTUP_ZIP.is_file(), "Run sync_startup_routing_kernel_pack.py --ensure-sync --yes before this test."
    with zipfile.ZipFile(STARTUP_ZIP, "r") as archive:
        names = set(archive.namelist())
        assert "11_chatgpt_kanda_routing_choice_output_protocol.md" in names
        boot = archive.read("00_START_HERE_FOR_AI.md").decode("utf-8-sig")
        generated = archive.read("11_chatgpt_kanda_routing_choice_output_protocol.md").decode("utf-8-sig")
        manifest = json.loads(archive.read("STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json").decode("utf-8-sig"))

    assert "11_chatgpt_kanda_routing_choice_output_protocol.md" in boot
    assert "KANDA_ROUTING_CHOICE_START" in generated
    assert "KPR-02-001" in generated
    assert any(
        item.get("prompt_id") == "chatgpt_kanda_routing_choice_output_protocol"
        and item.get("load_mode") == "always_startup"
        for item in manifest.get("files", [])
    )


def test_paste_after_file_tells_user_to_load_the_protocol_file() -> None:
    assert PASTE_FILE.is_file(), "Run sync_startup_routing_kernel_pack.py --ensure-sync --yes before this test."
    text = PASTE_FILE.read_text(encoding="utf-8-sig")
    assert "11_chatgpt_kanda_routing_choice_output_protocol.md" in text


if __name__ == "__main__":
    test_protocol_prompt_and_metadata_are_coded_and_startup_loaded()
    test_source_map_includes_protocol_as_always_startup_entry()
    test_startup_delivery_after_sync_contains_protocol_and_boot_lists_it()
    test_paste_after_file_tells_user_to_load_the_protocol_file()
    print("VALIDATION OK: chatgpt kanda routing choice output protocol")
