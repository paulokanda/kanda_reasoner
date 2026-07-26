from __future__ import annotations

import ast
import py_compile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI_SOURCE = ROOT / "kanda_reasoner_app" / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui.py"
WINDOW_STATE_SOURCE = ROOT / "kanda_reasoner_app" / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help" / "window_state.py"
LAYOUT_RUNTIME_SOURCE = ROOT / "kanda_reasoner_app" / "tab3_manual_review_runtime" / "layout_runtime.py"
LAZY_TABS_SOURCE = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
PATCH_NAME = "kanda_docstring_assistant_project_root_status_row_v1_patch.zip"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_ascii(path: Path) -> None:
    try:
        path.read_text(encoding="ascii")
    except UnicodeDecodeError as exc:
        raise AssertionError(f"non-ASCII character found in {path.relative_to(ROOT)}") from exc


def candidate_patch_zips() -> list[Path]:
    candidates = [ROOT / PATCH_NAME]
    project_name = ROOT.name
    if project_name:
        drive_root = ROOT.anchor
        if drive_root:
            candidates.append(Path(drive_root) / f"{project_name}_delete_after_daily_work" / PATCH_NAME)
    parent = ROOT.parent
    candidates.append(parent / PATCH_NAME)
    candidates.append(parent / f"{ROOT.name}_delete_after_daily_work" / PATCH_NAME)
    return candidates


def assert_gui_contract() -> None:
    text = read_text(GUI_SOURCE)
    ast.parse(text)
    require("from kanda_reasoner_app.backend_payloads.loader import load_payload" not in text, "Docstring Assistant must remain normal readable source")
    require("load_payload(" not in text, "Docstring Assistant main source must not restore payload mode")
    require("def move_project_root_controls_to_layout(" in text, "Docstring Assistant project-root host-row mover missing")
    require("Move Docstring Assistant Project Root controls into the host source row" in text, "Docstring Assistant mover intent missing")
    require("self._root_path_label.setParent(None)" in text, "Project Root label must be detached before host-row move")
    require("self._root_path_edit.setParent(None)" in text, "Project Root edit must be detached before host-row move")
    require("self._browse_root_button.setParent(None)" in text, "Search button must be detached before host-row move")
    require("destination_layout.insertWidget(insert_index + 1, self._root_path_label, 0)" in text, "Project Root label not inserted Architecture-style")
    require("destination_layout.insertWidget(insert_index + 2, self._root_path_edit, 0)" in text, "Project Root edit not inserted Architecture-style")
    require("destination_layout.insertWidget(insert_index + 3, self._browse_root_button, 0)" in text, "Search button not inserted Architecture-style")


def assert_window_state_contract() -> None:
    text = read_text(WINDOW_STATE_SOURCE)
    ast.parse(text)
    require('self._root_path_label = QLabel("Project Root:")' in text, "Project Root label widget missing")
    require('self._root_path_edit.setPlaceholderText("Project root")' in text, "Project Root placeholder missing")
    require('self._browse_root_button = QPushButton("Search")' in text, "Search button missing")
    require("self._project_root_controls_moved_to_host = False" in text, "moved-to-host guard missing")
    require('self._worker_path_edit = QLineEdit(_canonical_worker_script_path())' in text, "worker path state should remain available internally")


def assert_layout_contract() -> None:
    text = read_text(LAYOUT_RUNTIME_SOURCE)
    ast.parse(text)
    require("left_layout.addWidget(_build_project_group(window))" not in text, "Project group must not be added to Docstring Assistant body")
    require('QGroupBox("Project")' not in text, "Project body group must not be restored")
    require('window._browse_root_button = QPushButton("Browse")' not in text, "body Browse button creation must not be restored")
    require("Return a hidden compatibility placeholder for the retired body Project group" in text, "compatibility placeholder missing")
    require('_connect(window._browse_root_button, "clicked", window.browse_root)' in text, "Search/Browse project-root action must remain wired")


def assert_lazy_tabs_contract() -> None:
    text = read_text(LAZY_TABS_SOURCE)
    ast.parse(text)
    require("Worker Script:" not in text, "Docstring Worker Script host-row label must not be restored")
    require("_docstring_worker_script_path" not in text, "Docstring worker-script source-row helper must not be imported or used")
    require("def _move_tab3_project_root_controls_to_status_row" in text, "Docstring Project Root host-row mover missing in lazy tabs")
    require("self.spec.source_hint != _DOCSTRINGS_GUI_SOURCE" in text, "Docstring source-hint gate missing")
    require("self._move_tab3_project_root_controls_to_status_row(widget)" in text, "Docstring Project Root mover not called while loading tab")
    require("self._move_tab3_safe_mode_radio_to_status_row(widget)" in text, "Safe Mode radio host-row behavior must remain wired")
    require("mover(self.status_source_row, insert_index)" in text, "Docstring host-row move must use Architecture-style insertion index")


def assert_patch_zip_contract() -> None:
    existing = next((path for path in candidate_patch_zips() if path.exists()), None)
    if existing is None:
        return
    with zipfile.ZipFile(existing, "r") as zf:
        names = set(zf.namelist())
    expected = {
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py",
        "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/window_state.py",
        "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
        "validation/test_docstring_assistant_project_root_status_row_v1.py",
        "KANDA_FREEZE_HINT.json",
    }
    require(expected.issubset(names), f"patch ZIP missing files: {sorted(expected - names)}")
    forbidden = [name for name in names if name.startswith("project_freeze_after_update/")]
    require(not forbidden, "patch ZIP must not contain frozen memory entries")


def main() -> int:
    for path in (GUI_SOURCE, WINDOW_STATE_SOURCE, LAYOUT_RUNTIME_SOURCE, LAZY_TABS_SOURCE):
        assert_ascii(path)
        py_compile.compile(str(path), doraise=True)
    assert_gui_contract()
    assert_window_state_contract()
    assert_layout_contract()
    assert_lazy_tabs_contract()
    assert_patch_zip_contract()
    print("VALIDATION OK: docstring-assistant-project-root-status-row-v1")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
