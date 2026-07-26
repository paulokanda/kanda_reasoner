"""Validate Architecture Review Audit Copy Buttons v1."""
from __future__ import annotations

import ast
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-audit-copy-buttons-v1"
GUI_RELATIVE_PATH = Path("kanda_reasoner_app/manage_architecture/manage_architecture_gui.py")
PROTOCOL_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
)


def _fail(message: str) -> int:
    print(f"VALIDATION FAIL: {FEATURE_ID}")
    print(message)
    return 1


def main() -> int:
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    gui_path = project_root / GUI_RELATIVE_PATH
    protocol_path = project_root / PROTOCOL_RELATIVE_PATH
    if not gui_path.exists():
        return _fail(f"Missing GUI file: {GUI_RELATIVE_PATH}")
    if not protocol_path.exists():
        return _fail(f"Missing canonical protocol file: {PROTOCOL_RELATIVE_PATH}")
    text = gui_path.read_text(encoding="utf-8")
    protocol_text = protocol_path.read_text(encoding="utf-8")
    ast.parse(text)

    required_present = [
        "QAction('Clear Audit', self)",
        "QAction('Save Audit', self)",
        "QPushButton('Copy Audit')",
        "QPushButton('Large Module Creation/Refactor Protocol')",
        "QLabel('Audit')",
        "def copy_audit_to_clipboard(self) -> None:",
        "def copy_large_module_protocol_to_clipboard(self) -> None:",
        "def _large_module_protocol_path(self) -> Path | None:",
        "LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH",
        str(PROTOCOL_RELATIVE_PATH).replace("\\", "/"),
        "QApplication.clipboard().setText(audit_text)",
        "prompt_path.read_text(encoding='utf-8')",
        "Copied audit to clipboard",
        "Copied Large Module Creation/Refactor Protocol to clipboard",
    ]
    for needle in required_present:
        if needle not in text:
            return _fail(f"Missing expected GUI marker: {needle}")

    forbidden = [
        "QAction('Clear Output', self)",
        "QAction('Save Output', self)",
        "layout.addWidget(QLabel('Output'))",
        "Check the output panel for details.",
        "architecture_manager_output.txt",
    ]
    for needle in forbidden:
        if needle in text:
            return _fail(f"Forbidden old Output marker remains: {needle}")

    if "Version: 6.1" not in protocol_text:
        return _fail("Canonical large-module protocol is not Version: 6.1")
    if "Large Module Creation and Refactor Protocol" not in protocol_text:
        return _fail("Canonical large-module protocol title missing")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
