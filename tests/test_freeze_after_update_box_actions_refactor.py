"""Characterization tests for Freeze tab box-action mixin."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update.result import (
    FreezeAfterUpdateResult,
    FreezeAfterUpdateStatus,
)
from kanda_reasoner_app.freeze_after_update_gui._box_actions import FreezeBoxActionsMixin
from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
    FreezeAfterUpdateTab,
)


class _DummyLog:
    def __init__(self) -> None:
        self.text = ""
        self.cursor_moves: list[object] = []

    def append(self, message: str) -> None:
        self.text += str(message) + "\n"

    def toPlainText(self) -> str:
        return self.text

    def setPlainText(self, value: str) -> None:
        self.text = value

    def moveCursor(self, operation: object) -> None:
        self.cursor_moves.append(operation)


class _DummyButton:
    def __init__(self) -> None:
        self.enabled = False
        self.tooltip = ""

    def setEnabled(self, value: bool) -> None:
        self.enabled = value

    def setToolTip(self, value: str) -> None:
        self.tooltip = value


class _DummyLabel:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _DummyActions(FreezeBoxActionsMixin):
    def __init__(self) -> None:
        self.output_log = _DummyLog()
        self.status_label = _DummyLabel()
        self.box_folder_button = _DummyButton()
        self.external_ai_review_folder_button = _DummyButton()
        self.do_staged_action_button = _DummyButton()
        self.undo_staged_action_button = _DummyButton()
        self._last_output_folder = None
        self._pending_staged_project_root = None
        self._pending_staged_action = None


def test_box_actions_mixin_stays_below_facade_and_import_compatible() -> None:
    source = Path(sys.modules[FreezeBoxActionsMixin.__module__].__file__).read_text(encoding="utf-8")

    assert issubclass(FreezeAfterUpdateTab, FreezeBoxActionsMixin)
    assert "freeze_after_update_tab" not in source
    assert "__all__ = [\"FreezeBoxActionsMixin\"]" in source


def test_append_log_block_preserves_plain_text_order() -> None:
    dummy = _DummyActions()
    dummy.output_log.setPlainText("existing\n")

    dummy._append_log_block("next\nblock\n")

    assert dummy.output_log.toPlainText() == "existing\nnext\nblock\n"
    assert dummy.output_log.cursor_moves


def test_pending_staged_action_updates_buttons_and_state() -> None:
    dummy = _DummyActions()
    project_root = Path("E:/demo")

    dummy._set_pending_staged_action(project_root, "refresh_ai_compliance_package")

    assert dummy._pending_staged_project_root == project_root
    assert dummy._pending_staged_action == "refresh_ai_compliance_package"
    assert dummy.do_staged_action_button.enabled
    assert dummy.undo_staged_action_button.enabled

    dummy._set_pending_staged_action(None, None)

    assert dummy._pending_staged_project_root is None
    assert dummy._pending_staged_action is None
    assert not dummy.do_staged_action_button.enabled
    assert not dummy.undo_staged_action_button.enabled


def test_show_result_updates_status_log_and_folder_tooltips() -> None:
    dummy = _DummyActions()
    box_root = Path("E:/demo/project_freeze_after_update")
    result = FreezeAfterUpdateResult(
        status=FreezeAfterUpdateStatus.VALID,
        box_root=box_root,
        message="Freeze Feature After Update box is valid.",
        freeze_count=2,
    )

    dummy._show_result(result)

    assert dummy.status_label.text == "valid: Freeze Feature After Update box is valid."
    assert "Freeze entries included: 2" in dummy.output_log.toPlainText()
    assert str(box_root) in dummy.box_folder_button.tooltip
    assert "files_to_send_ai" in dummy.external_ai_review_folder_button.tooltip


def main() -> int:
    test_box_actions_mixin_stays_below_facade_and_import_compatible()
    test_append_log_block_preserves_plain_text_order()
    test_pending_staged_action_updates_buttons_and_state()
    test_show_result_updates_status_log_and_folder_tooltips()
    print("VALIDATION OK: freeze-after-update-box-actions-refactor")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
