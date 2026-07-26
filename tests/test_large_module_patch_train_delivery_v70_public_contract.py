"""Public contract checks for Large Module Refactor Protocol v7.0 patch-train delivery bundles."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
TEMPLATE = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_template.md"


def test_protocol_keeps_v70_and_adds_patch_train_rules() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "Version: 7.0" in text
    assert "### Patch-train delivery bundle" in text
    assert "each inner patch has its own feature id" in text
    assert "Patch B is built against the result of Patch A" in text
    assert "install Patch A -> validate Patch A -> freeze Patch A" in text
    assert "do not freeze the outer bundle as one vague memory entry" in text


def test_template_mentions_patch_train_delivery_bundle() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "Version: 3.1.0" in text
    assert "## Patch-train Delivery Bundle" in text
    assert "each inner patch has its own feature id" in text
    assert "Patch A: install -> validate -> freeze" in text
