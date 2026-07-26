# project-path: kanda_reasoner_app/prompt_router_reasoner_gui/_prompt_router_reasoner_tab_ui.py
"""Private visual composition and bounded debounce support for Prompt Router tab."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QMetaObject
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

__all__: list[str] = []


class _SingleShotDebounceTimer:
    """UI-thread debounce owner backed by QObject timer events."""

    def __init__(self, owner: QWidget, callback: Callable[[], None]) -> None:
        self._owner = owner
        self._callback = callback
        self._single_shot = False
        self._timer_id = 0
        self._interval_ms = 0

    def setSingleShot(self, enabled: bool) -> None:  # noqa: N802 - Qt-compatible private API
        """Set whether the next timer event stops before callback execution."""
        self._single_shot = bool(enabled)

    def isSingleShot(self) -> bool:  # noqa: N802 - Qt-compatible private API
        """Return the configured single-shot mode."""
        return self._single_shot

    def start(self, interval_ms: int) -> None:
        """Restart the debounce timer with the requested interval."""
        self.stop()
        self._interval_ms = int(interval_ms)
        self._timer_id = int(self._owner.startTimer(self._interval_ms))

    def interval(self) -> int:
        """Return the configured interval in milliseconds."""
        return self._interval_ms

    def isActive(self) -> bool:  # noqa: N802 - Qt-compatible private API
        """Return whether a debounce timer event is currently pending."""
        return bool(self._timer_id)

    def stop(self) -> None:
        """Stop the active owner timer, if any."""
        if not self._timer_id:
            return
        self._owner.killTimer(self._timer_id)
        self._timer_id = 0

    def handle_timer_event(self, event: Any) -> bool:
        """Consume the matching timer event and run the callback."""
        if not self._timer_id or int(event.timerId()) != self._timer_id:
            return False
        if self._single_shot:
            self.stop()
        self._callback()
        return True


def create_auto_capture_timer(
    owner: QWidget,
    callback: Callable[[], None],
) -> _SingleShotDebounceTimer:
    """Create the tab's single-shot debounce owner."""
    timer = _SingleShotDebounceTimer(owner, callback)
    timer.setSingleShot(True)
    return timer


def build_tab_ui(owner: QWidget) -> None:
    """Compose the visible two-editor Prompt Router workspace."""
    outer = QVBoxLayout(owner)
    outer.setContentsMargins(12, 12, 12, 12)
    outer.setSpacing(10)

    outer.addWidget(owner._build_header())
    outer.addWidget(owner._build_manual_code_group(), 1)
    outer.addWidget(owner._build_final_prompt_group(), 2)
    QMetaObject.connectSlotsByName(owner)


def build_header(owner, tab_title: str) -> QWidget:
    """Support build header behavior.
    
    Returns
    -------
    QWidget
        The qwidget result.
    """
    
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(4)

    title = QLabel(tab_title)
    title.setObjectName("prompt_router_reasoner_title_label")
    title.setStyleSheet("font-size: 16px; font-weight: bold;")
    layout.addWidget(title)

    subtitle = QLabel(
        "Manual round-trip workspace. Paste the KANDA_ROUTING_CHOICE block "
        "from browser ChatGPT; KANDA validates it and automatically loads "
        "the complete canonical prompt below."
    )
    subtitle.setObjectName("prompt_router_reasoner_subtitle_label")
    subtitle.setWordWrap(True)
    layout.addWidget(subtitle)

    root_row = QHBoxLayout()
    root_row.addWidget(QLabel("Project root:"))
    owner.project_root_edit = QLineEdit()
    owner.project_root_edit.setObjectName("project_root_edit")
    owner.project_root_edit.setReadOnly(True)
    owner.project_root_edit.setPlaceholderText("Project root will be supplied by the shell")
    root_row.addWidget(owner.project_root_edit, 1)
    layout.addLayout(root_row)

    owner.manual_router_choice_status_label = QLabel(
        "Manual capture status: waiting for ChatGPT KANDA_ROUTING_CHOICE code."
    )
    owner.manual_router_choice_status_label.setObjectName(
        "prompt_router_reasoner_manual_router_choice_status_label"
    )
    owner.manual_router_choice_status_label.setWordWrap(True)
    layout.addWidget(owner.manual_router_choice_status_label)
    return panel


