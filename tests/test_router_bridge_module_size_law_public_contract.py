"""Public contract tests for router bridge module-size law hardening."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md"


def test_router_bridge_enforces_explicit_module_size_law() -> None:
    text = BRIDGE.read_text(encoding="utf-8")
    assert "Ideal module size: <= 400 lines." in text
    assert "Maximum module size: <= 500 lines." in text
    assert "If a new Python code module is expected to exceed 500 lines, do not create it as one file." in text
    assert "large_module_refactor_protocol v7.0" in text
    assert "Line-count risk: current N lines; projected M lines; ideal <=400; maximum <=500; v7.0 routing needed YES/NO." in text
