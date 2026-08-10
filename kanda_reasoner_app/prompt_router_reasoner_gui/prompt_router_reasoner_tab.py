# project-path: kanda_reasoner_app/prompt_router_reasoner_gui/prompt_router_reasoner_tab.py
"""Simplified Prompt Router Reasoner manual round-trip tab.

This tab is intentionally narrow: browser ChatGPT emits a KANDA_ROUTING_CHOICE
block, the user pastes it here, KANDA validates prompt_code/prompt_id/path,
loads canonical ACTIVE_PROMPTS text, and shows one editable final prompt for
copy/paste back to ChatGPT.

It deliberately removes the previous heuristic-vs-ML review workspace from the
visible UI. ML remains sleeping and outside the critical path.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication, QFrame, QGroupBox, QWidget

from kanda_reasoner_app.external_ai_workflow import (
    handoff_to_selected_external_ai,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_manual_router_choice_capture import (
    ManualRouterChoiceCaptureError,
    capture_manual_router_choice,
    sha256_text,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_models import REVIEW_FOLDER_NAME

from ._prompt_router_reasoner_tab_ui import (
    build_final_prompt_group as _build_final_prompt_group_ui,
    build_header as _build_header_ui,
    build_manual_code_group as _build_manual_code_group_ui,
    build_tab_ui as _build_tab_ui,
    create_auto_capture_timer as _create_auto_capture_timer,
)

__all__ = [
    "PROMPT_ROUTER_REASONER_TAB_TITLE",
    "PromptRouterReasonerTab",
    "PromptRouterReasonerTabContract",
]

PROMPT_ROUTER_REASONER_TAB_TITLE = "Prompt Router Reasoner"
MANUAL_ROUTER_CHOICE_MODE = "manual_router_choice_capture"


@dataclass(frozen=True)
class PromptRouterReasonerTabContract:
    """Static contract exposed for regression tests and future wiring."""

    tab_title: str
    default_router_mode: str
    ml_mode_locked: bool
    has_three_columns: bool
    has_review_controls: bool
    has_ask_ai_button: bool
    has_readiness_bars: bool
    wired_to_runtime_router: bool
    has_manual_code_editor: bool = True
    has_manual_final_prompt_editor: bool = True
    manual_capture_auto_loads: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable description of this simplified tab."""
        return {
            "tab_title": self.tab_title,
            "default_router_mode": self.default_router_mode,
            "ml_mode_locked": self.ml_mode_locked,
            "has_three_columns": self.has_three_columns,
            "has_review_controls": self.has_review_controls,
            "has_ask_ai_button": self.has_ask_ai_button,
            "has_readiness_bars": self.has_readiness_bars,
            "wired_to_runtime_router": self.wired_to_runtime_router,
            "has_manual_code_editor": self.has_manual_code_editor,
            "has_manual_final_prompt_editor": self.has_manual_final_prompt_editor,
            "manual_capture_auto_loads": self.manual_capture_auto_loads,
        }


