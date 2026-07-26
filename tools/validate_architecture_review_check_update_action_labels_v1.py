"""Validate beginner-facing Architecture Review action labels."""

from __future__ import annotations

import ast
from pathlib import Path
import sys

__all__ = ["main"]

FEATURE_ID = "architecture-review-check-update-action-labels-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUBTABS_REL = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
MODE_UI_REL = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_mode_ui.py"
)
HELP_SOURCE_REL = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/"
    "architecture_review.md"
)
HELP_RENDERED_REL = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/"
    "architecture_review.html"
)
EXPECTED_LABELS = {
    "validate": "Validate Project",
    "diff": "Preview Changes",
    "scan": "Scan Project",
    "write": "Write Architecture Files",
}


class FakeSignal:
    """Capture and emit one text-change callback."""

    def __init__(self) -> None:
        self._callback = None

    def connect(self, callback: object) -> None:
        self._callback = callback

    def emit(self, value: str) -> None:
        if self._callback is None:
            raise AssertionError("SIGNAL_CALLBACK_NOT_CONNECTED")
        self._callback(value)


class FakeCombo:
    """Small mode-combo substitute for headless validation."""

    def __init__(self, current_text: str) -> None:
        self._current_text = current_text
        self.currentTextChanged = FakeSignal()

    def currentText(self) -> str:
        return self._current_text


class FakeButton:
    """Capture the latest button label."""

    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


def require(condition: bool, marker: str) -> None:
    """Print one marker or raise a focused validation error."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def read_text(relative_path: Path) -> str:
    """Read one project file as UTF-8 text."""
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"MISSING_FILE:{relative_path.as_posix()}")
    return path.read_text(encoding="utf-8")


def validate_python_contract() -> None:
    """Validate syntax, module size, and visible GUI wiring."""
    subtabs_text = read_text(SUBTABS_REL)
    mode_ui_text = read_text(MODE_UI_REL)
    for relative_path, source in (
        (SUBTABS_REL, subtabs_text),
        (MODE_UI_REL, mode_ui_text),
    ):
        ast.parse(source, filename=str(relative_path))
        require(
            len(source.splitlines()) <= 500,
            f"MODULE_MAX_500_LINES:{relative_path.as_posix()}",
        )
        source.encode("ascii")

    require(
        'QPushButton("Check Update Architecture")' in subtabs_text
        or '"Check Update Architecture"' in subtabs_text,
        "CHECK_UPDATE_ARCHITECTURE_SUBTAB_LABEL",
    )
    require(
        'QPushButton("Validate Project")' in subtabs_text,
        "DEFAULT_VALIDATE_PROJECT_BUTTON_LABEL",
    )
    require(
        "bind_mode_action_button" in subtabs_text,
        "MODE_SELECTION_UPDATES_ACTION_BUTTON",
    )
    require(
        '["validate", "diff", "scan", "write"]' in subtabs_text,
        "TECHNICAL_MODE_NAMES_PRESERVED",
    )


def validate_mode_label_mapping() -> None:
    """Execute the real pure label mapping without importing Qt."""
    sys.path.insert(0, str(PROJECT_ROOT))
    from kanda_reasoner_app.manage_architecture import (
        architecture_review_mode_ui,
    )

    for mode, expected_label in EXPECTED_LABELS.items():
        require(
            architecture_review_mode_ui.action_label_for_mode(mode)
            == expected_label,
            f"MODE_LABEL_{mode.upper()}",
        )
    require(
        architecture_review_mode_ui.action_label_for_mode("unknown")
        == "Run Selected Action",
        "UNKNOWN_MODE_SAFE_FALLBACK",
    )

    combo = FakeCombo("validate")
    button = FakeButton()
    architecture_review_mode_ui.bind_mode_action_button(combo, button)
    require(button.text == "Validate Project", "INITIAL_MODE_LABEL_SYNC")
    combo.currentTextChanged.emit("diff")
    require(button.text == "Preview Changes", "SIGNAL_MODE_LABEL_SYNC")


def validate_help_alignment() -> None:
    """Ensure canonical and rendered help use the new visible labels."""
    source_text = read_text(HELP_SOURCE_REL)
    rendered_text = read_text(HELP_RENDERED_REL)
    source_labels = (
        "Check Update Architecture",
        *EXPECTED_LABELS.values(),
    )
    rendered_labels = (
        "Check Update Architecture",
        *EXPECTED_LABELS.values(),
    )
    for label in source_labels:
        require(label in source_text, f"HELP_SOURCE_LABEL:{label}")
    for label in rendered_labels:
        require(label in rendered_text, f"HELP_RENDERED_LABEL:{label}")
    require(
        "Run Selected Mode" not in source_text,
        "HELP_SOURCE_OLD_LABEL_REMOVED",
    )
    require(
        "Run Selected Mode" not in rendered_text,
        "HELP_RENDERED_OLD_LABEL_REMOVED",
    )


def main() -> int:
    """Run focused validation for the Architecture Review label update."""
    validate_python_contract()
    validate_mode_label_mapping()
    validate_help_alignment()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(
        "VALIDATION OK: "
        "audit-project-architecture-review-three-level-tabs-v1"
    )
    print(
        "VALIDATION OK: "
        "audit-project-architecture-review-three-level-tabs-v1r2"
    )
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
