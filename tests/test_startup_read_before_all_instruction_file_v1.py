"""Regression tests for tell_AI_read_before_all.md startup instruction delivery."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "kanda_prompt_workspace"
DELIVER = WORKSPACE / "first_AI_deliver"


def test_generator_creates_read_before_all_startup_instruction() -> None:
    script = WORKSPACE / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    result = subprocess.run(
        [sys.executable, str(script), "--ensure-sync", "--yes", "--project-root", str(ROOT)],
        cwd=str(WORKSPACE),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert result.returncode == 0, result.stdout

    startup_zip = DELIVER / "first_prompts_to_ai.zip"
    prompt_library_zip = DELIVER / "prompt_library.zip"
    read_before_all = DELIVER / "tell_AI_read_before_all.md"
    legacy_paste_after = DELIVER / "paste_after_first_prompts_to_ai.md"

    assert startup_zip.is_file()
    assert prompt_library_zip.is_file()
    assert read_before_all.is_file()
    assert not legacy_paste_after.exists()

    text = read_before_all.read_text(encoding="utf-8")
    assert "# TELL AI: READ BEFORE ALL STARTUP ZIP CONTENTS" in text
    assert "Read this instruction before opening ZIP contents" in text
    assert "first_prompts_to_ai.zip" in text
    assert "prompt_library.zip" in text
    assert "tell_AI_read_before_all.md" in text
    assert "Do not read every prompt at startup" in text
    assert "not already present in `first_prompts_to_ai.zip`" in text
    assert "Do not depend on the local Prompt Router Reasoner tab" in text

    with zipfile.ZipFile(prompt_library_zip, "r") as z:
        names = set(z.namelist())
        assert "PROMPT_LIBRARY_ZIP_MANIFEST.json" in names
        assert "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md" in names
        assert "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/chatgpt_kanda_routing_choice_output_protocol.md" in names
        assert not any(name.startswith("prompt_library/") for name in names)


def test_startup_protocol_mentions_read_before_all_and_lazy_prompt_library_access() -> None:
    protocol = ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "chatgpt_kanda_routing_choice_output_protocol.md"
    text = protocol.read_text(encoding="utf-8")
    assert "Version: 2.1.0" in text
    assert "tell_AI_read_before_all.md" in text
    assert "Read/paste this file before the AI opens ZIP contents" in text
    assert "Do not read the whole prompt library at startup" in text
    assert "not already in first_prompts_to_ai.zip" in text
    assert "Do not depend on a local Prompt Router Reasoner tab" in text
    assert "KPR-02-001" in text


def test_generator_source_tracks_legacy_cleanup() -> None:
    script = WORKSPACE / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    source = script.read_text(encoding="utf-8")
    assert 'PASTE_AFTER_UPLOAD_FILENAME = "tell_AI_read_before_all.md"' in source
    assert 'LEGACY_PASTE_AFTER_FIRST_PROMPTS_FILENAME = "paste_after_first_prompts_to_ai.md"' in source
    assert "prompt_library.zip only when a specific prompt is needed" in source
