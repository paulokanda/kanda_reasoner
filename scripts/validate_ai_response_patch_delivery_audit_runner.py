# project-path: scripts/validate_ai_response_patch_delivery_audit_runner.py
"""Patch delivery response validation runner."""

from __future__ import annotations

import json

__all__ = []  # Implementation-only module; public facade owns exported validator symbols.

try:
    from scripts.validate_ai_response_patch_delivery_contract import (
        DAILY_WORK_TOKEN,
        ERROR_LESSON_BEGIN,
        ERROR_LESSON_END,
        ERROR_MEMORY_INTAKE_TOKEN,
        ERROR_MEMORY_REQUIRED_ACTIVE_FIELDS,
        FORBIDDEN_INLINE_PYTHON_TERMS,
        FORBIDDEN_INSTALL_BLOCK_TERMS,
        FORBIDDEN_TERMINAL_CLOSING_TERMS,
        FREEZE_FORM_REQUIRED_FIELDS,
        FREEZE_HINT_INTAKE_TOKEN,
        INSTALL_SUCCESS_TERMINAL_TERMS,
        NON_INSTALL_TERMINAL_TERMS,
        OLD_TERMINAL_FOOTER_TERMS,
        PROJECT_ROOT_TERMS,
        RECEIVER_CLASSIFICATION_VALUES,
        RECEIVER_GATE_FIELDS,
        REQUIRED_GATE_FIELDS,
        TRANSIENT_TERMS,
        _code_blocks,
        _fail,
        _has_zip_reference,
    )
    from scripts.validate_ai_response_patch_delivery_text_helpers import (
        _extract_marker_json,
        _field_value,
        _gate_section_value,
        _has_any_term,
        _has_install_block,
        _has_validation_block,
        _install_proves_token,
        _is_install_block,
        _is_non_install_terminal_block,
        _receiver_flag,
        _receiver_gate_value,
        _require_non_empty,
        _needs_receiver_gate,
        _validate_helper_project_import_path_contract,
    )
    from scripts.validate_ai_response_patch_delivery_staging_gate import (
        validate_root_drive_staging_install_block,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    from validate_ai_response_patch_delivery_contract import (
        DAILY_WORK_TOKEN,
        ERROR_LESSON_BEGIN,
        ERROR_LESSON_END,
        ERROR_MEMORY_INTAKE_TOKEN,
        ERROR_MEMORY_REQUIRED_ACTIVE_FIELDS,
        FORBIDDEN_INLINE_PYTHON_TERMS,
        FORBIDDEN_INSTALL_BLOCK_TERMS,
        FORBIDDEN_TERMINAL_CLOSING_TERMS,
        FREEZE_FORM_REQUIRED_FIELDS,
        FREEZE_HINT_INTAKE_TOKEN,
        INSTALL_SUCCESS_TERMINAL_TERMS,
        NON_INSTALL_TERMINAL_TERMS,
        OLD_TERMINAL_FOOTER_TERMS,
        PROJECT_ROOT_TERMS,
        RECEIVER_CLASSIFICATION_VALUES,
        RECEIVER_GATE_FIELDS,
        REQUIRED_GATE_FIELDS,
        TRANSIENT_TERMS,
        _code_blocks,
        _fail,
        _has_zip_reference,
    )
    from validate_ai_response_patch_delivery_text_helpers import (
        _extract_marker_json,
        _field_value,
        _gate_section_value,
        _has_any_term,
        _has_install_block,
        _has_validation_block,
        _install_proves_token,
        _is_install_block,
        _is_non_install_terminal_block,
        _receiver_flag,
        _receiver_gate_value,
        _require_non_empty,
        _needs_receiver_gate,
        _validate_helper_project_import_path_contract,
    )
    from validate_ai_response_patch_delivery_staging_gate import (
        validate_root_drive_staging_install_block,
    )


def _validate_daily_work_gate_values(text: str) -> None:
    """Support validate daily work gate values behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    """
    
    placement = _gate_section_value(text, "ZIP placement path:")
    allowed = _gate_section_value(text, "Allowed write paths:")
    forbidden = _gate_section_value(text, "Forbidden write paths:")
    daily_text = placement + "\n" + allowed
    if DAILY_WORK_TOKEN not in daily_text:
        _fail(
            "Patch Delivery Gate must name the dynamic "
            + DAILY_WORK_TOKEN
            + " folder in ZIP placement or allowed write paths."
        )
    if not _has_any_term(forbidden, PROJECT_ROOT_TERMS):
        _fail(
            "Forbidden write paths must explicitly protect the active project root "
            "from transient delivery artifacts."
        )
    if not _has_any_term(forbidden, TRANSIENT_TERMS):
        _fail(
            "Forbidden write paths must explicitly forbid transient install, temp, "
            "correction, patch, validation-helper, or staging files in project root."
        )


def _validate_no_forbidden_terminal_fragments(block: str) -> None:
    """Support validate no forbidden terminal fragments behavior.
    
    Parameters
    ----------
    block : str
        The block value.
    """
    
    lowered = block.lower()
    old_fragments = [term for term in OLD_TERMINAL_FOOTER_TERMS if term in lowered]
    if old_fragments:
        _fail("Terminal block uses old terminal cleanup footer fragments: " + ", ".join(old_fragments))
    closing = [term for term in FORBIDDEN_TERMINAL_CLOSING_TERMS if term in lowered]
    if closing:
        _fail("Terminal block must keep the terminal open and must not use: " + ", ".join(closing))
    inline_python = [term for term in FORBIDDEN_INLINE_PYTHON_TERMS if term in lowered]
    if inline_python:
        _fail(
            "Terminal block must not use inline Python execution because Windows "
            "PowerShell can strip embedded quotes: " + ", ".join(inline_python)
        )


def _validate_install_terminal_footer(block: str) -> None:
    """Support validate install terminal footer behavior.
    
    Parameters
    ----------
    block : str
        The block value.
    """
    
    lowered = block.lower()
    success_index = lowered.find("install ok")
    if success_index < 0:
        _fail("Install block is missing an INSTALL OK success marker.")
    success_region = lowered[success_index:].split("catch", 1)[0]
    missing = [term for term in INSTALL_SUCCESS_TERMINAL_TERMS if term not in success_region]
    if missing:
        _fail("Install success path is missing Enter Enter final-clear fragments: " + ", ".join(missing))
    error_required = (
        "install error",
        'read-host "press enter to clear terminal"',
        'read-host "press enter again to clear"',
        "clear-host",
    )
    missing_error = [term for term in error_required if term not in lowered]
    if missing_error:
        _fail("Install error path is missing Enter Enter final-clear fragments: " + ", ".join(missing_error))


def _validate_non_install_terminal_footer(block: str) -> None:
    """Support validate non install terminal footer behavior.
    
    Parameters
    ----------
    block : str
        The block value.
    """
    
    lowered = block.lower()
    missing = [term for term in NON_INSTALL_TERMINAL_TERMS if term not in lowered]
    if missing:
        _fail("Non-install terminal block is missing Enter Enter final-clear footer fragments: " + ", ".join(missing))


def _validate_terminal_footer_contract(blocks: list[str]) -> None:
    """Support validate terminal footer contract behavior.
    
    Parameters
    ----------
    blocks : list[str]
        The blocks value.
    """
    
    for block in blocks:
        _validate_no_forbidden_terminal_fragments(block)
        _validate_helper_project_import_path_contract(block)
        if _is_install_block(block):
            _validate_install_terminal_footer(block)
        elif _is_non_install_terminal_block(block):
            _validate_non_install_terminal_footer(block)


def _validate_install_blocks(blocks: list[str]) -> None:
    """Support validate install blocks behavior.
    
    Parameters
    ----------
    blocks : list[str]
        The blocks value.
    """
    
    install_like_blocks = [block for block in blocks if "expand-archive" in block.lower()]
    for block in install_like_blocks:
        lowered = block.lower()
        forbidden = [term for term in FORBIDDEN_INSTALL_BLOCK_TERMS if term in lowered]
        if forbidden:
            _fail(
                "Install block contains forbidden generic path fallback terms: "
                + ", ".join(forbidden)
            )
        required = (
            "$project_root",
            "$patch_name",
            "$drive_root",
            "$root_patch_zip",
            DAILY_WORK_TOKEN,
            "expand-archive",
        )
        missing = [fragment for fragment in required if fragment not in lowered]
        if missing:
            _fail(
                "Install block is missing required dynamic daily-work staging fragments: "
                + ", ".join(missing)
            )
        validate_root_drive_staging_install_block(block)
        safety_tokens = (
            "system.io.compression.zipfile",
            ".entries",
            "fullname",
            "..",
        )
        if not all(token in lowered for token in safety_tokens):
            _fail(
                "Install block must validate ZIP member names before Expand-Archive "
                "using System.IO.Compression.ZipFile, Entries, FullName, and traversal checks."
            )


def _validate_error_memory_object(obj: object) -> None:
    """Support validate error memory object behavior.
    
    Parameters
    ----------
    obj : object
        The obj value.
    """
    
    if obj is None:
        return
    if not isinstance(obj, dict):
        _fail("Error Memory lesson JSON must be an object.")
    missing = [field for field in ERROR_MEMORY_REQUIRED_ACTIVE_FIELDS if field not in obj]
    if missing:
        _fail("Error Memory active-ready lesson missing required fields: " + ", ".join(missing))
    if obj.get("status") == "active":
        optional_empty_fields = {"superseded_by"}
        for field in ERROR_MEMORY_REQUIRED_ACTIVE_FIELDS:
            if field not in optional_empty_fields:
                _require_non_empty(obj.get(field), field)
    redaction = obj.get("redaction")
    if not isinstance(redaction, dict):
        _fail("Error Memory redaction must be an object.")
    if redaction.get("applied") is not True:
        _fail("Error Memory redaction.applied must be true.")
    if redaction.get("export_safe") is not True:
        _fail("Error Memory redaction.export_safe must be true.")
    rules = redaction.get("rules")
    if not isinstance(rules, list) or not rules or not all(isinstance(rule, str) and rule.strip() for rule in rules):
        _fail("Error Memory redaction.rules must be a non-empty list of strings.")
    regression_check = obj.get("regression_check")
    if not isinstance(regression_check, dict):
        _fail("Error Memory regression_check must be an object.")
    if regression_check.get("type") != "validation_command":
        _fail("Error Memory regression_check.type must be validation_command.")
    command = regression_check.get("command")
    if not isinstance(command, str) or not command.strip():
        _fail("Error Memory regression_check.command must be a non-empty string.")


def _validate_freeze_form_object(obj: object) -> None:
    """Support validate freeze form object behavior.
    
    Parameters
    ----------
    obj : object
        The obj value.
    """
    
    if obj is None:
        return
    if not isinstance(obj, dict):
        _fail("Freeze form JSON must be an object.")
    missing = [field for field in FREEZE_FORM_REQUIRED_FIELDS if field not in obj]
    if missing:
        _fail("Freeze form JSON missing required fields: " + ", ".join(missing))
    for field in FREEZE_FORM_REQUIRED_FIELDS:
        _require_non_empty(obj.get(field), field)
    evidence = str(obj.get("validation_evidence_summary", ""))
    if "VALIDATION OK:" not in evidence:
        _fail("Freeze form validation_evidence_summary must include VALIDATION OK: <feature_id>.")
    if "STATUS: IN_SYNC" not in evidence:
        _fail("Freeze form validation_evidence_summary must include STATUS: IN_SYNC when local validation completed.")


def _validate_marker_wrapped_error_memory(text: str) -> None:
    """Support validate marker wrapped error memory behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    """
    
    obj = _extract_marker_json(text, ERROR_LESSON_BEGIN, ERROR_LESSON_END, "Error Memory lesson")
    _validate_error_memory_object(obj)


def _freeze_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build a Freeze JSON object while rejecting duplicate keys."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            _fail("Freeze form JSON contains duplicate key: " + key)
        result[key] = value
    return result


def _reject_freeze_constant(value: str) -> None:
    _fail("Freeze form JSON contains non-standard constant: " + value)


def _validate_manual_freeze_form_json(text: str) -> None:
    """Validate exactly one canonical Freeze object when one is present."""
    decoder = json.JSONDecoder(
        object_pairs_hook=_freeze_object_pairs,
        parse_constant=_reject_freeze_constant,
    )
    expected = set(FREEZE_FORM_REQUIRED_FIELDS)
    candidates: list[dict[str, object]] = []
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text, index)
        except (json.JSONDecodeError, ResponseValidationError):
            continue
        if isinstance(obj, dict) and set(obj) == expected:
            candidates.append(obj)
    if len(candidates) > 1:
        _fail("Freeze response contains more than one valid 11-field JSON object.")
    if candidates:
        _validate_freeze_form_object(candidates[0])


