"""Validate the surgical Show Project to AI toolbar-only UI update."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path


FEATURE_ID = "show-project-toolbar-surgical-ui-v1"
WINDOW_RELATIVE = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "window_methods_private_impl.py"
)
CONTROLS_RELATIVE = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "png_reuse_cancel_controls_private_impl.py"
)


def require(condition: bool, message: str) -> None:
    """Raise an assertion with a clear validation message."""
    if not condition:
        raise AssertionError(message)


def read_text(root: Path, relative_path: Path) -> str:
    """Read one required UTF-8 source file."""
    path = root / relative_path
    require(path.is_file(), "Required source file is missing: " + str(path))
    return path.read_text(encoding="utf-8")


def validate_python(text: str, relative_path: Path) -> None:
    """Compile source text through the Python parser."""
    ast.parse(text, filename=str(relative_path))


def validate_toolbar_layout(window_text: str, controls_text: str) -> None:
    """Validate the three requested visual changes and preserved wiring."""
    create_add = (
        "project_root_row.addWidget("
        "self.create_first_and_second_prompt_files_button)"
    )
    install_call = "_png_controls.install_controls(self, project_root_row)"
    cancel_add = "row.addWidget(window.cancel_prompt_files_button)"
    reuse_add = "row.addWidget(window.copy_png_reuse_prompt_button)"

    require(create_add in window_text, "Create button layout marker is missing.")
    require(install_call in window_text, "PNG control installation marker is missing.")
    require(
        window_text.index(create_add) < window_text.index(install_call),
        "Create button must remain before the combined controls.",
    )
    require(cancel_add in controls_text, "Cancel button layout marker is missing.")
    require(reuse_add in controls_text, "Reuse PNG layout marker is missing.")
    require(
        controls_text.index(cancel_add) < controls_text.index(reuse_add),
        "Cancel must be immediately before Reuse PNG inside the helper order.",
    )
    require(
        'QPushButton("Cancel")' in controls_text,
        "Cancel button text changed unexpectedly.",
    )
    require(
        'QColor("#008000")' in controls_text,
        "Cancel button green font contract changed unexpectedly.",
    )
    print("CANCEL_IMMEDIATELY_RIGHT_OF_CREATE: PASS")


def validate_removed_label(window_text: str) -> None:
    """Validate removal of the requested label only."""
    require(
        "AI answer Routine Blueprint" not in window_text,
        "The AI answer Routine Blueprint label is still present.",
    )
    require(
        "copy_patch_validate_freeze_routine_button" in window_text,
        "The routine button must remain present.",
    )
    print("AI_ANSWER_ROUTINE_LABEL_REMOVED: PASS")


def validate_logic_rename(window_text: str) -> None:
    """Validate text-only rename while preserving object and signal wiring."""
    require(
        'self.copy_machine_card_logic_button = QPushButton("Logic")'
        in window_text,
        "Machine-Card button text was not renamed to Logic.",
    )
    require(
        'QPushButton("MCard Logic")' not in window_text,
        "Legacy MCard Logic button text remains in active UI source.",
    )
    require(
        "self.copy_machine_card_logic_button.clicked.connect(" in window_text,
        "Machine-Card button signal wiring is missing.",
    )
    require(
        "copy_machine_card_logic_to_clipboard(self)" in window_text,
        "Machine-Card clipboard action changed unexpectedly.",
    )
    print("MCARD_LOGIC_BUTTON_RENAMED_LOGIC: PASS")


def validate_preserved_controls_logic(controls_text: str) -> None:
    """Validate that only layout order changed in the helper."""
    required_markers = (
        "PNG_REUSE_PROMPT = (",
        "def copy_prompt() -> None:",
        "QApplication.clipboard().setText(PNG_REUSE_PROMPT)",
        "def update_cancel_enabled(window: Any) -> None:",
        "def cancel_run(window: Any) -> None:",
        "process.terminate()",
        "process.kill()",
        "def consume_cancel_on_finish(window: Any, finish_status) -> bool:",
        "Previous published delivery was preserved.",
    )
    for marker in required_markers:
        require(marker in controls_text, "Preserved controls marker missing: " + marker)
    print("PNG_REUSE_AND_CANCEL_LOGIC_PRESERVED: PASS")


def validate_module_sizes(root: Path) -> None:
    """Enforce the current 500-line physical module limit."""
    for relative_path in (WINDOW_RELATIVE, CONTROLS_RELATIVE):
        path = root / relative_path
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(
            line_count <= 500,
            str(relative_path) + " exceeds 500 physical lines.",
        )
    print("MODULE_SIZE_GATE: PASS")


def main() -> int:
    """Run the focused source-level regression validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    require(root.is_dir(), "Project root does not exist: " + str(root))

    window_text = read_text(root, WINDOW_RELATIVE)
    controls_text = read_text(root, CONTROLS_RELATIVE)
    validate_python(window_text, WINDOW_RELATIVE)
    validate_python(controls_text, CONTROLS_RELATIVE)
    print("SHOW_PROJECT_TOOLBAR_PYTHON_SYNTAX: PASS")

    validate_toolbar_layout(window_text, controls_text)
    validate_removed_label(window_text)
    validate_logic_rename(window_text)
    validate_preserved_controls_logic(controls_text)
    validate_module_sizes(root)

    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
