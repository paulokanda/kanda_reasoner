# project-path: kanda_reasoner_app/error_memory_gui/_lesson_status_summary.py
"""Status summary chips for the Error Memory Lessons table."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

__all__ = [
    "LESSON_STATUS_SUMMARY_ORDER",
    "count_lesson_statuses",
    "lesson_status_summary_items",
    "normalized_lesson_status",
    "render_lesson_status_summary",
]

LESSON_STATUS_SUMMARY_ORDER: tuple[tuple[str, str, str], ...] = (
    (
        "active",
        "Active",
        "Exported as enforced Error Memory guidance for AI.",
    ),
    (
        "draft",
        "Draft",
        "Saved in the lesson store for later correction or completion; not exported as active guidance.",
    ),
    (
        "deprecated",
        "Deprecated",
        "Kept in the lesson store but excluded from active exports.",
    ),
    (
        "superseded",
        "Superseded",
        "Replaced by another lesson; should record the replacement in superseded_by.",
    ),
    (
        "pending_edit",
        "Pending edit",
        "Raw pending evidence waiting for edition. Virtual row; not saved until the user acts.",
    ),
    (
        "pending_review",
        "Pending review",
        "Formatted pending lesson waiting for user review. Virtual row; not saved until the user acts.",
    ),
    (
        "pending_duplicate",
        "Pending duplicated",
        "Formatted pending lesson appears to duplicate an existing lesson. Virtual row; review or clean before saving.",
    ),
)

_SUMMARY_STATUS_KEYS = {status for status, _label, _tooltip in LESSON_STATUS_SUMMARY_ORDER}


def normalized_lesson_status(value: Any) -> str:
    """Return a stable status key for lesson and pending-row handling."""
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def count_lesson_statuses(
    lessons: Iterable[Mapping[str, Any]],
    pending_rows: Iterable[Mapping[str, Any]],
) -> dict[str, int]:
    """Return counts for saved and pending Lessons-table statuses."""
    counts = {status: 0 for status, _label, _tooltip in LESSON_STATUS_SUMMARY_ORDER}
    for lesson in lessons:
        status = normalized_lesson_status(lesson.get("status"))
        if status in _SUMMARY_STATUS_KEYS:
            counts[status] += 1
    for pending in pending_rows:
        status = normalized_lesson_status(pending.get("status") or pending.get("kind"))
        if status in _SUMMARY_STATUS_KEYS:
            counts[status] += 1
    return counts


def lesson_status_summary_items(
    lessons: Iterable[Mapping[str, Any]],
    pending_rows: Iterable[Mapping[str, Any]],
) -> list[tuple[str, str, int, str]]:
    """Return nonzero summary items in the required display order."""
    counts = count_lesson_statuses(lessons, pending_rows)
    items: list[tuple[str, str, int, str]] = []
    for status, label, tooltip in LESSON_STATUS_SUMMARY_ORDER:
        count = counts.get(status, 0)
        if count > 0:
            items.append((status, label, count, tooltip))
    return items


def _clear_layout(layout: Any) -> None:
    """Remove existing Qt widgets/items from a layout."""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()


def _set_status_priority(tab: Any, status: str) -> None:
    """Set the clicked status as the Lessons-table priority status."""
    tab._lesson_status_priority_status = status
    reload_table = getattr(tab, "_reload_table", None)
    if callable(reload_table):
        reload_table()


def render_lesson_status_summary(
    tab: Any,
    lessons: Iterable[Mapping[str, Any]],
    pending_rows: Iterable[Mapping[str, Any]],
) -> None:
    """Render clickable nonzero Lessons status counters above the table."""
    layout = getattr(tab, "lesson_status_summary_layout", None)
    if layout is None:
        return
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QPushButton

    selected_status = normalized_lesson_status(
        getattr(tab, "_lesson_status_priority_status", "")
    )
    _clear_layout(layout)
    for status, label, count, tooltip in lesson_status_summary_items(lessons, pending_rows):
        chip = QPushButton(label + " " + str(count))
        chip.setObjectName("error_memory_lesson_status_summary_" + status)
        chip.setToolTip(tooltip + " Click to bring these rows to the top of the Lessons list.")
        chip.setCursor(Qt.PointingHandCursor)
        if status == selected_status:
            chip.setStyleSheet(
                "QPushButton { padding: 3px 8px; border: 1px solid #4F79C7; "
                "border-radius: 8px; background: #EAF1FF; color: #102A5C; "
                "font-weight: 700; }"
            )
        else:
            chip.setStyleSheet(
                "QPushButton { padding: 3px 8px; border: 1px solid #C9D2E3; "
                "border-radius: 8px; background: #F7F9FC; color: #20314D; }"
                "QPushButton:hover { border-color: #7896CC; background: #EEF4FF; }"
            )
        chip.clicked.connect(lambda _checked=False, value=status: _set_status_priority(tab, value))
        layout.addWidget(chip)
    layout.addStretch(1)
