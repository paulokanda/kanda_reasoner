"""Regression tests for read-before-all startup compliance refresh alignment."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update" / "contract.py"
GUI_TAB = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"
GENERATOR = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "sync_startup_routing_kernel_pack.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def test_compliance_contract_reports_read_before_all_and_prompt_library_zip() -> None:
    text = _read(CONTRACT)

    assert 'read_before_all = workspace_root / "first_AI_deliver" / "tell_AI_read_before_all.md"' in text
    assert 'prompt_library_zip = workspace_root / "first_AI_deliver" / "prompt_library.zip"' in text
    assert '"read_before_all_instruction": str(read_before_all)' in text
    assert '"prompt_library_zip": str(prompt_library_zip)' in text
    assert 'paste_after_first_prompts_to_ai.md' not in text


def test_freeze_gui_log_uses_read_before_all_label_not_paste_after_label() -> None:
    text = _read(GUI_TAB)

    assert "Read-before-all file:" in text
    assert "Prompt library ZIP:" in text
    assert "Paste-after file:" not in text
    assert "read_before_all_instruction" in text


def test_startup_generator_user_visible_messages_are_aligned() -> None:
    text = _read(GENERATOR)

    assert "tell_AI_read_before_all.md" in text
    assert "prompt_library.zip" in text
    assert "current startup ZIP, prompt_library.zip, and tell_AI_read_before_all.md file" in text
    assert "startup ZIP, prompt_library.zip, and tell_AI_read_before_all.md file" in text
    assert "This will regenerate first_AI_deliver with the current startup ZIP and paste_after_first_prompts_to_ai file." not in text
    assert "Regenerate first_AI_deliver startup ZIP and paste_after_first_prompts_to_ai file" not in text


if __name__ == "__main__":
    test_compliance_contract_reports_read_before_all_and_prompt_library_zip()
    test_freeze_gui_log_uses_read_before_all_label_not_paste_after_label()
    test_startup_generator_user_visible_messages_are_aligned()
    print("VALIDATION OK: startup read before all compliance refresh alignment")
