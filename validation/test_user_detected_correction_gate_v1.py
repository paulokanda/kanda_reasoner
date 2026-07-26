"""Validate User-Detected Correction Gate v1 prompt routing contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "kanda-router-bridge-user-detected-correction-gate-v1"
MARKER = "VALIDATION OK: kanda-router-bridge-user-detected-correction-gate-v1"
GATE_MARKER = "USER-DETECTED CORRECTION GATE: PASS"


def read_text(relative_path: str) -> str:
    """Read a project text file using UTF-8."""
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def require_contains(text: str, needle: str, label: str) -> None:
    """Raise AssertionError when expected text is absent."""
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def require_json(path: Path) -> dict:
    """Load a JSON object and fail if the file is not an object."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"Expected JSON object: {path}")
    return data


def main() -> int:
    """Run deterministic validation checks for the routed correction bridge."""
    prompt_rel = (
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "05_patch_delivery_and_validation/router_bridge_user_detected_correction.md"
    )
    meta_rel = "kanda_prompt_workspace/prompt_library/METADATA/router_bridge_user_detected_correction.meta.json"
    router_rel = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md"
    nav_rel = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
    impl_rel = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md"

    prompt_text = read_text(prompt_rel)
    router_text = read_text(router_rel)
    nav_text = read_text(nav_rel)
    impl_text = read_text(impl_rel)
    meta = require_json(ROOT / meta_rel)

    if meta.get("prompt_id") != "router_bridge_user_detected_correction":
        raise AssertionError("Metadata prompt_id mismatch.")
    if meta.get("load_type") != "routed":
        raise AssertionError("User-detected correction bridge must stay routed, not always startup.")
    if meta.get("category") != "05_patch_delivery_and_validation":
        raise AssertionError("User-detected correction bridge category mismatch.")

    required_prompt_phrases = [
        "USER-DETECTED CORRECTION GATE",
        "Reported mistake:",
        "Exact cause audited:",
        "Files inspected:",
        "Patch needed: YES / NO",
        "Install code needed: YES / NO",
        "Validation code needed: YES / NO",
        "Error Memory intake needed: YES / NO",
        "Freeze/freeze-intake needed: YES / NO",
        "May deliver: YES / NO",
        "No governed correction patch may be delivered unless May deliver is YES.",
        "Do not create active-ready Error Memory JSON from memory alone.",
        "Do not freeze stale or pre-validation sidecars.",
        "Do not produce an isolated ZIP",
    ]
    for phrase in required_prompt_phrases:
        require_contains(prompt_text, phrase, "correction bridge prompt phrase")

    for phrase in [
        "router_bridge_user_detected_correction",
        "USER_DETECTED_CORRECTION_ROUTER_BRIDGE_V1_START",
        "failed validation",
        "blocked freeze",
        "missing Error Memory",
        "missing freeze hint",
    ]:
        require_contains(router_text, phrase, "prompt_router correction bridge")

    for phrase in [
        "USER_DETECTED_CORRECTION_NAVIGATION_GATE_V1_START",
        "router_bridge_user_detected_correction",
        "Error Memory intake",
        "Preview or Confirm and Write",
    ]:
        require_contains(nav_text, phrase, "navigation correction bridge")

    for phrase in [
        "USER_DETECTED_CORRECTION_DELIVERY_FORMAT_V1_START",
        "router_bridge_user_detected_correction",
        "USER-DETECTED CORRECTION GATE",
        "Do not answer a governed correction with apology-only text.",
        "Do not invent validation evidence.",
    ]:
        require_contains(impl_text, phrase, "implementation protocol correction format")

    # Positive trigger phrases must be visible in metadata for router coverage.
    triggers = "\n".join(str(item) for item in meta.get("trigger_phrases", []))
    for phrase in [
        "you forgot install code",
        "validation failed",
        "freeze blocked",
        "wrong path",
        "missing STATUS: IN_SYNC",
    ]:
        require_contains(triggers, phrase, "metadata trigger phrase")

    print(MARKER)
    print(GATE_MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
