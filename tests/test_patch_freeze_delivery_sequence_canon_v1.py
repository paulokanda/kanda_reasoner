from __future__ import annotations

import sys
import zipfile
from pathlib import Path


FEATURE_ID = "patch_freeze_delivery_sequence_canon_v1"
MARKER = "PATCH_FREEZE_DELIVERY_SEQUENCE_CANON_V1_START"
SEQUENCE_TEXT = "patch ZIP with root KANDA_FREEZE_HINT.json"
PIR_TEXT = "PIR-003 - Freeze-ready patch sequence drift"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _zip_text(zip_path: Path, member: str) -> str:
    with zipfile.ZipFile(zip_path) as zf:
        return zf.read(member).decode("utf-8", errors="replace")


def test_patch_freeze_delivery_sequence_canon_installed() -> None:
    root = Path.cwd()

    canonical_files = [
        root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md",
        root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
        root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md",
        root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
        root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
    ]

    for path in canonical_files:
        text = _read_text(path)
        assert MARKER in text, f"missing sequence canon marker in {path}"
        assert SEQUENCE_TEXT in text, f"missing short-form sequence in {path}"
        assert "VALIDATION OK: <feature_id>" in text, f"missing validation marker rule in {path}"
        assert "STATUS: IN_SYNC" in text, f"missing sync marker rule in {path}"

    register = root / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/patch_install_delivery_error_register.md"
    assert PIR_TEXT in _read_text(register), "PIR-003 register entry missing"

    tell = root / "kanda_prompt_workspace/first_AI_deliver/tell_AI_read_before_all.md"
    tell_text = _read_text(tell)
    assert MARKER in tell_text
    assert SEQUENCE_TEXT in tell_text

    startup_zip = root / "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
    prompt_library_zip = root / "kanda_prompt_workspace/first_AI_deliver/prompt_library.zip"

    startup_members = [
        "00_START_HERE_FOR_AI.md",
        "02_prompt_navigation_index.md",
        "07_daily_patch_delivery_guardrails.md",
    ]
    for member in startup_members:
        text = _zip_text(startup_zip, member)
        assert MARKER in text, f"missing marker in startup ZIP member {member}"
        assert SEQUENCE_TEXT in text, f"missing short-form sequence in startup ZIP member {member}"

    assert PIR_TEXT in _zip_text(startup_zip, "09_patch_install_delivery_error_register.md")

    prompt_library_members = [
        "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md",
        "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
        "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md",
        "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
        "ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
    ]
    for member in prompt_library_members:
        text = _zip_text(prompt_library_zip, member)
        assert MARKER in text, f"missing marker in prompt_library ZIP member {member}"
        assert SEQUENCE_TEXT in text, f"missing short-form sequence in prompt_library ZIP member {member}"

    assert PIR_TEXT in _zip_text(
        prompt_library_zip,
        "ACTIVE_PROMPTS/01_session_start_and_navigation/patch_install_delivery_error_register.md",
    )

    root_hint = root / "KANDA_FREEZE_HINT.json"
    assert not root_hint.exists(), "KANDA_FREEZE_HINT.json must not be installed into project root"


if __name__ == "__main__":
    test_patch_freeze_delivery_sequence_canon_installed()
    print("VALIDATION OK: " + FEATURE_ID)
    print("VALIDATION OK: patch freeze delivery sequence canon")
    print("STATUS: IN_SYNC")
