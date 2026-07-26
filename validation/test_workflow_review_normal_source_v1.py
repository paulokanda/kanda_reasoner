"""Validate Workflow Review normal-source migration v1."""

from __future__ import annotations

import py_compile
from pathlib import Path

FEATURE_ID = "workflow-review-normal-source-v1"
MARKER = "VALIDATION OK: " + FEATURE_ID
ROOT = Path(__file__).resolve().parents[1]

FACADE = ROOT / "kanda_reasoner_app/manage_workflows/manage_workflows_gui.py"
WINDOW = (
    ROOT
    / "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py"
)
LAZY_TABS = ROOT / "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_ascii(path: Path) -> None:
    data = path.read_text(encoding="utf-8")
    bad = [char for char in data if ord(char) > 127]
    require(not bad, "non-ASCII character found in " + path.as_posix())


def assert_normal_source() -> None:
    facade = read(FACADE)
    window = read(WINDOW)

    require("load_payload" not in facade, "facade still loads an encoded payload")
    require("load_payload" not in window, "window still loads an encoded payload")
    require("PAYLOAD_PARTS" not in facade, "facade still exposes payload parts")
    require("PAYLOAD_PARTS" not in window, "window still exposes payload parts")
    require(
        "class WorkflowManagerWindow(QMainWindow):" in window,
        "WorkflowManagerWindow is not readable normal source",
    )
    require(
        "This is the canonical readable source for Workflow Review" in window,
        "normal-source migration note is missing",
    )
    require(
        "encoded backend payload is deprecated" in window,
        "payload deprecation note is missing from the window source",
    )
    require(
        "encoded backend payload\nloader is deprecated" in facade,
        "payload deprecation note is missing from facade",
    )


def assert_layout_contract() -> None:
    window = read(WINDOW)
    lazy = read(LAZY_TABS)

    require('toolbar = QToolBar("Main")' in window, "Main QToolBar is missing")
    require(
        '"workflow_review_run_options_toolbar_widget"' in window,
        "run options toolbar widget object name is missing",
    )
    require(
        "toolbar.addWidget(self._run_options_toolbar_widget)" in window,
        "run options are not placed inside the toolbar",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._mode_combo)" in window,
        "mode dropdown is not in the toolbar run options widget",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._strict_write_checkbox)" in window,
        "confirm-before-write checkbox is not in the toolbar run options widget",
    )
    require(
        "move_project_root_controls_to_layout" in window,
        "Workflow Review project root host-row move hook is missing",
    )
    require(
        "Workflow Review no longer shows script controls" in window,
        "deprecated script selector move hook is not explicit",
    )
    require(
        "move_script_selector_to_layout" in window,
        "compatibility script selector move hook is missing",
    )
    require(
        "_move_tab2_project_root_controls_to_status_row" in lazy,
        "lazy tab host no longer moves Tab 2 project root controls",
    )
    require(
        "_move_tab2_worker_script_selector_to_status_row" not in lazy,
        "lazy tab host still tries to move Tab 2 worker script controls",
    )


def assert_ai_review_preserved() -> None:
    window = read(WINDOW)
    require(
        "create_tab2_ai_review_window_class" in window,
        "Tab 2 AI review class wrapper is not preserved",
    )
    require(
        "WorkflowManagerWindow = _create_tab2_ai_review_window_class" in window,
        "Tab 2 AI review window wrapping is not preserved",
    )


def assert_compiles() -> None:
    for path in (FACADE, WINDOW, LAZY_TABS):
        py_compile.compile(str(path), doraise=True)
        assert_ascii(path)


def _external_show_project_root(project_root: Path) -> Path:
    """Return the external Show Project to AI root for this project."""
    project_name = project_root.name
    if project_root.drive:
        return Path(project_root.drive + "\\") / (project_name + "_show_project_to_AI")
    return project_root.parent / (project_name + "_show_project_to_AI")


def assert_installed_patch_contract() -> None:
    expected_files = [
        "kanda_reasoner_app/manage_workflows/manage_workflows_gui.py",
        "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
        "validation/test_workflow_review_normal_source_v1.py",
    ]
    for relative in expected_files:
        require((ROOT / relative).exists(), "missing expected file: " + relative)

    # KANDA_FREEZE_HINT.json is a patch-ZIP root file, not an installed
    # project-root file. The installer stages it under the external
    # freeze-intake folder, so validation must not require it at ROOT.
    forbidden_root_hint = ROOT / "KANDA_FREEZE_HINT.json"
    require(
        not forbidden_root_hint.exists(),
        "KANDA_FREEZE_HINT.json should not be installed at the project root",
    )


def assert_freeze_hint_staging_contract() -> None:
    show_root = _external_show_project_root(ROOT)
    hint_path = (
        show_root
        / "project_freeze_after_update"
        / "freeze_hint_intake"
        / "workflow-review-normal-source-v1__KANDA_FREEZE_HINT.json"
    )
    if hint_path.exists():
        data = hint_path.read_text(encoding="utf-8")
        require(
            "VALIDATION OK: workflow-review-normal-source-v1" in data,
            "staged freeze hint is missing the validation marker",
        )
        require(
            "STATUS: IN_SYNC" in data,
            "staged freeze hint is missing the sync marker",
        )


def main() -> int:
    assert_compiles()
    assert_normal_source()
    assert_layout_contract()
    assert_ai_review_preserved()
    assert_installed_patch_contract()
    assert_freeze_hint_staging_contract()
    print(MARKER)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
