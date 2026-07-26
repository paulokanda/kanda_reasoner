# project-path: kanda_reasoner_app/error_memory/intake_plain_text.py
"""Plain-text fallback intake for Error Memory AI responses."""

from __future__ import annotations

from typing import Any

from .intake_normalization import _REQUIRED_ACTIVE_AI_KEYS, _as_list


def _normalize_plain_text_input(raw_text: str) -> str:
    """Normalize raw plain-text intake without importing the JSON parser."""
    return (
        str(raw_text or "")
        .replace("\ufeff", "")
        .replace("\u200b", "")
        .replace("\u200c", "")
        .replace("\u200d", "")
        .replace("\u00a0", " ")
        .strip()
    )


def _strip_list_marker(line: str) -> str:
    """Remove common bullet/list prefixes from one plain-text line."""
    cleaned = str(line or "").strip()
    while cleaned.startswith(("-", "*", "\u2022")):
        cleaned = cleaned[1:].strip()
    if len(cleaned) > 2 and cleaned[0].isdigit() and cleaned[1] in {".", ")"}:
        cleaned = cleaned[2:].strip()
    return cleaned


def _label_key(line: str) -> tuple[str, str] | None:
    """Return a normalized field label/value pair for simple plain-text labels."""
    if ":" not in line:
        return None
    left, right = line.split(":", 1)
    label = left.strip().lower().replace("-", "_").replace(" ", "_")
    mapping = {
        "symptom": "symptom",
        "problem": "symptom",
        "error": "raw_error_text",
        "raw_error": "raw_error_text",
        "raw_error_text": "raw_error_text",
        "phase": "operation_phase",
        "operation_phase": "operation_phase",
        "root_cause": "root_cause",
        "cause": "root_cause",
        "wrong_assumption": "wrong_assumption",
        "assumption": "wrong_assumption",
        "correct_fix": "correct_fix",
        "fix": "correct_fix",
        "correction": "correct_fix",
        "long_term_prevention": "long_term_prevention",
        "prevention": "long_term_prevention",
        "do_not_repeat_rule": "do_not_repeat_rule",
        "do_not_repeat": "do_not_repeat_rule",
        "rule": "do_not_repeat_rule",
        "prevention_triggers": "prevention_triggers",
        "triggers": "prevention_triggers",
        "validation_evidence": "validation_evidence",
        "evidence": "validation_evidence",
        "notes": "notes",
    }
    key = mapping.get(label)
    if not key:
        return None
    return key, right.strip()


def _infer_phase_from_plain_text(text: str) -> str:
    """Infer the operation phase from an unstructured error/lesson note."""
    lowered = text.lower()
    if "zip contract" in lowered or "patch zip" in lowered:
        return "patch_contract"
    if "install" in lowered or "installer" in lowered:
        return "install"
    if "validation" in lowered or "pytest" in lowered or "py_compile" in lowered:
        return "validation"
    if "freeze" in lowered:
        return "freeze_write"
    if "gui" in lowered or "tab" in lowered:
        return "gui"
    if "traceback" in lowered or "exception" in lowered:
        return "runtime"
    return "unknown"


def _plain_text_triggers(text: str) -> list[str]:
    """Extract conservative trigger phrases from a short plain-text lesson."""
    triggers: list[str] = []
    lowered = text.lower()
    known_terms = [
        "keyerror",
        "modulenotfounderror",
        "filenotfounderror",
        "syntaxerror",
        "assertionerror",
        "validation failed",
        "zip contract",
        "status: in_sync",
        "gui state",
        "validation-visible gui key",
        "project_error_memory",
        "second_prompt_files",
    ]
    for term in known_terms:
        if term in lowered:
            triggers.append(term)
    for token in ("missing", "not found", "must return", "do not add", "do not install", "must not"):
        if token in lowered:
            triggers.append(token)
    # Preserve specific snake_case identifiers because they are useful exact triggers.
    for raw in text.replace("'", " ").replace('"', " ").split():
        word = raw.strip(".,;:()[]{}<>\\/")
        if "_" in word and len(word) >= 6 and word not in triggers:
            triggers.append(word[:120])
    return triggers[:12]


def _plain_text_to_form(raw_text: str) -> dict[str, Any]:
    """Convert unstructured AI lesson text into a draft Error Memory form.

    This is intentionally a fallback. It prevents the GUI from doing nothing
    when AI returns a short lesson sentence instead of the strict JSON block.
    The result defaults to draft unless enough required fields are present.
    """
    normalized = _normalize_plain_text_input(raw_text)
    lines = [_strip_list_marker(line) for line in normalized.splitlines() if _strip_list_marker(line)]
    if not lines:
        raise ValueError("Empty Error Memory lesson text.")
    form: dict[str, Any] = {
        "status": "draft",
        "raw_error_text": normalized,
        "operation_phase": _infer_phase_from_plain_text(normalized),
        "symptom": "",
        "root_cause": "",
        "wrong_assumption": "",
        "correct_fix": "",
        "long_term_prevention": "",
        "do_not_repeat_rule": "",
        "prevention_triggers": _plain_text_triggers(normalized),
        "validation_evidence": [],
        "regression_check": {
            "type": "not_available",
            "command": "",
            "expected_marker": "",
            "required_before_freeze": False,
        },
        "source_patch_zip": "",
        "install_command_summary": "",
        "validation_command_summary": "",
        "notes": "Plain-text fallback intake. Ask AI for the full KANDA_ERROR_LESSON_JSON block to convert this draft into a complete active lesson.",
    }
    unlabeled: list[str] = []
    for line in lines:
        labeled = _label_key(line)
        if labeled:
            key, value = labeled
            if key in {"prevention_triggers", "validation_evidence"}:
                form[key] = _as_list(value)
            else:
                form[key] = value
            continue
        unlabeled.append(line)
    if not form["symptom"] and unlabeled:
        form["symptom"] = unlabeled[0][:220]
    if not form["do_not_repeat_rule"]:
        do_not_lines = [line for line in unlabeled[1:] if line.lower().startswith(("do not", "don't", "never", "avoid", "must not"))]
        if do_not_lines:
            form["do_not_repeat_rule"] = do_not_lines[0]
        elif len(unlabeled) >= 2:
            form["do_not_repeat_rule"] = unlabeled[1][:300]
    # If a concise AI note provides only symptom + rule, treat it as a useful draft.
    if form["symptom"] and form["do_not_repeat_rule"] and not form["prevention_triggers"]:
        form["prevention_triggers"] = _plain_text_triggers(form["symptom"] + "\n" + form["do_not_repeat_rule"])
    required_present = all(str(form.get(key) or "").strip() for key in _REQUIRED_ACTIVE_AI_KEYS if key != "prevention_triggers")
    if required_present and _as_list(form.get("prevention_triggers")):
        form["status"] = str(form.get("status") or "active").lower()
    else:
        form["status"] = "draft"
    return form
