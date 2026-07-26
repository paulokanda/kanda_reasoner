"""Regression tests for prompt_library.zip direct retrieval startup delivery."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "kanda_prompt_workspace"
DELIVER = WORKSPACE / "first_AI_deliver"


def test_prompt_router_reasoner_tab_removed_from_tool_registry() -> None:
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

    titles = [tool.step_title for tool in TOOLS]
    tab_ids = [tool.tab_id for tool in TOOLS]
    assert "Prompt Router Reasoner" not in titles
    assert "prompt_router_reasoner" not in tab_ids


def test_generator_creates_prompt_library_zip_and_updates_paste_instruction() -> None:
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
    paste_file = DELIVER / "paste_after_first_prompts_to_ai.md"

    assert startup_zip.is_file()
    assert prompt_library_zip.is_file()
    assert paste_file.is_file()

    paste_text = paste_file.read_text(encoding="utf-8")
    assert "first_prompts_to_ai.zip" in paste_text
    assert "prompt_library.zip" in paste_text
    assert "paste_after_first_prompts_to_ai.md" in paste_text
    assert "three-file startup delivery" in paste_text
    assert "Do not read every prompt at startup" in paste_text
    assert "open only the specific addressed file" in paste_text
    assert "Do not depend on the local Prompt Router Reasoner tab" in paste_text

    with zipfile.ZipFile(prompt_library_zip, "r") as z:
        names = set(z.namelist())
        assert "PROMPT_LIBRARY_ZIP_MANIFEST.json" in names
        assert "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md" in names
        assert "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md" in names
        assert "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/chatgpt_kanda_routing_choice_output_protocol.md" in names
        assert not any(name.startswith("prompt_library/") for name in names)
        manifest = json.loads(z.read("PROMPT_LIBRARY_ZIP_MANIFEST.json").decode("utf-8"))

    assert manifest["kind"] == "prompt_library_zip_manifest"
    assert manifest["zip_filename"] == "prompt_library.zip"
    assert manifest["source_fingerprint"]
    assert any(
        entry.get("prompt_code") == "KPR-02-001"
        or entry.get("prompt_id") == "chatgpt_kanda_routing_choice_output_protocol"
        for entry in manifest.get("prompt_entries", [])
    )


def test_startup_protocol_uses_direct_prompt_library_retrieval() -> None:
    protocol = ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "chatgpt_kanda_routing_choice_output_protocol.md"
    text = protocol.read_text(encoding="utf-8")
    assert "prompt_library.zip" in text
    assert "paste_after_first_prompts_to_ai.md" in text
    assert "three-file startup delivery" in text
    assert "Do not read the whole prompt library at startup" in text
    assert "opens only that addressed prompt file" in text
    assert "Do not depend on a local Prompt Router Reasoner tab" in text
    assert "KPR-02-001" in text