class PromptRouterReasonerTab(QWidget):
    """Minimal manual prompt-routing round-trip workspace.

    The visible workflow has two editors only:

    1. ChatGPT router-choice code editor, with Paste/Clear/Undo.
    2. Editable final prompt editor, with Edit/Save/Clear/Undo/Copy.

    It does not show global router mode, generator review queue, heuristic prompt
    selector, ML selector, Ask AI controls, or readiness bars.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        parent : QWidget | None, optional
            The optional parent value.
        """
        
        super().__init__(parent)
        self.setObjectName("PromptRouterReasonerTab")
        self._project_root: Path | None = None
        self._last_loaded_code_hash = ""
        self._last_saved_final_prompt_path = ""
        self._last_manual_router_choice_capture_result: dict[str, Any] = {
            "ok": False,
            "status_text": "No manual router choice captured yet.",
            "metric_excluded": True,
            "ml_sleeping": True,
            "ui_mode": MANUAL_ROUTER_CHOICE_MODE,
        }
        self._auto_capture_timer = _create_auto_capture_timer(
            self,
            self._auto_load_manual_router_choice_from_editor,
        )
        self._build_ui()

    @staticmethod
    def contract() -> PromptRouterReasonerTabContract:
        """Return the simplified manual-router-choice tab contract."""
        return PromptRouterReasonerTabContract(
            tab_title=PROMPT_ROUTER_REASONER_TAB_TITLE,
            default_router_mode=MANUAL_ROUTER_CHOICE_MODE,
            ml_mode_locked=True,
            has_three_columns=False,
            has_review_controls=False,
            has_ask_ai_button=False,
            has_readiness_bars=False,
            wired_to_runtime_router=False,
            has_manual_code_editor=True,
            has_manual_final_prompt_editor=True,
            manual_capture_auto_loads=True,
        )

    def get_declared_router_modes(self) -> tuple[str, ...]:
        """Return the single visible workflow mode.

        Previous global router-mode buttons were intentionally removed from the
        tab UI. ML remains unavailable from this simplified workspace.
        """
        return (MANUAL_ROUTER_CHOICE_MODE,)

    def is_ml_pilot_control_locked(self) -> bool:
        """Return True because ML controls are not visible or actionable here."""
        return True

    def _build_ui(self) -> None:
        """Build the visible Prompt Router workspace through the private UI owner."""
        _build_tab_ui(self)
    def _build_header(self) -> QWidget:
        """Build the header while preserving the private compatibility method."""
        return _build_header_ui(self, PROMPT_ROUTER_REASONER_TAB_TITLE)
    def _build_manual_code_group(self) -> QGroupBox:
        """Build manual code controls through the private UI owner."""
        return _build_manual_code_group_ui(self)
    def _build_final_prompt_group(self) -> QGroupBox:
        """Build final prompt controls through the private UI owner."""
        return _build_final_prompt_group_ui(self)

    @Slot(str)
    def on_project_root_edit_textChanged(self, text: str) -> None:  # noqa: N802
        self._on_project_root_text_changed(text)

    @Slot()
    def on_manual_router_choice_code_editor_textChanged(self) -> None:  # noqa: N802
        self._schedule_auto_capture()

    @Slot()
    def on_prompt_router_reasoner_paste_router_choice_code_button_clicked(self) -> None:
        self.paste_manual_router_choice_code()

    @Slot()
    def on_prompt_router_reasoner_undo_router_choice_code_button_clicked(self) -> None:
        self.manual_router_choice_code_editor.undo()

    @Slot()
    def on_prompt_router_reasoner_clear_router_choice_code_button_clicked(self) -> None:
        self.clear_manual_router_choice_code()

    @Slot()
    def on_manual_router_final_prompt_editor_textChanged(self) -> None:  # noqa: N802
        self._on_final_prompt_text_changed()

    @Slot()
    def on_prompt_router_reasoner_edit_final_prompt_button_clicked(self) -> None:
        self.enable_final_prompt_editing()

    @Slot()
    def on_prompt_router_reasoner_save_final_prompt_edit_button_clicked(self) -> None:
        self.save_manual_router_final_prompt_edit()

    @Slot()
    def on_prompt_router_reasoner_undo_final_prompt_edit_button_clicked(self) -> None:
        self.manual_router_final_prompt_editor.undo()

    @Slot()
    def on_prompt_router_reasoner_clear_final_prompt_button_clicked(self) -> None:
        self.clear_manual_router_final_prompt()

    @Slot()
    def on_prompt_router_reasoner_copy_manual_router_final_prompt_button_clicked(self) -> None:
        self.copy_manual_router_final_prompt()

    def _schedule_auto_capture(self) -> None:
        """Debounce code-paste validation so a pasted block autoloads once."""
        self._auto_capture_timer.start(450)

    def _auto_load_manual_router_choice_from_editor(self) -> None:
        """Auto-validate pasted code and populate the final prompt editor."""
        code_text = self.manual_router_choice_code_editor.toPlainText()
        if not code_text.strip():
            self._last_loaded_code_hash = ""
            self._last_manual_router_choice_capture_result = {
                "ok": False,
                "status_text": "Manual capture status: waiting for ChatGPT KANDA_ROUTING_CHOICE code.",
                "metric_excluded": True,
                "ml_sleeping": True,
                "ui_mode": MANUAL_ROUTER_CHOICE_MODE,
            }
            self.manual_router_choice_status_label.setText(
                "Manual capture status: waiting for ChatGPT KANDA_ROUTING_CHOICE code."
            )
            self._set_final_prompt_actions_enabled(False)
            return

        code_hash = sha256_text(code_text)
        if code_hash == self._last_loaded_code_hash:
            return

        result = self.validate_and_load_manual_router_choice()
        if result.get("ok"):
            self._last_loaded_code_hash = code_hash
        else:
            self._last_loaded_code_hash = ""

    def paste_manual_router_choice_code(self) -> None:
        """Paste router-choice code from the clipboard and trigger autoload."""
        self.manual_router_choice_code_editor.setPlainText(QApplication.clipboard().text())
        self._auto_load_manual_router_choice_from_editor()

    def clear_manual_router_choice_code(self) -> None:
        """Clear the ChatGPT-code editor and its loaded final prompt."""
        self._auto_capture_timer.stop()
        self.manual_router_choice_code_editor.clear()
        self.manual_router_final_prompt_editor.clear()
        self._last_loaded_code_hash = ""
        self._last_saved_final_prompt_path = ""
        self._last_manual_router_choice_capture_result = {
            "ok": False,
            "status_text": "Manual capture status: cleared.",
            "metric_excluded": True,
            "ml_sleeping": True,
            "ui_mode": MANUAL_ROUTER_CHOICE_MODE,
        }
        self._set_final_prompt_actions_enabled(False)
        self.saved_final_prompt_status_label.setText("Saved edit: none.")
        self.manual_router_choice_status_label.setText("Manual capture status: cleared.")

    def clear_manual_router_final_prompt(self) -> None:
        """Clear only the editable complete-prompt window."""
        self.manual_router_final_prompt_editor.clear()
        self._set_final_prompt_actions_enabled(False)
        self.manual_router_choice_status_label.setText("Complete prompt editor cleared.")

    def enable_final_prompt_editing(self) -> None:
        """Keep final prompt editor editable and focus it."""
        self.manual_router_final_prompt_editor.setReadOnly(False)
        self.manual_router_final_prompt_editor.setFocus(Qt.OtherFocusReason)
        self.manual_router_choice_status_label.setText("Edit mode enabled for complete prompt editor.")

    def validate_and_load_manual_router_choice(self) -> dict[str, Any]:
        """Validate pasted browser routing choice and load canonical prompt text."""
        project_root = self._project_root_from_field()
        if project_root is None:
            result = {
                "ok": False,
                "error": "project root missing",
                "status_text": "Manual capture failed: project root is missing.",
                "metric_excluded": True,
                "ml_sleeping": True,
                "ui_mode": MANUAL_ROUTER_CHOICE_MODE,
            }
            self._last_manual_router_choice_capture_result = dict(result)
            self.manual_router_choice_status_label.setText(str(result["status_text"]))
            self.manual_router_final_prompt_editor.clear()
            self._set_final_prompt_actions_enabled(False)
            return result

        try:
            result = capture_manual_router_choice(
                project_root,
                self.manual_router_choice_code_editor.toPlainText(),
            )
        except (ManualRouterChoiceCaptureError, OSError, ValueError) as exc:
            result = {
                "ok": False,
                "error": str(exc),
                "status_text": "Manual capture failed: " + str(exc),
                "metric_excluded": True,
                "ml_sleeping": True,
                "ui_mode": MANUAL_ROUTER_CHOICE_MODE,
            }
            self._last_manual_router_choice_capture_result = dict(result)
            self.manual_router_choice_status_label.setText(str(result["status_text"]))
            self.manual_router_final_prompt_editor.clear()
            self._set_final_prompt_actions_enabled(False)
            return result

        result = dict(result)
        result["ui_mode"] = MANUAL_ROUTER_CHOICE_MODE
        result["status_text"] = (
            "Manual capture OK: complete prompt loaded automatically from canonical ACTIVE_PROMPTS. "
            "ML remains sleeping; metrics excluded."
        )
        self._last_manual_router_choice_capture_result = dict(result)
        self.manual_router_final_prompt_editor.setPlainText(str(result.get("assembled_prompt", "")))
        self._set_final_prompt_actions_enabled(True)
        self.saved_final_prompt_status_label.setText("Saved edit: none.")
        self.manual_router_choice_status_label.setText(str(result["status_text"]))
        return dict(result)

    def _set_final_prompt_actions_enabled(self, enabled: bool) -> None:
        """Support set final prompt actions enabled behavior.
        
        Parameters
        ----------
        enabled : bool
            The enabled value.
        """
        
        self.copy_manual_router_final_prompt_button.setEnabled(enabled)
        self.save_final_prompt_edit_button.setEnabled(enabled)

    def _on_final_prompt_text_changed(self) -> None:
        """Support on final prompt text changed behavior.
        """
        
        has_text = bool(self.manual_router_final_prompt_editor.toPlainText().strip())
        self._set_final_prompt_actions_enabled(has_text)

    def copy_manual_router_final_prompt(self) -> None:
        """Copy the editable final prompt and open the selected external AI."""
        prompt_text = self.manual_router_final_prompt_editor.toPlainText()
        if not prompt_text.strip():
            self.manual_router_choice_status_label.setText("No complete prompt text to copy.")
            self.copy_manual_router_final_prompt_button.setEnabled(False)
            return
        handoff = handoff_to_selected_external_ai(prompt_text)
        self.manual_router_choice_status_label.setText(
            "External AI handoff: "
            + (handoff.display_name if handoff.ok else handoff.error)
            + ". Stored prompts and router state unchanged."
        )

    def save_manual_router_final_prompt_edit(self) -> dict[str, Any]:
        """Save the edited final prompt as a project-local audit artifact only."""
        project_root = self._project_root_from_field()
        prompt_text = self.manual_router_final_prompt_editor.toPlainText()
        if project_root is None:
            result = {"ok": False, "error": "project root missing"}
            self.saved_final_prompt_status_label.setText("Save failed: project root missing.")
            return result
        if not prompt_text.strip():
            result = {"ok": False, "error": "final prompt text is empty"}
            self.saved_final_prompt_status_label.setText("Save failed: final prompt text is empty.")
            return result

        capture_id = str(self._last_manual_router_choice_capture_result.get("capture_id") or "manual")
        safe_capture_id = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in capture_id)
        save_dir = project_root / REVIEW_FOLDER_NAME / "manual_router_choice_captures" / "edited_final_prompts"
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / (safe_capture_id + "_edited_final_prompt.md")
        save_path.write_text(prompt_text, encoding="utf-8")

        self._last_saved_final_prompt_path = str(save_path)
        result = {
            "ok": True,
            "saved_path": str(save_path),
            "metric_excluded": True,
            "ml_sleeping": True,
            "ui_mode": MANUAL_ROUTER_CHOICE_MODE,
        }
        self.saved_final_prompt_status_label.setText("Saved edit: " + str(save_path))
        self.manual_router_choice_status_label.setText("Saved edited complete prompt as audit artifact only.")
        return result

    def get_manual_router_choice_capture_state(self) -> dict[str, Any]:
        """Return simplified manual capture GUI state for validation tests."""
        return {
            "last_result": dict(self._last_manual_router_choice_capture_result),
            "code_text_length": len(self.manual_router_choice_code_editor.toPlainText()),
            "final_prompt_length": len(self.manual_router_final_prompt_editor.toPlainText()),
            "copy_enabled": self.copy_manual_router_final_prompt_button.isEnabled(),
            "save_enabled": self.save_final_prompt_edit_button.isEnabled(),
            "status_text": self.manual_router_choice_status_label.text(),
            "saved_final_prompt_path": self._last_saved_final_prompt_path,
            "router_with_ml_locked": True,
            "metric_excluded": True,
            "ml_sleeping": True,
            "ui_mode": MANUAL_ROUTER_CHOICE_MODE,
            "removed_global_router_mode_group": True,
            "removed_generator_text_review_queue_group": True,
            "removed_heuristic_selector_group": True,
            "removed_ml_selector_group": True,
        }

    def set_project_root(self, project_root: str | Path | None) -> None:
        """Set the project root for manual prompt-code resolution."""
        if project_root is None or str(project_root).strip() == "":
            self._project_root = None
            self.project_root_edit.clear()
            self.manual_router_choice_status_label.setText("Project root cleared.")
            return

        resolved = Path(project_root).expanduser().resolve()
        self._project_root = resolved
        root_text = str(resolved)
        if self.project_root_edit.text() != root_text:
            self.project_root_edit.setText(root_text)
        else:
            self._on_project_root_text_changed(root_text)

    def refresh_runtime_capture_visibility(self) -> None:
        """Compatibility no-op: old review-queue refresh was intentionally removed."""
        self.manual_router_choice_status_label.setText(
            "Review queue removed. Paste ChatGPT KANDA_ROUTING_CHOICE code to load a prompt."
        )

    def refresh_review_list(self) -> None:
        """Compatibility no-op: old generator text review queue was removed."""
        self.refresh_runtime_capture_visibility()

    def apply_review_filter(self) -> None:
        """Compatibility no-op: review filters were removed with the review queue."""
        self.refresh_runtime_capture_visibility()

    def refresh_stats_panel(self) -> None:
        """Compatibility no-op: heuristic/ML readiness bars were removed."""
        self.refresh_runtime_capture_visibility()

    def timerEvent(self, event: Any) -> None:  # noqa: N802 - Qt override name
        """Dispatch owner timer events to the bounded debounce controller."""
        if self._auto_capture_timer.handle_timer_event(event):
            return
        super().timerEvent(event)

    def showEvent(self, event: Any) -> None:  # noqa: N802 - Qt override name
        """Qt hook kept deliberately inert; no review queue auto-refresh remains."""
        try:
            super().showEvent(event)
        except Exception:
            pass

    def _on_project_root_text_changed(self, text: str) -> None:
        """Support on project root text changed behavior.
        
        Parameters
        ----------
        text : str
            The text value.
        """
        
        candidate = str(text or "").strip()
        if not candidate:
            self._project_root = None
            return
        self._project_root = Path(candidate).expanduser().resolve()
        if self.manual_router_choice_code_editor.toPlainText().strip():
            self._schedule_auto_capture()

    def _project_root_from_field(self) -> Path | None:
        """Support project root from field behavior.
        
        Returns
        -------
        Path | None
            The resolved path.
        """
        
        if self._project_root is not None:
            return self._project_root
        text = self.project_root_edit.text().strip()
        if not text:
            return None
        self._project_root = Path(text).expanduser().resolve()
        return self._project_root

    @staticmethod
    def _vertical_separator() -> QFrame:
        """Return a separator kept for compatibility with older code/tests."""
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        return line
