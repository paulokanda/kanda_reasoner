"""Prompt builder for AI-assisted Error Memory lesson intake."""

from __future__ import annotations

__all__: list[str] = []


import json
from pathlib import Path

from .intake_normalization import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    _REQUIRED_ACTIVE_AI_KEYS,
)


def build_error_lesson_ai_form_prompt(
    *,
    selected_project_root: str | Path,
    raw_error_text: str = "",
    operation_phase: str = "unknown",
) -> str:
    """Return the AI prompt for one active-ready Error Memory lesson.

    This prompt is the source of the text that AI produces for the
    AI-assisted error lesson intake window. It must therefore ask for the same
    fields that Memorize Error and the package validator require. The older
    minimal form omitted active-ready metadata and caused AI to return lessons
    that looked reasonable but could not be memorized safely.
    """
    current_form = {
        "schema_version": "1.0",
        "project_slug": Path(selected_project_root).name,
        "lesson_id": "lesson-<stable-slug>-v1",
        "status": "active",
        "operation_phase": operation_phase or "unknown",
        "created_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
        "updated_at_utc": "<YYYY-MM-DDTHH:MM:SSZ>",
        "source_patch_zip": "",
        "raw_error_text": raw_error_text,
        "raw_error_snapshot_scrubbed": "short scrubbed error/context snapshot",
        "symptom": "",
        "root_cause": "",
        "wrong_assumption": "",
        "correct_fix": "",
        "do_not_repeat_rule": "",
        "long_term_prevention": "",
        "exception": {
            "type": "",
            "phase": operation_phase or "unknown",
            "relative_file_path": "",
            "function_or_test_name": "",
            "message_normalized": "",
            "stacktrace_scrubbed": "",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": [],
            "fingerprint_hash": "",
        },
        "prevention_triggers": [],
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": [],
        },
        "regression_check": {
            "type": "validation_command",
            "command": "",
            "expected_marker": "",
            "required_before_freeze": False,
        },
        "validation_command_summary": "",
        "validation_evidence": [],
        "install_command_summary": "",
        "notes": "",
    }
    current_json = json.dumps(current_form, ensure_ascii=False, indent=2)
    required = ", ".join(_REQUIRED_ACTIVE_AI_KEYS)
    return (
        "You are a specialist in KANDA Reasoner, repeat-error prevention, validation engines, "
        "safe AI-assisted programming workflows, and project-specific Error Memory governance.\n\n"
        "Context:\n"
        "I have an error, validation failure, patch-install failure, freeze-intake failure, GUI crash, or AI implementation mistake that should become "
        "a KANDA Error Memory lesson. The lesson will be pasted or staged into the AI-assisted error lesson intake window and then memorized only after human review.\n\n"
        "Task:\n"
        "Create one active-ready Error Memory lesson JSON object from the actual evidence supplied. Focus on the concrete failure, proven root cause, corrected fix, and prevention rule. "
        "Do not invent missing details. If a required active-ready field cannot be supported by the evidence, set status to draft and state what is missing in notes.\n\n"
        "Critical rules:\n"
        "- Return only the receive-ready block for KANDA's AI-assisted error lesson intake window.\n"
        "- The first visible characters must be KANDA_ERROR_LESSON_JSON_BEGIN.\n"
        "- The last visible characters must be KANDA_ERROR_LESSON_JSON_END.\n"
        "- Between the markers, return one valid JSON object only. No markdown. No code fences. No comments. No trailing commas.\n"
        "- Use double quotes for every key and string value. Use forward slashes (/) for every command or path in the JSON object, including regression_check.command. Do not use Windows backslashes in Error Memory JSON because sequences such as \\t can corrupt the parsed command.\n"
        "- Do not use the older minimal lesson form. Active lessons must include the complete active-ready metadata.\n"
        "- Required active-ready keys: " + required + ".\n"
        "- Do not provide owner_scope, owner_id, owner_slug, owner_root_fingerprint, or affected_box as authority. The selected Tool or Project backend assigns canonical ownership and ignores AI-supplied ownership fields.\n"
        "- project_slug is informational in the form and is normalized by the selected canonical backend before saving.\n"
        "- Include raw_error_text and raw_error_snapshot_scrubbed as scrubbed/export-safe summaries of the actual error or reported failure.\n"
        "- Include redaction.applied=true, redaction.export_safe=true, and redaction.rules explaining why the payload is export-safe.\n"
        "- Include exception.type, exception.phase, exception.relative_file_path, exception.function_or_test_name, exception.message_normalized, and exception.stacktrace_scrubbed. If no traceback exists, say that no traceback was provided rather than inventing one.\n"
        "- Include fingerprint.strategy, fingerprint.components, and fingerprint.fingerprint_hash. Use a stable structural hash only when derivable; otherwise use status draft.\n"
        "- Use validation_evidence only for real evidence from this chat, terminal output, user report, validation output, or inspected artifacts.\n"
        "- Use status active only when all required active-ready fields are present and evidence-backed. Otherwise use status draft.\n"
        "- Keep language factual and blameless. Use wrong_assumption for the preventable assumption.\n"
        "- Before emitting the block, validate the exact outgoing text: marker wrapper present, json.loads succeeds, active-ready fields are present, redaction.rules is non-empty, and regression_check.command contains no backslashes or control characters. If this check fails, do not output status active.\n\n"
        "Copy/paste-ready answer shape:\n"
        f"{ERROR_LESSON_JSON_BEGIN}\n"
        "{\n"
        "  \"schema_version\": \"1.0\",\n"
        "  \"project_slug\": \"kanda_reasoner\",\n"
        "  \"lesson_id\": \"lesson-<stable-slug>-v1\",\n"
        "  \"status\": \"active\",\n"
        "  \"operation_phase\": \"validation\",\n"
        "  \"created_at_utc\": \"<YYYY-MM-DDTHH:MM:SSZ>\",\n"
        "  \"updated_at_utc\": \"<YYYY-MM-DDTHH:MM:SSZ>\",\n"
        "  \"source_patch_zip\": \"<patch zip or empty>\",\n"
        "  \"raw_error_text\": \"short scrubbed error/context snapshot\",\n"
        "  \"raw_error_snapshot_scrubbed\": \"scrubbed raw error/context snapshot\",\n"
        "  \"symptom\": \"what failed\",\n"
        "  \"root_cause\": \"why it failed, only if proven\",\n"
        "  \"wrong_assumption\": \"the assumption or missing safeguard that caused the mistake\",\n"
        "  \"correct_fix\": \"how it was corrected or should be corrected\",\n"
        "  \"do_not_repeat_rule\": \"single clear prevention rule\",\n"
        "  \"long_term_prevention\": \"future workflow/test/architecture rule that prevents recurrence\",\n"
        "  \"exception\": {\n"
        "    \"type\": \"<error type or domain error>\",\n"
        "    \"phase\": \"<phase>\",\n"
        "    \"relative_file_path\": \"<relative path or empty>\",\n"
        "    \"function_or_test_name\": \"<function/test/workflow or empty>\",\n"
        "    \"message_normalized\": \"<normalized error message>\",\n"
        "    \"stacktrace_scrubbed\": \"<scrubbed trace or explicit no-traceback note>\"\n"
        "  },\n"
        "  \"fingerprint\": {\n"
        "    \"strategy\": \"v1_structural_conservative\",\n"
        "    \"components\": [\"<type>\", \"<relative path>\", \"<workflow/function>\", \"<phase>\", \"<normalized trigger>\"],\n"
        "    \"fingerprint_hash\": \"<stable sha256>\"\n"
        "  },\n"
        "  \"prevention_triggers\": [\"trigger phrase 1\", \"trigger phrase 2\"],\n"
        "  \"redaction\": {\n"
        "    \"applied\": true,\n"
        "    \"export_safe\": true,\n"
        "    \"rules\": [\"No secrets or credentials present.\", \"No patient data present.\", \"Project identifiers are intentional technical context.\"]\n"
        "  },\n"
        "  \"regression_check\": {\n"
        "    \"type\": \"validation_command\",\n"
        "    \"command\": \"python validation/<test_name>.py\",\n"
        "    \"expected_marker\": \"VALIDATION OK: <feature-id>\",\n"
        "    \"required_before_freeze\": true\n"
        "  },\n"
        "  \"validation_command_summary\": \"what validation proves\",\n"
        "  \"validation_evidence\": [\"real evidence item 1\"],\n"
        "  \"install_command_summary\": \"what the installer stages or changes\",\n"
        "  \"notes\": \"short blameless notes\"\n"
        "}\n"
        f"{ERROR_LESSON_JSON_END}\n\n"
        f"Active project root: {selected_project_root}\n\n"
        "Current error/draft JSON for completion or correction:\n"
        f"{current_json}\n"
    )
