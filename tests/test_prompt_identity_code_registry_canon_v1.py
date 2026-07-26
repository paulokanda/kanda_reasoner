"""Regression tests for Prompt Identity Code Registry Canon v1."""

from __future__ import annotations

import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_prompt_code_canon_file_metadata_and_folder_assimilation_are_registered() -> None:
    prompt_rel = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_identity_code_registry_canon.md"
    metadata_rel = "kanda_prompt_workspace/prompt_library/METADATA/prompt_identity_code_registry_canon.meta.json"
    folder_rel = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/07_prompt_authoring_and_audit/_FOLDER_ASSIMILATION.md"

    prompt_path = PROJECT_ROOT / prompt_rel
    metadata_path = PROJECT_ROOT / metadata_rel

    assert prompt_path.exists(), prompt_rel
    assert metadata_path.exists(), metadata_rel

    prompt_text = read_text(prompt_rel)
    assert "KPR-<folder_number>-<sequence>" in prompt_text
    assert "prompt_code" in prompt_text
    assert "prompt_id" in prompt_text
    assert "KANDA_ROUTING_CHOICE_START" in prompt_text
    assert "Do not reuse a retired prompt_code" in prompt_text

    metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    assert metadata["prompt_code"] == "KPR-07-002"
    assert re.fullmatch(r"KPR-\d{2}-\d{3}", metadata["prompt_code"])
    assert metadata["prompt_id"] == "prompt_identity_code_registry_canon"
    assert metadata["category"] == "07_prompt_authoring_and_audit"
    assert metadata["load_type"] == "routed"
    assert "always_startup" in metadata["load_mode_rule"]

    folder_text = read_text(folder_rel)
    assert "prompt_identity_code_registry_canon" in folder_text
    assert "KPR prompt_code" in folder_text


def test_prompt_insertion_protocol_requires_prompt_code_canon() -> None:
    insertion_text = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/07_prompt_authoring_and_audit/prompt_insertion_and_router_registration_protocol.md"
    )

    assert "prompt_identity_code_registry_canon" in insertion_text
    assert "KPR-<folder_number>-<sequence>" in insertion_text
    assert "Do not register a new prompt in router logic without a stable prompt_code" in insertion_text
    assert '"prompt_code": "KPR-<folder_number>-<sequence>"' in insertion_text


def test_router_and_navigation_route_prompt_code_requests_to_canon() -> None:
    navigation_text = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
    )
    router_text = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md"
    )

    for text in (navigation_text, router_text):
        assert "prompt_identity_code_registry_canon" in text
        assert "KPR-<folder_number>-<sequence>" in text
        assert "prompt_code" in text

    assert "Every new prompt must receive prompt_code" in navigation_text
    assert "ChatGPT router-choice blocks must display prompt_code and prompt_id" in router_text


def test_prompt_code_canon_is_routed_not_always_startup() -> None:
    source_map_path = PROJECT_ROOT / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
    if source_map_path.exists():
        source_map = source_map_path.read_text(encoding="utf-8-sig")
        assert "prompt_identity_code_registry_canon" not in source_map

    metadata_path = PROJECT_ROOT / "kanda_prompt_workspace/prompt_library/METADATA/prompt_identity_code_registry_canon.meta.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    assert metadata["load_type"] == "routed"


if __name__ == "__main__":
    test_prompt_code_canon_file_metadata_and_folder_assimilation_are_registered()
    test_prompt_insertion_protocol_requires_prompt_code_canon()
    test_router_and_navigation_route_prompt_code_requests_to_canon()
    test_prompt_code_canon_is_routed_not_always_startup()
    print("VALIDATION OK: prompt identity code registry canon")
