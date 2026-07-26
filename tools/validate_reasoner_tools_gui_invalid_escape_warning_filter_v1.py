# project-path: tools/test_reasoner_tools_gui_invalid_escape_warning_filter_v1.py
"""Validate reasoner-tools-gui-invalid-escape-warning-filter-v1."""

from __future__ import annotations

import importlib.util
import json
import py_compile
import warnings
from pathlib import Path

FEATURE_ID = "reasoner-tools-gui-invalid-escape-warning-filter-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = PROJECT_ROOT / "reasoner_tools_gui.py"
LESSON_ID = "lesson-reasoner-tools-gui-invalid-escape-warning-filter-v1"

__all__ = ["main"]


def require(condition: bool, message: str) -> None:
    """Raise AssertionError when condition is false."""

    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    """Read UTF-8 text with BOM tolerance."""

    return path.read_text(encoding="utf-8-sig", errors="replace")


def _project_name() -> str:
    """Return the active project folder name."""

    return PROJECT_ROOT.name


def _daily_root() -> Path:
    """Return the expected daily-work root."""

    return PROJECT_ROOT.drive + "/" if False else PROJECT_ROOT.parent / (_project_name() + "_delete_after_daily_work")


def _support_root() -> Path:
    """Return the expected Show Project support root."""

    return PROJECT_ROOT.parent / (_project_name() + "_show_project_to_AI")


def _pending_lesson_path() -> Path:
    """Return the expected pending Error Memory lesson path."""

    return (
        _support_root()
        / "project_error_memory"
        / "pending_ai_assisted_error_lesson_intake"
        / (LESSON_ID + ".txt")
    )


def validate_compile() -> None:
    """Compile the changed launcher."""

    require(LAUNCHER.is_file(), "Missing launcher: " + str(LAUNCHER))
    py_compile.compile(str(LAUNCHER), doraise=True)


def validate_launcher_filter_text() -> None:
    """Verify the launcher contains the narrow warning filter."""

    text = _read(LAUNCHER)
    require("def _configure_known_warning_filters" in text, "Missing warning filter helper.")
    require("warnings.filterwarnings" in text, "Missing warnings.filterwarnings call.")
    require("invalid escape sequence" in text, "Missing invalid-escape message filter.")
    require("category=SyntaxWarning" in text, "Filter must target SyntaxWarning.")
    require('simplefilter("ignore", SyntaxWarning)' not in text, "Do not silence all SyntaxWarning output.")


def validate_filter_behavior() -> None:
    """Import the launcher and verify only the observed warning is suppressed."""

    spec = importlib.util.spec_from_file_location("_kanda_launcher_warning_filter_check", LAUNCHER)
    require(spec is not None and spec.loader is not None, "Could not build launcher import spec.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    with warnings.catch_warnings(record=True) as records:
        warnings.warn("invalid escape sequence '\\['", SyntaxWarning)
        warnings.warn("unrelated syntax warning should remain visible", SyntaxWarning)

    messages = [str(item.message) for item in records]
    require(
        "invalid escape sequence '\\['" not in messages,
        "Observed invalid-escape warning was not suppressed.",
    )
    require(
        "unrelated syntax warning should remain visible" in messages,
        "Unrelated SyntaxWarning was suppressed unexpectedly.",
    )


def validate_pending_error_memory_lesson() -> None:
    """Verify the Error Memory lesson was staged for the tab."""

    pending = _pending_lesson_path()
    require(pending.is_file(), "Pending Error Memory lesson not found: " + str(pending))
    text = _read(pending)
    require(text.startswith("KANDA_ERROR_LESSON_JSON_BEGIN"), "Missing Error Memory begin marker.")
    require(text.rstrip().endswith("KANDA_ERROR_LESSON_JSON_END"), "Missing Error Memory end marker.")
    body = text.split("KANDA_ERROR_LESSON_JSON_BEGIN", 1)[1].split("KANDA_ERROR_LESSON_JSON_END", 1)[0]
    payload = json.loads(body)
    require(payload.get("lesson_id") == LESSON_ID, "Lesson id mismatch.")
    redaction = payload.get("redaction") or {}
    require(redaction.get("applied") is True, "Redaction applied must be true.")
    require(redaction.get("export_safe") is True, "Redaction export_safe must be true.")
    require(bool(redaction.get("rules")), "Redaction rules must be present.")
    regression = payload.get("regression_check") or {}
    require(regression.get("type") == "validation_command", "Regression check type mismatch.")
    require(bool(regression.get("command")), "Regression command missing.")
    require(bool(regression.get("expected_marker")), "Regression expected marker missing.")
    require(regression.get("required_before_freeze") is True, "Regression freeze gate missing.")
    require(bool(payload.get("validation_evidence")), "Validation evidence missing.")


def main() -> int:
    """Run focused validation."""

    validate_compile()
    validate_launcher_filter_text()
    validate_filter_behavior()
    validate_pending_error_memory_lesson()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
