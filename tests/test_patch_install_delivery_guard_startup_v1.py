from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "kanda_prompt_workspace"


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_error_register_is_in_startup_source_map() -> None:
    source_map = json.loads(
        (WORKSPACE / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json").read_text(
            encoding="utf-8"
        )
    )
    entries = source_map["startup_sources"]
    matches = [
        item for item in entries
        if item.get("prompt_id") == "patch_install_delivery_error_register"
    ]
    assert len(matches) == 1
    entry = matches[0]
    assert entry["load_mode"] == "always_startup"
    assert entry["generated_filename"].endswith("patch_install_delivery_error_register.md")
    assert (WORKSPACE / entry["canonical_source"]).is_file()


def test_error_register_blocks_known_install_regressions() -> None:
    text = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/patch_install_delivery_error_register.md"
    )
    assert "PIR-001" in text
    assert "PIR-002" in text
    assert "Downloads/Desktop-first" in text
    assert "delete_after_daily_work" in text
    assert "zip is not in root of drive" in text
    assert "Append-only update protocol" in text


def test_guardrails_reference_error_register_and_root_staging() -> None:
    daily = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md"
    )
    pre_output = read_text(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md"
    )
    generator = read_text("kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py")

    for text in (daily, pre_output, generator):
        assert "patch_install_delivery_error_register" in text

    assert "$ROOT_PATCH_ZIP" in daily
    assert "$WORK_PATCH_ZIP" in daily
    assert "Remove-Item -Path $ROOT_PATCH_ZIP" in daily
    assert "Downloads/Desktop" in pre_output


def test_generated_startup_zip_contains_error_register_after_sync() -> None:
    zip_path = WORKSPACE / "first_AI_deliver" / "first_prompts_to_ai.zip"
    paste_path = WORKSPACE / "first_AI_deliver" / "paste_after_first_prompts_to_ai.md"
    assert zip_path.is_file(), "run sync_startup_routing_kernel_pack.py --ensure-sync --yes first"
    assert paste_path.is_file(), "run sync_startup_routing_kernel_pack.py --ensure-sync --yes first"

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
        target = [name for name in names if name.endswith("patch_install_delivery_error_register.md")]
        assert target, sorted(names)
        generated_text = zf.read(target[0]).decode("utf-8")
        assert "Patch Install Delivery Error Register" in generated_text

    paste_text = paste_path.read_text(encoding="utf-8")
    assert "patch_install_delivery_error_register.md" in paste_text
    assert "Mandatory pre-output contract gate hook loaded" in paste_text



def main() -> None:
    test_error_register_is_in_startup_source_map()
    test_error_register_blocks_known_install_regressions()
    test_guardrails_reference_error_register_and_root_staging()
    test_generated_startup_zip_contains_error_register_after_sync()
    print("TEST OK: patch_install_delivery_guard_startup_v1")


if __name__ == "__main__":
    main()
