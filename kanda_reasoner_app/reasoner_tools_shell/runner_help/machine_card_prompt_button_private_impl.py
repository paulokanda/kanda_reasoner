"""Clipboard wrapper for the canonical Architecture Review Machine-Card prompt."""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "build_machine_card_logic_wrapper",
    "copy_machine_card_logic_to_clipboard",
]

_PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/architecture_review_project_card_machine_canon.md"
)
_BEGIN_MARKER = "KANDA_MACHINE_CARD_LOGIC_BEGIN"
_END_MARKER = "KANDA_MACHINE_CARD_LOGIC_END"


def build_machine_card_logic_wrapper(project_root: str | Path) -> str:
    """Build a wrapper containing the canonical Machine-Card logic prompt."""
    root = Path(project_root).expanduser().resolve(strict=False)
    prompt_path = _resolve_prompt_path(root)
    prompt_text = prompt_path.read_text(encoding="utf-8").rstrip()
    parts = [
        _BEGIN_MARKER,
        "Prompt code: KPR-12-005",
        "Prompt id: architecture_review_project_card_machine_canon",
        "Purpose: apply the canonical Architecture Review Machine-Card lifecycle logic.",
        "Source: canonical KANDA prompt-library file.",
        "",
        "KANDA_MACHINE_CARD_PROMPT_FILE_BEGIN architecture_review_project_card_machine_canon.md",
        prompt_text,
        "KANDA_MACHINE_CARD_PROMPT_FILE_END architecture_review_project_card_machine_canon.md",
        "",
        _END_MARKER,
    ]
    return "\n".join(parts) + "\n"


def copy_machine_card_logic_to_clipboard(window: object) -> None:
    """Copy the canonical Machine-Card logic wrapper to the clipboard."""
    try:
        from PySide6.QtWidgets import QApplication

        raw_root = str(getattr(window, "project_root_edit").text()).strip()
        if not raw_root:
            raise ValueError("Project root field is empty.")
        text = build_machine_card_logic_wrapper(Path(raw_root))
        QApplication.clipboard().setText(text)
        message = "Copied Machine-Card logic prompt to clipboard."
        _set_status(window, message)
        _append_log(window, message)
    except Exception as exc:
        message = "[ERROR] Could not copy Machine-Card logic prompt: " + str(exc)
        _set_status(window, message)
        _append_log(window, message)


def _resolve_prompt_path(project_root: Path) -> Path:
    selected = project_root / _PROMPT_REL
    if selected.is_file():
        return selected
    app_root = Path(__file__).resolve().parents[3]
    fallback = app_root / _PROMPT_REL
    if fallback.is_file():
        return fallback
    raise FileNotFoundError("Canonical Machine-Card prompt not found: " + str(_PROMPT_REL))


def _set_status(window: object, message: str) -> None:
    status = getattr(window, "first_prompt_status_label", None)
    if status is not None:
        try:
            status.setText(message)
        except Exception:
            pass


def _append_log(window: object, message: str) -> None:
    try:
        getattr(window, "_append_log")(message)
    except Exception:
        pass
