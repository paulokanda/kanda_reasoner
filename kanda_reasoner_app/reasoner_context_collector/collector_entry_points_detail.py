# project-path: kanda_reasoner_app/reasoner_context_collector/collector_entry_points_detail.py
"""Build detailed entry point records for Project Reasoner web AI.

This module creates a compact additive companion to project_summary.entry_files.
It helps web AI distinguish GUI entry points, collector tools, splitter tools,
CLI modules, tests, and scripts.

It does not replace entry_files, files, symbol_index, or any existing collector
output.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "build_entry_points_detail",
    "build_entry_points_detail_summary",
]


def _safe_text(value: Any) -> str:
    """Return a safe stripped string."""
    return str(value or "").strip()


def _normalize_path(value: Any) -> str:
    """Normalize file paths to forward slashes."""
    text = _safe_text(value).replace("\\", "/")
    while "//" in text:
        text = text.replace("//", "/")
    return text.strip("/")


def _lower_blob(parts: list[Any]) -> str:
    """Build a lowercase search blob from mixed values."""
    return " ".join(_safe_text(item) for item in parts).lower()


def _iter_symbols(file_record: dict[str, Any]) -> list[str]:
    """Return function/class/method names from a file record."""
    names: list[str] = []

    for function_record in file_record.get("functions", []):
        if isinstance(function_record, dict):
            names.append(_safe_text(function_record.get("name", "")))
            names.append(_safe_text(function_record.get("qualname", "")))

    for class_record in file_record.get("classes", []):
        if not isinstance(class_record, dict):
            continue

        names.append(_safe_text(class_record.get("name", "")))
        names.append(_safe_text(class_record.get("qualname", "")))

        for method_record in class_record.get("methods", []):
            if isinstance(method_record, dict):
                names.append(_safe_text(method_record.get("name", "")))
                names.append(_safe_text(method_record.get("qualname", "")))

    return [name for name in names if name]


def _entry_marker_set(file_record: dict[str, Any]) -> set[str]:
    """Return normalized entry markers from an existing file record."""
    out: set[str] = set()
    markers = file_record.get("entry_markers", [])
    if isinstance(markers, list):
        for marker in markers:
            text = _safe_text(marker)
            if text:
                out.add(text)
    return out


def _has_main_guard(blob: str) -> bool:
    """Return True when source text hints at a Python main guard."""
    return "__name__" in blob and "__main__" in blob


def _classify_entry_kind(
    path: str,
    blob: str,
    entry_markers: set[str],
) -> tuple[str, str, str]:
    """Return kind, role, and confidence for an entry-like file."""
    normalized = _normalize_path(path)
    lowered_path = normalized.lower()
    basename = lowered_path.rsplit("/", 1)[-1]

    explicit_entry = bool("entry_candidate" in entry_markers)
    has_main_guard = _has_main_guard(blob)
    has_qapplication = "qapplication(" in blob

    if has_qapplication or "qmainwindow" in blob or "runnerwindow" in blob:
        if "data_collector" in lowered_path or "collector" in lowered_path:
            return "gui_tool", "project_structure_collector_gui", "high"
        if "json_splitter" in lowered_path or "splitter" in lowered_path:
            return "gui_tool", "json_splitter_gui", "high"
        return "gui", "main_gui_entry_or_window", "high" if explicit_entry else "medium"

    if "runner.py" in basename or lowered_path.endswith("/runner.py"):
        return "gui_tool", "tool_runner", "medium"

    if "splitter" in lowered_path:
        return "tool", "json_splitter_tool", "medium"

    if "collector" in lowered_path:
        return "tool", "collector_tool", "medium"

    if basename.startswith("test_") or "/tests/" in lowered_path:
        return "test", "test_entry_or_test_module", "low"

    if has_main_guard:
        return "cli", "command_line_entry", "high"

    if explicit_entry:
        return "script", "entry_candidate", "medium"

    return "module", "not_entry_or_support_module", "low"


def _entry_reason(
    path: str,
    blob: str,
    entry_markers: set[str],
    symbols: list[str],
) -> list[str]:
    """Return concise reason labels for an entry detail record."""
    reasons: list[str] = []
    lowered_path = path.lower()

    if "entry_candidate" in entry_markers:
        reasons.append("existing_entry_marker")

    if _has_main_guard(blob):
        reasons.append("main_guard")

    if "qapplication(" in blob:
        reasons.append("qapplication")

    if "qmainwindow" in blob:
        reasons.append("qmainwindow")

    if "runner" in lowered_path:
        reasons.append("runner_path")

    if "collector" in lowered_path:
        reasons.append("collector_path")

    if "splitter" in lowered_path:
        reasons.append("splitter_path")

    if any(name.lower().endswith("window") for name in symbols):
        reasons.append("window_symbol")

    if not reasons:
        reasons.append("entry_file_list")

    return reasons


def build_entry_points_detail_summary(
    entry_points_detail: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build compact summary for entry_points_detail."""
    kind_frequency: dict[str, int] = {}
    confidence_frequency: dict[str, int] = {}

    for item in entry_points_detail:
        if not isinstance(item, dict):
            continue
        kind = _safe_text(item.get("kind", "")) or "unknown"
        confidence = _safe_text(item.get("confidence", "")) or "unknown"
        kind_frequency[kind] = kind_frequency.get(kind, 0) + 1
        confidence_frequency[confidence] = confidence_frequency.get(confidence, 0) + 1

    return {
        "entry_point_count": len(entry_points_detail),
        "kind_frequency": dict(sorted(kind_frequency.items())),
        "confidence_frequency": dict(sorted(confidence_frequency.items())),
    }