def build_manual_code_group(owner) -> QGroupBox:
    """Support build manual code group behavior.
    
    Returns
    -------
    QGroupBox
        The qgroup box result.
    """
    
    group = QGroupBox("Manual router choice capture")
    group.setObjectName("prompt_router_reasoner_manual_router_choice_capture_group")
    layout = QVBoxLayout(group)

    intro = QLabel(
        "Paste code copied from ChatGPT here. When the block is valid, the "
        "complete prompt loads automatically in the editor below. This does "
        "not activate ML and does not write prompt-library or freeze files."
    )
    intro.setObjectName("prompt_router_reasoner_manual_router_choice_intro")
    intro.setWordWrap(True)
    layout.addWidget(intro)

    owner.manual_router_choice_code_editor = QPlainTextEdit()
    owner.manual_router_choice_code_editor.setObjectName("manual_router_choice_code_editor")
    owner.manual_router_choice_code_editor.setPlaceholderText(
        "Paste KANDA_ROUTING_CHOICE_START ... KANDA_ROUTING_CHOICE_END here."
    )
    layout.addWidget(owner.manual_router_choice_code_editor, 1)

    button_row = QHBoxLayout()
    owner.paste_router_choice_code_button = QPushButton("Paste")
    owner.paste_router_choice_code_button.setObjectName(
        "prompt_router_reasoner_paste_router_choice_code_button"
    )
    owner.paste_router_choice_code_button.setToolTip("Paste router-choice code from clipboard.")
    button_row.addWidget(owner.paste_router_choice_code_button)

    owner.undo_router_choice_code_button = QPushButton("Undo")
    owner.undo_router_choice_code_button.setObjectName(
        "prompt_router_reasoner_undo_router_choice_code_button"
    )
    owner.undo_router_choice_code_button.setToolTip("Undo changes in the ChatGPT-code editor.")
    button_row.addWidget(owner.undo_router_choice_code_button)

    owner.clear_router_choice_code_button = QPushButton("Clear")
    owner.clear_router_choice_code_button.setObjectName(
        "prompt_router_reasoner_clear_router_choice_code_button"
    )
    owner.clear_router_choice_code_button.setToolTip("Clear pasted code and final prompt editor.")
    button_row.addWidget(owner.clear_router_choice_code_button)
    button_row.addStretch(1)
    layout.addLayout(button_row)
    return group


def build_final_prompt_group(owner) -> QGroupBox:
    """Support build final prompt group behavior.
    
    Returns
    -------
    QGroupBox
        The qgroup box result.
    """
    
    group = QGroupBox("Complete prompt editor")
    group.setObjectName("prompt_router_reasoner_complete_prompt_editor_group")
    layout = QVBoxLayout(group)

    intro = QLabel(
        "The complete routed prompt appears here automatically after validation. "
        "You can edit it, save the edited version as an audit artifact, and copy "
        "it back to browser ChatGPT."
    )
    intro.setObjectName("prompt_router_reasoner_complete_prompt_editor_intro")
    intro.setWordWrap(True)
    layout.addWidget(intro)

    owner.manual_router_final_prompt_editor = QPlainTextEdit()
    owner.manual_router_final_prompt_editor.setObjectName("manual_router_final_prompt_editor")
    owner.manual_router_final_prompt_editor.setPlaceholderText(
        "Valid ChatGPT routing code will automatically load the complete prompt here."
    )
    owner.manual_router_final_prompt_editor.setReadOnly(False)
    layout.addWidget(owner.manual_router_final_prompt_editor, 1)

    button_row = QHBoxLayout()
    owner.edit_final_prompt_button = QPushButton("Edit")
    owner.edit_final_prompt_button.setObjectName("prompt_router_reasoner_edit_final_prompt_button")
    owner.edit_final_prompt_button.setToolTip("Enable editing and focus the complete prompt editor.")
    button_row.addWidget(owner.edit_final_prompt_button)

    owner.save_final_prompt_edit_button = QPushButton("Save edit")
    owner.save_final_prompt_edit_button.setObjectName(
        "prompt_router_reasoner_save_final_prompt_edit_button"
    )
    owner.save_final_prompt_edit_button.setEnabled(False)
    owner.save_final_prompt_edit_button.setToolTip(
        "Save the edited final prompt under prompt_router_reasoner_reviews/manual_router_choice_captures."
    )
    button_row.addWidget(owner.save_final_prompt_edit_button)

    owner.undo_final_prompt_edit_button = QPushButton("Undo")
    owner.undo_final_prompt_edit_button.setObjectName("prompt_router_reasoner_undo_final_prompt_edit_button")
    owner.undo_final_prompt_edit_button.setToolTip("Undo changes in the complete prompt editor.")
    button_row.addWidget(owner.undo_final_prompt_edit_button)

    owner.clear_final_prompt_button = QPushButton("Clear")
    owner.clear_final_prompt_button.setObjectName("prompt_router_reasoner_clear_final_prompt_button")
    owner.clear_final_prompt_button.setToolTip("Clear only the complete prompt editor.")
    button_row.addWidget(owner.clear_final_prompt_button)

    owner.copy_manual_router_final_prompt_button = QPushButton("Copy")
    owner.copy_manual_router_final_prompt_button.setObjectName(
        "prompt_router_reasoner_copy_manual_router_final_prompt_button"
    )
    owner.copy_manual_router_final_prompt_button.setEnabled(False)
    owner.copy_manual_router_final_prompt_button.setToolTip(
        "Copy the editable final prompt to paste back into browser ChatGPT."
    )
    button_row.addWidget(owner.copy_manual_router_final_prompt_button)
    button_row.addStretch(1)
    layout.addLayout(button_row)

    owner.saved_final_prompt_status_label = QLabel("Saved edit: none.")
    owner.saved_final_prompt_status_label.setObjectName(
        "prompt_router_reasoner_saved_final_prompt_status_label"
    )
    owner.saved_final_prompt_status_label.setWordWrap(True)
    layout.addWidget(owner.saved_final_prompt_status_label)
    return group
