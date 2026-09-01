# project-path: kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py
"""Clipboard-only AI transport for one Freeze formulary draft."""

from __future__ import annotations

import json
from typing import Any, Mapping

from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import (
    canonical_formulary_payload,
)

from PySide6.QtWidgets import QApplication

__all__ = [
    "build_freeze_external_ai_prompt",
    "copy_freeze_formulary_to_clipboard",
]

def build_freeze_external_ai_prompt(inputs: Mapping[str, Any]) -> str:
    """Build the canonical draft-only Freeze formulary review prompt."""
    current_json = json.dumps(
        canonical_formulary_payload(inputs),
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
        "Return exactly one valid JSON object with the same 11 fields and no "
        "additional fields. Do not use marker wrappers, Markdown fences, comments, "
        "or prose.\n\n"
        "Transport rules:\n"
        "- Keep validated_files, generated_files, protected_paths, "
        "do_not_regress_rules, and validation_evidence_summary as JSON arrays.\n"
        "- Encode Windows backslashes as doubled backslashes or \\u005C.\n"
        "- Use double quotes and no trailing commas.\n"
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