def _validate_receiver_delivery_gate(text: str, blocks: list[str]) -> None:
    """Support validate receiver delivery gate behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    blocks : list[str]
        The blocks value.
    """
    
    _validate_marker_wrapped_error_memory(text)
    _validate_manual_freeze_form_json(text)
    if not _needs_receiver_gate(text):
        return

    missing = [field for field in RECEIVER_GATE_FIELDS if field not in text]
    if missing:
        _fail("Missing required Receiver Delivery Check fields: " + ", ".join(missing))

    classification = _receiver_gate_value(text, "Receiver classification:").splitlines()[0].strip()
    if classification not in RECEIVER_CLASSIFICATION_VALUES:
        _fail("Receiver classification must be one of: " + ", ".join(RECEIVER_CLASSIFICATION_VALUES))

    receiver_text = "\n".join(
        _receiver_gate_value(text, field)
        for field in (
            "Actual receiver path or action:",
            "Installer stages to receiver:",
            "Manual paste required:",
            "Storage-only helper:",
            "Receiver proof:",
        )
    )
    lowered = text.lower()
    receiver_lower = receiver_text.lower()

    installer_stages = _receiver_flag(text, "Installer stages to receiver:")
    manual_required = _receiver_flag(text, "Manual paste required:")
    storage_only = _receiver_flag(text, "Storage-only helper:")

    if classification == "ERROR_MEMORY_AI_ASSISTED_INTAKE":
        if "yes" not in installer_stages or "no" not in manual_required or "no" not in storage_only:
            _fail("ERROR_MEMORY_AI_ASSISTED_INTAKE must set installer YES, manual paste NO, storage-only NO.")
        if ERROR_MEMORY_INTAKE_TOKEN not in receiver_lower and ERROR_MEMORY_INTAKE_TOKEN not in lowered:
            _fail("ERROR_MEMORY_AI_ASSISTED_INTAKE delivery must name " + ERROR_MEMORY_INTAKE_TOKEN + ".")
        if not _install_proves_token(blocks, ERROR_MEMORY_INTAKE_TOKEN, require_copy=True):
            _fail("ERROR_MEMORY_AI_ASSISTED_INTAKE must be proven in install code with Copy-Item into " + ERROR_MEMORY_INTAKE_TOKEN + ".")

    if classification == "FREEZE_HINT_INTAKE":
        if "yes" not in installer_stages or "no" not in storage_only:
            _fail("FREEZE_HINT_INTAKE must set installer YES and storage-only NO.")
        if FREEZE_HINT_INTAKE_TOKEN not in receiver_lower and FREEZE_HINT_INTAKE_TOKEN not in lowered:
            _fail("FREEZE_HINT_INTAKE delivery must stage or update freeze_hint_intake.")
        has_copy = _install_proves_token(blocks, FREEZE_HINT_INTAKE_TOKEN, require_copy=True) and "kanda_freeze_hint.json" in lowered
        has_merge = "merge_freeze_validation_evidence.py" in lowered or "merge_validation_evidence" in lowered
        if not (has_copy or has_merge):
            _fail("FREEZE_HINT_INTAKE must be proven by Copy-Item of KANDA_FREEZE_HINT.json into freeze_hint_intake or by merge validation evidence command.")

    if classification == "MANUAL_FREEZE_FORM_RECEIVER":
        if "yes" not in manual_required or "no" not in installer_stages:
            _fail("MANUAL_FREEZE_FORM_RECEIVER must set manual paste YES and installer stages NO.")
        if "manual" not in receiver_lower and "paste" not in receiver_lower:
            _fail("MANUAL_FREEZE_FORM_RECEIVER must explicitly say manual paste/action is required.")

    if classification == "STORAGE_ONLY_MANUAL_HELPER":
        if "yes" not in storage_only or "yes" not in manual_required or "no" not in installer_stages:
            _fail("STORAGE_ONLY_MANUAL_HELPER must set storage-only YES, manual paste YES, installer stages NO.")
        if "manual" not in receiver_lower and "paste" not in receiver_lower:
            _fail("STORAGE_ONLY_MANUAL_HELPER must explain the manual receiver action.")

    if "governance intake" in lowered or "manual receiver bundle" in lowered:
        if classification not in {"STORAGE_ONLY_MANUAL_HELPER", "ERROR_MEMORY_AI_ASSISTED_INTAKE", "FREEZE_HINT_INTAKE", "MANUAL_FREEZE_FORM_RECEIVER"}:
            _fail("Governance/manual receiver bundles must declare the actual receiver classification.")


