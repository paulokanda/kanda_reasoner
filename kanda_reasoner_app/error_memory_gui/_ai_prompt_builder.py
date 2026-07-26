# project-path: kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py
"""Prompt builder for local AI Error Memory correction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = [
    "build_error_memory_correction_messages",
    "build_error_memory_retry_messages",
]

_REQUIRED_FIELDS = (
    "schema_version, project_slug, lesson_id, status, superseded_by, operation_phase, "
    "created_at_utc, updated_at_utc, source_patch_zip, raw_error_text, "
    "raw_error_snapshot_scrubbed, symptom, root_cause, wrong_assumption, "
    "correct_fix, do_not_repeat_rule, long_term_prevention, redaction, exception, "
    "fingerprint, prevention_triggers, regression_check, validation_command_summary, "
    "validation_evidence, install_command_summary, notes"
)

_SKELETON = """{
  "schema_version": "1.0",
  "project_slug": "<project_slug>",
  "lesson_id": "lesson-<stable-slug>-v1",
  "status": "draft",
  "superseded_by": "",
  "operation_phase": "<phase>",
  "created_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "updated_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
  "source_patch_zip": "<artifact-or-patch-name>",
  "raw_error_text": "<observed error>",
  "raw_error_snapshot_scrubbed": "<scrubbed chronology>",
  "symptom": "<observed symptom>",
  "root_cause": "<root cause>",
  "wrong_assumption": "<wrong assumption>",
  "correct_fix": "<correct fix>",
  "do_not_repeat_rule": "<enforceable rule>",
  "long_term_prevention": "<future prevention>",
  "redaction": {
    "applied": true,
    "export_safe": true,
    "rules": ["No secrets included."]
  },
  "exception": {
    "type": "<type>",
    "phase": "<phase>",
    "relative_file_path": "<path-or-surface>",
    "function_or_test_name": "<function-or-command>",
    "message_normalized": "<normalized message>",
    "stacktrace_scrubbed": "<scrubbed traceback or no traceback summary>"
  },
  "fingerprint": {
    "strategy": "v1_structural_conservative",
    "components": ["<component>"],
    "fingerprint_hash": "<stable_slug>"
  },
  "prevention_triggers": ["<trigger>"],
  "regression_check": {
    "type": "validation_command",
    "command": "<command with forward slashes>",
    "expected_marker": "<expected marker>",
    "required_before_freeze": true
  },
  "validation_command_summary": "<summary>",
  "validation_evidence": ["No successful validation evidence was provided in the input; keep status draft."],
  "install_command_summary": "<install summary>",
  "notes": "<notes>"
}"""


def _project_slug(project_root: Any) -> str:
    """Return the project slug used in Error Memory lessons."""
    try:
        name = Path(project_root).name.strip()
    except Exception:
        name = ""
    return name or "kanda_reasoner"


def _format_evidence_hints(evidence_hints: list[str] | None) -> str:
    """Return prompt text for recovered project evidence hints."""
    items = [str(item).strip() for item in (evidence_hints or []) if str(item).strip()]
    if not items:
        return "No observed validation evidence was recovered from project files."
    return "\n".join("- " + item for item in items)


def _base_user_prompt(*, intake_text: str, editor_text: str, project_root: Any, evidence_hints: list[str] | None = None) -> str:
    """Build the shared user prompt body for correction and retry."""
    raw_intake = str(intake_text or "").strip()
    current_editor = str(editor_text or "").strip()
    slug = _project_slug(project_root)
    return (
        "TASK:\n"
        "Create or correct exactly one KANDA Error Memory lesson.\n\n"
        "OUTPUT CONTRACT:\n"
        "Return exactly one block and nothing outside it:\n"
        "KANDA_ERROR_LESSON_JSON_BEGIN\n"
        "{ one JSON object }\n"
        "KANDA_ERROR_LESSON_JSON_END\n\n"
        "HARD RULES:\n"
        "- Use JSON only between the markers.\n"
        "- Do not use markdown fences.\n"
        "- Do not add prose before or after the markers.\n"
        "- Include superseded_by every time; use an empty string when not superseded.\n"
        "- Include exception every time as an object with type, phase, relative_file_path, function_or_test_name, message_normalized, and stacktrace_scrubbed.\n"
        "- Set status to draft unless successful validation evidence is explicit in the input.\n"
        "- Do not invent validation evidence, commands, patch names, or file paths.\n"
        "- Follow the active-ready/model template contract: replace placeholders with concrete values.\n"
        "- source_patch_zip is mandatory and non-empty; use the patch ZIP name or a truthful relevant artifact from the input, such as a validation script, command surface, or generated artifact name.\n"
        "- wrong_assumption, install_command_summary, and notes are mandatory and non-empty.\n"
        "- Preserve project-specific fields when present.\n"
        "- Use forward slashes inside regression_check.command. Write Windows paths like E:/kanda_reasoner. "
        "Any backslash or control character is invalid and will trigger a retry.\n"
        "- validation_evidence must be a non-empty JSON list, never [] and never a string.\n"
        "- If PROJECT EVIDENCE HINTS below contain recovered observed markers, you may use those lines as validation_evidence.\n"
        "- If PROJECT EVIDENCE HINTS says no evidence was recovered, use exactly this list: "
        "[\"No successful validation evidence was provided in the input; keep status draft.\"]\n"
        "- prevention_triggers, fingerprint.components, and redaction.rules must be JSON lists.\n"
        "- Include redaction.applied true, redaction.export_safe true, and redaction.rules.\n"
        "- install_command_summary and notes must be non-empty.\n"
        "- If evidence is missing, say so inside validation_evidence and keep status draft.\n\n"
        "REQUIRED FIELDS:\n"
        f"{_REQUIRED_FIELDS}\n\n"
        "MANDATORY JSON SKELETON SHAPE:\n"
        f"{_SKELETON}\n\n"
        "PROJECT SLUG:\n"
        f"{slug}\n\n"
        "PROJECT EVIDENCE HINTS RECOVERED BY THE APP:\n"
        f"{_format_evidence_hints(evidence_hints)}\n\n"
        "AI-ASSISTED ERROR LESSON INTAKE TEXT:\n"
        f"{raw_intake}\n\n"
        "CURRENT ERROR EDITOR TEXT, IF ANY:\n"
        f"{current_editor}\n"
    )


def build_error_memory_correction_messages(
    *,
    intake_text: str,
    editor_text: str = "",
    project_root: Any = "",
    evidence_hints: list[str] | None = None,
) -> list[dict[str, str]]:
    """Build strict local-AI messages for one Error Memory lesson correction."""
    return [
        {
            "role": "system",
            "content": (
                "You correct one KANDA Error Memory lesson for a Python desktop app. "
                "Return only the requested marker-wrapped JSON block. Do not explain. "
                "Do not invent validation evidence. Include every required key, including "
                "superseded_by and exception."
            ),
        },
        {
            "role": "user",
            "content": _base_user_prompt(
                intake_text=intake_text,
                editor_text=editor_text,
                project_root=project_root,
                evidence_hints=evidence_hints,
            ),
        },
    ]


def build_error_memory_retry_messages(
    *,
    intake_text: str,
    editor_text: str = "",
    project_root: Any = "",
    validation_error: str,
    raw_ai_response: str,
    evidence_hints: list[str] | None = None,
) -> list[dict[str, str]]:
    """Build a retry prompt that teaches the local model from validation feedback."""
    base = build_error_memory_correction_messages(
        intake_text=intake_text,
        editor_text=editor_text,
        project_root=project_root,
        evidence_hints=evidence_hints,
    )
    base.append({"role": "assistant", "content": str(raw_ai_response or "")})
    base.append(
        {
            "role": "user",
            "content": (
                "Your previous answer failed deterministic validation.\n"
                "Validation error:\n"
                f"{validation_error}\n\n"
                "Return the corrected lesson again. The next answer must contain exactly "
                "one marker-wrapped JSON block and nothing else. Do not omit superseded_by or exception. "
                "Use an empty string for superseded_by when there is no replacement lesson. Keep exception as an object. "
                "Use forward slashes in regression_check.command and write Windows paths like E:/kanda_reasoner. "
                "Any backslash or control character is invalid. validation_evidence must be "
                "a non-empty JSON list. source_patch_zip, wrong_assumption, "
                "install_command_summary, and notes must be non-empty. "
                "Use recovered project evidence hints only when present. "
                "If no successful validation evidence was provided or recovered, use exactly "
                "[\"No successful validation evidence was provided in the input; keep status draft.\"]."
            ),
        }
    )
    return base
