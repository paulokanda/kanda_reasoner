# project-path: kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py
"""Clipboard-only AI transport for one Freeze formulary draft."""

from __future__ import annotations

import json
from typing import Any, Mapping

from PySide6.QtWidgets import QApplication

__all__ = [
    "build_freeze_external_ai_prompt",
    "copy_freeze_formulary_to_clipboard",
]

_MANUAL_FORM_MULTILINE_FIELDS = (
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
)


def _transport_payload(inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Return a Markdown-safe freeze payload with multiline arrays."""
    payload: dict[str, Any] = {
        str(key): str(value or "") for key, value in inputs.items()
    }
    for field in _MANUAL_FORM_MULTILINE_FIELDS:
        payload[field] = [
            line.rstrip()
            for line in str(inputs.get(field, "") or "").splitlines()
            if line.strip()
        ]
    return payload


def build_freeze_external_ai_prompt(inputs: Mapping[str, Any]) -> str:
    """Build the strict draft-only Freeze formulary review prompt."""
    current_json = json.dumps(
        _transport_payload(inputs),
        ensure_ascii=False,
        indent=2,
    )
    return (
        "Review this KANDA Freeze formulary for the current validated feature only. "
        "Do not invent evidence. Preserve every validated file, protected path, "
        "rule, and validation line. The returned content is a draft only. Preview "
        "is read-only and Confirm and Write remains an explicit human action. "
        "Project memory stays under <project>_show_project_to_AI/"
        "project_freeze_after_update/frozen_features_memory.\n\n"
        "Return exactly this transport shape, with no prose before or after it:\n"
        "KANDA_FREEZE_FORM_JSON_BEGIN\n"
        "```json\n"
        "{ one valid JSON object }\n"
        "```\n"
        "KANDA_FREEZE_FORM_JSON_END\n\n"
        "Transport rules:\n"
        "- Keep validated_files, generated_files, protected_paths, "
        "do_not_regress_rules, and validation_evidence_summary as JSON arrays.\n"
        "- Keep the JSON inside the fenced code block; never place it in ordinary "
        "Markdown prose.\n"
        "- Encode Windows backslashes as doubled backslashes or \\u005C.\n"
        "- Use double quotes, no comments, and no trailing commas.\n"
        "- Do not claim validation, Freeze, or write authority.\n\n"
        "CURRENT FORM JSON:\n"
        + current_json
    )



def copy_freeze_formulary_to_clipboard(inputs: Mapping[str, Any]) -> str:
    """Copy the strict Freeze draft prompt without opening an external site."""
    application = QApplication.instance()
    if application is None:
        raise RuntimeError("A Qt application is required to access the clipboard.")
    prompt = build_freeze_external_ai_prompt(inputs)
    clipboard = application.clipboard()
    clipboard.setText(prompt)
    return prompt
