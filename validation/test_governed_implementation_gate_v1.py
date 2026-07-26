"""Validate Governed Implementation Gate v1 prompt-router hardening."""

from __future__ import annotations

import json
from pathlib import Path

FEATURE_ID = "kanda-router-bridge-governed-implementation-gate-v1"
EXPECTED_MARKER = "VALIDATION OK: " + FEATURE_ID

ROOT = Path(__file__).resolve().parents[1]

BRIDGE = ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "05_patch_delivery_and_validation" / "router_bridge_governed_implementation.md"
META = ROOT / "kanda_prompt_workspace" / "prompt_library" / "METADATA" / "router_bridge_governed_implementation.meta.json"
ROUTER = ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_router.md"
NAVIGATION = ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
IMPLEMENTATION_PROTOCOL = ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "05_patch_delivery_and_validation" / "implementation_and_delivery_protocol.md"
STARTUP_SOURCE_MAP = ROOT / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"

REQUIRED_GATE_FIELDS = [
    "IMPLEMENTATION GATE",
    "Task domain:",
    "Router bridge selected:",
    "Required prompt path:",
    "Target box:",
    "Forbidden box:",
    "Source files inspected:",
    "Generated-vs-canonical status:",
    "Project/tool disambiguation needed:",
    "Line-count risk:",
    "GUI-resolution risk, if GUI:",
    "May implement: YES / NO",
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def assert_contains(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        raise AssertionError(f"Missing {label}: {fragment}")


def assert_not_contains(text: str, fragment: str, label: str) -> None:
    if fragment in text:
        raise AssertionError(f"Unexpected {label}: {fragment}")


def validate_bridge_prompt() -> None:
    text = read_text(BRIDGE)
    assert_contains(text, "prompt_id: router_bridge_governed_implementation", "bridge prompt id")
    assert_contains(text, "load_type: routed", "routed load type")
    assert_contains(text, "No governed implementation may begin unless May implement is YES", "hard rule")
    assert_contains(text, "Do not load the entire prompt library", "on-demand rule")
    assert_contains(text, "Do not code from memory", "source audit rule")
    assert_contains(text, "Generated-vs-canonical", "generated canonical rule")
    assert_contains(text, "laptop-to-4K", "GUI resolution rule")
    for field in REQUIRED_GATE_FIELDS:
        assert_contains(text, field, "implementation gate field")


def validate_metadata() -> None:
    raw = read_text(META)
    data = json.loads(raw)
    expected = {
        "prompt_id": "router_bridge_governed_implementation",
        "filename": "router_bridge_governed_implementation.md",
        "category": "05_patch_delivery_and_validation",
        "load_type": "routed",
        "status": "active",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise AssertionError(f"Metadata {key} expected {value!r}, got {data.get(key)!r}")
    triggers = data.get("trigger_phrases")
    if not isinstance(triggers, list) or "implement code" not in triggers:
        raise AssertionError("Metadata trigger_phrases must include implement code.")


def validate_router_and_navigation() -> None:
    router = read_text(ROUTER)
    navigation = read_text(NAVIGATION)
    protocol = read_text(IMPLEMENTATION_PROTOCOL)
    for text, label in ((router, "prompt_router"), (navigation, "prompt_navigation_index"), (protocol, "implementation protocol")):
        assert_contains(text, "router_bridge_governed_implementation", label)
        assert_contains(text, "IMPLEMENTATION GATE", label)
        assert_contains(text, "Generated-vs-canonical", label)
        assert_contains(text, "Source files inspected", label)
    assert_contains(router, "GOVERNED_IMPLEMENTATION_ROUTER_BRIDGE_V1_START", "router marker")
    assert_contains(navigation, "GOVERNED_IMPLEMENTATION_NAVIGATION_GATE_V1_START", "navigation marker")
    assert_contains(protocol, "GOVERNED_IMPLEMENTATION_GATE_V1_START", "implementation protocol marker")


def validate_startup_source_map() -> None:
    if not STARTUP_SOURCE_MAP.exists():
        return
    raw = read_text(STARTUP_SOURCE_MAP)
    assert_not_contains(
        raw,
        "router_bridge_governed_implementation.md",
        "full governed implementation bridge in always-startup source map",
    )


def main() -> int:
    validate_bridge_prompt()
    validate_metadata()
    validate_router_and_navigation()
    validate_startup_source_map()
    print(EXPECTED_MARKER)
    print("GOVERNED IMPLEMENTATION GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
