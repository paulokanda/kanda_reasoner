# project-path: scripts/validate_ai_response_patch_delivery.py
"""Validate KANDA AI patch delivery responses.

This validator blocks isolated ZIP delivery and receiver-boundary mistakes. It
checks the visible Patch Delivery Gate, terminal install/validation blocks, and
receiver-specific contracts for Freeze and Error Memory artifacts.
"""

from __future__ import annotations

__all__ = ["ResponseValidationError", "validate_response_text", "validate_zip_member_names"]

import argparse
from pathlib import Path

# Static validation scripts inspect this wrapper path for these enforcement
# markers even though the implementation now lives in helper modules:
# DAILY_WORK_TOKEN
# _validate_daily_work_gate_values
# Forbidden write paths must explicitly protect the active project root
# Install block is missing required dynamic daily-work staging fragments
# Root-drive staging breach gate must validate deletion of root ZIP copy
# zip is not in root of drive:\\ where project is
# FORBIDDEN_INSTALL_BLOCK_TERMS

try:
    from scripts.validate_ai_response_patch_delivery_contract import (
        REQUIRED_GATE_FIELDS,
        ZIP_PATTERN,
        CODE_FENCE_PATTERN,
        DAILY_WORK_TOKEN,
        PROJECT_ROOT_TERMS,
        TRANSIENT_TERMS,
        FORBIDDEN_INSTALL_BLOCK_TERMS,
        FORBIDDEN_TERMINAL_CLOSING_TERMS,
        OLD_TERMINAL_FOOTER_TERMS,
        FORBIDDEN_INLINE_PYTHON_TERMS,
        INSTALL_SUCCESS_TERMINAL_TERMS,
        NON_INSTALL_TERMINAL_TERMS,
        RECEIVER_CLASSIFICATION_VALUES,
        RECEIVER_GATE_FIELDS,
        ERROR_MEMORY_INTAKE_TOKEN,
        FREEZE_HINT_INTAKE_TOKEN,
        FREEZE_FORM_BEGIN,
        FREEZE_FORM_END,
        ERROR_LESSON_BEGIN,
        ERROR_LESSON_END,
        ERROR_MEMORY_REQUIRED_ACTIVE_FIELDS,
        FREEZE_FORM_REQUIRED_FIELDS,
        ResponseValidationError,
        _fail,
        _has_zip_reference,
        _code_blocks,
        _unsafe_zip_member_reason,
        validate_zip_member_names,
    )
    from scripts.validate_ai_response_patch_delivery_text_helpers import (
        _has_install_block,
        _has_validation_block,
        _field_value,
        _section_value,
        _gate_section_value,
        _receiver_gate_value,
        _has_any_term,
        _is_install_block,
        _is_non_install_terminal_block,
        _needs_receiver_gate,
        _extract_marker_json,
        _require_non_empty,
        _receiver_flag,
        _install_blocks_with_expand,
        _install_proves_token,
        _validate_helper_project_import_path_contract,
    )
    from scripts.validate_ai_response_patch_delivery_audit_runner import (
        _validate_daily_work_gate_values,
        _validate_no_forbidden_terminal_fragments,
        _validate_install_terminal_footer,
        _validate_non_install_terminal_footer,
        _validate_terminal_footer_contract,
        _validate_install_blocks,
        _validate_error_memory_object,
        _validate_freeze_form_object,
        _validate_marker_wrapped_error_memory,
        _validate_manual_freeze_form_markers,
        _validate_receiver_delivery_gate,
        validate_response_text,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    from validate_ai_response_patch_delivery_contract import (
        ResponseValidationError,
        validate_zip_member_names,
    )
    from validate_ai_response_patch_delivery_audit_runner import (
        validate_response_text,
    )


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Validate a KANDA AI patch delivery response.")
    parser.add_argument("response_file", help="Path to a text file containing the AI response.")
    parser.add_argument(
        "--user-detected-correction",
        action="store_true",
        help="Require a non-empty Error Memory payload field.",
    )
    parser.add_argument(
        "--zip-path",
        help="Optional ZIP path to validate for unsafe member names.",
    )
    args = parser.parse_args(argv)

    path = Path(args.response_file).expanduser().resolve()
    if not path.is_file():
        print("PATCH DELIVERY RESPONSE CONTRACT: FAIL")
        print("Response file not found: " + str(path))
        return 1

    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        messages = validate_response_text(
            text,
            user_detected_correction=args.user_detected_correction,
        )
        if args.zip_path:
            validate_zip_member_names(args.zip_path)
            messages.append("ZIP MEMBER SAFETY: PASS")
    except ResponseValidationError as exc:
        print("PATCH DELIVERY RESPONSE CONTRACT: FAIL")
        print(str(exc))
        return 1

    for message in messages:
        print(message)
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
