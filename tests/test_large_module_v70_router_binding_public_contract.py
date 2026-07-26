"""Public contract tests for Large Module v7.0 router binding."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_prompt_router_routes_large_modules_to_v70_protocol() -> None:
    text = read_text("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md")
    assert "### Large module refactor" in text
    section = text.split("### Large module refactor", 1)[1].split("### Architecture warning cleanup", 1)[0]
    assert "large_module_refactor_protocol" in section
    assert "large_module_refactor_template" in section
    assert "AST Split Audit" in section
    assert "candidate-island queue" in section
    assert "patch-train delivery bundle" in section
    assert "install -> validate -> freeze" in section


def test_prompt_router_metadata_has_large_module_v70_triggers() -> None:
    data = json.loads((ROOT / "kanda_prompt_workspace/prompt_library/METADATA/prompt_router.meta.json").read_text(encoding="utf-8"))
    triggers = set(data.get("trigger_phrases", []))
    assert "large module protocol v7" in triggers
    assert "AST Split Audit" in triggers
    assert "patch train" in triggers
    companions = set(data.get("required_companion_prompts", []))
    assert "large_module_refactor_protocol" in companions
    assert "large_module_refactor_template" in companions
    assert "router_bridge_governed_implementation" in companions
    binding = data.get("large_module_router_binding", {})
    assert binding.get("version") == "7.0"
    assert binding.get("requires_ast_split_audit_when_available") is True
    assert binding.get("max_islands_per_inner_patch") == 2
