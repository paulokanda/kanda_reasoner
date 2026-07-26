"""Validate show-project-clean-2sec-2xenter-button-v1."""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "show-project-clean-2sec-2xenter-button-v1"
UI_REL = "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py"
PROMPT_REL = "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/terminal_cleanup_contract.md"
META_REL = "kanda_prompt_workspace/prompt_library/METADATA/terminal_cleanup_contract.meta.json"
BUTTON_TEXT = "Clean 2sec 2xEnter"
VALIDATOR = "validate_show_project_clean_2sec_2xenter_button_v1.py"

PROTECTED_NOT_PACKAGED = [
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_persistence.py",
    "kanda_reasoner_app/error_memory_gui/_lesson_status_summary.py",
    "kanda_reasoner_app/error_memory_gui/_table_view.py",
    "kanda_reasoner_app/error_memory_gui/schema.py",
    "kanda_reasoner_app/error_memory_gui/store.py",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_validate_freeze_error_memory_routine_blueprint.md",
]


def assert_true(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear validation message."""
    if not condition:
        raise AssertionError(message)


def read_text(root: Path, rel: str) -> str:
    """Read a UTF-8 project file."""
    path = root / rel
    assert_true(path.is_file(), "Missing file: " + rel)
    return path.read_text(encoding="utf-8")


def validate_ui(root: Path) -> None:
    """Validate the new button is only a dynamic prompt-library wrapper."""
    text = read_text(root, UI_REL)
    path = root / UI_REL
    required = [
        'self.copy_terminal_cleanup_contract_button = QPushButton("' + BUTTON_TEXT + '")',
        "project_root_row.addWidget(self.copy_terminal_cleanup_contract_button)",
        "def _copy_terminal_cleanup_contract() -> None:",
        "terminal_cleanup_contract.md",
        "prompt_path = project_root / prompt_rel",
        "app_root = Path(__file__).resolve().parents[3]",
        "prompt_path = app_root / prompt_rel",
        'QApplication.clipboard().setText(prompt_path.read_text(encoding="utf-8"))',
        "Copied Clean 2sec 2xEnter prompt",
        "self.copy_terminal_cleanup_contract_button.clicked.connect(",
        "_copy_terminal_cleanup_contract",
        "Answer, Validate, Freeze, Memorize Error",
        'QColor("#ff4d00")',
        "answer_routine_button_font.setBold(True)",
        "terminal_cleanup_button_palette.setColor(",
        "self.copy_terminal_cleanup_contract_button.setPalette(",
        "terminal_cleanup_button_font.setBold(True)",
        "self.copy_terminal_cleanup_contract_button.setFont(terminal_cleanup_button_font)",
    ]
    for item in required:
        assert_true(item in text, "UI missing required fragment: " + item)

    button_index = text.index('self.copy_terminal_cleanup_contract_button = QPushButton("' + BUTTON_TEXT + '")')
    answer_index = text.index('self.copy_patch_validate_freeze_routine_button = QPushButton')
    bridge_index = text.index('self.bridge_list_label = QLabel("Bridge List:")')
    handler_index = text.index("def _copy_terminal_cleanup_contract() -> None:")
    connect_index = text.index("self.copy_terminal_cleanup_contract_button.clicked.connect(", handler_index)
    assert_true(answer_index < button_index < bridge_index, "Clean button must sit beside the Answer routine button before Bridge List.")
    assert_true(handler_index < connect_index, "Clean button handler must be defined before connect.")

    handler_end = text.index("    self.copy_terminal_cleanup_contract_button.clicked.connect(", handler_index)
    handler_block = text[handler_index:handler_end]
    assert_true("# Terminal Cleanup Contract" not in handler_block, "Button must not hard-code prompt body.")
    assert_true("Canonical PowerShell footer" not in handler_block, "Button must not hard-code prompt body.")
    assert_true("Start-Sleep -Seconds 2" not in handler_block, "Button must read prompt content instead of hard-coding cleanup commands.")
    assert_true("Downloads" not in text and "Desktop" not in text, "UI helper must not use Downloads/Desktop fallback.")
    assert_true(len(text.splitlines()) <= 500, "Touched UI module exceeds 500 lines.")
    py_compile.compile(str(path), doraise=True)


def validate_prompt(root: Path) -> None:
    """Validate the copied prompt source exists and owns the terminal cleanup contract."""
    prompt = read_text(root, PROMPT_REL)
    required = [
        "prompt_id: terminal_cleanup_contract",
        "title: Terminal Cleanup Contract",
        "load_type: always_startup",
        "# Terminal Cleanup Contract",
        "Wait about 2 seconds",
        "Start-Sleep -Seconds 2",
        'Read-Host "Press Enter to clear terminal"',
        'Read-Host "Press Enter again to clear"',
        "Clear-Host",
        "Do not close the terminal",
    ]
    for item in required:
        assert_true(item in prompt, "Terminal cleanup prompt missing fragment: " + item)
    assert_true("5 seconds" not in prompt.lower(), "Terminal cleanup prompt must not contain stale five-second rule.")

    meta_text = read_text(root, META_REL)
    meta = json.loads(meta_text)
    assert_true(meta.get("prompt_id") == "terminal_cleanup_contract", "Metadata prompt_id mismatch.")
    assert_true(meta.get("status") == "active", "Metadata status must be active.")


def validate_patch_payload(patch_root: Path) -> None:
    """Validate patch package boundaries and scripts."""
    expected = {
        "INSTALL.ps1",
        "VALIDATE.ps1",
        "FREEZE.ps1",
        "PATCH_README.txt",
        "KANDA_FREEZE_HINT.json",
        UI_REL,
        PROMPT_REL,
        META_REL,
        "tools/" + VALIDATOR,
    }
    actual = {
        path.relative_to(patch_root).as_posix()
        for path in patch_root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }
    assert_true(actual == expected, "Unexpected patch payload: " + repr(sorted(actual)))
    for rel in PROTECTED_NOT_PACKAGED:
        assert_true(not (patch_root / rel).exists(), "Protected file was packaged: " + rel)
    for script_name in ("INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"):
        text = read_text(patch_root, script_name)
        assert_true("" not in text, script_name + " contains vertical-tab control character")
        assert_true("" not in text, script_name + " contains form-feed control character")
        assert_true("Downloads" not in text and "Desktop" not in text, script_name + " uses forbidden fallback")


def main() -> int:
    """Run validation for the installed project and exact patch payload."""
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    validate_ui(root)
    validate_prompt(root)
    patch_root = Path(__file__).resolve().parents[1]
    validate_patch_payload(patch_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
