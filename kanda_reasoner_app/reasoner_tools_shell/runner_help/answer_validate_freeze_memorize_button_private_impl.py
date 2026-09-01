"""Clipboard owner for the complete Answer/Validate/Freeze routine."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from kanda_reasoner_app.project_artifact_staging import (
    build_project_artifact_staging_contract,
)
from kanda_reasoner_app.project_support_boundary import (
    canonical_project_support_root,
)

__all__ = [
    "build_answer_validate_freeze_memorize_wrapper",
    "copy_answer_validate_freeze_memorize_to_clipboard",
]

_LOGGER = logging.getLogger(__name__)

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
    support_root = canonical_project_support_root(project_root)
    staging = build_project_artifact_staging_contract(project_root)
    transient_root = Path(str(staging["transient_root"]))
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
        "Artifact root inbox: " + str(staging["root_inbox"]),
        "Artifact staging required before use: YES",
        "Artifact staging integrity: copy, SHA-256 verify, then remove root source",
        "Project-switch rule: re-derive paths and recheck selection_ticket before root-source deletion",
        "Canonical prompt source: " + str(prompt_path),
        "Project interpreter: resolve from current Project handoff or validator owner; do not default to plain python.",
        "Hard boundary: selected Project owns payload, install, live validation, Freeze memory, and Error Memory.",
        "Tool boundary: KANDA Reasoner owns this prompt and governance UI; do not patch it for an external Project failure unless a separate Tool defect is proven.",
        "Continuation rule: resume from the last reliable marker; need new training prompt: NO.",
        "Compact update rule: use current uploaded artifacts, pasted compact updates, local validation output, Freeze snippets, and Error Memory evidence as one continuation context.",
        "Single-ZIP rule: one primary feature release uses one self-contained update ZIP with packaged install and validation scripts; do not create separate installer, validator, runner, or disposable validation-report downloads.",
        "Terminal chain rule: deliver one paste-safe INSTALL -> Enter -> Enter -> Clear-Host -> VALIDATE chain; INSTALL.ps1 and VALIDATE.ps1 remain separate owners, and any failed phase stops later phases.",
        "Freeze rule: after current VALIDATION OK and STATUS: IN_SYNC, prepare Freeze directly; Preview and Confirm and Write remain human-only.",
        "Error Memory end rule: evaluate verified reusable non-duplicate failures only after the validated Freeze is confirmed correct; emit Error Memory separately when required; Memorize Error remains human-only.",
        "Stop rule: if ZIP staging, INSTALL, VALIDATE, Freeze audit/intake, or Error Memory admission fails, stop at that phase and do not emit later-phase artifacts.",
        "PowerShell paste rule: the INSTALL->VALIDATE wrapper is one independent paste unit using separate packaged scripts; prefer direct script invocation; no else, elseif, or finally.",
        "",
        _PROMPT_BEGIN,
        prompt_text,
        _PROMPT_END,
        _END,
    ]
    return "\n".join(lines) + "\n"


def copy_answer_validate_freeze_memorize_to_clipboard(window: object) -> bool:
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
        return True
    except Exception as exc:
        message = "[ERROR] Could not copy Answer, Validate, Freeze, Memorize Error routine: " + str(exc)
        _LOGGER.exception(message)
        _set_status(window, message)
        _append_log(window, message)
        return False


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
