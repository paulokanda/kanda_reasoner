"""Validation for Error Memory AI formulary startup canon v1."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT / "kanda_prompt_workspace"
PROMPT_PATH = WORKSPACE_ROOT / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "error_memory_ai_formulary_startup_canon.md"
SOURCE_MAP_PATH = WORKSPACE_ROOT / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
SYNC_SCRIPT = WORKSPACE_ROOT / "prompt_tools" / "sync_startup_routing_kernel_pack.py"


def test_prompt_source_contains_receive_contract() -> None:
    text = PROMPT_PATH.read_text(encoding="utf-8")
    assert "KANDA_ERROR_LESSON_JSON_BEGIN" in text
    assert "KANDA_ERROR_LESSON_JSON_END" in text
    assert "Receive Formulary from AI" in text
    assert "correction patch" in text
    assert "Do not invent validation evidence" in text
    assert "source_patch_zip" in text
    assert "install_command_summary" in text
    assert "validation_command_summary" in text


def test_startup_source_map_registers_prompt() -> None:
    payload = json.loads(SOURCE_MAP_PATH.read_text(encoding="utf-8-sig"))
    entries = payload["startup_sources"]
    matches = [entry for entry in entries if entry.get("prompt_id") == "error_memory_ai_formulary_startup_canon"]
    assert len(matches) == 1
    entry = matches[0]
    assert entry["generated_filename"] == "12_error_memory_ai_formulary_startup_canon.md"
    assert entry["load_mode"] == "always_startup"
    assert entry["canonical_source"].endswith("error_memory_ai_formulary_startup_canon.md")
    assert [int(item["load_order"]) for item in entries] == list(range(1, len(entries) + 1))



def test_source_map_can_resolve_error_memory_prompt_source() -> None:
    payload = json.loads(SOURCE_MAP_PATH.read_text(encoding="utf-8-sig"))
    match = next(
        entry for entry in payload["startup_sources"]
        if entry.get("prompt_id") == "error_memory_ai_formulary_startup_canon"
    )
    resolved = WORKSPACE_ROOT / match["canonical_source"]
    assert resolved == PROMPT_PATH
    assert resolved.is_file()
    assert match["generated_filename"] == "12_error_memory_ai_formulary_startup_canon.md"


def main() -> int:
    test_prompt_source_contains_receive_contract()
    test_startup_source_map_registers_prompt()
    test_source_map_can_resolve_error_memory_prompt_source()
    print("VALIDATION OK: error-memory-ai-formulary-startup-canon-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
