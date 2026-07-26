"""Validate the Error Memory canonical delivery prompt copy button."""
from __future__ import annotations

import argparse
import os
import py_compile
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "error-memory-get-correct-way-to-send-errors-button-v1"
PROMPT_RELATIVE = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/error_memory_ai_formulary_startup_canon.md"
)
TAB_RELATIVE = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
BLUEPRINT_RELATIVE = Path(
    "kanda_reasoner_app/error_memory_gui/_intake_blueprint.py"
)
CLIPBOARD_RELATIVE = Path(
    "kanda_reasoner_app/error_memory_gui/_clipboard_export.py"
)
ROUTER_RELATIVE = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "02_prompt_routing_and_indexing/prompt_router.md"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _read(path: Path) -> str:
    _require(path.exists() and path.is_file(), f"Required file missing: {path}")
    return path.read_text(encoding="utf-8")


def _validate_sources(project_root: Path) -> tuple[str, str]:
    tab_path = project_root / TAB_RELATIVE
    blueprint_path = project_root / BLUEPRINT_RELATIVE
    clipboard_path = project_root / CLIPBOARD_RELATIVE
    prompt_path = project_root / PROMPT_RELATIVE
    router_path = project_root / ROUTER_RELATIVE

    tab_text = _read(tab_path)
    blueprint_text = _read(blueprint_path)
    clipboard_text = _read(clipboard_path)
    prompt_text = _read(prompt_path)
    router_text = _read(router_path)

    _require(
        "QPushButton('Get correct way to send me errors')" in tab_text,
        "Required button label is missing.",
    )
    _require(
        "setStyleSheet('color: #FF8C00; font-weight: bold;')" in tab_text,
        "Required bold orange button style is missing.",
    )
    second_path_add = (
        "path_action_row.addWidget(self.copy_second_prompt_path_button)"
    )
    canon_button_add = (
        "path_action_row.addWidget(self.copy_correct_error_delivery_button)"
    )
    _require(second_path_add in tab_text, "Second Prompt path button row wiring missing.")
    _require(canon_button_add in tab_text, "Canonical delivery button row wiring missing.")
    _require(
        tab_text.index(second_path_add) < tab_text.index(canon_button_add),
        "Canonical delivery button is not after Get path to Second Prompt Files.",
    )
    _require(
        "copy_correct_error_delivery_canon_to_clipboard(self)" in tab_text,
        "Button click is not wired to canonical prompt clipboard delivery.",
    )
    _require(
        "01_session_start_and_navigation/error_memory_ai_formulary_startup_canon.md"
        in blueprint_text,
        "Canonical prompt relative path is missing from Error Memory resolver.",
    )
    _require(
        "read_error_memory_ai_formulary_canon" in clipboard_text,
        "Clipboard helper does not read the canonical prompt at click time.",
    )
    _require(
        "QApplication.clipboard().setText" in clipboard_text,
        "Clipboard helper does not write prompt content to the clipboard.",
    )
    _require("Version: 1.4" in prompt_text, "Canonical prompt is not version 1.4.")
    _require(
        "This file is the canonical owner prompt for the Error Memory AI-assisted intake workflow."
        in prompt_text,
        "Canonical owner declaration is missing from the prompt.",
    )
    _require(
        "live-refresh bridge" in prompt_text,
        "Canonical prompt does not contain the live-refresh delivery contract.",
    )
    _require(
        "error_memory_ai_formulary_startup_canon" in router_text
        and "owner canon" in router_text,
        "Prompt router bridge to the Error Memory owner canon is missing.",
    )

    for path in (tab_path, blueprint_path, clipboard_path):
        py_compile.compile(str(path), doraise=True)

    tab_lines = len(tab_text.splitlines())
    _require(tab_lines <= 500, f"Module size gate failed: {TAB_RELATIVE} has {tab_lines} lines.")

    sys.path.insert(0, str(project_root))
    from kanda_reasoner_app.error_memory_gui._intake_blueprint import (
        error_memory_ai_formulary_canon_path,
        read_error_memory_ai_formulary_canon,
    )

    resolved = error_memory_ai_formulary_canon_path(
        project_root,
        module_file=str(blueprint_path),
    ).resolve(strict=False)
    _require(
        resolved == prompt_path.resolve(strict=False),
        f"Resolver returned wrong canonical prompt path: {resolved}",
    )
    loaded = read_error_memory_ai_formulary_canon(
        project_root,
        module_file=str(blueprint_path),
    )
    _require(loaded == prompt_text, "Prompt reader did not return exact canonical prompt text.")

    return prompt_text, str(prompt_path)


def _validate_gui_click_if_available(project_root: Path, prompt_text: str) -> str:
    try:
        import PySide6  # noqa: F401
    except ModuleNotFoundError:
        return "SKIPPED_NO_PYSIDE6"

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    old_cwd = Path.cwd()
    os.chdir(project_root)
    try:
        from PySide6.QtWidgets import QApplication
        from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab

        app = QApplication.instance() or QApplication([])
        tab = ErrorMemoryTab()
        tab._show_action_done = lambda *args, **kwargs: None

        button = tab.copy_correct_error_delivery_button
        _require(
            button.text() == "Get correct way to send me errors",
            "Runtime button label mismatch.",
        )
        style = button.styleSheet()
        _require("#FF8C00" in style and "font-weight: bold" in style, "Runtime button style mismatch.")

        QApplication.clipboard().clear()
        button.click()
        app.processEvents()
        _require(
            QApplication.clipboard().text() == prompt_text,
            "Runtime button click did not copy exact canonical prompt content.",
        )
        tab.close()
        app.processEvents()
        return "PASS"
    finally:
        os.chdir(old_cwd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve(strict=False)
    _require(project_root.exists() and project_root.is_dir(), f"Project root missing: {project_root}")

    prompt_text, prompt_path = _validate_sources(project_root)
    gui_result = _validate_gui_click_if_available(project_root, prompt_text)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("BUTTON_ORDER: AFTER_SECOND_PROMPT_PATH")
    print("STYLE: #FF8C00_BOLD")
    print("CANON_SOURCE: error_memory_ai_formulary_startup_canon.md")
    print(f"CANON_PATH: {prompt_path}")
    print("CLIPBOARD_PAYLOAD: EXACT_CANON_TEXT")
    print("ROUTER_BRIDGE: PRESENT")
    print("MODULE_SIZE_GATE: PASS")
    print(f"GUI_CLICK_CLIPBOARD_TEST: {gui_result}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
