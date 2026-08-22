# project-path: kanda_reasoner_app/error_memory_gui/_lesson_status_summary.py
"""Status summary chips for the Error Memory lesson library."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

__all__ = [
    "LESSON_STATUS_SUMMARY_ORDER",
    "count_lesson_statuses",
    "lesson_status_summary_items",
    "normalized_lesson_status",
    "render_lesson_status_summary",
    "status_matches_summary_priority",
]

LESSON_STATUS_SUMMARY_ORDER: tuple[tuple[str, str, str], ...] = (
    ("active", "Active", "Lessons currently available as Error Memory guidance."),
    (
        "to_memorize",
        "To memorize",
        "Pending Error Memory lessons waiting for human Memorize Error.",
    ),
    ("draft", "Draft", "Saved lessons still being edited or reviewed."),
    (
        "retired",
        "Retired",
        "Known obsolete lessons kept so older Cards cannot silently resurrect them.",
    ),
)

_SUMMARY_STATUS_KEYS = {
    status for status, _label, _tooltip in LESSON_STATUS_SUMMARY_ORDER
}
_LEGACY_PENDING_STATUSES = {
    "pending_review", "pending_tool_review", "tool_pending_review",
    "pending_edit", "tool_pending_edit", "pending_duplicate",
    "tool_pending_duplicate",
}


def normalized_lesson_status(value: Any) -> str:
    """Return one stable lesson-library lifecycle status."""
    status = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if status in {"deprecated", "superseded"}:
        return "retired"
    if status in _LEGACY_PENDING_STATUSES:
        return "pending"
    return status


def count_lesson_statuses(
    lessons: Iterable[Mapping[str, Any]],
    pending_rows: Iterable[Mapping[str, Any]],
) -> dict[str, int]:
    """Return the four user-facing lesson-library lifecycle counts."""
    counts = {
        status: 0 for status, _label, _tooltip in LESSON_STATUS_SUMMARY_ORDER
    }
    for lesson in lessons:
        status = normalized_lesson_status(lesson.get("status"))
        if status == "pending":
            counts["to_memorize"] += 1
        elif status in _SUMMARY_STATUS_KEYS:
            counts[status] += 1
    for pending in pending_rows:
        status = normalized_lesson_status(
            pending.get("status") or pending.get("kind")
        )
        if status == "pending":
            counts["to_memorize"] += 1
        elif status in _SUMMARY_STATUS_KEYS:
            counts[status] += 1
    return counts


def lesson_status_summary_items(
    lessons,
    pending_rows,
):
    """Return canonical Error Memory counts plus separate To memorize."""
    saved = list(lessons or [])
    transport = list(pending_rows or [])

    counts = {"active": 0, "retired": 0, "draft": 0, "pending": 0}
    for lesson in saved:
        if not isinstance(lesson, dict):
            continue
        status = str(lesson.get("status") or "").strip().lower()
        if status in counts:
            counts[status] += 1

    return [
        ("active", "Active", counts["active"], "Canonical active Error Memory Lessons."),
        ("retired", "Retired", counts["retired"], "Canonical retired Error Memory Lessons."),
        ("draft", "Draft", counts["draft"], "Canonical draft Error Memory Lessons."),
        ("pending", "Pending", counts["pending"], "Canonical pending Error Memory Lessons."),
        ("", "Total", len(saved), "Total canonical Error Memory Lessons."),
        (
            "pending_review",
            "To memorize",
            len(transport),
            "Separate human-review intake queue; not yet canonical Lessons.",
        ),
    ]



def status_matches_summary_priority(
    row_status: Any,
    priority_status: Any,
) -> bool:
    """Return whether one row belongs to one clickable lesson-library summary group."""
    row = normalized_lesson_status(row_status)
    priority = normalized_lesson_status(priority_status)
    if priority == "to_memorize":
        return row == "pending"
    return bool(priority and row == priority)


def _clear_layout(layout: Any) -> None:
    """Remove existing Qt widgets/items from a layout."""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()


def _set_status_priority(tab: Any, status: str) -> None:
    """Set the clicked lesson status as the Lessons-table priority."""
    tab._lesson_status_priority_status = status
    reload_table = getattr(tab, "_reload_table", None)
    if callable(reload_table):
        reload_table()


def render_lesson_status_summary(
    tab: Any,
    lessons: Iterable[Mapping[str, Any]],
    pending_rows: Iterable[Mapping[str, Any]],
) -> None:
    """Render all Error Memory counters, including zeros."""
    layout = getattr(tab, "lesson_status_summary_layout", None)
    if layout is None:
        return

    from PySide6.QtWidgets import QPushButton

    selected_status = normalized_lesson_status(
        getattr(tab, "_lesson_status_priority_status", "")
    )
    _clear_layout(layout)

    for status, label, count, tooltip in lesson_status_summary_items(
        lessons,
        pending_rows,
    ):
        button = QPushButton(f"{label} {count}")
        button.setToolTip(tooltip)
        if status:
            normalized = normalized_lesson_status(status)
            button.setCheckable(True)
            button.setChecked(bool(normalized and normalized == selected_status))
            button.clicked.connect(
                lambda _checked=False, value=status: _set_status_priority(tab, value)
            )
        else:
            button.setCheckable(False)
        layout.addWidget(button)

    layout.addStretch(1)