def validate_response_text(text: str, *, user_detected_correction: bool = False) -> list[str]:
    """Validate response text and return message strings when it passes."""
    if not _has_zip_reference(text):
        return ["No ZIP reference found; isolated ZIP gate not required."]

    missing = [field for field in REQUIRED_GATE_FIELDS if field not in text]
    if missing:
        _fail("Missing required Patch Delivery Gate fields: " + ", ".join(missing))

    zip_index = text.lower().find(".zip")
    gate_index = text.find("PATCH DELIVERY GATE")
    if gate_index == -1 or (zip_index != -1 and gate_index > zip_index):
        _fail("PATCH DELIVERY GATE must appear before the first ZIP reference.")

    _validate_daily_work_gate_values(text)

    blocks = _code_blocks(text)
    if not _has_install_block(blocks):
        _fail("Missing install PowerShell block with root-to-staging ZIP extraction.")
    _validate_install_blocks(blocks)
    if not _has_validation_block(blocks):
        _fail("Missing validation block that runs Python validation.")
    _validate_terminal_footer_contract(blocks)

    _validate_receiver_delivery_gate(text, blocks)

    if "VALIDATION OK:" not in text:
        _fail("Missing expected validation marker: VALIDATION OK: <feature_id>.")

    if user_detected_correction:
        value = _field_value(text, "Error Memory payload:")
        lowered = value.lower()
        if not value or lowered in {"n/a", "na", "none"} or "not applicable" in lowered:
            _fail("User-detected correction requires a non-empty Error Memory payload field.")

    return ["PATCH DELIVERY RESPONSE CONTRACT: PASS"]
