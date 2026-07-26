"""Clipboard helpers for Show Project anti-hallucination prompt groups."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

__all__ = [
    "build_full_anti_hallucination_group",
    "build_short_anti_hallucination_group",
    "copy_full_anti_hallucination_group_to_clipboard",
    "copy_short_anti_hallucination_group_to_clipboard",
]

_PROMPT_DIR = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "09_python_quality_security_observability"
)

_FULL_FILES = (
    "anti_hallucination_full_group.md",
    "anti_hallucination_independent_ai_audit_full.md",
    "anti_hallucination_web_evidence_audit_full.md",
    "anti_hallucination_book_literature_audit_full.md",
    "anti_hallucination_master_protocol_full.md",
)

_SHORT_FILES = (
    "anti_hallucination_short_group.md",
    "anti_hallucination_independent_ai_audit_short.md",
    "anti_hallucination_web_evidence_audit_short.md",
    "anti_hallucination_book_literature_audit_short.md",
    "anti_hallucination_protocol_short.md",
)


def build_full_anti_hallucination_group(project_root: str | Path) -> str:
    """Build the complete anti-hallucination prompt group wrapper."""
    return _build_group(
        project_root,
        label="FULL",
        filenames=_FULL_FILES,
        begin_marker="KANDA_ANTI_HALLUCINATION_FULL_BEGIN",
        end_marker="KANDA_ANTI_HALLUCINATION_FULL_END",
    )


def build_short_anti_hallucination_group(project_root: str | Path) -> str:
    """Build the summarized anti-hallucination prompt group wrapper."""
    return _build_group(
        project_root,
        label="SHORT",
        filenames=_SHORT_FILES,
        begin_marker="KANDA_ANTI_HALLUCINATION_SHORT_BEGIN",
        end_marker="KANDA_ANTI_HALLUCINATION_SHORT_END",
    )


def copy_full_anti_hallucination_group_to_clipboard(window: object) -> None:
    """Copy the full anti-hallucination group to the clipboard."""
    _copy_group(window, "Full", build_full_anti_hallucination_group)


def copy_short_anti_hallucination_group_to_clipboard(window: object) -> None:
    """Copy the short anti-hallucination group to the clipboard."""
    _copy_group(window, "Short", build_short_anti_hallucination_group)


def _build_group(
    project_root: str | Path,
    *,
    label: str,
    filenames: Iterable[str],
    begin_marker: str,
    end_marker: str,
) -> str:
    root = Path(project_root).expanduser().resolve(strict=False)
    prompt_dir = _resolve_prompt_dir(root)
    output = [begin_marker]
    output.append("Purpose: pass the " + label + " anti-hallucination prompt group to AI.")
    output.append("Source: canonical KANDA prompt-library files in declared order.")
    for index, filename in enumerate(filenames, start=1):
        path = prompt_dir / filename
        if not path.is_file():
            raise FileNotFoundError("Anti-hallucination prompt not found: " + str(path))
        output.append("")
        output.append("KANDA_ANTI_HALLUCINATION_FILE_BEGIN " + str(index) + " " + filename)
        output.append(path.read_text(encoding="utf-8").rstrip())
        output.append("KANDA_ANTI_HALLUCINATION_FILE_END " + str(index) + " " + filename)
    output.append("")
    output.append(end_marker)
    return "\n".join(output) + "\n"


def _resolve_prompt_dir(project_root: Path) -> Path:
    selected = project_root / _PROMPT_DIR
    if selected.is_dir():
        return selected
    app_root = Path(__file__).resolve().parents[3]
    fallback = app_root / _PROMPT_DIR
    if fallback.is_dir():
        return fallback
    raise FileNotFoundError("Canonical anti-hallucination prompt folder not found: " + str(_PROMPT_DIR))


def _copy_group(window: object, label: str, builder) -> None:
    try:
        from PySide6.QtWidgets import QApplication

        raw_root = str(getattr(window, "project_root_edit").text()).strip()
        if not raw_root:
            raise ValueError("Project root field is empty.")
        text = builder(Path(raw_root))
        QApplication.clipboard().setText(text)
        message = "Copied Anti-hallucination " + label + " group to clipboard."
        _set_status(window, message)
        _append_log(window, message)
    except Exception as exc:
        message = "[ERROR] Could not copy Anti-hallucination " + label + " group: " + str(exc)
        _set_status(window, message)
        _append_log(window, message)


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
