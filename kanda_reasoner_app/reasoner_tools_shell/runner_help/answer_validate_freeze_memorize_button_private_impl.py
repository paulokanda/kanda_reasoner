"""Clipboard owner for the complete Answer/Validate/Freeze routine."""

from __future__ import annotations

import os
from pathlib import Path

__all__ = [
    "build_answer_validate_freeze_memorize_wrapper",
    "copy_answer_validate_freeze_memorize_to_clipboard",
]

_PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "patch_validate_freeze_error_memory_routine_blueprint.md"
)
_BEGIN = "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT_BEGIN"
_END = "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT_END"
_PROMPT_BEGIN = "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_PROMPT_BEGIN"
_PROMPT_END = "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_PROMPT_END"


def build_answer_validate_freeze_memorize_wrapper(
    selected_project_root: str | Path,
    *,
    tool_root: str | Path | None = None,
) -> str:
    """Build the routine prompt with resolved Tool and Project identities."""
    project_root = _resolve_existing_directory(selected_project_root, "Selected project")
    resolved_tool_root = _resolve_existing_directory(
        tool_root if tool_root is not None else Path(__file__).resolve().parents[3],
        "KANDA Reasoner tool",
    )
    prompt_path = resolved_tool_root / _PROMPT_REL
    if not prompt_path.is_file():
        raise FileNotFoundError("Canonical routine prompt not found: " + str(prompt_path))

    project_slug = project_root.name
    support_root = project_root.parent / (project_slug + "_show_project_to_AI")
    transient_root = project_root.parent / (project_slug + "_delete_after_daily_work")
    same_physical = _same_physical_root(project_root, resolved_tool_root)
    prompt_text = prompt_path.read_text(encoding="utf-8-sig").rstrip()

    lines = [
        _BEGIN,
        "Selected project slug: " + project_slug,
        "Selected project source root: " + str(project_root),
        "KANDA Reasoner tool root: " + str(resolved_tool_root),
        "Same physical root: " + ("YES" if same_physical else "NO"),
        "Selected Project Support root: " + str(support_root),
        "Selected project-linked transient root: " + str(transient_root),
        "Canonical prompt source: " + str(prompt_path),
        "Project interpreter: resolve from current Project handoff or validator owner; do not default to plain python.",
        "Hard boundary: selected Project owns payload, install, live validation, Freeze memory, and Error Memory.",
        "Tool boundary: KANDA Reasoner owns this prompt and governance UI; do not patch it for an external Project failure unless a separate Tool defect is proven.",
        "Continuation rule: resume from the last reliable marker; need new training prompt: NO.",
        "PowerShell paste rule: every user-facing block is one independent paste unit; prefer direct packaged scripts; no else, elseif, or finally.",
        "",
        _PROMPT_BEGIN,
        prompt_text,
        _PROMPT_END,
        _END,
    ]
    return "\n".join(lines) + "\n"


def copy_answer_validate_freeze_memorize_to_clipboard(window: object) -> None:
    """Copy the resolved cross-project routine wrapper to the clipboard."""
    try:
        from PySide6.QtWidgets import QApplication

        raw_root = str(getattr(window, "project_root_edit").text()).strip()
        if not raw_root:
            raise ValueError("Project root field is empty.")
        text = build_answer_validate_freeze_memorize_wrapper(raw_root)
        QApplication.clipboard().setText(text)
        message = "Copied complete routine for selected Project: " + Path(raw_root).name
        _set_status(window, message)
        _append_log(window, message)
    except Exception as exc:
        message = "[ERROR] Could not copy Answer, Validate, Freeze, Memorize Error routine: " + str(exc)
        _set_status(window, message)
        _append_log(window, message)


def _resolve_existing_directory(value: str | Path, label: str) -> Path:
    text = str(value).strip()
    if not text:
        raise ValueError(label + " root is empty.")
    path = Path(text).expanduser().resolve(strict=False)
    if not path.is_dir():
        raise FileNotFoundError(label + " root is not a directory: " + str(path))
    return path


def _same_physical_root(left: Path, right: Path) -> bool:
    try:
        return os.path.samefile(left, right)
    except OSError:
        return os.path.normcase(str(left)) == os.path.normcase(str(right))


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
