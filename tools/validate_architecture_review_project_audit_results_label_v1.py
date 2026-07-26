# project-path: tools/validate_architecture_review_project_audit_results_label_v1.py
"""Validate Architecture Review Project Audit Results Label v1."""
from __future__ import annotations

import ast
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-project-audit-results-label-v1"
GUI_RELATIVE_PATH = Path("kanda_reasoner_app/manage_architecture/manage_architecture_gui.py")
PROTOCOL_RELATIVE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
)


def _fail(message: str) -> int:
    """Support fail behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    
    Returns
    -------
    int
        The integer result.
    """
    
    print(f"VALIDATION FAIL: {FEATURE_ID}")
    print(message)
    return 1


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
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

    required = [
        "QAction('Clear Audit Results', self)",
        "QAction('Save Audit Results', self)",
        "self._run_button = QPushButton('Run Selected Mode')",
        "self._run_button.setStyleSheet('color: #008000; font-weight: bold;')",
        "self._audit_results_label = QLabel('Project Audit Results')",
        "self._audit_results_label.setStyleSheet('color: #000000; font-weight: bold;')",
        "audit_header.addWidget(self._audit_results_label)",
        "QPushButton('Copy Audit Results')",
        "QPushButton('Large Module Creation/Refactor Protocol')",
        "def copy_audit_to_clipboard(self) -> None:",
        "QApplication.clipboard().setText(audit_text)",
        "Copied Project Audit Results to clipboard",
        "def copy_large_module_protocol_to_clipboard(self) -> None:",
        "prompt_path.read_text(encoding='utf-8')",
    ]
    for needle in required:
        if needle not in text:
            return _fail(f"Missing expected GUI marker: {needle}")

    forbidden = [
        "QAction('Clear Audit', self)",
        "QAction('Save Audit', self)",
        "QPushButton('Copy Audit')",
        "QLabel('Audit')",
        "Copied audit to clipboard",
        "border: 1px solid #2E7D32;",
    ]
    for needle in forbidden:
        if needle in text:
            return _fail(f"Old Audit-only marker remains: {needle}")

    label_index = text.find("self._audit_results_label = QLabel('Project Audit Results')")
    copy_index = text.find("self._copy_audit_btn = QPushButton('Copy Audit Results')")
    protocol_index = text.find("self._copy_large_module_protocol_btn = QPushButton('Large Module Creation/Refactor Protocol')")
    if not (0 <= label_index < copy_index < protocol_index):
        return _fail("Project Audit Results label must appear before the copy/protocol buttons.")

    mover_index = text.find("def move_project_root_controls_to_layout(")
    if mover_index < 0:
        return _fail("Architecture Review host-row mover is missing.")
    browse_move_index = text.find("destination_layout.insertWidget(insert_index + 3, self._browse_root_btn, 0)", mover_index)
    audit_move_index = text.find("destination_layout.insertWidget(insert_index + 5, self._audit_results_label, 0)", mover_index)
    copy_move_index = text.find("destination_layout.insertWidget(insert_index + 6, self._copy_audit_btn, 0)", mover_index)
    protocol_move_index = text.find(
        "destination_layout.insertWidget(insert_index + 7, self._copy_large_module_protocol_btn, 0)",
        mover_index,
    )
    if not (0 <= browse_move_index < audit_move_index < copy_move_index < protocol_move_index):
        return _fail("Project Audit Results controls must move into the host LOADED row to the right of Browse.")

    run_button_index = text.find("self._run_button = QPushButton('Run Selected Mode')")
    validate_button_index = text.find("for mode in ('validate', 'diff', 'scan', 'write'):")
    run_options_label_index = text.find("self._run_options_toolbar_label = QLabel('Run options')")
    mode_label_index = text.find("self._mode_toolbar_label = QLabel('Mode')")
    if not (0 <= run_button_index < validate_button_index < run_options_label_index < mode_label_index):
        return _fail("Run Selected Mode / Validate / Diff / Scan / Write group must be left of Run options / Mode.")
    if "buttons.addWidget(self._run_button)" in text:
        return _fail("Run Selected Mode button still appears in the body button row.")

    if "Version: 7.0" not in protocol_text:
        return _fail("Canonical large-module protocol is not Version: 7.0")
    for needle in [
        "AST-assisted heuristic split audit",
        "Multi-Island Execution Layer",
        "Patch-train delivery bundle",
        "install -> validate -> freeze",
    ]:
        if needle not in protocol_text:
            return _fail(f"Canonical large-module protocol missing v7.0 marker: {needle}")
    if "Large Module Creation and Refactor Protocol" not in protocol_text:
        return _fail("Canonical large-module protocol title missing")

    for needle in [
        "QPushButton('Run AST Split Audit')",
        "QPushButton('Copy Split Handoff for AI')",
        "run_large_module_split_audit",
    ]:
        if needle not in text:
            return _fail(f"Architecture Review missing v7.0 AST split-audit marker: {needle}")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
