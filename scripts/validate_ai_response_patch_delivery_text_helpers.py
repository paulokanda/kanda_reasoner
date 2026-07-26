# project-path: scripts/validate_ai_response_patch_delivery_text_helpers.py
"""Text, gate, and code-block helper functions for patch delivery validation."""

from __future__ import annotations

__all__ = []  # Implementation-only module; public facade owns exported validator symbols.

import json
import re

try:
    from scripts.validate_ai_response_patch_delivery_contract import (
        CODE_FENCE_PATTERN,
        DAILY_WORK_TOKEN,
        RECEIVER_GATE_FIELDS,
        REQUIRED_GATE_FIELDS,
        ZIP_PATTERN,
        _fail,
        _has_zip_reference,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    from validate_ai_response_patch_delivery_contract import (
        CODE_FENCE_PATTERN,
        DAILY_WORK_TOKEN,
        RECEIVER_GATE_FIELDS,
        REQUIRED_GATE_FIELDS,
        ZIP_PATTERN,
        _fail,
        _has_zip_reference,
    )


def _has_install_block(blocks: list[str]) -> bool:
    """Support has install block behavior.
    
    Parameters
    ----------
    blocks : list[str]
        The blocks value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for block in blocks:
        lowered = block.lower()
        if DAILY_WORK_TOKEN in lowered and "expand-archive" in lowered:
            if "[system.io.path]::getpathroot" in lowered or "getpathroot" in lowered:
                return True
    return False


def _has_validation_block(blocks: list[str]) -> bool:
    """Support has validation block behavior.
    
    Parameters
    ----------
    blocks : list[str]
        The blocks value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for block in blocks:
        lowered = block.lower()
        if "python" in lowered and "validation" in lowered:
            return True
    return False


def _field_value(text: str, field: str) -> str:
    """Support field value behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    field : str
        The field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _gate_section_value(text, field).splitlines()[0].strip()


def _section_value(text: str, field: str, all_fields: tuple[str, ...], title_field: str) -> str:
    """Support section value behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    field : str
        The field value.
    all_fields : tuple[str, ...]
        The all fields value.
    title_field : str
        The title field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    pattern = re.compile(r"(?im)^" + re.escape(field) + r"\s*(.*)$")
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    first_line = match.group(1).strip()
    next_positions = []
    for candidate in all_fields:
        if candidate == field or candidate == title_field:
            continue
        candidate_pattern = re.compile(r"(?im)^" + re.escape(candidate))
        candidate_match = candidate_pattern.search(text, start)
        if candidate_match:
            next_positions.append(candidate_match.start())
    end = min(next_positions) if next_positions else len(text)
    continuation = text[start:end].strip()
    if continuation:
        return (first_line + "\n" + continuation).strip()
    return first_line


def _gate_section_value(text: str, field: str) -> str:
    """Support gate section value behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    field : str
        The field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _section_value(text, field, REQUIRED_GATE_FIELDS, "PATCH DELIVERY GATE")


def _receiver_gate_value(text: str, field: str) -> str:
    """Support receiver gate value behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    field : str
        The field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _section_value(text, field, RECEIVER_GATE_FIELDS, "RECEIVER DELIVERY CHECK")


def _has_any_term(text: str, terms: tuple[str, ...]) -> bool:
    """Support has any term behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    terms : tuple[str, ...]
        The terms value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = text.lower()
    return any(term in lowered for term in terms)


def _is_install_block(block: str) -> bool:
    """Return whether the block appears to be a KANDA install block."""
    lowered = block.lower()
    return "expand-archive" in lowered and DAILY_WORK_TOKEN in lowered


def _is_non_install_terminal_block(block: str) -> bool:
    """Return whether the block needs the non-install terminal cleanup footer."""
    lowered = block.lower()
    if _is_install_block(block):
        return False
    terminal_triggers = (
        "read-host",
        "clear-host",
        "python ",
        "set-location",
        "validation",
        "validate_",
        "freeze",
        "merge_validation",
        "zip contract",
    )
    return any(trigger in lowered for trigger in terminal_triggers)


def _needs_receiver_gate(text: str) -> bool:
    """Support needs receiver gate behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = text.lower()
    triggers = (
        "governance intake",
        "manual receiver bundle",
        "receiver-ready",
        "freeze form",
        "freeze hint",
        "freeze_hint_intake",
        "kanda_freeze_hint.json",
        "error memory lesson",
        "error memory intake",
        "ai-assisted error lesson intake",
        "kanda_freeze_form_json_begin",
        "kanda_error_lesson_json_begin",
    )
    return _has_zip_reference(text) and any(trigger in lowered for trigger in triggers)


def _extract_marker_json(text: str, begin_marker: str, end_marker: str, label: str) -> object | None:
    """Support extract marker json behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    begin_marker : str
        The begin marker value.
    end_marker : str
        The end marker value.
    label : str
        The label value.
    
    Returns
    -------
    object | None
        The object result.
    """
    
    if begin_marker not in text and end_marker not in text:
        return None
    if begin_marker not in text or end_marker not in text:
        _fail(label + " marker wrapper must include both BEGIN and END markers.")
    begin = text.find(begin_marker)
    end = text.find(end_marker, begin)
    if begin == -1 or end == -1 or end <= begin:
        _fail(label + " markers are malformed or out of order.")
    fence_before = text.rfind("```", 0, begin)
    fence_after = text.find("```", begin, end)
    if fence_before != -1 and fence_after != -1 and fence_before < begin < fence_after:
        _fail(label + " markers must not be wrapped inside markdown code fences.")
    payload = text[begin + len(begin_marker):end].strip()
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        _fail(label + " marker content must be valid JSON: " + str(exc))
    return None


def _require_non_empty(value: object, field: str) -> None:
    """Support require non empty behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    field : str
        The field value.
    """
    
    if value is None:
        _fail(field + " is required and cannot be null.")
    if isinstance(value, str) and not value.strip():
        _fail(field + " is required and cannot be empty.")
    if isinstance(value, (list, tuple, dict)) and not value:
        _fail(field + " is required and cannot be empty.")


def _receiver_flag(text: str, field: str) -> str:
    """Support receiver flag behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    field : str
        The field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _receiver_gate_value(text, field).splitlines()[0].strip().lower()


def _install_blocks_with_expand(blocks: list[str]) -> list[str]:
    """Support install blocks with expand behavior.
    
    Parameters
    ----------
    blocks : list[str]
        The blocks value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return [block for block in blocks if "expand-archive" in block.lower()]


def _install_proves_token(blocks: list[str], token: str, *, require_copy: bool = True) -> bool:
    """Support install proves token behavior.
    
    Parameters
    ----------
    blocks : list[str]
        The blocks value.
    token : str
        The token value.
    require_copy : bool, optional
        The optional require copy value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for block in _install_blocks_with_expand(blocks):
        lowered = block.lower()
        if token.lower() in lowered and (not require_copy or "copy-item" in lowered):
            return True
    return False


def _validate_helper_project_import_path_contract(block: str) -> None:
    """Support validate helper project import path contract behavior.
    
    Parameters
    ----------
    block : str
        The block value.
    """
    
    lowered = block.lower()
    helper_terms = (
        "$helper_py",
        "freeze_prep",
        "merge_validation_evidence_into_latest_hint",
        "scan_and_save_latest_freeze_hint",
    )
    runs_helper = "$helper_py" in lowered and re.search(r"python(?:\.exe)?\s+\$helper_py", lowered) is not None
    imports_project = "kanda_reasoner_app" in lowered or any(term in lowered for term in helper_terms[1:])
    if not (runs_helper and imports_project):
        return
    has_powershell_path = "$env:pythonpath" in lowered and "$project_root" in lowered
    has_helper_sys_path = "sys.path.insert" in lowered and "project_root" in lowered
    if not has_powershell_path:
        _fail("Python helper blocks that import project packages must set $env:PYTHONPATH = $PROJECT_ROOT before running the helper.")
    if not has_helper_sys_path:
        _fail("Python helper files that import project packages must insert project_root into sys.path before project imports.")
