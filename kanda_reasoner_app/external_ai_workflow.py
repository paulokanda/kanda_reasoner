# project-path: kanda_reasoner_app/external_ai_workflow.py
"""Shared manual external-AI handoff facade for existing KANDA workflows."""

from __future__ import annotations

from dataclasses import dataclass

from kanda_reasoner_app.external_ai_configuration import (
    application_external_ai_configuration,
)
from kanda_reasoner_app.external_ai_handoff import (
    copy_and_open_external_assistant,
)

__all__ = [
    "ExternalAIWorkflowResult",
    "build_external_ai_package_prompt",
    "handoff_package",
    "handoff_to_selected_external_ai",
]


@dataclass(frozen=True, slots=True)
class ExternalAIWorkflowResult:
    """Report one bounded copy-and-open workflow result without browser control."""

    ok: bool
    assistant_id: str
    display_name: str
    copied_characters: int
    browser_open_requested: bool
    official_url: str
    error: str = ""


def handoff_to_selected_external_ai(prompt_text: str) -> ExternalAIWorkflowResult:
    """Copy one reviewed prompt and open the selected official assistant site."""
    assistant_id = ""
    display_name = ""
    try:
        controller = application_external_ai_configuration()
        assistant = controller.selected_assistant()
        assistant_id = assistant.assistant_id
        display_name = assistant.display_name
        result = copy_and_open_external_assistant(assistant, prompt_text)
    except (RuntimeError, ValueError) as exc:
        return ExternalAIWorkflowResult(
            ok=False,
            assistant_id=assistant_id,
            display_name=display_name,
            copied_characters=0,
            browser_open_requested=False,
            official_url="",
            error=type(exc).__name__ + ":" + str(exc),
        )
    return ExternalAIWorkflowResult(
        ok=True,
        assistant_id=result.assistant_id,
        display_name=display_name,
        copied_characters=result.copied_characters,
        browser_open_requested=result.browser_open_requested,
        official_url=result.official_url,
    )


def build_external_ai_package_prompt(
    *,
    title: str,
    zip_path: str,
    task_text: str,
    task_path: str = "",
    package_sha256: str = "",
) -> str:
    """Build deterministic manual instructions for one already-governed package."""
    clean_title = str(title or "").strip()
    clean_zip_path = str(zip_path or "").strip()
    clean_task = str(task_text or "").strip()
    if not clean_title:
        raise ValueError("External AI package title is empty.")
    if not clean_zip_path:
        raise ValueError("External AI package ZIP path is empty.")
    if not clean_task:
        raise ValueError("External AI package task text is empty.")
    lines = [
        clean_title,
        "",
        "MANUAL EXTERNAL AI HANDOFF",
        "1. Upload the ZIP shown below.",
        "2. Paste the complete task text from this clipboard payload.",
        "3. Review the external answer before importing anything into KANDA.",
        "4. Do not let the external service write canonical Project source.",
        "",
        "PACKAGE_ZIP:",
        clean_zip_path,
    ]
    clean_task_path = str(task_path or "").strip()
    if clean_task_path:
        lines.extend(["", "TASK_FILE:", clean_task_path])
    clean_sha = str(package_sha256 or "").strip().lower()
    if clean_sha:
        lines.extend(["", "PACKAGE_SHA256:", clean_sha])
    lines.extend(["", "TASK_BEGIN", clean_task, "TASK_END"])
    return "\n".join(lines) + "\n"


def handoff_package(
    *,
    title: str,
    zip_path: str,
    task_text: str,
    task_path: str = "",
    package_sha256: str = "",
) -> ExternalAIWorkflowResult:
    """Copy package instructions and open the selected external assistant."""
    try:
        prompt_text = build_external_ai_package_prompt(
            title=title,
            zip_path=zip_path,
            task_text=task_text,
            task_path=task_path,
            package_sha256=package_sha256,
        )
    except ValueError as exc:
        return ExternalAIWorkflowResult(
            ok=False,
            assistant_id="",
            display_name="",
            copied_characters=0,
            browser_open_requested=False,
            official_url="",
            error=type(exc).__name__ + ":" + str(exc),
        )
    return handoff_to_selected_external_ai(prompt_text)
