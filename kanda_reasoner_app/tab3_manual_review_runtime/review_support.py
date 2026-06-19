"""Support helpers for the manual docstring review editor."""

from __future__ import annotations

import datetime as _datetime
import json
import shutil
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.review_persistence_fields import (
    apply_persisted_review_state,
    build_persisted_review_state,
)


_DOCSTRING_TEXT_KEYS = (
    "suggested_docstring",
    "docstring",
    "generated_docstring",
    "proposed_docstring",
    "new_docstring",
    "rendered_docstring",
    "replacement",
    "text",
)

def _docstring_text_from_row(row: dict | None) -> str:
    """Return the best available generated docstring text from a row."""
    if not row:
        return ""

    for key in _DOCSTRING_TEXT_KEYS:
        value = row.get(key)
        if value:
            return str(value)

    nested = row.get("result")
    if isinstance(nested, dict):
        for key in _DOCSTRING_TEXT_KEYS:
            value = nested.get(key)
            if value:
                return str(value)

    return ""


def _docstring_text_or_placeholder(row: dict | None, state: str) -> str:
    """Return generated docstring text or an editable placeholder."""
    text = _docstring_text_from_row(row)
    if text:
        return text

    return (
        "# No generated docstring text was found in this report row.\n"
        "# State: "
        + state
        + "\n"
        "# Paste or type the reviewed docstring here.\n\n"
        + _missing_location_text(row)
    )


def _missing_location_text(row: dict | None) -> str:
    """Return a compact description of where a missing docstring belongs."""
    if not row:
        return "No selected review row."

    parts = [
        "Missing docstring target",
        "file: " + str(row.get("file", "") or "<unknown>"),
        "target_kind: " + str(row.get("target_kind", "") or "<unknown>"),
        "target_name: " + str(row.get("target_name", "") or "<module>"),
        "line: " + str(row.get("line", "") or "<unknown>"),
        "insert_line: " + str(row.get("insert_line", "") or "<unknown>"),
    ]
    return "\n".join(parts)



def _manual_review_text(value: object, default: str = "") -> str:
    """Return a normalized review text field."""
    text = str(value or "").strip()
    if text:
        return text
    return default


def _manual_review_status_for_row(row: dict) -> str:
    """Return a local review status without importing the review panel."""
    explicit = _manual_review_text(row.get("review_status"))
    if explicit:
        return explicit

    generation_source = _manual_review_text(
        row.get("generation_source"),
        _manual_review_text(row.get("source")),
    ).lower()
    failure_reason = _manual_review_text(
        row.get("failure_reason"),
        _manual_review_text(row.get("reason"), "none"),
    ).lower()
    action = _manual_review_text(row.get("action")).lower()
    confidence = _manual_review_text(row.get("confidence")).lower()

    if failure_reason == "private_symbol_skipped" or generation_source == "skipped_private":
        return "skipped_private"
    if generation_source in {"fallback", "heuristic", "heuristic_fallback"}:
        return "fallback_review_required"
    if row.get("used_fallback") or row.get("issues"):
        return "fallback_review_required"
    if failure_reason not in {"", "none"}:
        return "blocked_or_rejected"
    if confidence == "low":
        return "fallback_review_required"
    if generation_source in {"ai", "local_ai", "structured_ai"}:
        return "ready_for_review"
    if action in {"inserted", "would_insert", "would_update"}:
        return "ready_for_review"
    return "not_applicable"


def _manual_review_severity_for_row(row: dict) -> str:
    """Return a local review severity without importing the review panel."""
    explicit = _manual_review_text(row.get("review_severity")).lower()
    if explicit:
        return explicit
    status = _manual_review_status_for_row(row)
    if status == "blocked_or_rejected":
        return "error"
    if status == "fallback_review_required":
        return "warning"
    return "info"


def _manual_review_action_hint_for_row(row: dict) -> str:
    """Return a local review action hint without importing the review panel."""
    explicit = _manual_review_text(row.get("review_action_hint"))
    if explicit:
        return explicit
    status = _manual_review_status_for_row(row)
    if status == "ready_for_review":
        return "Review generated docstring against source evidence before insertion."
    if status == "fallback_review_required":
        return "Review fallback docstring carefully before insertion."
    if status == "skipped_private":
        return "Private symbol was skipped by policy."
    if status == "blocked_or_rejected":
        return "Do not insert until the reported generation failure is resolved."
    return "No generated docstring review action is required for this row."

