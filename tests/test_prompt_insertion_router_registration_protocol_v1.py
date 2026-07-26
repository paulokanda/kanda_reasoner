"""Regression tests for Prompt Insertion and Router Registration Protocol v1."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_prompt_file_metadata_and_folder_assimilation_are_registered() -> None:
    prompt_rel = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_insertion_and_router_registration_protocol.md"
    metadata_rel = "kanda_prompt_workspace/prompt_library/METADATA/prompt_insertion_and_router_registration_protocol.meta.json"
    folder_rel = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/07_prompt_authoring_and_audit/_FOLDER_ASSIMILATION.md"

    prompt_path = PROJECT_ROOT / prompt_rel
    metadata_path = PROJECT_ROOT / metadata_rel

    assert prompt_path.exists(), prompt_rel
    assert metadata_path.exists(), metadata_rel

    prompt_text = read_text(prompt_rel)
    assert "Purpose" in prompt_text
    assert "The correct folder depends on prompt type" in prompt_text
    assert "PROMPT INSERTION ROUTE CHECK" in prompt_text
    assert "Do not guess the folder" in prompt_text

    metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    assert metadata["prompt_id"] == "prompt_insertion_and_router_registration_protocol"
    assert metadata["category"] == "07_prompt_authoring_and_audit"
    assert metadata["load_type"] == "routed"
    assert "always_startup" in metadata["load_mode_rule"]

    folder_text = read_text(folder_rel)
    assert "prompt_insertion_and_router_registration_protocol" in folder_text
    assert "insert/register/activate/connect a prompt" in folder_text


def test_router_and_navigation_call_protocol_for_prompt_insertion_tasks() -> None:
    navigation_text = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
    )
    router_text = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md"
    )

    required = [
        "prompt_insertion_and_router_registration_protocol",
        "prompt_canon_reconciliation_protocol",
        "prompt_audit_canon",
        "project_specific_prompt_generalization",
        "Relevant ACTIVE_PROMPTS folder card or _FOLDER_ASSIMILATION",
    ]

    for token in required:
        assert token in navigation_text, token

    assert "connect a prompt to router logic" in router_text
    assert "make the router call this prompt when necessary" in router_text
    assert "07_prompt_authoring_and_audit" in router_text
    assert "02_prompt_routing_and_indexing" in router_text


def test_protocol_is_routed_not_always_startup() -> None:
    source_map_path = PROJECT_ROOT / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
    if source_map_path.exists():
        source_map = source_map_path.read_text(encoding="utf-8-sig")
        assert "prompt_insertion_and_router_registration_protocol" not in source_map

    metadata_path = PROJECT_ROOT / "kanda_prompt_workspace/prompt_library/METADATA/prompt_insertion_and_router_registration_protocol.meta.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    assert metadata["load_type"] == "routed"


if __name__ == "__main__":
    test_prompt_file_metadata_and_folder_assimilation_are_registered()
    test_router_and_navigation_call_protocol_for_prompt_insertion_tasks()
    test_protocol_is_routed_not_always_startup()
    print("VALIDATION OK: prompt insertion and router registration protocol")
