"""Validate show-project-answer-button-label-international-orange-v1."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "show-project-answer-button-label-international-orange-v1"
UI_REL = "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py"
BUTTON_TEXT = "Answer, Validate, Freeze, Memorize Error"
ORANGE_HEX = "#f04A00"


PROTECTED = [
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_persistence.py",
    "kanda_reasoner_app/error_memory_gui/_lesson_status_summary.py",
    "kanda_reasoner_app/error_memory_gui/_table_view.py",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_validate_freeze_error_memory_routine_blueprint.md",
]


def assert_true(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear validation message."""
    if not condition:
        raise AssertionError(message)


def read_text(root: Path, rel: str) -> str:
    """Read a UTF-8 source file."""
    path = root / rel
    assert_true(path.is_file(), "Missing file: " + rel)
    return path.read_text(encoding="utf-8")


def validate_ui(root: Path) -> None:
    """Validate that only the button text label color is set to orange."""
    path = root / UI_REL
    text = read_text(root, UI_REL)
    required = [
        "from PySide6.QtGui import QColor, QFont, QPalette",
        "copy_patch_validate_freeze_routine_button",
        BUTTON_TEXT,
        "answer_routine_button_palette = (",
        "QPalette.ButtonText",
        "QColor(\"" + ORANGE_HEX + "\")",
        "setPalette(",
        "patch_validate_freeze_error_memory_routine_blueprint.md",
        "QApplication.clipboard().setText",
    ]
    for item in required:
        assert_true(item in text, "UI missing required fragment: " + item)
    button_index = text.index("self.copy_patch_validate_freeze_routine_button = QPushButton")
    palette_index = text.index("answer_routine_button_palette = (", button_index)
    set_color_index = text.index("QPalette.ButtonText", palette_index)
    set_palette_index = text.index("self.copy_patch_validate_freeze_routine_button.setPalette", set_color_index)
    add_index = text.index("project_root_row.addWidget(self.copy_patch_validate_freeze_routine_button)", button_index)
    assert_true(
        button_index < palette_index < set_color_index < set_palette_index < add_index,
        "Button label palette must be applied before adding the button to the row.",
    )
    forbidden_after_button = text[button_index:add_index]
    assert_true(
        "copy_patch_validate_freeze_routine_button.setStyleSheet" not in forbidden_after_button,
        "Do not style the full button; only set QPalette.ButtonText for the label.",
    )
    assert_true(ORANGE_HEX in text, "International Orange color must use exact requested hex.")
    assert_true("#F04A00" not in text, "Do not replace the requested lowercase hex with uppercase variant.")
    assert_true("Downloads" not in text and "Desktop" not in text, "UI copy helper must not use Downloads/Desktop fallback.")
    line_count = len(text.splitlines())
    assert_true(line_count <= 500, "Touched UI module exceeds 500 lines: " + str(line_count))
    py_compile.compile(str(path), doraise=True)


def validate_protected_files_not_packaged(patch_root: Path) -> None:
    """Ensure this patch does not include protected files."""
    for rel in PROTECTED:
        assert_true(not (patch_root / rel).exists(), "Protected file was packaged: " + rel)


def validate_patch_scripts(patch_root: Path) -> None:
    """Reject control characters and stale forbidden paths in patch scripts."""
    for name in ("INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"):
        text = read_text(patch_root, name)
        assert_true("\x0b" not in text, name + " contains vertical-tab control character")
        assert_true("\x0c" not in text, name + " contains form-feed control character")
        assert_true("Downloads" not in text and "Desktop" not in text, name + " uses forbidden fallback")


def main() -> int:
    """Run validation for installed project."""
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    validate_ui(root)
    patch_root = Path(__file__).resolve().parents[1]
    validate_protected_files_not_packaged(patch_root)
    validate_patch_scripts(patch_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