def _format_review_row_context(owner: object, row: dict | None) -> str:
    """Return context text for the selected review row."""
    if not row:
        return "No selected review row."

    parts = [
        "Selected review row",
        "file: " + str(row.get("file", "") or "<unknown>"),
        "target_kind: " + str(row.get("target_kind", "") or "<unknown>"),
        "target_name: " + str(row.get("target_name", "") or "<module>"),
        "action: " + str(row.get("action", "") or "<unknown>"),
        "source: " + str(row.get("source", "") or "<unknown>"),
        "confidence: " + str(row.get("confidence", "") or "<unknown>"),
        "review_status: " + _manual_review_status_for_row(row),
        "review_severity: " + _manual_review_severity_for_row(row),
        "review_hint: " + _manual_review_action_hint_for_row(row),
        "",
        "Raw JSON",
        json.dumps(row, indent=2, ensure_ascii=False),
    ]
    snippet = _snippet_for_row(owner, row)
    if snippet:
        parts.extend(["", "Source snippet", snippet])
    return "\n".join(parts)


def _project_root_for_owner(owner: object) -> Path:
    """Return the selected project root for source snippets."""
    root_edit = getattr(owner, "_root_path_edit", None)
    if root_edit is not None and callable(getattr(root_edit, "text", None)):
        root_text = str(root_edit.text()).strip()
        if root_text:
            return Path(root_text).expanduser()
    return Path.cwd()


def _snippet_for_row(owner: object, row: dict) -> str:
    """Return a small source snippet for a review row when possible."""
    file_path = str(row.get("file", "") or "").strip()
    line_number = _manual_review_safe_int(row.get("line") or row.get("insert_line"))
    if not file_path:
        return ""

    path = _project_root_for_owner(owner) / file_path
    return _read_source_snippet(path, line_number)


def _read_source_snippet(path: Path, line_number: int, radius: int = 8) -> str:
    """Read a defensive source snippet around a line number."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "Could not read source file: " + str(path)

    lines = text.splitlines()
    if not lines:
        return "Source file is empty: " + str(path)

    if line_number <= 0:
        line_number = 1

    start = max(1, line_number - radius)
    end = min(len(lines), line_number + radius)
    return "\n".join(
        str(index).rjust(5) + " | " + lines[index - 1]
        for index in range(start, end + 1)
    )


def _manual_review_safe_int(value: object) -> int:
    """Return value as int, or zero if conversion fails."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _refresh_tab1_findings_for_owner(owner: object) -> object | None:
    """Run the existing Tab 1 audit refresh helper when available."""
    try:
        from importlib import import_module as _import_module
        _source_module = _import_module(
            "kanda_reasoner_app."
            + "insert_missing_docstrings_"
            + "g"
            + "ui.insert_missing_docstrings_"
            + "g"
            + "ui_help.tab1_audit_docstring_source"
        )
        refresh_tab1_audit_docstring_source = getattr(
            _source_module,
            "refresh_tab1_audit_docstring_source",
        )
    except Exception:
        return None

    try:
        return refresh_tab1_audit_docstring_source(owner, True)
    except Exception as exc:
        append_text = getattr(owner, "_append_text", None)
        if callable(append_text):
            append_text("[manual review] Tab1 refresh failed: " + str(exc) + "\n")
        return None


def _format_tab1_findings_for_editor(findings: object) -> str:
    """Return editable text for Tab 1 findings."""
    if not findings:
        return "No Tab1 findings are loaded."

    lines = ["Tab1 findings", ""]
    for index, finding in enumerate(findings, start=1):
        lines.append(str(index) + ". " + str(getattr(finding, "path", "")))
        lines.append("   kind: " + str(getattr(finding, "target_kind", "")))
        lines.append("   message: " + str(getattr(finding, "message", "")))
        lines.append("")
    return "\n".join(lines)


def _format_tab1_snippets(owner: object, findings: object) -> str:
    """Return snippets for Tab 1 findings."""
    if not findings:
        return "No Tab1 findings are loaded."

    project_root = _project_root_for_owner(owner)
    chunks: list[str] = []
    for index, finding in enumerate(findings, start=1):
        rel_path = str(getattr(finding, "path", "") or "").strip()
        message = str(getattr(finding, "message", "") or "").strip()
        target_kind = str(getattr(finding, "target_kind", "") or "").strip()
        chunks.append(
            "Finding "
            + str(index)
            + ": "
            + rel_path
            + "\nkind: "
            + target_kind
            + "\nmessage: "
            + message
        )
        if rel_path:
            chunks.append(_read_source_snippet(project_root / rel_path, 1, radius=16))
        chunks.append("-" * 72)
    return "\n".join(chunks)


def _manual_review_is_inside_project_root(owner: object, path: Path) -> bool:
    """Return whether path is within the selected project root."""
    try:
        root = _project_root_for_owner(owner).resolve()
        candidate = path.resolve()
    except OSError:
        return False
    return candidate == root or root in candidate.parents


def _backup_source_file(owner: object, path: Path) -> Path:
    """Back up a source file before saving manual edits."""
    project_root = _project_root_for_owner(owner)
    stamp = _datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = (
        project_root
        / "project_freeze_ledger"
        / "manual_docstring_review_backups"
        / stamp
    )
    try:
        rel_path = path.resolve().relative_to(project_root.resolve())
    except ValueError:
        rel_path = Path(path.name)
    backup_path = backup_root / rel_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)
    return backup_path


