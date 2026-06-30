# project-path: kanda_reasoner_app/freeze_after_update_gui/local_freeze_preview_log.py
"""Plain-text renderer for local freeze-entry preview log visibility.

This module intentionally has no Qt dependency so the preview/log contract can
be tested without importing the GUI toolkit. It only formats already-generated
preview dictionaries; it never writes freeze memory.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


LOCAL_FREEZE_PREVIEW_LOG_BEGIN = "LOCAL FREEZE ENTRY PREVIEW BEGIN"
LOCAL_FREEZE_PREVIEW_LOG_END = "LOCAL FREEZE ENTRY PREVIEW END"


def _as_lines(value: Any) -> list[str]:
    """Support as lines behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "")
    return [line.strip() for line in text.splitlines() if line.strip()]


def _extend_findings(lines: list[str], label: str, findings: Any) -> None:
    """Support extend findings behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    label : str
        The label value.
    findings : Any
        The findings value.
    """
    
    items = _as_lines(findings)
    if not items:
        return
    lines.append(label + ":")
    lines.extend("- " + item for item in items)
    lines.append("")


def build_local_freeze_preview_log_text(
    preview: Mapping[str, Any],
    validation: Mapping[str, Any] | None = None,
) -> str:
    """Render the real freeze-entry preview for the human-visible log.

    The Freeze Feature After Update tab already shows a dedicated read-only
    preview field inside the local-freeze dialog. This renderer mirrors the
    same preview Markdown into the main log so the human can verify exactly
    what will be frozen before pressing Confirm and Write.
    """

    preview_dict = dict(preview or {})
    validation_dict = dict(validation or {}) if validation is not None else None
    markdown = str(preview_dict.get("markdown") or "").rstrip()

    lines: list[str] = [LOCAL_FREEZE_PREVIEW_LOG_BEGIN]
    lines.append("Freeze ID: " + str(preview_dict.get("freeze_id") or ""))
    lines.append("Feature title: " + str(preview_dict.get("feature_title") or ""))
    lines.append("Primary box: " + str(preview_dict.get("primary_box") or ""))
    lines.append("Box type: " + str(preview_dict.get("box_type") or ""))
    lines.append("Writable: " + ("YES" if preview_dict.get("is_writable") else "NO"))
    if validation_dict is None:
        lines.append("Validation: NOT RUN")
    else:
        lines.append("Validation: " + ("OK" if validation_dict.get("ok") else "BLOCKED"))
    lines.append("")

    _extend_findings(lines, "Preview errors", preview_dict.get("errors"))
    _extend_findings(lines, "Preview warnings", preview_dict.get("warnings"))
    if validation_dict is not None:
        _extend_findings(lines, "Validation errors", validation_dict.get("errors"))
        _extend_findings(lines, "Validation warnings", validation_dict.get("warnings"))

    targets = _as_lines(preview_dict.get("write_targets"))
    if targets:
        lines.append("Will write after Confirm and Write:")
        lines.extend("- " + target for target in targets)
        lines.append("")

    lines.append("Preview Markdown:")
    if markdown:
        lines.append(markdown)
    else:
        lines.append("[No preview markdown was returned by preview_freeze_entry.]")
    lines.append(LOCAL_FREEZE_PREVIEW_LOG_END)
    return "\n".join(lines).rstrip() + "\n"
