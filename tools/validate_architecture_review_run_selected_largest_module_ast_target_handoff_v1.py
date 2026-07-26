"""Validate Run Selected Mode largest-module handoff into AST Split Audit."""
from __future__ import annotations

import ast
from pathlib import Path
import sys
import types

__all__ = [
    "main",
]

FEATURE_ID = "architecture-review-run-selected-largest-module-ast-target-handoff-v1"
ROOT = Path(__file__).resolve().parents[1]
GUI_REL = Path("kanda_reasoner_app/manage_architecture/large_module_split_audit_gui.py")
SUBTABS_REL = Path("kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py")
TOUCHED_SOURCE = (GUI_REL, SUBTABS_REL)


def require(condition: bool, marker: str) -> None:
    """Print one PASS marker or fail validation."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def install_import_stubs() -> None:
    """Install minimal GUI stubs so the real mixin can be imported headlessly."""
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    for name in ("QApplication", "QFileDialog", "QMessageBox"):
        setattr(qtwidgets, name, type(name, (), {}))
    pyside = types.ModuleType("PySide6")
    pyside.__path__ = []
    pyside.QtWidgets = qtwidgets
    sys.modules.setdefault("PySide6", pyside)
    sys.modules.setdefault("PySide6.QtWidgets", qtwidgets)

    floating = types.ModuleType("kanda_reasoner_app.templates.floating_windows")
    floating.show_auto_close_action_window = lambda *args, **kwargs: None
    floating.show_error_copy_close_window = lambda *args, **kwargs: None
    sys.modules["kanda_reasoner_app.templates.floating_windows"] = floating


class FakeEdit:
    """Small line-edit substitute for focused mixin validation."""

    def __init__(self) -> None:
        self.value = ""
        self.placeholder = ""

    def text(self) -> str:
        return self.value

    def setText(self, value: str) -> None:
        self.value = value

    def clear(self) -> None:
        self.value = ""

    def setPlaceholderText(self, value: str) -> None:
        self.placeholder = value


class FakeOutput:
    """Small plain-text output substitute."""

    def __init__(self, text: str) -> None:
        self.value = text

    def toPlainText(self) -> str:
        return self.value


class FakeStatus:
    """Capture the most recent status message."""

    def __init__(self) -> None:
        self.message = ""

    def showMessage(self, value: str) -> None:
        self.message = value


def build_fake_window(mixin: type, text: str) -> object:
    """Return one focused fake Architecture Review window."""

    class FakeWindow(mixin):
        def __init__(self) -> None:
            self._output = FakeOutput(text)
            self._large_module_target_edit = FakeEdit()
            self._large_module_targets = []
            self._large_module_target_index = -1
            self._large_module_target_source = "none"
            self._last_large_module_split_handoff = ""
            self._status = FakeStatus()

        def statusBar(self) -> FakeStatus:
            return self._status

        def _clear_large_module_split_output(self) -> None:
            self._split_output_cleared = True

        def _sync_large_module_target_controls(self) -> None:
            self._controls_synced = True

    return FakeWindow()


def validate_functional_handoff() -> None:
    """Exercise the real handoff mixin against ordered and manual target cases."""
    install_import_stubs()
    from kanda_reasoner_app.manage_architecture.large_module_split_audit_gui import (
        LargeModuleSplitAuditGuiMixin,
    )

    output = """ARCHITECTURE VALIDATION SUMMARY
DETAILS
WARNING MODULE_TOO_LARGE pkg/small.py :: Module has 600 lines; split threshold is 500.
WARNING MODULE_TOO_LARGE pkg/largest.py :: Module has 1200 lines; split threshold is 500.
WARNING MODULE_TOO_LARGE pkg/mid.py :: Module has 800 lines; split threshold is 500.
"""
    window = build_fake_window(LargeModuleSplitAuditGuiMixin, output)
    changed = window._sync_largest_module_target_from_latest_run_results()
    require(changed is True, "AST_SUBTAB_HANDOFF_TRIGGERED")
    require(
        window._large_module_target_edit.text() == "pkg/largest.py",
        "RUN_SELECTED_LARGEST_MODULE_POPULATES_TARGET",
    )
    require(
        [item.path for item in window._large_module_targets]
        == ["pkg/largest.py", "pkg/mid.py", "pkg/small.py"],
        "AUDIT_QUEUE_REMAINS_LARGEST_FIRST",
    )

    window._large_module_target_source = "manual"
    window._large_module_target_edit.setText("pkg/mid.py")
    changed = window._sync_largest_module_target_from_latest_run_results()
    require(changed is False, "MANUAL_TARGET_PRESERVED_FOR_SAME_RUN")
    require(
        window._large_module_target_edit.text() == "pkg/mid.py",
        "MANUAL_TARGET_NOT_OVERWRITTEN_ON_REOPEN",
    )

    window._reset_large_module_target_state_for_new_project_audit_run("scan")
    window._output.value = output
    changed = window._sync_largest_module_target_from_latest_run_results()
    require(changed is True, "NEW_RUN_REARMS_AST_HANDOFF")
    require(
        window._large_module_target_edit.text() == "pkg/largest.py",
        "NEW_RUN_REINSERTS_LARGEST_MODULE_CARD",
    )


def validate_static_wiring() -> None:
    """Prove the AST subtab activation hook and touched module size policy."""
    gui_text = (ROOT / GUI_REL).read_text(encoding="utf-8")
    subtabs_text = (ROOT / SUBTABS_REL).read_text(encoding="utf-8")
    require(
        "def _sync_largest_module_target_from_latest_run_results" in gui_text,
        "LARGEST_MODULE_HANDOFF_OWNER_PRESENT",
    )
    require(
        "if index == 1:" in subtabs_text
        and '"_sync_largest_module_target_from_latest_run_results"' in subtabs_text,
        "AST_SUBTAB_OPEN_SYNCS_LATEST_RUN_RESULTS",
    )
    for rel in TOUCHED_SOURCE:
        source = (ROOT / rel).read_text(encoding="utf-8")
        ast.parse(source, filename=str(rel))
        if len(source.splitlines()) > 500:
            raise AssertionError(f"TOUCHED_MODULE_TOO_LARGE:{rel}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run focused functional and static validation."""
    validate_functional_handoff()
    validate_static_wiring()
    print("CARD_MACHINE_LARGEST_MODULE_HANDOFF: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