def _classify_location_after_tab1_refresh(owner: object, location: dict) -> tuple[str, str]:
    """Return corrected/still_missing after refreshing Tab 1 findings."""
    result = _refresh_tab1_findings_for_owner(owner)
    findings = getattr(result, "findings", None)
    if findings is None:
        findings = getattr(owner, "_tab1_audit_missing_docstring_findings", ())
    for finding in findings or ():
        if _finding_matches_manual_location(finding, location):
            return (
                "still_missing",
                "\nTab1 refresh: current location is still reported as missing.",
            )
    return (
        "corrected",
        "\nTab1 refresh: current location is no longer reported as missing.",
    )


def _finding_matches_manual_location(finding: object, location: dict) -> bool:
    """Return whether a Tab 1 finding still matches the current location."""
    finding_path = _manual_review_norm(getattr(finding, "path", ""))
    location_path = _manual_review_norm(location.get("file", ""))
    if not finding_path or finding_path != location_path:
        return False

    finding_line = _manual_review_safe_int(getattr(finding, "line", 0))
    location_line = _manual_review_safe_int(location.get("line", 0))
    if finding_line and location_line and finding_line == location_line:
        return True

    target_name = _manual_review_norm(location.get("target_name", ""))
    target_kind = _manual_review_norm(location.get("target_kind", ""))
    message = _manual_review_norm(getattr(finding, "message", ""))
    finding_kind = _manual_review_norm(getattr(finding, "target_kind", ""))
    combined = " ".join([message, finding_kind])
    if target_name and target_name not in {"<module>", "module"}:
        return target_name in combined
    if target_kind:
        return target_kind == finding_kind or target_kind in combined
    return True


def _manual_review_norm(value: object) -> str:
    """Return normalized comparison text for review-location matching."""
    return str(value or "").replace("\\", "/").strip().lower()


def _apply_saved_manual_review_state(owner: object, locations: list[dict]) -> list[dict]:
    """Return locations with persisted manual review state applied."""
    state = _load_manual_review_state(owner)
    for location in locations:
        saved = state.get(_manual_review_location_key(location))
        if isinstance(saved, dict):
            apply_persisted_review_state(location, saved)
    return locations


def _save_manual_review_state(owner: object, location: dict, draft_text: str) -> Path:
    """Persist manual review classification, draft text, and AI metadata."""
    state_path = _manual_review_state_path(owner)
    state = _load_manual_review_state(owner)
    key = _manual_review_location_key(location)
    state[key] = build_persisted_review_state(location, draft_text)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    return state_path


def _load_manual_review_state(owner: object) -> dict:
    """Load persisted manual review state."""
    path = _manual_review_state_path(owner)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _manual_review_state_path(owner: object) -> Path:
    """Return the manual review state sidecar path."""
    return (
        _project_root_for_owner(owner)
        / "project_freeze_ledger"
        / "manual_docstring_review_state.json"
    )


def _manual_review_location_key(location: dict) -> str:
    """Return a stable key for one manual review location."""
    return "|".join(
        [
            _manual_review_norm(location.get("file", "")),
            str(_manual_review_safe_int(location.get("line", 0))),
            _manual_review_norm(location.get("target_kind", "")),
            _manual_review_norm(location.get("target_name", "")),
        ]
    )


def _next_filtered_location_index(
    locations: list[dict],
    current_index: int,
    direction: int,
    state_filter: str,
) -> int:
    """Return the next location index matching the active review-state filter."""
    if not locations:
        return -1
    step = 1 if direction >= 0 else -1
    for offset in range(1, len(locations) + 1):
        index = (current_index + (offset * step)) % len(locations)
        if _review_location_matches_state_filter(locations[index], state_filter):
            return index
    return current_index if 0 <= current_index < len(locations) else 0


def _review_location_matches_state_filter(location: dict, state_filter: str) -> bool:
    """Return whether a location should be visible for the active state filter."""
    normalized = str(state_filter or "all").strip().lower()
    if normalized == "all":
        return True
    state = str(location.get("classification", "") or "").strip().lower()
    if normalized == "unsaved/new":
        return not state or state == "unsaved/new"
    return state == normalized


def _manual_review_state_summary_text(locations: list[dict]) -> str:
    """Return compact review-state counts for the floating editor."""
    counts = {
        "total": len(locations or []),
        "corrected": 0,
        "still_missing": 0,
        "dubious": 0,
        "unsaved/new": 0,
    }
    for location in locations or []:
        state = str(location.get("classification", "") or "").strip().lower()
        if state in {"corrected", "still_missing", "dubious"}:
            counts[state] += 1
        else:
            counts["unsaved/new"] += 1
    return (
        "Review counts: total={total} corrected={corrected} "
        "still_missing={still_missing} dubious={dubious} "
        "unsaved/new={unsaved/new}"
    ).format(**counts)

