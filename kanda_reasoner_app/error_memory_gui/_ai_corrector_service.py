# project-path: kanda_reasoner_app/error_memory_gui/_ai_corrector_service.py
"""Service-layer runner for local AI Error Memory correction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kanda_reasoner_app.error_memory_gui._ai_evidence_recovery import (
    recover_validation_evidence,
)
from kanda_reasoner_app.error_memory_gui._ai_prompt_builder import (
    build_error_memory_correction_messages,
    build_error_memory_retry_messages,
)
from kanda_reasoner_app.error_memory_gui._ai_response_validator import (
    AIResponseValidationError,
    ValidatedLessonBlock,
    build_source_lesson_defaults,
    format_lesson_block,
    parse_one_lesson_block,
)
from kanda_reasoner_app.reasoner_engine.local_ai_chat_service import (
    LocalAIChatError,
    chat_with_local_model,
    get_local_ai_model_candidates,
)

__all__ = [
    "ErrorMemoryAICorrectionResult",
    "correct_error_memory_lesson_with_local_ai",
]


@dataclass(frozen=True)
class ErrorMemoryAICorrectionResult:
    """Result of one local AI Error Memory correction request."""

    ok: bool
    lesson_block: ValidatedLessonBlock | None
    message: str
    model_name: str = ""
    raw_response: str = ""


def _request_model(
    messages: list[dict[str, str]],
    *,
    model_name: str,
) -> tuple[str, str]:
    """Request one model response for Error Memory correction."""
    return chat_with_local_model(
        messages,
        model_selection=model_name,
        temperature=0.03,
        max_tokens=4200,
    )


def _has_placeholder_evidence(block: ValidatedLessonBlock) -> bool:
    """Return whether validation evidence is only the draft placeholder."""
    evidence = block.lesson.get("validation_evidence")
    if not isinstance(evidence, list):
        return False
    joined = "\n".join(str(item).lower() for item in evidence)
    return "no successful validation evidence was provided" in joined


def _merge_recovered_evidence(
    block: ValidatedLessonBlock,
    *,
    evidence_hints: list[str],
) -> ValidatedLessonBlock:
    """Replace placeholder validation evidence with recovered project evidence."""
    if not evidence_hints or not _has_placeholder_evidence(block):
        return block
    lesson = dict(block.lesson)
    lesson["validation_evidence"] = list(evidence_hints)
    warning = block.warning
    extra = "validation_evidence was recovered from project files."
    warning = (warning + "\n" + extra).strip() if warning else extra
    return ValidatedLessonBlock(
        lesson=lesson,
        formatted_text=format_lesson_block(lesson),
        warning=warning,
    )


def _context_text(intake_text: str, editor_text: str) -> str:
    """Combine current GUI texts for evidence recovery."""
    return str(intake_text or "") + "\n" + str(editor_text or "")


def _try_model_with_feedback(
    *,
    model_name: str,
    intake_text: str,
    editor_text: str,
    project_root: Any,
    evidence_hints: list[str],
    source_defaults: dict[str, Any],
) -> tuple[ValidatedLessonBlock, str, str]:
    """Try one model, then retry once with deterministic validation feedback."""
    messages = build_error_memory_correction_messages(
        intake_text=intake_text,
        editor_text=editor_text,
        project_root=project_root,
        evidence_hints=evidence_hints,
    )
    response_text, used_model = _request_model(messages, model_name=model_name)
    try:
        block = parse_one_lesson_block(response_text, source_defaults=source_defaults)
        block = _merge_recovered_evidence(block, evidence_hints=evidence_hints)
        return block, used_model, ""
    except AIResponseValidationError as exc:
        first_error = str(exc)
        retry_messages = build_error_memory_retry_messages(
            intake_text=intake_text,
            editor_text=editor_text,
            project_root=project_root,
            validation_error=first_error,
            raw_ai_response=response_text,
            evidence_hints=evidence_hints,
        )
        retry_response, retry_model = chat_with_local_model(
            retry_messages,
            model_selection=used_model,
            temperature=0.02,
            max_tokens=4200,
        )
        block = parse_one_lesson_block(retry_response, source_defaults=source_defaults)
        block = _merge_recovered_evidence(block, evidence_hints=evidence_hints)
        return block, retry_model, "Retried after validation feedback: " + first_error


def correct_error_memory_lesson_with_local_ai(
    *,
    intake_text: str,
    editor_text: str = "",
    project_root: Any = "",
    model_selection: str = "",
) -> ErrorMemoryAICorrectionResult:
    """Ask the selected local model to return one corrected lesson block."""
    try:
        candidates = get_local_ai_model_candidates(model_selection)
    except LocalAIChatError as exc:
        return ErrorMemoryAICorrectionResult(False, None, str(exc))
    except Exception as exc:
        return ErrorMemoryAICorrectionResult(False, None, "Local AI model lookup failed: " + str(exc))
    if not candidates:
        return ErrorMemoryAICorrectionResult(
            False,
            None,
            "No global Local AI model is configured. Open Config AI > Config Local AI.",
        )

    evidence_hints = recover_validation_evidence(
        project_root=project_root,
        context_text=_context_text(intake_text, editor_text),
    )
    source_defaults = build_source_lesson_defaults(intake_text, editor_text)

    errors: list[str] = []
    last_response = ""
    for model_name in candidates:
        try:
            block, used_model, retry_note = _try_model_with_feedback(
                model_name=model_name,
                intake_text=intake_text,
                editor_text=editor_text,
                project_root=project_root,
                evidence_hints=evidence_hints,
                source_defaults=source_defaults,
            )
        except AIResponseValidationError as exc:
            errors.append(model_name + ": invalid Error Memory JSON: " + str(exc))
            continue
        except LocalAIChatError as exc:
            errors.append(model_name + ": " + str(exc))
            continue
        except Exception as exc:
            errors.append(model_name + ": local AI request failed: " + str(exc))
            continue
        message = "Corrected Error Memory lesson with local model: " + used_model
        if retry_note:
            message += "\n" + retry_note
        if block.warning:
            message += "\n" + block.warning
        return ErrorMemoryAICorrectionResult(
            True,
            block,
            message,
            model_name=used_model,
            raw_response=block.formatted_text,
        )

    return ErrorMemoryAICorrectionResult(
        False,
        None,
        "Local AI could not produce valid Error Memory JSON after normalization and one retry. "
        + " | ".join(errors),
        raw_response=last_response,
    )
