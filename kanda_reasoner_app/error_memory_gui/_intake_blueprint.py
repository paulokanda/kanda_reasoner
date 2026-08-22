# project-path: kanda_reasoner_app/error_memory_gui/_intake_blueprint.py
"""Non-GUI helpers for Error Memory intake blueprint clipboard payloads."""
from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tool_runtime_identity import (
    current_tool_runtime_identity,
)

ERROR_MEMORY_TEMPLATE_RELATIVE_DIR = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons"
)
ERROR_MEMORY_AI_FORMULARY_CANON_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/error_memory_ai_formulary_startup_canon.md"
)
SEND_ZIP_ERRORS_PROMPT_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/self_contained_error_memory_lesson_intake_zip.md"
)
ACTIVE_READY_JSON_TEMPLATE_NAME = "error_memory_active_ready_json_template.md"
MODEL_TEMPLATE_NAME = "error_memory_model_template.md"

__all__ = [
    "ACTIVE_READY_JSON_TEMPLATE_NAME",
    "ERROR_MEMORY_AI_FORMULARY_CANON_RELATIVE_PATH",
    "ERROR_MEMORY_TEMPLATE_RELATIVE_DIR",
    "MODEL_TEMPLATE_NAME",
    "SEND_ZIP_ERRORS_PROMPT_RELATIVE_PATH",
    "error_lesson_intake_blueprint_clipboard_text",
    "error_memory_ai_formulary_canon_path",
    "error_memory_prompt_template_dir",
    "read_error_memory_ai_formulary_canon",
    "read_error_memory_intake_template_file",
    "read_send_zip_errors_prompt",
    "send_zip_errors_prompt_path",
]


def error_memory_ai_formulary_canon_path(
    project_root: Path | None,
    *,
    module_file: str,
) -> Path:
    """Return the Tool-owned Error Memory startup canon independent of Project."""
    del project_root
    return (
        Path(module_file).resolve(strict=False).parents[2]
        / ERROR_MEMORY_AI_FORMULARY_CANON_RELATIVE_PATH
    )


def read_error_memory_ai_formulary_canon(
    project_root: Path,
    *,
    module_file: str,
) -> str:
    """Read the canonical Error Memory AI formulary startup prompt."""
    path = error_memory_ai_formulary_canon_path(
        project_root,
        module_file=module_file,
    )
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(
            "Error Memory AI formulary startup canon not found: " + str(path)
        )
    return path.read_text(encoding="utf-8")


def send_zip_errors_prompt_path(
    project_root: Path | None,
    *,
    module_file: str,
) -> Path:
    """Return the Tool-owned Error Memory lesson ZIP prompt."""
    del project_root
    return (
        Path(module_file).resolve(strict=False).parents[2]
        / SEND_ZIP_ERRORS_PROMPT_RELATIVE_PATH
    )


def _source_zip_error_intake_available() -> bool:
    """Return whether executable Error Memory ZIP intake is source-safe."""
    mode = str(current_tool_runtime_identity().runtime_mode).strip().upper()
    return mode == "SOURCE"


def read_send_zip_errors_prompt(project_root: Path, *, module_file: str) -> str:
    """Read the runtime-safe Error Memory delivery prompt."""
    if not _source_zip_error_intake_available():
        return error_lesson_intake_blueprint_clipboard_text(
            project_root,
            context_text="",
            module_file=module_file,
        )
    path = send_zip_errors_prompt_path(project_root, module_file=module_file)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError("Send Zip Errors prompt not found: " + str(path))
    return path.read_text(encoding="utf-8")


def error_memory_prompt_template_dir(project_root: Path, *, module_file: str) -> Path:
    """Return the prompt-library folder containing Error Memory intake templates."""
    root = Path(project_root).expanduser().resolve(strict=False)
    candidates = [
        root / ERROR_MEMORY_TEMPLATE_RELATIVE_DIR,
        Path(module_file).resolve(strict=False).parents[2] / ERROR_MEMORY_TEMPLATE_RELATIVE_DIR,
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    return candidates[0]


def read_error_memory_intake_template_file(project_root: Path, filename: str, *, module_file: str) -> str:
    """Read one Error Memory intake prompt template from the active prompt library."""
    path = error_memory_prompt_template_dir(project_root, module_file=module_file) / filename
    if not path.exists() or not path.is_file():
        raise FileNotFoundError("Error Memory intake template not found: " + str(path))
    return path.read_text(encoding="utf-8")


def error_lesson_intake_blueprint_clipboard_text(
    project_root: Path,
    *,
    context_text: str = "",
    module_file: str,
) -> str:
    """Return clipboard text that instructs AI how to create active-ready intake JSON."""
    json_template = read_error_memory_intake_template_file(
        project_root,
        ACTIVE_READY_JSON_TEMPLATE_NAME,
        module_file=module_file,
    )
    model_template = read_error_memory_intake_template_file(
        project_root,
        MODEL_TEMPLATE_NAME,
        module_file=module_file,
    )
    template_dir = error_memory_prompt_template_dir(project_root, module_file=module_file)
    sections = [
        "ERROR MEMORY AI INTAKE REQUEST",
        "Task for AI: create or correct one KANDA Error Memory lesson for the KANDA Reasoner Error Memory tab -> AI-assisted error lesson intake text window.",
        "Before writing the intake lesson, read and follow these templates in order:",
        "1. kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_active_ready_json_template.md",
        "2. kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/error_memory_model_template.md",
        "Return exactly one KANDA_ERROR_LESSON_JSON_BEGIN / KANDA_ERROR_LESSON_JSON_END block, with no markdown fence and no prose around it. Replace every placeholder with concrete evidence. Do not invent validation evidence.",
        "",
        "LOCAL TEMPLATE DIRECTORY:",
        str(template_dir),
    ]
    if context_text.strip():
        sections.extend(["", "ERROR OR DRAFT CONTEXT TO CONVERT:", context_text.strip()])
    sections.extend(
        [
            "",
            "--- BEGIN error_memory_active_ready_json_template.md ---",
            json_template.rstrip(),
            "--- END error_memory_active_ready_json_template.md ---",
            "",
            "--- BEGIN error_memory_model_template.md ---",
            model_template.rstrip(),
            "--- END error_memory_model_template.md ---",
        ]
    )
    return "\n".join(sections).strip() + "\n"