def build_entry_points_detail(
    files_payload: list[dict[str, Any]],
    entry_files: list[str],
    *,
    enabled: bool = True,
) -> list[dict[str, Any]]:
    """Build additive detailed entry point records.

    Existing project_summary.entry_files remains the compatibility field. This
    helper only creates a richer companion list for web AI.
    """
    if not enabled:
        return []

    entry_file_set = {_normalize_path(item) for item in entry_files if _safe_text(item)}
    rows: list[dict[str, Any]] = []

    for file_record in files_payload:
        if not isinstance(file_record, dict):
            continue

        path = _normalize_path(file_record.get("path", ""))
        if not path:
            continue

        entry_markers = _entry_marker_set(file_record)
        symbols = _iter_symbols(file_record)

        strings = file_record.get("strings", [])
        if not isinstance(strings, list):
            strings = []
        comments = file_record.get("comments", [])
        if not isinstance(comments, list):
            comments = []

        blob = _lower_blob(
            [
                path,
                file_record.get("module_name", ""),
                file_record.get("docstring", ""),
                " ".join(strings),
                " ".join(comments),
                " ".join(symbols),
                " ".join(entry_markers),
            ]
        )

        explicit_entry = path in entry_file_set or "entry_candidate" in entry_markers
        path_hint = any(
            marker in path.lower()
            for marker in ("runner.py", "main.py", "app.py", "cli.py", "splitter", "collector")
        )

        if not explicit_entry and not path_hint:
            continue

        kind, role, confidence = _classify_entry_kind(path, blob, entry_markers)
        reasons = _entry_reason(path, blob, entry_markers, symbols)

        rows.append(
            {
                "path": path,
                "module_name": _safe_text(file_record.get("module_name", "")),
                "kind": kind,
                "role": role,
                "confidence": confidence,
                "is_existing_entry_file": path in entry_file_set,
                "entry_markers": sorted(entry_markers),
                "reason_parts": reasons,
                "important_symbols": symbols[:12],
            }
        )

    rows.sort(
        key=lambda item: (
            str(item.get("kind", "")),
            str(item.get("role", "")),
            str(item.get("path", "")),
        )
    )
    return rows
