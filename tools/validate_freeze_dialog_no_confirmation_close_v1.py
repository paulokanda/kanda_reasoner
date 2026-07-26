# project-path: tools/validate_freeze_dialog_no_confirmation_close_v1.py
"""Focused validator for Local Freeze dialog no-confirmation close behavior."""
from __future__ import annotations

import py_compile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "freeze-dialog-no-confirmation-close-v1"
TOUCHED = [
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py",
    "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py",
    "kanda_reasoner_app/freeze_after_update_gui/local_freeze_confirmation_binding.py",
]


def _read(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"Missing expected file: {relative_path}")
    return path.read_text(encoding="utf-8")


def _line_count(relative_path: str) -> int:
    return len(_read(relative_path).splitlines())


def _function_block(source: str, marker: str, next_marker: str) -> str:
    start = source.index(marker)
    end = source.index(next_marker, start)
    return source[start:end]


def _validate_line_counts() -> None:
    for relative_path in TOUCHED + ["tools/validate_freeze_dialog_no_confirmation_close_v1.py"]:
        count = _line_count(relative_path)
        if count > 500:
            raise AssertionError(f"{relative_path} has {count} lines; expected <= 500")


def _validate_compile() -> None:
    for relative_path in TOUCHED + ["tools/validate_freeze_dialog_no_confirmation_close_v1.py"]:
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def _validate_ignore_freeze_closes_without_question(tab_source: str) -> None:
    block = _function_block(
        tab_source,
        "        def ignore_this_freeze() -> None:",
        "        def confirm_and_write_local_freeze() -> None:",
    )
    forbidden = [
        "QMessageBox.question",
        "Continue?",
        "Ignore this freeze",
        "cancelled by human",
        "reply =",
    ]
    for token in forbidden:
        if token in block:
            raise AssertionError(f"Ignore this Freeze still contains confirmation token: {token}")
    if "mark_latest_freeze_hint_used(" not in block or 'freeze_id="ignored-by-human"' not in block:
        raise AssertionError("Ignore this Freeze must still mark the current freeze hint as ignored/used")
    if "dialog.close()" not in block:
        raise AssertionError("Ignore this Freeze must close the local freeze dialog immediately")


def _validate_confirm_write_closes_without_question(tab_source: str) -> None:
    block = _function_block(
        tab_source,
        "        def confirm_and_write_local_freeze() -> None:",
        "        widgets.copy_to_ai_button.clicked.connect",
    )
    forbidden = [
        "QMessageBox.question",
        "Confirm local freeze write",
        "WILL WRITE:",
        "Continue?",
        "show_auto_close_action_window",
        "Local freeze written; AI compliance refresh warning",
        "show_error_copy_close_window(self, title='Local freeze write failed'",
    ]
    for token in forbidden:
        if token in block:
            raise AssertionError(f"Confirm and Write still contains popup/confirmation token: {token}")
    if "write_confirmed_freeze_entry(" not in block or "confirmation=True" not in block:
        raise AssertionError("Confirm and Write must still write through the confirmed freeze entry contract")
    if block.count("dialog.close()") < 3:
        raise AssertionError("Confirm and Write must close immediately on missing preview, write failure, and final completion")
    if "refresh_ai_compliance_context(project_root)" not in block:
        raise AssertionError("Confirm and Write must still refresh AI compliance context after a successful write")
    if "Local freeze write skipped: no valid preview was available." not in block:
        raise AssertionError("Missing-preview path must log and close instead of showing a popup")


def _validate_cancel_direct_close(tab_source: str) -> None:
    if "cancel_button.clicked.connect(dialog.close)" not in tab_source:
        raise AssertionError("Cancel must directly close the local freeze dialog")


def _validate_copy_mentions_button_click_is_confirmation(widgets_source: str, tab_source: str, binding_source: str) -> None:
    if "Confirm and Write still requires human confirmation" in widgets_source:
        raise AssertionError("Dialog intro still claims a separate human confirmation is required")
    if "closes immediately" not in widgets_source:
        raise AssertionError("Dialog intro must mention immediate close behavior")
    combined = tab_source + binding_source
    if not ("Write this validated local freeze entry" in combined and "immediately." in combined):
        raise AssertionError("Confirm button tooltip must describe immediate close behavior")


def main() -> int:
    _validate_line_counts()
    _validate_compile()
    tab_source = _read("kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py")
    runtime_source = _read("kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py")
    widgets_source = _read("kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_widgets.py")
    _validate_ignore_freeze_closes_without_question(runtime_source)
    _validate_confirm_write_closes_without_question(runtime_source)
    _validate_cancel_direct_close(runtime_source)
    binding_source = _read("kanda_reasoner_app/freeze_after_update_gui/local_freeze_confirmation_binding.py")
    _validate_copy_mentions_button_click_is_confirmation(widgets_source, runtime_source, binding_source)
    if "FreezeLocalEntryRuntimeMixin" not in tab_source:
        raise AssertionError("Freeze tab must delegate dialog behavior to the bounded runtime mixin")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
